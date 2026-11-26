#!/usr/bin/env python3
"""E2: re-test 'omega(tau) <= kappa tau' and 'omega(tau)/tau -> kappa' with a well-scaled LP
(h = (nu - delta_xs)/tau), to separate solver tolerance from mathematics."""
import numpy as np
from scipy.optimize import linprog
from part1_checks import kappa
rng = np.random.default_rng(987654321)

def slope(Phi, rho, xs, tau, norm):
    """omega(tau)/tau = max rho.h : sum h = 0, h >= 0 off xs, h_xs >= -1/tau, |D h| <= 1."""
    m, N = Phi.shape; D = Phi - Phi[:, [xs]]
    bounds = [(0, None)] * N; bounds[xs] = (-1.0 / tau, None)
    if norm == "inf":
        res = linprog(-rho, A_ub=np.vstack([D, -D]), b_ub=np.ones(2 * m), A_eq=np.ones((1, N)), b_eq=[0.0],
                      bounds=bounds, method="highs")
    else:
        c = np.concatenate([-rho, np.zeros(m)])
        A_ub = np.vstack([np.hstack([D, -np.eye(m)]), np.hstack([-D, -np.eye(m)]),
                          np.concatenate([np.zeros(N), np.ones(m)])[None, :]])
        res = linprog(c, A_ub=A_ub, b_ub=np.concatenate([np.zeros(2 * m), [1.0]]),
                      A_eq=np.concatenate([np.ones(N), np.zeros(m)])[None, :], b_eq=[0.0],
                      bounds=bounds + [(0, None)] * m, method="highs")
    assert res.status == 0, res.message
    return -res.fun

viol = 0; lin = 0.0; fin = 0; mono = 0
for _ in range(1500):
    N = int(rng.integers(3, 10)); m = int(rng.integers(1, 5))
    P = rng.random((N, 2)); d = np.linalg.norm(P[:, None] - P[None], axis=2)
    xs = int(rng.integers(N))
    kind = rng.integers(3)
    if kind == 0: Phi = rng.normal(size=(m, N))
    elif kind == 1: Phi = rng.integers(-1, 2, size=(m, N)).astype(float)
    else:
        Phi = rng.normal(size=(m, N)); Phi[0] = d[xs] * (0.5 + rng.random(N))
    rho = d[xs].copy()
    for norm in ("inf", "l1"):
        kap = kappa(Phi, rho, xs, norm)
        if not np.isfinite(kap):
            continue
        fin += 1
        prev = np.inf
        for tau in (1e-6, 1e-4, 1e-2, 1.0, 100.0):
            s = slope(Phi, rho, xs, tau, norm)
            viol += (s > kap * (1 + 1e-7) + 1e-9)
            mono += (s > prev * (1 + 1e-7) + 1e-9); prev = s
        lin = max(lin, abs(slope(Phi, rho, xs, 1e-6, norm) - kap) / max(kap, 1e-9))
print(f"E2 rescaled: kappa finite {fin}; omega/tau > kappa: {viol}; omega/tau not non-increasing: {mono}; "
      f"max rel |omega(1e-6)/1e-6 - kappa|: {lin:.2e}")
