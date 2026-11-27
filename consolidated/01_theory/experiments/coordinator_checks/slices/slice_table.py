#!/usr/bin/env python3
"""Table of Theorem 11.90: slices at u = 1 (and u = 2): R^kappa(0), the best centre type, a^kappa = N^kappa(0+) = sup_m F(l*)."""
import numpy as np
from slice_lib import *
def a_of(m, k, u):
    hi = lam_range(m, k)[1]
    _, ls = golden(lambda l: -(u*l - F(m, k, l)), 0.0, hi*(1 - 1e-13))
    return F(m, k, ls)
for u in (1.0, 2.0):
    print(f"u = {u}:  cube R_unif(0) = {R_unif(u, 0.0):.6f},  a = KL(p_u || 1/2) = {kl(1/(1+math.exp(u)), 0.5):.6f}")
    for k in (0.5, 0.45, 0.4, 0.3, 0.2, 0.1, 0.05):
        sb, mb = slice_best(k, u, 0.0)
        ms = np.linspace(0.02, 0.98, 97); vals = [a_of(m, k, u) for m in ms]; i = int(np.argmax(vals))
        v, ma = golden(lambda mm: -a_of(mm, k, u), ms[max(i-1, 0)], ms[min(i+1, 96)], tol=1e-10)
        e1 = 0.3*R_unif(u, 0.0); sb1, mb1 = slice_best(k, u, e1)
        print(f"   kappa = {k:4.2f}:  R(0) = {sb:.6f} (m = {mb:.4f});  a = {-v:.6f} (m = {ma:.4f});  R at e = 0.3 R_unif(0): {sb1:.6f} (cube {R_unif(u, e1):.6f})")
