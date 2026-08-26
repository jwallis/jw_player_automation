"""Real Appium test scenarios for the "Library Browsing & Navigation" epic
- see docs/qa/test_cases.md. One function per test case, built on the
service layer only (never raw driver/page calls) - see
unittests/test_unit_tests.py's own docstring for why these live apart from
framework plumbing checks.
"""

from __future__ import annotations

from config.config import load_config
from driver.driver_factory import DriverFactory
from pages.library_page import LibraryPage
from services.library_service import LibraryService
from utils.app_util import AppUtil


def test_PLAYER_TC_044_empty_library_placeholder_invites_listening_to_music():
    config = load_config()
    driver_wrapper = DriverFactory.create(config)
    try:
        # Cycle through one throwaway restart before relying on anything
        # shown on screen - see AppUtil.restart_app.
        app_util = AppUtil(driver_wrapper, config)
        app_util.restart_app()

        library_page = LibraryPage(driver_wrapper)
        service = LibraryService(library_page)

        service.validate_empty_library_message_shown()
    finally:
        DriverFactory.quit(driver_wrapper)
