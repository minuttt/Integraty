import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, Callable, List
from pathlib import Path
import uuid
from enum import Enum

from integraty.core.screen_capture import ScreenCaptureEngine, ScreenshotScheduler
from integraty.core.window_monitor import WindowMonitor, WindowMonitorScheduler


class SessionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ERROR = "error"


class MonitoringSession:
    """
    Manages a single monitoring session including screen capture,
    window monitoring, and session lifecycle.
    """

    def __init__(
        self,
        session_id: str,
        user_id: str,
        config: Dict,
        data_dir: Path,
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.config = config
        self.data_dir = data_dir

        self.status = SessionStatus.PENDING
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

        # Initialize monitoring components
        self.screen_capture = ScreenCaptureEngine(
            output_dir=data_dir / "screenshots",
            quality=config.get("screenshot_quality", 85),
        )

        self.screenshot_scheduler = ScreenshotScheduler(
            capture_engine=self.screen_capture,
            interval=config.get("screenshot_interval", 30),
        )

        self.window_monitor = WindowMonitor()
        self.window_monitor_scheduler = WindowMonitorScheduler(
            monitor=self.window_monitor,
            check_interval=1,
        )

        # Event callbacks
        self.on_screenshot: Optional[Callable] = None
        self.on_window_change: Optional[Callable] = None
        self.on_status_change: Optional[Callable] = None

        # Statistics
        self.stats = {
            "screenshots_captured": 0,
            "window_changes": 0,
            "detections": 0,
        }

    async def start(self):
        """Start the monitoring session"""
        if self.status != SessionStatus.PENDING:
            raise ValueError(f"Cannot start session in status: {self.status}")

        self.status = SessionStatus.ACTIVE
        self.start_time = datetime.utcnow()

        if self.on_status_change:
            await self.on_status_change(self.status)

        # Start screenshot capture
        await self.screenshot_scheduler.start(
            session_id=self.session_id,
            callback=self._handle_screenshot,
        )

        # Start window monitoring
        asyncio.create_task(
            self.window_monitor_scheduler.start(callback=self._handle_window_change)
        )

    async def pause(self):
        """Pause the monitoring session"""
        if self.status != SessionStatus.ACTIVE:
            raise ValueError(f"Cannot pause session in status: {self.status}")

        self.status = SessionStatus.PAUSED
        self.screenshot_scheduler.pause()

        if self.on_status_change:
            await self.on_status_change(self.status)

    async def resume(self):
        """Resume a paused session"""
        if self.status != SessionStatus.PAUSED:
            raise ValueError(f"Cannot resume session in status: {self.status}")

        self.status = SessionStatus.ACTIVE
        self.screenshot_scheduler.resume()

        if self.on_status_change:
            await self.on_status_change(self.status)

    async def complete(self):
        """Complete the monitoring session"""
        if self.status not in [SessionStatus.ACTIVE, SessionStatus.PAUSED]:
            raise ValueError(f"Cannot complete session in status: {self.status}")

        self.status = SessionStatus.COMPLETED
        self.end_time = datetime.utcnow()

        # Stop monitoring
        await self.screenshot_scheduler.stop()
        self.window_monitor_scheduler.stop()

        # Cleanup
        self.screen_capture.close()

        if self.on_status_change:
            await self.on_status_change(self.status)

    async def cancel(self):
        """Cancel the monitoring session"""
        self.status = SessionStatus.CANCELLED
        self.end_time = datetime.utcnow()

        await self.screenshot_scheduler.stop()
        self.window_monitor_scheduler.stop()
        self.screen_capture.close()

        if self.on_status_change:
            await self.on_status_change(self.status)

    async def _handle_screenshot(self, full_path: Path, thumbnail_path: Path, metadata: Dict):
        """Internal callback for screenshot capture"""
        self.stats["screenshots_captured"] += 1

        if self.on_screenshot:
            await self.on_screenshot(full_path, thumbnail_path, metadata)

    async def _handle_window_change(self, window_event: Dict):
        """Internal callback for window changes"""
        self.stats["window_changes"] += 1

        if self.on_window_change:
            await self.on_window_change(window_event)

    def get_duration(self) -> Optional[timedelta]:
        """Get session duration"""
        if self.start_time is None:
            return None

        end = self.end_time or datetime.utcnow()
        return end - self.start_time

    def get_stats(self) -> Dict:
        """Get session statistics"""
        duration = self.get_duration()
        return {
            **self.stats,
            "duration_seconds": int(duration.total_seconds()) if duration else 0,
            "status": self.status,
        }


class SessionManager:
    """
    Manages multiple monitoring sessions.
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.sessions: Dict[str, MonitoringSession] = {}

    def create_session(
        self,
        user_id: str,
        config: Dict,
        session_id: Optional[str] = None,
    ) -> MonitoringSession:
        """
        Create a new monitoring session.

        Args:
            user_id: User ID
            config: Session configuration
            session_id: Optional custom session ID

        Returns:
            MonitoringSession instance
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        if session_id in self.sessions:
            raise ValueError(f"Session {session_id} already exists")

        session = MonitoringSession(
            session_id=session_id,
            user_id=user_id,
            config=config,
            data_dir=self.data_dir,
        )

        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[MonitoringSession]:
        """Get a session by ID"""
        return self.sessions.get(session_id)

    def get_active_sessions(self) -> List[MonitoringSession]:
        """Get all active sessions"""
        return [
            session
            for session in self.sessions.values()
            if session.status == SessionStatus.ACTIVE
        ]

    async def stop_all_sessions(self):
        """Stop all active sessions"""
        tasks = []
        for session in self.get_active_sessions():
            tasks.append(session.complete())

        if tasks:
            await asyncio.gather(*tasks)

    def remove_session(self, session_id: str):
        """Remove a session from the manager"""
        if session_id in self.sessions:
            del self.sessions[session_id]
