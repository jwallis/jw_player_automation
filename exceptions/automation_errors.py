"""Custom exceptions for this framework - see docs/standards/standards.md
rule 3 (exceptions get their own directory, never folded into pages/ or
services/)."""

from __future__ import annotations


class AutomationError(Exception):
    """Base class for every exception this framework raises on purpose."""


class ElementNotFoundError(AutomationError):
    def __init__(self, locator: str, page_source: str | None = None):
        message = f"Element not found: {locator}"
        if page_source:
            message += f"\nPage source at failure time:\n{page_source}"
        super().__init__(message)
        self.locator = locator


class ValidationError(AutomationError):
    """Raised by a service's validate_* method when the assertion fails."""
