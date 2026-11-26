#!/usr/bin/env python3
"""probe: the one two-torsion case of t3c_linear_images_run1.log in which LM found 7 of the 8 predicted images
(n = 16, hinges [3, 8]) and the short-segment case hinges [1, 8]: hits per predicted point with 3000 starts."""
import numpy as np, time
import r22lib as L
import importlib.util, sys
t0 = time.time()
# re-create the same instances by replaying the random stream of t3c_linear_images.py is fragile; build fresh ones instead
COS = -1.0/3.0
def rot(axis, ang):
    a = axis/np.linalg.norm(axis); K = np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]])
    return np.eye(3)+np.sin(ang)*K+(1-np.cos(ang))*(K@K)
from scipy.optimize import least_squares
def enum(z, nstart, rng, tol=1e-9):
    n, m = z.shape; Ed = np.array([z[j]-z[i] for i,j in L.E0(n)]); l2 = (Ed**2).sum(1)
    res = lambda a: ((Ed@a.reshape(3,m).T)**2).sum(1)/l2-1.0
    def jac(a):
        AE = Ed@a.reshape(3,m).T
        return (2.0*AE[:,:,None]*Ed[:,None,:]/l2[:,None,None]).reshape(len(Ed),3*m)
    found=[]; nconv=0
    for s in range(nstart):
        a0 = rng.normal(size=3*m)*rng.uniform(0.3,2.5)
        sol = least_squares(res,a0,jac=jac,method="lm",xtol=1e-15,ftol=1e-15,gtol=1e-15,max_nfev=4000)
        if np.abs(sol.fun).max()>tol: continue
        nconv+=1; Dx = L.sqdist(z@sol.x.reshape(3,m).T)
        for f in found:
            if np.abs(f[0]-Dx).max()<1e-5: f[1]+=1; break
        else: found.append([Dx,1])
    return found, nconv
def rehinge(X1, hinges, rhos):
    X = X1.copy(); B = np.eye(3)
    for h, rho in zip(hinges, rhos):
        p = h+1; B = B@rho; X[p:] = X[p]+(X1[p:]-X1[p])@B.T
    return X
W=(0.37,0.63)
for seed,(n,hinges) in ((1,(16,[3,8])),(2,(16,[3,8])),(3,(16,[3,8])),(4,(16,[1,8])),(5,(16,[1,8])),(6,(18,[4,10]))):
    rng = np.random.default_rng(1000+seed)
    th = rng.uniform(0.5,2.6,2)*rng.choice([-1,1],2)
    t1 = rng.uniform(-np.pi,np.pi,n-3); t2=t1.copy(); t2[hinges[0]]+=th[0]; t2[hinges[1]]+=th[1]
    X1,X2 = L.chain(t1,COS),L.chain(t2,COS); z = L.stack([X1,X2],W)
    b=[X1[h+2]-X1[h+1] for h in hinges]; e=np.cross(b[0],b[1]); e/=np.linalg.norm(e); s=np.eye(3)-2*np.outer(e,e)
    R1,R2=rot(b[0],th[0]),rot(b[1],th[1]); I3=np.eye(3)
    pred=[(I3,I3),(R1,R2),(R1,s),(I3,s@R2),(s,R2),(R1@s,I3),(R1@s,s@R2),(s,s)]
    DY=[L.sqdist(rehinge(X1,hinges,rr)) for rr in pred]
    sep = min(np.abs(DY[a]-DY[c]).max() for a in range(8) for c in range(a+1,8))
    found,nconv = enum(z,1500,rng)
    hits=[0]*8; extra=0
    for D,h in found:
        k=[i for i in range(8) if np.abs(D-DY[i]).max()<1e-5]
        if k: hits[k[0]]+=h
        else: extra+=1
    print(f"n={n} hinges={hinges} thetas=({th[0]:+.3f},{th[1]:+.3f}) seg sizes {[hinges[0]+3, hinges[1]-hinges[0]+2, n-1-hinges[1]]}: min separation of predicted D's {sep:.3f}; "
          f"converged {nconv}/1500; hits per predicted point {hits}; images outside the predicted list: {extra}")
print(f"ALL DONE {time.time()-t0:.1f} s")
