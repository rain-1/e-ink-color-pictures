"""Candelilla — 10 p.m., 11 October 1492, the Santa María's quarterdeck. The Admiral
thinks he sees a light to the west 'like a little wax candle, rising and falling' and
calls Pedro Gutiérrez to look. Two figures at the rail, rim-lit by the stern lantern;
a sky of stars; the black sea; one yellow pinprick on the horizon, four hours before land."""
import math, random
import numpy as np
from common import *

random.seed(1011)
c = Canvas(K)
HZ = 352

# ---------- sky: Milky Way as a stipple band, then stars
h2, w2 = H * S, W * S
yy, xx = np.mgrid[0:H, 0:W].astype(float)   # masks are built at 1x, then doubled
up = lambda m: np.kron(m, np.ones((S, S), dtype=bool))
# band running from upper-left to the horizon at right
dband = np.abs((yy - 40) - (xx * 0.55)) / 70
mw = np.exp(-dband ** 2) * (0.6 + 0.4 * np.sin(xx / 23 + yy / 31) * np.sin(xx / 11 - yy / 17))
rnd = np.random.default_rng(5).random((H, W))
stip = (rnd < mw * 0.16) & (yy < HZ - 2)
# dark rift down the middle of the band
rift = np.abs((yy - 46) - (xx * 0.55) + 6 * np.sin(xx / 30)) < 9
stip &= ~(rift & (rnd > 0.02))
c.mask_fill(up(stip), Wt)
for _ in range(520):
    x, y = random.uniform(0, 400), random.uniform(0, HZ - 6) ** 1.0
    m = random.random() ** 3
    r = 0.45 + m * 1.4
    col = Wt
    if m > 0.5:
        col = random.choice([Wt, Wt, Y, R, B])
    c.circle(x, y, r, fill=col)
    if m > 0.75:   # diffraction cross on the bright ones
        L = r * 4
        c.line([(x - L, y), (x + L, y)], fill=col, width=0.5)
        c.line([(x, y - L), (x, y + L)], fill=col, width=0.5)
# a meteor
c.line([(300, 60), (348, 84)], fill=Wt, width=0.8)
c.line([(330, 75), (348, 84)], fill=Wt, width=1.4)

# ---------- sea
c.rect(0, HZ, 400, 600, fill=K)
y = HZ + 2
while y < 600:
    d = (y - HZ) / (600 - HZ)
    x = random.uniform(-10, 0)
    while x < 400:
        L = 2 + d * 18 * random.random()
        if random.random() < 0.55 - d * 0.25:
            c.line([(x, y), (x + L, y)], fill=B, width=0.5 + d * 0.9)
        x += L + random.uniform(4, 16) * (1 + 2 * d)
    y += 2 + d * 7
# star reflections, broken
for _ in range(50):
    x = random.uniform(0, 400); y = random.uniform(HZ + 4, 470)
    c.line([(x, y), (x + random.uniform(1, 3), y)], fill=Wt, width=0.5)

c.line([(0, HZ), (400, HZ)], fill=B, width=0.6)
# ---------- the light on the horizon, rising and falling
lx, ly = 268, HZ - 1.5
for k, dy in enumerate([-5, -2.6, 2.4]):
    c.circle(lx, ly + dy, 0.6, fill=R if k != 1 else Y)
c.circle(lx, ly, 1.6, fill=Y)
c.line([(lx, ly + 3), (lx, ly + 22)], fill=Y, width=0.6)  # its reflection
c.line([(lx, ly + 6), (lx, ly + 10)], fill=Y, width=1.2)

# ---------- rigging: mizzen shrouds and backstays, dark blue against the stars
for k in range(6):
    c.line([(18 + k * 9, 470), (-30 + k * 4, -10)], fill=B, width=0.8)
for k in range(5):
    c.line([(360 + k * 8, 470), (420 + k * 2, -10)], fill=B, width=0.8)
for j in range(22):  # ratlines on the left shrouds
    yy0 = 440 - j * 20
    c.line([(16 - (470 - yy0) * 0.1, yy0), (64 - (470 - yy0) * 0.13, yy0)], fill=B, width=0.5)
c.line([(400, 120), (300, -10)], fill=B, width=0.7)

# ---------- the stern lantern (left), glowing — screened tone rings
LX, LY = 70, 404
glow = np.exp(-(((xx - LX) ** 2 + (yy - LY) ** 2) ** 0.5) / 26)
tone = glow * 0.75
scr = screen(tone, H, W, 8)
c.mask_fill(up(scr & (glow > 0.42)), R)
c.mask_fill(up(scr & (glow <= 0.42) & (glow > 0.12)), B)
# lantern body
c.line([(LX, 372), (LX, 384)], fill=Y, width=1.2)
c.poly([(LX - 12, 384), (LX + 12, 384), (LX + 8, 378), (LX - 8, 378)], fill=R, outline=K, width=0.8)
c.poly([(LX - 11, 386), (LX + 11, 386), (LX + 8, 418), (LX - 8, 418)], fill=Y, outline=K, width=1)
for k in (-4, 0, 4):
    c.line([(LX + k, 386), (LX + k * 0.75, 418)], fill=K, width=1)
