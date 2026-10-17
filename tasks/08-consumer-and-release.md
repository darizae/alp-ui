# Task 08 — Independent installed-wheel consumer and release readiness

**Dependencies:** Task 07 completed. **Task type:** external consumer validation and packaging; do not publish automatically.

## Read first

`AGENTS.md`, `SPEC.md` (§8), `QUALITY.md`, `DECISIONS.md`, `references/LICENSE_AND_RESEARCH.md`, `REPO_STRUCTURE.md`.

## Work

1. Build wheel and sdist via standard Python packaging. Verify metadata and `twine check` (dev utility). Inspect distribution archives to confirm correct modules, fonts, MIT LICENSE, OFL notices, and no external reference directories/source code/assets.
2. In a **fresh** virtual environment **outside the repository**, install built wheel. Ensure source repo is not on `sys.path`. Create a tiny consuming Qt Widgets application: caller creates QApplication, installs ALPACA_LIGHT, lays out Button, TextInput, Badge, and DataTable backed by its own Qt model, and handles signals.
3. Repeat installation at least once with an overridden color token Theme to demonstrate application customization without source edits.
4. Run consumer and Gallery using only installed assets offline on Windows x86-64. Verify import paths, native Qt plugin loading, fonts and resource relative paths, clean shutdown.
5. Finalize README quick start, API index, versioning guidance and known limitations. Include a **downstream Qt LGPL compliance checklist**: notice/license texts, corresponding Qt sources or compliant offer, user-replaceable/relinkable Qt binaries, module-license audit, installers/frozen app review. Avoid promising commercial distribution has zero restrictions.
6. Verify MIT source copyright correctly identifies owner, OFL copyright notices intact, and no TypeScript source/Alpaca app code copied. Mark first tested release `0.1.0` only if all acceptance gates pass.
7. Produce release-readiness handoff; do **not** push to PyPI or publish a release without separate explicit owner instruction.

## Artifacts

Built distribution for inspection, independent `examples/consumer_app`, package/release report, source and dependency notice audit, final docs.

## Acceptance

- [ ] Fresh venv consumer can use components and theme **from wheel** without importing source tree.
- [ ] Fonts and Qt platform plugins resolve in offline Windows consumer.
- [ ] Full build, tests, docs, and release matrix pass; clear list of OS and Python versions tested.
- [ ] Repository and distribution contents include correct license/third-party notices.
- [ ] No domain-specific behavior, plots, or optional component dependencies appear.
- [ ] Final report identifies remaining limitations and any distribution compliance action still required of the consuming application.
- [ ] No automatic public upload or GitHub release performed.
