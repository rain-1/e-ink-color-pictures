# Night — "Nubeculae". The southern sky as the fleet saw it from the strait, late October
# 1520, about ten at night, looking south from 53°S: the two Magellanic Clouds (Pigafetta
# was the first European to write them down), the Cross low in the south, Canopus, Achernar
# near the zenith, the Milky Way with the Coalsack. Below, the shore of Tierra del Fuego —
# the "land of fire", named for the campfires the fleet saw at night — and the water
# with the fires in it. Star positions computed from a real catalogue and a real hour.
# Drawn with PIL in pure palette colours; render with --dither none.
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
random.seed(1520)
W, H = 400, 600
K, Wt, R, Y, B, G = (0, 0, 0), (255, 255, 255), (224, 27, 36), (245, 212, 0), (18, 61, 176), (30, 155, 60)
im = Image.new("RGB", (W, H), K); dr = ImageDraw.Draw(im)
LAT, LST = -53.0, 1.0            # observer latitude, local sidereal time (hours)
HORIZON = 470                    # y of the sea horizon

def altaz(ra_h, dec):
    ha = math.radians((LST - ra_h) * 15); d = math.radians(dec); f = math.radians(LAT)
    sa = math.sin(f) * math.sin(d) + math.cos(f) * math.cos(d) * math.cos(ha)
    alt = math.asin(max(-1, min(1, sa)))
    az = math.atan2(-math.sin(ha) * math.cos(d), math.cos(f) * math.sin(d) - math.sin(f) * math.cos(d) * math.cos(ha))
    return math.degrees(alt), (math.degrees(az) + 360) % 360
def screen_xy(ra_h, dec):
    alt, az = altaz(ra_h, dec)
    dx = ((az - 180) + 180) % 360 - 180          # 0 at due south
    if abs(dx) > 84 or alt < -2: return None
    return (200 + dx / 84 * 200, HORIZON - alt / 88 * (HORIZON - 14)), alt

