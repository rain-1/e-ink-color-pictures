"""Afternoon: an engraved, hand-coloured chart of the drift, with a log of the 101 nights' moons.
Pure palette, aliased drawing (fontmode 1) so nothing needs quantising."""
import os, sys, math, datetime as dt
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

im = Image.new("RGB", (W, H), WH); dr = ImageDraw.Draw(im); dr.fontmode = "1"

# ---------- map frame & projection (equirectangular, lon 156W..70W, lat 5N..31S)
MX0, MX1, MY0 = 12, 388, 74
LON0, LON1, LAT0, LAT1 = -156, -70, 5, -31
k = (MX1 - MX0) / (LON1 - LON0)
MY1 = MY0 + (LAT0 - LAT1) * k
def P(lon, lat): return (MX0 + (lon - LON0) * k, MY0 + (LAT0 - lat) * k)

# sea: engraved horizontal lines, densest near the coasts is too fussy — uniform, blue
for y in range(int(MY0) + 1, int(MY1), 3):
    dr.line([(MX0, y), (MX1, y)], fill=B)

# land: South America
coast = [(-77.5, 5), (-77.3, 3.5), (-78.8, 1.8), (-80.1, 0.0), (-80.9, -2.2), (-80.0, -3.0), (-81.3, -4.6),
         (-81.2, -6.0), (-79.9, -7.0), (-78.6, -9.0), (-77.1, -12.0), (-76.2, -13.7), (-75.0, -15.4),
         (-72.3, -17.0), (-70.3, -18.5), (-70.1, -20.2), (-70.4, -23.6), (-70.7, -27.0), (-71.4, -30.0), (-71.5, -31)]
land = [P(*c) for c in coast] + [(MX1, MY1), (MX1, MY0)]
dr.polygon(land, fill=Y)
# coastal ripple lines (old engraver's trick): offset copies of the coast in the sea
for off in (2.5, 5, 8):
    pts = [(x - off * (1 + i * 0.0), y) for i, (x, y) in enumerate([P(*c) for c in coast])]
    dr.line(pts, fill=WH, width=2)
    dr.line(pts, fill=B, width=1) if off == 8 else None
dr.line([P(*c) for c in coast], fill=K, width=2)
# the Andes: little hachured peaks
rng = np.random.default_rng(6)
for lat in np.arange(3, -31, -1.6):
    for j in range(2):
        cx = -76.5 + 2.2 * j + (0 if lat > -14 else 4.2) + (lat + 14) * 0.08 + rng.uniform(-0.5, 0.5)
        if cx > -70.4: continue
        x, y = P(cx, lat)
        dr.polygon([(x - 5, y + 3), (x, y - 5), (x + 5, y + 3)], fill=Y, outline=K)
        dr.line([(x, y - 5), (x + 2, y + 3)], fill=K)
dr.text(P(-75.4, -1.0), "PERU", fill=K, font=font(10, "serifb")) if False else None

def island(lon, lat, r=1.6, name=None, dx=4, dy=-12, ring=False, f=None):
    x, y = P(lon, lat)
    if ring:
        dr.ellipse([x - r, y - r, x + r, y + r], outline=K)
    else:
        dr.ellipse([x - r, y - r, x + r, y + r], fill=G, outline=K)
    if name:
        dr.rectangle([x + dx - 1, y + dy + 1, x + dx + dr.textlength(name, font=f or font(11, "serifi")) + 1, y + dy + 13], fill=WH)
        dr.text((x + dx, y + dy), name, fill=K, font=f or font(11, "serifi"))

# Tuamotus: a scatter of atolls (rings)
atolls = [(-148.0, -15.0), (-147.6, -15.2), (-146.4, -15.0), (-145.6, -16.3), (-145.0, -14.5), (-144.6, -15.6),
          (-143.6, -16.6), (-142.9, -14.9), (-142.2, -17.4), (-141.4, -18.3), (-140.9, -18.1), (-140.6, -19.6),
          (-139.0, -17.8), (-138.8, -14.8), (-140.9, -15.85), (-142.4, -16.0), (-144.0, -17.6), (-146.8, -16.1),
          (-137.0, -18.8), (-136.4, -19.8), (-139.4, -20.7), (-143.0, -19.3)]
