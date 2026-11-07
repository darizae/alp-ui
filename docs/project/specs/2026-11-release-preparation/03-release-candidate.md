# 03 — Prepare alp-ui's next independently tagged release

**Observed baseline:** `pyproject.toml: 0.1.0a0`; no Git tags or GitHub Releases as of 2026-11-07. Earlier readiness reports are historical candidate evidence in Git history, not a release. Proposal: **`v0.1.0a1`** as the next source-package prerelease after README/doc consolidation and any approved upstream API fixes. Do not label `0.1.0` stable solely from macOS gallery screenshots.

## Release task sequence

1. Merge the reviewed upstream code/documentation PR; inspect `main` and identify the exact release commit. Bump `project.version` to `0.1.0a1`, make Python/Qt support and changelog text truthful, and keep GPL-impacting scientific work outside this package.
2. Run the **base** `python -m pytest`, `ruff check .`, `ruff format --check .`; follow existing Windows 3.11–3.13 CI matrix. Build sdist/wheel with `python -m build`, `python -m twine check dist/*`; verify bundled fonts/OFL and MIT/Qt notices, and import an isolated installed wheel.
3. Record package artifact SHA-256, Python/Qt dependency metadata and the tested commit. Run only a focused public-API consumer smoke if convenient; **do not run BioCall Studio's entire suite here**. That final full application suite belongs exclusively to [BioCall Studio 05](https://github.com/darizae/biocall-studio/blob/main/docs/specs/release-preparation-2026-11/05-final-upstream-release-qualification.md) after both upstream packages are released and Studio installers are ready. Do not rerun old project-stage tests, request fresh native macOS captures, soak, or large scientific workloads.
4. On **verified `main` only**, create an **annotated** tag `v0.1.0a1` at that exact SHA (not from the current planning branch). Draft a concise GitHub prerelease with the installed-wheel snippet and verified wheel/sdist files. No PyPI publishing without a separate explicit decision.
5. Confirm tag SHA, release URLs/assets/checksums, and source documentation. Never move the tag to fix an error; use a new version.

## Mandatory candidate and release CI gate (A3)

- Start only from the *verified merged* post-A2 `main`, and record that SHA.
  Before the first candidate push, run repository-wide Ruff lint and formatting
  with a CI-compatible toolchain (also check Markdown Python examples), plus
  task-scoped tests, packaging validation and isolated wheel smoke as applicable.
- Require all Windows Python 3.11/3.12/3.13 CI jobs to pass on the **final
  release-prep PR head**. Review and merge that PR before release qualification.
  Only the **merged main** SHA may be frozen as `ALP_RELEASE_SHA`; rerun the
  owning test/build/wheel-install checks against precisely that SHA.
- Record the passing CI links, actual test counts, wheel/sdist hashes and
  review/owner promotion decision in PR/release evidence. A post-green commit
  (even release notes) changes the tested SHA and triggers new qualification;
  never reuse old CI/artifact evidence or tag a PR head.

## Tool allocation and gates

- **GitHub API:** change metadata/docs, prepare PR, inspect CI, check existing tags/releases and draft notes.
- **ChatGPT VM:** ordinary Python test/lint/build/wheel smoke and checksums **when the environment supports Qt**. If not, rely on actual GitHub CI result, not guessed passes.
- **Local native:** neither macOS re-capture nor installer work is a gate for this prerelease. If later choosing a separately advertised stable Windows-supported `v0.1.0`, resolve the historical Windows DPI/keyboard/Narrator qualification honestly; do not import those tasks into this small prerelease.

**Do not tag now:** this document is only the release specification; tag and GitHub Release are separate promotion actions after checks.

## Branch, PR, merge and exact tag

Follow [VERSION_CONTROL.md](VERSION_CONTROL.md). From **post-02 `main`**, create `release/alp-ui-v0.1.0a1` for version metadata and release notes; **merge its reviewed PR to `main` before any final release build**. Freeze actual `ALP_RELEASE_SHA = main HEAD`, run alp-ui's owning base tests/CI and install/build at exactly that SHA, then (only after owner promotion approval) annotate `v0.1.0a1` at **that merged-main commit**, upload its tested wheel/sdist and hashes. A fix after freeze requires a new reviewed PR/merged SHA plus repeated release checks and builds. No tags on PR/spec branch or orphan release notes. Handoff published artifact hashes and tag commit SHA to BioCall Studio; do **not** run Studio's full suite here.
