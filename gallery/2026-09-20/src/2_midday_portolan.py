# Midday — "Carta de marear". A portolan chart of the Atlantic with the armada's route.
# Portolan conventions kept: rhumb lines in the traditional three inks (black for the
# eight winds, green for the half-winds, red for the quarter-winds), names written on the
# land side perpendicular to the coast, red for the chief ports, a wind rose with a
# fleur-de-lis, a trunk of leagues. Land yellow, sea the white of the vellum. Emits SVG.
import os, math
W, H = 400, 600
K, Wh, R, Y, B, G = "#000000", "#FFFFFF", "#E01B24", "#F5D400", "#123DB0", "#1E9B3C"
MX0, MY0, MW, MH = 20, 30, 360, 540
LON0, LAT0, S = -72.0, 48.0, 360 / 70.0
def P(lon, lat): return (MX0 + (lon - LON0) * S, MY0 + (LAT0 - lat) * S)
def pts(coords): return " ".join(f"{P(a, b)[0]:.1f},{P(a, b)[1]:.1f}" for a, b in coords)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
     f'<defs><clipPath id="m"><rect x="{MX0}" y="{MY0}" width="{MW}" height="{MH}"/></clipPath></defs>',
     f'<rect width="{W}" height="{H}" fill="{Wh}"/>', '<g clip-path="url(#m)">']
add = o.append

# ---------------- coastlines (approximate, from memory; good enough at four inches) ----
IBERIA = [(-2, 43.4), (-3.8, 43.4), (-5.8, 43.6), (-7.6, 43.7), (-8.3, 43.4), (-9.3, 43.0), (-8.9, 42.2),
          (-8.9, 41.2), (-8.8, 40.2), (-9.4, 39.0), (-9.5, 38.7), (-8.9, 38.4), (-8.8, 37.5), (-9.0, 37.0),
          (-8.0, 37.1), (-7.4, 37.2), (-6.9, 37.2), (-6.4, 36.8), (-6.2, 36.5), (-6.0, 36.2), (-5.6, 36.0),
          (-5.3, 36.2), (-4.4, 36.7), (-3.5, 36.7), (-2, 36.8)]
FRANCE = [(-2, 43.4), (-1.5, 43.5), (-1.3, 44.6), (-1.2, 46.0), (-2.0, 46.9), (-2.4, 47.3), (-3.6, 47.7),
          (-4.6, 48.0), (-4.7, 48.4), (-2, 48.4)]
AFRICA = [(-2, 35.1), (-3.0, 35.3), (-4.4, 35.2), (-5.3, 35.9), (-5.9, 35.8), (-6.4, 34.6), (-6.8, 34.0),
          (-7.6, 33.6), (-8.5, 33.2), (-9.2, 32.4), (-9.8, 31.4), (-9.6, 30.4), (-10.2, 29.4), (-11.0, 28.6),
          (-12.4, 28.0), (-13.1, 27.6), (-13.5, 26.2), (-14.5, 24.6), (-15.4, 23.6), (-16.1, 22.8), (-17.0, 21.0),
          (-16.6, 20.2), (-16.4, 19.2), (-16.2, 17.8), (-16.5, 16.2), (-16.8, 15.2), (-17.5, 14.7), (-17.0, 14.2),
          (-16.8, 13.4), (-16.7, 12.4), (-16.2, 11.9), (-15.4, 11.4), (-14.8, 10.8), (-13.9, 10.0), (-13.4, 9.0),
          (-13.2, 8.4), (-12.6, 7.5), (-11.6, 6.9), (-10.6, 6.2), (-9.5, 5.4), (-8.4, 4.6), (-7.5, 4.4),
          (-6.0, 4.9), (-4.5, 5.2), (-3.0, 5.1), (-2, 4.8)]
