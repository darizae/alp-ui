# Task 05 — Model/view DataTable

**Dependencies:** Task 04 completed. **Task type:** single data-heavy reusable widget.

## Read first

`AGENTS.md`, `docs/project/COMPONENT_CATALOG.md`, `docs/project/SPEC.md` (§5), `docs/project/THEME_ALPACA_LIGHT.md`, `docs/project/QUALITY.md`, and the visual references listed for this task in the ignored `references/SOURCE_MAP.md`.

## Work

1. Implement `DataTable` as a documented styled `QTableView` subclass/composition. Its authoritative input is a caller-provided `QAbstractItemModel`; do **not** define another table-row schema or own data.
2. Adapt Alpaca's slate-50 header background, slate-200 border, muted uppercase monospace header text and compact vertical padding through Qt header style/delegate/size hints. Do not imitate web overflow containers.
3. Respect normal Qt keyboard table navigation, row selection, scrollbars, header resizing and model notifications. Styling must not introduce cell widgets for every row.
4. Include gallery mock `QAbstractTableModel` with 10,000 rows to exercise virtualized Qt view rendering, without network or backend data.
5. Add tests for model replacement, `dataChanged` and reset handling, selection, empty model, no implicit sort/filter/reorder, header theme and accessibility.
6. Document explicitly what the consumer owns (data model, sort proxies, business columns, persistence) and what the library owns (view appearance and native Qt integration).

## Artifacts

`components/data.py` (or justified module), `DataTable` export, gallery dataset model/example, tests and usage docs.

## Acceptance

- [ ] Works with arbitrary valid caller-supplied `QAbstractItemModel`.
- [ ] A 10,000-row model loads/scrolls without creating per-cell QWidget objects or copying rows into a secondary model.
- [ ] Qt selection, header, scrollbar and model notifications work.
- [ ] MUI table style intent is recognizable but native Qt behavior is preserved.
- [ ] No application-specific data/status mappings or arbitrary sorting introduced.

**Owner checkpoint:** review data table usability and header aesthetics. Corrections should remain targeted, not create a separate rendering framework.
