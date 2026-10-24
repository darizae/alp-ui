# Components

Create the consumer application's one `QApplication` and install the Theme before
constructing Components. All imports below come from `alp_ui.components`.
Components preserve Qt parenting, focus, enabled state, keyboard behavior, and native
signals; they do not own application data or work.

## Button

Use `Button` for an action. `Button(text, parent=None, *, variant="primary",
size="medium", loading=False, loading_text="Loading…")` subclasses `QPushButton`.
Variants are `primary`, `secondary`, `outline`, and `danger`; sizes are `small`,
`medium`, and `large`. Inherited `clicked`, `pressed`, shortcuts, icons, and enabled
state remain available.

`setLoading(True)` changes the visible and accessible label and prevents activation;
it starts no work. Prefer a text label, or set an accessible name when using only an
icon.

```python
from alp_ui.components import Button

save = Button("Save", variant="primary")
save.clicked.connect(save_document)
save.setLoading(True)
```

Button provides a natural size hint, but ordinary Qt layouts remain authoritative: a
grid column can stretch it, while an aligned row keeps it content-sized. The Gallery
uses aligned rows so variants and sizes are shown representatively.

## Text

Use `Text` for styled interface copy. `Text(text, parent=None, *, role="body",
selectable=False, word_wrap=False)` subclasses `QLabel`; roles are `title`, `heading`,
`subheading`, `body`, `caption`, and `overline`. It adds no signals beyond `QLabel`.
Enable wrapping for long or translated text, and use heading roles in logical reading
order.

```python
from alp_ui.components import Text

title = Text("Account", role="heading")
details = Text("Long selectable details", selectable=True, word_wrap=True)
```

## Card

Use `Card(parent=None, *, shadow=True)` to group related content on a bordered surface.
It subclasses `QFrame` and exposes its padded `QVBoxLayout` as `content_layout`; it adds
no custom signals. Use `shadow=False` for dense or repeated Cards. Child content must
provide the meaningful accessible labels because the surface itself is structural.

```python
from alp_ui.components import Card, Text

card = Card()
card.content_layout.addWidget(Text("Summary", role="heading"))
```

## Divider

Use `Divider(orientation=Qt.Horizontal, parent=None)` to separate adjacent content. It
subclasses `QFrame`, accepts only `Qt.Horizontal` or `Qt.Vertical`, and adds no signals.
A Divider is visual structure; do not rely on it as the only accessible indication of a
section change.

```python
from PySide6.QtCore import Qt
from alp_ui.components import Divider

horizontal = Divider()
vertical = Divider(Qt.Vertical)
```

## TextInput

Use `TextInput(text="", parent=None, *, label="", description="", error="",
placeholder="", validator=None, input_mask="", completer=None)` for labeled text entry.
It is a `QWidget` composition whose native `QLineEdit` is available as `control`.
`textChanged` and `editingFinished` are forwarded, along with common text, validator,
input-mask, completer, and read-only methods.

The visible label becomes the control's accessible name and focus buddy. Description
and error text become its accessible description. The consumer owns validation and any
work that supplies completion values.

```python
from PySide6.QtWidgets import QCompleter
from alp_ui.components import TextInput

name = TextInput(label="Name", placeholder="Ada Lovelace")
name.textChanged.connect(on_name_changed)
name.setCompleter(QCompleter(["Ada Lovelace", "Grace Hopper"], name))
name.setErrorText("A name is required")
```

## NumberInput

Use `NumberInput(parent=None, *, kind="integer", value=None, minimum=None,
maximum=None, step=None, decimals=2, label="", description="", error="")` for bounded
numeric entry. `kind="integer"` uses `QSpinBox`; `kind="decimal"` uses
`QDoubleSpinBox`. The native control is `control`, and `valueChanged` plus common range,
step, and value methods are forwarded. Labels and feedback use the same accessibility
mapping as `TextInput`; the Component never parses units or strings.

```python
from alp_ui.components import NumberInput

count = NumberInput(kind="integer", minimum=1, maximum=20, value=1, label="Count")
price = NumberInput(kind="decimal", decimals=2, step=0.25, label="Price")
count.valueChanged.connect(on_count_changed)
```

## SelectInput

Use `SelectInput(items=(), parent=None, *, label="", description="", error="")` for a
bounded choice. It is a `QWidget` composition around the public `QComboBox` in
`control`. `currentIndexChanged` and `currentTextChanged` are forwarded, along with
common item, index, and model methods. Supply a visible label, or set the control's
accessible name when context provides no label.

```python
from alp_ui.components import SelectInput

choice = SelectInput(("Alpha", "Beta"), label="Choice")
choice.currentIndexChanged.connect(on_choice_changed)
choice.setModel(application_model)
```

## FolderPicker

Use `FolderPicker(parent=None, *, label="")` to display a selected local folder and
let the user choose another one with the operating system's native directory dialog.
It is a `QWidget` composition around a read-only `QLineEdit` in `control` and an
outline `Choose folder` Button. `setFolderPath(path)` and `folderPath()` preserve the
consumer-provided string exactly; an empty string means no selection. `folderChanged`
emits that string only when it changes, whether set by the consumer or selected from
the dialog. Cancel leaves the prior value untouched.

The label is the path field's accessible name, and the full path is exposed through
its accessible description and tooltip even when the field cannot show it all. The
Component does not resolve, validate, read, scan, persist, or monitor a folder. React
to `folderChanged` from consumer-owned application code.

