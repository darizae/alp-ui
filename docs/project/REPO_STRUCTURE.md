# Repository structure

The tree below describes the maintained repository layout. Human guides, internal
project contracts, and legal notices are deliberately separated.

```text
python-ui-library/
├── README.md                          # human-facing project overview
├── AGENTS.md                          # agent onboarding and authority
├── LICENSE                            # MIT source license
├── pyproject.toml                     # build and package metadata
├── docs/
│   ├── getting-started.md             # human-oriented introduction
│   ├── components.md                  # public Component guide
│   ├── theme.md                       # public Theme guide
│   ├── legal/
│   │   └── THIRD_PARTY_NOTICES.md
│   └── project/                       # internal contracts and plans
│       ├── PRIMER.md
│       ├── GLOSSARY.md
│       ├── DECISIONS.md
│       ├── SPEC.md
│       ├── IMPLEMENTATION_PLAN.md
│       ├── THEME_ALPACA_LIGHT.md
│       ├── COMPONENT_CATALOG.md
│       ├── QUALITY.md
│       ├── REPO_STRUCTURE.md
│       └── reports/
│           ├── quality-and-compatibility.md
│           └── release-readiness.md
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
│   └── main.py                         # native component showcase app
├── examples/
│   └── consumer_app/                   # clean-wheel consuming app
├── tests/                              # behavior, Gallery, and package tests
└── .github/workflows/ci.yml            # Windows 3.11-3.13 matrix
```

This tree is illustrative for **internal module arrangement**, not a strict mandate to create one class/file per symbol. Subpackages are acceptable if a real group becomes too large. No monorepo or duplicate `core`, `base`, `helpers`, `ui2` etc. without evidence.

The external read-only design references are **not** shipped in this repository or its
distributions. Their local roots and file-level mappings belong only in the ignored
`references/SOURCE_MAP.md`.
