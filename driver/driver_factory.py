"""Driver/Appium wrapper layer - session creation.

Builds the raw Appium session and hands back a DriverWrapper, not the raw
driver - nothing above this layer should ever hold a raw webdriver.Remote.
"""

from __future__ import annotations

from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.config import AutomationConfig
from driver.driver_wrapper import DriverWrapper


class DriverFactory:
    @staticmethod
    def create(config: AutomationConfig) -> DriverWrapper:
        options = UiAutomator2Options().load_capabilities(config.capabilities)
        raw_driver = webdriver.Remote(config.appium_server_url, options=options)
        raw_driver.implicitly_wait(config.implicit_wait_seconds)
        return DriverWrapper(raw_driver, config.implicit_wait_seconds)

    @staticmethod
    def quit(driver_wrapper: DriverWrapper) -> None:
        driver_wrapper.driver.quit()
