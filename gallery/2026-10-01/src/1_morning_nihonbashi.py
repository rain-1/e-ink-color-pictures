# Morning — "Nihonbashi, Dawn Departure". After Hiroshige's first Tōkaidō print (1833):
# the wooden bridge at first light, a daimyo procession of spears and boxes coming over the
# arch, fishmongers in the foreground, a red dawn band, the kido gate framing it all.
# Full palette, drawn in palette colours with a Bayer screen for the bokashi sky.
import os, sys, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ukiyo import *
from PIL import Image, ImageDraw
rng = np.random.default_rng(1833)
im = Image.new("RGB", (W, H), Wh)

# --- sky: bokashi. blue at the zenith fading to paper, a red band burning up from the horizon
yy, xx = np.mgrid[0:H, 0:W].astype(float)
HZ = 262
top = np.clip(1 - yy / 120, 0, 1) ** 1.3
im = blend(im, top, Wh, B, mask=yy < 140)
red = np.clip((yy - 170) / (HZ - 170), 0, 1) ** 1.1
im = blend(im, red, Wh, R, mask=(yy >= 160) & (yy < HZ))
# a single yellow sun-sliver sitting on the horizon behind the warehouses
d = ImageDraw.Draw(im); d.fontmode = "1"
d.ellipse((238, HZ - 22, 282, HZ + 22), fill=Y)
# stripes of cloud: long horizontal paper-white bars across the red, blue bars across the blue
for y, x0, x1 in ((188, 40, 230), (200, 150, 400), (214, 0, 120), (226, 260, 400), (240, 60, 210)):
    d.rectangle((x0, y, x1, y + 3), fill=Wh)
for y, x0, x1 in ((40, 0, 170), (58, 220, 400), (82, 90, 300)):
    d.rectangle((x0, y, x1, y + 4), fill=Wh)
# geese, a skein, very small, black
for i in range(9):
    gx, gy = 70 + i * 9, 120 + abs(i - 4) * 5
    d.line((gx - 3, gy - 2, gx, gy, gx + 3, gy - 2), fill=K)

# --- far bank: kura storehouses (white walls, black tiled roofs), fire-watch tower, masts
x = -5
while x < W:
    w = int(rng.integers(18, 42)); h = int(rng.integers(14, 30))
    top_y = HZ - h
    d.rectangle((x, top_y, x + w, HZ + 4), fill=Wh, outline=K)
    d.polygon([(x - 3, top_y), (x + w + 3, top_y), (x + w - 2, top_y - 7), (x + 2, top_y - 7)], fill=K)
    for k in range(x, x + w, 3):  # roof tile ticks
        d.line((k, top_y - 6, k, top_y - 1), fill=B)
    if rng.random() < 0.6:  # a small barred window
        wx = x + w // 2 - 3; d.rectangle((wx, top_y + 5, wx + 6, top_y + 10), fill=K)
    d.line((x, HZ - 2, x + w, HZ - 2), fill=K)  # plaster band
    x += w + int(rng.integers(0, 4))
# fire lookout tower (hinomi-yagura) left of centre
tx = 86
d.line((tx - 6, HZ - 30, tx - 2, HZ - 78), fill=K, width=2); d.line((tx + 6, HZ - 30, tx + 2, HZ - 78), fill=K, width=2)
for k in range(5):
    yk = HZ - 36 - k * 9
    d.line((tx - 5 + k * .4, yk, tx + 5 - k * .4, yk - 8), fill=K); d.line((tx + 5 - k * .4, yk, tx - 5 + k * .4, yk - 8), fill=K)
