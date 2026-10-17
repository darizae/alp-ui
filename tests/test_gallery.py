from __future__ import annotations

from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton

from gallery.main import build_window
from python_ui_library.components import (
    Button,
    Card,
    CheckBox,
    NumberInput,
    SelectInput,
    Switch,
    TextInput,
)
from python_ui_library.theme import install_theme


def test_theme_gallery_builds_with_keyboard_controls(qapp: QApplication) -> None:
    install_theme(qapp)
    window = build_window()

    assert window.accessibleName() == "Alpaca Light Theme Gallery"
    assert window.findChildren(QPushButton)
    field = window.findChild(QLineEdit)
    assert field is not None
    assert field.focusPolicy().value != 0
    assert field.accessibleName() == "Theme demo text field"
    assert len(window.findChildren(Button)) >= 8
    assert any(button.isLoading() for button in window.findChildren(Button))
    assert window.findChild(Card) is not None
    assert window.findChildren(TextInput)
    assert window.findChild(NumberInput) is not None
    assert window.findChild(SelectInput) is not None
    assert window.findChildren(CheckBox)
    assert window.findChild(Switch) is not None
    window.close()
