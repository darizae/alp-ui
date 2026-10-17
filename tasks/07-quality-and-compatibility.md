# Task 07 — Accessibility, packaging resource, and compatibility verification

**Dependencies:** Task 06 completed. **Task type:** quality hardening; avoid speculative architecture changes.

## Read first

`AGENTS.md`, `docs/project/DECISIONS.md`, `docs/project/SPEC.md`, `docs/project/QUALITY.md`, `references/LICENSE_AND_RESEARCH.md`, tests and all public component docs.

## Work

1. Run the full behavior suite and fix failures at owning component/theme layers. Confirm constructors enforce variant/intent invariants clearly.
2. Manually test keyboard navigation/visibility of focus and screen reader-accessible naming where available. Validate long labels/text, scaling (100% and 150%) and representative window sizes. Record results and visual screenshots for review.
3. Verify source theme tokens are still centralized, no global QSS has crept in, fonts load offline, and fallback behavior works. Review Qt-native appearance across basic widgets and any targeted `QProxyStyle` changes.
4. Test Python 3.11, 3.12, 3.13 on Windows x86-64 (CI or documented manual runs), with bounded tested PySide6-Essentials 6.11.x patch versions. Smoke-test Linux/macOS optionally, but do not claim certification.
5. Inspect package imports/test reports for unwanted runtime deps, domain state or widgets constructed on import, duplicated class interfaces, and per-cell table widgets.
6. Check all open issues against v0.1 acceptance criteria; fix genuine P0 failures but move new ideas to backlog rather than expanding API.

## Artifacts

Quality report with matrices/screenshots, tightened tests, minimal bug fixes, updated docs for real observed limitations.

## Acceptance

- [ ] Every item in `docs/project/QUALITY.md` release matrix addressed with test evidence or documented owner-approved exception.
- [ ] Focus/keyboard/accessible text checked for all interactive controls.
- [ ] Installed resources work without internet and at normal/high DPI.
- [ ] Runtime remains PySide6-Essentials only, GPL-only Qt imports absent, plotting absent.
- [ ] No incomplete P0 component is exposed publicly as supported.

**Stop condition:** a severe unfixable Qt-version/licensing issue requires owner review rather than changing the framework/version decision silently.
