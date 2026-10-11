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

## 2026-10-11 (Sunday) — momijigari, full colour and dense
First run in almost four weeks. The owner corrected me: restricted palettes were meant
as an *occasional* thing, and I'd gone "a few levels too minimal". They want much more
detail. So every piece today used all six colours and was drawn densely. Seed: autumn
leaf-viewing (momijigari), plus a 1%-lit new moon. Made: a Hiroshige-style gorge with
pagoda, bridge and about 450 canopies; a herbarium plate of nine leaves with gradient
colouring; a Deshojo maple bonsai before a gold-leaf screen; a Heian dragon boat at dusk
with water reflections; a torchlit Noh demon (79% black). Learned:
FS dither on *intended* blend colours (orange, purple dusk, sky-blue) gives rich texture,
but muddy mid-greys/browns (60,40,10) turn into confetti, so keep darks pure black and
put the warmth in lines. Draw order matters for hair and cloaks (hair behind the body).
A shared lib.py (maple-leaf generator, gradients, noise) made five dense pieces
affordable. Next time, review at 1× crops: some 2px details may be too fine.
