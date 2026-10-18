"""Generic feedback components built from native Qt Widgets."""

from __future__ import annotations

from typing import Literal

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from alp_ui.theme.appearance import interactions
from alp_ui.theme.install import _METADATA_FONT_PROPERTY, _current_theme

Intent = Literal["neutral", "info", "success", "warning", "danger"]
_INTENTS = ("neutral", "info", "success", "warning", "danger")


def _validate_intent(intent: str) -> None:
    if intent not in _INTENTS:
        choices = ", ".join(_INTENTS)
        raise ValueError(f"intent must be one of: {choices}")


def _intent_colors(intent: Intent) -> tuple[str, str]:
    theme = _current_theme()
    colors = theme.colors
    state = interactions(theme)
    if intent == "neutral":
        return colors.border, colors.background
    return getattr(colors, intent), getattr(state, f"feedback_{intent}")


def _metadata_font(widget: QWidget) -> QFont:
    theme = _current_theme()
    font = QFont(widget.font())
    app = QApplication.instance()
    resolved = app.property(_METADATA_FONT_PROPERTY) if isinstance(app, QApplication) else None
    font.setFamily(resolved if isinstance(resolved, str) else theme.typography.metadata_family)
    font.setPointSizeF(theme.typography.overline_size)
    font.setWeight(QFont.Weight(theme.typography.metadata_weight))
    return font


class Badge(QLabel):
    """Compact text label with a generic semantic intent."""

    def __init__(
        self,
        text: str = "",
        parent: QWidget | None = None,
        *,
        intent: Intent = "neutral",
    ) -> None:
        _validate_intent(intent)
        super().__init__(text, parent)
        self.intent: Intent = intent

        theme = _current_theme()
        accent, background = _intent_colors(intent)
        self.setFont(_metadata_font(self))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.setAccessibleName(text)
        self.setAccessibleDescription(f"{intent.capitalize()} intent")
        # Local QSS provides the compact rounded badge shape across native styles.
        self.setStyleSheet(
            f"""
            Badge {{
                background-color: {background};
                color: {theme.colors.text};
                border: 1px solid {accent};
                border-radius: {theme.radii.feedback}px;
                padding: {theme.spacing.xsmall // 2}px {theme.spacing.small}px;
            }}
            """
        )


class Alert(QFrame):
    """Text feedback with an optional title and consumer-supplied action widget."""

    def __init__(
        self,
        text: str,
        parent: QWidget | None = None,
        *,
        title: str = "",
        intent: Intent = "neutral",
        action: QWidget | None = None,
    ) -> None:
        _validate_intent(intent)
        super().__init__(parent)
        self.intent: Intent = intent
        self.title_widget = QLabel(title, self)
        self.text_widget = QLabel(text, self)
        self.action_widget = action

        theme = _current_theme()
        accent, background = _intent_colors(intent)
        title_font = QFont(self.title_widget.font())
        title_font.setWeight(QFont.Weight(theme.typography.button_weight))
        self.title_widget.setFont(title_font)
        self.title_widget.setVisible(bool(title))
        self.title_widget.setWordWrap(True)
        self.text_widget.setWordWrap(True)

        for label in (self.title_widget, self.text_widget):
            palette = label.palette()
            palette.setColor(QPalette.ColorRole.WindowText, QColor(theme.colors.text))
            label.setPalette(palette)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(theme.spacing.xsmall)
        content_layout.addWidget(self.title_widget)
        content_layout.addWidget(self.text_widget)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(*(theme.spacing.medium,) * 4)
        layout.setSpacing(theme.spacing.medium)
        layout.addLayout(content_layout, 1)
        if action is not None:
            layout.addWidget(action, 0, Qt.AlignmentFlag.AlignVCenter)

        self.setAccessibleName(f"{intent.capitalize()} alert: {title or text}")
        self.setAccessibleDescription(text if title else "")
        # Local QSS supplies the semantic accent and rounded feedback surface.
        self.setStyleSheet(
            f"""
            Alert {{
                background-color: {background};
                border: 1px solid {theme.colors.border};
                border-left: {theme.spacing.xsmall}px solid {accent};
                border-radius: {theme.radii.feedback}px;
            }}
            """
        )


class ProgressBar(QProgressBar):
    """Themed native determinate or indeterminate progress indicator."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        minimum: int = 0,
        maximum: int = 100,
        value: int = 0,
    ) -> None:
        super().__init__(parent)
        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setAccessibleName("Progress")

        theme = _current_theme()
        colors = theme.colors
        # Local QSS keeps text legible while leaving range and animation to QProgressBar.
        self.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: {colors.background};
                color: {colors.text};
                border: 1px solid {colors.border};
                border-radius: {theme.radii.feedback}px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {colors.primary};
                border-radius: {theme.radii.feedback}px;
            }}
            """
        )


class EmptyState(QWidget):
    """Centered empty-state text with optional icon and action widget."""

    def __init__(
        self,
        title: str,
        parent: QWidget | None = None,
        *,
        text: str = "",
        icon: QIcon | None = None,
        action: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.icon_widget = QLabel(self)
        self.title_widget = QLabel(title, self)
        self.text_widget = QLabel(text, self)
        self.action_widget = action

        theme = _current_theme()
        self.icon_widget.setVisible(icon is not None)
        if icon is not None:
            icon_size = QSize(theme.spacing.xlarge, theme.spacing.xlarge)
            self.icon_widget.setPixmap(icon.pixmap(icon_size))

        title_font = QFont(self.title_widget.font())
        title_font.setWeight(QFont.Weight(theme.typography.button_weight))
        self.title_widget.setFont(title_font)
        self.title_widget.setWordWrap(True)
        self.text_widget.setVisible(bool(text))
        self.text_widget.setWordWrap(True)
        muted_palette = self.text_widget.palette()
        muted_palette.setColor(QPalette.ColorRole.WindowText, QColor(theme.colors.text_muted))
        self.text_widget.setPalette(muted_palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(*(theme.spacing.large,) * 4)
        layout.setSpacing(theme.spacing.small)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for widget in (self.icon_widget, self.title_widget, self.text_widget):
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(widget)
        if action is not None:
            layout.addWidget(action, 0, Qt.AlignmentFlag.AlignHCenter)

        self.setAccessibleName(title)
        self.setAccessibleDescription(text)
