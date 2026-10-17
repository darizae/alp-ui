# Project quality, tests, and release acceptance

## Test pyramid

1. **Pure theme tests:** immutable typed Theme, known hex colors, valid overrides, repeatable derived state colors, expected fallbacks.
2. **Qt component behavior tests:** instantiate with `QApplication` fixture, inspect native Qt signals and control state, keyboard/focus/parenting, invalid input boundaries. Prefer `pytest-qt` (development-only) when available.
3. **Gallery/manual appearance:** representative snapshots across states and Windows DPI/resolution settings. Use manual baseline review as needed rather than fragile hardcoded pixel screenshots across platforms.
4. **Packaged consumer test:** fresh virtual environment, installed built wheel, resource/font loading and native Qt plugin import, no source tree on import path.

## Per-component review checklist

- [ ] Fully documented constructors, bounded variants/intents/size and inherited Qt signals.
- [ ] Idle, hover (where applicable), focused, disabled, invalid (where applicable), and pressed/busy (only where applicable) are legible.
- [ ] Keyboard navigation, Tab/Shift+Tab, Space/Enter where native behavior applies; no focus trap.
- [ ] Accessible name and error message semantics are available through Qt APIs.
- [ ] Correct parent/child lifetime, cleanup, and no duplicate QApplication creation.
- [ ] Font fallback doesn't overflow or truncate unexpectedly; long labels and translated text tested.
- [ ] Light-theme background/surface/text/interactive contrast manually checked; errors have text not only colors.
- [ ] No theme-specific hex literal outside tokens; no global QSS style blanket.
- [ ] No application-owned data or processing introduced.
- [ ] Gallery entry and public import demonstration match implementation.

## Component specific critical tests

- Buttons: emits **one** native clicked event per activation; disabled button does not activate; focus indicator exists.
- Button loading: visible text, accessible name, no activation, caller enabled state restored, and no worker created.
- Text and Cards: respect Qt layout resizing and ownership; nested text can wrap; no redundant shadow effects in large lists.
- Inputs: native `textChanged` / value changed preserved; validation feedback visible; tab and label focus forwarding work.
- Switch: native checked signal fires once for keyboard activation; disabled state does not toggle; focus remains visible.
- Badge/Alert: semantic intent displayed with accessible text; unknown intent fails meaningfully.
- ProgressBar: handles minimum/maximum, value boundaries and native indefinite mode; no worker thread created.
- DataTable: accepts normal `QAbstractItemModel`, uses native scrollbar, honors model reset/dataChanged notifications, selection, column resizing; no `setCellWidget` per row, no implicit sorting/re-ordering. A model of **10,000 rows** must open and scroll without 10,000 child widgets (do not assert arbitrary benchmark time without a measured baseline).
- Theme: exact Alpaca Light palette, Theme immutable, startup overrides honored, no network dependency for fonts, failed font resources handled gracefully.

## Platform, DPI, and environment matrix

| Matrix item | Initial obligation |
|---|---|
| Windows x86-64 / Python 3.11, 3.12, 3.13 | Release check (CI or documented supported manual run) |
| PySide6-Essentials 6.11.x | Pin tested patch versions in CI and metadata bounds |
| 100% and 150% display scaling | Manual gallery review at minimum |
| Keyboard only / visible focus | Manual plus automated widget tests |
| Offline execution | Required; no font downloads at startup |
| Windows built-wheel consumer | Required |
| Linux/macOS | Optional smoke tests, **not marketed as certified** |
| Font resources in final wheel | Required |

## Automated tooling (dev only)

Recommended, not forced: `pytest`, `pytest-qt`, `ruff`, a static type checker, `build`, and `twine check`. The agent chooses minimal configurations and records exact choices; never make them runtime dependencies. Use Qt offscreen mode for suitable headless tests, but always keep real Windows GUI review because offscreen rendering doesn't validate appearance or native window behavior fully.

## Release checklist

- [ ] All task acceptance gates passed with evidence.
- [ ] `pyproject.toml` names distribution, runtime dependency, interpreter/platform scope, package assets accurately.
- [ ] MIT `LICENSE` and third-party notices included in source distribution, wheel where relevant, and README.
- [ ] Official unmodified fonts and their SIL OFL license/copyright notices included in distribution.
- [ ] No dependencies on the TypeScript repo, Alpaca UI application, Qt Addons, QFluentWidgets, superqt, plotting, or networking.
- [ ] Built wheel installed in isolated environment; `import python_ui_library` and its public Components work.
- [ ] Consumer creates exactly one QApplication, installs Theme, creates UI, exits normally.
- [ ] Qt redistribution/commercial usage caveat clearly stated in documentation.
- [ ] Gallery covers required variants/states; descriptions and examples match current API.
- [ ] Package versioned as `0.1.0` once gates pass; publication is an explicitly separate owner action.
