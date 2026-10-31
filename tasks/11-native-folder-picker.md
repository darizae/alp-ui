# Agent task 11 — Native folder selection Component

**Status:** proposed post-v0.1 extension, explicitly requested by the repository owner on 24 October 2026.  
**Repository:** `alp-ui` (`alp_ui` import root); local installation from `../alp-ui`, **not PyPI**.  
**Consumer evidence:** `../alpacaDesktop/docs/design/prototypes/training-first/app.js` (`home`, `chooseFolder`, `scanLocalFolder`), [Trainer audit](../../alpacaDesktop/docs/design/ALP_UI_TRAINER_GAP_AUDIT.md) when available in the sibling repo.  
**Ownership:** generic Qt presentation + folder *selection*, not reading or interpreting folder contents.

## 1. Need and narrow scope

**alpaca Desktop Trainer** starts with “Select folder”. On macOS and Windows the user needs one consistent, themed row displaying the chosen local folder and opening the operating system's standard directory picker. The existing `Button`, `TextInput`, and `QFileDialog` can be composed by each consumer, but their combined label, current path, Browse action, cancellation behavior, focus, and accessible description are a plausible repeated interaction across desktop applications. The owner has expressly requested this reusable capability upstream.

Implement **one `FolderPicker` Component**: a read-only folder path display + native folder-browse action. No custom filesystem tree/browser, no drag-and-drop system, no source-data validation or async scanning. If inspection shows a truly identical existing public Component, reuse it and document evidence rather than duplicate it.

**What the user sees:** a plain label (e.g. “Folder”), the selected folder path, and a button reading **“Choose folder”**. No technical terms such as “binding”, “canonical reference”, “artifact”, “index”, or “import” in the library's visible copy. The consumer supplies any domain-specific title such as “Collection”.

## 2. Inspect existing source first

Follow [AGENTS.md](../AGENTS.md) onboarding and its order. Pay special attention to `docs/project/{GLOSSARY,DECISIONS,SPEC,COMPONENT_CATALOG,QUALITY}.md`, `src/alp_ui/components/{inputs,actions}.py`, `src/alp_ui/theme/{install,tokens,appearance}.py`, `gallery/main.py`, `docs/components.md`, `tests/{test_inputs,test_consumer_example}.py`. Native equivalents: `QFileDialog`, `QLineEdit` in read-only mode, `QPushButton`, `QLabel`, `QHBoxLayout`, `QFileDialog.Directory` and `ShowDirsOnly`. Existing components expose native Qt controls/signals where appropriate, preserve the consumer's sole `QApplication`, and avoid workers. Do not port HTML file-picker code from the prototype.

A `FolderPicker` is an explicitly requested post-v0.1 candidate in `docs/project/COMPONENT_CATALOG.md`; record its promotion from candidate to approved *planned* extension. D02/D03/D07/D08/D12 remain unchanged: native Widgets, theme tokens, no new runtime dependency and no app data.

## 3. Proposed public contract

Refine naming only for concrete Qt consistency reasons and document any choice:

```python
from alp_ui.components import FolderPicker

folder = FolderPicker(label="Folder", show_hidden=True)
folder.folderChanged.connect(on_folder_changed)  # string native path, consumer handles it
folder.setFolderPath("/home/example/audio")
selected_path = folder.folderPath()  # "" means none chosen
```

