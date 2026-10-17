"""Typed design tokens shared by all themes."""

from __future__ import annotations

import re
from dataclasses import dataclass, fields


@dataclass(frozen=True, slots=True)
class ColorTokens:
    """Semantic colors expressed as ``#RRGGBB`` values."""

    primary: str
    primary_hover: str
    on_primary: str
    secondary: str
    background: str
    surface: str
    border: str
    text: str
    text_muted: str
    success: str
    warning: str
    danger: str
    info: str
    shadow: str

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, str) or re.fullmatch(r"#[0-9A-Fa-f]{6}", value) is None:
                raise ValueError(f"colors.{field.name} must be a #RRGGBB value")


@dataclass(frozen=True, slots=True)
class TypographyTokens:
    """Font families, fallbacks, sizes in points, and Qt-compatible weights."""

    body_family: str
    metadata_family: str
    body_fallbacks: tuple[str, ...]
    metadata_fallbacks: tuple[str, ...]
    body_size: float
    heading_size: float
    overline_size: float
    body_weight: int
    heading_weight: int
    button_weight: int
    metadata_weight: int

    def __post_init__(self) -> None:
        if not self.body_family.strip() or not self.metadata_family.strip():
            raise ValueError("typography font families must not be empty")
        if not all(family.strip() for family in (*self.body_fallbacks, *self.metadata_fallbacks)):
            raise ValueError("typography fallback families must not be empty")
        if min(self.body_size, self.heading_size, self.overline_size) <= 0:
            raise ValueError("typography point sizes must be positive")
        weights = (
            self.body_weight,
            self.heading_weight,
            self.button_weight,
            self.metadata_weight,
        )
        if not all(1 <= weight <= 1000 for weight in weights):
            raise ValueError("typography weights must be between 1 and 1000")


@dataclass(frozen=True, slots=True)
class SpacingTokens:
    """Logical-pixel spacing scale."""

    none: int
    xsmall: int
    small: int
    medium: int
    large: int
    xlarge: int
    xxlarge: int
    card_padding: int

    def __post_init__(self) -> None:
        if any(type(getattr(self, field.name)) is not int for field in fields(self)):
            raise TypeError("spacing values must be integers")
        if any(getattr(self, field.name) < 0 for field in fields(self)):
            raise ValueError("spacing values must not be negative")


@dataclass(frozen=True, slots=True)
class RadiiTokens:
    """Logical-pixel corner radii."""

    default: int
    button: int
    feedback: int

    def __post_init__(self) -> None:
        if any(type(getattr(self, field.name)) is not int for field in fields(self)):
            raise TypeError("radius values must be integers")
        if any(getattr(self, field.name) < 0 for field in fields(self)):
            raise ValueError("radius values must not be negative")


@dataclass(frozen=True, slots=True)
class Theme:
    """Immutable semantic design tokens for one application theme."""

    colors: ColorTokens
    typography: TypographyTokens
    spacing: SpacingTokens
    radii: RadiiTokens
