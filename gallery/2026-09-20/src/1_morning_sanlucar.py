# Morning — "Sanlúcar, dawn". An engraved harbour plate: five ships leaving the mouth of
# the Guadalquivir on 20 September 1519, sun just clearing the town. All six colours,
# white in charge; the tone is drawn with hatching, not dithered. Emits SVG, renders 2x.
import os, math, random
random.seed(1519)
W, H = 400, 600
K, Wh, R, Y, B, G = "#000000", "#FFFFFF", "#E01B24", "#F5D400", "#123DB0", "#1E9B3C"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{Wh}"/>']
add = o.append
HOR = 330                       # horizon
SUN = (292, 262, 36)            # cx, cy, r

# ---------------- sky: engraved horizontal hatching, denser toward the horizon -------
y = 118.0; gap = 17.0
while y < HOR - 4:
    amp = 0.6
    pts = " ".join(f"{x},{y + amp * math.sin(x / 23 + y):.1f}" for x in range(8, W - 7, 8))
    add(f'<polyline points="{pts}" fill="none" stroke="{K}" stroke-width="0.9"/>')
    y += gap; gap = max(4.4, gap * 0.9)
# clear a halo around the sun, then radiating engraved rays
add(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="98" fill="{Wh}"/>')
for i in range(48):
    a = math.radians(i * 7.5 + 3)
    r0 = SUN[2] + 8; r1 = SUN[2] + (30 if i % 2 else 52) + (8 if i % 4 == 0 else 0)
    add(f'<line x1="{SUN[0] + r0 * math.cos(a):.1f}" y1="{SUN[1] + r0 * math.sin(a):.1f}" '
        f'x2="{SUN[0] + r1 * math.cos(a):.1f}" y2="{SUN[1] + r1 * math.sin(a):.1f}" '
        f'stroke="{K}" stroke-width="{1.4 if i % 2 == 0 else 0.9}"/>')
# sun disc: yellow, engraved with fine concentric rings
add(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="{SUN[2]}" fill="{Y}" stroke="{K}" stroke-width="2"/>')
for r in range(8, SUN[2] - 3, 6):
    add(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="{r}" fill="none" stroke="{K}" stroke-width="0.8" stroke-dasharray="3,2.5"/>')

# clouds: lens shapes with internal hatching, drifting in from the left
def cloud(cx, cy, w, h):
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{w}" ry="{h}" fill="{Wh}" stroke="{K}" stroke-width="1.3"/>')
    for k in range(-h + 4, h - 2, 4):
        hw = w * math.sqrt(max(0.0, 1 - (k / h) ** 2)) - 3
        add(f'<line x1="{cx - hw:.1f}" y1="{cy + k}" x2="{cx + hw:.1f}" y2="{cy + k}" stroke="{K}" stroke-width="0.7"/>')
    # a lit rim: a white cut along the top edge
    add(f'<path d="M{cx - w * 0.8:.1f},{cy - h * 0.55:.1f} Q{cx:.1f},{cy - h - 6:.1f} {cx + w * 0.8:.1f},{cy - h * 0.55:.1f}" fill="none" stroke="{Wh}" stroke-width="3"/>')
    add(f'<path d="M{cx - w * 0.8:.1f},{cy - h * 0.55:.1f} Q{cx:.1f},{cy - h - 6:.1f} {cx + w * 0.8:.1f},{cy - h * 0.55:.1f}" fill="none" stroke="{K}" stroke-width="1.2"/>')
cloud(92, 96, 70, 14); cloud(150, 128, 48, 10); cloud(40, 150, 38, 8); cloud(210, 82, 30, 7)
# gulls
for (gx, gy, gs) in [(60, 210, 6), (84, 222, 5), (120, 200, 7), (140, 236, 4), (250, 190, 6), (330, 160, 5), (355, 205, 4), (30, 260, 5)]:
    add(f'<path d="M{gx - gs},{gy} q{gs / 2},{-gs / 2} {gs},0 q{gs / 2},{-gs / 2} {gs},0" fill="none" stroke="{K}" stroke-width="1.4"/>')

# ---------------- far shore -------------------------------------------------------------
# left: the sand spit and marsh of Doñana
add(f'<path d="M0,{HOR - 10} L60,{HOR - 12} L120,{HOR - 9} L170,{HOR - 6} L170,{HOR + 2} L0,{HOR + 2} Z" fill="{Y}" stroke="{K}" stroke-width="1.2"/>')
for x in range(6, 165, 7):
    add(f'<line x1="{x}" y1="{HOR - 4}" x2="{x + 3}" y2="{HOR - 10 - (x % 3)}" stroke="{G}" stroke-width="1.6"/>')
for (px, ph) in [(20, 14), (34, 18), (50, 12), (96, 16), (110, 13)]:      # stone pines
    add(f'<line x1="{px}" y1="{HOR - 10}" x2="{px}" y2="{HOR - 10 - ph}" stroke="{K}" stroke-width="1.6"/>')
    add(f'<ellipse cx="{px}" cy="{HOR - 10 - ph}" rx="{ph * 0.6:.0f}" ry="{ph * 0.32:.0f}" fill="{G}" stroke="{K}" stroke-width="1"/>')
# right: the town — Sanlúcar's white houses, red roofs, the castle, the church
add(f'<rect x="170" y="{HOR - 2}" width="230" height="5" fill="{Y}" stroke="{K}" stroke-width="1"/>')
x = 172
random.seed(7)
buildings = []
while x < 396:
    w = random.choice([10, 12, 14, 18, 22]); h = random.choice([12, 14, 16, 20, 24])
    buildings.append((x, w, h)); x += w + random.choice([0, 0, 2])
for (bx, bw, bh) in buildings:
    add(f'<rect x="{bx}" y="{HOR - 2 - bh}" width="{bw}" height="{bh}" fill="{Wh}" stroke="{K}" stroke-width="1.1"/>')
    if random.random() < 0.7:
        add(f'<polygon points="{bx - 1},{HOR - 2 - bh} {bx + bw / 2:.0f},{HOR - 2 - bh - bw * 0.35:.0f} {bx + bw + 1},{HOR - 2 - bh}" fill="{R}" stroke="{K}" stroke-width="1"/>')
    else:
        add(f'<rect x="{bx}" y="{HOR - 5 - bh}" width="{bw}" height="3" fill="{R}" stroke="{K}" stroke-width="0.8"/>')
    for wx in range(bx + 3, bx + bw - 2, 5):
        for wy in range(HOR - bh + 2, HOR - 5, 6):
            add(f'<rect x="{wx}" y="{wy}" width="2" height="3" fill="{K}"/>')
# castle of Santiago: crenellated block
add(f'<rect x="196" y="{HOR - 36}" width="46" height="34" fill="{Wh}" stroke="{K}" stroke-width="1.4"/>')
for cx in range(198, 240, 6):
    add(f'<rect x="{cx}" y="{HOR - 40}" width="3" height="5" fill="{K}"/>')
add(f'<rect x="200" y="{HOR - 30}" width="38" height="2" fill="{K}"/>')
for wy in range(HOR - 26, HOR - 6, 6):
    for wx in (206, 218, 230):
        add(f'<rect x="{wx}" y="{wy}" width="2" height="3" fill="{K}"/>')
add(f'<polygon points="243,{HOR - 40} 243,{HOR - 50} 251,{HOR - 46} 243,{HOR - 43}" fill="{R}" stroke="{K}" stroke-width="0.8"/>')
add(f'<line x1="243" y1="{HOR - 36}" x2="243" y2="{HOR - 52}" stroke="{K}" stroke-width="1.2"/>')
# the church of Nuestra Señora de la O: nave and tower
add(f'<rect x="300" y="{HOR - 34}" width="40" height="32" fill="{Wh}" stroke="{K}" stroke-width="1.4"/>')
add(f'<polygon points="299,{HOR - 34} 320,{HOR - 46} 341,{HOR - 34}" fill="{R}" stroke="{K}" stroke-width="1.1"/>')
add(f'<rect x="338" y="{HOR - 62}" width="16" height="60" fill="{Wh}" stroke="{K}" stroke-width="1.4"/>')
add(f'<polygon points="337,{HOR - 62} 346,{HOR - 76} 355,{HOR - 62}" fill="{R}" stroke="{K}" stroke-width="1.1"/>')
add(f'<line x1="346" y1="{HOR - 76}" x2="346" y2="{HOR - 86}" stroke="{K}" stroke-width="1.5"/>')
add(f'<line x1="342" y1="{HOR - 82}" x2="350" y2="{HOR - 82}" stroke="{K}" stroke-width="1.5"/>')
for wy in (HOR - 56, HOR - 44, HOR - 32):
    add(f'<path d="M343,{wy + 5} L343,{wy} A3,3 0 0 1 349,{wy} L349,{wy + 5} Z" fill="{K}"/>')
for wx in (306, 316, 326):
    add(f'<path d="M{wx},{HOR - 12} L{wx},{HOR - 24} A3,3 0 0 1 {wx + 6},{HOR - 24} L{wx + 6},{HOR - 12} Z" fill="{K}"/>')
# trees along the waterfront
for tx in range(176, 400, 17):
    add(f'<circle cx="{tx}" cy="{HOR - 6}" r="4" fill="{G}" stroke="{K}" stroke-width="0.9"/>')

# ---------------- water: blue, with engraved wave lines that grow toward the viewer ----
add(f'<rect x="0" y="{HOR + 3}" width="{W}" height="{H - HOR - 3}" fill="{B}"/>')
add(f'<line x1="0" y1="{HOR + 3}" x2="{W}" y2="{HOR + 3}" stroke="{K}" stroke-width="1.5"/>')
y = HOR + 8.0; gap = 3.0; i = 0
while y < H:
    amp = 0.4 + (y - HOR) / 60
    lam = 18 + (y - HOR) / 6
    pts = " ".join(f"{x},{y + amp * math.sin(x / lam * 2 + i * 1.7):.1f}" for x in range(0, W + 1, 5))
    add(f'<polyline points="{pts}" fill="none" stroke="{K}" stroke-width="{0.8 + (y - HOR) / 260:.2f}"/>')
    if i % 3 == 1:   # a white crest highlight on every third line
        pts2 = " ".join(f"{x},{y - 1.6 + amp * math.sin(x / lam * 2 + i * 1.7):.1f}" for x in range(0, W + 1, 5))
        add(f'<polyline points="{pts2}" fill="none" stroke="{Wh}" stroke-width="{0.9 + (y - HOR) / 300:.2f}" stroke-dasharray="{14 + i},{9 + i // 2}"/>')
    y += gap; gap *= 1.055; i += 1
# the sun's track on the water
for k in range(14):
    yy = HOR + 6 + k * (4 + k * 0.9)
    hw = 8 + k * 2.2
    add(f'<line x1="{SUN[0] - hw + random.uniform(-4, 4):.1f}" y1="{yy:.1f}" x2="{SUN[0] + hw + random.uniform(-4, 4):.1f}" y2="{yy:.1f}" stroke="{Y}" stroke-width="{2.6 + k * 0.2:.1f}"/>')

# ---------------- a carrack (nao), drawn in local units, hull ~124 long ---------------
def ship(cx, wy, s, flip=False, saltire=True):
    g = [f'<g transform="translate({cx},{wy}) scale({-s if flip else s},{s})">']
    a = g.append
    # reflection first (under the hull)
    for k in range(1, 7):
        a(f'<line x1="{-44 + k * 3}" y1="{k * 5}" x2="{44 - k * 2}" y2="{k * 5}" stroke="{K}" stroke-width="1.6" stroke-dasharray="{7 - k},{4 + k}"/>')
    # hull above the waterline: high sterncastle aft (left), forecastle forward (right)
    a(f'<path d="M-62,-36 L-40,-36 L-40,-23 L20,-21 L20,-31 L52,-31 L61,-19 L58,0 L-58,0 L-65,-12 Z" fill="{K}"/>')
    a(f'<path d="M-57,-8 Q0,-12 56,-8" fill="none" stroke="{Wh}" stroke-width="1.4"/>')
    a(f'<path d="M-57,-15 Q0,-18 55,-14" fill="none" stroke="{Wh}" stroke-width="1.1"/>')
    # castle railings and the stern lantern
    a(f'<line x1="-60" y1="-36" x2="-42" y2="-36" stroke="{Wh}" stroke-width="1.2"/>')
    a(f'<line x1="22" y1="-31" x2="50" y2="-31" stroke="{Wh}" stroke-width="1.2"/>')
    for xx in range(-58, -40, 4):
        a(f'<line x1="{xx}" y1="-36" x2="{xx}" y2="-31" stroke="{Wh}" stroke-width="0.9"/>')
    a(f'<circle cx="-66" cy="-40" r="3" fill="{Y}" stroke="{K}" stroke-width="1"/>')
    # bowsprit with spritsail
    a(f'<line x1="48" y1="-31" x2="96" y2="-60" stroke="{K}" stroke-width="2.2"/>')
    a(f'<path d="M66,-48 L84,-59 L88,-45 Q78,-32 68,-36 Z" fill="{Wh}" stroke="{K}" stroke-width="1.3"/>')
    # masts: fore, main, mizzen
    masts = [(28, -108), (-2, -142), (-42, -96)]
    for (mx, top) in masts:
        a(f'<line x1="{mx}" y1="-22" x2="{mx}" y2="{top}" stroke="{K}" stroke-width="2.6"/>')
    # square sails: (mast x, yard y, half width, foot y)
    def sq(mx, yy, hw, foot, cross=False):
        a(f'<line x1="{mx - hw - 5}" y1="{yy}" x2="{mx + hw + 5}" y2="{yy}" stroke="{K}" stroke-width="2"/>')
        d = foot - yy
        a(f'<path d="M{mx - hw},{yy} L{mx + hw},{yy} Q{mx + hw + 7},{yy + d * 0.55} {mx + hw - 3},{foot} '
          f'Q{mx},{foot + 7} {mx - hw + 3},{foot} Q{mx - hw - 7},{yy + d * 0.55} {mx - hw},{yy} Z" fill="{Wh}" stroke="{K}" stroke-width="1.5"/>')
        for k in range(1, 4):   # the belly of the sail: curved hatch lines
            yk = yy + d * k / 4
            a(f'<path d="M{mx - hw + 2},{yk} Q{mx},{yk + 4 + k} {mx + hw - 2},{yk}" fill="none" stroke="{K}" stroke-width="0.9"/>')
        if cross:               # the ragged cross of Burgundy on the course
            a(f'<line x1="{mx - hw + 6}" y1="{yy + 4}" x2="{mx + hw - 6}" y2="{foot - 4}" stroke="{R}" stroke-width="3"/>')
            a(f'<line x1="{mx + hw - 6}" y1="{yy + 4}" x2="{mx - hw + 6}" y2="{foot - 4}" stroke="{R}" stroke-width="3"/>')
    sq(-2, -96, 40, -44, cross=saltire); sq(-2, -134, 22, -102)
    sq(28, -80, 28, -38); sq(28, -105, 14, -84)
    # mizzen lateen
    a(f'<line x1="-72" y1="-40" x2="-14" y2="-104" stroke="{K}" stroke-width="2"/>')
    a(f'<path d="M-70,-42 L-16,-100 Q-20,-70 -30,-40 Z" fill="{Wh}" stroke="{K}" stroke-width="1.4"/>')
    for k in range(1, 4):
        t = k / 4
        a(f'<line x1="{-70 + 54 * t:.0f}" y1="{-42 - 58 * t:.0f}" x2="{-30 - 6 * k:.0f}" y2="{-40 - 12 * k}" stroke="{K}" stroke-width="0.8"/>')
    # tops (crow's nests)
    for (mx, top) in masts[:2]:
        ty = top + (masts[0][1] - top) * 0 + 30 if mx == 28 else top + 46
        a(f'<rect x="{mx - 6}" y="{ty}" width="12" height="5" fill="{K}"/>')
        a(f'<line x1="{mx - 6}" y1="{ty}" x2="{mx + 6}" y2="{ty}" stroke="{Wh}" stroke-width="1"/>')
    # shrouds and ratlines
    for (mx, top, n) in [(28, -80, 3), (-2, -100, 4), (-42, -70, 2)]:
        for side in (-1, 1):
            xs = [mx + side * (12 + k * 5) for k in range(n)]
            for xx in xs:
                a(f'<line x1="{mx}" y1="{top}" x2="{xx}" y2="-22" stroke="{K}" stroke-width="0.8"/>')
            for r in range(6, 40, 5):     # ratlines: ticks between the outer shrouds
                t = r / (-22 - top) if top != -22 else 0
                yy = -22 - r
                x0 = mx + (xs[0] - mx) * (1 - r / (-22 - top))
                x1 = mx + (xs[-1] - mx) * (1 - r / (-22 - top))
                a(f'<line x1="{x0:.1f}" y1="{yy}" x2="{x1:.1f}" y2="{yy}" stroke="{K}" stroke-width="0.6"/>')
    # stays
    a(f'<line x1="-2" y1="-142" x2="28" y2="-108" stroke="{K}" stroke-width="0.9"/>')
    a(f'<line x1="28" y1="-108" x2="96" y2="-60" stroke="{K}" stroke-width="0.9"/>')
    a(f'<line x1="-2" y1="-142" x2="-42" y2="-96" stroke="{K}" stroke-width="0.9"/>')
    # flags: red, swallow-tailed, streaming aft; a long pennant on the main
    for (mx, top) in masts:
        a(f'<polygon points="{mx},{top} {mx - 18},{top + 2} {mx - 13},{top + 6} {mx - 18},{top + 10} {mx},{top + 11}" fill="{R}" stroke="{K}" stroke-width="0.8"/>')
    a(f'<path d="M-2,-150 L-2,-142 L-40,-146 Q-60,-150 -80,-140 Q-60,-145 -40,-152 Z" fill="{R}" stroke="{K}" stroke-width="0.7"/>')
    g.append('</g>')
    add("\n".join(g))

# five ships: two near, three far, all heading out to sea (to the left)
ship(262, 358, 0.22, saltire=False)
ship(84, 374, 0.30, saltire=False)
ship(188, 404, 0.42)
ship(312, 466, 0.72)
ship(118, 530, 1.02)
# a rowing boat seeing them off, bottom right
add(f'<path d="M318,574 L392,574 L384,586 L326,586 Z" fill="{K}"/>')
add(f'<path d="M322,576 L388,576" stroke="{Wh}" stroke-width="1"/>')
for fx in (338, 352, 366):
    add(f'<circle cx="{fx}" cy="{566}" r="3.2" fill="{K}"/>')
    add(f'<rect x="{fx - 3}" y="569" width="6" height="6" fill="{K}"/>')
    add(f'<line x1="{fx + 6}" y1="562" x2="{fx + 14}" y2="580" stroke="{K}" stroke-width="1.4"/>')

# ---------------- plate border and caption ----------------------------------------------
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="{Wh}" stroke-width="12"/>')
add(f'<rect x="7" y="7" width="{W - 14}" height="{H - 14}" fill="none" stroke="{K}" stroke-width="2"/>')
add(f'<rect x="10" y="10" width="{W - 20}" height="{H - 20}" fill="none" stroke="{K}" stroke-width="0.8"/>')
add(f'<rect x="7" y="{H - 34}" width="{W - 14}" height="27" fill="{Wh}" stroke="{K}" stroke-width="1"/>')
add(f'<text x="200" y="{H - 21}" font-family="Liberation Serif" font-size="10.5" fill="{K}" text-anchor="middle" letter-spacing="1.2">SANLVCAR DE BARRAMEDA · XX SEPTIEMBRE MDXIX</text>')
add(f'<text x="200" y="{H - 10}" font-family="FreeSerif" font-style="italic" font-size="9" fill="{K}" text-anchor="middle">La Armada de Molucca se hace a la mar: Trinidad, San Antonio, Concepción, Victoria, Santiago</text>')
add('</svg>')

import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgtools import finish
finish("\n".join(o), W, H)
