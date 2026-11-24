# Midday — "The Lodge, in section". Full palette on white paper; blue water in charge.
# A natural-history plate: the pond cut through like a cake. Stick-and-mud dome, the dry
# sleeping chamber above the waterline, plunge holes, the winter food raft, first ice on the
# surface, the dam at the right, trout, a beaver bringing in one more aspen branch.
import math, random
import numpy as np
from common import *
rng = random.Random(1859); img, d = new(Wh)
WL, BT = 262, 468                                    # waterline, pond bottom
n = fbm(4, 50, 3)
bot = (BT + 14 * (n[BT] - 0.5)).astype(int)          # bottom profile per column
bank_top = lambda x: WL - 34 * max(0, (56 - x) / 56) ** 0.7

# --- water body, lighter near the surface
water = (YY > WL) & (YY < bot[None, :])
tone(img, water, B, Wh, 0.42 * np.exp(-(YY - WL) / 70) + 0.04)
for y in range(WL + 14, BT, 9):                       # faint strata
    tone(img, water & (YY == y), None, Wh, 0.3)
# --- pond floor: mud, stones
mud = (YY >= bot[None, :]) & (YY < 500)
tone(img, mud, K, Y, 0.3 + 0.3 * fbm(5, 10, 2))
for x in range(W - 1): d.line((x, bot[x], x + 1, bot[x + 1]), fill=K)
for _ in range(26):
    x = rng.randrange(8, W - 8); y = bot[x] + rng.randint(4, 24); s = rng.randint(3, 7)
    d.ellipse((x - s, y - s * 0.6, x + s, y + s * 0.6), fill=Wh, outline=K)
# --- left bank with turf
bank = [(0, 500), (0, WL - 34)] + [(x, bank_top(x)) for x in range(0, 56, 4)] + [(56, WL), (62, WL + 70), (74, int(bot[74])), (74, 500)]
bm = poly_mask(bank); tone(img, bm, K, Y, 0.36 + 0.3 * fbm(6, 8, 2)); d.line(bank[1:-1], fill=K)
for x in range(0, 56, 2):
    y = bank_top(x); L = rng.uniform(4, 11); d.line((x, y, x + rng.uniform(-3, 3), y - L), fill=rng.choice([G, G, K, Y]))
for _ in range(30):                                     # roots in the bank
    x = rng.uniform(0, 44); y = rng.uniform(WL - 20, WL + 80); d.line((x, y, x + rng.uniform(4, 14), y + rng.uniform(2, 12)), fill=Wh)

# --- the lodge mound
LX, TOP, HW = 190, 176, 96
def half(y): return HW * math.sqrt(max(0, 1 - ((BT - y) / (BT - TOP)) ** 3.4))
dome = [(LX - half(y) + 3 * math.sin(y / 5), y) for y in range(BT, TOP - 1, -3)] + [(LX + half(y) + 3 * math.cos(y / 6), y) for y in range(TOP, BT + 1, 3)]
dm = poly_mask(dome)
tone(img, dm, Y, K, 0.10 + 0.22 * fbm(7, 9, 2))                  # mud core
shell = dm & ~poly_mask([(LX + (x - LX) * 0.8, TOP + 20 + (y - TOP) * 0.86) for (x, y) in dome])
tone(img, shell, Y, Wh, 0.25)
for _ in range(1500):                                           # the sticks
    y = rng.uniform(TOP, BT); hw = half(y); x = LX + rng.uniform(-hw, hw)
    inshell = shell[int(y), int(min(max(x, 0), W - 1))]
    if not inshell and rng.random() < 0.86: continue
    a = math.atan2((y - (BT + 60)), (x - LX)) + math.pi / 2 + rng.gauss(0, 0.45); L = rng.uniform(5, 15)
    p = [x - math.cos(a) * L, y - math.sin(a) * L, x + math.cos(a) * L, y + math.sin(a) * L]
    ok = all(0 <= p[i] < W and 0 <= p[i + 1] < H and dm[int(p[i + 1]), int(p[i])] for i in (0, 2))
    if ok or (inshell and y < WL and rng.random() < 0.25):
        d.line(p, fill=rng.choice([K, K, K, R, Wh, G] if inshell else [K, R, Wh]), width=2 if rng.random() < 0.12 else 1)
