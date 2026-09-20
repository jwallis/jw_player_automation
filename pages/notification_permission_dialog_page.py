"""Android's native runtime-permission dialog (com.android.permissioncontroller) -
not our app, so there are no testTags here. The "Allow" button is matched by
text (case-insensitively), same reasoning as system_folder_picker_page.py -
this is a standard system dialog whose resource-ids can vary across OEM
permission-controller skins."""

from __future__ import annotations

from driver.driver_wrapper import DriverWrapper


class NotificationPermissionDialogPage:
    ALLOW_SELECTOR = 'new UiSelector().textMatches("(?i)allow")'

    def __init__(self, driver_wrapper: DriverWrapper):
        self.driver_wrapper = driver_wrapper

    def tap_allow(self) -> None:
        self.driver_wrapper.tap_uiautomator(self.ALLOW_SELECTOR, locator="notification permission ALLOW button")
