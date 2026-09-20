# Production verification

Verified 20 September 2026 for release 1.1.0.

- 22 SVG masters parse successfully and use editable vector outlines, with no embedded raster images or live text/font dependency.
- 22 PNG exports checked for expected widths. Transparent versions have alpha transparency; background versions are explicitly named.
- All 10 square installed-app icons retain their original white-on-Navy files.
  The transparent teal SVG and ICO browser favicons match the exact blobs from
  webapp revision `65f7a3374e3b60c326692a6d05a680eff38a5a36`.
- Web manifest icon references resolve within the kit.
- The 11-page PDF was rendered and visually reviewed for spacing, legibility and clipping. Text remains extractable.
- Logo and wordmark size studies reviewed on light and dark backgrounds. See `Size-Proof.png` at actual pixel size. Recommended minimums are documented in the guide.
- Text contrast calculated with the WCAG relative-luminance method: ink/paper 14.43:1; slate/paper 5.49:1; text teal/paper 5.64:1; aqua/navy 9.58:1. Deep teal/paper is 4.43:1 and is reserved for the logo and suitable large accents, not small text.
- Original supporting-font license files are bundled.
- Both manifests are deterministic and omit their own hash where necessary to
  avoid a self-hash cycle. Tests cover manifest consistency, font licenses, sync
  idempotency and modification-time preservation, missing/tampered file repair,
  and rejection of extra files/directories without extra-directory traversal.
  Snapshot regressions verify an unchanged consumer tree for links to consumer
  `SOURCE.md`, approved files and external targets; internal/external directory
  links; dangling, matching-byte and extra links; root links through both the
  API and CLI; misplaced/unsupported entries; and late invalid manifest paths.
- Lock tests cover deterministic version/commit/manifest identity, missing or
  malformed/stale/mismatched locks, lock topology, lock mtime preservation and
  explicit upgrades. Isolated temporary Git repositories exercise committed CLI
  sync/check, revision mismatches, and dirty/staged/untracked/status-hidden source
  rejection. Topology tests mock only source-revision validation so pending work
  can be checked without claiming it is a published source commit.

## Reproduce

```sh
python3 scripts/brand_distribution.py generate --check
python3 scripts/brand_distribution.py check-source
python3 -m unittest discover -s tests -v
```

## Limits

These checks cover the supplied artifacts and temporary consumer trees. They do
not establish a real consumer sync, deployed state, browser cache state,
physical print, embroidery, signage, app-store-specific masking, or live-product
rendering. Print color and minimum sizes require a physical proof on the intended
process and material. The optional tagline and editorial examples are proposals.