d.rectangle((tx - 5, HZ - 84, tx + 5, HZ - 78), fill=K); d.polygon([(tx - 8, HZ - 84), (tx + 8, HZ - 84), (tx, HZ - 92)], fill=K)
d.line((tx, HZ - 92, tx, HZ - 98), fill=K)  # bell
# Fuji, tiny, far left, the whole road's destination direction
d.polygon([(8, HZ - 32), (30, HZ - 52), (40, HZ - 52), (62, HZ - 32)], fill=B)
d.polygon([(26, HZ - 48), (30, HZ - 52), (40, HZ - 52), (44, HZ - 48), (39, HZ - 46), (35, HZ - 49), (31, HZ - 46)], fill=Wh)

# --- river: blue with white wave combs, a boat or two
RIV0, RIV1 = HZ + 4, 420
d.rectangle((0, RIV0, W, RIV1), fill=B)
waves(d, 0, RIV0 + 4, W, RIV1, ink=Wh, spacing=6, amp=1.2, rng=rng)
def boat(x, y, L, load=True):
    d.polygon([(x, y), (x + L, y), (x + L + 8, y - 6), (x - 3, y - 4)], fill=K)
    d.line((x - 3, y - 4, x + L + 8, y - 6), fill=Wh)
    if load:
        for k in range(4):
            d.rectangle((x + 6 + k * 9, y - 12, x + 13 + k * 9, y - 5), fill=Y, outline=K)
    traveller(d, x + L - 4, y - 5, 18, robe=B, hat=Y, facing=-1)
    d.line((x + L - 2, y - 18, x + L + 18, y + 6), fill=K)  # pole
boat(20, 300, 48); boat(300, 286, 40, load=False)

# --- the bridge: arch, deck, balusters, piers. Drawn after the river, before figures.
def arch_y(x, base=372, apex=318):
    t = (x - 200) / 230.0
    return apex + (base - apex) * t * t
# piers: forest of black legs + cross braces below the deck
for px in range(-10, W + 10, 22):
    y_top = arch_y(px) + 10
    d.rectangle((px - 2, y_top, px + 2, RIV1), fill=K)
    d.rectangle((px + 7, y_top + 2, px + 10, RIV1), fill=K)
    for by in range(int(y_top) + 8, RIV1 - 6, 18):
        d.line((px - 2, by, px + 10, by + 10), fill=K); d.line((px + 10, by, px - 2, by + 10), fill=K)
# deck: thick plank beam in wood-yellow with black lines, white underside
xs = np.arange(-20, W + 21, 2)
top_pts = [(x, arch_y(x)) for x in xs]
bot_pts = [(x, arch_y(x) + 12) for x in xs[::-1]]
d.polygon(top_pts + bot_pts, fill=Y, outline=K)
d.line([(x, arch_y(x) + 6) for x in xs], fill=K)
for x in range(-20, W + 20, 6):
    d.line((x, arch_y(x) + 7, x, arch_y(x) + 11), fill=K)
# railing (far side) — drawn before figures; near railing drawn after (figures walk between)
def railing(off, dy, step, cap=True):
    d.line([(x, arch_y(x) - dy) for x in xs], fill=K, width=2)
    d.line([(x, arch_y(x) - dy + 6) for x in xs], fill=K, width=1)
    for x in range(-20, W + 20, step):
        d.line((x, arch_y(x) - dy, x, arch_y(x) + off), fill=K, width=1)
    if cap:
        for x in (40, 360):
            y = arch_y(x)
            d.rectangle((x - 3, y - dy - 2, x + 3, y), fill=K)
            d.ellipse((x - 4, y - dy - 10, x + 4, y - dy - 2), fill=Y, outline=K)  # giboshi
            d.line((x, y - dy - 14, x, y - dy - 10), fill=K)
railing(-0, 26, 9, cap=False)

# --- the procession over the arch: spears, boxes, banners, walking left toward the viewer
order = ["spear", "spear", "box", None, "spear", "box", "spear", None, "spear", "spear", "box", None, "spear", "box", "spear", "spear"]
for i, load in enumerate(order):
    fx = 392 - i * 25 + rng.uniform(-3, 3)
    fy = arch_y(fx) - 1
    robe = [K, B, K, Wh][i % 4]
    traveller(d, fx, fy, 28, robe=robe, hat=K if load == "spear" else Y, facing=-1,
              stride=0.5 * math.sin(i * 1.7), load=load)
