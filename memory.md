# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## READ THIS FIRST — the memory is broken (found 2026-11-10)
- Every run since 09-16 was pushed to its own throwaway `claude/*` branch and never merged.
  `main` — which is what the frame fetches (`…/main/current`) — is stuck at 09-14, and each
  run started from the 09-14 memory. If the journal's last entry is far behind today's date,
  it has happened again: run `git fetch origin && git for-each-ref --sort=-committerdate
  refs/remotes/origin | head` to see what other days exist, and tell the owner.
- I am not allowed to push to main myself. The owner was notified on 11-10. Until it is
  fixed, the owner is seeing old pictures and repeating old feedback.
- Lost days (on orphan branches, 09-16 … 10-14) used these seeds — don't repeat them soon:
  Kandinsky, Enterprise, equinox, colours, Magellan, Wells, Michaelmas blackberries,
  Zauberflöte, Tōkaidō/Hiroshige, Alex Raymond, Steve Reich, St Francis, Patinir, Kon-Tiki,
  Luna 3, 1871 fires/Draconids, Hangul Day, Giacometti, momijigari, Columbus/Sea Symphony,
  Berni's Juanito Laguna, Hastings + Pooh.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They like *code-made* art most. Not keen on image diffusion. 3D renders: yes, sometimes.
- STANDING FEEDBACK (11-10, and evidently said many times before): the work went "a few
  levels too minimal". Restricted palettes were only ever meant as an *occasional* thing.
  They want me to "express myself with much more detail". So: full six-colour palette by
  default, dense, drawn, inhabited pictures. At most one restricted-palette piece a day.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~1px and text under ~8px are at risk (still unverified on hardware).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: unknown, publishing as UTC. Location unknown too (no local weather). Ask.
- sensors.jsonl / feedback.jsonl: still empty as of 11-10.

## Environment
- `python` is 3.11 with no numpy. Use `/usr/local/bin/python3.13` for everything
  (numpy, scipy, PIL, cairosvg are there). Fonts: Liberation Serif/Sans, DejaVu, Inter.
- `scripts/kit.py` is my drawing kit (copy it into the day's `src/` or set PYTHONPATH):
  draw at 3× in pure palette colours with PIL; `save()` shrinks with `vote_down`.
  Render with `PYTHONPATH=gallery/DATE/src python3.13 scripts/render.py … --dither none`.

## Taste I'm developing (mine — revise freely)
- Density with hierarchy: one big readable shape (a river's S, a spiral, a façade grid, a
  pool of candlelight) and then hundreds of small drawn things inside it.
- Inhabit the picture: windows with people in them, animals, boats, a cat somewhere.
  A recurring creature across the day (11-10: Hogarth's pug) is a nice spine.
- A day should have a thread — one seed, five readings — plus a motif hidden in each piece.
- Vary *kind* across the day: map-landscape, engraved plate, 3-D, street elevation, still life.
- Texture comes from drawn pattern (furrows, bricks, tiles, hatching), not from noise.
- Night: mostly black (80%+), one pool of warm light, a window with the real sky in it.
- Put the actual sky in: tonight's moon phase, the meteor shower that's on.

## Working methods that are proven
- Flat procedural drawing at 3× with `vote_down` → crisp, no stray colours (11-10 pieces 1,2,4).
- Warped-Voronoi patchwork in numpy, per-cell stripe/dot textures, hedges from cell edges,
  then objects painted back-to-front by y with a depth scale (11-10 valley).
- 3-D without a raytracer: project points yourself (k = F/(F+depth)), paint polygons deepest
  first. Then `pair_screen` (kit) to quantise tones as a Bayer screen of just two inks.
- Engraving shader: albedo map + angle map drawn with PIL; tone = albedo × light falloff;
  ink where cos-line-screen < tone; cross-hatch above 0.5; black contours from gradients;
  colour the ink by which light is stronger (11-10 night).
- Raymarched heightfields in numpy are cheap (09-14). Camera first, lighting second.
- Numbered-specimen plates: a grid of cells, one tiny function per figure (11-10 plate).

## Avoid / learned the hard way
- Never LANCZOS-shrink line art then nearest-quantise: thin black on white → grey → GREEN;
  black on yellow → olive → GREEN. Use `vote_down`, or exclude green in `pair_screen`.
- A stairwell/tunnel only reads if the opening nearly fills the frame; otherwise the top
  ring swallows everything (11-10, three tries).
- Engraving shader on a mid-tone wall = wallpaper. Keep background albedo low (<0.2).
- Random dark bricks >10% of a wall look like blotches.
- Draw sky decorations (rays) before the land or clip them.
- Silhouettes under ~40px don't read; cells of pixel patterns ≥10px (09-13).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14).
- Morning valley 11-10 is at the limit of busy for 4": beyond that, give the eye a rest area.

## Running threads
- Hogarth could return: "Four Times of the Day", signboards, the pug.
- Illustrated maps; street elevations at different hours; rooms by candlelight.
- 3-D by hand-projection: a library, a greenhouse, a lighthouse stair, a canal lock.
- Charts and plates: star charts, tide tables, old technical drawings as art.

## Recently used (last ~14 days on THIS branch; see lost-days list above too)
- 11-10 styles: illustrated-map landscape, numbered engraved plate, projected 3-D
  stairwell, flat street elevation, code-engraved candlelit still life.
- 11-10 subjects: meander river valley, Analysis of Beauty diagrams, oval staircase,
  terrace of houses with lamplighter, candle/violin/window with Taurids.
- 11-10 palettes: four full-palette pieces, one restricted (K/W/Y + red accents).
