"""Night — Nut, the sky, arched over the earth with the stars on her body; the sun sails
through her on the night barque. Under her arch: tonight's real sky — Orion (Sah) rising
with Sirius (Sopdet) behind him, and the waning gibbous moon two days past full."""
import math, random
from common import *

random.seed(22)
c = C(K)

# ---------- Nut: legs down the left, torso across the top, arms down the right ----------
OUT = [(30, 548), (30, 120), (48, 70), (96, 48), (300, 48), (348, 66), (370, 110), (370, 548)]
def arch(inset):
    x0, x1, top = 30 + inset, 370 - inset, 48 + inset
    r = max(6, 62 - inset)
    pts = [(x0, 540)]
    pts += [(x0 + r - r * math.cos(a), top + r - r * math.sin(a)) for a in np.linspace(0, math.pi / 2, 14)]
    pts += [(x1 - r + r * math.sin(a), top + r - r * math.cos(a)) for a in np.linspace(0, math.pi / 2, 14)]
    pts += [(x1, 540)]
    return pts
outer, inner = arch(0), arch(44)
band = outer + inner[::-1]
c.poly(band, B)
c.line(outer, Y, 1.6); c.line(inner, Y, 1.6)
# feet (left) and hands (right) on the ground
c.poly([(30, 540), (74, 540), (74, 548), (92, 556), (92, 562), (30, 562)], B, Y, 1.4)
for i in range(4): c.line([(80 + i * 3, 557), (80 + i * 3, 561)], Y, .8)
c.poly([(326, 540), (370, 540), (370, 566), (360, 572), (350, 566), (344, 572), (336, 566), (326, 560)], B, Y, 1.4)
for x in (338, 346, 354, 362): c.line([(x, 552), (x, 566)], Y, .8)
c.line([(30, 524), (74, 524)], Y, 2); c.line([(30, 530), (74, 530)], Y, 1)          # anklet
c.line([(326, 520), (370, 520)], Y, 2); c.line([(326, 526), (370, 526)], Y, 1)      # bracelet
c.line([(326, 300), (370, 300)], Y, 2); c.line([(326, 306), (370, 306)], R, 1.6)    # armlet
# her head, hanging between her arms, facing down toward the earth
hx, hy = 296, 118
c.poly([(hx - 22, 92), (hx + 30, 92), (hx + 30, 150), (hx + 18, 190), (hx + 4, 190), (hx + 8, 150), (hx - 22, 140)], K, Y, 1.2)   # hair
for i in range(9): c.line([(hx + 10 + i * 2.4, 96), (hx + 8 + i * 2.2, 186 - abs(i - 4) * 2)], B, .9)
c.poly([(hx - 20, 96), (hx + 8, 96), (hx + 8, 140), (hx - 4, 148), (hx - 16, 144), (hx - 22, 132), (hx - 28, 128), (hx - 22, 118)], Y, K, 1)  # face
c.poly([(hx - 14, 110), (hx - 4, 106), (hx + 4, 110), (hx - 4, 114)], WH, K, 1); c.circ(hx - 5, 110, 2.2, fill=K)
c.line([(hx - 16, 103), (hx + 5, 102)], K, 1.6); c.line([(hx + 4, 110), (hx + 9, 110)], K, 1.4)
c.line([(hx - 16, 136), (hx - 9, 137)], R, 1.6)
c.rect(hx - 22, 90, hx + 30, 96, fill=R, outline=Y, w=1)                              # fillet
# collar where torso meets arms
for j in range(4): c.arc(326, 92, 20 + j * 5, 90, 200, [Y, R, Y, G][j], 1.6)

# stars on her body, in ranks, and the sun's nightly passage as red discs
def on_band(t, off):
    """Point along the arch centre line; t in 0..1 from feet to hands, off = lateral offset."""
    mid = arch(22)
    seg = [(math.hypot(bx - ax, by - ay)) for (ax, ay), (bx, by) in zip(mid, mid[1:])]
    tot = sum(seg); d = t * tot
    for ((ax, ay), (bx, by)), s in zip(zip(mid, mid[1:]), seg):
        if d <= s:
            ux, uy = (bx - ax) / s, (by - ay) / s
            return (ax + ux * d - uy * off, ay + uy * d + ux * off)
        d -= s
    return mid[-1]
