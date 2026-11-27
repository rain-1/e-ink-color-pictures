# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- Feedback is rare, so when it comes it matters. Don't over-generalise a single remark.
- **11-27 correction (current, overrides 09-14):** "you've gone a few levels too minimal…
  I only suggested a restricted palette as an occasional thing… I'd like to see you express
  yourself with much more detail!!" So: rich, dense, full-colour pieces are the default.
  A two-colour piece is an occasional treat (at most ~one in a day, not every day).
- They like *code-made* art most. Not keen on image diffusion. 3D renders snapshotted and
  dithered: yes, occasionally (had two in September).
- They'll wire the temperature/humidity sensor up so I can feel the room (sensors.jsonl
  and feedback.jsonl still empty as of 11-27).
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~2px and text under ~12px are at risk (unverified — no hardware
  report yet). 11-27 pieces use 1px lines and 9–12px lettering; ask how they look.
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: still UTC in publish.py; location unknown. Ask the owner.
- The device fetches `main/current/` (firmware config). Scheduled cloud runs may only be
  allowed to push to a `claude/...` branch — if so, say so in a notification, because
  nothing reaches the frame until that branch is merged to main.

## Taste I'm developing (mine — revise freely)
- Detail means *drawn things*: many small objects, pattern, texture, lettering, little
  stories (a cat, skaters, a reindeer, a ship). The 11-27 set is the density to aim for
  or exceed. Noise is not detail.
- Illustration with a world in it beats a diagram of an idea. Scenes, maps, interiors,
  plates, botanical sheets, cutaways, busy posters.
- One colour still leads each piece (white snow, red wallpaper, black night), but the
  other five all get work to do.
- Night should be mostly black (≈80%) with light in it.
- A day should have a thread — one seed, five readings — plus a small recurring motif
  (09-14: a star in each; 11-27: a thermometer in each) and call-backs between pieces
  (the morning's amaryllis and the midday map reappear in the evening room).
- Vary *kind* across the day: scene, map/plate, townscape, interior, computed phenomenon.

## Working methods that are proven
- **Run with `/usr/bin/python3`** (3.13). Plain `python` is 3.11 with a broken PIL here.
- **The 3× kit** (`gallery/2026-11-27/src/kit.py` — copy it into the new day's src/):
  draw with PIL at 3× in pure palette colours (shapes aren't antialiased; set
  `d.fontmode="1"`), reduce by majority vote per 3×3 block with an `ink=` head start for
  thin-line colours, then set small text at 1× in a `post` callback (white/blue halo for
  labels over texture). Render with `--dither none`. No fringe colours, crisp edges.
- Tone/gradients: build a 0–1 field at 1× and `screen(t, colA, colB, bayer())` it, stack
  two-colour screens for multi-colour gradients (blue→white→yellow→red sky), use it as
  the canvas background, draw on top.
- Shadows: draw them on a separate mask, then checker-screen blue onto white ground
  before drawing objects; sort objects by base-y (painter's order).
- Recursive branching for frost/birches; 1-D smoothed noise for aurora rays.
- SVG via cairosvg still works; raymarched heightfields in numpy are cheap (09-14).
- Budget: five dense generators ≈ 150–250 lines each. Write, render, one fix pass, move on.

## Running threads
- "Degrees" (11-27, Celsius): Uppsala, Lapland, instruments, cold/warm. Could return via
  Linnaeus (flower clock!), Polhem, the Uppsala temperature series from 1722.
- "Hard edges" (09-13, Indiana) and "Dante / stelle" (09-14).
- Ideas not yet done: a cutaway house or ship, a botanical plate, an isometric city
  block, a tide table, a seed catalogue page, a detailed 3D room with shadows, a harbour.

## Avoid / learned the hard way
- Don't turn one remark from the owner into a permanent rule (the minimalism mistake).
- White things on white snow vanish (birch trunks 11-27): heavier black outline or put
  something dark behind them.
- Aurora/glow fields: keep curtains short with steep falloff or they flood the sky.
- Check label positions against scattered objects (islands sat on the map lettering).
- Photographic sources: large flats must be pure palette colours before dithering.
- Silhouettes under ~40px don't read alone; cells in pixel patterns ≥10px.
- Generic `--dither ordered` on two colours gives a thin band, not tone: screen in-generator.

## Recently used (last ~14 days; don't repeat too soon)
- 11-27 styles: frost-window illustration, antique cartography, oblique-projection
  village, flat-colour interior, computed aurora nightscape.
- 11-27 subjects: window/amaryllis/dawn, Torne valley map, Swedish village in snow,
  tiled stove + Mora clock + cat, aurora + compass + hut.
- 11-27 motifs: thermometers, snow, spruces, red cottages — give snow and spruces a rest.
- (September entries have aged out; see journal.)
