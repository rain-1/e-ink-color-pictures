"""Midday — a section through Monkswell Manor. Doll's-house cutaway; every room papered
in a different pattern, eight guests, and the mice below stairs."""
import math, random
import numpy as np
from common import *
random.seed(25)
im, d = new(B)

# ---------------------------------------------------------------- outside: snow sky, ground
for _ in range(260):
    x, y = random.randrange(W), random.randrange(0, 404)
    d.point((x, y), fill=WH)
    if random.random() < .3: d.rectangle([x, y, x + 1, y + 1], fill=WH)
rect(im, (0, 398, W, 412), WH)
rect(im, (0, 410, W, 546), Y, K, p_hatch(3, 1))                       # earth
for _ in range(60):                                                    # stones, roots
    x, y = random.randrange(W), random.randrange(416, 544)
    d.ellipse([x, y, x + random.randrange(2, 6), y + random.randrange(2, 4)], fill=WH, outline=K)

L, Rr = 30, 370
F_ATT, F_1, F_G, F_C = 150, 268, 404, 520                               # floor tops

# ---------------------------------------------------------------- roof + attic
roof = [(12, 152), (200, 30), (388, 152)]
poly(im, roof, K)
attic = [(40, 150), (200, 46), (360, 150)]
poly(im, attic, Y, K, p_planks(9))
d.line([(12, 152), (200, 30), (388, 152)], fill=K, width=3)
d.line([(8, 146), (200, 21), (392, 146)], fill=WH, width=8)            # snow load
d.line([(8, 141), (200, 16), (392, 141)], fill=WH, width=2)
for x in range(10, 392, 7):                                           # icicles at the eaves
    if x < 60 or x > 340: d.line([(x, 150), (x, 150 + random.randrange(3, 10))], fill=WH)
# rafters & king post
d.line([(200, 50), (200, 150)], fill=K, width=3)
for sx in (-1, 1):
    d.line([(200 + sx * 70, 150), (200, 92)], fill=K, width=2)
    d.line([(200 + sx * 110, 150), (200 + sx * 110, 106)], fill=K, width=2)
# round window, cobweb
d.ellipse([186, 62, 214, 90], fill=B, outline=K, width=2); d.line([(200, 62), (200, 90)], fill=K); d.line([(186, 76), (214, 76)], fill=K)
for r in (8, 15, 22):
    d.arc([90 - r, 106 - r, 90 + r, 106 + r], 20, 100, fill=WH)
for ang in (20, 45, 70, 100):
    d.line([(90, 106), (90 + 24 * math.cos(math.radians(ang)), 106 + 24 * math.sin(math.radians(ang)))], fill=WH)
# trunks, hat box, dress form, rocking horse
d.rectangle([62, 128, 104, 149], fill=R, outline=K); d.line([(62, 135), (104, 135)], fill=K); d.rectangle([80, 133, 86, 138], fill=Y, outline=K)
d.rectangle([108, 136, 134, 149], fill=G, outline=K); d.rectangle([112, 126, 130, 136], fill=B, outline=K)
d.ellipse([146, 132, 168, 149], fill=WH, outline=K); d.line([(146, 138), (168, 138)], fill=R)
d.polygon([(236, 112), (250, 112), (254, 128), (247, 138), (239, 138), (232, 128)], fill=WH, outline=K); d.line([(243, 138), (243, 149)], fill=K, width=2); d.line([(236, 149), (250, 149)], fill=K)
d.arc([268, 136, 310, 156], 200, 340, fill=K, width=2)                 # rocking horse
d.polygon([(276, 128), (300, 128), (302, 122), (308, 118), (310, 124), (304, 130), (300, 140), (296, 140), (294, 134), (282, 134), (280, 140), (276, 140)], fill=WH, outline=K)
d.line([(276, 128), (271, 134)], fill=R, width=2); d.point((306, 121), fill=K)
d.rectangle([322, 138, 346, 149], fill=K); d.text((325, 138), "1926", font=font(8, "sans"), fill=Y)
mouse(d, 180, 149, .7, K, eye=WH)

# ---------------------------------------------------------------- room papers
def room(x0, y0, x1, y1, c1, c2, pat, dado=None):
    rect(im, (x0, y0, x1, y1), c1, c2, pat)
    if dado:
        rect(im, (x0, y1 - 26, x1, y1), *dado); d.line([(x0, y1 - 27), (x1, y1 - 27)], fill=K)
    rect(im, (x0, y1 - 4, x1, y1), K)                                   # skirting
