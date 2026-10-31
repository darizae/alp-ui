# Project component catalog and public API boundaries

**Rule:** use existing Qt behavior first. A public component needs tangible added visual consistency or generic interaction. Names below are intended public concepts, not exhaustive method signatures. Keep ordinary Qt inherited methods/signals available.

## v0.1 — required components

| Component | Qt foundation | Public choices / behavior | Explicit non-responsibility |
|---|---|---|---|
| `Button` | `QPushButton` | `variant`: `primary`, quiet `secondary`, `outline`, `danger`; optional `size` (small/medium/large); native `clicked`; disabled, focus, and consumer-controlled loading presentation | Does not execute jobs, persist state, or manage application-wide async operations. |
| `Text` | `QLabel` | Semantic role `title`, `heading`, `subheading`, `body`, `caption`, `overline`; mouse- and keyboard-selectable by default with an explicit opt-out | Does not implement markdown editor or layout engine. |
| `Card` | `QFrame`/`QWidget` + Qt layout | Background, border, padding, theme-defined subtle shadow with opt-out | Does not store a data object or own navigation. |
| `Divider` | `QFrame` | Horizontal/vertical separator, theme border | No page system. |
| `TextInput` | `QLineEdit` | Label/description/error presentation; placeholder; native `textChanged`, `editingFinished`, validator, input-mask, and `QCompleter` APIs | Does not own form submission, schema validation, asynchronous work, or suggestion loading. |
| `NumberInput` | `QSpinBox`/`QDoubleSpinBox` | Type-specific native limits/step/decimals; label/error presentation | No manual string-number parser or magical units conversion. |
| `SelectInput` | `QComboBox` | Label/help/error; native model/items and `currentIndexChanged` | No app-specific dropdown data loader. |
| `CheckBox` | `QCheckBox` | Consistent typography/spacing, native checkable state/signal | Does not imply the immediate-action semantics of a Switch. |
| `Switch` | `QCheckBox` | Two-state switch appearance; native checked state, signal, keyboard, focus, and accessibility behavior | No tri-state meaning, persistence, or feature-flag service. |
| `Badge` | `QLabel` or small custom `QWidget` | Validated `intent`: neutral/info/success/warning/danger at construction or through `setIntent`; updates semantic styling and accessibility in place | No domain status mapping. |
| `Alert` | `QFrame` + labels/layout | Intent, title/body, optional actions supplied by consumer | No global notification bus or persistence. |
| `ProgressBar` | `QProgressBar` | Determinate/indeterminate using native semantics; theme styles | No computation/thread/process controller. |
| `DataTable` | `QTableView` | Styled header, whole-row selection, muted state highlights, density-aware rows; accepts **external `QAbstractItemModel`** | No parallel Python list/table schema, business-level filters, or lazy filesystem discovery. |
| `EmptyState` | QWidget composition | Text, optional illustration using Qt standard icon, optional consumer-supplied action widget | No automatic data fetching. |

## Owner-approved post-v0.1 extensions

| Component | Qt foundation | Public choices / behavior | Explicit non-responsibility |
|---|---|---|---|
| `HelpHint` | `QToolButton` | Required plain-text explanation, optional accessibility subject, native tooltip and What's This view, native clicked/focus/keyboard behavior | No field wrapping, tooltip manager, popup framework, help-content lookup, translations service, or domain behavior. |
| `FolderPicker` | `QWidget` composition with read-only `QLineEdit`, `Button`, and `QFileDialog` | Optional label, optional hidden-directory visibility, exact path `setFolderPath`/`folderPath`, and one `folderChanged(str)` signal for actual changes; Cancel preserves the prior selection | Does not resolve, validate, scan, persist, monitor, or interpret folder contents. |

`TextInput`, `NumberInput`, and `SelectInput` may each use a small internal `FieldFrame`/label composition once **two real implementations** show meaningful shared behavior. Do not make an elaborate field framework in advance.

## Post-v0.1 candidates — outside initial release

- `Plot` — authorized post-v0.1: native `QWidget`/`QPainter` presentation of ordered finite numeric line series or ordered categorical bars. It provides axes, a simple line legend, empty feedback, Theme alignment, and a text summary through native accessibility properties. It does not own scientific meaning, data collection, a model/view schema, timers, zoom/pan, selection, export, smoothing, multiple axes, waveforms, or spectrograms.
- `IconButton` (only after icon design is satisfactory), `ButtonGroup` (Qt native group may suffice), `SearchInput` (likely `TextInput` composition), `Tabs`, `Sidebar`, `PageHeader`, `ConfirmDialog`, `FilePicker`, `DropZone`, advanced date/range widgets, and toasts.
- The candidates after `Plot` are **backlog candidates, not authorized phase deliverables**. Promote one only after a consumer demonstrates need, it is specified, and a named task is approved. Native `QTabWidget`, `QFileDialog`, `QMessageBox`, etc. can already be used directly by consumers.
- No chart adapters, third-party plotting dependencies, advanced charting, waveform, or spectrogram Components are authorized.

## Behavior contract across components

- Preserve normal QWidget parenting, focus, event loop, tab ordering, keyboard shortcuts, signal semantics, tooltips, and enabled/disabled behavior.
- Avoid reraising native events as duplicate custom signals unless a real consumer needs transformed semantics.
- Prefer `QSizePolicy`, `sizeHint`, and Qt layouts over hardcoded widths and heights. Honor UI scaling and long/localized labels.
- Render empty/invalid/loading only where conceptually applicable; don't add a generic state machine to every component.
- Accessible names and descriptions must reflect visible labels; keyboard-only use cannot depend on hover.
- Constructors shouldn't mutate global theme or create a `QApplication`. Components read the installed theme or sensible default.
- Do not provide style customization as an unrestricted per-component dictionary; consuming apps use semantic Theme overrides and standard Qt APIs.
- No user-facing methods or components named for Alpaca (except the **theme preset** name).

## Theme interaction and model/view constraints

`DataTable` never copies the full model into cells. Sorting/filtering are application-owned or use native Qt proxy models when a consumer explicitly opts in. When there is no model, the table shows a documented empty state without becoming the owner of data. Model updates should flow through Qt model notifications. For very large datasets, tests should confirm widgets are not created per cell.

## In-scope gallery categories

Actions, Typography, Surfaces, Fields, Feedback, and Data. Each exhibits all implemented variants and meaningful states, with keyboard instructions and copyable Python examples maintained in Markdown docs (not generated JS). The separate Showcase demonstrates composition without adding Sidebar, navigation, or page-shell Components.
