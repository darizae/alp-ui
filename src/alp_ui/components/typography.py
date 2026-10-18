"""Semantic text built on QLabel."""

from __future__ import annotations

from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication, QLabel, QWidget

from alp_ui.theme.install import _METADATA_FONT_PROPERTY, _current_theme

TextRole = Literal["title", "heading", "subheading", "body", "caption", "overline"]
_ROLES = ("title", "heading", "subheading", "body", "caption", "overline")


class Text(QLabel):
    """QLabel with a bounded semantic typography role."""

    def __init__(
        self,
        text: str = "",
        parent: QWidget | None = None,
        *,
        role: TextRole = "body",
        selectable: bool = False,
        word_wrap: bool = False,
    ) -> None:
        if role not in _ROLES:
            choices = ", ".join(_ROLES)
            raise ValueError(f"role must be one of: {choices}")

        super().__init__(text, parent)
        self.role: TextRole = role
        self.setWordWrap(word_wrap)

        theme = _current_theme()
        typography = theme.typography
        if role == "title":
            family, size, weight = (
                typography.body_family,
                typography.title_size,
                typography.heading_weight,
            )
        elif role == "subheading":
            family, size, weight = (
                typography.body_family,
                typography.subheading_size,
                typography.button_weight,
            )
        elif role == "caption":
            family, size, weight = (
                typography.body_family,
                typography.caption_size,
                typography.body_weight,
            )
        elif role == "heading":
            family, size, weight = (
                typography.body_family,
                typography.heading_size,
                typography.heading_weight,
            )
        elif role == "overline":
            family, size, weight = (
                typography.metadata_family,
                typography.overline_size,
                typography.metadata_weight,
            )
        else:
            family, size, weight = (
                typography.body_family,
                typography.body_size,
                typography.body_weight,
            )

        font = QFont(self.font())
        if role == "overline":
            app = QApplication.instance()
            resolved = (
                app.property(_METADATA_FONT_PROPERTY) if isinstance(app, QApplication) else None
            )
            font.setFamily(resolved if isinstance(resolved, str) else family)
        font.setPointSizeF(size)
        font.setWeight(QFont.Weight(weight))
        if role in ("title", "heading"):
            font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 98.0)
        elif role == "overline":
            font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 108.0)
        self.setFont(font)

        palette = self.palette()
        color = theme.colors.text_muted if role in ("caption", "overline") else theme.colors.text
        palette.setColor(QPalette.ColorRole.WindowText, QColor(color))
        self.setPalette(palette)

        if selectable:
            self.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
                | Qt.TextInteractionFlag.TextSelectableByKeyboard
            )
