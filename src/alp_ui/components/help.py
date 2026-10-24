"""Accessible contextual help built on the native Qt help popup."""

from __future__ import annotations

from html import escape

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QToolButton, QWhatsThis, QWidget

from alp_ui.theme.appearance import interactions
from alp_ui.theme.install import _current_theme


def _plain_text_for_qt(text: str) -> str:
    """Escape text because Qt's tooltip and What's This views accept rich text."""

    return escape(text).replace("\n", "<br>")


class HelpHint(QToolButton):
    """A compact, keyboard-accessible control for short contextual help."""

    def __init__(
        self,
        help_text: str,
        parent: QWidget | None = None,
        *,
        subject: str = "",
    ) -> None:
        _validate_plain_text(help_text, "help_text")
        _validate_plain_text(subject, "subject", allow_empty=True)
        subject = subject.strip()
        super().__init__(parent)

        theme = _current_theme()
        state = interactions(theme)
        diameter = theme.spacing.large + (
            theme.spacing.small if theme.density == "standard" else theme.spacing.xsmall
        )

        self.setText("?")
        self.setAutoRaise(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(diameter, diameter)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.setAccessibleName(f"More about {subject}" if subject else "More information")

        font = QFont(self.font())
        font.setPointSizeF(theme.typography.body_size)
        font.setWeight(QFont.Weight(theme.typography.button_weight))
        self.setFont(font)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Button, QColor(theme.colors.surface))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme.colors.text_muted))
        self.setPalette(palette)

        # Local QSS gives this tiny native button a stable, visible focus border.
        self.setStyleSheet(
            f"""
            HelpHint {{
                background-color: {theme.colors.surface};
                color: {theme.colors.text_muted};
                border: 1px solid {theme.colors.border};
                border-radius: {diameter // 2}px;
                padding: 0;
            }}
            HelpHint:hover {{
                background-color: {state.hover_surface};
                border-color: {state.border_hover};
                color: {theme.colors.text};
            }}
            HelpHint:pressed {{ background-color: {state.pressed_surface}; }}
            HelpHint:focus {{ border-color: {state.focus}; }}
            HelpHint:disabled {{
                background-color: {state.disabled_surface};
                color: {state.disabled_text};
                border-color: {theme.colors.border};
            }}
            """
        )
        self.setHelpText(help_text)
        self.clicked.connect(self._show_help)

    def setHelpText(self, help_text: str) -> None:  # noqa: N802
        """Set the plain-text explanation used by tooltip, help view, and accessibility."""

        _validate_plain_text(help_text, "help_text")
        self._help_text = help_text
        self._display_text = _plain_text_for_qt(help_text)
        self.setToolTip(self._display_text)
        self.setWhatsThis(self._display_text)
        self.setAccessibleDescription(help_text)

    def _show_help(self) -> None:
        if not self.isEnabled():
            return
        QWhatsThis.showText(self.mapToGlobal(self.rect().bottomLeft()), self._display_text, self)


def _validate_plain_text(value: str, name: str, *, allow_empty: bool = False) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str")
    if not allow_empty and not value.strip():
        raise ValueError(f"{name} must not be empty or whitespace")
