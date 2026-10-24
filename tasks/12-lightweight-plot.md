# Agent task 12 — General-purpose, lightweight Plot Component

**Status:** owner-requested post-v0.1 scope addition; the locked D13 decision **must be amended before implementation** following the repository's change procedure.  
**Repository:** `alp-ui` (`alp_ui` import root), installed locally by consumers; no PyPI requirement.  
**Consumer evidence:** `../alpacaDesktop/docs/design/prototypes/training-first/app.js`: CNN loss **line** curves and Random Forest feature-importance **bars**; see the [consumer gap audit](../../alpacaDesktop/docs/design/ALP_UI_TRAINER_GAP_AUDIT.md) in the sibling repo.

## 1. User need, alternatives and authorization boundary

The repository owner explicitly requests that consumer applications be able to show plots using `alp-ui`, not necessarily plots specialized for training. The Trainer demonstrates two distinct reusable shapes: a numeric x–y line plot that changes as values arrive, and a categorical bar plot. Other consumers should supply plain data and labels without implementing their own theme-aware axes, legend, spacing, empty state and basic accessibility from scratch.

**Smallest suitable public addition:** one read-only **`Plot` Component** with `kind="line"` and `kind="bar"`. Use native `QWidget`/`QPainter`, Qt text metrics and Theme tokens, not a full charting engine. The library owns **rendering**, not scientific metrics, transformations, aggregation, chart data collection or update cadence.

**Alternatives evaluated at planning time:**

1. **Consumer-written QPainter widgets:** technically feasible and currently allowed, but duplicate generic axes/legend/density/empty-state rules now that the owner asks for reusable plotting.
2. **Qt Charts / PySide6-Addons, matplotlib, pyqtgraph:** unnecessary for the demonstrated two simple plots and contrary to D03's single `PySide6-Essentials` runtime-dependency contract. Do not introduce them, even as optional extras.
3. **QGraphicsView or model/view plotting abstraction:** not needed for these static/read-only shapes; native `QPainter` is the smaller baseline. If an existing Qt primitive clearly reduces code without a new dependency, document and reuse it.

### Required locked-decision review (before code)

`docs/project/DECISIONS.md` **D13** currently excludes plots and charting tasks **in any phase**. `docs/project/COMPONENT_CATALOG.md`, `docs/project/SPEC.md`, `docs/project/PRIMER.md`, `docs/project/QUALITY.md`, and `README.md` also document the old exclusion. The repository owner's explicit instruction on 24 October 2026 authorizes this limited change in direction. **Do not silently ignore the locked text**: record the amendment and its consequences before code. No additional owner decision is needed for the stated dependency-free line/bar scope; ask only if implementation would require a larger departure. The implementing agent must record an owner-approved, dated ADR-like amendment with:

- **Problem / named consumer:** lightweight numeric line and categorical bar data visualizations required by the Trainer and other consumer applications.
- **Alternatives rejected:** repeated app-local QPainter implementation or new plotting/Qt Addons dependencies; reasons above.
- **Decision:** D13 now excludes **third-party plotting dependencies, advanced charting, waveform and spectrogram visualization**, while allowing **one native Qt-painted generic read-only Plot Component** as an explicit **post-v0.1** extension. Initial v0.1 scope remains historically accurate; no unsupported release claim.
- **Consequences:** extra Qt rendering tests, chart accessibility/visual qualification, no changes to D02/D03/D07/D08/D12 or licensing/runtime dependency policy.
- **Acceptance:** tests below, Gallery + independent built-wheel consumer, separate native Windows qualification.

Update the authoritative decision, catalog and post-v0.1 specification/plan together **before implementing Plot**. Any further scope conflict requires owner approval; no mandate to create graph frameworks. Keep README and `docs/components.md` factual about what is actually shipped; update them when the API exists. If the stated narrow amendment cannot be recorded or reveals a genuine incompatibility, stop **task 12**, report the conflict and continue independent tasks 10 and 11.

## 2. Source search / ownership

