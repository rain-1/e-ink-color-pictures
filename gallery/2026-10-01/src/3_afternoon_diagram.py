# Afternoon — "Diagram, 1 October 1964". A Marey train graph (the Japanese dia, ダイヤ) of the
# opening day: twelve stations down the page at true distance, the clock across, every
# Hikari (red) and Kodama (black) as a diagonal. Hikari 1 is picked out in yellow. Down the
# left margin, 53 ticks for the old road's stations — a walker's diagram would need thirteen days.
# Departure pattern is after the opening timetable (Hikari on the hour, Kodama on the half
# hour, 4h and 5h end to end) — the shape is right, individual minutes are approximate.
import os, sys, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ukiyo import *
from PIL import Image, ImageDraw
im = Image.new("RGB", (W, H), Wh); d = ImageDraw.Draw(im); d.fontmode = "1"
ST = [("東京", "Tokyo", 0.0), ("新横浜", "Shin-Yokohama", 28.8), ("小田原", "Odawara", 83.9), ("熱海", "Atami", 104.6),
      ("静岡", "Shizuoka", 180.2), ("浜松", "Hamamatsu", 257.1), ("豊橋", "Toyohashi", 293.6), ("名古屋", "Nagoya", 366.0),
      ("岐阜羽島", "Hashima", 396.3), ("米原", "Maibara", 445.9), ("京都", "Kyoto", 513.6), ("新大阪", "Shin-Osaka", 552.6)]
X0, X1, Y0, Y1 = 66, 390, 86, 520
T0, T1 = 6.0, 24.5
fx = lambda t: X0 + (t - T0) / (T1 - T0) * (X1 - X0)
fy = lambda km: Y0 + km / 552.6 * (Y1 - Y0)

# --- title block
d.rectangle((0, 0, W, 50), fill=B)
d.text((12, 6), "東海道新幹線 列車運行図表", font=font(16, jp=True), fill=Wh)
d.text((12, 29), "TRAIN DIAGRAM · TŌKAIDŌ SHINKANSEN · OPENING DAY, 1 OCT 1964", font=font(9, serif=False, bold=True), fill=Y)
d.rectangle((0, 50, W, 54), fill=R)

