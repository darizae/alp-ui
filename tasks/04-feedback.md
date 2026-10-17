# Task 04 — Generic feedback and empty states

**Dependencies:** Task 03 completed. **Task type:** visual feedback only, no app event bus.

## Read first

`AGENTS.md`, `GLOSSARY.md`, `COMPONENT_CATALOG.md`, `THEME_ALPACA_LIGHT.md`, `SPEC.md`, `QUALITY.md`, and the visual references listed for this task in the ignored `references/SOURCE_MAP.md`.

## Work

1. Implement `Badge` with typed semantic `intent`: `neutral`, `info`, `success`, `warning`, `danger`. Explore outlined and filled forms only if clearly visible and cheap; keep badges readable with text and contrast. Never hardcode status enums (`running`, `completed`, etc.).
2. Implement `Alert` with text/title and semantic intent; consumer may add an action widget; no global toaster, banner queue, or persistence.
3. Implement `ProgressBar` wrapping `QProgressBar`; validate native determinate and indeterminate modes and correct visual progress in dark text/light background palette.
4. Implement `EmptyState` as a small composition with text and optional icon/action widget; no data fetching, no file scanning.
5. Add unit/UI tests for intent validation, accessibility text, correct Qt parent ownership, progress value/range semantics, wrapping, and palette changes. Gallery example for each intent/state.

## Artifacts

Feedback component module(s), exports, state examples and public docs, tests.

## Acceptance

- [ ] Component uses only generic intents; no domain-specific status vocabulary.
- [ ] Status communicated with readable text and visuals, not only color.
- [ ] ProgressBar does **not** start computation or own a worker process.
- [ ] Unknown intent fails with actionable validation error.
- [ ] No notification service infrastructure or extra dependencies introduced.
