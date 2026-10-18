"""Theme installation for a consumer-owned QApplication."""

from __future__ import annotations

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

from alp_ui.theme.alpaca_light import ALPACA_LIGHT
from alp_ui.theme.fonts import resolve_fonts
from alp_ui.theme.tokens import Theme

_THEME_PROPERTY = "alp_ui_theme"
_METADATA_FONT_PROPERTY = "alp_ui_metadata_font"


def _current_theme() -> Theme:
    """Return the startup Theme, or the default for component previews."""

    app = QApplication.instance()
    if isinstance(app, QApplication):
        theme = app.property(_THEME_PROPERTY)
        if isinstance(theme, Theme):
            return theme
    return ALPACA_LIGHT


def _palette(theme: Theme) -> QPalette:
    colors = theme.colors
    palette = QPalette()
    roles = {
        QPalette.ColorRole.Window: colors.background,
        QPalette.ColorRole.WindowText: colors.text,
        QPalette.ColorRole.Base: colors.surface,
        QPalette.ColorRole.AlternateBase: colors.background,
        QPalette.ColorRole.ToolTipBase: colors.surface,
        QPalette.ColorRole.ToolTipText: colors.text,
        QPalette.ColorRole.Text: colors.text,
        QPalette.ColorRole.Button: colors.surface,
        QPalette.ColorRole.ButtonText: colors.text,
        QPalette.ColorRole.BrightText: colors.on_primary,
        QPalette.ColorRole.Highlight: colors.primary,
        QPalette.ColorRole.HighlightedText: colors.on_primary,
        QPalette.ColorRole.Link: colors.info,
        QPalette.ColorRole.LinkVisited: colors.primary_hover,
        QPalette.ColorRole.PlaceholderText: colors.text_muted,
        QPalette.ColorRole.Mid: colors.border,
        QPalette.ColorRole.Midlight: colors.border,
    }
    for role, value in roles.items():
        palette.setColor(role, QColor(value))
    for role in (
        QPalette.ColorRole.WindowText,
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
    ):
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(colors.text_muted))
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(colors.background)
    )
    return palette


def install_theme(app: QApplication, theme: Theme = ALPACA_LIGHT) -> None:
    """Apply a Theme to an existing QApplication without replacing its native style."""

    if not isinstance(app, QApplication):
        raise TypeError("install_theme requires the consumer-owned QApplication")
    if not isinstance(theme, Theme):
        raise TypeError("theme must be a Theme instance")

    fonts = resolve_fonts(theme.typography)
    font = QFont(fonts.body)
    font.setPointSizeF(theme.typography.body_size)
    font.setWeight(QFont.Weight(theme.typography.body_weight))
    app.setPalette(_palette(theme))
    app.setFont(font)
    app.setProperty(_THEME_PROPERTY, theme)
    app.setProperty(_METADATA_FONT_PROPERTY, fonts.metadata)
