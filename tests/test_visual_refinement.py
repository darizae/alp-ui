"""Behavior checks for the visual pass; run on the actual Qt runtime."""

from __future__ import annotations

from dataclasses import replace

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QSpinBox,
    QStyle,
    QStyleOptionSpinBox,
)

from alp_ui.components import (
    Button,
    Card,
    CheckBox,
    DataTable,
    NumberInput,
    SelectInput,
    Switch,
    Text,
    TextInput,
)
from alp_ui.theme import (
    ALPACA_LIGHT,
    install_theme,
    interactions,
    make_icon,
)
from alp_ui.theme.appearance import density_metrics
from gallery.showcase import build_showcase


def test_compact_density_follows_theme_without_shrinking_font(qapp: QApplication) -> None:
    compact = replace(ALPACA_LIGHT, density="compact")
    install_theme(qapp, compact)
    field, numeric = TextInput(label="Name"), NumberInput(label="Count")
    select = SelectInput(["One", "Two"], label="Choice")
    button, table, card = Button("Save"), DataTable(), Card(shadow=False)
    assert field.control.minimumHeight() == 34
    assert numeric.control.minimumHeight() == 34
    assert select.control.minimumHeight() == 34
    assert button.minimumHeight() == 34
    assert table.verticalHeader().defaultSectionSize() == 36
    assert card.content_layout.contentsMargins().left() == 16
    assert qapp.font().pointSizeF() == ALPACA_LIGHT.typography.body_size
    install_theme(qapp)


def test_standard_density_defaults_remain_stable(qapp: QApplication) -> None:
    install_theme(qapp)
    assert density_metrics(ALPACA_LIGHT).card_padding == 24
    assert Button("Save").minimumHeight() == 40
    assert TextInput().control.minimumHeight() == 40
    assert DataTable().verticalHeader().defaultSectionSize() == 44


def test_interactions_are_shared_and_overridable(qapp: QApplication) -> None:
    custom = replace(
        ALPACA_LIGHT,
        colors=replace(ALPACA_LIGHT.colors, primary="#0F766E"),
    )
    assert interactions(custom).selected_surface != interactions(ALPACA_LIGHT).selected_surface
    assert interactions(ALPACA_LIGHT).primary_pressed == "#056C52"
    assert interactions(ALPACA_LIGHT).danger_hover == "#B92327"
    special = replace(custom, interaction=replace(interactions(custom), focus="#8B5CF6"))
    install_theme(qapp, special)
    fields = (TextInput(), NumberInput(), SelectInput())
    for field in fields:
        assert "#8B5CF6" in field.control.styleSheet()
        assert "border: 2px" not in field.control.styleSheet()
    assert "#8B5CF6" in Button("Save").styleSheet()
    install_theme(qapp)


def test_native_form_subcontrols_still_exist(qapp: QApplication, qtbot) -> None:
    install_theme(qapp)
    count = NumberInput(value=2, minimum=0, maximum=10)
    amount = NumberInput(kind="decimal", value=2.5)
    choice = SelectInput(["A", "B"])
    for field in (count, amount, choice):
        qtbot.addWidget(field)
        field.show()
        assert field.control.focusPolicy() != Qt.FocusPolicy.NoFocus
        assert field.control.grab().isNull() is False
    assert isinstance(count.control, QSpinBox)
    assert isinstance(amount.control, QDoubleSpinBox)
    assert isinstance(choice.control, QComboBox)
    count.control.setFocus()
    QTest.keyClick(count.control, Qt.Key.Key_Up)
    assert count.value() == 3
    choice.setCurrentIndex(1)
    assert choice.currentText() == "B"


def test_native_form_subcontrols_handle_mouse_and_rtl(qapp: QApplication, qtbot) -> None:
    install_theme(qapp)
    count = NumberInput(value=5, minimum=0, maximum=10)
    choice = SelectInput(["A", "B"])
    for field in (count, choice):
        qtbot.addWidget(field)
        field.resize(240, field.sizeHint().height())
        field.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        field.show()

    option = QStyleOptionSpinBox()
    count.control.initStyleOption(option)
    up = count.control.style().subControlRect(
        QStyle.ComplexControl.CC_SpinBox,
        option,
        QStyle.SubControl.SC_SpinBoxUp,
        count.control,
    )
    down = count.control.style().subControlRect(
        QStyle.ComplexControl.CC_SpinBox,
        option,
        QStyle.SubControl.SC_SpinBoxDown,
        count.control,
    )
    assert up.center().x() < count.control.width() / 2
    qtbot.mouseClick(count.control, Qt.MouseButton.LeftButton, pos=up.center())
    assert count.value() == 6
    qtbot.mouseClick(count.control, Qt.MouseButton.LeftButton, pos=down.center())
    assert count.value() == 5

    choice.control.showPopup()
    assert choice.control.view().isVisible()
    choice.control.hidePopup()


def test_check_and_switch_keep_native_states(qapp: QApplication, qtbot) -> None:
    install_theme(qapp)
    checked = CheckBox("Enabled")
    toggle = Switch("Active")
    for control in (checked, toggle):
        qtbot.addWidget(control)
        control.show()
        control.setFocus()
        QTest.keyClick(control, Qt.Key.Key_Space)
        assert control.isChecked()
        assert not control.grab().isNull()


def test_typography_and_original_icons(qapp: QApplication) -> None:
    install_theme(qapp)
    title = Text("Dashboard", role="title")
    section = Text("Section", role="subheading")
    caption = Text("Info", role="caption")
    assert title.font().pointSizeF() > section.font().pointSizeF() > caption.font().pointSizeF()
    for name in ("grid", "folder", "list", "settings", "plus", "search", "info", "check"):
        icon = make_icon(name, color=ALPACA_LIGHT.colors.primary)
        assert not icon.pixmap(20, 20).isNull()


def test_refinement_tokens_and_icons_reject_invalid_values(qapp: QApplication) -> None:
    with pytest.raises(ValueError, match="density must be"):
        replace(ALPACA_LIGHT, density="dense")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match=r"interaction\.focus"):
        replace(interactions(ALPACA_LIGHT), focus="blue")
    with pytest.raises(ValueError, match="unsupported icon"):
        make_icon("unknown")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least 12"):
        make_icon("check", size=8)
    with pytest.raises(ValueError, match="Qt-valid color"):
        make_icon("check", color="")


def test_composed_showcase_is_independent(qapp: QApplication) -> None:
    install_theme(qapp, replace(ALPACA_LIGHT, density="compact"))
    window = build_showcase()
    assert window.objectName() == "applicationShowcase"
    assert len(window.findChildren(Card)) == 1
    assert len(window.findChildren(DataTable)) == 1
    assert window.findChildren(DataTable)[0].model().rowCount() == 5
    assert len(window.findChildren(TextInput)) >= 2
    window.close()
    install_theme(qapp)
