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

## 2026-11-25 (Wednesday) — more detail, full palette; The Mousetrap
First run since 09-14 (ten weeks of nothing in the gallery — I don't know why). The owner
left a note on the prompt: I'd gone "a few levels too minimal"; restricted palettes were
meant as an occasional thing, and they want much more detail. Took that as the brief.
Seed: The Mousetrap opened 25 Nov 1952. Five views of snowbound Monkswell Manor, a mouse
in each: dawn exterior (morning), doll's-house section with eight people and a cellar
(midday), blueprint ground plan with pencilled detective notes (afternoon), proscenium
and red curtains from the stalls (evening), telephone wires as a stave with mice for notes
under the real post-full moon near Aldebaran (night). Method change: everything drawn 1:1
in pure palette colours with PIL, tone from patterns (Bayer tints, brick, hatch, wallpaper
repeats), `--dither none`. A shared `src/common.py` held palette, patterns, fonts, a mouse.
Noticed: patterned fills are what make a small picture feel rich — every room got its own
paper. Text on a dithered ground breaks up; give it a solid plate. Red on blue is nearly
invisible; yellow on blue sings. First night draft had a white snowfield — had to pull it
down to blue/black. Environment: `python` is 3.11 without the deps; use `python3.13`.
DejaVu has no serif italic; Liberation has every style. Would do differently: the smoke
(stacked arcs read as springs) and Orion, which got lost behind the wires.
