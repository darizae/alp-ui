"""Composed, realistic consumer-style screen; not a public navigation framework."""

from __future__ import annotations

import sys
from dataclasses import replace

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from alp_ui.components import (
    Badge,
    Button,
    Card,
    CheckBox,
    DataTable,
    Divider,
    NumberInput,
    SelectInput,
    Text,
    TextInput,
)
from alp_ui.theme import ALPACA_LIGHT, install_theme, interactions, make_icon


class _RecordsModel(QAbstractTableModel):
    """Small, model-owned demonstration data, independent of application concepts."""

    _records = (
        ("Release summary", "Documents", "Ready", "Today"),
        ("Component audit", "Design", "In review", "Yesterday"),
        ("Accessibility pass", "Quality", "Ready", "16 Oct"),
        ("Layout research", "Design", "Draft", "14 Oct"),
        ("Consumer example", "Documents", "Ready", "12 Oct"),
    )

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._records)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else 4

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return self._records[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):  # noqa: N802
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return ("NAME", "CATEGORY", "STATUS", "UPDATED")[section]
        return None


def _nav_item(text: str, icon_name: str, *, selected: bool) -> QPushButton:
    colors = ALPACA_LIGHT.colors
    nav = QPushButton(text)
    nav.setIcon(make_icon(icon_name, color=colors.primary if selected else colors.text_muted))
    nav.setCursor(Qt.CursorShape.PointingHandCursor)
    nav.setAccessibleName(f"{text} navigation")
    nav.setMinimumHeight(38)
    selected_surface = interactions(ALPACA_LIGHT).selected_surface
    nav.setStyleSheet(f"""
        QPushButton {{
            text-align: left;
            background: {(selected_surface if selected else "transparent")};
            color: {(colors.primary_hover if selected else colors.text_muted)};
            border: 0; border-radius: 8px;
            padding: 0 14px;
            font-weight: {600 if selected else 400};
        }}
        QPushButton:hover {{
            background: {selected_surface};
            color: {colors.primary_hover};
        }}
        QPushButton:focus {{ border: 1px solid {colors.info}; }}
    """)
    return nav


def _sidebar() -> QWidget:
    sidebar = QFrame()
    sidebar.setFixedWidth(220)
    sidebar.setObjectName("showcaseSidebar")
    sidebar.setStyleSheet(f"""
        QFrame#showcaseSidebar {{ background: {ALPACA_LIGHT.colors.surface};
                 border-right: 1px solid {ALPACA_LIGHT.colors.border}; }}
    """)
    layout = QVBoxLayout(sidebar)
    layout.setContentsMargins(18, 27, 18, 18)
    layout.setSpacing(7)
    logo = QHBoxLayout()
    brand_icon = QLabel()
    brand_icon.setPixmap(
        make_icon("grid", color=ALPACA_LIGHT.colors.primary, size=25).pixmap(25, 25)
    )
    logo.addWidget(brand_icon)
    logo.addWidget(Text("STUDIO", role="subheading"))
    logo.addStretch()
    layout.addLayout(logo)
    layout.addSpacing(34)
    for label, name, selected in (
        ("Overview", "grid", True),
        ("Records", "folder", False),
        ("Activity", "list", False),
        ("Preferences", "settings", False),
    ):
        layout.addWidget(_nav_item(label, name, selected=selected))
    layout.addStretch()
    layout.addWidget(Divider())
    caption = Text("Theme · Alpaca Light", role="caption")
    layout.addWidget(caption)
    return sidebar


def build_showcase() -> QWidget:
    """An ordinary application may compose these widgets without a special shell."""
    w = QWidget()
    w.setWindowTitle("alp-ui — application showcase")
    w.setObjectName("applicationShowcase")
    w.setAccessibleName("Composed application showcase")
    w.resize(1180, 790)
    main = QHBoxLayout(w)
    main.setContentsMargins(0, 0, 0, 0)
    main.setSpacing(0)
    main.addWidget(_sidebar())

    body = QWidget()
    outer = QVBoxLayout(body)
    outer.setContentsMargins(38, 30, 38, 30)
    outer.setSpacing(20)
    header = QHBoxLayout()
    heading = QVBoxLayout()
    heading.setSpacing(3)
    heading.addWidget(Text("Overview", role="title"))
    heading.addWidget(Text("Organize your work in one place.", role="caption"))
    header.addLayout(heading)
    header.addStretch()
    status = Badge("All systems ready", intent="success")
    header.addWidget(status)
    header.addSpacing(12)
    new_button = Button("New record", size="medium")
    new_button.setIcon(make_icon("plus", color=ALPACA_LIGHT.colors.on_primary))
    header.addWidget(new_button)
    outer.addLayout(header)
    outer.addSpacing(8)

    section_title = QHBoxLayout()
    section_title.addWidget(Text("Quick settings", role="subheading"))
    section_title.addStretch()
    section_title.addWidget(Text("Edit your defaults", role="caption"))
    outer.addLayout(section_title)
    form = Card(shadow=False)
    fields = QHBoxLayout()
    fields.setSpacing(16)
    title = TextInput(label="Workspace name", text="My workspace", placeholder="Enter a name")
    group = SelectInput(["Personal", "Team", "Shared"], label="Visibility")
    limit = NumberInput(kind="integer", value=12, minimum=1, maximum=100, label="Items per page")
    fields.addWidget(title, 3)
    fields.addWidget(group, 2)
    fields.addWidget(limit, 2)
    form.content_layout.addLayout(fields)
    footer = QHBoxLayout()
    footer.addWidget(CheckBox("Enable notifications"))
    footer.addStretch()
    footer.addWidget(Button("Cancel", variant="secondary", size="small"))
    footer.addWidget(Button("Save changes", size="small"))
    form.content_layout.addLayout(footer)
    outer.addWidget(form)
    outer.addSpacing(12)

    table_header = QHBoxLayout()
    table_header.addWidget(Text("Recent records", role="subheading"))
    table_header.addStretch()
    query = TextInput(placeholder="Search records…")
    query.control.setAccessibleName("Search records")
    query.setMaximumWidth(245)
    table_header.addWidget(query)
    table_header.addWidget(Button("View all", variant="outline", size="small"))
    outer.addLayout(table_header)
    table = DataTable()
    table.setAccessibleName("Recent records")
    model = _RecordsModel(table)
    table.setModel(model)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.setAlternatingRowColors(False)
    table.setMinimumHeight(230)
    table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    outer.addWidget(table)
    outer.addStretch(1)
    main.addWidget(body, 1)
    # Hold Python model reference; Qt parent also owns its lifetime.
    w._records_model = model
    return w


def main() -> int:
    app = QApplication(sys.argv)
    install_theme(app, replace(ALPACA_LIGHT, density="compact"))
    window = build_showcase()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
