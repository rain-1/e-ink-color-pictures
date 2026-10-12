"""Carta de la Mar Océana — a portolan of the first voyage, drawn sideways (east up,
north to the left), as portolans were read from any side of the table. Rhumb-line
network from a central rose and sixteen satellites; 3 Aug Palos -> 6 Sep Gomera ->
7 Oct the turn after the birds -> 12 Oct Guanahaní. Coastlines approximate."""
import math, random
from common import *
from PIL import Image, ImageDraw, ImageFont

random.seed(3)
c = Canvas(Y)
X0, X1, Y0, Y1 = 22, 378, 26, 516
LAT0, LAT1, LON0, LON1 = 13.0, 43.0, -82.0, 2.0
def P(lon, lat):
    return (X0 + (LAT1 - lat) / (LAT1 - LAT0) * (X1 - X0), Y0 + (LON1 - lon) / (LON1 - LON0) * (Y1 - Y0))

def rtext(x, y, s, size, angle, fill=K, font=SERIF_I):
    f = ImageFont.truetype(font, round(size * S))
    w = int(f.getlength(s)) + 8; h = round(size * S * 1.6)
    lay = Image.new("L", (w, h), 0)
    ImageDraw.Draw(lay).text((w / 2, h / 2), s, font=f, fill=255, anchor="mm")
    lay = lay.rotate(angle, expand=True, resample=Image.NEAREST)
    lay = lay.point(lambda v: 255 if v > 110 else 0)
    solid = Image.new("RGB", lay.size, fill)
    c.im.paste(solid, (round(x * S - lay.width / 2), round(y * S - lay.height / 2)), lay)

# ---------------- rhumb-line network
CX, CY = P(-44, 29)
RR = 205
centres = [(CX, CY)] + [(CX + RR * math.cos(2 * math.pi * k / 16), CY + RR * math.sin(2 * math.pi * k / 16)) for k in range(16)]
for (ox, oy) in centres:
    for k in range(32):
        a = 2 * math.pi * k / 32
        col = K if k % 4 == 0 else (G if k % 2 == 0 else R)
        wdt = 0.5
        c.line([(ox, oy), (ox + 700 * math.cos(a), oy + 700 * math.sin(a))], fill=col, width=wdt)

# ---------------- land
IBERIA = [(-1.8, 43.4), (-4, 43.5), (-8, 43.7), (-9.3, 43), (-8.8, 42), (-8.9, 40.5), (-9.5, 38.8), (-8.8, 38), (-8.9, 37),
          (-7.4, 37.2), (-6.3, 36.8), (-5.6, 36), (-4.5, 36.7), (-2, 36.7), (0, 38), (0, 44)]
AFRICA = [(-5.9, 35.8), (-6.9, 34), (-8.5, 33.2), (-9.6, 30.4), (-10.2, 29.3), (-11.5, 28.2), (-13, 27.6), (-14.5, 26.1), (-16, 24),
          (-16.9, 21.3), (-17, 20.8), (-16.1, 18), (-16.5, 16), (-17.5, 14.7), (-16.7, 13), (-16.7, 11), (0, 11), (0, 35.8)]
FLORIDA = [(-80.1, 27.5), (-80.1, 26), (-80.4, 25.2), (-81.1, 25.1), (-81.8, 26.1), (-82.6, 27.5), (-83, 30), (-80, 30)]
CUBA = [(-84.9, 21.9), (-83, 22.9), (-81, 23.1), (-79.5, 22.6), (-77.6, 21.8), (-75.7, 21.1), (-74.1, 20.2), (-74.5, 20.0),
        (-77.7, 19.9), (-77.2, 20.6), (-78.5, 21.5), (-80.5, 21.8), (-81.8, 22.2), (-83, 21.8)]
