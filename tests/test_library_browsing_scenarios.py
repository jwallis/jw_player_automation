"""Real Appium test scenarios for the "Library Browsing & Navigation" epic
- see docs/qa/test_cases.md. One function per test case, built on the
service layer only (never raw driver/page calls) - see
unittests/test_unit_tests.py's own docstring for why these live apart from
framework plumbing checks.
"""

from __future__ import annotations

from driver.driver_wrapper import DriverWrapper
from pages.library_page import LibraryPage
from services.library_service import LibraryService


def test_PLAYER_TC_044_empty_library_placeholder_invites_to_get_started(driver_wrapper: DriverWrapper):
    library_page = LibraryPage(driver_wrapper)
    service = LibraryService(library_page)

    service.validate_empty_library_message_shown()
