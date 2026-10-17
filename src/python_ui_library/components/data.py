"""Model/view components that keep consumer data in native Qt models."""

from __future__ import annotations

from PySide6.QtCore import QAbstractItemModel, Qt
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication, QHeaderView, QStyleOptionHeader, QTableView, QWidget

from python_ui_library.theme.install import _METADATA_FONT_PROPERTY, _current_theme


class _TableHeader(QHeaderView):
    """Native horizontal header with uppercase presentation-only labels."""

    def initStyleOptionForIndex(  # noqa: N802
        self, option: QStyleOptionHeader, logical_index: int
    ) -> None:
        super().initStyleOptionForIndex(option, logical_index)
        option.text = option.text.upper()


class DataTable(QTableView):
    """Themed QTableView that displays a caller-provided QAbstractItemModel."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        model: QAbstractItemModel | None = None,
    ) -> None:
        super().__init__(parent)
        theme = _current_theme()
        colors = theme.colors

        header = _TableHeader(Qt.Orientation.Horizontal, self)
        self.setHorizontalHeader(header)
        header.setAccessibleName("Table columns")
        self.verticalHeader().hide()

        app = QApplication.instance()
        resolved = app.property(_METADATA_FONT_PROPERTY) if isinstance(app, QApplication) else None
        header_font = QFont(header.font())
        header_font.setFamily(
            resolved if isinstance(resolved, str) else theme.typography.metadata_family
        )
        header_font.setPointSizeF(theme.typography.overline_size)
        header_font.setWeight(QFont.Weight(theme.typography.button_weight))
        header_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 106.0)
        header.setFont(header_font)

        header_palette = header.palette()
        header_palette.setColor(QPalette.ColorRole.Button, QColor(colors.background))
        header_palette.setColor(QPalette.ColorRole.Window, QColor(colors.background))
        header_palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors.text_muted))
        header_palette.setColor(QPalette.ColorRole.WindowText, QColor(colors.text_muted))
        header.setPalette(header_palette)
        header.setStyleSheet(
            f"""
            QHeaderView::section {{
                background-color: {colors.background};
                color: {colors.text_muted};
                border: 0;
                border-right: 1px solid {colors.border};
                border-bottom: 1px solid {colors.border};
                padding: {theme.spacing.small}px;
            }}
            """
        )

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(colors.surface))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors.background))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors.text))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors.primary))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors.on_primary))
        self.setPalette(palette)
        self.setStyleSheet(
            f"""
            DataTable {{
                background-color: {colors.surface};
                color: {colors.text};
                border: 1px solid {colors.border};
                gridline-color: {colors.border};
            }}
            DataTable::item:focus {{
                border: 1px solid {colors.info};
            }}
            """
        )
        self.verticalHeader().setDefaultSectionSize(
            self.fontMetrics().height() + 2 * theme.spacing.medium
        )
        self.setAccessibleName("Data table")

        if model is not None:
            self.setModel(model)
