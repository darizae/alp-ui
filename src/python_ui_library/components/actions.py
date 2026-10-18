"""Action components built on native Qt buttons."""

from __future__ import annotations

from typing import Literal

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QPushButton, QWidget

from python_ui_library.theme.appearance import density_metrics, interactions
from python_ui_library.theme.install import _current_theme

ButtonVariant = Literal["primary", "secondary", "outline", "danger"]
ButtonSize = Literal["small", "medium", "large"]

_VARIANTS = ("primary", "secondary", "outline", "danger")
_SIZES = ("small", "medium", "large")


class Button(QPushButton):
    """Sentence-case action button preserving QPushButton signals and behavior."""

    def __init__(
        self,
        text: str = "",
        parent: QWidget | None = None,
        *,
        variant: ButtonVariant = "primary",
        size: ButtonSize = "medium",
        loading: bool = False,
        loading_text: str = "Loading…",
    ) -> None:
        if variant not in _VARIANTS:
            choices = ", ".join(_VARIANTS)
            raise ValueError(f"variant must be one of: {choices}")
        if size not in _SIZES:
            choices = ", ".join(_SIZES)
            raise ValueError(f"size must be one of: {choices}")
        if type(loading) is not bool:
            raise TypeError("loading must be a bool")
        if not loading_text:
            raise ValueError("loading_text must not be empty")

        super().__init__(text, parent)
        self.variant: ButtonVariant = variant
        self.component_size: ButtonSize = size
        self._loading = False
        self._loading_text = loading_text
        self._resting_text = text
        self._enabled_after_loading = True
        self._accessible_name_after_loading = text.replace("&", "")
        self.setAccessibleName(text.replace("&", ""))

        theme = _current_theme()
        colors = theme.colors
        states = interactions(theme)
        density = density_metrics(theme)
        if variant == "primary":
            background, foreground, border, hover = (
                colors.primary,
                colors.on_primary,
                colors.primary,
                colors.primary_hover,
            )
        elif variant == "secondary":
            background, foreground, border, hover = (
                states.secondary_surface,
                colors.text,
                colors.border,
                states.secondary_hover,
            )
        elif variant == "danger":
            background, foreground, border, hover = (
                colors.danger,
                colors.on_primary,
                colors.danger,
                states.danger_hover,
            )
        else:
            background, foreground, border, hover = (
                colors.surface,
                colors.text,
                colors.border,
                states.hover_surface,
            )

        font = QFont(self.font())
        font.setWeight(QFont.Weight(theme.typography.button_weight))
        self.setFont(font)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Button, QColor(background))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(foreground))
        self.setPalette(palette)

        self.setMinimumHeight(
            {
                "small": density.button_small,
                "medium": density.button_medium,
                "large": density.button_large,
            }[size]
        )
        horizontal = {
            "small": theme.spacing.medium,
            "medium": theme.spacing.large,
            "large": theme.spacing.xlarge,
        }[size]
        hover_border = states.border_hover if variant in ("secondary", "outline") else hover
        pressed_background = (
            states.primary_pressed
            if variant == "primary"
            else states.pressed_surface
            if variant in ("secondary", "outline")
            else states.danger_hover
        )
        pressed_border = border if variant in ("secondary", "outline") else hover
        # Local QSS is required because native styles do not reliably render variant palettes.
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {background};
                color: {foreground};
                border: 1px solid {border};
                border-radius: {theme.radii.button}px;
                padding: 0 {horizontal}px;
            }}
            QPushButton:hover {{
                background-color: {hover};
                border-color: {hover_border};
            }}
            QPushButton:pressed {{
                background-color: {pressed_background};
                border-color: {pressed_border};
            }}
            QPushButton:focus {{
                border: 1px solid {states.focus};
            }}
            QPushButton:disabled {{
                background-color: {states.disabled_surface};
                color: {states.disabled_text};
                border-color: {colors.border};
            }}
            """
        )
        self.setLoading(loading)

    def isLoading(self) -> bool:
        """Return whether the button is presenting its consumer-owned busy state."""

        return self._loading

    def setLoading(self, loading: bool) -> None:
        """Present or clear a busy state without starting application work."""

        if type(loading) is not bool:
            raise TypeError("loading must be a bool")
        if loading == self._loading:
            return
        if loading:
            self._resting_text = self.text()
            self._enabled_after_loading = self.isEnabled()
            self._accessible_name_after_loading = self.accessibleName()
            self._loading = True
            super().setText(self._loading_text)
            self.setAccessibleName(self._loading_text)
            super().setEnabled(False)
        else:
            self._loading = False
            super().setText(self._resting_text)
            self.setAccessibleName(self._accessible_name_after_loading)
            super().setEnabled(self._enabled_after_loading)

    def setEnabled(self, enabled: bool) -> None:
        """Retain the caller's enabled state while loading keeps activation disabled."""

        if getattr(self, "_loading", False):
            self._enabled_after_loading = enabled
            super().setEnabled(False)
        else:
            super().setEnabled(enabled)
