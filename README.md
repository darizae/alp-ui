# python-ui-library — specification bundle

**Status:** planning package; no implementation included.  
**As of:** 2026-10-17.  
**Repository name:** `python-ui-library`  
**Distribution name (planned):** `python-ui-library`  
**Python import root (planned):** `python_ui_library`.

A standalone, reusable, styled library of **PySide6 Qt Widgets** for general-purpose desktop applications. The first named visual preset is **Alpaca Light**, faithfully grounded in the uploaded `alpaca-ui-frontend` MUI theme. The component architecture takes useful principles from the uploaded React/TypeScript `ui_library` without translating its runtime or its application-specific components.

This repository is **not** Alpaca Desktop and has no knowledge of scientific artifacts, workflows, backend services, storage, routing, or jobs. There is **no plotting integration** in the roadmap.

## Start here

1. [PRIMER.md](PRIMER.md) — what we are building, how Qt Widgets works, and what a consumer should experience.
2. [AGENTS.md](AGENTS.md) — mandatory reading, task protocol, constraints.
3. [GLOSSARY.md](GLOSSARY.md) — canonical technical and product language.
4. [DECISIONS.md](DECISIONS.md) — locked architectural, styling, scope, and licensing decisions.
5. [SPEC.md](SPEC.md) — authoritative behavior, interfaces, components, and acceptance requirements.
6. [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) — execution order and cross-task gates.
7. [`tasks/`](tasks/) — one individually delegable implementation task per Markdown file.

Supporting references:

- [THEME_ALPACA_LIGHT.md](THEME_ALPACA_LIGHT.md) — exact source palette and typography mappings.
- [COMPONENT_CATALOG.md](COMPONENT_CATALOG.md) — explicit initial component inventory and scope boundaries.
- [QUALITY.md](QUALITY.md) — test matrix, gallery standards, release gates.
- [REPO_STRUCTURE.md](REPO_STRUCTURE.md) — target directory layout **to create later**.
- [references/SOURCE_MAP.md](references/SOURCE_MAP.md) — source ZIP inspection paths and copied-vs-not-copied ideas.
- [references/LICENSE_AND_RESEARCH.md](references/LICENSE_AND_RESEARCH.md) — licensing decisions and upstream citations.

## Authority

When documents disagree, follow in order: **DECISIONS.md → SPEC.md → THEME_ALPACA_LIGHT.md / COMPONENT_CATALOG.md / QUALITY.md → task files**. A task does not override a locked decision. [GLOSSARY.md](GLOSSARY.md) governs naming throughout. External references describe evidence, not an alternative contract.

## Delegation

Execute `tasks/00-...` through `tasks/08-...` in order, as separate agent assignments. An agent must begin with `AGENTS.md`, read the shared specs, inspect source evidence when applicable, and report acceptance checks. The tasks are not invitations to add anticipated features or replicate all existing TypeScript components.

## Bundle contents

This handoff includes **Markdown documentation only**. It does not include the original ZIPs, third-party fonts, third-party source, generated application files, license text binaries, or starter code. The implementing agent needs the original `ui_library.zip` and `alpaca-ui-frontend.zip` available in its workspace to inspect the evidence cited here. If source archives are unavailable, do not claim to have verified their code; follow the documented extracted evidence and identify that limitation.
