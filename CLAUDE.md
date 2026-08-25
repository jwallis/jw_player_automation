# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project state

Appium/Python test automation framework for `jw_player` (a native Android MP3 player app). Owns the whole QA layer for that app: test cases (`docs/qa/test_cases.md`) and the automation scripts that exercise them live here together, not in `jw_player`. Not yet executing against a real device or Device Farm - that's a later phase.

## Architecture

Python 3.11. Layered: `config/`, `driver/`, `pages/`, `services/`, `exceptions/`, `utils/`, `tests/` - see `docs/standards/standards.md` for the full naming rules and the reasoning behind the layering. Locates elements by `testTag`/resource-id (`jw_player`'s Compose `testTagsAsResourceId`), never `contentDescription` - that's a translatable string, unsafe to depend on for automation once the app supports more than one language. Every file starts with `from __future__ import annotations` (lets type hints use the `X | None` union syntax regardless of Python version) - keep doing that in new files. Dependencies go in `requirements.txt`, not hardcoded versions elsewhere.

## Commands

- Run framework/unit tests: `pytest tests/`
- Type-check: `mypy .`
- Install dependencies: `pip install -r requirements.txt`

## Conventions to follow

- **Follow `docs/standards/standards.md` exactly** - the `get_`/`click_`/`open_`/`set_` prefixes on page-object methods, user-action-named service methods (`play_song`, `restart_song`, never "click"/"set" in the name), `validate_*` for every assertion method, `exceptions`/`utils` each in their own directory.
- **`testTag` goes on the element that actually carries the data** (text, state), not just a wrapping container - Compose doesn't make a container's tag automatically expose a child's text or state; verify against a real device dump if unsure, not just by reading the Kotlin.
- **Write a unit test for any new non-trivial logic you add** (a new service method's state-checking logic, a new page object's locator-building logic) in `tests/`, using a mocked `DriverWrapper` (see `tests/test_framework_wiring.py` for the pattern) - no real device needed, and these tests must actually run in CI (`ci.yml`). Framework unit tests are a different thing from real Appium test scenarios (one function per `docs/qa/test_cases.md` case, using the service layer) - keep them apart, see `test_framework_wiring.py`'s own docstring.
- **Run `pytest tests/` and `mypy .` before finishing** - both are hard gates in `ci.yml`, not optional.
