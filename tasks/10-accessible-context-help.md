# Agent task 10 — Accessible contextual help for Qt Widgets consumers

**Status:** owner-requested post-v0.1 Component extension; specified for agent implementation.  
**Library:** `alp-ui` (`alp_ui` public Python import, local wheel; no PyPI)  
**Evidence:** `alpacaDesktop/docs/design/ALP_UI_TRAINER_GAP_AUDIT.md` in the sibling repository; Trainer prototype at `../alpacaDesktop/docs/design/prototypes/training-first/app.js` and `styles.css`.

## 1. Problem and smallest justified change

The **alpaca Desktop Trainer** prototype contains a repeated `?` beside form labels and section headings. Its `tip(...)` helper occurs 34 times. The same explanation must be discoverable by pointer users **and** keyboard users, rather than depending on hover. The current public `alp_ui.components` inventory has no such Component. Recreating the same small help button, popup, focus treatment, accessible name and description dozens of times in each consumer would repeat generic presentation logic.

**Deliver one reusable `HelpHint` Component** implemented using native Qt Widgets. It is a *small control displaying short contextual text*, not a global tooltip manager, form system, documentation viewer or popup framework. No Trainer-specific terminology or behavior enters the library.

This assignment is **limited to contextual help**. The repository owner has also requested generic folder selection and plotting as separate, independently testable follow-ups: [task 11](11-native-folder-picker.md) and [task 12](12-lightweight-plot.md). Do not add either within task 10. The plotting scope requires the explicit, recorded post-v0.1 D13 amendment specified in task 12; D03 still forbids additional plotting/runtime dependencies. Progress stages, wizards, data loaders, job controllers, and application-specific statuses remain outside the library.

## 2. Read and inspect before changing code

Follow `AGENTS.md` and its full onboarding sequence. In particular inspect:

- `docs/project/PRIMER.md`, `GLOSSARY.md`, `DECISIONS.md`, `SPEC.md`, `COMPONENT_CATALOG.md`, `THEME_ALPACA_LIGHT.md`, `QUALITY.md`, `REPO_STRUCTURE.md`, `IMPLEMENTATION_PLAN.md`;
- `src/alp_ui/components/__init__.py`, `actions.py`, `inputs.py`, `feedback.py`; `src/alp_ui/theme/install.py`, `tokens.py`, `appearance.py`;
- `gallery/main.py`, `gallery/showcase.py`, `docs/components.md`, `docs/getting-started.md`, `tests/test_components.py`, `tests/test_inputs.py`, `tests/test_feedback.py`, `tests/test_consumer_example.py`;
- the consumer's `tip(...)` in `../alpacaDesktop/docs/design/prototypes/training-first/app.js` and corresponding `.tip` style in `styles.css`.

**Existing-equivalent search:** Qt already offers `QToolButton`, `QToolTip`, `QWhatsThis`, focus policy, accessible name/description and normal parent layouts. Existing `Button` is meant for regular actions; field `description=` creates persistent explanatory text rather than a compact help affordance; existing Components do not standardize the combined help behavior. Favor a small `QToolButton` subclass reusing Qt's `QWhatsThis` popup over a custom popup system. If a native composition fully satisfies every requirement without a new public class, report the concrete evidence and ask the owner to cancel this task instead of adding a redundant wrapper.

## 3. Contract and ownership

Proposed public API (refine only for a demonstrated Qt reason):

```python
from alp_ui.components import HelpHint

help_hint = HelpHint(
    "Sets how many items appear on each page.",
    subject="Items per page",
)
# A consumer places help_hint next to its own QLabel or field label.
help_hint.setHelpText("Choose how many items to show at once.")
```

- **Base:** subclass `QToolButton` (or a smaller equivalent native Qt Widget only if proven necessary). Reuse native `clicked`, parent ownership, `enabled`, focus and layout APIs; add no custom signal unless native behavior demonstrably cannot describe an event.
- **Content:** required non-empty *plain-text* `help_text`; reject missing/blank explanation with an actionable `ValueError`. Optional plain-text `subject` identifies what is being explained for accessibility. Do not parse Markdown or allow caller HTML to become rich-text markup accidentally.
- **Presentation:** compact `?` affordance with a natural `sizeHint`, using Theme semantic colors, spacing, typography and focus/interaction tokens. Do not add a generic IconButton API, external icon dependency, image asset, per-instance styling dictionary or hard-coded brand hex values.
- **Mouse:** hover exposes the full explanation through a native tooltip; clicking opens a persistent-enough native help view suitable for reading the short explanation. Prefer `QWhatsThis.showText` anchored to the button; confirm its actual behavior on target platforms rather than inventing another popup class.
- **Keyboard:** the button can be reached with Tab/Shift+Tab; focus is visible; Space (and Return if available on that native control) opens help; the user can dismiss help with Escape and resume navigation. Do not make mere keyboard focus automatically open a disruptive popup. Reuse Qt keyboard semantics and test what actually works.
- **Accessibility:** `accessibleName` describes the action without punctuation-only text, e.g. “More about Items per page” when `subject` is provided; otherwise use a generic localized-ready label such as “More information”. `accessibleDescription` contains the plain explanation even when the popup is closed. Update tooltip, accessible description, and displayed help together when `setHelpText()` is called. The `?` glyph alone is never the accessible name.
- **Layout:** the Component stands alone. **The consumer** owns whether to place it beside a field label, section heading or table header, and keeps label-to-input focus buddies intact. No automatic wrapping of existing field Components or changing their public constructors in this task.
- **Behavior:** no domain data, persistence, translations service, network, background thread, timers owned by the consumer, app-wide registry, custom notification bus or help-content lookup.
- **Theme:** respect `Alpaca Light` and startup Theme overrides, both `standard` and `compact` density, native disabled state, higher DPI, long translations and right-to-left layouts as existing Components do.

