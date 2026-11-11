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

## 2026-11-10 (Tuesday) — the line of beauty; and nothing has reached main since 09-14
Owner said (again, it turns out): far too minimal, restricted palettes were only meant as an
occasional thing, express yourself with much more detail. Seed: Hogarth born 1697 → his
serpentine "line of beauty" hidden in five crowded, full-palette pieces: map-landscape with
an S river (~100 textured fields, 190 trees, village), an engraved plate with 20 numbered
specimens, an oval staircase projected in 3-D and painted back to front, a street elevation
with ~40 inhabited windows, and a candlelit still life engraved by code (tone → line width,
angle per object). Learned: (1) downsampling thin black lines makes grey, and grey snaps to
GREEN — fixed with a vote-downsampler in kit.py; (2) a 3-D stairwell only reads if the well
nearly fills the frame; (3) the engraving shader needs black contours and a dark wall or it
is all texture. Would do differently: the morning piece is at the edge of too busy for 4".
DISCOVERY: `python` here is 3.11 without numpy — use /usr/local/bin/python3.13. And every
run since 09-16 pushed to its own claude/* branch; none was merged, so main (what the frame
fetches) still shows 09-14 and each day's memory.md was lost. ~27 days of work sit on
orphan branches (09-16…10-14). Told the owner.

## 2026-11-11 (Wednesday) — the dot and the repeat; main is still stuck
Owner's note again: too minimal, more detail (they are still seeing 09-14 on the frame).
Started on main's stale memory, found yesterday's branch (dreamy-einstein-ez7p4n) and
fast-forwarded onto it, so the journal is continuous from 11-10. Seed: Signac and Vuillard
share this birthday → dots and patterns, plus Martinmas and the Northern Taurid maximum; a
sailing boat hidden in each piece. Made: a pointillist port rebuilt from 28,000 pure-ink
strokes; a Vuillard interior of seven stacked repeats; a spiral pinwheel of eight patterns
off a painter's brush; a lantern procession zigzagging up a half-timbered hill town; a
scratchboard harbour under tonight's real eastern sky. Learned: (1) stochastic two-ink
strokes are a far better "dither" than any screen — but forbid black unless the tone is
truly dark, and make strokes overlap or white paper eats the picture; (2) full-canvas
pattern layers pasted through polygon masks make pattern-on-pattern cheap; (3) patterns
indexed by (log r, spiral angle) bend beautifully; (4) white line on black needs
vote_down(wk≈0.4) or hairlines vanish. Would do differently: fewer walkers per metre of lane
(the white zigzag nearly drowned), and labels under 8px on black are not legible.
