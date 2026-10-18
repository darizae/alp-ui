"""Offline font registration and deterministic fallback selection."""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from functools import cache
from importlib.resources import as_file, files

from PySide6.QtGui import QFontDatabase

from alp_ui.theme.tokens import TypographyTokens

_BUNDLED_FONTS = {
    "DM Sans": (
        "DMSans-Regular.ttf",
        "DMSans-Medium.ttf",
        "DMSans-SemiBold.ttf",
        "DMSans-Bold.ttf",
    ),
    "JetBrains Mono": (
        "JetBrainsMono-Regular.ttf",
        "JetBrainsMono-Medium.ttf",
        "JetBrainsMono-SemiBold.ttf",
    ),
}


@dataclass(frozen=True, slots=True)
class ResolvedFonts:
    body: str
    metadata: str


@cache
def _load_font_resource(filename: str) -> tuple[str, ...]:
    resource = files("alp_ui.theme").joinpath("resources", "fonts", filename)
    try:
        with as_file(resource) as path:
            font_id = QFontDatabase.addApplicationFont(str(path.resolve()))
    except (FileNotFoundError, OSError):
        return ()
    if font_id < 0:
        return ()
    return tuple(QFontDatabase.applicationFontFamilies(font_id))


def _resolve_family(
    requested: str,
    fallbacks: tuple[str, ...],
    system_font: QFontDatabase.SystemFont,
) -> str:
    font_files = _BUNDLED_FONTS.get(requested, ())
    loaded = tuple(_load_font_resource(filename) for filename in font_files)
    available = set(QFontDatabase.families())
    if requested in available:
        if font_files and not all(loaded):
            warnings.warn(
                f"Some bundled {requested} files failed to load; Qt may synthesize missing weights",
                RuntimeWarning,
                stacklevel=3,
            )
        return requested

    fallback = next((family for family in fallbacks if family in available), None)
    fallback = fallback or QFontDatabase.systemFont(system_font).family()
    warnings.warn(
        f"Font family {requested!r} is unavailable; using {fallback!r}",
        RuntimeWarning,
        stacklevel=3,
    )
    return fallback


def resolve_fonts(typography: TypographyTokens) -> ResolvedFonts:
    """Register bundled fonts and select deterministic installed families."""

    return ResolvedFonts(
        body=_resolve_family(
            typography.body_family,
            typography.body_fallbacks,
            QFontDatabase.SystemFont.GeneralFont,
        ),
        metadata=_resolve_family(
            typography.metadata_family,
            typography.metadata_fallbacks,
            QFontDatabase.SystemFont.FixedFont,
        ),
    )
