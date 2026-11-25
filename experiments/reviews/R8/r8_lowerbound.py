#!/usr/bin/env python3
"""Referee R8 -- the hinted lower bound of Theorem 11.25(a) in the three regimes of Theorem K3 / Corollary K3'
(item 9 of the brief): exponent of (1-2 delta) 2^n/|B(n,k*(eps))|, k*(eps) the least k with Delta_k > eps,
Delta_k = ln(1 + 2^{-n} E_k(n)), for (i) fixed eps, (ii) eps_n -> 0 with ln(1/eps_n) = o(n), (iii) eps_n -> inf,
eps_n = o(n); and for comparison one sequence outside the theorem (eps_n = e^{-0.02 n}).  Own code.
Part 1: k* in exact integer arithmetic for e^u = 2 against the floating-point tables (n <= 3000)."""
import math, sys, time
from fractions import Fraction as Fr
import numpy as np
from r8_flat import tabF
t0 = time.time()
# part 1: exact k* for e^u = 2
bad = 0; ncmp = 0
for n in (10, 57, 200, 1000, 3000):
    C = 1; ball = 0; F = 0
    Es = []
    for r in range(n + 1):
        C = C if r == 0 else C * (n - r + 1) // r
        ball += C
        F = 2 * (F + C)                 # F_r = e^u (F_{r-1} + C(n,r)), e^u = 2
        Es.append(F - ball)             # E_r exact integer
    t = tabF(n, math.log(2.0))
    for eps_fr in (Fr(1, 1000), Fr(1, 10), Fr(1), Fr(10), Fr(50)):
        # least k with E_k > 2^n (e^eps - 1): compare with rational bounds of e^eps - 1 from mpmath
        import mpmath as mp
        mp.mp.dps = 50
        thr = mp.mpf(2) ** n * (mp.e ** (mp.mpf(eps_fr.numerator) / eps_fr.denominator) - 1)
        k_ex = next(k for k in range(n + 1) if mp.mpf(Es[k]) > thr) if mp.mpf(Es[n]) > thr else None
        target = n * math.log(2) + math.log(math.expm1(float(eps_fr)))
        k_fl = int(np.searchsorted(t.lE, target, side='right'))
        k_fl = k_fl if k_fl <= n else None
        ncmp += 1
        if k_ex != k_fl:
            bad += 1; print("k* differs:", n, eps_fr, k_ex, k_fl)
print("part 1: k*(eps) from exact integers (e^u = 2) against the floating-point tables: %d comparisons, %d differences" % (ncmp, bad))
# part 2: exponents
for u in (0.5, 1.0, 2.0):
    lam1 = math.log(2 / (1 + math.exp(-u))); rho = lam1 / u
    h = math.log(2) + rho * math.log(rho) + (1 - rho) * math.log(1 - rho)
    print("u = %.1f, h = %.6f; entries: n^{-1} ln[(1-2 delta) 2^n / |B(n,k*)|] / h  with delta = 0.25  (and k*/n - Lambda_1/u)" % (u, h))
    # each sequence is given by ln(eps_n)
    seqs = [("eps = 0.01", lambda n: math.log(0.01)), ("eps = 1", lambda n: 0.0), ("eps = 30", lambda n: math.log(30.0)),
            ("eps_n = n^-3", lambda n: -3.0 * math.log(n)), ("eps_n = exp(-sqrt n)", lambda n: -math.sqrt(n)),
            ("eps_n = exp(-n^0.8)", lambda n: -n ** 0.8),
            ("eps_n = sqrt n", lambda n: 0.5 * math.log(n)), ("eps_n = n/ln(n)^2", lambda n: math.log(n) - 2 * math.log(math.log(n))),
            ("[outside] eps_n = exp(-0.02 n)", lambda n: -0.02 * n)]
    ns = (1000, 10000, 100000, 1000000)
    print("   %-32s" % "sequence" + "".join("      n=%-9d" % n for n in ns))
    for name, f in seqs:
        row = ""
        for n in ns:
            t = tabF(n, u)
            le = f(n)
            if le < -20:
                lt = le                               # ln(e^eps - 1) = ln eps + O(eps)
            elif le < math.log(30):
                lt = math.log(math.expm1(math.exp(le)))
            else:
                e_ = math.exp(le)
                lt = e_ + math.log1p(-math.exp(-e_))
            target = n * math.log(2) + lt
            k = int(np.searchsorted(t.lE, target, side='right'))
            k = min(k, n)
            val = (math.log(0.5) + n * math.log(2) - t.lB[k]) / n
            row += "  %6.4f (%+.4f)" % (val / h, k / n - rho)
        print("   %-32s%s" % (name, row))
print("[%.0f s]" % (time.time() - t0))
