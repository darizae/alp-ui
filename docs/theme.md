# Theme

Create the application's **one** `QApplication`, then install a Theme before creating widgets:

```python
from PySide6.QtWidgets import QApplication
from alp_ui.theme import install_theme

app = QApplication([])
install_theme(app)
```

All Theme groups are immutable, typed dataclasses. Alpaca Light uses a green primary
and amber secondary accent. `secondary` is a palette accent, not an instruction to
make every secondary action amber.

## Startup customization and density

```python
from dataclasses import replace
from alp_ui.theme import ALPACA_LIGHT, install_theme

custom = replace(
    ALPACA_LIGHT,
    colors=replace(ALPACA_LIGHT.colors, primary="#0F766E"),
    density="compact",
)
install_theme(app, custom)
```

The `standard` density is the default. `compact` retains the same readable font size
while reducing controls and surface padding:

| Metric (logical px) | Standard | Compact |
|---|---:|---:|
| Minimum text/number/select control height | 40 | 34 |
| Minimum Button small / medium / large height | 32 / 40 / 44 | 30 / 34 / 38 |
| DataTable row | 44 | 36 |
| Card content padding | 24 | 16 |

Density is chosen at startup. Existing components do not support runtime re-theming;
reinstalling Theme after constructing widgets is not guaranteed to update them.

## Shared interaction colors

`theme.appearance.interactions(theme)` derives a single set of hover, pressed,
selected, focus, disabled, and subtle surface colors from the theme's semantic
palette. Components do not individually darken or tint colors. For a specific
custom theme, use a typed `InteractionTokens` override:

```python
from dataclasses import replace
from alp_ui.theme import ALPACA_LIGHT, interactions

custom = replace(
    ALPACA_LIGHT,
    interaction=replace(interactions(ALPACA_LIGHT), focus="#7C3AED"),
)
```

If only semantic colors are overridden, the interaction colors are derived from the
new colors automatically. If the explicit interaction override is supplied, it is the
consumer's responsibility to keep contrast appropriate when changing base colors.

Local QSS is used only by components that require consistent shape or subcontrol
appearance. Qt retains native widget input semantics, native signals, model/view,
keyboard navigation and accessibility metadata. Custom-painted details are the
checkbox indicator, switch and minimal native select/spinbox glyphs; this is not a
custom QWidget framework or global stylesheet.

## Typography and icons

Body font: **DM Sans**. Metadata font: **JetBrains Mono**. Text roles: `title`,
`heading`, `subheading`, `body`, `caption`, `overline`.

Original, library-drawn stroke icons use `make_icon`:

```python
from alp_ui.theme import make_icon

button.setIcon(make_icon("plus", color="#FFFFFF", size=20))
```

Supported names: `grid`, `folder`, `list`, `settings`, `plus`, `search`, `info`,
`check`. There is no downloaded icon pack or new runtime dependency.

Bundled, unmodified DM Sans and JetBrains Mono files load offline. Missing resources
produce a warning and a platform font fallback. The library does not fetch Google
Fonts or replace the native `QStyle` object.

## Preview

Run `python -m gallery.main` for the Component catalog and
`python -m gallery.showcase` for an application-like composition. Native rendering
can vary by operating system and display scale.
