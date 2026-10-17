# Getting started

`python-ui-library` is a presentation layer for PySide6 desktop applications. It gives
common Qt Widgets a consistent visual language while preserving the APIs and behavior
that make Qt useful.

If you already know Qt Widgets, the library should feel unsurprising. If you are new
to Qt, three ideas are enough to get oriented:

1. Your application creates the single `QApplication` and owns the event loop.
2. Widgets live in a parent/child tree and are arranged with Qt layouts.
3. Signals describe user interaction; models provide data to views such as DataTable.

The library does not add an application framework around those concepts.

## Installation

The current version is a pre-release. Build the repository and install its wheel into
the consumer application's environment:

```bash
python -m build
python -m pip install dist/python_ui_library-0.1.0a0-py3-none-any.whl
```

The only runtime dependency is `PySide6-Essentials>=6.11,<6.12`.

## Install the Theme once

Theme installation belongs at application startup, before the main widgets are
constructed:

```python
from PySide6.QtWidgets import QApplication

from python_ui_library.theme import install_theme

app = QApplication([])
install_theme(app)
```

`install_theme` styles the consumer-owned application. It never creates another
`QApplication`, starts the event loop, performs network access, or replaces the native
Qt style.

## Compose Components like Qt Widgets

Components can sit beside native controls in any Qt layout:

```python
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from python_ui_library.components import Button, Card, TextInput

window = QWidget()
layout = QVBoxLayout(window)

card = Card()
name = TextInput(label="Display name", description="Shown in the application")
save = Button("Save")
save.clicked.connect(lambda: print(name.text()))

card.content_layout.addWidget(QLabel("Profile"))
card.content_layout.addWidget(name)
card.content_layout.addWidget(save)
layout.addWidget(card)
```

Parenting, enabled state, focus, tooltips, and native signals continue to work normally.
Use the Component's documented options for its reusable visual choices and inherited
Qt methods for ordinary widget behavior.

## Think in semantic choices

Visual APIs describe meaning rather than colors. A Button uses variants such as
`primary` or `danger`; feedback Components use intents such as `info`, `success`, or
`warning`. The Theme maps those meanings to actual colors and typography.

For an application-specific startup Theme, replace typed tokens instead of editing
Component styles:

```python
from dataclasses import replace

from python_ui_library.theme import ALPACA_LIGHT, install_theme

theme = replace(
    ALPACA_LIGHT,
    colors=replace(ALPACA_LIGHT.colors, primary="#0F766E"),
)
install_theme(app, theme)
```

Runtime Theme switching is outside the current contract.

## Keep validation and suggestions application-owned

TextInput forwards native Qt validator, input-mask, and completer APIs. The application
decides what is valid and supplies any suggestion data; the Component presents the
label, help, and error state accessibly.

```python
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from python_ui_library.components import TextInput

validator = QRegularExpressionValidator(QRegularExpression(r"[A-Z]{2}\d{2}"))
code = TextInput(label="Code", validator=validator)

if not code.hasAcceptableInput():
    code.setErrorText("Use two capital letters followed by two digits")
```

The same boundary applies to loading: a Button can present a loading state, but the
application owns the operation and decides when that state begins and ends.

## Give DataTable a Qt model

DataTable is a styled `QTableView`, not a second table-data abstraction:

```python
from python_ui_library.components import DataTable

table = DataTable(model=application_model)
table.setAccessibleName("Accounts")
table.doubleClicked.connect(open_selected_account)
```

Use `QAbstractItemModel` implementations and Qt proxy models for data, sorting, and
filtering. Model notifications update the view without copying rows into widgets.

## Accessibility and keyboard use

Visible labels become accessible names for field controls, help and error text become
accessible descriptions, and native keyboard behavior is retained. Supply an explicit
accessible name when context replaces a visible label, especially for tables,
progress indicators, and icon-only actions.

Use the Gallery to inspect focus order and supported states with the keyboard. A real
application should still be reviewed with its target platform's screen reader and DPI
settings before distribution.

## Where to go next

- Browse every public API in the [Component guide](components.md).
- Learn about tokens and overrides in the [Theme guide](theme.md).
- Run the [installed-wheel consumer](../examples/consumer_app/README.md).
- Review [third-party terms](legal/THIRD_PARTY_NOTICES.md) before distributing an
  application with Qt.
