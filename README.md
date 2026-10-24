<p align="center">
  <img src="docs/brand/transparent/lockup-original.png" alt="Alp-ui logo — Alpaca tile icon and wordmark" width="220">
</p>

<h1 align="center">alp-ui</h1>

A compact, native desktop UI library for Python applications built with PySide6 Qt
Widgets. It provides a coherent light Theme and a practical set of styled Components
without taking over your application architecture.

The result still feels like Qt: widgets have normal parents, layouts, signals, keyboard
behavior, accessibility, and model/view data flow. The library owns presentation and
small reusable interactions; your application owns its data and work.

- **Status:** pre-release `0.1.0a0`
- **Python:** 3.11–3.13
- **Qt:** PySide6-Essentials 6.11.x

## What you get

- **Actions:** Button variants and a caller-controlled loading presentation.
- **Typography and surfaces:** Text roles, Cards, and Dividers.
- **Forms:** Text, number, select, checkbox, and switch Components built on native Qt
  controls.
- **Feedback:** Badges, Alerts, Progress Bars, and Empty States using semantic intent.
- **Data and plots:** A styled DataTable that consumes your `QAbstractItemModel`
  directly, plus a lightweight native `Plot` for numeric line and categorical bar
  presentation.
- **Theme:** Alpaca Light, with typed semantic tokens, shared state colors, density,
  and additional typography roles.

Components mix freely with ordinary Qt Widgets. There is no routing framework, data
layer, network client, worker system, or application-specific state model hidden
inside the package.

## Install

The project is not yet published as a stable PyPI release. Install a built wheel while
evaluating it:

```bash
python -m pip install dist/alp_ui-0.1.0a0-py3-none-any.whl
```

Applications create their own `QApplication` and install the Theme once, before
constructing the main window.

## A small application

```python
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from alp_ui.components import Badge, Button, TextInput
from alp_ui.theme import install_theme

app = QApplication([])
install_theme(app)

window = QWidget()
window.setWindowTitle("Example")
layout = QVBoxLayout(window)
layout.setContentsMargins(24, 24, 24, 24)
layout.setSpacing(16)

name = TextInput(label="Name", placeholder="Ada Lovelace")
status = Badge("Ready", intent="success")
save = Button("Save", variant="primary")
save.clicked.connect(name.clear)

layout.addWidget(name)
layout.addWidget(status)
layout.addWidget(save, 0, Qt.AlignmentFlag.AlignLeft)
window.show()

app.exec()
```

This is ordinary Qt composition: connect native signals, use native layouts, and keep
business logic in the consumer application.

## Explore the Gallery

The Gallery shows every public Component, supported variants, disabled and invalid
states, keyboard focus, Theme tokens, and a 10,000-row caller-owned table model.

From a development checkout:

```bash
.venv/bin/python -m gallery.main
```

On Windows, use `.venv\Scripts\python -m gallery.main`.

### Composed application showcase

For a realistic compact layout with a sidebar, header, toolbar, form Card, and
DataTable, run:

```bash
python -m gallery.showcase
```

The Showcase is an example composition, **not** a new navigation framework or public
Sidebar component.

## Gallery images

These PNGs were rendered from the current PySide6 Widgets implementation on macOS;
they are not browser mockups.

Regenerate the full set from the actual Qt widgets with:

```bash
.venv/bin/python -m gallery.capture
```

<img src="docs/images/showcase.png" alt="Compact composed application Showcase using the library's Components" width="100%">

<p>
  <img src="docs/images/gallery-actions.png" alt="Natural-width Button variants and Card surfaces in the native Qt Gallery" width="49%">
  <img src="docs/images/gallery-fields.png" alt="Native Qt fields, checkbox, switch, badges, and Alerts in the Gallery" width="49%">
</p>
<p>
  <img src="docs/images/gallery-feedback.png" alt="Feedback intent components and a progress bar in the Gallery" width="49%">
  <img src="docs/images/gallery-data.png" alt="10,000-row and empty caller-owned table models in the Gallery" width="49%">
</p>

This minimal consumer uses the normal `install_theme(app)` defaults and ordinary Qt
layouts, with no consumer stylesheet or density override:

<img src="docs/images/consumer-default.png" alt="Minimal standard-density consumer using public alp-ui Components" width="600">

## Brand assets

The repository logo is the owner-provided Alp-ui artwork, kept under
[`docs/brand/`](docs/brand/README.md) with the exact original source, transparent and
inverse lockups, wordmarks, on-background composites, and downscaled app icons
(including the Windows `.ico`). Usage and provenance notes live beside the files.

## Documentation

- [Getting started](docs/getting-started.md) explains the library's mental model,
  installation, composition, theming, forms, and model/view usage.
- [Component guide](docs/components.md) documents each public Component and its native
  Qt surface.
- [Theme guide](docs/theme.md) covers startup overrides, compact/standard density,
  shared interaction tokens, typography roles, and original icons.
- [Installed-wheel example](examples/consumer_app/README.md) demonstrates an
  independent consumer with its own table model.

## Current boundaries

- Alpaca Light is the only included Theme; runtime Theme switching is unsupported.
- Windows x86-64 is the release qualification target. The current candidate still
  requires its final Windows DPI, keyboard, and Narrator review.
- The owner-approved post-v0.1 `Plot` Component provides only native-painted numeric
  line and categorical bar presentation. There are no charting dependencies, web
  views, Qt Quick controls, domain models, persistence, networking, or background-job
  abstractions.
- Pre-1.0 versions may make breaking changes.

## License

The library source is MIT-licensed. PySide6/Qt and bundled fonts retain their own
terms; see [third-party licenses and notices](docs/legal/THIRD_PARTY_NOTICES.md).
Applications that redistribute Qt are responsible for satisfying their chosen Qt
license and packaging obligations.