SAMERICA = [(-72, 11.8), (-70.4, 11.9), (-69.5, 11.3), (-68.2, 10.6), (-66.0, 10.6), (-64.0, 10.5),
            (-62.5, 10.5), (-61.5, 9.5), (-60.5, 8.5), (-59.0, 7.8), (-57.5, 6.2), (-55.5, 5.9), (-53.5, 5.6),
            (-52.0, 4.9), (-51.2, 4.0), (-50.2, 2.0), (-50.0, 0.4), (-49.0, -0.5), (-48.3, -1.2), (-46.5, -1.0),
            (-44.5, -2.3), (-42.5, -2.8), (-41.0, -2.9), (-39.5, -3.2), (-38.4, -3.8), (-37.2, -4.9),
            (-35.6, -5.2), (-35.0, -6.2), (-34.9, -8.3), (-35.6, -9.8), (-36.6, -10.6), (-37.6, -12.0),
            (-38.5, -13.0), (-38.9, -14.8), (-39.1, -16.5), (-39.4, -18.0), (-39.7, -19.6), (-40.6, -20.8),
            (-41.5, -22.0), (-42.5, -22.9), (-43.3, -23.0), (-44.6, -23.3), (-46.3, -24.0), (-47.7, -25.2),
            (-48.6, -27.0), (-49.2, -28.8), (-50.2, -30.4), (-51.6, -32.0), (-53.3, -33.6), (-54.9, -34.8),
            (-56.2, -34.9), (-57.5, -34.5), (-58.4, -34.6), (-57.6, -36.3), (-56.7, -37.0), (-57.5, -38.2),
            (-59.5, -38.8), (-62.2, -39.0), (-62.4, -40.6), (-64.2, -40.8), (-65.0, -41.9), (-64.3, -42.5),
            (-65.2, -43.6), (-65.3, -45.0), (-67.4, -46.0), (-67.6, -47.6), (-66.2, -47.9), (-67.7, -49.3),
            (-68.6, -50.2), (-69.1, -51.4), (-68.4, -52.4), (-68.0, -53.2), (-66.5, -54.4), (-65.2, -54.9),
            (-66.6, -55.2), (-67.3, -55.9), (-69.0, -55.4), (-70.6, -54.9), (-72, -54.3)]
ISLANDS = [  # centre lon, lat, radius px, name
    (-16.6, 28.3, 3.2, ""), (-15.6, 28.0, 2.6, ""), (-13.7, 29.0, 2.0, ""), (-14.0, 28.4, 2.2, ""), (-17.9, 28.7, 1.8, ""),
    (-17.0, 32.7, 2.2, ""), (-25.6, 37.8, 1.6, ""), (-27.2, 38.5, 1.4, ""), (-28.4, 38.6, 1.6, ""), (-31.1, 39.4, 1.3, ""),
    (-25.0, 17.1, 2.0, ""), (-23.5, 15.1, 2.4, ""), (-24.6, 14.9, 1.6, ""), (-23.0, 16.7, 1.7, ""), (-22.9, 16.1, 1.4, ""),
    (-32.4, -3.85, 1.8, ""), (-14.4, -7.9, 1.6, ""), (-5.7, -15.9, 1.6, ""), (-12.3, -37.1, 1.8, ""),
    (-59.5, -51.7, 4.0, ""), (-58.2, -51.9, 3.2, ""), (-61.2, 10.4, 3.0, ""), (-66.4, 18.2, 4.0, ""),
    (-61.5, 13.0, 1.6, ""), (-61.6, 15.3, 1.8, ""), (-61.2, 16.2, 1.6, ""), (-60.9, 14.0, 1.6, ""),
]
def land(coords):
    add(f'<polyline points="{pts(coords)}" fill="none" stroke="{B}" stroke-width="5.5" stroke-linejoin="round"/>')
    add(f'<polygon points="{pts(coords)}" fill="{Y}"/>')
    add(f'<polyline points="{pts(coords)}" fill="none" stroke="{K}" stroke-width="1.5" stroke-linejoin="round"/>')

