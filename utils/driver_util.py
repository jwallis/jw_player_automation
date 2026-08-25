"""Device/OS-level manipulation - bezel swipes, device settings, etc.
Not app-level (that's AppUtil). Stubbed until a real device/emulator is in
the loop (Phase 7) - nothing in jw_player's own test cases needs this yet."""

from __future__ import annotations

from driver.driver_wrapper import DriverWrapper


class DriverUtil:
    def __init__(self, driver_wrapper: DriverWrapper):
        self.driver_wrapper = driver_wrapper

    def press_back(self) -> None:
        self.driver_wrapper.driver.back()

    def open_notifications(self) -> None:
        self.driver_wrapper.driver.open_notifications()
