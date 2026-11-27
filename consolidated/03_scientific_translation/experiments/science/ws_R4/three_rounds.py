#!/usr/bin/env python3
"""R4 -- an upper bound for the three-round value T^(3)(0) of Theorem 11.84(a) from two of the
admissible ladders (own code; the recursion is a minimum over ladders, so each ladder gives an
upper bound):
  (1,1,1): min_{phi, xi1>xi2>0} max{ phi a + (1-phi) tna(xi1),
                                     min(phi a,(1-phi) xi1) + (1-phi) tna(xi2),
                                     min(phi a,(1-phi) xi2) + (1-phi) a }
  (1,2)  : min_{phi, xi1}       max{ phi a + (1-phi) tna(xi1), min(phi a,(1-phi) xi1) + (1-phi) T2(0) }
with tna = theta_na (xi = k(rho), tna = f(rho), rho in [p_u,1/2]) and T2(0) from exponents.py.
"""
import sys
import numpy as np
from exponents import Cube, f

u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
C = Cube(u)
a = C.a
T2 = C.T2_balance()[0]
nr = 700
rho = np.linspace(C.pu, 0.5, nr)
xi = C.k(rho)
tna = f(rho)
best111 = (9.0, None)
best12 = (9.0, None)
for phi in np.linspace(0.02, 0.98, 481):
    t1 = phi * a + (1 - phi) * tna                               # index: rho1
    t3 = np.minimum(phi * a, (1 - phi) * xi) + (1 - phi) * a     # index: rho2
    t2 = np.minimum(phi * a, (1 - phi) * xi)[:, None] + (1 - phi) * tna[None, :]   # [rho1, rho2]
    val = np.maximum(np.maximum(t1[:, None], t2), t3[None, :])
    val = np.where(np.arange(nr)[:, None] > np.arange(nr)[None, :], val, np.inf)   # keep rho1 > rho2, i.e. xi1 > xi2
    i, j = np.unravel_index(int(np.argmin(val)), val.shape)
    if val[i, j] < best111[0]:
        best111 = (float(val[i, j]), (phi, float(xi[i]), float(xi[j])))
    v12 = np.maximum(t1, np.minimum(phi * a, (1 - phi) * xi) + (1 - phi) * T2)
    i = int(np.argmin(v12))
    if v12[i] < best12[0]:
        best12 = (float(v12[i]), (phi, float(xi[i])))
print(f"u={u}: a={a:.6f} h/a={C.h/a:.4f} T2(0)/a={T2/a:.5f}")
print(f"  ladder (1,1,1): {best111[0]/a:.4f} a  at phi={best111[1][0]:.3f}, xi1/a={best111[1][1]/a:.3f}, xi2/a={best111[1][2]/a:.3f}")
print(f"  ladder (1,2)  : {best12[0]/a:.4f} a  at phi={best12[1][0]:.3f}, xi1/a={best12[1][1]/a:.3f}")
print(f"  => T3(0) <= {min(best111[0], best12[0])/a:.4f} a   (grid values: upper bounds)")
