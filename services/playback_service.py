"""Playback service (business layer).

Method names describe what a user does, not what the UI does - see
docs/standards/standards.md rule 2. Test scripts call into this, never into
LibraryPage directly.
"""

from __future__ import annotations

import time

from pages.library_page import LibraryPage
from exceptions.automation_errors import ValidationError


class PlaybackService:
    def __init__(self, library_page: LibraryPage):
        self.library_page = library_page

    def play_song(self, song_path: str, settle_seconds: float = 1) -> None:
        """Accepts a full path like "/genre_c/artist_a/song_a.mp3" -
        navigates into each folder in turn, then taps the file. The
        extension is stripped before building the file's tag, matching
        DirectoryLister.displayName()'s testTag convention on the app side
        (title = filename without its extension).

        Pauses briefly after each folder tap: confirmed live that tapping
        two folders back-to-back with no settle time can silently miss the
        second navigation - back_row (which mirrors currentFolderDoc.name)
        stayed on the first folder even though the tap on the second one
        returned successfully, meaning the click landed before Compose's
        recomposition into the new folder's contents was ready."""
        parts = [part for part in song_path.split("/") if part]
        *folders, filename = parts
        song_name = filename.rsplit(".", 1)[0]
        for folder in folders:
            self.library_page.driver_wrapper.tap(LibraryPage.folder_tag(folder))
            time.sleep(settle_seconds)
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

    def get_elapsed_seconds(self) -> int:
        """Parses the "MM:SS" elapsed_time_text into total seconds."""
        minutes, seconds = self.library_page.get_elapsed_time_text().split(":")
        return int(minutes) * 60 + int(seconds)

    def validate_elapsed_time_is_zero(self) -> None:
        elapsed = self.get_elapsed_seconds()
        if elapsed != 0:
            raise ValidationError(f"Expected elapsed time to be 0s, but got {elapsed}s")

    def validate_elapsed_time_has_advanced(self) -> None:
        elapsed = self.get_elapsed_seconds()
        if elapsed <= 0:
            raise ValidationError(f"Expected elapsed time to have advanced past 0s, but got {elapsed}s")

    def wait_for_elapsed_time_to_advance(self, timeout_seconds: float = 10, poll_interval: float = 1) -> None:
        """Polls elapsed time until it advances past 0s, instead of a single
        fixed sleep-then-check - confirmed live that playback-start latency
        is variable enough across runs/hardware for a fixed short wait to
        flake. Raises the same ValidationError validate_elapsed_time_has_advanced
        would if it never advances within the timeout."""
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            if self.get_elapsed_seconds() > 0:
                return
            time.sleep(poll_interval)
        self.validate_elapsed_time_has_advanced()