# first floor
room(36, 156, 138, 268, WH, G, p_vlines(8, 3))                          # green stripe bedroom
room(144, 156, 252, 268, WH, R, p_diamond(8), dado=(R, K, p_vlines(6, 1)))  # landing
room(258, 156, 364, 268, B, WH, p_dots2(8))                             # blue spot bedroom
# ground floor
room(36, 274, 252, 404, Y, R, p_diamond(10), dado=(K, R, p_planks(9)))  # great hall
room(258, 274, 364, 404, WH, B, p_dots(5), dado=(WH, B, p_check(5)))    # kitchen
# cellar
rect(im, (36, 410, 364, 520), R, K, p_brick(12, 6))
a = np.array(im); m = mask_rect(36, 410, 364, 520) & p_bayer(.42) ; a[m] = K; im.paste(Image.fromarray(a))   # gloom
# structure: walls and floors
for x in (L, Rr - 6): rect(im, (x, 150, x + 6, 526), K)
for x, y0, y1 in ((138, 156, 268), (252, 156, 268), (252, 274, 404)): rect(im, (x, y0, x + 6, y1), K)
for fy in (F_ATT, F_1, F_G, F_C):
    rect(im, (L, fy, Rr, fy + 6), K)
    for x in range(L + 6, Rr - 4, 12): d.rectangle([x, fy + 2, x + 5, fy + 4], fill=Y)   # joist ends
rect(im, (0, 404, L, 407), WH); rect(im, (Rr, 404, W, 407), WH)

# ---------------------------------------------------------------- people
def person(x, y, body, skirt=False, sit=False, hair=K, hat=None, arm=None):
    """(x,y) = feet. ~34px tall."""
    h = 22 if sit else 34
    if sit:
        d.rectangle([x - 4, y - 14, x + 10, y - 9], fill=body); d.rectangle([x + 7, y - 10, x + 10, y], fill=K)
    elif skirt:
        d.polygon([(x - 4, y - 20), (x + 4, y - 20), (x + 8, y - 5), (x - 8, y - 5)], fill=body)
        d.line([(x - 3, y - 5), (x - 3, y)], fill=K, width=2); d.line([(x + 2, y - 5), (x + 2, y)], fill=K, width=2)
    else:
        d.rectangle([x - 4, y - 14, x - 1, y], fill=K); d.rectangle([x + 1, y - 14, x + 4, y], fill=K)
    d.rectangle([x - 5, y - h + 7, x + 5, y - h + 21], fill=body, outline=K)
    d.ellipse([x - 4, y - h - 1, x + 4, y - h + 7], fill=WH, outline=K)
    d.pieslice([x - 5, y - h - 3, x + 5, y - h + 5], 180, 360, fill=hair)
    if hat: d.rectangle([x - 6, y - h - 3, x + 6, y - h - 2], fill=hat); d.rectangle([x - 3, y - h - 7, x + 3, y - h - 3], fill=hat)
    if arm: d.line([(x + 5, y - h + 10), arm], fill=K, width=2)

person(216, 150, R, hair=Y, arm=(228, 128))                                             # Christopher Wren, exploring the attic

# ---------------------------------------------------------------- green bedroom (first floor, left)
d.rectangle([44, 232, 104, 262], fill=WH, outline=K)                                    # bed
rect(im, (62, 236, 104, 258), R, WH, p_check(4)); d.rectangle([62, 236, 104, 258], outline=K)
d.rectangle([40, 214, 46, 264], fill=K); d.rectangle([102, 228, 107, 264], fill=K)
d.ellipse([47, 226, 62, 236], fill=WH, outline=K)
d.rectangle([58, 172, 96, 204], fill=B, outline=K, width=2); d.line([(77, 172), (77, 204)], fill=K); d.line([(58, 188), (96, 188)], fill=K)  # window
for k in range(8): d.point((60 + k * 4, 201 - (k % 3)), fill=WH)
d.polygon([(54, 170), (66, 170), (56, 206)], fill=Y, outline=K); d.polygon([(100, 170), (88, 170), (98, 206)], fill=Y, outline=K)
d.rectangle([112, 196, 134, 264], fill=Y, outline=K); d.line([(123, 196), (123, 264)], fill=K); d.point((121, 232), fill=K); d.point((125, 232), fill=K)  # wardrobe
d.rectangle([110, 192, 136, 196], fill=K)
d.rectangle([116, 180, 130, 192], fill=R, outline=K)                                    # suitcase on top
person(84, 264, B, skirt=True, hair=R, arm=(96, 240))                                   # Miss Casewell, restless

