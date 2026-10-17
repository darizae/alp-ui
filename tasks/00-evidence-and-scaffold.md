# Task 00 — Verify evidence and scaffold the standalone package

**Dependencies:** none. **Task type:** independent agent assignment. **Scope:** documentation reconciliation, dependency/license verification, and installable skeletal Python package; no widgets yet.

## Read first

`AGENTS.md`, `PRIMER.md`, `GLOSSARY.md`, `DECISIONS.md`, `SPEC.md`, `REPO_STRUCTURE.md`, `references/SOURCE_MAP.md`, `references/LICENSE_AND_RESEARCH.md`.

## Work

1. Inspect the external design references at the exact roots and paths listed in the ignored `references/SOURCE_MAP.md`. Confirm colors, typography, reusable architecture, and license status. Never copy their source/assets into the new package or tracked evidence files.
2. Verify exact Python/PySide6-Essentials 6.11.x platform support and installed module licenses against current official documentation/package metadata. Record tested patch version. Confirm `QtCore`, `QtGui`, and `QtWidgets` imports work with **only** PySide6-Essentials installed.
3. Create a new Git repository named `python-ui-library` with one `src/python_ui_library` package and a standard `pyproject.toml`, initialized at pre-release version. Use explicit Python bounds 3.11–3.13 and a bounded PySide6-Essentials 6.11.x runtime requirement. Avoid exact-patch pinning for consumers unless required; pin tested environments in CI.
4. Add MIT `LICENSE` with accurate copyright holder (obtain repository owner identity when available; **do not invent**); add `THIRD_PARTY_NOTICES.md` skeleton that accurately distinguishes future bundled font assets and Qt obligations; CI/dev dependency setup with minimal test/lint/build tools.
5. Copy the planning Markdown bundle to repo root intact; add a minimal README explaining status and imports; ensure no Python module automatically initializes Qt.
6. Build and install a skeletal wheel in a fresh venv. Verify `import python_ui_library` and `PySide6.QtWidgets` import without side effects or a running display session.
7. Create an empty test suite entrypoint and a simple pre-commit/code-quality strategy. Do not add application controllers, custom component classes, fonts, QSS, or theme implementation yet.

## Artifacts

`pyproject.toml`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, importable `src/python_ui_library`, test/CI scaffold, documentation copy, reproducible build instructions.

## Acceptance

- [ ] Source files from archives confirmed or missing evidence explicitly reported.
- [ ] Python/PySide6 version, module selection, and licensing verified and recorded with source links.
- [ ] Runtime dependency list contains **PySide6-Essentials only**.
- [ ] Wheel builds, installs in fresh venv, imports without creating `QApplication` or making network requests.
- [ ] MIT copyright metadata is correct; no third-party code copied.
- [ ] Agent supplies changed-file list, test commands/results, risk log, and gate verdict.

**Stop condition:** if license verification reveals a GPL-only module imported by the selected path, do not silently switch framework; report the specific module and seek approval for a minimal correction.
