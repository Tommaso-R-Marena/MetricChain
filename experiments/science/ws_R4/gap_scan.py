#!/usr/bin/env python3
"""R4 -- is the gap of the twins monotone in the budget T?  (justifies 'the largest budget with gap > 1'
found by bisection in twins_exact.py).  Also prints the mass split of F_D: inside V2 vs outside."""
import sys
import numpy as np
from scipy.special import logsumexp
from twins_exact import Twins

u = float(sys.argv[1]); n = int(sys.argv[2]); n1 = int(sys.argv[3])
n2 = n - n1
prev = None
nonmono = 0
print(f"# u={u} n={n} n1={n1}:  T/n   gap   lnA_S   lnA_D   -ln(p1+p2)/n   ln(mass of F_D outside V2)")
for T in np.linspace(0.004 * n, 0.09 * n * max(1.0, u), 60):
    t = Twins(n1, n2, u, float(T))
    if not t.ok:
        continue
    outside = ~t.V2
    lm_out = float(logsumexp((t.lp - t.FD)[outside])) if outside.any() else float("-inf")
    flag = ""
    if prev is not None and t.gap > prev + 1e-9:
        nonmono += 1
        flag = "  <-- gap increased"
    prev = t.gap
    print(f"{T/n:.5f}  {t.gap:9.4f}  {t.lnA_S:7.3f}  {t.lnA_D:9.3f}  {t.E():.5f}  {lm_out:9.3f}{flag}")
print(f"# number of grid steps at which the gap increased: {nonmono}")
