#!/usr/bin/env python3
"""Control: the field (phi = theta*kappa).  Known values at p = 0.1, u = 2 (theory report §11.20; THY-REQ-0007):
R^max(0) = 0.048130, E = 0.21227, R^max(0.3E) = 0.023273, R_0(0.3E) = 0.019497, theta_na(0.3E) = 0.036246."""
import numpy as np, math, sys, time
from mf_lib import Model, hb

p, u = 0.1, 2.0
theta = math.log((1 - p) / p)
M = Model(lambda k: theta * k, u, G=int(sys.argv[1]) if len(sys.argv) > 1 else 601)
ms = np.linspace(0.02, 0.98, 49)
E = 0.21227
t0 = time.time()
for e, want_R, want_R0, want_na in ((0.0, 0.048130, None, None), (0.3 * E, 0.023273, 0.019497, 0.036246)):
    RH, mH = M.R_formula(e, ms, "v")
    R0, m0 = M.R_formula(e, ms, "0")
    na, mna = M.theta_na(e if e > 0 else 1e-9, ms)
    pair, _ = M.theta_na(e + RH, ms)
    print(f"e = {e:.5f}: R_H(formula) = {RH:.6f} (m={mH:.2f}; known R^max {want_R})   R_0 = {R0:.6f} (known {want_R0})   "
          f"theta_na(e) = {na:.6f} (known {want_na})   pair: theta_na(e + R_H) = {pair:.6f}")
print("time", round(time.time() - t0, 1))
# dip exponents by the variational definition, for the flat-histogram instance and for additive instances
ms2 = np.linspace(0.05, 0.95, 19)
chiH = -M.vk
t0 = time.time()
for e in (0.0, 0.3 * E):
    RHd, mm = M.R_dip(chiH, e, ms2)
    best = (0, None)
    for gam in np.linspace(-1.6, 0.4, 11):
        Rg, mg = M.R_dip(gam * M.kap, e, ms2)
        if Rg > best[0]:
            best = (Rg, gam)
    print(f"e = {e:.5f}: R_H(dip definition) = {RHd:.6f} (m={mm});  max over additive instances = {best[0]:.6f} at gamma = {best[1]:.2f}")
print("time", round(time.time() - t0, 1))