```python
from alp_ui.components import FolderPicker

folder = FolderPicker(label="Folder")
folder.folderChanged.connect(scan_selected_folder)
folder.setFolderPath("/Users/example/audio")
selected_path = folder.folderPath()
```

## CheckBox

Use `CheckBox(text="", parent=None)` for an optional or multi-select choice. It directly
subclasses `QCheckBox` and preserves native `toggled`, `checkStateChanged`, tri-state,
focus, and Space-key behavior. Its text is the accessible name; set one explicitly if
the visible text is empty.

```python
from alp_ui.components import CheckBox

enabled = CheckBox("Enable summaries")
enabled.toggled.connect(on_summary_toggled)
```

## Switch

Use `Switch(text="", parent=None)` for a two-state setting that takes effect
immediately. It is a painted `QCheckBox` with native `toggled`, checked state, focus,
and Space-key behavior. Tri-state mode is rejected. Its visible text supplies the
accessible name; describe the resulting setting, not the gesture.

```python
from alp_ui.components import Switch

automatic = Switch("Update automatically")
automatic.toggled.connect(on_automatic_changed)
```

## Badge

Use `Badge(text="", parent=None, *, intent="neutral")` for compact read-only feedback.
It subclasses `QLabel` and adds no signals. Generic intents are `neutral`, `info`,
`success`, `warning`, and `danger`; unknown values fail at construction. The text is
the accessible name and the intent is included in the accessible description, so use
meaningful text rather than color alone.

```python
from alp_ui.components import Badge

availability = Badge("Available", intent="success")
```

## Alert

Use `Alert(text, parent=None, *, title="", intent="neutral", action=None)` for
persistent inline feedback. It subclasses `QFrame`, supports the same generic intents
as `Badge`, and reparents an optional consumer-supplied action widget into its layout.
It adds no notification bus or custom signal; connect the action's native signal. The
accessible name includes the intent and title or text, while the body becomes the
description when a title is present.

```python
from alp_ui.components import Alert, Button

retry = Button("Retry", variant="outline", size="small")
message = Alert(
    "Try again when the connection returns.",
    title="Connection unavailable",
    intent="danger",
    action=retry,
)
retry.clicked.connect(retry_connection)
```

## ProgressBar

Use `ProgressBar(parent=None, *, minimum=0, maximum=100, value=0)` to present progress
owned by the consumer. It subclasses `QProgressBar`; native `valueChanged`, range,
format, orientation, and text visibility remain available. A zero minimum and maximum
select Qt's indeterminate mode. It never creates a worker. Replace the default
accessible name, `Progress`, when multiple operations are visible.

```python
from alp_ui.components import ProgressBar

progress = ProgressBar(value=40)
progress.setAccessibleName("Export progress")
waiting = ProgressBar(minimum=0, maximum=0)
```

## EmptyState

Use `EmptyState(title, parent=None, *, text="", icon=None, action=None)` when a view has
no content. It is a `QWidget` composition that accepts an optional `QIcon` and reparents
an optional action widget. It adds no signals or data fetching. The title is the
accessible name and supporting text is the description; treat the icon as decorative
unless the text conveys the same meaning.

```python
from PySide6.QtWidgets import QStyle
from alp_ui.components import EmptyState

empty = EmptyState(
    "No items",
    text="Add an item to get started.",
    icon=app.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView),
)
```

## DataTable

Use `DataTable(parent=None, *, model=None)` to display a caller-owned
`QAbstractItemModel`. It subclasses `QTableView`; native `clicked`, `doubleClicked`,
`activated`, keyboard navigation, selection model, header resizing, and scrollbars
remain available. Pass a model at construction or with inherited `setModel()`.

The Component owns view appearance only. The consumer owns records, column meaning,
edits, sort/filter proxy models, and persistence. No rows are copied and no widgets are
installed per cell. Sorting is not enabled implicitly. Give each table a contextual
accessible name when the surrounding label is insufficient.

```python
from PySide6.QtCore import QSortFilterProxyModel
from alp_ui.components import DataTable

proxy = QSortFilterProxyModel()
proxy.setSourceModel(application_model)
table = DataTable(model=proxy)
table.setAccessibleName("Accounts")
table.clicked.connect(open_selected_record)
```

Run the native Gallery to inspect every Component, variant, disabled/error state,
keyboard focus, and empty or large-model table without a backend:

```bash
python -m gallery.main
```

The Gallery uses the default `standard` density and ordinary Qt layouts. Its action
and feedback examples keep their natural size; fields, Cards, Alerts, progress bars,
and DataTables expand where width communicates their real layout behavior.

## Density and interaction

Components share state colors from `theme.appearance.interactions`, a startup
`Theme.density` choice, and consistent control geometry. `Button("Cancel",
variant="secondary")` is intentionally quiet: slate surface, muted border, and
subtle hover; amber remains available as the semantic `colors.secondary` accent.

`TextInput`, `NumberInput`, and `SelectInput` use the same height and stable one-pixel
focus border (changing its color, not width). Select/spin controls retain their
native Qt models, signals, editing, keyboard, popup and step behavior but paint
original minimal arrows. `CheckBox` paints a matching indicator while retaining Qt's
label layout and checked state; `Switch` retains its painted two-state toggle.

`DataTable` uses row selection, quiet highlights, and row heights determined by
density; no per-cell QWidget objects are created. The optional Card shadow remains,
but prefer `Card(shadow=False)` for content-dense pages to avoid repeated box
borders/effects.

To see these controls in an application-like composition (not an exported Sidebar or
routing framework), run `python -m gallery.showcase`. This screen intentionally uses
native Qt layouts and a caller-owned `QAbstractTableModel`.
