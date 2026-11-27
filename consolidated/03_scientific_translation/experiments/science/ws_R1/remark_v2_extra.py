#!/usr/bin/env python3
"""R1: follow-up on (S5) of remark_v2_sites.py.  At u = 0.5 the grid maximum of h over three-letter laws was 0.007675 at
(0.05, 0.45, 0.5) -- slightly ABOVE the two-letter value h_2 = 0.007673.  Is that real?  High-resolution evaluation with
duality brackets, and a local search over three-letter laws.  (Formulas of Theorem 11.99 taken as given.)"""
import math, sys
import numpy as np
from scipy.optimize import minimize
from remark_v2_sites import vertex_laws, Fstar, h_k

def h_precise(pi, u, n=400):
    P, _ = vertex_laws(pi, u)
    ts = np.linspace(0.3, 0.7, n)
    best = (-1, None, None)
    for t in ts:
        lo, up, _ = Fstar(P, float(t))
        if lo > best[0]:
            best = (lo, up, float(t))
    return best

u = 0.5
print(f"u = {u}:  h_2 = {h_k(2, u):.9f}   h_3 = {h_k(3, u):.9f}")
print("   law pi                      h (lower)     (upper)       t*")
for pi in ([0.5, 0.5], [0.05, 0.45, 0.5], [0.05, 0.475, 0.475], [0.02, 0.48, 0.5], [0.02, 0.49, 0.49], [0.01, 0.47, 0.52],
           [0.05, 0.40, 0.55], [0.1, 0.4, 0.5], [0.001, 0.4995, 0.4995], [0.45/0.95, 0.5/0.95]):
    lo, up, t = h_precise(pi, u)
    print(f"   {str([round(x, 4) for x in pi]):26s}  {lo:.9f}   {up:.9f}   {t:.3f}")
# local search over three-letter laws
def neg(z):
    w = np.exp(z - z.max()); pi = list(w / w.sum())
    return -h_precise(pi, u, n=60)[0]
best = None
for z0 in ([math.log(0.05), math.log(0.45), math.log(0.5)], [math.log(0.02), math.log(0.48), math.log(0.5)]):
    res = minimize(neg, np.array(z0), method="Nelder-Mead", options={"xatol": 1e-4, "fatol": 1e-11, "maxiter": 150})
    w = np.exp(res.x - res.x.max()); pi = w / w.sum()
    lo, up, t = h_precise(list(pi), u, n=400)
    print(f"   local search from {[round(math.exp(v), 3) for v in z0]}: pi = {[round(float(x), 5) for x in pi]}  h in [{lo:.9f}, {up:.9f}]")
    if best is None or lo > best[0]:
        best = (lo, up, pi)
print(f"   largest h found on three letters at u = {u}: {best[0]:.9f} (bracket upper {best[1]:.9f}) vs two-letter cube {h_k(2, u):.9f}: "
      f"excess {best[0] - h_k(2, u):.3e}")
