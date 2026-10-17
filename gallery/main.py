"""Small native Qt Gallery for Alpaca Light and public components."""

from __future__ import annotations

import sys
from dataclasses import fields

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QCompleter,
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from python_ui_library.components import (
    Button,
    Card,
    CheckBox,
    Divider,
    NumberInput,
    SelectInput,
    Switch,
    Text,
    TextInput,
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

    typography = QGroupBox("Typography components")
    type_layout = QVBoxLayout(typography)
    type_layout.addWidget(Text("Build clear desktop interfaces", role="heading"))
    type_layout.addWidget(
        Text(
            "Body text wraps safely when the window narrows or translations grow longer.",
            word_wrap=True,
            selectable=True,
        )
    )
    type_layout.addWidget(Text("Supporting caption text", role="caption"))
    type_layout.addWidget(Text("JETBRAINS MONO · OVERLINE · 0123456789", role="overline"))
    layout.addWidget(typography)

    actions = QGroupBox("Actions")
    action_layout = QGridLayout(actions)
    for column, variant in enumerate(("primary", "secondary", "outline", "danger")):
        action_layout.addWidget(Button(variant.title(), variant=variant), 0, column)
    disabled = Button("Disabled")
    disabled.setEnabled(False)
    action_layout.addWidget(Button("Small", size="small"), 1, 0)
    action_layout.addWidget(Button("Large", size="large"), 1, 1)
    action_layout.addWidget(disabled, 1, 2)
    action_layout.addWidget(Button("Load", loading=True), 1, 3)
    layout.addWidget(actions)

    surfaces = QGroupBox("Surfaces")
    surface_layout = QVBoxLayout(surfaces)
    card = Card()
    card.content_layout.addWidget(Text("Card title", role="heading"))
    card.content_layout.addWidget(Divider())
    card.content_layout.addWidget(
        Text(
            "Cards own presentation and layout, while consumer applications own data.",
            word_wrap=True,
        )
    )
    surface_layout.addWidget(card)
    layout.addWidget(surfaces)

    fields_group = QGroupBox("Fields")
    field_layout = QGridLayout(fields_group)
    text_input = TextInput(
        label="Name",
        description="Native textChanged and editingFinished signals are preserved.",
        placeholder="Focus this field with Tab",
    )
    text_input.control.setAccessibleName("Theme demo text field")
    text_input.setCompleter(QCompleter(["Ada Lovelace", "Grace Hopper"], text_input))
    invalid_input = TextInput(label="Reference", error="A reference is required")
    masked_input = TextInput(label="Code", input_mask="AA-0000;_", placeholder="AB-1234")
    number_input = NumberInput(
        kind="decimal",
        value=2.5,
        minimum=0,
        maximum=10,
        step=0.5,
        label="Quantity",
    )
    select_input = SelectInput(("First", "Second", "Third"), label="Choice")
    check_box = CheckBox("Use compact results")
    disabled_check_box = CheckBox("Disabled option")
    disabled_check_box.setEnabled(False)
    switch = Switch("Enable summaries")
    switch.setChecked(True)
    field_layout.addWidget(text_input, 0, 0)
    field_layout.addWidget(invalid_input, 0, 1)
    field_layout.addWidget(number_input, 1, 0)
    field_layout.addWidget(select_input, 1, 1)
    field_layout.addWidget(masked_input, 2, 0)
    field_layout.addWidget(switch, 2, 1)
    field_layout.addWidget(check_box, 3, 0)
    field_layout.addWidget(disabled_check_box, 3, 1)
    layout.addWidget(fields_group)
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