# ---------------- rhumb-line network (drawn under the land) ----------------------------
CX, CY, RR = 200, 322, 236
def rhumb(cx, cy, n_dirs, L, w_scale=1.0):
    for j in range(n_dirs):
        a = 2 * math.pi * j / n_dirs
        col, w = (K, 1.0) if j % (n_dirs // 8) == 0 else ((G, 0.85) if j % (n_dirs // 16) == 0 else (R, 0.85))
        x2, y2 = cx + L * math.cos(a), cy + L * math.sin(a)
        add(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w * w_scale:.2f}"/>')
rhumb(CX, CY, 32, 900)
nodes = [(CX + RR * math.cos(2 * math.pi * k / 16), CY + RR * math.sin(2 * math.pi * k / 16)) for k in range(16)]
for (nx, ny) in nodes:
    rhumb(nx, ny, 16, 900, 0.9)
# equator and tropics, as the Cantino planisphere draws them
for lat, col, dash, name in [(0, G, "", "LINEA EQUINOCTIALIS"), (23.44, R, "5,3", "TROPICVS CANCRI"), (-23.44, R, "5,3", "TROPICVS CAPRICORNI")]:
    yy = P(0, lat)[1]
    add(f'<line x1="{MX0}" y1="{yy:.1f}" x2="{MX0 + MW}" y2="{yy:.1f}" stroke="{col}" stroke-width="1.8" stroke-dasharray="{dash}"/>')
    add(f'<text x="{MX0 + MW - 6}" y="{yy - 3:.1f}" font-family="Liberation Serif" font-size="7.5" fill="{col}" text-anchor="end" letter-spacing="1.5">{name}</text>')

# ---------------- land ----------------------------------------------------------------
for c in (FRANCE, IBERIA, AFRICA, SAMERICA):
    land(c)
for (lo, la, r, _) in ISLANDS:
    x, y = P(lo, la)
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 1.6:.1f}" fill="{B}"/>')
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{Y}" stroke="{K}" stroke-width="1"/>')
# the Strait, cut through Patagonia
add(f'<polyline points="{pts([(-68.4, -52.4), (-69.6, -52.7), (-70.4, -53.4), (-71.0, -53.9), (-72, -53.3)])}" fill="none" stroke="{B}" stroke-width="3" stroke-linecap="round"/>')
# rivers
for riv in [[(-50.0, 0.4), (-52, -1.5), (-55, -2.5), (-58, -3.2), (-62, -3.8), (-66, -3.5), (-70, -4.2)],
            [(-57.5, -34.5), (-58.4, -33.5), (-58.9, -31.5), (-59.7, -29.0), (-58.2, -26.5)],
            [(-16.5, 16.1), (-15.0, 16.5), (-13.0, 15.6), (-11.5, 14.4)],
            [(-6.4, 36.8), (-6.2, 37.2), (-6.0, 37.6), (-5.6, 38.0)]]:
    add(f'<polyline points="{pts(riv)}" fill="none" stroke="{B}" stroke-width="2" stroke-linecap="round"/>')
# mountains and trees inland: Atlas, the Brazilian coast range, the Andes' edge
def mountain(x, y, w):
    add(f'<path d="M{x - w},{y} L{x - w * 0.4},{y - w * 0.9} L{x},{y - w * 0.5} L{x + w * 0.4},{y - w * 1.1} L{x + w},{y} Z" fill="{Wh}" stroke="{K}" stroke-width="1"/>')
    add(f'<path d="M{x + w * 0.4},{y - w * 1.1} L{x + w * 0.65},{y - w * 0.4} L{x + w},{y}" fill="{K}"/>')
for lo, la in [(-6, 31.5), (-4.5, 32.5), (-3, 33.2), (-8, 30.5)]:
    x, y = P(lo, la); mountain(x, y, 9)
for lo, la in [(-45, -21.5), (-43, -20), (-41, -18.5), (-44.5, -23.5), (-48, -25.5)]:
    x, y = P(lo, la); mountain(x, y, 7)
for k in range(10):
    x, y = P(-71.2 + (k % 2) * 0.6, 8 - k * 5.8); mountain(x, y, 7)
def tree(x, y):
    add(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 7:.1f}" stroke="{K}" stroke-width="1.2"/>')
    add(f'<circle cx="{x:.1f}" cy="{y - 8:.1f}" r="3.2" fill="{G}" stroke="{K}" stroke-width="0.8"/>')
for lo, la in [(-56, -8), (-60, -5), (-63, -9), (-53, -11), (-57, -14), (-50, -7), (-64, 2), (-60, 0.5),
               (-10, 9), (-12, 11), (-8, 7), (-14, 13), (-6, 33.5), (-60, -30), (-62, -34)]:
    tree(*P(lo, la))
