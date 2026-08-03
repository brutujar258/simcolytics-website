"""Render the Simcolytics mark from measured geometry, at any size/palette.

Geometry constants come from build_mark.py (measured off the original raster).
This module adds: arbitrary placement, palette overrides, and an optional
light "lens" disc for use on dark backgrounds.
"""
import math
import numpy as np
from PIL import Image, ImageDraw

# ---- geometry, in "mark units" (origin = ring centre) ------------------------
RING_MID, RING_HALF = 73.0, 7.0
NECK_R0, NECK_R1, NECK_HALF = 74.0, 100.0, 7.5
HANDLE_R0, HANDLE_R1, HANDLE_HALF = 97.0, 175.0, 15.0
BATT_LEN, BATT_WID, BATT_CORNER, BATT_STROKE = 83.0, 54.0, 13.0, 5.0
NUB_WID, NUB_DEEP, NUB_CORNER = 24.0, 8.0, 3.0
BOLT_H, BOLT_W = 58.0, 32.0
AXIS, BATT_AXIS = 45.0, 135.0
LIGHT_DIR = 120.0

MEC_ALONG = (HANDLE_R1 + HANDLE_HALF - 80.0) / 2.0
MEC_R = (HANDLE_R1 + HANDLE_HALF + 80.0) / 2.0

BOLT_UNIT = [(0.32, -1.00), (-0.75, 0.13), (-0.14, 0.13),
             (-0.32, 1.00), (0.75, -0.13), (0.14, -0.13)]

# ---- palettes ---------------------------------------------------------------
LIGHT_BG = dict(                       # for white / light surfaces (Wise, print)
    gold=((0xBE, 0x9E, 0x4D), (0x68, 0x49, 0x16)),
    bolt=((0xD2, 0xB2, 0x5C), (0x96, 0x76, 0x2A)),
    green=((0x1C, 0x51, 0x27), (0x0E, 0x33, 0x16)),
    brown=((0x5C, 0x36, 0x18), (0x3F, 0x23, 0x0E)),
    lens=None,
)
DARK_LIFT = dict(                      # hue-preserving luminance lift
    gold=((0xD8, 0xB5, 0x5A), (0x9A, 0x78, 0x2E)),
    bolt=((0xF0, 0xD2, 0x76), (0xC2, 0x9C, 0x44)),
    green=((0x46, 0xA0, 0x5E), (0x2A, 0x6E, 0x3C)),
    brown=((0xA0, 0x6E, 0x3E), (0x74, 0x4A, 0x24)),
    lens=None,
)
DARK_LENS = dict(                      # keep brand colours, add a glass fill
    gold=((0xD8, 0xB5, 0x5A), (0x9A, 0x78, 0x2E)),
    bolt=((0xD2, 0xB2, 0x5C), (0x96, 0x76, 0x2A)),
    green=((0x1C, 0x51, 0x27), (0x0E, 0x33, 0x16)),
    brown=((0xA0, 0x6E, 0x3E), (0x74, 0x4A, 0x24)),
    lens=(0xF4, 0xF1, 0xE8),
)


