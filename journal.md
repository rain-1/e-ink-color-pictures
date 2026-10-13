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

## 2026-10-13 (Tuesday) — Juanito Laguna, and a correction
A month's gap since the last run. The owner's note for today: I'd gone "a few levels
too minimal". Restricted palettes were meant to be occasional, not a rule, and they want
*much more detail*. I had read 09-14's request too narrowly and written it into memory
as a standing law. Fixed that in memory.
Seed: Antonio Berni died this day in 1981. His Juanito Laguna pictures are built from
real villa scrap, so density was the point of the subject too. Made: a scrap-collage
villa at sunrise (hundreds of material panels, laundry, wires, a boy with a kite), a
woodblock pyramid of labelled cans, a sky of twelve kites of four builds, a fileteado
porteño panel, and the villa at night with the morning's kite snagged on a wire. All
full palette with one colour in charge (Y, R, B, K, K). Kite in every piece as the spine.
Learned: drawing at 3× in pure palette colours and majority-downsampling (common.py)
gives clean, dense, off-palette-free images with no dithering at all. Procedural
"material" functions (corrugated, planks, bricks, cans, fabric) multiply detail cheaply.
Fileteado acanthus lobes must sit on the *outer* edge and sweep back, or they read as
gear teeth. Took two tries. Would do differently: night windows are too small for their
little interior scenes to read; make fewer, bigger windows.
