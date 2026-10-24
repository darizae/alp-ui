from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAccessible
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
)

from alp_ui import components
from alp_ui.components import (
    Alert,
    Badge,
    Button,
    Card,
    CheckBox,
    DataTable,
    Divider,
    EmptyState,
    HelpHint,
    NumberInput,
    ProgressBar,
    SelectInput,
    Switch,
    Text,
    TextInput,
)
from alp_ui.theme import install_theme
from gallery.main import build_window

ROOT = Path(__file__).parents[1]


def test_theme_gallery_builds_with_keyboard_controls(qapp: QApplication) -> None:
    install_theme(qapp)
    window = build_window()

    assert window.accessibleName() == "Alpaca Light Theme Gallery"
    categories = {group.title() for group in window.findChildren(QGroupBox)}
    assert {"Actions", "Typography", "Surfaces", "Fields", "Feedback", "Data"} <= categories
    assert all("border: 0" in group.styleSheet() for group in window.findChildren(QGroupBox))
    focus_help = window.findChild(QLabel, "focusInstructions")
    assert focus_help is not None
    assert "Tab and Shift+Tab" in focus_help.text()
    assert window.findChildren(QPushButton)
    field = window.findChild(QLineEdit)
    assert field is not None
    assert field.focusPolicy().value != 0
    assert field.accessibleName() == "Theme demo text field"
    buttons = window.findChildren(Button)
    assert {button.variant for button in buttons} == {
        "primary",
        "secondary",
        "outline",
        "danger",
    }
    assert {button.component_size for button in buttons} == {"small", "medium", "large"}
    assert any(not button.isEnabled() for button in buttons)
    assert any(button.isLoading() for button in window.findChildren(Button))
    actions = window.findChild(QGroupBox, "galleryActions")
    assert actions is not None
    window.show()
    qapp.processEvents()
    assert all(
        button.width() == button.sizeHint().width() for button in actions.findChildren(Button)
    )
    assert window.findChild(QPushButton, "nativeButtonComparison") is not None
    assert {text.role for text in window.findChildren(Text)} == {
        "title",
        "subheading",
        "body",
        "caption",
        "heading",
        "overline",
    }
    cards = window.findChildren(Card)
    assert any(card.graphicsEffect() is not None for card in cards)
    assert any(card.graphicsEffect() is None for card in cards)
    assert {divider.orientation for divider in window.findChildren(Divider)} == {
        Qt.Orientation.Horizontal,
        Qt.Orientation.Vertical,
    }
    text_inputs = window.findChildren(TextInput)
    assert text_inputs
    assert any(field.errorText() for field in text_inputs)
    assert {field.kind for field in window.findChildren(NumberInput)} == {"integer", "decimal"}
    assert window.findChild(SelectInput) is not None
    assert any(box.isChecked() for box in window.findChildren(CheckBox))
    switches = window.findChildren(Switch)
    assert {switch.isChecked() for switch in switches} == {False, True}
    assert any(not switch.isEnabled() for switch in switches)
    intents = {"neutral", "info", "success", "warning", "danger"}
    assert {badge.intent for badge in window.findChildren(Badge)} == intents
    assert {alert.intent for alert in window.findChildren(Alert)} == intents
    progress_bars = window.findChildren(ProgressBar)
    assert {(bar.minimum(), bar.maximum()) for bar in progress_bars} == {(0, 0), (0, 100)}
    assert window.findChild(EmptyState) is not None
    assert len(window.findChildren(HelpHint)) == 2
    tables = window.findChildren(DataTable)
    assert len(tables) == 2
    assert {table.model().rowCount() for table in tables} == {0, 10_000}
    window.close()


def test_gallery_and_docs_cover_exact_public_component_surface(qapp: QApplication) -> None:
    install_theme(qapp)
    window = build_window()
    docs = (ROOT / "docs" / "components.md").read_text(encoding="utf-8")

    for name in components.__all__:
        component_type = getattr(components, name)
        assert window.findChild(component_type) is not None, name
        assert f"## {name}\n" in docs

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert ".venv\\Scripts\\python -m gallery.main" in readme
    window.close()


def test_gallery_interactive_controls_are_named_and_focusable(qapp: QApplication) -> None:
    install_theme(qapp)
    window = build_window()
    window.show()
    qapp.processEvents()

    interactive = [
        *window.findChildren(QPushButton),
        *window.findChildren(CheckBox),
        *window.findChildren(Switch),
        *window.findChildren(HelpHint),
        *(field.control for field in window.findChildren(TextInput)),
        *(field.control for field in window.findChildren(NumberInput)),
        *(field.control for field in window.findChildren(SelectInput)),
        *window.findChildren(DataTable),
    ]
    for control in interactive:
        interface = QAccessible.queryAccessibleInterface(control)
        assert interface is not None
        assert interface.text(QAccessible.Text.Name), type(control).__name__
        if control.isEnabled():
            assert control.focusPolicy() != Qt.FocusPolicy.NoFocus

    window.close()


def test_gallery_keeps_narrow_catalog_free_of_horizontal_scrolling(qapp: QApplication) -> None:
    install_theme(qapp)
    window = build_window()
    window.resize(480, 620)
    window.show()
    qapp.processEvents()

    scroll = window.findChild(QScrollArea)
    assert scroll is not None
    assert scroll.horizontalScrollBarPolicy() == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    assert not scroll.horizontalScrollBar().isVisible()
    assert scroll.widget().minimumSizeHint().width() <= window.width()
    window.close()
