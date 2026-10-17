# Task 03 — Forms: text, numeric, selection, checkbox

**Dependencies:** Task 02 completed. **Task type:** generic form controls, no validation engine or async loader.

## Read first

`AGENTS.md`, `docs/project/COMPONENT_CATALOG.md`, `docs/project/SPEC.md` (§5), `docs/project/THEME_ALPACA_LIGHT.md`, `docs/project/QUALITY.md`.

## Work

1. Implement `TextInput` around native `QLineEdit` with consistent small outlined appearance, optional label/help/error, placeholder, native `textChanged` and `editingFinished` exposed without duplicate custom signals. Forward native `QValidator`, input-mask, and `QCompleter` APIs; consumers own any asynchronous model updates.
2. Implement `NumberInput` using actual `QSpinBox`/`QDoubleSpinBox`; choose a compact predictable public API for int/float without manual text parsing or speculative conversion. Preserve range, step, decimals, and keyboard semantics.
3. Implement `SelectInput` using `QComboBox`, native item/model and selection APIs, keyboard opening/navigation, optional label/help/error.
4. Implement `CheckBox` using `QCheckBox` with theme typography and native checked signal. Implement the separately named `Switch` requested by the owner as a painted two-state `QCheckBox`, retaining its native signal, focus, keyboard, and accessibility behavior.
5. Compose labels, errors, and descriptions so screen readers can identify them and keyboard focus goes to controls; share a tiny private field composition only after repeated implementation justifies it.
6. Add tests for valid/invalid input display, label association, selection change, text signal behavior, disabled, tab/focus, long labels, and theme tokens. Add gallery pages for controls and states.

## Artifacts

`components/inputs.py` (or justified modules), private field composition only if actually reused, public exports, tests, Gallery and usage docs.

## Acceptance

- [ ] Five controls available through public imports, preserve Qt native behavior and signals.
- [ ] Field labels/help/errors visually legible and exposed through Qt accessibility descriptions.
- [ ] No custom validation framework or persisted form state; native validation and masks remain authoritative.
- [ ] `Switch` remains two-state and QCheckBox-backed; completion uses caller-supplied `QCompleter` models with no async loader, file dialog, or extra runtime dependency.
- [ ] Automated tests plus keyboard manual review passed.

**Owner checkpoint:** review button/form visual cohesion after Tasks 02 and 03. Any mismatch should be addressed through Theme/styles, not duplicated per-component CSS-like strings.
