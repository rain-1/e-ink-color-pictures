# memory.md

Rewritten by me at the end of every daily run. Hard cap: 150 lines. If it's longer,
something has to go. Git keeps the old versions; journal.md keeps the day-by-day.

## READ THIS FIRST — the memory is broken (found 11-10, still broken 11-11)
- Each run is given a fresh `claude/*` branch cut from `main`, and nothing is ever merged.
  `main` — what the frame fetches (`…/main/current`) — is stuck at 09-14. So every run
  starts with the 09-14 memory, and the owner keeps seeing 09-14 and repeating old feedback.
- FIRST THING EACH RUN: `git fetch origin && git for-each-ref --sort=-committerdate
  --format='%(committerdate:short) %(refname:short) %(subject)' refs/remotes/origin | head`.
  If a branch is newer than your HEAD and HEAD is its ancestor, `git merge --ff-only` it
  before reading memory (11-11 did this onto `claude/dreamy-einstein-ez7p4n`).
  The newest chain so far: main(09-14) → ez7p4n(11-10) → dreamy-einstein-6672h1(11-11).
- I may not push to main or open a PR unasked. Owner was notified 11-10 and 11-11: they
  need to merge the newest claude/* branch into main (or point the frame/schedule at it).
- Lost days (orphan branches 09-16 … 10-14) used these seeds — don't repeat them soon:
  Kandinsky, Enterprise, equinox, colours, Magellan, Wells, Michaelmas blackberries,
  Zauberflöte, Tōkaidō/Hiroshige, Alex Raymond, Steve Reich, St Francis, Patinir, Kon-Tiki,
  Luna 3, 1871 fires/Draconids, Hangul Day, Giacometti, momijigari, Columbus/Sea Symphony,
  Berni's Juanito Laguna, Hastings + Pooh.

## Who this is for
- One person, who bought a 4" six-colour e-paper frame and handed it to me.
- They like *code-made* art most. Not keen on image diffusion. 3D renders: yes, sometimes.
- STANDING FEEDBACK (repeated verbatim every run because they only ever see 09-14): the
  work went "a few levels too minimal"; restricted palettes were meant as an *occasional*
  thing; "express yourself with much more detail". So: full six-colour palette by default,
  dense, drawn, inhabited pictures. At most one restricted-palette piece a day.
- "Don't be a perfectionist. There's always tomorrow."

## The frame
- 400×600 portrait. Six colours: black, white, red, yellow, blue, green.
- Real panel is duller than the ideal palette: white is paper-grey, green olive-ish, blue
  deep. Lines under ~1px and text under ~8px are at risk (still unverified on hardware).
- Refresh 15–30 s with visible flashing: five changes a day.
- Slots (local): morning 06, midday 10, afternoon 14, evening 18, night 22.
- Timezone: unknown, publishing as UTC. Location unknown (I assume ~50°N for skies). Ask.
- sensors.jsonl / feedback.jsonl: still empty as of 11-11.

## Environment
- `python` is 3.11 with no numpy. Use `/usr/local/bin/python3.13` for everything
  (numpy, scipy, PIL, cairosvg are there). Fonts: Liberation Serif/Sans, DejaVu, Inter.
- `scripts/kit.py` is my drawing kit (copy into the day's `src/`): draw at 3× in pure
  palette colours with PIL; `save()` shrinks with `vote_down`. Render with
  `PYTHONPATH=gallery/DATE/src python3.13 scripts/render.py SRC --out N.png --dither none`.
- A full day (five dense pieces) is ~1,000 lines of Python; write each piece in one go,
  look once, fix once.

## Taste I'm developing (mine — revise freely)
- Density with hierarchy: one big readable shape (a river's S, a spiral, a white zigzag
  lane, a sun's rings) and then hundreds of small drawn things inside it.
- Inhabit the picture: windows with people, animals, boats, a cat somewhere.
- A day has a thread — one seed, five readings — plus a motif hidden in each piece
  (11-10 Hogarth's pug; 11-11 a sailing boat).
- Vary *kind* across the day: painterly strokes, flat pattern interior, mathematical
  ornament + figure, picture-map, line-on-black.
- Texture comes from drawn pattern (repeats, bricks, tiles, hatching), not from noise.
  Pattern laid on pattern (Vuillard) suits this panel extremely well.
- Night: 80%+ black, scratched line, the real sky for the date (moon phase, meteor shower,
  constellations placed from RA/Dec).
- Art-history birthdays are reliable seeds when the artist's *method* maps onto six inks.

## Working methods that are proven
- Flat procedural drawing at 3× with `vote_down` → crisp, no stray colours.
- Pattern layers: draw each repeat on its own full-canvas image, then
  `im.paste(layer, mask=polygon_mask)`; outline the polygon afterwards (11-11 #2).
- Stroke painting: paint a continuous-tone target (numpy gradients + PIL shapes), then lay
  ~28k overlapping brick strokes on a jittered 3.5×2.5 grid; each stroke's ink = random
  choice between the best two-ink pair, weighted by the mix; orientation from a field
  (circles round the sun, flat on water) or an angle map. No black unless max(rgb)<105.
  Redraw masts/sun edge on top as lines (11-11 #1).
- Swirl ornament: per-pixel numpy with sector = floor(θ − k·log(1+r/c)); patterns in
  (log r, angular fraction) bend along the spiral; mix with flat stamped layers (11-11 #3).
- Zigzag terraces painted top-down: houses above a lane, then lane, then walkers (11-11 #4).
- Sky maps: x=−ΔRA·15·cos δ, y=Δδ, rotate by (90°−lat) for a rising eastern sky (11-11 #5).
- White-on-black: finish with `vote_down(im, S, wk=0.42)` so hairlines beat the black.
- Warped-Voronoi patchwork landscapes; hand-projected 3-D painted deepest first;
  `pair_screen` for two-ink tone; engraving shader (albedo × light → line screen) (11-10).
- Raymarched heightfields in numpy are cheap (09-14). Camera first, lighting second.

## Avoid / learned the hard way
- Never LANCZOS-shrink line art then nearest-quantise: thin black on white → grey → GREEN.
  Use `vote_down`, or exclude green in `pair_screen`.
- Strokes/dabs that don't overlap leave white paper showing and wash the picture out.
- Crowds: ≤ one figure per ~20px of path or the path disappears (11-11 #4 was borderline).
- Labels under 8px on black don't read; either 9px+ or leave them off.
- A stairwell/tunnel only reads if the opening nearly fills the frame (11-10).
- Engraving shader on a mid-tone wall = wallpaper. Keep background albedo low (<0.2).
- Random dark bricks >10% of a wall look like blotches. Draw sky rays before the land.
- Silhouettes under ~40px don't read; cells of pixel patterns ≥10px (09-13).
- Draw stacked forms bottom-up so upper tiers overlap lower ones (09-14).

## Running threads
- Signac/Vuillard could return: Seurat (2 Dec), Cross, Bonnard; Vuillard's theatre posters.
- Hogarth: "Four Times of the Day", signboards, the pug.
- Illustrated maps; street elevations at different hours; rooms by candlelight.
- 3-D by hand-projection: a library, a greenhouse, a lighthouse stair, a canal lock.
- Charts and plates: tide tables, old technical drawings as art. Leonids peak ~17 Nov.

## Recently used (last ~14 days on this chain; see lost-days list above too)
- 11-10 styles: illustrated-map landscape, numbered engraved plate, projected 3-D
  stairwell, flat street elevation, code-engraved candlelit still life.
- 11-10 subjects: meander river valley, Analysis of Beauty diagrams, oval staircase,
  terrace of houses with lamplighter, candle/violin/window with Taurids.
- 11-11 styles: pointillist stroke-painting, pattern-on-pattern interior, spiral pinwheel
  ornament with portrait, dusk picture-map of a hill town, scratchboard star-chart nocturne.
- 11-11 subjects: Saint-Tropez harbour sunrise, seamstress at a gingham table, painter with
  six-ink palette, Martinmas lantern procession, harbour + lighthouse under Orion/Taurus.
- Taurids have now been the night piece twice running — pick another night subject next.
- Palettes: all full-palette except 11-11 night (K/W with Y/B accents).
