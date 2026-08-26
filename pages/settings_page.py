"""Settings screen page object.

Locators are the literal testTag values from SettingsScreen.kt (JWP-3, plus a
follow-up structural fix) - same "don't invent placeholders" rule as
library_page.py. root_folder_button/white_noise_file_button's tags sit on
the inner label Text, not the outer Button - reading .text off the located
element returns the actual selected name (or the "Select..." placeholder)
directly. white_noise_play_button/white_noise_pause_button are two distinct,
static tags reflecting state - not read from contentDescription, since
that's a translatable string.
"""

from __future__ import annotations

from pages.base_page import BasePage


class SettingsPage(BasePage):
    BACK_BUTTON = "back_button"
    ROOT_FOLDER_BUTTON = "root_folder_button"
    WHITE_NOISE_FILE_BUTTON = "white_noise_file_button"
    WHITE_NOISE_PLAY_BUTTON = "white_noise_play_button"
    WHITE_NOISE_PAUSE_BUTTON = "white_noise_pause_button"

    def click_back(self) -> None:
        self.driver_wrapper.tap(self.BACK_BUTTON)

    def click_root_folder_button(self) -> None:
        self.driver_wrapper.tap(self.ROOT_FOLDER_BUTTON)

    def get_root_folder_label(self) -> str:
        return self.driver_wrapper.find_by(self.ROOT_FOLDER_BUTTON).text

    def get_white_noise_file_label(self) -> str:
        return self.driver_wrapper.find_by(self.WHITE_NOISE_FILE_BUTTON).text

    def is_white_noise_playing(self) -> bool:
        return self.driver_wrapper.is_present(self.WHITE_NOISE_PAUSE_BUTTON)