for a in atolls: island(*a, r=2.2, ring=True)
for a in [(-140.1, -8.9), (-139.0, -9.8), (-138.6, -10.5), (-140.1, -9.4), (-139.6, -8.0)]: island(*a, r=2.2)
for a in [(-149.4, -17.6), (-149.8, -17.5), (-151.4, -16.7), (-151.7, -16.5)]: island(*a, r=2.4)
for a in [(-90.5, -0.6), (-91.2, -0.8), (-89.6, -0.9), (-90.3, -0.3), (-91.5, -0.2)]: island(*a, r=2.0)
for a in [(-109.4, -27.1), (-130.1, -25.1), (-134.9, -23.1), (-105.4, -26.5)]: island(*a, r=2.0)
F = font(11, "serifi")
island(-140.0, -9.0, 0, "Marquesas", dx=-70, dy=-14, f=F)
island(-149.4, -17.6, 0, "Tahiti", dx=-14, dy=6, f=F)
island(-90.5, -0.5, 0, "Galápagos", dx=-24, dy=6, f=F)
island(-109.4, -27.1, 0, "Rapa Nui", dx=-22, dy=4, f=F)
island(-130.1, -25.1, 0, "Pitcairn", dx=-20, dy=4, f=F)
island(-140.0, -19.5, 0, "Tuamotu", dx=-16, dy=6, f=F)

# currents: Humboldt north along the coast, South Equatorial westward — green arrows
def arrow(pts, col=G):
    q = [P(*p) for p in pts]
    dr.line(q, fill=col, width=2)
    (x1, y1), (x2, y2) = q[-2], q[-1]
    a = math.atan2(y2 - y1, x2 - x1)
    dr.polygon([(x2, y2), (x2 - 7 * math.cos(a - 0.45), y2 - 7 * math.sin(a - 0.45)),
                (x2 - 7 * math.cos(a + 0.45), y2 - 7 * math.sin(a + 0.45))], fill=col)
arrow([(-74.5, -28), (-75.5, -22), (-78, -16), (-81, -11), (-84, -8)])
arrow([(-80, -26), (-82, -20), (-86, -14), (-92, -10)])
for lon in (-100, -116, -132):
    arrow([(lon, -3.0), (lon - 8, -3.4)])
    arrow([(lon + 3, -11.5), (lon - 6, -12.0)])
for lbl, ll in (("Humboldt", (-86.6, -20.6)), ("S. Equatorial Current", (-155, -0.2))):
    x_, y_ = P(*ll); dr.rectangle([x_ - 1, y_ + 1, x_ + dr.textlength(lbl, font=font(11, "serifi")) + 1, y_ + 13], fill=WH)
dr.text(P(-86.6, -20.6), "Humboldt", fill=G, font=font(11, "serifi"))
dr.text(P(-155, -0.2), "S. Equatorial Current", fill=G, font=font(11, "serifi"))

# graticule
for lon in range(-150, -69, 10):
    x, _ = P(lon, 0)
    for y in range(int(MY0), int(MY1), 4): dr.point((x, y), fill=K)
    dr.text((x - 10, MY1 + 2), f"{-lon}°", fill=K, font=font(10, "sans"))
for lat in (0, -10, -20, -30):
    _, y = P(0, lat)
    for x in range(MX0, MX1, 4): dr.point((x, y), fill=K)
    dr.rectangle([MX1 - 31, y - 12, MX1 - 1, y], fill=WH, outline=K)
    dr.text((MX1 - 29, y - 12), f"{-lat}°S" if lat else "Eq.", fill=K, font=font(10, "sansb"))

# the track: Callao -> Raroia, 101 days
track = [(-77.1, -12.05), (-78.3, -11.6), (-80.5, -10.0), (-85, -8.0), (-90, -6.8), (-95, -6.3), (-100, -6.2),
         (-105, -6.5), (-110, -6.8), (-115, -7.0), (-120, -7.5), (-125, -8.0), (-130, -8.8), (-134, -10.2),
         (-137, -12.5), (-138.8, -14.4), (-140.9, -15.5), (-142.4, -16.0)]
