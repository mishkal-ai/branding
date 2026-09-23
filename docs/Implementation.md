# Placement and implementation

For a light header, use the primary SVG at 260 px wide, allowing height to follow its aspect ratio. The minimum full-logo width is 220 px.

```html
<a href="/" aria-label="PHIOON home">
  <img src="/brand/svg/phioon-horizontal-color.svg"
       alt="" width="260" style="height:auto" />
</a>
```

For a dark header, use `phioon-horizontal-white.svg`. Below 220 px available width, switch to the wordmark (minimum 170 px) or symbol. Keep the built-in clear-space frame. The white SVG is transparent and may look blank on a white viewer canvas.

## Browser icons

```html
<link rel="icon" href="/brand/icons/favicon.svg" type="image/svg+xml" />
<link rel="alternate icon" href="/brand/icons/favicon.ico" />
<link rel="apple-touch-icon" href="/brand/icons/phioon-icon-180.png" />
<link rel="manifest" href="/brand/icons/site.webmanifest" />
```

Manifest icon URLs are relative to the manifest. The square icons are for `any` use; they are not dedicated maskable app-store assets. The 16/24/32 px PNGs use the optical small-size symbol. The ICO retains the exact supplied 16/32/48/64 px frames.

The supplied browser favicon is white on Deep Navy, matching the PHIOON app
icon treatment. This release intentionally replaces the transparent teal browser
favicon from the Mishkal 1.1.0 distribution; do not recreate that older treatment.

## Editing

Logos contain vector paths with no font or external-image dependency. Keep their proportions. If inserting raw SVG markup multiple times into a document, namespace IDs and title references; using image elements avoids shared ID conflicts.

Manrope and IBM Plex Mono support the surrounding interface and documents. They
do not recreate the PHIOON wordmark. Import `brand-tokens.css` for `--phioon-*`
tokens without font requests. Optional `font-faces.css` uses `./fonts/` relative
to itself; it is intended for the complete kit layout, not the web distribution.
Web consumers receive binaries under `app/fonts` and licenses under
`public/brand/fonts`, and must retain their own font-loading setup.

## Consumer migration

Use the committed distribution tool, then update consumer references from
`mishkal-*` assets and `--mishkal-*` tokens to the corresponding `phioon-*` names.
Update visible names and accessible labels to PHIOON, plus document titles,
metadata, manifest references, favicon and touch-icon selections. Give full
horizontal logos at least 220 px; compact slots may use the wordmark at 170 px
or a standalone symbol. Verify light and dark surfaces and narrow screens.
Keep operational domains, repository coordinates and persistent identifiers
unless their own migration is explicitly authorized. See
[Distribution](Distribution.md) for safe asset retirement and lock validation.

Use vector artwork for print. Convert colors with the print provider’s profile and check a physical proof. Do not infer print readiness from a screen preview.
