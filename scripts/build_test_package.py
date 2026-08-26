"""Builds the zip Device Farm actually runs: framework support code plus
only the standing critical-path test and whatever's new per
`last_generated_tests.txt` - never the whole accumulated tests/ directory,
per Phase 7's "only run what's new" design.
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

MANIFEST_PATH = Path("last_generated_tests.txt")
PACKAGE_DIR = Path("device_farm_package")
ZIP_PATH = Path("test_package.zip")
ALWAYS_INCLUDED = ["tests/test_critical_path.py"]
FRAMEWORK_DIRS = ["pages", "driver", "services", "exceptions", "utils", "config"]


def _manifest_test_files() -> set[str]:
    if not MANIFEST_PATH.exists():
        return set()
    files = set()
    for line in MANIFEST_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        file_path = line.split("::", 1)[0]
        files.add(file_path)
    return files


def main() -> None:
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir()

    ignore = shutil.ignore_patterns("__pycache__", ".DS_Store", "*.pyc")
    for directory in FRAMEWORK_DIRS:
        shutil.copytree(directory, PACKAGE_DIR / directory, ignore=ignore)
    shutil.copy("requirements.txt", PACKAGE_DIR / "requirements.txt")

    (PACKAGE_DIR / "tests").mkdir()
    (PACKAGE_DIR / "tests" / "__init__.py").touch()

    test_files = set(ALWAYS_INCLUDED) | _manifest_test_files()
    for test_file in sorted(test_files):
        destination = PACKAGE_DIR / test_file
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(test_file, destination)

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for path in PACKAGE_DIR.rglob("*"):
            if path.is_file():
                zip_file.write(path, path.relative_to(PACKAGE_DIR))

    print(f"Packaged {len(test_files)} test file(s) into {ZIP_PATH}: {sorted(test_files)}")


if __name__ == "__main__":
    main()
