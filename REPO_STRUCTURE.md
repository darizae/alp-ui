# Repository tree to implement

The **present ZIP contains only specification Markdown**. The tree below is **a target for the implementing agent**; it must not be mistaken for files already created.

```text
python-ui-library/
├── README.md                          # project README, updated after implementation
├── AGENTS.md                          # agent onboarding
├── PRIMER.md
├── GLOSSARY.md
├── DECISIONS.md
├── SPEC.md
├── IMPLEMENTATION_PLAN.md
├── THEME_ALPACA_LIGHT.md
├── COMPONENT_CATALOG.md
├── QUALITY.md
├── REPO_STRUCTURE.md
├── references/
│   ├── SOURCE_MAP.md
│   └── LICENSE_AND_RESEARCH.md
├── tasks/
│   ├── 00-evidence-and-scaffold.md
│   ├── 01-theme-and-assets.md
│   ├── 02-actions-typography-surfaces.md
│   ├── 03-inputs.md
│   ├── 04-feedback.md
│   ├── 05-data-table.md
│   ├── 06-gallery-and-docs.md
│   ├── 07-quality-and-compatibility.md
│   └── 08-consumer-and-release.md
├── pyproject.toml                      # FUTURE
├── LICENSE                             # FUTURE: MIT license text
├── THIRD_PARTY_NOTICES.md             # FUTURE: fonts / Qt acknowledgements
├── src/
│   └── python_ui_library/
│       ├── __init__.py
│       ├── theme/
│       │   ├── __init__.py
│       │   ├── tokens.py
│       │   ├── alpaca_light.py
│       │   ├── install.py
│       │   └── resources/             # OFL fonts, copyright & license notices
│       └── components/
│           ├── __init__.py
│           ├── actions.py
│           ├── typography.py
│           ├── surfaces.py
│           ├── inputs.py
│           ├── feedback.py
│           └── data.py
├── gallery/
│   └── main.py                         # FUTURE: component showcase app
├── examples/
│   └── consumer_app/                   # FUTURE: clean-wheel consuming app
├── tests/
│   ├── test_theme.py
│   ├── test_components.py
│   ├── test_data_table.py
│   └── test_packaging.py
└── docs/
    └── components/                    # FUTURE: public API/examples
```

This tree is illustrative for **internal module arrangement**, not a strict mandate to create one class/file per symbol. Subpackages are acceptable if a real group becomes too large. No monorepo or duplicate `core`, `base`, `helpers`, `ui2` etc. without evidence.

The original design reference archives are **not** shipped in the new repository. They may be staged outside it for one-time inspection, per `references/SOURCE_MAP.md`.
