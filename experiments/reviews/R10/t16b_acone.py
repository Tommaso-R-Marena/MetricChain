"""a_cone = max_m MI(Gibbs shell of the cone around a centre of type m), bJ=1.5, B=0, u=1: fine scan in m
(the report: 0.0446).  Both wells are examined separately."""
import numpy as np
from scipy import optimize
from r10lib import *
M = Model(1.5, 0.0, 1.0)
u = 1.0
def shells(m):
    lam = np.array([m, 1 - m])
    def G(nu):
        nu = np.clip(nu, 1e-12, 1 - 1e-12)
        return MI(lam, nu) + float(M.I(lam @ nu)) + u * (m * (1 - nu[0]) + (1 - m) * nu[1])
    out = []
    for x0 in ((0.24, 0.04), (0.96, 0.76), (0.6, 0.4), (0.8, 0.2)):
        r = optimize.minimize(G, x0, method='Nelder-Mead', options={'xatol': 1e-11, 'fatol': 1e-15, 'maxiter': 4000})
        out.append((r.fun, MI(lam, np.clip(r.x, 0, 1)), r.x))
    return out
print("  m     [G_min, MI, nu] for the starts (lower well) (upper well) (middle) (near centre)")
for m in (0.30, 0.40, 0.45, 0.49, 0.50, 0.51, 0.55, 0.60, 0.70, 0.80):
    o = shells(m)
    best = min(o, key=lambda t: t[0])
    print(f"  {m:.2f}  " + " | ".join(f"G={a:.6f} MI={b:.6f} nu=({c[0]:.3f},{c[1]:.3f})" for a, b, c in o) + f"   => global shell MI = {best[1]:.6f}")