- **Structure:** `QWidget` composition around a read-only, accessible `QLineEdit` (or smaller native equivalent) and styled `Button`, with an optional label and native `QFileDialog`. Preserve normal parent/layout ownership; expose `.control` for the path field only if it matches existing input conventions. Use existing Theme sizing and spacing, both `standard`/`compact` densities, no component-specific brand hex literals.
- **Path state:** a single Unicode path string. Initially empty by default; use `setFolderPath(str)` and `folderPath() -> str`. `""` means no selection; it is not an invalid Collection. Do not convert it into a scientific path, resolve symlinks, touch the folder, read metadata, or persist settings. Preserve returned native path exactly except a Qt-required, documented display conversion; do not silently rewrite canonical app paths. The visible display may elide **without changing the returned value**; full value remains available via accessible description/tool tip.
- **Signals:** one `folderChanged(str)` signal when the selected path actually changes, whether through `setFolderPath` or the picker. Cancellation, failure to open, and reselecting the same path **do not** emit a change or clear prior state. Do not forward duplicate signals from internal controls. The consumer can use `QSignalBlocker` when restoring startup state.
- **Browse:** user click/keyboard activation opens Qt's native directory-selection dialog by default, parented to the component/window. `show_hidden=True` uses Qt's widget-based directory dialog with `QDir.Hidden`, because the native API has no portable show-hidden option. A returned directory changes path; Cancel leaves it intact. Starting directory may be the currently chosen directory, otherwise Qt's standard default. Do not implement an app-owned recent-folders list, history or save default. Avoid global `chdir` and shell/file-system subprocesses.
- **No validation:** never require a particular hierarchy, file extension, existing user permissions, writable directory, or non-empty collection. A consumer may show its own `Alert` or call a worker after the signal. The native dialog's normal directory selection is not scientific validation.
- **Accessibility:** the path field has the visible label as its accessible name, and the browse button exposes “Choose folder” (or “Choose <label>” if the label is supplied) rather than an icon-only name. Normal keyboard Tab order, visible focus and Space/Return button activation. Screen readers can obtain the full selected path, not only visually shortened text. Preserve RTL and translated/long label behavior. For a read-only field, do not imply the user may type into it.
- **No silent work:** the Component does not start a thread, validate, scan, hash, cache, enumerate or monitor folders. `folderChanged` is a UI signal, not an assurance that the folder is usable.
- **Native dialog API:** using `QFileDialog.getExistingDirectory` is acceptable if the existing event-loop behavior and testability suffice; otherwise retain a parent-owned `QFileDialog` instance. Avoid introducing async claims, a second event loop, or a dialog abstraction used nowhere else.

Do not add a `FilePicker`, path tokenizer, a general-purpose resource chooser, or a cross-platform path persistence service as speculative adjacent features.

## 4. Implementation and documentation files

- Add `FolderPicker` to an appropriate existing input module or `src/alp_ui/components/folders.py` **only if** ownership is clearer; search before introducing a new module.
- Export from `src/alp_ui/components/__init__.py`, add typed API with ordinary Qt setters/signals.
- Document constructor, `setFolderPath`, `folderPath`, `folderChanged`, cancellation, limits and a consumer-controlled scan example in `docs/components.md`; give a small gallery example in `gallery/main.py` and an import test from the built wheel.
- Update `docs/project/COMPONENT_CATALOG.md` and the post-v0.1 plan/spec as *implemented* only after tests pass. The current v0.1 public list remains historical, not retroactively modified. Update `docs/project/GLOSSARY.md` only if a new generic *term* is truly needed; `FolderPicker` is already just a **Component**.
- No Theme API additions unless an existing semantic token is demonstrably inadequate. No new dependency/license notice is expected.

## 5. Tests and acceptance (planned until executed)

| Boundary | Smallest fixture/action | Expected evidence |
|---|---|---|
| Qt Component | Construct with empty path and optional label | Correct accessible names, button/path field, native parent ownership; no folder read, no extra `QApplication`. |
| Qt Component | `setFolderPath` with ordinary, long, Unicode and Windows-shaped strings | Exact `folderPath` round trip and full accessible value; visible elision does not truncate stored path. |
| Qt Component | Set same path twice, change once | Exactly one `folderChanged` for the actual change; no double emission. |
| Qt Component | Mock only the native dialog result: valid folder, Cancel, repeated folder | Selection updates once; Cancel leaves state unchanged. Tests must not claim a mocked dialog proves native UX. |
| Qt Component | Tab/Shift+Tab, mouse click, keyboard activate, disabled, RTL | Browse control remains reachable, has visible focus, disabled activation does nothing. |
| Qt Component | Theme override and both densities, 100%/150% scaling | Layout and text legible; no clipping of action or hard-coded colors; manual review as needed. |
| Installed wheel | Independent consumer imports and places picker in normal Qt layout | Works with `install_theme(app)` and PySide6-Essentials alone. |
| Native OS smoke | Real macOS + Windows directory dialog, choose/cancel, long/Unicode path | OS-native selection behaves correctly. Do not claim Windows pass from macOS/offscreen tests. |

Use temporary *empty* directories for true filesystem/dialog smoke tests; WAV files, Collection manifests, permissions, and metadata-cache fixtures belong in the Trainer's own integration tests. Run the existing `pytest`, `ruff`, `build`, `twine check` and Gallery workflows specified by `AGENTS.md`; report environment and outcomes.

## 6. Completion gate

A third-party consumer can render a themed folder selector, open a native directory dialog, read the selected path and react to **one** change signal. The library does **not** decide whether the folder is a valid input, what to load, how long scanning takes, or where metadata is saved. No new runtime dependency, domain wording or controller is introduced.
