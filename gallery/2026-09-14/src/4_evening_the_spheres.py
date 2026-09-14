# Evening — "The Spheres" (Paradiso). Palette: blue, yellow, white.
# Dante's cosmos as an astronomer's plate: Earth at centre, then the spheres of the Moon,
# Mercury, Venus, Sun, Mars, Jupiter, Saturn, the Fixed Stars, and the Primum Mobile.
# Engraved in yellow line on deep blue; the fixed-star sphere carries a band of white stars;
# the one star is Venus, the evening star, on its own ring. Emits SVG.
import os, math, random
random.seed(1265)
W,H=400,600; CX,CY=200,318
B,Y,Wh="#123DB0","#F5D400","#FFFFFF"
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',f'<rect width="{W}" height="{H}" fill="{B}"/>']
def circle(r,sw=1.2,col=Y,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{r:.1f}" fill="none" stroke="{col}" stroke-width="{sw}"{d}/>')
def ticks(r,n,length,sw=1,col=Y,every=1):
    for i in range(n):
        if i%every: continue
        a=2*math.pi*i/n
        o.append(f'<line x1="{CX+r*math.cos(a):.1f}" y1="{CY+r*math.sin(a):.1f}" x2="{CX+(r+length)*math.cos(a):.1f}" y2="{CY+(r+length)*math.sin(a):.1f}" stroke="{col}" stroke-width="{sw}"/>')
def arctext(r,text,start_deg,size=9,col=Y,letter=4):
    # place letters one by one along the ring, upright-ish, reading clockwise from start
    a=math.radians(start_deg)
    for ch in text:
        x=CX+r*math.cos(a); y=CY+r*math.sin(a)
        rot=math.degrees(a)+90
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Georgia, serif" font-size="{size}" fill="{col}" text-anchor="middle" transform="rotate({rot:.1f} {x:.1f} {y:.1f})">{ch}</text>')
        a+= (size*0.62+letter*0.5)/r
spheres=["LUNA","MERCURIUS","VENUS","SOL","MARS","IUPPITER","SATURNUS","STELLAE FIXAE","PRIMUM MOBILE"]
radii=[34,52,70,90,110,130,150,172,190]
# earth: a small disc with a horizon and water hatch
o.append(f'<circle cx="{CX}" cy="{CY}" r="16" fill="{Y}"/>')
o.append(f'<path d="M{CX-16},{CY} A16,16 0 0 0 {CX+16},{CY} Z" fill="{B}"/>')
for k in range(3):
    yy=CY+4+k*4
    hw=math.sqrt(max(0,16*16-(yy-CY)**2))
    o.append(f'<line x1="{CX-hw+1:.1f}" y1="{yy}" x2="{CX+hw-1:.1f}" y2="{yy}" stroke="{Y}" stroke-width="1"/>')
# spheres
for name,r in zip(spheres,radii):
    circle(r,1.4)
    circle(r-3,0.6)                             # doubled engraving line
    ticks(r,72,3,0.7)
    ticks(r,12,7,1.2)
    arctext(r-9,name,-90+8,size=9 if r<150 else 10)
# the planets as small yellow discs on their rings, at chosen angles; the Sun a bigger disc with rays
angles={"LUNA":200,"MERCURIUS":300,"VENUS":150,"SOL":335,"MARS":40,"IUPPITER":250,"SATURNUS":110}
for name,r in zip(spheres,radii):
    if name not in angles: continue
    a=math.radians(angles[name]); x=CX+r*math.cos(a); y=CY+r*math.sin(a)
    if name=="SOL":
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{Y}"/>')
        for i in range(12):
            b=2*math.pi*i/12
            o.append(f'<line x1="{x+11*math.cos(b):.1f}" y1="{y+11*math.sin(b):.1f}" x2="{x+16*math.cos(b):.1f}" y2="{y+16*math.sin(b):.1f}" stroke="{Y}" stroke-width="1.3"/>')
    elif name=="LUNA":
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{Y}"/>')
        o.append(f'<circle cx="{x+3:.1f}" cy="{y-1:.1f}" r="5.5" fill="{B}"/>')
    elif name=="VENUS":
        # the one star: Venus, white, six-pointed
        pts=" ".join(f"{x+(9 if i%2==0 else 3.5)*math.cos(math.pi*i/6+math.pi/2):.1f},{y+(9 if i%2==0 else 3.5)*math.sin(math.pi*i/6+math.pi/2):.1f}" for i in range(12))
        o.append(f'<polygon points="{pts}" fill="{Wh}"/>')
    elif name=="SATURNUS":
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{Y}"/>')
        o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="10" ry="3" fill="none" stroke="{Y}" stroke-width="1.2" transform="rotate(-20 {x:.1f} {y:.1f})"/>')
    else:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{Y}"/>')
# the fixed stars: a band of white pinpricks between r=161 and r=171
for _ in range(210):
    a=random.uniform(0,2*math.pi); r=random.uniform(160,170)
    s=random.choice([0.8,1.0,1.3,1.6])
    o.append(f'<circle cx="{CX+r*math.cos(a):.1f}" cy="{CY+r*math.sin(a):.1f}" r="{s}" fill="{Wh}"/>')
# zodiac band on the Primum Mobile: twelve sectors, each with a tiny glyph-like mark (abstract)
for i in range(12):
    a=math.radians(i*30-90+15); x=CX+181*math.cos(a); y=CY+181*math.sin(a)
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="none" stroke="{Wh}" stroke-width="0.9"/>')
# the outermost line: the Empyrean, not a sphere but a border of the plate — corner ornaments
o.append(f'<rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="{Y}" stroke-width="1.5"/>')
o.append(f'<rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" stroke="{Y}" stroke-width="0.6"/>')
for (x,y) in [(12,12),(W-12,12),(12,H-12),(W-12,H-12)]:
    o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{B}" stroke="{Y}" stroke-width="1.2"/>')
# plate title and a line from the last canto's idea, set small at the foot
o.append(f'<text x="200" y="548" font-family="Georgia, serif" font-size="15" fill="{Y}" text-anchor="middle" letter-spacing="5">PARADISO</text>')
o.append(f'<text x="200" y="568" font-family="Georgia, serif" font-style="italic" font-size="10" fill="{Wh}" text-anchor="middle">the nine spheres · Ravenna · 14 September 1321</text>')
o.append(f'<text x="200" y="52" font-family="Georgia, serif" font-size="10" fill="{Y}" text-anchor="middle" letter-spacing="3">TABULA CAELI</text>')
svg="\n".join(o+["</svg>"])
open(os.environ["OUT_RAW"].replace(".png",".svg"),"w").write(svg)
import cairosvg; cairosvg.svg2png(bytestring=svg.encode(),write_to=os.environ["OUT_RAW"],output_width=800,output_height=1200)
