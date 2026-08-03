#!/usr/bin/env python3
"""Regenerate every Simcolytics logo asset from geometry.

    python3 tools/build_assets.py

Writes into the repository root. Deterministic: same inputs -> same bytes.
Requires numpy and Pillow.

Why this exists
---------------
The original artwork (kept here as original-artwork.png) was a 226px raster
with noise baked into the battery fill, a white keyline around the bolt, a
gloss streak on the battery's lower-left, and the battery sitting ~5px off the
ring centre. None of that is removable by filtering, so the icon is redrawn
from geometry measured off that original. See render_mark.py for the numbers.

The "Simcolytics" lettering is NOT redrawn -- it is lifted from the original
artwork so the typography stays exactly as designed.
"""
import pathlib
import sys
from collections import deque

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import render_mark as R  # noqa: E402

ORIGINAL = HERE / 'original-artwork.png'
RING = (84.84, 86.58)   # icon ring centre within the original artwork
SCALE = 0.9973          # artwork pixels per mark unit
TYPE_X = 180            # lettering starts at x=189; icon parts all begin < 180


def lettering():
    """The wordmark's type, with the old icon removed exactly.

    The icon is three connected components (ring+neck, battery, handle) and
    every one of them starts left of TYPE_X, while no glyph does. Removing
    whole components takes the antialiased edges with them -- a geometric
    mask with a fixed margin leaves a sliver of the old handle behind.
    """
    im = Image.open(ORIGINAL).convert('RGBA')
    a = np.array(im)
    solid = a[..., 3] > 8
    H, W = solid.shape

    seen = np.zeros_like(solid)
    drop = np.zeros_like(solid)
    for sy in range(H):
        for sx in range(W):
            if not solid[sy, sx] or seen[sy, sx]:
                continue
            q, comp, min_x = deque([(sy, sx)]), [], sx
            seen[sy, sx] = True
            while q:
                y, x = q.popleft()
                comp.append((y, x))
                min_x = min(min_x, x)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = y + dy, x + dx
                        if (0 <= ny < H and 0 <= nx < W
                                and solid[ny, nx] and not seen[ny, nx]):
                            seen[ny, nx] = True
                            q.append((ny, nx))
            if min_x < TYPE_X:                      # part of the old icon
                for y, x in comp:
                    drop[y, x] = True

    a[..., 3] *= ~drop
    return Image.fromarray(a, 'RGBA')


def lockup(palette, out_name, letters, supersample=3):
    """New icon + original type, at the artwork's own dimensions."""
    W, H = Image.open(ORIGINAL).size
    big = (W * supersample, H * supersample)
    icon = R.render(big, (RING[0] * supersample, RING[1] * supersample),
                    SCALE * supersample, palette)
    icon.alpha_composite(letters.resize(big, Image.LANCZOS))
    icon.resize((W, H), Image.LANCZOS).save(ROOT / out_name)
    print('  wrote', out_name)


def svg(out_name='logo-mark.svg', size=512.0, safe=0.90):
    import math
    f = (safe * size / 2.0) / R.MEC_R
    ang = math.radians(R.AXIS)
    cx = size / 2.0 - R.MEC_ALONG * math.cos(ang) * f
    cy = size / 2.0 - R.MEC_ALONG * math.sin(ang) * f
    hexs = lambda c: '#%02X%02X%02X' % c

    def grad(gid, pair):
        t = math.radians(R.LIGHT_DIR)
        dx, dy = 88.0 * math.cos(t) * f, 88.0 * math.sin(t) * f
        return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
                f'x1="{cx-dx:.2f}" y1="{cy-dy:.2f}" x2="{cx+dx:.2f}" y2="{cy+dy:.2f}">'
                f'<stop offset="0" stop-color="{hexs(pair[0])}"/>'
                f'<stop offset="1" stop-color="{hexs(pair[1])}"/></linearGradient>')

    at = lambda r, d: (cx + r * math.cos(math.radians(d)) * f,
                       cy + r * math.sin(math.radians(d)) * f)
    p = R.LIGHT_BG
    nx0, ny0 = at(R.NECK_R0, R.AXIS);   nx1, ny1 = at(R.NECK_R1, R.AXIS)
    hx0, hy0 = at(R.HANDLE_R0, R.AXIS); hx1, hy1 = at(R.HANDLE_R1, R.AXIS)
    bw, bl = R.BATT_WID * f, R.BATT_LEN * f
    iw = (R.BATT_WID - 2 * R.BATT_STROKE) * f
    il = (R.BATT_LEN - 2 * R.BATT_STROKE) * f
    noff = (R.BATT_LEN / 2 + R.NUB_DEEP / 2 - 0.5) * f
    nw, nh = R.NUB_WID * f, (R.NUB_DEEP + 6) * f
    bolt = ' '.join(f'{cx + uy*R.BOLT_H/2*f:.2f},{cy + ux*R.BOLT_W/2*f:.2f}'
                    for ux, uy in R.BOLT_UNIT)

    out = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Simcolytics">
