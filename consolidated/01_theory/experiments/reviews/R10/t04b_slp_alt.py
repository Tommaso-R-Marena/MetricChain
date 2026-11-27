"""alternating SLP (finite-mass moves on the law of the block types) and Nelder-Mead (continuous
moves of atoms and weights), from structured and random starts; the best profiles are re-evaluated
with S1(fine), S2 (dual per exit type, I) and S3 (primal SLSQP, I).
usage: python3 t04b_slp_alt.py bJ bB u e seed nrandom tlimit [kmax]"""
import time, sys
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
from r10slp import *
bJ, bB, u, e = (float(x) for x in sys.argv[1:5])
seed, nrandom = int(sys.argv[5]), int(sys.argv[6])
tlimit = float(sys.argv[7])
kmax = int(sys.argv[8]) if len(sys.argv) > 8 else 6
t0 = time.time()
M = Model(bJ=bJ, bB=bB, u=u)
phip = (lambda k: -2 * bJ * (2 * k - 1) - 2 * bB) if bJ >= 0 else None
rng = np.random.default_rng(seed)
print(f"# bJ={bJ} bB={bB} u={u} e={e} seed={seed}; R_unif(e) = {R_unif(e,u):.9f}", flush=True)

def sym(atoms, weights):
    """symmetric profile from atoms x_i < 1/2 with weights w_i (each used twice) and a free block"""
    atoms = np.asarray(atoms, float); weights = np.asarray(weights, float)
    return np.concatenate((weights, weights)), np.concatenate((atoms, 1 - atoms))

starts = []
pu = p_u(u)
starts.append(("binary shell", binary(0.5, pu + 0.03, pu + 0.03)))
starts.append(("S3", (np.array([0.43, 0.14, 0.43]), np.array([1 - pu - 0.008, 0.5, pu + 0.008]))))
starts.append(("S4", (np.array([0.396, 0.104, 0.104, 0.396]), np.array([0.273, 0.430, 0.570, 0.727]))))
starts.append(("S5", (np.array([0.36, 0.09, 0.10, 0.09, 0.36]), np.array([0.270, 0.388, 0.5, 0.612, 0.730]))))
starts.append(("S6", (np.array([0.33, 0.09, 0.08, 0.08, 0.09, 0.33]), np.array([0.270, 0.36, 0.45, 0.55, 0.64, 0.730]))))
starts.append(("asym3", (np.array([0.45, 0.14, 0.41]), np.array([0.30, 0.53, 0.75]))))
starts.append(("frozen", (np.array([0.05, 0.45, 0.45, 0.05]), np.array([0.01, 0.29, 0.71, 0.99]))))
for s in range(nrandom):
    k = int(rng.integers(2, kmax + 1))
    lam = rng.dirichlet(np.ones(k))
    mode = s % 3
    mu = rng.random(k) if mode == 0 else (np.clip(0.5 + 0.22 * rng.standard_normal(k), 0.02, 0.98) if mode == 1 else rng.beta(0.7, 0.7, size=k))
    starts.append((f"random{s}", (lam, mu)))
results = []
for name, (lam, mu) in starts:
    if time.time() - t0 > tlimit:
        break
    lam = np.asarray(lam, float) / np.sum(lam)
    cur = r_mu(M, lam, mu, e)
    if not np.isfinite(cur):
        cur = -1.0
    v0 = cur
    for cycle in range(4):
        val, l1, m1, hist = slp(M, lam, mu, e, phip, nM=801)
        cand = [(val, l1, m1)]
        l2, m2 = coarsen(l1, m1, tol=0.003)
        v2 = r_mu(M, l2, m2, e)
        if np.isfinite(v2):
            cand.append((v2, l2, m2))
            if len(m2) <= 8:
                v3, l3, m3 = nm(M, e, l2, m2, maxiter=400 * len(m2))
                cand.append((v3, l3, m3))
        best = max(cand, key=lambda c: c[0])
        if best[0] <= cur + 2e-9:
            if best[0] > cur:
                cur, lam, mu = best
            break
        cur, lam, mu = best
        if time.time() - t0 > tlimit:
            break
    lam, mu = merge(lam, mu, tol=1e-5, wmin=1e-6)
    results.append((cur, lam, mu, name))
    print(f"{name:12s} v0={v0:.7f} -> {cur:.9f} ({cycle+1} cycles) [{fmt(lam, mu)}] mean {float(lam@mu):.4f} t={time.time()-t0:.0f}", flush=True)
results.sort(key=lambda r: -r[0])
print("# best three, re-evaluated:")
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)
for v3, l3, m3, name in results[:3]:
    B = e + alpha(M, l3, m3)
    s1 = inner_clip(M, l3, m3, B, **fine)[0]
    s2, k2, loc = inner_dual(M, l3, m3, B, nk=1201, refine=5)
    s3 = inner_primal(M, l3, m3, B, nstart=40)[0]
    print(f"  {name}: {v3:.9f} [{fmt(l3, m3)}]\n     S1fine {s1:.9f}  S2(dual, I) {s2:.9f}  S3(primal, I) {s3:.9f}  exits {[(round(a,4), round(b,8)) for a,b in loc[:5]]}", flush=True)
print("# time", time.time() - t0)
