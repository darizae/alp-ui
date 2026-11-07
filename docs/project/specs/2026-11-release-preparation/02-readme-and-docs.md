# 02 — A human-facing, branded README; significantly leaner Markdown

## Keep the working visual story

The current README already uses the **original Alpaca** lockup and genuine tracked Qt screenshots; improve hierarchy and cropping rather than replace these with mockups or generic AI prose. Use `docs/brand/transparent/lockup-original.png` or the tracked light/dark alternatives (check contrast); hero `docs/images/showcase.png`, side-by-side `gallery-actions.png` and `gallery-fields.png`, with `gallery-feedback.png`, `gallery-data.png`, and `consumer-default.png` as secondary proof. All paths must remain relative and alt text describe actual controls. No capture regeneration unless a referenced file is missing, genuinely wrong, or shows changed behavior.

Lead with what it lets a Python/Qt developer make, one strong screenshot and a short installed example. Keep the ordinary Qt composition story, install/quickstart, concise component overview, links to detailed guides, status/platform caveat and license. Remove duplicated inventories, stage/history prose, repeated pre-release disclaimers and administrative release checklists from the landing page. Keep a small, friendly CTA to launch Gallery. **Do not** market implementation completeness as the product.

Use compact standard GitHub-rendered badges with accurate destinations: MIT license badge linked to `LICENSE`, current Python support, and CI workflow status linked to `.github/workflows/ci.yml`; use version/release badge only once a corresponding actual release exists. The Alpaca brand is not replaced by a badge strip.

## Markdown reduction scope

- **Preserve:** `AGENTS.md` (shrink its mandatory onboarding and remove non-existent `references/` requirements), a short agent route, `docs/project/DECISIONS.md` locked product choices, compact core `SPEC.md`/architecture/boundaries, `docs/components.md`, `docs/getting-started.md`, `docs/theme.md`, `docs/brand/README.md`, `docs/legal/THIRD_PARTY_NOTICES.md`, and a current release procedure.
- **Evaluate removal/consolidation after cross-link audit:** finished `tasks/00-*.md` through `tasks/12-*.md`, duplicate `docs/project/{PRIMER,GLOSSARY,REPO_STRUCTURE,IMPLEMENTATION_PLAN,COMPONENT_CATALOG,QUALITY,THEME_ALPACA_LIGHT}.md`, and historical `docs/project/reports/`. Merge only unique normative decisions into the retained contracts; retain necessary license evidence. Do not preserve a second version of the same API guide.
- Keep finished historical work in Git history, not a parallel `archive/` Markdown tree. Preserve the current specs until executed; subsequently trim these too.
- Check local relative links, references in `AGENTS.md`/CI and public API examples after deletion. A route to a removed document is a failure.

## Where and how

**GitHub API:** list references, edit/delete Markdown and README, review PR. **ChatGPT VM:** static broken-link/image existence scanner, basic Markdown preview if available, build/wheel metadata and ordinary test commands; screenshots already exist. **Local native:** none for this editorial work.

**Acceptance:** brand artwork visible on GitHub light/dark themes; images are authentic and legible; license/status claims are true; one quickstart runs against public API; materially fewer live documentation files and no broken routes; no functional code changes merely to satisfy prose.

## Branch, PR and synchronization

Follow [VERSION_CONTROL.md](VERSION_CONTROL.md). Start from the reviewed **post-01 `main`**; use `docs/alp-ui-02-human-readme`, not the existing long-lived spec branch. Keep all authentic images/legal content in the reviewed changeset, run link/API/docs checks, then merge the README/docs PR to `main` **before** the release branch begins. Record merged-`main` SHA and close obsolete references; do not postpone documentation cleanup to after tagging.
