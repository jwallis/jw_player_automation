"""Configuration layer.

Every device/server/environment value the rest of the framework needs comes
through here - nothing below this layer should read an env var or a YAML
file directly. See docs/standards/standards.md "Config vs. environment" for
why this is two files, not one: config.yaml holds values that are genuinely
constant regardless of environment; environments/<name>.yaml holds
appium_server_url, app_package, and app_activity, since all three could
legitimately differ per environment. Which environment file to load is
picked via the JWP_AUTOMATION_ENV env var (defaults to "default").
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

_CONFIG_DIR = Path(__file__).parent
_ENVIRONMENTS_DIR = _CONFIG_DIR / "environments"


@dataclass(frozen=True)
class AutomationConfig:
    appium_server_url: str
    platform_name: str
    automation_name: str
    app_package: str
    app_activity: str
    implicit_wait_seconds: int
    splash_screen_wait_seconds: int
    device_farm_project_arn: str
    device_farm_pool_arn: str
    device_farm_test_spec_arn: str
    device_farm_extra_data_path: str

    @property
    def capabilities(self) -> dict:
        return {
            "platformName": self.platform_name,
            "appium:automationName": self.automation_name,
            "appium:appPackage": self.app_package,
            "appium:appActivity": self.app_activity,
        }


def load_config(environment: str | None = None) -> AutomationConfig:
    """Load config.yaml merged with an environment's file. Raises
    FileNotFoundError with a clear message if the named environment doesn't
    exist, rather than silently falling back to defaults."""
    env_name = environment or os.environ.get("JWP_AUTOMATION_ENV", "default")
    environment_path = _ENVIRONMENTS_DIR / f"{env_name}.yaml"
    if not environment_path.exists():
        raise FileNotFoundError(
            f"No environment config at {environment_path} (environment: {env_name!r})"
        )
    with (_CONFIG_DIR / "config.yaml").open() as f:
        merged = yaml.safe_load(f)
    with environment_path.open() as f:
        merged.update(yaml.safe_load(f))
    return AutomationConfig(**merged)
