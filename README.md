# Mishkal production brand kit 1.1.0

Production artwork based on the selected **A1.2 / Light** direction: Portfolio Weave symbol, lowercase Signature lettering and the split k. Created 18 September 2026; web distribution updated 20 September 2026.

## Start here

- **Mishkal-Brand-Guide-v1.pdf:** the complete 11-page identity guide.
- **Mishkal-Identity-Preview.png:** a quick visual overview of the production logo.
- **svg/mishkal-horizontal-color.svg:** the primary editable vector master for light backgrounds.
- **svg/mishkal-horizontal-white.svg:** the reversed, transparent logo for dark backgrounds.
- **icons/favicon.svg:** the optical small-size symbol in Mishkal Teal on transparency.

All logo lettering is outlined. You do not need to install a font to use or edit the logos. SVG files contain editable paths, not embedded images. Keep the supplied proportions and viewBox.

For repository work, read [AGENTS.md](AGENTS.md) and
[repository controls](docs/Repository.md), including the shared reasoning trial
and model-upgrade policy. Branding owns approved identity; Website
and Webapp own their compositions. The shared frontend role serves explicitly
assigned consumers, while Branding has an explicitly bounded writer. A consumer
upgrade follows the distribution contract and its own registered task.

CI cancels superseded runs of the same pull request and bounds `brand-kit` to
10 minutes. Every source, manifest and distribution check remains enabled;
see [repository controls](docs/Repository.md) for scope and verification limits.
The repository is public so locked consumer builds can acquire an exact release
revision without a dedicated cross-repository secret. Consumers still validate
the committed lock and assets; public access does not replace integrity checks.

## Assets

| Folder or file | Contents |
|---|---|
| `svg/` | Horizontal, stacked, wordmark, standard symbol and small-size symbol; color, ink, pure black and white variants. Also two named background versions. |
| `png/` | Transparent exports at 1600 px wide for lockups and wordmarks; 512 px wide for standalone symbols. Background versions are explicitly named. |
| `icons/` | Navy installed-app PNGs at 16, 24, 32, 48, 64, 128, 180, 192, 256 and 512 px; transparent browser favicon SVG and ICO; app icon SVG; web manifest. |
| `fonts/` | Original Manrope variable TTF, IBM Plex Mono regular and medium TTF, and SIL OFL license files. |
| `docs/` | Usage notes, small-size proof, distribution contract and verification record. |
| `brand-tokens.css` | Semantic color and type tokens with no font-loading side effects. |
| `font-faces.css` | Optional local declarations for the bundled supporting fonts. |
| `geometry.json` | Documented path geometry, color values and layout dimensions. SVG masters remain the placement reference. |
| `Asset-Manifest.json` | Deterministic full release inventory and checksums; excludes itself. |
| `Web-Distribution.json` | Approved, checksummed source-to-consumer web allowlist. |

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

The logo is custom vector lettering, not a downloadable typeface. For supporting communication, use Manrope 400 for body text and 500-600 for headings and controls. Use IBM Plex Mono 400-500 sparingly for aligned values and research metadata. The included fonts retain their original licenses. Import `font-faces.css` only when a consumer wants the bundled local font-loading behavior; importing `brand-tokens.css` alone never requests a font resource.

## Web distribution

`Web-Distribution.json` is the schema-versioned contract for the approved web
subset. It records each source path, consumer path, byte count and SHA-256 in
source-path order. It includes semantic tokens, selected logo masters, browser
and installed-app icons, supporting fonts, and their SIL licenses. It excludes
itself, optional `font-faces.css`, preview artwork, and print assets.

```sh
python3 scripts/brand_distribution.py sync --consumer-root ../webapp
python3 scripts/brand_distribution.py check-consumer --consumer-root ../webapp
```

These consumer commands require clean, committed Branding source. Sync generates
the consumer's `brand.lock.json` with version, exact Branding commit and manifest
checksum. Commit the lock with the assets. Consumer CI acquires that pinned source
and runs read-only `check-consumer`; absent or mismatched locks fail verification.
See `docs/Distribution.md` for acquisition, versioning and release/upgrade steps.

Consumer-owned files such as `public/brand/SOURCE.md` are preserved. Unexpected
files or directories inside managed brand directories fail preflight and are
never deleted automatically. Before any consumer write, sync rejects invalid
manifest paths, root or managed-path symlinks, and unsupported or misplaced
entries, leaving the consumer tree unchanged. Missing or tampered regular files
can be repaired; matching regular files retain their modification times. See
`docs/Distribution.md` for the contract, access requirements and release procedure.

## Scope and status

The user selected the A1.2 visual direction. This kit reconstructs its outlines, regularizes edges and stems, and adds production layouts, optical small-size artwork and usage guidance. The broader typography, palette roles and editorial examples are documented as the proposed supporting system. The line "Trade with clarity. Live in balance." remains an editorial option, not an approved part of the logo.

Version 1.1.0 adopts the transparent browser favicon approved in webapp revision
`65f7a3374e3b60c326692a6d05a680eff38a5a36`. It retains the existing
small-symbol paths in Mishkal Teal and is not an artwork redesign. Installed app
and touch icons remain white on Deep Navy. No product code, website, account,
deployment, or consumer checkout was changed. The kit's logo shapes are vector
artwork, not a fresh image-generated variation.

## Font provenance

- [Manrope font source](https://github.com/google/fonts/tree/main/ofl/manrope) and [license](https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/OFL.txt).
- [IBM Plex Mono font source](https://github.com/google/fonts/tree/main/ofl/ibmplexmono) and [license](https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/OFL.txt).
- [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) supports the text contrast checks.

See `docs/Verification.md` for the checks performed and their limits.
