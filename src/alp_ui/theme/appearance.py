"""Theme-derived interaction palette and density metrics (logical pixels)."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QColor

from alp_ui.theme.tokens import InteractionTokens, Theme


def blend(foreground: str, background: str, amount: float) -> str:
    """Blend semantic colors once at the Theme boundary, not in Components."""
    front, back = QColor(foreground), QColor(background)
    return (
        QColor.fromRgbF(
            front.redF() * amount + back.redF() * (1 - amount),
            front.greenF() * amount + back.greenF() * (1 - amount),
            front.blueF() * amount + back.blueF() * (1 - amount),
        )
        .name()
        .upper()
    )


def interactions(theme: Theme) -> InteractionTokens:
    """Return centralized state colors, respecting a custom Theme override."""
    if theme.interaction is not None:
        return theme.interaction
    c = theme.colors
    return InteractionTokens(
        focus=c.info,
        border_hover=blend(c.text_muted, c.border, 0.32),
        hover_surface=blend(c.primary, c.surface, 0.045),
        pressed_surface=blend(c.primary, c.surface, 0.09),
        selected_surface=blend(c.primary, c.surface, 0.10),
        disabled_surface=c.background,
        disabled_text=c.text_muted,
        secondary_surface=c.background,
        secondary_hover=blend(c.primary, c.surface, 0.075),
        danger_hover=blend(c.text, c.danger, 0.17),
        primary_pressed=blend(c.text, c.primary_hover, 0.12),
        feedback_info=blend(c.info, c.surface, 0.075),
        feedback_success=blend(c.success, c.surface, 0.075),
        feedback_warning=blend(c.warning, c.surface, 0.075),
        feedback_danger=blend(c.danger, c.surface, 0.075),
    )


@dataclass(frozen=True, slots=True)
class DensityMetrics:
    control_height: int
    table_row_height: int
    card_padding: int
    button_small: int
    button_medium: int
    button_large: int


def density_metrics(theme: Theme) -> DensityMetrics:
    """Density is a startup Theme choice; native font points stay unchanged."""
    if theme.density == "compact":
        return DensityMetrics(34, 36, 16, 30, 34, 38)
    return DensityMetrics(40, 44, theme.spacing.card_padding, 32, 40, 44)
