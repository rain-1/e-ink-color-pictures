# Evening — Kandinsky's 1923 Bauhaus questionnaire answer: yellow belongs to the
# triangle, red to the square, blue to the circle. Three large flat shapes climbing
# the sheet on a white ground, evening light warming toward the top (yellow highest).
import os
from PIL import Image, ImageDraw
W, H = 400, 600
WHT, YEL, RED, BLU, BLK = (255, 255, 255), (0xF5, 0xD4, 0x00), (0xE0, 0x1B, 0x24), (0x12, 0x3D, 0xB0), (0, 0, 0)
im = Image.new("RGB", (W, H), WHT)
d = ImageDraw.Draw(im)

# blue circle, lowest — heaviest, most at rest
d.ellipse((60, 400, 300, 560), fill=BLU)
# red square, middle — tension between the circle's calm and the triangle's thrust
d.rectangle((110, 220, 340, 400), fill=RED)
# yellow triangle, highest — sharp, advancing, aspirational
d.polygon([(90, 200), (330, 200), (250, 30)], fill=YEL)

# thin black baseline grid marks the three registers were chosen, not accidental
for y in (30, 200, 400, 560):
    d.line((20, y, 40, y), fill=BLK, width=2)

# the circle motif recurs at small scale inside the square and the triangle
d.ellipse((205, 295, 245, 335), fill=BLU)
d.ellipse((195, 100, 219, 124), fill=RED)

im.save(os.environ["OUT_RAW"])
