# Agent Spec — Align Alp-UI's Base Components with the Polished Showcase

## 1. Objective

Refine `alp-ui` so its **default theme, reusable components, and component gallery naturally reflect the polished visual design demonstrated in `docs/images/showcase.png`**.

The showcase is the visual quality reference, **not an application template to reproduce**.

The component gallery should remain a component gallery. However, the individual components, their default styling, typography, sizing, spacing, surfaces, and interaction states should look like the building blocks of that polished application.

**Core principle:** A developer should be able to install `alp-ui`, call `install_theme(app)`, compose components with ordinary Qt layouts, and obtain a cohesive, polished interface without writing custom stylesheets or manually recreating the showcase's visual language.

Implement this alignment, test it, and regenerate screenshots. Favor the smallest effective changes.

## 2. Understand the Existing Project First

Before modifying code, inspect:

- `README.md`
- `docs/project/PRIMER.md`
- `docs/project/SPEC.md`
- `docs/project/DECISIONS.md`
- `docs/project/THEME_ALPACA_LIGHT.md`
- `docs/theme.md` and `docs/components.md`
- `src/alp_ui/theme/` and `src/alp_ui/components/`
- `gallery/main.py` and `gallery/showcase.py`
- Existing tests and screenshot evidence

Treat `docs/images/showcase.png` as the primary visual reference and the current gallery screenshots as the baseline to improve.

Understand the original constraints: reusable PySide6 Qt Widgets, semantic theme tokens, native Qt behavior, minimal targeted styling, and no application-specific frameworks or extra runtime dependencies.

Respect locked project decisions. Document any necessary deviation rather than silently changing the architecture.

## 3. Identify and Correct the Misalignment

Audit the current implementation at three distinct levels.

### A. Library-level appearance

Determine whether the existing theme and components already express the showcase's intended appearance.

Inspect all public component families:

- Buttons and action states
- Typography and text hierarchy
- Cards, surfaces, and dividers
- Text, numeric, and select inputs
- Checkboxes and switches
- Badges, alerts, progress, and empty states
- DataTable headers, rows, borders, and interaction states

Check default dimensions, visual weight, spacing, alignment, typography, color usage, borders, focus, hover, disabled states, and density.

**Where an inconsistency exists in a reusable component, fix it in the library—not in the gallery or showcase.**

### B. Theme-level consistency

Review `ALPACA_LIGHT`, `install_theme()`, and shared token/appearance utilities.

The showcase currently uses `compact` density while the normal theme and gallery default to `standard`. Assess whether the default metrics should be refined so the out-of-the-box appearance is closer to the showcase.

Keep both densities coherent and documented. Do not rely on the showcase's special configuration to conceal weaknesses in the default theme.

Reuse semantic tokens rather than duplicating styling constants across components.

Preserve the existing brand palette and visual identity unless a specific correction is justified.

### C. Gallery presentation

Review how `gallery/main.py` presents components.

Distinguish actual component defects from gallery layout artifacts. For example, its `QGridLayout` stretches buttons horizontally, making them appear much larger than the compact, natural-width buttons in the showcase.

Refine the gallery's presentation so components are displayed at representative sizes, in clear groups, with intentional whitespace and hierarchy.

Use the gallery to demonstrate the library's real visual system, not to invent another visual system.

The gallery should **not** become an application dashboard, acquire application navigation, or require extensive custom styling to look good.

## 4. Implementation Requirements

Make a focused refinement pass following these priorities:

1. **Shared design foundation:** Fix recurring inconsistencies in theme metrics, tokens, density, and typography first.
2. **Reusable components:** Refine component-level styling only where the existing behavior does not meet the intended visual standard.
3. **Gallery:** Improve component arrangements and presentation using those same reusable building blocks.
4. **Showcase:** Remove redundant showcase-specific styling where equivalent reusable library styling is now available. Keep application-specific composition in the showcase.
5. **Consumer examples:** Ensure the README quickstart and independent consumer example communicate the actual appearance of the installed library.

Avoid introducing unnecessary public components or abstractions. A recurring problem should have one reusable solution; a gallery-only layout problem should stay in the gallery.

Do not introduce a global QSS skin, styling framework, routing system, domain logic, copied third-party UI implementations, or runtime dependencies.

Preserve normal Qt parenting, layouts, signals, model/view behavior, keyboard interaction, accessibility, and theme customization.

Do not rewrite components that already meet the target.

## 5. Testing and Visual Verification

### Automated checks

Run the existing quality pipeline:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest
python -m build
python -m twine check dist/*
```

Add or update targeted tests for meaningful changes, especially:

- Default styling and density metrics
- Theme overrides propagating to components
- Focus, disabled, and invalid states
- Sizing and layout behavior
- Component gallery coverage
- Public API and native Qt behavior
- Installed-wheel consumer compatibility

Avoid brittle pixel-perfect assertions across operating systems.

### Screenshots

Regenerate the committed screenshots from the actual running PySide6 implementation:

- `docs/images/gallery-actions.png`
- `docs/images/gallery-fields.png`
- `docs/images/gallery-feedback.png`
- `docs/images/gallery-data.png`
- `docs/images/showcase.png`

Also capture a minimal consumer using the normal `install_theme(app)` defaults, without custom stylesheets. This is an essential test of the actual library experience.

Use `QWidget.grab()` if desktop screenshot permissions are unavailable, as documented in `docs/evidence.md`. Prefer a small, reproducible capture script instead of a one-off manual process.

Where relevant, inspect standard and compact densities, focus/invalid/disabled states, narrow layouts, and 100%/150% scaling.

Use the showcase as a visual reference, but judge the final component gallery independently. The gallery should look consistent with the showcase without imitating its application structure.

Do not claim Windows visual qualification unless Windows was actually tested.

## 6. Documentation and Deliverables

Update the README and relevant theme/component documentation to reflect the refined default appearance.

Keep the quickstart genuinely minimal. If the library now achieves its intended visual quality without special setup, demonstrate that clearly.

Deliver:

1. The focused code changes.
2. Updated or added tests, with actual results.
3. Regenerated gallery and showcase screenshots, plus the minimal consumer capture.
4. Updated documentation where behavior or defaults changed.
5. A concise summary of what was previously inconsistent, what changed, and why.
6. Any remaining cross-platform visual limitations.

Do not stop after producing an implementation plan. Complete the changes and verification within the available environment.

## 7. Definition of Done

The work is complete when:

- **The default library looks polished:** An ordinary PySide6 application using `install_theme(app)` and the public components exhibits the design language of the showcase without requiring bespoke widget styling.
- **The gallery is representative:** Its screenshots show consistent, appropriately sized, well-presented base components rather than visually disconnected demonstrations.
- **The showcase is not special-cased unnecessarily:** Its polish results primarily from library components and semantic theme settings, with custom code limited to legitimate application composition.
- **The architecture remains small:** No new framework, gratuitous component abstractions, dependency expansion, or duplicated styling system has been introduced.
- **The implementation is verified:** Existing functionality remains intact, relevant tests pass, and refreshed screenshots have been visually inspected.

**Success is not making the gallery look like the showcase. Success is making the library's components good enough that building something like the showcase is straightforward and doesn't require reinventing their appearance.**