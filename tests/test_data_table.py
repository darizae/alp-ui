from __future__ import annotations

import pytest
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtTest import QSignalSpy
from PySide6.QtWidgets import QApplication, QHeaderView, QStyleOptionHeader, QWidget

from python_ui_library.components import DataTable
from python_ui_library.theme import ALPACA_LIGHT, install_theme


class _TableModel(QAbstractTableModel):
    def __init__(self, rows: list[list[str]]) -> None:
        super().__init__()
        self._rows = rows

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else 2

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return self._rows[index.row()][index.column()]
        return None

    def headerData(  # noqa: N802
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ("Name", "Value")[section]
        return None

    def set_name(self, row: int, name: str) -> None:
        self._rows[row][0] = name
        index = self.index(row, 0)
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])

    def replace_rows(self, rows: list[list[str]]) -> None:
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()


class _LargeModel(QAbstractTableModel):
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else 10_000

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else 3

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return f"{index.row()}:{index.column()}"
        return None


@pytest.fixture(autouse=True)
def _install_default_theme(qapp: QApplication) -> None:
    install_theme(qapp)


def test_data_table_uses_and_replaces_caller_models_without_copying() -> None:
    first = _TableModel([["Alpha", "1"]])
    second = _TableModel([["Beta", "2"], ["Gamma", "3"]])
    table = DataTable(model=first)

    assert table.model() is first
    table.setModel(second)
    assert table.model() is second
    assert table.model().rowCount() == 2
    assert not table.isSortingEnabled()
    assert not table.horizontalHeader().sectionsMovable()


def test_data_table_honors_data_changes_resets_selection_and_keyboard(qtbot) -> None:
    model = _TableModel([["Alpha", "1"], ["Beta", "2"]])
    table = DataTable(model=model)
    qtbot.addWidget(table)
    table.show()
    table.setCurrentIndex(model.index(0, 0))
    table.setFocus()
    changed = QSignalSpy(model.dataChanged)
    reset = QSignalSpy(model.modelReset)

    model.set_name(0, "Updated")
    assert changed.count() == 1
    assert table.model().data(table.model().index(0, 0)) == "Updated"

    table.selectRow(1)
    assert {index.row() for index in table.selectionModel().selectedIndexes()} == {1}
    table.setCurrentIndex(model.index(0, 0))
    qtbot.keyClick(table, Qt.Key.Key_Down)
    assert table.currentIndex().row() == 1

    model.replace_rows([])
    assert reset.count() == 1
    assert table.model() is model
    assert table.model().rowCount() == 0


def test_large_model_scrolls_without_per_cell_widgets(qtbot) -> None:
    model = _LargeModel()
    table = DataTable(model=model)
    table.resize(480, 240)
    qtbot.addWidget(table)
    table.show()
    qtbot.waitUntil(lambda: table.verticalScrollBar().maximum() > 0)

    assert table.model() is model
    assert table.model().rowCount() == 10_000
    assert table.verticalScrollBar().maximum() > 0
    for row in (0, 4_999, 9_999):
        assert table.indexWidget(model.index(row, 0)) is None
    assert len(table.findChildren(QWidget)) < 30

    table.scrollToBottom()
    assert table.verticalScrollBar().value() == table.verticalScrollBar().maximum()


def test_header_uses_theme_and_uppercase_presentation() -> None:
    model = _TableModel([["Alpha", "1"]])
    table = DataTable(model=model)
    header = table.horizontalHeader()
    option = QStyleOptionHeader()

    header.initStyleOptionForIndex(option, 0)

    assert isinstance(header, QHeaderView)
    assert option.text == "NAME"
    assert header.palette().color(QPalette.ColorRole.Button) == QColor(
        ALPACA_LIGHT.colors.background
    )
    assert header.palette().color(QPalette.ColorRole.ButtonText) == QColor(
        ALPACA_LIGHT.colors.text_muted
    )
    assert header.sectionResizeMode(0) == QHeaderView.ResizeMode.Interactive
    assert table.accessibleName() == "Data table"
