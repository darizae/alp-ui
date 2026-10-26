# Project Theme specification — Alpaca Light

## Provenance and authority

Alpaca Light's values are a locked library contract. Detailed provenance, file-level
mappings, and inspection notes remain local in the ignored `references/SOURCE_MAP.md`
and `docs/evidence.md`; this tracked document records only the resulting public theme
and independently authored Qt implementation requirements.

## Color palette (locked)

| Semantic token | Hex | Library role |
|---|---|---|
| `primary` | `#059669` | Primary actions and accents |
| `primary_hover` | `#047857` | Primary hover and pressed interaction |
| `on_primary` | `#FFFFFF` | Text and icons on primary fills |
| `secondary` | `#F59E0B` | Secondary accent |
| `background` | `#F8FAFC` | Application background |
| `surface` | `#FFFFFF` | Raised and grouped surfaces |
| `border` | `#E2E8F0` | Dividers and control outlines |
| `text` | `#0F172A` | Primary text |
| `text_muted` | `#64748B` | Supporting text |
| `success` | `#22C55E` | Successful state |
| `warning` | `#D97706` | Warning state |
| `danger` | `#DC2626` | Errors and destructive actions |
| `info` | `#2563EB` | Informational and focus state |
| `shadow` | `#000000` | Card shadow RGB base; component sets opacity |

The red semantic token is named `danger`; add an `error` alias only if a concrete
consumer requires it. `primary_hover` is the centralized interaction color. Secondary
is an accent, **not** a mandate to draw every secondary button amber.

## Typography and visual rules

| Feature | Library value | Qt implementation requirement |
|---|---|---|
| General family | `"DM Sans", sans-serif` | Prefer bundled unmodified DM Sans; documented system fallback. |
| Metadata family | `"JetBrains Mono", monospace` | Prefer bundled unmodified JetBrains Mono for badges/table heading/metadata, not body text. |
| Type scale | Body 12 pt; caption 11 pt; overline 10 pt; subheading 15 pt; heading 20 pt; title 26 pt | Readable native desktop defaults. Density changes geometry, never font size. |
| `h4` | Weight 700, letter spacing `-0.02em` | Approximate via QFont and font letter-spacing support if consistent. |
| `h5` | Weight 600, letter spacing `-0.01em` | Use QFont appropriate to platform font metrics. |
| `h6` | Weight 600 | Consistent headings. |
| Button text | No automatic uppercase, weight 600 | Sentence case, semibold. |
| Overline | Mono, `0.68rem`, weight 500, letter-spacing `0.08em` | Map to a documented compact Qt text role; not a literal pixel-equivalence promise. |
| Shape | Default radius `10px` | Card/default surface corner radius 10 logical px when custom-drawn. |
| Buttons | Radius `8px`, padding `6px 18px`, no elevation | Button variant appearance/size hint follows these proportions. |
| Cards | 1px border `#E2E8F0`, white surface, subtle `0 1px 3px rgba(0,0,0,0.08)` shadow | Preserve border and quiet shadow when performance and style permit; do not apply shadow effects to thousands of items. |
| Card content | 24px padding | Component token `card_padding = 24` logical px. |
| Text inputs | Small, outlined | Compact outlined form factor. |
| Table cells | Vertical padding 10px | Prefer row height/font metrics that approximate intent; keep large tables fast. |
| Table headings | Mono, `0.72rem`, 600, uppercase, `0.06em` tracking, muted text, slate-50 background | Header delegate/style metrics; keep data cells unaffected. |
| Tooltip | Mono `0.72rem` | Optional style polish in later phase; no mandatory custom Tooltip component. |
| Alerts | 8px radius | Tone-based feedback. |

Do not encode application-specific statuses in theme or feedback components. Data
tables use native `QTableView` scrolling rather than browser-style layout mechanics.

## Additional library-level values

- Spacing base unit: **4 logical px**; available spacings `0, 4, 8, 12, 16, 24, 32`. Prefer Qt size hints and layouts over fixed dimensions.
- Component sizes: `small`, `medium`, `large` only where a component truly benefits from size variants.
- Focus: visible keyboard focus state is mandatory, using theme `info` or primary with sufficient contrast. Exact ring thickness/color is to be determined in Phase 1 by accessibility tests; do not assume Qt native focus remains visible after styling.
- Disabled: muted, visibly distinct, still legible. Define the actual derived colors centrally after validating contrast, not by scattering manually mixed colors.
- Warning/danger tinted backgrounds: derive programmatically from semantic colors and surface in theme helper when a named feedback component needs them; do not invent extra persisted palette tokens.
- Light theme only, but data types should allow a future dark preset without changing component APIs.

## Theme API contracts

1. Theme is a **frozen typed object**, with subgroups for `colors`, `typography`, `spacing`, and `radii`; all tokens used by components must be declared.
2. Export one constant/preset named `ALPACA_LIGHT`; `Theme` and `install_theme` are public. `Theme` overrides use standard typed object construction (e.g., dataclass replacement) rather than string-key dict magic.
3. `install_theme(app, theme=ALPACA_LIGHT)` applies palette/font/style once before UI construction. It **does not** create the QApplication, start the event loop, or affect filesystem/network.
4. Consumers may construct another `Theme` preset and install at app startup. Switching Theme after widgets exist is not a v0.1 guarantee.
5. `QProxyStyle` adjustments require a measured/visual gap and targeted tests; do not implement a full custom rendering engine for pixel-perfect rendering.
6. Local QSS is an exception: document why a control cannot be styled adequately using palette/style/custom paint, limit selectors to that component, and never set a global changing stylesheet.
7. All fonts/resources must load offline via the installed wheel; font fallback must be deterministic and explained. Never fetch fonts from Google at application launch.

## Acceptance

The gallery must show theme token swatches, type samples, side-by-side native vs styled controls, and focus/disabled/error/hover states. The palette hex values above must be asserted in tests. A clean install must display the bundled fonts or explicitly report fallback in diagnostics. Components must have sufficient contrast at normal text sizes; use documented manual checks where automation cannot judge Qt rendering.

## Interaction states and density

The complete **original semantic Alpaca palette remains locked unchanged**. The
`InteractionTokens` are derived centrally from the semantic palette at the Theme
boundary (or explicitly overridden by a custom consumer Theme), rather than by
Component-local darkening/tinting. The `secondary` amber token remains available for
semantic accents; default secondary **Button** presentation is now quiet slate.

### Density (logical px)

| Metric | Standard (default) | Compact |
|---|---:|---:|
| Minimum text, numeric, select height | 40 | 34 |
| Minimum Button small, medium, large height | 32, 40, 44 | 30, 34, 38 |
| DataTable row | 44 | 36 |
| Card padding | 24 | 16 |

Text point sizes do not shrink when density is compact, and minimum heights may expand
for larger fonts. Qt retains its native editing, popup, step, and accessibility
behaviors; controls draw only small consistent vector subparts.

### Typography and icons

Keep DM Sans/JetBrains Mono and the readable role scale defined in the typography
table above. `make_icon` provides small original single-stroke Qt icons without an
external icon pack.

### Surface hierarchy

Prefer clear headings, whitespace, unbordered Gallery sections, quiet secondary
actions, and one Card surface around a form—not nested outlined groups inside
outlined Cards. The composed Showcase demonstrates this rather than adding a
public navigation component.
