from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from PySide6.QtWidgets import QApplication, QHeaderView

from alp_ui.components import Button, DataTable, Text, TextInput
from alp_ui.theme import ALPACA_LIGHT, install_theme
from examples.consumer_app.main import build_window

ROOT = Path(__file__).parents[1]
EXAMPLE = ROOT / "examples" / "consumer_app" / "main.py"


def test_default_consumer_uses_normal_theme_and_natural_action_size(qapp: QApplication) -> None:
    install_theme(qapp)
    window = build_window()
    window.show()
    qapp.processEvents()

    title = next(text for text in window.findChildren(Text) if text.role == "title")
    field = window.findChild(TextInput)
    button = window.findChild(Button)
    table = window.findChild(DataTable)
    assert title.text() == "Items"
    assert field is not None
    assert field.control.minimumHeight() == 40
    assert button is not None
    assert button.width() == button.sizeHint().width()
    assert table is not None
    assert table.horizontalHeader().sectionResizeMode(0) == QHeaderView.ResizeMode.Stretch
    assert window.styleSheet() == ""
    assert ALPACA_LIGHT.density == "standard"
    window.close()


@pytest.mark.parametrize("options", [[], ["--custom-theme"]])
def test_consumer_example_starts_and_stops_cleanly(options: list[str], tmp_path: Path) -> None:
    environment = os.environ.copy()
    environment["QT_QPA_PLATFORM"] = "offscreen"
    result = subprocess.run(
        [sys.executable, "-I", str(EXAMPLE), *options, "--smoke"],
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
