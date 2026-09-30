"""5 · Night — Sternenflammende Königin. After Schinkel's 1815 set for the Queen of the Night:
a vault of stars in perspective rows, the Queen on a crescent above a bank of cloud,
seen through a proscenium, with her aria's high notes along the bottom."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from common import *

random.seed(1791)
c = Canvas(K)
CX, AY, AR = 200, 205, 172          # arch centre / radius
AX0, AX1, ABOT = CX - AR, CX + AR, 470

def arch(dr, s, pad=0):
    dr.pieslice([(CX - AR + pad) * s, (AY - AR + pad) * s, (CX + AR - pad) * s, (AY + AR - pad) * s], 180, 360, fill=255)
    dr.rectangle([(AX0 + pad) * s, AY * s, (AX1 - pad) * s, ABOT * s], fill=255)

def inside(x, y, pad=0):
    if not (AX0 + pad < x < AX1 - pad and y < ABOT): return False
    return y >= AY or math.hypot(x - CX, y - AY) < AR - pad

# 1. vault ground: blue screened toward black at the rim, brightest behind the Queen
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.hypot((xx - CX) / 190, (yy - 300) / 230)
c.tone(arch, np.clip(0.95 - 0.95 * r ** 1.4, 0, 1) * 0.72 + 0.04, B, K)
c.snapshot_layer()

# 2. glory: rays around the Queen's head
QX, QY = 200, 262
for i in range(72):
    a = i * 2 * math.pi / 72
    r0, r1 = 26, (70 if i % 2 == 0 else 52) + (18 if i % 6 == 0 else 0)
    c.line([(QX + r0 * math.cos(a), QY + r0 * math.sin(a)), (QX + r1 * math.cos(a), QY + r1 * math.sin(a))], Y, 0.9 if i % 2 else 1.3)
for rr in (24, 30):
    c.ell(QX, QY, rr, outline=Y, width=0.8)

# 3. star vault: lat/lon grid on the inside of a sphere, perspective from its centre
f, pitch = 210, math.radians(26)
cp, sp = math.cos(pitch), math.sin(pitch)
stars = []
for li, lat in enumerate(np.arange(-10, 88, 6.3)):
    phi = math.radians(lat)
    step = 6.3 / max(math.cos(phi), 0.12)
    off = (li % 2) * step / 2
    for lon in np.arange(-180 + off, 180, step):
        th = math.radians(lon)
        dx, dy, dz = math.cos(phi) * math.sin(th), math.sin(phi), math.cos(phi) * math.cos(th)
        y2, z2 = dy * cp - dz * sp, dy * sp + dz * cp        # pitch camera up
        if z2 < 0.15: continue
        x, y = CX + f * dx / z2, 300 - f * y2 / z2
        if inside(x, y, 6) and math.hypot(x - QX, y - QY - 40) > 62:
            stars.append((x, y, z2))
for x, y, z in stars:
    rr = 1.6 + 2.4 * min(1, z)
    d = math.hypot(x - QX, y - QY)
    col = Y if d < 120 else Wh
    c.star(x, y, rr, col, 4, 0.3)
    if rr > 3.2: c.star(x, y, rr * 0.6, col, 4, 0.3, rot=-math.pi / 4)

# 4. veil: a great star-strewn cloak spreading behind her like wings
veil = []
for i in range(41):
    t = i / 40
    a = math.pi * (1.08 + 0.84 * t)
    rr = 118 + 10 * math.sin(t * math.pi * 5)
    veil.append((QX + rr * math.cos(a) * 1.05, QY + 125 + rr * math.sin(a) * 0.95))
veil = [(QX + 10, QY + 20)] + veil[::-1] + [(QX - 10, QY + 20)]
veil = [(QX - 12, QY + 24)] + [(QX - 114 + 4 * math.sin(k), QY + 130 - k * 2.6 - 18 * math.sin(k / 30 * math.pi)) for k in range(0, 60, 2)] \
     + [(QX - 60, QY - 20), (QX, QY + 8), (QX + 60, QY - 20)] \
     + [(QX + 114 - 4 * math.sin(k), QY + 130 - k * 2.6 - 18 * math.sin(k / 30 * math.pi)) for k in range(58, -1, -2)] + [(QX + 12, QY + 24)]
c.poly(veil, fill=K)
# veil hem folds + stars
for side in (-1, 1):
    for k in range(6):
        x0 = QX + side * (22 + k * 16)
        c.line([(x0, QY + 30 + k * 2), (x0 + side * 8, QY + 128 - k * 4)], B, 1)
    for k in range(26):
        rx, ry = QX + side * random.uniform(20, 108), QY + random.uniform(-6, 126)
        c.star(rx, ry, random.choice([1.6, 2.2, 3]), random.choice([Y, Y, Wh]), 4, 0.3)
c.line(veil[1:31], Y, 1.1); c.line(veil[-31:-1], Y, 1.1)

# 5. crescent moon, horns up
MX, MY = 200, 400
moon = Image.new("L", (W * S, H * S), 0); md = ImageDraw.Draw(moon)
md.ellipse([(MX - 72) * S, (MY - 40) * S, (MX + 72) * S, (MY + 40) * S], fill=255)
md.ellipse([(MX - 64) * S, (MY - 52) * S, (MX + 64) * S, (MY + 22) * S], fill=0)
c.im.paste(Y, (0, 0), moon); c.d = ImageDraw.Draw(c.im)
for k in range(14):  # engraved shading on the moon's belly
    x = MX - 52 + k * 8
    c.line([(x, MY + 18 + abs(k - 6.5) * -0.6), (x + 2, MY + 28 - abs(k - 6.5) * 1.2)], R, 0.9)

# 6. the Queen: robe, bodice, head, crown of stars, raised arms
robe = [(QX - 9, QY + 24), (QX + 9, QY + 24), (QX + 16, QY + 60), (QX + 34, QY + 128), (QX + 40, QY + 142),
        (QX - 40, QY + 142), (QX - 34, QY + 128), (QX - 16, QY + 60)]
c.poly(robe, fill=B, outline=Y, width=1)
for k in range(-3, 4):   # skirt pleats
    c.line([(QX + k * 2.5, QY + 60), (QX + k * 11, QY + 141)], K, 1)
for row in range(5):     # stars sewn on the skirt
    yv = QY + 70 + row * 15
    half = 16 + row * 4.5
    for k in range(-(row + 2), row + 3):
        c.star(QX + k * half / (row + 2), yv, 2.2, Wh if (k + row) % 2 else Y, 4, 0.3)
c.poly([(QX - 10, QY + 22), (QX + 10, QY + 22), (QX + 7, QY + 58), (QX - 7, QY + 58)], fill=K, outline=Y, width=0.8)
for k in range(4): c.line([(QX - 6, QY + 28 + k * 8), (QX + 6, QY + 28 + k * 8)], Y, 0.7)
c.ell(QX, QY + 58, 12, 3, fill=Y)                       # girdle
for side in (-1, 1):   # arms raised, commanding
    c.line([(QX + side * 9, QY + 26), (QX + side * 26, QY + 14), (QX + side * 44, QY - 16)], Wh, 2.4)
    c.ell(QX + side * 45, QY - 18, 2.8, fill=Wh)
    c.poly([(QX + side * 10, QY + 20), (QX + side * 26, QY + 26), (QX + side * 14, QY + 36)], fill=B, outline=Y, width=0.6)
c.poly([(QX - 11, QY - 2), (QX - 14, QY + 26), (QX - 6, QY + 22), (QX + 6, QY + 22), (QX + 14, QY + 26), (QX + 11, QY - 2)], fill=K)  # hair falling
c.ell(QX, QY + 5, 9, 11, fill=Wh)                        # face
c.d.chord([(QX - 10) * S, (QY - 7) * S, (QX + 10) * S, (QY + 9) * S], 180, 360, fill=K)   # hair parting
c.ell(QX - 3.5, QY + 5, 1.1, fill=K); c.ell(QX + 3.5, QY + 5, 1.1, fill=K)
c.line([(QX - 6, QY + 2.5), (QX - 2, QY + 3)], K, 0.7); c.line([(QX + 6, QY + 2.5), (QX + 2, QY + 3)], K, 0.7)  # stern brows
c.line([(QX - 2.5, QY + 11), (QX + 2.5, QY + 11)], R, 1.2)
for k in range(7):     # crown: seven stars on points
    a = math.radians(-150 + k * 20)
    c.line([(QX + 9 * math.cos(a), QY + 2 + 9 * math.sin(a)), (QX + 18 * math.cos(a), QY + 2 + 18 * math.sin(a))], Y, 1)
    c.star(QX + 20 * math.cos(a), QY + 2 + 20 * math.sin(a), 3.6 if k == 3 else 2.6, Y, 5, 0.42)

# 7. cloud bank: rows of lobes, back to front, black with blue rims and white edge-light
random.seed(3)
for row, (yb, rmin, rmax) in enumerate([(430, 16, 26), (448, 18, 30), (466, 20, 34)]):
    x = AX0 - 10
    lobes = []
    while x < AX1 + 20:
        rr = random.uniform(rmin, rmax)
        if abs(x - MX) < 60 and row == 0: x += rr; continue   # keep the moon clear
        lobes.append((x, yb + random.uniform(-6, 6), rr)); x += rr * 1.25
    for x, y, rr in lobes:
        c.ell(x, y, rr + 1.6, fill=B if row < 2 else Wh)
    for x, y, rr in lobes:
        c.ell(x, y + 1.5, rr, fill=K)
    for x, y, rr in lobes:   # hatching inside each lobe
        for k in range(3):
            c.d.arc([(x - rr * (0.75 - k * .18)) * S, (y - rr * (0.75 - k * .18)) * S, (x + rr * (0.75 - k * .18)) * S, (y + rr * (0.75 - k * .18)) * S],
                    200, 300, fill=B, width=S)

# 8. proscenium: black outside the arch, then gold mouldings and rosettes
m = Image.new("L", (W * S, H * S), 255); arch(ImageDraw.Draw(m), S); m = m.point(lambda v: 255 - v)
c.im.paste(K, (0, 0), m); c.d = ImageDraw.Draw(c.im)
for pad, wd in ((-3, 1.6), (-8, 0.8)):
    c.d.arc([(CX - AR + pad) * S, (AY - AR + pad) * S, (CX + AR - pad) * S, (AY + AR - pad) * S], 180, 360, fill=Y, width=round(wd * S))
    c.line([(AX0 + pad, AY), (AX0 + pad, ABOT)], Y, wd); c.line([(AX1 - pad, AY), (AX1 - pad, ABOT)], Y, wd)
for k in range(25):     # egg-and-dart on the arch
    a = math.pi + k * math.pi / 24
    c.ell(CX + (AR + 14) * math.cos(a), AY + (AR + 14) * math.sin(a), 2.4, 3.4 if k % 2 == 0 else 1.2, fill=Y if k % 2 == 0 else B)
for y in range(AY + 12, ABOT, 16):
    for x in (AX0 - 14, AX1 + 14):
        c.ell(x, y, 2.4, 3.4, fill=Y); c.ell(x, y + 8, 1.1, fill=B)
for x in (14, 386):   # corner rosettes
    c.star(x, 18, 8, Y, 8, 0.45); c.ell(x, 18, 2.4, fill=R)
c.star(CX, 20, 7, Y, 8, 0.45); c.ell(CX, 20, 2, fill=R)

# 9. stage apron, footlights, the aria's high notes
c.rect(0, ABOT, W, ABOT + 2, fill=Y)
for i in range(-14, 15):   # floorboards in perspective
    c.line([(CX + i * 13, ABOT + 2), (CX + i * 22, 512)], B, 0.8)
c.rect(0, 512, W, 516, fill=Y)
for x in range(22, W - 10, 24):   # footlights
    c.poly([(x - 4, 512), (x + 4, 512), (x, 500)], fill=Y); c.ell(x, 506, 1.4, fill=Wh)
st0 = 534
for k in range(5):
    c.line([(30, st0 + k * 4.5), (370, st0 + k * 4.5)], Wh, 0.7)
# G clef, drawn: a spiral round the G line with a tall loop and tail
cl = [(40 + 5.5 * math.cos(t) * (1 - t / 16), st0 + 11.5 + 5.5 * math.sin(t) * (1 - t / 16)) for t in np.linspace(math.pi, 3.2 * math.pi, 24)]
c.line([(44, st0 + 26), (41, st0 + 22), (40, st0 - 6), (44, st0 - 9), (46, st0 - 4), (38, st0 + 6), (34, st0 + 12), (38, st0 + 17), (45, st0 + 16), (46, st0 + 10), (41, st0 + 8), (38, st0 + 12)], Wh, 1.2)
# F-major arpeggio, staccato: F5 A5 C6 F6 ... (step = half of 4.5)
def ny(step): return st0 + 18 - step * 2.25        # step 0 = E4 bottom line
notes = [(1 + 7, 0), (3 + 7, 0), (5 + 7, 0), (1 + 14, 0), (5 + 7, 0), (3 + 7, 0), (1 + 7, 0), (5 + 7, 1),
         (1 + 14, 0), (5 + 7, 0), (1 + 14, 0), (5 + 7, 0), (1 + 14, 0), (3 + 14, 0), (1 + 14, 0), (5 + 7, 0)]
xn = 62
for i, (sn, _) in enumerate(notes):
    y = ny(sn)
    s = sn
    while s >= 10:     # ledger lines above the staff (G5 line at 10 -> ledger at A5? staff top F5=8)
        if s % 2 == 0: c.line([(xn - 5, ny(s)), (xn + 5, ny(s))], Wh, 0.7)
        s -= 1
    c.ell(xn, y, 2.9, 2.2, fill=Y)
    c.line([(xn + 2.6, y), (xn + 2.6, y + 14)], Y, 0.8) if sn >= 6 else None
    c.ell(xn, y - 5, 0.8, fill=Wh)                   # staccato dot
    xn += 19
for g in range(4):   # beams
    x0 = 62 + g * 76 + 2.6
    c.line([(x0, ny(notes[g * 4][0]) + 14), (x0 + 57, ny(notes[g * 4 + 3][0]) + 14)], Y, 1.6)
c.text((200, 568), "DER HÖLLE RACHE KOCHT IN MEINEM HERZEN", Y, 9.5, "mm", bold=True, spacing=1.2)
c.text((200, 584), "Die Zauberflöte · Wien · 30. IX. 1791", Wh, 9, "mm")
c.finish()
