import psutil
import time
from datetime import datetime
from typing import Optional, Dict, List
import platform

# Windows-specific imports
if platform.system() == "Windows":
    try:
        import win32gui
        import win32process
        WINDOWS_AVAILABLE = True
    except ImportError:
        WINDOWS_AVAILABLE = False
else:
    WINDOWS_AVAILABLE = False


class WindowMonitor:
    """
    Monitor active windows and applications during a session.
    """

    def __init__(self):
        self.current_window: Optional[Dict] = None
        self.window_start_time: Optional[datetime] = None

    def get_active_window(self) -> Optional[Dict]:
        """
        Get information about the currently active window.

        Returns:
            Dictionary with window information or None
        """
        if platform.system() == "Windows" and WINDOWS_AVAILABLE:
            return self._get_active_window_windows()
        elif platform.system() == "Darwin":
            return self._get_active_window_macos()
        elif platform.system() == "Linux":
            return self._get_active_window_linux()
        else:
            return None

    def _get_active_window_windows(self) -> Optional[Dict]:
        """Get active window on Windows"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return None

            # Get window title
            window_title = win32gui.GetWindowText(hwnd)

            # Get process ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            # Get process information
            try:
                process = psutil.Process(pid)
                process_name = process.name()
                process_exe = process.exe()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Unknown"
                process_exe = None

            # Get window position
            try:
                rect = win32gui.GetWindowRect(hwnd)
                x, y, width, height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
            except:
                x, y, width, height = 0, 0, 0, 0

            return {
                "window_title": window_title,
                "process_name": process_name,
                "process_id": pid,
                "process_exe": process_exe,
                "x_position": x,
                "y_position": y,
                "window_width": width,
                "window_height": height,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            print(f"Error getting active window: {e}")
            return None

    def _get_active_window_macos(self) -> Optional[Dict]:
        """Get active window on macOS (placeholder)"""
        # TODO: Implement using Quartz/AppKit
        return None

    def _get_active_window_linux(self) -> Optional[Dict]:
        """Get active window on Linux (placeholder)"""
        # TODO: Implement using python-xlib
        return None

    def track_window_change(self) -> Optional[Dict]:
        """
        Track when the active window changes.

        Returns:
            Window event if window changed, None otherwise
        """
        current = self.get_active_window()

        if current is None:
            return None

        # Check if window changed
        if self.current_window is None:
            # First window
            self.current_window = current
            self.window_start_time = datetime.utcnow()
            return None

        # Check if window title or process changed
        if (
            current["window_title"] != self.current_window.get("window_title")
            or current["process_name"] != self.current_window.get("process_name")
        ):
            # Window changed
            end_time = datetime.utcnow()
            duration = (end_time - self.window_start_time).total_seconds()

            event = {
                **self.current_window,
                "start_time": self.window_start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": int(duration),
            }

            # Update current window
            self.current_window = current
            self.window_start_time = end_time

            return event

        return None

    def get_running_processes(self) -> List[Dict]:
        """
        Get list of all running processes.

        Returns:
            List of process dictionaries
        """
        processes = []
        for proc in psutil.process_iter(["pid", "name", "exe", "create_time"]):
            try:
                info = proc.info
                processes.append({
                    "pid": info["pid"],
                    "name": info["name"],
                    "exe": info["exe"],
                    "create_time": datetime.fromtimestamp(info["create_time"]).isoformat() if info["create_time"] else None,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return processes

    def is_browser(self, process_name: str) -> bool:
        """Check if process is a browser"""
        browser_names = [
            "chrome.exe", "firefox.exe", "msedge.exe", "safari", "brave.exe",
            "opera.exe", "vivaldi.exe", "iexplore.exe", "chrome", "firefox",
        ]
        return any(browser in process_name.lower() for browser in browser_names)

    def is_ide(self, process_name: str) -> bool:
        """Check if process is an IDE"""
        ide_names = [
            "code.exe", "pycharm", "idea", "eclipse", "netbeans", "atom",
            "sublime", "notepad++", "vim", "emacs", "vscode", "code",
        ]
        return any(ide in process_name.lower() for ide in ide_names)

    def categorize_window(self, window_info: Dict) -> str:
        """
        Categorize the window based on process name.

        Returns:
            Category string (browser, ide, office, etc.)
        """
        process_name = window_info.get("process_name", "").lower()

        if self.is_browser(process_name):
            return "browser"
        elif self.is_ide(process_name):
            return "ide"
        elif any(app in process_name for app in ["word", "excel", "powerpoint", "outlook"]):
            return "office"
        elif any(app in process_name for app in ["notepad", "wordpad", "write"]):
            return "text_editor"
        elif any(app in process_name for app in ["explorer", "finder"]):
            return "file_manager"
        else:
            return "other"


class WindowMonitorScheduler:
    """
    Scheduler for periodic window monitoring.
    """

    def __init__(self, monitor: WindowMonitor, check_interval: int = 1):
        self.monitor = monitor
        self.check_interval = check_interval
        self.is_running = False

    async def start(self, callback=None):
        """
        Start monitoring window changes.

        Args:
            callback: Optional async callback function(window_event)
        """
        import asyncio

        self.is_running = True

        while self.is_running:
            try:
                event = self.monitor.track_window_change()
                if event and callback:
                    await callback(event)
            except Exception as e:
                print(f"Error monitoring window: {e}")

            await asyncio.sleep(self.check_interval)

    def stop(self):
        """Stop window monitoring"""
        self.is_running = False
