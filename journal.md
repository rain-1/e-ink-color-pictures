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

## 2026-10-09 (Friday) — Hangul Day, and a correction
Owner's note today: I'd gone "a few levels too minimal". Restricted palettes were meant as an
occasional thing, not a rule, and they want much more detail. Fair: 09-14 was spare. (The
gap since 09-14 means some days didn't run or weren't recorded.) Seed: Hangul Day, the
1446 Hunminjeongeum, whose letters are drawn from the mouth and from heaven/earth/person.
Made, all six colours and dense: Irworobongdo screen (morning), Haerye anatomical plate
with stroke-drawn jamo (midday), a 12-compartment chaekgeori bookshelf (afternoon),
magpies in a persimmon tree at dusk (evening), Draconids over a village (night).
Learned: drawing everything at 1× directly in palette inks with PIL, plus a Bayer screen
between two named inks for tone, gives crisp, rich results with --dither none. Small object
libraries (book, vase, persimmon, magpie, hanok) multiply detail cheaply. Mistakes I fixed:
the first tree had about 200 fruits, and the sun vanished into a yellow sky (keep the sky
redder so a pure-yellow disc pops). No Korean font, so I wrote jamo as stroke specs in
kit.py; IPAGothic covers hanja. Next time: check that each piece has a focal point
inside the detail; the bookshelf is charming but has no single hero.
