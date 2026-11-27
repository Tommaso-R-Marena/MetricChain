#!/usr/bin/env python3
"""Workstream R27, Item 2 (iv) -- Corollary L.3 ("the exponent is sharp; Theta(n^2) on helices; infinitesimal rigidity with a constant").
REPLICATION from the statement:
  (a) ideal helices, distances of separation <= K (K >= 4 fixed): the first-order constant for DISTANCE errors, C_inf = 1/s_7(R), satisfies
          h^2 n^2 / (139 rho b K^{3/2})  <=  C_inf  <=  9.6 (b^2/(s* tau*)) (n+2)^2 ;
  (b) every chain with tau* > 0:  mu >= s* tau* / (2.4 b (n+2)^2),  mu = (3n-6)-th singular value of the half-Jacobian of the squared distances.
Controls (must fail): the lower bound multiplied by 100; the upper bound divided by 10^4; (b) with the right side multiplied by 10^3.
Run:  OMP_NUM_THREADS=1 python3 -B item2_cor_L3.py > item2_cor_L3_<stamp>.log
"""
import os, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from r27lib import cap_memory, peak_mb, now, helix, angle_chain, random_unit_chain, chain_consts, pair_arrays, half_jacobian

cap_memory(2.0)
t0 = time.time()
rng = np.random.default_rng(27120)
print(f"R27 item2_cor_L3.py started {now()}")


def s7_and_mu(X, K):
    n = len(X)
    J, Kk = pair_arrays(n, K)
    A = half_jacobian(X, J, Kk)
    d = np.linalg.norm(X[J] - X[Kk], axis=1)
    S = np.linalg.svd(A, compute_uv=False)
    S = np.concatenate([S, np.zeros(max(0, 3 * n - len(S)))])
    S2 = np.linalg.svd(A / d[:, None], compute_uv=False)
    S2 = np.concatenate([S2, np.zeros(max(0, 3 * n - len(S2)))])
    return S2[3 * n - 7], S[3 * n - 7], S2[3 * n - 6]


viol = 0; c_lo = 0; c_hi = 0; c_b = 0; tot = 0
for name, rho, h, turn in (("helix-like (2.3, 1.5, 100)", 2.3, 1.5, 100.0), ("strand-like (0.94, 3.3, 160)", 0.94, 3.3, 160.0),
                           ("strand-like (0.94, 3.3, 175)", 0.94, 3.3, 175.0)):
    print(f"\n{name}:  columns: n | K | 1/s_7 | lower bound h^2 n^2/(139 rho b K^1.5) | upper bound 9.6 b^2 (n+2)^2/(s* tau*) | (1/s_7)/n^2 | mu | s* tau*/(2.4 b (n+2)^2) | mu/that")
    rows = {4: [], 6: []}
    for n in (20, 40, 80, 160, 320):
        X = helix(n, rho, h, turn)
        tau, s, b = chain_consts(X)
        for K in (4, 6):
            s7, mu, zero = s7_and_mu(X, K)
            lo = h * h * n * n / (139 * rho * b * K ** 1.5)
            hi = 9.6 * b * b * (n + 2) ** 2 / (s.min() * tau.min())
            mub = s.min() * tau.min() / (2.4 * b * (n + 2) ** 2)
            ok = lo <= 1 / s7 * (1 + 1e-9) and 1 / s7 <= hi * (1 + 1e-9) and (K != 4 or mu >= mub * (1 - 1e-9))
            tot += 1; viol += int(not ok)
            c_lo += int(100 * lo > 1 / s7); c_hi += int(1 / s7 > hi / 1e4); c_b += int(K == 4 and mu < 1e3 * mub)
            rows[K].append((n, 1 / s7))
            print(f"   {n:4d} | {K} | {1 / s7:10.4f} | {lo:10.4f} | {hi:12.4g} | {1 / s7 / n ** 2:.5f} | {mu:.5g} | {mub:.3e} | {mu / mub:8.1f}" + ("" if ok else "   VIOLATION"))
    for K in (4, 6):
        nn = np.log([r[0] for r in rows[K]]); cc = np.log([r[1] for r in rows[K]])
        slope = np.polyfit(nn[1:], cc[1:], 1)[0]
        print(f"   K = {K}: fitted exponent of 1/s_7 in n (n = 40 ... 320): {slope:.3f};  more pairs lower the constant: {all(a[1] >= b_[1] - 1e-12 for a, b_ in zip(rows[4], rows[6]))}")

print("\n(b) on other chains (angle-constrained and unconstrained random unit chains): mu against s* tau*/(2.4 b (n+2)^2)")
minr = 1e300
for rep in range(200):
    n = int(rng.integers(5, 40))
    X = angle_chain(n, rng) if rep % 2 else random_unit_chain(n, rng)
    tau, s, b = chain_consts(X)
    if tau.min() < 1e-6:
        continue
    s7, mu, zero = s7_and_mu(X, 4)
    mub = s.min() * tau.min() / (2.4 * b * (n + 2) ** 2)
    tot += 1; viol += int(mu < mub * (1 - 1e-9)); c_b += int(mu < 1e3 * mub)
    minr = min(minr, mu / mub)
print(f"   smallest mu/(lower bound) over the random chains: {minr:.1f}  (>= 1 means (b) holds)")
print(f"\nchecks: {tot}   violations: {viol}   CONTROLS: lower bound x 100 violated {c_lo} times; upper bound / 10^4 violated {c_hi} times; (b) with the bound x 10^3 violated {c_b} times")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
