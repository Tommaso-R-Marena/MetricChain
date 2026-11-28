"""Minimal reproduction: ci.tau_grad returns NaN in the model-free case (Lw = 0, no exact part b).

At the root tau = max_j s0_j no point has s > 0, so the extremal weights om = wt*(Lw + Gw*(s > 0)) are all zero and
tau_grad divides 0 by 0.  A subgradient exists (the measured observables of an arg-max point).  Effect: the
L-BFGS-B stages of solve_upper(..., "descent") receive NaN gradients for l = 0 problems with a non-box region
(the descent route is the only one for an ellipsoid); Nelder-Mead still runs.  Not a soundness issue: whatever eta
is returned, tau_root(eta) certifies.  It can make model-free intervals on ellipsoids (B3 on F3) wider than exact.

    python experiments/eng/certinf/bugs/tau_grad_nan_modelfree.py     # prints the NaN gradient, exits 1
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from metricchain_eng import certinf as ci  # noqa: E402

rng = np.random.default_rng(0)
f, phi = rng.uniform(-1, 1, 20), rng.uniform(-1, 1, (20, 2))
P = ci.Problem(f, phi, Lw=0.0, Gw=1.0, region=ci.Ellipsoid([0.0, 0.0], 0.01 * np.eye(2)))
g = ci.tau_grad(P, np.array([0.3, -0.2]))
print("tau_grad:", g)
sys.exit(1 if np.any(np.isnan(g)) else 0)
