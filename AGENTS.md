# Agent instructions — python-ui-library

## Mandatory onboarding (before every delegated task)

Read these in order:

1. `PRIMER.md`
2. `GLOSSARY.md`
3. `DECISIONS.md`
4. `SPEC.md`
5. `THEME_ALPACA_LIGHT.md` and `COMPONENT_CATALOG.md`
6. `QUALITY.md` and `REPO_STRUCTURE.md`
7. `IMPLEMENTATION_PLAN.md`
8. The assigned file in `tasks/`
9. `references/SOURCE_MAP.md` and `references/LICENSE_AND_RESEARCH.md` when working with source styling, dependencies, licenses, packaging, or release

Source archives `ui_library.zip` and `alpaca-ui-frontend.zip` are **read-only design references**, not repositories to convert. Inspect cited source files before implementing behavior or design borrowed from them. Do not import Alpaca's obsolete navigation/workflows into this general-purpose library.

## Invariants

- Follow `GLOSSARY.md` everywhere; if a missing shared technical concept must be named, add one definition instead of inventing synonyms.
- Use **PySide6 Qt Widgets**, not QML/Qt Quick, browser UI, React, or TypeScript.
- The core runtime dependency is **PySide6-Essentials** only; no MUI, QFluentWidgets, qt-material, PyQt, superqt, plotting, icon packs, or networking dependencies.
- The library source is MIT-licensed; third-party Qt and font terms remain separate. Apply the licensing checklist to any distributed application and to bundled fonts.
- **Alpaca Light** is the first theme. Colors must be semantic tokens rather than component literals.
- Reuse native Qt controls, Qt signals, model/view interfaces, keyboard handling, and accessibility where possible.
- Do not create wrappers that add no reusable styling, behavior, or contract.
- No domain models or app-specific controllers, status enums, persistence, routing, or pipeline assumptions.
- No backward compatibility requirement for the old TypeScript library or Alpaca UI.
- Keep Qt UI work on the GUI thread. Never insert application computation into a widget.
- Do not create public helpers/speculative knobs without a documented consumer.

## How to execute one task

1. Inspect repository state and search for existing equivalents before adding a class, function, or module.
2. Restate scope, external dependencies, artifacts to change, and the precise Qt primitive being reused.
3. Implement **only** the assigned task's work. Each task ends at a runnable/testable seam; do not silently implement the next one.
4. Add focused unit/interaction tests through public component APIs, relevant gallery states, and concise documentation.
5. Validate keyboard behavior, focus, accessibility naming, layout scaling, theme colors, and packaging as applicable.
6. Report: changed files; acceptance criteria passed/failed; tests run; newly found limitations; third-party license review; proposed decisions needing owner approval.

If a locked decision is unworkable, **stop the affected portion**, show concrete evidence (file/API/version/test), propose the smallest correction, and request a decision. Continue only independent work. Do not silently alter `DECISIONS.md`.

## Spec/implementation review discipline

Follow the spirit of Alpaca Desktop's `SPEC_WRITING_AND_IMPLEMENTATION_PRINCIPLES.md`: search first, reuse the authoritative implementation, name actual consumers, enforce invariants at owning boundaries, test through public contracts, avoid duplicate derived state, and do not extract infrastructure preemptively. This is an independent UI repository, so Alpaca-specific persistence and domain rules do **not** become part of this package.
