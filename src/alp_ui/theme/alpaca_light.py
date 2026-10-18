"""The Alpaca Light theme preset."""

from alp_ui.theme.tokens import (
    ColorTokens,
    RadiiTokens,
    SpacingTokens,
    Theme,
    TypographyTokens,
)

ALPACA_LIGHT = Theme(
    colors=ColorTokens(
        primary="#059669",
        primary_hover="#047857",
        on_primary="#FFFFFF",
        secondary="#F59E0B",
        background="#F8FAFC",
        surface="#FFFFFF",
        border="#E2E8F0",
        text="#0F172A",
        text_muted="#64748B",
        success="#22C55E",
        warning="#D97706",
        danger="#DC2626",
        info="#2563EB",
        shadow="#000000",
    ),
    typography=TypographyTokens(
        body_family="DM Sans",
        metadata_family="JetBrains Mono",
        body_fallbacks=("Segoe UI", "Arial"),
        metadata_fallbacks=("Cascadia Mono", "Consolas", "Menlo"),
        body_size=10.0,
        heading_size=18.0,
        overline_size=8.0,
        body_weight=400,
        heading_weight=700,
        button_weight=600,
        metadata_weight=500,
    ),
    spacing=SpacingTokens(
        none=0,
        xsmall=4,
        small=8,
        medium=12,
        large=16,
        xlarge=24,
        xxlarge=32,
        card_padding=24,
    ),
    radii=RadiiTokens(default=10, button=8, feedback=8),
)
