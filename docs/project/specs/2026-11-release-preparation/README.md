# alp-ui — November 2026 release-preparation specs

**Planning only; no source code, README, tag, or release changed by this series.** Baseline: `main@8cdc91f56005fcd0f3c4004b66016b3d237a10c3`, package `0.1.0a0`. Consumer: BioCall Studio. Execute in the following order; keep implementation work on focused follow-up branches.

1. [01 — Ownership and library boundary](01-boundaries-and-reuse.md) — verify actual reusable widgets before accepting extraction requests.
2. [02 — Human README and documentation reduction](02-readme-and-docs.md) — keep gallery proof, recognizable Alpaca branding and short public guides; retire finished project planning.
3. [03 — Prepare next source-package release](03-release-candidate.md) — propose `v0.1.0a1`; never tag an untested or unmerged candidate.

**Execution channels:** GitHub API for repository inspection, Markdown edits, branches, PRs and release metadata; ChatGPT VM for link/asset audits, local base tests and wheel checks if dependencies can be installed; native Windows only for an independently chosen stable platform-qualification stage, not for these documentation tasks. No fresh macOS capture, physical audio playback, soak or large-data performance work.

**Cross-repository order:** library boundaries and any upstream improvements first; then a BioCall Studio pinned dependency update and README sync; library releases before the Studio installer-gated release. A released API is not inferred from a pending spec.

Retain `AGENTS.md`, a short routing path, architectural invariants, MIT/Qt/font notices, public API docs and exact visual source provenance. The history of completed tasks is recoverable from Git rather than replicated indefinitely in live docs.
