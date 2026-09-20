"""Real Appium test scenarios for the "Library Playback" epic - see
docs/qa/test_cases.md. One function per test case, built on the service
layer only (never raw driver/page calls) - see unittests/test_unit_tests.py's
own docstring for why these live apart from framework plumbing checks.
"""

from __future__ import annotations

from driver.driver_wrapper import DriverWrapper
from pages.library_page import LibraryPage
from pages.notification_permission_dialog_page import NotificationPermissionDialogPage
from pages.settings_page import SettingsPage
from services.permissions_service import PermissionsService
from services.playback_service import PlaybackService
from services.settings_service import SettingsService

ROOT_FOLDER_PATH = "device_farm_extra_data"
FIRST_SONG_PATH = "/FolderA/track_a1.mp3"
SECOND_SONG_PATH = "/seek_test.mp3"
SECOND_SONG_DURATION_SECONDS = 60


def test_PLAYER_TC_050_seek_bar_uses_currently_playing_tracks_duration(driver_wrapper: DriverWrapper):
    permissions_page = NotificationPermissionDialogPage(driver_wrapper)
    PermissionsService(permissions_page).allow_notifications()

    library_page = LibraryPage(driver_wrapper)
    library_page.open_settings()

    settings_page = SettingsPage(driver_wrapper)
    SettingsService(settings_page).set_root_folder(ROOT_FOLDER_PATH)
    settings_page.click_back()

    service = PlaybackService(library_page)
    service.play_song(FIRST_SONG_PATH)
    service.wait_for_elapsed_time_to_advance()

    service.play_song(SECOND_SONG_PATH)
    service.wait_for_elapsed_time_to_advance()

    service.seek_to_fraction(0.5)
    service.validate_elapsed_time_within(SECOND_SONG_DURATION_SECONDS // 2, tolerance_seconds=3)
