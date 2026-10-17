# Task 06 — Finish local component gallery and public documentation

**Dependencies:** Task 05 completed. **Task type:** docs, examples, showcase; not feature expansion.

## Read first

`AGENTS.md`, `docs/project/SPEC.md`, `docs/project/COMPONENT_CATALOG.md`, `docs/project/THEME_ALPACA_LIGHT.md`, `docs/project/QUALITY.md`, `references/SOURCE_MAP.md`; use TypeScript Storybook and regression app **for intent, not code**.

## Work

1. Finish native Qt Gallery as a standalone local app that displays every v0.1 Component categorized into Actions, Typography, Surfaces, Fields, Feedback, Data.
2. Show Theme swatches/type specimens, required variants, focus and disabled states, field errors, alerts/intents, determinate/indeterminate progress, blank and large-model tables.
3. Provide self-contained user docs per public Component: import path, when to use it, constructor args, Qt inherited signals, example usage, accessibility caveats. Ensure wording follows `docs/project/GLOSSARY.md` and does not mention Alpaca workflows.
4. Offer a clear interactive way to inspect keyboard focus; gallery pages are demonstrative, not a second theme editor or design tool.
5. Make gallery invocable from a documented dev command; use package absolute imports. Avoid Storybook, HTTP servers, generated JS, and non-PySide UI dependencies.
6. Ensure gallery covers actually shipped public surface. Do not promote a component without tests/docs or add backlog widgets merely to fill navigation tabs.

## Artifacts

Finished `gallery/` app, `docs/components/` references, quick-start README with consumer-owned QApplication and theme install, example screenshots if useful.

## Acceptance

- [ ] Every public component/variant appears in Gallery and docs and has corresponding tests.
- [ ] Gallery launches using ordinary PySide6 Qt Widgets and offline bundled resources.
- [ ] One documented command launches Gallery on Windows; no app backend required.
- [ ] Focus, disabled and error states inspectable; documented signals match implementation.
- [ ] No TypeScript/web components, charts, or domain models imported.
