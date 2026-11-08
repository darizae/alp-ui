# Core architecture and component contract — alp-ui

[Locked product decisions](DECISIONS.md) are authoritative. The public
[component guide](../components.md), [getting started](../getting-started.md)
and [theme guide](../theme.md) document actual exported APIs and their use.

## Native Qt boundaries

- Distribution `alp-ui`, import root `alp_ui`; CPython 3.11–3.13 and
  PySide6-Essentials 6.11.x, using QtCore/QtGui/QtWidgets only at runtime.
- The consumer creates one `QApplication`, installs `install_theme(app)`
  before constructing UI, and composes components in ordinary Qt layouts.
- Preserve widget parenting, lifetimes, signals, native focus/keyboard,
  accessible names/descriptions, enabled state and resizing behavior.
- Application code owns business data, state, workers, networking, filesystem,
  persistence, validation, navigation and model/view data. No implicit
  `QApplication`, browser renderer, Qt Quick/QML, or page framework.
- `DataTable` accepts a caller's `QAbstractItemModel`, using Qt proxy
  models as needed rather than copying data into per-cell widgets.
- `Plot` paints caller-owned finite numeric line series and categorical
  bars; it performs no analysis, waveform/spectrogram, zoom or export.
- Reuse native Qt and existing Components before new abstractions.
  Do not add Qt Addons, science/charting, styling-framework, or
  application-specific runtime dependencies.

## Theme and assets

`Theme` is immutable typed semantic tokens; `ALPACA_LIGHT` is the
default. Use `QPalette`/`QFont` with native `QStyle`, and only measured
local QSS or narrow custom painting. No global QSS or hot retheming.
Interaction states are derived centrally; do not scatter hex colors
inside Components. Consumer overrides take effect at startup.

The locked original Alpaca Light semantic palette:

| Token | Hex | Token | Hex |
| --- | --- | --- | --- |
| `primary` | `#059669` | `primary_hover` | `#047857` |
| `on_primary` | `#FFFFFF` | `secondary` | `#F59E0B` |
| `background` | `#F8FAFC` | `surface` | `#FFFFFF` |
| `border` | `#E2E8F0` | `text` | `#0F172A` |
| `text_muted` | `#64748B` | `success` | `#22C55E` |
| `warning` | `#D97706` | `danger` | `#DC2626` |
| `info` | `#2563EB` | `shadow` | `#000000` |

Amber `secondary` is an accent, not an amber secondary Button.
Use a 4-logical-pixel spacing base; standard and compact densities
change geometry, never font sizes. Fonts: unmodified bundled
DM Sans and JetBrains Mono with offline fallback and complete OFL
notices. Original lightweight `make_icon` artwork uses Qt drawing.
The [theme guide](../theme.md) covers actual density metrics, typed
overrides, state colors, and type roles.

Keep accessible focus, sufficiently legible colors and text feedback
that does not rely on hue. Project source is MIT; Qt redistribution
and bundled fonts retain separate obligations in
[legal notices](../legal/THIRD_PARTY_NOTICES.md). Never copy the
historical reference applications or unlicensed icons.

## Verification and release gate

Public Widgets need accurate constructor docs, Gallery examples,
behavior tests of native interactions and accessible labels, relevant
loading/disabled/invalid states and large-model efficiency. Run
repository-wide Ruff, pytest, wheel/sdist build, Twine metadata and an
isolated wheel-installed consumer. Windows x86-64 with Python
3.11/3.12/3.13 is the release target; DPI 100%/150%, keyboard and
screen-reader claims require native review. macOS captures and
offscreen tests do not certify Windows. Linux/macOS are not
release-qualified by the existing snapshots.

[Gallery](../../gallery/main.py) is the component explorer;
[Showcase](../../gallery/showcase.py) is native composition, not a
public shell. The shipped `v0.1.0a1` pre-release provenance is in
[GitHub Releases](https://github.com/darizae/alp-ui/releases); follow the
reviewed-PR delivery convention in [AGENTS.md](../../AGENTS.md) for later
changes. Documentation work alone authorizes no release, tag or version bump.

## A1 reuse decision — 2026-11-07

Merged [PR #2](https://github.com/darizae/alp-ui/pull/2) found no
justified new Component. BioCall Studio uses existing public
presentation, fields, feedback, data table and Plot APIs; its
navigation, workflow, domain-specific `SpectrogramView`, audio/FFT,
caching and overlays stay downstream. Extract only on evidence of
a generic independent consumer. The detailed A1 evidence remains in
Git history and the merged PR.
