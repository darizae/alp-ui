# python-ui-library

**Status:** pre-alpha (`0.1.0a0`); theme foundation implemented.
**Python:** 3.11–3.13  
**Qt:** PySide6-Essentials 6.11.x

A standalone, reusable, styled library of **PySide6 Qt Widgets** for general-purpose desktop applications. The first named visual preset is **Alpaca Light**, faithfully grounded in the uploaded `alpaca-ui-frontend` MUI theme. The component architecture takes useful principles from the uploaded React/TypeScript `ui_library` without translating its runtime or its application-specific components.

This repository is **not** Alpaca Desktop and has no knowledge of scientific artifacts, workflows, backend services, storage, routing, or jobs. There is **no plotting integration** in the roadmap.

```python
from PySide6.QtWidgets import QApplication

from python_ui_library.theme import install_theme

app = QApplication([])
install_theme(app)
```

See [docs/theme.md](docs/theme.md) for typed overrides and the local Theme Gallery.

## Development

Create an isolated environment and install the package with its development tools:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]" "PySide6-Essentials==6.11.2"
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
.venv/bin/python -m build
```

On Windows, use `.venv\\Scripts\\python` in place of `.venv/bin/python`. GitHub
Actions runs lint, tests, and builds on Windows for Python 3.11, 3.12, and 3.13.

## Project documentation

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
- `references/` contains local-only source evidence and is intentionally ignored by Git.
- [docs/evidence.md](docs/evidence.md) records implementation-time verification.

## Authority

When documents disagree, follow in order: **DECISIONS.md → SPEC.md → THEME_ALPACA_LIGHT.md / COMPONENT_CATALOG.md / QUALITY.md → task files**. A task does not override a locked decision. [GLOSSARY.md](GLOSSARY.md) governs naming throughout. External references describe evidence, not an alternative contract.

## Delegation

Execute `tasks/00-...` through `tasks/08-...` in order, as separate agent assignments. An agent must begin with `AGENTS.md`, read the shared specs, inspect source evidence when applicable, and report acceptance checks. The tasks are not invitations to add anticipated features or replicate all existing TypeScript components.

## License

The library source is MIT-licensed. PySide6/Qt and bundled fonts have separate terms;
see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). A consumer application that
redistributes Qt must satisfy its chosen Qt license, including the LGPLv3 obligations
when using the community packages under that route.