d.line(dome + [dome[0]], fill=K)

# --- hollows: chamber, feeding shelf, two plunge holes, vent
cham = (ell_mask(LX + 4, 236, 46, 30) & (YY < 244)) | (ell_mask(LX - 34, 246, 20, 14) & (YY < 254) & (YY > 236))
def tube(pts, w):
    return mask_of(lambda q: (q.line(pts, fill=1, width=w), [q.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=1) for x, y in pts]))
t1 = tube([(LX - 40, 250), (LX - 44, 300), (LX - 58, 362), (LX - 92, 410)], 17)
t2 = tube([(LX + 30, 242), (LX + 38, 300), (LX + 56, 366), (LX + 94, 418)], 17)
vent = tube([(LX, 208), (LX + 2, 192), (LX - 1, TOP - 2)], 5)
holes = cham | t1 | t2
a = np.asarray(img).copy(); a[holes & (YY <= WL)] = Wh; img.paste(Image.fromarray(a))
tone(img, holes & (YY > WL), B, Wh, 0.12)
tone(img, vent, Wh, K, 0.3)
edge = holes & ~(np.roll(holes, 1, 0) & np.roll(holes, -1, 0) & np.roll(holes, 1, 1) & np.roll(holes, -1, 1))
a = np.asarray(img).copy(); a[edge] = K; img.paste(Image.fromarray(a))
for x in (LX - 60, LX - 44, LX + 22, LX + 38):                    # water surface inside the holes
    pass
d.line((LX - 48, WL, LX - 34, WL), fill=Wh); d.line((LX + 24, WL, LX + 38, WL), fill=Wh)
for _ in range(120):                                              # bedding of shredded wood
    x = LX + rng.uniform(-40, 48); y = 243 - rng.uniform(0, 4)
    if cham[int(y) - 1, int(x)]: d.line((x, y, x + rng.uniform(-4, 4), y - rng.uniform(0, 3)), fill=rng.choice([Y, Y, K]))
for k in range(4):                                                # warm breath out of the vent
    x0 = LX - 6 + k * 4
    pts = [(x0 + 5 * math.sin(t / 5 + k) + (k - 1.5) * t * 0.12, TOP - 6 - t) for t in range(0, 44 - k * 6, 3)]
    d.line(pts, fill=B)

def beaver(x, y, s, flip=1, swim=False, col_t=0.45):
    """Side view; x,y = centre of body; s = scale; flip=-1 faces left."""
    f = flip
    body = ell_mask(x, y, 22 * s, (9 if swim else 12) * s) | ell_mask(x + f * 19 * s, y - (0 if swim else 4) * s, 10 * s, 8 * s)
    if swim:
        o = body.copy()
        for sh in ((1, 0), (-1, 0), (1, 1), (-1, 1)): o |= np.roll(body, sh[0], sh[1])
        tone(img, o, Wh, Wh, 1)
    tone(img, body, R, K, col_t)
    tx = x - f * 34 * s; ty = y + (2 if swim else 8) * s                    # tail
    d.ellipse((tx - 15 * s, ty - 4 * s, tx + 15 * s, ty + 4 * s), fill=K)
    for k in range(-3, 4): d.line((tx + k * 4 * s - 2, ty - 2 * s, tx + k * 4 * s + 2, ty + 2 * s), fill=Wh)
    hx = x + f * 19 * s; hy = y - (0 if swim else 4) * s
    d.ellipse((hx + f * 2 * s - 1, hy - 4 * s - 1, hx + f * 2 * s + 1, hy - 4 * s + 1), fill=Wh); d.point((hx + f * 2 * s, hy - 4 * s), fill=K)
    d.ellipse((hx - f * 5 * s - 2, hy - 8 * s - 2, hx - f * 5 * s + 2, hy - 8 * s + 1), fill=K)
    d.ellipse((hx + f * 8 * s - 2, hy - 1, hx + f * 8 * s + 2, hy + 3), fill=K)
    d.line((hx + f * 7 * s, hy + 4 * s, hx + f * 7 * s, hy + 6 * s), fill=Y, width=2)   # the orange incisor
    if swim:
        d.line((x - f * 8 * s, y + 8 * s, x - f * 20 * s, y + 15 * s), fill=K, width=2); d.polygon([(x - f * 20 * s, y + 15 * s), (x - f * 27 * s, y + 13 * s), (x - f * 25 * s, y + 19 * s)], fill=K)
        d.line((x + f * 8 * s, y + 8 * s, x + f * 13 * s, y + 13 * s), fill=K, width=2)
    else:
        d.line((x - f * 10 * s, y + 10 * s, x - f * 4 * s, y + 13 * s), fill=K, width=2); d.line((x + f * 10 * s, y + 9 * s, x + f * 15 * s, y + 13 * s), fill=K, width=2)
