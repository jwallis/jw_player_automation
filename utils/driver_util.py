"""Device/OS-level manipulation - bezel swipes, device settings, etc.
Not app-level (that's AppUtil)."""

from __future__ import annotations

from driver.driver_wrapper import DriverWrapper

_TEST_SET_ROOT_FOLDER_ACTION = "com.joshuawallis.jwplayer.TEST_SET_ROOT_FOLDER"


class DriverUtil:
    def __init__(self, driver_wrapper: DriverWrapper):
        self.driver_wrapper = driver_wrapper

    def press_back(self) -> None:
        self.driver_wrapper.driver.back()

    def open_notifications(self) -> None:
        self.driver_wrapper.driver.open_notifications()

    def set_root_folder_via_backdoor(self, path: str) -> None:
        """Debug-build-only automation backdoor (see jw_player's
        debug/TestSetRootFolderReceiver.kt) - sets the root folder directly,
        bypassing the real Storage Access Framework picker, which
        test_cases.md already marks not automatable."""
        self.driver_wrapper.shell(
            "am",
            [
                "broadcast",
                "-a",
                _TEST_SET_ROOT_FOLDER_ACTION,
                "--es",
                "path",
                path,
                "--receiver-include-background",
            ],
        )
