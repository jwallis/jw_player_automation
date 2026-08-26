"""Standing critical-path smoke test - see CLAUDE.md. Runs against a real
device on every Device Farm invocation, alongside whatever's new that push -
not gated on a specific PLAYER_TC entry, a fast general regression check
that the core playback loop still works.

Sets the root folder via the debug-only automation backdoor (see
utils/driver_util.py's set_root_folder_via_backdoor) rather than the real
Storage Access Framework picker, which test_cases.md already marks not
automatable. The app is force-stopped and relaunched right after, since
NavGraph.kt only reads the stored root-folder URI once, at first
composition - it won't pick up a change made after the app's already
running without a fresh launch.
"""

from __future__ import annotations

from config.config import load_config
from driver.driver_factory import DriverFactory
from pages.library_page import LibraryPage
from services.playback_service import PlaybackService
from utils.app_util import AppUtil
from utils.driver_util import DriverUtil

ROOT_FOLDER_PATH = "/sdcard/device_farm_extra_data"
SONG_PATH = "/genre_c/artist_a/song_a.mp3"


def test_critical_path_play_song_and_verify_playing():
    config = load_config()
    driver_wrapper = DriverFactory.create(config)
    try:
        DriverUtil(driver_wrapper).set_root_folder_via_backdoor(ROOT_FOLDER_PATH)

        app_util = AppUtil(driver_wrapper, config)
        app_util.quit_app()
        app_util.launch_app()

        library_page = LibraryPage(driver_wrapper)
        service = PlaybackService(library_page)

        service.play_song(SONG_PATH)
        service.validate_song_is_playing("song_a")
    finally:
        DriverFactory.quit(driver_wrapper)
