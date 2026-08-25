# JW Player Automation - Coding Standards

## Rules

1. **Page class method prefixes reflect what the method does**, not what
   screen it's on: `get_` for anything that returns data (current elapsed
   time, a filename, current play/pause state), `click_`/`tap_` for a plain
   tap action, `open_` for navigating to another screen/section, `set_` for
   entering a value. Locator constants/builders (e.g. a method that just
   returns an accessibility-id string for a given folder name) are data, not
   actions, and are exempt from this - they're not prefixed.
2. **Service class methods never reference the UI mechanics** ("click this",
   "set that") - names describe the user-level action: `play_song(name)`,
   `quit_app()`, `find_song(name)`, `fast_forward(seconds)`,
   `restart_song()`. Every validation method starts with `validate_`
   (`validate_song_is_playing(name)`, not `check_` or `assert_` or a bare
   `is_playing()`).
3. **Exceptions and utilities each get their own top-level directory**
   (`exceptions/`, `utils/`) - never folded into `pages/` or `services/`.

## Concepts (guidance, not hard rules)

1. **The driver wrapper owns raw interaction** (`tap()`, `find_by()`,
   `is_present()`, gesture actions like a press-and-hold) - not the page
   layer. `BasePage` holds a reference to the driver wrapper and pages call
   through it (`self.driver_wrapper.tap(...)`); `BasePage` itself doesn't
   implement `tap()`/`find_by()`. This keeps interaction strategy (locator
   fallbacks, retry/wait behavior, gesture implementation) centralized in one
   place instead of duplicated or drifting across every page.
2. **Config vs. environment**: `platform_name`, `automation_name`, and wait
   durations are just config, not something that varies by environment.
   `appium_server_url`, `app_package`, and `app_activity` live in the
   environment file instead - the server URL obviously varies per
   environment, and package/activity could too (a debug build variant with a
   suffixed applicationId, for example) even though today's single
   environment happens to only need one value for each. Wait durations
   arguably *could* be environment-specific too (a remote device farm vs. a
   local emulator might warrant different timeouts) but live in `config.yaml`
   anyway for now rather than splitting early.
