#!/usr/bin/env python3
"""14 — THE WAR OF THE WORLDS (1898): the machines come up the valley.

Not a plate this time but a full-bleed illustration, in the manner of the
inky 1906 Alvim Correa edition that Wells liked better than his own prose.
The sky is one flat red and every value in it is made with ruled lines that
thin towards the light, the way a wood-engraver made a sky. The tripods are
generated: hood, cowl-rings, tentacles and three jointed legs from a few
parameters, so each one stands differently. Yellow appears exactly twice, at
the lens and along the heat-ray, and nowhere else.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plate import Plate, K, P, R, Y, poly

p = Plate(bg=R)
rnd = random.Random(1898)

HOR = 372          # the far bank
CAP = 492          # caption band
BEAM = (232, 150)  # where the ray starts


# --------------------------------------------------------------------- sky
sky = p.clip_rect(0, 0, 400, HOR)
# ruled cloud bands, opening out around the glare
p.rule_field(sky, (0, 0, 400, HOR), 4, 6.0, 1.3, K,
             taper=lambda t: max(0.0, min(1.0, abs(t - 0.62) * 2.6 - 0.05)))
p.rule_field(sky, (0, 0, 400, HOR), -3, 11.0, 1.0, K,
             taper=lambda t: max(0.0, min(1.0, abs(t - 0.55) * 2.2)))
# glare: white behind the horizon, thrown up in rays
glare = []
for i in range(26):
    a = math.pi + math.pi * i / 25
    glare.append((BEAM[0] + 520 * math.cos(a), HOR + 30 + 520 * math.sin(a) * 0.62))
p.add(f'<g clip-path="url(#{sky})">')
for i in range(40):
    a = -math.pi + math.pi * (i + 0.5) / 40
    if i % 7:
        continue
    w = 0.008
    d = poly([(BEAM[0], HOR - 6),
              (BEAM[0] + 640 * math.cos(a - w), HOR - 6 + 640 * math.sin(a - w)),
              (BEAM[0] + 640 * math.cos(a + w), HOR - 6 + 640 * math.sin(a + w))])
    p.add(f'<path d="{d}" fill="{P}" opacity="1"/>')
p.add('</g>')
# a low white bank of smoke along the horizon, ruled back into red
smoke = [(0, HOR)]
for i in range(41):
    x = i * 10
    smoke.append((x, HOR - 26 - 30 * math.exp(-((x - 230) / 110) ** 2)
                  - 12 * math.exp(-((x - 60) / 50) ** 2) - rnd.uniform(0, 7)))
smoke.append((400, HOR))
p.add(f'<path d="{poly(smoke)}" fill="{P}"/>')
p.rule_field(p.clip(poly(smoke)), (0, HOR - 80, 400, HOR), 6, 4.6, 1.0, R,
             taper=lambda t: max(0.0, 1.0 - t * 1.5))

# crows going the other way
for (bx, by, bs) in ((58, 96, 7), (78, 112, 5), (44, 126, 6), (330, 84, 6), (352, 104, 5)):
    p.add(f'<path d="M {bx-bs} {by} q {bs*0.5} {-bs*0.8} {bs} 0 q {bs*0.5} {-bs*0.8} {bs} 0" '
          f'fill="none" stroke="{K}" stroke-width="1.8"/>')


# ------------------------------------------------------------------ tripods
def tripod(hx, hy, s, phase=0.0, seed=0, ray=False, tentacles=7):
    """A fighting-machine: cowl, rings, tentacles, three jointed legs."""
    r = random.Random(seed)
    hw, hh = 34 * s, 21 * s          # hood
    # hood
    p.add(f'<ellipse cx="{hx}" cy="{hy}" rx="{hw}" ry="{hh}" fill="{K}"/>')
    p.add(f'<path d="{poly([(hx-hw, hy), (hx+hw, hy), (hx+hw*0.72, hy+hh*1.30), (hx-hw*0.72, hy+hh*1.30)])}" fill="{K}"/>')
    # cowl rings, drawn in red over the black so they read as turned metal
    for i in range(4):
        yy = hy - hh * 0.55 + i * hh * 0.52
        rr = hw * (0.98 - 0.12 * i)
        p.add(f'<path d="M {hx-rr:.1f} {yy:.1f} q {rr:.1f} {hh*0.42:.1f} {2*rr:.1f} 0" '
              f'fill="none" stroke="{R}" stroke-width="{1.6*s:.1f}"/>')
    # the lens
    p.add(f'<ellipse cx="{hx+hw*0.22:.1f}" cy="{hy+hh*0.12:.1f}" rx="{hw*0.20:.1f}" '
          f'ry="{hh*0.30:.1f}" fill="{Y}" stroke="{K}" stroke-width="{1.4*s:.1f}"/>')
    p.add(f'<ellipse cx="{hx+hw*0.22:.1f}" cy="{hy+hh*0.12:.1f}" rx="{hw*0.07:.1f}" '
          f'ry="{hh*0.12:.1f}" fill="{K}"/>')
    # tentacles
    for i in range(tentacles):
        t = (i + 0.5) / tentacles
        ox = hx - hw * 0.66 + hw * 1.32 * t
        L = 34 * s * (0.6 + 0.7 * r.random())
        sway = (r.random() - 0.5) * 30 * s
        p.add(f'<path d="M {ox:.1f} {hy+hh*1.20:.1f} C {ox+sway*0.4:.1f} {hy+hh*1.2+L*0.45:.1f} '
              f'{ox+sway:.1f} {hy+hh*1.2+L*0.7:.1f} {ox+sway*0.6:.1f} {hy+hh*1.2+L:.1f}" '
              f'fill="none" stroke="{K}" stroke-width="{max(1.6, 3.4*s):.1f}" stroke-linecap="round"/>')
    # the carrier basket slung behind
    p.add(f'<path d="{poly([(hx-hw*1.02, hy+hh*0.5), (hx-hw*0.62, hy+hh*0.5), (hx-hw*0.72, hy+hh*1.5), (hx-hw*1.10, hy+hh*1.4)])}" fill="{K}"/>')

    # three legs: hip -> knee -> foot, the far one shorter
    hipy = hy + hh * 1.25
    legs = ((-1.0, 1.00, 0.0), (0.25, 0.92, 1.9), (0.85, 0.72, 3.5))
    for (dirn, scale, ph) in legs:
        reach = 150 * s * scale
        knee_out = dirn * 64 * s + 16 * s * math.sin(phase + ph)
        footx = hx + dirn * 120 * s + 26 * s * math.sin(phase + ph * 1.3)
        kneex = hx + knee_out
        kneey = hipy + reach * 0.44
        footy = hipy + reach
        for (x0, y0, x1, y1, w0, w1) in ((hx, hipy, kneex, kneey, 7.0 * s, 4.6 * s),
                                         (kneex, kneey, footx, footy, 4.6 * s, 2.6 * s)):
            a = math.atan2(y1 - y0, x1 - x0)
            nx, ny = -math.sin(a), math.cos(a)
            d = poly([(x0 + nx * w0, y0 + ny * w0), (x1 + nx * w1, y1 + ny * w1),
                      (x1 - nx * w1, y1 - ny * w1), (x0 - nx * w0, y0 - ny * w0)])
            p.add(f'<path d="{d}" fill="{K}"/>')
            # segment joints, ruled in red across the black
            seg = math.hypot(x1 - x0, y1 - y0)
            for j in range(int(seg / (13 * s)) + 1):
                t = (j + 0.5) / max(1, int(seg / (13 * s)) + 1)
                jx, jy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
                ww = (w0 + (w1 - w0) * t) * 0.9
                p.add(f'<line x1="{jx+nx*ww:.1f}" y1="{jy+ny*ww:.1f}" x2="{jx-nx*ww:.1f}" '
                      f'y2="{jy-ny*ww:.1f}" stroke="{R}" stroke-width="{max(0.9, 1.3*s):.1f}"/>')
        p.add(f'<circle cx="{kneex:.1f}" cy="{kneey:.1f}" r="{7.5*s:.1f}" fill="{K}"/>')
        p.add(f'<circle cx="{kneex:.1f}" cy="{kneey:.1f}" r="{3.4*s:.1f}" fill="{R}"/>')
        # splayed foot
        p.add(f'<path d="{poly([(footx-11*s, footy), (footx+11*s, footy), (footx+5*s, footy+5*s), (footx-5*s, footy+5*s)])}" fill="{K}"/>')

    if ray:
        # the heat-ray: a yellow wedge with a white core, thrown at the town
        tip = (346, HOR - 22)
        src = (hx + hw * 0.30, hy + hh * 0.9)
        for (col, spread) in ((Y, 9.5), (P, 3.4)):
            d = poly([(src[0], src[1] - spread * 0.4), (tip[0], tip[1] - spread),
                      (tip[0], tip[1] + spread), (src[0], src[1] + spread * 0.4)])
            p.add(f'<path d="{d}" fill="{col}"/>')
        for k in range(16):
            a = rnd.uniform(0, 2 * math.pi)
            L = rnd.uniform(10, 34)
            p.add(f'<line x1="{tip[0]}" y1="{tip[1]}" x2="{tip[0]+L*math.cos(a):.1f}" '
                  f'y2="{tip[1]+L*math.sin(a):.1f}" stroke="{Y}" stroke-width="2.0"/>')


# ------------------------------------------------------------ the far shore
town = [(0, HOR)]
x = 0
while x < 400:
    w = rnd.uniform(14, 34)
    h = rnd.uniform(12, 34)
    town += [(x, HOR - h), (x + w * 0.5, HOR - h - rnd.uniform(0, 12)), (x + w, HOR - h * 0.8)]
    x += w
town += [(400, HOR)]
p.add(f'<path d="{poly(town)}" fill="{K}"/>')
# a church spire and chimneys that survive the skyline
p.add(f'<path d="{poly([(96, HOR), (96, HOR-46), (104, HOR-78), (112, HOR-46), (112, HOR)])}" fill="{K}"/>')
p.add(f'<rect x="102" y="{HOR-96}" width="4" height="20" fill="{K}"/>')
for (cx_, ch_) in ((150, 40), (168, 52), (286, 44), (306, 58), (60, 36)):
    p.add(f'<rect x="{cx_}" y="{HOR-ch_}" width="7" height="{ch_}" fill="{K}"/>')
# white smoke boiling off the burning quarter: heads stacked and ruled
for (sx, base_w, hgt, sd) in ((330, 15, 86, 2), (292, 11, 58, 5), (366, 12, 66, 9)):
    pr = random.Random(sd)
    heads = []
    for i in range(11):
        t = i / 10
        r_ = base_w * (0.42 + 0.72 * t)
        cx_ = sx + 30 * t * math.sin(t * 2.8 + sd) + pr.uniform(-5, 5)
        cy_ = HOR - 6 - hgt * t
        heads.append((cx_, cy_, r_))
    grp = "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{c:.1f}"/>' for a, b, c in heads)
    p.add(f'<g fill="{P}" stroke="{K}" stroke-width="2.0">{grp}</g>')
    p.add(f'<g fill="{P}" stroke="none">{grp}</g>')
    cid = p.uid("smk")
    p.defs.append(f'<clipPath id="{cid}">' + "".join(
        f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{c:.1f}"/>' for a, b, c in heads) + '</clipPath>')
    # curls of shadow inside the plume, in red
    for (a, b, c) in heads[::2]:
        p.add(f'<g clip-path="url(#{cid})"><path d="M {a-c*0.8:.1f} {b+c*0.25:.1f} '
              f'q {c*0.55:.1f} {c*0.60:.1f} {c*1.3:.1f} {-c*0.1:.1f}" fill="none" '
              f'stroke="{R}" stroke-width="2.0"/></g>')
    p.rule_field(cid, (sx - 80, HOR - hgt - 40, sx + 80, HOR), 74, 6.5, 1.2, R,
                 taper=lambda t: max(0.0, 1.0 - t * 1.4))

# ---------------------------------------------------------------- the river
BANK = 452
p.add(f'<rect x="0" y="{HOR}" width="400" height="{BANK-HOR}" fill="{P}"/>')
p.add(f'<line x1="0" y1="{HOR}" x2="400" y2="{HOR}" stroke="{K}" stroke-width="2.4"/>')
riv = p.clip_rect(0, HOR, 400, BANK - HOR)
p.rule_field(riv, (0, HOR, 400, BANK), 0, 6.0, 1.2, K,
             taper=lambda t: max(0.0, 0.25 + t * 0.9))

# tripods, farthest first
tripod(92, 196, 0.46, phase=1.2, seed=3, tentacles=5)
tripod(322, 168, 0.40, phase=2.6, seed=7, tentacles=5)
tripod(206, 120, 0.86, phase=0.0, seed=11, ray=True, tentacles=9)

# broken reflections, shivering wider as they come towards us
for (rx, rw) in ((96, 11), (206, 22), (320, 9)):
    for i in range(7):
        yy = HOR + 5 + i * 11
        j = rnd.uniform(-5, 5)
        p.add(f'<rect x="{rx-rw/2+j:.1f}" y="{yy}" width="{rw*(1+i*0.10):.1f}" height="5.0" fill="{K}"/>')

# people wading out, small and black against the water
for (fx, fh, lean) in ((52, 42, -6), (86, 36, -8), (284, 40, 7), (318, 32, 5)):
    fy = BANK - 10
    p.add(f'<path d="{poly([(fx-6, fy), (fx+6, fy), (fx+4+lean*0.4, fy-fh*0.55), (fx-4+lean*0.4, fy-fh*0.55)])}" fill="{K}"/>')
    p.add(f'<path d="{poly([(fx-6+lean*0.4, fy-fh*0.52), (fx+6+lean*0.4, fy-fh*0.52), (fx+4+lean, fy-fh*0.88), (fx-6+lean, fy-fh*0.88)])}" fill="{K}"/>')
    p.add(f'<circle cx="{fx+lean}" cy="{fy-fh*0.95}" r="{fh*0.14:.1f}" fill="{K}"/>')
    p.add(f'<path d="M {fx+4+lean} {fy-fh*0.74} l {11 if lean>0 else -11} {-7}" stroke="{K}" stroke-width="3.4" stroke-linecap="round"/>')
    p.add(f'<ellipse cx="{fx}" cy="{fy}" rx="{fh*0.34:.1f}" ry="3.0" fill="{P}" stroke="{K}" stroke-width="1.6"/>')

# ------------------------------------------------------------- the near bank
p.add(f'<rect x="0" y="{BANK}" width="400" height="{CAP-BANK}" fill="{K}"/>')
p.add(f'<path d="{poly([(0, BANK), (400, BANK), (400, BANK+6), (0, BANK+10)])}" fill="{K}"/>')

# the red weed, growing off the black bank into the light
for i in range(34):
    wx = rnd.uniform(-8, 408)
    wy = CAP - rnd.uniform(0, 30)
    hgt = rnd.uniform(26, 62)
    tipx = wx + rnd.uniform(-12, 12)
    p.add(f'<path d="M {wx:.1f} {wy:.1f} C {wx-11:.1f} {wy-hgt*0.5:.1f} {tipx+11:.1f} '
          f'{wy-hgt*0.7:.1f} {tipx:.1f} {wy-hgt:.1f}" fill="none" stroke="{R}" stroke-width="3.0"/>')
    for b in range(4):
        t = (b + 1) / 5
        bx = wx + (tipx - wx) * t
        by = wy - hgt * t
        L = 11 * (1 - t * 0.4)
        sgn = 1 if (b + i) % 2 else -1
        p.add(f'<path d="M {bx:.1f} {by:.1f} q {sgn*L*0.6:.1f} {-L*0.3:.1f} {sgn*L:.1f} {-L*0.9:.1f}" '
              f'fill="none" stroke="{R}" stroke-width="2.2"/>')

# ------------------------------------------------------------- caption band
p.add(f'<rect x="0" y="{CAP}" width="400" height="{600-CAP}" fill="{K}"/>')
p.add(f'<line x1="14" y1="{CAP+7}" x2="386" y2="{CAP+7}" stroke="{P}" stroke-width="1.4"/>')
p.text(200, CAP + 36, "THE WAR OF THE WORLDS", size=24, color=P, anchor="middle", spacing=1.3)
p.add(f'<line x1="92" y1="{CAP+45}" x2="308" y2="{CAP+45}" stroke="{P}" stroke-width="1.0"/>')
p.text(200, CAP + 62, "“And this Thing I saw! How can I describe it?”", size=11.5,
       color=P, anchor="middle", style="italic")
p.text(200, CAP + 80, "THE COMING OF THE FIGHTING-MACHINES, UP THE VALLEY OF THE THAMES",
       size=8.8, color=P, anchor="middle", spacing=0.5)
p.text(200, CAP + 98, "H. G. Wells, 1898", size=9.6, color=P, anchor="middle", style="italic")

p.add(f'<rect x="4" y="4" width="392" height="592" fill="none" stroke="{K}" stroke-width="3.0"/>')
p.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "3_afternoon_the_fighting_machines.svg"),
       names=(K, P, R, Y))
