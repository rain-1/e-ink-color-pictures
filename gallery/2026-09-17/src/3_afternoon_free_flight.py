# Afternoon — "Free Flight". Palette: red, blue only.
# 12 August 1977: Enterprise separates from the 747 for the first time and glides down alone
# to Rogers Dry Lake. Two colours, hard-edged, diagonal — the separation itself as the whole
# composition. The day's light becomes negative space: a blue beacon punched out of the red hull.
import os, math
import numpy as np
from PIL import Image, ImageDraw

W, H = 400, 600
RED, BLU = (0xE0, 0x1B, 0x24), (0x12, 0x3D, 0xB0)
rng = np.random.default_rng(19770812)

im = Image.new("RGB", (W, H), BLU)   # sky, dominant
d = ImageDraw.Draw(im)

# sun, upper-left, radiating thin red rays across the sky
sx, sy = 60, 90
for a in np.linspace(0, 2 * math.pi, 28, endpoint=False):
    x1, y1 = sx + 40 * math.cos(a), sy + 40 * math.sin(a)
    x2, y2 = sx + 230 * math.cos(a), sy + 230 * math.sin(a)
    d.line((x1, y1, x2, y2), fill=RED, width=1)
d.ellipse((sx - 26, sy - 26, sx + 26, sy + 26), fill=RED)

# the carrier, small and level, already receding in the upper right — a simple flat silhouette
cx, cy = 300, 130
d.polygon([(cx - 60, cy), (cx - 40, cy - 6), (cx + 55, cy - 6), (cx + 66, cy + 4),
           (cx + 66, cy + 10), (cx - 60, cy + 10)], fill=RED)
d.polygon([(cx + 46, cy - 6), (cx + 60, cy - 6), (cx + 70, cy - 32), (cx + 56, cy - 32)], fill=RED)
for wx in range(cx - 40, cx + 40, 12):
    d.line((wx, cy + 2, wx, cy + 2), fill=BLU, width=1)

# the orbiter: banking hard, diagonal nose-down, streaking from upper-right to lower-left
CX, CY = 190, 330
ang = math.radians(35)   # long axis direction
def rot(px, py):
    c, s = math.cos(ang), math.sin(ang)
    return (CX + px * c - py * s, CY + px * s + py * c)
body = [(-150, -8), (-150, 8), (60, 24), (95, 8), (110, 0), (95, -8), (60, -24)]
d.polygon([rot(*p) for p in body], fill=RED)
tail = [(-110, -8), (-95, -8), (-70, -55), (-90, -55)]
d.polygon([rot(*p) for p in tail], fill=RED)
wingL = [(-10, 20), (60, 24), (30, 85), (-25, 55)]
wingR = [(-10, -20), (60, -24), (30, -85), (-25, -55)]
d.polygon([rot(*p) for p in wingL], fill=RED)
d.polygon([rot(*p) for p in wingR], fill=RED)

# speed lines trailing the orbiter, blue on red-sky diagonal
for i in range(7):
    off = 20 + i * 16
    p0 = rot(-150 - off, -4 + i * 1.2)
    p1 = rot(-230 - off, -4 + i * 1.2)
    d.line((p0, p1), fill=BLU, width=2 if i % 2 else 1)

# the day's light, as negative space: a small blue ring — the anti-collision beacon — punched
# through the red tail fin
bx, by = rot(-82, -30)
d.ellipse((bx - 5, by - 5, bx + 5, by + 5), fill=BLU)

# the dry lakebed below, red, with fine blue crack-hatching
d.rectangle((0, 520, W, H), fill=RED)
for _ in range(140):
    x0 = rng.uniform(0, W); y0 = rng.uniform(520, H)
    ln = rng.uniform(8, 30); a2 = rng.uniform(0, math.pi)
    d.line((x0, y0, x0 + ln * math.cos(a2), y0 + ln * math.sin(a2) * 0.3), fill=BLU, width=1)
d.line((0, 520, W, 520), fill=BLU, width=2)

d.text((14, H - 16), "ROGERS DRY LAKE · FREE FLIGHT 1 · 12 AUGUST 1977", fill=BLU)

im.save(os.environ["OUT_RAW"])