# a banner pole with a red streamer
bx = 150; by = arch_y(bx)
d.line((bx, by, bx, by - 60), fill=K, width=1)
d.polygon([(bx, by - 60), (bx + 16, by - 58), (bx + 14, by - 40), (bx, by - 42)], fill=R, outline=K)
railing(0, 11, 11)

# --- foreground ground: packed earth, paper-white with a fine stipple, a gutter of blue
G0 = 420
d.rectangle((0, G0, W, H), fill=Wh)
earth = np.clip((yy - G0) / (H - G0), 0, 1) * 0.30 + 0.08
im = blend(im, earth, Wh, Y, mask=yy >= G0)
d = ImageDraw.Draw(im); d.fontmode = "1"
# stone embankment (ishigaki) along the near bank
d.rectangle((0, G0, W, G0 + 16), fill=Wh, outline=K)
for row, y in enumerate((G0, G0 + 8)):
    x = -(row * 7)
    while x < W:
        w = int(rng.integers(10, 18)); d.rectangle((x, y, x + w, y + 8), outline=K); x += w
d.line((0, G0 + 16, W, G0 + 16), fill=K, width=2)
for k in range(260):  # pebbles / footprints
    px, py = rng.uniform(0, W), rng.uniform(G0 + 4, H)
    d.point((px, py), fill=K)

# --- fishmongers: two big figures with tenbin baskets of fish, one with a bonito over shoulder
def fish(x, y, L, c=B):
    d.polygon([(x, y), (x + L * .7, y - L * .18), (x + L, y), (x + L * .7, y + L * .18)], fill=c, outline=K)
    d.polygon([(x + L, y), (x + L * 1.25, y - L * .15), (x + L * 1.25, y + L * .15)], fill=c, outline=K)
    d.point((x + L * .15, y - 1), fill=Wh)
    for k in range(3):
        d.line((x + L * (.3 + k * .12), y - L * .1, x + L * (.3 + k * .12), y + L * .1), fill=K)
def monger(x, y, h, facing, robe):
    s = h / 30
    traveller(d, x, y, h, robe=robe, hat=None, facing=facing, stride=0.8)
    # hachimaki headband
    d.line((x - 2.4 * s, y - 23.2 * s, x + 2.4 * s, y - 23.2 * s), fill=R, width=max(1, int(s)))
    px0, px1 = x - 13 * s, x + 13 * s; py = y - 20 * s
    d.line((px0, py + 1.5 * s, px1, py - 1.5 * s), fill=K, width=max(2, int(1.3 * s)))
    for px, pyy in ((px0, py + 1.5 * s), (px1, py - 1.5 * s)):
        d.line((px - 3 * s, pyy, px - 4 * s, pyy + 7 * s), fill=K); d.line((px + 3 * s, pyy, px + 4 * s, pyy + 7 * s), fill=K)
        bx0, by0 = px - 6 * s, pyy + 7 * s
        d.polygon([(bx0, by0), (bx0 + 12 * s, by0), (bx0 + 10.5 * s, by0 + 6 * s), (bx0 + 1.5 * s, by0 + 6 * s)], fill=Y, outline=K)
        for k in range(1, 6):  # basket weave
            d.line((bx0 + k * 2 * s, by0, bx0 + k * 2 * s - .2 * s, by0 + 6 * s), fill=K)
        for k in range(3):    # fish heaped in the basket
            fish(bx0 + 1 * s + k * 2.5 * s, by0 - 1 * s - (k % 2) * 1.5 * s, 6 * s, c=[B, Wh, B][k])