n = 58
for i in range(n):
    t = (i + .5) / n
    if 0.03 < t < 0.965:
        for off in (-11, 11) if i % 2 else (0,):
            x, y = on_band(t, off)
            if not (270 < x < 330 and 86 < y < 196) and 60 < y < 512 or (y <= 60):
                c.star(x, y, 5, Y, 1.1)
for k, t in enumerate(np.linspace(.08, .92, 12)):                                      # the twelve hours of night
    x, y = on_band(t, 0)
    if 270 < x < 332 and 80 < y < 200: continue
    c.circ(x, y, 6.5, fill=K); c.circ(x, y, 5.4, fill=R)

# ---------- under the arch: the real sky tonight ----------
# Orion, scaled from RA/Dec, tilted as he rises in the east
ORI = {"Betelgeuse": (5.92, 7.4, 3.6, R), "Rigel": (5.24, -8.2, 3.8, WH), "Bellatrix": (5.42, 6.3, 2.8, WH),
       "Saiph": (5.80, -9.7, 2.6, WH), "Alnitak": (5.68, -1.9, 2.6, WH), "Alnilam": (5.60, -1.2, 2.7, WH),
       "Mintaka": (5.53, -0.3, 2.5, WH), "Meissa": (5.59, 9.9, 2.0, WH), "Sirius": (6.75, -16.7, 4.6, WH),
       "Aldebaran": (4.60, 16.5, 3.2, R)}
def sky(ra, dec):
    x = -(ra - 5.6) * 15 * 5.4; y = -(dec + 1) * 5.4
    a = math.radians(-38)                                                              # rising: lying on his side
    return (196 + x * math.cos(a) - y * math.sin(a), 300 + x * math.sin(a) + y * math.cos(a))
P = {k: sky(v[0], v[1]) for k, v in ORI.items()}
# background ranks of small stars, as on a tomb ceiling
for row, y in enumerate(range(108, 470, 22)):
    for col, x in enumerate(range(92, 316, 22)):
        xx, yy_ = x + (11 if row % 2 else 0), y
        if xx > 262 and yy_ < 200: continue                                           # her face
        if any(math.hypot(xx - px, yy_ - py) < 15 for px, py in P.values()): continue
        if math.hypot(xx - 126, yy_ - 150) < 38: continue                             # the moon
        c.star(xx, yy_, 3.2, B if (row + col) % 3 else Y, .9)
for a, b in (("Betelgeuse", "Bellatrix"), ("Betelgeuse", "Alnitak"), ("Bellatrix", "Mintaka"), ("Alnitak", "Saiph"),
             ("Mintaka", "Rigel"), ("Saiph", "Rigel"), ("Alnitak", "Alnilam"), ("Alnilam", "Mintaka"),
             ("Betelgeuse", "Meissa"), ("Bellatrix", "Meissa")):
    c.line([P[a], P[b]], WH, 1)
for k, (ra, dec, r, col) in ORI.items():
    x, y = P[k]
    c.circ(x, y, r + 2.2, fill=K)
    c.star(x, y, r * 2.4, col if col != WH else Y, 1.2); c.circ(x, y, r, fill=col)
# the moon, waning gibbous (the dark limb on the right, as seen from the north)
mx, my, mr = 126, 150, 27
c.circ(mx, my, mr + 2, fill=K); c.circ(mx, my, mr, fill=WH)
for i in range(-mr, mr + 1):                                                           # shave the terminator
    hw = math.sqrt(max(0, mr * mr - i * i))
    c.line([(mx + hw * .78, my + i), (mx + hw, my + i)], K, 1.2)
