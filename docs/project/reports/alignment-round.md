# Alignment round report — Task 09

Checked on 2026-10-24 against the polished `docs/images/showcase.png` reference.

## Result

The shared Theme and public Components already expressed the Showcase design through
semantic colors, typography roles, density metrics, stable focus borders, and local
Component styling. The visible mismatch came primarily from Gallery composition:
`QGridLayout` expanded Buttons to column width, which obscured their real size hints.

The Gallery now groups Button variants, sizes, and states in natural-width rows,
keeps Badge examples in a narrow-safe grid, and uses vertical-only catalog scrolling.
The Showcase uses the Card's shared spacing instead of a local override. The
independent consumer demonstrates standard density in ordinary Qt layouts without a
consumer stylesheet, while the Showcase continues to demonstrate the documented
compact density.

No public API, semantic color, locked density metric, runtime dependency, license, or
packaging contract changed.

## Changed artifacts

- `gallery/main.py`: representative action/feedback arrangements and narrow layout.
- `gallery/showcase.py`: removed redundant Card spacing customization.
- `gallery/capture.py`: reproducible `QWidget.grab()` captures, with each Theme
  configuration installed in a fresh process.
- `examples/consumer_app/`: composed default-density example and usage notes.
- `tests/`: Gallery sizing/narrow-layout, consumer-default, and capture checks.
- `README.md`, `docs/components.md`, `docs/getting-started.md`, and `docs/theme.md`:
  default appearance, Qt layout behavior, density intent, and capture instructions.
- `docs/images/`: refreshed Gallery and Showcase images plus
  `consumer-default.png`.

The task specification remained a pre-existing user worktree change and was not
included in implementation commits.

## Automated evidence

Environment: macOS 26.6.2 arm64, CPython 3.13.13, PySide6 6.11.2.

| Check | Result |
|---|---|
| `.venv/bin/python -m ruff check .` | Pass |
| `.venv/bin/python -m ruff format --check .` | Pass |
| `.venv/bin/python -m pytest` | 69 passed |
| `.venv/bin/python -m build` | Pass |
| `.venv/bin/python -m twine check dist/*` | Pass |
| Fresh external venv, offline wheel install, `consumer_app --smoke` | Pass |

The isolated consumer imported `alp_ui` from its temporary environment's
`site-packages`, not from the source checkout. Both the default and custom startup
Theme paths remain covered by the automated consumer test.

## Visual review

The committed images were regenerated from the real PySide6 widgets on macOS Retina:

- Gallery: 760 by 700 logical pixels, standard density.
- Showcase: 1180 by 790 logical pixels, compact density.
- Consumer: 600 by 480 logical pixels, standard density, no consumer stylesheet.

The review covered natural action sizing, expanding fields and data surfaces,
standard and compact density, focus, invalid and disabled states, feedback intents,
and empty/large model views. An ignored offscreen capture at 480 by 620 logical
pixels confirmed the Gallery has no visible horizontal scrollbar. An ignored 150%
scale consumer capture rendered at 900 by 720 pixels without clipping.

## Remaining limitations

This pass did not run on Windows or with Narrator. Windows x86-64 at 100% and 150%
display scaling, keyboard-only navigation, and screen-reader behavior remain release
qualification gates. Native rendering may vary by platform; the automated tests avoid
pixel-perfect comparisons.
