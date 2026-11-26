"""r10_07d: the upper ends of the brackets of Y_REPORT section 0.2 from the tilt-state recursion,
with my own cell-based safe discretisation (r10_tilt.py), G = 801 by default.

  h_inf <= sup_t F_inf(t),  F_inf(t) <= B(t) := safe Renyi rate with a symmetric Markov reference
  q~(t);  between grid points  F_inf(t) <= min( B(t1) t/t1, B(t2) (1-t)/(1-t2) )  because
  F_inf(t)/t is nonincreasing and F_inf(t)/(1-t) nondecreasing;  below the first grid point
  F_inf(t) <= t E_up, above the last one F_inf(t) <= (1-t) a_up.
usage: python3 r10_07d_upper_ends.py p [G]
"""
import sys
import time
import numpy as np
from r10lib import cube_exponents, E_F, golden_max
from r10_tilt import Tilt

p = float(sys.argv[1])
G = int(sys.argv[2]) if len(sys.argv) > 2 else 801
u = 1.0
t0 = time.time()
T = Tilt(p, u, G, "safe")
print("p=%g u=%g G=%d u*=%.4f  (build %.0fs)" % (p, u, G, T.us, time.time() - t0), flush=True)


def rate(t, qt, w=None):
    a, b, w = T.renyi_rate(t, qt, sweeps=1500, tol=1e-8, w=w)
    return a


def best_q(t, lo, hi):
    """golden section on q~ (minimise the safe rate)."""
    g = (np.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = rate(t, c), rate(t, d)
    while b - a > 0.004 * p:
        if fc > fd:
            a, c, fc = c, d, fd
            d = a + g * (b - a); fd = rate(t, d)
        else:
            b, d, fd = d, c, fc
            c = b - g * (b - a); fc = rate(t, c)
    return (c, fc) if fc < fd else (d, fd)


# --- E and a
eS, eR, _ = T.thr_rate(sweeps=4000, tol=1e-10)
print("E <= %.6f  (safe, reference Q = pi)   E_F = %.6f   excess %.2e   (%.0fs)" % (eS, E_F(p, u), eS - E_F(p, u), time.time() - t0), flush=True)
best_e = (eS, p)
for qt in (0.9 * p, 0.8 * p, 0.7 * p, 1.1 * p):
    e2 = T.thr_rate(qt, sweeps=4000, tol=1e-10)[0]
    if e2 < best_e[0]:
        best_e = (e2, qt)
print("E <= %.6f with reference Markov(q~=%.4f)   (%.0fs)" % (best_e[0], best_e[1], time.time() - t0), flush=True)
E_up = best_e[0]
best_a = (9.0, None)
for qt in np.linspace(0.6 * p, 1.0 * p, 9):
    a2 = T.cap_rate(qt, sweeps=4000, tol=1e-9)[0]
    if a2 < best_a[0]:
        best_a = (a2, qt)
print("a <= %.6f  (safe, q~=%.4f)   cube a = %.6f   (%.0fs)" % (best_a[0], best_a[1], cube_exponents(u)[2], time.time() - t0), flush=True)
a_up = best_a[0]

# --- h
anchors = [0.2, 0.32, 0.44, 0.56, 0.7]
qa = []
for t in anchors:
    q, v = best_q(t, 0.55 * p, 1.02 * p)
    qa.append(q)
    print("   anchor t=%.2f: best q~=%.4f (%.3f p)  B=%.6f   (%.0fs)" % (t, q, q / p, v, time.time() - t0), flush=True)
qfun = lambda t: float(np.interp(t, anchors, qa))
B = {}
for t in np.round(np.arange(0.14, 0.761, 0.02), 4):
    B[float(t)] = rate(float(t), qfun(float(t)))


def interval_bounds(B):
    ts = sorted(B)
    out = []
    for t1, t2 in zip(ts[:-1], ts[1:]):
        out.append((min(B[t1] * t2 / t1, B[t2] * (1 - t1) / (1 - t2)), t1, t2))
    return out


for rnd in range(6):
    ib = sorted(interval_bounds(B), reverse=True)
    top = ib[0][0]
    gridmax = max(B.values())
    print("   round %d: %d grid points, largest grid value %.6f, largest interval bound %.6f on [%.4f, %.4f]   (%.0fs)"
          % (rnd, len(B), gridmax, top, ib[0][1], ib[0][2], time.time() - t0), flush=True)
    if top < gridmax * 1.003:
        break
    for v, t1, t2 in ib[:6]:
        if v > gridmax * 1.003:
            tm = round(0.5 * (t1 + t2), 6)
            B[tm] = rate(tm, qfun(tm))
ts = sorted(B)
ib = interval_bounds(B)
h_up = max([v for v, _, _ in ib] + [ts[0] * E_up, (1 - ts[-1]) * a_up])
print("tails: t<%.2f: t*E_up <= %.6f ;  t>%.2f: (1-t)*a_up <= %.6f" % (ts[0], ts[0] * E_up, ts[-1], (1 - ts[-1]) * a_up))
tb = max(B, key=B.get)
print("RESULT p=%g G=%d:  h <= %.6f  (largest grid value %.6f at t=%.3f, q~=%.4f);  a <= %.6f;  E <= %.6f;   cube: h %.6f a %.6f E %.6f   (%.0fs)"
      % (p, G, h_up, B[tb], tb, qfun(tb), a_up, E_up, *[cube_exponents(u)[i] for i in (0, 2, 3)], time.time() - t0))
