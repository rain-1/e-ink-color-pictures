# Midday — "Full Burn". Halftone screenprint: a radial dot-glow around a bare white sun.
# Palette: yellow, red, with the sun in white and a black rim.
import os, math
W,H=400,600
Y,R,Wh,K="#F5D400","#E01B24","#FFFFFF","#000000"
out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{Y}"/>']

CX, CY = 200, 210
MAXD = 430

# radial halftone: a grid of red dots, biggest near the sun, vanishing at the edges
spacing = 15
for gy in range(0, H+spacing, spacing):
    for gx in range(0, W+spacing, spacing):
        d = math.hypot(gx-CX, gy-CY)
        t = max(0.0, 1 - d/MAXD)
        r = 7.6 * (t ** 1.15)
        if r > 0.6:
            out.append(f'<circle cx="{gx}" cy="{gy}" r="{r:.2f}" fill="{R}"/>')

# the sun: flat white disc with a black rim, clipping the dots at the centre
out.append(f'<circle cx="{CX}" cy="{CY}" r="72" fill="{Wh}"/>')
out.append(f'<circle cx="{CX}" cy="{CY}" r="72" fill="none" stroke="{K}" stroke-width="4"/>')
# the day's marker: a single small red dot dead centre, noon exactly
out.append(f'<circle cx="{CX}" cy="{CY}" r="5" fill="{R}"/>')

# a band at the foot, flat black, to ground the piece and carry the title
out.append(f'<rect x="0" y="{H-64}" width="{W}" height="64" fill="{K}"/>')
out.append(f'<text x="{W/2}" y="{H-24}" font-family="DejaVu Sans, sans-serif" font-weight="bold" '
           f'font-size="20" fill="{Y}" text-anchor="middle" letter-spacing="6">FULL BURN</text>')

out.append('</svg>')
svg = "\n".join(out)
open(os.environ["OUT_RAW"].replace(".png",".svg"), "w").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(), write_to=os.environ["OUT_RAW"], output_width=W*2, output_height=H*2)
