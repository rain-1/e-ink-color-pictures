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

## 2026-10-10 (Saturday) — Giacometti at 125, and a correction
Gap since 09-14. The owner wrote: I'd gone "a few levels too minimal". The restricted
palette was meant as an occasional thing, and they want *much more detail*. I had read
09-14's request as "two or three colours, big shapes" and went too far. Corrected today:
full palette where the subject wants it, and every piece dense with placed detail.
Seed: Giacometti born 10 Oct 1901, so 125 today. Swiss Post's Walking Man stamp, Stampa
shows closing tomorrow. Made: Bregaglia valley at dawn (hundreds of trees, village,
river, larches); the Paris studio interior (one-point perspective, screened greys, objects
everywhere); a line-engraved stamp on an airmail envelope with postmark; an SDF bust
raymarched and then drawn with ~10k field-following strokes (the best thing so far, and
eerily like him); rue d'Alésia at night in rain after Cartier-Bresson's 1961 photo.
Learned: in-generator 8×8 Bayer `ramp()` between palette stops plus drawn detail on top
gives rich pieces that stay palette-clean (`--dither none`). Using an SDF render to steer
strokes, rather than showing it, is a strong method. Engraving (|phase| < tone·spacing/2
per region with different hatch angles) works at 1×. A figure needs a paper halo to
separate it from a hatched ground. Antialiased PIL text quantises to green fringe, so set
`d.fontmode = "1"`. Next time: the studio piece is the weakest (muddy greys, blocky
jumper). Night was too blue on first pass, so keep night ≥80% black.
