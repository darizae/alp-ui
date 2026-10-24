from __future__ import annotations

import pytest
from PySide6.QtCore import QRegularExpression, QStringListModel, Qt
from PySide6.QtGui import QColor, QPalette, QRegularExpressionValidator
from PySide6.QtTest import QSignalSpy
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QCompleter,
    QDoubleSpinBox,
    QFileDialog,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from alp_ui.components import CheckBox, FolderPicker, NumberInput, SelectInput, Switch, TextInput
from alp_ui.theme import ALPACA_LIGHT, install_theme


@pytest.fixture(autouse=True)
def _install_default_theme(qapp: QApplication) -> None:
    install_theme(qapp)


def test_text_input_associates_label_help_error_and_focus() -> None:
    field = TextInput(
        label="&Name",
        description="Shown in exports",
        error="A name is required",
        placeholder="Ada Lovelace",
    )

    assert isinstance(field.control, QLineEdit)
    assert field.label_widget.buddy() is field.control
    assert field.control.accessibleName() == "Name"
    assert field.control.accessibleDescription() == "Shown in exports Error: A name is required"
    assert field.control.parent() is field
    assert field.control.property("invalid") is True
    assert field.error_widget.isVisibleTo(field)
    assert field.focusProxy() is field.control
    assert field.placeholderText() == "Ada Lovelace"

    field.setErrorText("")
    assert not field.error_widget.isVisibleTo(field)
    assert field.control.property("invalid") is False
    assert field.control.accessibleDescription() == "Shown in exports"


def test_text_input_emits_only_native_text_and_keyboard_finish_signals(qtbot) -> None:
    field = TextInput()
    qtbot.addWidget(field)
    field.show()
    field.activateWindow()
    field.control.setFocus()
    qtbot.waitUntil(field.control.hasFocus)
    changed = QSignalSpy(field.textChanged)
    finished = QSignalSpy(field.editingFinished)

    field.setText("hello")
    qtbot.keyClick(field.control, Qt.Key.Key_Return)

    assert changed.count() == 1
    assert finished.count() == 1
    assert field.text() == "hello"


def test_text_input_forwards_native_validation_mask_and_completion() -> None:
    validator = QRegularExpressionValidator(QRegularExpression(r"[A-Z]{2}\d{2}"))
    completer = QCompleter(["AB12", "CD34"])
    field = TextInput(validator=validator, completer=completer)

    field.setText("AB12")
    assert field.hasAcceptableInput()
    field.setText("invalid")
    assert not field.hasAcceptableInput()
    assert field.validator() is validator
    assert field.completer() is completer

    field.setInputMask("000-000;_")
    field.setValidator(None)
    field.setText("123456")
    assert field.inputMask() == "000-000;_"
    assert field.text() == "123-456"


def test_folder_picker_preserves_paths_accessibility_and_change_signal() -> None:
    picker = FolderPicker(label="&Folder")
    changed = QSignalSpy(picker.folderChanged)
    path = "C:\\Users\\Ada\\音楽\\a very long folder name"

    assert isinstance(picker.control, QLineEdit)
    assert picker.control.isReadOnly()
    assert picker.control.parent() is picker
    assert picker.choose_button.parent() is picker
    assert picker.label_widget.buddy() is picker.control
    assert picker.control.accessibleName() == "Folder"
    assert picker.choose_button.accessibleName() == "Choose Folder"
    assert picker.folderPath() == ""
    assert FolderPicker().choose_button.accessibleName() == "Choose folder"

    picker.setFolderPath(path)
    picker.setFolderPath(path)

    assert picker.folderPath() == path
    assert picker.control.text() == path
    assert picker.control.accessibleDescription() == path
    assert picker.control.toolTip() == path
    assert changed.count() == 1
    assert changed.at(0) == [path]


def test_folder_picker_uses_native_dialog_and_keeps_path_on_cancel(qtbot, monkeypatch) -> None:
    picker = FolderPicker(label="Folder")
    qtbot.addWidget(picker)
    picker.show()
    selected = "/tmp/selected folder"
    calls: list[tuple[object, ...]] = []

    def choose_directory(*args):
        calls.append(args)
        return selected

    monkeypatch.setattr(QFileDialog, "getExistingDirectory", choose_directory)
    changed = QSignalSpy(picker.folderChanged)
    picker.choose_button.setFocus()
    picker.activateWindow()
    qtbot.waitUntil(picker.choose_button.hasFocus)
    qtbot.keyClick(picker.choose_button, Qt.Key.Key_Return)

    assert calls
    assert calls[0][0] is picker
    assert calls[0][3] == QFileDialog.Option.ShowDirsOnly
    assert picker.folderPath() == selected
    assert changed.count() == 1

    picker.choose_button.click()
    assert picker.folderPath() == selected
    assert changed.count() == 1
    assert calls[1][2] == selected

    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda *_: "")
    picker.choose_button.click()
    assert picker.folderPath() == selected
    assert changed.count() == 1

    picker.choose_button.setEnabled(False)
    picker.choose_button.click()
    assert picker.folderPath() == selected