HISP = [(-74.4, 18.4), (-73, 19.9), (-71, 19.9), (-69, 19.3), (-68.3, 18.6), (-69, 18.4), (-71, 17.6), (-72.8, 18.2)]
PR = [(-67.2, 18.5), (-65.6, 18.4), (-65.6, 18.0), (-67.2, 18.0)]
JAM = [(-78.3, 18.4), (-76.2, 18.0), (-76.8, 17.8), (-78.3, 18.2)]
for poly in (IBERIA, AFRICA, FLORIDA, CUBA, HISP):
    pts = [P(*q) for q in poly]
    c.poly(pts, fill=G)
for poly in (PR, JAM):
    c.poly([P(*q) for q in poly], fill=R, outline=K, width=0.8)

# coast fringe: a white band and a black line, like ink over a wash
def coast(poly, closed=True):
    pts = [P(*q) for q in poly]
    if closed: pts = pts + [pts[0]]
    c.line(pts, fill=Wt, width=3.2)
    c.line(pts, fill=K, width=1)
for poly, cl in ((IBERIA, False), (AFRICA, False), (FLORIDA, False), (CUBA, True), (HISP, True)):
    coast(poly, cl)
# inland: little hills and castles in black on green, portolan-style vignettes
def hill(x, y, s=5):
    c.poly([(x - s, y + s * 0.6), (x, y - s * 0.6), (x + s, y + s * 0.6)], fill=G, outline=K, width=0.8)
    c.line([(x - s * 0.2, y), (x + s * 0.3, y + s * 0.5)], fill=K, width=0.5)
def castle(x, y, col=R):
    c.rect(x - 5, y - 4, x + 5, y + 4, fill=col, outline=K, width=0.7)
    for i in range(3):
        c.rect(x - 5 + i * 4, y - 7, x - 3 + i * 4, y - 4, fill=col, outline=K, width=0.5)
    c.rect(x - 1, y, x + 1, y + 4, fill=K)
for lon, lat in [(-5, 41), (-3, 39.5), (-6, 38.5), (-7.5, 41.5), (-2, 42), (-1, 40)]:
    hill(*P(lon, lat))
for lon, lat in [(-7, 31), (-9, 28.5), (-12, 24), (-8, 26), (-6, 29), (-13, 20), (-11, 17), (-14, 14.5), (-8, 15), (-9, 21)]:
    hill(*P(lon, lat), s=random.uniform(4, 7))
castle(*P(-4.5, 40.2))           # Castile
castle(*P(-7.5, 33.2), Wt)
# palms on Cuba and Hispaniola
def palm(x, y):
    c.line([(x, y + 6), (x + 1, y)], fill=K, width=1)
    for a in (-150, -110, -70, -30):
        r = math.radians(a)
        c.line([(x + 1, y), (x + 1 + 5 * math.cos(r), y + 5 * math.sin(r) + 2)], fill=K, width=0.8)
for lon, lat in [(-79, 22.2), (-76, 20.6), (-82, 22.4), (-71.5, 19), (-69.8, 18.9)]:
    palm(*P(lon, lat))

# islands, portolan-coloured
def isle(lon, lat, rx, ry, col, ang=0):
    x, y = P(lon, lat)
    c.ellipse(x, y, rx, ry, fill=col, outline=K, width=0.8)
canaries = [(-18, 28.7, 3, 3.5), (-17.3, 28.1, 3, 3), (-16.6, 28.3, 5, 6), (-15.6, 28, 4.5, 4.5), (-14, 28.4, 3.5, 7), (-13.6, 29, 3.5, 6), (-17.9, 27.7, 2.5, 2.5)]
for i, (lo, la, rx, ry) in enumerate(canaries):
    isle(lo, la, rx, ry, R if i % 2 else B)
x, y = P(-16.6, 28.3); c.poly([(x - 4, y + 2), (x, y - 5), (x + 4, y + 2)], fill=Wt, outline=K, width=0.6)  # Teide
for lo, la in [(-16.9, 32.7), (-16.3, 33.06)]:
    isle(lo, la, 3.5, 5, R)