Read `AGENTS.md` in its prescribed order. Inspect `docs/project/{DECISIONS,SPEC,COMPONENT_CATALOG,GLOSSARY,QUALITY,THEME_ALPACA_LIGHT}.md`, `src/alp_ui/components/{data,feedback}.py`, `src/alp_ui/theme/{tokens,install,appearance}.py`, `gallery/main.py`, `docs/components.md`, and tests for Components, Theme and packaging. Search the repo for existing plotting/rendering helpers and re-use appropriate existing Theme/font/paint infrastructure. `DataTable` already consumes external data and `QPainter` is already used to draw native details in `inputs.py`; neither is a Plot or chart renderer.

A `Plot` is a **Component** under the existing Glossary. Data *series* and *category* are plain chart descriptors, not scientific entities. Do not introduce terms such as Training Run, Dataset, Source Recording or feature importance in public symbols or Gallery examples. Generic visible labels should say e.g. “Time”, “Value”, “Category”, “No data to display”.

## 3. Minimal public API to implement

Proposed signatures, subject to evidence-backed refinement **before implementation**:

```python
from alp_ui.components import Plot

line = Plot(kind="line", x_label="Time (s)", y_label="Value")
line.setLines({
    "Series A": [(0.0, 0.3), (1.0, 0.4), (2.0, 0.7)],
    "Series B": [(0.0, 0.5), (1.0, 0.45), (2.0, 0.55)],
})

bars = Plot(kind="bar", x_label="Category", y_label="Value")
bars.setBars([("A", 0.62), ("B", 0.24), ("C", 0.14)])
```

- **Qt:** subclass `QWidget`; ordinary Qt parenting, layout, sizeHint/minimumSizeHint and `update()` semantics. Public kind choices are exactly `line` and `bar`. No Plot-specific dependency. Choose one minimal internal representation per kind; don't invent a general chart schema or domain model.
- **Data semantics:** line data: ordered mapping `label -> sequence of (finite numeric x, finite numeric y)` points; bar data: ordered sequence of `(nonempty category label, finite numeric value)` pairs. Preserve caller-supplied series, point and category ordering. Labels are plain text and may contain Unicode. Validation catches nonnumeric/nonfinite values and malformed pairs **at the public data boundary**, with useful errors; no silent dropping or rounding of scientific values.
- **Empty state:** an empty data set is valid, draws a neutral “No data to display” message, and does not fabricate a zero data point. Empty individual series and single-point series are legitimate. Chart setter updates repaint the widget but do not start work or a timer. Do not silently connect data across missing/undefined values; callers must resolve absent data before passing it.
- **Line view:** x/y numeric axes with readable automatic tick labels; one or more labeled series, point/line rendering, simple legend. Handle flat, negative, positive, and small decimal ranges without division-by-zero or fake precision. If x values are not monotonic, either render in input order without re-sorting (and document it) or reject with a clear rule and test. Do not add smoothing or statistical derivation. Keep y-axis scaled to supplied data (do not force a misleading zero unless justified/documented).
- **Bar view:** one category axis and one numeric value axis, zero baseline, negative and positive values; a single readable bar per input item with a common neutral theme-derived appearance. Make long category names and narrow layouts usable through documented elision/tooltip/full accessible data rather than overflowing; don't quietly reorder by size.
- **Visual composition:** title/caption and surrounding Cards belong to the consumer. `Plot` draws axes, ticks, data, optional simple legend, and empty feedback. Use Theme colors/typography/spacing; no hard-coded palette or scientific color meanings. For multiple lines differentiate by **line style or marker as well as color**. Default Bar needs no rainbow. Standard vs compact affects spacing, not hiding essential labels. No per-point child QWidgets, global QSS, or unbounded widget trees.
- **Accessibility:** meaningful `accessibleName` supplied by the consumer (e.g. “Measurements”), with `accessibleDescription` summarizing chart type and series/category counts; give a concise semantic text alternative when data updates. Color must not be the sole series distinction. The public docs must say: **a plot does not replace a readable numeric summary or DataTable** for precise values or assistive access. Test native accessibility properties; do not pretend a painted widget exposes individual data points as OS-level accessible children if not implemented.
- **Resizing and scaling:** redraw from current bounded caller data on Qt paint/resize; no eager re-layout per new sample, no internal files/network/worker. The consumer decides when to supply updated data and how often; the Plot must not create a polling timer, Trainer-specific epoch model, plot persistence, or an app-run controller.
- **Non-goals:** zoom, pan, cursors, selection, exporting images/CSV, plotting functions, arbitrary rich HTML labels, heatmaps, waveforms, spectrograms, stacked charts, subplots, smoothing, multiple y-axes, live socket feeds or an analytics engine. Add only upon separate evidence and approval.

