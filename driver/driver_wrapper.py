"""Driver/Appium wrapper layer.

Owns raw interaction (tap, find, gestures) - see docs/standards/standards.md
concept 1. Pages hold a reference to an instance of this and call through it;
they never touch the raw Appium driver or a locator strategy directly.

Locates by resource-id, matching jw_player's testTag values exposed via
Jetpack Compose's testTagsAsResourceId (enabled once, at the root, in
MainActivity) - bare testTag strings are matched as-is, with no
package-name prefix needed. Requires UiAutomator2 driver >= 8.4.0.
Deliberately not accessibility id / contentDescription - that's still there
for TalkBack, but it's dynamic (e.g. "Now playing: <title>") and never meant
to be a stable automation hook.

Locates via a raw UiSelector().resourceId(...) query
(AppiumBy.ANDROID_UIAUTOMATOR), not AppiumBy.ID / By.ID - confirmed live,
reproduced against both a local emulator and real Device Farm hardware,
that AppiumBy.ID never matches any of these bare (unprefixed) Compose
testTag resource-ids on this UiAutomator2 driver version, even though the
exact same string is plainly present in driver.page_source and a raw
UiSelector resourceId() query matches it immediately. Every real-device
ElementNotFoundError this framework has ever hit traces back to this - not
a timing or rendering issue.
"""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from exceptions.automation_errors import ElementNotFoundError


def _resource_id_selector(test_tag: str) -> str:
    escaped = test_tag.replace("\\", "\\\\").replace('"', '\\"')
    return f'new UiSelector().resourceId("{escaped}")'


class DriverWrapper:
    def __init__(self, driver: WebDriver, timeout_seconds: int):
        self.driver = driver
        self.timeout_seconds = timeout_seconds

    def find_by(self, test_tag: str) -> WebElement:
        return self.find_by_uiautomator(_resource_id_selector(test_tag), locator=test_tag)

    def find_by_uiautomator(self, selector: str, locator: str | None = None) -> WebElement:
        """Locate by a raw UiAutomator selector expression (e.g.
        'new UiSelector().text("...")') - for elements outside this app
        (system UI, other apps) that have no testTag/resource-id of ours to
        match on. `locator` is only used to label the error if not found;
        defaults to the selector itself."""
        try:
            return WebDriverWait(self.driver, self.timeout_seconds).until(
                EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, selector))
            )
        except Exception as e:
            try:
                page_source = self.driver.page_source
            except Exception:
                page_source = None
            raise ElementNotFoundError(locator or selector, page_source) from e

    def is_present(self, test_tag: str) -> bool:
        try:
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, _resource_id_selector(test_tag))
            return True
        except Exception:
            return False

    def tap(self, test_tag: str) -> None:
        self.find_by(test_tag).click()

    def tap_uiautomator(self, selector: str, locator: str | None = None) -> None:
        self.find_by_uiautomator(selector, locator).click()

    def press_and_hold(self, test_tag: str, hold_seconds: float) -> None:
        element = self.find_by(test_tag)
        self.driver.execute_script(
            "mobile: longClickGesture",
            {"elementId": element.id, "duration": int(hold_seconds * 1000)},
        )

    def shell(self, command: str, args: list[str] | None = None) -> str:
        result = self.driver.execute_script("mobile: shell", {"command": command, "args": args or []})
        return str(result)
