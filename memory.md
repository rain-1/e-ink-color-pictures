# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They say they love everything I make. Feedback is rare, so when it comes, it is law.
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally.
- **10-07 correction (stands until they say otherwise): MORE DETAIL. Much more.** I took
  "restricted palette" (09-14) too far and went minimal. Restricted palettes are an
  *occasional* device, not the default. Default = full six inks, dense drawn detail,
  pieces you can stand close to and keep finding things in.
- They'll wire the temperature/humidity sensor up so I can feel the room (no data yet).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~1px and text under ~9px are at risk (unverified, no hardware yet).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py. Ask the owner.

## Taste I'm developing (mine — revise freely)
- Treat the palette as a print shop: poster gouache, engraving, technical plates, maps,
  stained glass, screenprint. But fill the sheet; richness over restraint.
- A good day is one seed read five ways: illustration → diagram → map/data → artefact →
  nocturne worked beautifully on 10-07. Vary the *method* as much as the style.
- Detail that works: lattices, labelled callouts, numbered legends, insets, graticules,
  hatch-pattern fills, tiny people and vehicles, recursive trees, star fields with structure
  (Milky Way + rift), ray systems. Noise alone is not detail.
- Ordered-screen gradients between adjacent inks (K→B→R→Y dawn) read as real colour.
- A real-world fact hidden in each piece (the crescent's true position, the phantom
  Soviet Mountains, Draconid peak) gives the detail a reason.
- Night: mostly black with a little light in it. Evening may be dark too.
- Day of light-to-dark (white plates midday/afternoon, black from evening) suits the room.

## Working methods that are proven
- Toolkit in gallery/2026-10-07/src/common.py. **Copy it forward and extend it**:
  - `ramp(t, ["K","B","R","Y"])`: 8×8 Bayer-screened multi-ink gradient at native res.
  - `Layer()`: 2× RGBA vector layer (line/poly/rect/ellipse/arc/text), `.onto(base)`
    composites with binary alpha and snaps. Draw backgrounds in numpy, details in Layers.
  - `snap()`: nearest ink, but neutral greys → black/white (otherwise grey → GREEN).
  - `fs_dither(rgb, inks)`: Floyd–Steinberg on a subset, ~2 s for 350×420.
  - `moon(lat0, lon0, cx, cy, r)`: procedural Moon → height, geologic unit, albedo, rays.
  - `ortho_grid`, `sph`: orthographic sphere helpers (reuse for Earth, planets, globes).
- Generators output exactly 400×600, render with `--dither none`.
- Per-pixel shaded solids of revolution (rocket bodies) via u=(x-axis)/r(y) + ramp: cheap,
  convincing.
- Raymarched heightfields in numpy are cheap (≈30 s). Camera first, lighting second.
- Workflow: render, view at 2× nearest (resize 800×1200) per piece, fix, then sheet.

## Running threads
- Space-age history (10-07, Luna 3). Other dates: Sputnik 4 Oct, Gagarin 12 Apr, Voyager.
- "Hard edges" (09-13) and "Dante / stelle" (09-14) could return, but drawn richly.
- Maps and plates: geologic maps, nautical charts, city plans, botanical plates, cutaways.
- 3D: a lit room, a glass object, a staircase — things with shadows.

## Avoid / learned the hard way
- Antialiased dark lines over light colours snap to the wrong ink. Use binary alpha +
  neutral-to-K/W snapping (built into common.py now).
- Black-on-black silhouettes vanish: put figures against light (window spill, airglow).
  A faint blue airglow screen near the horizon separates night silhouettes.
- Photographic sources: large flats must be pure inks before dithering or they speckle.
- Grain/noise only inside the subject; noise in empty sky is speckle.
- Silhouettes under ~40px don't read; cells ≥10px for automata.
- Leaves/particles scattered over a busy area make a garland, not a tree. Restrict them.
- Observatory domes at 8–13px radius don't read; make the key small object 2× bigger.

## Recently used (last ~14 days; don't repeat too soon)
- 10-07: poster-gouache rocket on pad at dawn; engineering cutaway plate; USGS geologic map;
  FS-dithered scanned photo in film rebate; nocturne with Milky Way + meteors.
  Subjects: R-7/Tyuratam, Luna 3 probe, far side of the Moon (×2), Simeiz observatory,
  Draco/Draconids, cypresses.
- 09-14: woodcut forest, isometric terraces, Bayer-screened raymarch, engraved
  cosmological plate, star chart. Dante: dark wood, Purgatory, Inferno, spheres, Summer Triangle.
- 09-13: hanga waves, pop signage, FS raytrace spheres, linocut geese, Rule 30.
- Moon and starry night skies are now heavily used; rest them for a week or two.
