# Production verification

Verified 19 September 2026.

- 22 SVG masters parse successfully and use editable vector outlines, with no embedded raster images or live text/font dependency.
- 22 PNG exports checked for expected widths. Transparent versions have alpha transparency; background versions are explicitly named.
- All 10 square icon sizes checked. The ICO contains exact supplied 16, 32, 48 and 64 px frames, including optical corrections at the smaller sizes.
- Web manifest icon references resolve within the kit.
- The 11-page PDF was rendered and visually reviewed for spacing, legibility and clipping. Text remains extractable.
- Logo and wordmark size studies reviewed on light and dark backgrounds. See `Size-Proof.png` at actual pixel size. Recommended minimums are documented in the guide.
- Text contrast calculated with the WCAG relative-luminance method: ink/paper 14.43:1; slate/paper 5.49:1; text teal/paper 5.64:1; aqua/navy 9.58:1. Deep teal/paper is 4.43:1 and is reserved for the logo and suitable large accents, not small text.
- Original supporting-font license files are bundled.

## Limits

These checks cover the supplied digital artifacts. Physical print, embroidery, signage, app-store-specific masking and rendering in the live Mishkal product have not been tested. Print color and minimum sizes require a physical proof on the intended process and material. The optional tagline and supporting editorial examples are proposals.
