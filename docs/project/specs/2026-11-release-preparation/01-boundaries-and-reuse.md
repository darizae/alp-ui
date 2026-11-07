# 01 — Keep alp-ui small and genuinely reusable

## Finding

`alp-ui` already exposes native PySide6 Widgets, model/view tables, themed controls, HelpHint, folder picker, and a **lightweight** numeric line / categorical bar `Plot`. Source: `src/alp_ui/components/`, `gallery/`, `docs/components.md`. Its `pyproject.toml` has only `PySide6-Essentials` at runtime. BioCall Studio consumes it and owns its own application routes.

## Required implementation decision

- Check every proposed BioCall Studio widget or plot against `src/alp_ui/components/__init__.py`, `docs/components.md`, `gallery/showcase.py`, and normal native Qt primitives **before** adding an API.
- Move only a presentation primitive that demonstrably serves a second consumer and has a stable Qt-only contract. Suitable candidates are reusable styling/accessibility defects or generic raster viewing/axis affordances **if** existing Qt and `Plot` cannot meet the requirement.
- Do **not** move WAV readers, FFT/STFT, spectrogram settings/presets, peak-relative dB, sample-frame semantics, BioCall's spectrogram cache keys, audio playback, Review state, immutable Results, image generation, or domain-specific overlays into this library.
- The existing `SpectrogramView` in `biocall_studio/review/gui/audio_proof.py` is **not** automatically an alp-ui component: it knows candidate interval/time/frequency metadata. Keep it downstream unless a domain-free, second-consumer use is proven and an API review approves extraction.
- No new runtime FFT/scientific, plotting or multimedia dependency for `alp-ui`. Keep source/backwards compatibility explicit for the consumer.

## Work / acceptance

1. **API / VM:** inventory imported `alp_ui` symbols in BioCall Studio; categorize each as public, plain Qt composition, or accidental app wrapper. Record a terse reuse table in the implementation PR, not an enduring spec dump.
2. **VM:** if an actual upstream issue exists, add only focused Qt component tests + Gallery showcase usage; run the ordinary `pytest`, Ruff, build and `twine check`. An absence of gaps is a valid result—no speculative widget.
3. **Local native:** no required new Cocoa screenshots. Current `docs/images/{showcase,gallery-*,consumer-default}.png` prove the public gallery presentation. Do not call these Windows evidence or installer qualification.
4. **Downstream:** BioCall Studio must reinstall the reviewed upstream wheel/commit and pass affected base tests before pinning a changed version/SHA.

**Done when:** no app/science code was dragged into the UI package, existing public components are preferred, and any real extracted Qt API has a named non-BioCall consumer or convincing generic contract, public tests, and gallery demonstration.

## Branch, PR and synchronization

Follow [VERSION_CONTROL.md](VERSION_CONTROL.md). **After spec PR #1 has been reviewed and merged**, branch `feat/alp-ui-01-reuse-boundaries` from that `main`. Commit actual reuse/API findings and any justified public widget/tests, create a focused implementation PR, review and merge to `main` **before** alp-ui 02. Report both feature PR SHA and the resulting merged-`main` SHA. A no-extraction result is valid; do not introduce fake code. No version tag at this stage.
