#!/usr/bin/env python3
"""06 — THE TIME MACHINE (1895): general arrangement.

A patent plate for a thing that cannot be patented. Paper-white ground,
black line, the dawn coming through the laboratory window as three flat
yellow shafts. Everything is rendered the way an 1890s engraver rendered
machinery: outline first, then contour lines to round it, then cross-hatch
in the shadows. Ink never sits on yellow — the panel has no dark yellow, so
tone is made on white and colour is kept flat.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plate import Plate, K, P, R, Y, B, poly

p = Plate(bg=P)

FLOOR = 452

# ------------------------------------------------------------ three shafts
# laid down first, so every line drawn afterwards crosses them in black
SHAFTS = []
for (sy, sh, dy) in ((58, 30, 150), (100, 40, 176), (152, 22, 196)):
    d = poly([(140, sy), (140, sy + sh), (392, sy + sh + dy), (392, sy + dy)])
    SHAFTS.append(d)
    p.add(f'<path d="{d}" fill="{Y}"/>')
    p.add(f'<path d="{d}" fill="none" stroke="{K}" stroke-width="1.4"/>')

# motes turning over in the light
for n, d in enumerate(SHAFTS):
    p.stipple(p.clip(d), (140, 40, 392, 380), 130, rmin=0.8, rmax=1.9, color=K, seed=11 + n)

# ---------------------------------------------------------------- the wall
wall = p.clip_rect(16, 16, 368, FLOOR - 16)
p.rule_field(wall, (16, 16, 384, FLOOR), 90, 9.0, 1.0, K,
             taper=lambda t: max(0.0, min(1.0, (t - 0.42) * 2.2)))

# window, upper left: small panes, a low red sun, yellow sky
wx, wy, ww, wh = 32, 38, 108, 136
p.add(f'<rect x="{wx-6}" y="{wy-6}" width="{ww+12}" height="{wh+12}" fill="{P}" stroke="{K}" stroke-width="3.0"/>')
p.add(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="{Y}"/>')
win = p.clip_rect(wx, wy, ww, wh)
p.add(f'<g clip-path="url(#{win})"><circle cx="{wx+ww*0.60}" cy="{wy+wh*0.66}" r="27" fill="{R}"/>'
      f'<circle cx="{wx+ww*0.60}" cy="{wy+wh*0.66}" r="27" fill="none" stroke="{K}" stroke-width="1.6"/>'
      # chimneys of Richmond on the sill line
      f'<path d="{poly([(wx,wy+wh*0.86),(wx+18,wy+wh*0.86),(wx+18,wy+wh*0.74),(wx+30,wy+wh*0.74),(wx+30,wy+wh*0.88),(wx+52,wy+wh*0.88),(wx+52,wy+wh*0.78),(wx+64,wy+wh*0.78),(wx+64,wy+wh*0.90),(wx+86,wy+wh*0.90),(wx+86,wy+wh*0.80),(wx+ww,wy+wh*0.80),(wx+ww,wy+wh),(wx,wy+wh)])}" fill="{K}"/>'
      f'</g>')
for i in range(1, 4):
    p.add(f'<line x1="{wx+ww*i/4}" y1="{wy}" x2="{wx+ww*i/4}" y2="{wy+wh}" stroke="{K}" stroke-width="3.0"/>')
for i in range(1, 5):
    p.add(f'<line x1="{wx}" y1="{wy+wh*i/5}" x2="{wx+ww}" y2="{wy+wh*i/5}" stroke="{K}" stroke-width="3.0"/>')
p.add(f'<rect x="{wx-10}" y="{wy+wh+6}" width="{ww+20}" height="7" fill="{K}"/>')

# the wall clock, stopped at the hour he left
ccx, ccy, ccr = 330, 54, 27
p.add(f'<circle cx="{ccx}" cy="{ccy}" r="{ccr+5}" fill="{K}"/>')
p.dial(ccx, ccy, ccr, 128, ticks=12, sw=1.8)
p.add(f'<line x1="{ccx}" y1="{ccy}" x2="{ccx-15}" y2="{ccy+9}" stroke="{K}" stroke-width="2.6" stroke-linecap="round"/>')
p.add(f'<path d="{poly([(ccx-7,ccy+ccr+4),(ccx+7,ccy+ccr+4),(ccx+4,ccy+ccr+20),(ccx-4,ccy+ccr+20)])}" fill="{K}"/>')

# a bench under the window: retorts, a candle, the notebook of the evening before
bx, by = 26, 300
p.add(f'<rect x="{bx}" y="{by}" width="94" height="6" fill="{K}"/>')
p.add(f'<rect x="{bx+6}" y="{by+6}" width="6" height="{FLOOR-by-6}" fill="{K}"/>')
p.add(f'<rect x="{bx+80}" y="{by+6}" width="6" height="{FLOOR-by-6}" fill="{K}"/>')
# retort
p.add(f'<circle cx="{bx+24}" cy="{by-14}" r="13" fill="{P}" stroke="{K}" stroke-width="1.8"/>')
p.contour_shade(p.clip_circle(bx + 24, by - 14, 12), bx + 24, by - 14, 3, 12, step=3.0, width=0.85)
p.add(f'<path d="M {bx+34} {by-22} Q {bx+52} {by-34} {bx+56} {by-12}" fill="none" stroke="{K}" stroke-width="1.8"/>')
# graduated cylinder
p.add(f'<rect x="{bx+60}" y="{by-30}" width="14" height="30" fill="{P}" stroke="{K}" stroke-width="1.6"/>')
p.add(f'<rect x="{bx+61}" y="{by-14}" width="12" height="14" fill="{B}"/>')
for i in range(6):
    p.add(f'<line x1="{bx+60}" y1="{by-26+i*4.6}" x2="{bx+67}" y2="{by-26+i*4.6}" stroke="{K}" stroke-width="0.9"/>')
# candle, just gone out
p.add(f'<rect x="{bx+2}" y="{by-26}" width="8" height="26" fill="{P}" stroke="{K}" stroke-width="1.5"/>')
p.add(f'<line x1="{bx+6}" y1="{by-26}" x2="{bx+6}" y2="{by-33}" stroke="{K}" stroke-width="1.6"/>')

# ---------------------------------------------------------------- the floor
p.add(f'<rect x="16" y="{FLOOR}" width="368" height="{600-FLOOR}" fill="{P}"/>')
p.add(f'<line x1="16" y1="{FLOOR}" x2="384" y2="{FLOOR}" stroke="{K}" stroke-width="2.6"/>')
for i in range(-1, 10):
    x = 16 + i * 44
    p.add(f'<line x1="{x}" y1="{FLOOR}" x2="{x-22}" y2="{FLOOR+34}" stroke="{K}" stroke-width="1.3"/>')
p.rule_field(p.clip_rect(16, FLOOR, 368, 34), (16, FLOOR, 384, FLOOR + 34), 0, 4.0, 0.9, K)

# ---------------------------------------------------------------- the frame
def bar(x1, y1, x2, y2, w=6.0):
    a = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
    d = poly([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)])
    p.add(f'<path d="{d}" fill="{P}" stroke="{K}" stroke-width="1.7"/>')
    p.add(f'<line x1="{x1+nx*0.5:.1f}" y1="{y1+ny*0.5:.1f}" x2="{x2+nx*0.5:.1f}" y2="{y2+ny*0.5:.1f}" '
          f'stroke="{K}" stroke-width="1.0"/>')

BASE = poly([(112, 438), (296, 438), (272, 404), (136, 404)])
p.add(f'<path d="{BASE}" fill="{P}" stroke="{K}" stroke-width="2.2"/>')
p.hatch(BASE, (112, 404, 296, 438), angle=-56, spacing=4.0, width=1.0)
p.add(f'<path d="{poly([(112,438),(296,438),(296,449),(112,449)])}" fill="{K}"/>')
# cast shadow on the floor
p.add(f'<path d="{poly([(96,449),(312,449),(348,470),(60,470)])}" fill="{P}" stroke="{K}" stroke-width="1.2"/>')
p.hatch(poly([(96, 449), (312, 449), (348, 470), (60, 470)]), (60, 449, 348, 470), angle=0, spacing=2.6, width=1.1)

for (x1, y1, x2, y2) in ((132, 406, 132, 248), (276, 406, 276, 248),
                         (158, 398, 158, 260), (250, 398, 250, 260)):
    bar(x1, y1, x2, y2, 7.0)
bar(124, 250, 284, 250, 7.5)
bar(152, 262, 256, 262, 6.0)
p.rivets([(128, 250), (280, 250), (132, 402), (276, 402), (158, 394), (250, 394)], r=2.2)

# ------------------------------------------------ the great quartz disc (1)
CX, CY, RR = 202, 278, 86
p.add(f'<circle cx="{CX}" cy="{CY}" r="{RR+8}" fill="{P}" stroke="{K}" stroke-width="2.0"/>')
p.add(f'<circle cx="{CX}" cy="{CY}" r="{RR}" fill="{P}"/>')
disc = p.clip_circle(CX, CY, RR - 1)
for i in range(28):
    a0 = 2 * math.pi * i / 28
    a1 = 2 * math.pi * (i + 1) / 28
    d = poly([(CX, CY), (CX + RR * math.cos(a0), CY + RR * math.sin(a0)),
              (CX + RR * math.cos(a1), CY + RR * math.sin(a1))])
    p.add(f'<path d="{d}" fill="none" stroke="{K}" stroke-width="1.0"/>')
    if i % 2 == 0:
        p.hatch(d, (CX - RR, CY - RR, CX + RR, CY + RR),
                angle=math.degrees(a0) + 90, spacing=3.4, width=1.0)
p.contour_shade(disc, CX, CY, 14, RR, step=7.0, width=0.95)
# the shadowed lower-right quadrant, cross-hatched twice over
sh = poly([(CX, CY),
           (CX + RR * math.cos(math.radians(-6)), CY + RR * math.sin(math.radians(-6))),
           (CX + RR * 1.42 * math.cos(math.radians(45)), CY + RR * 1.42 * math.sin(math.radians(45))),
           (CX + RR * math.cos(math.radians(96)), CY + RR * math.sin(math.radians(96)))])
shc = p.clip(sh)
shb = (CX - RR, CY - RR, CX + RR, CY + RR)
p.rule_field(p.clip(f"{sh}"), shb, 30, 4.4, 1.0, K)
p.add(f'<circle cx="{CX}" cy="{CY}" r="{RR}" fill="none" stroke="{K}" stroke-width="2.6"/>')
p.gear(CX, CY, 27, 18, tooth=6.5, fill=P, sw=1.6, spokes=6, bore=9)
p.add(f'<circle cx="{CX}" cy="{CY}" r="4.6" fill="{R}" stroke="{K}" stroke-width="1.2"/>')

# ------------------------------------------- the second disc (2), in brass
D2X, D2Y, D2R = 300, 232, 48
p.add(f'<circle cx="{D2X}" cy="{D2Y}" r="{D2R}" fill="{Y}" stroke="{K}" stroke-width="2.4"/>')
for i in range(20):
    a = 2 * math.pi * i / 20
    p.add(f'<line x1="{D2X + 15*math.cos(a):.1f}" y1="{D2Y + 15*math.sin(a):.1f}" '
          f'x2="{D2X + (D2R-2)*math.cos(a):.1f}" y2="{D2Y + (D2R-2)*math.sin(a):.1f}" '
          f'stroke="{K}" stroke-width="2.0"/>')
p.add(f'<circle cx="{D2X}" cy="{D2Y}" r="{D2R-9}" fill="none" stroke="{K}" stroke-width="2.0"/>')
p.gear(D2X, D2Y, 16, 14, tooth=5.0, fill=P, sw=1.5, spokes=4, bore=5)

# -------------------------------------------------------------- the saddle
SD = poly([(168, 368), (246, 368), (253, 382), (240, 394), (176, 394), (162, 382)])
p.add(f'<path d="{SD}" fill="{K}"/>')
p.add(f'<path d="M 172 373 L 244 373" stroke="{P}" stroke-width="1.8"/>')
p.add(f'<path d="M 178 379 L 238 379" stroke="{P}" stroke-width="1.1"/>')
bar(206, 394, 206, 422, 5.5)

# levers: forward (vermilion), and the one that stops it
p.add(f'<path d="M 190 368 L 176 316" stroke="{K}" stroke-width="5.0" stroke-linecap="round"/>')
p.add(f'<circle cx="175" cy="312" r="8.5" fill="{R}" stroke="{K}" stroke-width="1.8"/>')
p.add(f'<path d="M 224 368 L 240 322" stroke="{K}" stroke-width="5.0" stroke-linecap="round"/>')
p.add(f'<circle cx="241" cy="318" r="8.5" fill="{P}" stroke="{K}" stroke-width="1.8"/>')
p.add(f'<circle cx="241" cy="318" r="3.2" fill="{K}"/>')

# ivory guide-rails (5)
for y in (340, 351):
    p.add(f'<line x1="146" y1="{y}" x2="266" y2="{y-7}" stroke="{K}" stroke-width="2.8"/>')
    p.add(f'<line x1="146" y1="{y-1.3}" x2="266" y2="{y-8.3}" stroke="{P}" stroke-width="1.1"/>')

# a bar of blue quartz threaded through the frame
qd = poly([(118, 300), (290, 282), (290, 293), (118, 311)])
p.add(f'<path d="{qd}" fill="{B}" stroke="{K}" stroke-width="1.8"/>')
p.add(f'<line x1="120" y1="303" x2="288" y2="285" stroke="{P}" stroke-width="1.3"/>')

# index dials (7) and the differential train (6)
p.dial(136, 410, 18, 212, ticks=24)
p.dial(175, 417, 14, 64, ticks=16)
p.dial(234, 417, 14, 305, ticks=16)
p.dial(272, 410, 18, 139, ticks=24)
p.gear(180, 430, 13, 12, tooth=4.4, fill=P, sw=1.3, spokes=3, bore=3.6)
p.gear(206, 426, 10, 10, tooth=4.0, fill=P, sw=1.3, bore=2.8)
p.gear(232, 430, 13, 12, tooth=4.4, fill=P, sw=1.3, spokes=3, bore=3.6)

# ------------------------------------------------------ the Time Traveller
fx, fy = 344, 449
p.add(f'<path d="{poly([(fx-14,fy),(fx+14,fy),(fx+12,fy-54),(fx+6,fy-64),(fx-8,fy-64),(fx-14,fy-52)])}" fill="{K}"/>')
p.add(f'<path d="{poly([(fx-3,fy-64),(fx+4,fy-64),(fx+5,fy-45),(fx-4,fy-45)])}" fill="{P}"/>')
p.add(f'<circle cx="{fx-1}" cy="{fy-73}" r="9.0" fill="{K}"/>')
p.add(f'<rect x="{fx-12}" y="{fy-82}" width="22" height="4" fill="{K}"/>')
p.add(f'<rect x="{fx-8}" y="{fy-95}" width="14" height="14" fill="{K}"/>')
p.add(f'<path d="M {fx-14} {fy-48} L {fx-32} {fy-32}" stroke="{K}" stroke-width="5.4" stroke-linecap="round"/>')
p.add(f'<rect x="{fx-48}" y="{fy-40}" width="19" height="14" fill="{P}" stroke="{K}" stroke-width="1.5"/>')
p.rule_field(p.clip_rect(fx - 48, fy - 40, 19, 14), (fx - 48, fy - 40, fx - 29, fy - 26), 0, 3.4, 0.9, K)

# ------------------------------------------------------------ numbered keys
for (n, x, y) in (("1", CX - 66, CY - 62), ("2", 300, 176), ("3", 206, 358),
                  ("4", 152, 296), ("5", 274, 330), ("6", 206, 447), ("7", 112, 410)):
    p.add(f'<circle cx="{x}" cy="{y}" r="8.4" fill="{P}" stroke="{K}" stroke-width="1.8"/>')
    p.text(x, y + 4.2, n, size=12, anchor="middle", weight="bold")

# ------------------------------------------------------------- the lettering
p.add(f'<rect x="0" y="480" width="400" height="120" fill="{P}"/>')
p.add(f'<line x1="16" y1="482" x2="384" y2="482" stroke="{K}" stroke-width="3.2"/>')
p.text(200, 509, "THE TIME MACHINE", size=26, anchor="middle", spacing=1.4)
p.add(f'<line x1="104" y1="517" x2="296" y2="517" stroke="{K}" stroke-width="1.3"/>')
p.text(200, 530, "Fig. 1.  General arrangement, as exhibited at Richmond.", size=11,
       anchor="middle", style="italic")
LEG = [("1", "quartz disc, upper"), ("5", "ivory guide-rails"),
       ("2", "brass disc, lower"), ("6", "differential train"),
       ("3", "saddle, starting lever"), ("7", "index dials, four")]
for i in range(0, 6, 2):
    yy = 543 + (i // 2) * 12.0
    for j, (n, s) in enumerate(LEG[i:i + 2]):
        x = 30 + j * 184
        p.text(x, yy, f"{n}.", size=11, weight="bold")
        p.text(x + 14, yy, s, size=11)
p.text(200, 578, "H. G. WELLS · BORN BROMLEY 21 SEPTEMBER 1866 · 160 YEARS",
       size=9.2, anchor="middle", spacing=0.3)

p.border(m=9, rules=(3.2, 1.3), gap=5)
p.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "1_morning_the_time_machine.svg"),
       names=(K, P, R, Y, B))
