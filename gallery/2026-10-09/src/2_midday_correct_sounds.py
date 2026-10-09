"""Hunminjeongeum Haerye as an anatomical plate: the five basic consonants drawn from the
organs that make them, the stroke-added series, and the three vowel roots heaven, earth, person."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from kit import *

img = Image.new("RGB", (W, H), WH)
d = ImageDraw.Draw(img); d.fontmode = "1"
f9, f11, f13, f15 = font(10), font(11), font(13), font(15, bold=True)
cjk = lambda s: ImageFont.truetype("/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf", s)

# ---- title band
d.rectangle([0, 0, W, 44], fill=K)
d.text((14, 8), "訓民正音", font=cjk(26), fill=WH)
d.text((140, 8), "THE CORRECT SOUNDS FOR", font=f11, fill=Y)
d.text((140, 23), "THE INSTRUCTION OF THE PEOPLE", font=f11, fill=Y)
d.rectangle([352, 48, 394, 62], fill=R); d.text((358, 49), "1446", font=f11, fill=WH)

# ---- head in section (facing left)
head = [(250, 62), (205, 64), (160, 76), (128, 100), (114, 130), (112, 150), (96, 170), (80, 188),
        (86, 196), (102, 200), (100, 212), (92, 220), (98, 230), (94, 238), (100, 250), (104, 266),
        (114, 282), (140, 290), (168, 296), (178, 318), (180, 342), (292, 342), (290, 300), (300, 270),
        (322, 240), (336, 200), (336, 150), (322, 108), (292, 76)]
hm = mask_of(lambda m: m.polygon(head, fill=255))
a = to_arr(img)
yy, xx = np.mgrid[0:H, 0:W]
hatch = ((xx + yy) % 6 == 0)
a[hm] = WH
a[hm & hatch] = K
img = Image.fromarray(a); d = ImageDraw.Draw(img); d.fontmode = "1"

# cavities (white), drawn over the hatch
nasal = [(112, 152), (150, 140), (205, 142), (232, 158), (236, 178), (200, 176), (150, 178), (110, 186)]
oral = [(102, 206), (130, 200), (170, 198), (206, 196), (232, 188), (240, 208), (236, 232), (200, 236),
        (150, 238), (112, 236), (100, 226)]
phar = [(232, 158), (250, 166), (252, 210), (246, 260), (240, 300), (238, 342), (212, 342), (214, 300),
        (220, 260), (228, 232), (240, 208)]
for poly in (nasal, oral, phar):
    d.polygon(poly, fill=WH)
for poly in (nasal, oral, phar):
    d.line(poly + [poly[0]], fill=K, width=2)
# nasal conchae
for k in range(3):
    d.arc([140 + k * 6, 146 + k * 9, 210 - k * 4, 166 + k * 9], 190, 350, fill=B, width=2)
# tongue
tongue = [(110, 232), (122, 220), (150, 212), (185, 210), (215, 214), (232, 230), (234, 258), (226, 286),
          (215, 300), (195, 290), (170, 268), (140, 252), (115, 244)]
d.polygon(tongue, fill=R, outline=K)
d.line([(130, 232), (205, 230), (222, 262)], fill=K, width=1)  # midline groove
# teeth
for i in range(5):
    x = 104 + i * 9
    d.rectangle([x, 199, x + 7, 210], fill=WH, outline=K)
    d.rectangle([x + 2, 233, x + 9, 243], fill=WH, outline=K)
# lips, red
d.ellipse([88, 210, 102, 222], fill=R, outline=K); d.ellipse([90, 226, 104, 238], fill=R, outline=K)
# soft palate / uvula
d.line([(206, 196), (226, 196), (236, 212)], fill=K, width=3)
d.ellipse([231, 208, 241, 220], fill=R, outline=K)
# larynx rings
for k in range(5):
    d.line([(214, 308 + k * 7), (238, 308 + k * 7)], fill=B, width=2)
# eye and ear
d.ellipse([140, 120, 162, 132], fill=WH, outline=K, width=2); d.ellipse([147, 121, 156, 131], fill=K)
d.arc([132, 108, 170, 126], 200, 340, fill=K, width=2)
d.ellipse([288, 150, 318, 200], fill=WH, outline=K, width=2); d.arc([294, 158, 314, 192], 270, 90, fill=K, width=2)
d.line(head + [head[0]], fill=K, width=3)

# ---- leaders to the five letters
labels = [  # glyph, anchor on head, label pos, caption
    ("ㄱ", (226, 228), (356, 196), "tongue\nroot"),
    ("ㄴ", (124, 218), (12, 246), "tongue\ntip"),
    ("ㅁ", (92, 224), (12, 176), "lips"),
    ("ㅅ", (112, 204), (12, 306), "tooth"),
    ("ㅇ", (228, 300), (356, 280), "throat"),
]
for ch, (ax, ay), (lx, ly), cap in labels:
    right = lx > 200
    tx = lx - 6 if right else lx + 40
    d.line([(ax, ay), (tx, ly + 14)], fill=B, width=1)
    d.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=B)
    d.rectangle([lx - 2, ly - 2, lx + 34, ly + 32], fill=WH, outline=B, width=2)
    glyph(d, ch, lx, ly, 32, K, 4)
    d.multiline_text((lx, ly + 35), cap, font=f9, fill=K, spacing=1)

# ---- derivation table
ty = 378
d.line([(10, ty - 6), (390, ty - 6)], fill=K, width=2)
d.text((12, ty - 2), "ADD A STROKE  ·  THE SOUND GROWS HARSHER", font=f9, fill=R)
cols = [["ㄱ", "ㅋ"], ["ㄴ", "ㄷ", "ㅌ"], ["ㅁ", "ㅂ", "ㅍ"], ["ㅅ", "ㅈ", "ㅊ"], ["ㅇ", "ㆆ", "ㅎ"]]
names = ["molar", "lingual", "labial", "dental", "throat"]
for i, col in enumerate(cols):
    cx = 14 + i * 76
    d.rectangle([cx, ty + 14, cx + 70, ty + 132], outline=K, width=1)
    d.rectangle([cx, ty + 14, cx + 70, ty + 26], fill=B)
    d.text((cx + 5, ty + 14), names[i], font=f9, fill=WH)
    for j, ch in enumerate(col):
        gy = ty + 30 + j * 34
        glyph(d, ch, cx + 20, gy, 30, R if j == 0 else K, 4)
        if j:
            d.polygon([(cx + 8, gy - 4), (cx + 14, gy - 4), (cx + 11, gy + 1)], fill=R)

# ---- heaven, earth, person
by = 520
d.line([(10, by - 6), (390, by - 6)], fill=K, width=2)
cells = [("·", "天", "HEAVEN"), ("ㅡ", "地", "EARTH"), ("ㅣ", "人", "PERSON")]
for i, (ch, hz, en) in enumerate(cells):
    cx = 14 + i * 126
    d.rectangle([cx, by, cx + 120, by + 70], fill=[Y, G, WH][i], outline=K, width=2)
    glyph(d, ch, cx + 4, by + 8, 56, K, 9)
    d.text((cx + 68, by + 10), hz, font=cjk(26), fill=K if i != 1 else WH)
    d.text((cx + 66, by + 46), en, font=f9, fill=K if i != 1 else WH)
# little emblem for each: sun, ground hatching, a figure
d.ellipse([110, by + 52, 126, by + 68], fill=R) if False else None
for k in range(6):
    d.line([(140 + 8 + k * 8, by + 66), (140 + 14 + k * 8, by + 60)], fill=K, width=1)

# seal
d.rectangle([12, 54, 60, 100], fill=R)
d.text((16, 62), "正音", font=cjk(20), fill=WH)
d.rectangle([15, 57, 57, 97], outline=WH, width=1)
d.rectangle([0, 0, W - 1, H - 1], outline=K, width=3)
save(img)