# ---------------- twilight: a screened blue band low in the south-west ----------------
b8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38],
               [60, 28, 52, 20, 62, 30, 54, 22], [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
               [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64.0
px = im.load()
for y in range(330, HORIZON):
    for x in range(W):
        t = ((y - 330) / (HORIZON - 330)) ** 2.2 * (0.25 + 0.55 * max(0.0, (x - 60) / 340))   # brighter to the west (right)
        if t > b8[y % 8, x % 8] * 0.75:
            px[x, y] = B

# ---------------- galactic → equatorial, for the Milky Way ------------------------------
AG, DG, LN = math.radians(192.859), math.radians(27.128), math.radians(122.932)
def gal2eq(l, b):
    l, b = math.radians(l), math.radians(b)
    sd = math.sin(DG) * math.sin(b) + math.cos(DG) * math.cos(b) * math.cos(LN - l)
    d = math.asin(sd)
    y = math.cos(b) * math.sin(LN - l)
    x = math.cos(DG) * math.sin(b) - math.sin(DG) * math.cos(b) * math.cos(LN - l)
    a = AG + math.atan2(y, x)
    return (math.degrees(a) / 15) % 24, math.degrees(d)
def bright(l):   # the band is brightest toward the centre (l≈0) and Carina, faintest at the anticentre
    return 0.35 + 0.65 * (0.5 + 0.5 * math.cos(math.radians(l))) ** 1.2 + 0.35 * math.exp(-((l - 290) / 25) ** 2)
def ink(pt, col, r=0):
    x, y = pt
    if y >= HORIZON - 1: return
    if r <= 0: dr.point((x, y), fill=col)
    else: dr.ellipse([x - r, y - r, x + r, y + r], fill=col)
for _ in range(16000):
    l = random.uniform(0, 360); b = random.gauss(0, 5.5)
    if random.random() > bright(l) * 0.9: continue
    # the Coalsack and the great rift are holes
    if math.hypot(l - 303, b + 1.5) < 3.2 and random.random() < 0.93: continue
    if 0 < l < 40 and -2 < b < 6 and random.random() < 0.7: continue
    ra, dec = gal2eq(l, b)
    s = screen_xy(ra, dec)
    if s: ink(s[0], Wt)
# the Carina nebula and Omega Centauri as small dense patches; 47 Tucanae
for (ra, dec, n, sig, r) in [(10.75, -59.7, 260, 0.9, 0), (13.45, -47.5, 110, 0.35, 0), (0.40, -72.1, 130, 0.35, 0)]:
    for _ in range(n):
        s = screen_xy(ra + random.gauss(0, sig) / 15 / math.cos(math.radians(dec)), dec + random.gauss(0, sig))
        if s: ink(s[0], Wt)

# ---------------- the two clouds -----------------------------------------------------
def cloud(ra, dec, n, sx, sy, ang, bar=0.0):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    for i in range(n):
        u, v = random.gauss(0, sx), random.gauss(0, sy)
        if bar and random.random() < bar: u, v = random.uniform(-sx * 1.4, sx * 1.4), random.gauss(0, sy * 0.28)
        dl, db = u * ca - v * sa, u * sa + v * ca
        s = screen_xy(ra + dl / 15 / math.cos(math.radians(dec)), dec + db)
        if s: ink(s[0], Wt, 1 if random.random() < 0.06 else 0)
cloud(5.39, -69.75, 1700, 2.6, 1.7, 25, bar=0.35)      # Nubecula Major, with its bar
cloud(0.87, -72.8, 700, 1.6, 1.0, 40)                   # Nubecula Minor
for _ in range(60):                                      # the Tarantula, a knot at the LMC's edge
    s = screen_xy(5.65 + random.gauss(0, 0.02), -69.1 + random.gauss(0, 0.3))
    if s: ink(s[0], Wt)

# ---------------- stars ---------------------------------------------------------------
STARS = {  # name: (RA h, Dec °, mag)
    "Acrux": (12.44, -63.1, 0.8), "Mimosa": (12.80, -59.7, 1.3), "Gacrux": (12.52, -57.1, 1.6), "δ Cru": (12.25, -58.7, 2.8), "ε Cru": (12.36, -60.4, 3.6),
    "Rigil Kent": (14.66, -60.8, -0.3), "Hadar": (14.06, -60.4, 0.6), "γ Cen": (12.69, -49.0, 2.2), "ε Cen": (13.66, -53.5, 2.3), "ζ Cen": (13.93, -47.3, 2.5),
    "δ Cen": (12.14, -50.7, 2.6), "η Cen": (14.59, -42.2, 2.3), "θ Cen": (14.11, -36.4, 2.1), "ι Cen": (13.34, -36.7, 2.7),
    "Canopus": (6.40, -52.7, -0.7), "Miaplacidus": (9.22, -69.7, 1.7), "Avior": (8.38, -59.5, 1.9), "Aspidiske": (9.28, -59.3, 2.2), "θ Car": (10.72, -64.4, 2.8), "υ Car": (9.78, -65.1, 3.0),
    "γ Vel": (8.16, -47.3, 1.8), "δ Vel": (8.75, -54.7, 2.0), "λ Vel": (9.13, -43.4, 2.2), "κ Vel": (9.37, -55.0, 2.5), "μ Vel": (10.78, -49.4, 2.7),
    "Naos": (8.06, -40.0, 2.2), "π Pup": (7.28, -37.1, 2.7), "Sirius": (6.75, -16.7, -1.5), "Adhara": (6.98, -29.0, 1.5), "Wezen": (7.14, -26.4, 1.8), "Mirzam": (6.38, -18.0, 2.0),
    "Achernar": (1.63, -57.2, 0.5), "Acamar": (2.97, -40.3, 3.2), "β Hyi": (0.43, -77.3, 2.8), "α Hyi": (1.98, -61.6, 2.9), "γ Hyi": (3.79, -74.2, 3.2),
    "α Tuc": (22.31, -60.3, 2.9), "Peacock": (20.43, -56.7, 1.9), "Alnair": (22.14, -47.0, 1.7), "β Gru": (22.71, -46.9, 2.1), "γ Gru": (21.90, -37.4, 3.0),
    "Ankaa": (0.44, -42.3, 2.4), "β Phe": (1.10, -46.7, 3.3), "Fomalhaut": (22.96, -29.6, 1.2), "Atria": (16.81, -69.0, 1.9), "β TrA": (15.92, -63.4, 2.8), "γ TrA": (15.32, -68.7, 2.9),
    "α Mus": (12.62, -69.1, 2.7), "β Mus": (12.77, -68.1, 3.0), "α Dor": (4.57, -55.0, 3.3), "α Ret": (4.24, -62.5, 3.4), "β Dor": (5.56, -62.5, 3.5),
    "α Lup": (14.70, -47.4, 2.3), "β Lup": (14.98, -43.1, 2.7), "β Ara": (17.42, -55.5, 2.8), "α Ara": (17.53, -49.9, 2.9), "Phact": (5.66, -34.1, 2.6),
    "α Pav": (20.43, -56.7, 1.9), "β Pav": (20.75, -66.2, 3.4), "α Ind": (20.63, -47.3, 3.1), "Deneb Kaitos": (0.73, -18.0, 2.0), "ζ Pup": (8.06, -40.0, 2.2),
    "ε Car": (8.38, -59.5, 1.9), "ι Car": (9.28, -59.3, 2.2), "α Cha": (8.31, -76.9, 4.1), "δ Oct": (14.45, -83.7, 4.3), "ν Oct": (21.69, -77.4, 3.7),
    "ε Ind": (22.05, -56.8, 4.7), "α Cae": (4.68, -41.9, 4.4), "β Cet": (0.73, -18.0, 2.0), "τ Cet": (1.73, -15.9, 3.5), "η Eri": (2.94, -8.9, 3.9),
    "θ Eri": (2.97, -40.3, 3.2), "φ Eri": (2.28, -51.5, 3.6), "χ Eri": (1.93, -51.6, 3.7), "ι Eri": (2.67, -39.9, 4.1), "κ Eri": (2.45, -47.7, 4.2), "υ Eri": (4.60, -30.6, 3.8),
    "ε Ret": (4.28, -59.3, 4.4), "γ Dor": (4.27, -51.5, 4.2), "ζ Dor": (5.09, -57.5, 4.7), "δ Dor": (5.75, -65.7, 4.3), "β Ret": (3.74, -64.8, 3.8),
    "γ Tuc": (23.29, -58.2, 4.0), "ζ Tuc": (0.33, -64.9, 4.2), "β Tuc": (0.53, -62.9, 4.4), "δ Pav": (20.15, -66.2, 3.6), "γ Pav": (21.44, -65.4, 4.2),
    "ε Pav": (20.01, -72.9, 4.0), "ζ Pav": (18.72, -71.4, 4.0), "λ Vel2": (9.13, -43.4, 2.2), "ν Pup": (6.63, -43.2, 3.2), "τ Pup": (6.83, -50.6, 2.9),
    "σ Pup": (7.49, -43.3, 3.3), "χ Car": (7.95, -53.0, 3.5), "ω Car": (10.23, -70.0, 3.3), "β Car2": (9.22, -69.7, 1.7), "N Vel": (9.52, -57.0, 3.1),
    "p Car": (10.53, -61.7, 3.3), "q Car": (10.29, -61.3, 3.4), "λ Cen": (11.60, -63.0, 3.1), "π Cen": (11.35, -54.5, 3.9), "σ Cen": (12.47, -50.2, 3.9),
    "ρ Cen": (12.19, -52.4, 3.9), "μ Cen": (13.83, -42.5, 3.0), "ν Cen": (13.82, -41.7, 3.4), "κ Cen": (14.99, -42.1, 3.1), "γ Lup": (15.59, -41.2, 2.8),
    "δ Lup": (15.36, -40.6, 3.2), "ε Lup": (15.38, -44.7, 3.4), "ζ Lup": (15.20, -52.1, 3.4), "η Lup": (16.00, -38.4, 3.4), "α Cir": (14.71, -65.0, 3.2),
    "δ Mus": (13.04, -71.5, 3.6), "γ Mus": (12.54, -72.1, 3.9), "λ Mus": (11.76, -66.7, 3.6), "ε Mus": (12.29, -67.9, 4.1), "η Car": (10.75, -59.7, 4.5),
    "θ Ara": (18.11, -50.1, 3.7), "ζ Ara": (16.98, -56.0, 3.1), "η Ara": (16.83, -59.0, 3.8), "δ Ara": (17.52, -60.7, 3.6), "γ Ara": (17.42, -56.4, 3.3),
    "ε TrA": (15.61, -66.3, 4.1), "δ TrA": (16.26, -63.7, 3.9), "Antares": (16.49, -26.4, 1.0), "Shaula": (17.56, -37.1, 1.6), "Sargas": (17.62, -43.0, 1.9),
    "κ Sco": (17.71, -39.0, 2.4), "ε Sco": (16.84, -34.3, 2.3), "μ Sco": (16.87, -38.0, 3.0), "ζ Sco": (16.91, -42.4, 3.6), "η Sco": (17.20, -43.2, 3.3),
    "ι Sco": (17.79, -40.1, 3.0), "λ Sco2": (17.56, -37.1, 1.6), "β Col": (5.85, -35.8, 3.1), "ε Col": (5.52, -35.5, 3.9), "η Col": (5.99, -42.8, 3.9),
    "α Pic": (6.80, -61.9, 3.3), "β Pic": (5.79, -51.1, 3.9), "γ Pic": (5.83, -56.2, 4.5), "α Vol": (9.04, -66.4, 4.0), "β Vol": (8.43, -66.1, 3.8), "γ Vol": (7.14, -70.5, 3.6),
    "δ Vol": (7.28, -67.9, 3.9), "ε Vol": (8.13, -68.6, 4.3), "α Aps": (14.80, -79.0, 3.8), "γ Aps": (16.56, -78.9, 3.9), "β Aps": (16.72, -77.5, 4.2),
    "α Men": (6.17, -74.7, 5.1), "γ Men": (5.53, -76.3, 5.2), "ν Hyi": (2.84, -75.1, 4.8), "δ Hyi": (2.36, -68.7, 4.1), "ε Hyi": (2.66, -68.3, 4.1),
    "λ Gru": (22.10, -39.5, 4.5), "δ1 Gru": (22.49, -43.5, 4.0), "ε Gru": (22.81, -51.3, 3.5), "ζ Gru": (23.02, -52.8, 4.1), "ι Gru": (23.17, -45.2, 3.9), "θ Gru": (23.11, -43.5, 4.3),
    "α PsA": (22.96, -29.6, 1.2), "ε PsA": (22.68, -27.0, 4.2), "δ PsA": (22.93, -32.5, 4.2), "β PsA": (22.53, -32.3, 4.3), "γ Scl": (23.31, -32.5, 4.4), "α Scl": (0.98, -29.4, 4.3),
    "γ Phe": (1.47, -43.3, 3.4), "δ Phe": (1.52, -49.1, 3.9), "ε Phe": (0.16, -45.7, 3.9), "ζ Phe": (1.14, -55.2, 3.9), "κ Phe": (0.44, -43.7, 3.9),
}
LINES = [("Acrux", "Gacrux"), ("Mimosa", "δ Cru"), ("Rigil Kent", "Hadar"), ("Hadar", "ε Cen"), ("ε Cen", "γ Cen"), ("γ Cen", "δ Cen"),
         ("ε Cen", "ζ Cen"), ("ζ Cen", "η Cen"), ("η Cen", "θ Cen"), ("θ Cen", "ι Cen"), ("ι Cen", "γ Cen"),
         ("Canopus", "Avior"), ("Avior", "Aspidiske"), ("Aspidiske", "θ Car"), ("θ Car", "υ Car"), ("υ Car", "Miaplacidus"), ("Miaplacidus", "Canopus"),
         ("γ Vel", "δ Vel"), ("δ Vel", "κ Vel"), ("κ Vel", "μ Vel"), ("μ Vel", "λ Vel"), ("λ Vel", "γ Vel"), ("Naos", "γ Vel"),
         ("Achernar", "α Hyi"), ("α Hyi", "β Hyi"), ("β Hyi", "γ Hyi"), ("γ Hyi", "α Hyi"), ("Achernar", "χ Eri"), ("χ Eri", "φ Eri"), ("φ Eri", "κ Eri"), ("κ Eri", "θ Eri"),
         ("Atria", "β TrA"), ("β TrA", "γ TrA"), ("γ TrA", "Atria"), ("Alnair", "β Gru"), ("β Gru", "ε Gru"), ("Alnair", "δ1 Gru"), ("δ1 Gru", "γ Gru"), ("β Gru", "ι Gru"),
         ("Ankaa", "β Phe"), ("β Phe", "γ Phe"), ("Ankaa", "κ Phe"), ("β Phe", "ζ Phe"), ("Peacock", "β Pav"), ("β Pav", "δ Pav"), ("δ Pav", "γ Pav"),
         ("α Mus", "β Mus"), ("α Mus", "δ Mus"), ("α Mus", "λ Mus"), ("Sirius", "Mirzam"), ("Sirius", "Wezen"), ("Wezen", "Adhara"),
         ("α Tuc", "γ Tuc"), ("γ Tuc", "ζ Tuc"), ("ζ Tuc", "β Tuc"), ("α Dor", "β Dor"), ("α Dor", "γ Dor"), ("α Ret", "β Ret"), ("Phact", "β Col"), ("β Col", "η Col"),
         ("α Pic", "β Pic"), ("α Vol", "β Vol"), ("β Vol", "γ Vol"), ("γ Vol", "δ Vol"), ("δ Vol", "ε Vol"), ("ε Vol", "α Vol")]
NAMED = ["Canopus", "Achernar", "Acrux", "Rigil Kent", "Hadar", "Fomalhaut", "Peacock", "Alnair", "Miaplacidus", "Atria", "Sirius"]
pos = {}
for name, (ra, dec, mag) in STARS.items():
    s = screen_xy(ra, dec)
    if s: pos[name] = s[0]
for a, b in LINES:
    if a in pos and b in pos:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        if max(y0, y1) < HORIZON - 2:
            L = math.hypot(x1 - x0, y1 - y0)
            if L < 140:
                # leave a gap around each star
                ux, uy = (x1 - x0) / L, (y1 - y0) / L
                dr.line([(x0 + ux * 5, y0 + uy * 5), (x1 - ux * 5, y1 - uy * 5)], fill=Wt, width=1)
for name, (ra, dec, mag) in STARS.items():
    if name not in pos: continue
    x, y = pos[name]
    if y >= HORIZON - 2: continue
    r = max(0.0, 3.6 - mag * 0.85)
    if r < 0.8:
        dr.point((x, y), fill=Wt); dr.point((x + 1, y), fill=Wt)
    else:
        dr.ellipse([x - r, y - r, x + r, y + r], fill=Wt)
        if mag < 1.0:   # the very brightest get a four-point spike
            dr.line([(x - r - 5, y), (x + r + 5, y)], fill=Wt, width=1)
            dr.line([(x, y - r - 5), (x, y + r + 5)], fill=Wt, width=1)
try:
    fn = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
    fi = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf", 10)
    ft = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", 11)
except OSError:
    fn = fi = ft = ImageFont.load_default()
for name in NAMED:
    if name in pos:
        x, y = pos[name]
        if y < HORIZON - 10: dr.text((x + 6, y - 3), name, fill=Wt, font=fn)
for (ra, dec, t, off) in [(5.39, -69.75, "Nubecula Major", (-30, 26)), (0.87, -72.8, "Nubecula Minor", (-52, 14)), (12.9, -63.0, "Saccus Carbonarius", (6, 8))]:
    s = screen_xy(ra, dec)
    if s: dr.text((s[0][0] + off[0], s[0][1] + off[1]), t, fill=Y, font=fi)
# the south celestial pole, marked as the chartmakers did, with a small yellow cross
s = screen_xy(0.0, -89.99)
if s:
    x, y = s[0]
    dr.line([(x - 4, y), (x + 4, y)], fill=Y, width=1); dr.line([(x, y - 4), (x, y + 4)], fill=Y, width=1)
    dr.text((x + 6, y + 2), "polus antarcticus", fill=Y, font=fi)

# ---------------- Tierra del Fuego: the shore, and the fires -----------------------------
def ridge(x, base, amp, seed):
    random.seed(seed)
    ph = [random.uniform(0, 6.3) for _ in range(5)]
    return base - amp * (0.5 + 0.5 * math.sin(x / 61 + ph[0])) - amp * 0.5 * (0.5 + 0.5 * math.sin(x / 23 + ph[1])) - amp * 0.2 * math.sin(x / 7 + ph[2])
# a far ridge in blue-screened silhouette (the last of the twilight behind it), then the near shore in black
far = [(x, ridge(x, HORIZON - 10, 28, 3)) for x in range(0, W + 1, 2)]
dr.polygon(far + [(W, HORIZON), (0, HORIZON)], fill=K)
for (x, y) in far[::2]:            # a thin blue rim where the last light catches the far ridge
    if x > 120: dr.point((x, y - 1), fill=B)
near = [(x, ridge(x, HORIZON + 26, 22, 11)) for x in range(0, W + 1, 2)]
dr.polygon(near + [(W, HORIZON + 44), (0, HORIZON + 44)], fill=K)
# a green fringe of beech forest along the near shore, screened so it stays dark
random.seed(5)
for (x, y) in near:
    for k in range(0, 14, 2):
        if random.random() < 0.45 - k * 0.03:
            dr.point((x + random.randint(0, 1), y + 6 + k), fill=G)
# water
WATER_Y = HORIZON + 44
dr.rectangle([0, WATER_Y, W, H], fill=K)
def fire(x, y, s):
    """a campfire: yellow core, red tongues, sparks, and its reflection in the water"""
    dr.polygon([(x - 3 * s, y), (x - 1 * s, y - 5 * s), (x, y - 2 * s), (x + 1.5 * s, y - 7 * s), (x + 3 * s, y)], fill=R)
    dr.polygon([(x - 1.5 * s, y), (x - 0.5 * s, y - 3 * s), (x + 0.5 * s, y - 1.5 * s), (x + 1.5 * s, y)], fill=Y)
    for _ in range(int(6 * s)):
        dr.point((x + random.gauss(0, 3 * s), y - 7 * s - abs(random.gauss(0, 4 * s))), fill=random.choice([R, Y]))
    for k in range(3):        # the lit ground and figures beside it
        dr.point((x + random.randint(-6, 6), y + random.randint(0, 2)), fill=R)
    # reflection: a wavering column of dashes down the water
    for k in range(0, 60, 3):
        yy = WATER_Y + 4 + k * 1.6
        if yy > H - 14: break
        if random.random() < 0.7 - k / 90:
            wob = int(2 * math.sin(k / 3 + x))
            dr.line([(x + wob - s, yy), (x + wob + s, yy)], fill=Y if k % 2 == 0 else R, width=1)
random.seed(1520)
for (fx, fy_off, fs) in [(48, 0, 1.0), (96, 4, 0.8), (150, -2, 1.2), (206, 3, 0.7), (238, 0, 1.0), (292, 2, 0.9), (330, -3, 1.3), (372, 1, 0.8)]:
    fy = ridge(fx, HORIZON + 26, 22, 11) + 5 + fy_off
    fire(fx, fy, fs)
# figures on the shore, watching the ships
for (fx, fs) in [(60, 1), (160, 1), (245, 1), (318, 1)]:
    fy = ridge(fx, HORIZON + 26, 22, 11) + 5
    dr.line([(fx, fy - 2), (fx, fy + 4)], fill=Y, width=1); dr.point((fx, fy - 3), fill=Y)
# the three ships at anchor, silhouettes with a single lantern each, and lantern reflections
hull = [(-62, -36), (-40, -36), (-40, -23), (20, -21), (20, -31), (52, -31), (61, -19), (58, 0), (-58, 0), (-65, -12)]
def nao(sx, sy, s):
    def T(x, y): return (sx + x * s, sy + y * s)
    dr.polygon([T(*p) for p in hull], fill=K, outline=Wt)
    for (mx, top) in [(28, -108), (-2, -142), (-42, -96)]:
        dr.line([T(mx, -22), T(mx, top)], fill=Wt, width=1)
    for (mx, yy, hw) in [(-2, -96, 40), (-2, -134, 22), (28, -80, 28), (28, -105, 14)]:
        dr.line([T(mx - hw, yy), T(mx + hw, yy)], fill=Wt, width=1)
    dr.line([T(48, -31), T(96, -60)], fill=Wt, width=1)
    for side in (-1, 1):
        for k in range(3):
            dr.line([T(-2, -100), T(-2 + side * (12 + k * 5), -22)], fill=Wt, width=1)
    lx, ly = T(-66, -40)
    dr.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=Y)
    for k in range(0, 40, 4):
        if random.random() < 0.75:
            dr.line([(lx - 1, sy + 6 + k), (lx + 1, sy + 6 + k)], fill=Y, width=1)
nao(300, 556, 0.42); nao(130, 542, 0.30); nao(215, 534, 0.22)
# caption
dr.text((200, 588), "N V B E C V L A E  ·  Tierra del Fuego  ·  MDXX", fill=Wt, font=ft, anchor="mm")
im.save(os.environ["OUT_RAW"])
