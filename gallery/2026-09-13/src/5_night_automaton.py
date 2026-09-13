# Night — "Rule 30, Blue". A one-dimensional cellular automaton grown from a single seed,
# blue cells on black, a few white cells where three neighbours agree. Coarse 10px cells.
import os, numpy as np
from PIL import Image
W,H=400,600; C=10; cols,rows=W//C,H//C
rule=30; table=[(rule>>i)&1 for i in range(8)]
grid=np.zeros((rows,cols),np.uint8); grid[0,cols//2]=1
for r in range(1,rows):
    p=grid[r-1]; l=np.roll(p,1); rr=np.roll(p,-1)
    grid[r]=[table[(a<<2)|(b<<1)|c] for a,b,c in zip(l,p,rr)]
img=np.zeros((rows,cols,3),np.uint8)
img[grid==1]=(18,61,176)
# white "stars": cells whose row above was fully lit around them
dense=np.zeros_like(grid)
dense[1:,1:-1]=grid[:-1,:-2]&grid[:-1,1:-1]&grid[:-1,2:]
img[(grid==1)&(dense==1)]=(255,255,255)
# thin yellow moon in the top-left dark
out=Image.fromarray(np.kron(img,np.ones((C,C,1),np.uint8)))
from PIL import ImageDraw
d=ImageDraw.Draw(out)
d.ellipse((40,60,120,140),fill=(245,212,0)); d.ellipse((62,52,142,132),fill=(0,0,0))
out.save(os.environ["OUT_RAW"])
