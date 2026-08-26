"""Uploads the app + test package (+ optional Extra Data fixture zip) to AWS
Device Farm, schedules a run against the configured device pool, polls for
completion, and writes a structured result to `device_farm_result.json` for
the workflow's Slack step to read. Exits non-zero if the run's overall
result isn't PASSED, so the calling workflow step fails accordingly.

Configuration comes entirely from environment variables (set by
run-automation.yml from GitHub secrets/repo variables), not hardcoded here:
DEVICE_FARM_PROJECT_ARN, DEVICE_FARM_POOL_ARN, DEVICE_FARM_TEST_SPEC_ARN,
APK_PATH, TEST_PACKAGE_PATH, EXTRA_DATA_PATH (optional).
"""

from __future__ import annotations

import datetime
import json
import os
import sys
import time
from typing import Any

import boto3
import requests

UPLOAD_POLL_SECONDS = 5
RUN_POLL_SECONDS = 15


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
    project_arn = _require_env("DEVICE_FARM_PROJECT_ARN")
    pool_arn = _require_env("DEVICE_FARM_POOL_ARN")
    test_spec_arn = _require_env("DEVICE_FARM_TEST_SPEC_ARN")
    apk_path = _require_env("APK_PATH")
    test_package_path = _require_env("TEST_PACKAGE_PATH")
    extra_data_env = os.environ.get("EXTRA_DATA_PATH")
    extra_data_path = extra_data_env if extra_data_env and os.path.isfile(extra_data_env) else None

    client = boto3.client("devicefarm")

    app_arn = _upload_and_wait(client, project_arn, apk_path, "ANDROID_APP")
    test_package_arn = _upload_and_wait(
        client, project_arn, test_package_path, "APPIUM_PYTHON_TEST_PACKAGE"
    )

    configuration: dict[str, Any] = {}
    if extra_data_path:
        extra_data_arn = _upload_and_wait(client, project_arn, extra_data_path, "EXTERNAL_DATA")
        configuration["extraDataPackageArn"] = extra_data_arn

    run_name = "jw-player-automation-" + datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    schedule_kwargs: dict[str, Any] = {
        "projectArn": project_arn,
        "appArn": app_arn,
        "devicePoolArn": pool_arn,
        "name": run_name,
        "test": {
            "type": "APPIUM_PYTHON",
            "testSpecArn": test_spec_arn,
            "testPackageArn": test_package_arn,
        },
    }
    if configuration:
        schedule_kwargs["configuration"] = configuration

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
