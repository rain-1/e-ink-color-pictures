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

## 2026-10-02 (Friday) — Rocket Sunday; correcting course to full detail
Gap since 09-14. Owner said I'd gone "a few levels too minimal": the restricted palette
was meant as an occasional thing, and they want much more detail. So: all six inks in
every piece, and many more drawn elements. Seed: Alex Raymond (Flash Gordon, b. 1909) and
Gwen Marston (liberated quilts, b. 1936) share today's birthday. Made: deco dawn launch over
a windowed city, an original five-panel Sunday comic page, a liberated medallion quilt
with a pieced rocket, an alien jungle moonrise with recursive ferns, and a cockpit at night
with dials and a radar scope. A red rocket in each. Built `src/ink.py`: a 1x, no-AA canvas
with masks, Bayer ramps, Ben-Day dots and hatching, so output is palette-pure and
`--dither none` works. Every piece took one fix: watchers vanished black-on-black (gave
them a yellow halo); black ferns vanished on hatched ground (thicker, red halo); comic
panel text got cut off; postcard label ran off the bottom. Far more satisfying than the
minimal days. Next time: check sizes against the edges before rendering, and maybe let
one piece be a single huge detailed object instead of a full scene.
