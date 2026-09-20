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
# song_a is ~75s and song_b ~35s (testdata/device_farm_extra_data.zip), so a
# seek computed from the first track's duration lands nowhere near the
# second track's midpoint.
FIRST_SONG_PATH = "/genre_c/artist_a/song_a.mp3"
SECOND_SONG_NAME = "song_b.mp3"
SECOND_SONG_MIDPOINT_SECONDS = 18
MIDPOINT_TOLERANCE_SECONDS = 4


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

    service.play_song(SECOND_SONG_NAME)
    service.wait_for_elapsed_time_to_advance()

    service.seek_to_fraction(0.5)
    service.validate_elapsed_time_within(SECOND_SONG_MIDPOINT_SECONDS, tolerance_seconds=MIDPOINT_TOLERANCE_SECONDS)