for lo, la in [(-25.5, 37.8), (-25.1, 37.0), (-27.2, 38.7), (-28.0, 38.5), (-28.4, 38.4), (-28.7, 38.6), (-31.1, 39.4), (-31.2, 39.7)]:
    isle(lo, la, 3, 4, B)
for lo, la in [(-23.6, 15.1), (-24.4, 16.6), (-22.9, 16.1), (-22.9, 16.7), (-25.1, 17), (-24.7, 14.9), (-23.4, 15.2)]:
    isle(lo, la, 2.8, 3.2, R)
bahamas = [(-78, 24.4, 6, 9, G), (-77.4, 25.05, 2, 2.5, R), (-76.3, 25.2, 2, 8, B), (-75.5, 24.4, 2, 5, R),
           (-75.1, 23.3, 2, 6, B), (-76.2, 23.8, 1.5, 5, R), (-74, 22.4, 3, 4, B), (-73.3, 21.1, 5, 5, R),
           (-78.4, 26.6, 3, 9, B), (-77.2, 26.4, 4, 5, R), (-73.6, 22.9, 2, 2, R), (-72.2, 21.8, 3, 2.5, B)]
for lo, la, rx, ry, col in bahamas:
    isle(lo, la, rx, ry, col)
# Guanahaní: gold with a red cross
gx, gy = P(-74.5, 24.05)
c.circle(gx, gy, 6, fill=Wt, outline=K, width=1)
c.rect(gx - 1, gy - 4.5, gx + 1, gy + 4.5, fill=R); c.rect(gx - 4.5, gy - 1, gx + 4.5, gy + 1, fill=R)

# ---------------- the route
route = [(-6.95, 37.2), (-8.5, 35), (-12, 31), (-16, 28.5), (-17.3, 28.1), (-25, 28), (-35, 27.8), (-45, 27.5), (-55, 26.8),
         (-63, 26.2), (-67, 25.4), (-71, 24.6), (-74.3, 24.1)]