<title>Simcolytics</title>
<defs>
{grad('g', p['gold'])}
{grad('b', p['brown'])}
{grad('v', p['green'])}
{grad('z', p['bolt'])}
</defs>
<line x1="{nx0:.2f}" y1="{ny0:.2f}" x2="{nx1:.2f}" y2="{ny1:.2f}" stroke="url(#g)" stroke-width="{2*R.NECK_HALF*f:.2f}" stroke-linecap="round"/>
<line x1="{hx0:.2f}" y1="{hy0:.2f}" x2="{hx1:.2f}" y2="{hy1:.2f}" stroke="url(#b)" stroke-width="{2*R.HANDLE_HALF*f:.2f}" stroke-linecap="round"/>
<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R.RING_MID*f:.2f}" fill="none" stroke="url(#g)" stroke-width="{2*R.RING_HALF*f:.2f}"/>
<g transform="rotate({R.BATT_AXIS} {cx:.2f} {cy:.2f})">
  <rect x="{cx-noff-nh/2:.2f}" y="{cy-nw/2:.2f}" width="{nh:.2f}" height="{nw:.2f}" rx="{R.NUB_CORNER*f:.2f}" fill="url(#g)"/>
  <rect x="{cx-bl/2:.2f}" y="{cy-bw/2:.2f}" width="{bl:.2f}" height="{bw:.2f}" rx="{R.BATT_CORNER*f:.2f}" fill="url(#g)"/>
  <rect x="{cx-il/2:.2f}" y="{cy-iw/2:.2f}" width="{il:.2f}" height="{iw:.2f}" rx="{(R.BATT_CORNER-R.BATT_STROKE)*f:.2f}" fill="url(#v)"/>
  <polygon points="{bolt}" fill="url(#z)"/>
</g>
</svg>
'''
    (ROOT / out_name).write_text(out)
    print('  wrote', out_name)


def main():
    print('extracting lettering from original artwork...')
    letters = lettering()

    print('wordmark lockups:')
    lockup(R.LIGHT_BG,  'logo.png', letters)          # og:image, light surfaces
    lockup(R.DARK_LIFT, 'logo-on-dark.png', letters)  # site header (dark theme)

    print('icons:')
    R.avatar(256, safe=0.92).save(ROOT / 'favicon.png')
    print('  wrote favicon.png')

    apple = Image.new('RGBA', (180, 180), (255, 255, 255, 255))
    apple.alpha_composite(R.avatar(180, safe=0.84))   # iOS ignores alpha
    apple.convert('RGB').save(ROOT / 'apple-touch-icon.png')
    print('  wrote apple-touch-icon.png')

    print('invoice / profile avatars:')
    for px in (512, 1024):
        sfx = '' if px == 512 else f'-{px}'
        im = R.avatar(px)
        im.save(ROOT / f'logo-wise-avatar{sfx}.png')
        white = Image.new('RGBA', im.size, (255, 255, 255, 255))
        white.alpha_composite(im)
        white.convert('RGB').save(ROOT / f'logo-wise-avatar-white{sfx}.png')
        print(f'  wrote logo-wise-avatar{sfx}.png (+ -white)')

    print('vector:')
    svg()
    print('done.')


if __name__ == '__main__':
    main()