beaver(LX + 16, 231, 0.72, 1); beaver(LX - 22, 237, 0.4, -1, col_t=0.3)
d.line((LX - 46, 250, LX - 30, 246), fill=G, width=2); d.line((LX - 44, 252, LX - 28, 251), fill=Y)   # a peeled stick on the shelf

# --- winter food raft, left of the lodge
for _ in range(210):
    x = rng.uniform(60, 108); y = WL - 6 + abs(rng.gauss(0, 34)); 
    if y > WL + 86 or dm[int(y), int(x)] and rng.random() < 0.9: continue
    a = rng.gauss(0.25, 0.5); L = rng.uniform(8, 22)
    d.line((x - math.cos(a) * L, y - math.sin(a) * L, x + math.cos(a) * L, y + math.sin(a) * L), fill=rng.choice([G, G, Y, K, Wh, R]), width=2 if rng.random() < 0.2 else 1)
for _ in range(16):
    x = rng.uniform(60, 108); branch(d, x, WL - 2, -math.pi / 2 + rng.gauss(0, 0.5), rng.uniform(10, 24), 1.4, 3, K, rng, 0.6, 0.7)
# --- first ice: a thin skin with open leads
for x in range(58, 372):
    if dm[WL, x] or (x % 53) in range(0, 7): continue
    d.line((x, WL - 1, x, WL + 1), fill=Wh); d.point((x, WL - 2), fill=K); 
    if x % 4 == 0: d.point((x, WL + 2), fill=K)

# --- the dam at the right, and the lower stream beyond it
dam = [(348, 500), (372, WL - 8), (382, WL - 10), (400, 300), (400, 500)]
dmk = poly_mask(dam); tone(img, dmk, Y, K, 0.4 + 0.3 * fbm(8, 8, 2))
for _ in range(240):
    x = rng.uniform(350, 400); y = rng.uniform(WL - 12, 480)
    if not dmk[int(y), int(min(x, W - 1))]: continue
    a = rng.gauss(-1.15, 0.35); L = rng.uniform(5, 14)
    d.line((x - math.cos(a) * L, y - math.sin(a) * L, x + math.cos(a) * L, y + math.sin(a) * L), fill=rng.choice([K, K, Wh, R, G]))
d.line(dam[:4], fill=K)

# --- pond life
def fish(x, y, s, f=1):
    d.polygon([(x - f * 9 * s, y), (x - f * 15 * s, y - 4 * s), (x - f * 15 * s, y + 4 * s)], fill=R)
    d.ellipse((x - 10 * s, y - 3.5 * s, x + 10 * s, y + 3.5 * s), fill=Wh, outline=K)
    d.point((x + f * 6 * s, y - 1), fill=K); d.line((x - 3 * s, y + 1, x + 3 * s, y + 1), fill=R)
fish(92, 430, 0.8, 1); fish(318, 446, 0.8, -1); fish(296, 436, 0.6, -1); fish(336, 300, 0.7, 1); fish(84, 380, 0.6, -1)
for _ in range(38):                                               # waterweed
    x = rng.randrange(6, 350)
    if dm[min(int(bot[x]) - 6, H - 1), x]: continue
    L = rng.randint(10, 34); pts = [(x + 3 * math.sin(t / 4 + x), bot[x] - t) for t in range(0, L, 2)]
    d.line(pts, fill=G if rng.random() < 0.8 else K)
