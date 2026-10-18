"""Surface and separator components."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from python_ui_library.theme.appearance import density_metrics
from python_ui_library.theme.install import _current_theme


class Card(QFrame):
    """A bordered surface with a ready-to-use padded vertical layout."""

    def __init__(self, parent: QWidget | None = None, *, shadow: bool = True) -> None:
        if type(shadow) is not bool:
            raise TypeError("shadow must be a bool")

        super().__init__(parent)
        theme = _current_theme()
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(*(density_metrics(theme).card_padding,) * 4)
        self.content_layout.setSpacing(theme.spacing.medium)
        # Local QSS is the smallest reliable way to retain a rounded one-pixel border.
        self.setStyleSheet(
            f"""
            Card {{
                background-color: {theme.colors.surface};
                border: 1px solid {theme.colors.border};
                border-radius: {theme.radii.default}px;
            }}
            """
        )
        if shadow:
            effect = QGraphicsDropShadowEffect(self)
            shadow_color = QColor(theme.colors.shadow)
            shadow_color.setAlphaF(0.08)
            effect.setColor(shadow_color)
            effect.setBlurRadius(3.0)
            effect.setOffset(0.0, 1.0)
            self.setGraphicsEffect(effect)


class Divider(QFrame):
    """Native horizontal or vertical separator using the Theme border token."""

    def __init__(
        self,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        parent: QWidget | None = None,
    ) -> None:
        if orientation not in (Qt.Orientation.Horizontal, Qt.Orientation.Vertical):
            raise ValueError("orientation must be Qt.Horizontal or Qt.Vertical")

        super().__init__(parent)
        self.orientation = orientation
        self.setFrameShape(
            QFrame.Shape.HLine if orientation == Qt.Orientation.Horizontal else QFrame.Shape.VLine
        )
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(1)
        if orientation == Qt.Orientation.Horizontal:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        else:
            self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        border = QColor(_current_theme().colors.border)
        palette = self.palette()
        for role in (
            QPalette.ColorRole.WindowText,
            QPalette.ColorRole.Mid,
            QPalette.ColorRole.Dark,
            QPalette.ColorRole.Light,
            QPalette.ColorRole.Shadow,
        ):
            palette.setColor(role, border)
        self.setPalette(palette)
