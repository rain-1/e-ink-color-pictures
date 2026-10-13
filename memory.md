# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They rarely give feedback, so when they do it matters. I am mostly my own critic.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted
  and dithered: welcome occasionally.
- **10-13 correction from the owner:** I had gone "a few levels too minimal". Restricted
  palettes were only an *occasional* suggestion. They want me to "express myself with
  much more detail". So the default is now: **full palette, dense, richly drawn**.
  A restricted-palette piece is a once-in-a-while choice, at most one per day.
- They'll wire the temperature/humidity sensor up so I can feel the room (still empty
  as of 10-13).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal: white is paper-grey, green olive-ish, blue deep.
  Lines under ~1px and text under ~9px may not survive (unverified, no hardware yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine — revise freely)
- **Density is the default.** Fill the frame with drawn things: textures, patterns,
  labels, small figures, wires, laundry, stars, ornaments. Hundreds of elements, not ten.
  10-13 was the first day at this level and was the strongest set so far.
- Still one colour *in charge* per piece (a big field of it), with all six available
  as ink on top. Dense ≠ muddy: dominant ground + black linework keeps it legible.
- Print-shop and folk vocabularies suit the panel and reward detail: scrap collage,
  woodblock with grain, fileteado, screenprint, star charts, technical plates,
  stained glass, embroidery, map-making, Persian miniatures, Mexican papel picado,
  Indian textile blocks, Japanese hanga crowds. Lots still untried.
- Night should be mostly black (~85%), but *busy* black: lit windows, linework, stars.
- A day should have a thread (one seed, five readings), and a small recurring motif
  across the five (09-14: a star; 10-13: a kite).
- Drawn detail, not noise: hatching, ticks, labels, tiny figures, stitching, rivets.
- A tiny figure gives scale and story. Make it ≥30px tall if it matters.

## Working methods that are proven
- **10-13 pipeline (best so far):** a `common.py` beside the sources with a canvas
  class that draws at 3× in *pure palette colours* with PIL, then majority-downsamples
  to 400×600 (centre pixel breaks ties). Render with `--dither none`. Crisp, dense,
  never off-palette. Copy it from gallery/2026-10-13/src/common.py and extend.
- Write reusable "material" or "motif" functions (corrugated tin, planks, brick, cans,
  fabric, kite, scroll), then scatter them procedurally with a seeded RNG. Cheap detail.
- Python/PIL generators write to $OUT_RAW. SVG for hand-placed geometry.
- `--palette a,b,c` on render.py restricts quantisation (for the occasional limited piece).
  For two-colour tone, do an 8×8 Bayer screen in the generator (common.bayer()).
- Raymarched heightfields in numpy are cheap (≈30 s). Camera first, lighting second.
- Floyd–Steinberg only for a halftone/photographic feel.
- pip install into /usr/local python: `python -m pip install -r requirements.txt`
  (plain `pip` installs to a different interpreter in this container).

## Running threads
- "Hard edges" (09-13), "Dante / stelle" (09-14), "Juanito Laguna / Berni" (10-13).
- 3D: a lit room, a glass object, a staircase, a single chair, things with shadows.
- Untried ideas worth a day: a dense illustrated map; a crowded market scene; a
  botanical plate with every leaf veined; an embroidered sampler; a stained-glass
  window with leading; a busy isometric city block cut open; a tarot-card-style plate.

## Avoid / learned the hard way
- Minimalism as a habit. The owner pushed back on it (10-13). Check each piece: is
  there enough to look at for a minute?
- Photographic / raytraced sources: large flats must be pure palette colours before
  dithering or they speckle (09-13).
- Silhouettes under ~40px don't read; figures under ~20px vanish (09-13, 10-13).
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Generic ordered dither on a two-colour palette gives a band of texture, not tone (09-14).
- Draw stacked forms bottom-up / back-to-front so nearer things overlap (09-14, 10-13).
- Rows of houses need height ≥ row spacing or the background shows as stripes (10-13).
- Ornamental leaves on spirals: put them on the side *away* from the curl centre and
  sweep them back, else gear teeth (10-13).
- Tiny scenes inside small windows don't read. Fewer, bigger (10-13).

## Recently used (last ~14 days; don't repeat too soon)
- 10-13 styles: generated scrap collage, woodblock still life, kite-sky illustration,
  fileteado porteño, night linework villa.
- 10-13 subjects: shantytown at sunrise, tin cans, kites, carnation/scrolls, villa at
  night, Southern Cross. Motif: kite. Dominants: Y, R, B, K, K.
- Older (now outside two weeks, free to revisit): 09-13 hanga waves, pop numeral,
  raytraced spheres, linocut geese, Rule 30; 09-14 woodcut forest, Purgatory, Inferno
  raymarch, Ptolemaic plate, star chart.
- Avoid for a while: kites, tin/scrap collage, fileteado, Buenos Aires.
