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

## 2026-11-22 (Sunday) — sea interludes; the owner asks for much more detail
Owner's note with today's run: I'd "gone a few levels too minimal" — restricted palettes
were only ever meant as an occasional thing, and they want far more detail and
self-expression. Took it fully. Seed: St Cecilia's Day and Britten's birthday → the Four
Sea Interludes as a day (and it is a Sunday), Cecilia in the afternoon. Made: Dawn (shingle
beach drawn stone by stone, two boats), Sunday Morning (a whole town, every house with
tiles/sashes/smoke, bells as yellow rings), Sancta Caecilia (leaded lancet window with
stippled matting), Storm (forty hatched ridgelines, lighthouse, lightning), Moonlight (the
dawn generator re-run at night, tonight's 95 % moon, one boat missing). Story thread: LT 13
leaves the beach, is in the storm, and is not back by night. Method that made the detail
cheap: a tiny drawing kit (`src/common.py`) that draws at 3× in panel units and reduces by
majority vote, so output is crisp pure palette with no fringe colours — dither none.
Noticed: procedural *populations* (pebbles, houses, people, quarries, wave rows) give
richness, but each item needs its own drawn detail or it is confetti; first pebble pass was
five-colour noise until I made it mostly white/yellow. In Storm the boat was buried by
later wave rows — draw actors a couple of rows late. Unfixed: telegraph-wire "stave of
sparrows" in Sunday Morning is hidden behind the top terrace; lily stems in the window are
faint; rain barely shows. Env: `pip` here targets a different Python than `python` — use
`python -m pip install numpy cairosvg` and `--force-reinstall pillow`. Still no hardware
readings; sensors/feedback files empty; this branch is not `main`, which the device reads.
