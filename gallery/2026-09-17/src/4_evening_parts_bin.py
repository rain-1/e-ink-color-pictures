# Evening — "Parts Bin". Palette: green, black, red (tag).
# Enterprise never flew to space, but in 2003 the Columbia Accident Investigation Board shot
# foam at a section of her left wing at Southwest Research Institute, to see if that was what
# doomed Columbia. It was. A single hangar light over a dark shape on jacks, one panel already
# gone from the leading edge — the day's light turned into a warning tag instead of a spotlight.
import os, math
from PIL import Image, ImageDraw

W, H = 400, 600
GRN, BLK, RED = (0x1E, 0x9B, 0x3C), (0, 0, 0), (0xE0, 0x1B, 0x24)

im = Image.new("RGB", (W, H), BLK)
d = ImageDraw.Draw(im)

# a single work-light fixture overhead, just a bar — its light is what's picking the shape
# out of the dark; most of the frame stays black
fx, fy = 210, 46
d.rectangle((fx - 26, fy - 8, fx + 26, fy - 2), fill=GRN)
d.line((fx - 22, fy - 5, fx + 22, fy - 5), fill=BLK, width=1)

# the orbiter, side view, resting on jacks: nose, cabin, tail fin, delta wing — one clean
# silhouette, picked out by the light
CX, CY = 195, 250
nose = [(CX - 175, CY + 6), (CX - 130, CY - 18), (CX - 60, CY - 18), (CX - 60, CY + 22)]
d.polygon(nose, fill=GRN)
d.polygon([(CX - 60, CY - 18), (CX + 90, CY - 18), (CX + 130, CY + 2), (CX + 130, CY + 24),
           (CX - 60, CY + 24)], fill=GRN)                                   # fuselage
d.polygon([(CX + 60, CY - 18), (CX + 78, CY - 18), (CX + 108, CY - 92), (CX + 88, CY - 92)], fill=GRN)  # tail fin
for wx in range(CX - 150, CX - 90, 14):                                     # cockpit windows, cut black
    d.rectangle((wx, CY - 12, wx + 8, CY - 4), fill=BLK)

# delta wing, leading edge toward the viewer, in the foreground shadow below the fuselage —
# the same wing, just closer, so the missing panel reads clearly
WX, WY = 150, 400
wing = [(WX - 130, WY + 90), (WX - 10, WY - 10), (WX + 150, WY - 40), (WX + 190, WY + 10),
        (WX + 70, WY + 110), (WX - 50, WY + 120)]
d.polygon(wing, fill=GRN)
d.line([(WX - 10, WY - 10), (WX + 150, WY - 40)], fill=BLK, width=1)  # trailing crease, subtle

# leading edge, front-left of the wing: solid black rib line, with one gap where panel 8 used
# to be — the gap is red, hatched, and tagged
e0, e1 = (WX - 130, WY + 90), (WX - 10, WY - 10)
g0 = (e0[0] + (e1[0] - e0[0]) * 0.42, e0[1] + (e1[1] - e0[1]) * 0.42)
g1 = (e0[0] + (e1[0] - e0[0]) * 0.62, e0[1] + (e1[1] - e0[1]) * 0.62)
d.line((e0, g0), fill=BLK, width=5)
d.line((g1, e1), fill=BLK, width=5)
d.line((g0, g1), fill=RED, width=5)
perp = (-(g1[1] - g0[1]), g1[0] - g0[0])
pl = math.hypot(*perp); perp = (perp[0] / pl, perp[1] / pl)
for s in [0.2, 0.4, 0.6, 0.8]:
    gx = g0[0] + (g1[0] - g0[0]) * s
    gy = g0[1] + (g1[1] - g0[1]) * s
    d.line((gx, gy, gx + perp[0] * 20, gy + perp[1] * 20), fill=RED, width=2)
d.ellipse((g0[0] - 4, g0[1] - 4, g0[0] + 4, g0[1] + 4), fill=RED)

# the red tag: a small flag hanging off the gap, the day's light turned into a warning
tagx, tagy = (g0[0] + g1[0]) / 2 + perp[0] * 22, (g0[1] + g1[1]) / 2 + perp[1] * 22
d.line((g0[0], g0[1], tagx, tagy), fill=RED, width=2)
d.polygon([(tagx, tagy), (tagx + 44, tagy - 4), (tagx + 44, tagy + 16),
           (tagx + 22, tagy + 26), (tagx, tagy + 16)], fill=RED)
d.text((tagx + 6, tagy + 3), "RCC 8", fill=BLK)

d.text((14, H - 30), "LEFT WING, RCC PANEL 8", fill=GRN)
d.text((14, H - 16), "Palmdale storage · 2003", fill=GRN)

im.save(os.environ["OUT_RAW"])
