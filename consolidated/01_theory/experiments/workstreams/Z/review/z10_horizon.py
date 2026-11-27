#!/usr/bin/env python3
"""z10: Proposition Z3 at horizons far above the dimension (N = 100 d ... 3000 d, d small) -- the least accuracy X = X_0(N) + 1
is then well above X_0(d) + 1 and the grid of the inner family is much finer than 1/d.  Same checks as z03 (A), (B), (C), (D);
ALL admissible outer blocks are evaluated exactly (d is small).  Usage: python3 z10_horizon.py [seconds]"""
import math
import random
import sys
import time

import numpy as np

sys.dont_write_bytecode = True
import zrev
import zlev

TMAX = float(sys.argv[1]) if len(sys.argv) > 1 else 120.0
random.seed(17)
t0 = time.time()
tot = dict(cases=0, levels=0)
worst = dict(A=-1e18, B=-1e18, C=-1e18, D=-1e18, gave=0.0)
viol = 0
chains = {}
for u, dst, eps1 in ((1.0, 0.05, 0.003), (2.0, 0.05, 0.01), (0.5, 0.05, 0.0008)):
    cu = zrev.Cube(u)
    chains[u] = (cu, zrev.Chain(cu, dst, eps1, 14))
while time.time() - t0 < TMAX:
    u = random.choice(list(chains))
    cu, C = chains[u]
    dm = zlev.dmin(u)
    d = dm + random.randint(1, 120)
    N = d * random.choice([100, 300, 1000, 3000])
    j = random.choice([0, 1, 3, 5, 6, 8, 12])
    ld = random.choice([math.log(0.3), math.log(1e-6), -3.0 * d])
    X0d = zlev.X0(u, d)
    calX = zlev.X0(u, N) + 1
    xh = calX + random.choice([0.0, 0.5, 3.0, 0.2 * d, u * d])
    y = xh - X0d
    Bs, Ws = C.grid(j, N)
    lines = zlev.Lines(Bs, np.minimum(Ws, 1.0))
    Bn, Wn = C.grid(j + 1, N)
    nxt = zlev.Lines(Bn, np.minimum(Wn, 1.0))
    inner = zlev.Sat(lines)
    Lam = -ld + d * zlev.LN2
    l0 = zlev.ell0(u, d, Lam)
    nos, Pi = zlev.proxy_all(cu, d, y, lines)
    kb = int(np.argmin(Pi))
    exC = Pi[kb] - (d * float(nxt.env([y / d])[0]) + d / N + 1 + cu.a * dm)
    typ = float(nxt.major(d, [xh])[0])
    best = 1e300
    for n_o in nos:
        r = zlev.level_Z2(cu, d, int(n_o), y, ld, inner.cost)
        tot['levels'] += 1
        worst['A'] = max(worst['A'], r['xout'] - xh)
        worst['B'] = max(worst['B'], r['lC'] - (float(Pi[n_o - 1]) + l0))
        best = min(best, r['lC'])
        if n_o == nos[kb]:
            lstar = r['lC']
    exD = lstar - (typ + l0 + X0d + dm * zlev.LN2 + 2)
    worst['C'] = max(worst['C'], exC)
    worst['D'] = max(worst['D'], exD)
    worst['gave'] = max(worst['gave'], lstar - best)
    viol += (exC > 1e-9) + (exD > 1e-9)
    tot['cases'] += 1
viol += (worst['A'] > 1e-9) + (worst['B'] > 1e-9)
print("horizons N = 100 d ... 3000 d, d = d_min + 1 ... d_min + 120, u in {1/2, 1, 2}, levels j <= 12: %d cases, %d levels (every admissible n_o)  [%.0f s]"
      % (tot['cases'], tot['levels'], time.time() - t0))
print("largest excess (negative = slack): (A) accuracy %.4f, (B) (U-infinity) %.3f, (C) exponent step %.4f, (D) type %.3f;  violations: %d"
      % (worst['A'], worst['B'], worst['C'], worst['D'], viol))
print("the proxy choice of n_o costs at most %.3f nats more than the n_o with the least certified bound" % worst['gave'])
