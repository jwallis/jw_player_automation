"""Android's native Storage Access Framework folder picker
(com.google.android.documentsui) - not our app, so there are no testTags
here. Locators are raw UiAutomator selector expressions against the real
system UI, confirmed live against a real picker session (see
docs/ai/summary.md): the breadcrumb's first entry is always the true
storage root, folder rows are android:id/title matched by display text,
and the "use this folder" / "allow" buttons are matched by their text
(case-insensitively - confirmed live that real Device Farm hardware
renders "Use this folder" where a local emulator rendered "USE THIS
FOLDER", so an exact-case match is not portable across devices) since
their resource-ids (android:id/button1) are reused across unrelated
dialogs in the same flow.
"""

from __future__ import annotations

from driver.driver_wrapper import DriverWrapper


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


class SystemFolderPickerPage:
    ROOT_BREADCRUMB_SELECTOR = (
        'new UiSelector().resourceId("com.google.android.documentsui:id/breadcrumb_text").instance(0)'
    )
    USE_THIS_FOLDER_SELECTOR = 'new UiSelector().textMatches("(?i)use this folder")'
    ALLOW_SELECTOR = 'new UiSelector().textMatches("(?i)allow")'

    def __init__(self, driver_wrapper: DriverWrapper):
        self.driver_wrapper = driver_wrapper

    @staticmethod
    def _folder_row_selector(name: str) -> str:
        return f'new UiSelector().resourceId("android:id/title").text("{_escape(name)}")'

    def navigate_to_root(self) -> None:
        self.driver_wrapper.tap_uiautomator(self.ROOT_BREADCRUMB_SELECTOR, locator="picker root breadcrumb")

    def open_folder(self, name: str) -> None:
        self.driver_wrapper.tap_uiautomator(self._folder_row_selector(name), locator=f"picker folder row {name!r}")

    def use_this_folder(self) -> None:
        self.driver_wrapper.tap_uiautomator(self.USE_THIS_FOLDER_SELECTOR, locator="USE THIS FOLDER button")

    def allow_access(self) -> None:
        self.driver_wrapper.tap_uiautomator(self.ALLOW_SELECTOR, locator="ALLOW button")
