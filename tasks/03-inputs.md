# Task 03 — Forms: text, numeric, selection, checkbox

**Dependencies:** Task 02 completed. **Task type:** generic form controls, no validation engine.

## Read first

`AGENTS.md`, `COMPONENT_CATALOG.md`, `SPEC.md` (§5), `THEME_ALPACA_LIGHT.md`, `QUALITY.md`.

## Work

1. Implement `TextInput` around native `QLineEdit` with consistent small outlined appearance, optional label/help/error, placeholder, native `textChanged` and `editingFinished` exposed without duplicate custom signals.
2. Implement `NumberInput` using actual `QSpinBox`/`QDoubleSpinBox`; choose a compact predictable public API for int/float without manual text parsing or speculative conversion. Preserve range, step, decimals, and keyboard semantics.
3. Implement `SelectInput` using `QComboBox`, native item/model and selection APIs, keyboard opening/navigation, optional label/help/error.
4. Implement `CheckBox` using `QCheckBox` (not a custom Toggle/Switch) with theme typography and native checked signal.
5. Compose labels, errors, and descriptions so screen readers can identify them and keyboard focus goes to controls; share a tiny private field composition only after repeated implementation justifies it.
6. Add tests for valid/invalid input display, label association, selection change, text signal behavior, disabled, tab/focus, long labels, and theme tokens. Add gallery pages for controls and states.

## Artifacts

`components/inputs.py` (or justified modules), private field composition only if actually reused, public exports, tests, Gallery and usage docs.

## Acceptance

- [ ] Four controls available through public imports, preserve Qt native behavior and signals.
- [ ] Field labels/help/errors visually legible and exposed through Qt accessibility descriptions.
- [ ] No custom validation framework or persisted form state.
- [ ] No custom switch, input masks, async suggestions, file dialog, or extra runtime dependencies.
- [ ] Automated tests plus keyboard manual review passed.

**Owner checkpoint:** review button/form visual cohesion after Tasks 02 and 03. Any mismatch should be addressed through Theme/styles, not duplicated per-component CSS-like strings.
