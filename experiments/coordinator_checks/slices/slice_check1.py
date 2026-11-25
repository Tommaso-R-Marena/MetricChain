#!/usr/bin/env python3
"""Check 1 (theory report 11.25): binary centres suffice on a slice, the closed forms, and domination by the cube."""
import math, numpy as np
from slice_lib import *
rng = np.random.default_rng(20261125)
# (a) closed forms against direct evaluation; the two forms of Psi
w1 = w2 = w3 = 0
for _ in range(24):
    k = rng.uniform(0.1, 0.9); m = rng.uniform(0.1, 0.9); u = rng.uniform(0.3, 3)
    w1 = max(w1, abs(Psi(m, k, u) - Psi_dual(m, k, u)))
    e = rng.uniform(0, 0.8)*Psi(m, k, u)
    w2 = max(w2, abs(V_binary(m, k, u, e) - V_binary_direct(m, k, u, e)))
    lam2 = [m, 1 - m]
    P = Psi(m, k, u); hi = lam_range(m, k)[1]
    # the binary profile at the best shell, through the multi-block solver
    best = 0.0
    for l in np.linspace(0.02*hi, 0.98*hi, 99):
        mu = [k + l/(2*m), k - l/(2*(1 - m))]
        best = max(best, r_slice(lam2, mu, k, u, e))
    w3 = max(w3, abs(best - V_binary(m, k, u, e)))
print(f"(a) Psi two ways: {w1:.1e};  closed form V = F((Psi(u) - e)/u) against direct: {w2:.1e};  against the multi-block solver on two blocks: {w3:.1e} (grid of 99 shells)")
# (b) multi-block profiles never beat the best binary centre
worst = -1; cases = 0
for trial in range(300):
    k = rng.uniform(0.15, 0.85); u = rng.choice([0.5, 1.0, 2.0]); kb = rng.integers(3, 6)
    lam = rng.dirichlet(np.ones(kb)*rng.choice([0.5, 1, 3]))
    mu = rng.uniform(0, 1, kb)
    # move to the slice: shift the densities so that the type is kappa (rescale towards 0 or 1)
    t = float(np.dot(lam, mu))
    mu = mu*k/t if t > k else 1 - (1 - mu)*(1 - k)/(1 - t)
    if abs(np.dot(lam, mu) - k) > 1e-12 or mu.min() < 0 or mu.max() > 1: continue
    sb0, _ = slice_best(k, u, 0.0)
    e = rng.choice([0.0, 0.2, 0.5])*sb0
    val = r_slice(list(lam), list(mu), k, u, e)
    sb, _ = slice_best(k, u, e)
    worst = max(worst, val - sb); cases += 1
print(f"(b) {cases} random profiles with 3-5 blocks in a slice: largest r_slice(mu, e) - sup over binary centres = {worst:.3e}  (must be <= 0)")
# (c) adversarial: local improvement of a 3-block profile from the best binary one
from scipy.optimize import minimize
gap = -1
for (k, u, e_frac) in [(0.5, 1.0, 0.0), (0.5, 1.0, 0.3), (0.3, 1.0, 0.0), (0.3, 2.0, 0.2), (0.7, 0.5, 0.0)]:
    sb0, mb = slice_best(k, u, 0.0); e = e_frac*sb0; sb, mb = slice_best(k, u, e)
    def neg(z):
        l1, l2, a, b = z
        l3 = 1 - l1 - l2
        if min(l1, l2, l3) < 1e-3 or not (0 < a < 1 and 0 < b < 1): return 1.0
        c = (k - l1*a - l2*b)/l3
        if not (0 < c < 1): return 1.0
        return -r_slice([l1, l2, l3], [a, b, c], k, u, e)
    bestv = 0
    for s in range(6):
        z0 = [rng.uniform(0.1, 0.5), rng.uniform(0.1, 0.4), rng.uniform(0.05, 0.95), rng.uniform(0.05, 0.95)]
        res = minimize(neg, z0, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-13, "maxiter": 700})
        bestv = max(bestv, -res.fun)
    gap = max(gap, bestv - sb)
    print(f"    kappa={k}, u={u}, e={e:.5f}: best 3-block by Nelder-Mead {bestv:.7f}; best binary {sb:.7f} (m = {mb:.4f}); cube {R_unif(u, e):.7f}")
print(f"(c) largest (3-block optimum - binary optimum): {gap:.2e}")
# (d) domination by the cube, pointwise in t, random draws; and the non-adaptive function
wF = wN = -1
for _ in range(300):
    k = rng.uniform(0.03, 0.97); m = rng.uniform(0.03, 0.97); u = rng.uniform(0.2, 4); t = rng.uniform(0, 1)
    Lc = lambda s: math.log(math.cosh(s))
    wF = max(wF, Fstar(m, k, u, t) - (t*Lc(u/2) - Lc(t*u/2)))
    X = rng.uniform(0.02, 1.0)*Lc(u/2)
    wN = max(wN, N_binary(m, k, u, X) - N_cube(u, X))
print(f"(d) largest F*_(m,kappa)(t) - F*_cube(t): {wF:.2e};  largest N_(m,kappa)(X) - N_cube(X): {wN:.2e}  (both must be <= 0)")
print(f"    cube check: N_binary(1/2, 1/2) - N_cube at u = 1, X = 0.01, 0.05: {N_binary(0.5, 0.5, 1.0, 0.01) - N_cube(1.0, 0.01):.1e}, {N_binary(0.5, 0.5, 1.0, 0.05) - N_cube(1.0, 0.05):.1e};  V - R_unif: {V_binary(0.5, 0.5, 1.0, 0.01) - R_unif(1.0, 0.01):.1e}")
# (e) the table: slices at u = 1
print("(e) u = 1, e = 0:  kappa, sup_m V (best centre type), a := N at X -> 0+")
for k in (0.5, 0.45, 0.4, 0.3, 0.2, 0.1, 0.05):
    sb, mb = slice_best(k, 1.0, 0.0)
    na = max(N_binary(m, k, 1.0, 1e-9) for m in np.linspace(0.02, 0.98, 97))
    print(f"    {k:5.2f}  {sb:.6f} (m = {mb:.4f})   {na:.6f}")
