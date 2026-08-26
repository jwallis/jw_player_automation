"""Posts the real Device Farm run result to Slack: every test that ran plus
its pass/fail status, and a link to the run on the AWS console - no
screenshots or video links, per Phase 7's design.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests

RESULT_ICONS = {"PASSED": ":white_check_mark:", "FAILED": ":x:"}


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> int:
    webhook_url = _require_env("SLACK_JW_PLAYER_CI_WEBHOOK_URL")
    result_path = Path("device_farm_result.json")

    if not result_path.exists():
        text = "[Appium] :x: Failed — Device Farm run did not produce a result file."
        requests.post(webhook_url, json={"text": text})
        return 0

    summary = json.loads(result_path.read_text())
    run_result = summary["run_result"]
    icon = RESULT_ICONS.get(run_result, ":warning:")

    lines = [f"[Appium] {icon} Run {run_result} — {summary['console_url']}"]
    for test in summary["tests"]:
        test_icon = RESULT_ICONS.get(test["result"], ":warning:")
        lines.append(f"{test_icon} {test['name']}: {test['result']}")

    requests.post(webhook_url, json={"text": "\n".join(lines)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
