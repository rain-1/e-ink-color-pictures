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

## 2026-10-06 (Tuesday) — Kon-Tiki, and a correction
Owner's note: I went "a few levels too minimal". They meant restricted palettes as an
*occasional* thing, and they want much more detail. Fair. 09-14 had read "restricted" as a rule.
Seed: Thor Heyerdahl's birthday (1914) → one day's light across the 101-day drift.
Made, all full-palette and dense: FS-dithered painted sunrise with raft and sun-god sail;
a natural-history plate of what swam under the raft (whale shark spot-grid, dorados,
barnacles, numbered key); an engraved chart of the track with a 101-cell log of computed
moon phases; a screenprint sunset of the wreck on Raroia reef with a big palm; a stippled
night of Milky Way, Crux, plankton wake and a glowing thing below.
Noticed: PIL text antialiasing snaps to *green* when quantised. Set `dr.fontmode = "1"`.
FS on a painted RGB scene looks noisy on the contact sheet but rich at full size, and
`--dither ordered` is bolder but turns sea glitter into green blotches. Brown has no
palette home (it becomes red+green speckle), so paint wood as black with yellow highlights.
A shared `lib.py` (Bayer screen, noise, fonts) made five detailed pieces cheap. Keep it.
Next time: the sunrise sail covered the sun on the first try, so sketch the composition
before painting. Two of five pieces carried text. That's enough.
