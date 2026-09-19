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

The CSS token file references the bundled fonts relative to its own location. Preserve the folder relationship or adjust URLs when integrating. It does not style or modify an existing product automatically.

## Browser and app icons

```html
<link rel="icon" href="/brand/icons/favicon.svg" type="image/svg+xml" />
<link rel="alternate icon" href="/brand/icons/favicon.ico" />
<link rel="apple-touch-icon" href="/brand/icons/mishkal-icon-180.png" />
<link rel="manifest" href="/brand/icons/site.webmanifest" />
```

The manifest's icon URLs are relative to the manifest. The square icons use a navy background and are declared for `any` use, not `maskable`. Add platform-specific exports or safe-area variants if a particular app store requires them.

The ICO contains individually supplied 16, 32, 48 and 64 px PNG frames. The 16 and 32 px frames preserve the small-size optical corrections; they are not downscaled copies of the standard 512 px icon.

## Editing

Open the SVG in a vector editor. Separate `symbol` and `wordmark` groups and named `letter-*` paths make the geometry accessible. The supplied outlines are the source of truth for the logo. The accompanying Manrope and IBM Plex Mono fonts are for supporting content only.

If embedding SVG markup directly more than once in a document, namespace its IDs or replace the title reference with an appropriate accessible label. Using separate image elements avoids shared ID conflicts.

## Print

Use the vector artwork rather than enlarging a PNG. Use the pure black variant for one-color work. Convert brand colors using the print provider's specified profile, then check a physical proof. No Pantone match, substrate-specific correction or press proof has been established in this kit.
