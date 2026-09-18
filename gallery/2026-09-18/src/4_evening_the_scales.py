# Evening — "The Scales". Bold poster / screenprint: a balance beam with day in one pan,
# night in the other, still tipped toward day but nearly level. Palette: red, blue, white.
import os, math
W,H=400,600
R,Bl,Wh,K="#E01B24","#123DB0","#FFFFFF","#000000"
out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">']

# poster ground: split field, red upper (day), blue lower (night), hard edge
SPLIT = 300
out.append(f'<rect x="0" y="0" width="{W}" height="{SPLIT}" fill="{R}"/>')
out.append(f'<rect x="0" y="{SPLIT}" width="{W}" height="{H-SPLIT}" fill="{Bl}"/>')

CX, FULCRUM_Y = 200, 330
BEAM_LEN = 260
TILT = math.radians(7)  # still tipped toward day, four days out from level

# fulcrum: a flat white triangle
out.append(f'<polygon points="{CX-26},{FULCRUM_Y+70} {CX+26},{FULCRUM_Y+70} {CX},{FULCRUM_Y} " fill="{Wh}"/>')
out.append(f'<rect x="{CX-40}" y="{FULCRUM_Y+70}" width="80" height="14" fill="{Wh}"/>')

# beam, tilted: left end up (lighter, day pan) is drawn lower value... left = day higher? Day
# is heavier this week (longer), so its pan sits lower.
lx = CX - BEAM_LEN/2*math.cos(TILT); ly = FULCRUM_Y - BEAM_LEN/2*math.sin(TILT)
rx = CX + BEAM_LEN/2*math.cos(TILT); ry = FULCRUM_Y + BEAM_LEN/2*math.sin(TILT)
out.append(f'<line x1="{lx:.1f}" y1="{ly:.1f}" x2="{rx:.1f}" y2="{ry:.1f}" stroke="{Wh}" stroke-width="7"/>')
out.append(f'<circle cx="{CX}" cy="{FULCRUM_Y}" r="7" fill="{Wh}"/>')

# chains and pans
def pan(px, py, fill, symbol):
    out.append(f'<line x1="{px-30:.1f}" y1="{py-40:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="{Wh}" stroke-width="2.5"/>')
    out.append(f'<line x1="{px+30:.1f}" y1="{py-40:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="{Wh}" stroke-width="2.5"/>')
    out.append(f'<path d="M{px-38:.1f},{py:.1f} A38,14 0 0 0 {px+38:.1f},{py:.1f} Z" fill="{fill}" stroke="{Wh}" stroke-width="3"/>')
    symbol(px, py-10)

def sun_symbol(px,py):
    out.append(f'<circle cx="{px}" cy="{py}" r="17" fill="{Wh}"/>')
    for i in range(8):
        a = i*math.pi/4
        out.append(f'<line x1="{px+22*math.cos(a):.1f}" y1="{py+22*math.sin(a):.1f}" '
                   f'x2="{px+30*math.cos(a):.1f}" y2="{py+30*math.sin(a):.1f}" stroke="{Wh}" stroke-width="3"/>')

def star_symbol(px,py):
    pts=[]
    for i in range(8):
        r = 17 if i%2==0 else 8
        a = i*math.pi/4 - math.pi/2
        pts.append(f"{px+r*math.cos(a):.1f},{py+r*math.sin(a):.1f}")
    out.append(f'<polygon points="{" ".join(pts)}" fill="{Wh}"/>')

pans_y = ly+38, ry+38
pan(lx, pans_y[0], R, sun_symbol)   # day, left, heavier this week: sits lower relative to beam
pan(rx, pans_y[1], Bl, star_symbol) # night, right

# a thin white rule marking true level, for reference, faint
lvl_y = FULCRUM_Y
out.append(f'<line x1="{CX-BEAM_LEN/2-14:.1f}" y1="{lvl_y}" x2="{CX+BEAM_LEN/2+14:.1f}" y2="{lvl_y}" '
           f'stroke="{Wh}" stroke-width="0.8" stroke-dasharray="1,4"/>')

# title, bottom, reversed out of the blue field
out.append(f'<text x="{CX}" y="{H-30}" font-family="DejaVu Serif, serif" font-size="18" fill="{Wh}" '
           f'text-anchor="middle" letter-spacing="5">THE SCALES</text>')
out.append(f'<text x="{CX}" y="{H-14}" font-family="DejaVu Sans Mono, monospace" font-size="9" fill="{Wh}" '
           f'text-anchor="middle" letter-spacing="1">FOUR DAYS FROM LEVEL</text>')

out.append('</svg>')
svg = "\n".join(out)
open(os.environ["OUT_RAW"].replace(".png",".svg"), "w").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(), write_to=os.environ["OUT_RAW"], output_width=W*2, output_height=H*2)
