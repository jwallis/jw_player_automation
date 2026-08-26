"""Standing critical-path smoke test - see CLAUDE.md. Runs against a real
device on every Device Farm invocation, alongside whatever's new that push -
not gated on a specific PLAYER_TC entry, a fast general regression check
that the core playback loop still works.
"""

from __future__ import annotations

from config.config import load_config
from driver.driver_factory import DriverFactory
from pages.library_page import LibraryPage
from services.playback_service import PlaybackService


def test_critical_path_play_song_and_verify_playing():
    config = load_config()
    driver_wrapper = DriverFactory.create(config)
    try:
        library_page = LibraryPage(driver_wrapper)
        service = PlaybackService(library_page)

        service.play_song("seek_test")
        service.validate_song_is_playing("seek_test")
    finally:
        DriverFactory.quit(driver_wrapper)
