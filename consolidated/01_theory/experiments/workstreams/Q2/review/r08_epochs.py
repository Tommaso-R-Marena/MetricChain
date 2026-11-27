#!/usr/bin/env python3
"""r08_epochs.py -- referee: the epoch arithmetic used by Proposition A' and Theorem B, numerically (60 epochs)."""
import math, sys
sys.dont_write_bytecode = True
import rlib
for u in (0.25, 0.5, 1.0, 2.0, 4.0):
    cu = rlib.Cube(u)
    a, h = cu.a, cu.h
    M = 60
    seq = rlib.epochs(cu, M)
    kap = h * h * a / ((a - h) * (a + h) * (2 * a - h))
    c1 = h * (1 + kap) / kap
    c2 = (a + h) * (2 * a - h) / (h * a) - 2
    rbar = (2 * a - h) / (a - h)
    ok = True
    worst = dict(rate=0.0, jump=0.0, sl=0.0, M=0.0)
    for m in range(M):
        d, J, k, B = seq['d'][m], seq['J'][m], seq['k'][m], seq['B'][m]
        ok &= d <= J < d + 1
        ok &= abs(seq['B'][m + 1] - (1 - seq['phi'][m]) * B) < 1e-12 * B          # B_{m+1} = (1 - phi_m) B_m
        ok &= B - h <= c1 / (k + c2) * (1 + 1e-12)
        worst['rate'] = max(worst['rate'], (B - h) * (k + c2) / c1)
        ok &= seq['k'][m + 1] < (1 + rbar) * k
        worst['jump'] = max(worst['jump'], seq['k'][m + 1] / k)
        ok &= J * (J + 1) / (2 * d) < J / 2 + a / h + 1e-12
        worst['sl'] = max(worst['sl'], (J * (J + 1) / (2 * d) - J / 2) / (a / h))
        ok &= seq['R'][m] <= h + 1e-15 and seq['B'][m] <= a + 1e-15 and seq['B'][m] >= h
        if m >= 1:
            ok &= m <= 1 + math.log(k + 1) / math.log(1 + kap)
        ok &= J / d >= 1 and (J - 1) / d < 1
    print("u = %.2f: all checks %s;  max (B_m - h)(k_m + c2)/c1 = %.4f;  max k_{m+1}/k_m = %.3f (1 + rbar = %.3f);"
          "  max [J(J+1)/(2d) - J/2]/(a/h) = %.3f;  c2 = %.3f >= 0;  B_0 = a: %s"
          % (u, "ok" if ok else "FAILED", worst['rate'], worst['jump'], 1 + rbar, worst['sl'], c2, abs(seq['B'][0] - a) < 1e-12))
