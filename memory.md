# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback will be rare; I am my own critic.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally (spheres 09-13, Inferno funnel 09-14).
- **10-03 correction from them:** I'd gone "a few levels too minimal". Restricted palettes
  were meant as an *occasional* thing, not the rule. They want MUCH MORE DETAIL — express
  myself fully. Default now: all six inks, richly drawn scenes, many small parts. A
  restricted palette is fine maybe once a week as a deliberate change of pace.
- They'll wire the temperature/humidity sensor up so I can feel the room (sensors.jsonl
  still empty as of 10-03).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- The real panel is duller than the ideal palette: white is paper-grey, green olive-ish,
  blue deep. Still unverified on hardware.
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.
- Runs aren't daily in practice: 09-13, 09-14, then 10-03. Don't assume yesterday happened.

## Taste I'm developing (mine — revise freely)
- Detail is the point. Scenes with *things* in them: instruments, machines, buildings,
  people, weather, labels, rivets, wood grain, wires. A piece should reward a second look.
- Still keep one colour in charge of each piece (coverage ~40–60%) so it reads at a glance;
  the detail lives inside that.
- Vary the *kind* of picture across the day: diagram, top-down plan, landscape, still life,
  long-exposure abstraction. 10-03 did that well.
- Night should be mostly black with a little light in it (10-03 night: 86% black).
- A day should have a thread, one seed read five ways. Small text labels (titles, dates,
  captions) make a piece feel like an object. Keep them ≥6px tall.
- Noise is not detail. Grain, rain and furrows should be sparse and deliberate.

## Working methods that are proven
- **gallery/2026-10-03/src/ink.py**: Canvas drawn at 2x; `mix(c1,c2,t)` / `ramp([...],t)`
  give Bayer-screened tone fields between inks; `paste_mask(arr, mask)` for numpy-shaped
  fills; save() snaps each 2x2 block by majority (ties → darker ink). Render with
  `--dither none`. Copy it into each new day's src/ and improve it.
- In ink.py: lines must be width ≥1.0 or they vanish on contrasting grounds. Lines and
  outlines take solid tuples only, not screens.
- Metaball clouds/steam: f=Σr²/d², mask f>2, shade with tanh-saturated density sampled
  toward the light. Raw density gives holes.
- `place(x,y,angle)` local-coordinate transforms make it easy to draw rotated objects
  (instruments, players) in top-down plans.
- Raymarched heightfields in numpy are cheap (≈30 s). Camera first, lighting second, fog last.
- Floyd–Steinberg only when I want a photographic feel.

## Running threads / ideas
- Music as image: Reich (done 10-03). Others could get the same treatment: Satie, Cage,
  Glass, Riley's In C, a gamelan, Bach's canons.
- 3D: a lit room, a glass object, a staircase. Things with shadows. Not since 09-14.
- Charts and plates: star charts, tide tables, technical drawings, but drawn *richly*.
- Sky: Saturn at opposition 4 Oct 2026; Moon occults Mars 5 Oct and Jupiter 6 Oct
  (pre-dawn). Hunter's Moon later in October; Draconids ~8 Oct.

## Avoid / learned the hard way
- Being too minimal (owner, 10-03). If a piece could be described in five words, add more.
- Large flats must be pure ink colours before any dithering, or they speckle (09-13).
- Silhouettes under ~40px don't read; tiny top-down figures need a bright shirt + dark head.
- Cellular automata / pixel patterns: cells ≥10px or it's static (09-13).
- Draw stacked forms bottom-up; draw "behind" layers first (10-03: far truss, train,
  then near truss).
- Unicode ♯/▶ glyphs: DejaVuSans has ▶■●, DejaVuSans-Bold lacks ♯. Check glyphs.

## Recently used (last ~14 days; don't repeat too soon)
- styles 10-03: phase-wheel diagram, top-down stage plan, pastoral railway landscape,
  interior still life at a window, long-exposure string-art strobe.
- subjects 10-03: Piano Phase/two grands, 18-musician stage, streamliner on truss bridge,
  reel-to-reel + rainy SF dusk, swinging mics + speakers + Saturn.
- older (09-13/14, now stale but recent-ish): woodcut forest, terraced mountain, raymarched
  funnel, cosmological plate, star chart, hanga waves, pop numeral, raytraced spheres,
  geese, Rule 30.
