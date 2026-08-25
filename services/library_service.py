"""Library browsing service (business layer)."""

from __future__ import annotations

from pages.library_page import LibraryPage


class LibraryService:
    def __init__(self, library_page: LibraryPage):
        self.library_page = library_page

    def open_folder(self, folder_name: str) -> None:
        self.library_page.driver_wrapper.tap(LibraryPage.folder_tag(folder_name))

    def go_up_one_folder(self) -> None:
        self.library_page.driver_wrapper.tap(LibraryPage.BACK_ROW)

    def find_song(self, song_name: str) -> bool:
        return self.library_page.driver_wrapper.is_present(LibraryPage.file_tag(song_name))
