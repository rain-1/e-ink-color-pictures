"""Afternoon: The Serpentine Stair. Hogarth said the line of grace is a wire wound round
a cone. Here it is as a handrail: an oval staircase seen from the top landing, drawn as
real 3-D geometry (perspective projection, painter's algorithm), four turns down to a
chequered hall where the pug is waiting."""
import math, random
from kit import *
rnd = random.Random(53)
im, d = canvas(Y)
F = 520.0; A_, B_ = 160.0, 232.0; CAM = (14.0, -18.0); VP = (207.0, 312.0)
NT = 24; TURN = 300.0; RISE = TURN / NT; NSTEP = int(NT * 3.3); D0 = 60.0; HB = 88.0
R0, R1 = 1.0, 2.4; TH0 = math.radians(205); DTH = -2 * math.pi / NT
DFLOOR = D0 + NSTEP * RISE + 8
LA = math.radians(-70)                       # where the window light comes from, in plan

def pt(rf, th, dp):
    k = F / (F + dp)
    return (VP[0] + (rf * A_ * math.cos(th) - CAM[0]) * k, VP[1] + (rf * B_ * math.sin(th) - CAM[1]) * k)
def arc(rf, t0, t1, dp, n=5):
    return [pt(rf, t0 + (t1 - t0) * i / n, dp) for i in range(n + 1)]
def fog(dp):                                 # 0 near, 1 deep
    return min(1.0, max(0.0, (dp - D0) / (DFLOOR - D0))) ** 0.8

# ---------- hall floor: chequers in plan, a rug, the pug
kf = F / (F + DFLOOR)
def fl(x, y): return (VP[0] + (x - CAM[0]) * kf, VP[1] + (y - CAM[1]) * kf)
T = 30
for i in range(-9, 9):
    for j in range(-12, 12):
        x, y = i * T, j * T
        lit = math.hypot((x + 15 - 20) / 150, (y + 15 + 30) / 190)
        c = (Wh if (i + j) % 2 else mix(K, B, 0.55)) if lit < 1 else (mix(Wh, B, 0.75) if (i + j) % 2 else K)
        poly(d, [fl(x, y), fl(x + T, y), fl(x + T, y + T), fl(x, y + T)], c)
        if (i + j) % 2 and lit < 1:
            poly(d, [fl(x + 15, y + 9), fl(x + 21, y + 15), fl(x + 15, y + 21), fl(x + 9, y + 15)], R)
# round rug
for rr, c in ((66, R), (58, Y), (54, R), (30, Y), (26, B)):
    poly(d, [fl(10 + rr * math.cos(a / 20 * math.pi), -20 + rr * 1.2 * math.sin(a / 20 * math.pi)) for a in range(40)], c)
for a in range(16):
    t = a / 16 * 2 * math.pi
    poly(d, [fl(10 + 34 * math.cos(t), -20 + 41 * math.sin(t)), fl(10 + 50 * math.cos(t + .12), -20 + 60 * math.sin(t + .12)), fl(10 + 50 * math.cos(t - .12), -20 + 60 * math.sin(t - .12))], Y)
# the pug, from above: body, head, ears, curled tail
def fp(x, y): return fl(10 + 1.7 * x, -20 + 1.7 * y)
px_, py_ = fp(0, 0)
poly(d, [fp(14 * math.cos(a / 12 * math.pi) - 2, 9 * math.sin(a / 12 * math.pi)) for a in range(24)], Wh)
poly(d, [fp(15 + 7 * math.cos(a / 12 * math.pi), 7 * math.sin(a / 12 * math.pi)) for a in range(24)], Wh)
poly(d, [fp(20 + 4 * math.cos(a / 12 * math.pi), 4 * math.sin(a / 12 * math.pi)) for a in range(24)], K)
for sy in (-1, 1): poly(d, [fp(12, sy * 5), fp(16, sy * 9), fp(18, sy * 5)], K)
line(d, [fp(-16 + 5 * math.cos(a / 8 * math.pi) * (1 - a / 30), 5 * math.sin(a / 8 * math.pi) * (1 - a / 30)) for a in range(22)], Wh, 1.2)

