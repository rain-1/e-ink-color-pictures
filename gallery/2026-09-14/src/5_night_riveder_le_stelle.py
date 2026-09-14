# Night — "E quindi uscimmo a riveder le stelle" (Inferno XXXIV, last line). Palette: black, white.
# A star chart of the mid-September evening sky as seen from Italy: the Summer Triangle
# (Vega, Deneb, Altair) with Cygnus, Lyra and Aquila drawn in, the Milky Way as stipple,
# a faint RA/Dec grid, and at the foot two small figures stepping out of a black cleft.
# Approximate catalogue positions (RA hours, Dec degrees, visual magnitude), from memory.
import os, math, numpy as np
from PIL import Image, ImageDraw
W,H=400,600; rng=np.random.default_rng(1300)
BLK,WHT=(0,0,0),(255,255,255)
stars={ # name: (RA h, Dec °, mag)
 "Vega":(18.62,38.78,0.0),"Deneb":(20.69,45.28,1.25),"Altair":(19.85,8.87,0.77),
 "Sadr":(20.37,40.26,2.2),"Albireo":(19.51,27.96,3.1),"Gienah":(20.77,33.97,2.5),"DeltaCyg":(19.75,45.13,2.9),
 "Sheliak":(18.83,33.36,3.5),"Sulafat":(18.98,32.69,3.2),"ZetaLyr":(18.75,37.6,4.3),"DeltaLyr":(18.9,36.9,4.3),
 "Tarazed":(19.77,10.61,2.7),"Alshain":(19.92,6.41,3.7),"DeltaAql":(19.42,3.11,3.4),"ZetaAql":(19.09,13.86,3.0),
 "ThetaAql":(20.19,-0.82,3.2),"LambdaAql":(19.1,-4.88,3.4),
 "Rasalhague":(17.58,12.56,2.1),"Enif":(21.74,9.87,2.4),"Sadalmelik":(22.1,-0.32,2.9),"Alderamin":(21.31,62.59,2.5),
 "Kappa Cyg":(19.28,53.37,3.8),"Iota Cyg":(19.5,51.73,3.8),
}
lines=[("Deneb","Sadr"),("Sadr","Gienah"),("Sadr","DeltaCyg"),("Sadr","Albireo"),       # Cygnus cross
       ("Vega","Sheliak"),("Vega","ZetaLyr"),("ZetaLyr","DeltaLyr"),("DeltaLyr","Sulafat"),("Sulafat","Sheliak"),("ZetaLyr","Sheliak"), # Lyra
       ("Altair","Tarazed"),("Altair","Alshain"),("Altair","DeltaAql"),("DeltaAql","ZetaAql"),("Altair","ThetaAql"),("DeltaAql","LambdaAql"), # Aquila
       ("Vega","Deneb"),("Deneb","Altair"),("Altair","Vega")]   # the Triangle, dashed
# projection: stereographic, centre RA 19.7h, Dec +30
RA0,DE0=19.7,30.0; scale=560
def proj(ra,dec):
    lam=math.radians((ra-RA0)*15); phi=math.radians(dec); phi0=math.radians(DE0)
    k=2/(1+math.sin(phi0)*math.sin(phi)+math.cos(phi0)*math.cos(phi)*math.cos(lam))
    x=k*math.cos(phi)*math.sin(lam); y=k*(math.cos(phi0)*math.sin(phi)-math.sin(phi0)*math.cos(phi)*math.cos(lam))
    return W/2 - x*scale/2, H/2+40 - y*scale/2      # east to the left, as on a real chart
im=Image.new("RGB",(W,H),BLK); d=ImageDraw.Draw(im)
# grid: RA every hour, Dec every 10°, thin dotted
for ra in np.arange(16,24,1.0):
    pts=[proj(ra,dec) for dec in np.arange(-20,75,2)]
    for i,((x0,y0),(x1,y1)) in enumerate(zip(pts,pts[1:])):
        if i%4==0: d.line((x0,y0,x1,y1),fill=WHT,width=1)
