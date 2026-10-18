from __future__ import annotations

from dataclasses import replace

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtTest import QSignalSpy
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsDropShadowEffect,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from alp_ui.components import Button, Card, Divider, Text
from alp_ui.theme import ALPACA_LIGHT, install_theme


@pytest.fixture(autouse=True)
def _install_default_theme(qapp: QApplication) -> None:
    install_theme(qapp)


def test_button_validates_variant_and_size() -> None:
    with pytest.raises(ValueError, match="variant must be one of"):
        Button("Unknown", variant="quiet")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="size must be one of"):
        Button("Unknown", size="huge")  # type: ignore[arg-type]


def test_button_preserves_single_click_focus_and_disabled_behavior(qtbot) -> None:
    button = Button("Save", variant="primary")
    qtbot.addWidget(button)
    button.show()
    button.activateWindow()
    button.setFocus()
    qtbot.waitUntil(button.hasFocus)
    assert ":focus" in button.styleSheet()

    clicked = QSignalSpy(button.clicked)
    qtbot.keyClick(button, Qt.Key.Key_Space)
    assert clicked.count() == 1

    button.setEnabled(False)
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    assert clicked.count() == 1


def test_button_uses_installed_theme_and_semibold_font(qapp: QApplication) -> None:
    custom = replace(
        ALPACA_LIGHT,
        colors=replace(ALPACA_LIGHT.colors, primary="#0F766E"),
    )
    install_theme(qapp, custom)
    button = Button("Save")

    assert button.palette().color(QPalette.ColorRole.Button) == QColor("#0F766E")
    assert button.font().weight() == custom.typography.button_weight
    assert button.accessibleName() == "Save"


def test_button_loading_is_presentational_and_preserves_caller_state(qtbot) -> None:
    button = Button("Load results")
    clicked = QSignalSpy(button.clicked)

    button.setLoading(True)

    assert button.isLoading()
    assert button.text() == "Loading…"
    assert button.accessibleName() == "Loading…"
    assert not button.isEnabled()
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    assert clicked.count() == 0

    button.setEnabled(False)
    button.setLoading(False)
    assert button.text() == "Load results"
    assert button.accessibleName() == "Load results"
    assert not button.isEnabled()


def test_button_loading_constructor_validates_options() -> None:
    assert Button("Save", loading=True).isLoading()
    with pytest.raises(TypeError, match="loading must be a bool"):
        Button("Save", loading=1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="loading_text must not be empty"):
        Button("Save", loading_text="")


@pytest.mark.parametrize("role", ["title", "heading", "subheading", "body", "caption", "overline"])
def test_text_roles_are_available(role: str) -> None:
    text = Text("Example", role=role)  # type: ignore[arg-type]
    assert text.role == role


def test_text_validates_role_and_supports_wrapping_and_selection() -> None:
    with pytest.raises(ValueError, match="role must be one of"):
        Text("Example", role="display")  # type: ignore[arg-type]

    text = Text("A long translated label " * 8, selectable=True, word_wrap=True)
    assert text.wordWrap()
    assert text.textInteractionFlags() & Qt.TextInteractionFlag.TextSelectableByKeyboard
    assert text.heightForWidth(120) > text.heightForWidth(500)


def test_card_owns_layout_children_and_theme_metrics() -> None:
    parent = QWidget()
    card = Card(parent)
    child = Text("A long line of content that can wrap inside its card.", word_wrap=True)
    card.content_layout.addWidget(child)

    assert card.parent() is parent
    assert child.parent() is card
    assert card.content_layout.contentsMargins().left() == ALPACA_LIGHT.spacing.card_padding
    assert ALPACA_LIGHT.colors.surface in card.styleSheet()
    assert ALPACA_LIGHT.colors.border in card.styleSheet()
    effect = card.graphicsEffect()
    assert isinstance(effect, QGraphicsDropShadowEffect)
    assert effect.blurRadius() == 3.0
    assert effect.offset().y() == 1.0
    assert effect.color().name().upper() == ALPACA_LIGHT.colors.shadow
    assert Card(shadow=False).graphicsEffect() is None
    with pytest.raises(TypeError, match="shadow must be a bool"):
        Card(shadow=1)  # type: ignore[arg-type]


def test_divider_uses_native_orientation_and_border_palette() -> None:
    horizontal = Divider()
    vertical = Divider(Qt.Orientation.Vertical)

    assert horizontal.frameShape() == horizontal.Shape.HLine
    assert vertical.frameShape() == vertical.Shape.VLine
    assert horizontal.palette().color(QPalette.ColorRole.Mid) == QColor(ALPACA_LIGHT.colors.border)
    with pytest.raises(ValueError, match="Qt.Horizontal or Qt.Vertical"):
        Divider(3)  # type: ignore[arg-type]


def test_components_work_in_ordinary_qt_layout() -> None:
    parent = QWidget()
    layout = QVBoxLayout(parent)
    button = Button("Action")
    label = Text("Details")
    divider = Divider()
    layout.addWidget(button)
    layout.addWidget(label)
    layout.addWidget(divider)

    assert parent.findChildren(Button) == [button]
    assert isinstance(label, QLabel)
