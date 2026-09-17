# Midday — "Mate, SCA 905". Palette: blue, white, red (stamp).
# 1977: Enterprise rides piggyback on N905NA, the Boeing 747 Shuttle Carrier Aircraft, for
# the Approach and Landing Test ferry and captive flights out of Edwards. Drawn as an
# engineering elevation on blueprint paper: white line on blue, dimensioned, stamped.
import os, math
W, H = 400, 600
B, Wh, R = "#123DB0", "#FFFFFF", "#E01B24"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{B}"/>']

# graph-paper grid, faint (thin white lines, widely spaced so it reads as texture not noise)
for x in range(0, W + 1, 20):
    o.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{Wh}" stroke-width="0.4" opacity="0.35"/>')
for y in range(0, H + 1, 20):
    o.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{Wh}" stroke-width="0.4" opacity="0.35"/>')

# border plate
o.append(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="{Wh}" stroke-width="1.5"/>')

CY = 300  # fuselage centreline of the carrier
FX0, FX1 = 55, 345  # fuselage nose/tail x

def line(x0, y0, x1, y1, sw=1.4, col=Wh, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="{sw}"{d}/>')

def poly(pts, fill="none", col=Wh, sw=1.4):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    o.append(f'<polygon points="{p}" fill="{fill}" stroke="{col}" stroke-width="{sw}"/>')

# --- 747 carrier: fuselage tube, tail fin, one visible wing stub, nose taper ---
poly([(FX0, CY - 16), (FX0 + 20, CY - 22), (FX1 - 25, CY - 22), (FX1, CY - 6),
      (FX1, CY + 10), (FX1 - 25, CY + 18), (FX0 + 12, CY + 18), (FX0, CY + 2)])
poly([(FX1 - 40, CY - 22), (FX1 - 10, CY - 22), (FX1 + 6, CY - 92), (FX1 - 22, CY - 92)])   # tail fin
line(FX1 - 34, CY - 22, FX1 - 6, CY - 78, sw=1.2)                                           # fin leading edge detail
poly([(150, CY + 14), (100, CY + 70), (86, CY + 70), (150, CY + 16)])                       # wing root, near side
o.append(f'<circle cx="128" cy="{CY+52}" r="7" fill="none" stroke="{Wh}" stroke-width="1.2"/>')  # inboard engine
o.append(f'<circle cx="102" cy="{CY+62}" r="6" fill="none" stroke="{Wh}" stroke-width="1.2"/>')  # outboard engine
for wx in (95, 130, 165, 200, 235, 270, 300):    # cabin windows, a dotted row
    o.append(f'<circle cx="{wx}" cy="{CY-14}" r="1.4" fill="{Wh}"/>')

# --- orbiter, dorsal, mated on two struts, nose toward the carrier's nose ---
OY = CY - 58
poly([(90, OY), (108, OY - 8), (190, OY - 8), (205, OY + 6), (205, OY + 18), (90, OY + 18)], sw=1.3)  # fuselage
poly([(150, OY - 8), (150, OY - 34), (172, OY - 34), (172, OY - 8)], sw=1.2)                            # vertical tail
poly([(190, OY + 18), (230, OY + 30), (230, OY + 38), (195, OY + 24)], sw=1.2)                          # delta wing, near side
line(90, OY, 78, OY + 10, sw=1.2)         # nose cap line
# mating struts
line(120, OY + 18, 120, CY - 22, sw=2)
line(178, OY + 18, 178, CY - 22, sw=2)

# --- dimension lines ---
def dim(x0, x1, y, label):
    line(x0, y, x1, y, sw=0.9)
    line(x0, y - 5, x0, y + 5, sw=0.9)
    line(x1, y - 5, x1, y + 5, sw=0.9)
    o.append(f'<text x="{(x0+x1)/2:.1f}" y="{y-6:.1f}" font-family="Georgia, serif" font-size="9" '
              f'fill="{Wh}" text-anchor="middle">{label}</text>')
dim(FX0, FX1, CY + 110, "231 FT · SCA 905  (N905NA)")
dim(90, 230, OY - 46, "122 FT · OV–101 ENTERPRISE")

# --- callouts: leader line + dot + label ---
def callout(px, py, tx, ty, label, anchor="start"):
    line(px, py, tx, ty, sw=0.8)
    o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="1.6" fill="{Wh}"/>')
    o.append(f'<text x="{tx+ (4 if anchor=="start" else -4):.1f}" y="{ty:.1f}" font-family="Georgia, serif" '
              f'font-size="8.5" fill="{Wh}" text-anchor="{anchor}">{label}</text>')
callout(120, OY + 18, 60, 140, "FWD ATTACH STRUT")
callout(178, OY + 18, 320, 150, "AFT ATTACH STRUT", anchor="end")
callout(FX1 - 5, CY - 60, 320, 60, "TAIL CONE FAIRING — SMOOTHS THE WAKE", anchor="end")
callout(FX0 + 14, CY - 18, 60, 440, "FLIGHT DECK, N905NA", anchor="start")

# --- position light: single red navigation light at the carrier's tail, the day's motif ---
o.append(f'<circle cx="{FX1+4:.1f}" cy="{CY-4:.1f}" r="2.6" fill="{R}"/>')
o.append(f'<circle cx="{FX1+4:.1f}" cy="{CY-4:.1f}" r="5.5" fill="none" stroke="{R}" stroke-width="0.8" opacity="0.6"/>')

# --- red stamp, corner: an approval ring, slightly canted, like a rubber date stamp ---
import random
random.seed(19770118)
sxc, syc = 320, 500
o.append(f'<g transform="rotate(-9 {sxc} {syc})">')
o.append(f'<circle cx="{sxc}" cy="{syc}" r="34" fill="none" stroke="{R}" stroke-width="2"/>')
o.append(f'<circle cx="{sxc}" cy="{syc}" r="27" fill="none" stroke="{R}" stroke-width="1"/>')
o.append(f'<text x="{sxc}" y="{syc-1}" font-family="Georgia, serif" font-size="9" fill="{R}" '
          f'text-anchor="middle" letter-spacing="1">CAPTIVE</text>')
o.append(f'<text x="{sxc}" y="{syc+11}" font-family="Georgia, serif" font-size="9" fill="{R}" '
          f'text-anchor="middle" letter-spacing="1">FLIGHT NO.1</text>')
o.append(f'<text x="{sxc}" y="{syc+22}" font-family="Georgia, serif" font-size="7.5" fill="{R}" '
          f'text-anchor="middle">18 · II · 77</text>')
o.append('</g>')

o.append(f'<text x="200" y="565" font-family="Georgia, serif" font-size="13" fill="{Wh}" '
          f'text-anchor="middle" letter-spacing="4">APPROACH &amp; LANDING TEST</text>')
o.append(f'<text x="200" y="580" font-family="Georgia, serif" font-style="italic" font-size="9.5" '
          f'fill="{Wh}" text-anchor="middle">Edwards Air Force Base, California</text>')

svg = "\n".join(o + ["</svg>"])
open(os.environ["OUT_RAW"].replace(".png", ".svg"), "w").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(), write_to=os.environ["OUT_RAW"], output_width=800, output_height=1200)
