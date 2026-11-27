#!/usr/bin/env python3
"""R9, item 2(b): E' = -ln max(p1,p2)/n against E = -ln(p1+p2)/n on the rows of the table of Theorem 11.86.
RE-RUN of R4's code (experiments/science/ws_R4/twins_exact.py, class Twins and largest_budget; imported read-only,
no bytecode written).  For n <= 1600 the budget is found by R4's bisection for every split; for n = 3200 the stored
best split and budget of R4's output are used for one evaluation."""
import sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/MetricChain/experiments/science/ws_R4")
import twins_exact as TE

def row(u, n, splits=(0.45, 0.50, 0.55, 0.60, 0.65)):
    best = None
    for s in splits:
        n1 = int(round(s * n)); n2 = n - n1
        t = TE.largest_budget(n1, n2, u, 1.0)
        if t is None:
            continue
        if best is None or t.E() > best.E():
            best = t
    return best

def report(u, t):
    n = t.n1 + t.n2
    E = t.E(); Ep = -max(t.lnp1, t.lnp2) / n
    print(f"u = {u}, n = {n:5d}, n1 = {t.n1:5d}, T = {t.T:10.4f}: lnp1 = {t.lnp1:.6f}, lnp2 = {t.lnp2:.6f};  E = {E:.7f}  E' = {Ep:.7f}  "
          f"E' - E = {Ep - E:.3e}   (4 decimals: {E:.4f} / {Ep:.4f}; 4 significant: {E:.3e} / {Ep:.3e});  ln2/n = {math.log(2)/n:.2e}")
    sys.stdout.flush()

for u, ns in ((1.0, (200, 400, 800, 1600)), (2.0, (200, 400, 1600))):
    for n in ns:
        t = row(u, n)
        if t is None:
            print(f"u = {u}, n = {n}: no budget with gap > 1"); continue
        report(u, t)
t = TE.Twins(1760, 1440, 1.0, 125.6841)
report(1.0, t)
