"""Pendulum Music (1968): four microphones swung over four upturned speakers; each howl of
feedback as a mic passes over its speaker, until they all hang still. A strobe of the swing."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ink import *

random.seed(68)
c = Canvas(K)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# --- high window: Saturn, a night from opposition, among a few stars ---------
c.rect(262, 52, 372, 132, fill=mix(K, B, 0.18), outline=B, width=1)
c.rect(316, 52, 318, 132, fill=K)
for _ in range(26):
    sx, sy = random.uniform(266, 368), random.uniform(56, 128)
    if 314 < sx < 320:
        continue
    c.rect(sx, sy, sx + 0.6, sy + 0.6, fill=Wh)
SX, SY = 342, 84
ring = [(SX + 15 * math.cos(t), SY + 4 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 40)]
c.line(ring[20:] + [ring[0]], Y, 1)                     # far half of the rings
c.ellipse(SX, SY, 7, 7, fill=Y)
c.line([(SX - 7, SY - 1), (SX + 7, SY - 1)], K, 0.4)
c.line(ring[:21], Y, 1)                                 # near half, in front of the ball
c.text((317, 140), "SATURN · OPPOSITION 4 OCT", B, 4.6, anchor="mt")

# --- floor in perspective ---------------------------------------------------
FLOOR = 440
VPX, VPY = 200, 250
fl = (yy > FLOOR)
c.paste_mask(mix(K, B, np.clip((yy - FLOOR) / 400, 0, 0.22)), fl)
for i in range(-12, 13):
    x_far = VPX + i * 34 * (FLOOR - VPY) / (H - VPY) * 1.0
    c.line([(VPX + (x_far - VPX), FLOOR), (VPX + (x_far - VPX) * (H - VPY) / (FLOOR - VPY), H)], K, 0.6)
for k in range(1, 9):
    y = FLOOR + (H - FLOOR) * (1 - 1 / (1 + k * 0.35))
    c.line([(0, y), (W, y)], K, 0.6)

# --- the beam ---------------------------------------------------------------
BEAM = 30
c.rect(0, BEAM - 12, W, BEAM, fill=mix(K, B, 0.25))
c.line([(0, BEAM), (W, BEAM)], B, 1)
c.line([(0, BEAM - 12), (W, BEAM - 12)], B, 0.5)
for bx in range(10, W, 40):
    c.ellipse(bx, BEAM - 6, 1.5, 1.5, fill=B)

PIV = [62, 154, 246, 338]
COLS = [Y, R, Wh, G]
LEN = 420
SPK_Y = 476


def speaker(cx, cy, rx, ry):
    # cabinet: a box lying on its back, seen in perspective
    c.poly([(cx - rx - 6, cy - ry - 4), (cx + rx + 6, cy - ry - 4), (cx + rx + 9, cy + ry + 8),
            (cx - rx - 9, cy + ry + 8)], fill=mix(K, B, 0.2), outline=B, width=1)
    c.poly([(cx - rx - 9, cy + ry + 8), (cx + rx + 9, cy + ry + 8), (cx + rx + 9, cy + ry + 16),
            (cx - rx - 9, cy + ry + 16)], fill=K, outline=B, width=0.6)
    for sx in (-rx - 3, rx + 3):
        for sy in (-ry - 1, ry + 4):
            c.ellipse(cx + sx, cy + sy, 1, 0.8, fill=B)
    c.ellipse(cx, cy, rx, ry, fill=K, outline=Wh, width=0.6)
    for k in np.linspace(0.85, 0.35, 6):
        c.ellipse(cx, cy + (1 - k) * 2, rx * k, ry * k, outline=B, width=0.4)
    c.ellipse(cx, cy + 2.5, rx * 0.22, ry * 0.22, fill=B, outline=Wh, width=0.4)


for i, (px, col) in enumerate(zip(PIV, COLS)):
    speaker(px, SPK_Y, 34, 11)

# --- strobe of each swing: amplitude decays, phases differ -----------------
for i, (px, col) in enumerate(zip(PIV, COLS)):
    A0 = [0.17, 0.13, 0.10, 0.075][i]
    om = [1.0, 1.03, 1.07, 1.12][i]
    ph = [0.0, 0.9, 2.1, 3.0][i]
    N = 26
    for k in range(N):
        t = k * 0.55
        th = A0 * math.exp(-0.04 * t) * math.cos(om * t + ph)
        mx, my = px + LEN * math.sin(th), BEAM + LEN * math.cos(th)
        age = 1 - k / (N - 1)         # 1 = oldest, 0 = now
        bright = 0.12 + 0.88 * (1 - age) ** 1.6
        # cable ghosts: older swings fade into dark
        if k < N - 1:
            c.line([(px, BEAM), (mx, my - 12)], col if bright > 0.6 else B, 1)
            c.ellipse(mx, my, 4.5, 7, fill=mix(K, col, bright))
        else:
            c.line([(px, BEAM), (mx, my - 12)], Wh, 1.5)
            # the live microphone: body, grille, rim light
            T = lambda pts: [(mx + x * math.cos(th) + y * math.sin(th), my - x * math.sin(th) + y * math.cos(th)) for x, y in pts]
            c.poly(T([(-3, -13), (3, -13), (4, 2), (-4, 2)]), fill=K, outline=col, width=0.8)
            c.ellipse(*T([(0, 5)])[0], 5.2, 5.2, fill=col, outline=K, width=0.6)
            for g in (-2.5, 0, 2.5):
                a1, a2 = T([(g, 1), (g, 9)])
                c.line([a1, a2], K, 0.35)
            # feedback: when the mic is near the cone, the speaker howls in rings
            near = abs(mx - px) < 14
            for r in range(1, 6 if near else 2):
                c.ellipse(px, SPK_Y, 34 + r * 9, 11 + r * 3.4, outline=col, width=0.8 if near else 0.5)
    # swing envelope: the decaying arc traced on the dark
    arc = [(px + (LEN + 8) * math.sin(a), BEAM + (LEN + 8) * math.cos(a)) for a in np.linspace(-A0, A0, 30)]
    c.line(arc, B, 1)
    c.ellipse(px, BEAM, 2.6, 2.6, fill=col)

# --- four traces drifting out of phase -------------------------------------
TY = 540
c.rect(10, TY - 6, 390, 594, fill=K, outline=B, width=0.6)
for gx in range(10, 391, 19):
    c.line([(gx, TY - 6), (gx, 594)], B, 0.25)
for i, col in enumerate(COLS):
    base = TY + 6 + i * 12
    pts = []
    om = [1.0, 1.03, 1.07, 1.12][i]
    ph = [0.0, 0.9, 2.1, 3.0][i]
    for x in range(12, 389):
        t = (x - 12) / 377 * 60
        env = math.exp(-0.04 * t)
        swing = math.cos(om * t + ph)
        burst = math.exp(-(swing * 6) ** 2) * env  # howl when crossing the centre
        y = base - 5 * burst * math.sin(x * 2.3)
        pts.append((x, y))
    c.line(pts, col, 1)
c.text((14, TY - 10), "PENDULUM MUSIC · 1968", Wh, 6, anchor="ls")
c.text((386, TY - 10), "until all four hang still", B, 5.5, anchor="rs", font=SERIF)
c.save()