bx, by = 326, 372                                                 # the late worker, towing aspen
beaver(bx, by, 0.75, -1, swim=True, col_t=0.3)
d.line((bx - 18, by + 3, bx - 40, by - 16), fill=K, width=2); tips = []
for k in range(3): branch(d, bx - 24 - k * 6, by - 2 - k * 5, -math.pi / 2 - 0.9 + (k % 2) * 1.6, 11, 1, 2, K, rng, 0.6, 0.7, tips)
for (tx, ty) in tips: d.ellipse((tx - 2, ty - 2, tx + 2, ty + 1), fill=Y, outline=K)
for k in range(9): 
    x = bx + 30 + k * 6 + rng.uniform(-2, 2); y = by - 6 - k * 5; s = rng.choice([1, 2, 2, 3]); d.ellipse((x - s, y - s, x + s, y + s), outline=Wh)

# --- above the water: a gnawed birch on the bank, low sun, falling snow
d.polygon([(12, WL - 30), (14, WL - 62), (20, WL - 70), (26, WL - 62), (28, WL - 28)], fill=Wh, outline=K)
d.polygon([(15, WL - 62), (20, WL - 74), (25, WL - 62)], fill=Y, outline=K)
for k in range(5): d.line((14, WL - 34 - k * 6, 20 + k, WL - 34 - k * 6), fill=K)
d.polygon([(30, WL - 60), (98, WL - 10), (96, WL - 2), (26, WL - 52)], fill=Wh, outline=K)
for k in range(9): d.line((38 + k * 7, WL - 51 + k * 5.2, 40 + k * 7, WL - 45 + k * 5.2), fill=K)
for _ in range(60):
    x, y = rng.randrange(8, W - 8), rng.randrange(64, WL - 8)
    if not dm[y, x] and not (x < 105 and y > WL - 80): d.point((x, y), fill=B); d.point((x + 1, y + 1), fill=B)

# --- callouts
fn = font("DejaVu Sans:bold", 9); fl = font("DejaVu Sans", 9)
def call(i, px, py, lx, ly):
    d.line((px, py, lx, ly), fill=K); d.ellipse((px - 1, py - 1, px + 1, py + 1), fill=K)
    d.ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=Wh, outline=K); d.text((lx - 2.5, ly - 6), str(i), font=fn, fill=R)
call(1, LX + 2, 192, LX + 62, 112); call(2, LX + 40, 224, 336, 160); call(3, LX - 38, 244, 62, 150)
call(4, LX - 45, 330, 26, 330); call(5, 84, WL + 26, 26, 396); call(6, LX + 80, 300, 344, 204)
call(7, 384, WL + 60, 366, 478); call(8, 310, WL, 350, 236)
# --- title and legend
d.rectangle((5, 5, W - 6, H - 6), outline=K); d.rectangle((8, 8, W - 9, H - 9), outline=K)
spaced(d, 200, 18, "THE LODGE", font("DejaVu Serif:bold", 20), K, gap=6)
ft = font("DejaVu Serif:italic", 11); s = "Castor canadensis — a winter house, in section"
d.text((200 - d.textlength(s, font=ft) / 2, 46), s, font=ft, fill=B)
d.line((70, 64, 330, 64), fill=K)
a = np.asarray(img).copy(); a[500:592, 10:390] = Wh; img.paste(Image.fromarray(a)); d.line((10, 500, 390, 500), fill=K); d.line((10, 503, 390, 503), fill=K)
leg = ["Vent — the lodge breathes", "Sleeping chamber, dry", "Feeding shelf", "Plunge hole",
       "Winter food raft", "Mud-and-stick wall", "Dam", "First ice"]
for i, t in enumerate(leg):
    col, row = divmod(i, 4); x = 22 + col * 190; y = 514 + row * 18
    d.ellipse((x - 2, y - 2, x + 12, y + 12), outline=K); d.text((x + 2.5, y - 1), str(i + 1), font=fn, fill=R); d.text((x + 20, y), t, font=fl, fill=K)
save(img)