If one component with two simple kinds becomes significantly more complex than two small native widgets during investigation, record the evidence and propose **two explicitly scoped Components** before implementation; do not broaden the API or build a framework on speculation.

## 4. Files and documentation

- One small, owned module such as `src/alp_ui/components/plots.py`, plus public export in `src/alp_ui/components/__init__.py`.
- Add concise `Plot` documentation with examples for both kinds in `docs/components.md`; include data shape, axes, no-numeric-data behavior, accessibility, and consumer-owned data updates.
- Add generic line and bar examples to `gallery/main.py`, and only minimal consumer-example coverage where needed to prove installed-wheel API import and resizing. The Gallery uses generic series such as “Observed” and “Reference”, not Trainer domain objects.
- Update `docs/project/{DECISIONS,SPEC,COMPONENT_CATALOG,IMPLEMENTATION_PLAN,QUALITY}.md` for the approved post-v0.1 scope. If `README.md` or other guides currently claim plots are excluded, update those **after** implementation to avoid advertising a nonexistent feature. Amend the Glossary only if a truly new shared library concept beyond **Component** is necessary.
- Never add `matplotlib`, `pyqtgraph`, `PySide6-Addons`, `QtCharts`, networking or icon dependencies; legal notices must stay truthful.

## 5. Tests and acceptance (planned until actually run)

| Level | Fixture / operation | Expected observable behavior |
|---|---|---|
| Pure/Qt Component | Empty line/bar data, then one point/bar | Neutral empty state; no crash or invented values; later repaint reflects supplied input. |
| Pure/Qt Component | Repeated updates with two labeled short line series | Preserved series and point order, data boundary validation, no worker/timer; correct legend and number of series. |
| Pure/Qt Component | Negative, all-zero, constant, extreme-small, positive ranges | Valid axis bounds/ticks; no NaN, division-by-zero, nonsensical scaling or invisible zero baseline. |
| Pure/Qt Component | Malformed pairs, `NaN`/infinity, nonnumeric values, bad `kind` | Useful early errors, no partial or silently corrupted data state. |
| Pure/Qt Component | Unicode/long category labels and 20–50 synthetic bars | Bars remain distinct; content not painted outside bounds; labels handled as documented; supplied order preserved. |
| Qt layout | Small/narrow width, expansion, 100%/150% scaling, standard/compact Theme and custom Theme tokens | Axes and essential information remain readable or degrade explicitly; no clipped foreground without defined fallback. |
| Qt accessibility | Named plot, new data, disabled/hidden widget, color differentiation | Accessible name/summary updates; non-color visual distinction for multiple series; numeric alternative documented. |
| Rendering regression | Offscreen or native rendered plot images + meaningful pixel/geometry checks | Actually draws axes, lines/bars, empty state; no background-only false pass. Avoid brittle OS-specific pixel snapshots as sole proof. |
| Installed-wheel consumer | Fresh environment, import `Plot`, render both kinds under `install_theme(app)` | No source-tree dependency, network or extra runtime requirement. |
| Native release | Windows x86-64, keyboard/Narrator as relevant, 100%/150% DPI and real Gallery review | Recorded Windows evidence required; macOS/offscreen tests not a substitute. |

For common updates, exercise at least two series with hundreds of points without per-point widgets or GUI work outside `paintEvent`/`update()`; document any measured redraw limits rather than inventing a universal performance claim. No WAVs, TensorFlow/PyTorch, Training Runs, or scientific metric fixtures are necessary in `alp-ui`. The **Trainer** must separately test that its own loss/feature values and correct units are passed to `Plot`, and that undefined scores are not falsely displayed as valid. Use small generated in-memory data for UI tests. Preserve existing quality/packaging and lint gates listed in `AGENTS.md`.

## 6. Completion gate

A separately installed consumer can embed a themed `Plot` and present small line or categorical-bar data sets through documented Qt methods, without implementing axes or adding a plotting package. The interface remains about **presentation**, not training or the origin/meaning of data. D13's amended scope is recorded, D03 remains intact, no released API is advertised before code exists, and genuine public-API/visual/accessibility/Windows/built-wheel evidence is reported honestly.
