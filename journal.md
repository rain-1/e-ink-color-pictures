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

## 2026-11-24 (Tuesday) — the Beaver Moon; turning the detail up
Owner's note with today's prompt: I had gone "a few levels too minimal" — restricted palettes
were meant as an occasional thing, and they want much more detail. Fair. Seed: tonight's
perigee full moon, the Beaver Moon, so five readings of beavers and the moon (plus
Lautrec's birthday for the evening). Made: shin-hanga pond at moonset (full palette),
keyed cross-section of a lodge, a survey map of a dammed valley with generated terrain,
a Lautrec-style spatter poster of moonrise through alders, a lunar-atlas page with key and
phase strip. All five are Python/PIL drawn at native 400×600 with no anti-aliasing, tone done
by Bayer or spatter screens inside the generator, sharing `src/common.py`. Noticed: density
comes cheaply from loops (sticks, twigs, tree glyphs, craters) but *legibility* still needs
a few big shapes underneath — every piece kept one. Screening blue over a yellow dither
reads as grey mud; don't. A lodge drawn to scale fills the pond — lay out the open water
first. Thin trunks drawn as chained ellipses need ~400 steps or they bead. Black figure on a
black bank vanishes; stand it against the bright reflection. Would do differently: the
shell of the lodge still reads grey rather than stick-brown; the poster beaver could be
bigger. First run since 09-14 — ten weeks' gap; sensors and feedback files still empty.
Environment: system Pillow was broken for python3.11; `pip install --ignore-installed pillow` fixed it.
