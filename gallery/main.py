"""Small native Qt Gallery for Alpaca Light and public components."""

from __future__ import annotations

import sys
from dataclasses import fields

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QCompleter,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from alp_ui.components import (
    Alert,
    Badge,
    Button,
    Card,
    CheckBox,
    DataTable,
    Divider,
    EmptyState,
    FolderPicker,
    HelpHint,
    NumberInput,
    Plot,
    ProgressBar,
    SelectInput,
    Switch,
    Text,
    TextInput,
)
from alp_ui.theme import ALPACA_LIGHT, install_theme, make_icon

_BUTTON_VARIANTS = ("primary", "secondary", "outline", "danger")
_FEEDBACK_INTENTS = ("neutral", "info", "success", "warning", "danger")


class _GalleryTableModel(QAbstractTableModel):
    """Computed demo records that do not allocate a second 10,000-row collection."""

    def __init__(self, rows: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._rows = rows

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else self._rows

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else 3

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole or not index.isValid():
            return None
        row = index.row()
        return (f"Item {row + 1:05}", f"Group {row % 5 + 1}", row * 4)[index.column()]

    def headerData(  # noqa: N802
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ("Item", "Category", "Value")[section]
        return None


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


def _section(title: str) -> QGroupBox:
    """Return a Gallery section that remains token-colored on native macOS styles."""

    theme = ALPACA_LIGHT
    section = QGroupBox(title)
    section.setObjectName(f"gallery{title}")
    # Local QSS is required because QMacStyle ignores QPalette for QGroupBox fills.
    section.setStyleSheet(
        f"""
        QGroupBox {{
            background-color: transparent;
            border: 0;
            margin-top: {theme.spacing.xlarge}px;
            padding-top: {theme.spacing.small}px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 0;
            padding: 0;
            color: {theme.colors.text};
        }}
        """
    )
    return section


def _component_row(*widgets: QWidget) -> QWidget:
    """Lay out examples at their native size instead of stretching a grid column."""

    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(ALPACA_LIGHT.spacing.medium)
    for widget in widgets:
        layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    layout.addStretch()
    return row


def build_window() -> QWidget:
    theme = ALPACA_LIGHT
    window = QWidget()
    window.setWindowTitle("alp-ui — Theme Gallery")
    window.setAccessibleName("Alpaca Light Theme Gallery")
    window.resize(760, 700)

    content = QWidget()
    layout = QVBoxLayout(content)
    layout.setContentsMargins(*(theme.spacing.xlarge,) * 4)
    layout.setSpacing(theme.spacing.large)

    heading = Text("Alpaca Light", role="title")
    heading.setAccessibleName("Theme heading")
    layout.addWidget(heading)
    introduction = QLabel("Alpaca palette · native Qt behavior · consistent desktop components.")
    introduction.setWordWrap(True)
    layout.addWidget(introduction)
    layout.addWidget(
        Text(
            "Readable type scale with quieter surfaces and consistent controls.",
            role="caption",
            word_wrap=True,
        )
    )
    focus_help = QLabel(
        "Keyboard focus check: click Primary, then use Tab and Shift+Tab; "
        "the blue outline marks focus."
    )
    focus_help.setObjectName("focusInstructions")
    focus_help.setWordWrap(True)
    layout.addWidget(focus_help)

    swatches = _section("Colors")
    swatch_layout = QGridLayout(swatches)
    for index, field in enumerate(fields(theme.colors)):
        name = field.name
        value = getattr(theme.colors, name)
        swatch_layout.addWidget(_swatch(name, value), index // 2, index % 2)
    layout.addWidget(swatches)

    typography = _section("Typography")
    type_layout = QVBoxLayout(typography)
    type_layout.addWidget(Text("Build clear desktop interfaces", role="heading"))
    type_layout.addWidget(
        Text(
            "Body text wraps safely when the window narrows or translations grow longer.",
            word_wrap=True,
        )
    )
    type_layout.addWidget(Text("Supporting caption text", role="caption"))
    type_layout.addWidget(Text("JETBRAINS MONO · OVERLINE · 0123456789", role="overline"))
    type_layout.addWidget(Text("Page title · DM Sans", role="title"))
    type_layout.addWidget(Text("Section heading · semibold", role="subheading"))
    layout.addWidget(typography)

    actions = _section("Actions")
    action_layout = QVBoxLayout(actions)
    action_layout.setSpacing(theme.spacing.medium)
    action_layout.addWidget(Text("Variants", role="overline"))
    variant_buttons = [Button(variant.title(), variant=variant) for variant in _BUTTON_VARIANTS]
    action_layout.addWidget(_component_row(*variant_buttons[:2]))
    action_layout.addWidget(_component_row(*variant_buttons[2:]))
    action_layout.addWidget(Text("Sizes", role="overline"))
    action_layout.addWidget(
        _component_row(
            Button("Small", size="small"),
            Button("Medium", size="medium"),
            Button("Large", size="large"),
        )
    )
    disabled = Button("Disabled")
    disabled.setEnabled(False)
    action_layout.addWidget(Text("States", role="overline"))
    action_layout.addWidget(_component_row(disabled, Button("Load", loading=True)))
    action_layout.addWidget(Text("Native comparison", role="overline"))
    native_button = QPushButton("Native QPushButton")
    native_button.setObjectName("nativeButtonComparison")
    action_layout.addWidget(
        _component_row(native_button, Button("Styled Button", variant="outline"))
    )
    layout.addWidget(actions)

    surfaces = _section("Surfaces")
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
    flat_card = Card(shadow=False)
    flat_card.content_layout.addWidget(Text("Card without shadow", role="heading"))
    flat_card.content_layout.addWidget(
        Text("Use the opt-out for dense or repeated surfaces.", word_wrap=True)
    )
    surface_layout.addWidget(flat_card)
    divider_row = QWidget()
    divider_layout = QHBoxLayout(divider_row)
    divider_layout.setContentsMargins(0, 0, 0, 0)
    divider_layout.addWidget(Text("Left"))
    divider_layout.addWidget(Divider(Qt.Orientation.Vertical))
    divider_layout.addWidget(Text("Right"))
    surface_layout.addWidget(divider_row)
    layout.addWidget(surfaces)

    fields_group = _section("Fields")
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
    integer_input = NumberInput(kind="integer", value=2, minimum=0, maximum=10, label="Count")
    decimal_input = NumberInput(
        kind="decimal",
        value=2.5,
        minimum=0,
        maximum=10,
        step=0.5,
        label="Quantity",
    )
    select_input = SelectInput(("First", "Second", "Third"), label="Choice")
    check_box = CheckBox("Use compact results")
    check_box.setChecked(True)
    disabled_check_box = CheckBox("Disabled option")
    disabled_check_box.setEnabled(False)
    enabled_switch = Switch("Enabled setting")
    enabled_switch.setChecked(True)
    disabled_switch = Switch("Disabled setting")
    disabled_switch.setEnabled(False)
    page_size = NumberInput(kind="integer", value=25, minimum=1, maximum=100, label="")
    page_size_label = QLabel("&Items per page")
    page_size_label.setBuddy(page_size.control)
    page_size.control.setAccessibleName("Items per page")
    page_size_help = HelpHint("Sets how many items appear on each page.", subject="Items per page")
    page_size_example = QWidget()
    page_size_layout = QVBoxLayout(page_size_example)
    page_size_layout.setContentsMargins(0, 0, 0, 0)
    page_size_layout.setSpacing(theme.spacing.xsmall)
    page_size_layout.addWidget(_component_row(page_size_label, page_size_help))
    page_size_layout.addWidget(page_size)
    heading_help = HelpHint(
        "Groups controls that change how results are displayed.", subject="Display options"
    )
    folder_picker = FolderPicker(label="Folder")
    field_layout.addWidget(text_input, 0, 0)
    field_layout.addWidget(invalid_input, 0, 1)
    field_layout.addWidget(masked_input, 1, 0)
    field_layout.addWidget(select_input, 1, 1)
    field_layout.addWidget(integer_input, 2, 0)
    field_layout.addWidget(decimal_input, 2, 1)
    field_layout.addWidget(check_box, 3, 0)
    field_layout.addWidget(disabled_check_box, 3, 1)
    field_layout.addWidget(enabled_switch, 4, 0)
    field_layout.addWidget(Switch("Setting off"), 4, 1)
    field_layout.addWidget(disabled_switch, 5, 0)
    field_layout.addWidget(page_size_example, 6, 0)
    field_layout.addWidget(
        _component_row(Text("Display options", role="subheading"), heading_help), 6, 1
    )
    field_layout.addWidget(folder_picker, 7, 0, 1, 2)
    field_help_instructions = QLabel(
        "Contextual help: hover the ? button, or reach it with Tab and press Space."
    )
    field_help_instructions.setWordWrap(True)
    field_layout.addWidget(field_help_instructions, 8, 0, 1, 2)
    layout.addWidget(fields_group)

    feedback = _section("Feedback")
    feedback_layout = QVBoxLayout(feedback)
    badges = QWidget()
    badges.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
    badge_layout = QGridLayout(badges)
    badge_layout.setContentsMargins(0, 0, 0, 0)
    badge_layout.setHorizontalSpacing(theme.spacing.medium)
    badge_layout.setVerticalSpacing(theme.spacing.small)
    for index, intent in enumerate(_FEEDBACK_INTENTS):
        badge_layout.addWidget(
            Badge(intent.title(), intent=intent),
            index // 3,
            index % 3,
            Qt.AlignmentFlag.AlignLeft,
        )
    feedback_layout.addWidget(badges, 0, Qt.AlignmentFlag.AlignLeft)
    for intent in ("neutral", "info", "success", "warning", "danger"):
        feedback_layout.addWidget(
            Alert(
                f"This is generic {intent} feedback.",
                title=intent.title(),
                intent=intent,
                action=(
                    Button("Dismiss", variant="outline", size="small") if intent == "info" else None
                ),
            )
        )
    progress = ProgressBar(value=64)
    progress.setAccessibleName("Example operation progress")
    feedback_layout.addWidget(progress)
    waiting = ProgressBar(minimum=0, maximum=0)
    waiting.setAccessibleName("Example operation waiting")
    feedback_layout.addWidget(waiting)
    empty_action = Button("Add item", variant="outline", size="small")
    feedback_layout.addWidget(
        EmptyState(
            "Nothing here yet",
            text="Add an item to populate this view.",
            icon=make_icon("info", color=theme.colors.text_muted, size=24),
            action=empty_action,
        )
    )
    layout.addWidget(feedback)

    data_group = _section("Data")
    data_layout = QVBoxLayout(data_group)
    data_layout.addWidget(Text("10,000-row caller model", role="overline"))
    large_table = DataTable()
    large_table.setAccessibleName("10,000-row example table")
    large_model = _GalleryTableModel(10_000, large_table)
    large_table.setModel(large_model)
    large_table.horizontalHeader().setStretchLastSection(True)
    large_table.setMinimumHeight(240)
    data_layout.addWidget(large_table)
    data_layout.addWidget(Text("Empty caller model", role="overline"))
    empty_table = DataTable()
    empty_table.setAccessibleName("Empty example table")
    empty_model = _GalleryTableModel(0, empty_table)
    empty_table.setModel(empty_model)
    empty_table.setMinimumHeight(120)
    data_layout.addWidget(empty_table)
    layout.addWidget(data_group)

    plots_group = _section("Plots")
    plots_layout = QVBoxLayout(plots_group)
    plots_layout.addWidget(Text("Numeric line series", role="overline"))
    line_plot = Plot(kind="line", x_label="Time", y_label="Value")
    line_plot.setAccessibleName("Observed and reference values")
    line_plot.setLines(
        {
            "Observed": [(0.0, 0.3), (1.0, 0.55), (2.0, 0.48), (3.0, 0.72)],
            "Reference": [(0.0, 0.42), (1.0, 0.47), (2.0, 0.58), (3.0, 0.62)],
        }
    )
    line_plot.setMinimumHeight(220)
    plots_layout.addWidget(line_plot)
    plots_layout.addWidget(Text("Categorical bars", role="overline"))
    bar_plot = Plot(kind="bar", x_label="Category", y_label="Value")
    bar_plot.setAccessibleName("Example category values")
    bar_plot.setBars([("Alpha", 0.62), ("Beta", 0.24), ("Gamma", -0.14), ("Delta", 0.41)])
    bar_plot.setMinimumHeight(220)
    plots_layout.addWidget(bar_plot)
    layout.addWidget(plots_group)
    layout.addStretch()

    scroll = QScrollArea(window)
    scroll.setWidgetResizable(True)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
