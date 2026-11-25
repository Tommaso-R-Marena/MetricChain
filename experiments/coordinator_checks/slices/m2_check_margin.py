#!/usr/bin/env python3
"""M2, supplement: the five cases in which the LP optimum is a three-atom law with zero budget, re-run with the
feasibility constraint tightened by 1e-9 (E_rho KL >= -e + 1e-9), so that the LP's own tolerance (about 1e-11) cannot
make the optimal law infeasible; then weak duality gives LP - te <= sup r <= max(R2, -e) without any tolerance."""
import math, sys, numpy as np
from scipy.optimize import linprog
import m2_check as M

ETA = 1e-9
def lp_value(x, klx, t, xi, k, u, e, want_rho=False):
    g = M.gfun(x, t, xi, k, u)
    res = linprog(-g, A_ub=[-klx], b_ub=[e - ETA], A_eq=[np.ones_like(x), x], b_eq=[1.0, k], bounds=(0, None), method="highs")
    if res.status != 0:
        return (-math.inf, None) if want_rho else -math.inf
    val = -res.fun - t * e
    return (val, res.x) if want_rho else val
M.lp_value = lp_value
for (k, u, e) in [(0.5, 1.0, -0.15), (0.3, 1.0, -0.2), (0.2, 0.5, -0.02), (0.1, 1.0, -0.05), (0.3, 1.0, -0.55)]:
    r2, mb = M.R2(k, u, e)
    lpv, tt, xi, atoms, mi, nlp = M.lp_sup(k, u, e)
    print(f"kappa={k}, u={u}, e={e}: max(R2, -e) = {max(r2, -e):.12f};  sup_(t,xi)[LP - te] = {lpv:.12f} at t = {tt:.3f}, xi = {xi:.3f};  "
          f"LP - max(R2, -e) = {lpv - max(r2, -e):+.2e};  {len(atoms)} atoms, budget e + MI = {e + mi:+.2e}")
    sys.stdout.flush()
