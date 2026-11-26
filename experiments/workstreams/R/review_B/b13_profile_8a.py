"""Referee B, check 13 (NOT in the brief: section 8a, Proposition S, was added to the report after the review began).
A quick independent look at the closed form  f(zeta) = sup_z [2 z^2 + 2 zeta z cot z] - zeta^2/2:
 (a) the stated values f(0) = 2 pi^2, f(2) = pi^2/2 - 2, f(3) = 3/2, f'(2) = -2, f'(3) = -1, and the ODE residual;
 (b) the position formula  p_k(h + delta) - L ~ -sqrt(delta/A) cot(sqrt(A delta) k/h)  on a pair of mine ((1 - sqrt e)_+^3);
 (c) k^2 [T_k(zeta h/k) - theta_hint(zeta h/k)]/(h^2 vartheta) from MY iteration of the recursion (T_cubroot_61.npy, level 61;
     T_gauss_level40.npy) against f(zeta);  theta_hint by the shear: theta_hint(x) = y with theta(x + y) = y."""
import math
import numpy as np
import blib


def f(zeta):
    best = -1e99
    for i in range(1, 200000):
        z = math.pi * i / 200000
        best = max(best, 2 * z * z + 2 * zeta * z / math.tan(z))
    for i in range(1, 20000):
        y = 20.0 * i / 20000
        best = max(best, -2 * y * y + 2 * zeta * y / math.tanh(y))
    best = max(best, 2 * zeta)                      # z -> 0
    return best - zeta * zeta / 2


print("(a) f(0) = %.6f (2 pi^2 = %.6f);  f(2) = %.6f (pi^2/2 - 2 = %.6f);  f(3) = %.6f (3/2)" % (f(1e-9), 2 * math.pi ** 2, f(2), math.pi ** 2 / 2 - 2, f(3)))
d = 1e-4
for z in [0.5, 1.0, 2.0, 3.0, 4.0]:
    f0, f1 = f(z), (f(z + d) - f(z - d)) / (2 * d)
    print("    zeta = %.1f: f = %.6f, f' = %.5f, ODE residual zeta f'^2/2 + zeta f' + (zeta - 2) f = %+.2e" % (z, f0, f1, z * f1 * f1 / 2 + z * f1 + (z - 2) * f0))

print("(b) position of the orbit, pair (1 - sqrt e)_+^3")
P = blib.cubroot().setup()
A = 1 / (2 * P.vartheta)
for k in [100, 400, 1600]:
    row = []
    for z in [0.5, 1.0, 1.5708, 2.2, 2.8]:
        dl = (z * P.h / k) ** 2 / A
        pk = P.p(P.h + dl, k)
        pred = -math.sqrt(dl / A) / math.tan(z)
        row.append("z=%.2f: k (p_k - L) = %+.4f, prediction %+.4f" % (z, k * (pk - P.L), k * pred))
    print("    k = %4d:  " + "; ".join(row) if False else "    k = %4d:  %s" % (k, "; ".join(row)))


def theta_hint(P, x):
    lo, hi = 0.0, P.a
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if P.theta(x + mid) > mid:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


print("(c) the recursion's profile against f")
for name, fn, lev, P in [("(1 - sqrt e)_+^3", "T_cubroot_61.npy", 61, blib.cubroot().setup()), ("Gaussian", "T_gauss_level40.npy", 40, blib.gauss().setup())]:
    x, T = np.load(fn)
    row = []
    for zeta in [0.25, 0.5, 1.0, 2.0, 3.0, 5.0]:
        xx = zeta * P.h / lev
        val = (float(np.interp(xx, x, T)) - theta_hint(P, xx)) * lev * lev / (P.h ** 2 * P.vartheta)
        row.append("%.3f (f = %.3f)" % (val, f(zeta)))
    tau = T[0]
    print("    %s, k = %d:  zeta = 0: %.3f (f = %.3f);  zeta = .25, .5, 1, 2, 3, 5:  %s" % (name, lev, (tau - P.h) * lev * lev / (P.h ** 2 * P.vartheta), 2 * math.pi ** 2, "  ".join(row)))
