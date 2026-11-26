#!/usr/bin/env python3
"""z8_defect_profile.py [u]  --  Is the defect of the envelope majorant largest at accuracy zero?  (floating point [N])

For the envelope sequence (W_k, b_k) of docs/workstreams/Z_ADDENDUM.md and M_k(g) = max_B (B - W_k(B) g):

    Claim U:   sup_{g >= 0} [ M_k(g) - theta_hint(g) ]  =  b_k - h      (attained at g = 0).

By convex duality (theta_hint(g) = sup_t [J(t) - t g], J concave increasing on [0, L]) Claim U is equivalent to

    W_k(B)  >=  t_1(B - (b_k - h))   on [0, b_k],      t_1 = the inverse of J on [0, h]  (t_1 = 0 below 0, t_1(h) = L):

the envelope curve lies above the fixed-point curve of the slope map shifted to the right by b_k - h.  If it holds,
the bound of Theorem 11.58e(e) holds at every accuracy relative to n theta_hint(xhat/n).  NOT PROVED: the obvious
induction (the image of the shifted curve under the slope map dominates the next shifted curve) needs
(b_k - h)^2/(theta_hint''(0) h^2) >= b_k - b_{k+1} near the top, which fails from about ten levels on.
This script checks both forms numerically; the second column is the least value of W_k(B) - t_1(B - delta_k) over
the part of [0, b_k] where the shifted curve is positive (B >= delta_k + 0.002 b_k).
"""
import sys, math, numpy as np
sys.path.insert(0, '.')
import zetalib
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
E = zetalib.EnvZ(u, 60, NG=8000)
h, L, a = E.h, E.L, E.a
J = lambda t: E._J(t)
def t1(Bp):
    Bp = np.asarray(Bp, dtype=float)
    lo = np.zeros(Bp.shape); hi = np.full(Bp.shape, L)
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        ok = J(mid) < Bp
        lo = np.where(ok, mid, lo); hi = np.where(ok, hi, mid)
    return np.where(Bp <= 0, 0.0, np.where(Bp >= h, L, 0.5 * (lo + hi)))
# theta_hint(g) = max_t (J(t) - t g)
ts = np.linspace(0, L, 200001); Jt = J(ts)
def th_hint(g): return float(np.max(Jt - ts * g))
print("# cube u = %g: Claim U  <=>  W_k(B) >= t1(B - (b_k - h)) on [0, b_k];  and directly  sup_g [M_k(g) - theta_hint(g)] <= b_k - h" % u)
print("#  k   (b_k-h)/h    min [W_k(B) - t1(B - delta_k)] over B >= delta_k + 0.002 b_k   at B/b_k     sup_g [M_k(g) - theta_hint(g)]/(b_k - h)   at g/h")
gs = np.concatenate([[0.0], np.geomspace(1e-5, 6.0, 240) * h])
ok = True
for k in list(range(1, 13)) + [16, 20, 30, 40, 60]:
    x, W = E.curves[k]; bk = E.b[k]; dk = bk - h
    d = W - t1(x - dk)
    d = np.where(x >= dk + 0.002 * bk, d, np.inf)
    i = int(np.argmin(d))
    Dg = [float(np.max(x - W * g)) - th_hint(g) for g in gs]
    j = int(np.argmax(Dg))
    print("%4d   %9.6f    %+.3e                                             %.4f        %.6f                              %.4f" % (k, dk / h, d[i], x[i] / bk, Dg[j] / dk, gs[j] / h))
    ok = ok and d[i] >= -1e-9 and Dg[j] <= dk * (1 + 1e-6)
print("ALL CHECKS PASS (Claim U holds at every level computed)" if ok else "CLAIM U FAILS AT SOME LEVEL")
