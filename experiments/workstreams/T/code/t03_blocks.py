#!/usr/bin/env python3
"""t03 -- is a binary centre enough?  sup over block profiles with k = 3, 4 blocks of
       V(mu, e + alpha(mu); v) = min{ MI(nu) : u dist(nu,mu) + v(kappa(nu)) <= e + alpha(mu) }
against the binary value.  Global search: differential evolution (fixed seed) + Nelder-Mead polish from (i) the DE
result, (ii) the binary optimum split into k blocks and perturbed.  Every reported value is re-evaluated with a fine
inner solver (ng = 2001).
usage: python3 t03_blocks.py bJ bB u e k [seed] [maxiter]
"""
import sys, time, math
import numpy as np
from scipy.optimize import differential_evolution, minimize
import tlib as T

bJ, bB, u, e, k = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 1
maxiter = int(sys.argv[7]) if len(sys.argv) > 7 else 120
t0 = time.time()
K = T.Known(T.phi_cw(bJ, bB), u)
lam = K.v
print(f"bJ={bJ} bB={bB} u={u} e={e} k={k} seed={seed}; contact set {K.contact_pieces()}")

Rb, argb = T.R_bin(K, e, lam, nrand=3)
lb, mb = T.bin_blocks(*argb)
Rb_fine = T.obj_blocks(K, e, lam, lb, mb, ng=2001, zoom=6)
print(f"binary optimum: R = {Rb:.9f} (fine inner solver {Rb_fine:.9f}) at (m,a,b) = ({argb[0]:.6f},{argb[1]:.6f},{argb[2]:.6f})  [{time.time()-t0:.0f}s]", flush=True)


def unpack(x):
    """x in [0,1]^(2k-1): stick-breaking weights, block types"""
    s = x[:k - 1]
    lams = np.empty(k)
    rest = 1.0
    for j in range(k - 1):
        lams[j] = rest * s[j]
        rest *= (1.0 - s[j])
    lams[k - 1] = rest
    return lams, np.asarray(x[k - 1:], dtype=float)


def f(x):
    x = np.clip(x, 0.0, 1.0)
    lams, mus = unpack(x)
    if lams.min() < 1e-6:
        return 0.0
    return -T.obj_blocks(K, e, lam, lams, mus)


def pack(lams, mus):
    s = []
    rest = 1.0
    for j in range(k - 1):
        s.append(lams[j] / rest if rest > 0 else 0.5)
        rest -= lams[j]
    return np.r_[np.clip(s, 1e-6, 1 - 1e-6), mus]


best = (Rb_fine, lb, mb, "binary")
rng = np.random.default_rng(seed)

# (ii) binary optimum split into k blocks, perturbed
for trial in range(6):
    if k == 3:
        w = rng.uniform(0.2, 0.8)
        which = trial % 2
        if which == 0:
            lams = np.array([lb[0] * w, lb[0] * (1 - w), lb[1]])
            mus = np.array([mb[0], mb[0], mb[1]])
        else:
            lams = np.array([lb[0], lb[1] * w, lb[1] * (1 - w)])
            mus = np.array([mb[0], mb[1], mb[1]])
    else:
        w1, w2 = rng.uniform(0.2, 0.8, 2)
        lams = np.array([lb[0] * w1, lb[0] * (1 - w1), lb[1] * w2, lb[1] * (1 - w2)])
        mus = np.array([mb[0], mb[0], mb[1], mb[1]])
    mus = np.clip(mus + rng.normal(0, 0.04, k), 0.001, 0.999)
    x0 = pack(lams, mus)
    r = minimize(f, x0, method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-12, "maxiter": 2500})
    r = minimize(f, r.x, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-13, "maxiter": 1500})
    lams, mus = unpack(np.clip(r.x, 0, 1))
    val = T.obj_blocks(K, e, lam, lams, mus, ng=2001, zoom=6)
    print(f"  split start {trial}: NM -> {-r.fun:.9f}, fine {val:.9f};  lams {np.round(lams,5)}, mus {np.round(mus,5)}  [{time.time()-t0:.0f}s]", flush=True)
    if val > best[0]:
        best = (val, lams, mus, f"split{trial}")

# (i) differential evolution
res = differential_evolution(f, bounds=[(1e-3, 1 - 1e-3)] * (k - 1) + [(0.0, 1.0)] * k, seed=seed, maxiter=maxiter, popsize=14,
                             tol=1e-10, polish=False, init="sobol")
r = minimize(f, res.x, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-13, "maxiter": 2500})
lams, mus = unpack(np.clip(r.x, 0, 1))
val = T.obj_blocks(K, e, lam, lams, mus, ng=2001, zoom=6)
print(f"  differential evolution: {-res.fun:.9f} -> NM {-r.fun:.9f}, fine {val:.9f};  lams {np.round(lams,5)}, mus {np.round(mus,5)}  [{time.time()-t0:.0f}s]", flush=True)
if val > best[0]:
    best = (val, lams, mus, "DE")

print(f"RESULT bJ={bJ} bB={bB} u={u} e={e} k={k}: best over {k} blocks = {best[0]:.9f} ({best[3]});  binary = {Rb_fine:.9f};  gain = {best[0]-Rb_fine:+.2e}")
print(f"   lams = {np.round(best[1],6)}, mus = {np.round(best[2],6)}")
print(f"time {time.time()-t0:.0f}s")
