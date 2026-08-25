"""Custom exceptions for this framework - see docs/standards/standards.md
rule 3 (exceptions get their own directory, never folded into pages/ or
services/)."""

from __future__ import annotations


class AutomationError(Exception):
    """Base class for every exception this framework raises on purpose."""


class ElementNotFoundError(AutomationError):
    def __init__(self, locator: str):
        super().__init__(f"Element not found: {locator}")
        self.locator = locator


class ValidationError(AutomationError):
    """Raised by a service's validate_* method when the assertion fails."""