for dec in range(-10,71,10):
    pts=[proj(ra,dec) for ra in np.arange(16,24,0.1)]
    for i,((x0,y0),(x1,y1)) in enumerate(zip(pts,pts[1:])):
        if i%3==0: d.line((x0,y0,x1,y1),fill=WHT,width=1)
# Milky Way: a broad stipple band running roughly Aquila → Cygnus → Cepheus, wider near Cygnus
for _ in range(9000):
    t=rng.random()
    ra=17.9+t*4.2; dec=-8+t*70+rng.normal(0,7*(0.6+t))
    x,y=proj(ra,dec)
    if 0<=x<W and 0<=y<H and rng.random()<0.55:
        im.putpixel((int(x),int(y)),WHT)
# background faint stars
for _ in range(700):
    x,y=rng.integers(0,W),rng.integers(0,H)
    im.putpixel((int(x),int(y)),WHT)
# constellation lines: solid; the Triangle dashed
def dash(x0,y0,x1,y1,on=5,off=6):
    L=math.hypot(x1-x0,y1-y0); n=int(L/(on+off)); ux,uy=(x1-x0)/L,(y1-y0)/L
    for i in range(n+1):
        s=i*(on+off); d.line((x0+ux*s,y0+uy*s,x0+ux*min(s+on,L),y0+uy*min(s+on,L)),fill=WHT,width=1)
for a,b in lines:
    (x0,y0),(x1,y1)=proj(*stars[a][:2]),proj(*stars[b][:2])
    if (a,b) in [("Vega","Deneb"),("Deneb","Altair"),("Altair","Vega")]: dash(x0,y0,x1,y1)
    else: d.line((x0,y0,x1,y1),fill=WHT,width=1)
# stars by magnitude: disc radius from brightness, with a black gap ring so lines don't touch
for name,(ra,dec,mag) in stars.items():
    x,y=proj(ra,dec); r=max(1.2,6.5-mag*1.5)
    d.ellipse((x-r-2,y-r-2,x+r+2,y+r+2),fill=BLK)
    d.ellipse((x-r,y-r,x+r,y+r),fill=WHT)
    if mag<1.5:  # the three bright ones get four spikes and a label
        for ang in (0,math.pi/2):
            d.line((x-(r+7)*math.cos(ang),y-(r+7)*math.sin(ang),x+(r+7)*math.cos(ang),y+(r+7)*math.sin(ang)),fill=WHT,width=1)
        d.text((x+9,y-6),name.upper(),fill=WHT)
# the one star: Vega, brightest, gets a small ring (the "stelle" of the title)
x,y=proj(*stars["Vega"][:2]); d.ellipse((x-12,y-12,x+12,y+12),outline=WHT,width=1)
# foot: black ground with a cleft; two figures (one taller with a staff, one shorter) stepping up out of it
d.rectangle((0,520,W,H),fill=BLK)
# a faint horizon of white marks — grass — so the ground reads
for _ in range(90):
    x=rng.integers(0,W); d.line((x,520,x+rng.integers(-2,3),520-rng.integers(3,9)),fill=WHT,width=1)
def figure(x,base,h,staff=False):
    d.ellipse((x-h*0.09,base-h,x+h*0.09,base-h*0.82),fill=WHT)
    d.polygon([(x-h*0.13,base-h*0.78),(x+h*0.13,base-h*0.78),(x+h*0.18,base),(x-h*0.18,base)],fill=WHT)
    if staff: d.line((x+h*0.24,base-h*1.05,x+h*0.24,base),fill=WHT,width=2)
figure(228,522,46,staff=True); figure(252,530,38)
# title, small, bottom
d.text((14,568),"E QUINDI USCIMMO A RIVEDER LE STELLE",fill=WHT)
d.text((14,582),"Inf. XXXIV · the sky over Ravenna, 14 IX, 22h",fill=WHT)
im.save(os.environ["OUT_RAW"])
