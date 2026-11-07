# alp-ui — November 2026 release-preparation specs

**Planning only; no source code, README, tag, or release changed by this series.** Baseline: `main@8cdc91f56005fcd0f3c4004b66016b3d237a10c3`, package `0.1.0a0`. Consumer: BioCall Studio. Execute in the following order; keep implementation work on focused follow-up branches.

1. [01 — Ownership and library boundary](01-boundaries-and-reuse.md) — verify actual reusable widgets before accepting extraction requests.
2. [02 — Human README and documentation reduction](02-readme-and-docs.md) — keep gallery proof, recognizable Alpaca branding and short public guides; retire finished project planning.
3. [03 — Prepare next source-package release](03-release-candidate.md) — propose `v0.1.0a1`; never tag an untested or unmerged candidate.

**Execution channels:** GitHub API for repository inspection, Markdown edits, branches, PRs and release metadata; ChatGPT VM for link/asset audits, local base tests and wheel checks if dependencies can be installed; native Windows only for an independently chosen stable platform-qualification stage, not for these documentation tasks. No fresh macOS capture, physical audio playback, soak or large-data performance work.

**Cross-repository order:** this alp-ui 01 → 02 → 03 sequence may proceed in parallel with the independent [toolbox 01 → 02 → 03](https://github.com/darizae/bioacoustics-dl-toolbox/tree/spec/2026-11-release-preparation/docs/specs/2026-11-release-preparation). Both libraries must produce real tagged GitHub Releases and tested wheel artifacts **before** [BioCall Studio 01](https://github.com/darizae/biocall-studio/blob/spec/2026-11-release-preparation/docs/specs/release-preparation-2026-11/01-upstream-ownership.md) adopts them. The **only final full BioCall Studio base suite** belongs to [Studio 05](https://github.com/darizae/biocall-studio/blob/spec/2026-11-release-preparation/docs/specs/release-preparation-2026-11/05-final-upstream-release-qualification.md) after both native installer lanes are prepared. A released API is not inferred from a pending spec.

Retain `AGENTS.md`, a short routing path, architectural invariants, MIT/Qt/font notices, public API docs and exact visual source provenance. The history of completed tasks is recoverable from Git rather than replicated indefinitely in live docs.
