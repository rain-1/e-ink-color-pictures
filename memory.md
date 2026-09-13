# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. I believe them and I don't rely on it —
  it means feedback will be rare, so I have to be my own critic.
- They like *code-made* art most. They're not keen on image diffusion, though
  curious to see it if I ever have a real reason. 3D renders snapshotted and
  dithered: yes please, occasionally.
- They'll wire the temperature/humidity sensor up so I can feel the room.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours only: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green is
  olive-ish, blue is deep. Big flat shapes and strong contrast survive; thin
  lines under ~3px and fine gradients don't.
- Refresh is 15–30 s with visible flashing, so five changes a day, not more.
- Slots (local time): morning 06, midday 10, afternoon 14, evening 18, night 22.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop, not a screen. Riso, screenprint, woodblock,
  linocut, poster, cut-paper, stained glass, needlepoint, pixel art all fit.
- Night pieces should be mostly black or blue with a little light in them.
- Let one colour dominate a piece. Six colours evenly is noise.
- Ordered/Bayer dither reads as an intentional texture; Floyd–Steinberg reads
  as "photo" — use it when I want that, not by default.

## Running threads
- 2026-09-13 opened with "hard edges" (Robert Indiana's birthday). Could return to hard-edge / pop signage as a recurring family.
- Tiny numpy raytracer worked well; try other 3D subjects (glass, a room, a single chair).

## Avoid / learned the hard way
- Raytraced / photographic sources: make skies and large flats *pure* palette colours before dithering, or they speckle.
- Silhouettes under ~40px tall don't read. Double them.
- Cellular automata / pixel patterns: cells ≥10px or it's static.
- Timezone: still UTC in publish.py — set to the owner's real tz once known.

## Recently used (last ~14 days; don't repeat too soon)
- styles: hanga waves, pop signage, raytrace+FS dither, linocut bands, 1-D automaton (all 09-13)
- subjects: sunrise+boat, numeral 13, spheres still-life, geese/harvest sky, Rule 30 (all 09-13)
