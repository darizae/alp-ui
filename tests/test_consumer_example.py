from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
EXAMPLE = ROOT / "examples" / "consumer_app" / "main.py"


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
