"""App-level manipulation - background, launch, quit, current state.
Not device/OS-level (that's DriverUtil)."""

from __future__ import annotations

import time

from config.config import AutomationConfig
from driver.driver_wrapper import DriverWrapper


class AppUtil:
    def __init__(self, driver_wrapper: DriverWrapper, config: AutomationConfig):
        self.driver_wrapper = driver_wrapper
        self.config = config

    def launch_app(self) -> None:
        self.driver_wrapper.driver.activate_app(self.config.app_package)

    def background_app(self, seconds: int) -> None:
        self.driver_wrapper.driver.background_app(seconds)

    def foreground_app(self) -> None:
        self.driver_wrapper.driver.activate_app(self.config.app_package)

    def quit_app(self) -> None:
        self.driver_wrapper.driver.terminate_app(self.config.app_package)

    def restart_app(self, settle_seconds: int = 3) -> None:
        """Force-stop and relaunch, pausing before/after each step. Real
        Device Farm hardware has shown a first-launch render race (app
        appears but its content doesn't draw until a later launch) that
        these pauses work around."""
        time.sleep(settle_seconds)
        self.quit_app()
        time.sleep(settle_seconds)
        self.launch_app()
        time.sleep(settle_seconds)

    def get_current_activity(self) -> str:
        return self.driver_wrapper.driver.current_activity
