# python-ui-library

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
- **Data:** A styled DataTable that consumes your `QAbstractItemModel` directly.
- **Theme:** Alpaca Light, with typed color, typography, spacing, and radius tokens.

Components mix freely with ordinary Qt Widgets. There is no routing framework, data
layer, network client, worker system, or application-specific state model hidden
inside the package.

## Install

The project is not yet published as a stable PyPI release. Install a built wheel while
evaluating it:

```bash
python -m pip install dist/python_ui_library-0.1.0a0-py3-none-any.whl
```

Applications create their own `QApplication` and install the Theme once, before
constructing the main window.

## A small application

```python
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from python_ui_library.components import Badge, Button, TextInput
from python_ui_library.theme import install_theme

app = QApplication([])
install_theme(app)

window = QWidget()
window.setWindowTitle("Example")
layout = QVBoxLayout(window)

name = TextInput(label="Name", placeholder="Ada Lovelace")
status = Badge("Ready", intent="success")
save = Button("Save", variant="primary")
save.clicked.connect(name.clear)

layout.addWidget(name)
layout.addWidget(status)
layout.addWidget(save)
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

## Gallery images

These PNGs are rendered directly by the real PySide6 Gallery Widgets on macOS; they
are not browser mockups or desktop recordings.

<p>
  <img src="docs/images/gallery-actions.png" alt="Button variants, Cards, and an invalid text field in the native Qt Gallery" width="49%">
  <img src="docs/images/gallery-fields.png" alt="Native Qt fields, checkbox, switch, badges, and Alerts in the Gallery" width="49%">
</p>
<p>
  <img src="docs/images/gallery-feedback.png" alt="Feedback intent components and a progress bar in the Gallery" width="49%">
  <img src="docs/images/gallery-data.png" alt="10,000-row and empty caller-owned table models in the Gallery" width="49%">
</p>

## Documentation

- [Getting started](docs/getting-started.md) explains the library's mental model,
  installation, composition, theming, forms, and model/view usage.
- [Component guide](docs/components.md) documents each public Component and its native
  Qt surface.
- [Theme guide](docs/theme.md) covers installation and typed startup overrides.
- [Installed-wheel example](examples/consumer_app/README.md) demonstrates an
  independent consumer with its own table model.

## Current boundaries

- Alpaca Light is the only included Theme; runtime Theme switching is unsupported.
- Windows x86-64 is the release qualification target. The current candidate still
  requires its final Windows DPI, keyboard, and Narrator review.
- There are deliberately no plots, web views, Qt Quick controls, domain models,
  persistence, networking, or background-job abstractions.
- Pre-1.0 versions may make breaking changes.

## License

The library source is MIT-licensed. PySide6/Qt and bundled fonts retain their own
terms; see [third-party licenses and notices](docs/legal/THIRD_PARTY_NOTICES.md).
Applications that redistribute Qt are responsible for satisfying their chosen Qt
license and packaging obligations.

Repository maintenance and agent instructions are kept separately in
[AGENTS.md](AGENTS.md).
