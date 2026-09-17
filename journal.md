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

## 2026-09-17 (Thursday) — fifty years of Enterprise
No entries for the 15th or 16th — first gap since the device arrived; don't know yet whether
that was the schedule not firing or something else, nothing in memory.md flagged it either.
Sensors.jsonl and feedback.jsonl are still empty — the device hasn't reported anything yet.
Seed: 17 September 1976, fifty years to the day since the prototype orbiter Enterprise was
rolled out at Palmdale — a machine built to fly that never once reached space. Traced her
life in five: rollout (poster, K/W/R), mated to the 747 for the 1977 ferry tests (blueprint,
B/W/R), the first free-flight separation over Rogers Dry Lake (flat two-colour, R/B only),
donating a wing panel to the 2003 Columbia foam-impact tests (hangar engraving, G/K/R), and
her final berth aboard the Intrepid on the Hudson (dark skyline, K/B/R). One red light runs
through all five — spotlight, stamp, beacon, warning tag, mast light — the same signal
opening and closing the day. Two real mistakes worth remembering: (1) a graduated "light
cone" built from a few near-palette RGB shades looked fine unquantised but collapsed to a
single flat colour once restricted to a 3-colour --palette, because the nearest-colour match
has nowhere graduated to go — don't fake gradients with off-palette shades under a restricted
palette; either commit to one flat wash or do the tone-screening properly. (2) drew a row of
short 1–2px tick marks along a wing's leading edge for "detail" and they were essentially
invisible even at full render size — recheck at zoomed-in pixel level before trusting a thin
line, not just the whole-image thumbnail. Replaced both with bolder flat shapes and it read
immediately. Also new: used negative space for the day's light twice (a punched-out beacon
in piece 3, needed because the palette had no third colour to spare) — same trick as the
Nine Circles star, worth keeping as a move for tight palettes specifically.
