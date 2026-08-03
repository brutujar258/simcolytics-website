# Logo tooling

Regenerates every logo asset in the repository root from geometry.

```sh
python3 tools/build_assets.py      # needs numpy + Pillow
```

Deterministic — the same inputs always produce the same bytes. Nothing here is
part of the website; `_config.yml` keeps this directory out of the published
site.

## Files

| File | Purpose |
|---|---|
| `render_mark.py` | Mark geometry, colour palettes, and the renderer |
| `build_assets.py` | Entry point: extracts the lettering, writes every asset |
| `original-artwork.png` | The pre-rebuild wordmark, kept as the source of the type |

## What gets written

| Asset | Used by |
|---|---|
| `logo.png` | `og:image`, and any light background |
| `logo-on-dark.png` | Site header (dark theme) |
| `favicon.png` | Browser tab |
| `apple-touch-icon.png` | iOS home screen — opaque, because iOS ignores alpha |
| `logo-wise-avatar*.png` | Invoicing and profile avatars (square, circle-safe) |
| `logo-mark.svg` | Print and arbitrary scaling |

## Why the icon is redrawn but the type is not

The original artwork was a 226px raster carrying baked-in defects: noise in the
battery fill, a white keyline around the bolt, a gloss streak on the battery's
lower-left, and the battery sitting ~5px off the ring centre. Filtering cannot
remove any of that, so the icon is redrawn from geometry measured off the
original — ring inner r66 / outer r80, handle on the 45° axis, battery long axis
at 135°, with colours sampled from the artwork. `render_mark.py` documents the
measurements.

The "Simcolytics" lettering is a designed typeface and is **not** redrawn. It is
lifted from `original-artwork.png` unchanged.

## Removing the old icon from the wordmark

`build_assets.lettering()` deletes whole connected components rather than
masking a region. The old icon is three components — ring+neck, battery, and
handle — and each begins left of x=180, while no glyph does.

This matters: an earlier version used a geometric mask with a fixed margin and
left a one-pixel sliver of the old handle's antialiased edge behind, which then
shipped. Deleting components takes the soft edges with them.

## Palettes

`render_mark.py` defines three, and adding one is the supported way to make a
new colourway:

- `LIGHT_BG` — for white and light surfaces
- `DARK_LIFT` — hue-preserving luminance lift for dark backgrounds. Against the
  site's `#0b0b0b`, the untouched brown and green sit at 1.63:1 and 1.72:1,
  which reads as a smudge; this lifts them to 2.6–6.0:1.
- `DARK_LENS` — an alternative that keeps the exact brand green by filling the
  glass with a light disc. Not currently used.
