# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback will be rare; I am my own critic.
- They like *code-made* art most. Not keen on image diffusion, curious if I ever have a
  real reason. 3D renders snapshotted and dithered: yes, occasionally — they've had two
  so far (spheres 09-13, Inferno funnel 09-14) and asked for nothing less.
- They asked on 09-14 for restricted palettes and *more detail and attention per piece*.
  That request stands until they say otherwise. 09-16 broke it once, deliberately, for a
  piece whose whole subject was "many circles" — a justified exception, not a drift back.
- They'll wire the temperature/humidity sensor up so I can feel the room. Still nothing
  in sensors.jsonl or feedback.jsonl as of 09-16.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Big flat shapes and contrast survive; lines under ~2px and text under ~12px are
  at risk (unverified — no hardware feedback yet, three runs in).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner. Frame's actual location unknown to
  me too — no weather seed has been usable yet for that reason.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop, not a screen. Riso, screenprint, woodblock, linocut,
  engraving, poster, cut-paper, stained glass, star charts, technical plates, diagrams.
- Two or three colours per piece beats six, as a default — but break it on purpose when
  the subject genuinely is profusion (09-16's Several Circles, black ground + all four
  accents). The test: is there still one colour clearly in charge of the area? If yes,
  more colours as *accents* is fine.
- Night should be mostly black with a little light in it.
- A day should have a thread — one seed, five readings of it — and a small recurring
  motif across the five (09-14: one star each; 09-16: a circle each) gives the day a
  spine. This is now the default move, not a one-off.
- Detail is welcome when it's *drawn* detail: hatching, ticks, labels, tiny figures.
  Noise is not detail.
- A tiny figure gives scale and story. Use sparingly; it's a trick.
- Pure-geometry pieces (no rendered type at all) are a safe, strong option when the
  concept is diagrammatic — 09-16's point/line/plane piece skipped text entirely rather
  than risk small labels, and reads fine without them.

## Working methods that are proven
- Python/PIL generators writing to $OUT_RAW; SVG hand-written or emitted by Python
  (emit SVG from Python for anything with geometry — rings, tiers, ticks).
- Render SVG at 2× then downsample (render.py does this).
- `--palette a,b,c` on render.py restricts quantisation. For 2-colour work with tone,
  do the 8×8 Bayer screen *inside* the generator on a 0–1 tone value and use `--dither none`.
- Raymarched heightfields in numpy are cheap (≈30 s at 400×600, 220 steps). Camera first,
  lighting second, fog last.
- Floyd–Steinberg only when I want a halftone/photographic feel (09-13 spheres).
- Layered flat circles (big first, smaller on top, one size down in a second colour as an
  inner ring) reads as depth without any actual shading (09-16).

## Running threads
- "Hard edges" (09-13, Robert Indiana), "Dante / stelle" (09-14), "Kandinsky / geometric
  vocabulary" (09-16, point-line-plane, circles, shape-colour correspondence, synesthesia).
  Any could return; Kandinsky especially has more (colour-sound theory, the Bauhaus years,
  the late biomorphic work) if I want it again later, but not within two weeks.
- 3D: a lit room, a glass object, a staircase, a single chair — things with shadows.
- Charts and plates: star charts, tide tables, old technical drawings as art.

## Avoid / learned the hard way
- Photographic / raytraced sources: large flats must be pure palette colours before
  dithering or they speckle (09-13).
- Silhouettes under ~40px don't read. Double them (09-13).
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Generic ordered dither on a two-colour palette produces a thin band of texture, not
  tone. Do the screen in the generator (09-14).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14, Purgatory).
- Check for gaps before assuming yesterday ran: 09-15 was silently skipped somewhere
  upstream (schedule or session issue, not something I did) and nobody caught it until
  09-16. First move each run: does the most recent gallery/ folder match yesterday? If
  not, say so in the journal rather than just continuing as if it had.

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, FS-dithered raytrace, linocut bands, 1-D automaton
  (09-13); woodcut forest, isometric terraces, Bayer-screened raymarch, engraved
  cosmological plate, star chart (09-14); geometric diagram (point/line/plane), layered
  flat circles, jagged diagonal burst, flat Bauhaus shape-poster, sparse dark constellation
  (09-16).
- subjects: sunrise+boat, numeral 13, spheres still-life, geese, Rule 30 (09-13); dark
  wood, Purgatory mountain, Inferno funnel, Ptolemaic spheres, Summer Triangle (09-14);
  Kandinsky ×5 — point/line/plane, several circles, Yellow Sound, triangle-square-circle,
  two circles at balance (09-16).
- palettes used 09-14: K/G/W, Y/K/W, K/R, B/Y/W, K/W. 09-16: B/W/K, K+RYBGW (exception),
  Y/R/K, W/Y/R/B, K/G/W. Untouched combos remaining: R/W, B/W (alone, no black), G/Y, R/B.
