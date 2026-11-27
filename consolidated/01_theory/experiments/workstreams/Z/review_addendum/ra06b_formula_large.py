#!/usr/bin/env python3
"""RA06b -- the rows n = 10^12 and 10^15 of the table of A8 at the k of the table (484, 4510) and at neighbouring k,
with the referee's unrolling (as in ra06_formula.py) and the referee's tops (structural to k = 600, h + c_*^2/k^2 beyond).
Usage: python3 -B ra06b_formula_large.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(HERE, '..', '..', 'Q2'))
import q2lib as Q2      # noqa: E402

import ra_lib as R      # noqa: E402

Q = Q2.Q
LN2 = math.log(2.0)
u = 1.0
P = R.Cube(u).setup()
a, h, c2 = P.a, P.h, P.cstar2
cu = Q.Cube(u)
KEX = 600
S = R.EnvSeq(P, KEX)
dmin = int(math.floor(1.0 / (2 * u))) + 2
seq = Q.epoch_seq(cu, 70)


def X0(d):
    return 2.0 + math.log(3.0 * (d + 1)) + 2 * u + math.exp(u)


def b_of(k):
    return S.b[k] if k <= KEX else h + c2 / k ** 2


def E_env(n, eps, dln, k):
    Lam = dln + n * LN2
    X0n = X0(n)
    calX = X0n + 1.0
    chains = levels = 0.0
    for j in range(k, 0, -1):
        alpha = min(eps, 1.0) if j == k else 1.0
        Bp = b_of(j)
        m = Q2.Chain.design_m(cu, n, Bp, calX, alpha, Lam)
        ch = Q2.Chain(cu, n, Bp, calX, alpha, m)
        Lam = Lam + ch.j(n) * Q2.qT(cu, n, Lam + n * Bp, ch.c)
        chains += ch.A_T(n, Lam) + ch.j(n) * ch.Delta_T(n, Lam) + calX + 1.0
        levels += Q2.ell0(cu, n, Lam) + X0n + dmin * LN2 + 2.0
        Lam += Q2.qSb(cu, n, Lam)
    base = Q2.E_new(cu, n, 1.0, Lam - n * LN2, 0, seq)
    return chains, levels, base


dln = math.log(1 / 0.05)
print("# ratio k^2 (b_k - h)/c_*^2 of the structural tops at k = 484, 600: %.5f %.5f" % (484 ** 2 * (S.b[484] - h) / c2, 600 ** 2 * (S.b[600] - h) / c2))
print("#       n       k     total      n(b_k-h)    chains     levels     base      | table of A8")
for ex, ks, tab in ((12, (440, 484, 530), "9.68e5 (484): 3.04e5 / 5.86e5 / 7.80e4 / 514"), (15, (4100, 4510, 4950), "1.13e7 (4510): 3.50e6 / 6.89e6 / 8.91e5 / 643")):
    n = 10 ** ex
    for k in ks:
        c, l, b = E_env(n, 1.0, dln, k)
        nb = n * (b_of(k) - h)
        print("  10^%-3d  %5d  %10.4g  %10.4g  %10.4g  %9.4g  %7.4g     | %s" % (ex, k, nb + c + l + b, nb, c, l, b, tab if k == ks[1] else ""))
