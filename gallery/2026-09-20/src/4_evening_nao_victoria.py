# Evening — "Nao Victoria, lámina IV". A shipwright's blueprint of the one ship that came
# home: sheer plan with the sail plan, body plan (frames), half-breadth plan (deck), a
# table of the sails, a metre scale. Blue in charge (the paper), white lines, yellow for
# the sails, red for the waterline and the flag. Dimensions are those of the replica;
# nobody kept the originals. Emits SVG.
import os, math
W, H = 400, 600
K, Wh, R, Y, B, G = "#000000", "#FFFFFF", "#E01B24", "#F5D400", "#123DB0", "#1E9B3C"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{B}"/>']
add = o.append
LAB = 'font-family="DejaVu Serif" font-weight="bold"'
MONO = 'font-family="Liberation Mono" font-weight="bold"'
# drawing-sheet grid: dots every 20px
for gx in range(20, W, 20):
    for gy in range(20, H, 20):
        add(f'<circle cx="{gx}" cy="{gy}" r="1.0" fill="{Wh}"/>')
# frame
add(f'<rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="none" stroke="{Wh}" stroke-width="2.2"/>')
add(f'<rect x="12" y="12" width="{W - 24}" height="{H - 24}" fill="none" stroke="{Wh}" stroke-width="0.9"/>')

def label(x, y, t, size=9.5, anchor="start", col=Wh, rot=0, fam=LAB, ls=0):
    add(f'<text transform="translate({x},{y}) rotate({rot})" {fam} font-size="{size}" fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{t}</text>')
