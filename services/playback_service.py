"""Playback service (business layer).

Method names describe what a user does, not what the UI does - see
docs/standards/standards.md rule 2. Test scripts call into this, never into
LibraryPage directly.
"""

from __future__ import annotations

from pages.library_page import LibraryPage
from exceptions.automation_errors import ValidationError


class PlaybackService:
    def __init__(self, library_page: LibraryPage):
        self.library_page = library_page

    def play_song(self, song_name: str) -> None:
        self.library_page.driver_wrapper.tap(LibraryPage.file_tag(song_name))

    def pause_song(self) -> None:
        if self.library_page.is_playing():
            self.library_page.driver_wrapper.tap(LibraryPage.PAUSE_BUTTON)

    def resume_song(self) -> None:
        if not self.library_page.is_playing():
            self.library_page.driver_wrapper.tap(LibraryPage.PLAY_BUTTON)

    def skip_song(self) -> None:
        self.library_page.driver_wrapper.tap(LibraryPage.NEXT_BUTTON)

    def restart_song(self) -> None:
        # Restarts the current track from 0:00 if more than 3s have
        # elapsed, otherwise jumps to the previous track - see
        # MiniPlayer.kt/PlaybackViewModel's restart-or-previous behavior.
        self.library_page.driver_wrapper.tap(LibraryPage.PREVIOUS_BUTTON)

    def fast_forward(self, seconds: float) -> None:
        self.library_page.driver_wrapper.press_and_hold(LibraryPage.SEEK_FORWARD_BUTTON, seconds)

    def rewind(self, seconds: float) -> None:
        self.library_page.driver_wrapper.press_and_hold(LibraryPage.SEEK_BACKWARD_BUTTON, seconds)

    def validate_song_is_playing(self, song_name: str) -> None:
        if not self.library_page.is_playing():
            raise ValidationError(f"Expected {song_name!r} to be playing, but nothing is")
        now_playing = self.library_page.get_now_playing_text()
        if song_name not in now_playing:
            raise ValidationError(f"Expected {song_name!r} to be playing, but got {now_playing!r}")