Do not invent a “HelpHint intent”, scientific classes, automatic validation rules or second data model. This reusable control is only a generic **Component** under the library's established ubiquitous language.

## 4. Deliverables (upstream repository paths)

- `src/alp_ui/components/help.py` (or an existing module if the codebase demonstrates a better owner): one `HelpHint` public class with small Qt-native implementation.
- `src/alp_ui/components/__init__.py`: export `HelpHint`.
- `docs/components.md`: compact API, keyboard/pointer use, accessibility, and a consumer-controlled label layout example.
- `gallery/main.py`: one representative contextual-help row showing a field and a section-heading placement, including hover/keyboard activation instructions. Add no Trainer domain language.
- `tests/test_help_hint.py`: focused public-API widget tests (prefer the existing `pytest-qt` fixtures/patterns). Extend existing Gallery and built-wheel consumer tests only where the public export/packaging handoff needs evidence; don't duplicate the entire suite.
- `docs/project/COMPONENT_CATALOG.md`: record this explicitly owner-approved, narrow post-v0.1 Component and its non-responsibilities. Update `docs/project/GLOSSARY.md` only if a new broadly used library term is truly needed; `HelpHint` itself is a Component, not a new domain concept.
- `docs/project/SPEC.md` / API docs: align declared scope with the approved new Component without silently rewriting locked decisions or representing v0.1 historical constraints as already delivered.
- `examples/consumer_app/main.py` **only if** a compact independent-consumer example adds evidence not already supplied by Gallery and existing installed-wheel checks. Avoid unrelated changes.

Use the same local wheel workflow and ordinary `install_theme(app)` as the existing consumer; do not introduce a PyPI installation requirement.

## 5. Acceptance behavior and test plan

| Level | Data / operation | Observable result |
|---|---|---|
| Qt component test | Construct with valid text and no `subject` | A focusable themed Qt control, generic accessible name, full help in tooltip/description; no new `QApplication` or worker. |
| Qt component test | Construct with blank/whitespace explanation | Clear early failure; no half-initialized public Component. |
| Qt component test | Construct with `subject="Items per page"` | Accessible name identifies the subject; explanation is accessible independently of hover. |
| Qt component test | Call `setHelpText()` after construction | Pointer, click and accessible description all return updated text; old text is not displayed. |
| Qt component test | Keyboard Tab/Space and Shift+Tab/Escape through normal parent layout | Discoverable help, visible focus, no focus trap, expected dismiss behavior. Native `clicked` fires once per activation. |
| Qt component test | Disabled state | No popup activation; text remains available in the surrounding application's own content when required. |
| Qt component test | Theme override + both densities | No unthemed hard-coded appearance; hover/focus/disabled remain legible, reasonable natural size. |
| Qt component test | Long text, characters resembling markup, Unicode, narrow container, RTL | Content is displayed as plain text without accidental HTML rendering, clipping where avoidable or escaping outside the screen. |
| Gallery/manual | Both field and heading placement with mouse and keyboard | Looks aligned with existing Components; help reachable without hovering and without obscuring the entire window. |
| Installed-wheel consumer | Import from `alp_ui.components`, create after theme installation | Runs in the same consumer environment with no additional runtime requirement. |
| Native Windows qualification | Windows keyboard/visual/Narrator at 100% and 150% scaling | Run and report separately; Linux/macOS/offscreen evidence is not a Windows pass. |

**Testing at owning seams:** these are Qt Component tests, not Dataset/Training integration tests. No WAV fixture, Workspace, real Run, asynchronous worker or chart is needed. If a behavior depends on the real native popup, complement a mocked `QWhatsThis.showText` argument assertion with one actual Qt/popup smoke test; avoid claiming that only mocking proves keyboard/assistive behavior.

Run and report, to the extent supported by the agent's environment:

```bash
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m build
.venv/bin/python -m twine check dist/*
```

Use the existing gallery/capture workflow; compare `standard` and `compact` densities, focus and long-copy handling. Report platform and test limitations explicitly. Do not claim Windows-native checks passed when they have not run.

## 6. Completion criteria and exclusions

- A third-party consumer can add short, accessible, keyboard-openable explanations with **one imported Component** while retaining full control of copy and placement.
- No change to existing `TextInput`, `NumberInput`, `SelectInput`, `Button`, `ProgressBar`, `DataTable` or application behavior is required for ordinary use.
- The Component is theme-coherent, documented, shown in Gallery, tested through its public API, and available in the built package.
- Task 10 itself changes no locked decision, introduces no runtime dependency or global QSS, and adds no generic popup framework. Plotting is addressed independently in task 12 after its required D13 scope amendment.
- A single `HelpHint` API is the entire implementation task. If a locked decision must change or native popup behavior makes the API infeasible, explain the exact conflict to the owner before expanding scope.

**Implementation principles:** validate the consumer demand; reuse Qt and shared Theme primitives; expose the smallest contract; avoid speculative variants and duplicated state; keep presentation in `alp-ui` and meaning in the consumer; test behavior at its actual owner. Update documentation to match the implemented behavior rather than claiming untested accessibility guarantees.