# --- grid: minor every 10 min (blue dots), hour lines (blue), station rules (black)
for m in range(int(T0 * 60), int(T1 * 60) + 1, 10):
    x = fx(m / 60)
    if m % 60 == 0:
        d.line((x, Y0 - 4, x, Y1 + 4), fill=B)
        hh = (m // 60) % 24
        if hh % 2 == 0:
            d.text((x - 6, Y0 - 18), f"{hh:02d}", font=font(10, serif=False, bold=True), fill=K)
            d.text((x - 6, Y1 + 6), f"{hh:02d}", font=font(10, serif=False, bold=True), fill=K)
    else:
        for y in range(Y0, Y1 + 1, 4):
            d.point((x, y), fill=B)
for jp, en, km in ST:
    y = fy(km)
    d.line((X0, y, X1, y), fill=K)
    d.text((4, y - 6), en if len(en) < 11 else en.replace("Shin-", "S-"), font=font(9, serif=False), fill=K)
d.rectangle((X0, Y0, X1, Y1), outline=K)

# --- the trains
HIK = [6 + h for h in range(0, 15)]          # departures each hour 06:00–20:00
KOD = [6.5 + h for h in range(0, 14)]        # 06:30–19:30
def path(dep, kind, down=True):
    stops = [0, 7, 10, 11] if kind == "H" else list(range(12))
    total = 4.0 if kind == "H" else 5.0
    dwell = 1 / 60 if kind == "H" else 1.5 / 60
    run = total - dwell * (len(stops) - 2)
    t = dep; pts = []
    seq = stops if down else list(reversed(stops))
    for a, b in zip(seq, seq[1:]):
        ka, kb = ST[a][2], ST[b][2]
        pts.append((fx(t), fy(ka)))
        t += run * abs(kb - ka) / 552.6
        pts.append((fx(t), fy(kb)))
        t += dwell
    return pts
for dep in KOD:
    d.line(path(dep, "K", True), fill=K, width=1)
    d.line(path(dep + 0.25, "K", False), fill=K, width=1)
for dep in HIK:
    d.line(path(dep, "H", True), fill=R, width=2)
    d.line(path(dep, "H", False), fill=R, width=2)
# Hikari 1: yellow halo under a red line, with a flag
p1 = path(6.0, "H", True)
d.line(p1, fill=Y, width=6); d.line(p1, fill=R, width=2)
d.rectangle((fx(6.0) + 6, Y0 + 4, fx(6.0) + 68, Y0 + 18), fill=Y, outline=K)
d.text((fx(6.0) + 9, Y0 + 5), "ひかり1号", font=font(11, jp=True), fill=K)
# meets: where a down and up Hikari cross, a small open circle — count them
downs = [path(h, "H", True) for h in HIK]; ups = [path(h, "H", False) for h in HIK]
def seg_x(p, q):
    (x1, y1), (x2, y2) = p; (x3, y3), (x4, y4) = q
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0: return None
    ta = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    ub = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
    if 0 <= ta <= 1 and 0 <= ub <= 1: return (x1 + ta * (x2 - x1), y1 + ta * (y2 - y1))
meets = 0; seen = set()
for a in downs:
    for b in ups:
        for i in range(len(a) - 1):
            for j in range(len(b) - 1):
                c = seg_x((a[i], a[i + 1]), (b[j], b[j + 1]))
                if c and (round(c[0]), round(c[1])) not in seen:
                    seen.add((round(c[0]), round(c[1]))); meets += 1
                    d.ellipse((c[0] - 2, c[1] - 2, c[0] + 2, c[1] + 2), fill=Wh, outline=K)
d.rectangle((X1 + 1, 0, W, H), fill=Wh)  # trim overspill past the frame
d.line((X1, Y0, X1, Y1), fill=K)

# --- the old road: 53 ticks down a yellow strip on the left margin
d.rectangle((58, Y0, 62, Y1), fill=Y)
for i in range(55):
    y = Y0 + i / 54 * (Y1 - Y0)
    d.line((56 if i % 5 else 53, y, 58, y), fill=K)

# --- legend and the comparison bar
LY = 540
d.line((10, LY, 34, LY), fill=R, width=2); d.text((38, LY - 6), "ひかり", font=font(10, jp=True), fill=K)
d.text((74, LY - 6), "HIKARI", font=font(9, serif=False, bold=True), fill=K)
d.line((130, LY, 154, LY), fill=K); d.text((158, LY - 6), "こだま", font=font(10, jp=True), fill=K)
d.text((194, LY - 6), "KODAMA", font=font(9, serif=False, bold=True), fill=K)
d.ellipse((260, LY - 2, 264, LY + 2), outline=K); d.text((268, LY - 6), f"{meets} Hikari meets", font=font(9, serif=False), fill=K)
d.rectangle((0, 556, W, H), fill=K)
bars = [("on foot  13 days", 13 * 24, Y), ("steam  20 h (1889)", 20.1, Wh), ("Kodama  5 h", 5, B), ("Hikari  4 h", 4, R)]
mx = 13 * 24
for i, (lab, hrs, c) in enumerate(bars):
    y = 559 + i * 10
    L = max(3, 250 * math.log1p(hrs) / math.log1p(mx))
    d.text((8, y - 2), lab, font=font(9, serif=False, bold=True), fill=c if c != B else Wh)
    d.rectangle((135, y + 1, 135 + L, y + 6), fill=c)
d.text((300, 589), "TOKYO→OSAKA, log", font=font(8, serif=False), fill=Wh)
im.save(os.environ.get("OUT_RAW", "/tmp/3.png"))
