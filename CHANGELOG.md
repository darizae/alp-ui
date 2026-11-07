# Changelog

Entries describe changes in source; publication requires a separate, verified
annotated tag and matching GitHub Release.

## 0.1.0a1 — 2026-11-07 (alpha)

- Prepared an alpha source-package prerelease following the reviewed Qt ownership
  boundary and README/documentation consolidation. No new public `alp_ui` component
  or domain-specific BioCall Studio API is introduced.
- Retained the native PySide6 Qt Widgets API, Alpaca Light theme, Gallery and
  installed-wheel consumer example. Supported Python: 3.11–3.13; runtime
  dependency: `PySide6-Essentials>=6.11,<6.12`.
- Kept the MIT source license, Qt redistribution notices, and both SIL OFL font
  notices with the bundled DM Sans and JetBrains Mono font resources.
- Tightened packaging checks to validate this version and install the built
  wheel into a virtual environment without access to system site-packages.
  Windows CI retains Python 3.11, 3.12 and 3.13 coverage.

The alpha does not claim stable Windows accessibility/DPI qualification,
PyPI publication, or a passing BioCall Studio full application suite.