tp = [P(*p) for p in track]
seg = [math.dist(tp[i], tp[i + 1]) for i in range(len(tp) - 1)]
L = sum(seg)
def along(f):
    d = f * L
    for i, s in enumerate(seg):
        if d <= s: t = d / s; return (tp[i][0] + (tp[i + 1][0] - tp[i][0]) * t, tp[i][1] + (tp[i + 1][1] - tp[i][1]) * t)
        d -= s
    return tp[-1]
for i in range(0, 200):
    if i % 2 == 0:
        dr.line([along(i / 200), along((i + 1) / 200)], fill=R, width=3)
for d in range(10, 81, 10):   # every ten days a tick + number
    x, y = along(d / 101)
    dr.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=K)
    dr.text((x - 6, y + 4), str(d), fill=K, font=font(10, "sansb"))
x, y = P(-77.1, -12.05); dr.ellipse([x - 4, y - 4, x + 4, y + 4], fill=R, outline=K)
dr.text((x - 14, y + 6), "Callao", fill=K, font=font(11, "serifb"))
x, y = P(-142.4, -16.0); dr.ellipse([x - 4, y - 4, x + 4, y + 4], fill=R, outline=K)
dr.rectangle([x - 46, y - 18, x - 5, y - 5], fill=WH)
dr.text((x - 45, y - 18), "Raroia", fill=K, font=font(11, "serifb"))

# tiny raft on the track, mid-ocean
rx, ry = along(0.5)
dr.rectangle([rx - 9, ry - 10, rx + 9, ry - 7], fill=Y, outline=K)
dr.polygon([(rx - 6, ry - 24), (rx + 6, ry - 24), (rx + 6, ry - 11), (rx - 6, ry - 11)], fill=WH, outline=K)
dr.ellipse([rx - 3, ry - 21, rx + 3, ry - 14], outline=R)

# compass rose, in open water south-west
cx, cy = P(-122, -21)
for i in range(16):
    a = i * math.pi / 8 - math.pi / 2
    Ln = 22 if i % 4 == 0 else (14 if i % 2 == 0 else 9)
    tip = (cx + Ln * math.cos(a), cy + Ln * math.sin(a))
    l = (cx + 3.5 * math.cos(a - math.pi / 2), cy + 3.5 * math.sin(a - math.pi / 2))
    r = (cx + 3.5 * math.cos(a + math.pi / 2), cy + 3.5 * math.sin(a + math.pi / 2))
    dr.polygon([l, tip, (cx, cy)], fill=K if i % 4 == 0 else WH, outline=K)
    dr.polygon([r, tip, (cx, cy)], fill=R if i % 4 == 0 else Y, outline=K)
dr.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], outline=K)
dr.text((cx - 4, cy - 40), "N", fill=K, font=font(11, "serifb"))

# whale, in the empty middle — the cartographer's sea-creature
wx, wy = P(-102, -18)
dr.chord([wx - 26, wy - 9, wx + 22, wy + 13], 180, 360, fill=K)
dr.polygon([(wx + 20, wy + 2), (wx + 32, wy - 9), (wx + 28, wy + 2), (wx + 34, wy + 10)], fill=K)
dr.line([(wx - 16, wy - 9), (wx - 20, wy - 17)], fill=B, width=1); dr.line([(wx - 16, wy - 9), (wx - 12, wy - 17)], fill=B, width=1)
dr.point((wx - 18, wy - 2), fill=WH)

dr.rectangle([MX0, MY0, MX1, MY1], outline=K, width=2)
dr.rectangle([MX0 - 3, MY0 - 3, MX1 + 3, MY1 + 3], outline=K, width=1)

# ---------- title cartouche
dr.text((MX0, 6), "KON-TIKI", fill=R, font=font(34, "serifb"))
dr.text((MX0 + 196, 10), "The drift of a balsa raft", fill=K, font=font(12, "serifi"))
dr.text((MX0 + 196, 26), "from Callao to Raroia, 1947", fill=K, font=font(12, "serifi"))
dr.text((MX0 + 196, 44), "for Thor Heyerdahl, b. 6.x.1914", fill=K, font=font(11, "serif"))
dr.line([(MX0, 54), (MX0 + 180, 54)], fill=K, width=2)
dr.text((MX0, 56), "4,300 nautical miles  ·  101 days", fill=K, font=font(10, "sans"))

