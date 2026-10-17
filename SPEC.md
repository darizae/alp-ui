# General implementation specification — python-ui-library

**Normative scope:** first public version `0.1.0`; deliver reusable PySide6 Qt Widgets styled with **Alpaca Light**. All requirements here are independent of Alpaca Desktop. `DECISIONS.md` is the highest-level locked contract.

## 1. Product and non-goals

A consumer application should install a wheel, import components by stable names, apply a Theme once to its `QApplication`, add Components to ordinary Qt layouts, connect Qt signals, and supply Qt data models. It must not know how widgets are painted internally.

No page routing framework, domain data, job execution, network calls, window manager, persistence, render-to-HTML, PyQt bindings, Qt Quick/QML, dark mode, runtime theme switching, plots, or charting. Do not wrap every native Qt Widget preemptively.

## 2. Supported runtime and dependency policy

- **Runtime:** CPython 3.11–3.13, PySide6-Essentials 6.11.x, QtCore/QtGui/QtWidgets only. Build metadata should use supported-version bounds reflecting the tested line; developer tools can have dev dependencies but not leak into runtime.
- **Target platform:** Windows x86-64 for release. Aim for portability; do not claim other platforms are certified until tested.
- **Packaging:** standard `pyproject.toml` and wheel. Implement as one distribution under `src/python_ui_library`. Avoid ad hoc import path manipulation, requirements copied from React, and bundling Qt binaries ourselves.
- **Resources:** the wheel contains the official unmodified font binaries required to display DM Sans/JetBrains Mono offline and complete OFL notices. Build tests verify these assets are packaged and load using installed resource paths.
- **Licenses:** `LICENSE` for MIT project source and `THIRD_PARTY_NOTICES.md` or equivalent for bundled licensed assets. Do not redistribute source repos or their copied components.

## 3. Public interface contract

Initial recommended stable exports (task agents may refine **method** details only within existing semantics):

- `python_ui_library.theme`: `Theme`, `ALPACA_LIGHT`, `install_theme(app, theme=ALPACA_LIGHT)`.
- `python_ui_library.components`: `Button`, `Text`, `Card`, `Divider`, `TextInput`, `NumberInput`, `SelectInput`, `CheckBox`, `Switch`, `Badge`, `Alert`, `ProgressBar`, `DataTable`, `EmptyState`.
- Class names are public, QWidget-compatible; no private Qt shims required by consumers. Fine-grained submodule imports also work and have no surprise side effects.
- Use typed constructors or a documented bounded set of setters; rely on inherited methods for ordinary Qt behavior. Define `variant`, `size`, and `intent` consistently with `GLOSSARY.md`/`COMPONENT_CATALOG.md`. Invalid values fail early with actionable errors at component construction.
- Theme install accepts the consumer-owned `QApplication`. Passing a non-QApplication or attempting installation after UI construction is documented as unsupported; reject clearly where detectable. `install_theme` must not silently construct or replace the QApplication.
- Default theme may be used for component preview when not installed but **normal documented consumer path requires startup installation**. Avoid global singleton registries unless there is a demonstrated consumer need.
- Public APIs must be explainable and reasonably typed. Preserve Qt signals/slots and `QObject` parenting. No async framework dependency.

## 4. Styling architecture

`Theme` maps semantic visual values to `QPalette` roles, `QFont` choices, and minimal narrowly-scoped Qt styling. Components should use Qt native `QStyle` rendering when possible, with a tiny `QProxyStyle` adapter only for measured differences; any special painting delegates must follow Qt focus, disabled, and high-DPI behavior. A one-time local QSS override is allowed only if documented in source as an exception with behavior tests. Never install a large global stylesheet.

Font resources must use explicit offline loading (`QFontDatabase` or appropriate Qt API), safely handle repeat use, and fall back gracefully. No `@font-face` from web is available. Browser `rem`, CSS grids, and arbitrary Tailwind classes do not transfer to Qt.

`ALPACA_LIGHT` uses exact colors and salient styling in `THEME_ALPACA_LIGHT.md`. Arbitrary consumer Themes work via semantic values rather than conditionals recognizing Alpaca. No hardcoded color hex literal in individual components besides a clearly justified UI state fallback.

## 5. Component behavior

`COMPONENT_CATALOG.md` is the authoritative v0.1 inventory. Each Component's implementation must declare: native base control, bounded variants/roles, constructor/Qt signals, ownership of child widgets (if composed), label/accessibility mappings, data boundary, states, and tests. Prefer subclassing the native control when it preserves public Qt behavior; prefer composition when it must supply label/error/help content.

**Forms:** Native validators, input masks, completers, and Qt spin boxes remain authoritative. A field may show error text; it does not silently alter, sanitize, or persist caller data. All errors must be accessible and visually connected to the label/control. Keyboard focus remains on the proper input widget. Consumers may update a `QCompleter` model from their own application work; the library does not fetch suggestions or own asynchronous work.

**Tables:** `DataTable` is a themed `QTableView` consuming a caller-provided `QAbstractItemModel`. Sorting/selection behavior should be normal Qt behavior; do not invent the table's data format or hold redundant row copies. Header style approximates the MUI visual source; scrolling is native Qt behavior. Large models remain responsive.

**Feedback:** `Badge`/`Alert` consume semantic `intent`, not product status enums. `ProgressBar` displays a value or native indefinite state; never owns a background worker.

## 6. Quality, accessibility, and supported behavior

- All components render with gallery examples and tests of normal, focused, disabled, invalid, and relevant hover/pressed states.
- Components honor high-DPI scaling, normal resizing, internationalized/long labels, keyboard navigation, tab order, native menu/focus behavior, and ordinary screen readers via Qt accessible names/descriptions.
- No invisible focus indicators; no clickable color-only semantics for status or errors. Critical feedback includes text, not hue alone.
- Assert theme token values and component public behaviors; avoid brittle pixel-perfect assertions that vary by OS and font renderer. Manually compare selected Windows screenshot samples against Alpaca UI inspiration.
- Isolated consumer sample runs **from built wheel installed into fresh environment**. The source tree must not accidentally be importable.
- Tests must not rely on networks, login, company infrastructure, or files outside the repo; packaged fonts supplied at implementation time.

## 7. Documentation and gallery

Gallery is a normal PySide6 application with a list/tree of component examples (not an HTML/Storybook server). It must demonstrate theme, variants, component states, field validation, large-data model/view behavior, and keyboard focus without requiring domain services. Include a gallery screenshot reference for release review and a small consumer snippet per public component. Ensure gallery itself depends on the installed library import contract in at least one CI check.

## 8. Release contract and gating

All delegated tasks in `IMPLEMENTATION_PLAN.md` complete, `QUALITY.md` gates pass, licenses/notices included, metadata/wheel validated, and a consumer example from a fresh venv runs successfully on Windows x86-64. Release only components actually implemented and tested. Missing gallery/test coverage means the component remains private or out of scope.

## 9. Open implementation choices (not permission to change decisions)

The implementation agent may select a standard build backend, formatter/type checker, internal file splits, and unit-test utilities. It may determine whether a certain native widget requires `QProxyStyle`, a local QSS adjustment, or a small composition **inside the locked styling architecture**. It may also derive exact focus/disabled colors from existing tokens, provided they are centralized and tested for legibility. Any change adding dependencies, dynamic theme switching, dark mode, new public components, GPL-only modules, or plots requires a decision change first.
