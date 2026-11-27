#!/usr/bin/env python3
"""Check 1: the two inner solvers agree (numerical test of the clipping lemma T6 and of Lemma T7), and the headline numbers."""
import numpy as np, time
from tv_lib import *
t0 = time.time()
M = Model(curie_weiss(1.5, 0.0), 1.0)
rng = np.random.default_rng(11)
print("== A. fast (clipping, v) against slow (generic convex programme per exit type, I): random profiles, two-phase model")
worst = 0
for trial in range(14):
    k = int(rng.integers(2, 5))
    lam = rng.dirichlet(np.ones(k) * 2); mu = rng.uniform(0.05, 0.95, k)
    e = float(rng.choice([-0.02, 0.0, 0.01, 0.03]))
    B = e + alpha(M, lam, mu)
    if B < float(M.v((lam * mu).sum())):
        continue
    f = r_fast(M, lam, mu, B); s, arg = r_slow(M, lam, mu, B, nk=300)
    # refine the slow one around its best exit type
    if arg is not None:
        kp = arg[0]; s2, _ = r_slow(M, lam, mu, B, kgrid=np.linspace(max(kp - 0.004, 1e-4), min(kp + 0.004, 1 - 1e-4), 81)); s = min(s, s2)
    worst = max(worst, abs(f - s))
    print(f"   k={k} e={e:+.2f}  fast {f:.7f}  slow {s:.7f}  diff {f-s:+.1e}   [{time.time()-t0:.0f}s]", flush=True)
print(f"   worst |fast - slow| = {worst:.1e}")