# the crowd behind the mongers: smaller, further back
traveller(d, 52, 476, 44, robe=R, hat=None, facing=1, umbrella=R)         # woman with a red parasol
traveller(d, 168, 470, 40, robe=K, hat=K, facing=-1, staff=True)          # pilgrim with staff
traveller(d, 262, 478, 46, robe=G, hat=Y, facing=1, load="box")           # porter
traveller(d, 350, 474, 42, robe=B, hat=Y, facing=-1, load="pole")         # vegetable seller
traveller(d, 318, 486, 26, robe=Y, hat=None, facing=1, stride=1)          # child running
# samurai with two swords, mid-ground
sx, sy = 226, 508
traveller(d, sx, sy, 58, robe=K, hat=Y, facing=-1)
d.line((sx - 6, sy - 26, sx + 14, sy - 34), fill=Wh, width=2); d.line((sx - 4, sy - 22, sx + 10, sy - 27), fill=Wh)
# a fish tub on the ground with tails sticking out
tx, ty = 196, 556
d.ellipse((tx - 26, ty - 8, tx + 26, ty + 8), fill=Y, outline=K, width=2)
d.rectangle((tx - 26, ty, tx + 26, ty + 18), fill=Y); d.line((tx - 26, ty, tx - 26, ty + 18), fill=K, width=2)
d.line((tx + 26, ty, tx + 26, ty + 18), fill=K, width=2); d.arc((tx - 26, ty + 10, tx + 26, ty + 26), 0, 180, fill=K, width=2)
for k in range(5): d.line((tx - 22 + k * 11, ty + 2, tx - 22 + k * 11, ty + 22), fill=K)
for k in range(4): fish(tx - 20 + k * 9, ty - 3 - (k % 2) * 4, 14, c=[B, Wh, R, B][k])
monger(100, 552, 86, 1, B)
monger(300, 575, 104, -1, Wh)
# a dog sniffing, small, between them
dx, dy = 372, 528
d.ellipse((dx - 12, dy - 10, dx + 10, dy), fill=Wh, outline=K)
d.ellipse((dx - 20, dy - 9, dx - 9, dy - 1), fill=Wh, outline=K)
d.ellipse((dx - 7, dy - 9, dx - 1, dy - 4), fill=K)
for lx in (-9, -5, 4, 8):
    d.line((dx + lx, dy - 1, dx + lx, dy + 6), fill=K)
d.line((dx + 10, dy - 7, dx + 16, dy - 13), fill=K)

# --- the kido gate: two posts and a beam with a little tiled roof, framing everything
for x0 in (0, W - 22):
    d.rectangle((x0, 30, x0 + 22, H), fill=K)
    for y in range(40, H, 9):  # wood grain, cut white
        d.line((x0 + 5, y, x0 + 5, y + 5), fill=Wh); d.line((x0 + 15, y + 4, x0 + 15, y + 8), fill=Wh)
d.rectangle((0, 30, W, 46), fill=K)
d.polygon([(-10, 30), (W + 10, 30), (W - 6, 6), (6, 6)], fill=K)
for x in range(8, W - 8, 5):
    d.line((x, 9, x, 28), fill=B)
d.line((0, 31, W, 31), fill=Wh)
# hanging lantern under the beam
d.line((200, 46, 200, 54), fill=K)
d.ellipse((190, 54, 210, 80), fill=Wh, outline=K, width=2)
d.rectangle((192, 52, 208, 56), fill=K); d.rectangle((192, 78, 208, 82), fill=K)
d.text((195, 59), "橋", font=font(12, jp=True), fill=R)

# --- cartouches: title (red, vertical) and series (yellow), as on the print
cartouche(d, 340, 90, "日本橋", font(14, jp=True), R, Wh)
cartouche(d, 318, 90, "朝之景", font(11, jp=True), Y, K, pad=3)
d.rectangle((22, 586, 378, 600), fill=K)
d.text((30, 587), "TŌKAIDŌ 1/53 · NIHONBASHI · 1833", font=font(10, serif=False), fill=Wh)

im.save(os.environ.get("OUT_RAW", "/tmp/1.png"))
