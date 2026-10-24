from __future__ import annotations

import subprocess
import sys
import tarfile
import zipfile
from email.parser import BytesParser
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


PACKAGE_FILES = {
    "alp_ui/__init__.py",
    "alp_ui/components/__init__.py",
    "alp_ui/components/actions.py",
    "alp_ui/components/data.py",
    "alp_ui/components/feedback.py",
    "alp_ui/components/help.py",
    "alp_ui/components/inputs.py",
    "alp_ui/components/surfaces.py",
    "alp_ui/components/typography.py",
    "alp_ui/theme/__init__.py",
    "alp_ui/theme/alpaca_light.py",
    "alp_ui/theme/fonts.py",
    "alp_ui/theme/install.py",
    "alp_ui/theme/tokens.py",
}
FORBIDDEN_PARTS = {"references", "alpaca-ui-frontend", "ui_library", "evidence.md"}


def test_distributions_are_complete_and_clean(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "build", "--no-isolation", "--outdir", str(tmp_path)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    wheel = next(tmp_path.glob("*.whl"))
    sdist = next(tmp_path.glob("*.tar.gz"))

    checked = subprocess.run(
        [sys.executable, "-m", "twine", "check", str(wheel), str(sdist)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert checked.returncode == 0, checked.stdout + checked.stderr

    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
        metadata = BytesParser().parsebytes(archive.read(metadata_name))
    resource_root = "alp_ui/theme/resources/fonts/"
    assert PACKAGE_FILES <= names
    assert {resource_root + filename for filename in FONT_FILES} <= names
    assert any(name.endswith(".dist-info/licenses/LICENSE") for name in names)
    notice_suffix = ".dist-info/licenses/docs/legal/THIRD_PARTY_NOTICES.md"
    assert any(name.endswith(notice_suffix) for name in names)
    assert metadata["Name"] == "alp-ui"
    assert metadata["Version"] == "0.1.0a0"
    runtime_requirements = [
        requirement
        for requirement in metadata.get_all("Requires-Dist", [])
        if "; extra ==" not in requirement
    ]
    assert runtime_requirements == ["pyside6-essentials<6.12,>=6.11"]

    with tarfile.open(sdist) as archive:
        sdist_names = set(archive.getnames())
    root = "alp_ui-0.1.0a0/"
    assert {
        root + "LICENSE",
        root + "docs/legal/THIRD_PARTY_NOTICES.md",
        root + "examples/consumer_app/main.py",
        *(root + "src/" + name for name in PACKAGE_FILES),
        *(root + "src/" + resource_root + filename for filename in FONT_FILES),
    } <= sdist_names

    for name in names | sdist_names:
        assert not FORBIDDEN_PARTS.intersection(Path(name).parts), name