# ---------------------------------------------------------------- landing + stairs
d.rectangle([160, 170, 182, 200], fill=WH, outline=K, width=2)                          # portrait
d.ellipse([166, 175, 176, 187], fill=K); d.polygon([(163, 198), (171, 186), (179, 198)], fill=K)
d.rectangle([196, 176, 236, 198], fill=G, outline=K, width=2)                           # landscape
d.polygon([(198, 196), (210, 182), (220, 192), (228, 184), (234, 196)], fill=WH)
for i in range(11):                                                                     # balustrade
    x = 150 + i * 10; d.line([(x, 244), (x, 264)], fill=K, width=2)
d.line([(146, 243), (252, 243)], fill=K, width=3)
person(214, 264, G, hair=WH, hat=None, arm=(224, 246))                                  # the Major on the landing
d.rectangle([226, 252, 232, 256], fill=K)
# staircase from hall up to landing
for i in range(13):
    x0 = 150 + i * 8; y0 = 404 - (i + 1) * 10
    rect(im, (x0, y0, 252, y0 + 10), WH, K, p_vlines(4, 1)); d.line([(x0, y0), (252, y0)], fill=K, width=2)
    d.line([(x0 + 4, y0), (x0 + 4, y0 - 22)], fill=K)
d.line([(150, 372), (252, 244)], fill=K, width=3)
rect(im, (150, 274, 252, 280), K)

# ---------------------------------------------------------------- blue bedroom (first floor, right)
d.rectangle([300, 236, 356, 262], fill=WH, outline=K); rect(im, (300, 240, 340, 258), Y, K, p_hlines(4, 1)); d.rectangle([300, 240, 340, 258], outline=K)
d.rectangle([354, 216, 360, 264], fill=K); d.rectangle([296, 230, 300, 264], fill=K); d.ellipse([340, 228, 354, 238], fill=WH, outline=K)
d.rectangle([312, 170, 346, 204], fill=K, outline=K); d.rectangle([314, 172, 344, 202], fill=B, outline=WH)
d.line([(329, 172), (329, 202)], fill=WH); d.line([(314, 187), (344, 187)], fill=WH)
d.rectangle([264, 240, 288, 264], fill=R, outline=K); d.rectangle([266, 244, 286, 250], fill=Y, outline=K); d.rectangle([266, 254, 286, 260], fill=Y, outline=K)  # chest
d.ellipse([268, 226, 284, 240], fill=WH, outline=K); d.rectangle([272, 222, 280, 228], fill=WH, outline=K)                                      # ewer
d.rectangle([266, 184, 282, 206], fill=WH, outline=K); d.ellipse([269, 187, 279, 203], outline=K)                                             # mirror
person(292, 264, K, hair=K, hat=K, arm=(282, 250))                                      # Mr Paravicini and his bag
d.rectangle([276, 250, 288, 258], fill=R, outline=K) if False else None

# ---------------------------------------------------------------- great hall
# fireplace
d.rectangle([52, 330, 112, 400], fill=WH, outline=K, width=2); d.rectangle([46, 322, 118, 330], fill=WH, outline=K, width=2)
d.rectangle([62, 346, 102, 400], fill=K)
for fx, fh, c in ((70, 26, R), (80, 36, R), (90, 28, R), (76, 16, Y), (86, 20, Y), (82, 10, WH)):
    d.polygon([(fx - 6, 398), (fx, 398 - fh), (fx + 6, 398)], fill=c)
