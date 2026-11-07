# Locked project decisions

**Status:** LOCKED for the initial release. Only the repo owner may change a locked decision after an explicit ADR-like note showing evidence and consequences. A task agent may raise a correction but must not silently change one.

| ID | Locked decision | Rationale / consequence |
|---|---|---|
| D01 | Git repository and distribution are `alp-ui`; import root is `alp_ui`. | Owner-selected name; repository, package metadata, imports, docs, and tests use it consistently. Check distribution-name availability at publish time. No compatibility alias is provided for the pre-release name. |
| D02 | Build a **Qt Widgets** library with **PySide6** only. No Qt Quick/QML, PyQt compatibility abstraction, React, or webview. | Smallest integration surface for desktop components and existing Python applications. |
| D03 | First-release **only required UI runtime dependency** is `PySide6-Essentials`, using `QtCore`, `QtGui`, `QtWidgets`. | Avoid full UI framework chains, plotting/Qt Addons, and bindings adapters. `PySide6-Essentials` bundles Qt runtime libraries; apps must handle its license. |
| D04 | **No QFluentWidgets, qt-material, PyQtDarkTheme, or superqt** as runtime dependencies in v0.1. | Native Qt covers initial components; zero extra licenses and tighter dependency surface. `superqt` BSD-3-Clause remains an evaluated, optional *future* reuse option for an actual missing control. |
| D05 | `alp-ui` **source license is MIT**. | Easy reuse; add `LICENSE` text when implementing. MIT applies only to our source, not to Qt or bundled fonts. |
| D06 | Use **Alpaca Light** as the initial and default Theme. No dark theme in v0.1. | Reuse the actual MUI palette/typography in the user's archived Alpaca UI. |
| D07 | **Theme = immutable typed semantic tokens** (colors, spacing, typography, radii). Consumer overrides occur at **startup**. No hot theme switching in v0.1. | Customizable across apps without repaint/repolish complexity. No component-specific hard-coded palette. |
| D08 | Styling uses `QPalette`/`QFont` with native Qt `QStyle` and **minimal targeted `QProxyStyle` overrides** when justified; no global QSS theme. QSS may be used **locally and sparingly** with explicit review. | Current Qt production styling guidance; preserves native behavior and efficiency. No custom full `QCommonStyle` or Qt Labs StyleKit dependency initially. |
| D09 | Use **DM Sans** for general text and **JetBrains Mono** for metadata/badges/table headings. Bundle official, unmodified SIL OFL-1.1 font assets plus their copyright/license notices for offline use; provide platform fallbacks. | Matches Alpaca visual identity and avoids Google Fonts/network fetches at runtime. Bundled assets must be added by the implementation agent, not by this docs bundle. |
| D10 | Icons default to Qt standard icons and/or original MIT-compatible drawings made for this project; no MUI icon files or external icon pack runtime. | Small, low-risk license surface. If existing standard icons cannot achieve the desired result, raise a separate design/dependency decision. |
| D11 | Build a **single Python package**, no monorepo, CLI framework, internal design-system server, plugin architecture, or code generation. | Do less; extract on demonstrated second use only. |
| D12 | Components are generic, Qt-native, composable, and do not own app data/controllers. Data tables consume Qt's model/view protocol. | Consumers retain their own data and business behavior. |
| D13 | No third-party plotting dependencies, advanced charting, waveform, or spectrogram visualization. One native Qt-painted, generic, read-only `Plot` Component is authorized as a post-v0.1 extension. | Keeps the PySide6-Essentials-only runtime while allowing the demonstrated numeric-line and categorical-bar presentation need. |
| D14 | Windows x86-64 is the **release qualification platform**. Avoid OS-specific public APIs; Linux/macOS can be smoke-tested opportunistically but are not guaranteed in v0.1. | Grounded in initial desktop use while remaining portable in design. |
| D15 | Implementation/test baseline: CPython **3.11–3.13**; target PySide6-Essentials **6.11.x** initially, with a bounded compatible release spec and CI recording exact tested patch versions. | Restricts compatibility claims to a known Qt minor line; newer versions require compatibility testing and explicit range expansion. |
| D16 | Ship **small, documented public components**, a local Qt Gallery, automated behavioral tests, and a built-wheel example consumer. | Verifiable usefulness, not an empty styling toolkit. |
| D17 | No implicit `QApplication` creation, network access, telemetry, background work, global persistence, or application navigation framework. | Library does not become a second application. |
| D18 | No backwards-compatibility requirement with the TypeScript library or Alpaca UI app. | Copy patterns and values, not obsolete implementation surfaces. |
| D19 | Respect Qt/PySide6 LGPLv3 **in each redistributed application**, even though our own library is MIT; use eligible LGPL modules and dynamically supplied Qt libraries. Do not claim license-free closed-source distribution. | Legally conservative, explicit separation of source license and dependency obligations. |
| D20 | Do not include the `ui_library` or `alpaca-ui-frontend` reference directories/archives in the package or wheel, or copy their source. | Reference-only source inspection; no unverified IP transfer. |
| D21 | Owner-approved v0.1 expansion: `Switch` retains `QCheckBox` behavior with custom painting; `Button` may present a consumer-controlled loading state; `TextInput` forwards native validator, input-mask, and `QCompleter` APIs. | Meets the named consumer request without a validation engine, async controller, network behavior, or added dependency. |