# a few tents and a king in the Sahara, and a lion, the way the Catalan Atlas does it
for lo, la in [(-8, 24), (-11, 22), (-5, 20)]:
    x, y = P(lo, la)
    add(f'<path d="M{x - 6},{y} L{x},{y - 9} L{x + 6},{y} Z" fill="{Wh}" stroke="{K}" stroke-width="1"/>')
    add(f'<line x1="{x}" y1="{y - 9}" x2="{x}" y2="{y - 13}" stroke="{K}" stroke-width="1"/>')
    add(f'<polygon points="{x},{y - 13} {x + 5},{y - 12} {x},{y - 10.5}" fill="{R}"/>')

# ---------------- place names: (lon, lat, text, angle, anchor, important) -------------
NAMES = [
    (-9.2, 38.9, "lisboa", 0, "start", 1), (-8.7, 37.1, "c. s. vicente", 0, "start", 0), (-6.2, 36.9, "SANLVCAR", 0, "start", 1),
    (-5.8, 36.3, "cadiz", 0, "start", 0), (-5.6, 37.5, "sevilla", 0, "start", 0), (-8.7, 41.3, "porto", 0, "start", 0),
    (-5.6, 35.5, "tanger", 0, "start", 0), (-6.6, 34.0, "sale", 0, "start", 0), (-9.0, 32.3, "safi", 0, "start", 0),
    (-9.6, 31.4, "mogador", 0, "start", 0), (-13.0, 27.5, "c. bojador", 0, "start", 0), (-14.3, 24.5, "rio do ouro", 0, "start", 0),
    (-16.6, 21.0, "c. blanco", 0, "start", 0), (-16.2, 19.6, "arguim", 0, "start", 0), (-16.0, 17.9, "senegal", 0, "start", 0),
    (-17.2, 14.6, "c. verde", 0, "start", 0), (-16.4, 12.9, "gambia", 0, "start", 0), (-13.0, 8.5, "SERRA LEOA", 0, "start", 1),
    (-7.3, 4.6, "c. das palmas", 0, "start", 0), (-4.2, 5.4, "mina", 0, "start", 0), (-11.0, 6.6, "malagueta", 0, "start", 0),
    (-16.4, 29.4, "canarias", 0, "middle", 1), (-16.8, 33.4, "madeira", 0, "middle", 0), (-28.0, 39.6, "açores", 0, "middle", 0),
    (-24.0, 18.0, "c. verde ins.", 0, "middle", 0), (-32.4, -2.9, "s. joam", 0, "middle", 0),
    (-34.7, -8.3, "c. s. agostinho", 0, "end", 0), (-38.7, -13.0, "b. todos santos", 0, "end", 0), (-39.5, -16.5, "porto seguro", 0, "end", 0),
    (-43.5, -23.1, "RIO DE JANEIRO", 0, "end", 1), (-47.9, -25.3, "cananea", 0, "end", 0), (-50.5, -30.4, "rio dos patos", 0, "end", 0),
    (-58.6, -35.2, "RIO DE LA PLATA", 0, "end", 1), (-62.5, -39.2, "bahia blanca", 0, "end", 0), (-64.5, -42.3, "golfo s. mathias", 0, "end", 0),
    (-67.8, -49.2, "S. IVLIAN", 0, "end", 1), (-68.7, -50.2, "s. cruz", 0, "end", 0), (-68.5, -52.2, "c. virgenes", 0, "end", 0),
    (-69.5, -54.8, "TIERRA DEL FVEGO", 0, "middle", 1), (-36.0, -5.5, "c. s. roque", 0, "end", 0),
    (-42.0, -3.8, "maranham", -90, "middle", 0), (-49.5, -1.8, "marañon", -90, "middle", 0), (-52.5, 3.4, "guayana", -90, "middle", 0),
    (-64.0, 9.2, "paria", -90, "middle", 0), (-61.2, 9.4, "trinidad", 0, "start", 0),
    (-59.0, -52.7, "ins. de sanson", 0, "middle", 0), (-12.3, -38.2, "tristan", 0, "middle", 0), (-5.7, -17.0, "s. helena", 0, "middle", 0),
    (-3.4, 45.6, "galia", 0, "start", 0), (-5.2, 40.0, "HISPANIA", 0, "middle", 1), (-8.0, 17.5, "LIBIA", 0, "middle", 1),
    (-55.0, -18.0, "BRASIL", 0, "middle", 1), (-66.0, -44.0, "patagones", -90, "middle", 0), (-24.0, -55.0, "MARE INCOGNITVM", 0, "middle", 0),
]
for (lo, la, t, ang, anc, imp) in NAMES:
    x, y = P(lo, la)
    fs = 9.5 if imp else 7.2
    col = R if imp else K
    add(f'<text transform="translate({x:.1f},{y:.1f}) rotate({ang})" font-family="FreeSerif" font-style="italic" font-size="{fs}" fill="{col}" text-anchor="{anc}" letter-spacing="{0.8 if imp else 0}">{t}</text>')
