"""Framework self-check, not an app test scenario - proves the layers
(config -> driver wrapper -> pages -> services) actually wire together
correctly, without needing a real device/Appium server. Real Appium test
scenarios (the "test script layer" - one function per docs/qa/test_cases.md
case) are separate files in this same directory once Phase 6 generates them;
this file exists to keep them apart from framework plumbing checks.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from config.config import load_config
from pages.library_page import LibraryPage
from pages.settings_page import SettingsPage
from services.playback_service import PlaybackService
from services.settings_service import SettingsService
from exceptions.automation_errors import ValidationError


def test_config_loads_and_merges_environment():
    config = load_config()
    assert config.appium_server_url == "http://127.0.0.1:4723"
    assert config.app_package == "com.joshuawallis.jwplayer"
    assert config.capabilities["appium:appPackage"] == "com.joshuawallis.jwplayer"


def test_playback_service_reports_paused_state():
    driver_wrapper = MagicMock()
    driver_wrapper.is_present.return_value = False  # pause_button not present -> not playing
    library_page = LibraryPage(driver_wrapper)
    service = PlaybackService(library_page)

    assert library_page.is_playing() is False
    assert service is not None  # wiring didn't blow up constructing it


def test_playback_service_validates_song_playing():
    driver_wrapper = MagicMock()
    driver_wrapper.is_present.return_value = True  # pause_button present -> playing
    driver_wrapper.find_by.return_value.text = "seek_test"
    library_page = LibraryPage(driver_wrapper)
    service = PlaybackService(library_page)

    service.validate_song_is_playing("seek_test")  # should not raise


def test_playback_service_validation_fails_when_not_playing():
    driver_wrapper = MagicMock()
    driver_wrapper.is_present.return_value = False
    library_page = LibraryPage(driver_wrapper)
    service = PlaybackService(library_page)

    try:
        service.validate_song_is_playing("seek_test")
        assert False, "expected ValidationError"
    except ValidationError:
        pass


def test_settings_service_reports_white_noise_state():
    driver_wrapper = MagicMock()
    driver_wrapper.is_present.return_value = True  # white_noise_pause_button present -> playing
    settings_page = SettingsPage(driver_wrapper)
    service = SettingsService(settings_page)

    service.validate_white_noise_is_playing()  # should not raise
