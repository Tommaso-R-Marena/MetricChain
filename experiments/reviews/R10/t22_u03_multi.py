"""bJ = 1.5, B = 0, u = 0.30, e = 0: is the binary barrier shell (0.0022646, a marginal shell) the best
profile?  Alternating SLP / Nelder-Mead from shells perturbed by finite masses and from free-block
profiles; re-evaluation with S1(fine), S2, S3.  (The report: one 3-block search returned the binary shell.)"""
import time, sys
import numpy as np
from r10lib import *
from r10search import *
from r10slp import *
t0 = time.time()
u, e = 0.30, float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
bJ = 1.5
M = Model(bJ, 0.0, u)
phip = lambda k: -2 * bJ * (2 * k - 1)
rng = np.random.default_rng(12)
starts = [("shell 0.4409", binary(0.5, 0.44091, 0.44091)), ("shell 0.445", binary(0.5, 0.445, 0.445)), ("shell 0.4514", binary(0.5, 0.4514, 0.4514))]
for lf in (0.05, 0.14, 0.3):
    for x in (0.435, 0.442, 0.45):
        starts.append((f"free block lf={lf} x={x}", (np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x, 0.5, x]))))
for s in range(12):
    k = int(rng.integers(3, 6))
    lam = rng.dirichlet(np.ones(k) * 2)
    mu = np.clip(0.5 + rng.choice([-1, 1], size=k) * (0.05 + 0.02 * rng.random(k)), 0.02, 0.98)
    starts.append((f"random{s}", (lam, mu)))
results = []
for name, (lam, mu) in starts:
    if time.time() - t0 > 480:
        break
    cur = r_mu(M, lam, mu, e)
    cur = cur if np.isfinite(cur) else -1.0
    v0 = cur
    for cycle in range(3):
        val, l1, m1, hist = slp(M, lam, mu, e, phip, nM=801)
        cand = [(val, l1, m1)]
        l2, m2 = coarsen(l1, m1, tol=0.002)
        v2 = r_mu(M, l2, m2, e)
        if np.isfinite(v2):
            cand.append((v2, l2, m2))
            if len(m2) <= 6:
                cand.append(nm(M, e, l2, m2, maxiter=300 * len(m2), step=0.01))
        best = max(cand, key=lambda c: c[0] if np.isfinite(c[0]) else -1)
        if not np.isfinite(best[0]) or best[0] <= cur + 1e-10:
            break
        cur, lam, mu = best
    results.append((cur, lam, mu, name))
    print(f"{name:26s} v0={v0:.8f} -> {cur:.9f} [{fmt(lam, mu)}] t={time.time()-t0:.0f}", flush=True)
results.sort(key=lambda r: -r[0])
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)
print("# best three re-evaluated (binary barrier shell: 0.0022646)")
for v, l, m, name in results[:3]:
    B = e + alpha(M, l, m)
    s1 = inner_clip(M, l, m, B, **fine)[0]
    s2, k2, loc = inner_dual(M, l, m, B, nk=2001, refine=5)
    s3 = inner_primal(M, l, m, B, nstart=40)[0]
    print(f"  {name}: {v:.9f} [{fmt(l, m)}]  S1fine {s1:.9f}  S2(dual, I) {s2:.9f}  S3(primal, I) {s3:.9f}", flush=True)
print("time", time.time() - t0)
