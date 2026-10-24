"""Reproduce the committed Gallery, Showcase, and default-consumer images."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "images"


def _save(widget, path: Path) -> None:
    pixmap = widget.grab()
    if pixmap.isNull() or not pixmap.save(str(path), "PNG"):
        raise RuntimeError(f"could not capture {path}")


def _settle(app, window) -> None:
    from PySide6.QtCore import QPoint
    from PySide6.QtGui import QCursor

    QCursor.setPos(window.mapToGlobal(QPoint(-20, -20)))
    for _ in range(4):
        app.processEvents()


def _capture_gallery(output_dir: Path) -> None:
    from PySide6.QtWidgets import QApplication, QGroupBox, QScrollArea

    from alp_ui.theme import install_theme
    from gallery.main import build_window

    app = QApplication([])
    install_theme(app)
    window = build_window()
    window.show()
    _settle(app, window)

    scroll = window.findChild(QScrollArea)
    if scroll is None:
        raise RuntimeError("Gallery scroll area was not found")
    targets = {
        "gallery-actions.png": "galleryActions",
        "gallery-fields.png": "galleryFields",
        "gallery-feedback.png": "galleryFeedback",
        "gallery-data.png": "galleryData",
    }
    for filename, object_name in targets.items():
        section = window.findChild(QGroupBox, object_name)
        if section is None:
            raise RuntimeError(f"Gallery section {object_name!r} was not found")
        scroll.verticalScrollBar().setValue(section.y())
        _settle(app, window)
        _save(window, output_dir / filename)
    window.close()


def _capture_showcase(output_dir: Path) -> None:
    from dataclasses import replace

    from PySide6.QtWidgets import QApplication

    from alp_ui.theme import ALPACA_LIGHT, install_theme
    from gallery.showcase import build_showcase

    app = QApplication([])
    install_theme(app, replace(ALPACA_LIGHT, density="compact"))
    window = build_showcase()
    window.show()
    _settle(app, window)
    _save(window, output_dir / "showcase.png")
    window.close()


def _capture_consumer(output_dir: Path) -> None:
    from PySide6.QtWidgets import QApplication

    from alp_ui.theme import install_theme
    from examples.consumer_app.main import build_window

    app = QApplication([])
    install_theme(app)
    window = build_window()
    window.show()
    _settle(app, window)
    _save(window, output_dir / "consumer-default.png")
    window.close()


def _capture_in_fresh_processes(output_dir: Path) -> None:
    for target in ("gallery", "showcase", "consumer"):
        subprocess.run(
            [
                sys.executable,
                "-m",
                "gallery.capture",
                "--target",
                target,
                "--output-dir",
                str(output_dir),
            ],
            cwd=ROOT,
            check=True,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=("all", "gallery", "showcase", "consumer"),
        default="all",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    options = parser.parse_args(argv)
    output_dir = options.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if options.target == "all":
        _capture_in_fresh_processes(output_dir)
    elif options.target == "gallery":
        _capture_gallery(output_dir)
    elif options.target == "showcase":
        _capture_showcase(output_dir)
    else:
        _capture_consumer(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
