"""Small native Qt Gallery for the Alpaca Light theme foundation."""

from __future__ import annotations

import sys
from dataclasses import fields

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from python_ui_library.theme import ALPACA_LIGHT, install_theme


def _font(family: str, size: float, weight: int) -> QFont:
    font = QFont(family)
    font.setPointSizeF(size)
    font.setWeight(QFont.Weight(weight))
    return font


def _swatch(name: str, value: str) -> QWidget:
    row = QWidget()
    layout = QGridLayout(row)
    sample = QFrame()
    sample.setFixedSize(48, 32)
    sample.setFrameShape(QFrame.Shape.Box)
    sample.setAutoFillBackground(True)
    palette = sample.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor(value))
    sample.setPalette(palette)
    sample.setAccessibleName(f"{name} color {value}")
    layout.addWidget(sample, 0, 0, 2, 1)
    layout.addWidget(QLabel(name), 0, 1)
    value_label = QLabel(value)
    value_label.setFont(_font(ALPACA_LIGHT.typography.metadata_family, 8.5, 500))
    layout.addWidget(value_label, 1, 1)
    return row


def build_window() -> QWidget:
    theme = ALPACA_LIGHT
    window = QWidget()
    window.setWindowTitle("python-ui-library — Theme Gallery")
    window.setAccessibleName("Alpaca Light Theme Gallery")
    window.resize(760, 700)

    content = QWidget()
    layout = QVBoxLayout(content)
    layout.setContentsMargins(*(theme.spacing.xlarge,) * 4)
    layout.setSpacing(theme.spacing.large)

    heading = QLabel("Alpaca Light")
    heading.setFont(
        _font(
            theme.typography.body_family,
            theme.typography.heading_size,
            theme.typography.heading_weight,
        )
    )
    heading.setAccessibleName("Theme heading")
    layout.addWidget(heading)
    layout.addWidget(QLabel("Semantic tokens applied to native PySide6 Qt Widgets."))

    swatches = QGroupBox("Colors")
    swatch_layout = QGridLayout(swatches)
    for index, field in enumerate(fields(theme.colors)):
        name = field.name
        value = getattr(theme.colors, name)
        swatch_layout.addWidget(_swatch(name, value), index // 2, index % 2)
    layout.addWidget(swatches)

    typography = QGroupBox("Typography")
    type_layout = QVBoxLayout(typography)
    body = QLabel("DM Sans body — The quick brown fox jumps over the lazy dog.")
    body.setFont(_font(theme.typography.body_family, theme.typography.body_size, 400))
    type_layout.addWidget(body)
    metadata = QLabel("JETBRAINS MONO · METADATA · 0123456789")
    metadata.setFont(
        _font(
            theme.typography.metadata_family,
            theme.typography.overline_size,
            theme.typography.metadata_weight,
        )
    )
    type_layout.addWidget(metadata)
    layout.addWidget(typography)

    controls = QGroupBox("Native Qt controls")
    control_layout = QGridLayout(controls)
    action = QPushButton("Action")
    action.setAccessibleName("Theme demo action")
    disabled = QPushButton("Disabled")
    disabled.setEnabled(False)
    field = QLineEdit()
    field.setPlaceholderText("Focus this field with Tab")
    field.setAccessibleName("Theme demo text field")
    control_layout.addWidget(action, 0, 0)
    control_layout.addWidget(disabled, 0, 1)
    control_layout.addWidget(field, 1, 0, 1, 2)
    layout.addWidget(controls)
    layout.addStretch()

    scroll = QScrollArea(window)
    scroll.setWidgetResizable(True)
    scroll.setWidget(content)
    window_layout = QVBoxLayout(window)
    window_layout.setContentsMargins(0, 0, 0, 0)
    window_layout.addWidget(scroll)
    return window


def main() -> int:
    app = QApplication(sys.argv)
    install_theme(app)
    window = build_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
