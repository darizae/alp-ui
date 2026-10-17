from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).parents[1]
FONT_FILES = {
    "DM-Sans-OFL.txt",
    "DMSans-Bold.ttf",
    "DMSans-Medium.ttf",
    "DMSans-Regular.ttf",
    "DMSans-SemiBold.ttf",
    "JetBrains-Mono-OFL.txt",
    "JetBrainsMono-Medium.ttf",
    "JetBrainsMono-Regular.ttf",
    "JetBrainsMono-SemiBold.ttf",
}


def test_wheel_contains_theme_fonts_and_notices(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--no-isolation", "--outdir", str(tmp_path)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    wheel = next(tmp_path.glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
    resource_root = "python_ui_library/theme/resources/fonts/"
    assert {resource_root + filename for filename in FONT_FILES} <= names
    assert not any(name.startswith("references/") for name in names)
