#!/usr/bin/env python3
"""r00_selftest.py -- brute-force check of rlib.Tables for small m, and of the cube constants."""
import math, sys
sys.dont_write_bytecode = True
import rlib
from math import comb

def brute(u, m, eta):
    ce = (1 - eta) / (1 + eta)
    B = [sum(comb(m, j) for j in range(r + 1)) for r in range(m + 1)]
    E = [sum(comb(m, j) * (math.exp(u * (r + 1 - j)) - 1) for j in range(r + 1)) for r in range(m + 1)]
    T = [sum(comb(m, j) * math.exp(-u * max(j - k, 0)) for j in range(m + 1)) for k in range(m + 1)]
    Gt = [math.exp(u) - 1] + [E[r] / B[r - 1] for r in range(1, m + 1)]
    kap = []
    for r in range(m + 1):
        thr = max(1.0, ce * (B[r - 1] if r >= 1 else 0))
        k = max(k for k in range(m + 1) if B[k] <= thr * (1 + 1e-13))
        kap.append(k)
    G2 = [E[r] / T[kap[r]] for r in range(m + 1)]
    return B, E, T, Gt, kap, G2

worst = 0.0
for u in (0.5, 1.0, 2.0):
    for m in (1, 2, 3, 7, 20, 61, 150):
        for eta in (0.5, 0.05, 1/13/7):
            t = rlib.Tables(u, m, eta)
            B, E, T, Gt, kap, G2 = brute(u, m, eta)
            for r in range(m + 1):
                for (x, y) in ((t.lB[r], math.log(B[r])), (t.lE[r], math.log(E[r])), (t.lT[r], math.log(T[r])),
                               (t.lGt[r], math.log(Gt[r])), (t.lG2[r], math.log(G2[r]))):
                    worst = max(worst, abs(x - y))
                assert t.kappa[r] == kap[r], (u, m, eta, r, t.kappa[r], kap[r])
            # r_dagger by brute force for a few thresholds
            for lth in (-3.0, 0.0, 2.0, 5.0, 0.3 * m):
                for lnu0 in (0.0, 3.0, 12.0):
                    th = math.exp(lth); nu0 = math.exp(lnu0)
                    rd = -1
                    for r in range(m):
                        if Gt[r] <= th * (1 - eta) * nu0 * (1 + 1e-12) and min(Gt[r] / ((1 - eta) / (1 + eta)), G2[r]) <= th * (1 + 1e-12):
                            rd = r
                        else:
                            break
                    assert rd == t.rdag(lth, lnu0), (u, m, eta, lth, lnu0, rd, t.rdag(lth, lnu0))
print("tables: max |log difference| against brute force = %.2e ; kappa and r_dagger agree in all cases" % worst)
for u in (0.5, 1.0, 2.0, 4.0):
    cu = rlib.Cube(u)
    kap = cu.h ** 2 * cu.a / ((cu.a - cu.h) * (cu.a + cu.h) * (2 * cu.a - cu.h))
    c1 = cu.h * (1 + kap) / kap
    rbar = (2 * cu.a - cu.h) / (cu.a - cu.h)
    Cs = 2 * math.sqrt((1 + rbar) * c1 * (cu.a / cu.h + 4))
    Csp = 3 * math.sqrt(2 * (1 + rbar) * c1)
    print("u=%.1f p=%.5f a=%.6f h=%.6f h/a=%.5f eps*=%.5f eps*/h=%.3f  kappa=%.5f c1=%.4f c1/a=%.3f rbar=%.4f  C*=%.3f C*'=%.3f ratio=%.4f sqrt(4.5/(a/h+4))=%.4f"
          % (u, cu.p, cu.a, cu.h, cu.h / cu.a, cu.eps_star, cu.eps_star / cu.h, kap, c1, c1 / cu.a, rbar, Cs, Csp, Csp / Cs,
             math.sqrt(4.5 / (cu.a / cu.h + 4))))
# w(c) <= 6.25 c on (0, 1/13], and the three numerical constants of Q7(3)
import numpy as np
cs = np.linspace(1e-9, 1/3, 200001)
w = np.log(np.exp(cs) * (1 + cs) / (1 - cs) + 2 * cs) + cs
print("max w(c)/c on (0,1/3]: %.4f (at c=%.4f);  on (0,1/13]: %.4f" % ((w / cs).max(), cs[(w / cs).argmax()], (w / cs)[cs <= 1/13].max()))
print("2(1+c)e^c/(1-c), 2(1+c)^2e^c/(1-c), 4(1+c)e^c/(1-c), (e^c-1)/c at c=1/3: %.4f %.4f %.4f %.4f" %
      (2*(4/3)*math.exp(1/3)/(2/3), 2*(16/9)*math.exp(1/3)/(2/3), 4*(4/3)*math.exp(1/3)/(2/3), (math.exp(1/3)-1)*3))
print("same at c=1/13: %.4f %.4f %.4f %.4f" % (2*(14/13)*math.exp(1/13)/(12/13), 2*(14/13)**2*math.exp(1/13)/(12/13),
      4*(14/13)*math.exp(1/13)/(12/13), (math.exp(1/13)-1)*13))
