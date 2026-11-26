#!/usr/bin/env python3
"""r07_U1.py -- referee: Corollary U1.  The level AS BUILT of Proposition Q6 (ladder capped at ceil(x-hat), b = 1, e = h)
against the sharper error term:  ln C_max <= n B - sigma' x-hat + sigma'(1 + c_log(n) + h) + ell_0(n, Lam) + E(n, 1; Lam + q_S)."""
import math, sys, time
sys.dont_write_bytecode = True
import numpy as np
import rlib
from rlib import LN2, INF
import r04_built as R4

t0 = time.time()
tot = viol = 0
gmin = (INF, None)
maxgain = 0.0
Efl = R4.__dict__.get('Efl', None)
Efs = [None, lambda d, x, Lam: 3 * math.sqrt(d) + 0 * x, lambda d, x, Lam: Lam / 7 + 0 * x]
for u in (0.5, 1.0, 2.0):
    cu = rlib.Cube(u)
    a, h = cu.a, cu.h
    seq = rlib.epochs(cu, 13)
    types = []
    for m in range(0, 13):
        for j in sorted(set([1, 2, (seq['J'][m] + 1) // 2, seq['J'][m]])):
            if 1 <= j <= seq['J'][m]:
                s = (j - 1) / seq['d'][m]
                types.append((seq['B'][m], s, h / (j - 1) if j >= 2 else INF))
    for (Bh, s, Rh) in ((1.0, 0.0, INF), (1.01, 0.3, 1.0), (2.0, 1.0, 1 / 3), (11.0, 0.3, 1 / 50), (2.0, 0.0, INF), (11.0, 1.0, 1.0)):
        types.append((Bh * h, s, Rh * h if Rh < INF else INF))
    for (B, s, R) in types:
        if R < INF and B < s * R:
            continue
        Rp = h if R == INF else R * h / (h + R)
        sp = s + B / h - 1
        for n in (300, 3000, 30000, 300000):
            X0 = 1 + rlib.c_log(cu, n) + h
            top = Rp * n
            if top < X0:
                continue
            for xh in sorted(set([X0, X0 + h, 0.5 * (X0 + top), top])):
                for ie, ld in enumerate((math.log(0.05), -27.6, -float(n), -50.0 * n)):
                    Ef = Efs[ie % 3]
                    fam = rlib.SatFamily([(B, s)], R, Ef, floor0=True)
                    n_o = math.floor((xh - 1 - rlib.c_log(cu, n)) / h + 1e-12)
                    n_i = n - n_o
                    lth = rlib.ltheta_for_accuracy(cu, n, xh, 1.0)
                    x1 = min(math.ceil(xh - 1e-12), math.ceil(2 * u * n_i - 1e-12) - 1)       # Q6's ladder
                    xs = [float(x1 - i) for i in range(x1)]
                    lev = rlib.Level(u, n, n_o, 1.0, 0.5, 1.0, lth, 1.0, 1.0, ld, len(xs))
                    lcm = lev.lcmax(xs, R4.costs(fam, n_i, xs, lev.ldp))
                    Lam = -ld + n * LN2
                    E1 = fam.E(n, 1.0, Lam + rlib.q_b(cu, n, Lam))
                    bound = n * B - sp * xh + sp * (1 + rlib.c_log(cu, n) + h) + rlib.ell0_b(cu, n, Lam) + E1
                    tot += 1
                    sl = bound - lcm
                    if sl < -1e-9 or abs(lev.x_out - xh) > 1e-9:
                        viol += 1
                    if sl < gmin[0]:
                        gmin = (sl, (u, n, n_o, round(xh, 2), round(B / h, 3), round(s, 3), "inf" if R == INF else round(R / h, 3), round(ld, 1)))
                    maxgain = max(maxgain, (1 - s) * (1 + rlib.c_log(cu, n) + h))
    print("u = %.1f done [%.0f s]" % (u, time.time() - t0), flush=True)
print("levels of Q6 as built: %d, violations of the bound with c_S' %d, least slack %.3f at (u, n, n_o, x-hat, B/h, sigma, R/h, ln delta) = %s"
      % (tot, viol, gmin[0], gmin[1]))
print("largest c_S - c_S' over the cases: %.1f nats" % maxgain)
