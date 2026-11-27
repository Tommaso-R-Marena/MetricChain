#!/usr/bin/env python3
"""R1: what replaces the failed comparison for q >= 3 letters -- a universal (Hoeffding) ceiling.
 (U1) Potts pair, any alphabet, any marginals:  I(s) <= s^2/8.
      [P: I(s) = int_0^s s' rho(s') ds' along the fixed-marginal fibre, rho = residual variance of 1[b=x] <= 1/4.]
 (U2) Any site law pi on q letters with the Hamming envelope u, vertex channel of Theorem 11.99:
      F*(t) = min_Q max_S (1-t) D_t(pi_S || Q) <= max_S [t Lam_S(1) - Lam_S(t)] <= t(1-t) u^2/8,  Lam_S(t) = ln E_pi exp(-t u 1_S)
      hence h <= u^2/32, E <= u^2/8, a <= u^2/8.  [P given the formula: take Q = pi; Lam'' <= u^2/4.]
      The two-letter cube attains the ceiling to leading order in u:  h_2 = u^2/32 - O(u^4).
 (U3) the pair identity on a slice: N^kappa(e + R^kappa(e)) = R^kappa(e)   (Remark after Theorem 11.90)."""
import math, sys
import numpy as np
from remark_v2_sites import vertex_laws, Fstar, threshold_E, capacity_a, h_k
from potts_three_letters import sinkhorn_table, mi_table
from thm_1190 import best_centre
rng = np.random.default_rng(8)
ok = True
# (U1)
worst = -math.inf; n = 0
for _ in range(4000):
    q = int(rng.integers(2, 7)); s = float(rng.choice([0.05, 0.3, 1.0, 2.0, 4.0]) * rng.uniform(0.5, 1.5))
    al = rng.dirichlet(np.ones(q) * rng.choice([0.3, 1, 5])); ga = rng.dirichlet(np.ones(q) * rng.choice([0.3, 1, 5]))
    P = np.outer(al, ga) * (np.ones((q, q)) + (math.exp(s) - 1) * np.eye(q)); P /= P.sum()
    worst = max(worst, mi_table(P) / (s * s / 8)); n += 1
print(f"(U1) {n} random Potts pairs (q = 2..6): max I/(s^2/8) = {worst:.6f} (<= 1)")
ok &= worst <= 1 + 1e-12
# (U2)
worstF = worstE = worsta = -math.inf; m = 0
for _ in range(60):
    q = int(rng.integers(2, 5)); u = float(rng.choice([0.25, 0.5, 1.0, 2.0, 3.0]))
    pi = rng.dirichlet(np.ones(q) * rng.choice([0.5, 2, 10]))
    P, _ = vertex_laws(list(pi), u)
    for t in (0.15, 0.4, 0.5, 0.7, 0.9):
        lo, up, _ = Fstar(P, t)
        worstF = max(worstF, up / (t * (1 - t) * u * u / 8))
    worstE = max(worstE, threshold_E(P)[1] / (u * u / 8)); worsta = max(worsta, capacity_a(P)[1] / (u * u / 8)); m += 1
print(f"(U2) {m} random sites (q = 2..4, u in .25..3): max F*(t)/(t(1-t)u^2/8) = {worstF:.6f}; max E/(u^2/8) = {worstE:.6f}; max a/(u^2/8) = {worsta:.6f} (all <= 1)")
ok &= worstF <= 1 + 1e-9 and worstE <= 1 + 1e-9 and worsta <= 1 + 1e-9
print("     two-letter cube against the ceiling u^2/32:  " + ", ".join(f"u={u}: h_2/(u^2/32) = {h_k(2, u) / (u * u / 32):.4f}" for u in (0.1, 0.25, 0.5, 1.0, 2.0)))
print("     three-letter cube:                           " + ", ".join(f"u={u}: h_3/(u^2/32) = {h_k(3, u) / (u * u / 32):.4f}" for u in (0.1, 0.25, 0.5, 1.0, 2.0)))
# (U3)
err = 0.0
for kappa, u in ((0.3, 1.0), (0.5, 1.0), (0.2, 2.0)):
    for e in (0.0, 0.01, 0.03):
        R = best_centre(kappa, u, e, "V")[0]
        N = best_centre(kappa, u, None, "N", X=e + R)[0]
        err = max(err, abs(N - R))
print(f"(U3) pair identity on slices: |N^kappa(e + R^kappa(e)) - R^kappa(e)| <= {err:.2e} (kappa,u) in (.3,1),(.5,1),(.2,2); e in 0,.01,.03")
ok &= err < 1e-8
print("SUMMARY:", "ALL PASS" if ok else "FAILURES")
