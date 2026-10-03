"""It's Gonna Rain (1965): a tape loop of a street preacher, two machines drifting apart.
An upright reel-to-reel in front of a rain-streaked window at dusk."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from ink import *

random.seed(1965)
c = Canvas(K)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# --- the window: dusk over the city ---------------------------------------
WX0, WX1, WY0, WY1 = 18, 382, 18, 400
win = (xx > WX0) & (xx < WX1) & (yy > WY0) & (yy < WY1)
HZ = 300
c.paste_mask(ramp([K, R, R, Y, Wh], np.clip((yy - 0) / HZ, 0, 1) ** 1.3 * 0.98), win & (yy < HZ + 40))
# cloud bars across the afterglow
for by, bx0, bx1 in [(258, 210, 382), (270, 160, 330), (286, 240, 382), (230, 18, 200), (210, 60, 260)]:
    c.rect(bx0, by, bx1, by + 3.5, fill=R)
    c.line([(bx0 + 4, by + 3.5), (bx1 - 2, by + 3.5)], K, 0.4)
# skyline: Union Square-ish blocks, cable towers, a Dewey column
random.seed(4)
x = WX0
while x < WX1:
    w_ = random.uniform(16, 38)
    h_ = random.uniform(40, 120)
    top = HZ + 30 - h_
    c.rect(x, top, x + w_, WY1, fill=K)
    if random.random() < 0.3:
        c.rect(x + w_ * 0.3, top - 10, x + w_ * 0.7, top, fill=K)
        c.line([(x + w_ / 2, top - 10), (x + w_ / 2, top - 22)], K, 0.8)
    for wy in np.arange(top + 5, WY1 - 6, 6):
        for wx in np.arange(x + 3, x + w_ - 4, 5):
            if random.random() < 0.18:
                c.rect(wx, wy, wx + 2.5, wy + 3, fill=Y if random.random() < 0.8 else Wh)
    x += w_ + random.uniform(-2, 3)
c.line([(196, 330), (196, 236)], K, 3)                 # the column in the square
c.ellipse(196, 232, 3.5, 5, fill=K)
c.line([(192, 228), (200, 236)], K, 1)
# rain: long slanted streaks, and beaded drops on the glass
for i in range(260):
    x0 = random.uniform(WX0, WX1 + 40); y0 = random.uniform(WY0, WY1)
    L = random.uniform(8, 22)
    col = Wh if y0 < HZ - 60 else (B if random.random() < 0.6 else Wh)
    c.line([(x0, y0), (x0 - L * 0.28, y0 + L)], col, 1)
for i in range(70):
    dx, dy = random.uniform(WX0 + 4, WX1 - 4), random.uniform(WY0 + 4, WY1 - 4)
    r = random.uniform(1.5, 4)
    c.ellipse(dx, dy, r, r * 1.15, fill=K)
    c.ellipse(dx + r * 0.25, dy + r * 0.2, r * 0.6, r * 0.7, fill=Y if dy < HZ else R)
    c.ellipse(dx - r * 0.3, dy - r * 0.35, max(0.7, r * 0.25), max(0.7, r * 0.25), fill=Wh)
    if random.random() < 0.35:  # trickle
        c.line([(dx, dy + r), (dx + random.uniform(-2, 2), dy + r + random.uniform(10, 40))], Wh, 1)
# window frame: mullions and sill
c.rect(WX0 - 4, WY0 - 4, WX1 + 4, WY1 + 4, outline=R, width=1)
c.rect(196, WY0, 204, WY1, fill=K)
c.rect(WX0, 205, WX1, 212, fill=K)
c.line([(197, WY0), (197, WY1)], R, 0.6)
c.line([(WX0, 206), (WX1, 206)], R, 0.6)
c.rect(0, WY1, W, WY1 + 10, fill=mix(K, R, 0.35))
c.line([(0, WY1), (W, WY1)], Y, 0.6)

# --- the machine ------------------------------------------------------------
DX0, DX1, DY0, DY1 = 70, 330, 120, 586
GREY = mix(Wh, K, 0.42)
c.rect(DX0 + 8, DY0 + 8, DX1 + 8, DY1 + 8, fill=mix(K, R, 0.25))   # shadow on the wall
c.rect(DX0, DY0, DX1, DY1, fill=GREY, outline=K, width=1.4)
c.rect(DX0 + 7, DY0 + 7, DX1 - 7, DY1 - 120, fill=mix(Wh, K, 0.6), outline=K, width=0.8)
# rim light from the window on the top edge and left
c.line([(DX0 + 1, DY0 + 1), (DX1 - 1, DY0 + 1)], R, 1.2)
c.line([(DX0 + 1, DY0 + 1), (DX0 + 1, DY1 - 1)], R, 0.9)
for sx, sy in [(DX0 + 4, DY0 + 4), (DX1 - 4, DY0 + 4), (DX0 + 4, DY1 - 4), (DX1 - 4, DY1 - 4)]:
    c.ellipse(sx, sy, 2, 2, fill=K)
    c.line([(sx - 1.4, sy), (sx + 1.4, sy)], Wh, 0.4)

def reel(cx, cy, R0, pack, ang):
    c.ellipse(cx, cy, R0 + 2, R0 + 2, fill=K)
    c.ellipse(cx, cy, R0, R0, fill=B, outline=K, width=0.8)
    # tape pack visible through the flange cut-outs
    c.ellipse(cx, cy, pack, pack, fill=mix(R, K, 0.55))
    for k in range(3, int(pack), 3):
        c.ellipse(cx, cy, k, k, outline=K, width=0.25)
    c.ellipse(cx, cy, pack, pack, outline=R, width=0.6)
    # flange cut-outs: three rounded windows
    for k in range(3):
        a = ang + k * 2 * math.pi / 3
        pts = []
        for t in np.linspace(-0.62, 0.62, 12):
            pts.append((cx + (R0 - 7) * math.cos(a + t), cy + (R0 - 7) * math.sin(a + t)))
        for t in np.linspace(0.45, -0.45, 10):
            pts.append((cx + 18 * math.cos(a + t), cy + 18 * math.sin(a + t)))
        mask_pts = pts
        # inside the window: the pack (dark) or empty spool space (grey through)
        c.poly(mask_pts, fill=mix(K, B, 0.2))
        inner = [p for p in mask_pts]
        for rr in range(20, int(pack), 3):
            arc = [(cx + rr * math.cos(a + t), cy + rr * math.sin(a + t)) for t in np.linspace(-0.5, 0.5, 10)]
            c.line(arc, R if rr % 2 else K, 0.5)
        c.line(mask_pts + [mask_pts[0]], K, 0.8)
    # hub
    c.ellipse(cx, cy, 15, 15, fill=Wh, outline=K, width=0.8)
    for k in range(3):
        a = ang + math.pi / 3 + k * 2 * math.pi / 3
        c.line([(cx, cy), (cx + 11 * math.cos(a), cy + 11 * math.sin(a))], K, 2)
    c.ellipse(cx, cy, 4.5, 4.5, fill=GREY, outline=K, width=0.6)
    c.ellipse(cx, cy, 1.5, 1.5, fill=K)
    # specular sweep on the flange
    arc = [(cx + (R0 - 3) * math.cos(t), cy + (R0 - 3) * math.sin(t)) for t in np.linspace(-2.5, -1.7, 10)]
    c.line(arc, Wh, 1.2)

RC = 200
reel(RC, 196, 68, 46, 0.4)
reel(RC, 362, 68, 30, 1.1)

# head block between the reels; tape threads from the top reel down past the heads
HB = (110, 272, 290, 290)
# tape path: right edges of reels around guide posts
guide_r = (300, 276)
guide_l = (100, 276)
c.line([(RC + 46, 196), (guide_r[0] + 3, guide_r[1])], R, 1.4)
c.line([(guide_r[0] + 3, guide_r[1] + 6), (RC + 30, 362)], R, 1.4)
c.rect(HB[0], HB[1], HB[2], HB[3], fill=K)
c.rect(HB[0] + 2, HB[1] + 2, HB[2] - 2, HB[3] - 2, fill=mix(Wh, K, 0.3))
for hx, lab in [(150, "E"), (190, "R"), (230, "P")]:
    c.rect(hx - 9, 268, hx + 9, 285, fill=Wh, outline=K, width=0.8)
    c.rect(hx - 2, 268, hx + 2, 272, fill=K)
    c.text((hx, 280), lab, K, 5.5, anchor="mm")
# capstan and pinch roller
c.ellipse(268, 281, 4, 4, fill=Wh, outline=K, width=0.8)
c.ellipse(278, 281, 7, 7, fill=K)
c.ellipse(278, 281, 2.5, 2.5, fill=GREY)
for g in (guide_r, guide_l):
    c.ellipse(g[0], g[1] + 3, 5, 5, fill=Wh, outline=K, width=0.8)
c.line([(guide_l[0] + 5, 276), (guide_r[0] - 5, 276)], R, 1.6)  # tape across the heads
# the loop: a long strand leaving the deck to the right, round a pencil held off-frame
c.line([(guide_r[0] + 5, 279), (352, 300), (372, 340), (376, 400), (372, 470)], R, 1.4)
c.line([(guide_l[0] - 5, 279), (52, 300), (40, 380), (36, 470)], R, 1.4)
c.text((362, 420), "LOOP", Y, 5, anchor="mm")

# --- control panel ---------------------------------------------------------
PY = DY1 - 112
c.rect(DX0 + 7, PY, DX1 - 7, DY1 - 7, fill=K)
# two VU meters: left and right channel — the two machines, out of phase
for i, (mx, needle) in enumerate([(130, -0.5), (270, 0.25)]):
    c.rect(mx - 42, PY + 8, mx + 42, PY + 50, fill=Y, outline=Wh, width=0.8)
    for t in np.linspace(-0.85, 0.85, 21):
        r1, r2 = 30, 34 if abs(t * 20) % 5 < 0.6 else 32
        c.line([(mx + r1 * math.sin(t), PY + 48 - r1 * math.cos(t)), (mx + r2 * math.sin(t), PY + 48 - r2 * math.cos(t))],
               R if t > 0.45 else K, 0.6)
    arc = [(mx + 30 * math.sin(t), PY + 48 - 30 * math.cos(t)) for t in np.linspace(0.45, 0.85, 8)]
    c.line(arc, R, 1.6)
    c.text((mx - 34, PY + 13), "VU", K, 5, anchor="lt")
    c.text((mx + 34, PY + 13), "LR"[i], K, 6, anchor="rt")
    c.line([(mx, PY + 48), (mx + 33 * math.sin(needle), PY + 48 - 33 * math.cos(needle))], K, 0.9)
    c.ellipse(mx, PY + 48, 3, 3, fill=K)
c.text((200, PY + 28), "IT'S\nGONNA\nRAIN", Wh, 5.5, anchor="mm")
# transport buttons and knobs
for i, lab in enumerate(["◀◀", "▶", "■", "▶▶", "●"]):
    bx = 112 + i * 44
    c.rect(bx - 16, PY + 60, bx + 16, PY + 76, fill=Wh if lab != "●" else R, outline=Wh, width=0.8)
    c.text((bx, PY + 68.5), lab, K if lab != "●" else Wh, 7, font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", anchor="mm")
for i in range(6):
    kx = 100 + i * 40
    c.ellipse(kx, PY + 93, 8, 8, fill=GREY, outline=Wh, width=0.6)
    a = -2.2 + i * 0.7
    c.line([(kx, PY + 93), (kx + 7 * math.cos(a), PY + 93 + 7 * math.sin(a))], Wh, 1)
# masking-tape label with the two phrases drifting
c.poly([(DX0 + 14, DY0 + 12), (DX0 + 120, DY0 + 10), (DX0 + 121, DY0 + 26), (DX0 + 14, DY0 + 27)], fill=Y, outline=K, width=0.5)
c.text((DX0 + 18, DY0 + 14), "it's gonna rain it's gonna rain", K, 4.6, anchor="lt", font=SERIF)
c.text((DX0 + 22, DY0 + 20.5), "it's gonna rain it's gonna rai", R, 4.6, anchor="lt", font=SERIF)
c.text((DX1 - 14, DY0 + 18), "UNION SQ · SF · 1964", Wh, 5, anchor="rm")

c.text((200, 597), "STEVE REICH · 90", R, 6, anchor="ms")
c.save()
