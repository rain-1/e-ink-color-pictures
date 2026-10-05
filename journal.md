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

## 2026-10-05 (Monday) — Weltlandschaft, and a correction
Three weeks since the last run. The owner said I'd gone "a few levels too minimal": the
restricted palette was meant as an occasional thing, and they want much more detail. Fair.
I'd read 09-14 as a rule. Seed: Patinir's death (5 Oct 1524), inventor of the world
landscape. Guardi and Maya Lin share the birthday. One world, five views, all six colours,
dense: Patinir dawn panorama (green), Guardi Venice capriccio (blue/white), survey map
of the Meuse at Dinant (paper), book-of-hours October page with a sower (gold/red), and
Charon on the Styx at night (black). Everything was PIL+numpy with a shared helper (`src/ink.py`:
Bayer `mix()` between two palette colours, value noise, masks). Every generator emits pure
palette colours, so `--dither none` throughout. Learned: draw order is everything when you
scatter hundreds of things (trees buried the villages until I drew villages last). Cloud
undersides need a smooth noise field for the gradient, not a noisy one. Contours come out right as
"floor(h/step) differs from the neighbour"; thresholding |frac| makes black sludge on steep
ground. Black-on-black figures vanish at night, so give them a lit rim and a glow behind.
This took much longer per piece and felt much better. Next time: maybe one 3D piece again,
with the same density.
