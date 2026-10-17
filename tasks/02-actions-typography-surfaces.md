# Task 02 — Core actions, typography, and surfaces

**Dependencies:** Task 01 completed. **Task type:** four coherent components; no fields/feedback/data.

## Read first

`AGENTS.md`, `docs/project/COMPONENT_CATALOG.md`, `docs/project/THEME_ALPACA_LIGHT.md`, `docs/project/SPEC.md`, `docs/project/QUALITY.md`, and the read-only files listed for this task in the ignored `references/SOURCE_MAP.md`.

## Work

1. Implement public `Button` reusing `QPushButton`, with documented `primary`, `secondary`, `outline`, `danger` variants; sizes only where useful; native `clicked`, keyboard activation, icon/text support via existing Qt API. Provide the owner-requested consumer-controlled loading presentation without adding a worker controller.
2. Implement `Text` from `QLabel` using typed roles `body`, `caption`, `heading`, `overline`, honoring DM Sans/JetBrains Mono and safe text selection/wrap behavior.
3. Implement `Card` as a container wrapping Qt layout(s), using white surface, 1px slate border, 10px rounding, 24px content padding, and the theme-defined subtle shadow with an opt-out for dense/repeated use. Avoid many nested pseudo-components unless consumers justify them.
4. Implement `Divider` on native separator behavior and the `border` token.
5. Add focused component tests for variant validation, theme inheritance, focus and disabled, click signal exactly once, proper parenting/lifetime, long text and resizing. Add representative Gallery sections/examples for these widgets (final gallery structure comes later).
6. Document constructor choices and Qt inherited methods. Avoid implementing framework-like `asChild`, `Slot`, or JSX composition contracts.

## Artifacts

`components/actions.py`, `typography.py`, `surfaces.py` (or a justified equivalent), public exports, tests, Gallery examples and docs.

## Acceptance

- [ ] Buttons have required variants, clickable/disabled/focus behavior, and no duplicate clicked signal.
- [ ] Loading presentation disables activation, is accessible, restores caller state, and starts no work.
- [ ] Source theme's semibold sentence-case buttons and font choices visible.
- [ ] Card/Divider honor semantic theme colors and Qt layout resizing.
- [ ] All exported classes are ordinary QWidget-compatible objects, installed package imports succeed.
- [ ] No hardcoded source hex colors in component modules, global stylesheet, or extra runtime library.
- [ ] Every public component has at least one test and Gallery example.
