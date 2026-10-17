# Primer — reusable styled desktop UI for Python

## The user need

When building another Python desktop app, the developer should be able to install `python-ui-library`, initialize the **Alpaca Light** theme, and compose ready-styled buttons, fields, cards, badges, tables, and feedback widgets without restyling every app separately.

**The library owns appearance and generic interaction, not application behavior.** For example, the library can render a status badge with `success` intent; the consuming application decides what *success* means. The library can show a table; the application supplies the row model.

## First principles: how Qt differs from React

- **Qt Widgets:** real desktop widget objects in a parent-child tree, laid out with Qt layouts. Widget properties can be changed in place. `QApplication` runs an event loop.
- **Signals and slots:** event notification and handlers, analogous in purpose to event callbacks, but using Qt's native object/event system.
- **Qt model/view:** tables and lists read data via models (`QAbstractItemModel`) and render via views (`QTableView`), rather than creating one React DOM component per row.
- **Theme:** reusable semantic tokens describing intent: `primary`, `surface`, `text_muted`, `border`, etc. Qt's `QPalette`, `QFont`, `QStyle`/`QProxyStyle`, and small local painting adjustments render them.
- **No browser CSS engine:** QSS is a restricted CSS-like syntax. It does not provide Tailwind, Flexbox, a DOM, or React rerenders. We must avoid a large global QSS replacement skin.
- **Component:** a documented reusable `QWidget` subclass or a small composition that encapsulates appearance plus appropriate behavior. Consumers can use ordinary Qt methods, layouts, and signals.

## Experience we want

1. Install the package in a regular Python project.
2. Create the consumer's single `QApplication`.
3. Install the theme **before constructing the main window**.
4. Construct library controls alongside native Qt controls and use regular Qt layouts/signals.
5. Override semantic theme tokens on application startup without editing library source.
6. Run the gallery to see every reusable component and its supported states.

The library must **not** create a `QApplication` on import or perform network requests, analytics, thread management, data storage, service calls, or routing.

## Design direction

- Library architecture: systematic variants, reusable subcomponents, semantic tokens, modular public imports, gallery-first examples, and independent consumer regression checks.
- Alpaca Light preset: emerald primary, amber secondary, slate neutrals, light surfaces, DM Sans and JetBrains Mono, compact outlined fields, semibold sentence-case actions, lightly bordered cards, and monospace table headers.
- Excluded: browser runtime assumptions, web-style responsive breakpoints, application-specific workflows or domain statuses, app state managers, and plotting/chart packages.

## Success

A clean third-party PySide6 Widgets application installs and uses our library from a built wheel, with no knowledge of Alpaca or the source repos. Its controls look consistent, behave like desktop controls, and support keyboard/accessibility basics. The library itself can be licensed under MIT; downstream Qt licensing is handled separately and explicitly.
