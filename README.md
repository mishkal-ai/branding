# mishkal - production brand kit 1.0

Production artwork based on the selected **A1.2 / Light** direction: Portfolio Weave symbol, lowercase Signature lettering and the split k. Created 18 September 2026.

## Start here

- **Mishkal-Brand-Guide-v1.pdf:** the complete 11-page identity guide.
- **Mishkal-Identity-Preview.png:** a quick visual overview of the production logo.
- **svg/mishkal-horizontal-color.svg:** the primary editable vector master for light backgrounds.
- **svg/mishkal-horizontal-white.svg:** the reversed, transparent logo for dark backgrounds.
- **icons/favicon.svg:** the optical small-size symbol on navy.

All logo lettering is outlined. You do not need to install a font to use or edit the logos. SVG files contain editable paths, not embedded images. Keep the supplied proportions and viewBox.

## Assets

| Folder or file | Contents |
|---|---|
| `svg/` | Horizontal, stacked, wordmark, standard symbol and small-size symbol; color, ink, pure black and white variants. Also two named background versions. |
| `png/` | Transparent exports at 1600 px wide for lockups and wordmarks; 512 px wide for standalone symbols. Background versions are explicitly named. |
| `icons/` | Square PNGs at 16, 24, 32, 48, 64, 128, 180, 192, 256 and 512 px; favicon SVG and ICO; app icon SVG; web manifest. |
| `fonts/` | Original Manrope variable TTF, IBM Plex Mono regular and medium TTF, and SIL OFL license files. |
| `docs/` | Usage notes, small-size proof and verification record. |
| `brand-tokens.css` | Local font declarations and color/type tokens for later implementation. |
| `geometry.json` | Documented path geometry, color values and layout dimensions. SVG masters remain the placement reference. |
| `Asset-Manifest.json` | File inventory and checksums. |

## Layout and size

Use the horizontal logo by default. Use the wordmark when the layout is too narrow, and the symbol by itself where the brand is already understood.

Digital minimum widths, including the built-in clear-space frame:

- Horizontal logo: **200 px**.
- Wordmark: **140 px**.
- Stacked logo: **180 px**.
- Square app icon: **16 px**. Use the optical small-size version below 48 px; the supplied 16, 24 and 32 px files already do this.

The master unit `u` is 40 design units, approximately one-sixth of the symbol height. Horizontal symbol-to-wordmark separation is `u`. Minimum external clear space is `u`; it is already included in the SVG canvas. The horizontal canvas is 1342 x 318 units.

Physical print starting sizes: 35 mm horizontal width, 25 mm stacked width, and 8 mm symbol width. These require a proof on the intended process and material. The kit uses an sRGB palette; it is not a set of printer-specific CMYK separations.

## Colors

| Name | Hex | Role |
|---|---|---|
| Deep teal | `#007F78` | Symbol and brand accents |
| Ink | `#10252B` | Text and one-color digital logo |
| Warm paper | `#F5F4EF` | Light surfaces |
| Deep navy | `#071C22` | Dark surfaces |
| Text teal | `#006D67` | Small text and links on warm paper |
| Aqua | `#34D6BB` | Accents on navy |
| Slate | `#52666B` | Secondary text on paper |

Use text teal rather than deep teal for small text on paper. Preserve the deep teal in the logo. Use white for the primary reversed logo. `black` assets use pure `#000000` for one-color artwork.

## Typography

The logo is custom vector lettering, not a downloadable typeface. For supporting communication, use Manrope 400 for body text and 500-600 for headings and controls. Use IBM Plex Mono 400-500 sparingly for aligned values and research metadata. The included fonts retain their original licenses.

## Scope and status

The user selected the A1.2 visual direction. This kit reconstructs its outlines, regularizes edges and stems, and adds production layouts, optical small-size artwork and usage guidance. The broader typography, palette roles and editorial examples are documented as the proposed supporting system. The line "Trade with clarity. Live in balance." remains an editorial option, not an approved part of the logo.

No product code, website, account or deployment was changed. Source research plans informed the brand context; their implementation instructions were not executed. The kit's logo shapes are vector artwork, not a fresh image-generated variation.

## Font provenance

- [Manrope font source](https://github.com/google/fonts/tree/main/ofl/manrope) and [license](https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/OFL.txt).
- [IBM Plex Mono font source](https://github.com/google/fonts/tree/main/ofl/ibmplexmono) and [license](https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/OFL.txt).
- [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) supports the text contrast checks.

See `docs/Verification.md` for the checks performed and their limits.
