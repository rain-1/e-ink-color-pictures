# Morning — "First Light, Blue Water". Hanga-style stacked waves, a red sun.
# Uses only palette colours so it is rendered with --dither none.
import os, numpy as np
from PIL import Image, ImageDraw
W,H=400,600
BLK,WHT,RED,YEL,BLU=(0,0,0),(255,255,255),(224,27,36),(245,212,0),(18,61,176)
im=Image.new("RGB",(W,H),YEL); d=ImageDraw.Draw(im)
# sky bands: pale morning = white with a yellow rim near horizon
d.rectangle((0,0,W,230),fill=WHT)
d.rectangle((0,230,W,262),fill=YEL)
# sun
d.ellipse((W/2-70,120,W/2+70,260),fill=RED)
# sea: rows of overlapping wave arcs, blue dominant, white crests
rng=np.random.default_rng(13)
y=262
row=0
while y<H+40:
    step=46
    off=(row%2)*step//2
    for x in range(-step+off,W+step,step):
        d.chord((x-30,y-20,x+30,y+24),0,180,fill=BLU)   # blue body
        d.arc((x-30,y-20,x+30,y+24),200,340,fill=WHT,width=5)  # crest
        d.arc((x-22,y-14,x+22,y+18),200,340,fill=BLK,width=3)
    y+=28; row+=1
# horizon line and a black boat silhouette
d.rectangle((0,262,W,268),fill=BLK)
d.polygon([(150,262),(250,262),(232,282),(168,282)],fill=BLK)
d.rectangle((198,225,204,262),fill=BLK)
d.polygon([(204,228),(240,258),(204,258)],fill=BLK)
im.save(os.environ["OUT_RAW"])
