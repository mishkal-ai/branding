# Placement notes

## Web

Use the SVG master in an image element and let its height follow its intrinsic aspect ratio. For example, after placing the kit under `/brand/`:

```html
<a href="/" aria-label="Mishkal home">
  <img src="/brand/svg/mishkal-horizontal-color.svg"
       alt="" width="200" style="height:auto" />
</a>
```

For a dark header use `mishkal-horizontal-white.svg`. The white SVG is transparent; it can appear blank in a viewer with a white canvas. Use the named dark-background version when a visible standalone preview is needed.

Keep the SVG clear-space frame. Do not crop it away with a negative margin or `object-fit: cover`. If the primary logo has less than 200 px available, switch to the wordmark or symbol asset.

`brand-tokens.css` only declares semantic custom properties; it neither loads
fonts nor styles product elements. Consumers may load fonts through their own
framework, or import `font-faces.css` when its relative `fonts/` directory is
preserved. Font loading is deliberately optional.

## Browser and app icons

```html
<link rel="icon" href="/brand/icons/favicon.svg" type="image/svg+xml" />
<link rel="alternate icon" href="/brand/icons/favicon.ico" />
<link rel="apple-touch-icon" href="/brand/icons/mishkal-icon-180.png" />
<link rel="manifest" href="/brand/icons/site.webmanifest" />
```

The manifest's icon URLs are relative to the manifest. Browser favicon assets
use the optically corrected Mishkal Teal symbol on transparency. The square
installed-app and touch icons remain white on Navy and are declared for `any`
use, not `maskable`. Add safe-area variants if an app store requires them.

The transparent ICO is the exact browser artifact approved in webapp revision
`65f7a3374e3b60c326692a6d05a680eff38a5a36`. Browser caches can retain an older
favicon after deployment; a source check does not establish displayed state.

## Consumer synchronization

The distribution manifest maps source paths to approved webapp locations:

```sh
python3 scripts/brand_distribution.py sync --consumer-root /path/to/webapp
python3 scripts/brand_distribution.py check-consumer --consumer-root /path/to/webapp
```

Sync verifies the source, replaces missing or mismatched approved files
atomically, skips matching files, writes `brand.lock.json`, and verifies the
result. Consumer commands require a clean committed Branding checkout; the lock
binds its version, full commit and exact web-manifest checksum. Commit the lock
with the assets, and use `check-consumer` from the consumer root in CI with the
locked Branding source explicitly acquired. See `Distribution.md` for acquisition,
release and upgrade instructions. It never deletes
unexpected consumer files; extras in managed directories must be resolved
explicitly. Before any write, sync validates every manifest path and preflights
the consumer root, managed destinations, lock and intervening directories. Root or
managed-path symlinks, unsupported or misplaced entry types, and extras reject
the whole operation with the consumer tree unchanged. Extra directories are
not traversed. Matching files retain their modification times. See
`Distribution.md` for diagnostics and the exclusive-access requirement.

## Editing

Open the SVG in a vector editor. Separate `symbol` and `wordmark` groups and named `letter-*` paths make the geometry accessible. The supplied outlines are the source of truth for the logo. The accompanying Manrope and IBM Plex Mono fonts are for supporting content only.

If embedding SVG markup directly more than once in a document, namespace its IDs or replace the title reference with an appropriate accessible label. Using separate image elements avoids shared ID conflicts.

## Print

Use the vector artwork rather than enlarging a PNG. Use the pure black variant for one-color work. Convert brand colors using the print provider's specified profile, then check a physical proof. No Pantone match, substrate-specific correction or press proof has been established in this kit.
