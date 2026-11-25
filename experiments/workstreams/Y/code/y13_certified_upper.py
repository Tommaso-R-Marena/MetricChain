"""Upper bounds for the game function of the binary symmetric chain from the tilt-state recursion in its CONSERVATIVE
discretisation (ydp3.DP3, mode +1): for every t and every symmetric Markov reference Q_qt,
    F_inf(t) <= safe rate(t, qt)        (relaxation proved in the report; grid value on the safe side by construction),
    E_inf    <= safe growth of max KL(pi || pi_phi)      (to be compared with the closed form E_F),
    a_inf    <= safe growth of max KL(pi_phi || Q_qt).
h = max_t F_inf(t) is bounded on every grid interval [t1,t2] by min( B(t1) t2/t1, B(t2) (1-t1)/(1-t2) ) (F/t nonincreasing, F/(1-t) nondecreasing).
usage: python3 y13_certified_upper.py p [Gfine]"""
import sys, time, math
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import cube_numbers
from ylyap import E_F
from ydp3 import DP3

t0 = time.time(); u = 1.0
p = float(sys.argv[1]); Gf = int(sys.argv[2]) if len(sys.argv) > 2 else 801
hc, ac, Ec = cube_numbers(u)
print("p = %.2f, u = 1; cube h = %.6f, a = %.6f, E = %.6f;  E_F = %.7f" % (p, hc, ac, Ec, E_F(p, u)), flush=True)
# ---- E
for G in (801, 1601, 3201):
    s = DP3(p, u, G, +1).kl_rate(); uns = DP3(p, u, min(G, 801), -1).kl_rate()
    print("  E: G=%4d: safe growth of the relaxed max KL(pi||pi_phi): %.7f (bracket %.1e);  grid-restricted (unsafe) value: %.7f;  safe - E_F = %.2e   [%.0f s]" % (
        G, s[1], s[1] - s[0], uns[1], s[1] - E_F(p, u), time.time() - t0), flush=True)
# ---- F(t), h
dc = DP3(p, u, 401, +1); cache = {}
def safe(d, t, q):
    k = (d.G, round(t, 6), round(q, 6))
    if k not in cache: cache[k] = d.renyi_rate(t, q, iters=2500, tol=1e-8)[1]
    return cache[k]
qc = np.linspace(0.55 * p, min(1.15 * p, 0.5), 13)
B = {}
for t in (0.1, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9):
    v = [safe(dc, t, q) for q in qc]; i = int(np.argmin(v)); B[t] = (v[i], qc[i])
print("  coarse (G=401): " + "  ".join("B(%.2f)=%.5f@qt=%.3f" % (t, B[t][0], B[t][1]) for t in sorted(B)) + "   [%.0f s]" % (time.time() - t0), flush=True)
# all coarse points on the fine grid G, then adaptive bisection of the interval with the largest bound
df = DP3(p, u, Gf, +1); dq = qc[1] - qc[0]
allB = {}
for t in sorted(B):
    v = [(safe(df, t, q), q) for q in (B[t][1] - dq / 2, B[t][1], B[t][1] + dq / 2)]; allB[t] = min(v)
def interval_bounds():
    tt = sorted(allB); out = [(allB[tt[0]][0] / (1 - tt[0]), 0.0, tt[0]), (allB[tt[-1]][0] / tt[-1], tt[-1], 1.0)]
    for t1, t2 in zip(tt[:-1], tt[1:]):
        out.append((min(allB[t1][0] * t2 / t1, allB[t2][0] * (1 - t1) / (1 - t2)), t1, t2))
    return sorted(out, reverse=True)
NREF = int(sys.argv[3]) if len(sys.argv) > 3 else 70
for it in range(NREF):
    ib = interval_bounds(); top = max(v[0] for v in allB.values())
    if ib[0][0] <= top * 1.004: break
    b, t1, t2 = ib[0]
    if t1 == 0.0: tn = t2 / 2
    elif t2 == 1.0: tn = (1 + t1) / 2
    else: tn = round(0.5 * (t1 + t2), 5)
    near = min(allB, key=lambda s_: abs(s_ - tn)); q0 = allB[near][1]
    allB[tn] = min((safe(df, tn, q), q) for q in (q0 - dq / 3, q0, q0 + dq / 3))
ib = interval_bounds(); tbest = max(allB, key=lambda t: allB[t][0])
print("  G=%d, %d values of t: largest grid value B(t) = %.6f at t = %.4f (qt = %.4f)   [%.0f s]" % (Gf, len(allB), allB[tbest][0], tbest, allB[tbest][1], time.time() - t0), flush=True)
cert = ib[0][0]
print("  h <= %.6f  (bound over ALL t in (0,1) by the interval rule, worst interval [%.4f, %.4f]; ratio to the cube %.3f)" % (cert, ib[0][1], ib[0][2], cert / hc), flush=True)
# ---- a
va = [(df.shannon_rate(q, iters=4000, tol=1e-8)[1], q) for q in np.linspace(0.7 * p, min(1.1 * p, 0.5), 9)]
a_up = min(va)
print("  a <= %.6f at qt = %.4f (safe, G=%d; ratio to the cube %.3f);  scan: %s   [%.0f s]" % (
    a_up[0], a_up[1], Gf, a_up[0] / ac, " ".join("%.5f" % x[0] for x in va), time.time() - t0), flush=True)
print("%.1f s" % (time.time() - t0))