d.line([(64, 398), (100, 398)], fill=Y, width=2)
d.rectangle([60, 308, 70, 322], fill=G, outline=K); d.ellipse([78, 304, 92, 322], fill=WH, outline=K); d.line([(85, 313), (85, 308)], fill=K); d.line([(85, 313), (89, 313)], fill=K)  # clock
d.rectangle([100, 310, 108, 322], fill=R, outline=K)
d.rectangle([56, 284, 108, 300], fill=K); d.polygon([(60, 298), (72, 288), (82, 296), (92, 286), (104, 298)], fill=WH)   # antlers-ish painting
# big hall window with the storm behind it
d.rectangle([120, 286, 164, 346], fill=B, outline=K, width=3)
for i in (1, 2): d.line([(120 + i * 14.7, 286), (120 + i * 14.7, 346)], fill=K)
for j in (1, 2, 3): d.line([(120, 286 + j * 15), (164, 286 + j * 15)], fill=K)
for _ in range(34): d.point((random.randrange(122, 163), random.randrange(288, 345)), fill=WH)
d.polygon([(122, 345), (140, 338), (162, 342), (162, 345)], fill=WH)
d.polygon([(114, 282), (128, 282), (118, 352), (114, 352)], fill=R, outline=K); d.polygon([(170, 282), (156, 282), (166, 352), (170, 352)], fill=R, outline=K)
d.line([(112, 282), (172, 282)], fill=K, width=3)
# armchairs, rug, wireless, telephone with its wire cut
rect(im, (40, 400, 150, 404), R, Y, p_vlines(4, 2))
d.rounded_rectangle([122, 366, 148, 400], 5, fill=G, outline=K); d.rectangle([118, 382, 152, 400], fill=G, outline=K); d.rectangle([116, 378, 122, 400], fill=G, outline=K)
person(136, 400, R, sit=True, hair=WH, skirt=True)                                       # Mrs Boyle, by the fire
d.rectangle([40, 384, 52, 400], fill=K); d.rectangle([38, 380, 54, 384], fill=K)           # coal scuttle
d.rectangle([168, 352, 196, 372], fill=R, outline=K, width=2); d.ellipse([172, 356, 184, 368], fill=Y, outline=K); d.line([(188, 357), (193, 357)], fill=K); d.line([(188, 362), (193, 362)], fill=K); d.line([(188, 367), (193, 367)], fill=K)
for r in (5, 9, 13): d.arc([182 - r, 346 - r, 182 + r, 346 + r], 215, 325, fill=K)
d.rectangle([164, 372, 200, 376], fill=K); d.line([(168, 376), (168, 400)], fill=K, width=2); d.line([(196, 376), (196, 400)], fill=K, width=2)
person(182, 400, B, hair=Y, arm=(176, 372)) if False else None
# sergeant with skis at the hall door (under the stairs)
d.line([(232, 400), (236, 340)], fill=WH, width=2); d.line([(238, 400), (241, 342)], fill=WH, width=2)
person(218, 400, B, hair=K, hat=B, arm=(232, 372))
# Christopher Wren, sprawled on the rug
person(76, 404, Y, hair=R, sit=True) if False else None

# ---------------------------------------------------------------- kitchen
d.rectangle([264, 350, 306, 400], fill=K); d.rectangle([268, 362, 284, 384], fill=K, outline=WH); d.rectangle([288, 362, 302, 384], fill=K, outline=WH)   # range
d.rectangle([270, 368, 282, 380], fill=R); d.line([(270, 372), (282, 372)], fill=Y); d.line([(270, 376), (282, 376)], fill=Y)
d.rectangle([272, 274, 282, 350], fill=K)                                                # flue
d.ellipse([270, 340, 286, 351], fill=Y, outline=K); d.rectangle([290, 338, 302, 350], fill=R, outline=K)                                     # pots
for k in range(5): d.arc([292 + k, 322 - k * 4, 300 + k, 332 - k * 4], 90, 270, fill=K)   # steam
d.line([(290, 296), (360, 296)], fill=K, width=2)                                        # rail of pans
for i, c in enumerate((Y, R, Y, K)):
    x = 300 + i * 16; d.line([(x, 296), (x, 304)], fill=K); d.ellipse([x - 5, 304, x + 5, 314], fill=c, outline=K)
d.rectangle([318, 376, 362, 380], fill=Y, outline=K); d.line([(322, 380), (322, 400)], fill=K, width=2); d.line([(358, 380), (358, 400)], fill=K, width=2)   # table
d.ellipse([340, 366, 358, 377], fill=WH, outline=K); d.polygon([(344, 366), (349, 358), (354, 366)], fill=R)                                 # pie
d.rectangle([322, 368, 334, 376], fill=G, outline=K)
rect(im, (258, 398, 364, 404), K, WH, p_check(6))
person(326, 398, G, skirt=True, hair=Y, arm=(338, 372))                                   # Mollie, cooking for seven
d.rectangle([316, 372, 336, 384], fill=WH, outline=K)                                    # apron

