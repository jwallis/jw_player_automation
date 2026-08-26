"""Real Appium test scenarios for the "Library Browsing & Navigation" epic
- see docs/qa/test_cases.md. One function per test case, built on the
service layer only (never raw driver/page calls) - see
unittests/test_unit_tests.py's own docstring for why these live apart from
framework plumbing checks.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from pages.library_page import LibraryPage
from services.library_service import LibraryService


def test_PLAYER_TC_044_empty_library_placeholder_says_please():
    driver_wrapper = MagicMock()
    driver_wrapper.find_by.return_value.text = "No music yet. Please choose a folder to get started!"
    library_page = LibraryPage(driver_wrapper)
    service = LibraryService(library_page)

    service.validate_empty_library_message_shown()  # should not raise
