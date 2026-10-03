"""Piano Phase (1967): the twelve-note pattern, one ring per phase step, over two nested pianos."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ink import *

c = Canvas(Wh)
yy, xx = np.mgrid[0:H, 0:W]
# morning light: a yellow wash from the top that thins out
c.paste_mask(mix(Wh, Y, np.clip(1 - yy / 330, 0, 1) ** 1.6 * 0.55), yy < 600)

# --- the phase wheel -------------------------------------------------------
NOTES = ["E", "F#", "B", "C#", "D", "F#", "E", "C#", "B", "F#", "D", "C#"]
COL = {"E": R, "F#": B, "B": G, "C#": K, "D": Y}
cx, cy = 200, 222
r0, r1 = 46, 176
c.ellipse(cx, cy, r1 + 14, r1 + 14, fill=Wh, outline=K, width=1.5)
c.ellipse(cx, cy, r1 + 3, r1 + 3, outline=K, width=0.8)
rings = 12
dr = (r1 - r0) / rings

def sector(rin, rout, a0, a1, fill):
    n = 10
    pts = [(cx + rout * math.cos(a0 + (a1 - a0) * i / n), cy + rout * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    pts += [(cx + rin * math.cos(a1 - (a1 - a0) * i / n), cy + rin * math.sin(a1 - (a1 - a0) * i / n)) for i in range(n + 1)]
    c.poly(pts, fill=fill)

step = 2 * math.pi / 12
for k in range(rings):           # k = how far pianist two has drifted ahead
    rin, rout = r0 + k * dr, r0 + (k + 1) * dr
    mid = (rin + rout) / 2
    for i in range(12):
        a0 = -math.pi / 2 + i * step + 0.012
        a1 = a0 + step - 0.024
        n1, n2 = NOTES[i], NOTES[(i + k) % 12]
        if n1 == n2:
            sector(rin + 0.6, rout - 0.6, a0, a1, COL[n1])
        else:  # outer half: first piano; inner half: second piano
            sector(mid, rout - 0.6, a0, a1, COL[n1])
            sector(rin + 0.6, mid, a0, a1, COL[n2])
        if COL[n1] == Y or COL[n2] == Y:  # yellow needs a keyline on white
            pass
    c.ellipse(cx, cy, rout, rout, outline=K, width=0.5)

# spokes and rim ticks
for i in range(12):
    a = -math.pi / 2 + i * step
    c.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + (r1 + 3) * math.cos(a), cy + (r1 + 3) * math.sin(a))], K, 0.8)
for i in range(96):
    a = -math.pi / 2 + i * step / 8
    L = 6 if i % 8 == 0 else (3.5 if i % 4 == 0 else 2)
    c.line([(cx + (r1 + 3) * math.cos(a), cy + (r1 + 3) * math.sin(a)),
            (cx + (r1 + 3 + L) * math.cos(a), cy + (r1 + 3 + L) * math.sin(a))], K, 0.7)
# note names round the rim
for i, n in enumerate(NOTES):
    a = -math.pi / 2 + (i + 0.5) * step
    rr = r1 + 9.5
    c.text((cx + rr * math.cos(a), cy + rr * math.sin(a)), n, K, 7, anchor="mm")
# hub: the unison, a small sun
c.ellipse(cx, cy, r0 - 2, r0 - 2, fill=Y, outline=K, width=1)
for i in range(24):
    a = i * math.pi / 12
    c.line([(cx + 12 * math.cos(a), cy + 12 * math.sin(a)), (cx + (r0 - 7) * math.cos(a), cy + (r0 - 7) * math.sin(a))], R if i % 2 else K, 1.2 if i % 2 else 0.6)
c.ellipse(cx, cy, 11, 11, fill=R, outline=K, width=0.8)
c.text((cx, cy + 0.5), "12", Wh, 8.5, anchor="mm")

# legend in the corners
for j, (n, col) in enumerate([("E", R), ("F#", B), ("B", G), ("C#", K), ("D", Y)]):
    x = 16 + j * 20
    c.rect(x, 14, x + 11, 25, fill=col, outline=K, width=0.6)
    c.text((x + 5.5, 33), n, K, 6.5, anchor="mt")
c.text((384, 14), "PIANO PHASE", K, 10, anchor="ra")
c.text((384, 27), "1967 · two pianos, one pattern", K, 6.5, anchor="ra")

# --- two grand pianos, nested head to tail ----------------------------------
def grand(x0, y0, flip):
    """Top-down grand piano, keyboard on the left (or right if flip), lid open-ish."""
    L, Wd = 250, 86
    def X(x): return x0 - x if flip else x0 + x
    # case outline: straight spine top, curved bent side bottom, tail rounded
    pts = [(X(0), y0), (X(L * 0.72), y0)]
    for i in range(21):  # tail curve
        t = i / 20
        a = -math.pi / 2 + t * math.pi
        pts.append((X(L * 0.72 + (L * 0.28) * math.cos(a) * 0.9), y0 + Wd * 0.22 + Wd * 0.22 * math.sin(a)))
    for i in range(21):  # the S-shaped bent side
        t = i / 20
        x = L * 0.66 * (1 - t)
        y = Wd * 0.44 + (Wd - Wd * 0.44) * (0.5 - 0.5 * math.cos(math.pi * t))
        pts.append((X(x + 6), y0 + y))
    pts.append((X(0), y0 + Wd))
    c.poly(pts, fill=K, outline=K, width=1)
    # inner rim and the iron plate (gold)
    inner = [(X(px if not flip else x0 - px), py) for px, py in []]
    plate = []
    for (px, py) in pts:
        rx = (px - x0) if not flip else (x0 - px)
        plate.append((X(14 + (rx - 0) * 0.93), y0 + 6 + (py - y0) * 0.86))
    c.poly(plate[2:-1] + [(X(30), y0 + Wd - 8), (X(30), y0 + 6)], fill=Y)
    # strings: fan from keyboard end towards tail, cut by plate struts
    for s in range(34):
        f = s / 33
        ya = y0 + 9 + f * (Wd - 20)
        xb = L * (0.95 - 0.55 * f)
        c.line([(X(34), ya), (X(max(40, xb - 18)), y0 + 9 + f * (Wd * 0.8) * (1 - 0.25 * f))], K, 0.45)
    # plate holes (the famous round openings)
    for hx, hy, hr in [(95, 0.55, 7), (135, 0.42, 6), (172, 0.32, 5)]:
        c.ellipse(X(hx), y0 + Wd * hy, hr, hr, fill=K, outline=K)
        c.ellipse(X(hx), y0 + Wd * hy, hr - 2, hr - 2, fill=Y)
    # struts
    for sx in [70, 120, 165]:
        c.line([(X(30), y0 + 8), (X(sx), y0 + Wd * 0.75 - sx * 0.12)], R, 1.3)
    # keyboard block
    kx0, kx1 = X(-22), X(4)
    c.rect(min(kx0, kx1), y0 - 4, max(kx0, kx1), y0 + Wd + 4, fill=K)
    keys = 30
    kh = (Wd + 2) / keys
    for i in range(keys):
        ky = y0 - 2 + i * kh
        c.rect(min(X(-20), X(2)), ky + 0.3, max(X(-20), X(2)), ky + kh - 0.3, fill=Wh)
    for i in range(keys - 1):
        if i % 7 in (2, 6):
            continue
        ky = y0 - 2 + (i + 1) * kh
        c.rect(min(X(-8), X(2)), ky - kh * 0.32, max(X(-8), X(2)), ky + kh * 0.32, fill=K)
    # bench and player (top-down: shoulders, head, hands on keys)
    bx = X(-44)
    c.rect(min(bx - 9, bx + 9), y0 + Wd * 0.2, max(bx - 9, bx + 9), y0 + Wd * 0.8, fill=R, outline=K, width=0.8)
    c.ellipse(bx, y0 + Wd / 2, 11, 25, fill=B, outline=K, width=0.8)  # shoulders
    for side in (-1, 1):
        c.line([(bx, y0 + Wd / 2 + side * 16), (X(-12), y0 + Wd / 2 + side * 13)], B, 4)
        c.ellipse(X(-12), y0 + Wd / 2 + side * 13, 3, 3, fill=Wh, outline=K, width=0.6)
    c.ellipse(bx, y0 + Wd / 2, 7.5, 7.5, fill=K)

grand(70, 412, False)
grand(330, 492, True)

# floor marks: score pages scattered between
for (x, y, a) in [(330, 425, 0.2), (352, 438, -0.15), (40, 560, 0.1)]:
    pts = [(-11, -8), (11, -8), (11, 8), (-11, 8)]
    pp = [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts]
    c.poly(pp, fill=Wh, outline=K, width=0.6)
    for l in range(5):
        yy0 = -5 + l * 2.5
        c.line([(x + (-8) * math.cos(a) - yy0 * math.sin(a), y + (-8) * math.sin(a) + yy0 * math.cos(a)),
                (x + 8 * math.cos(a) - yy0 * math.sin(a), y + 8 * math.sin(a) + yy0 * math.cos(a))], K, 0.4)

c.text((200, 590), "STEVE REICH · 90 · 3 OCTOBER 2026", K, 7.5, anchor="ms")
c.save()
