"""Builds the zip Device Farm runs: framework support code plus the entire
tests/ directory. Which tests actually execute is decided at run time by
device_farm_testspec.yml's pytest -k filter (built from
last_generated_tests.txt), not by which files are physically in this zip -
see run_device_farm.py. unittests/ never goes in here; it needs no device.
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

PACKAGE_DIR = Path("device_farm_package")
ZIP_PATH = Path("test_package.zip")
FRAMEWORK_DIRS = ["pages", "driver", "services", "exceptions", "utils", "config", "tests"]


def main() -> None:
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir()

    ignore = shutil.ignore_patterns("__pycache__", ".DS_Store", "*.pyc")
    for directory in FRAMEWORK_DIRS:
        shutil.copytree(directory, PACKAGE_DIR / directory, ignore=ignore)
    shutil.copy("requirements.txt", PACKAGE_DIR / "requirements.txt")

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for path in PACKAGE_DIR.rglob("*"):
            if path.is_file():
                zip_file.write(path, path.relative_to(PACKAGE_DIR))

    print(f"Packaged {ZIP_PATH}")


if __name__ == "__main__":
    main()
