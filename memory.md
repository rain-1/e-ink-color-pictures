# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare, so when it comes it's law.
- They like *code-made* art most. Not keen on image diffusion. 3D renders: yes, they like them.
- **10-01 correction (standing):** I had gone "a few levels too minimal". Restricted
  palettes were only ever meant as an *occasional* thing. They want me to express myself
  with **much more detail**. Default is now FULL palette and DENSE, rich pieces. Restrict a
  palette only now and then, when the idea really needs it (at most one piece a day).
- They'll wire the temperature/humidity sensor up so I can feel the room (sensors.jsonl
  still empty as of 10-01).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~2px and text under ~10px are at risk (still unverified, no hardware
  feedback yet). Detail is wanted anyway: lean on 1–2px drawn detail, keep labels ≥9px.
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine — revise freely)
- Richness: crowds of small figures, architecture with every tile and baluster, weather,
  reflections, labels, cartouches, insets, scale bars. A piece should reward a long look.
- One seed, five readings, a thread through the day. 10-01's was two eras of one road, and
  it worked well: two layers of time in one frame (the Kodama behind Hiroshige's bamboo).
- Vary the *method* across the day: woodblock, 3D render, data plate, map, poem/type...
- Treat the palette like a print shop (screenprint, woodblock, poster, chart), but use all
  six inks. One colour still leads each piece.
- Night is mostly black with lights in it (10-01's night map was 93% black, and that's right).
- Real data makes great detail: coastlines, timetables, star positions, tides.

## Working methods that are proven
- Python/PIL generators writing to $OUT_RAW, drawing directly in palette colours at 1x,
  `d.fontmode = "1"` (no antialiased text fringes), render with `--dither none`.
- Tone: an 8×8 Bayer screen inside the generator between two inks (see 2026-10-01/src/ukiyo.py:
  `blend()`, plus `traveller()` figures, `pine()`, `waves()`, vertical JP `cartouche()`).
  Reuse it, copy it forward and extend it.
- 3D: numpy raymarch (SDFs plus heightfield, ~3 s at half-res preview with SCALE=2, ~12 s full).
  Then **per-material ink ramps**: each material maps shade → its own 2–3 colours through
  the Bayer screen. This looks printed, not dithered. Classify materials by geometry
  (height, distance), not by an |y−h| tolerance, because hit tolerance grows with distance.
  Telephoto (FOV ~0.3) to make a far mountain loom. Overlay hand-drawn figures afterwards.
- Japanese fonts exist: /usr/share/fonts/opentype/ipafont-gothic/ipag.ttf.
- Natural Earth geojson: raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/
  (naciscdn is blocked). Clip and save a small json next to the source.
- `--palette a,b,c` on render.py still exists for the occasional restricted piece.

## Running threads
- Hiroshige's Tōkaidō (10-01 used Nihonbashi 1/53 and Shōno 46/53). Other stations would
  make a fine recurring series: Kambara night snow (winter!), Hakone, Mishima mist,
  Kyoto Sanjō bridge (the end).
- "Hard edges" (09-13), Dante (09-14). 3D: a lit room, glass, a staircase.
- Charts and plates: star charts, tide tables, train graphs, night maps.

## Avoid / learned the hard way
- Too minimal (the 09-14 style of 2–3 inks and sparse drawing) is NOT what they want as a default.
- 50% grey screens over big areas read as static. Keep screens light (<30%) or dark (>70%),
  or use a flat ink.
- Silhouettes under ~40px don't read alone, but crowds of 20–30px figures do read as a crowd.
- Raytraced sources: large flats should be pure inks, not FS-dithered (09-13).
- Cellular automata: cells ≥10px (09-13).
- Draw stacked forms bottom-up (09-14). Flood fills on clipped coastlines leak, so seed carefully.
- Check the direction logic on any reversed sequence (up vs down trains, 10-01).

## Recently used (last ~14 days; don't repeat too soon)
- 09-13: hanga waves, pop "13" sign, FS raytrace spheres, linocut geese, Rule 30.
- 09-14: woodcut dark wood, Purgatory terraces, raymarched Inferno funnel, Ptolemaic plate,
  star chart.
- 10-01: Hiroshige-style woodblock (Nihonbashi), raymarched train + Fuji poster, Marey train
  graph, woodblock rain (Shōno), night corridor map with real coastline.
- Subjects to rest until mid-October: Fuji, bullet trains, Japanese woodblock pastiche
  (unless continuing the Tōkaidō series deliberately), train diagrams.
