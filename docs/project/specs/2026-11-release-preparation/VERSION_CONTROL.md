# Git and release delivery — alp-ui

This is the version-control contract for [specs 01–03](README.md). Current planning source: [PR #1](https://github.com/darizae/alp-ui/pull/1) on `spec/2026-11-release-preparation`; the branch is **not** the release branch. Do not recreate or discard it.

## Bootstrap once

1. Review and merge **existing PR #1 → `main`**, after checking that its exact spec files and this delivery contract are present; record the actual merge commit. No implementation should branch from old `main` before that merge. This changes documentation only; it creates **no tag or release**.
2. For each numbered spec: create the exact focused implementation branch **from the current reviewed `main`**, make its changes, validate, open a new PR, obtain owner/code review, merge it into `main`, and record the **resulting main SHA** before starting the next spec. Do not stack implementation on an unmerged sibling branch.
3. Branch names are targets, not existing refs. If the named branch/PR already exists, inspect and continue it rather than create duplicates. Never force push, rewrite tags or erase other contributors' work. The old `AGENTS.md` may give more historical task-specific instructions; this owner-approved cross-repository spec series governs its own Git delivery after the planning PR is reviewed.

## Integration order

| Spec | Implementation branch from reviewed `main` | PR → sync point |
|---|---|---|
| [01 — Qt ownership](01-boundaries-and-reuse.md) | `feat/alp-ui-01-reuse-boundaries` | Merge to `main` after actual public-component checks (even when the result is deliberately no new component). |
| [02 — README/docs](02-readme-and-docs.md) | `docs/alp-ui-02-human-readme` | Branch from **post-01 main**; merge its authentic screenshots/docs/link audit before a release candidate. |
| [03 — release](03-release-candidate.md) | `release/alp-ui-v0.1.0a1` | Branch from **post-02 main**; update `pyproject.toml` version and truthful release notes; merge candidate PR to `main` first. |

If 01 produces no code changes, its review record/PR can be documentation-only; do not create a fake feature just to justify a branch.

## One immutable release commit

- Only after the **release-prep PR is merged** do we choose `ALP_RELEASE_SHA = main HEAD`. Run the package's own ordinary pytest, Ruff, Windows CI where required, wheel/sdist and isolated installed-wheel checks **against that exact SHA**. Build/upload only artifacts from it, calculate and record their hashes.
- Create an annotated **`v0.1.0a1`** pointing at `ALP_RELEASE_SHA`, then publish its actual GitHub prerelease and wheel/sdist assets only after review and owner promotion approval. Do not tag the spec branch or the pre-merge PR head; do not put the version bump after tests. If checks fail and a fix is merged, choose the new `main` SHA and **rerun all owning release checks/builds**.
- `main` must already contain every approved spec implementation, README/docs consolidation, license notices and final version **before** tagging. After publication, verify `main` contains the release-tag commit, and hand BioCall Studio the published version, tag target commit SHA, wheel hashes and artifact URLs. The final *Studio* suite is [BioCall Studio 05](https://github.com/darizae/biocall-studio/blob/spec/2026-11-release-preparation/docs/specs/release-preparation-2026-11/05-final-upstream-release-qualification.md), not an alp-ui release test.

**Execution:** GitHub API (branches, PRs, reviews, merges, readbacks); ChatGPT VM/CI (base tests, installed wheel, hashes); native Windows CI for the existing alp-ui matrix. If release upload or annotated-tag capability is absent, stop at a verified candidate and request the needed release-capable runner/permission. No PyPI publication was approved.
