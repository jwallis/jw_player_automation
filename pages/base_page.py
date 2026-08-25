"""Model layer (Page Object Model) - base class.

Every screen's page object extends this. Holds a reference to the
DriverWrapper and delegates all interaction to it - see
docs/standards/standards.md concept 1 (interaction is a driver-wrapper
concern, not a page concern).
"""

from __future__ import annotations

from driver.driver_wrapper import DriverWrapper


class BasePage:
    def __init__(self, driver_wrapper: DriverWrapper):
        self.driver_wrapper = driver_wrapper