for (dx, dy, r) in ((6, -8, 6), (-4, 6, 4.5), (10, 8, 3.5), (-2, -14, 3), (14, -2, 2.5), (2, 16, 2.5)):   # maria, hatched
    for j in range(int(-r), int(r) + 1, 2):
        hw = math.sqrt(max(0, r * r - j * j))
        c.line([(mx + dx - hw, my + dy + j), (mx + dx + hw, my + dy + j)], K, .8)

# ---------- the night barque on the waters under the earth ----------
by = 476
c.rect(74, by + 22, 326, by + 46, fill=B)
for j in range(3):
    pts = [(74 + i * 6, by + 28 + j * 7 + (2.4 if (i + j) % 2 else -2.4)) for i in range(43)]
    c.line(pts, WH if j == 0 else Y, 1)
hull = bez((112, by + 2), (150, by + 30), (250, by + 30), (288, by + 2), 24)
c.poly(hull + [(288, by - 4)] + bez((282, by + 2), (250, by + 18), (150, by + 18), (118, by + 2), 24)[::1] + [(112, by - 4)], Y, K, 1)
c.poly(hull + [(200, by + 6)], Y)
for i in range(9): c.line([(140 + i * 15, by + 12 + 6 * math.sin(i / 8 * math.pi)), (140 + i * 15, by + 20 + 6 * math.sin(i / 8 * math.pi))], K, .8)
for sd, x in ((-1, 112), (1, 288)):                                                    # papyrus prow and stern
    st = bez((x, by + 2), (x + sd * 12, by - 12), (x + sd * 4, by - 26), (x + sd * 14, by - 36), 10)
    c.line(st, Y, 3)
    for a in range(-50, 51, 25):
        aa = math.radians(a - 90 + sd * 20)
        c.line([st[-1], (st[-1][0] + 9 * math.cos(aa), st[-1][1] + 9 * math.sin(aa))], G, 1.4)
# shrine with the sun inside, wrapped by the serpent Mehen
c.rect(176, by - 44, 224, by + 4, fill=K, outline=Y, w=1.6)
c.poly([(172, by - 44), (228, by - 44), (224, by - 51), (176, by - 51)], Y)
for i in range(7): c.line([(180 + i * 7, by - 50), (180 + i * 7, by - 45)], K, .8)
c.circ(200, by - 20, 15.5, fill=Y); c.circ(200, by - 20, 13.5, fill=R)
mehen = [(200 + (21 + 2 * math.sin(t * 6)) * math.cos(t), by - 20 + (21 + 2 * math.sin(t * 6)) * math.sin(t)) for t in np.linspace(-.3, math.pi * 1.25, 40)]
c.line(mehen, G, 2.2); c.circ(mehen[0][0] + 1, mehen[0][1] - 2, 2.6, fill=G)
# steering oars, and the crew: two small gods fore and aft
for x in (252, 262): c.line([(x, by - 30), (x + 18, by + 34)], Y, 1.6); c.poly([(x + 14, by + 22), (x + 22, by + 24), (x + 20, by + 40), (x + 15, by + 38)], Y)
for x, col in ((148, WH), (236, WH), (130, G)):
    c.poly([(x - 5, by + 6), (x + 5, by + 6), (x + 3.5, by - 16), (x - 3.5, by - 16)], col)
    c.circ(x, by - 21, 4.2, fill=Y); c.rect(x - 4.5, by - 27, x + 4.5, by - 23, fill=B)
    c.line([(x - 2, by - 12), (x - 9, by - 4)], col, 1.4)
c.line([(148, by - 30), (148, by - 40)], Y, 1.2); c.circ(148, by - 43, 3, outline=Y, w=1)   # an ankh held up

# Geb, the earth: a strip of reeds along the bottom
c.rect(22, 562, 378, 580, fill=G)
for x in range(26, 378, 7):
    h = 8 + 5 * math.sin(x * .7)
    c.line([(x, 580), (x + 1.5, 580 - h - 6)], K, 1)
c.line([(22, 562), (378, 562)], Y, 1.4)

block_border(c, 6, 6, 394, 594, 14, [B, K, Y, K, R, K], seg=11, line=K, bg=Y)
c.save()
