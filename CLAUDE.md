# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project state

Appium/Python test automation framework for `jw_player` (a native Android MP3 player app). Owns the whole QA layer for that app: test cases (`docs/qa/test_cases.md`) and the automation scripts that exercise them live here together, not in `jw_player`. Real Appium scenario tests execute against actual AWS Device Farm devices via `run-automation.yml` - `pytest`/`mypy`/CI never run them, since no real device exists in those environments.

## Architecture

Python 3.11. Layered: `config/`, `driver/`, `pages/`, `services/`, `exceptions/`, `utils/` - see `docs/standards/standards.md` for the full naming rules and the reasoning behind the layering. Tests are split into two top-level directories: `tests/` holds real Appium scenario tests (one function per `docs/qa/test_cases.md` case, service-layer only - this is what a real device run packages), `unittests/` holds mocked-`DriverWrapper` framework unit tests (no device needed) - keep them apart, they test different things. Locates elements by `testTag`/resource-id (`jw_player`'s Compose `testTagsAsResourceId`), never `contentDescription` - that's a translatable string, unsafe to depend on for automation once the app supports more than one language. Every file starts with `from __future__ import annotations` (lets type hints use the `X | None` union syntax regardless of Python version) - keep doing that in new files. Dependencies go in `requirements.txt`, not hardcoded versions elsewhere.

## Commands

- Run scenario tests (needs a real device/Appium session - a local emulator, or Device Farm): `pytest tests/`
- Run framework/unit tests (no device needed, this is what CI actually runs): `pytest unittests/`
- Type-check (covers both directories, doesn't execute anything so needs no device): `mypy .`
- Install dependencies: `pip install -r requirements.txt`

## Conventions to follow

- **Follow `docs/standards/standards.md` exactly** - the `get_`/`click_`/`open_`/`set_` prefixes on page-object methods, user-action-named service methods (`play_song`, `restart_song`, never "click"/"set" in the name), `validate_*` for every assertion method, `exceptions`/`utils` each in their own directory.
- **`testTag` goes on the element that actually carries the data** (text, state), not just a wrapping container - Compose doesn't make a container's tag automatically expose a child's text or state; verify against a real device dump if unsure, not just by reading the Kotlin.
- **Write a unit test for any new non-trivial logic you add** (a new service method's state-checking logic, a new page object's locator-building logic) in `unittests/`, using a mocked `DriverWrapper` (see `unittests/test_unit_tests.py` for the pattern) - no real device needed, and these tests must actually run in CI. Framework unit tests are a different thing from real Appium test scenarios (one function per `docs/qa/test_cases.md` case, using the service layer, built with a real `DriverFactory.create(load_config())` connection, never a mock) - keep them apart, see `unittests/test_unit_tests.py`'s own docstring.
- **Run `pytest unittests/` and `mypy .` before finishing** - both are hard gates in CI, not optional. Don't try to run `pytest tests/` in an environment with no real device (CI, a generation run) - a connection failure there doesn't mean the test is wrong, it means there's no device to test against; only an actual Device Farm run proves a scenario test itself works.