# ---------- the log: one cell per day, with that night's moon
LY0 = MY1 + 30
dr.text((MX0, LY0 - 16), "LOG  ·  the moon on each of the hundred and one nights", fill=K, font=font(11, "serifb"))
start = dt.datetime(1947, 4, 28, 4)          # UTC, roughly local midnight in Peru
ref_new = dt.datetime(2000, 1, 6, 18, 14)
syn = 29.530588853
cols, cw, ch = 11, 34, 30
gx0 = (W - cols * cw) / 2
months = {4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII"}
for d in range(101):
    day = start + dt.timedelta(days=d)
    r_, c_ = divmod(d, cols)
    x0, y0 = gx0 + c_ * cw, LY0 + r_ * ch
    bg = B if day.month % 2 == 0 else K
    dr.rectangle([x0, y0, x0 + cw - 2, y0 + ch - 2], fill=bg)
    # moon phase: 0 new .. 0.5 full
    ph = ((day - ref_new).total_seconds() / 86400 / syn) % 1
    mx, my, mr = x0 + cw - 12, y0 + ch / 2 + 1, 8
    yy_, xx_ = np.mgrid[-mr:mr + 1, -mr:mr + 1]
    inside = xx_ ** 2 + yy_ ** 2 <= mr * mr
    tx = np.cos(2 * math.pi * ph) * np.sqrt(np.clip(mr * mr - yy_ ** 2, 0, None))
    lit = (xx_ < -tx) if ph < 0.5 else (xx_ > tx)       # seen from 10°S the waxing moon is lit on the left
    for (yy2, xx2) in zip(*np.nonzero(inside)):
        dr.point((mx + xx2 - mr, my + yy2 - mr), fill=Y if lit[yy2, xx2] else (bg if bg != K else K))
    dr.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=Y if bg == K else WH)
    dr.text((x0 + 2, y0 + 1), str(day.day), fill=WH, font=font(10, "sansb"))
    if day.day == 1 or d == 0:
        dr.text((x0 + 2, y0 + 14), months[day.month], fill=Y, font=font(9, "sansb"))
    if d == 0:
        dr.rectangle([x0, y0, x0 + cw - 2, y0 + ch - 2], outline=R, width=2)
    if day.date() in (dt.date(1947, 7, 30), dt.date(1947, 8, 4)):          # land sighted
        dr.rectangle([x0, y0, x0 + cw - 2, y0 + ch - 2], fill=G)
        dr.text((x0 + 2, y0 + 1), str(day.day), fill=WH, font=font(10, "sansb"))
        dr.line([(x0 + 22, y0 + 24), (x0 + 24, y0 + 8)], fill=K, width=2)
        for a in (-2.6, -2.0, -1.2, -0.5):
            dr.line([(x0 + 24, y0 + 8), (x0 + 24 + 8 * math.cos(a), y0 + 8 - 6 * math.sin(-a) + 4)], fill=Y, width=2)
    if d == 100:
        dr.rectangle([x0, y0, x0 + cw - 2, y0 + ch - 2], fill=R)
        dr.text((x0 + 2, y0 + 1), str(day.day), fill=WH, font=font(10, "sansb"))
        for j in range(4):
            dr.line([(x0 + 14 + j * 4, y0 + 22), (x0 + 18 + j * 4, y0 + 12)], fill=WH, width=2)
# legend under the log
ly = LY0 + 10 * ch + 2
dr.rectangle([gx0 + 2 * cw, ly + 2, gx0 + 2 * cw + 12, ly + 14], fill=G)
dr.text((gx0 + 2 * cw + 16, ly + 1), "land sighted", fill=K, font=font(11, "serif"))
dr.rectangle([gx0 + 6 * cw, ly + 2, gx0 + 6 * cw + 12, ly + 14], fill=R)
dr.text((gx0 + 6 * cw + 16, ly + 1), "on the reef", fill=K, font=font(11, "serif"))
im.save(os.environ.get("OUT_RAW", "chart.png"))
