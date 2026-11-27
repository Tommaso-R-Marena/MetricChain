"""Tilt-state recursion (DP2): (1) finite chains against exact maxima over all vertices (n = 3, 4); (2) the threshold: relaxed
growth rate of max KL(pi || pi_phi) against E_F; (3) upper bounds for F_inf(t), h, a with a symmetric Markov reference Q.
usage: python3 y10_dp2.py [part ...]   parts: 1 2 3 (default all);  for part 3 optionally p values after '--'"""
import sys, time, math
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *
from ylyap import E_F
from ydp2 import DP2

t0 = time.time(); u = 1.0
args = sys.argv[1:]
ps = [float(x) for x in args[args.index("--") + 1:]] if "--" in args else [0.4, 0.3, 0.2, 0.1]
parts = [a for a in (args[:args.index("--")] if "--" in args else args)] or ["1", "2", "3"]
hc, ac, Ec = cube_numbers(u)

def markov_law(n, q):
    return bsc_block_law(n, q)

if "1" in parts:
    print("(1) finite chains: relaxed value (G=401, C=41) against the exact maximum over ALL vertices")
    for n in (3, 4):
        H = height_functions(n) * u
        for p in (0.4, 0.3, 0.1):
            pi = bsc_block_law(n, p); P = gibbs_rows(pi, H); dp = DP2(p, u, 401, 41)
            row = []
            for t in (0.3, 0.45, 0.7):
                for qt in (p, 0.5 * (p + 0.5)):
                    Q = markov_law(n, qt)
                    exact = float((-np.log((P ** t) @ (Q ** (1 - t)))).max())
                    rel = dp.renyi_finite(n, t, qt)
                    row.append("t=%.2f qt=%.2f: exact %.6f relaxed %.6f" % (t, qt, exact, rel))
            exactK = float(((pi * np.log(pi)).sum() - np.log(P) @ pi).max())
            print("  n=%d p=%.1f: %s" % (n, p, " | ".join(row)))
            print("          max_phi KL(pi||pi_phi): exact %.7f, relaxed %.7f" % (exactK, dp.kl_finite(n)))
    print("  %.0f s" % (time.time() - t0))

if "2" in parts:
    print("\n(2) threshold: growth rate of the relaxed maximum of KL(pi||pi_phi) (upper bound for E_inf) against E_F")
    for p in (0.4, 0.3, 0.2, 0.1):
        row = []
        for (G, C) in ((201, 21), (401, 41), (801, 41)):
            lo, hi = DP2(p, u, G, C).kl_rate()
            row.append("G=%d,C=%d: [%.7f, %.7f]" % (G, C, lo, hi))
        print("  p=%.1f: E_F = %.7f;  relaxed rate %s" % (p, E_F(p, u), "  ".join(row)))
    print("  %.0f s" % (time.time() - t0))

if "3" in parts:
    print("\n(3) upper bounds for the game function: F_inf(t) <= min_qt rate(t, qt)   (cube h = %.6f, a = %.6f)" % (hc, ac))
    for p in ps:
        dp = DP2(p, u, 301, 21)
        def best_q(t):
            f = lambda q: -dp.renyi_rate(t, q)[1]
            qs = np.linspace(0.5 * p, 0.5, 9); vals = [f(q) for q in qs]; i = int(np.argmax(vals))
            q, v = golden_max(f, qs[max(i - 1, 0)], qs[min(i + 1, len(qs) - 1)], it=14)
            return -v, q
        res = {}
        for t in (0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.8, 0.9, 0.97):
            res[t] = best_q(t)
        tb = max((t for t in res if t <= 0.6), key=lambda t: res[t][0])
        tt, hb = golden_max(lambda t: best_q(t)[0], max(tb - 0.07, 0.05), tb + 0.07, it=10)
        # grid check at the optimum
        qb = best_q(tt)[1]
        chk = DP2(p, u, 601, 41).renyi_rate(tt, qb)[1]
        print("  p=%.1f: " % p + "  ".join("F(%.2f)<=%.6f(qt=%.3f)" % (t, res[t][0], res[t][1]) for t in sorted(res)))
        print("        h <= %.6f at t=%.3f, qt=%.3f (G=301,C=21);  same point with G=601,C=41: %.6f  | a <= sup_t F/(1-t) on the grid: %s  [%.0f s]" % (
            hb, tt, qb, chk, "  ".join("t=%.2f: %.6f" % (t, res[t][0] / (1 - t)) for t in (0.8, 0.9, 0.97)), time.time() - t0))
print("%.1f s" % (time.time() - t0))
