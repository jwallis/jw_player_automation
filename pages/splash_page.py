"""Splash screen page object.

jw_player's splash is a 1.5s hand-rolled Compose screen with no interactive
elements - the only thing worth modeling is waiting for it to clear.
"""

from __future__ import annotations

import time

from pages.base_page import BasePage


class SplashPage(BasePage):
    def wait_for_dismissal(self, wait_seconds: int) -> None:
        time.sleep(wait_seconds)
