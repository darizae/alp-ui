# Project glossary and ubiquitous language

Use these exact terms in documentation, code, tests, examples, issues, and task reports. These terms are **library concepts**; they do not rename concepts in other projects.

| Term | Canonical meaning |
|---|---|
| **Component** | Reusable public Qt Widget subclass or widget composition with a documented API and added styling/behavior. |
| **Native Qt control** | Control already provided by Qt Widgets, such as `QPushButton`, `QLineEdit`, or `QTableView`. |
| **Consumer application** | Any separate Python desktop application using this library. Owns the `QApplication`, data, navigation, and business logic. |
| **Design token** | Named, typed visual value (color, spacing, radius, typography metric) rather than a literal embedded in components. |
| **Semantic token** | Design token named for role/meaning (e.g., `primary`, `surface`, `danger`) instead of a concrete hue. |
| **Theme** | Immutable set of design tokens; the library's initial named Theme is `Alpaca Light`. |
| **Alpaca Light** | Theme preset derived from the uploaded Alpaca UI MUI theme's light palette and typography. It does not import Alpaca application behavior. |
| **Theme installation** | One startup operation applying a Theme to a consumer-owned `QApplication`, before its main widgets are created. |
| **Theme override** | A consumer-provided value replacing a semantic token for its app without modifying library source. |
| **Density** | Startup Theme choice, `standard` or `compact`, that changes control/table geometry and Card padding without shrinking font point sizes. |
| **Interaction Tokens** | Theme-owned colors for hover, pressed, focus, selected, disabled, and subtle feedback surfaces, derived from semantic tokens unless explicitly overridden. |
| **Variant** | A finite, documented visual style choice for a Component, such as `primary`, `secondary`, `outline`, or `danger`. |
| **Size** | A documented, bounded component sizing option, initially `small`, `medium`, or `large` where useful. |
| **State** | An observable UI condition, such as idle, hover, pressed, focused, disabled, invalid, or busy; only valid when the component actually supports it. |
| **Intent** | Semantic meaning used by feedback Components: `neutral`, `info`, `success`, `warning`, `danger`. |
| **Gallery** | Runnable local Python/Qt catalog displaying documented Components, variants, states, and interaction examples; not a web Storybook server. |
| **Showcase** | Composed application-like example in `gallery/showcase.py`; not a public Component, navigation system, or application framework. |
| **Example consumer** | Minimal independent application installed against the built package, not source-tree imports. |
| **Public API** | Stable, importable names and documented properties/signals provided to consumer applications. |
| **Qt model/view contract** | `QAbstractItemModel` provides records, `QTableView` displays them, delegates optionally render/edit; the library doesn't invent a second table data format. |
| **Acceptance gate** | Evidence required before moving to the next delegated task or publishing a release. |
| **Third-party notice** | Required upstream attribution, copyright and license information for separately licensed dependencies and fonts. |

## Terminology exclusions

Do not use `ThemeProvider`, `CSS class`, `DOM`, `useState`, `styled-components`, or `React hook` as Python API concepts. They may appear only in comparisons. Do not use `Workflow`, `Run`, `Corpus`, `Dataset`, or related scientific terms in component APIs or example contracts. Do not call generated Qt Stylesheets a general browser CSS engine.

## Amendment rule

Before adding a broadly used new term, check this file. If it is not covered, define it once, state relationship to existing terms, and use the new term consistently. Changes to scope or architecture still require a decision review.
