# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare but it is worth a lot when
  it comes; I am otherwise my own critic.
- They like *code-made* art most. Not keen on image diffusion, curious if I ever have
  a real reason. 3D renders snapshotted and dithered: yes, occasionally.
- **09-21, corrected me directly**: the restricted palette was only ever meant as an
  occasional thing, and I had taken it as licence to be minimal in *detail* too. They
  want me to express myself with much more detail. That request stands until they say
  otherwise. Two-colour minimalism is now the exception, not the default.
- They'll wire the temperature/humidity sensor up so I can feel the room. Still empty.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish,
  blue deep. Big flat shapes and contrast survive; lines under ~1.5px and text under
  ~10px are at risk (still unverified — no hardware yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## The one hard rule of this palette (learned 09-21, cost me an hour)
There are no greys and no tints. Every soft pixel a renderer produces is a blend of
two inks, and plain nearest-colour quantising gets it *wrong*: mid-grey resolves to
blue, black-over-yellow resolves to green. So:
- `src/plate.py:snap(img, names)` unmixes instead. For each pixel it finds the pair of
  palette colours and the mix fraction that best explain it, then rounds to whichever
  of the two it is mostly made of. Black rules stay black over a yellow flat.
- Generators should call `snap` themselves and hand render.py a finished 400×600 PNG,
  then render with `--dither none`. Pass only the colours the drawing actually uses.
- PIL/ImageDraw does not antialias shapes but *does* antialias truetype text, so a
  numpy piece still needs one `snap` pass at the end.
- Copy `plate.py` forward into each new day's `src/`. It is worth keeping.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop, not a screen. Riso, screenprint, woodblock,
  linocut, engraving, poster, cut-paper, stained glass, star charts, technical plates.
- **Detail should be drawn detail**: hatching, contour lines, ticks, leaders, labels,
  legends, tiny figures, ornament. Noise is not detail, and neither is a gradient.
- One colour in charge, three or four others doing jobs. Not two. Not six.
- Tone is made by line *spacing*, never by grey — after `snap` a hatch line is either
  fully black or gone.
- Night should be 85%+ black with a little light in it.
- A day should have a thread — one seed, five readings of it — and each slot should
  get a different *trade*: a patent plate, a chart, an illustration, a section, a
  nocturne. That variety carried 09-21 more than any single piece did.
- A tiny figure gives scale and story. Use sparingly; it's a trick.
- Put a white backing rect behind every label that sits over line work.

## What code is good at, and what it isn't
- **Good**: systems. Coastlines, contours, galleries, mechanisms, gear trains, rhumb
  lines, compass roses, scale bars, sections, strata, ruled skies, screened light.
- **Bad**: bodies. I tried twice on 09-21 to generate upright hybrid animal figures
  from parameters (ear, snout, pelt, stance) and both times they read as boxes —
  proportion is the problem and hatching cannot rescue a bad silhouette. Threw it out,
  drew a chart of the same island instead, and the chart was better in a fifth of the
  time. If a piece needs a convincing figure, find the diagram that implies it.

## Working methods that are proven
- Python emitting SVG (`plate.Plate`) for anything with geometry; render at 2× inside
  the generator, LANCZOS down, then `snap`.
- `rule_field(..., taper=f)` — ruled lines whose width falls to zero across the field.
  This is how skies, water and shadow get made. `contour_shade` rounds a solid.
- Numpy tone field + an 8×8 Bayer screen *inside* the generator, for light that has to
  be continuous. Clamp the field to zero below ~0.08 first or faint tone speckles
  isolated dots across the whole sky.
- Raymarched heightfields in numpy are cheap (≈30 s at 400×600). Camera first.
- Floyd–Steinberg only for a halftone/photographic feel (09-13 spheres).

## Running threads
- "Hard edges" (09-13), "Dante / stelle" (09-14), "Wells at 160" (09-21).
- Wells has plenty left: The Invisible Man, The Sleeper Wakes, The Country of the
  Blind, The Shape of Things to Come, Little Wars, the Outline of History.
- Charts and plates generally: tide tables, weather maps, anatomical sheets, orreries,
  railway diagrams, seed catalogues.
- Not yet tried: a plate built entirely of line with no flat colour anywhere.

## Avoid / learned the hard way
- Never hatch black over a colour flat and hope; use `snap` or keep ink on white.
- Photographic sources: large flats must be pure palette colours before dithering.
- Silhouettes under ~40px don't read; a black silhouette over a black ground reads
  even worse (the crab, 09-21 — it should have stood against the lit water).
- Cellular automata / pixel patterns: cells ≥10px or it's static.
- Generic ordered dither on a two-colour palette gives a thin band of texture, not
  tone. Do the screen in the generator.
- Draw stacked forms bottom-up so upper tiers overlap lower ones.
- A sunburst of white rays turns an engraving into a film poster. Six shafts, thin.

## Recently used (last ~14 days; don't repeat too soon)
- styles 09-13: hanga waves, pop signage, FS-dithered raytrace, linocut bands, 1-D automaton.
- styles 09-14: woodcut forest, isometric terraces, Bayer-screened raymarch, engraved
  cosmological plate, star chart.
- styles 09-21: patent/mechanical plate, hydrographic chart, full-bleed ink
  illustration, vertical section diagram, screened nocturne.
- subjects 09-13: sunrise+boat, numeral 13, spheres, geese, Rule 30.
- subjects 09-14: dark wood, Purgatory, Inferno funnel, Ptolemaic spheres, Summer Triangle.
- subjects 09-21: the Time Machine, Noble's Isle, fighting-machines, the lunar crust,
  the terminal beach.
- palettes 09-21: K/P/R/Y/B, K/P/R/Y/G, K/P/R/Y, K/P/Y/B, K/P/R. Green and blue have
  each led once now; untouched as a *lead*: yellow alone, red+green, blue+yellow.
