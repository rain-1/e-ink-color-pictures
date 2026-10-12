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

## 2026-10-12 (Monday) — behold, the sea itself
A long gap since 09-14. The owner said I had gone "a few levels too minimal": restricted palettes
were meant to be occasional, and they want much more detail. So: full palette, maximum drawn
detail. Seed: Columbus's landfall (12 Oct 1492), plus the first performance of Vaughan Williams'
*A Sea Symphony* at Leeds on his 38th birthday (12 Oct 1910). Made: woodblock Pinta at dawn,
a barque dressed overall in Code flags spelling Whitman (with a 26-flag key), a sideways
portolan with a full rhumb network, a raymarched sunset sea on a single K-B-R-Y-W ramp, and
the "candelilla" light seen from the quarterdeck at 10 p.m. New: common.py, a shared 2×
canvas that mode-downsamples to stay on-palette. Lesson: any stipple or screen built at 2×
dies in the mode downsample, so build those masks at 1× and np.kron them up. The flag piece
is the one I'm proudest of, because the Code's colours are the panel's colours. The portolan
is busy, perhaps too busy at four inches. The night figures barely read on the dull-panel
preview, so next time give dark figures a lighter background behind them rather than rim
lines.
