# Quality and compatibility report — v0.1 candidate

Checked on 2026-10-18 for the v0.1 release candidate. This report distinguishes
automated evidence from platform checks that still require Windows hardware.

## Tested environment

| Item | Result |
|---|---|
| Host | macOS 26.6.2, arm64 |
| Python | CPython 3.13.13 |
| Qt binding | PySide6-Essentials 6.11.2 |
| Automated behavior tests | Pass |
| Ruff lint and format | Pass |
| macOS offscreen Gallery smoke | Pass at 100% and 150% scale |
| Windows x86-64, Python 3.11-3.13 | Configured in `.github/workflows/ci.yml`; not executable on this host |

Windows remains the release qualification platform. The Windows CI matrix and a real
Windows Gallery review at 100% and 150% display scaling must pass before publication;
this macOS result is not a substitute or a certification claim.

## Interaction and accessibility

Automated tests exercise the public control rather than duplicate internal state:

| Component group | Evidence |
|---|---|
| Button | Space activation emits one `clicked`, disabled/loading states do not activate, and keyboard focus has a visible themed outline. |
| TextInput | Label buddy and accessible name/description, error text, validator, mask, completer, Return, and native signals. |
| NumberInput and SelectInput | Native controls, keyboard changes, native signals/models, labels, and focus participation. |
| CheckBox and Switch | Space toggles once, disabled controls do not toggle, two-state Switch contract, accessible names, and visible native/custom focus. |
| DataTable | Keyboard row movement, selection, native scrollbars, model change/reset notifications, accessible name, and no per-cell widgets for 10,000 rows. |
| Feedback | Text accompanies every intent; Alert, Badge, ProgressBar, and EmptyState expose accessible names/descriptions. |
| Gallery | Every enabled interactive example has a non-empty Qt accessibility name and accepts focus. Long text wraps at a 480-pixel representative window width. |

The Gallery was visually reviewed offscreen at a 760 by 700 logical-pixel window at
100% and 150% scale, and at a compact 480 by 620 window with Button, field, and table
focus. Qt produced 760 by 700 and 1140 by 1050 pixel captures for the two scale
factors. The local captures are retained under the ignored
`references/quality-screenshots/` evidence directory; they are not shipped.

No screen reader was available on this host. Qt accessibility properties and label
relations are covered by tests, but Narrator behavior still belongs to the Windows
manual gate.

## Theme, resource, and dependency audit

- Semantic color literals remain centralized in `theme/alpaca_light.py`; Components
  consume Theme tokens.
- Components use only documented local QSS. Theme installation does not install a
  global stylesheet or replace the native Qt style, and no `QProxyStyle` is present.
- Bundled DM Sans and JetBrains Mono files load from package resources without a
  network request. Missing-resource fallback emits a warning and uses a deterministic
  installed/system family.
- The sole direct runtime dependency remains
  `PySide6-Essentials>=6.11,<6.12`. Runtime imports are limited to QtCore, QtGui, and
  QtWidgets; no GPL-only Qt Addons, plotting, networking, or domain model dependency
  was found.
- Imports do not construct a `QApplication`. DataTable keeps the consumer's model and
  does not install cell widgets or enable implicit sorting.
- Constructor tests reject unsupported Button variants/sizes, Text roles, field
  kinds/ranges, Divider orientations, Switch tri-state mode, and feedback intents.

## Open release gates

- Run the committed Windows CI matrix for Python 3.11, 3.12, and 3.13.
- Review the installed-wheel Gallery on Windows x86-64 at 100% and 150% scaling using
  keyboard-only navigation and Narrator.
- Recheck Qt and font license terms immediately before a public release or packaged
  consumer distribution.

No known P0 component regression was found in the checks available on this host.
