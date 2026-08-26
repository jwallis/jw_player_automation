"""Shared fixture for real-device scenario tests - every real Device Farm
job runs multiple scenario tests against one shared app install, so each
test gets a genuinely fresh install here rather than relying on execution
order or leftover state from whatever ran before it."""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

from config.config import load_config
from driver.driver_factory import DriverFactory
from driver.driver_wrapper import DriverWrapper
from utils.app_util import AppUtil


@pytest.fixture
def driver_wrapper() -> Iterator[DriverWrapper]:
    config = load_config()
    wrapper = DriverFactory.create(config)
    try:
        app_util = AppUtil(wrapper, config)
        app_util.reinstall_app(os.environ["DEVICEFARM_APP_PATH"])
        app_util.launch_app()
        # Cycle through one throwaway restart before relying on anything
        # shown on screen - see AppUtil.restart_app.
        app_util.restart_app()
        yield wrapper
    finally:
        DriverFactory.quit(wrapper)
