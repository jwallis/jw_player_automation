"""Driver/Appium wrapper layer.

Owns raw interaction (tap, find, gestures) - see docs/standards/standards.md
concept 1. Pages hold a reference to an instance of this and call through it;
they never touch the raw Appium driver or a locator strategy directly.

Locates by resource-id (AppiumBy.ID), matching jw_player's testTag values
exposed via Jetpack Compose's testTagsAsResourceId (enabled once, at the
root, in MainActivity) - bare testTag strings are matched as-is, with no
package-name prefix needed. Requires UiAutomator2 driver >= 8.4.0.
Deliberately not accessibility id / contentDescription - that's still there
for TalkBack, but it's dynamic (e.g. "Now playing: <title>") and never meant
to be a stable automation hook.
"""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from exceptions.automation_errors import ElementNotFoundError


class DriverWrapper:
    def __init__(self, driver: WebDriver, timeout_seconds: int):
        self.driver = driver
        self.timeout_seconds = timeout_seconds

    def find_by(self, test_tag: str) -> WebElement:
        try:
            return WebDriverWait(self.driver, self.timeout_seconds).until(
                EC.presence_of_element_located((AppiumBy.ID, test_tag))
            )
        except Exception as e:
            raise ElementNotFoundError(test_tag) from e

    def is_present(self, test_tag: str) -> bool:
        try:
            self.driver.find_element(AppiumBy.ID, test_tag)
            return True
        except Exception:
            return False

    def tap(self, test_tag: str) -> None:
        self.find_by(test_tag).click()

    def press_and_hold(self, test_tag: str, hold_seconds: float) -> None:
        element = self.find_by(test_tag)
        self.driver.execute_script(
            "mobile: longClickGesture",
            {"elementId": element.id, "duration": int(hold_seconds * 1000)},
        )
