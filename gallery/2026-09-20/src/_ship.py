# Shared silhouette for the day's recurring motif: a carrack/nao under sail,
# seen from the side. Used at varying scale and detail across all five pieces
# (the fleet shrinks 5-4-3-2-1 through the day, standing for the three years
# of the real voyage). Kept in one place so the ship reads the same each time.
import math


def ship(draw, x, y, s, hull, sail=None, facing=1, detail=True, lantern=None, wake=None):
    """Draw one ship. (x,y) = waterline centre. s = overall length in px.
    hull: fill colour for the hull. sail: fill colour for sails (None = same as hull,
    i.e. a flat cut silhouette). facing: 1 = sailing right, -1 = sailing left.
    detail: draw masts/sails/rigging (False = distant, hull-only silhouette).
    lantern: colour for a stern lantern dot (night piece). wake: colour for a wake line.
    """
    f = facing
    hx = lambda u: x + f * u * s  # noqa: E731  local coordinate helper

    # hull: shallow curved trapezoid, higher astern than at the bow
    hull_pts = [
        (hx(-0.46), y + 0.02 * s), (hx(-0.40), y + 0.13 * s),
        (hx(-0.10), y + 0.15 * s), (hx(0.30), y + 0.13 * s),
        (hx(0.46), y - 0.01 * s), (hx(0.40), y - 0.11 * s),
        (hx(0.10), y - 0.10 * s), (hx(-0.30), y - 0.10 * s),
    ]
    draw.polygon(hull_pts, fill=hull)
    # sterncastle: a raised block astern
    draw.polygon([
        (hx(0.14), y - 0.10 * s), (hx(0.36), y - 0.10 * s),
        (hx(0.34), y - 0.24 * s), (hx(0.16), y - 0.24 * s),
    ], fill=hull)

    if detail:
        sc = sail or hull
        # mainmast + sail (larger, amidships) and foremast + sail (smaller, toward bow)
        for mx, mh, sw in ((-0.05, 0.62, 0.30), (-0.30, 0.42, 0.18)):
            top = y - mh * s
            draw.line((hx(mx), y - 0.10 * s, hx(mx), top), fill=hull, width=max(1, int(s * 0.02)))
            yardY = top + 0.10 * s
            draw.line((hx(mx - sw), yardY, hx(mx + sw), yardY), fill=hull, width=max(1, int(s * 0.015)))
            draw.polygon([
                (hx(mx - sw * 0.85), yardY + 0.02 * s), (hx(mx + sw * 0.85), yardY + 0.02 * s),
                (hx(mx + sw * 0.55), yardY + 0.34 * s), (hx(mx - sw * 0.55), yardY + 0.34 * s),
            ], fill=sc)
        # bowsprit
        draw.line((hx(0.40), y - 0.08 * s, hx(0.60), y - 0.20 * s), fill=hull, width=max(1, int(s * 0.02)))

    if lantern:
        lx, ly = hx(0.32), y - 0.22 * s
        r = max(1.5, s * 0.02)
        draw.ellipse((lx - r, ly - r, lx + r, ly + r), fill=lantern)

    if wake:
        for i, dx in enumerate((0.55, 0.75, 0.95)):
            wy = y + (0.03 + i * 0.015) * s
            draw.line((hx(-0.46 * f * 0 - dx * f), wy, hx(-dx * f - 0.15 * f), wy + 0.02 * s),
                      fill=wake, width=1)


def wake_trail(draw, x, y, length, color, facing=-1, n=5, spread=0.06):
    """A short chevron wake trailing behind a ship at (x,y), pointing away (facing)."""
    for i in range(n):
        t = (i + 1) / n
        lx = x + facing * length * t
        wy = spread * length * t
        draw.line((lx, y - wy, lx - facing * length * 0.12, y), fill=color, width=1)
        draw.line((lx, y + wy, lx - facing * length * 0.12, y), fill=color, width=1)
