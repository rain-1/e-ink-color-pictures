# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback will be rare; I am my own critic.
- They like *code-made* art most. Not keen on image diffusion, curious if I ever have a
  real reason. 3D renders snapshotted and dithered: yes, occasionally — they've had two
  (spheres 09-13, Inferno funnel 09-14) and asked for nothing less.
- They asked on 09-14 for restricted palettes and *more detail and attention per piece*.
  That request stands until they say otherwise.
- They'll wire the temperature/humidity sensor up so I can feel the room — still not
  connected as of 09-19 (sensors.jsonl and feedback.jsonl are both still empty).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Big flat shapes and contrast survive; lines under ~2px and text under ~12px are
  at risk (unverified — still no hardware confirmation as of 09-19).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.
- Runs are not guaranteed daily — 09-15 through 09-18 have no journal entries or gallery
  folders. If a gap like that recurs, just pick the thread back up; don't try to backfill.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop, not a screen. Riso, screenprint, woodblock, linocut,
  engraving, poster, cut-paper, stained glass, star charts, technical plates, aquatint.
- Two or three colours per piece beats six. One colour in charge; the others are ink.
- Night should be mostly black with a little light in it.
- A day should have a thread — one seed, five readings of it — and a small recurring
  motif across the five (09-14: one star each; 09-19: one flag/pennant each) gives the
  day a spine.
- Detail is welcome when it's *drawn* detail: hatching, ticks, labels, tiny figures.
  Noise is not detail. Aquatint-style stipple (many tiny dots, density varying) is
  another way to get a filled tone without repeating a technique already used that week.
- A tiny figure gives scale and story. Use sparingly; it's a trick.
- When a silhouette needs to read against a busy or same-colour background (a boat
  against its own sunset), keep the *readable* part (mast, flag) on open ground and
  let only the ambiguous mass (hull-into-sun) blend — don't let the one legible element
  of the piece sit on top of same-coloured chaos.
- Don't over-engineer topological accuracy (a "real" bowline, a "real" constellation) —
  one clean, legible gesture beats four accurate ones that tangle. It's art, not a manual.

## Working methods that are proven
- Python/PIL generators writing to $OUT_RAW; SVG hand-written or emitted by Python
  (emit SVG from Python for anything with geometry — rings, tiers, ticks, compass roses).
- Render SVG at 2× then downsample (render.py does this); for Python generators,
  supersample 4× in PIL and downsample with LANCZOS for the same clean-edge effect.
- `--palette a,b,c` on render.py restricts quantisation. For 2-colour work with tone,
  do the 8×8 Bayer screen *inside* the generator on a 0–1 tone value and use `--dither none`.
- Raymarched heightfields in numpy are cheap (≈30 s at 400×600, 220 steps). Camera first,
  lighting second, fog last.
- Floyd–Steinberg only when I want a halftone/photographic feel (09-13 spheres).
- PIL's `ImageDraw.ellipse(..., outline=colour, width=w)` draws a clean thick circle —
  use it directly for anything that actually is a circle (compass rose, knot loop, sun);
  save hand-rolled bezier paths for genuinely irregular curves (coastlines, rope tails).
- SVG XML comments can't contain `--` (an em-dash-style pause) — cairosvg's parser will
  fail on it. Use a comma or semicolon in source comments instead.
- For a flat 2-colour "over/under" crossing (rope, knots, interlace): draw the under
  shape, punch a white gap slightly larger than the stroke width at the crossing point,
  then draw the over shape on top so it repaints through the gap. Only reliable for a
  single crossing per gap — don't chain more than one or two per piece.

## Running threads
- "Hard edges" (09-13, Robert Indiana) and "Dante / stelle" (09-14). Both could return.
- Nautical / maritime (09-19: signal flags, charts, knots, ships) — rich vein, could
  return: other knots, other code flags, tide tables, lighthouses, rigging.
- 3D: a lit room, a glass object, a staircase, a single chair — things with shadows.
- Charts and plates: star charts, tide tables, sonar/fathometer traces, old technical
  drawings as art.

## Avoid / learned the hard way
- Photographic / raytraced sources: large flats must be pure palette colours before
  dithering or they speckle (09-13).
- Silhouettes under ~40px don't read. Double them (09-13).
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Generic ordered dither on a two-colour palette produces a thin band of texture, not
  tone. Do the screen in the generator (09-14).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14, Purgatory).
- Don't stack a same-colour focal element (a flag) on top of another same-colour mass
  (a sun) — it disappears. Give the one thing that has to read its own clear ground
  (09-19, evening piece's first draft looked like a church, not a boat).
- A "correct" multi-crossing knot/interlace drawn from scratch tangles fast — one loop
  and one small bight reads as a knot; four intertwined bezier segments read as a mess
  (09-19).

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, FS-dithered raytrace, linocut bands, 1-D automaton
  (09-13); woodcut forest, isometric terraces, Bayer-screened raymarch, engraved
  cosmological plate, star chart (09-14); hard-edge flag poster, sonar/fathometer chart,
  rope/knot diagram, cut-paper silhouette, aquatint stipple (09-19).
- subjects: sunrise+boat, numeral 13, spheres still-life, geese, Rule 30 (09-13);
  dark wood, Purgatory mountain, Inferno funnel, Ptolemaic spheres, Summer Triangle
  (09-14); signal flags, chart/compass rose, bowline knot, ship at sunset, ship at night
  under Polaris (09-19).
- palettes used: K/G/W, Y/K/W, K/R, B/Y/W, K/W (09-14); R/B/W, G/K, B/W, R/Y, K/B
  (09-19). Untouched two-colour combos: R/W, G/Y, R/B (three-colour W/G/R and Y/G/B
  also untried).
