# 03 — Prepare alp-ui's next independently tagged release

**Observed baseline:** `pyproject.toml: 0.1.0a0`; no Git tags or GitHub Releases as of 2026-11-07. Existing `docs/project/reports/release-readiness.md` is historical candidate evidence, not a release. Proposal: **`v0.1.0a1`** as the next source-package prerelease after README/doc consolidation and any approved upstream API fixes. Do not label `0.1.0` stable solely from macOS gallery screenshots.

## Release task sequence

1. Merge the reviewed upstream code/documentation PR; inspect `main` and identify the exact release commit. Bump `project.version` to `0.1.0a1`, make Python/Qt support and changelog text truthful, and keep GPL-impacting scientific work outside this package.
2. Run the **base** `python -m pytest`, `ruff check .`, `ruff format --check .`; follow existing Windows 3.11–3.13 CI matrix. Build sdist/wheel with `python -m build`, `python -m twine check dist/*`; verify bundled fonts/OFL and MIT/Qt notices, and import an isolated installed wheel.
3. Record package artifact SHA-256, Python/Qt dependency metadata, the tested commit, and the BioCall Studio API consumer/pin check. Do not rerun old project-stage tests, request fresh native macOS captures, soak, or large scientific workloads.
4. On **verified `main` only**, create an **annotated** tag `v0.1.0a1` at that exact SHA (not from the current planning branch). Draft a concise GitHub prerelease with the installed-wheel snippet and verified wheel/sdist files. No PyPI publishing without a separate explicit decision.
5. Confirm tag SHA, release URLs/assets/checksums, and source documentation. Never move the tag to fix an error; use a new version.

## Tool allocation and gates

- **GitHub API:** change metadata/docs, prepare PR, inspect CI, check existing tags/releases and draft notes.
- **ChatGPT VM:** ordinary Python test/lint/build/wheel smoke and checksums **when the environment supports Qt**. If not, rely on actual GitHub CI result, not guessed passes.
- **Local native:** neither macOS re-capture nor installer work is a gate for this prerelease. If later choosing a separately advertised stable Windows-supported `v0.1.0`, resolve the historical Windows DPI/keyboard/Narrator qualification honestly; do not import those tasks into this small prerelease.

**Do not tag now:** this document is only the release specification; tag and GitHub Release are separate promotion actions after checks.
