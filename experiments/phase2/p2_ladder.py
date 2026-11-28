#!/usr/bin/env python3
"""p2_ladder.py -- a tempering ladder with L rungs on a dip (docs/phase2/BRIDGE_NOTE.md, section 6.7; a question
of the certified-MBAR division, MBAR-MSG-0001 section 5(a)).

Instance: the dip w = max(1, e^{u (r - d)}) on the n-cube (d the Hamming distance to a centre) and its tempered
ensembles mu_k proportional to w^{k/L} pi, k = 0..L.  Everything is radial, so all sums are binomial sums in
log-space (exact up to floating point).

  L1  the least overlap of two consecutive tempered ensembles of the last rung, maximised over the radius:
      exponent c_L = -(1/n) ln sum_d min(mu_{L-1}(d), mu_L(d)).
  L2  a lower bound for the asymptotic variance V_c(s) of the end-to-end free-energy contrast in the multistate
      model, valid for EVERY allocation s on the simplex, from the test function a = 1{d < r} in the dual form
          V_c(s) >= (f_L - f_0)^2 / sum_k s_k f_k (1 - f_k) >= (f_L - f_0)^2 / max_k f_k (1 - f_k),
      f_k = mu_k(d < r): its exponent, maximised over the radius, against the upper bound u/L of the path bound
      (chi^2 of a step at most e^{u n / L}/4).

Printed: L x exponent for L = 2..16 at u = 1, 2; PASS if the exponents are positive, decrease with L, stay below
u/L, and L x exponent stays within a factor 1.5 over the range of L (a 1/L law).
"""
import math
import sys
import numpy as np

FAILS = []


def lgC(n):
    lg = np.array([math.lgamma(k + 1) for k in range(n + 1)])
    return lg[n] - lg - lg[::-1]


def lse(v):
    m = v.max()
    return m + math.log(np.exp(v - m).sum())


def radial_log_law(n, u, r, lam, lc):
    d = np.arange(n + 1)
    lw = lc - n * math.log(2) + np.maximum(0.0, lam * u * (r - d))
    return lw - lse(lw)


n = 20000
lc = lgC(n)
radii = range(int(0.05 * n), int(0.5 * n), 50)
for u in (1.0, 2.0):
    rows1, rows2, e1, e2 = [], [], [], []
    for L in (2, 3, 4, 8, 16):
        best1, best2 = (-1.0, None), (-1.0, None)
        for r in radii:
            laws = [radial_log_law(n, u, r, k / L, lc) for k in range(L + 1)]
            c_last = -lse(np.minimum(laws[L - 1], laws[L])) / n
            if c_last > best1[0]:
                best1 = (c_last, r)
            lf = [(lse(l[:r]), lse(l[r:])) for l in laws]              # ln f_k, ln (1 - f_k)
            fL, f0 = math.exp(lf[L][0]), math.exp(lf[0][0])
            if fL > f0:
                lb = (2 * math.log(fL - f0) - max(a_ + b_ for (a_, b_) in lf)) / n
                if lb > best2[0]:
                    best2 = (lb, r)
        e1.append(best1[0])
        e2.append(best2[0])
        rows1.append("L=%d: %.5f (r/n=%.3f, L x = %.4f)" % (L, best1[0], best1[1] / n, L * best1[0]))
        rows2.append("L=%d: %.5f (r/n=%.3f, L x = %.4f; u/L = %.4f)" % (L, best2[0], best2[1] / n, L * best2[0], u / L))
    Ls = (2, 3, 4, 8, 16)
    ok1 = all(x > 0 for x in e1) and all(e1[i] > e1[i + 1] for i in range(4)) and max(L * x for L, x in zip(Ls, e1)) < 1.5 * min(L * x for L, x in zip(Ls, e1))
    ok2 = all(x > 0 for x in e2) and all(e2[i] > e2[i + 1] for i in range(4)) and all(x < u / L for L, x in zip(Ls, e2)) \
        and max(L * x for L, x in zip(Ls, e2)) < 1.5 * min(L * x for L, x in zip(Ls, e2))
    for name, ok, rows in (("L1 least overlap of the last two tempered ensembles (exponent)", ok1, rows1),
                           ("L2 lower bound for the variance of the end-to-end contrast, every allocation (exponent)", ok2, rows2)):
        print("%s %s, u=%g, n=%d\n    %s" % ("PASS" if ok else "FAIL", name, u, n, "; ".join(rows)))
        if not ok:
            FAILS.append(name)
print("ALL PASS" if not FAILS else "FAILED")
sys.exit(1 if FAILS else 0)