c.poly([(LX - 9, 418), (LX + 9, 418), (LX, 426)], fill=R, outline=K, width=0.8)
c.ellipse(LX, 404, 2.2, 5, fill=Wt)
c.line([(LX, 372), (LX + 40, 360), (LX + 60, 470)], fill=K, width=1.6)

# ---------- quarterdeck rail across the foreground, lit from the left
RAIL = 466
c.rect(0, RAIL, 400, 600, fill=K)
c.rect(0, RAIL - 8, 400, RAIL, fill=K)
c.line([(0, RAIL - 8), (400, RAIL - 8)], fill=Y, width=1.4)
c.line([(0, RAIL - 6), (400, RAIL - 6)], fill=R, width=0.6)
for i in range(22):  # turned balusters, lit on their left edge, fading with distance from the lantern
    x = 6 + i * 18.4
    near = max(0.0, 1 - abs(x - LX) / 260)
    lit = Y if near > 0.55 else (R if near > 0.2 else B)
    pts_l = [(x - 3, RAIL), (x - 5, RAIL + 10), (x - 3, RAIL + 18), (x - 6, RAIL + 30), (x - 3, RAIL + 44)]
    c.line(pts_l, fill=lit, width=1.1)
    c.line([(p[0] + 7.5, p[1]) for p in pts_l], fill=K, width=1.1)
    c.circle(x - 1.5, RAIL + 18, 1.2, fill=lit)
c.rect(0, RAIL + 44, 400, RAIL + 52, fill=K)
c.line([(0, RAIL + 44), (400, RAIL + 44)], fill=R, width=1)
# deck planks receding
for k in range(9):
    yk = RAIL + 56 + k * k * 0.9
    c.line([(0, yk), (400, yk)], fill=B if k % 2 else K, width=0.6)
for k in range(-12, 13):
    c.line([(200 + k * 12, RAIL + 54), (200 + k * 52, 600)], fill=B, width=0.5)
# a coil of rope by the lantern, catching the light
for r in range(4):
    c.ellipse(46, 575, 22 - r * 4, 7 - r, outline=R if r % 2 else Y, width=1)

# ---------- two figures at the rail, seen from behind, rim-lit from the left
def figure(x, base, h, hat, pointing=False):
    s = h / 160
    def q(u, v): return (x + u * s, base - v * s)
    body = [q(-26, 0), q(-30, 60), q(-24, 104), q(-15, 120), q(15, 120), q(24, 104), q(28, 60), q(26, 0)]
    c.poly(body, fill=K)
    # cloak folds
    for u in (-14, -2, 10):
        c.line([q(u, 4), q(u + 3, 96)], fill=B, width=0.5)
    c.line([q(-26, 0), q(-30, 60), q(-24, 104), q(-15, 120)], fill=Y, width=2.2)
    c.line([q(26, 0), q(28, 60), q(24, 104), q(15, 120)], fill=B, width=1.2)   # rim light
    c.line([q(-15, 120), q(-6, 124)], fill=R, width=1)
    # head
    c.ellipse(x, base - 136 * s, 10 * s, 13 * s, fill=K)
    c.arc(x, base - 136 * s, 10 * s, 13 * s, 90, 270, fill=Y, width=1.8)
    c.arc(x, base - 136 * s, 10 * s, 13 * s, 270, 90, fill=B, width=1)
    c.rect(x - 7 * s, base - 124 * s, x + 7 * s, base - 120 * s, fill=K)
    if hat == "cap":
        c.poly([q(-12, 141), q(-9, 156), q(9, 156), q(12, 141)], fill=K)
        c.line([q(-12, 141), q(-9, 156)], fill=R, width=1.1)
        c.line([q(-13, 141), q(13, 141)], fill=R, width=0.8)
    else:
        c.ellipse(x, base - 146 * s, 22 * s, 4 * s, fill=K)
        c.poly([q(-10, 146), q(-8, 160), q(8, 160), q(10, 146)], fill=K)
        c.arc(x, base - 146 * s, 22 * s, 4 * s, 120, 240, fill=Y, width=1)
    if pointing:
        arm = [q(20, 112), q(52, 128), q(78, 138)]
        c.line(arm, fill=K, width=6 * s)
        c.line([q(20, 116), q(52, 132), q(78, 142)], fill=R, width=0.8)
        c.circle(*q(80, 139), 3.2 * s, fill=K)
figure(142, RAIL + 2, 150, "hat")          # Gutiérrez, behind
figure(206, RAIL + 2, 172, "cap", pointing=True)  # the Admiral

# ---------- the log line
c.text((200, 590), "“una candelilla de cera que se alzaba y levantaba”", 10, fill=Y, font=SERIF_BI, anchor="mm")
finish(c)
