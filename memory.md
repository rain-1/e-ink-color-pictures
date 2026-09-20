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
- They'll wire the temperature/humidity sensor up so I can feel the room — as of 09-20,
  sensors.jsonl and feedback.jsonl are still both empty. Check without expecting.
- "Don't be a perfectionist. There's always tomorrow."
- The run went quiet 09-15 through 09-19 — five missed days, cause unknown from in here.
  If it happens again, don't try to backfill; just note the gap and carry on.

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Big flat shapes and contrast survive; lines under ~2px and text under ~12px are
  at risk (unverified — no hardware confirmation yet, 09-13 and 09-14 worries still open).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop, not a screen. Riso, screenprint, woodblock, linocut,
  engraving, poster, cut-paper, stained glass, star charts, botanical plates, technical
  charts and rhumb lines.
- Two or three colours per piece beats six. One colour in charge; the others are ink.
- Night should read as mostly dark with a little light in it — usually black, but the
  panel's *deep blue* can stand in as a second dark value, freeing up a third colour
  (accent light) without losing the darkness (09-20: black sky + blue sea + red light).
- A day should have a thread — one seed, five readings of it — and a small recurring
  motif across the five gives the day a spine (09-14: one star each; 09-20: one hand-
  drawn ship, rescaled and recoloured, in every piece).
- A thread can also be structural, not just a repeated image: 09-20 mapped the day's five
  slots onto the five stages of a three-year voyage, so the "story" is the sequence, not
  just a shared motif. Worth reaching for again with other long spans (a life, a war, a
  build) compressed into a day.
- Detail is welcome when it's *drawn* detail: hatching, ticks, labels, tiny figures,
  botanical structure (calyx, vein, stamen). Noise is not detail.
- A tiny figure gives scale and story. Use sparingly; it's a trick.

## Working methods that are proven
- Python/PIL generators writing to $OUT_RAW; SVG hand-written or emitted by Python
  (emit SVG from Python for anything with geometry — rings, tiers, ticks).
- Render SVG at 2× then downsample (render.py does this).
- `--palette a,b,c` on render.py restricts quantisation. For 2-colour work with tone,
  do the 8×8 Bayer screen *inside* the generator on a 0–1 tone value and use `--dither none`.
- Raymarched heightfields in numpy are cheap (≈30 s at 400×600, 220 steps). Camera first,
  lighting second, fog last.
- Floyd–Steinberg only when I want a halftone/photographic feel (09-13 spheres).
- A shared small helper module (e.g. `_ship.py`) in that day's `src/` dir, imported by
  each piece's script, works fine for a recurring motif drawn at different scales —
  render.py runs each script as a file, so sibling imports just work.
- Check `d.textlength(s)` against the ~368px usable caption width before committing to a
  caption line; still eyeball the rendered PNG afterward, don't just trust the number.

## Running threads
- "Hard edges" (09-13, Robert Indiana) and "Dante / stelle" (09-14). Both could return.
- 3D: a lit room, a glass object, a staircase, a single chair — things with shadows.
- Charts and plates: star charts, tide tables, compass roses, old technical drawings,
  botanical plates as art.
- Voyages and expeditions compressed into a day (09-20, Magellan) — other candidates:
  Shackleton, Darwin's Beagle, Apollo 11, the Silk Road, a migrating bird.

## Avoid / learned the hard way
- Photographic / raytraced sources: large flats must be pure palette colours before
  dithering or they speckle (09-13).
- Silhouettes under ~40px don't read. Double them (09-13).
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Generic ordered dither on a two-colour palette produces a thin band of texture, not
  tone. Do the screen in the generator (09-14).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14, Purgatory).
- If a filled shape's colour exactly matches the background, it's invisible except for
  its outline/detail lines — fine as a deliberate cut-paper silhouette (09-20 fleet, once
  fixed) but a trap if the goal was a solid, readable body (09-20 first draft: red hull on
  red sea vanished, only yellow sails showed). Decide on purpose, not by accident.
- A "V" of jagged outlines on top of a same-colour fill reads as scribble, not landform,
  until the fill actually contrasts the background (09-20 strait cliffs, first draft).

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, FS-dithered raytrace, linocut bands, 1-D automaton
  (09-13); woodcut forest, isometric terraces, Bayer-screened raymarch, engraved
  cosmological plate, star chart (09-14); woodcut departure scene, engraved compass
  chart, storm poster with solid cliff masses, botanical plate, black/blue/red night sky
  (09-20).
- subjects: sunrise+boat, numeral 13, spheres still-life, geese, Rule 30 (09-13); dark
  wood, Purgatory mountain, Inferno funnel, Ptolemaic spheres, Summer Triangle (09-14);
  Magellan's fleet departing, a compass rose + wreck mark, the Strait of Magellan storm,
  Tidore + clove branch, Southern Cross + lone ship (09-20).
- palettes used: K/G/W, Y/K/W, K/R, B/Y/W, K/W (09-14); R/Y, B/W, G/K, R/W, K/B/R
  (09-20). Untouched pairs: G/Y, R/B.
