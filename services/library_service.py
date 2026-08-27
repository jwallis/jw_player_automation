"""Library browsing service (business layer)."""

from __future__ import annotations

from pages.library_page import LibraryPage
from exceptions.automation_errors import ValidationError

EMPTY_LIBRARY_MESSAGE = "Choose a root folder to get started!"


class LibraryService:
    def __init__(self, library_page: LibraryPage):
        self.library_page = library_page

    def open_folder(self, folder_name: str) -> None:
        self.library_page.driver_wrapper.tap(LibraryPage.folder_tag(folder_name))

    def go_up_one_folder(self) -> None:
        self.library_page.driver_wrapper.tap(LibraryPage.BACK_ROW)

    def find_song(self, song_name: str) -> bool:
        return self.library_page.driver_wrapper.is_present(LibraryPage.file_tag(song_name))

    def validate_empty_library_message_shown(self) -> None:
        actual = self.library_page.get_empty_library_message()
        if actual != EMPTY_LIBRARY_MESSAGE:
            raise ValidationError(
                f"Expected empty-library message {EMPTY_LIBRARY_MESSAGE!r}, but got {actual!r}"
            )
