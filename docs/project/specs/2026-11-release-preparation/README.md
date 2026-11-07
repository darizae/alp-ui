# alp-ui — November 2026 release-preparation specs

**Execution tracker; no tag or release yet.** Planning PR #1 and A1 PR #2 were merged to `main` (post-A1 SHA `2f9eaeab6915a0e4c2d65fe61ff62d4464f2970a`). Package remains `0.1.0a0`. Consumer: BioCall Studio. A2 must merge before A3 branches from the new reviewed `main`.

1. [01 — Ownership and library boundary](01-boundaries-and-reuse.md) — verify actual reusable widgets before accepting extraction requests.
2. [02 — Human README and documentation reduction](02-readme-and-docs.md) — keep gallery proof, recognizable Alpaca branding and short public guides; retire finished project planning.
3. [03 — Prepare next source-package release](03-release-candidate.md) — propose `v0.1.0a1`; never tag an untested or unmerged candidate.

**Execution channels:** GitHub API for repository inspection, Markdown edits, branches, PRs and release metadata; ChatGPT VM for link/asset audits, local base tests and wheel checks if dependencies can be installed; native Windows only for an independently chosen stable platform-qualification stage, not for these documentation tasks. No fresh macOS capture, physical audio playback, soak or large-data performance work.

**Cross-repository order:** this alp-ui 01 → 02 → 03 sequence may proceed in parallel with the independent [toolbox 01 → 02 → 03](https://github.com/darizae/bioacoustics-dl-toolbox/tree/main/docs/specs/2026-11-release-preparation). Both libraries must produce real tagged GitHub Releases and tested wheel artifacts **before** [BioCall Studio 01](https://github.com/darizae/biocall-studio/blob/main/docs/specs/release-preparation-2026-11/01-upstream-ownership.md) adopts them. The **only final full BioCall Studio base suite** belongs to [Studio 05](https://github.com/darizae/biocall-studio/blob/main/docs/specs/release-preparation-2026-11/05-final-upstream-release-qualification.md) after both native installer lanes are prepared. A released API is not inferred from a pending spec.

Retain `AGENTS.md`, a short routing path, architectural invariants, MIT/Qt/font notices, public API docs and exact visual source provenance. The history of completed tasks is recoverable from Git rather than replicated indefinitely in live docs.

## Branch and `main` synchronization

The [Git and release delivery contract](VERSION_CONTROL.md) is mandatory for each spec. [Planning PR #1](https://github.com/darizae/alp-ui/pull/1) and [A1 PR #2](https://github.com/darizae/alp-ui/pull/2) are merged. Next: review/merge A2 into `main` → branch/review/merge A3 → run release QA on merged `main` → after owner promotion approval, annotate the immutable tag and publish a GitHub prerelease. This lane may proceed in parallel with the toolbox lane, but not with BioCall Studio 01 until both libraries are actually released. Follow permanent cross-repo spec links on `main` after all planning PRs are merged.
