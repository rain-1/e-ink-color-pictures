# Midday — "The Mountain" (Purgatorio). Palette: yellow, black, white.
# Seven terraces rising to a flat summit, a stair spiralling up the sunlit side, a figure
# climbing, a hard white sun. Drawn as stacked tiers with a shaded face. Emits SVG.
import os, math
W,H=400,600
Y,B,Wh="#F5D400","#000000","#FFFFFF"
out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{Y}"/>']
# sun: white disc with a black rim-ring, hard midday, upper right
out.append(f'<circle cx="318" cy="88" r="46" fill="{Wh}"/>')
out.append(f'<circle cx="318" cy="88" r="52" fill="none" stroke="{B}" stroke-width="3"/>')
# sea at the foot of the mountain: black horizontal rules that thin as they go up
for i,y in enumerate(range(560,470,-9)):
    out.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{B}" stroke-width="{max(1,4-i*0.4):.1f}"/>')
out.append(f'<rect x="0" y="560" width="{W}" height="40" fill="{B}"/>')
# terraces: 7 tiers + summit. Each tier: an ellipse top (yellow), a right-side shadow (black)
CX=200; base_y=500; base_rx=190; ry_ratio=0.28; tier_h=52
tiers=7
for i in range(0,tiers+1):
    frac=i/tiers
    rx=base_rx*(0.18+0.82*(1-frac)); ry=rx*ry_ratio
    y=base_y-i*tier_h
    # the cylinder wall of this tier (from this tier's top down to the one below)
    out.append(f'<rect x="{CX-rx:.1f}" y="{y:.1f}" width="{2*rx:.1f}" height="{tier_h}" fill="{Y}"/>')
    # shadow side: right half of the wall in black, drawn as a path hugging the ellipse
    out.append(f'<path d="M{CX:.1f},{y:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {CX+rx:.1f},{y:.1f} '
               f'L{CX+rx:.1f},{y+tier_h:.1f} A{rx:.1f},{ry:.1f} 0 0 1 {CX:.1f},{y+tier_h:.1f} Z" fill="{B}"/>')
    # lit side gets thin black contour hatching (rock strata)
    for k in range(4):
        yy=y+10+k*11
        out.append(f'<path d="M{CX-rx+6:.1f},{yy:.1f} A{rx:.1f},{ry*0.9:.1f} 0 0 0 {CX-4:.1f},{yy+ry*0.85:.1f}" '
                   f'fill="none" stroke="{B}" stroke-width="1.2"/>')
    # top ellipse: yellow with black outline
    out.append(f'<ellipse cx="{CX}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{Y}" stroke="{B}" stroke-width="2.5"/>')
    # ledge shadow line just under the lip on the dark side
    out.append(f'<path d="M{CX:.1f},{y+ry:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {CX+rx:.1f},{y:.1f}" fill="none" stroke="{Wh}" stroke-width="1.5"/>')
# the stair: a zig-zag cut into the lit face, tier by tier
for i in range(tiers):
    frac=i/tiers; rx=base_rx*(0.18+0.82*(1-frac)); y=base_y-i*tier_h
    x0=CX-rx*0.55; x1=CX-rx*0.15
    steps=6
    for s in range(steps):
        t=s/steps; t2=(s+1)/steps
        xa=x0+(x1-x0)*t; xb=x0+(x1-x0)*t2
        ya=y+tier_h-(tier_h)*t; yb=y+tier_h-(tier_h)*t2
        out.append(f'<path d="M{xa:.1f},{ya:.1f} L{xb:.1f},{ya:.1f} L{xb:.1f},{yb:.1f}" fill="none" stroke="{B}" stroke-width="2.5"/>')
        out.append(f'<line x1="{xa+1:.1f}" y1="{ya-1.5:.1f}" x2="{xb:.1f}" y2="{ya-1.5:.1f}" stroke="{Wh}" stroke-width="1.5"/>')
# a gate at the third terrace (the gate of Purgatory, three steps)
gy=base_y-2*tier_h+tier_h-2; gx=CX-base_rx*(0.18+0.82*(1-2/tiers))*0.35
out.append(f'<rect x="{gx-8:.1f}" y="{gy-26:.1f}" width="16" height="26" fill="{B}"/>')
out.append(f'<path d="M{gx-8:.1f},{gy-26:.1f} A8,8 0 0 1 {gx+8:.1f},{gy-26:.1f}" fill="{B}"/>')
# the climber: on the fifth terrace, small, black, with a white staff
fy=base_y-4*tier_h+tier_h-4; fx=CX-base_rx*(0.18+0.82*(1-4/tiers))*0.35
out.append(f'<circle cx="{fx:.1f}" cy="{fy-16:.1f}" r="3.5" fill="{B}"/>')
out.append(f'<path d="M{fx-3:.1f},{fy-12:.1f} L{fx+3:.1f},{fy-12:.1f} L{fx+4:.1f},{fy:.1f} L{fx-4:.1f},{fy:.1f} Z" fill="{B}"/>')
out.append(f'<line x1="{fx+7:.1f}" y1="{fy-20:.1f}" x2="{fx+7:.1f}" y2="{fy:.1f}" stroke="{Wh}" stroke-width="1.5"/>')
out.append(f'<line x1="{fx+7:.1f}" y1="{fy-20:.1f}" x2="{fx+7:.1f}" y2="{fy:.1f}" stroke="{B}" stroke-width="3.5" stroke-dasharray="1,2"/>')
# the summit: a single tree on the flat top (the earthly paradise) and the one star straight above it
ty=base_y-tiers*tier_h
out.append(f'<line x1="{CX}" y1="{ty:.1f}" x2="{CX}" y2="{ty-30:.1f}" stroke="{B}" stroke-width="3"/>')
out.append(f'<ellipse cx="{CX}" cy="{ty-38:.1f}" rx="14" ry="12" fill="{B}"/>')
out.append(f'<ellipse cx="{CX}" cy="{ty-38:.1f}" rx="6" ry="5" fill="{Y}"/>')
sx,sy=CX,34
out.append(f'<polygon points="{sx},{sy-12} {sx+3},{sy-3} {sx+12},{sy} {sx+3},{sy+3} {sx},{sy+12} {sx-3},{sy+3} {sx-12},{sy} {sx-3},{sy-3}" fill="{Wh}" stroke="{B}" stroke-width="1.5"/>')
# title rule, printed
out.append(f'<text x="200" y="590" font-family="Georgia, serif" font-size="13" fill="{Y}" text-anchor="middle" letter-spacing="4">PURGATORIO</text>')
out.append('</svg>')
open(os.environ["OUT_RAW"].replace(".png",".svg"),"w").write("\n".join(out))
import cairosvg; cairosvg.svg2png(bytestring="\n".join(out).encode(),write_to=os.environ["OUT_RAW"],output_width=800,output_height=1200)
