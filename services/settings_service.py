"""Settings screen service (business layer)."""

from __future__ import annotations

from pages.settings_page import SettingsPage
from pages.system_folder_picker_page import SystemFolderPickerPage
from exceptions.automation_errors import ValidationError


class SettingsService:
    def __init__(self, settings_page: SettingsPage):
        self.settings_page = settings_page

    def set_root_folder(self, folder_path: str) -> None:
        """Drives the real Storage Access Framework picker end to end:
        opens it from Settings, navigates to the true storage root, opens
        each named folder in turn (e.g. "/device_farm_extra_data"), confirms
        the selection, and grants the resulting access prompt. Deliberately
        not the debug backdoor - confirmed live that a raw file:// URI
        (what the backdoor sets) can see folders but not files under scoped
        storage, while a real SAF grant from this picker can see both."""
        self.settings_page.click_root_folder_button()
        picker = SystemFolderPickerPage(self.settings_page.driver_wrapper)
        picker.navigate_to_root()
        for folder in [part for part in folder_path.split("/") if part]:
            picker.open_folder(folder)
        picker.use_this_folder()
        picker.allow_access()

    def play_white_noise(self) -> None:
        if not self.settings_page.is_white_noise_playing():
            self.settings_page.driver_wrapper.tap(SettingsPage.WHITE_NOISE_PLAY_BUTTON)

    def pause_white_noise(self) -> None:
        if self.settings_page.is_white_noise_playing():
            self.settings_page.driver_wrapper.tap(SettingsPage.WHITE_NOISE_PAUSE_BUTTON)

    def validate_white_noise_is_playing(self) -> None:
        if not self.settings_page.is_white_noise_playing():
            raise ValidationError("Expected white noise to be playing, but it isn't")