def test_number_input_uses_native_type_specific_controls(qtbot) -> None:
    integer = NumberInput(
        kind="integer",
        value=2,
        minimum=1,
        maximum=8,
        step=2,
        label="Count",
    )
    decimal = NumberInput(
        kind="decimal",
        value=1.25,
        minimum=0.0,
        maximum=2.0,
        step=0.25,
        decimals=2,
        label="Price",
    )

    assert isinstance(integer.control, QSpinBox)
    assert integer.value() == 2
    assert integer.singleStep() == 2
    integer_changed = QSignalSpy(integer.valueChanged)
    qtbot.keyClick(integer.control, Qt.Key.Key_Up)
    assert integer.value() == 4
    assert integer_changed.count() == 1
    assert isinstance(decimal.control, QDoubleSpinBox)
    assert decimal.value() == 1.25
    assert decimal.control.decimals() == 2

    changed = QSignalSpy(decimal.valueChanged)
    decimal.setValue(1.5)
    assert changed.count() == 1


def test_number_input_rejects_invalid_public_options() -> None:
    with pytest.raises(ValueError, match="kind must be one of"):
        NumberInput(kind="currency")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="minimum must not exceed maximum"):
        NumberInput(minimum=2, maximum=1)
    with pytest.raises(ValueError, match="step must be positive"):
        NumberInput(step=0)
    with pytest.raises(ValueError, match="decimals must not be negative"):
        NumberInput(kind="decimal", decimals=-1)


def test_select_input_preserves_items_models_and_keyboard_signal(qtbot) -> None:
    field = SelectInput(("First", "Second"), label="Choice")
    qtbot.addWidget(field)
    field.show()
    field.activateWindow()
    field.control.setFocus()
    qtbot.waitUntil(field.control.hasFocus)
    changed = QSignalSpy(field.currentIndexChanged)

    qtbot.keyClick(field.control, Qt.Key.Key_Down)

    assert changed.count() == 1
    assert field.currentText() == "Second"

    model = QStringListModel(["North", "South"])
    field.setModel(model)
    assert field.model() is model
    assert field.currentText() == "North"


def test_checkbox_preserves_keyboard_signal_and_disabled_behavior(qtbot) -> None:
    checkbox = CheckBox("Enable summaries")
    qtbot.addWidget(checkbox)
    checkbox.show()
    checkbox.setFocus()
    toggled = QSignalSpy(checkbox.toggled)

    qtbot.keyClick(checkbox, Qt.Key.Key_Space)
    assert toggled.count() == 1
    assert checkbox.isChecked()

    checkbox.setEnabled(False)
    qtbot.keyClick(checkbox, Qt.Key.Key_Space)
    assert toggled.count() == 1
    assert checkbox.accessibleName() == "Enable summaries"


def test_switch_uses_native_checkbox_state_keyboard_and_accessibility(qtbot) -> None:
    switch = Switch("Enable summaries")
    qtbot.addWidget(switch)
    switch.show()
    switch.activateWindow()
    switch.setFocus()
    qtbot.waitUntil(switch.hasFocus)
    toggled = QSignalSpy(switch.toggled)

    qtbot.keyClick(switch, Qt.Key.Key_Space)

    assert isinstance(switch, QCheckBox)
    assert switch.isChecked()
    assert toggled.count() == 1
    assert switch.accessibleName() == "Enable summaries"
    assert switch.sizeHint().width() > switch.sizeHint().height()
    with pytest.raises(ValueError, match="two states only"):
        switch.setTristate(True)

    switch.setEnabled(False)
    qtbot.keyClick(switch, Qt.Key.Key_Space)
    assert toggled.count() == 1


def test_field_tab_order_and_disabled_state(qtbot) -> None:
    window = QWidget()
    layout = QVBoxLayout(window)
    first = TextInput(label="First")
    second = SelectInput(("A", "B"), label="Second")
    layout.addWidget(first)
    layout.addWidget(second)
    qtbot.addWidget(window)
    window.show()
    window.activateWindow()
    first.control.setFocus()
    qtbot.waitUntil(first.control.hasFocus)

    qtbot.keyClick(first.control, Qt.Key.Key_Tab)

    qtbot.waitUntil(second.control.hasFocus)
    second.setEnabled(False)
    assert not second.control.isEnabled()


def test_long_label_wraps_and_controls_use_theme_tokens() -> None:
    field = TextInput(label="A translated and intentionally very long field label " * 3)

    assert field.label_widget.wordWrap()
    assert field.control.palette().color(QPalette.ColorRole.Base) == QColor(
        ALPACA_LIGHT.colors.surface
    )
    assert ALPACA_LIGHT.colors.border in field.control.styleSheet()
