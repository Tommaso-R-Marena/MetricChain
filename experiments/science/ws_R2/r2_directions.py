#!/usr/bin/env python3
"""R2 — "about two thirds of all directions": fraction of directions c whose maximiser over K1 (resp. K2)
is one of the three proved vertices (0,0,0), (1/2,2,3/2), (1,5,6).  The number depends on the measure on
directions; three choices are reported: (a) the authors' c=(9d1,4d2,d3), d uniform on the sphere;
(b) c uniform on the sphere in p-coordinates; (c) uniform on the sphere in the dual of the u-coordinates."""
import numpy as np
V1=np.array([(0,0,0),(0,0,2),(0,1,4),(0,2,2),(0,2,4.5),(0,3,4),(0,3,4.5),(1/3,3,8/3),(1/3,11/3,4),(.5,2,1.5),(.5,2,3),(1,5,6)])
V2=np.array([(0,0,0),(0,0,2),(0,1,4),(0,2,2),(0,2,4.5),(0,3,4),(0,3,4.5),(.5,2,1.5),(.5,2,3),(.5,3.5,3.5),(.5,4,4.5),(1,5,6)])
good=[(0,0,0),(.5,2,1.5),(1,5,6)]
rng=np.random.default_rng(1)
d=rng.normal(size=(400000,3)); d/=np.linalg.norm(d,axis=1)[:,None]
U=np.array([[5,0,0],[3,3,0],[1,1,1]],float)
for name,C in (("(a) c=(9d1,4d2,d3)",d*np.array([9,4,1])),("(b) c uniform in p-coordinates",d),("(c) c = U^T d (uniform in the dual of u)",d@U)):
    out=[]
    for V in (V1,V2):
        idx=(C@V.T).argmax(1)
        isgood=np.array([tuple(v) in good for v in V])
        out.append(isgood[idx].mean())
    print(f"{name}: fraction with a proved vertex as maximiser: K1 {out[0]:.3f}, K2 {out[1]:.3f}")
