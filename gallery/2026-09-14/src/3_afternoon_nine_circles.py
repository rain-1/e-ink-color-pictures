# Afternoon — "Nine Circles" (Inferno). Palette: black, red — two colours only.
# A raymarched heightfield: a funnel of nine concentric terraces, each dropping deeper,
# seen from above the rim. Lit from a low sun so the terrace walls throw shadows.
# Depth fog goes to black. Tone is carried entirely by ordered dither (a printer's screen).
import os, numpy as np
from PIL import Image
W,H=400,600
def height(x,z):
    """terrain height at (x,z). Nine steps down toward the centre, with a narrow shaft at the bottom."""
    r=np.sqrt(x*x+z*z)
    step=np.clip(np.floor((r-0.6)/0.9),-1,8)        # ring index 0..8 (outer rim = 8), -1 = the pit
    h=-1.0*(8-step)                                  # each ring 1 unit lower toward centre
    h=np.where(step<0,-14.0,h)
    # a shallow ridge on each terrace so it doesn't read as a perfect cylinder
    h=h+0.08*np.sin(r*14)*(step>=0)
    # a low rim wall at the outer edge
    h=np.where(r>8.4,1.2,h)
    return h
def rm(o,d,steps=220,dt=0.09):
    """march rays o+d*t until they dip below the heightfield; returns hit point & mask"""
    t=np.full(d.shape[:-1],0.0); hit=np.zeros(d.shape[:-1],bool)
    p=o+d*t[...,None]
    for _ in range(steps):
        p=o+d*t[...,None]
        h=height(p[...,0],p[...,2])
        below=p[...,1]<h
        newly=below&~hit
        hit|=newly
        t=np.where(hit,t,t+dt*np.maximum(0.5,(p[...,1]-h)))   # adaptive: bigger steps when high above
    return o+d*t[...,None],hit,t
# camera: above and behind the rim, looking down into the funnel
cam=np.array([0.0,7.0,-5.0]); target=np.array([0.0,-8.0,0.8])
fwd=target-cam; fwd/=np.linalg.norm(fwd)
right=np.cross(fwd,[0,1,0]); right/=np.linalg.norm(right); up=np.cross(right,fwd)
ys,xs=np.mgrid[0:H,0:W]
u=(xs+0.5)/W*2-1; v=1-(ys+0.5)/H*2
aspect=W/H
d=fwd[None,None,:]+ (u*aspect*1.05)[...,None]*right + (v*1.05)[...,None]*up
d/=np.linalg.norm(d,axis=-1,keepdims=True)
P,hit,t=rm(cam[None,None,:],d)
# normal by finite differences
e=0.05
hx=height(P[...,0]+e,P[...,2])-height(P[...,0]-e,P[...,2])
hz=height(P[...,0],P[...,2]+e)-height(P[...,0],P[...,2]-e)
N=np.stack([-hx,2*e*np.ones_like(hx),-hz],-1); N/=np.linalg.norm(N,axis=-1,keepdims=True)
light=np.array([-0.6,0.5,-0.4]); light/=np.linalg.norm(light)
diff=np.clip((N*light).sum(-1),0,1)
# shadow ray toward the light
Ps,hs,_=rm(P+N*0.05,np.broadcast_to(light,P.shape),steps=90,dt=0.12)
lit=~hs
tone=(0.12+0.88*diff*lit)
# fog with depth (deeper = darker), plus the pit itself is black
depth=np.clip((2.0-P[...,1])/20,0,1)
tone=tone*(1-depth)**1.2
tone=np.where(hit,tone,0.0)      # sky above the rim is black (it's underground)
# --- two-colour ordered dither done here, on tone, with an 8x8 Bayer screen ---
b8=np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],
             [60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],
             [15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]])/64.0
thr=np.tile(b8,(H//8+1,W//8+1))[:H,:W]
red=np.clip(tone,0,1)**0.8>thr
img=np.zeros((H,W,3),np.uint8); img[red]=(224,27,36)
# the one star: a single red pinprick straight up through the shaft... no — two colours, no white.
# Instead the star is the pit itself seen as a negative: leave the centre pure black.
Image.fromarray(img).save(os.environ["OUT_RAW"])
