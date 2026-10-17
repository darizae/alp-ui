# Agent instructions — python-ui-library

## Documentation authority

Human-facing documentation lives in `README.md` and `docs/`. Keep implementation
contracts and agent planning under `docs/project/`; do not leak task history or source
research into the user guide.

Completed quality and release evidence belongs in `docs/project/reports/`. Legal
notices belong in `docs/legal/`.

When documents disagree, follow this order:

1. `docs/project/DECISIONS.md`
2. `docs/project/SPEC.md`
3. `docs/project/THEME_ALPACA_LIGHT.md`,
   `docs/project/COMPONENT_CATALOG.md`, and `docs/project/QUALITY.md`
4. The assigned file in `tasks/`

`docs/project/GLOSSARY.md` governs naming everywhere. External references provide
evidence, not an alternative contract. Do not silently change a locked decision.

## Mandatory onboarding before every delegated task

Read these in order:

1. `docs/project/PRIMER.md`
2. `docs/project/GLOSSARY.md`
3. `docs/project/DECISIONS.md`
4. `docs/project/SPEC.md`
5. `docs/project/THEME_ALPACA_LIGHT.md` and
   `docs/project/COMPONENT_CATALOG.md`
6. `docs/project/QUALITY.md` and `docs/project/REPO_STRUCTURE.md`
7. `docs/project/IMPLEMENTATION_PLAN.md`
8. The assigned file in `tasks/`
9. `references/SOURCE_MAP.md` and `references/LICENSE_AND_RESEARCH.md` when working
   with styling sources, dependencies, licenses, packaging, or release

## External design evidence

The read-only references are `/Users/danie/Downloads/ui_library` and
`/Users/danie/Downloads/alpaca-ui-frontend`. They are design evidence, not repositories
to convert or sources to copy. Inspect cited originals before implementing borrowed
behavior or design. Do not import obsolete navigation or application workflows into
this general-purpose library.

Keep file mappings, excerpts, screenshots, and inspection notes only in ignored
`references/` or `docs/evidence.md`. Tracked documents may contain the library contract
and independently authored implementation decisions.

## Invariants

- Follow `docs/project/GLOSSARY.md`; define one missing shared term instead of
  inventing synonyms.
- Use PySide6 Qt Widgets, not QML/Qt Quick, browser UI, React, or TypeScript.
- The only runtime dependency is PySide6-Essentials. Do not add external UI
  frameworks, Qt Addons, plotting, icon-pack, or networking dependencies.
- The source is MIT-licensed; Qt and bundled fonts retain separate terms. Keep
  `docs/legal/THIRD_PARTY_NOTICES.md` and downstream compliance guidance accurate.
- Alpaca Light is the first Theme. Components consume semantic tokens rather than
  embedding brand colors.
- Prefer native Qt controls, signals, model/view interfaces, keyboard behavior, and
  accessibility.
- Do not create wrappers without reusable styling, behavior, or contract.
- Do not add domain models, app controllers, persistence, routing, application status
  enums, or pipeline assumptions.
- No backward compatibility is required for the old TypeScript library or Alpaca UI.
- Keep UI work on the GUI thread; widgets never own application computation.
- Do not add public helpers or speculative options without a documented consumer.

## Development and verification

Use the repository environment and keep generated output in ignored locations:

```bash
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m build
.venv/bin/python -m twine check dist/*
```

On Windows, use `.venv\Scripts\python`. The committed CI matrix covers Windows
with Python 3.11, 3.12, and 3.13. `dist/`, build output, and local visual evidence are
ignored; do not commit them.

## Executing a task

1. Inspect repository state and search for existing equivalents before adding a class,
   function, or module.
2. Restate scope, external dependencies, changed artifacts, callers, tests, fixtures,
   exports, and the Qt primitive being reused.
3. Implement only the assigned work and stop at its runnable/testable seam.
4. Test through public Component APIs and add relevant Gallery/docs coverage.
5. Validate keyboard behavior, focus, accessibility names, layout scaling, Theme
   colors, and packaging as applicable.
6. Report changed files, acceptance results, tests, visual review, limitations,
   dependency/license changes, and decisions needing owner approval.

If a locked decision is unworkable, stop that portion, provide concrete evidence,
propose the smallest correction, and request a decision. Continue independent work.

## Review discipline

Search first, reuse the authoritative implementation, name actual consumers, enforce
invariants at owning boundaries, test public contracts, avoid duplicate derived state,
and do not extract infrastructure preemptively. This repository is independent, so
application-specific persistence and domain rules do not enter the package.
