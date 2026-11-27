"""SLP ascent from random multi-atom profiles + Nelder-Mead polish; bJ, bB, u, e, seed, nstart on the command line.
usage: python3 t04_slp_search.py bJ bB u e seed nstart [tlimit]"""
import time, sys
import numpy as np
from r10lib import *
from r10search import *
from r10slp import *
bJ, bB, u, e = (float(x) for x in sys.argv[1:5])
seed, nstart = int(sys.argv[5]), int(sys.argv[6])
tlimit = float(sys.argv[7]) if len(sys.argv) > 7 else 540.0
t0 = time.time()
M = Model(bJ=bJ, bB=bB, u=u)
phip = (lambda k: -2 * bJ * (2 * k - 1) - 2 * bB) if bJ >= 0 else None
rng = np.random.default_rng(seed)
print(f"# bJ={bJ} bB={bB} u={u} e={e} seed={seed}; contact set {[(round(a,4), round(b,4)) for a,b in M.contact()]}", flush=True)
results = []
for s in range(nstart):
    if time.time() - t0 > tlimit:
        break
    k = int(rng.integers(2, 7))
    lam = rng.dirichlet(np.ones(k))
    mode = s % 4
    if mode == 0:
        mu = rng.random(k)
    elif mode == 1:
        mu = np.clip(0.5 + 0.25 * rng.standard_normal(k), 0.02, 0.98)
    elif mode == 2:
        mu = np.sort(rng.random(k)) * 0.6 + 0.2
    else:
        mu = rng.beta(0.6, 0.6, size=k)
    v0 = r_mu(M, lam, mu, e)
    val, l1, m1, hist = slp(M, lam, mu, e, phip)
    l2, m2 = coarsen(l1, m1)
    v2 = r_mu(M, l2, m2, e)
    if len(m2) <= 7 and np.isfinite(v2):
        v3, l3, m3 = nm(M, e, l2, m2, maxiter=1500)
    else:
        v3, l3, m3 = v2, l2, m2
    if not (v3 >= val):
        v3, l3, m3 = val, l1, m1
    results.append((v3, l3, m3))
    print(f"start {s:3d} k={k} v0={v0:.7f} slp={val:.8f} ({len(m1)} atoms, {len(hist)-1} its) coarse={v2:.8f} polished={v3:.9f} [{fmt(l3, m3)}] t={time.time()-t0:.0f}", flush=True)
results.sort(key=lambda r: -r[0])
print("# best:")
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)
for v3, l3, m3 in results[:3]:
    B = e + alpha(M, l3, m3)
    s1 = inner_clip(M, l3, m3, B, **fine)[0]
    s2, k2, loc = inner_dual(M, l3, m3, B, nk=1201, refine=5)
    s3 = inner_primal(M, l3, m3, B, nstart=40)[0]
    print(f"  {v3:.9f} [{fmt(l3, m3)}] mean {float(l3@m3):.5f}  S1fine {s1:.9f} S2(dual, I) {s2:.9f} S3(primal, I) {s3:.9f}", flush=True)
print("# time", time.time() - t0)
