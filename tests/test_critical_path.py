"""Standing critical-path smoke test - see CLAUDE.md. Runs against a real
device on every Device Farm invocation, alongside whatever's new that push -
not gated on a specific PLAYER_TC entry, a fast general regression check
that the core playback loop still works.

Sets the root folder by driving the real Storage Access Framework picker
(SettingsService.set_root_folder), not the debug-only backdoor - confirmed
live that the backdoor's raw file:// URI can see folders but not files
under scoped storage, while a real SAF grant sees both. The real picker
flow also fires the app's own onRootFolderChosen callback, so - unlike the
backdoor - no force-stop/relaunch is needed to pick up the change.
"""

from __future__ import annotations

from driver.driver_wrapper import DriverWrapper
from pages.library_page import LibraryPage
from pages.settings_page import SettingsPage
from services.playback_service import PlaybackService
from services.settings_service import SettingsService

ROOT_FOLDER_PATH = "device_farm_extra_data"
SONG_PATH = "/genre_c/artist_a/song_a.mp3"


def test_critical_path_play_song_and_verify_playing(driver_wrapper: DriverWrapper):
    library_page = LibraryPage(driver_wrapper)
    library_page.open_settings()

    settings_page = SettingsPage(driver_wrapper)
    SettingsService(settings_page).set_root_folder(ROOT_FOLDER_PATH)
    settings_page.click_back()

    service = PlaybackService(library_page)
    service.validate_elapsed_time_is_zero()
    service.play_song(SONG_PATH)
    service.wait_for_elapsed_time_to_advance()
    service.validate_song_is_playing("song_a")
