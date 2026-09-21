#!/usr/bin/env python3
"""22 — THE TIME MACHINE (1895): the further vision.

The day opened on the machine in a Richmond laboratory and closes on the same
machine thirty million years downstream, on the beach at the end of the world.

Made differently from the other four: no SVG. The light is a continuous field
computed in numpy — the dull red dome on the horizon, its glow falling off
through the cold air, the flat sea under it — and then screened through an 8x8
Bayer matrix *before* it ever meets the palette, so the gradient becomes an
honest print texture instead of a dither applied to a photograph. Only the
silhouettes are drawn, in flat ink, over the screen. Three colours: black,
red, and the white that survives in the snow and on the rims of things.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 600
K = (0, 0, 0)
P = (255, 255, 255)
R = (0xE0, 0x1B, 0x24)

HOR = 402
SUNX, SUNY, SUNR = 196, 396, 98

rnd = random.Random(30_000_000)

BAYER = np.array([
    [0, 32, 8, 40, 2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
], dtype=np.float32) / 64.0

# ------------------------------------------------------------- the light
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
d = np.hypot(xx - SUNX, (yy - SUNY) * 1.15)

tone = 0.95 * np.exp(-(d / 118.0) ** 1.6)                      # the dome's halo, and no more
tone += 0.20 * np.exp(-((yy - HOR) / 24.0) ** 2)               # haze lying on the horizon
tone *= np.clip((yy - 40) / 320.0, 0.02, 1.0)                  # the sky dead black overhead

# a bank of cloud drawn across the dome, eating the glow
cloud = np.zeros_like(tone)
for (cy, amp, wid, freq, ph) in ((300, 1.0, 26, 0.016, 0.4), (250, 0.7, 17, 0.026, 2.1),
                                 (346, 0.8, 13, 0.021, 4.0)):
    edge = cy + amp * 16 * np.sin(xx * freq + ph) + amp * 8 * np.sin(xx * freq * 2.7 + ph * 2)
    cloud += np.clip(1.0 - np.abs(yy - edge) / wid, 0, 1)
tone *= 1.0 - 0.72 * np.clip(cloud, 0, 1)

# the sea: flat, and lit only in a broken column under the sun
sea = yy > HOR
band = 0.80 * np.exp(-((xx - SUNX) / 54.0) ** 2)
ripple = (np.sin(yy * 0.85) * 0.5 + 0.5) * (np.sin(xx * 0.07 + yy * 0.4) * 0.5 + 0.5)
tone = np.where(sea, band * (0.25 + 0.90 * ripple) * np.exp(-(yy - HOR) / 84.0), tone)

# the beach, at the bottom: almost nothing reaches it
beach = yy > 500
tone = np.where(beach, 0.0, tone)

tone = np.where(tone < 0.085, 0.0, tone)   # nothing faint enough to speckle

screen = np.tile(BAYER, (H // 8 + 1, W // 8 + 1))[:H, :W]
ink = tone > screen
img = np.zeros((H, W, 3), dtype=np.uint8)
img[ink] = R
base = Image.fromarray(img, "RGB")
dr = ImageDraw.Draw(base)

# ------------------------------------------------------------- the dome
# the sun itself is solid, banded like a woodcut, with a hard white rim
dr.ellipse([SUNX - SUNR, SUNY - SUNR, SUNX + SUNR, SUNY + SUNR], fill=R)
for i in range(16):
    t = i / 15
    y0 = SUNY - SUNR + t * 2 * SUNR
    if abs(y0 - SUNY) > SUNR:
        continue
    hw = math.sqrt(max(0.0, SUNR ** 2 - (y0 - SUNY) ** 2))
    th = 1 + int(3.4 * t)
    dr.rectangle([SUNX - hw, y0, SUNX + hw, y0 + th], fill=K)
# the inner planet, crossing
EPX, EPY, EPR = 146, 334, 58
dr.ellipse([EPX - EPR, EPY - EPR, EPX + EPR, EPY + EPR], fill=K)
# brilliance along the free edge of the crescent
for a in range(-900, 900):
    ang = a / 900 * math.pi
    px, py = SUNX + SUNR * math.sin(ang), SUNY - SUNR * math.cos(ang)
    if math.hypot(px - EPX, py - EPY) < EPR + 1.5 or py > HOR:
        continue
    dr.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=P)

# stars, only where the sky is properly black
for _ in range(110):
    x, y = rnd.uniform(2, W - 2), rnd.uniform(2, 290)
    if tone[int(y), int(x)] > 0.10:
        continue
    r = rnd.choice([0.7, 0.7, 1.0, 1.4])
    dr.ellipse([x - r, y - r, x + r, y + r], fill=P)

# the sea's edge
dr.line([0, HOR, W, HOR], fill=K, width=3)
for i in range(46):
    x0 = rnd.uniform(-10, W)
    ln = rnd.uniform(14, 60)
    y0 = HOR + rnd.uniform(2, 76)
    dr.line([x0, y0, x0 + ln, y0], fill=K, width=2)

# --------------------------------------------------------------- the land
rock = [(0, 600), (0, 540)]
ridge = []
for i in range(33):
    x = i * W / 32
    hgt = (20 + 16 * math.sin(i * 0.8 + 1.2) + 10 * math.sin(i * 2.1) + rnd.uniform(0, 9))
    ridge.append((x, 536 - hgt * 0.5))
rock += ridge + [(W, 540), (W, 600)]
dr.polygon(rock, fill=K)
# frost catching on the seaward faces only
for i in range(len(ridge) - 1):
    if ridge[i + 1][1] < ridge[i][1]:
        dr.line([ridge[i], ridge[i + 1]], fill=P, width=2)
# boulders: flat black, a rim of frost on top
for (bx, by, bw, bh, sd) in ((58, 556, 78, 40, 1), (322, 548, 88, 44, 2), (196, 580, 104, 36, 3)):
    pr = random.Random(sd)
    pts = []
    for i in range(16):
        a = 2 * math.pi * i / 16
        rr = 1 + 0.22 * pr.random()
        pts.append((bx + bw / 2 * math.cos(a) * rr, by + bh / 2 * math.sin(a) * rr))
    dr.polygon(pts, fill=K)
    top = [q for q in pts if q[1] < by]
    if len(top) > 1:
        dr.line(sorted(top), fill=P, width=1)
    for _ in range(26):
        a = pr.uniform(math.pi, 2 * math.pi)
        rr = pr.random() ** 0.5
        dr.point((bx + bw / 2 * math.cos(a) * rr * 0.8,
                  by + bh / 2 * math.sin(a) * rr * 0.8), fill=R)

# --------------------------------------------------------------- the crab
def crab(cx, cy, s, seed=0, claws=True):
    pr = random.Random(seed)
    bw, bh = 62 * s, 34 * s
    # legs first, so the carapace sits over their roots
    for side in (-1, 1):
        for i in range(5):
            t = i / 4
            hipx = cx + side * bw * (0.22 + 0.52 * t) * 0.9
            hipy = cy - bh * 0.10 + bh * 0.12 * math.sin(t * 3)
            kx = hipx + side * 40 * s * (0.7 + 0.5 * t)
            ky = hipy - 34 * s * (1.0 - 0.45 * t)
            fx = kx + side * 26 * s * (0.6 + 0.6 * t)
            fy = cy + bh * (1.45 + 0.55 * t)
            dr.line([hipx, hipy, kx, ky], fill=K, width=max(3, int(7 * s)))
            dr.line([kx, ky, fx, fy], fill=K, width=max(2, int(5 * s)))
            dr.line([hipx, hipy - 1, kx, ky - 1], fill=P, width=1)
            dr.ellipse([kx - 4 * s, ky - 4 * s, kx + 4 * s, ky + 4 * s], fill=K)
    # carapace
    shell = []
    for i in range(29):
        a = math.pi * i / 28
        rr = 1 + 0.06 * math.sin(a * 7)
        shell.append((cx - bw * math.cos(a) * rr, cy - bh * math.sin(a) * rr * 1.05))
    for i in range(29):
        a = math.pi * i / 28
        shell.append((cx + bw * math.cos(a), cy + bh * 0.62 * math.sin(a)))
    dr.polygon(shell, fill=K, outline=P)
    # segment lines and the pitted texture across the back
    for i in range(1, 3):
        f = i / 5
        arc = [(cx - bw * (1 - 0.16 * i) * math.cos(math.pi * j / 20),
                cy - bh * (1 - 0.17 * i) * math.sin(math.pi * j / 20) * 1.05)
               for j in range(21)]
        dr.line(arc, fill=P, width=1)
    for _ in range(int(150 * s)):
        a = pr.uniform(0.15, math.pi - 0.15)
        rr = 0.45 + 0.5 * pr.random()
        px = cx - bw * math.cos(a) * rr
        py = cy - bh * math.sin(a) * rr * 1.05
        dr.point((px, py), fill=R)
    # eyes on stalks, and the mouth-parts working
    for side in (-1, 1):
        ex = cx + side * bw * 0.30
        ey = cy - bh * 1.05
        dr.line([ex, cy - bh * 0.55, ex + side * 5 * s, ey], fill=K, width=max(2, int(4 * s)))
        dr.line([ex, cy - bh * 0.55, ex + side * 5 * s, ey], fill=P, width=1)
        dr.ellipse([ex + side * 5 * s - 6 * s, ey - 6 * s, ex + side * 5 * s + 6 * s, ey + 6 * s],
                   fill=R, outline=P)
    for i in range(4):
        mx = cx - bw * 0.22 + i * bw * 0.145
        dr.line([mx, cy + bh * 0.30, mx + 3 * s, cy + bh * 0.62], fill=K, width=max(2, int(3 * s)))
    if claws:
        for side in (-1, 1):
            ax, ay = cx + side * bw * 0.86, cy + bh * 0.18
            bx2, by2 = ax + side * 46 * s, ay - 30 * s
            dr.line([ax, ay, bx2, by2], fill=K, width=max(4, int(9 * s)))
            dr.line([ax, ay - 1, bx2, by2 - 1], fill=P, width=1)
            tipx, tipy = bx2 + side * 34 * s, by2 - 10 * s
            dr.polygon([(bx2, by2 - 11 * s), (tipx, tipy - 5 * s), (tipx + side * 5 * s, tipy + 3 * s),
                        (bx2, by2 + 4 * s)], fill=K, outline=P)
            dr.polygon([(bx2, by2 + 4 * s), (tipx + side * 3 * s, tipy + 12 * s),
                        (bx2 - side * 4 * s, by2 + 13 * s)], fill=K)


crab(268, 470, 0.86, seed=7)
crab(356, 430, 0.30, seed=19, claws=False)


# ------------------------------------------- the machine, and the man on it
def machine(cx, base, s):
    disc_r = 42 * s
    dcx, dcy = cx - 6 * s, base - 64 * s
    dr.ellipse([dcx - disc_r, dcy - disc_r, dcx + disc_r, dcy + disc_r], fill=K, outline=P)
    for i in range(14):
        a = 2 * math.pi * i / 14
        dr.line([dcx, dcy, dcx + disc_r * math.cos(a), dcy + disc_r * math.sin(a)], fill=P, width=1)
    dr.ellipse([dcx - 9 * s, dcy - 9 * s, dcx + 9 * s, dcy + 9 * s], fill=K, outline=P)
    # a glint where the light catches the rim
    dr.arc([dcx - disc_r, dcy - disc_r, dcx + disc_r, dcy + disc_r], 195, 285, fill=P, width=3)
    # frame and saddle
    dr.polygon([(cx - 40 * s, base), (cx + 40 * s, base), (cx + 30 * s, base - 14 * s),
                (cx - 30 * s, base - 14 * s)], fill=K)
    for dx in (-30, -8, 14, 34):
        dr.line([cx + dx * s, base - 12 * s, cx + dx * s, base - 44 * s], fill=K, width=max(3, int(6 * s)))
    dr.polygon([(cx - 26 * s, base - 44 * s), (cx + 22 * s, base - 44 * s),
                (cx + 18 * s, base - 54 * s), (cx - 22 * s, base - 54 * s)], fill=K)
    dr.line([cx - 26 * s, base - 44 * s, cx + 22 * s, base - 44 * s], fill=P, width=1)
    # the Time Traveller, sitting, looking at the sun
    hx, hy = cx + 2 * s, base - 54 * s
    dr.polygon([(hx - 15 * s, hy), (hx + 13 * s, hy), (hx + 10 * s, hy - 36 * s),
                (hx - 10 * s, hy - 34 * s)], fill=K)
    dr.ellipse([hx + 2 * s - 9 * s, hy - 52 * s, hx + 2 * s + 9 * s, hy - 34 * s], fill=K)
    dr.line([hx + 10 * s, hy - 34 * s, hx + 11 * s, hy], fill=P, width=1)
    dr.arc([hx + 2 * s - 9 * s, hy - 52 * s, hx + 2 * s + 9 * s, hy - 34 * s], 300, 40, fill=P, width=1)
    dr.line([hx - 10 * s, hy - 26 * s, hx + 26 * s, hy - 18 * s], fill=K, width=max(3, int(6 * s)))


machine(88, 486, 0.84)

# ------------------------------------------------------------- the words
def font(sz, bold=False):
    path = ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
    return ImageFont.truetype(path, sz)


def centred(y, s, f, fill):
    w = dr.textlength(s, font=f)
    dr.text(((W - w) / 2, y), s, font=f, fill=fill)


dr.rectangle([0, 546, W, 600], fill=K)
dr.line([18, 551, W - 18, 551], fill=P, width=2)
centred(557, "THE FURTHER VISION", font(17, bold=True), P)
centred(579, "Thirty million years hence · THE TIME MACHINE, 1895", font(10), R)

# a plain rule round the edge, so the black has a limit
dr.rectangle([3, 3, W - 4, H - 4], outline=P, width=2)

# PIL antialiases truetype text and nothing else, so the only soft pixels in the
# whole image are the letter edges; unmix them back onto the three inks.
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plate import snap as _snap, K as _K, P as _P, R as _R

_snap(base, [_K, _P, _R]).save(os.environ.get("OUT_RAW", "5.png"))
