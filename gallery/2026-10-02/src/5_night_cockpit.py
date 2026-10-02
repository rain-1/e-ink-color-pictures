"""Night — Night Watch. Inside the rocket, lights down. A deco-arched windscreen on a
field of stars and tonight's waning gibbous moon; below, an instrument panel of
dials, a radar scope, toggles and tell-tale lamps; a postcard of this morning's
launch tucked in the frame. Mostly black, with the instruments glowing."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from ink import *

rnd = random.Random(22)
cv = Canvas(K)
ALL = np.ones((H, W), bool)

# --- windscreen -----------------------------------------------------------------
WY0, WY1 = 26, 246
win = Canvas.mask(lambda d: (d.rectangle([22, 110, 378, WY1], fill=1), d.pieslice([22, WY0, 378, 194], 180, 360, fill=1)))
# milky way: a diagonal band of fine white dots, densest at its spine
band = np.abs((XX - 40) * 0.55 - (YY - 30))
cv.benday(win & (band < 60), WH, pitch=3, r=np.clip(0.75 - band / 120, 0, 0.75), angle=20)
for _ in range(420):
    x, y = rnd.randrange(22, 378), rnd.randrange(WY0, WY1)
    if win[y, x]:
        cv.a[y, x] = rnd.choice([WH, WH, WH, Y, B])
for _ in range(14):
    x, y = rnd.randrange(30, 370), rnd.randrange(40, 230)
    if win[y, x]:
        c = rnd.choice([WH, Y])
        cv.a[y - 3:y + 4, x] = c; cv.a[y, x - 3:x + 4] = c; cv.a[y - 1:y + 2, x - 1:x + 2] = c
# tonight's moon: waning gibbous, lit from the left
MX, MY, MR = 292, 104, 30
moon = Canvas.mask(lambda d: d.ellipse([MX - MR, MY - MR, MX + MR, MY + MR], fill=1))
lit = moon & ((XX - MX) < 0.55 * MR * np.sqrt(np.clip(1 - ((YY - MY) / MR) ** 2, 0, 1)))
cv.fill(lit, WH)
cv.benday(lit & ((XX - MX) > 0.15 * MR), B, pitch=3, r=0.9)
for (cx, cy, r) in [(MX - 12, MY - 8, 6), (MX - 4, MY + 10, 5), (MX - 18, MY + 6, 3), (MX + 4, MY - 14, 4)]:
    cv.benday(Canvas.mask(lambda d: d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=1)) & lit, B, pitch=3, r=1.2)
cv.fill(Canvas.mask(lambda d: d.arc([MX - MR, MY - MR, MX + MR, MY + MR], 70, 290, fill=1, width=1)), Y)
# a Draconid, early
cv.draw(lambda d: d.line([70, 70, 150, 116], fill=1, width=1), WH)
cv.draw(lambda d: d.line([120, 99, 150, 116], fill=1, width=2), WH)
cv.a[115:118, 149:152] = Y
# distant ringed planet low in the window
cv.draw(lambda d: d.ellipse([90, 196, 120, 226], fill=1), R)
cv.benday(Canvas.mask(lambda d: d.ellipse([90, 196, 120, 226], fill=1)) & (XX > 104), K, 3, 1.1)
cv.draw(lambda d: d.ellipse([78, 207, 132, 215], outline=1, width=1), Y)

# --- window frame: deco struts and rivets ------------------------------------------------
frame = Canvas.mask(lambda d: (d.rectangle([22, 110, 378, WY1], outline=1, width=8),
                               d.arc([22, WY0, 378, 194], 180, 360, fill=1, width=8)))
for xs in (140, 260):
    frame |= Canvas.mask(lambda d: d.line([xs, WY0 + 10, xs, WY1], fill=1, width=7))
frame |= Canvas.mask(lambda d: d.line([22, 150, 378, 150], fill=1, width=4))
cv.fill(frame, B)
cv.hatch(frame, K, pitch=3, angle=90, width=1)
cv.fill(Canvas.mask(lambda d: d.arc([26, WY0 + 4, 374, 190], 200, 340, fill=1, width=1)), Y)
for k in range(0, 180, 9):
    a = math.radians(180 + k)
    rx, ry = 200 + 174 * math.cos(a), 110 + 80 * math.sin(a)
    cv.a[int(ry) - 1:int(ry) + 1, int(rx) - 1:int(rx) + 1] = Y
for y in range(116, WY1, 12):
    for x in (25, 375, 140, 260):
        cv.a[y:y + 2, x - 1:x + 1] = Y
# hull below the window, ribbed
hull = (YY >= WY1 + 4) & (YY < 266)
cv.fill(hull, B)
cv.hatch(hull, K, pitch=4, angle=0, width=2)
cv.fill((YY == WY1 + 4), R)

# --- instruments -------------------------------------------------------------------------
def dial(cx, cy, r, label, val, ticks=40, col=WH, needle=R):
    cv.draw(lambda d: d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=1), B)
    cv.hatch(Canvas.mask(lambda d: d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=1)), K, 3, 45, 1)
    cv.draw(lambda d: d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=1), K)
    cv.draw(lambda d: d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, width=1), Y)
    a0, a1 = math.radians(135), math.radians(405)
    for i in range(ticks + 1):
        a = a0 + (a1 - a0) * i / ticks
        L = 8 if i % 5 == 0 else 4
        cv.draw(lambda d: d.line([cx + (r - 3) * math.cos(a), cy + (r - 3) * math.sin(a),
                                  cx + (r - 3 - L) * math.cos(a), cy + (r - 3 - L) * math.sin(a)],
                                 fill=1, width=2 if i % 5 == 0 else 1), col if i < ticks * 0.8 else R)
    # red zone arc
    cv.draw(lambda d: d.arc([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], 351, 45, fill=1, width=2), R)
    a = a0 + (a1 - a0) * val
    cv.draw(lambda d: d.line([cx - 6 * math.cos(a), cy - 6 * math.sin(a), cx + (r - 10) * math.cos(a), cy + (r - 10) * math.sin(a)], fill=1, width=2), needle)
    cv.draw(lambda d: d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=1), Y)
    text(cv, (cx, cy + r * 0.45), label, 10, Y, anchor="mm")


def radar(cx, cy, r):
    cv.draw(lambda d: d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=1), B)
    cv.hatch(Canvas.mask(lambda d: d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=1)), K, 3, 0, 1)
    scope = Canvas.mask(lambda d: d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=1))
    cv.fill(scope, K)
    ang = (np.degrees(np.arctan2(YY - cy, XX - cx)) + 360) % 360
    sweep0 = 300
    behind = (sweep0 - ang) % 360
    cv.benday(scope & (behind < 70), G, pitch=3, r=np.clip(1.3 - behind / 55, 0, 1.3))
    for rr in (r * 0.33, r * 0.66):
        cv.draw(lambda d: d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=1, width=1), G)
    cv.draw(lambda d: d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, width=2), G)
    cv.draw(lambda d: d.line([cx - r, cy, cx + r, cy], fill=1, width=1), G)
    cv.draw(lambda d: d.line([cx, cy - r, cx, cy + r], fill=1, width=1), G)
    for k in range(0, 360, 10):
        a = math.radians(k)
        cv.draw(lambda d: d.line([cx + r * math.cos(a), cy + r * math.sin(a), cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a)], fill=1, width=1), G)
    a = math.radians(sweep0)
    cv.draw(lambda d: d.line([cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)], fill=1, width=2), WH)
    for (bx, by, c) in [(cx + 22, cy - 30, Y), (cx + 34, cy - 12, Y), (cx - 30, cy + 20, R), (cx + 10, cy + 38, Y)]:
        cv.draw(lambda d: d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=1), c)
    text(cv, (cx, cy + r + 10), "SCOPE", 10, G, anchor="mt")


radar(200, 352, 62)
dial(68, 312, 36, "ALT", 0.62)
dial(68, 406, 36, "FUEL", 0.28, needle=Y)
dial(332, 312, 36, "GRAV", 0.47)
dial(332, 406, 36, "O2", 0.81)

# bar meters between dials and scope
for i, (x, lvl) in enumerate([(116, 0.7), (126, 0.45), (274, 0.9), (284, 0.35)]):
    for k in range(12):
        y = 386 - k * 8
        c = (G if k < 7 else Y if k < 10 else R) if k < lvl * 12 else None
        if c is not None:
            cv.draw(lambda d: d.rectangle([x, y, x + 6, y + 5], fill=1), c)
        else:
            cv.draw(lambda d: d.rectangle([x, y, x + 6, y + 5], outline=1, width=1), B)

# toggle switches with tell-tale lamps
cv.draw(lambda d: d.rounded_rectangle([14, 446, 386, 510], radius=6, fill=1), B)
cv.hatch(Canvas.mask(lambda d: d.rounded_rectangle([14, 446, 386, 510], radius=6, fill=1)), K, 3, 90, 2)
cv.draw(lambda d: d.rounded_rectangle([14, 446, 386, 510], radius=6, outline=1, width=1), Y)
for i in range(12):
    x = 32 + i * 30
    up = rnd.random() < 0.6
    lamp = rnd.choice([R, Y, G, G]) if up else K
    cv.draw(lambda d: d.ellipse([x - 4, 452, x + 4, 460], fill=1), lamp)
    cv.draw(lambda d: d.ellipse([x - 4, 452, x + 4, 460], outline=1, width=1), WH if up else B)
    cv.draw(lambda d: d.rectangle([x - 6, 470, x + 6, 494], fill=1), K)
    cv.draw(lambda d: d.rectangle([x - 6, 470, x + 6, 494], outline=1, width=1), WH)
    cv.draw(lambda d: d.line([x, 482, x, 472 if up else 492], fill=1, width=3), WH)
    cv.draw(lambda d: d.ellipse([x - 3, (469 if up else 489), x + 3, (475 if up else 495)], fill=1), R if up else WH)
    cv.a[500:503, x - 4:x + 5] = Y if i % 3 == 0 else B

# lower deck: throttle levers, a lit keypad, and the postcard
cv.draw(lambda d: d.rectangle([0, 518, W, H], fill=1), K)
for i, h in enumerate([40, 28, 34]):
    x = 300 + i * 26
    cv.draw(lambda d: d.rectangle([x - 2, 590 - 50, x + 2, 590], fill=1), B)
    cv.draw(lambda d: d.line([x, 590 - 10, x, 590 - h - 10], fill=1, width=4), WH)
    cv.draw(lambda d: d.rounded_rectangle([x - 8, 590 - h - 22, x + 8, 590 - h - 8], radius=4, fill=1), R)
    cv.draw(lambda d: d.rounded_rectangle([x - 8, 590 - h - 22, x + 8, 590 - h - 8], radius=4, outline=1, width=1), Y)
for r_ in range(3):
    for c_ in range(4):
        x, y = 170 + c_ * 22, 530 + r_ * 20
        cv.draw(lambda d: d.rectangle([x, y, x + 16, y + 14], outline=1, width=1), G)
        text(cv, (x + 8, y + 7), "123456789*0#"[r_ * 4 + c_ if r_ * 4 + c_ < 12 else 0], 10, G, anchor="mm")
# postcard of this morning, tucked in at an angle
card = Image.new("RGB", (70, 78), WH)
from PIL import ImageDraw as _D
dd = _D.Draw(card)
dd.fontmode = "1"  # no anti-aliasing: stay on the palette
dd.rectangle([4, 4, 65, 70], fill=Y)
dd.rectangle([4, 4, 65, 30], fill=B)
dd.ellipse([10, 40, 40, 70], fill=R)
dd.rectangle([4, 58, 65, 70], fill=K)
for k in range(5):
    dd.rectangle([6 + k * 12, 50 - k % 3 * 6, 14 + k * 12, 70], fill=K)
dd.polygon([(48, 12), (52, 24), (52, 48), (44, 48), (44, 24)], fill=R)
dd.polygon([(44, 48), (52, 48), (48, 60)], fill=Y)
card = card.rotate(9, expand=True, fillcolor=(1, 2, 3), resample=Image.NEAREST)
ca = np.array(card)
cm = ~np.all(ca == (1, 2, 3), -1)
ox, oy = 26, 514
hh, ww = ca.shape[:2]
reg = cv.a[oy:oy + hh, ox:ox + ww]
reg[cm[:reg.shape[0], :reg.shape[1]]] = ca[:reg.shape[0], :reg.shape[1]][cm[:reg.shape[0], :reg.shape[1]]]
cv.draw(lambda d: d.rectangle([56, 512, 66, 520], fill=1), WH)  # tape
cv.save()
