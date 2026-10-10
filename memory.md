# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare and it MATTERS. Read it as written.
- They like *code-made* art most. Not keen on image diffusion. 3D renders: yes.
- **10-10 correction from them, the standing instruction:** I'd gone "a few levels too
  minimal". The restricted palette was only an *occasional* suggestion. They want me to
  "express myself with much more detail!!" So the default is full palette when the subject
  wants it, dense and drawn, with lots of placed things. Restricted palette is now a
  sometimes-tool (maybe one piece a day at most), and never an excuse for sparse.
- They'll wire the temperature/humidity sensor up so I can feel the room (nothing yet).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- The real panel is duller than the ideal palette: white is paper-grey, green olive-ish,
  blue deep. Lines under ~2px and text under ~12px may be at risk. That's unverified (no
  hardware feedback yet), and the owner prefers detail, so I accept the risk.
- Refresh 15–30 s with visible flashing, five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine; revise freely)
- Detail first: a piece should reward a second and third look. Hundreds of placed things
  (trees, roofs, windows, strokes, raindrops). Build scenes in layers: sky, far, mid,
  near, figure, weather.
- Still keep one colour (or a value, e.g. black at night) clearly in charge so it reads at
  four inches. Detail sits on top of a strong big-shape composition, not instead of one.
- Print-shop vocabulary still useful: engraving, woodcut, riso, poster, plate. But also
  illustration, scene-painting, drawing.
- Night should be mostly black (≥80%) with a little light in it.
- A day should have a thread, one seed and five readings of it, plus a small recurring
  motif (09-14 a star, 10-10 a tiny Walking Man).
- Real-world grounding (a place, a photo, an object, a date) makes pieces richer than
  pure abstraction.

## Working methods that are proven
- Python/PIL generators writing to $OUT_RAW, rendered with `--dither none`.
- Shared helpers per day in `src/common.py`. 10-10's has `ramp(t, stops)` (8×8 Bayer
  between palette stops), `tone_poly`, `polymask`, `paste_arr`, `fbm` value noise,
  `scribble`, and `walker`. Copy it forward rather than rewriting.
- Tone = in-generator Bayer between two adjacent palette colours (K/Wh greys, Y/K ochre,
  B/Wh sky). Then draw crisp detail over the top.
- SDF raymarch in numpy (≈8 s) → depth/normal/light → steer strokes along the
  perpendicular to the screen normal. Draw black in shadow, white in light, plus repeated
  jittered strokes on the silhouette and depth edges. Excellent (10-10 bust).
- Line engraving: per-region hatch angle, ink where |phase| < tone·spacing/2. Put a paper
  halo around figures.
- Heightfield raymarch (≈30 s) for landscapes (09-14). Camera first, light second, fog last.
- Text: real TTFs exist (DejaVu Serif Bold, Liberation Serif Italic, DejaVu Sans Mono in
  /usr/share/fonts). ALWAYS `d.fontmode = "1"` or the antialiasing fringes go green.
- Preview: upscale ×2 NEAREST into scratchpad and look. One fix pass per piece.
- pip install needs `python -m pip install pillow numpy cairosvg scipy` (pip ≠ python).

## Running threads
- Giacometti (10-10). Could return to the SDF-plus-strokes method for other sitters.
- "Hard edges" (09-13, Robert Indiana) and "Dante / stelle" (09-14).
- 3D: a lit room, a glass object, a staircase, things with shadows. SDF stroke drawing of
  still-lifes (bottles à la Morandi?).
- Detailed scenes: city streets, harbours, markets, interiors. Charts and plates.

## Avoid / learned the hard way
- Being too minimal (the 10-10 correction). Sparse pieces disappoint.
- Photographic / raytraced sources: large flats must be pure palette before dithering.
- Silhouettes under ~30px don't read unless set against a plain ground.
- Midpoint/fbm shading on mountains can make dark "holes". Keep noise amplitude modest.
- Forest of thousands of tiny triangles reads as texture. Fine as midground, needs a
  clear foreground in front of it.
- Bayer-screened mid-greys over a whole room go muddy (10-10 studio). Push values apart:
  dark ceiling, light back wall.
- Draw floor debris before furniture and figures, not after.
- Night: watch blue creep (rain, window outlines, sky). Pare back until black dominates.

## Recently used (last ~14 days; don't repeat too soon)
- 10-10: styles were screened landscape, perspective interior, line-engraved stamp,
  SDF + stroke portrait, and a night street in rain. Subjects were Val Bregaglia, the Paris
  studio, the Walking Man stamp/envelope, a bust (Diego), and rue d'Alésia.
- 09-14 (now >2 weeks old, free again): woodcut forest, Purgatory terraces, Inferno
  raymarch, Ptolemaic plate, star chart.
- 09-13 (free again): hanga waves, pop numeral, sphere raytrace, linocut geese, Rule 30.
