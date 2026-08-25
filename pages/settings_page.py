"""Settings screen page object.

Locators are the literal testTag values from SettingsScreen.kt (JWP-3) -
same "don't invent placeholders" rule as library_page.py. root_folder_button
and white_noise_file_button are each one fixed tag regardless of whether a
selection has been made - state/label comes from contentDescription instead.
"""

from __future__ import annotations

from pages.base_page import BasePage


class SettingsPage(BasePage):
    BACK_BUTTON = "back_button"
    ROOT_FOLDER_BUTTON = "root_folder_button"
    WHITE_NOISE_FILE_BUTTON = "white_noise_file_button"
    WHITE_NOISE_PLAY_PAUSE_BUTTON = "white_noise_play_pause_button"

    WHITE_NOISE_PLAY = "Play white noise"
    WHITE_NOISE_PAUSE = "Pause white noise"

    def click_back(self) -> None:
        self.driver_wrapper.tap(self.BACK_BUTTON)

    def get_root_folder_label(self) -> str:
        return self.driver_wrapper.find_by(self.ROOT_FOLDER_BUTTON).get_attribute("content-desc")

    def get_white_noise_file_label(self) -> str:
        return self.driver_wrapper.find_by(self.WHITE_NOISE_FILE_BUTTON).get_attribute("content-desc")

    def get_white_noise_play_pause_state(self) -> str:
        element = self.driver_wrapper.find_by(self.WHITE_NOISE_PLAY_PAUSE_BUTTON)
        return element.get_attribute("content-desc")
