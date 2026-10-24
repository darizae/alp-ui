from __future__ import annotations

from dataclasses import replace
from unittest.mock import patch

import pytest
from PySide6.QtCore import QPoint, Qt
from PySide6.QtTest import QSignalSpy
from PySide6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWhatsThis, QWidget

from alp_ui.components import HelpHint
from alp_ui.theme import ALPACA_LIGHT, install_theme


@pytest.fixture(autouse=True)
def _install_default_theme(qapp: QApplication) -> None:
    install_theme(qapp)


def test_help_hint_exposes_plain_text_help_and_generic_accessibility(qtbot) -> None:
    hint = HelpHint("Choose how many items to show at once.")
    qtbot.addWidget(hint)

    assert hint.text() == "?"
    assert hint.toolTip() == "Choose how many items to show at once."
    assert hint.whatsThis() == "Choose how many items to show at once."
    assert hint.accessibleName() == "More information"
    assert hint.accessibleDescription() == "Choose how many items to show at once."
    assert hint.focusPolicy() == Qt.FocusPolicy.StrongFocus
    assert hint.minimumSize().width() == 24
    assert ":focus" in hint.styleSheet()


@pytest.mark.parametrize("value", ["", "   ", "\n\t"])
def test_help_hint_rejects_blank_explanations(value: str) -> None:
    with pytest.raises(ValueError, match="help_text must not be empty or whitespace"):
        HelpHint(value)


def test_help_hint_validates_text_inputs() -> None:
    with pytest.raises(TypeError, match="help_text must be a str"):
        HelpHint(None)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="subject must be a str"):
        HelpHint("Explanation", subject=None)  # type: ignore[arg-type]
    assert HelpHint("Explanation", subject="  ").accessibleName() == "More information"


def test_help_hint_subject_and_updates_cover_tooltip_help_view_and_accessibility() -> None:
    hint = HelpHint("Initial explanation", subject="Items per page")

    assert hint.accessibleName() == "More about Items per page"
    hint.setHelpText("Choose how many items to show at once.")

    assert hint.toolTip() == "Choose how many items to show at once."
    assert hint.whatsThis() == "Choose how many items to show at once."
    assert hint.accessibleDescription() == "Choose how many items to show at once."


def test_help_hint_escapes_text_that_looks_like_markup() -> None:
    hint = HelpHint("Use <b>plain text</b> & keep it readable.")

    assert hint.accessibleDescription() == "Use <b>plain text</b> & keep it readable."
    assert hint.toolTip() == "Use &lt;b&gt;plain text&lt;/b&gt; &amp; keep it readable."


def test_help_hint_click_and_keyboard_use_native_clicked_once(qtbot) -> None:
    hint = HelpHint("Keyboard help")
    qtbot.addWidget(hint)
    hint.show()
    hint.activateWindow()
    hint.setFocus()
    qtbot.waitUntil(hint.hasFocus)
    clicked = QSignalSpy(hint.clicked)

    with patch("alp_ui.components.help.QWhatsThis.showText") as show_text:
        qtbot.keyClick(hint, Qt.Key.Key_Space)

    assert clicked.count() == 1
    show_text.assert_called_once()
    position, text, anchor = show_text.call_args.args
    assert isinstance(position, QPoint)
    assert text == "Keyboard help"
    assert anchor is hint


def test_help_hint_follows_normal_tab_order_and_disabled_state(qtbot) -> None:
    parent = QWidget()
    layout = QVBoxLayout(parent)
    before = QLineEdit()
    hint = HelpHint("Keyboard help")
    after = QLineEdit()
    layout.addWidget(before)
    layout.addWidget(hint)
    layout.addWidget(after)
    qtbot.addWidget(parent)
    parent.show()
    before.setFocus()
    qtbot.waitUntil(before.hasFocus)

    qtbot.keyClick(before, Qt.Key.Key_Tab)
    qtbot.waitUntil(hint.hasFocus)
    qtbot.keyClick(hint, Qt.Key.Key_Tab)
    qtbot.waitUntil(after.hasFocus)
    qtbot.keyClick(after, Qt.Key.Key_Backtab)
    qtbot.waitUntil(hint.hasFocus)

    hint.setEnabled(False)
    with patch("alp_ui.components.help.QWhatsThis.showText") as show_text:
        hint.click()
    show_text.assert_not_called()


@pytest.mark.parametrize("density, expected_size", [("standard", 24), ("compact", 20)])
def test_help_hint_uses_theme_override_and_density(
    qapp: QApplication, density: str, expected_size: int
) -> None:
    custom = replace(
        ALPACA_LIGHT,
        density=density,  # type: ignore[arg-type]
        colors=replace(ALPACA_LIGHT.colors, info="#0F766E"),
    )
    install_theme(qapp, custom)

    hint = HelpHint("Translated explanation — こんにちは")

    assert hint.minimumSize().width() == expected_size
    assert "#0F766E" in hint.styleSheet()


def test_help_hint_native_popup_smoke_and_escape(qtbot) -> None:
    hint = HelpHint("Native popup help")
    qtbot.addWidget(hint)
    hint.show()

    hint.click()
    qtbot.wait(10)
    qtbot.keyClick(hint, Qt.Key.Key_Escape)
    QWhatsThis.leaveWhatsThisMode()
