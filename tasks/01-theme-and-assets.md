# Task 01 — Typed Alpaca Light theme and offline fonts

**Dependencies:** Task 00 completed. **Task type:** theme/styling foundation only; no full component catalog.

## Read first

`AGENTS.md`, `THEME_ALPACA_LIGHT.md`, `DECISIONS.md`, `SPEC.md`, `QUALITY.md`, `references/SOURCE_MAP.md`, `references/LICENSE_AND_RESEARCH.md`.

## Work

1. Define typed, frozen `Theme` token groups (colors, typography, spacing, radii) and export `ALPACA_LIGHT`. Preserve **exact hex values** from Alpaca MUI. Distinguish source tokens and new derived interactions.
2. Define one public `install_theme(app, theme=ALPACA_LIGHT)` operation that accepts a consumer-created `QApplication`. Install appropriate Qt `QPalette` color roles and fonts; define minimal consistent native Qt style setup. Do **not** create QApplication or run event loop.
3. Probe Windows's native Qt style and Qt Fusion under PySide6 6.11.x. Introduce only targeted `QProxyStyle` changes when demonstrably needed (focus, button metrics, header painting, radii). Record observations and reasons; do not build global dynamic QSS or full `QCommonStyle` skin.
4. Obtain unmodified official DM Sans and JetBrains Mono font binaries from licensed sources, bundle enough weights for the specified hierarchy in package resources, include upstream copyright/OFL text, and load offline with Qt APIs. Confirm fallback on missing/corrupt resource.
5. Create initial local Theme Gallery page with color swatches, headings/body/monospace text, and test widgets demonstrating theme application. The full gallery navigation is Task 06.
6. Demonstrate consumer override using a typed Theme derived from preset, without editing package code. Explicitly leave runtime theme switching unsupported.
7. Add token tests, resource/wheel tests, QPalette role tests, font fallback tests, and clear errors for unsupported input.

## Artifacts

`theme/` implementation, bundled OFL assets and notices, theme README/examples, baseline theme Gallery view, tests.

## Acceptance

- [ ] All 12 exact source color values match `THEME_ALPACA_LIGHT.md`.
- [ ] Theme remains immutable and can be overridden at application startup.
- [ ] One-time install works with ordinary `QApplication` and no global QSS.
- [ ] Font binaries + correct official notices present and load in isolated installed wheel **offline**.
- [ ] Alternate/fallback font behavior is tested.
- [ ] Windows visual review shows intended typography and palette; targeted Qt style deviations recorded.
- [ ] No other runtime library or plotting dependency introduced.

**Gate for owner:** review Theme Gallery swatches and typography before building controls. Do not copy MUI CSS or SVG assets.