# sea names, spaced capitals
for (lo, la, t, fs) in [(-40, 34, "MAR OCEANO", 15), (-25, -14, "OCEANO", 13), (-25, -18, "ETHIOPICO", 13), (-30, 8, "MAR DE LAS YEGVAS", 9)]:
    x, y = P(lo, la)
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Liberation Serif" font-size="{fs}" fill="{K}" text-anchor="middle" letter-spacing="{fs * 0.45:.1f}">{t}</text>')

# ---------------- wind roses ----------------------------------------------------------
def rose(cx, cy, r, full=True):
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 1.08:.1f}" fill="{Wh}" stroke="{K}" stroke-width="1"/>')
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.98:.1f}" fill="none" stroke="{K}" stroke-width="0.6"/>')
    n = 32 if full else 16
    layers = [(2, r * 0.62, R), (1, r * 0.8, G), (0, r, K)] if full else [(1, r * 0.7, G), (0, r, K)]
    for (lvl, rl, col) in layers:
        for j in range(n):
            step = n // 8
            if lvl == 0 and j % step: continue
            if lvl == 1 and (j % (step // 2) or j % step == 0): continue
            if lvl == 2 and j % 2 == 0: continue
            a = 2 * math.pi * j / n - math.pi / 2
            tip = (cx + rl * math.cos(a), cy + rl * math.sin(a))
            wdt = rl * 0.14
            l = (cx + wdt * math.cos(a - math.pi / 2), cy + wdt * math.sin(a - math.pi / 2))
            rt = (cx + wdt * math.cos(a + math.pi / 2), cy + wdt * math.sin(a + math.pi / 2))
            add(f'<polygon points="{cx:.1f},{cy:.1f} {l[0]:.1f},{l[1]:.1f} {tip[0]:.1f},{tip[1]:.1f}" fill="{col}" stroke="{K}" stroke-width="0.6"/>')
            add(f'<polygon points="{cx:.1f},{cy:.1f} {rt[0]:.1f},{rt[1]:.1f} {tip[0]:.1f},{tip[1]:.1f}" fill="{Wh}" stroke="{K}" stroke-width="0.6"/>')
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.16:.1f}" fill="{Y}" stroke="{K}" stroke-width="1"/>')
    # fleur-de-lis for north
    fy = cy - r * 1.02
    add(f'<path d="M{cx:.1f},{fy - 8} Q{cx - 5:.1f},{fy - 2} {cx:.1f},{fy + 4} Q{cx + 5:.1f},{fy - 2} {cx:.1f},{fy - 8} Z '
        f'M{cx - 7:.1f},{fy - 3} Q{cx - 3:.1f},{fy + 1} {cx:.1f},{fy + 4} Q{cx - 8:.1f},{fy + 5} {cx - 7:.1f},{fy - 3} Z '
        f'M{cx + 7:.1f},{fy - 3} Q{cx + 3:.1f},{fy + 1} {cx:.1f},{fy + 4} Q{cx + 8:.1f},{fy + 5} {cx + 7:.1f},{fy - 3} Z" fill="{K}"/>')
    # a cross for east (Jerusalem)
    add(f'<path d="M{cx + r * 1.02 + 2:.1f},{cy - 5:.1f} v10 M{cx + r * 1.02 - 2:.1f},{cy - 2:.1f} h8" stroke="{R}" stroke-width="2"/>')
rose(104, 152, 36, True)                   # north-west Atlantic, off the network
rose(*nodes[2], 24, False)                 # south-east node
for k in (4, 6, 12, 14):                   # small studs at the other open-sea nodes
    nx, ny = nodes[k]
    add(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="5" fill="{Y}" stroke="{K}" stroke-width="1"/>')
    add(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="1.6" fill="{K}"/>')

# ---------------- the route, and the fleet shrinking along it --------------------------
ROUTE = [(-6.4, 36.6), (-8.5, 34.0), (-14.0, 30.0), (-16.6, 27.6), (-17.5, 22.0), (-17.8, 15.5), (-15.5, 10.0),
         (-14.0, 7.0), (-18.0, 2.0), (-24.0, -2.0), (-30.0, -5.5), (-34.5, -8.6), (-36.5, -13.0), (-38.5, -18.0),
         (-41.5, -22.5), (-43.3, -23.4), (-47.0, -26.0), (-51.0, -31.0), (-55.0, -34.5), (-58.0, -35.6), (-59.0, -38.5),
         (-62.0, -39.8), (-64.6, -42.0), (-65.8, -45.0), (-67.0, -47.5), (-67.4, -49.3), (-68.2, -50.3), (-68.5, -51.8),
         (-68.2, -52.5), (-70.2, -53.3), (-72, -53.3)]
add(f'<polyline points="{pts(ROUTE)}" fill="none" stroke="{K}" stroke-width="2" stroke-dasharray="5,3"/>')
def shipglyph(x, y, s=1.0):
    add(f'<g transform="translate({x:.1f},{y:.1f}) scale({s})">'
        f'<path d="M-7,0 L7,0 L5,4 L-6,4 Z" fill="{K}"/><line x1="0" y1="0" x2="0" y2="-11" stroke="{K}" stroke-width="1.3"/>'
        f'<path d="M-5,-10 L5,-10 Q7,-6 5,-2 L-5,-2 Q-7,-6 -5,-10 Z" fill="{Wh}" stroke="{K}" stroke-width="0.9"/>'
        f'<polygon points="0,-11 -4,-10 0,-8.5" fill="{R}"/></g>')
def fleet(lo, la, n, spread=8):
    x, y = P(lo, la)
    for i in range(n):
        shipglyph(x + (i - (n - 1) / 2) * spread, y + (i % 2) * 5)
fleet(-20.5, 27.0, 5); fleet(-29.0, -9.5, 5); fleet(-64.0, -49.6, 4); fleet(-63.0, -53.0, 3, 9)
# the wreck of the Santiago at the Santa Cruz river
x, y = P(-68.9, -50.4)
add(f'<path d="M{x - 5},{y} L{x + 4},{y - 4} M{x - 4},{y - 5} L{x + 5},{y + 1}" stroke="{R}" stroke-width="1.8"/>')
# a spouting whale in the South Atlantic
x, y = P(-19.0, -30.0)
add(f'<path d="M{x - 22},{y + 4} Q{x - 10},{y - 12} {x + 8},{y - 6} Q{x + 18},{y - 2} {x + 22},{y - 12} L{x + 26},{y - 4} '
    f'L{x + 30},{y - 10} Q{x + 22},{y + 6} {x + 8},{y + 6} Q{x - 8},{y + 8} {x - 22},{y + 4} Z" fill="{K}"/>')
add(f'<circle cx="{x - 12}" cy="{y - 2}" r="1.6" fill="{Wh}"/>')
add(f'<path d="M{x - 8},{y - 9} q-2,-8 2,-14 M{x - 8},{y - 9} q3,-8 7,-12 M{x - 8},{y - 9} q-6,-6 -8,-11" fill="none" stroke="{B}" stroke-width="1.3"/>')
for k in range(3):
    add(f'<path d="M{x - 30 + k * 26},{y + 12} q6,-4 12,0 q6,4 12,0" fill="none" stroke="{B}" stroke-width="1"/>')
add('</g>')

# ---------------- cartouche and trunk of leagues, bottom right, over open sea ---------
cx0, cy0, cw, ch = 214, 466, 164, 100
add(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" fill="{Wh}" stroke="{K}" stroke-width="2"/>')
add(f'<rect x="{cx0 + 4}" y="{cy0 + 4}" width="{cw - 8}" height="{ch - 8}" fill="none" stroke="{K}" stroke-width="0.8"/>')
for k in range(4):
    for (px, py) in [(cx0 + 2, cy0 + 2), (cx0 + cw - 2, cy0 + 2), (cx0 + 2, cy0 + ch - 2), (cx0 + cw - 2, cy0 + ch - 2)]:
        add(f'<circle cx="{px}" cy="{py}" r="{5 - k}" fill="{[R, Y, K, Wh][k]}"/>')
tx = cx0 + cw / 2
add(f'<text x="{tx}" y="{cy0 + 22}" font-family="Liberation Serif" font-size="12" fill="{K}" text-anchor="middle" letter-spacing="3">CARTA DE MAREAR</text>')
add(f'<text x="{tx}" y="{cy0 + 37}" font-family="FreeSerif" font-style="italic" font-size="9.5" fill="{R}" text-anchor="middle">de la Armada de Molucca</text>')
add(f'<text x="{tx}" y="{cy0 + 50}" font-family="FreeSerif" font-style="italic" font-size="8" fill="{K}" text-anchor="middle">Sanlúcar · xx de septiembre · MDXIX</text>')
add(f'<text x="{tx}" y="{cy0 + 61}" font-family="FreeSerif" font-style="italic" font-size="8" fill="{K}" text-anchor="middle">cinco naos · 270 hombres · rumbo al poniente</text>')
# trunk of leagues
bx, by, bw = cx0 + 14, cy0 + 76, cw - 28
add(f'<text x="{tx}" y="{by - 4}" font-family="Liberation Serif" font-size="7" fill="{K}" text-anchor="middle" letter-spacing="1.5">TRONCO DE LEGVAS</text>')
add(f'<rect x="{bx}" y="{by}" width="{bw}" height="6" fill="{Wh}" stroke="{K}" stroke-width="1"/>')
for k in range(0, 10):
    if k % 2 == 0:
        add(f'<rect x="{bx + k * bw / 10:.1f}" y="{by}" width="{bw / 10:.1f}" height="6" fill="{K}"/>')
for k in range(0, 11):
    add(f'<line x1="{bx + k * bw / 10:.1f}" y1="{by - 3}" x2="{bx + k * bw / 10:.1f}" y2="{by + 9}" stroke="{K}" stroke-width="1"/>')
    for m in range(1, 5):
        add(f'<line x1="{bx + (k + m / 5) * bw / 10:.1f}" y1="{by + 6}" x2="{bx + (k + m / 5) * bw / 10:.1f}" y2="{by + 8}" stroke="{K}" stroke-width="0.6"/>') if k < 10 else None
# the vellum's edge: a double border with a red fillet, and a neck at the top like a real skin
add(f'<rect x="{MX0}" y="{MY0}" width="{MW}" height="{MH}" fill="none" stroke="{K}" stroke-width="2.5"/>')
add(f'<rect x="{MX0 - 5}" y="{MY0 - 5}" width="{MW + 10}" height="{MH + 10}" fill="none" stroke="{R}" stroke-width="1.5"/>')
add(f'<rect x="{MX0 - 9}" y="{MY0 - 9}" width="{MW + 18}" height="{MH + 18}" fill="none" stroke="{K}" stroke-width="1"/>')
# latitude scale down the left margin, every 10 degrees
for la in range(-50, 50, 10):
    x, y = P(-72, la)
    add(f'<line x1="{MX0 - 9}" y1="{y:.1f}" x2="{MX0}" y2="{y:.1f}" stroke="{K}" stroke-width="1"/>')
    add(f'<text transform="translate({MX0 - 11},{y + 2:.1f}) rotate(-90)" font-family="Liberation Serif" font-size="6.5" fill="{K}" text-anchor="middle">{abs(la)}</text>')
add(f'<text x="200" y="{H - 8}" font-family="FreeSerif" font-style="italic" font-size="8.5" fill="{K}" text-anchor="middle">cum privilegio · la sola nao Victoria tornó, tres años después</text>')
add('</svg>')

import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgtools import finish
finish("\n".join(o), W, H)
