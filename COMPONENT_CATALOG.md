# Component catalog and public API boundaries

**Rule:** use existing Qt behavior first. A public component needs tangible added visual consistency or generic interaction. Names below are intended public concepts, not exhaustive method signatures. Keep ordinary Qt inherited methods/signals available.

## v0.1 — required components

| Component | Qt foundation | Public choices / behavior | Explicit non-responsibility |
|---|---|---|---|
| `Button` | `QPushButton` | `variant`: `primary`, `secondary`, `outline`, `danger`; optional `size` (small/medium/large); native `clicked`; disabled + focus states | Does not execute jobs, persist state, or manage application-wide async operations. |
| `Text` | `QLabel` | Semantic role `body`, `caption`, `heading`, `overline`; optional selectable text | Does not implement markdown editor or layout engine. |
| `Card` | `QFrame`/`QWidget` + Qt layout | Background, border, padding, optional header/content layout slots where evidence justifies | Does not store a data object or own navigation. |
| `Divider` | `QFrame` | Horizontal/vertical separator, theme border | No page system. |
| `TextInput` | `QLineEdit` | Label/description/error presentation; placeholder; native `textChanged`, `editingFinished`; optional validator passthrough | Does not own form submission or schema validation. |
| `NumberInput` | `QSpinBox`/`QDoubleSpinBox` | Type-specific native limits/step/decimals; label/error presentation | No manual string-number parser or magical units conversion. |
| `SelectInput` | `QComboBox` | Label/help/error; native model/items and `currentIndexChanged` | No app-specific dropdown data loader. |
| `CheckBox` | `QCheckBox` | Consistent typography/spacing, native checkable state/signal | No custom switch painting in v0.1. |
| `Badge` | `QLabel` or small custom `QWidget` | `intent`: neutral/info/success/warning/danger; outlined/filled only when tests justify both | No domain status mapping. |
| `Alert` | `QFrame` + labels/layout | Intent, title/body, optional actions supplied by consumer | No global notification bus or persistence. |
| `ProgressBar` | `QProgressBar` | Determinate/indeterminate using native semantics; theme styles | No computation/thread/process controller. |
| `DataTable` | `QTableView` | Styled header, selection, alternate rows if validated; accepts **external `QAbstractItemModel`** | No parallel Python list/table schema, business-level filters, or lazy filesystem discovery. |
| `EmptyState` | QWidget composition | Text, optional illustration using Qt standard icon, optional consumer-supplied action widget | No automatic data fetching. |

`TextInput`, `NumberInput`, and `SelectInput` may each use a small internal `FieldFrame`/label composition once **two real implementations** show meaningful shared behavior. Do not make an elaborate field framework in advance.

## Post-v0.1 candidates — outside initial release

- `IconButton` (only after icon design is satisfactory), `ButtonGroup` (Qt native group may suffice), `SearchInput` (likely `TextInput` composition), `Switch` (custom interaction costs), `Tabs`, `Sidebar`, `PageHeader`, `ConfirmDialog`, `FilePicker`, `FolderPicker`, `DropZone`, advanced date/range widgets, and toasts.
- These are **backlog candidates, not authorized phase deliverables**. Promote an item only after a consumer demonstrates need, it is specified, and a named task is approved. Native `QTabWidget`, `QFileDialog`, `QMessageBox`, etc. can already be used directly by consumers.
- **No plots or chart adapters in any phase.**

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

Actions, Typography, Surfaces, Fields, Feedback, and Data. Each exhibits all implemented variants and meaningful states, with keyboard instructions and copyable Python examples maintained in Markdown docs (not generated JS).
