# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare, so when it comes it counts.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted
  and dithered: yes, occasionally.
- **Standing request (10-14): much more detail, and use the full palette.** Restricted
  palettes were only ever meant as an occasional thing, and I over-applied them in
  September ("a few levels too minimal"). Default now: dense, drawn, all six colours.
  A two-colour piece is a rare exception and needs a reason.
- They'll wire the temperature/humidity sensor up so I can feel the room (still empty).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal: white paper-grey, green olive, blue deep.
- Lines ≥1px in solid palette colour drawn at native res look crisp in preview. Text
  ≥12px with `fontmode="1"` is legible (unverified on hardware).
- Refresh 15–30 s with flashing, five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste (mine, revise freely)
- Detail is the point: many individually placed, *drawn* things (trees, figures, shields,
  fronds, stones, stars) at a size that still reads, 3–8px elements en masse, plus a few
  big anchors (a figure, a building, a banner) so it reads at four inches.
- Print-shop and craft vocabularies still guide me: maps, battle plates, embroidery,
  engraving, woodblock, stained glass, star charts, technical plates. Now in full colour.
- Still one colour *in charge* (green field, white linen, black night), but the other
  five all get a job.
- Night stays mostly black with light in it.
- A day should have a thread: one seed, five readings. Two linked seeds work too
  (10-14: Hastings + Pooh, same county, same date).
- A tiny figure gives scale and story.

## Working methods that are proven
- **Native-res palette drawing** (PIL at 400×600, palette RGB constants, `d.fontmode="1"`,
  render `--dither none`). Best for maps, plates and dense drawn detail (10-14 #2, #3, #5).
- **Painterly 2× source + FS dither** (`--dither fs`): continuous colour at 800×1200 with
  drawn strokes on top. FS mixes orange, sky blue and dusk well (10-14 #1).
- **Stitch/fill engine** (10-14 #4, src/4_evening_hic_harold.py): numpy masks, each
  filled with angled thread lines and linen gaps, couching bars, ring grids for mail, and
  an edge outline. Reusable for any textile look (embroidery, quilt, tapestry, sampler).
  - Mask drawing needs an ImageDraw proxy that defaults fill=255, or shapes are empty.
  - Guard `% gap` maths when gap == 1 (it silently draws nothing).
- Emit SVG from Python for clean geometry; render.py does SVG at 2× and downsamples.
- Raymarched heightfields in numpy are cheap (≈30 s). Camera first, lighting second.
- For 2-colour tone: Bayer screen inside the generator on a 0–1 value, `--dither none`.
- Install deps with `python -m pip install -r requirements.txt` (bare `pip` targets a
  different interpreter here).

## Running threads / ideas banked
- Hastings and the Tapestry (on show in London until July 2027): more scenes are
  possible (Halley's comet in April, the ships at Pevensey, the feast).
- The Pooh centenary runs all year; National Pooh Day is 18 January (Milne's birthday).
- 3D: a lit room, a glass object, a staircase, a single chair, things with shadows.
- Charts and plates: tide tables, star charts, old technical drawings, now in colour.
- Textile engine: try a quilt, a sampler, or a Persian carpet.

## Avoid / learned the hard way
- Photographic sources: large flats must be pure palette before dithering or they speckle.
- Silhouettes under ~40px don't read alone; small figures work *en masse* or with a
  bright accent (a balloon, a banner).
- Cellular automata: cells ≥10px or it's static.
- Draw stacked forms bottom-up / back-to-front.
- FS on dark brown-reds produces green speckle; push heath and earth toward black or
  red rather than mid-brown.
- Parabola arcs for projectiles: use a quadratic Bezier with an explicit control point.

## Recently used (last ~14 days; don't repeat too soon)
- 10-14 styles: FS painterly landscape, hand-tinted map, bird's-eye battle plate,
  stitched tapestry panel, night engraving of architecture.
- 10-14 subjects: Ashdown Forest dawn, Pooh-walk map, Senlac/Hastings, Harold's death,
  Battle Abbey gatehouse + Halley's comet.
- (09-13 / 09-14 are now older than two weeks: free again, but don't drift back to minimal.)
