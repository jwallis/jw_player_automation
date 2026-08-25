"""Library/main screen page object.

Locators are the literal testTag values from jw_player's MainScreen.kt,
MiniPlayer.kt, and FolderListView.kt (JWP-3, plus a follow-up structural fix)
- not invented placeholders. play_button/pause_button are two distinct,
static tags reflecting state directly - deliberately not read from
contentDescription, since that's a translatable string and unsafe to depend
on once the app supports more than one language.
"""

from __future__ import annotations

from pages.base_page import BasePage


class LibraryPage(BasePage):
    SETTINGS_ICON = "settings_icon"
    NOW_PLAYING_TEXT = "now_playing_text"
    ELAPSED_TIME_TEXT = "elapsed_time_text"
    SEEK_BAR = "seek_bar"
    PREVIOUS_BUTTON = "previous_button"
    SEEK_BACKWARD_BUTTON = "seek_backward_button"
    PLAY_BUTTON = "play_button"
    PAUSE_BUTTON = "pause_button"
    SEEK_FORWARD_BUTTON = "seek_forward_button"
    NEXT_BUTTON = "next_button"
    SCROLL_UP_INDICATOR = "scroll_up_indicator"
    SCROLL_DOWN_INDICATOR = "scroll_down_indicator"
    BACK_ROW = "back_row"
    EMPTY_LIBRARY_MESSAGE = "empty_library_message"

    @staticmethod
    def folder_tag(name: str) -> str:
        return f"folder_{name}"

    @staticmethod
    def file_tag(name: str) -> str:
        return f"file_{name}"

    def open_settings(self) -> None:
        self.driver_wrapper.tap(self.SETTINGS_ICON)

    def is_playing(self) -> bool:
        return self.driver_wrapper.is_present(self.PAUSE_BUTTON)

    def get_now_playing_text(self) -> str:
        return self.driver_wrapper.find_by(self.NOW_PLAYING_TEXT).text

    def get_empty_library_message(self) -> str:
        return self.driver_wrapper.find_by(self.EMPTY_LIBRARY_MESSAGE).text
