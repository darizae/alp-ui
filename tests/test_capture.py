from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtGui import QImage

ROOT = Path(__file__).parents[1]


def test_default_consumer_capture_is_reproducible(tmp_path: Path) -> None:
    environment = os.environ.copy()
    environment["QT_QPA_PLATFORM"] = "offscreen"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "gallery.capture",
            "--target",
            "consumer",
            "--output-dir",
            str(tmp_path),
        ],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    image = QImage(str(tmp_path / "consumer-default.png"))
    assert not image.isNull()
    assert image.width() >= 600
    assert image.height() >= 480
