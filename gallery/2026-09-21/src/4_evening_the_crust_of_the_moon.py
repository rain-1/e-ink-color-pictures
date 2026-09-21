#!/usr/bin/env python3
"""18 — THE FIRST MEN IN THE MOON (1901): section through the crust.

Evening is the hour for a section drawing: everything above ground going dim,
everything below it lit. The rock is the one flat colour and it holds the
whole plate together; the galleries are cut out of it in white, the lamps and
the Grand Lunar's hall are the only yellow, and the Earth hangs in the sky
where our moon would be. Selenites are drawn at the scale the diagram gives
them, which is very small indeed. A depth scale runs down the left margin.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plate import Plate, K, P, R, Y, B, poly

p = Plate(bg=B)
rnd = random.Random(1901)

SURF = 176          # the lunar surface
FLOORB = 524        # bottom of the section
LM = 40             # left margin for the depth scale


# ------------------------------------------------------------------- sky
p.add(f'<rect x="0" y="0" width="400" height="{SURF}" fill="{B}"/>')
for _ in range(150):
    x, y = rnd.uniform(4, 396), rnd.uniform(4, SURF - 20)
    p.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(0.7, 1.7):.2f}" fill="{P}"/>')
# the Earth, gibbous, with its continents blocked in
EX, EY, ER = 306, 58, 38
p.add(f'<circle cx="{EX}" cy="{EY}" r="{ER+6}" fill="{B}" stroke="{P}" stroke-width="1.0"/>')
p.add(f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="{P}" stroke="{P}" stroke-width="1.0"/>')
ec = p.clip_circle(EX, EY, ER)
p.add(f'<g clip-path="url(#{ec})">')
p.add(f'<path d="{poly([(EX-ER-2, EY-ER-2), (EX-ER*0.30, EY-ER-2), (EX-ER*0.62, EY), (EX-ER*0.30, EY+ER+2), (EX-ER-2, EY+ER+2)])}" fill="{B}"/>')
# a scrap of coastline and cloud
for (ox, oy, rx_, ry_) in ((8, -14, 15, 9), (2, 10, 13, 11), (24, 20, 9, 6), (-10, 22, 8, 5)):
    p.add(f'<ellipse cx="{EX+ox}" cy="{EY+oy}" rx="{rx_}" ry="{ry_}" fill="{B}" opacity="1"/>')
p.rule_field(ec, (EX - ER, EY - ER, EX + ER, EY + ER), 0, 5.0, 1.0, B,
             taper=lambda t: max(0.0, (t - 0.55) * 2.6))
p.add('</g>')
p.text(EX, EY + ER + 18, "THE EARTH", size=9.4, color=P, anchor="middle", spacing=1.0)

# ------------------------------------------------- the surface and the crags
crag = [(0, SURF)]
for i in range(49):
    x = i * 400 / 48
    h = (20 + 16 * math.sin(i * 0.9) + 10 * math.sin(i * 2.3) + rnd.uniform(0, 9))
    if 150 < x < 250:
        h *= 0.35                      # the crater floor, scoured flat
    crag.append((x, SURF - h))
crag.append((400, SURF))
p.add(f'<path d="{poly(crag)}" fill="{P}" stroke="{K}" stroke-width="2.0"/>')
cragc = p.clip(poly(crag))
p.rule_field(cragc, (0, SURF - 60, 400, SURF), 62, 4.4, 1.0, K,
             taper=lambda t: max(0.0, (t - 0.25) * 1.6))

# the crater lid, thrown back on its hinge
p.add(f'<path d="{poly([(150, SURF-6), (250, SURF-6), (250, SURF), (150, SURF)])}" fill="{K}"/>')
p.add(f'<path d="{poly([(152, SURF-7), (196, SURF-52), (206, SURF-44), (164, SURF-6)])}" fill="{P}" stroke="{K}" stroke-width="2.0"/>')
p.hatch(poly([(152, SURF - 7), (196, SURF - 52), (206, SURF - 44), (164, SURF - 6)]),
        (150, SURF - 56, 210, SURF), angle=18, spacing=3.4, width=1.0)

# the sphere, at rest on the floor
SPX, SPY, SPR = 268, SURF - 20, 20
p.add(f'<circle cx="{SPX}" cy="{SPY}" r="{SPR}" fill="{P}" stroke="{K}" stroke-width="2.2"/>')
for i in range(5):
    rx = SPR * math.cos(math.pi * (i + 1) / 6)
    p.add(f'<ellipse cx="{SPX}" cy="{SPY}" rx="{abs(rx):.1f}" ry="{SPR}" fill="none" stroke="{K}" stroke-width="1.0"/>')
for i in range(3):
    yy = SPY - SPR * 0.55 + i * SPR * 0.55
    hw = math.sqrt(max(0.0, SPR ** 2 - (yy - SPY) ** 2))
    p.add(f'<line x1="{SPX-hw:.1f}" y1="{yy:.1f}" x2="{SPX+hw:.1f}" y2="{yy:.1f}" stroke="{K}" stroke-width="1.0"/>')
p.add(f'<rect x="{SPX-6}" y="{SPY-SPR-5}" width="12" height="6" fill="{K}"/>')

# Bedford and Cavor, at the scale the diagram allows
for (fx, fh) in ((222, 32), (238, 28)):
    fy = SURF - 4
    p.add(f'<path d="{poly([(fx-4, fy), (fx+4, fy), (fx+3, fy-fh*0.58), (fx-3, fy-fh*0.58)])}" fill="{K}"/>')
    p.add(f'<path d="{poly([(fx-5, fy-fh*0.55), (fx+5, fy-fh*0.55), (fx+4, fy-fh*0.86), (fx-4, fy-fh*0.86)])}" fill="{K}"/>')
    p.add(f'<circle cx="{fx}" cy="{fy-fh*0.94}" r="{fh*0.15:.1f}" fill="{K}"/>')

# lunar vegetation, the quick-growing spines
for _ in range(54):
    vx = rnd.uniform(4, 396)
    if 150 < vx < 258:
        continue
    vy = SURF - 4 - rnd.uniform(0, 16)
    L = rnd.uniform(9, 26)
    a = rnd.uniform(-0.5, 0.5)
    p.add(f'<path d="M {vx:.1f} {vy:.1f} l {math.sin(a)*L:.1f} {-math.cos(a)*L:.1f}" '
          f'stroke="{K}" stroke-width="1.6"/>')
    for k in range(3):
        t = (k + 1) / 4
        px, py = vx + math.sin(a) * L * t, vy - math.cos(a) * L * t
        for sgn in (-1, 1):
            p.add(f'<path d="M {px:.1f} {py:.1f} l {sgn*4.5:.1f} {-3.5:.1f}" stroke="{K}" stroke-width="1.2"/>')

# ------------------------------------------------------------- the crust
p.add(f'<rect x="0" y="{SURF}" width="400" height="{FLOORB-SURF}" fill="{B}"/>')
p.add(f'<line x1="0" y1="{SURF}" x2="400" y2="{SURF}" stroke="{K}" stroke-width="2.6"/>')
rock = p.clip_rect(0, SURF, 400, FLOORB - SURF)
# strata: long sagging lines, cross-hatched where the rock is oldest
for i in range(17):
    yy = SURF + 8 + i * 20
    pts = [(x, yy + 9 * math.sin(x / 90 + i * 0.7) + 5 * math.sin(x / 37 + i)) for x in range(-10, 412, 14)]
    p.add(f'<g clip-path="url(#{rock})"><path d="M ' + " L ".join(f"{a:.1f},{b:.1f}" for a, b in pts) +
          f'" fill="none" stroke="{K}" stroke-width="{1.5 if i % 3 == 0 else 1.0}"/></g>')
p.rule_field(rock, (0, SURF, 400, FLOORB), 58, 8.5, 1.0, K)


def gallery(x0, y0, x1, y1, w, label=None, lx=0, ly=0):
    """A tunnel cut out of the rock: white, with a black lining and a floor line."""
    a = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
    d = poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)])
    p.add(f'<path d="{d}" fill="{P}" stroke="{K}" stroke-width="2.2"/>')
    p.add(f'<line x1="{x0-nx*0.55:.1f}" y1="{y0-ny*0.55:.1f}" x2="{x1-nx*0.55:.1f}" '
          f'y2="{y1-ny*0.55:.1f}" stroke="{K}" stroke-width="1.1"/>')
    # ribs every so often
    L = math.hypot(x1 - x0, y1 - y0)
    for i in range(int(L / 26)):
        t = (i + 0.5) / max(1, int(L / 26))
        mx, my = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        p.add(f'<line x1="{mx+nx:.1f}" y1="{my+ny:.1f}" x2="{mx-nx:.1f}" y2="{my-ny:.1f}" '
              f'stroke="{K}" stroke-width="1.0"/>')
    return d


def selenite(cx, base, h, seed=0, arms_up=False):
    """Big brain-case, narrow body, insect limbs — a diagram-scale Selenite."""
    r = random.Random(seed)
    u = h / 10.0
    p.add(f'<ellipse cx="{cx}" cy="{base-8.2*u}" rx="{2.3*u:.1f}" ry="{2.0*u:.1f}" fill="{K}"/>')
    p.add(f'<path d="{poly([(cx-1.0*u, base-6.6*u), (cx+1.0*u, base-6.6*u), (cx+0.7*u, base-2.4*u), (cx-0.7*u, base-2.4*u)])}" fill="{K}"/>')
    for sgn in (-1, 1):
        p.add(f'<path d="M {cx+sgn*0.6*u:.1f} {base-2.4*u:.1f} L {cx+sgn*1.9*u:.1f} '
              f'{base-1.1*u:.1f} L {cx+sgn*1.3*u:.1f} {base:.1f}" fill="none" stroke="{K}" stroke-width="{max(1.2, 0.55*u):.1f}"/>')
        ay = base - 5.6 * u
        if arms_up:
            p.add(f'<path d="M {cx+sgn*0.9*u:.1f} {ay:.1f} L {cx+sgn*2.6*u:.1f} {ay-1.6*u:.1f} '
                  f'L {cx+sgn*2.2*u:.1f} {ay-3.4*u:.1f}" fill="none" stroke="{K}" stroke-width="{max(1.1, 0.45*u):.1f}"/>')
        else:
            p.add(f'<path d="M {cx+sgn*0.9*u:.1f} {ay:.1f} L {cx+sgn*2.4*u:.1f} {ay+1.2*u:.1f} '
                  f'L {cx+sgn*2.0*u:.1f} {ay+3.0*u:.1f}" fill="none" stroke="{K}" stroke-width="{max(1.1, 0.45*u):.1f}"/>')


def lamp(x, y, r=5.5):
    p.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{Y}" stroke="{K}" stroke-width="1.5"/>')
    for i in range(8):
        a = 2 * math.pi * i / 8
        p.add(f'<line x1="{x+r*1.25*math.cos(a):.1f}" y1="{y+r*1.25*math.sin(a):.1f}" '
              f'x2="{x+r*2.0*math.cos(a):.1f}" y2="{y+r*2.0*math.sin(a):.1f}" stroke="{Y}" stroke-width="1.6"/>')
    p.add(f'<line x1="{x}" y1="{y-r}" x2="{x}" y2="{y-r-7}" stroke="{K}" stroke-width="1.5"/>')


# the great shaft, straight down from the crater
gallery(200, SURF, 200, 320, 30)
gallery(200, 320, 200, 424, 20)
# the winding chain and its cage
p.add(f'<line x1="196" y1="{SURF+4}" x2="196" y2="308" stroke="{K}" stroke-width="1.4"/>')
p.add(f'<line x1="204" y1="{SURF+4}" x2="204" y2="308" stroke="{K}" stroke-width="1.4"/>')
p.add(f'<rect x="190" y="248" width="20" height="16" fill="{P}" stroke="{K}" stroke-width="2.0"/>')
for i in range(3):
    p.add(f'<line x1="{192+i*6}" y1="248" x2="{192+i*6}" y2="264" stroke="{K}" stroke-width="1.1"/>')

# horizontal galleries
gallery(52, 232, 348, 240, 20)
gallery(58, 300, 186, 296, 17)
gallery(214, 356, 362, 350, 17)
gallery(74, 404, 320, 410, 16)
# connectors
gallery(104, 240, 96, 300, 13)
gallery(310, 238, 322, 350, 13)
gallery(140, 298, 128, 406, 12)
gallery(288, 354, 274, 408, 12)

# the Grand Lunar's hall
HX, HY, HRX, HRY = 200, 470, 126, 40
p.add(f'<ellipse cx="{HX}" cy="{HY}" rx="{HRX}" ry="{HRY}" fill="{Y}" stroke="{K}" stroke-width="2.6"/>')
hall = p.clip(f"M {HX-HRX} {HY} a {HRX} {HRY} 0 1 0 {2*HRX} 0 a {HRX} {HRY} 0 1 0 {-2*HRX} 0 Z")
for i in range(11):
    a = math.pi * (i + 0.5) / 11
    p.add(f'<g clip-path="url(#{hall})"><line x1="{HX+HRX*math.cos(a):.1f}" y1="{HY+HRY*math.sin(a)*0.1:.1f}" '
          f'x2="{HX+HRX*0.2*math.cos(a):.1f}" y2="{HY-HRY:.1f}" stroke="{K}" stroke-width="1.2"/></g>')
p.add(f'<line x1="{HX-HRX+6}" y1="{HY+HRY*0.42:.0f}" x2="{HX+HRX-6}" y2="{HY+HRY*0.42:.0f}" stroke="{K}" stroke-width="2.0"/>')
# the Grand Lunar himself: almost all head
p.add(f'<ellipse cx="{HX}" cy="{HY-2}" rx="24" ry="20" fill="{K}"/>')
p.add(f'<ellipse cx="{HX}" cy="{HY-6}" rx="17" ry="13" fill="{Y}"/>')
for i in range(7):
    a = math.pi * i / 6
    p.add(f'<path d="M {HX-15*math.cos(a):.1f} {HY-6-11*math.sin(a):.1f} q 4 6 8 0" fill="none" stroke="{K}" stroke-width="1.2"/>')
p.add(f'<path d="{poly([(HX-5, HY+16), (HX+5, HY+16), (HX+3, HY+28), (HX-3, HY+28)])}" fill="{K}"/>')
for sgn in (-1, 1):
    p.add(f'<path d="M {HX+sgn*4} {HY+20} L {HX+sgn*15} {HY+26}" stroke="{K}" stroke-width="2.0"/>')
# attendants ringing the hall
for dx in (-92, -70, -50, 50, 70, 92):
    selenite(HX + dx, HY + 30, 22, seed=abs(dx), arms_up=(dx > 0))
lamp(HX - 108, HY - 14)
lamp(HX + 108, HY - 14)

# workers in the galleries
for (sx, sb, hh, up) in ((92, 240, 18, False), (150, 240, 16, True), (260, 240, 17, False),
                         (330, 240, 15, True), (86, 300, 16, False), (160, 296, 15, True),
                         (250, 356, 16, False), (330, 350, 15, True), (110, 404, 15, False),
                         (200, 410, 16, True), (270, 408, 15, False)):
    selenite(sx, sb - 2, hh, seed=sx, arms_up=up)
for (lx_, ly_) in ((120, 228), (230, 232), (300, 232), (70, 292), (300, 346), (160, 400), (250, 402)):
    lamp(lx_, ly_, 4.6)

# machinery in a side chamber
p.add(f'<rect x="46" y="336" width="86" height="52" fill="{P}" stroke="{K}" stroke-width="2.2"/>')
p.add(f'<circle cx="74" cy="362" r="19" fill="{P}" stroke="{K}" stroke-width="2.4"/>')
p.add(f'<circle cx="74" cy="362" r="14" fill="none" stroke="{K}" stroke-width="1.2"/>')
for _i in range(6):
    _a = math.pi * _i / 3
    p.add(f'<line x1="{74+4*math.cos(_a):.1f}" y1="{362+4*math.sin(_a):.1f}" '
          f'x2="{74+14*math.cos(_a):.1f}" y2="{362+14*math.sin(_a):.1f}" stroke="{K}" stroke-width="1.6"/>')
p.add(f'<circle cx="74" cy="362" r="4" fill="{K}"/>')
p.gear(108, 354, 10, 10, tooth=4.2, fill=P, sw=1.5, bore=3.4)
p.add(f'<rect x="96" y="370" width="30" height="10" fill="{K}"/>')
p.add(f'<line x1="74" y1="362" x2="106" y2="356" stroke="{K}" stroke-width="1.4"/>')
selenite(56, 386, 14, seed=99)

# ------------------------------------------------------------ depth scale
p.add(f'<line x1="{LM-16}" y1="{SURF}" x2="{LM-16}" y2="{FLOORB}" stroke="{P}" stroke-width="1.6"/>')
for i in range(8):
    yy = SURF + i * 50
    if yy > FLOORB:
        break
    p.add(f'<line x1="{LM-21}" y1="{yy}" x2="{LM-16}" y2="{yy}" stroke="{P}" stroke-width="1.6"/>')
    p.text(LM - 23, yy + 3.4, str(i), size=9, color=P, anchor="end")
p.text(LM - 16, SURF - 8, "DEPTH", size=8.6, color=P, anchor="middle", spacing=0.6)
p.text(LM - 16, FLOORB + 12, "MILES", size=8.6, color=K, anchor="middle", spacing=0.6)

# ------------------------------------------------------------------ labels
def note(x, y, s, anchor="start", color=P, size=9.4):
    p.text(x, y, s, size=size, color=color, anchor=anchor, style="italic")

note(206, SURF + 22, "The great shaft")
note(356, 226, "Galleries", anchor="end")
note(44, 330, "Engine chamber")
note(HX, HY - HRY - 12, "THE HALL OF THE GRAND LUNAR", anchor="middle", color=P, size=9.4)
note(150, SURF - 46, "the lid", anchor="end", color=K)
note(292, SURF - 44, "the sphere", color=K)

# ----------------------------------------------------------- caption plate
p.add(f'<rect x="0" y="{FLOORB}" width="400" height="{600-FLOORB}" fill="{P}"/>')
p.add(f'<line x1="0" y1="{FLOORB}" x2="400" y2="{FLOORB}" stroke="{K}" stroke-width="3.0"/>')
p.text(200, FLOORB + 28, "THE FIRST MEN IN THE MOON", size=20, anchor="middle", spacing=0.8)
p.add(f'<line x1="86" y1="{FLOORB+36}" x2="314" y2="{FLOORB+36}" stroke="{K}" stroke-width="1.2"/>')
p.text(200, FLOORB + 50, "Fig. 3.  Vertical section through the crust, from the crater to the Hall.",
       size=10, anchor="middle", style="italic")
p.text(200, FLOORB + 66, "H. G. WELLS, 1901  ·  “We are on the moon’s inside.”",
       size=9.4, anchor="middle")

p.add(f'<rect x="5" y="5" width="390" height="590" fill="none" stroke="{K}" stroke-width="3.0"/>')
p.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "4_evening_the_crust_of_the_moon.svg"),
       names=(K, P, Y, B))
