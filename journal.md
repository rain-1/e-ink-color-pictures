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

## 2026-10-04 (Sunday) — Laudes Creaturarum, and a correction
Owner said I'd gone "a few levels too minimal": restricted palettes were meant to be
occasional, and they want much more detail. I'd over-read 09-14. So today I used all six
colours and made every piece dense. The seed was Francis: 800 years since his death on 3 Oct
1226, his feast today, and World Animal Day. One verse of the Canticle per slot: a sun-face
over Assisi, a millefleur Mother Earth with the Wolf of Gubbio, a Giotto fresco of the
sermon to the birds, a simulated bonfire with friars, and the Porziuncola at night with
a spiral of larks under the moon. I wrote a shared common.py and briefed five parallel
agents, one per piece. Each iterated 2–4 times on its own. All five came back far richer
than anything before, and nothing needed fixing at review. Technical lessons: a box
downsample of 2x drawings turns black-on-yellow and black-on-white edges green, so snap
each 2x2 block to its majority colour instead. Bayer screens work on bounded objects and
read as speckle on big open fields. Fire comes alive when a noise field rises with the heat.
Next time: put the majority-snap finish into the shared helper from the start.
