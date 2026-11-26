#!/usr/bin/env python3
"""R9, item 3(a): an independent check of the formula (I - v)(P) = min_{gamma in L} KL(P || pi_gamma) on TWO letters, where
v(P) = min_{P'} [KL(P'||pi) + W(P',P)] can be computed by a one-dimensional grid search (no solver):
W(P',P) = d(0,1) (p'_0 - p_0)_+ + d(1,0) (p_0 - p'_0)_+   (first argument of d = the letter of X').
And the chi^2 bound against every window point."""
import math
import numpy as np
rng = np.random.default_rng(5)
KLv = lambda p, q: float(sum(a * math.log(a / b) for a, b in zip(p, q) if a > 0))
worst = 0.0; viol = 0; n = 0; worst_ratio = 0.0; nin = 0; worst_neg = 0.0
TOL = 2e-6          # the grid in p' has step 5e-7, so I - v_grid carries an error of that order (it can be -5e-7 for P in the window)
for trial in range(400):
    pi0 = rng.uniform(0.05, 0.95); d01, d10 = rng.uniform(0.05, 2.5, 2)
    p0 = rng.uniform(0.01, 0.99)
    pi, Pm = (pi0, 1 - pi0), (p0, 1 - p0)
    grid = np.linspace(1e-9, 1 - 1e-9, 2000001)
    val = grid * np.log(grid / pi0) + (1 - grid) * np.log((1 - grid) / (1 - pi0)) + d01 * np.maximum(grid - p0, 0) + d10 * np.maximum(p0 - grid, 0)
    v_grid = float(val.min())
    # dual: gamma = (0, g) with -d01 <= g <= d10  [gamma(1) - gamma(0) <= d(1,0), gamma(0) - gamma(1) <= d(0,1)]
    gs = np.linspace(-d01, d10, 400001)
    lz = np.log(pi0 + (1 - pi0) * np.exp(-gs))
    dualv = -lz - (1 - p0) * gs
    v_dual = float(dualv.max())
    g = gs[int(np.argmax(dualv))]
    I = KLv(Pm, pi)
    # min over gamma of KL(P || pi_gamma)
    q0 = pi0 / (pi0 + (1 - pi0) * np.exp(-gs))
    kl = p0 * np.log(p0 / q0) + (1 - p0) * np.log((1 - p0) / (1 - q0))
    worst = max(worst, abs(v_grid - v_dual), abs((I - v_dual) - float(kl.min())))
    n += 1
    # chi^2 bound against every window point Q = pi_gamma
    chi2 = (p0 - q0) ** 2 / q0 + (p0 - q0) ** 2 / (1 - q0)
    if np.any(I - v_grid > chi2 + TOL) or I - v_grid < -TOL: viol += 1
    nin += bool(q0.min() - 1e-6 <= p0 <= q0.max() + 1e-6)
    worst_neg = min(worst_neg, I - v_grid)
    j = int(np.argmin(chi2))
    if chi2[j] > 1e-9: worst_ratio = max(worst_ratio, (I - v_grid) / chi2[j])
print(f"two letters, {n} random (pi, asymmetric d, P): max |v_grid - v_dual| and |(I - v) - min_gamma KL(P||pi_gamma)| = {worst:.2e} (grid resolution 5e-7);"
      f" violations (beyond {TOL:g}) of 0 <= I - v <= chi^2(P||Q) over all window points Q: {viol}; largest (I - v)/min_Q chi^2 = {worst_ratio:.4f};"
      f" {nin} cases have P inside the window (I - v = 0); most negative I - v_grid = {worst_neg:.1e} (grid error)")
print("(first run of this script used the tolerance 1e-7 and reported 93 'violations': all of them cases with P in the window,")
print(" where I - v_grid = -5e-7 from the grid; a false alarm of mine, recorded in NOTES.md)")
