"""Minimal application consuming alp-ui from an installed wheel."""

from __future__ import annotations

import argparse
import sys
from dataclasses import replace

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from alp_ui.components import Badge, Button, DataTable, TextInput
from alp_ui.theme import ALPACA_LIGHT, install_theme


class ExampleModel(QAbstractTableModel):
    """Small caller-owned model used directly by DataTable."""

    _rows = (("Alpha", "1"), ("Beta", "2"), ("Gamma", "3"))

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
            return ("Item", "Value")[section]
        return None


def build_window() -> QWidget:
    """Compose public Components with ordinary Qt layout and signal APIs."""

    window = QWidget()
    window.setWindowTitle("alp-ui consumer")
    window.setAccessibleName("Installed wheel consumer example")
    window.resize(520, 420)

    layout = QVBoxLayout(window)
    name = TextInput(label="Name", placeholder="Enter a name")
    status = Badge("Ready", intent="success")
    save = Button("Save")
    table = DataTable(model=ExampleModel(window))
    table.setAccessibleName("Example items")

    def save_name() -> None:
        status.setText(f"Saved {name.text()}")
        status.setAccessibleName(status.text())

    name.textChanged.connect(lambda text: save.setEnabled(bool(text.strip())))
    save.clicked.connect(save_name)
    save.setEnabled(False)

    for widget in (name, status, save, table):
        layout.addWidget(widget)
    return window


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--custom-theme",
        action="store_true",
        help="demonstrate a startup semantic color override",
    )
    parser.add_argument("--smoke", action="store_true", help="open and close automatically")
    options = parser.parse_args(argv)

    app = QApplication(sys.argv[:1])
    theme = ALPACA_LIGHT
    if options.custom_theme:
        theme = replace(theme, colors=replace(theme.colors, primary="#0F766E"))
    install_theme(app, theme)

    window = build_window()
    window.show()
    if options.smoke:
        QTimer.singleShot(0, app.quit)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
