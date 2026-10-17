# Theme

Create the application's one `QApplication`, install a Theme before constructing the
main window, and then use ordinary Qt Widgets:

```python
from PySide6.QtWidgets import QApplication

from python_ui_library.theme import install_theme

app = QApplication([])
install_theme(app)
```

All token groups are frozen dataclasses. A startup override uses
`dataclasses.replace` instead of string-key configuration:

```python
from dataclasses import replace

from python_ui_library.theme import ALPACA_LIGHT, install_theme

custom = replace(
    ALPACA_LIGHT,
    colors=replace(ALPACA_LIGHT.colors, primary="#0F766E"),
)
install_theme(app, custom)
```

Runtime theme switching is unsupported in v0.1. `install_theme` preserves the current
native Qt style and installs no global stylesheet. It loads bundled, unmodified DM Sans
and JetBrains Mono files offline. If a resource cannot load, a `RuntimeWarning` names
the deterministic system fallback.

Run the current Theme Gallery from an editable installation:

```bash
python gallery/main.py
```

## Style probe

With PySide6-Essentials 6.11.2, the macOS installation exposes `macOS`, `Windows`, and
`Fusion` styles. An offscreen probe found a two-pixel default frame in `Windows` and a
one-pixel frame in `Fusion`; both report six-pixel button margins and two-pixel focus
margins. Palette, typography, native focus, disabled behavior, and scaling are retained,
so no `QProxyStyle` override is justified yet. Actual Windows visual review remains an
owner gate because the current implementation host is macOS.
