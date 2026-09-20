"""OS-level permission dialogs service (business layer). The app requests
POST_NOTIFICATIONS once, the first time its main screen appears - not tied
to any particular app screen, so this doesn't belong under settings or
playback."""

from __future__ import annotations

from pages.notification_permission_dialog_page import NotificationPermissionDialogPage


class PermissionsService:
    def __init__(self, dialog_page: NotificationPermissionDialogPage):
        self.dialog_page = dialog_page

    def allow_notifications(self) -> None:
        self.dialog_page.tap_allow()