# ---------- the stair, deepest step first
cat_step, man_step = 33, 44
for i in range(NSTEP - 1, -1, -1):
    t0, t1 = TH0 + i * DTH, TH0 + (i + 1) * DTH
    dp, dn = D0 + i * RISE, D0 + (i + 1) * RISE
    tm = (t0 + t1) / 2
    lamb = 0.5 + 0.5 * math.cos(tm - LA)                 # 1 = facing the window
    sh = round(min(1.0, 0.0 + 0.5 * (1 - lamb) + 0.45 * fog(dp)) * 4) / 4
    CA, CB = 1.09, 1.62                                  # carpet runner
    if i == 0:                                           # the top landing we are standing on
        ta, tb_ = TH0 + 1.75, TH0
        poly(d, arc(R0, ta, tb_, D0, 14) + arc(R1, tb_, ta, D0, 14), mix(Y, K, 0.1))
        for q in range(1, 9):
            rf = R0 + (R1 - R0) * q / 9 * 0.6
            line(d, arc(rf, ta, tb_, D0, 14), K, 0.6)
        for q in range(0, 15):
            tq = ta + (tb_ - ta) * q / 14
            line(d, [pt(R0 + (q % 3) * 0.16, tq, D0), pt(R0 + (q % 3) * 0.16 + 0.16, tq, D0)], K, 0.5)
        poly(d, arc(1.09, ta, tb_, D0, 14) + arc(1.62, tb_, ta, D0, 14), R)
        for rf in (1.14, 1.57): line(d, arc(rf, ta, tb_, D0, 14), Y, 1.4)
        for q in range(7):
            tq = ta + (tb_ - ta) * (q + 0.5) / 7; wq = 0.09
            poly(d, [pt(1.2, tq, D0), pt(1.35, tq - wq, D0), pt(1.5, tq, D0), pt(1.35, tq + wq, D0)], Y if q % 2 else B)
            c0 = pt(1.35, tq, D0); circ(d, c0[0], c0[1], 2.2, R if q % 2 else Y)
        line(d, arc(R0, ta, tb_, D0, 14), K, 1.2)
        for q in range(15):
            tq = ta + (tb_ - ta) * q / 14
            p0, p1 = pt(R0 + 0.03, tq, D0), pt(R0 + 0.03, tq, D0 - HB)
            line(d, [p0, p1], K, 2.6); line(d, [p0, p1], Wh, 1.3)
        line(d, arc(R0 + 0.03, ta, tb_, D0 - HB, 14), K, 7); line(d, arc(R0 + 0.03, ta, tb_, D0 - HB, 14), R, 4)
    # riser down to the next tread (at the t1 edge)
    for (ra, rb, col) in ((R0, CA, mix(Y, K, 0.72 + 0.2 * sh)), (CA, CB, mix(R, K, 0.55 + 0.4 * sh)), (CB, R1, mix(Y, K, 0.72 + 0.2 * sh))):
        poly(d, [pt(ra, t1, dp), pt(rb, t1, dp), pt(rb, t1, dn), pt(ra, t1, dn)], col)
    # tread
    wood = mix(Y, K, sh * 0.6); carpet = mix(R, K, sh * 0.9)
    poly(d, arc(R0, t0, t1, dp) + arc(R1, t1, t0, dp), wood)
    for q in range(1, 4):                                # floorboard grain, radial
        tq = t0 + (t1 - t0) * (q / 4 + rnd.uniform(-.06, .06))
        line(d, [pt(R0 + 0.01, tq, dp), pt(CA, tq, dp)], mix(Y, K, min(1, sh + 0.45)), 0.4)
        line(d, [pt(CB, tq, dp), pt(R1, tq, dp)], mix(Y, K, min(1, sh + 0.45)), 0.5)
    poly(d, arc(CA, t0, t1, dp) + arc(CB, t1, t0, dp), carpet)
    kk = F / (F + dp)
    for rf in (CA + 0.05, CB - 0.05): line(d, arc(rf, t0, t1, dp), Y, 1.5 * kk)
    for rf in (CA + 0.11, CB - 0.11): line(d, arc(rf, t0, t1, dp), K, 0.6 * kk)
    # carpet figure: a lozenge with a dot, alternating
    cr = 1.3
    wdt = (t1 - t0) * 0.32
    loz = [pt(cr - 0.13, tm, dp), pt(cr, tm - wdt, dp), pt(cr + 0.13, tm, dp), pt(cr, tm + wdt, dp)]
    poly(d, loz, Y if i % 2 else B); 
    c0 = pt(cr, tm, dp); circ(d, c0[0], c0[1], 2.2 * kk, R if i % 2 else Y)
    for rf in (cr - 0.17, cr + 0.17):
        c1 = pt(rf, tm, dp); circ(d, c1[0], c1[1], 1.3 * kk, Y)
    # stair rod where tread meets the riser of the step above, with finials
    line(d, [pt(CA - 0.04, t0, dp), pt(CB + 0.04, t0, dp)], K, 2.2 * kk); line(d, [pt(CA - 0.04, t0, dp), pt(CB + 0.04, t0, dp)], Y, 1.1 * kk)
    for rf in (CA - 0.05, CB + 0.05):
        c2 = pt(rf, t0, dp); circ(d, c2[0], c2[1], 1.8 * kk, Y, K, 0.4)
    # nosing: light catching the front edge
    line(d, [pt(R0, t1, dp), pt(CA, t1, dp)], Wh, 1.0 * kk + 0.2); line(d, [pt(CB, t1, dp), pt(R1, t1, dp)], Wh, 1.0 * kk + 0.2)
    line(d, [pt(CA, t1, dp), pt(CB, t1, dp)], mix(R, Wh, 0.5), 0.8 * kk + 0.2)
    # passengers
    if i == cat_step:
        c3 = pt(1.3, tm, dp); k3 = kk * 1.5
        ell(d, c3[0], c3[1], 8 * k3, 5 * k3, K); circ(d, c3[0] + 7 * k3, c3[1] - 3 * k3, 3.6 * k3, K)
        poly(d, [(c3[0] + 5 * k3, c3[1] - 5 * k3), (c3[0] + 5.5 * k3, c3[1] - 9.5 * k3), (c3[0] + 8 * k3, c3[1] - 6 * k3)], K); poly(d, [(c3[0] + 10 * k3, c3[1] - 4 * k3), (c3[0] + 11.5 * k3, c3[1] - 8 * k3), (c3[0] + 8 * k3, c3[1] - 6 * k3)], K)
        line(d, bez((c3[0] - 7 * k3, c3[1] + 2 * k3), (c3[0] - 14 * k3, c3[1] + 6 * k3), (c3[0] - 6 * k3, c3[1] + 10 * k3), (c3[0] - 2 * k3, c3[1] + 7 * k3), 8), K, 1.6 * k3)
        circ(d, c3[0] + 6 * k3, c3[1] - 3.4 * k3, 0.8 * k3, Y); circ(d, c3[0] + 8.6 * k3, c3[1] - 2.6 * k3, 0.8 * k3, Y)
    if i == man_step:                                    # a climber seen from above: hat, shoulders, hand on rail
        c4 = pt(1.28, tm, dp - 60); k4 = F / (F + dp - 60)
        c5 = pt(1.3, tm, dp)
        poly(d, [(c5[0] - 7 * k4, c5[1]), (c4[0] - 13 * k4, c4[1]), (c4[0] + 13 * k4, c4[1]), (c5[0] + 7 * k4, c5[1])], mix(B, K, 0.3))
        ell(d, c4[0], c4[1], 15 * k4, 9 * k4, B, K, 0.8); circ(d, c4[0], c4[1], 8.5 * k4, K); circ(d, c4[0], c4[1], 5 * k4, None, R, 1.0)
        h1 = pt(R0 + 0.03, tm, dp - HB); line(d, [(c4[0] - 12 * k4, c4[1]), h1], B, 3 * k4); circ(d, h1[0], h1[1], 2.6 * k4, Wh, K, 0.5)
    # the open string: inner face of the stair, with a painted scroll on each step-end
    sface = mix(Wh, B, min(1, 0.1 + 0.9 * (0.5 - 0.5 * math.cos(tm - LA)) * 0.7 + 0.5 * fog(dp)))
    poly(d, arc(R0, t0, t1, dp) + arc(R0, t1, t0, dn + 16), sface)
    line(d, arc(R0, t0, t1, dp), K, 0.9 * kk)
    line(d, [pt(R0, t1, dp), pt(R0, t1, dn + 16)], K, 0.5 * kk)
    line(d, arc(R0, t0, t1, dn + 16), K, 0.9 * kk)
    a0, a1 = pt(R0, t0 + (t1 - t0) * .2, dp + 4), pt(R0, t0 + (t1 - t0) * .8, dp + RISE + 8)
    line(d, bez(a0, (a1[0], a0[1]), (a0[0], a1[1]), a1, 8), R if fog(dp) < .7 else K, 0.8 * kk)
    # balusters (two a step) and the handrail
    for f_ in (0.25, 0.75):
        tb = t0 + (t1 - t0) * f_; db = dp
        p0, p1 = pt(R0 + 0.03, tb, db), pt(R0 + 0.03, tb, db - HB + RISE * f_)
        pm = pt(R0 + 0.03, tb, db - HB * 0.45)
        line(d, [p0, p1], K, 2.6 * kk); line(d, [p0, p1], Wh if fog(dp) < 0.75 else mix(Wh, B, .6), 1.3 * kk)
        circ(d, pm[0], pm[1], 2.0 * kk, Wh, K, 0.5)      # turned bead
    h0, h1 = pt(R0 + 0.03, t0, dp - HB), pt(R0 + 0.03, t1, dn - HB)
    kh = F / (F + dp - HB)
    line(d, [h0, h1], K, 6.5 * kh); line(d, [h0, h1], R, 3.6 * kh)
    hh0, hh1 = pt(R0 + 0.045, t0, dp - HB - 3), pt(R0 + 0.045, t1, dn - HB - 3)
    if lamb > 0.35: line(d, [hh0, hh1], Wh, 0.9 * kh)

# newel post and volute where the rail lands in the hall
i = NSTEP; tN = TH0 + i * DTH; dN = D0 + i * RISE
p0, p1 = pt(R0 + 0.03, tN, dN + 6), pt(R0 + 0.03, tN, dN - HB)
line(d, [p0, p1], K, 5); line(d, [p0, p1], Wh, 2.6); circ(d, p1[0], p1[1], 3.4, R, K, 0.8)

im = im.resize((W, H), Image.LANCZOS)
im = pair_screen(im, pairs={(i, j) for i in range(5) for j in range(i + 1, 5)})   # no green ink
save(im)
