# Afternoon — "Daylight, Plotted". A blueprint: hours of daylight from midsummer to
# midwinter at 45N (approximate), the curve crossing 12h at the equinox. Palette: blue, white.
import os, math, datetime
W,H=400,600
B,Wh="#123DB0","#FFFFFF"
out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{Wh}"/>']

# frame: a double blueprint border with corner register marks
out.append(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="{B}" stroke-width="2"/>')
out.append(f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="{B}" stroke-width="0.8"/>')
for cx,cy in [(10,10),(W-10,10),(10,H-10),(W-10,H-10)]:
    out.append(f'<line x1="{cx-9}" y1="{cy}" x2="{cx+9}" y2="{cy}" stroke="{B}" stroke-width="1"/>')
    out.append(f'<line x1="{cx}" y1="{cy-9}" x2="{cx}" y2="{cy+9}" stroke="{B}" stroke-width="1"/>')

PX0, PX1 = 46, 354      # plot area x
PY0, PY1 = 470, 130     # plot area y (PY0 bottom/low daylight, PY1 top/high daylight)
DOY0, DOY1 = 152, 365   # Jun 1 .. Dec 31
HMIN, HMAX = 8.0, 16.0  # hours axis range

def xy(doy, h):
    x = PX0 + (doy-DOY0)/(DOY1-DOY0)*(PX1-PX0)
    y = PY0 + (h-HMIN)/(HMAX-HMIN)*(PY1-PY0)
    return x, y

def daylen(doy):
    return 12 + 3.6*math.sin(2*math.pi*(doy-80)/365)

# horizontal gridlines at 8/10/12/14/16h, the 12h line drawn heavier — the balance line
for h in [8,10,12,14,16]:
    x0,y0 = xy(DOY0,h); x1,y1 = xy(DOY1,h)
    w = 1.6 if h==12 else 0.6
    dash = "" if h==12 else ' stroke-dasharray="1,3"'
    out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{B}" stroke-width="{w}"{dash}/>')
    out.append(f'<text x="{PX0-8:.1f}" y="{y0+3:.1f}" font-family="Courier New, monospace" font-size="9" '
               f'fill="{B}" text-anchor="end">{h}h</text>')

# vertical ticks per month
months = [("JUN",152),("JUL",182),("AUG",213),("SEP",244),("OCT",274),("NOV",305),("DEC",335)]
for name,doy in months:
    x,_ = xy(doy, HMIN)
    out.append(f'<line x1="{x:.1f}" y1="{PY0}" x2="{x:.1f}" y2="{PY0+5}" stroke="{B}" stroke-width="1"/>')
    out.append(f'<text x="{x:.1f}" y="{PY0+17}" font-family="Courier New, monospace" font-size="8.5" '
               f'fill="{B}" text-anchor="middle">{name}</text>')

# the curve
pts = []
for doy in range(DOY0, DOY1+1):
    x,y = xy(doy, daylen(doy))
    pts.append(f"{x:.1f},{y:.1f}")
out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{B}" stroke-width="2.4"/>')

# today (Sep 18, doy 261) and the equinox (Sep 22, doy 265)
for doy,label,r,filled in [(261,"SEP 18 - TODAY",4,True), (265,"SEP 22 - EQUINOX",6,False)]:
    x,y = xy(doy, daylen(doy))
    xt,_ = xy(doy, HMIN)
    out.append(f'<line x1="{xt:.1f}" y1="{y:.1f}" x2="{xt:.1f}" y2="{PY0}" stroke="{B}" stroke-width="0.6" stroke-dasharray="2,2"/>')
    fill = B if filled else Wh
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{B}" stroke-width="2"/>')

out.append(f'<text x="{PX0}" y="106" font-family="DejaVu Sans Mono, monospace" font-size="9" fill="{B}">SEP 18 - TODAY, 12h02m</text>')
out.append(f'<text x="{PX0}" y="120" font-family="DejaVu Sans Mono, monospace" font-size="9" fill="{B}">SEP 22 - EQUINOX, 12h00m exactly</text>')

# title block, bottom right, like a drafting sheet
out.append(f'<line x1="{PX0}" y1="500" x2="{PX1}" y2="500" stroke="{B}" stroke-width="1"/>')
out.append(f'<text x="{PX0}" y="516" font-family="DejaVu Serif, serif" font-size="14" fill="{B}" letter-spacing="2">DAYLIGHT, PLOTTED</text>')
out.append(f'<text x="{PX0}" y="532" font-family="DejaVu Sans Mono, monospace" font-size="8.5" fill="{B}">45N (APPROX.) - JUN-DEC 2026</text>')
out.append(f'<text x="{PX0}" y="546" font-family="DejaVu Sans Mono, monospace" font-size="8.5" fill="{B}">SCALE: 1 DIV = 2 HOURS</text>')

out.append('</svg>')
svg = "\n".join(out)
open(os.environ["OUT_RAW"].replace(".png",".svg"), "w").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(), write_to=os.environ["OUT_RAW"], output_width=W*2, output_height=H*2)