## License decision, plainly

The cleanest viable option **within the user's fixed PySide6 requirement** is: **MIT-authored widgets + unmodified PySide6-Essentials (LGPLv3 option for relevant modules) + unmodified OFL-1.1 fonts with notices**. This avoids directly depending on GPLv3 QFluentWidgets or distributing its UI code. **It does not mean there are no compliance obligations.** Qt's LGPLv3 requires notices/license text, access to corresponding Qt source, and user ability to replace/relink the relevant Qt libraries in distributed apps, subject to its conditions. Packaging into a single locked executable may interfere with these rights; review distributable installers before shipping. This document is engineering license guidance, not a legal opinion. See `docs/legal/THIRD_PARTY_NOTICES.md` for shipped license notices.

## Scope-change procedure

Document a proposed change as: problem and named consumer → investigated alternatives → effect on licenses/dependencies → minimal change → tests. Obtain owner approval before changing this file, then update the specification, public guides, and affected tests in one coherent revision.

## 2026-10-18 owner-approved project rename

- **Problem and consumer:** the repository owner selected the shorter project name
  `alp-ui` and requested the local repository folder use the same name.
- **Alternatives inspected:** retaining `python-ui-library` only as an import alias
  would leave two names for an unreleased package and has no named consumer.
- **Dependencies/licenses:** no dependency or license terms change.
- **Minimal change:** use `alp-ui` for the repository and distribution and `alp_ui`
  for Python imports and source layout. Do not ship a compatibility package.
- **Tests:** update public imports, packaging expectations, Gallery/consumer examples,
  and verify tests, lint, formatting, and built distributions.

## 2026-10-18 owner-approved component amendment

- **Problem and consumer:** the repository owner requested implementation of the
  deliberately deferred Card shadow, Button loading presentation, input masks,
  suggestions, validation access, and Switch.
- **Alternatives inspected:** design review confirmed the requested presentation
  patterns; Qt already provides `QValidator`, input masks, `QCompleter`,
  and `QCheckBox` behavior. Application-owned asynchronous work remains outside the
  library. Detailed inspection notes remain in ignored local evidence.
- **Dependencies/licenses:** no dependency or license change. External implementations
  are behavioral evidence only; no code or assets are copied.
- **Minimal change:** add presentational states and native API forwarding, plus a
  painted two-state `QCheckBox` subclass. Do not add a form schema, worker, networking,
  or suggestion loader.
- **Tests:** public behavior, keyboard activation, accessibility, rendering state,
  gallery coverage, and built-wheel import remain required.

## 2026-10-18 owner-approved visual refinement amendment

The owner explicitly approved refinement of existing Components rather than v0.2
feature expansion. This **extends D07/D08/D10** without changing the core decisions:

- **D07 extension:** add `Theme.density` (`standard` or `compact`), typed derived
  `InteractionTokens`, and new `title`, `subheading`, `caption` typography metrics.
  Alpaca Light's locked semantic hex values are unchanged. Startup-only application
  remains the contract.
- **D08 extension:** local QSS may normalize outline/height/chrome; draw only
  minimal checkbox, switch, select chevron, and spinbox arrows with QPainter. Preserve
  native Qt activation, popup, model, signal, focus, and keyboard behavior. A
  consistent focus border must not change border width (no layout shift).
- **D10 extension:** original lightweight Qt-painted icons, without external asset or
  new runtime dependencies, replace inconsistent generic stock icon imagery where
  appropriate. `make_icon` is a small theme utility, not a general icon library.
- **D12 extension:** sample navigation and page layout belong to `gallery/showcase.py`
  only. Do **not** expose them as new public components without a named consumer.
- **Non-goals at this amendment remained:** no plots, no dark Theme, no runtime theme
  switching, no new runtime dependencies, no application domain logic, and no
  compatibility adapters. The later D13 amendment narrowly supersedes only the plot
  exclusion.

## 2026-10-24 owner-approved lightweight Plot amendment

- **Problem and named consumer:** the Trainer needs lightweight numeric line views for
  changing loss values and categorical bar views for feature importance; other consumer
  applications need the same generic presentation without recreating axes, legends,
  empty feedback, and Theme alignment.
- **Alternatives inspected:** repeated consumer-local `QPainter` widgets would duplicate
  the generic rendering rules. Qt Charts/PySide6-Addons, matplotlib, and pyqtgraph add
  an unnecessary dependency surface. A `QGraphicsView` or model/view chart framework is
  larger than the two read-only shapes require.
- **Dependencies/licenses:** no dependency or license change. The Component uses only
  QtCore, QtGui, and QtWidgets from PySide6-Essentials; consumer evidence is not copied.
- **Decision:** amend D13 as stated in the table. `Plot` is an explicit post-v0.1
  extension with `line` and `bar` kinds, rendered by native `QWidget`/`QPainter` code.
  Initial v0.1 scope remains historical; this does not claim an earlier release shipped
  plotting.
- **Consequences:** add rendering, validation, accessibility, Gallery, built-wheel, and
  separate Windows visual qualification for Plot. D02, D03, D07, D08, D12, and the
  runtime/license policy remain unchanged. Advanced charting, waveform, spectrogram,
  plotting functions, and optional chart dependencies remain excluded.
- **Acceptance:** public Component tests, Gallery coverage, an independently installed
  wheel consumer, and native Windows qualification are required before release claims.
