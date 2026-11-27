#!/usr/bin/env python3
"""Workstream R27, Item 2 (iii) -- Corollaries L.1 and L.2 on instances (REPLICATION from the statements), and two small side claims.

 L.1: data q = |x_j - x_k|^2 + eps (separation <= 4); ANY Yhat with stress(Yhat) = sum (|yhat_j - yhat_k|^2 - q)^2 <= sum eps^2 satisfies
        d_P(Yhat, X) <= 2.4 (b/(s* tau*)) (n+2)^2 ||eps||_2          [constants of the TRUE configuration X].
 L.2: ANY Yhat with tau*(Yhat) > 0 and ||eps||_2 <= nu:
        d_P(X, Yhat) <= C(Yhat) (||r||_2 + nu),   r = |yhat_j - yhat_k|^2 - q,   C(Yhat) = 1.2 b(Yhat) (n+2)^2/(s*(Yhat) tau*(Yhat))
      -- every quantity on the right is computed here from Yhat, q and nu only (X is used only to generate q and to evaluate the left side).
 side claims: (i) sigma_3 of the centred four-point window lies between half of sigma_min of the edge matrix [x2-x1, x3-x1, x4-x1] and that
 value ("tau* lies between half of the tau of section 3.5 and that tau"); (ii) sigma_3(S) is non-decreasing in S.

Controls (must fail): L.1 with the constant divided by 1000; L.2 with nu left out (data that another configuration fits exactly);
L.2 with C computed from X instead of Yhat is NOT a control (it is Theorem L) -- printed for comparison only.
Run:  OMP_NUM_THREADS=1 python3 -B item2_corollaries.py > item2_corollaries_<stamp>.log
"""
import os, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize
from r27lib import (cap_memory, peak_mb, now, helix, angle_chain, random_unit_chain, chain_consts, pair_arrays, procrustes,
                    uniform_constant, sigma3)

cap_memory(2.0)
t0 = time.time()
rng = np.random.default_rng(27122)
print(f"R27 item2_corollaries.py started {now()}")


def sqd(Y, J, K):
    d = Y[J] - Y[K]
    return np.einsum("ij,ij->i", d, d)


def stress_min(q, J, K, Y0, iters=500):
    n = len(Y0)

    def fg(y):
        Y = y.reshape(n, 3)
        r = sqd(Y, J, K) - q
        v = (4 * r)[:, None] * (Y[J] - Y[K])
        G = np.zeros_like(Y)
        np.add.at(G, J, v); np.add.at(G, K, -v)
        return r @ r, G.ravel()

    res = minimize(fg, Y0.ravel(), jac=True, method="L-BFGS-B", options=dict(maxiter=iters))
    return res.x.reshape(n, 3), res.fun


def dP(X, Y):
    return np.linalg.norm(procrustes(X, Y)[2])


tot1 = viol1 = ctl1 = 0
tot2 = viol2 = ctl2 = 0
max1 = max2 = 0.0
rows = []
for name, X in (("helix-like n=12", helix(12, 2.3, 1.5, 100.0)), ("strand-like 160 n=12", helix(12, 0.94, 3.3, 160.0)),
                ("angle chain n=8", angle_chain(8, rng)), ("angle chain n=12", angle_chain(12, rng)), ("angle chain n=20", angle_chain(20, rng)),
                ("random unit chain n=10", random_unit_chain(10, rng))):
    n = len(X)
    J, K = pair_arrays(n)
    q0 = sqd(X, J, K)
    CX = uniform_constant(X)
    scale = np.sqrt(q0.mean())
    for lev in (1e-6, 1e-4, 1e-2, 0.1, 1.0, 10.0):
        for rep in range(4):
            eps = lev * scale ** 2 * rng.normal(size=len(J))
            q = q0 + eps
            ne = np.linalg.norm(eps)
            # --- L.1: a stress minimiser started at the truth (stress <= sum eps^2 by construction), and minimisers from random starts when they qualify
            cands = [stress_min(q, J, K, X)]
            for _ in range(2):
                cands.append(stress_min(q, J, K, X + scale * rng.normal(size=X.shape)))
            for Yh, st in cands:
                if st <= ne ** 2 * (1 + 1e-12):
                    d = dP(Yh, X)
                    tot1 += 1
                    max1 = max(max1, d / (2 * CX * ne))
                    viol1 += int(d > 2 * CX * ne * (1 + 1e-9))
                    ctl1 += int(d > 2 * CX * ne / 1000)
            # --- L.2: any Yhat with tau* > 0: minimisers, the truth plus noise, unrelated chains
            others = [c[0] for c in cands] + [X + lev * scale * rng.normal(size=X.shape), angle_chain(n, rng) * scale, X + scale * rng.normal(size=X.shape)]
            for Yh in others:
                tau, s, b = chain_consts(Yh)
                if tau.min() < 1e-9:
                    continue
                CY = 1.2 * b * (n + 2) ** 2 / (s.min() * tau.min())
                r = sqd(Yh, J, K) - q
                d = dP(X, Yh)
                bound = CY * (np.linalg.norm(r) + ne)
                tot2 += 1
                max2 = max(max2, d / bound)
                viol2 += int(d > bound * (1 + 1e-9))
        rows.append((name, lev))
    # control for L.2: data realised exactly by another configuration Y' (eps := eta(Y')): Yhat = Y' has r = 0 and d_P > 0
    for _ in range(5):
        Yp = X + 0.3 * scale * rng.normal(size=X.shape)
        q = sqd(Yp, J, K)
        r = sqd(Yp, J, K) - q
        tau, s, b = chain_consts(Yp)
        CY = 1.2 * b * (n + 2) ** 2 / (s.min() * tau.min())
        ctl2 += int(dP(X, Yp) > CY * np.linalg.norm(r) + 1e-9)
print(f"\nL.1: {tot1} estimates with stress <= sum eps^2 (noise levels 1e-6 ... 10 times the mean squared distance): violations {viol1};  max d_P/(2.4 C ||eps||) = {max1:.3e};"
      f"  CONTROL (constant / 1000): violated by {ctl1}")
print(f"L.2: {tot2} pairs (estimate = minimiser / truth + noise / unrelated chain; bound computed from the estimate, the data and nu = ||eps|| only): violations {viol2};"
      f"  max d_P/bound = {max2:.3e};  CONTROL (nu left out, data realised exactly by another configuration): violated in {ctl2} of 30 cases")

# ---- side claims ----------------------------------------------------------------------------------------------------------
lo = 1e9; hi = 0.0; mono = 0; totm = 0
for _ in range(20000):
    kind = rng.integers(3)
    W = rng.normal(size=(4, 3)) if kind == 0 else (random_unit_chain(4, rng) if kind == 1 else rng.normal(size=(4, 3)) @ np.diag([1, 1, 10.0 ** rng.uniform(-4, 0)]))
    sc = sigma3(W)
    P = np.c_[W[1] - W[0], W[2] - W[0], W[3] - W[0]]
    se = np.linalg.svd(P, compute_uv=False)[-1]
    if sc > 1e-12:
        lo = min(lo, se / sc); hi = max(hi, se / sc)
    extra = rng.normal(size=(1, 3))
    totm += 1
    mono += int(sigma3(np.vstack([W, extra])) >= sc * (1 - 1e-12))
print(f"side claim (i): sigma_min(edge matrix)/sigma_3(centred window) over 20000 four-point windows: min {lo:.4f}, max {hi:.4f}   (claimed: between 1 and 2)")
print(f"side claim (ii): sigma_3 does not decrease when a point is added: {mono} of {totm}")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
