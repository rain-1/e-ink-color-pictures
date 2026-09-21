#!/usr/bin/env python3
"""10 — THE ISLAND OF DOCTOR MOREAU (1896): a chart of Noble's Isle.

Midday is when a survey party goes ashore and starts measuring, so the second
plate is an Admiralty chart of an island that isn't on any Admiralty chart.
Everything in it is the vocabulary of 19th-century hydrographic engraving:
the coastline repeated in four thinning offsets to make the water ring, cliff
hachures, contour rings, depth soundings, a sixteen-point rose, rhumb lines,
a graduated border, a scale of miles, a cartouche, and a section cut through
the ravine. The land is the one flat colour; everything else is line.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plate import Plate, K, P, R, Y, G, poly

p = Plate(bg=P)
rnd = random.Random(1866)

M = 14                      # neat line
CX, CY = 194, 300           # island centre
N = 360


def radius(t):
    """Polar coastline: a broad south, a western spit, a bay in the east."""
    return 118 * (1
                  + 0.150 * math.sin(3 * t + 1.05)
                  + 0.095 * math.sin(5 * t + 0.35)
                  + 0.055 * math.sin(7 * t + 2.20)
                  + 0.035 * math.sin(11 * t + 0.90)
                  - 0.130 * math.exp(-((math.sin((t - 1.15) / 2)) ** 2) * 26)   # the east bay
                  + 0.105 * math.exp(-((math.sin((t - 3.35) / 2)) ** 2) * 40))  # the west spit


def coast(scale=0.0):
    pts = []
    for i in range(N):
        t = 2 * math.pi * i / N
        r = radius(t) + scale
        pts.append((CX + r * math.cos(t), CY + r * math.sin(t) * 1.06))
    return pts


COAST = coast()
COAST_D = poly(COAST)

# ------------------------------------------------------------------ the sea
sea = p.clip_rect(M + 4, M + 4, 400 - 2 * (M + 4), 600 - 2 * (M + 4))
land_clip = p.clip(COAST_D)

# rhumb lines from a hidden centre, the way a portolan rules the water
RCX, RCY = 316, 168
p.add(f'<g clip-path="url(#{sea})" stroke="{K}" stroke-width="0.9">')
for i in range(16):
    a = 2 * math.pi * i / 16
    p.add(f'<line x1="{RCX}" y1="{RCY}" x2="{RCX+620*math.cos(a):.1f}" y2="{RCY+620*math.sin(a):.1f}"/>')
p.add('</g>')

# the water ring: the coastline redrawn outward, thinner each time
for i, (off, sw) in enumerate(((6, 1.5), (12, 1.2), (19, 1.0), (27, 0.85), (37, 0.75))):
    p.add(f'<g clip-path="url(#{sea})"><path d="{poly(coast(off))}" fill="none" stroke="{K}" '
          f'stroke-width="{sw}"/></g>')

# soundings
p.add(f'<g clip-path="url(#{sea})">')
for _ in range(150):
    x = rnd.uniform(M + 8, 400 - M - 8)
    y = rnd.uniform(M + 8, 600 - M - 8)
    t = math.atan2((y - CY) / 1.06, x - CX)
    d = math.hypot(x - CX, (y - CY) / 1.06)
    if d < radius(t) + 44:
        continue
    depth = int(6 + (d - radius(t)) * 0.42 + rnd.uniform(-3, 3))
    p.add(f'<text x="{x:.0f}" y="{y:.0f}" font-family="Liberation Serif, serif" '
          f'font-size="8.4" fill="{K}">{depth}</text>')
p.add('</g>')

# the reef, east of the bay: stipple and a dashed danger line
reef = [(CX + (radius(t) + 30 + 16 * math.sin(t * 9)) * math.cos(t),
         CY + (radius(t) + 30 + 16 * math.sin(t * 9)) * math.sin(t) * 1.06)
        for t in [0.55 + i * 0.035 for i in range(26)]]
p.add(f'<path d="M ' + " L ".join(f"{x:.1f},{y:.1f}" for x, y in reef) +
      f'" fill="none" stroke="{K}" stroke-width="1.3" stroke-dasharray="5 3"/>')
for (x, y) in reef[::2]:
    for _ in range(4):
        p.add(f'<circle cx="{x+rnd.uniform(-7,7):.1f}" cy="{y+rnd.uniform(-7,7):.1f}" '
              f'r="{rnd.uniform(0.8,1.6):.1f}" fill="{K}"/>')

# ----------------------------------------------------------------- the land
p.add(f'<path d="{COAST_D}" fill="{G}" stroke="{K}" stroke-width="2.8"/>')

# cliff hachures on the weather side (south-west)
p.add(f'<g clip-path="url(#{land_clip})" stroke="{K}">')
for i in range(N):
    t = 2 * math.pi * i / N
    if not (1.9 < t < 4.5):
        continue
    r = radius(t)
    x0, y0 = CX + r * math.cos(t), CY + r * math.sin(t) * 1.06
    L = 7 + 7 * math.sin(i * 0.6)
    p.add(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0-L*math.cos(t):.1f}" '
          f'y2="{y0-L*math.sin(t)*1.06:.1f}" stroke-width="{1.0 if i%2 else 1.6}"/>')
p.add('</g>')

# contours climbing to the central peak
PKX, PKY = 186, 268
for k, rr in enumerate((96, 80, 64, 50, 37, 26, 17, 10)):
    pts = []
    for i in range(140):
        t = 2 * math.pi * i / 140
        rad = rr * (1 + 0.18 * math.sin(3 * t + 0.6 + k * 0.3) + 0.10 * math.sin(5 * t + k))
        pts.append((PKX + rad * math.cos(t), PKY + rad * math.sin(t) * 0.80))
    p.add(f'<g clip-path="url(#{land_clip})"><path d="{poly(pts)}" fill="none" stroke="{K}" '
          f'stroke-width="{1.0 if k % 2 else 1.4}"/></g>')
p.add(f'<circle cx="{PKX}" cy="{PKY}" r="3.4" fill="{K}"/>')
p.add(f'<rect x="{PKX+5}" y="{PKY-11}" width="44" height="10" fill="{P}"/>')
p.text(PKX + 7, PKY - 4, "1,142 ft.", size=8.6)

# the ravine: a barbed line running south-east off the peak
rav = [(PKX + 8, PKY + 14), (204, 310), (222, 342), (236, 378), (232, 408)]
p.add(f'<path d="M ' + " L ".join(f"{x},{y}" for x, y in rav) +
      f'" fill="none" stroke="{K}" stroke-width="2.4"/>')
for i in range(len(rav) - 1):
    x0, y0 = rav[i]; x1, y1 = rav[i + 1]
    seg = math.hypot(x1 - x0, y1 - y0)
    for s in range(int(seg / 7)):
        t = (s + 0.5) / (seg / 7)
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        nx, ny = (y1 - y0) / seg, -(x1 - x0) / seg
        for sgn in (-1, 1):
            p.add(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+sgn*nx*6:.1f}" y2="{y+sgn*ny*6:.1f}" '
                  f'stroke="{K}" stroke-width="1.1"/>')

# woodland: little engraved tree symbols scattered over the green
p.add(f'<g clip-path="url(#{land_clip})">')
for _ in range(190):
    x = rnd.uniform(CX - 150, CX + 150)
    y = rnd.uniform(CY - 140, CY + 140)
    if math.hypot(x - PKX, (y - PKY) / 0.8) < 48:
        continue
    s = rnd.uniform(2.6, 4.4)
    p.add(f'<path d="M {x:.1f} {y:.1f} l 0 {-s*1.9:.1f}" stroke="{K}" stroke-width="1.1"/>')
    p.add(f'<path d="M {x-s:.1f} {y-s*1.5:.1f} q {s:.1f} {-s*1.5:.1f} {s*2:.1f} 0" fill="none" '
          f'stroke="{K}" stroke-width="1.1"/>')
p.add('</g>')

# marsh hatching in the low ground, north-east
p.add(f'<g clip-path="url(#{land_clip})" stroke="{K}" stroke-width="1.1">')
for r in range(9):
    yy = 212 + r * 7
    for c in range(11):
        xx = 236 + c * 9 + (r % 2) * 4
        p.add(f'<line x1="{xx}" y1="{yy}" x2="{xx+6}" y2="{yy}"/>')
p.add('</g>')

# hot springs
for (sx, sy) in ((150, 350), (160, 362), (142, 364)):
    p.add(f'<circle cx="{sx}" cy="{sy}" r="4.2" fill="{Y}" stroke="{K}" stroke-width="1.4"/>')
    p.add(f'<path d="M {sx-3} {sy-7} q 3 -4 0 -8" fill="none" stroke="{K}" stroke-width="1.1"/>')
    p.add(f'<path d="M {sx+3} {sy-7} q 3 -4 0 -8" fill="none" stroke="{K}" stroke-width="1.1"/>')

# the enclosure: a walled yard with the house in it
ex, ey = 116, 296
p.add(f'<rect x="{ex-22}" y="{ey-16}" width="44" height="32" fill="{P}" stroke="{K}" stroke-width="2.2"/>')
p.add(f'<rect x="{ex-14}" y="{ey-9}" width="17" height="13" fill="{Y}" stroke="{K}" stroke-width="1.5"/>')
p.add(f'<rect x="{ex+6}" y="{ey-4}" width="11" height="9" fill="{K}"/>')
for i in range(9):
    p.add(f'<line x1="{ex-22+i*5.5}" y1="{ey+16}" x2="{ex-22+i*5.5}" y2="{ey+21}" stroke="{K}" stroke-width="1.1"/>')

# the huts of the Beast Folk, along the ravine
for (hx, hy) in ((228, 356), (240, 366), (226, 376), (244, 384), (232, 394)):
    p.add(f'<path d="{poly([(hx-6, hy+4), (hx, hy-6), (hx+6, hy+4)])}" fill="{K}"/>')

# the landing place, and the narrator's track inland, in red
p.add(f'<path d="M 268 226 L 250 250 L 232 262 L 214 280 L 196 286" fill="none" stroke="{R}" '
      f'stroke-width="2.4" stroke-dasharray="6 4"/>')
p.add(f'<path d="M 196 286 L 176 300 L 140 296" fill="none" stroke="{R}" stroke-width="2.4" '
      f'stroke-dasharray="6 4"/>')
p.add(f'<circle cx="268" cy="226" r="4.0" fill="{R}" stroke="{K}" stroke-width="1.3"/>')
# the longboat in the bay
bx, by = 292, 212
p.add(f'<path d="{poly([(bx-11, by), (bx+11, by), (bx+7, by+5), (bx-7, by+5)])}" fill="{K}"/>')
p.add(f'<line x1="{bx}" y1="{by}" x2="{bx}" y2="{by-13}" stroke="{K}" stroke-width="1.6"/>')

# ---------------------------------------------------------------- lettering
def place(x, y, s, size=9.6, anchor="start", style="italic", color=K, spacing=0.4):
    """Engraved name with the water or the wood cleared out from behind it."""
    w = len(s) * size * 0.50 + 4
    x0 = x - 2 if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w + 2)
    p.add(f'<rect x="{x0:.1f}" y="{y - size * 0.86:.1f}" width="{w:.1f}" '
          f'height="{size * 1.16:.1f}" fill="{P}"/>')
    p.text(x, y, s, size=size, anchor=anchor, style=style, color=color, spacing=spacing)

place(88, 322, "THE ENCLOSURE", size=9.4, style="normal", anchor="middle", spacing=0.8)
place(258, 344, "Huts", size=9.6)
place(250, 412, "RAVINE", size=9.4, style="normal", spacing=0.8)
place(120, 378, "Hot Springs", size=9.4)
place(258, 206, "Landing", size=9.6)
place(300, 240, "Beagle Bay", size=10.4)
place(252, 196, "Reef", size=9.6)
place(104, 232, "Cape Vulture", size=9.6)
place(140, 430, "SOUTHERN CLIFFS", size=9.4, style="normal", anchor="middle", spacing=0.8)
place(272, 288, "Cane Brake", size=9.6)

# ------------------------------------------------------------- compass rose
def rose(cx, cy, r):
    p.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{P}" stroke="{K}" stroke-width="1.6"/>')
    p.add(f'<circle cx="{cx}" cy="{cy}" r="{r*0.80:.1f}" fill="none" stroke="{K}" stroke-width="1.0"/>')
    for i in range(32):
        a = 2 * math.pi * i / 32 - math.pi / 2
        L = r if i % 8 == 0 else (r * 0.9 if i % 4 == 0 else r * 0.84)
        p.add(f'<line x1="{cx+r*0.80*math.cos(a):.1f}" y1="{cy+r*0.80*math.sin(a):.1f}" '
              f'x2="{cx+L*math.cos(a):.1f}" y2="{cy+L*math.sin(a):.1f}" stroke="{K}" '
              f'stroke-width="{1.5 if i%4==0 else 0.9}"/>')
    for i in range(8):
        a0 = 2 * math.pi * i / 8 - math.pi / 2
        a1 = a0 + math.pi / 8
        a2 = a0 - math.pi / 8
        R2 = r * 0.80 if i % 2 == 0 else r * 0.56
        tip = (cx + R2 * math.cos(a0), cy + R2 * math.sin(a0))
        for a in (a1, a2):
            d = poly([(cx, cy), tip, (cx + r * 0.18 * math.cos(a), cy + r * 0.18 * math.sin(a))])
            p.add(f'<path d="{d}" fill="{K if a is a1 else P}" stroke="{K}" stroke-width="1.1"/>')
    p.add(f'<circle cx="{cx}" cy="{cy}" r="3.0" fill="{K}"/>')
    # the north point, with a red fleur
    p.add(f'<path d="{poly([(cx, cy-r*1.16), (cx-5, cy-r*0.86), (cx+5, cy-r*0.86)])}" fill="{R}" stroke="{K}" stroke-width="1.2"/>')
    p.text(cx, cy - r * 1.26, "N", size=11, anchor="middle", weight="bold")


rose(RCX, RCY, 38)

# ------------------------------------------------------------ scale of miles
sx, sy = 40, 528
p.text(sx, sy - 7, "Scale of English Miles", size=9.2, style="italic")
for i in range(6):
    p.add(f'<rect x="{sx+i*22}" y="{sy}" width="22" height="7" fill="{K if i%2 else P}" '
          f'stroke="{K}" stroke-width="1.1"/>')
for i in range(7):
    p.add(f'<line x1="{sx+i*22}" y1="{sy+7}" x2="{sx+i*22}" y2="{sy+11}" stroke="{K}" stroke-width="1.1"/>')
    p.text(sx + i * 22, sy + 21, str(i), size=8.8, anchor="middle")

# ---------------------------------------------- section through the ravine
ix, iy, iw, ih = 224, 492, 152, 66
p.add(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="{P}" stroke="{K}" stroke-width="2.0"/>')
p.text(ix + iw / 2, iy + 13, "SECTION ON THE LINE A–B", size=8.6, anchor="middle", spacing=0.5)
prof = [(ix + 4, iy + ih - 6)]
for i in range(1, 37):
    x = ix + 4 + (iw - 8) * i / 36
    t = i / 36
    y = iy + ih - 6 - (30 * math.exp(-((t - 0.34) ** 2) * 26) + 16 * math.exp(-((t - 0.78) ** 2) * 60)
                       - 9 * math.exp(-((t - 0.56) ** 2) * 200))
    prof.append((x, y))
prof += [(ix + iw - 4, iy + ih - 6)]
p.add(f'<path d="{poly(prof)}" fill="{G}" stroke="{K}" stroke-width="1.8"/>')
p.rule_field(p.clip(poly(prof)), (ix, iy, ix + iw, iy + ih), 90, 4.2, 0.9, K)
p.add(f'<line x1="{ix+4}" y1="{iy+ih-6}" x2="{ix+iw-4}" y2="{iy+ih-6}" stroke="{K}" stroke-width="1.6"/>')
p.text(ix + 6, iy + ih - 10, "A", size=9.4, weight="bold")
p.text(ix + iw - 13, iy + ih - 10, "B", size=9.4, weight="bold")

# ------------------------------------------------------------- the cartouche
cx0, cy0, cw, ch = 26, 470, 186, 88
p.add(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" fill="{P}" stroke="{K}" stroke-width="2.4"/>')
p.add(f'<rect x="{cx0+4}" y="{cy0+4}" width="{cw-8}" height="{ch-8}" fill="none" stroke="{K}" stroke-width="1.0"/>')
p.text(cx0 + cw / 2, cy0 + 22, "NOBLE'S ISLE", size=19, anchor="middle", spacing=1.2)
p.add(f'<line x1="{cx0+28}" y1="{cy0+28}" x2="{cx0+cw-28}" y2="{cy0+28}" stroke="{K}" stroke-width="1.1"/>')
p.text(cx0 + cw / 2, cy0 + 41, "surveyed by E. Prendick, 1887", size=9.4, anchor="middle", style="italic")
p.text(cx0 + cw / 2, cy0 + 54, "lat. 5° 3′ S.  long. 101° W.", size=9.0, anchor="middle")
p.text(cx0 + cw / 2, cy0 + 70, "ARE WE NOT MEN?", size=10.4, anchor="middle", color=R,
       weight="bold", spacing=1.2)

# the title, engraved across the open water to the north
p.add(f'<rect x="30" y="28" width="340" height="48" fill="{P}"/>')
p.text(200, 46, "THE ISLAND OF DOCTOR MOREAU", size=15.6, anchor="middle", spacing=1.0)
p.add(f'<line x1="66" y1="54" x2="334" y2="54" stroke="{K}" stroke-width="1.2"/>')
p.text(200, 68, "H. G. Wells, 1896  ·  a chart of the place, compiled from the narrative",
       size=9.2, anchor="middle", style="italic")

# ------------------------------------------------------- graduated neat line
p.add(f'<rect x="{M}" y="{M}" width="{400-2*M}" height="{600-2*M}" fill="none" stroke="{K}" stroke-width="2.2"/>')
p.add(f'<rect x="{M+8}" y="{M+8}" width="{400-2*(M+8)}" height="{600-2*(M+8)}" fill="none" stroke="{K}" stroke-width="1.2"/>')
step = 14
x = M
i = 0
while x < 400 - M - 1:
    w = min(step, 400 - M - x)
    if i % 2 == 0:
        p.add(f'<rect x="{x}" y="{M+2}" width="{w}" height="6" fill="{K}"/>')
        p.add(f'<rect x="{x}" y="{600-M-8}" width="{w}" height="6" fill="{K}"/>')
    x += step; i += 1
y = M
i = 0
while y < 600 - M - 1:
    h = min(step, 600 - M - y)
    if i % 2 == 0:
        p.add(f'<rect x="{M+2}" y="{y}" width="6" height="{h}" fill="{K}"/>')
        p.add(f'<rect x="{400-M-8}" y="{y}" width="6" height="{h}" fill="{K}"/>')
    y += step; i += 1

p.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "2_midday_nobles_isle.svg"),
       names=(K, P, R, Y, G))
