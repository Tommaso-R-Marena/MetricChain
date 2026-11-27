#!/usr/bin/env python3
"""r29_i6_crossover.py [u]  --  Item 6: where is the bound of Theorem 11.58e below what non-adaptive algorithms need?

My own numbers for the non-adaptive side (theory report, Theorem 11.45(b), as quoted there): for the accuracy eps and
failure probability delta, every randomised non-adaptive algorithm that is (eps/2, delta)-correct on the cube class needs
at least  LB(n) = (1 - 2 delta) 2^n/|B(n, R - 1)|  evaluations, R the least radius with D_R > eps,
    D_R = n ln(1 + e^-u) - ln sum_j C(n, j) e^{-u max(j, R)}.
(Computed in the log domain with lgamma; a spot check against exact integer/40-digit arithmetic is printed.)
Against it:  n h (the hinted lower bound, up to O(1)),  n a,  n ln 2 (enumeration), and
  * the certified cost of their exact nests (two envelope levels over the real base; numbers of their committed
    outputs and of my re-runs, passed on the command line as  N:lncost ...),
  * the formula of Theorem 11.58e(d) as THEY evaluate it (out_z2_formula_u1_env.txt, read only):  n h + excess(n).
"""
import math
import sys

import numpy as np

import r29lib as R
import r29env as E

R.cap_memory()
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
nests = dict((int(x.split(":")[0]), float(x.split(":")[1])) for x in sys.argv[2:])
P = E.CubeF(u)
a, h = P.a, P.h
eps, delta = 1.0, 0.05


def lb_na(n):
    j = np.arange(0, n + 1)
    lC = np.array([math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) for k in j])
    lcum = np.logaddexp.accumulate(lC)                       # ln |B(n, r)|
    lZ = n * math.log(1 + math.exp(-u))

    def D(Rr):
        return lZ - float(np.logaddexp.reduce(lC - u * np.maximum(j, Rr)))
    lo, hi = 0, n                                            # D is nondecreasing in R, D_0 = 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if D(mid) > eps:
            hi = mid
        else:
            lo = mid
    Rr = hi
    return math.log(1 - 2 * delta) + n * math.log(2.0) - float(lcum[Rr - 1]), Rr, D(Rr)


def lb_na_exact(n):
    import mpmath
    mpmath.mp.dps = 40
    C = [1]
    for k in range(1, n + 1):
        C.append(C[-1] * (n - k + 1) // k)
    emu = mpmath.exp(-mpmath.mpf(u))
    lZ = n * mpmath.log(1 + emu)
    Rr = None
    for r in range(0, n + 1):
        s = sum(C[k] * emu ** max(k, r) for k in range(n + 1))
        if lZ - mpmath.log(s) > eps:
            Rr = r
            break
    return float(mpmath.log(mpmath.mpf(1 - 2 * delta) * mpmath.mpf(2) ** n / sum(C[:Rr]))), Rr


print("# cube u = %g: h = %.6f, a = %.6f; accuracy eps = 1, delta = 0.05" % (u, h, a))
for n in (200, 700):
    x1, r1, _ = lb_na(n)
    x2, r2 = lb_na_exact(n)
    print("# spot check n = %d: ln LB (log domain) = %.9f, R = %d;  exact integers / 40 digits: %.9f, R = %d" % (n, x1, r1, x2, r2))
print("#       n |     n h |     n a | ln LB_na (R; n a - ln LB) | n ln 2 | exact nest (their evaluator): ln cost | nest < ln LB_na ?")
for n in sorted(set([1000, 1400, 2000, 3000, 4000, 6000, 8000, 10000, 12000, 16000, 32000, 50000, 100000] + list(nests))):
    lb, Rr, DR = lb_na(n)
    nc = nests.get(n)
    print("  %7d | %7.1f | %7.1f | %9.2f (R = %5d; %6.2f) | %8.1f | %s | %s"
          % (n, n * h, n * a, lb, Rr, n * a - lb, n * math.log(2), ("%9.2f" % nc) if nc else "        -", ("yes" if nc < lb else "NO") if nc else "-"))
# their formula table (read only)
path = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_07cde81/experiments/workstreams/Z/out_z2_formula_u1_env.txt"
if u == 1.0:
    print("# their formula of Theorem 11.58e(d) (out_z2_formula_u1_env.txt): n | n h + excess | ln LB_na (mine) | below ?")
    for line in open(path):
        if line.startswith("#") or "|" not in line:
            continue
        f = line.split("|")
        n = int(round(10 ** float(f[0].split()[0].replace("10^", ""))))
        exc = float(f[3].split()[0])
        if n <= 10 ** 6:
            lb, Rr, _ = lb_na(n)
            print("  %8d | %10.1f | %10.1f | %s   (levels k = %s)" % (n, n * h + exc, lb, "yes" if n * h + exc < lb else "NO", f[3].split()[1]))
R.finish("r29_i6_crossover u=%g" % u)
