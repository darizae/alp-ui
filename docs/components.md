# Components

Install the Theme before constructing widgets. Components remain ordinary Qt Widgets;
signals, focus, parenting, enabled state, icons, models, validators, and keyboard behavior
come from their native Qt controls.

## Actions, typography, and surfaces

`Button(text, parent=None, *, variant="primary", size="medium", loading=False,
loading_text="Loading…")` subclasses
`QPushButton`. Variants are `primary`, `secondary`, `outline`, and `danger`; sizes are
`small`, `medium`, and `large`. Use inherited APIs such as `clicked`, `setIcon`,
`setEnabled`, and `setShortcut`. `setLoading(True)` replaces the visible and accessible
label, disables activation, and starts no work; the consumer remains responsible for
performing work and clearing the state.

```python
from python_ui_library.components import Button

save = Button("Save", variant="primary")
save.clicked.connect(save_document)
delete = Button("Delete", variant="danger", size="small")
save.setLoading(True)
```

`Text(text, parent=None, *, role="body", selectable=False, word_wrap=False)` subclasses
`QLabel`. Roles are `body`, `caption`, `heading`, and `overline`.

```python
from python_ui_library.components import Text

title = Text("Account", role="heading")
details = Text("Long selectable details", selectable=True, word_wrap=True)
```

`Card(parent=None, *, shadow=True)` subclasses `QFrame`, renders the theme-defined
subtle shadow by default, and exposes its padded `QVBoxLayout` as `content_layout`.
Use `shadow=False` for dense/repeated Card collections. `Divider(orientation=Qt.Horizontal,
parent=None)` subclasses
`QFrame` and accepts only `Qt.Horizontal` or `Qt.Vertical`.

```python
from python_ui_library.components import Card, Divider, Text

card = Card()
card.content_layout.addWidget(Text("Summary", role="heading"))
card.content_layout.addWidget(Divider())
```

## Fields

`TextInput`, `NumberInput`, and `SelectInput` are `QWidget` compositions. Their native
input is public as `control`; common value methods and native signals are also exposed
directly on the Component. A visible label becomes the control's accessible name and
focus buddy. Description and caller-provided error text become its accessible
description. `setErrorText("")` clears error presentation; components never validate or
persist consumer data themselves.

```python
from PySide6.QtWidgets import QCompleter

from python_ui_library.components import NumberInput, SelectInput, TextInput

name = TextInput(
    label="Name",
    description="Shown in exports",
    placeholder="Ada Lovelace",
)
name.textChanged.connect(on_name_changed)
name.setErrorText("A name is required")
name.setCompleter(QCompleter(["Ada Lovelace", "Grace Hopper"], name))

code = TextInput(label="Code", input_mask="AA-0000;_")
if not code.hasAcceptableInput():
    code.setErrorText("Enter two letters and four digits")

count = NumberInput(kind="integer", minimum=1, maximum=20, value=1, label="Count")
price = NumberInput(kind="decimal", decimals=2, step=0.25, label="Price")
count.valueChanged.connect(on_count_changed)

choice = SelectInput(("Alpha", "Beta"), label="Choice")
choice.currentIndexChanged.connect(on_choice_changed)
# Full native APIs remain available when needed:
choice.control.setModel(application_model)
```

`TextInput` forwards native `QValidator`, input-mask, and `QCompleter` behavior. The
library does not run asynchronous suggestion work; a consumer may update its completer
model on the GUI thread after its own application work finishes.

`NumberInput.kind` is either `integer` (`QSpinBox`) or `decimal` (`QDoubleSpinBox`).
Ranges, steps, decimals, and value changes use those native controls without parsing
strings. `CheckBox(text, parent=None)` directly subclasses `QCheckBox` and preserves
native `toggled`, `checkStateChanged`, and tri-state behavior. `Switch(text,
parent=None)` is a painted, two-state `QCheckBox` for settings that take effect
immediately; it preserves native focus, Space-key activation, checked state, and
signals.

```python
from python_ui_library.components import CheckBox, Switch

enabled = CheckBox("Enable summaries")
enabled.toggled.connect(on_summary_toggled)

automatic = Switch("Update automatically")
automatic.toggled.connect(on_automatic_changed)
```

Run `python gallery/main.py` from an editable installation to inspect variants, field
feedback, disabled states, resizing, and keyboard focus.
