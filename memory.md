# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally.
- **Standing instruction, 11-13 (their words, roughly):** "you've gone a few levels too
  minimal… I only suggested a restricted palette as an occasional thing… I'd like to see you
  express yourself with much more detail!!" So: full six-colour palette is the default;
  a restricted palette is an occasional treat (say one piece a week), not a rule. Dense,
  drawn, storytelling detail in every piece. The 09-13/09-14 work is the "too minimal" bar.
- Feedback is rare and arrives appended to the daily prompt. I am my own critic otherwise.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Unverified on hardware: 1-px hairlines and 9–12 px text. sensors.jsonl and
  feedback.jsonl are still empty — the device may not be wired up yet.
- Refresh 15–30 s with flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner if a chance comes.

## Taste I'm developing (mine — revise freely)
- Think illustrated book, sea chart, engineer's plate, poster: pictures you can *read* for
  a minute. Things inside things: a room in every window, a tree for every tree.
- One colour still leads each piece (11-13: white/yellow quilt room, white chart, blue sea
  and sky, blue stone, black night) — detail goes on top of a clear big structure, so it
  reads at arm's length *and* rewards the nose-to-glass look.
- Tone comes from drawn marks: line screens (thickness varying with a tone field), hatch,
  cross-hatch, dot grids, concentric rings for lamplight. Bayer speckle only for real
  gradients, never as shading on top of a pattern (reads as dirt).
- A 1-px keyline (black on light, white on dark) round every small object makes it pop.
- Night: ~85% black, light as hairlines and dots. Rigging/stars/reflections suit it.
- A day has one seed and five readings, plus a small recurring motif (09-14 a star; 11-13 a
  light). Tiny figures doing something give story: keep using them, more than before.
- Words in the picture are welcome (labels, a line of verse, a title block) if legible.

## Working methods that are proven
- **`scripts/kit.py`** (copy also in gallery/2026-11-13/src): Canvas of palette indices;
  Layer = supersampled 1-bit mask in 400×600 user coords (poly, line, rect, ellipse, ring,
  text), stamped with `put(colour, pattern)`. Patterns: hatch, cross, dots, tone (Bayer),
  checker, speckle; helpers grow(), depth() (distance inside a mask → coast-lines, rims),
  bez, smooth (Catmull-Rom), arc, star. Generators end with `c.save()` → $OUT_RAW; render
  with `--dither none`. Output is palette-pure by construction. Import with
  `sys.path.insert(0, 'scripts')` or copy kit.py beside the generator.
- `sprite(parts, x, y, s)` pattern (see 11-13 counterpane): list of (colour, draw-fn),
  union gets a keyline, then colours stamped. Good for toys, figures, boats.
- Small text: ≤13 px is drawn 1:1 with mono hinting — use fonts `lib-i`/`lib`/`lib-b`
  (Liberation Serif) at 12 px, `dserif` at 9 px for numerals. Bigger text: `serif-b`,
  `serif-bi` supersampled. Rotated small text is illegible — don't.
- Labels on busy ground: `halo=WH, hw=2` on plain paper; solid bordered tags over a line
  screen. Reserve label areas (grown mask) *before* scattering trees etc.
- Scatter with an occupancy grid, sort by y, then draw — overlaps come out right.
- Don't use cairosvg for multi-colour work: anti-aliased edges quantise to a third colour
  (blue|yellow → green fringe). Fine for two-colour pieces only.
- Raymarched heightfields in numpy remain cheap (≈30 s); do the screen in the generator.
- Environment: use `python` (3.11). If PIL import fails:
  `python -m pip install --force-reinstall pillow numpy cairosvg`.
- Preview while working: save, upscale 2× NEAREST, look. Budget ~2 looks per piece.

## Running threads
- Stevenson (11-13) has more in it: Kidnapped's map of the flight in the heather, Jekyll's
  door, the Travels with a Donkey route, Vailima in Samoa, "From a Railway Carriage".
- "Hard edges" (09-13) and Dante (09-14) could return — now with detail.
- Cutaways and sections (lighthouse worked): a ship's hull, a clock, a beehive, a tenement.
- Charts: tide tables, star charts of the actual night, old city plans.
- 3D: a lit room, a staircase, a glass object — not done since 09-14; due an outing.
- Sky events to watch: Leonids peak 11-17/18; first-quarter moon 11-17.

## Avoid / learned the hard way
- Too little: flat two-colour posters with one idea. That's what the owner pushed back on.
- Too much of one mark: 520 trees made a green blob; 330 with gaps read as woods.
- Vignettes under ~35 px wide (lighthouse rooms) are at the limit; prefer fewer, larger.
- Silhouettes under ~40 px need a keyline or doubling. CA cells ≥10 px.
- Photographic sources: flats must be pure palette before dithering.
- Draw stacked forms bottom-up; draw glows *before* the objects that sit in them.

## Recently used (last ~14 days; don't repeat too soon)
- 11-13 styles: picture-book interior with patchwork; antique sea chart; engineering
  section + line-engraved sky + hanga sea; flat poster street elevation; night marine with
  hairline rigging and star field.
- 11-13 subjects: child in bed / toy soldiers; treasure map; lighthouse cutaway; Georgian
  terrace with lamplighter; schooner at anchor, Leo, crescent moon.
- 11-13 was all full-palette. (09-13/09-14 are well outside the two-week window.)
