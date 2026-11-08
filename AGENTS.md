# Agent guide — alp-ui

## Routing and authority

1. Begin at [the project route](docs/project/README.md), then read the locked
   [decisions](docs/project/DECISIONS.md) and core [spec](docs/project/SPEC.md).
2. For current usage read [components](docs/components.md),
   [getting started](docs/getting-started.md), and [theme](docs/theme.md).
3. Review [legal notices](docs/legal/THIRD_PARTY_NOTICES.md) for assets and packaging.

The shipped `v0.1.0a1` pre-release provenance lives in [GitHub
Releases](https://github.com/darizae/alp-ui/releases) and the
[README compatibility note](README.md#learn-more); the completed 2026-11
release-preparation series is preserved in Git history and at the release tag.

Completed task plans and reports live in Git history. No `references/` folder,
machine-local reference tree, or second source of API documentation is required.

## Invariants

- Implement generic PySide6 **Qt Widgets**, not QML, browser UI, or navigation.
  Only PySide6-Essentials is a runtime dependency.
- Retain MIT source license and separate Qt/font notices; preserve authentic
  original brand assets.
- Install immutable, typed Alpaca Light Theme once before constructing widgets;
  use semantic tokens and localized styling, never global QSS or hot retheming.
- Preserve Qt parenting, model/view, signals, keyboard/focus and accessibility.
  The application owns all data, controllers, workers, filesystem, networking,
  persistence, validation rules, and navigation.
- Do not extract a new public Component without a real second consumer,
  architecture review, tests and Gallery example. Locked decisions need
  explicit owner approval before they change.

## Mandatory pre-push and final-head CI

CI validates the **entire repository**, including fenced Markdown Python.
Documentation-only edits are **not exempt**.

1. Record actual `main`/branch SHAs, current CI and tool versions
   (`python -m ruff --version`), scope, and review gate before editing.
2. From the root **before the first push and after each fix**, run
   `python -m ruff check .`, `python -m ruff format --check .` and
   `git diff --check`. Run scoped link/image/API-example checks as well.
3. For code and release changes, also run `python -m pytest`,
   `python -m build` and `python -m twine check dist/*`, with an
   isolated installed-wheel check where relevant.
4. If VM tools or checkout are unavailable, record exactly which checks
   were not run. Read genuine CI results and logs, correct the root
   cause, and rerun appropriate checks; never claim skipped tests passed.
5. Require the **full Windows Python 3.11/3.12/3.13 matrix on the final
   PR head SHA**, not an earlier green commit. Obtain owner/code review
   before merge. Put CI URLs, job results, test counts and review
   status in the PR body, avoiding post-green evidence-only commits.

Qt offscreen tests do not replace native visual, DPI, or screen-reader review
when such platform qualification is claimed.
