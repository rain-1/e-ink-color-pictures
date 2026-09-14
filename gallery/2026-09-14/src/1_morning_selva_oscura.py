# Morning — "Selva Oscura" (Inferno I). Palette: black, green, white.
# A woodcut: white paper, black trunks receding in perspective with knife-cut bark hatching,
# green undergrowth, shafts of dawn light cut out of the ground, one fading star.
import os, math, numpy as np
from PIL import Image, ImageDraw
W,H=400,600
BLK,WHT,GRN=(0,0,0),(255,255,255),(30,155,60)
rng=np.random.default_rng(1321)
im=Image.new("RGB",(W,H),WHT); d=ImageDraw.Draw(im)

# --- sky: horizontal knife strokes, denser toward the top (dawn still grey) ---
for y in range(0,300,4):
    density=1-(y/300)            # 1 at top → 0 at horizon
    x=0
    while x<W:
        L=int(rng.integers(6,40)); gap=int(rng.integers(2,10)+ (1-density)*30)
        if rng.random()<density: d.line((x,y,x+L,y),fill=BLK,width=1)
        x+=L+gap

# --- ground: green, with black cut marks (leaf litter / roots) ---
HORIZON=300
d.rectangle((0,HORIZON,W,H),fill=GRN)
for _ in range(900):
    x=rng.integers(0,W); y=rng.integers(HORIZON,H)
    depth=(y-HORIZON)/(H-HORIZON)                 # 0 far → 1 near
    L=int(3+depth*18); ang=rng.normal(0,0.25)
    d.line((x,y,x+L*math.cos(ang),y+L*math.sin(ang)),fill=BLK,width=1+int(depth*2))

# --- light shafts: white wedges through the ground, from a sun low behind the trees ---
SX,SY=290,HORIZON-40
for a in np.linspace(-0.55,0.35,7):
    spread=0.045
    pts=[(SX,SY),(SX+900*math.sin(a-spread),SY+900*math.cos(a-spread)),
         (SX+900*math.sin(a+spread),SY+900*math.cos(a+spread))]
    d.polygon(pts,fill=WHT)
# re-scatter litter on the shafts lightly so they're not dead flat
for _ in range(220):
    x=rng.integers(0,W); y=rng.integers(HORIZON,H)
    if im.getpixel((int(x),int(y)))==WHT and y>HORIZON:
        d.line((x,y,x+6,y+1),fill=GRN,width=1)

# --- trunks: far to near. far ones thin, near ones thick and hatched ---
trunks=[]
for i in range(38):
    depth=rng.random()**1.6                    # bias toward far
    x=rng.uniform(-20,W+20)
    w=3+depth*46
    base=HORIZON+depth*(H-HORIZON+60)          # nearer trunks root lower
    trunks.append((depth,x,w,base))
trunks.sort()
for depth,x,w,base in trunks:
    top=-10
    lean=rng.normal(0,0.02)
    # trunk polygon (slightly tapered, slightly leaning)
    pts=[(x-w/2,base),(x+w/2,base),(x+w*0.38+lean*base,top),(x-w*0.38+lean*base,top)]
    d.polygon(pts,fill=BLK)
    # bark: short white cuts across the trunk, denser near the light
    if w>10:
        y=top+20
        while y<base:
            n=int(rng.integers(1,3))
            for _ in range(n):
                cx=x+rng.uniform(-w*0.3,w*0.3)+lean*y
                L=rng.uniform(w*0.15,w*0.45)
                d.line((cx-L/2,y,cx+L/2,y+rng.uniform(-2,2)),fill=WHT,width=1 if w<24 else 2)
            y+=int(rng.integers(5,11))
    # root flare
    if w>16:
        d.polygon([(x-w/2-w*0.35,base+2),(x-w/2,base-w*0.6),(x-w/2,base+2)],fill=BLK)
        d.polygon([(x+w/2+w*0.35,base+2),(x+w/2,base-w*0.6),(x+w/2,base+2)],fill=BLK)

# --- canopy: black mass at the top with ragged lower edge, so the sky is only glimpsed ---
for x in range(0,W,6):
    h=int(40+60*abs(math.sin(x*0.035))+rng.integers(0,25))
    d.rectangle((x,0,x+6,h),fill=BLK)
    d.polygon([(x,h),(x+6,h),(x+3,h+rng.integers(6,22))],fill=BLK)

# --- the one star: the morning star, still visible in a gap ---
sx,sy=286,150
d.ellipse((sx-3,sy-3,sx+3,sy+3),fill=WHT)
for a in (0,math.pi/2):
    d.line((sx-8*math.cos(a),sy-8*math.sin(a),sx+8*math.cos(a),sy+8*math.sin(a)),fill=WHT,width=1)

im.save(os.environ["OUT_RAW"])
