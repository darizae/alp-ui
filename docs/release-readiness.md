# Release-readiness handoff

Checked on 2026-10-18 for package version `0.1.0a0`. No package upload, tag, GitHub
release, or public publication was performed.

## Result

The source, metadata, wheel, sdist, offline assets, and installed-wheel consumer pass
the checks available on macOS arm64. The candidate is **not yet releasable as 0.1.0**
because Windows x86-64 qualification and Narrator/DPI review have not run for this
commit. See [quality-and-compatibility.md](quality-and-compatibility.md).

## Distribution evidence

- Standard `python -m build` produces
  `python_ui_library-0.1.0a0-py3-none-any.whl` and
  `python_ui_library-0.1.0a0.tar.gz`.
- `twine check` passes both archives.
- The wheel contains all public modules, seven unmodified font files, both OFL texts,
  the MIT `LICENSE`, and `THIRD_PARTY_NOTICES.md`.
- The sdist additionally contains the Gallery, public docs, tests, and independent
  consumer example.
- Neither archive contains `references/`, ignored evidence, the source design
  directories, TypeScript source, or Alpaca application assets.
- Wheel metadata declares CPython 3.11-3.13 and exactly one direct runtime dependency:
  `PySide6-Essentials>=6.11,<6.12`.

The generated archives remain in the ignored local `dist/` directory for inspection.

## Independent consumer evidence

The app in `examples/consumer_app` creates its own `QApplication`, installs the Theme,
uses Button, TextInput, Badge, and DataTable, supplies its own `QAbstractTableModel`,
and handles native signals. It was executed through a temporary path outside the
repository in isolated Python mode from a fresh external virtual environment after an
offline wheel/dependency installation from the local package cache. Both the default
Theme and a typed startup color override opened, loaded bundled fonts/platform plugins
without network access, and shut down cleanly in the offscreen smoke run. The resolved
`python_ui_library` module path was inside that external environment, not this source
tree.

The Gallery was also launched against the installed wheel rather than an editable
source install. Its offscreen smoke completed with the bundled assets and normal
shutdown. A real Windows launch remains outstanding.

## License and provenance audit

- Project metadata and the MIT license identify the repository-provided owner as
  `darizae`; no ownership identity was invented during this task.
- The DM Sans and JetBrains Mono OFL copyright/license texts remain intact beside the
  unmodified font files and in wheel license metadata.
- The library wheel does not bundle Qt. `THIRD_PARTY_NOTICES.md` distinguishes the MIT
  library from Qt and font terms and points downstream distributors to Qt obligations.
- Runtime imports are limited to PySide6 QtCore, QtGui, and QtWidgets. No external UI
  framework, Qt Addon, plotting, networking, or domain dependency was added.
- No implementation or asset was copied from the read-only design references.

## Required before 0.1.0

1. Push the candidate and obtain passing Windows CI results for Python 3.11, 3.12, and
   3.13 with PySide6-Essentials 6.11.2.
2. On Windows x86-64, run the installed-wheel consumer and Gallery at 100% and 150%
   scaling; verify keyboard-only focus and Narrator output.
3. Recheck current Qt/PySide6 and font license terms and document the distribution
   method's LGPL source and replacement/relinking path.
4. Only after those gates pass, change the package version/status to `0.1.0`, rebuild,
   repeat archive/consumer checks, tag, and publish under a separate owner-approved
   release action.

## Downstream Qt LGPL checklist

A consuming application that redistributes community Qt under LGPLv3 must include
applicable notices and license texts, provide corresponding Qt source or a compliant
source route, preserve end-user replacement/relinking rights, audit the licenses of
all included Qt modules, and review installers or frozen/single-file bundles. If that
distribution cannot meet the LGPL terms, obtain suitable legal advice and consider a
commercial Qt license. This checklist is engineering guidance, not legal advice.
