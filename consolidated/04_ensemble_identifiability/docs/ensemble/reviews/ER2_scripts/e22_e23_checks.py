#!/usr/bin/env python3
"""ER2: Proposition E2.2 and Remark E2.3.

Q1  E2.2: the identification modulus omega(tau) = sup{ int |t| dnu : |int Phi dnu - Phi(0)|_inf <= tau } on X = [-1, 1]
    (grid of 4001 points, LP), x* = 0, for several smooth and non-smooth observables:
        Phi = t^2                 (kappa_2 = 1)      expected sqrt(tau)
        Phi = (t, t^2)                               expected sqrt(tau)
        Phi = t^4   (C-infinity, identified)         expected tau^(1/4):  NOT a square root
        Phi = |t|^1.5  (C^1, not C^2)                expected tau^(2/3):  NOT a square root
        Phi = (t, t^3)  (C-infinity)                 delta_0 not identified: omega(0) > 0
    In every case kappa = +infinity (E2.2(a)) and omega(tau) >= c sqrt(tau) for the C^2 ones.
Q2  E2.3: two examples for "tau is replaced by tau + eta".
    (i)  both ensembles seen through the true observables: the replacement is tau + 2 eta, and 2 eta is attained;
    (ii) "a certificate cannot use that the ensemble avoids the configurations where the model is poor":
         a certificate argument that does.
"""
import numpy as np
from scipy.optimize import linprog


def omega(ts, Phi, rho, tau):
    """sup int rho dnu  s.t. |int Phi dnu - Phi(x*)|_inf <= tau; x* = the grid point t = 0."""
    k0 = int(np.argmin(np.abs(ts)))
    D = Phi - Phi[:, [k0]]
    res = linprog(-rho, A_ub=np.vstack([D, -D]), b_ub=tau * np.ones(2 * len(D)), A_eq=np.ones((1, len(ts))), b_eq=[1.0],
                  bounds=[(0, None)] * len(ts), method="highs")
    return -res.fun


ts = np.linspace(-1, 1, 4001); rho = np.abs(ts)
cases = [("t^2", np.array([ts ** 2]), 0.5), ("(t, t^2)", np.array([ts, ts ** 2]), 0.5), ("t^4", np.array([ts ** 4]), 0.25),
         ("|t|^1.5", np.array([np.abs(ts) ** 1.5]), 2 / 3), ("(t, t^3)", np.array([ts, ts ** 3]), None)]
print("Q1  omega(tau) on [-1,1], x* = 0, rho = |t|")
print("    observables      tau = 1e-2    1e-3      1e-4      1e-5      local exponent (last two)   expected")
for name, Phi, expo in cases:
    vals = [omega(ts, Phi, rho, tau) for tau in (1e-2, 1e-3, 1e-4, 1e-5)]
    slope = np.log(vals[2] / vals[3]) / np.log(10.0)
    print(f"    {name:12s}   " + "  ".join(f"{v:.5f}" for v in vals) + f"      {slope:.3f}                      "
          + (f"{expo:.3f}" if expo else "omega(0) > 0 (not identified)"))
print("    kappa = sup omega(tau)/tau: omega(1e-5)/1e-5 = " + ", ".join(f"{omega(ts, P, rho, 1e-5) / 1e-5:.0f}" for _, P, _ in cases))

print("Q2  Remark E2.3")
eta = 0.1
# (i) X = {x*, y}: model Phi = (0, 2 eta), truth Phi~ = (eta, eta): sup error eta; delta_y and delta_x* have the same TRUE data
Phi = np.array([0.0, 2 * eta]); Phit = np.array([eta, eta])
print(f"    (i)  X = {{x*, y}}, model Phi = {Phi.tolist()}, true Phi~ = {Phit.tolist()} (sup error {np.abs(Phi - Phit).max()}): "
      f"true data of delta_y and delta_x* differ by {abs(Phit[1] - Phit[0])} (tau = 0); model data differ by {abs(Phi[1] - Phi[0])} = 2 eta > tau + eta = {eta}")
kappa = 1 / (2 * eta)
print(f"         rho(y) = 1, kappa = 1/(2 eta) = {kappa}: int rho d(delta_y) = 1 > kappa (tau + eta) = {kappa * eta};  = kappa (tau + 2 eta) = {kappa * 2 * eta}")
# (ii) X = {x*, y}: model Phi = (0, 1); truth exact at x*, anything within eta = 0.5 at y
eta = 0.5; tau = 0.01
worst_p = max(tau / (1 + d) for d in np.linspace(-eta, eta, 1001))
print(f"    (ii) X = {{x*, y}}, model Phi = (0, 1), certificate lambda = 1 (gap 1); true Phi~(x*) = 0, |Phi~(y) - 1| <= eta = {eta}; data p Phi~(y) within tau = {tau} of 0:")
print(f"         largest mass off x*: {worst_p:.4f} = tau/(1 - eta);  the bound of the remark (tau -> tau + eta): {tau + eta:.4f};  "
      f"certificate bound using where the model is poor: ||lam|| (tau + eta_S)/(gamma - ||lam|| (eta - eta_S)) = {tau / (1 - eta):.4f}")
