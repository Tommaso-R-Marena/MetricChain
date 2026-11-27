#!/usr/bin/env python3
"""The uniform measure on one slice (type kappa) as known part: dip exponent of the constant instance,
   R_slice(e) = sup over binary centres (m; a, b) with type kappa of min{ MI(nu) : type(nu) = kappa, u dist(nu, mu) <= e + MI(mu) }.
Is it the uniform cube's KL((Lambda_1 + e)/u || 1/2) at kappa = 1/2 ?  (limit beta J -> -infinity of the antiferromagnets)"""
import numpy as np, math
from scipy.optimize import minimize
def hb(x):
    x = np.clip(x, 1e-300, 1 - 1e-16); return -(x*np.log(x) + (1-x)*np.log1p(-x))
def val(m, a, kappa, e, u, G=200001):
    b = (kappa - m*(1-a))/(1-m)
    if not (0 < b < 1 and 0 < a < 1 and 0 < m < 1): return -1.0
    mi0 = hb(kappa) - m*hb(1-a) - (1-m)*hb(b)
    rad = (e + mi0)/u
    ap = np.linspace(0, 1, G)                         # exits (a', b') with the same type
    bp = (kappa - m*(1-ap))/(1-m)
    ok = (bp >= 0) & (bp <= 1) & (m*np.abs(ap-a) + (1-m)*np.abs(bp-b) <= rad)
    if not ok.any(): return -1.0
    return float((hb(kappa) - m*hb(1-ap[ok]) - (1-m)*hb(bp[ok])).min())
def R_unif(e, u):
    rho = (math.log(2/(1+math.exp(-u))) + e)/u
    return rho*math.log(2*rho) + (1-rho)*math.log(2*(1-rho)) if rho < 0.5 else 0.0
for u in (1.0, 2.0):
    pu = 1/(1+math.exp(u))
    for e in (0.0, 0.02):
        best = (0, None)
        for m in np.linspace(0.2, 0.8, 61):
            for a in np.linspace(0.02, 0.6, 117):
                v = val(m, a, 0.5, e, u, G=4001)
                if v > best[0]: best = (v, (m, a))
        r = minimize(lambda p: -val(p[0], p[1], 0.5, e, u), best[1], method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-12})
        print(f"u={u} e={e}: slice 1/2: sup = {-r.fun:.7f} at (m, a) = {np.round(r.x, 5)} (p_u = {pu:.5f});  uniform cube {R_unif(e, u):.7f};  symmetric shell on the slice {val(0.5, pu, 0.5, e, u):.7f}")
# other slices against the cube: is R_slice_kappa(e) <= R_unif(e)?
u = 1.0
for kappa in (0.4, 0.3, 0.2):
    best = (0, None)
    for m in np.linspace(0.05, 0.95, 91):
        for a in np.linspace(0.02, 0.9, 177):
            v = val(m, a, kappa, 0.0, u, G=4001)
            if v > best[0]: best = (v, (m, a))
    print(f"u=1 e=0 slice {kappa}: sup over binary centres = {best[0]:.6f} at (m, a) = {np.round(best[1], 3)};  uniform cube {R_unif(0.0, u):.6f}")