# ---------------------------------------------------------------- cellar
# coal heap
heap = [(40, 520), (60, 482), (84, 470), (108, 478), (130, 500), (144, 520)]
poly(im, heap, K)
for _ in range(60):
    x = random.randrange(46, 138); y = random.randrange(474, 518)
    if im.getpixel((x, y)) == K:
        d.line([(x, y), (x + 2, y - 1)], fill=WH); d.point((x + 1, y + 1), fill=B)
d.polygon([(40, 410), (64, 410), (58, 440), (40, 452)], fill=WH); d.polygon([(40, 410), (58, 410), (52, 432), (40, 440)], fill=B)   # coal chute, snow light
# boiler and pipes
d.rounded_rectangle([166, 446, 214, 518], 8, fill=K, outline=WH); d.rectangle([178, 486, 202, 508], fill=R, outline=Y)
d.polygon([(182, 506), (186, 494), (190, 502), (194, 490), (198, 506)], fill=Y)
d.ellipse([184, 456, 196, 468], fill=WH, outline=K); d.line([(190, 462), (194, 458)], fill=R)
for px in (176, 204):
    d.line([(px, 446), (px, 410)], fill=WH, width=3); d.line([(px, 446), (px, 410)], fill=K, width=1)
d.line([(204, 426), (360, 426)], fill=WH, width=3); d.line([(204, 426), (360, 426)], fill=K)
person(150, 520, WH, hair=K, arm=(140, 500))                                              # Giles, shovelling
d.line([(140, 500), (128, 512)], fill=WH, width=2); d.polygon([(128, 512), (120, 510), (122, 518), (130, 518)], fill=WH)
# wine rack
for i in range(5):
    for j in range(4):
        cx, cy = 240 + i * 13, 448 + j * 13
        d.rectangle([cx - 6, cy - 6, cx + 7, cy + 7], outline=Y); d.ellipse([cx - 3, cy - 3, cx + 4, cy + 4], fill=G if (i + j) % 3 else K, outline=K)
rect(im, (232, 494, 300, 498), Y)
# shelf of preserves
d.line([(310, 462), (362, 462)], fill=Y, width=2); d.line([(310, 492), (362, 492)], fill=Y, width=2)
for i in range(6):
    for sy, cols in ((462, (R, Y, G)), (492, (Y, R, WH))):
        x = 313 + i * 8; d.rectangle([x, sy - 12, x + 5, sy - 1], fill=cols[i % 3], outline=K); d.rectangle([x + 1, sy - 14, x + 4, sy - 12], fill=WH)
# the trap, the cheese, the mice
d.rectangle([258, 514, 282, 518], fill=Y, outline=K); d.arc([262, 504, 280, 522], 180, 360, fill=WH); d.polygon([(266, 513), (273, 508), (273, 513)], fill=Y, outline=K)
mouse(d, 302, 519, .9, WH, eye=K, flip=True); mouse(d, 330, 519, .7, WH, eye=K, flip=True); mouse(d, 350, 519, .55, WH, eye=K, flip=True)
d.pieslice([352, 506, 366, 532], 180, 270, fill=K)                                       # mouse hole
# hanging bulb
d.line([(228, 410), (228, 432)], fill=WH); d.ellipse([224, 432, 232, 441], fill=Y, outline=K)
for ang in range(20, 170, 30):
    d.line([(228 + 8 * math.cos(math.radians(ang)), 438 + 8 * math.sin(math.radians(ang))), (228 + 13 * math.cos(math.radians(ang)), 438 + 13 * math.sin(math.radians(ang)))], fill=Y)

# chimney stack
rect(im, (56, 80, 76, 132), R, K, p_brick(8, 4)) if False else None

# ---------------------------------------------------------------- title cartouche
rect(im, (0, 546, W, H), K)
d.rectangle([10, 552, W - 11, H - 7], outline=Y)
spaced(d, 200, 556, "MONKSWELL MANOR", font(15, "serif", True), WH, 3)
ctext(d, 200, 576, "a section, 25 November 1952 · eight souls & three mice", font(11, "serif"), Y)
save(im)
