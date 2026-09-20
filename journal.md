# journal.md

Append-only. One short entry per day: what I made, why, what I noticed.
Never edit old entries.

---

## 2026-09-13 (Sunday) — first run, before the device arrived
Seed was Robert Indiana's birthday → "hard edges" as the day's thread. Made: hanga waves
(morning), pop "13" sign (midday), numpy raytrace of spheres (afternoon), linocut geese
(evening), Rule 30 automaton (night). Review caught three things: a raytraced sky dithers
into speckle unless it's pure white; small silhouettes vanish — geese needed doubling;
cellular automata need ≥10px cells or they read as static. The raytracer was fun and
cheap — worth returning to with a different subject. Nothing seen on real hardware yet;
expect the white to be greyer and the green more olive than the preview.

## 2026-09-14 (Monday) — restricted palettes
Owner asked for two things: restricted palettes per piece, and more detail and attention.
Seed: Dante's death, this day 1321; every canticle ends on "stelle", so one star per piece.
Made: woodcut dark wood (K/G/W), terraced Purgatory (Y/K/W), raymarched Inferno funnel
(K/R only), engraved Ptolemaic spheres (B/Y/W), star chart of tonight's sky (K/W only).
Added `--palette` to render.py/palette.py. Learned: the generic ordered dither is useless
for two-colour work — do the Bayer screen inside the generator on a tone value. The
raymarch took two camera tries; get the camera right before touching lighting. Restricted
palettes made every piece stronger. Two or three colours may be the default, not the
experiment. Worry: 9px ring labels and 0.6px lines in the Spheres plate may not survive
the real panel — check when hardware arrives.

## 2026-09-20 (Sunday) — Armada de Molucca, and the correction
Owner said I'd gone "a few levels too minimal": the restricted palette was meant as an
occasional thing, not a rule, and the detail had thinned with it. Fair. Seed: Magellan's
five ships left Sanlúcar on this day in 1519; five ships, five slots. Made: an engraved
harbour at dawn (five carracks with full rigging, a town, hatched sky and water), a
portolan chart of the Atlantic with rhumb lines in the three traditional inks and ~60
place names, a raymarched fjord printed as a per-material two-ink screenprint, a blueprint
of the nao Victoria with sheer/body/half-breadth plans and dimension lines, and a computed
southern sky (≈200 stars, Milky Way sampled from galactic coordinates, both Clouds) over
the fires of Tierra del Fuego. Learned two real things. (1) Nearest-colour quantisation
sends antialiased grey to *green* — mid-grey is closest to the green ink. Added
`src/svgtools.py`: box-downsample from 2×, then snap low-chroma pixels to black/white by
luminance. Thin yellow-on-blue lines drift to green the same way; keep them ≥1.6px.
(2) Floyd–Steinberg on a continuous-tone 3D render is a speckle machine; screening each
material between two inks with Bayer (rock K/W, forest K/G, snow B/W, water K/B/W) gives
a clean screenprint and is the right way to do 3D on this panel. The fjord took three
renders (camera, then materials, then fog); ~75 s each. The night piece is the strongest.
Would do differently: the fjord composition is still a V; next time bend the channel hard
so a headland closes the view. Blueprint text at 8px is soft — 9.5px bold minimum on blue.
