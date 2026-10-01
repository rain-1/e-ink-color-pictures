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

## 2026-10-01 (Thursday) — the Tōkaidō, 1833 / 1964
Owner's note today: I'd gone "a few levels too minimal". Restricted palettes were meant to be
occasional, and they want much more detail. So: full palette and dense drawing all day.
Seed was the Tōkaidō Shinkansen opening on this date in 1964, set against Hiroshige's
Fifty-three Stations of the same road. Made: Nihonbashi woodblock with a procession, a crowd
and a gate frame (morning); a raymarched 0-series with Fuji and tea pickers, screened per
material (midday); a Marey train graph of the opening day (afternoon); Shōno driving rain
with a lit Kodama behind the bamboo (evening); a night chart of the corridor on a real
Natural Earth coastline (night). Noticed: per-material Bayer ramps (each surface gets its
own 2–3 inks) beat both FS and plain quantising for 3D, because it looks printed rather
than speckled. Mid-grey (50%) screens over big areas read as static, so keep screens light
or dark. Mistakes: an ugly first rain pass with groves masking everything; Fuji
mis-classified as fields until I keyed on height; an inverted station list for up trains.
Natural Earth geojson is reachable from raw.githubusercontent.com, but naciscdn is blocked.
Next time I'd give the evening piece one fewer layer.
