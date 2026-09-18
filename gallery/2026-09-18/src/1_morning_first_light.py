# Morning — "First Light". Hard-edge flat colour, no outlines (Indiana school).
# Palette: red, white, black. A sun cut by the horizon, rising; four ticks count
# the days to the equinox (Sept 22 is four days off).
import os, math
W,H=400,600
R,Wh,K="#E01B24","#FFFFFF","#000000"
out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{Wh}"/>']

CX, HORIZON = 200, 420
SUN_R = 150

# hard-edge rays: bold flat red triangles fanning up from the sun, alternating long/short
n_rays = 7
for i in range(n_rays):
    ang = -math.pi/2 + (i - n_rays//2) * (math.pi*0.78/n_rays)
    length = 250 if i % 2 == 0 else 175
    half = 0.075
    x0 = CX + SUN_R*0.25*math.cos(ang - half); y0 = HORIZON + SUN_R*0.25*math.sin(ang - half)
    x1 = CX + SUN_R*0.25*math.cos(ang + half); y1 = HORIZON + SUN_R*0.25*math.sin(ang + half)
    x2 = CX + length*math.cos(ang); y2 = HORIZON + length*math.sin(ang)
    out.append(f'<polygon points="{x0:.1f},{y0:.1f} {x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f}" fill="{R}"/>')

# the sun itself, a flat red disc straddling the horizon
out.append(f'<circle cx="{CX}" cy="{HORIZON}" r="{SUN_R}" fill="{R}"/>')

# land: a flat black hill silhouette that clips the lower half of the sun
out.append(f'<path d="M0,{HORIZON+34} C110,{HORIZON-26} 290,{HORIZON+58} {W},{HORIZON+10} '
           f'L{W},{H} L0,{H} Z" fill="{K}"/>')

# four ticks, cut white into the black land: days left to the equinox
tx, ty = 34, 500
for i in range(4):
    x = tx + i*16
    out.append(f'<line x1="{x}" y1="{ty}" x2="{x}" y2="{ty+26}" stroke="{Wh}" stroke-width="5"/>')
out.append(f'<text x="{tx}" y="{ty+46}" font-family="DejaVu Sans, sans-serif" '
           f'font-size="11" fill="{Wh}" letter-spacing="2">TO THE EQUINOX</text>')

out.append(f'<text x="{W-24}" y="60" font-family="DejaVu Sans, sans-serif" font-weight="bold" '
           f'font-size="15" fill="{K}" text-anchor="end" letter-spacing="3">FIRST LIGHT</text>')

out.append('</svg>')
svg = "\n".join(out)
open(os.environ["OUT_RAW"].replace(".png",".svg"), "w").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(), write_to=os.environ["OUT_RAW"], output_width=W*2, output_height=H*2)
