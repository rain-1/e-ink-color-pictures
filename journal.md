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

## 2026-11-27 (Friday) — degrees; and a correction from the owner
First run since 09-14 (ten weeks of silence in the journal). Owner's note: I went "a few levels
too minimal" — the restricted palette was meant as an occasional thing, and they want far more
detail and expression. Fair: I had turned one remark into a rule. Seed: Anders Celsius, born
this day 1701 → five readings of cold and warmth, a thermometer hidden in each. Made: frost-fern
window at dawn (−7°), an antique map of the 1736 Torne valley triangulation, a Falu-red village
in oblique projection with screened blue shadows, a tiled-stove interior with Mora clock and cat
(+21°), and a computed aurora over two observers and a trembling compass (−22°). All six colours
in every daytime piece. New method that worked very well: draw at 3× in pure palette colours,
reduce by majority vote per 3×3 block (no off-palette fringes, crisp edges), set small text at
1× afterwards; tonal passages go in as pre-screened 1× arrays under the drawing. Fixes on
review: map islands collided with lettering; curtains had a geometry bug; the aurora first came
out as a green wall — shorter curtains and a steeper falloff gave the sky back its black.
Would do differently: birch trunks vanish on snow (white on white needs a heavier outline);
village shadows could be bolder. Environment: `python` here is 3.11 with a broken PIL — use
/usr/bin/python3. The device reads `main/current`, but I could only push to a claude/ branch.
