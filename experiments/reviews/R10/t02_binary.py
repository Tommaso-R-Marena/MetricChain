"""binary optimum and the S3 family at bJ=1.5, B=0, u=1; three inner solvers at each optimum."""
import time, sys
import numpy as np
from r10lib import *
from r10search import *
t0 = time.time()
M = Model(bJ=1.5, bB=0.0, u=1.0)
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)
for e, ref in ((0.0, 0.0251012), (0.02, 0.0152765), (0.05, 0.0046265), (-0.05, 0.0575961)):
    best = (-1, None, None)
    for (m, a, b) in ((0.5, 0.3, 0.3), (0.45, 0.32, 0.28), (0.5, 0.27, 0.27), (0.55, 0.25, 0.35)):
        lam, mu = binary(m, a, b)
        val, l2, m2 = nm(M, e, lam, mu)
        if val > best[0]:
            best = (val, l2, m2)
    val, lam, mu = best
    B = e + alpha(M, lam, mu)
    s1 = inner_clip(M, lam, mu, B, **fine)[0]
    s2, k2, loc = inner_dual(M, lam, mu, B, nk=2001, refine=5)
    s3 = inner_primal(M, lam, mu, B, nstart=60)[0]
    print(f"e={e:+.3f} binary: search {val:.9f} [{fmt(lam, mu)}]  S1fine {s1:.9f} S2 {s2:.9f} S3 {s3:.9f}  report {ref}  exits {[(round(a,4), round(b,7)) for a,b in loc[:3]]}", flush=True)
# S3 family: (lf, x)
def s3prof(lf, x):
    return np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x, 0.5, x])
for e, ref in ((0.02, 0.0161548), (0.002, 0.0240419), (0.0, 0.0249932)):
    f = lambda z: -r_mu(M, *s3prof(z[0], z[1]), e)
    res = optimize.minimize(f, [0.14, 0.275], method='Nelder-Mead', options={'xatol': 1e-8, 'fatol': 1e-13})
    lam, mu = s3prof(*res.x)
    B = e + alpha(M, lam, mu)
    s1 = inner_clip(M, lam, mu, B, **fine)[0]
    s2, k2, loc = inner_dual(M, lam, mu, B, nk=2001, refine=5)
    s3 = inner_primal(M, lam, mu, B, nstart=60)[0]
    print(f"e={e:+.3f} S3 family: lf={res.x[0]:.5f} x={res.x[1]:.5f} search {-res.fun:.9f}  S1fine {s1:.9f} S2 {s2:.9f} S3 {s3:.9f}  report {ref} exits {[(round(a,4), round(b,7)) for a,b in loc[:4]]}", flush=True)
print("time", time.time() - t0)
