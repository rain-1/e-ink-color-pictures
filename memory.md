# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- Feedback is rare and arrives as a note appended to the daily prompt. Read the prompt's
  last paragraph every day — it may have changed.
- **Standing brief (note seen 11-25):** I went "a few levels too minimal". Restricted
  palettes were only ever meant as an *occasional* thing. They want me to express myself
  with **much more detail**. Default is now: full palette, dense drawn detail, a picture
  you can stand close to and keep finding things in. A 2–3 colour piece is a rare
  exception (at most one in a day, and not every day), and even then it must be detailed.
- They like *code-made* art most. Not keen on image diffusion. 3D renders dithered: yes,
  occasionally.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Still no hardware confirmation of what fine detail survives (sensors.jsonl and
  feedback.jsonl are empty as of 11-25).
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: unknown, publishing with UTC. Location unknown too — so no local weather.
  Ask the owner if a channel ever appears.

## Taste I'm developing (mine — revise freely)
- Rich, not sparse. Think illustrated book plate, doll's house, map, poster, stage set —
  things with rooms, labels, furniture, patterns, small people. Many small decisions.
- Detail must be *drawn*: wallpaper repeats, brick, hatching, ticks, labels, objects on
  shelves, figures doing something. Noise is not detail.
- One colour still leads each piece (it's what makes it read at four inches), but the
  other five should all get work. Across the day, rotate the leader:
  11-25 was white/blue, multi, blue, red, black.
- A day has a thread — one seed, five readings — and a small recurring motif hidden in
  each (09-14: a star; 11-25: a mouse). The owner can hunt for it.
- Tell a story across the slots: establishing shot → interior → investigation → event →
  quiet night coda worked well.
- Night: mostly black + blue, a little white and one yellow light. Watch snow/sky fields —
  my first drafts come out too bright.
- Tie the night piece to the real sky when I can (moon phase, bright stars near it).

## Working methods that are proven
- Run everything with `python3.13` (plain `python` is 3.11 and lacks numpy/cairosvg).
- **Pixel-direct method (11-25, best so far):** PIL at 400×600, pure palette colours only,
  `d.fontmode = "1"` for crisp text, `--dither none`. Tone and texture come from pattern
  fills composited through numpy masks: 8×8 Bayer tint of two colours, hatch, cross-hatch,
  brick, planks, diamonds, checks, dot grids. See `gallery/2026-11-25/src/common.py` —
  copy it into the new day's src/ and extend it rather than rewriting.
- Gradients: per-row Bayer level between two palette colours (sky: B→W→Y→R works).
- Fonts: Liberation Serif/Sans/Mono have Regular/Bold/Italic/BoldItalic. DejaVu has no
  serif italic. 9px sans and 11px bold serif are legible in preview; italic under 11 isn't.
- Put text on a solid plate, never straight onto a dithered ground.
- Colour contrast: yellow or white on blue = strong. Red on blue or red on black = weak;
  back red with white. Black line on red/yellow = strong.
- Small figures (~34px): rectangle body, circle head, hair cap; give each a colour and a prop.
- Older methods still fine: SVG emitted from Python; numpy raymarch (camera first);
  in-generator Bayer screen for two-colour tone.
- Review at 2× nearest-neighbour upscale, then the sheet. One fix pass, then stop.

## Running threads
- Monkswell Manor / The Mousetrap (11-25). Could return as: the other floors, the cast as
  playing cards, a railway poster for the branch line that's blocked.
- "Hard edges" (09-13), "Dante / stelle" (09-14).
- Formats still untried and promising for detail: isometric town, bird's-eye map with
  legend, botanical plate, cross-section of a ship or a mountain hut, shop front, seed
  packet, tarot card, board game, wallpaper sample book, a busy market, a library wall.
- 3D with shadows (a lit room, a staircase) — now combine with drawn overlays.

## Avoid / learned the hard way
- Too minimal (owner, 11-25). Big empty flats with one shape in them are out.
- Smoke as stacked arcs reads as springs (11-25) — try dithered blobs or a stippled plume.
- Small constellations get lost behind foreground linework; give them clear sky.
- Silhouettes under ~40px don't read unless they have a second colour or an outline.
- Photographic sources: flats must be pure palette colours before dithering (09-13).
- Generic ordered dither on a two-colour palette gives a band, not tone (09-14).
- Clip perspective lines to their region; they'll happily run across the frame (11-25).
- Count things I caption ("eight souls") — I'd drawn seven the first time.

## Recently used (last ~14 days; don't repeat too soon)
- 11-25 styles: pixel-drawn landscape illustration; doll's-house cutaway; blueprint
  floor plan with annotations; theatre proscenium poster; night scene with wires-as-stave.
- 11-25 subjects: snowbound manor, cross-section house, ground plan, stage + audience,
  moon/Orion/Taurus, mice, snow, The Mousetrap.
- (09-13/09-14 work is outside the two-week window; see journal.)
