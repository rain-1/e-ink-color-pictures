# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: yes.
- **Standing instruction (2026-11-20, their words, attached to the daily prompt):** "you've
  gone a few levels too minimal… I only suggested a restricted palette as an occasional
  thing… I'd like to see you express yourself with much more detail!!"
  → Default is now: full six colours, dense, layered, richly drawn pieces. A restricted
  two/three-colour piece is an occasional change of pace (at most ~1 in a week), and even
  then it should be intricate, not sparse. (My reading: they want to be able to stand at
  the frame and keep finding things.)
- Feedback is rare and comes as a note on the prompt. Take it seriously when it comes.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines of 1px and text under ~10px are at risk (still unverified — no hardware
  report, sensors.jsonl and feedback.jsonl are empty as of 11-20).
- Refresh 15–30 s with flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: unknown, publishing with UTC. Ask the owner if a channel ever opens.

## Taste I'm developing (mine — revise freely)
- Dense, not noisy. Density comes from *layers*, each with a job:
  1. a field (sky, sea, trunk) in one dominant colour;
  2. tone by screens — Bayer stipple or line-hatch between two palette colours;
  3. engraved structure — iso-lines/contours of the same noise that made the shape;
  4. drawn objects in their hundreds — trees, houses, windows, birds, leaves, soundings;
  5. one piece of wit or story — a red cone that doesn't fit the mountain, dividers
     walking a coast, an owl in a knot-hole.
- One colour still leads each piece even when all six are present (11-20: blue/white,
  blue/white, paper, red/black, black). Vary the leader across the day.
- Night: ≥70% black, light as blue stipple, white only at the source, yellow windows.
- A day wants a thread — one seed, five readings — plus a small recurring mark
  (09-14: a star; 11-20: a caption band with a clause and a tiny Mandelbrot set).
- Real data inside the picture is satisfying (11-20: the divider table was measured from
  the generated coastline). Do this more: tide tables, sun paths, actual star positions.
- Print-shop references still serve: engraving, survey plates, sea charts, woodblock,
  ukiyo-e, botanical plates, stained glass, comics — but filled in, not pared down.

## Working methods that are proven
- **Environment:** run everything with `/usr/bin/python3` (has numpy, PIL, cairosvg);
  bare `python`/`python3` on PATH is a different interpreter without them. No scipy.
- **Native palette drawing (11-20, best so far):** work at 400×600 in palette indices in a
  numpy array; PIL ImageDraw on a "P" image for vector parts (no antialiasing, crisp);
  render with `--dither none`. See `gallery/2026-11-20/src/common.py` — copy it forward:
  `Plate` (put/draw/stamp/caption/save), `fbm`, `screen` (8×8 Bayer on a 0–1 tone),
  `hatch` (line screen), `blur`, `grow`, `edge`, `mandel`, `font`.
- `Image.fromarray(...)` is read-only: `.copy()` before floodfill/drawing on it.
- fBm iso-lines (`floor(field/step)` differs from neighbour) = instant engraving.
- Worley F2−F1 on stretched, warped coords = bark, cracked mud, cells, scales, cobbles.
- Voronoi in perspective-warped coords = patchwork fields.
- Voxel-space terrain (Comanche-style column renderer) ≈ 5 s; start z ≥ 30 to avoid
  near-field streaks; ≤ 7 octaves; classify snow/forest by *percentiles of visible
  altitude*; get camera right before anything else (took 4 tries on 11-20).
- Midpoint displacement + recursive branches = lightning, rivers, cracks, roots.
- Distance from a mask by alternating square/plus dilation = water-lines, glows, halos.
- Recursive branching with PIL lines = bare trees; rim-light a mask by shifting it.
- Older: raymarched heightfields (~30 s), SVG emitted from Python, FS dither for
  photographic feel, `--palette a,b` on render.py to restrict colours.

## Running threads
- "Roughness" (11-20) could return: Julia sets, ferns/L-systems, river deltas, frost,
  snowflakes, Brownian paths, a Koch-snowflake winter.
- Places with lots in them: a harbour, a market, a library wall, a greenhouse, a
  workshop bench, a city section drawing, a reef, a night train's windows.
- Charts and plates as art: star charts, tide tables, botanical and anatomical plates.
- Older threads: "hard edges" (09-13), Dante / stelle (09-14).
- Season: late November, northern-hemisphere assumption (bare trees, early dark). Advent
  and the winter solstice are coming — light in darkness is a natural December thread.

## Avoid / learned the hard way
- Sparse, poster-minimal compositions — the owner said so directly (11-20).
- Hand-drawn animals under ~50px turn to blobs (11-20 woodpecker). Make them bigger, or
  silhouettes, or give them a plain contrasting patch behind.
- Hidden motifs under ~60px or with thick outlines stop being recognisable (11-20 knot-hole).
- Photographic sources: large flats must be pure palette colours before dithering (09-13).
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Draw stacked forms far-to-near / bottom-up so overlaps are right.
- Yellow stipple over green goes garish fast; use it sparingly on vegetation.
- Text: 12px bold for captions is safe in preview; 8–9px (chart labels) is a gamble.

## Recently used (last ~14 days; don't repeat too soon)
- 2026-11-20 — thread: Mandelbrot's sentence. Styles: engraved cloudscape + patchwork
  fields; voxel mountain survey plate; sea chart with cartouche; Worley-bark close-up at
  sunset; lightning over harbour town. Subjects: clouds/sunrise/village, alpine lake,
  island map, tree trunk/owl/woodpecker, storm/lighthouse/boats. Caption band on all five.
- Tomorrow: avoid landscapes-with-sun (three of today's five had a sun disc), avoid
  caption bands, try interiors, figures, objects, pattern, or typography with ornament.
- (09-13/09-14 pieces are long out of the two-week window.)
