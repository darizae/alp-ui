from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

import pytest
from PySide6.QtGui import QColor, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication

from python_ui_library.theme import (
    ALPACA_LIGHT,
    ColorTokens,
    Theme,
    install_theme,
)
from python_ui_library.theme import fonts as font_loading

EXPECTED_COLORS = {
    "primary": "#059669",
    "primary_hover": "#047857",
    "on_primary": "#FFFFFF",
    "secondary": "#F59E0B",
    "background": "#F8FAFC",
    "surface": "#FFFFFF",
    "border": "#E2E8F0",
    "text": "#0F172A",
    "text_muted": "#64748B",
    "success": "#22C55E",
    "warning": "#D97706",
    "danger": "#DC2626",
    "info": "#2563EB",
    "shadow": "#000000",
}


def test_alpaca_light_has_exact_source_colors() -> None:
    assert {name: getattr(ALPACA_LIGHT.colors, name) for name in EXPECTED_COLORS} == EXPECTED_COLORS


def test_theme_is_frozen_and_supports_typed_startup_override() -> None:
    with pytest.raises(FrozenInstanceError):
        ALPACA_LIGHT.colors.primary = "#000000"  # type: ignore[misc]

    overridden = replace(
        ALPACA_LIGHT,
        colors=replace(ALPACA_LIGHT.colors, primary="#0F766E"),
    )
    assert overridden.colors.primary == "#0F766E"
    assert ALPACA_LIGHT.colors.primary == "#059669"


def test_invalid_color_fails_at_construction() -> None:
    values = EXPECTED_COLORS | {"primary": "emerald"}
    with pytest.raises(ValueError, match=r"colors\.primary must be a #RRGGBB value"):
        ColorTokens(**values)


def test_invalid_metrics_fail_at_construction() -> None:
    with pytest.raises(ValueError, match="point sizes must be positive"):
        replace(ALPACA_LIGHT.typography, body_size=0)
    with pytest.raises(ValueError, match="spacing values must not be negative"):
        replace(ALPACA_LIGHT.spacing, small=-1)
    with pytest.raises(ValueError, match="radius values must not be negative"):
        replace(ALPACA_LIGHT.radii, default=-1)


def test_startup_override_is_applied(qapp: QApplication) -> None:
    overridden = replace(
        ALPACA_LIGHT,
        colors=replace(ALPACA_LIGHT.colors, primary="#0F766E"),
    )
    install_theme(qapp, overridden)
    assert qapp.palette().color(QPalette.ColorRole.Highlight) == QColor("#0F766E")


def test_install_theme_applies_palette_fonts_and_preserves_style(qapp: QApplication) -> None:
    original_style = qapp.style()
    original_stylesheet = qapp.styleSheet()

    install_theme(qapp)

    palette = qapp.palette()
    assert palette.color(QPalette.ColorRole.Window) == QColor(EXPECTED_COLORS["background"])
    assert palette.color(QPalette.ColorRole.Base) == QColor(EXPECTED_COLORS["surface"])
    assert palette.color(QPalette.ColorRole.Text) == QColor(EXPECTED_COLORS["text"])
    assert palette.color(QPalette.ColorRole.Highlight) == QColor(EXPECTED_COLORS["primary"])
    assert qapp.font().family() == "DM Sans"
    assert "JetBrains Mono" in QFontDatabase.families()
    assert qapp.style() is original_style
    assert qapp.styleSheet() == original_stylesheet


def test_install_theme_rejects_unsupported_input(qapp: QApplication) -> None:
    with pytest.raises(TypeError, match="consumer-owned QApplication"):
        install_theme(object())  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="Theme instance"):
        install_theme(qapp, object())  # type: ignore[arg-type]


def test_missing_font_resource_warns_and_uses_system_fallback(
    qapp: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    unavailable = replace(
        ALPACA_LIGHT,
        typography=replace(
            ALPACA_LIGHT.typography,
            body_family="Definitely Missing",
            body_fallbacks=(),
        ),
    )
    monkeypatch.setitem(font_loading._BUNDLED_FONTS, "Definitely Missing", ("missing.ttf",))
    font_loading._load_font_resource.cache_clear()

    with pytest.warns(RuntimeWarning, match="Definitely Missing"):
        install_theme(qapp, unavailable)

    assert qapp.font().family() != "Definitely Missing"
    install_theme(qapp)


def test_theme_type_is_public() -> None:
    assert isinstance(ALPACA_LIGHT, Theme)
