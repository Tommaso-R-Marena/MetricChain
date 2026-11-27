#!/usr/bin/env python3
"""a6_04_numbers.py  --  the numbers of A6a, recomputed with the referee's own code.  FLOATING POINT (not certified).

 (1) tau_2 and b_2 at u = 1 and u = 2 (and u = 1/2): the formula of A12(a), the closed form a^2/(a + x*), the envelope
     top b_2 by two floating-point sequences that err in opposite directions, the certified tops (coordinator's and
     referee's) for comparison.
 (2) A12(b) on the computed curves: tau(M_{W_j, b_j}) = inf_x a (x + M_j(x))/(a + x) against the next top b_{j+1},
     j = 1..12; in particular tau(M_{W_2, b_2}) against b_3 (the addendum's table has 0.363303 a against 0.363301 a).
 (3) the second level on the operator R itself: T_2 = min(theta, R[theta]) at the rates of the coordinator's table
     (out_z7_exactness_u1.txt), then tau_3 = tau(T_2) by a third independent computation (the coordinator has
     0.361189 a, the earlier referee 0.361184 a), and b_3 - tau_3.
"""
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a6lib as L                                               # noqa: E402

t00 = time.time()
FAIL = []


def check(name, ok, info=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", name, info))
    if not ok:
        FAIL.append(name)


def tau2_formula(P):
    t = np.linspace(0.0, 1.0, 4000001)
    e, th = P.e_of_t(t), P.th_of_t(t)
    val = P.a * np.maximum(P.a, e + th) / (P.a + e)
    i = int(np.argmin(val))
    tt = np.linspace(t[max(i - 2, 0)], t[min(i + 2, len(t) - 1)], 400001)
    e2, th2 = P.e_of_t(tt), P.th_of_t(tt)
    return float(np.min(P.a * np.maximum(P.a, e2 + th2) / (P.a + e2)))


def xstar(P):
    f = lambda t: float(2 * P.J(t) + (1 - 2 * t) * P.J1(t)) - P.a   # noqa: E731
    lo, hi = 0.0, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return float(P.e_of_t(0.5 * (lo + hi)))


def tau_of_curve_lines(P, V):
    """inf_x a (x + M(x))/(a + x) for M = M_{V, c} (ternary search: the ratio of a convex function and a positive
    linear one is quasi-convex), M evaluated exactly at the vertices"""
    a = P.a
    f = lambda x: a * (x + float(V.M(np.array([x]))[0])) / (a + x)   # noqa: E731
    lo, hi = 1e-9, 50.0
    for _ in range(300):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(m1) <= f(m2):
            hi = m2
        else:
            lo = m1
    return f(0.5 * (lo + hi))


def tau_of_curve_grid(P, x, w):
    a = P.a
    f = lambda z: a * (z + float(L.grid_M(x, w, np.array([z]))[0])) / (a + z)   # noqa: E731
    lo, hi = 1e-9, 50.0
    for _ in range(300):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(m1) <= f(m2):
            hi = m2
        else:
            lo = m1
    return f(0.5 * (lo + hi))


print("(1) tau_2 and b_2")
cert = {1.0: ("0.055517525617 (coordinator, K = 3000)", "0.055517524916064 (referee, a6_03)"),
        2.0: ("0.165747480 = 0.505615446 a (coordinator)", "0.165747479467515 (referee, a6_03)"),
        0.5: ("0.500026741 a (coordinator)", "-")}
seqs = {}
for u in (1.0, 2.0, 0.5):
    P = L.Cube(u)
    t2 = tau2_formula(P)
    xs = xstar(P)
    closed = P.a ** 2 / (P.a + xs)
    lt, lc = L.lines_sequence(P, 13, 20000, keep=set(range(14)), refine=500)
    gt, gc = L.grid_sequence(P, 13, 20000, keep=set(range(14)), refine=500)
    seqs[u] = (P, lt, lc, gt, gc)
    print("  u = %g:  a = %.12f" % (u, P.a))
    print("     tau_2 = inf_x a max(a, x + theta(x))/(a + x)   = %.12f = %.10f a" % (t2, t2 / P.a))
    print("     closed form a^2/(a + x*), x* = %.10f      = %.12f = %.10f a" % (xs, closed, closed / P.a))
    print("     b_2, floating point: grid (errs down) %.12f, lines (errs up) %.12f  = [%.10f, %.10f] a" % (gt[2], lt[2], gt[2] / P.a, lt[2] / P.a))
    print("     certified upper bounds: %s; %s" % cert[u])
    check("u = %g: tau_2 (formula) = closed form = b_2 to 2e-10 a" % u, abs(t2 - closed) < 2e-10 * P.a and abs(gt[2] - closed) < 2e-10 * P.a and abs(lt[2] - closed) < 2e-10 * P.a,
          "| (b_2 - tau_2)/a: grid %.1e, lines %.1e" % ((gt[2] - closed) / P.a, (lt[2] - closed) / P.a))
P1 = seqs[1.0][0]
check("u = 1: the addendum's numbers  tau_2 = 0.055517524915 = 0.500410018 a", abs(tau2_formula(P1) - 0.055517524915) < 2e-12)
check("u = 1: the addendum's grid value b_2 = 0.055517524693 is BELOW tau_2 = b_2 (by 2e-9 a: the grid errs downwards); its certified 0.055517525617 is above",
      0.055517524693 < 0.055517524915 < 0.055517525617)

print("(2) Proposition A12(b) on the computed curves:  tau(M_{W_j, b_j}) = b_{j+1}")
for u in (1.0, 2.0):
    P, lt, lc, gt, gc = seqs[u]
    worst = 0.0
    for j in range(1, 13):
        tl = tau_of_curve_lines(P, lc[j])
        tg = tau_of_curve_grid(P, *gc[j])
        worst = max(worst, abs(tl - lt[j + 1]) / P.a, abs(tg - gt[j + 1]) / P.a)
        if j in (1, 2, 3, 6, 12):
            print("     u = %g, j = %2d: tau(M_j)/a = %.12f (lines), %.12f (grid);   b_{j+1}/a = %.12f (lines), %.12f (grid)" % (
                u, j, tl / P.a, tg / P.a, lt[j + 1] / P.a, gt[j + 1] / P.a))
    check("u = %g: inf_x a (x + M_j(x))/(a + x) = next top, j = 1..12, both sequences" % u, worst < 1e-11, "| largest difference %.1e a" % worst)
P, lt, lc, gt, gc = seqs[1.0]
print("     u = 1: tau(M_{W_2, b_2}) = b_3 = %.10f a  (addendum's table: 0.363303 a and 0.363301 a -- the first is a grid value in phi)" % (lt[3] / P.a))
check("u = 1: b_3 = 0.3633006502 a (both floating-point sequences agree to 1e-12 a)", abs(lt[3] - gt[3]) < 1e-12 * P.a and abs(lt[3] / P.a - 0.3633006502) < 1e-9)

print("(3) the second and third level on the operator R itself (u = 1)")
P = P1
a = P.a
# a fast theta: table in q = sqrt(e) (theta is smooth in q at zero), linear interpolation, 2e6 points
NQ = 2000001
qtab = np.linspace(0.0, math.sqrt(P.eps), NQ)
ttab = P.theta(qtab ** 2)
ttab[0] = a
ttab[-1] = 0.0
chk = np.sort(np.random.default_rng(3).uniform(0, P.eps, 20000))
terr = float(np.max(np.abs(np.interp(np.sqrt(chk), qtab, ttab) - P.theta(chk))))
print("     table of theta_na (2e6 points in sqrt(e)): largest interpolation error on 20000 random rates: %.1e a" % (terr / a))


def th(e):
    e = np.asarray(e, dtype=float)
    return np.where(e >= P.eps, 0.0, np.interp(np.sqrt(np.clip(e, 0.0, P.eps)), qtab, ttab))


def R_theta(g, n1=1200, zooms=9):
    """R[theta](g) by minimisation over (phi, beta/g): first a mesh that is fine at both ends of both variables,
    then zooms; every mesh point is an upper bound.  Returns (value, phi, beta/g)."""
    def val(phi, bg):
        beta = bg * g
        mu = phi * th((g - beta) / phi)
        x = mu / (1 - phi)
        y0 = beta / (1 - phi)
        k1 = x + th(y0)
        k2 = np.maximum(y0 + th(y0), x + th(x))
        return (1 - phi) * np.where(y0 >= x, k1, k2)
    ph = np.unique(np.concatenate([np.linspace(1e-4, 1 - 1e-4, n1), np.geomspace(1e-7, 0.05, 150), 1 - np.geomspace(1e-7, 0.05, 150)]))
    bg = np.unique(np.concatenate([np.linspace(1e-4, 1 - 1e-4, 500), np.geomspace(1e-9, 0.05, 200), 1 - np.geomspace(1e-9, 0.05, 200)]))
    PH, BG = np.meshgrid(ph, bg, indexing="ij")
    Vv = val(PH, BG)
    # several starting cells: the best few local minima of the coarse mesh
    flat = np.argsort(Vv, axis=None)[:4000]
    starts = []
    for idx in flat:
        i, j = np.unravel_index(int(idx), Vv.shape)
        if all(abs(ph[i] - p0) > 0.02 or abs(bg[j] - b0) > 0.02 for p0, b0, _ in starts):
            starts.append((ph[i], bg[j], float(Vv[i, j])))
        if len(starts) >= 4:
            break
    best = (math.inf, 0.0, 0.0)
    for p0, b0, v0 in starts:
        dp, db = 0.01, 0.01
        cur = (v0, p0, b0)
        for z in range(zooms):
            p = np.linspace(max(1e-9, cur[1] - dp), min(1 - 1e-9, cur[1] + dp), 81)
            b = np.linspace(max(1e-12, cur[2] - db), min(1 - 1e-12, cur[2] + db), 81)
            PP, BB = np.meshgrid(p, b, indexing="ij")
            W = val(PP, BB)
            i, j = np.unravel_index(int(np.argmin(W)), W.shape)
            if W[i, j] < cur[0]:
                cur = (float(W[i, j]), float(p[i]), float(b[j]))
            dp, db = dp / 3, db / 3
        if cur[0] < best[0]:
            best = cur
    return best


def T2(g):
    return min(R_theta(g)[0], float(th(g)))


# (3a) against the coordinator's table of out_z7_exactness_u1.txt
coord = {0.001: 0.0522553962, 0.01: 0.0458555137, 0.1: 0.0295522827, 0.2: 0.0212155198, 0.4: 0.0109243554, 0.6: 0.0046821020, 0.9: 0.0002886242}
worst = 0.0
above = 0.0
for r, v in coord.items():
    mine, ph_, bg_ = R_theta(r * P.eps)
    worst = max(worst, abs(mine - v) / a)
    above = max(above, (mine - v) / a)
    print("     g = %.3f eps*:  R[theta](g) = %.10f  (phi = %.4f, beta/g = %.4f);  coordinator's table: %.10f;  difference %+.1e a" % (r, mine, ph_, bg_, v, (mine - v) / a))
check("the coordinator's values of R[theta] at seven rates are reproduced to 5e-7 a, and the referee's minima are never above them (any mesh point is an upper bound)",
      worst < 5e-7 and above < 1e-9, "| largest difference %.1e a" % worst)

# (3b) tau_3 = inf_x a (x + T_2#(x))/(a + x),  x + T_2#(x) = sup_{y <= x} (y + T_2(y)) = max(tau_2, sup ...)
tau2 = tau2_formula(P)
gridx = np.concatenate([np.geomspace(1e-5 * P.h, 0.5 * P.h, 14), np.linspace(0.6 * P.h, 4.2 * P.h, 37)])
vals = np.array([T2(float(x)) for x in gridx])
S = np.maximum.accumulate(np.maximum(gridx + vals, tau2))
print("     y + T_2(y) - tau_2 at y/h = %s:" % ", ".join("%.3g" % (x / P.h) for x in gridx[::6]))
print("        " + ", ".join("%+.2e" % ((x + v - tau2)) for x, v in zip(gridx[::6], vals[::6])))
# the first root of x + T_2(x) = tau_2
k = int(np.argmax(gridx + vals > tau2))
lo, hi = float(gridx[k - 1]), float(gridx[k])
for _ in range(40):
    mid = 0.5 * (lo + hi)
    if mid + T2(mid) > tau2:
        hi = mid
    else:
        lo = mid
x2 = 0.5 * (lo + hi)
tau3_kink = a * tau2 / (a + x2)
# is the kink the minimiser?  the function beyond it, a (x + T_2(x))/(a + x), on the coarse grid and close to x2
beyond = [a * (x + T2(x)) / (a + x) for x in (x2 * 1.0005, x2 * 1.002, x2 * 1.01, x2 * 1.05)]
coarse = float(np.min(a * S / (a + gridx)))
tau3 = min(tau3_kink, coarse, min(beyond))
print("     first root of x + T_2(x) = tau_2:  x* = %.6f h = %.6f eps*;   a tau_2/(a + x*) = %.6f a" % (x2 / P.h, x2 / P.eps, tau3_kink / a))
print("     a (x + T_2(x))/(a + x) at x = x*(1 + 5e-4, 2e-3, 1e-2, 5e-2): %s a;  coarse-grid minimum of a S(x)/(a + x): %.6f a" % (
    ", ".join("%.6f" % (b / a) for b in beyond), coarse / a))
check("the kink is the minimiser: the function increases beyond x* (so tau_3 = a tau_2/(a + x*))", all(b > tau3_kink for b in beyond) and coarse >= tau3_kink - 1e-12)
b3 = seqs[1.0][1][3]
print("     tau_3 = %.6f a   (coordinator: 0.361189 a; earlier referee: 0.361184 a; theory report: 0.361 a);   b_3 = %.6f a;   (b_3 - tau_3)/a = %.3e" % (tau3 / a, b3 / a, (b3 - tau3) / a))
check("tau_3 = 0.36118(4) a: agrees with the earlier referee's 0.361184 a to 2e-6 a; the coordinator's 0.361189 a is 5e-6 a above", abs(tau3 / a - 0.361184) < 2e-6)
check("tau_3 < b_3, by 2.1e-3 a (0.6 per cent)", 2.0e-3 < (b3 - tau3) / a < 2.2e-3)
print()
print("time %.0f s" % (time.time() - t00))
print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
