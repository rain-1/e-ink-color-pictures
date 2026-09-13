# Afternoon — "Two O'Clock Table". A tiny numpy raytracer: four spheres on a plane,
# hard afternoon light, long shadows. Rendered in full colour then Floyd–Steinberg dithered.
import os, numpy as np
from PIL import Image
W,H=400,600
# scene: spheres (center, radius, colour)
spheres=[((-1.1,0.7,4.2),0.7,(0.95,0.15,0.15)),
         (( 0.9,0.5,3.4),0.5,(0.10,0.30,0.85)),
         (( 0.2,0.35,2.6),0.35,(0.95,0.85,0.05)),
         ((-0.3,1.0,6.5),1.0,(0.15,0.65,0.25))]
plane_y=0.0
light=np.array([3.0,4.0,-1.0]); light/=np.linalg.norm(light)
aspect=W/H
ys,xs=np.mgrid[0:H,0:W]
u=(xs+0.5)/W*2-1; v=1-(ys+0.5)/H*2
dirs=np.stack([u*aspect*0.9, v*0.9 + 0.05, np.ones_like(u)*1.4],-1)
dirs/=np.linalg.norm(dirs,axis=-1,keepdims=True)
orig=np.array([0.0,1.3,0.0])
def hit_spheres(o,d):
    best=np.full(d.shape[:-1],np.inf); idx=np.full(d.shape[:-1],-1)
    for i,(c,r,_) in enumerate(spheres):
        oc=o-np.array(c); b=(d*oc).sum(-1); cc=(oc*oc).sum(-1)-r*r
        disc=b*b-cc; ok=disc>0
        t=-b-np.sqrt(np.where(ok,disc,0))
        m=ok&(t>1e-3)&(t<best); best=np.where(m,t,best); idx=np.where(m,i,idx)
    return best,idx
t,idx=hit_spheres(orig[None,None,:],dirs)
# plane
tp=(plane_y-orig[1])/dirs[...,1]; mp=(dirs[...,1]<0)&(tp>0)&(tp<t)
t=np.where(mp,tp,t); idx=np.where(mp,99,idx)
tt=np.where(np.isfinite(t),t,0)
P=orig+dirs*tt[...,None]
col=np.zeros((H,W,3)); col[:]=[1.0,1.0,1.0]  # sky: pure white so it doesn't dither
# normals & base colours
N=np.zeros_like(P); base=np.zeros_like(P)
for i,(c,r,k) in enumerate(spheres):
    m=idx==i; N[m]=(P[m]-np.array(c))/r; base[m]=k
m=idx==99; N[m]=[0,1,0]
# checker floor: white / pale
chk=((np.floor(P[...,0]*1.2)+np.floor(P[...,2]*1.2))%2)==0
base[m]=np.where(chk[m][:,None],[1.0,1.0,1.0],[0.05,0.05,0.05])
# shadows
sh_o=P+N*1e-3; sh_d=np.broadcast_to(light,P.shape)
st,si=hit_spheres(sh_o,sh_d); lit=~np.isfinite(st)
diff=np.clip((N*light).sum(-1),0,1)*lit
shade=base*(0.18+0.95*diff)[...,None]
shade[idx==99]=np.where(lit[idx==99][:,None],base[idx==99]*1.0+0.0,base[idx==99]*0.0+0.08)  # floor: flat, shadows go black
hitm=idx>=0
col[hitm]=shade[hitm]
img=(np.clip(col,0,1)**(1/1.8)*255).astype(np.uint8)
Image.fromarray(img).save(os.environ["OUT_RAW"])