pts = [P(*q) for q in route]
# dashed, double: black dashes over a white ground line
for i in range(len(pts) - 1):
    (ax, ay), (bx, by) = pts[i], pts[i + 1]
    L = math.dist(pts[i], pts[i + 1]); n = int(L / 5)
    for k in range(n):
        if k % 2: continue
        t0, t1 = k / n, (k + 1) / n
        seg = [(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)]
        c.line(seg, fill=Wt, width=4.2)
        c.line(seg, fill=R if (k // 2) % 2 else K, width=2.4)
# the turn on 7 Oct, following birds
bx, by = P(-63, 26.2)
for k, (dx, dy) in enumerate([(-14, -10), (-6, -16), (8, -14), (-18, 2)]):
    s = 3.2
    x, y = bx + dx, by + dy
    c.line([(x - s, y - s * 0.3), (x - s * 0.4, y - s * 0.6), (x, y), (x + s * 0.4, y - s * 0.6), (x + s, y - s * 0.3)], fill=K, width=0.9)

# date stations
def station(lon, lat, label, dx, dy, ang=0):
    x, y = P(lon, lat)
    c.circle(x, y, 3.2, fill=Wt, outline=K, width=1)
    c.circle(x, y, 1.2, fill=R)
    if ang:
        rtext(x + dx, y + dy, label, 8.5, ang, K, SERIF_BI)
    else:
        c.text((x + dx, y + dy), label, 8.5, fill=K, font=SERIF_BI, anchor="mm")
station(-6.95, 37.2, "Palos · 3 VIII", -38, 4)
station(-17.3, 28.1, "Gomera · 6 IX", -10, 22)
station(-63, 26.2, "7 X · pájaros", 36, 2)
station(-45, 27.5, "", 0, 0)

# three caravels along the route
def caravel(x, y, s=1.0, col=Wt):
    c.poly([(x - 9 * s, y), (x + 9 * s, y), (x + 6 * s, y + 4 * s), (x - 7 * s, y + 4 * s)], fill=K)
    c.line([(x, y), (x, y - 14 * s)], fill=K, width=1)
    c.poly([(x - 6 * s, y - 13 * s), (x + 6 * s, y - 13 * s), (x + 7 * s, y - 3 * s), (x - 5 * s, y - 3 * s)], fill=col, outline=K, width=0.8)
    c.rect(x - 0.8 * s, y - 11 * s, x + 0.8 * s, y - 5 * s, fill=R); c.rect(x - 3 * s, y - 8.6 * s, x + 3 * s, y - 7.2 * s, fill=R)
    c.poly([(x - 8 * s, y - 1), (x - 6 * s, y - 10 * s), (x - 3 * s, y - 1)], fill=col, outline=K, width=0.7)
    c.poly([(x, y - 14 * s), (x + 5 * s, y - 13 * s), (x, y - 12 * s)], fill=R)
for lon, lat in [(-50, 27.2), (-34, 27.9), (-27, 28.1)]:
    x, y = P(lon, lat)
    caravel(x - 18, y, 1.5)

# ---------------- central compass rose (north points left: the chart is read sideways)
def rose(cx, cy, r, north_angle):
    c.circle(cx, cy, r + 6, fill=Wt, outline=K, width=1)
    c.circle(cx, cy, r + 2, outline=K, width=0.6)
    for k in range(32):
        a = math.radians(north_angle + k * 360 / 32)
        c.line([(cx + (r + 2) * math.cos(a), cy + (r + 2) * math.sin(a)), (cx + (r + 6) * math.cos(a), cy + (r + 6) * math.sin(a))], fill=K, width=0.6)
    for tier, (n, L, wd) in enumerate([(16, 0.55, 0.09), (8, 0.75, 0.12), (8, 1.0, 0.16)]):
        off = 360 / 32 if tier == 0 else (360 / 16 if tier == 1 else 0)
        for k in range(n):
            a = math.radians(north_angle + off + k * 360 / n)
            tip = (cx + r * L * math.cos(a), cy + r * L * math.sin(a))
            pa, pb = a + math.pi / 2, a - math.pi / 2
            w = r * wd
            left = (cx + w * math.cos(pa), cy + w * math.sin(pa)); right = (cx + w * math.cos(pb), cy + w * math.sin(pb))
            cols = [(R, Wt), (G, Wt), (K, Y)][tier]
            c.poly([(cx, cy), left, tip], fill=cols[0], outline=K, width=0.5)
            c.poly([(cx, cy), right, tip], fill=cols[1], outline=K, width=0.5)
    c.circle(cx, cy, r * 0.12, fill=R, outline=K, width=0.8)
    # fleur-de-lis at north
    a = math.radians(north_angle)
    fx, fy = cx + (r + 16) * math.cos(a), cy + (r + 16) * math.sin(a)
    ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
    def q(u, v): return (fx + u * ux + v * vx, fy + u * uy + v * vy)
    c.poly([q(-6, 0), q(6, -1.5), q(10, 0), q(6, 1.5)], fill=K)
    c.poly([q(-4, 0), q(1, -6), q(6, -8), q(2, -3)], fill=K)
    c.poly([q(-4, 0), q(1, 6), q(6, 8), q(2, 3)], fill=K)
    c.line([q(-3, -4), q(-3, 4)], fill=K, width=1.4)
    # east cross
    a = math.radians(north_angle + 90)
    ex, ey = cx + (r + 14) * math.cos(a), cy + (r + 14) * math.sin(a)
    c.rect(ex - 1, ey - 5, ex + 1, ey + 5, fill=R); c.rect(ex - 4, ey - 1, ex + 4, ey + 1, fill=R)
rose(CX, CY, 46, 180)   # north = pointing left (180°)

# ---------------- labels in the sea and on the land
rtext(*P(-33, 20), "MAR  OCÉANO", 15, 90, B, SERIF_B)
rtext(*P(-56, 33), "Mar de los Sargazos", 9.5, 90, K, SERIF_I)
for k in range(40):   # sargasso weed: little green tufts
    lon, lat = random.uniform(-62, -40), random.uniform(29, 36)
    x, y = P(lon, lat)
    if math.dist((x, y), (CX, CY)) < 60: continue
    for j in range(3):
        c.arc(x + j * 2, y, 2, 1.5, 0, 180, fill=G, width=0.8)
x, y = P(-74.5, 24.05)
c.text((x - 44, y + 8), "Guanahaní", 10, fill=R, font=SERIF_BI, anchor="mm")
c.text((x - 44, y + 19), "12 X 1492", 8, fill=K, font=SERIF_I, anchor="mm")
rtext(*P(-78.5, 21.0), "Juana", 8.5, 90, K, SERIF_I)
rtext(*P(-71, 18.4), "Española", 8, 90, K, SERIF_I)
rtext(*P(-5.5, 40.3), "Castilla", 9, 90, K, SERIF_BI)
rtext(*P(-9.0, 23.5), "África", 11, 90, K, SERIF_BI)
c.text(P(-17, 33.8), "Madera", 7.5, fill=K, font=SERIF_I, anchor="mm")
c.text(P(-28, 40.4), "Açores", 7.5, fill=K, font=SERIF_I, anchor="mm")
c.text(P(-24, 13.6), "Cabo Verde", 7.5, fill=K, font=SERIF_I, anchor="mm")
c.text(P(-15.5, 26.6), "Canarias", 7.5, fill=K, font=SERIF_I, anchor="mm")

# sea creature off the Azores, as was customary
mx, my = P(-36, 37)
for k in range(4):
    c.arc(mx + k * 9, my, 5, 5, 180, 360, fill=K, width=2)
    c.arc(mx + k * 9, my, 3.4, 3.4, 180, 360, fill=G, width=1.4)
c.circle(mx - 6, my - 2, 3.4, fill=G, outline=K, width=0.8); c.circle(mx - 7, my - 3, 0.9, fill=K)
c.line([(mx + 33, my - 1), (mx + 38, my - 6), (mx + 40, my + 1)], fill=K, width=1.4)
for k in range(3):
    c.line([(mx - 6, my - 6), (mx - 9 - k * 2, my - 12 - k)], fill=B, width=0.7)

# ---------------- frame: checker border + scale of leagues + title
c.rect(0, 0, 400, 600, outline=K, width=12)
for i in range(0, 600, 10):
    c.rect(0, i, 6, i + 5, fill=R if (i // 10) % 2 else Y)
    c.rect(394, i, 400, i + 5, fill=R if (i // 10) % 2 else Y)
for i in range(0, 400, 10):
    c.rect(i, 0, i + 5, 6, fill=R if (i // 10) % 2 else Y)
    c.rect(i, 594, i + 5, 600, fill=R if (i // 10) % 2 else Y)
c.rect(X0 - 2, Y0 - 2, X1 + 2, Y1 + 2, outline=K, width=1)
# title panel
c.rect(12, 522, 388, 588, fill=Wt, outline=K, width=1.2)
c.rect(15, 525, 385, 585, outline=R, width=0.7)
c.text((200, 540), "Carta de la Mar Océana", 15, fill=K, font=SERIF_BI, anchor="mm")
c.text((200, 556), "primer viaje · Palos — Gomera — Guanahaní · 1492", 8.5, fill=R, font=SERIF_I, anchor="mm")
# scale of leagues
sx0 = 70
for i in range(12):
    c.rect(sx0 + i * 22, 566, sx0 + (i + 1) * 22, 572, fill=K if i % 2 else Wt, outline=K, width=0.6)
    for j in range(1, 5):
        c.circle(sx0 + i * 22 + j * 4.4, 569, 0.8, fill=Wt if i % 2 else K)
c.text((200, 580), "escala de leguas", 7, fill=K, font=SERIF_I, anchor="mm")

finish(c)
