"""2. Midday — The Station. Luna 3 as an engineering plate: half skin, half cutaway."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from common import *

rng = np.random.default_rng(3)
ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
img = np.full((H, W, 3), 255, np.uint8)
# graph paper: blue dots at every 10px, full rules every 50px
img[(ys % 10 == 0) & (xs % 10 == 0)] = INK["B"]
img[(ys % 50 == 0) & (xs % 3 == 0)] = INK["B"]
img[(xs % 50 == 0) & (ys % 3 == 0)] = INK["B"]
img[470:, :256] = INK["W"]

CX = 128
T0, C0, C1, B1 = 118, 176, 340, 392   # top of dome, cylinder top/bottom, bottom of dome
R = 52

def body_r(y):
    y = np.asarray(y, np.float32)
    top = R * np.sqrt(np.clip(1 - ((C0 - y) / (C0 - T0)) ** 2, 0, 1))
    bot = R * np.sqrt(np.clip(1 - ((y - C1) / (B1 - C1)) ** 2, 0, 1))
    return np.where(y < C0, top, np.where(y > C1, bot, R))

# clear the paper behind the station
rr = body_r(ys)
inside = (np.abs(xs - CX) < rr + 3) & (ys > T0 - 3) & (ys < B1 + 3)
img[inside] = INK["W"]
# exterior (left half): polished shell, lit from upper right; blue/white screened
u = (xs - CX) / np.maximum(rr, 0.01)
m_ext = (u < 0) & (u >= -1) & (rr > 0.5)
vy = np.where(ys < C0, (ys - C0) / (C0 - T0), np.where(ys > C1, (ys - C1) / (B1 - C1), 0))
nz = np.sqrt(np.clip(1 - u * u, 0, 1))
l = np.clip(0.45 * u + 0.8 * nz - 0.35 * vy, 0, 1)
shell = ramp(l, ["K", "B", "B", "W", "W"])
img[m_ext] = shell[m_ext]
# interior (right half): warm cavity, yellow screened toward the back wall
m_int = (u >= 0) & (u <= 1) & (rr > 0.5)
cav = ramp(0.25 + 0.35 * u, ["W", "Y", "Y"])
img[m_int] = cav[m_int]

L = Layer()
# solar cells: two belts on the skin
for y0 in (194, 290):
    L.rect(CX - R + 1, y0 - 2, CX - 2, y0 + 30, "K")
    for row in range(4):
        for x0 in range(int(CX - R + 3), int(CX - 4), 6):
            L.rect(x0, y0 + row * 7, x0 + 4.6, y0 + row * 7 + 5.4, "B")
            L.line([(x0 + 0.6, y0 + row * 7 + 1), (x0 + 3.6, y0 + row * 7 + 1)], "W", 0.5)
# thermal shutters: louvres between the belts
for k in range(11):
    uu = -0.95 + k * 0.085
    x = CX + R * math.sin(uu * math.pi / 2)
    L.rect(x, 232, x + 2.2, 282, "K")
    L.line([(x + 2.2, 232), (x + 2.2, 282)], "Y", 0.6)
L.rect(CX - R, 229, CX, 232, "K"); L.rect(CX - R, 282, CX, 285, "K")
# flanges
for y in (C0, C1):
    L.rect(CX - R - 7, y - 3, CX + R + 7, y + 3, "B", "K", 1)
    for x in range(int(CX - R - 4), int(CX + R + 6), 6):
        L.ellipse(x, y, 0.9, 0.9, "W")
# shell outline and the cut wall (right half), as a double line
pts_out = [(CX + float(body_r(y)), y) for y in np.linspace(T0, B1, 120)]
pts_in = [(CX + max(0.0, float(body_r(y)) - 5), y) for y in np.linspace(T0 + 4, B1 - 4, 120)]
L.line(pts_out, "K", 1.6); L.line(pts_in, "K", 1.0)
for i in range(0, 118, 3):
    (xa, ya), (xb, yb) = pts_out[i], pts_in[min(i + 2, 119)]
    L.line([(xa, ya), (xb, yb)], "R", 0.5)
pts_left = [(CX - float(body_r(y)), y) for y in np.linspace(T0, B1, 120)]
L.line(pts_left, "K", 1.6)
# the cut plane
L.line([(CX, T0 - 2), (CX, B1 + 2)], "K", 1.4)

# ---- components (right half)
# 1 photo window and its lid, hinged open
L.rect(CX + 2, T0 - 2, CX + 30, T0 + 3, "K")
L.poly([(CX + 30, T0 + 1), (CX + 33, T0 - 2), (CX + 54, T0 - 26), (CX + 50, T0 - 28)], "R", "K", 0.8)
# 2 camera: two lens barrels looking up through the window
for lx, lw, top in ((CX + 9, 7, T0 + 4), (CX + 22, 9, T0 + 4)):
    L.rect(lx - lw / 2, top, lx + lw / 2, 160, "R", "K", 0.8)
    for yy in range(int(top) + 3, 160, 5):
        L.line([(lx - lw / 2, yy), (lx + lw / 2, yy)], "K", 0.5)
    L.ellipse(lx, top + 1, lw / 2, 1.5, "B", "K", 0.5)
L.rect(CX + 3, 158, CX + 38, 172, "K")
L.rect(CX + 5, 160, CX + 36, 170, "R", "K", 0.5)
L.ellipse(CX + 32, 165, 3, 3, "Y", "K", 0.5)
# 3 film magazine: two spools and the film path
L.rect(CX + 4, 182, CX + 44, 208, "Y", "K", 1)
for sx in (CX + 14, CX + 34):
    L.ellipse(sx, 195, 8, 8, "W", "K", 0.8); L.ellipse(sx, 195, 4, 4, "K"); L.ellipse(sx, 195, 1.4, 1.4, "Y")
L.line([(CX + 14, 187), (CX + 34, 187)], "K", 0.6)
L.line([(CX + 34, 203), (CX + 40, 214), (CX + 40, 222)], "K", 0.8)
# 4 processing: developer-fixer, a heated bath, film snaking through
L.rect(CX + 4, 214, CX + 44, 240, "G", "K", 1)
for k in range(4):
    yy = 219 + k * 5
    L.line([(CX + 8 + j, yy + 1.5 * math.sin(j / 2.5)) for j in range(33)], "W", 0.6)
pts = []
for k in range(7):
    x = CX + 10 + k * 5
    pts += [(x, 216), (x + 2.5, 238)]
L.line(pts, "K", 0.6)
# 5 scanner: CRT lying on its side, beam through the film to 6 the photomultiplier
L.poly([(CX + 4, 248), (CX + 14, 248), (CX + 30, 244), (CX + 30, 264), (CX + 14, 260), (CX + 4, 260)], "G", "K", 0.8)
L.ellipse(CX + 30, 254, 3, 10, "W", "K", 0.6)
L.line([(CX + 33, 254), (CX + 41, 254)], "Y", 1.2)
L.rect(CX + 38, 246, CX + 40, 262, "K")
L.rect(CX + 41, 247, CX + 47, 261, "R", "K", 0.6)
# 7 transmitter: finned box, valves
L.rect(CX + 4, 270, CX + 46, 298, "B", "K", 1)
for x in range(int(CX + 8), int(CX + 44), 4):
    L.line([(x, 272), (x, 284)], "W", 0.7)
for x in (CX + 12, CX + 22, CX + 32):
    L.ellipse(x, 291, 3, 3.6, "Y", "K", 0.6)
# 8 batteries: silver-zinc cells in a stack
for row in range(3):
    for k in range(4):
        x0 = CX + 4 + k * 11; y0 = 304 + row * 11
        L.rect(x0, y0, x0 + 10, y0 + 10, "R" if (row + k) % 2 else "K", "K", 0.6)
        L.rect(x0 + 3, y0 - 1.4, x0 + 7, y0, "K")
# wiring harness
L.line([(CX + 48, 168), (CX + 48, 340)], "K", 0.8)
for y in (170, 195, 226, 254, 284, 318):
    L.line([(CX + 44, y), (CX + 48, y)], "K", 0.6)
# 9 circulation fan in the lower dome
L.ellipse(CX + 18, 358, 11, 11, "W", "K", 1)
for a in range(0, 360, 45):
    ar = math.radians(a)
    L.poly([(CX + 18, 358), (CX + 18 + 10 * math.cos(ar), 358 + 10 * math.sin(ar)),
            (CX + 18 + 10 * math.cos(ar + 0.45), 358 + 10 * math.sin(ar + 0.45))], "B")
L.ellipse(CX + 18, 358, 2, 2, "K")
# 10 nitrogen spheres for the attitude jets, and a nozzle out the bottom
L.ellipse(CX + 38, 358, 6.5, 6.5, "G", "K", 0.8); L.ellipse(CX + 36, 356, 1.6, 1.6, "W")
L.ellipse(CX + 12, 378, 5, 5, "G", "K", 0.8); L.ellipse(CX + 10.5, 376.5, 1.2, 1.2, "W")
L.line([(CX + 38, 365), (CX + 30, 386), (CX + 30, 398)], "K", 0.8)
L.poly([(CX + 27, 396), (CX + 33, 396), (CX + 35, 402), (CX + 25, 402)], "K")
# sensors on the dome: sun sensor (photocell) that started the sequence
L.rect(CX - 34, 128, CX - 22, 136, "Y", "K", 0.8); L.ellipse(CX - 28, 130, 2.5, 2.5, "K")
# antennas: four whips up, two down
for (x0, y0), (x1, y1) in [((CX - 40, 140), (CX - 102, 84)), ((CX - 18, 124), (CX - 46, 66)),
                           ((CX + 40, 140), (CX + 96, 92)), ((CX + 18, 124), (CX + 30, 70)),
                           ((CX - 36, 384), (CX - 92, 440)), ((CX + 36, 384), (CX + 80, 442))]:
    L.line([(x0, y0), (x1, y1)], "K", 1.3)
    L.ellipse(x0, y0, 2.2, 2.2, "K"); L.ellipse(x1, y1, 1.4, 1.4, "R")
# axis of symmetry, dash-dot red
y = 56
while y < 452:
    L.line([(CX, y), (CX, min(y + 9, 452))], "R", 0.7); y += 13
    if y < 452: L.ellipse(CX, y - 2, 0.6, 0.6, "R")
# dimension lines
L.line([(CX - R, 456), (CX + R, 456)], "K", 0.6)
for x in (CX - R, CX + R): L.line([(x, 452), (x, 460)], "K", 0.6)
L.poly([(CX - R, 456), (CX - R + 5, 454), (CX - R + 5, 458)], "K"); L.poly([(CX + R, 456), (CX + R - 5, 454), (CX + R - 5, 458)], "K")
L.text((CX, 452), "Ø 950", "K", 9, "monob", "md")

# callouts
calls = [  # n, target, bubble
    (1, (CX + 18, T0), (232, 96)), (2, (CX + 22, 140), (232, 124)), (3, (CX + 34, 195), (232, 182)),
    (4, (CX + 30, 228), (232, 214)), (5, (CX + 20, 254), (232, 240)), (6, (CX + 44, 254), (232, 262)),
    (7, (CX + 30, 284), (232, 288)), (8, (CX + 30, 320), (232, 318)), (9, (CX + 18, 358), (232, 346)),
    (10, (CX + 38, 358), (232, 372)), (11, (CX - 30, 206), (24, 200)), (12, (CX - 30, 258), (24, 256)),
    (13, (CX - 46, 66), (24, 100)), (14, (CX - 28, 132), (24, 140)),
]
for n, (tx, ty), (bx, by) in calls:
    L.line([(tx, ty), (bx + (-8 if bx > CX else 8), by)], "K", 0.6)
    L.ellipse(tx, ty, 1.5, 1.5, "K")
    L.ellipse(bx, by, 8, 8, "W", "K", 1.0)
    L.text((bx, by + 0.5), str(n), "R", 10, "sansb", "mm")

# title block
L.rect(8, 8, 392, 48, "K")
L.text((16, 12), "ЛУНА-3", "Y", 26, "serifb")
L.text((156, 15), "AUTOMATIC INTERPLANETARY", "W", 10, "sansb")
L.text((156, 28), "STATION · SECTION A–A · 1959", "W", 10, "sansb")
L.rect(352, 13, 386, 43, "R"); L.text((369, 28), "E-2A", "W", 9, "monob", "mm")

# ---- inset A: the trajectory, a figure of eight around the Moon
ix0, iy0, ix1, iy1 = 262, 60, 392, 236
L.rect(ix0, iy0, ix1, iy1, "W", "B", 1.4)
L.rect(ix0 + 3, iy0 + 3, ix1 - 3, iy1 - 3, None, "B", 0.5)
ex, ey = 327, 206; mxm, mym = 330, 96
# sun from above: rays
for k in range(9):
    x = ix0 + 14 + k * 13
    L.line([(x, iy0 + 8), (x, iy0 + 20)], "Y", 1.2)
    L.poly([(x - 2.5, iy0 + 19), (x + 2.5, iy0 + 19), (x, iy0 + 24)], "Y")
path = []
for k in range(220):
    s = k / 219 * 2 * math.pi * 0.98 + 0.15
    x = 327 + 30 * math.sin(2 * s) * (1 - 0.15 * math.cos(s))
    y = 151 - 60 * math.cos(s)
    path.append((x, y))
for i in range(0, len(path) - 1, 2):
    L.line([path[i], path[i + 1]], "R", 1.0)
L.ellipse(ex, ey, 11, 11, "B", "K", 0.8)
L.poly([(ex - 6, ey - 4), (ex + 2, ey - 8), (ex + 5, ey - 1), (ex - 2, ey + 4)], "G")
L.ellipse(mxm, mym, 6, 6, "W", "K", 0.8)
L.arc(mxm, mym, 5, 180, 360, "Y", 2.4)
for (x, y, s, a) in [(path[30][0], path[30][1], "4.X", "lm"), (path[95][0], path[95][1], "7.X 03:30", "rm"),
                     (path[150][0], path[150][1], "10.X", "lm"), (path[205][0], path[205][1], "18.X", "rm")]:
    L.ellipse(x, y, 2.2, 2.2, "K")
    L.text((x + (5 if a == "lm" else -5), y), s, "K", 9, "monob", a)
L.text((ix0 + 7, iy1 - 8), "ТРАЕКТОРИЯ", "B", 9, "sansb", "ls")

# ---- inset B: the film, 35 mm, three frames of the far side
fx0, fy0, fx1, fy1 = 262, 250, 392, 438
L.rect(fx0, fy0, fx1, fy1, "K")
for y in range(fy0 + 4, fy1 - 4, 9):
    L.rect(fx0 + 5, y, fx0 + 11, y + 5, "W"); L.rect(fx1 - 11, y, fx1 - 5, y + 5, "W")
for k in range(3):
    y0 = fy0 + 8 + k * 60
    L.rect(fx0 + 18, y0, fx1 - 18, y0 + 52, "B")
    L.text((fx0 + 21, y0 + 2), str(24 + k), "Y", 8, "monob")
img = L.onto(img)
# fill frames with tiny dithered far-side discs
for k in range(3):
    y0 = fy0 + 8 + k * 60
    cxk, cyk, rk = (fx0 + fx1) / 2 + (k - 1) * 4, y0 + 27, 21 + k
    d = np.hypot(xs - cxk, ys - cyk)
    mm = d < rk
    nzz = np.sqrt(np.clip(1 - (d / rk) ** 2, 0, 1))
    tex = 0.15 + 0.85 * nzz ** 0.6 - 0.5 * (np.hypot(xs - cxk + 6, ys - cyk + 7) < 6) - 0.4 * (np.hypot(xs - cxk - 5, ys - cyk - 9) < 4)
    tex -= 0.18 * (np.sin(xs * 0.9 + k) * np.sin(ys * 0.8) > 0.55)
    disc = ramp(np.clip(tex, 0, 1), ["K", "B", "W", "W"])
    img[mm] = disc[mm]

L2 = Layer()
L2.text((fx0, fy1 + 12), "29 EXPOSED", "K", 10, "monob")
L2.text((fx0, fy1 + 24), "17 RECEIVED", "R", 10, "monob")
# legend
items = ["Photo window & lid", "Camera, 200/500 mm", "Film, 40 frames", "Develop · fix · dry",
         "CRT flying-spot scan", "Photomultiplier", "Radio, 183.6 MHz",
         "Silver-zinc cells", "Circulation fan", "Nitrogen jets", "Solar cells", "Thermal shutters",
         "Whip antennas", "Sun sensor"]
L2.line([(8, 476), (256, 476)], "K", 1.2)
for i, s in enumerate(items):
    col, row = divmod(i, 7)
    x = 8 + col * 128; y = 485 + row * 15.5
    L2.ellipse(x + 6, y + 6, 6.2, 6.2, "R")
    L2.text((x + 6, y + 6.4), str(i + 1), "W", 8, "sansb", "mm")
    L2.text((x + 15, y), s, "K", 10, "sans")
L2.rect(262, 506, 392, 592, "R")
L2.text((327, 520), "7 OCTOBER 1959", "W", 11, "sansb", "mm")
L2.text((327, 540), "03:30 UT", "Y", 19, "monob", "mm")
L2.text((327, 562), "the camera opens", "W", 10, "sans", "mm")
L2.text((327, 577), "63 500 km out", "W", 10, "sans", "mm")
img = L2.onto(img)
save(img)
