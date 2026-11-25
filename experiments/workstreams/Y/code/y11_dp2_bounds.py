"""Tilt-state recursion (DP2) with a symmetric Markov reference Q (flip probability qt): upper bounds
F_inf(t) <= min_qt rate(t, qt), hence h <= max_t (...), a <= sup_t (...)/(1-t).  The value used is the SAFE end of the
value-iteration bracket (-ln of the smallest ratio W_{k+1}/W_k, which is monotone in k).
usage: python3 y11_dp2_bounds.py p [G C]"""
import sys, time, math
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *
from ydp2 import DP2

t0 = time.time(); u = 1.0
p = float(sys.argv[1]); G = int(sys.argv[2]) if len(sys.argv) > 2 else 201; C = int(sys.argv[3]) if len(sys.argv) > 3 else 21
hc, ac, Ec = cube_numbers(u)
dp = DP2(p, u, G, C); cache = {}
ITERS = int(sys.argv[4]) if len(sys.argv) > 4 else 2500
def rate(t, q):
    k = (round(t, 6), round(q, 6))
    if k not in cache: cache[k] = dp.renyi_rate(t, q, iters=ITERS, tol=1e-8)
    return cache[k]
def best_q(t):
    f = lambda q: -rate(t, q)[1]
    qs = np.linspace(0.5 * p, min(1.3 * p, 0.5), 7); vals = [f(q) for q in qs]; i = int(np.argmax(vals))
    q, v = golden_max(f, qs[max(i - 1, 0)], qs[min(i + 1, len(qs) - 1)], it=8)
    return -v, q, rate(t, q)[0]
print("p = %.2f, u = 1, grid G=%d, C=%d;  cube h = %.6f, a = %.6f" % (p, G, C, hc, ac), flush=True)
res = {}
for t in (0.35, 0.4, 0.45, 0.5):
    res[t] = best_q(t)
    print("  t=%.2f: F_inf(t) <= %.6f at qt=%.4f (unconverged end of the bracket: %.6f);  /(1-t): %.6f;  qt=p gives %.6f   [%.0f s]" % (
        t, res[t][0], res[t][1], res[t][2], res[t][0] / (1 - t), rate(t, p)[1], time.time() - t0), flush=True)
tb = max((t for t in res if t <= 0.6), key=lambda t: res[t][0])
tt, hb = golden_max(lambda t: best_q(t)[0], max(tb - 0.05, 0.05), tb + 0.05, it=7)
qb = best_q(tt)[1]
print("  h <= %.6f at t=%.3f, qt=%.4f   (ratio to the cube %.3f)   [%.0f s]" % (hb, tt, qb, hb / hc, time.time() - t0), flush=True)
chk = DP2(p, u, 2 * G - 1, 2 * C - 1).renyi_rate(tt, qb, iters=ITERS, tol=1e-8)
print("     the same point (t, qt) on the grid G=%d, C=%d: [%.6f, %.6f]   [%.0f s]" % (2 * G - 1, 2 * C - 1, chk[0], chk[1], time.time() - t0), flush=True)
# a: the Shannon version (t -> 1): a_inf <= min_qt growth of the relaxed max of KL(pi_phi || Q_qt)
fa = lambda q: -dp.shannon_rate(q, iters=ITERS, tol=1e-8)[1]
qs = np.linspace(0.6 * p, min(1.2 * p, 0.5), 7); vals = [fa(q) for q in qs]; i = int(np.argmax(vals))
qa, va = golden_max(fa, qs[max(i - 1, 0)], qs[min(i + 1, len(qs) - 1)], it=8)
print("  a <= %.6f at qt=%.4f (unconverged end %.6f; ratio to the cube %.3f)   [%.0f s]" % (-va, qa, dp.shannon_rate(qa, iters=ITERS, tol=1e-8)[0], -va / ac, time.time() - t0), flush=True)
lo, hi = dp.kl_rate()
from ylyap import E_F
print("  E <= %.7f (relaxed growth of max KL(pi||pi_phi); E_F = %.7f)" % (hi, E_F(p, u)), flush=True)
print("%.1f s" % (time.time() - t0))