def leader(x0, y0, x1, y1, col=Wh):
    add(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{col}" stroke-width="1"/>')
    add(f'<circle cx="{x0}" cy="{y0}" r="2" fill="none" stroke="{col}" stroke-width="1.2"/>')
def dim(x0, y0, x1, y1, text, off=8, col=Wh):
    """dimension line with arrowheads, text centred, offset perpendicular"""
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    ax0, ay0, ax1, ay1 = x0 + nx * off, y0 + ny * off, x1 + nx * off, y1 + ny * off
    add(f'<line x1="{x0}" y1="{y0}" x2="{ax0 + nx * 4:.1f}" y2="{ay0 + ny * 4:.1f}" stroke="{col}" stroke-width="0.9"/>')
    add(f'<line x1="{x1}" y1="{y1}" x2="{ax1 + nx * 4:.1f}" y2="{ay1 + ny * 4:.1f}" stroke="{col}" stroke-width="0.9"/>')
    add(f'<line x1="{ax0:.1f}" y1="{ay0:.1f}" x2="{ax1:.1f}" y2="{ay1:.1f}" stroke="{col}" stroke-width="1.1"/>')
    for (px, py, s) in [(ax0, ay0, 1), (ax1, ay1, -1)]:
        add(f'<polygon points="{px:.1f},{py:.1f} {px + s * ux * 7 + nx * 2.5:.1f},{py + s * uy * 7 + ny * 2.5:.1f} {px + s * ux * 7 - nx * 2.5:.1f},{py + s * uy * 7 - ny * 2.5:.1f}" fill="{col}"/>')
    ang = math.degrees(math.atan2(dy, dx))
    label((ax0 + ax1) / 2 + nx * 4, (ay0 + ay1) / 2 + ny * 4, text, 9, "middle", col, ang, MONO)

# ======================= SHEER PLAN with sail plan (top) ================================
WL = 232                      # waterline y
# the hull: keel, stem, sternpost, sheer, castles
hull = (f'M88,246 L300,246 C328,246 346,220 352,160 '            # keel and stem
        f'L338,160 C338,170 334,178 328,182 '                    # bow bulwark down to the waist
        f'L262,186 L262,166 L330,166 L330,160 L338,160 '         # forecastle
        f'M262,186 L168,190 L168,150 L118,150 L118,120 L64,124 L64,150 L64,174 L74,246 Z')  # waist, half-deck, poop, stern
add(f'<path d="{hull}" fill="none" stroke="{Wh}" stroke-width="1.6" stroke-linejoin="round"/>')
add(f'<path d="M64,174 L118,174 L118,150 M168,190 L168,174 L118,174 L118,150 L168,150 M64,150 L118,150" fill="none" stroke="{Wh}" stroke-width="1.1"/>')
add(f'<path d="M262,186 L262,166 M262,166 L330,166" fill="none" stroke="{Wh}" stroke-width="1.1"/>')
# wales: three longitudinal strakes following the sheer
for k, yy in enumerate([200, 212, 224]):
    add(f'<path d="M76,{yy + 8} Q200,{yy + 2} {336 - k * 6},{yy - 14 + k * 6}" fill="none" stroke="{Wh}" stroke-width="1.2"/>')
# underwater body: dashed
add(f'<path d="M74,246 Q60,236 66,214 M300,246 Q326,246 344,226" fill="none" stroke="{Wh}" stroke-width="1" stroke-dasharray="3,2"/>')
# rudder and tiller
add(f'<path d="M74,246 L62,246 L56,180 L66,178 Z" fill="none" stroke="{Wh}" stroke-width="1.3"/>')
for yy in (190, 206, 222, 238):
    add(f'<line x1="58" y1="{yy}" x2="70" y2="{yy}" stroke="{Wh}" stroke-width="1"/>')
# waterline in red, with the draught mark
add(f'<line x1="40" y1="{WL}" x2="370" y2="{WL}" stroke="{R}" stroke-width="2" stroke-dasharray="9,4"/>')
label(372, WL + 3, "LF", 8.5, "start", R, 0, MONO)
# masts: (x, deck y, top y)
MASTS = [(300, 166, 70), (204, 190, 28), (118, 150, 76)]
for (mx, dk, tp) in MASTS:
    add(f'<line x1="{mx}" y1="{dk}" x2="{mx}" y2="{tp}" stroke="{Wh}" stroke-width="2.4"/>')
    add(f'<line x1="{mx}" y1="{dk}" x2="{mx}" y2="{tp}" stroke="{B}" stroke-width="0.8"/>')
# tops (crow's nests)
for (mx, ty) in [(300, 108), (204, 84)]:
    add(f'<path d="M{mx - 9},{ty} L{mx + 9},{ty} L{mx + 6},{ty + 6} L{mx - 6},{ty + 6} Z" fill="none" stroke="{Wh}" stroke-width="1.2"/>')
# bowsprit
add(f'<line x1="330" y1="164" x2="384" y2="128" stroke="{Wh}" stroke-width="2.2"/>')
# sails: yellow, with blue seams (cloths), yards white
def sail(mx, yy, hw, foot, name=None):
    add(f'<line x1="{mx - hw - 6}" y1="{yy}" x2="{mx + hw + 6}" y2="{yy}" stroke="{Wh}" stroke-width="2.2"/>')
    d = foot - yy
    add(f'<path d="M{mx - hw},{yy} L{mx + hw},{yy} Q{mx + hw + 6},{yy + d * 0.55} {mx + hw - 2},{foot} '
        f'Q{mx},{foot + 6} {mx - hw + 2},{foot} Q{mx - hw - 6},{yy + d * 0.55} {mx - hw},{yy} Z" fill="{Y}" stroke="{Wh}" stroke-width="1"/>')
    n = max(3, int(hw / 6))
    for k in range(1, n):
        xx = mx - hw + 2 * hw * k / n
        add(f'<line x1="{xx:.1f}" y1="{yy + 2}" x2="{xx:.1f}" y2="{foot - 1}" stroke="{B}" stroke-width="1.8"/>')
    # reef band
    add(f'<line x1="{mx - hw + 3}" y1="{yy + d * 0.3:.1f}" x2="{mx + hw - 3}" y2="{yy + d * 0.3:.1f}" stroke="{B}" stroke-width="1.8"/>')
sail(204, 100, 52, 168)          # mayor (main course)
sail(204, 44, 26, 82)            # gavia (main topsail)
sail(300, 118, 36, 160)          # trinquete (fore course)
sail(300, 78, 16, 106)           # velacho
# cebadera (spritsail) under the bowsprit
add(f'<line x1="346" y1="134" x2="378" y2="154" stroke="{Wh}" stroke-width="1.8"/>')
add(f'<path d="M348,136 L374,152 L370,176 L346,162 Z" fill="{Y}" stroke="{Wh}" stroke-width="1"/>')
add(f'<line x1="356" y1="141" x2="354" y2="167" stroke="{B}" stroke-width="1.8"/>')
# mesana (lateen)
add(f'<line x1="82" y1="150" x2="150" y2="62" stroke="{Wh}" stroke-width="2"/>')
add(f'<path d="M86,148 L146,68 Q132,110 112,148 Z" fill="{Y}" stroke="{Wh}" stroke-width="1"/>')
add(f'<line x1="104" y1="126" x2="124" y2="100" stroke="{B}" stroke-width="1.8"/>')
# rigging: shrouds, stays
for (mx, tp, n, dk) in [(300, 108, 3, 166), (204, 84, 4, 190), (118, 100, 2, 150)]:
    for side in (-1, 1):
        for k in range(n):
            add(f'<line x1="{mx}" y1="{tp}" x2="{mx + side * (10 + k * 5)}" y2="{dk}" stroke="{Wh}" stroke-width="0.9"/>')
add(f'<path d="M204,28 L300,70 L384,128 M204,28 L118,76 M204,84 L300,118 M118,150 L64,124" fill="none" stroke="{Wh}" stroke-width="0.9" stroke-dasharray="4,2"/>')
# flag
add(f'<polygon points="204,28 204,18 234,22 204,26" fill="{R}"/>')
add(f'<polygon points="300,70 300,62 322,65 300,68" fill="{R}"/>')
# lantern at the poop
add(f'<circle cx="60" cy="116" r="3.5" fill="none" stroke="{Wh}" stroke-width="1.2"/>')
add(f'<line x1="60" y1="120" x2="64" y2="124" stroke="{Wh}" stroke-width="1"/>')
# labels with leaders
leader(204, 60, 250, 40); label(253, 43, "gavia", 9.5)
leader(240, 130, 250, 128); label(253, 131, "mayor", 9.5)
leader(300, 150, 332, 206); label(334, 209, "trinquete", 9.5)
leader(300, 92, 262, 74); label(236, 70, "velacho", 9.5, "start")
leader(362, 166, 366, 186); label(352, 197, "cebadera", 9.5)
leader(112, 118, 40, 100); label(22, 96, "mesana", 9.5)
leader(92, 136, 30, 140); label(18, 150, "toldilla", 9.5)
leader(140, 162, 30, 170); label(18, 181, "alcázar", 9.5)
leader(296, 176, 252, 206); label(230, 216, "castillo", 9.5)
leader(60, 210, 30, 220); label(18, 230, "timón", 9.5)
leader(370, 140, 340, 96); label(318, 92, "bauprés", 9.5, "start")
# dimensions: length overall, mainmast height
dim(64, 262, 352, 262, "eslora 27,0 m", 8)
dim(34, 246, 34, 150, "puntal", -8)
label(28, 34, "LÁMINA IV", 11, "start", Wh, 0, LAB, 3)
label(28, 48, "plano de velas y arboladura", 8.5, "start", Wh)

# ======================= BODY PLAN (frames), bottom left ================================
BX, BY, BW, BD = 108, 480, 66, 118     # centre x, keel y, max half-breadth, depth
add(f'<rect x="24" y="{BY - BD - 30}" width="168" height="{BD + 44}" fill="none" stroke="{Wh}" stroke-width="1"/>')
label(30, BY - BD - 18, "PLANO DE FORMAS", 9, "start", Wh, 0, LAB, 1.5)
add(f'<line x1="{BX}" y1="{BY - BD - 8}" x2="{BX}" y2="{BY + 6}" stroke="{Wh}" stroke-width="1" stroke-dasharray="6,3"/>')
add(f'<line x1="{BX - BW - 10}" y1="{BY}" x2="{BX + BW + 10}" y2="{BY}" stroke="{Wh}" stroke-width="1.6"/>')
# waterlines and buttocks
for k in range(1, 5):
    yy = BY - k * BD / 5
    add(f'<line x1="{BX - BW - 6}" y1="{yy:.1f}" x2="{BX + BW + 6}" y2="{yy:.1f}" stroke="{Wh}" stroke-width="0.8" stroke-dasharray="2,3"/>')
    label(BX - BW - 8, yy + 3, f"W{k}", 7.5, "end", Wh, 0, MONO)
for k in (1, 2, 3):
    xx = k * BW / 4
    for s in (-1, 1):
        add(f'<line x1="{BX + s * xx:.1f}" y1="{BY - BD - 4}" x2="{BX + s * xx:.1f}" y2="{BY}" stroke="{Wh}" stroke-width="0.7" stroke-dasharray="2,3"/>')
add(f'<line x1="{BX - BW - 6}" y1="{BY - BD * 0.42:.1f}" x2="{BX + BW + 6}" y2="{BY - BD * 0.42:.1f}" stroke="{R}" stroke-width="1.6" stroke-dasharray="7,3"/>')
# sections: forward stations on the right, aft on the left
def section(side, frac, full):
    # half-breadth b and depth of this frame; fuller frames have a rounder bilge
    b = BW * (1 - frac ** 2.1) * (1.0 if side > 0 else 0.97)
    dtop = BD * (1 - 0.35 * frac ** 1.5)
    yt = BY - dtop
    bil = 0.55 + 0.4 * (1 - frac)          # bilge roundness
    kx = BX + side * b; ky = BY
    path = (f'M{BX + side * b * 1.02:.1f},{yt:.1f} C{BX + side * b * 1.06:.1f},{yt + dtop * 0.35:.1f} '
            f'{BX + side * b * bil:.1f},{BY - dtop * 0.05:.1f} {BX + side * 3:.1f},{BY:.1f}')
    add(f'<path d="{path}" fill="none" stroke="{Wh}" stroke-width="{1.7 if frac < 0.05 else 1.1}"/>')
    # the deck line ends
    add(f'<line x1="{BX + side * b * 1.02:.1f}" y1="{yt:.1f}" x2="{BX + side * (b * 1.02 - 6):.1f}" y2="{yt + 1:.1f}" stroke="{Wh}" stroke-width="1.2"/>')
for i in range(8):
    section(1, i / 8, True); section(-1, i / 8, True)
for i, xx in enumerate(range(-3, 4)):
    label(BX + xx * 18, BY + 16, f"{abs(xx)}", 8, "middle", Wh, 0, MONO)
label(BX + 70, BY + 16, "proa", 8, "middle", Wh, 0, LAB); label(BX - 70, BY + 16, "popa", 8, "middle", Wh, 0, LAB)
dim(BX - BW, BY + 24, BX + BW, BY + 24, "manga 7,0 m", 6)

# ======================= HALF-BREADTH PLAN (deck), bottom right =========================
DX0, DX1, DY = 214, 376, 415
add(f'<rect x="206" y="{BY - BD - 30}" width="170" height="{BD + 44}" fill="none" stroke="{Wh}" stroke-width="1"/>')
label(212, BY - BD - 18, "PLANTA", 9, "start", Wh, 0, LAB, 1.5)
def deck_outline(hw, inset=0):
    x0, x1 = DX0 + inset, DX1 - inset * 1.4
    mid = (x0 + x1) * 0.48
    return (f'M{x0},{DY - hw * 0.62} Q{mid},{DY - hw * 1.32} {x1},{DY} Q{mid},{DY + hw * 1.32} {x0},{DY + hw * 0.62} Z')
add(f'<path d="{deck_outline(30)}" fill="none" stroke="{Wh}" stroke-width="1.6"/>')
for k, ins in enumerate([6, 12, 19]):
    add(f'<path d="{deck_outline(30 - k * 7, ins)}" fill="none" stroke="{Wh}" stroke-width="0.8" stroke-dasharray="3,2"/>')
add(f'<line x1="{DX0 - 6}" y1="{DY}" x2="{DX1 + 14}" y2="{DY}" stroke="{Wh}" stroke-width="0.9" stroke-dasharray="6,3"/>')
# stations across
for k in range(9):
    xx = DX0 + 8 + k * 18
    add(f'<line x1="{xx}" y1="{DY - 40}" x2="{xx}" y2="{DY + 40}" stroke="{Wh}" stroke-width="0.6" stroke-dasharray="2,3"/>')
# masts, hatches, capstan, tiller
for (mx, r) in [(DX0 + 40, 4.5), (DX0 + 98, 5.5), (DX0 + 138, 3.5)]:
    add(f'<circle cx="{mx}" cy="{DY}" r="{r}" fill="none" stroke="{Wh}" stroke-width="1.6"/>')
    add(f'<circle cx="{mx}" cy="{DY}" r="1.2" fill="{Wh}"/>')
add(f'<rect x="{DX0 + 66}" y="{DY - 9}" width="20" height="18" fill="none" stroke="{Wh}" stroke-width="1.3"/>')
add(f'<rect x="{DX0 + 110}" y="{DY - 7}" width="14" height="14" fill="none" stroke="{Wh}" stroke-width="1.3"/>')
add(f'<line x1="{DX0 + 66}" y1="{DY - 9}" x2="{DX0 + 86}" y2="{DY + 9}" stroke="{Wh}" stroke-width="0.8"/>')
add(f'<circle cx="{DX0 + 54}" cy="{DY + 14}" r="4" fill="none" stroke="{Wh}" stroke-width="1.2"/>')
add(f'<line x1="{DX0 + 50}" y1="{DY + 14}" x2="{DX0 + 58}" y2="{DY + 14}" stroke="{Wh}" stroke-width="1"/>')
add(f'<line x1="{DX0 - 4}" y1="{DY}" x2="{DX0 + 22}" y2="{DY}" stroke="{Wh}" stroke-width="2"/>')
add(f'<line x1="{DX1}" y1="{DY}" x2="{DX1 + 14}" y2="{DY - 4}" stroke="{Wh}" stroke-width="2"/>')
leader(DX0 + 76, DY - 9, DX0 + 76, DY - 30); label(DX0 + 76, DY - 33, "escotilla", 8, "middle")
leader(DX0 + 54, DY + 18, DX0 + 54, DY + 36); label(DX0 + 54, DY + 46, "cabrestante", 8, "middle")
leader(DX0 + 10, DY + 2, DX0 + 10, DY + 36); label(DX0 + 14, DY + 46, "caña", 8, "middle")
leader(DX0 + 138, DY - 4, DX0 + 138, DY - 30); label(DX0 + 138, DY - 33, "trinquete", 8, "middle")

# ======================= sail table and title block =====================================
TY = 508
add(f'<rect x="24" y="{TY}" width="352" height="70" fill="none" stroke="{Wh}" stroke-width="1.4"/>')
add(f'<line x1="24" y1="{TY + 22}" x2="376" y2="{TY + 22}" stroke="{Wh}" stroke-width="1"/>')
add(f'<line x1="150" y1="{TY}" x2="150" y2="{TY + 70}" stroke="{Wh}" stroke-width="1"/>')
label(30, TY + 16, "NAO VICTORIA", 13, "start", Wh, 0, LAB, 2.5)
label(30, TY + 36, "85 toneles · palo mayor 26 m", 8, "start", Wh)
label(30, TY + 48, "Armada de Molucca, 1519", 8, "start", Wh)
label(30, TY + 60, "Sanlúcar → Sanlúcar, 1522", 8, "start", Y)
rows = [("vela", "paño", "m²"), ("mayor", "12", "180"), ("trinquete", "9", "90"), ("gavia", "4", "30"), ("velacho", "3", "18"), ("mesana", "6", "60"), ("cebadera", "4", "40")]
for i, (a, b, c) in enumerate(rows):
    yy = TY + 15 + i * 9.2 if i == 0 else TY + 32 + (i - 1) * 8.4
    col = Y if i == 0 else Wh
    label(158, yy, a, 7.8, "start", col, 0, MONO); label(236, yy, b, 7.8, "end", col, 0, MONO); label(276, yy, c, 7.8, "end", col, 0, MONO)
# metre scale
sx, sy = 292, TY + 44
label(sx + 34, sy - 10, "escala 1:200", 7.5, "middle", Wh, 0, MONO)
add(f'<rect x="{sx}" y="{sy}" width="68" height="5" fill="none" stroke="{Wh}" stroke-width="1"/>')
for k in range(4):
    if k % 2 == 0: add(f'<rect x="{sx + k * 17}" y="{sy}" width="17" height="5" fill="{Wh}"/>')
for k, m in enumerate([0, 5, 10, 15, 20]):
    label(sx + k * 17, sy + 14, str(m), 7, "middle", Wh, 0, MONO)
label(sx + 34, sy + 26, "metros", 7.5, "middle", Wh, 0, MONO)
label(200, 590, "sólo esta nao volvió · 18 hombres de 270 · 6 de septiembre de 1522", 8, "middle", Wh)
add('</svg>')

import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgtools import finish
finish("\n".join(o), W, H, chroma_floor=40)
