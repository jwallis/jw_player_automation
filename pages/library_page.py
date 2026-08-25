"""Library/main screen page object.

Locators are the literal testTag values from jw_player's MainScreen.kt,
MiniPlayer.kt, and FolderListView.kt (JWP-3) - not invented placeholders.
Where a control's state isn't reflected in its tag (e.g. play_pause_button
is one fixed tag whether playing or paused), state is read from the located
element's still-dynamic contentDescription instead - testTag is the "find"
mechanism, contentDescription remains the "read state" mechanism.
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
    PLAY_PAUSE_BUTTON = "play_pause_button"
    SEEK_FORWARD_BUTTON = "seek_forward_button"
    NEXT_BUTTON = "next_button"
    SCROLL_UP_INDICATOR = "scroll_up_indicator"
    SCROLL_DOWN_INDICATOR = "scroll_down_indicator"
    BACK_ROW = "back_row"

    PLAY = "Play"
    PAUSE = "Pause"

    @staticmethod
    def folder_tag(name: str) -> str:
        return f"folder_{name}"

    @staticmethod
    def file_tag(name: str) -> str:
        return f"file_{name}"

    def open_settings(self) -> None:
        self.driver_wrapper.tap(self.SETTINGS_ICON)

    def get_play_pause_state(self) -> str:
        """Returns "Play" or "Pause" - play_pause_button is one fixed tag
        regardless of state, so state comes from its contentDescription."""
        element = self.driver_wrapper.find_by(self.PLAY_PAUSE_BUTTON)
        return element.get_attribute("content-desc")

    def get_now_playing_text(self) -> str:
        return self.driver_wrapper.find_by(self.NOW_PLAYING_TEXT).text
