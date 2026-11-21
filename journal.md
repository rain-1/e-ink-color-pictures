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

## 2026-11-21 (Saturday) — things that stay up; and a correction
Owner's note: I had gone "a few levels too minimal" — restricted palettes were meant as an
occasional thing and I'd also flattened the detail. They want much more detail and
expression. So: full six colours, dense drawing. Seed: first free balloon flight (La Muette,
21 Nov 1783, 1:54 pm) + Magritte's birthday (1898). One ornate Montgolfière in all five:
dawn inflation under the four morning planets; a Magritte room where the canvas continues
the window; a hand-coloured engraving over a thousand Paris roofs; an Empire-of-Light street
under a noon sky raining balloons; tonight's 89% moon and Saturn over sleeping Paris.
Method that made the detail possible: draw at 3x in one RGB image, keep pure-palette strokes
crisp, FS-dither only the mixed tones (`finish()` in src/common.py). The balloon is a texture
"skin" drawn flat then wrapped per-pixel round a profile, so the ornament foreshortens.
Learned: neutral grey is nearest to *green* on this palette, so grey tones dither into
red/green/blue confetti — screen greys in black/white by hand (the moon). 1-bit italic text
needs bold-italic ≥13px. Black figures on black ground vanish (dawn rope crews, the bowler
man) — give silhouettes a lit backdrop. Sensors and feedback files still empty; timezone
still unknown. Would do differently: fewer balloons in the evening lattice; plan where the
light is before placing figures.
