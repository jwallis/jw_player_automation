"""Settings screen service (business layer)."""

from __future__ import annotations

from pages.settings_page import SettingsPage
from exceptions.automation_errors import ValidationError


class SettingsService:
    def __init__(self, settings_page: SettingsPage):
        self.settings_page = settings_page

    def play_white_noise(self) -> None:
        if self.settings_page.get_white_noise_play_pause_state() == SettingsPage.WHITE_NOISE_PLAY:
            self.settings_page.driver_wrapper.tap(SettingsPage.WHITE_NOISE_PLAY_PAUSE_BUTTON)

    def pause_white_noise(self) -> None:
        if self.settings_page.get_white_noise_play_pause_state() == SettingsPage.WHITE_NOISE_PAUSE:
            self.settings_page.driver_wrapper.tap(SettingsPage.WHITE_NOISE_PLAY_PAUSE_BUTTON)

    def validate_white_noise_is_playing(self) -> None:
        if self.settings_page.get_white_noise_play_pause_state() != SettingsPage.WHITE_NOISE_PAUSE:
            raise ValidationError("Expected white noise to be playing, but it isn't")