def render(size_px, ring_xy, unit_scale, palette=LIGHT_BG, supersample=4):
    """Draw the mark into an RGBA image of `size_px` = (w, h).

    ring_xy      – where the ring centre lands, in final pixels
    unit_scale   – final pixels per mark unit
    """
    W, H = size_px
    ss = supersample
    SW, SH = W * ss, H * ss
    f = unit_scale * ss
    cx, cy = ring_xy[0] * ss, ring_xy[1] * ss

    yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
    px, py = (xx - cx) / f, (yy - cy) / f

    def cover(sdf):
        return np.clip(0.5 - sdf * f, 0.0, 1.0)

    def capsule(r0, r1, half, deg):
        t = math.radians(deg)
        ax, ay = math.cos(t) * r0, math.sin(t) * r0
        vx, vy = math.cos(t) * (r1 - r0), math.sin(t) * (r1 - r0)
        h = np.clip(((px - ax) * vx + (py - ay) * vy) / (vx * vx + vy * vy), 0, 1)
        return np.hypot(px - ax - h * vx, py - ay - h * vy) - half

    def rrect(ox, oy, w, l, rad, deg):
        t = math.radians(deg)
        ct, st = math.cos(t), math.sin(t)
        lx = (px - ox) * ct + (py - oy) * st
        ly = -(px - ox) * st + (py - oy) * ct
        qx, qy = np.abs(lx) - (l / 2 - rad), np.abs(ly) - (w / 2 - rad)
        return (np.hypot(np.maximum(qx, 0), np.maximum(qy, 0))
                + np.minimum(np.maximum(qx, qy), 0) - rad)

    def grad(pair):
        c0, c1 = pair
        t = math.radians(LIGHT_DIR)
        u = np.clip((px * math.cos(t) + py * math.sin(t)) / 176.0 + 0.5, 0, 1)[..., None]
        return np.array(c0, np.float32) * (1 - u) + np.array(c1, np.float32) * u

    rgb = np.zeros((SH, SW, 3), np.float32)
    alpha = np.zeros((SH, SW), np.float32)

    def paint(mask, colour):
        nonlocal rgb, alpha
        m = mask[..., None]
        rgb = colour * m + rgb * (1 - m)
        alpha = np.maximum(alpha, mask)

    gold, brown = grad(palette['gold']), grad(palette['brown'])
    green, bolt = grad(palette['green']), grad(palette['bolt'])

    if palette.get('lens'):
        lens = np.array(palette['lens'], np.float32)[None, None, :]
        paint(cover(np.hypot(px, py) - (RING_MID + RING_HALF - 1.0)), lens)

    paint(cover(capsule(NECK_R0, NECK_R1, NECK_HALF, AXIS)), gold)
    paint(cover(capsule(HANDLE_R0, HANDLE_R1, HANDLE_HALF, AXIS)), brown)
    paint(cover(np.abs(np.hypot(px, py) - RING_MID) - RING_HALF), gold)

    t = math.radians(BATT_AXIS)
    off = BATT_LEN / 2 + NUB_DEEP / 2 - 0.5
    paint(cover(rrect(-math.cos(t) * off, -math.sin(t) * off,
                      NUB_WID, NUB_DEEP + 6, NUB_CORNER, BATT_AXIS)), gold)
    paint(cover(rrect(0, 0, BATT_WID, BATT_LEN, BATT_CORNER, BATT_AXIS)), gold)
    paint(cover(rrect(0, 0, BATT_WID - 2 * BATT_STROKE, BATT_LEN - 2 * BATT_STROKE,
                      BATT_CORNER - BATT_STROKE, BATT_AXIS)), green)

    ct, st = math.cos(t), math.sin(t)
    poly = []
    for ux, uy in BOLT_UNIT:
        lx, ly = uy * BOLT_H / 2, ux * BOLT_W / 2
        poly.append((cx + (lx * ct - ly * st) * f, cy + (lx * st + ly * ct) * f))
    bm = Image.new('L', (SW, SH), 0)
    ImageDraw.Draw(bm).polygon(poly, fill=255)
    paint(np.asarray(bm, np.float32) / 255.0, bolt)

    arr = np.dstack([rgb, alpha * 255.0]).clip(0, 255)
    arr[..., :3] *= arr[..., 3:4] / 255.0            # premultiply for downsample
    small = Image.fromarray(arr.astype(np.uint8), 'RGBA').resize((W, H), Image.LANCZOS)
    sa = np.asarray(small, np.float32)
    sa[..., :3] = np.clip(sa[..., :3] * 255.0 / np.maximum(sa[..., 3:4], 1e-6), 0, 255)
    return Image.fromarray(sa.astype(np.uint8), 'RGBA')


def avatar(size=512, safe=0.90, palette=LIGHT_BG):
    """Square avatar: mark centred on its own minimum enclosing circle."""
    scale = (safe * size / 2.0) / MEC_R
    a = math.radians(AXIS)
    c = (size / 2.0 - MEC_ALONG * math.cos(a) * scale,
         size / 2.0 - MEC_ALONG * math.sin(a) * scale)
    return render((size, size), c, scale, palette)
