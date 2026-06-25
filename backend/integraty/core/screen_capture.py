import mss
import mss.tools
from PIL import Image
from pathlib import Path
from datetime import datetime
import hashlib
import asyncio
from typing import Tuple, Optional
import io


class ScreenCaptureEngine:
    """
    Screen capture engine for taking periodic screenshots during monitoring sessions.
    """

    def __init__(self, output_dir: Path, quality: int = 85):
        self.output_dir = output_dir
        self.quality = quality
        self.sct = mss.mss()

    def capture_screenshot(self, session_id: str, monitor_index: int = 0) -> Tuple[Path, Path, dict]:
        """
        Capture a screenshot and save it.

        Args:
            session_id: Session UUID
            monitor_index: Monitor to capture (0 = all monitors)

        Returns:
            Tuple of (full_path, thumbnail_path, metadata)
        """
        # Create session directory
        session_dir = self.output_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        thumbnail_dir = session_dir / "thumbnails"
        thumbnail_dir.mkdir(exist_ok=True)

        # Capture screenshot
        timestamp = datetime.utcnow()
        monitor = self.sct.monitors[monitor_index]

        screenshot = self.sct.grab(monitor)

        # Convert to PIL Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

        # Generate filename
        filename = f"screenshot_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.png"
        full_path = session_dir / filename
        thumbnail_path = thumbnail_dir / filename

        # Save full resolution
        img.save(full_path, "PNG", optimize=True, quality=self.quality)

        # Create thumbnail (400px width)
        thumbnail = img.copy()
        thumbnail.thumbnail((400, 400), Image.Resampling.LANCZOS)
        thumbnail.save(thumbnail_path, "JPEG", optimize=True, quality=70)

        # Calculate hash
        with open(full_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # Get file size
        file_size = full_path.stat().st_size

        metadata = {
            "timestamp": timestamp.isoformat(),
            "width": screenshot.width,
            "height": screenshot.height,
            "file_size": file_size,
            "sha256_hash": file_hash,
            "monitor_index": monitor_index,
            "monitor_count": len(self.sct.monitors) - 1,  # -1 for "all monitors"
        }

        return full_path, thumbnail_path, metadata

    async def capture_screenshot_async(self, session_id: str, monitor_index: int = 0) -> Tuple[Path, Path, dict]:
        """Async version of capture_screenshot"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.capture_screenshot, session_id, monitor_index)

    def get_monitor_info(self) -> list:
        """Get information about all available monitors"""
        monitors = []
        for i, monitor in enumerate(self.sct.monitors[1:], 1):  # Skip "all monitors"
            monitors.append({
                "index": i,
                "left": monitor["left"],
                "top": monitor["top"],
                "width": monitor["width"],
                "height": monitor["height"],
            })
        return monitors

    def close(self):
        """Clean up resources"""
        self.sct.close()


class ScreenshotScheduler:
    """
    Scheduler for periodic screenshot capture during a monitoring session.
    """

    def __init__(self, capture_engine: ScreenCaptureEngine, interval: int = 30):
        self.capture_engine = capture_engine
        self.interval = interval
        self.is_running = False
        self.task: Optional[asyncio.Task] = None

    async def start(self, session_id: str, callback=None):
        """
        Start periodic screenshot capture.

        Args:
            session_id: Session UUID
            callback: Optional async callback function(path, thumbnail, metadata)
        """
        self.is_running = True

        async def capture_loop():
            while self.is_running:
                try:
                    full_path, thumbnail_path, metadata = await self.capture_engine.capture_screenshot_async(
                        session_id
                    )

                    if callback:
                        await callback(full_path, thumbnail_path, metadata)

                except Exception as e:
                    print(f"Error capturing screenshot: {e}")

                await asyncio.sleep(self.interval)

        self.task = asyncio.create_task(capture_loop())

    async def stop(self):
        """Stop screenshot capture"""
        self.is_running = False
        if self.task:
            await self.task

    def pause(self):
        """Pause screenshot capture"""
        self.is_running = False

    def resume(self):
        """Resume screenshot capture"""
        self.is_running = True
