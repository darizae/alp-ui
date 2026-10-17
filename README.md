# python-ui-library

**Status:** pre-alpha (`0.1.0a0`); v0.1 Components, native Gallery, and public docs implemented.
**Python:** 3.11–3.13  
**Qt:** PySide6-Essentials 6.11.x

A standalone, reusable, styled library of **PySide6 Qt Widgets** for general-purpose desktop applications. The first named visual preset is **Alpaca Light**, faithfully grounded in the uploaded `alpaca-ui-frontend` MUI theme. The component architecture takes useful principles from the uploaded React/TypeScript `ui_library` without translating its runtime or its application-specific components.

This repository is **not** Alpaca Desktop and has no knowledge of scientific artifacts, workflows, backend services, storage, routing, or jobs. There is **no plotting integration** in the roadmap.

```python
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from python_ui_library.components import Button, TextInput
from python_ui_library.theme import install_theme

app = QApplication([])
install_theme(app)

window = QWidget()
layout = QVBoxLayout(window)
save = Button("Save", variant="primary")
name = TextInput(label="Name", placeholder="Ada Lovelace")
layout.addWidget(name)
layout.addWidget(save)
save.clicked.connect(name.clear)
window.show()
app.exec()
```

See [docs/theme.md](docs/theme.md) for typed overrides and
[docs/components.md](docs/components.md) for component constructors and native Qt APIs.

## Public API index

| Category | Components |
|---|---|
| Actions | `Button` |
| Typography | `Text` |
| Surfaces | `Card`, `Divider` |
| Fields | `TextInput`, `NumberInput`, `SelectInput`, `CheckBox`, `Switch` |
| Feedback | `Badge`, `Alert`, `ProgressBar`, `EmptyState` |
| Data | `DataTable` |
| Theme | `Theme`, `ALPACA_LIGHT`, `install_theme` and typed token groups |

Use the exports from `python_ui_library.components` and `python_ui_library.theme`.
Fine-grained submodule imports remain available, but Components do not create the
application, own data, or run application work.

## Gallery

After the editable development install, launch the offline native Qt Gallery from the
repository root. It contains every public Component and requires no backend:

```bash
# macOS or Linux
.venv/bin/python -m gallery.main

# Windows
.venv\Scripts\python -m gallery.main
```

Click the first action and use Tab or Shift+Tab to inspect keyboard focus. The Gallery
also includes disabled/error states, all feedback intents, and empty and 10,000-row
table models.

## Development

Create an isolated environment and install the package with its development tools:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]" "PySide6-Essentials==6.11.2"
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
.venv/bin/python -m build
.venv/bin/python -m twine check dist/*
```

On Windows, use `.venv\\Scripts\\python` in place of `.venv/bin/python`. GitHub
Actions runs lint, tests, and builds on Windows for Python 3.11, 3.12, and 3.13.

The independent [installed-wheel consumer](examples/consumer_app/README.md) covers a
caller-created application, startup Theme override, native signals, and a caller-owned
table model. The [quality report](docs/quality-and-compatibility.md) records the tested
platform matrix and remaining release gates.

## Versioning and known limitations

The package remains `0.1.0a0` until every release gate passes. The initial stable API
will be marked `0.1.0`; pre-1.0 releases may make breaking changes because no backward
compatibility is promised.

- Alpaca Light is the only Theme preset; runtime Theme switching is unsupported.
- Windows x86-64 is the release qualification target. macOS/Linux smoke results are
  useful evidence but are not certification claims.
- Real Windows 100%/150% DPI, keyboard, and Narrator review is still required for the
  current candidate.
- The library does not provide application routing, persistence, networking, worker
  management, plotting, or domain models.

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
- [REPO_STRUCTURE.md](REPO_STRUCTURE.md) — repository layout and packaging boundary.
- [docs/release-readiness.md](docs/release-readiness.md) — archive, installed-consumer,
  licensing, and outstanding release evidence.
- `references/` contains local-only source evidence and is intentionally ignored by Git.

## Authority

When documents disagree, follow in order: **DECISIONS.md → SPEC.md → THEME_ALPACA_LIGHT.md / COMPONENT_CATALOG.md / QUALITY.md → task files**. A task does not override a locked decision. [GLOSSARY.md](GLOSSARY.md) governs naming throughout. External references describe evidence, not an alternative contract.

## Delegation

Execute `tasks/00-...` through `tasks/08-...` in order, as separate agent assignments. An agent must begin with `AGENTS.md`, read the shared specs, inspect source evidence when applicable, and report acceptance checks. The tasks are not invitations to add anticipated features or replicate all existing TypeScript components.

## License

The library source is MIT-licensed. PySide6/Qt and bundled fonts have separate terms;
see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). A consumer application that
redistributes Qt must satisfy its chosen Qt license, including the LGPLv3 obligations
when using the community packages under that route.

For a consumer distributed with LGPL Qt libraries:

- include applicable Qt notices and license texts;
- provide the corresponding Qt source or a compliant offer/source route;
- preserve the user's ability to replace or relink the Qt libraries and run the
  modified combination;
- audit every bundled Qt module rather than assuming all modules use the same terms;
- review installer, application-store, and frozen/single-file packaging before
  distribution.

This is an engineering checklist, not legal advice. A commercial Qt license is a
separate option when the LGPL route cannot be satisfied.
