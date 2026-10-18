# Project implementation plan — delegated tasks

**Purpose:** each row links one self-contained Markdown agent assignment, performed sequentially against a separate repository `alp-ui`. Complete each acceptance gate before the next task. This document is the roadmap, not a substitute for the individual tasks.

| Order | Assignment | Exit gate | Dependent on |
|---|---|---|---|
| 00 | [Verify evidence, scaffold project](../../tasks/00-evidence-and-scaffold.md) | Wheel skeleton installs; license/source decisions verified | None |
| 01 | [Build typed Alpaca Light theme](../../tasks/01-theme-and-assets.md) | Palette/font application and packaging tests pass | 00 |
| 02 | [Core actions, text, surfaces](../../tasks/02-actions-typography-surfaces.md) | Button, Text, Card, Divider meet API/state/gallery tests | 01 |
| 03 | [Form field components](../../tasks/03-inputs.md) | TextInput, NumberInput, SelectInput, CheckBox, Switch validated | 02 |
| 04 | [Feedback components](../../tasks/04-feedback.md) | Badge, Alert, ProgressBar, EmptyState validated | 03 |
| 05 | [Data table](../../tasks/05-data-table.md) | Model/view integration, large-model tests, table header appearance | 04 |
| 06 | [Gallery and public docs](../../tasks/06-gallery-and-docs.md) | Every exported component documented/shown and interaction-tested | 05 |
| 07 | [Quality and accessibility pass](../../tasks/07-quality-and-compatibility.md) | Windows quality matrix complete, no known P0 regressions | 06 |
| 08 | [Independent consumer + packaging](../../tasks/08-consumer-and-release.md) | Built-wheel consumer, notices, metadata and release checklist pass | 07 |

## Why this order

The theme and resource loading are established before Components. Components accumulate only after a reusable control is proven. Model/view data behavior is tested independently. The gallery is hardened into documentation once the component APIs stabilize, followed by a final end-to-end consumer verification. Do not implement future-page widgets merely because they existed in a React package.

## Cross-task invariants

- **Source of truth for visual values:** `docs/project/THEME_ALPACA_LIGHT.md`, derived from archived MUI source; components do not define their own brand colors.
- **Source of truth for behavior:** native Qt Widgets API and `docs/project/COMPONENT_CATALOG.md`; consumer owns app logic and data.
- **Source of truth for rights:** repository MIT + independently licensed Qt/fonts, tracked in `references/LICENSE_AND_RESEARCH.md` and implementation notices.
- **Source of truth for imports:** `src/alp_ui/...`; never construct separate parallel implementations for gallery versus public components.
- **Tests:** test through public imports and Qt signals. Each task adds tests for its delivered behavior; task 07 consolidates, it does not postpone all testing.

## Task report format

At the end of each task, the agent reports: task ID and summary; inspected upstream files/docs; exact files changed; tests executed with pass/fail; screenshot/visual review notes; license/dependency changes (should ordinarily be none); acceptance checklist; deviations or owner decisions needed. It does not claim completion from code-only changes without tests.

## User review checkpoints

Owner should review the theme gallery after **Task 01**, the first real component showcase after **Task 03**, the Qt data table after **Task 05**, and the final built-wheel consumer after **Task 08**. These reviews do not override task acceptance tests.
