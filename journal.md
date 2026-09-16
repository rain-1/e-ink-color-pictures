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

## 2026-09-15 — no run
Missed. No entry, no gallery folder — the schedule didn't fire or nobody was watching.
Noticed on the 09-16 run when the branch turned out to already be merged to main with
nothing after 09-14 on it. Nothing to learn except: check for gaps at the start of each run.

## 2026-09-16 (Wednesday) — Kandinsky's birthday
Seed: Wassily Kandinsky, born this day in 1866. Instead of a scene, used his own visual
vocabulary as the day's five styles: point/line/plane (his 1926 treatise, pure geometry,
no type — morning), Several Circles (a crowded field of coloured discs on black, the one
piece let off the restricted-palette rule because the subject *is* many circles — midday),
Der Gelbe Klang (a diagonal burst of red/black shards out of a yellow ground, after his
synesthesia and 1912 stage piece — afternoon), the Bauhaus yellow-triangle/red-square/
blue-circle correspondence stacked as three flat shapes on white — evening), and two green
circles nearly level on black with the equinox six days off — night). The circle recurred
in all five as the day's spine, the way the star did on 09-14. No hardware feedback yet,
still going in blind on how small ticks/lines survive the real panel. Also: 09-15 was
skipped somewhere upstream — worth a first-thing check in future runs for a gap since the
last gallery folder, in case a run needs to be caught up rather than just continued.
