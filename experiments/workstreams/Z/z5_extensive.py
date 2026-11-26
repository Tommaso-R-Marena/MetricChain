#!/usr/bin/env python3
"""Z5: the envelope schedule at EXTENSIVE accuracies.  Proposition Z4 gives the type of the k-th family at every
accuracy, so  ln N(n; g n, delta) <= n M_{W_k, b_k}(g - X_0/n) + k c_Z ln n + O(ln n)  for every accuracy rate g:
the exponent at the rate g is  M_k(g) = max_{B <= b_k} [B - W_k(B) g]  >=  T_k(g)  >=  theta_hint(g).
This script prints M_k(g) - theta_hint(g) for the cube (floating point on grids, [N]) and k^2 times it:
is the 1/k^2 law uniform in the accuracy rate?
Usage: python3 z5_extensive.py [u]     (default 1.0)
"""
import math
import sys

import numpy as np

import zetalib as Z

u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
C = Z.EnvZ(u, 80, 8000)
a, h = C.a, C.h
lam1 = math.log(2 / (1 + math.exp(-u)))
epsstar = math.log(math.cosh(u / 2))


def kl(x, y):
    return x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))


def theta_hint(g):
    rho = (lam1 + g) / u
    return kl(rho, 0.5) if rho < 0.5 else 0.0


print("# cube u = %g: a = %.6f, h = %.6f, eps* = %.6f (theta_hint vanishes from eps* on); c_*^2 = %.6f" % (u, a, h, epsstar, C.P.const))
gs = [0.0, 0.01 * h, 0.1 * h, 0.5 * h, 1.0 * h, 0.25 * epsstar, 0.5 * epsstar, 0.8 * epsstar]
print("# rows: k;  columns: g = " + ", ".join("%.4g" % g for g in gs))
print("# entries: k^2 (M_k(g) - theta_hint(g)) / c_*^2      [at g = 0 this is k^2 (b_k - h)/c_*^2]")
ok = True
for k in (2, 3, 5, 10, 20, 40, 80):
    x, W = C.curves[k]
    row = []
    for g in gs:
        M = float(np.max(x - W * g))
        d = M - theta_hint(g)
        if d < -1e-7:
            ok = False
        row.append(k * k * d / C.P.const)
    print("  %3d  " % k + "  ".join("%8.4f" % r for r in row))
print("M_k(g) >= theta_hint(g) everywhere: %s" % ok)
