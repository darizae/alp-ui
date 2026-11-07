# A1 reuse-boundary decision — 2026-11-07

**Decision: keep the public API unchanged.** Inspection of `alp-ui` at
[`bd91cb08e1958ee57ba6934c7a4a250677f11a99`](https://github.com/darizae/alp-ui/commit/bd91cb08e1958ee57ba6934c7a4a250677f11a99)
against BioCall Studio at
[`34d1e728f0ed30463c4bdebe3b220ceaec8f6cc7`](https://github.com/darizae/biocall-studio/commit/34d1e728f0ed30463c4bdebe3b220ceaec8f6cc7)
found no demonstrated, stable, domain-free second-consumer need that requires a new Component.

Studio imports existing public Components for actions, typography, fields, feedback,
model/view tables, and numeric line/categorical bar plots; it also uses the public
Theme API. Application navigation, routes, workspace models, filtering, and selection
remain ordinary Qt composition and Studio-owned behavior. In particular,
[`SpectrogramView`](https://github.com/darizae/biocall-studio/blob/34d1e728f0ed30463c4bdebe3b220ceaec8f6cc7/src/biocall_studio/review/gui/audio_proof.py)
uses Studio's `SpectrogramMetadata` and `SpectrogramRaster` for sample-frame
coordinates, frequency axes, and candidate overlays. A generic raster/axis API has no
verified unrelated consumer and would expand the approved `Plot` contract.

No WAV, FFT/STFT, spectrogram configuration/cache, playback, Review state, Results,
image generation, domain overlay, runtime dependency, or application controller is
moved upstream. Existing public APIs, the Gallery, documentation of Components, and
library tests remain untouched.

**Verification scope:** source/API inspection at the exact SHAs above. This is a
documentation-only no-extraction record; there are no changed Python files or new
component tests to execute. The focused implementation PR records the symbol-by-symbol
reuse inventory and requests review. Do not begin A2 until that PR is reviewed and
merged and the resulting `main` SHA is recorded.
