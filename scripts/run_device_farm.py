"""Uploads the app + test package + test spec (+ optional Extra Data fixture
zip) to AWS Device Farm, schedules a run against the configured device
pool, polls for completion, and writes a structured result to
`device_farm_result.json` for the workflow's Slack step to read. Exits
non-zero if the run's overall result isn't PASSED, so the calling workflow
step fails accordingly.

The test package always contains the entire tests/ directory - which
test(s) actually execute is decided at run time by device_farm_testspec.yml
passing a pytest `-k` filter (built here from last_generated_tests.txt) via
Device Farm's own environmentVariables mechanism, not by curating which
files are in the zip. The test spec itself is uploaded fresh on every run,
same as the app/test package/fixture zip - it's a real, versioned file in
this repo, not a static pre-uploaded ARN that could silently go stale the
moment someone edits it.

The Device Farm project/pool ARNs and the Extra Data fixture path come from
`config/environments/default.yaml` and `config/config.yaml` via
`load_config()` - they're identifiers/paths, not secrets, set once during
the AWS setup session. APK_PATH and TEST_PACKAGE_PATH are environment
variables instead: they're computed fresh each run by earlier workflow
steps (the artifact download location, the packaging script's own output
file), not something set ahead of time.
"""

from __future__ import annotations

import datetime
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import boto3
import requests

from config.config import load_config

UPLOAD_POLL_SECONDS = 5
RUN_POLL_SECONDS = 15
TEST_SPEC_PATH = "device_farm_testspec.yml"
MANIFEST_PATH = Path("last_generated_tests.txt")
ALWAYS_RUN_FUNCTIONS = {"test_critical_path_play_song_and_verify_playing"}


def _pytest_filter_expression() -> str:
    function_names = set(ALWAYS_RUN_FUNCTIONS)
    if MANIFEST_PATH.exists():
        for line in MANIFEST_PATH.read_text().splitlines():
            line = line.strip()
            if line:
                function_names.add(line.split("::", 1)[-1])
    return " or ".join(sorted(function_names))


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def _upload_and_wait(client: Any, project_arn: str, file_path: str, upload_type: str) -> str:
    name = os.path.basename(file_path)
    response = client.create_upload(
        projectArn=project_arn,
        name=name,
        type=upload_type,
        contentType="application/octet-stream",
    )
    upload_arn = response["upload"]["arn"]
    upload_url = response["upload"]["url"]

    with open(file_path, "rb") as file_stream:
        put_response = requests.put(
            upload_url, data=file_stream, headers={"content-type": "application/octet-stream"}
        )
    if not put_response.ok:
        raise SystemExit(f"Failed to PUT {file_path} to Device Farm: {put_response.reason}")

    status = response["upload"]["status"]
    while status not in ("SUCCEEDED", "FAILED"):
        time.sleep(UPLOAD_POLL_SECONDS)
        response = client.get_upload(arn=upload_arn)
        status = response["upload"]["status"]

    if status == "FAILED":
        message = response["upload"].get("message", "no message")
        raise SystemExit(f"Device Farm upload of {file_path} failed: {message}")

    return upload_arn


def _console_url(run_arn: str) -> str:
    # arn:aws:devicefarm:{region}:{account}:run:{project-id}/{run-id}
    region = run_arn.split(":")[3]
    project_and_run = run_arn.split(":")[-1]
    project_id, run_id = project_and_run.split("/")
    return (
        f"https://{region}.console.aws.amazon.com/devicefarm/home"
        f"?region={region}#/mobile/projects/{project_id}/runs/{run_id}"
    )


def main() -> int:
    config = load_config()
    project_arn = config.device_farm_project_arn
    pool_arn = config.device_farm_pool_arn
    if not (project_arn and pool_arn):
        raise SystemExit(
            "device_farm_project_arn/pool_arn aren't set in "
            "config/environments/default.yaml yet - fill these in during the "
            "AWS setup session before this can run."
        )

    apk_path = _require_env("APK_PATH")
    test_package_path = _require_env("TEST_PACKAGE_PATH")
    extra_data_candidate = config.device_farm_extra_data_path
    extra_data_resolved = (
        (Path(__file__).resolve().parent.parent / extra_data_candidate) if extra_data_candidate else None
    )
    print(
        f"Extra Data fixture: candidate={extra_data_candidate!r} "
        f"resolved={extra_data_resolved} exists={extra_data_resolved.is_file() if extra_data_resolved else False} "
        f"cwd={os.getcwd()}"
    )
    extra_data_path = str(extra_data_resolved) if extra_data_resolved and extra_data_resolved.is_file() else None

    client = boto3.client("devicefarm")

    app_arn = _upload_and_wait(client, project_arn, apk_path, "ANDROID_APP")
    test_package_arn = _upload_and_wait(
        client, project_arn, test_package_path, "APPIUM_PYTHON_TEST_PACKAGE"
    )
    test_spec_arn = _upload_and_wait(client, project_arn, TEST_SPEC_PATH, "APPIUM_PYTHON_TEST_SPEC")

    configuration: dict[str, Any] = {
        "environmentVariables": [
            {"name": "PYTEST_TEST_FILTER", "value": _pytest_filter_expression()},
        ],
    }
    if extra_data_path:
        extra_data_arn = _upload_and_wait(client, project_arn, extra_data_path, "EXTERNAL_DATA")
        configuration["extraDataPackageArn"] = extra_data_arn

    run_name = "jw-player-automation-" + datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    schedule_kwargs: dict[str, Any] = {
        "projectArn": project_arn,
        "appArn": app_arn,
        "devicePoolArn": pool_arn,
        "name": run_name,
        "configuration": configuration,
        "test": {
            "type": "APPIUM_PYTHON",
            "testSpecArn": test_spec_arn,
            "testPackageArn": test_package_arn,
        },
    }

    response = client.schedule_run(**schedule_kwargs)
    run_arn = response["run"]["arn"]

    status = response["run"]["status"]
    while status not in ("COMPLETED", "ERRORED", "STOPPING"):
        time.sleep(RUN_POLL_SECONDS)
        response = client.get_run(arn=run_arn)
        status = response["run"]["status"]

    run_result = response["run"]["result"]
    console_url = _console_url(run_arn)

    tests: list[dict[str, str]] = []
    for job in client.list_jobs(arn=run_arn)["jobs"]:
        for suite in client.list_suites(arn=job["arn"])["suites"]:
            for test in client.list_tests(arn=suite["arn"])["tests"]:
                tests.append({"name": test["name"], "result": test["result"]})

    summary = {
        "run_arn": run_arn,
        "run_status": status,
        "run_result": run_result,
        "console_url": console_url,
        "tests": tests,
    }
    with open("device_farm_result.json", "w") as summary_file:
        json.dump(summary, summary_file, indent=2)

    print(json.dumps(summary, indent=2))
    return 0 if run_result == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
