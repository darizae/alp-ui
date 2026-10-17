from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_import_has_no_qapplication_side_effect() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import python_ui_library; "
                "from PySide6.QtWidgets import QApplication; "
                "assert QApplication.instance() is None"
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_essentials_modules_are_available() -> None:
    from PySide6 import QtCore, QtGui, QtWidgets

    assert QtCore and QtGui and QtWidgets


def test_runtime_dependency_is_only_pyside6_essentials() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["dependencies"] == ["PySide6-Essentials>=6.11,<6.12"]
