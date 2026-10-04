# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare, so when it comes, take it seriously.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally.
- **10-04 correction (standing):** "you've gone a few levels too minimal... I only
  suggested a restricted palette as an occasional thing... express yourself with much more
  detail!!" So the default is now **full six colours and rich, dense, crafted detail**.
  A restricted palette is an occasional choice (maybe one piece a week), not the norm.
  Flat big-shape minimalism is out unless there's a strong reason.
- The 10-04 set (sun-face over Assisi, millefleur, Giotto fresco, simulated bonfire,
  moonlit chapel with larks) is the benchmark for the level of detail they want.
- They'll wire the temperature/humidity sensor up so I can feel the room.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Marks ≥2px and text ≥12–13px are my floor (still unverified on hardware).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine — revise freely)
- Detail = many small *drawn* things: houses with windows, each leaf, each bird, each
  stone, plants as specimens, figures built from parts. Noise is not detail.
- Rich traditions suit the frame: illuminated manuscripts, millefleur tapestry, early
  Italian fresco, travel posters, Persian/Mughal miniatures, Japanese woodblock,
  natural-history plates, folk art, stained glass, maps with vignettes.
- One colour still leads each piece (by coverage), but the other five work as accents.
- Night should be mostly black/blue with a little warm light in it (≥55% dark).
- A day should have a thread: one seed, five readings of it. A text with five verses
  or sections (a canticle, a poem, a calendar) gives each slot its own subject.
- Inscription bands, borders and selvedges frame dense pieces well and carry a line of
  text from the source.

## Working methods that are proven
- **Parallel agents:** write a shared helper module in gallery/DAY/src/common.py, then
  brief one agent per piece in detail (subject, style, lead colour, list of elements,
  "iterate 2–4 times, look at a 2× crop"). It took about 10 minutes and quality was high.
- Draw at 2× (800×1200) in pure palette colours with PIL. Do tonal areas with an 8×8 Bayer
  screen computed at 1× and upscaled.
- **Downsample by majority colour per 2×2 block (ties to the darker ink), not a box
  filter.** A box filter turns black+yellow and black+white edges into green speckle. Put
  this in common.py from day one. White text needs its own coverage mask after the snap.
- Bayer screens suit bounded objects (walls, foliage, sky rings, moon maria). On big
  open fields they read as speckle; use solid colour plus drawn marks there.
- Stepped concentric rings, each with one fixed tone, make a cleaner sky than a smooth
  gradient.
- Fire: a Doom-fire heat field with symmetric spread and per-column decay read from a
  noise field that rises with the heat gives tongues, not a fuzzy cone.
- Figures: build them from parts (robe, shoulders, head, cowl, sleeve). Rim-light the
  side that faces the light source. Tilt perched birds about 20° head-up.
- Raymarched heightfields in numpy are cheap (≈30 s). Get the camera first, then lighting, fog last.
- `--palette a,b,c` on render.py for an occasional restricted piece; do the screen inside
  the generator.

## Running threads
- Francis / Canticle (10-04). Sister Water and Sister Death weren't used: Water could
  carry another day.
- "Hard edges" (09-13), Dante / stelle (09-14).
- 3D: a lit room, a glass object, a staircase, things with shadows.
- Charts and plates with lots of vignettes, e.g. a decorated map or an almanac page.

## Avoid / learned the hard way
- Minimalism as a default (owner correction, 10-04).
- Large flats in raytraced sources must be pure palette before dithering (09-13).
- Silhouettes under ~40px don't read; plants need a radius of 20–35px (10-04).
- Cellular automata: cells ≥10px (09-13).
- Small faces: a full beard or big hair shape turns into a mask. Use a thin jaw and a brow band.
- Yellow subject on yellow ground disappears. Check figure/ground per element.
- Draw stacked forms bottom-up (09-14).

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, FS raytrace, linocut, 1-D automaton (09-13);
  woodcut forest, isometric terraces, Bayer raymarch, engraved plate, star chart (09-14);
  illuminated travel poster, millefleur tapestry, Giotto fresco, fire simulation,
  moonlit nocturne with spiral flock (10-04).
- subjects: sunrise+boat, numeral 13, spheres, geese, Rule 30 (09-13); dark wood,
  Purgatory, Inferno, Ptolemaic spheres, Summer Triangle (09-14); Assisi at dawn,
  meadow with animals, birds, bonfire with friars, chapel + moon + larks (10-04).
- motifs to rest: sun-faces, moons, birds in flocks (all three used heavily recently).
