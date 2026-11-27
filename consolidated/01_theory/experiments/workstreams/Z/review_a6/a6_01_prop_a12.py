#!/usr/bin/env python3
"""a6_01_prop_a12.py -- Proposition A12 of Z_ADDENDUM.md (A6a), attacked numerically.  FLOATING POINT; own code.

Parts
 A  (a): tau(T) = inf_x a (x + T#(x))/(a + x) on random nonincreasing T (steps with jumps: suprema not attained),
         by a brute force on the definition  inf_phi sup_gamma [min(gamma, phi a) + (1 - phi) T(gamma/(1 - phi))].
 B  (b): M_{env f, b} = M_{f, b} for random f : [0, b] -> [0, 1];  tau(M_{W,b}) = max_B min(B, (1 - W(B)) a) for
         random convex W, by the same brute force.
 C  (c): theta# = max(theta, a - .) = M_{W_1, a}  and  tau_2 = b_2  for pairs with infinite, finite (> 1) and
         finite (<= 1) slope at zero; W_1 = lower convex envelope of min(1, Sigma(B, 0)) computed from the definition.
 D  the closed form tau_2 = a^2/(a + x*) "for the cube": for which slopes u is it true?
 E  the identity behind (c), (d) that the addendum quotes: sup T_2 = R[theta](0+) = tau(theta), by a brute force
    on the operator R itself at small accuracy rates.
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
rng = np.random.default_rng(20261126)
FAIL = []


def check(name, ok, info=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", name, info))
    if not ok:
        FAIL.append(name)


# ------------------------------------------------------------------------------------------------------------
# A. tau(T) for step functions
# ------------------------------------------------------------------------------------------------------------
print("A. Proposition A12(a): tau(T) = inf_x a (x + T#(x))/(a + x) = tau(T#)")


class Step:
    """nonincreasing right-continuous step function: T = v[i] on [y[i], y[i+1]), y[0] = 0, last piece to infinity"""

    def __init__(self, y, v):
        self.y, self.v = np.asarray(y, float), np.asarray(v, float)

    def __call__(self, x):
        i = np.searchsorted(self.y, np.asarray(x, float), side="right") - 1
        return self.v[np.maximum(i, 0)]

    def sharp(self, x):
        """T#(x) = sup_{0 <= y <= x} (y + T(y)) - x, exactly (suprema over half-open pieces)"""
        x = float(x)
        best = -math.inf
        for i in range(len(self.y)):
            if self.y[i] > x:
                break
            right = self.y[i + 1] if i + 1 < len(self.y) else math.inf
            best = max(best, min(right, x) + self.v[i])
        return best - x


def tau_brute(T, a, nphi=2001, ngam=40001, gmax=None):
    """inf over a grid of phi of sup over a grid of gamma (the suprema over open pieces are approached, not attained)"""
    best = math.inf
    phis = np.linspace(0.0005, 0.9995, nphi)
    for phi in phis:
        top = phi * a * 1.2 + (gmax or 1.0) * (1 - phi)
        gam = np.linspace(0.0, top, ngam)
        val = np.minimum(gam, phi * a) + (1 - phi) * T(gam / (1 - phi))
        best = min(best, float(np.max(val)))
    return best


def tau_formula(sharp, a, xs):
    return min(a * (x + sharp(x)) / (a + x) for x in xs)


worst = 0.0
for trial in range(12):
    a = float(rng.uniform(0.05, 1.0))
    n = int(rng.integers(2, 7))
    y = np.concatenate([[0.0], np.sort(rng.uniform(0.0, 1.5 * a, n))])
    v = np.sort(rng.uniform(0.0, 1.2 * a, n + 1))[::-1]
    T = Step(y, v)
    xs = np.concatenate([np.geomspace(1e-6, 60.0, 30001), y[1:], y[1:] * (1 - 1e-12)])
    f = tau_formula(T.sharp, a, xs)
    b = tau_brute(T, a, gmax=float(y[-1]) * 1.05 + 0.01)
    # T# is nonincreasing, nonnegative, and (T#)# = T#
    xx = np.sort(rng.uniform(0, 2 * a, 300))
    sh = np.array([T.sharp(x) for x in xx])
    mono = bool(np.all(np.diff(sh) <= 1e-12)) and bool(np.all(sh >= -1e-15))
    idem = bool(np.all(np.diff(xx + sh) >= -1e-12))            # x + T#(x) nondecreasing  <=>  (T#)# = T#
    worst = max(worst, abs(f - b) / a)
    check("random step function %2d: brute force %.6f, formula %.6f (a = %.4f)" % (trial, b, f, a),
          abs(f - b) < 2e-3 * a and mono and idem, "| T# nonincreasing, >= 0, idempotent: %s" % (mono and idem))
print("  largest |brute - formula|/a: %.2e (grid of the brute force: 1e-3 in phi)" % worst)

# ------------------------------------------------------------------------------------------------------------
# B. the envelope loses nothing; tau of a majorant
# ------------------------------------------------------------------------------------------------------------
print("B. Proposition A12(b)")
worst = 0.0
for trial in range(200):
    n = int(rng.integers(5, 400))
    b = float(rng.uniform(0.05, 1.0))
    x = np.sort(np.concatenate([[0.0, b], rng.uniform(0, b, n)]))
    f = rng.uniform(0, 1, len(x)) ** float(rng.uniform(0.3, 3))
    hull = L.lower_hull_points(x, f)
    env = np.interp(x, x[hull], f[hull])
    gs = np.concatenate([[0.0], np.geomspace(1e-4, 1e3, 60)])
    Mf = np.max(x[None, :] - gs[:, None] * f[None, :], axis=1)
    Me = np.max(x[None, :] - gs[:, None] * env[None, :], axis=1)
    worst = max(worst, float(np.max(np.abs(Mf - Me))))
check("M_{env f, b} = M_{f, b} on 200 random f, rates 0 and 1e-4..1e3", worst < 1e-12, "largest difference %.1e" % worst)

worst = 0.0
for trial in range(10):
    a = float(rng.uniform(0.05, 1.0))
    b = float(rng.uniform(0.2 * a, 1.3 * a))
    n = int(rng.integers(2, 9))
    xk = np.sort(np.concatenate([[0.0, b], rng.uniform(0, b, n)]))
    sl = np.sort(rng.uniform(0, 1, len(xk) - 1))                # increasing slopes: convex
    w = np.concatenate([[0.0], np.cumsum(sl * np.diff(xk))])
    w = w / max(1.0, w[-1] / float(rng.uniform(0.3, 1.0)))       # values in [0, 1]
    Bs = np.linspace(0, b, 200001)
    Wv = np.interp(Bs, xk, w)
    dual = float(np.max(np.minimum(Bs, (1 - Wv) * a)))           # max_B min(B, (1 - W(B)) a)
    reg = Bs < (1 - Wv) * a                                      # regular points, infinite slope at zero
    bplus = float(Bs[reg].max())
    M = lambda xx: np.max(xk[None, :] - np.atleast_1d(xx)[:, None] * w[None, :], axis=1)   # noqa: E731
    Mfun = lambda z: M(np.asarray(z, float).ravel()).reshape(np.shape(z))                   # noqa: E731
    tb = tau_brute(Mfun, a, nphi=1501, ngam=6001, gmax=1.0)
    worst = max(worst, abs(tb - dual) / a, abs(bplus - dual) / a)
    check("random convex W %d: tau(M) brute %.6f, max_B min(B, (1-W)a) %.6f, b+ %.6f" % (trial, tb, dual, bplus),
          abs(tb - dual) < 2e-3 * a and abs(bplus - dual) < 2e-5 * a)
print("  largest relative difference: %.2e" % worst)

# ------------------------------------------------------------------------------------------------------------
# C. theta# = max(theta, a - .) = M_{W_1, a};  tau_2 = b_2;  several pairs
# ------------------------------------------------------------------------------------------------------------
print("C. Proposition A12(c): theta# = max(theta, a - .) = M_{W_1, a};  tau_2 = tau(theta) = b_2 = b+(W_1, a)")


def generic_pair(name, theta, a, emax, slope0):
    """theta: vectorised callable on e > 0 (convex, nonincreasing), a = theta(0+), slope0 = |theta'(0+)| (inf allowed)"""
    e = np.concatenate([np.geomspace(1e-13, emax, 40001), np.geomspace(emax, 1e4 * emax, 400)[1:]])
    th = theta(e)
    NB = 3001
    Bs = np.linspace(0.0, a, NB)
    p1 = np.empty(NB)
    for k in range(0, NB, 200):                                 # Sigma(B, 0) = sup_e (B - theta(e))/e, in blocks
        p1[k:k + 200] = np.max((Bs[k:k + 200, None] - th[None, :]) / e[None, :], axis=1)
    p1 = np.maximum(p1, 0.0)
    p1[-1] = slope0                                             # the value at B = a is |theta'(0+)|
    f = np.minimum(1.0, p1)
    hull = L.lower_hull_points(Bs, f)
    xk, wk = Bs[hull], f[hull]
    # end value of the envelope step: the left limit of env f at a (A2); env f(a) may be larger -- same M
    xs = np.concatenate([[0.0], np.geomspace(1e-5 * a, 30 * max(a, emax), 4000)])
    Mw = np.max(xk[None, :] - xs[:, None] * wk[None, :], axis=1)
    thx = np.where(xs > 0, theta(np.maximum(xs, 1e-300)), a)
    sharp = np.maximum(thx, a - xs)
    d1 = float(np.max(np.abs(Mw - sharp))) / a
    # theta# from its definition
    ys = np.geomspace(1e-9, xs[-1], 200001)
    run = np.maximum.accumulate(ys + theta(ys))
    sh_def = np.maximum(a, np.interp(xs[1:], ys, run)) - xs[1:]
    d0 = float(np.max(np.abs(sh_def - sharp[1:]))) / a
    # tau_2 from (a) and b_2 from the envelope curve
    xf = np.geomspace(1e-7 * a, 1e3 * max(a, emax), 400001)
    val = a * np.maximum(a, xf + theta(xf)) / (a + xf)
    tau2 = float(val.min())
    Bf = np.linspace(0, a, 400001)
    Wf = np.interp(Bf, xk, wk)
    b2 = float(np.max(np.minimum(Bf, (1 - Wf) * a)))
    print("    %-34s a = %.6f  |theta'(0+)| = %-6s  max|theta# - max(theta, a-.)|/a = %.1e   max|M_{W1,a} - theta#|/a = %.1e"
          "   tau_2/a = %.6f  b_2/a = %.6f" % (name, a, ("inf" if math.isinf(slope0) else "%.2f" % slope0), d0, d1, tau2 / a, b2 / a))
    check("pair %s" % name, d0 < 2e-5 and d1 < 3e-4 and abs(tau2 - b2) < 3e-4 * a)
    return tau2, b2


for u in (0.5, 1.0, 2.0, 6.0, 8.0):
    P = L.Cube(u)
    generic_pair("cube u = %g" % u, lambda e, P=P: P.theta(e), P.a, P.eps, math.inf)
generic_pair("Gaussian (1 - sqrt e)_+^2", lambda e: np.maximum(1 - np.sqrt(e), 0.0) ** 2, 1.0, 1.0, math.inf)
generic_pair("(1 - 0.8 e)_+  (slope 0.8)", lambda e: np.maximum(1 - 0.8 * e, 0.0), 1.0, 1.25, 0.8)
generic_pair("(1 - 3 e)_+    (slope 3)", lambda e: np.maximum(1 - 3 * e, 0.0), 1.0, 1 / 3, 3.0)
generic_pair("exp(-3 e)      (slope 3)", lambda e: np.exp(-3 * e), 1.0, 12.0, 3.0)
generic_pair("0.3 exp(-e)    (slope 0.3)", lambda e: 0.3 * np.exp(-e), 0.3, 40.0, 0.3)
generic_pair("(1 - e)_+^2    (slope 2)", lambda e: np.maximum(1 - e, 0.0) ** 2, 1.0, 1.0, 2.0)
generic_pair("(1 - sqrt e)_+^3", lambda e: np.maximum(1 - np.sqrt(e), 0.0) ** 3, 1.0, 1.0, math.inf)

# ------------------------------------------------------------------------------------------------------------
# D. the closed form a^2/(a + x*) for the cube
# ------------------------------------------------------------------------------------------------------------
print("D. 'For the cube ... tau_2 = b_2 = a^2/(a + x*)':  true iff |theta'(x*)| <= x*/(a + x*)")


def cube_tau2(u):
    P = L.Cube(u)
    a = P.a
    # x + theta(x) in the parameter t: e(t) + theta(t) = 2 J + (1 - 2 t) J'; its minimum is at t = 1/2 (theta' = -1)
    f = lambda t: float(2 * P.J(t) + (1 - 2 * t) * P.J1(t)) - a      # noqa: E731
    if f(0.0) < 0:                                                   # x + theta(x) < a up to eps*: x* = a, theta = 0
        xs, lam = a, 0.0
    else:
        lo, hi = 0.0, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        ts = 0.5 * (lo + hi)
        xs, lam = float(P.e_of_t(ts)), ts / (1 - ts)
    closed = a * a / (a + xs)
    # tau_2 by minimising a max(a, x + theta(x))/(a + x) over x = e(t), t in [0, 1], and x >= eps* (increasing there)
    t = np.linspace(0.0, 1.0, 2000001)
    e, th = P.e_of_t(t), P.th_of_t(t)
    val = a * np.maximum(a, e + th) / (a + e)
    i = int(np.argmin(val))
    lo, hi = t[max(i - 1, 0)], t[min(i + 1, len(t) - 1)]
    tt = np.linspace(lo, hi, 200001)
    e2, th2 = P.e_of_t(tt), P.th_of_t(tt)
    tau2 = float(np.min(a * np.maximum(a, e2 + th2) / (a + e2)))
    # b_2 from the envelope curve W_1: either on the cap line (then a^2/(a + x*)) or on the curve: B = (1 - Sigma(B, 0)) a
    # tangency point of the cap line from (a, 1): the line of slope 1/x* through (a, 1); B_t = a - (1 - lam) x*
    Bt = a - (1 - lam) * xs
    # root of B = (1 - p_1(B)) a on the un-capped curve (p_1 = Sigma(., 0))
    lo, hi = 0.0, a
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid < (1 - float(P.sigma(mid, 0.0))) * a:
            lo = mid
        else:
            hi = mid
    Bcurve = 0.5 * (lo + hi)
    b2 = closed if closed >= Bt else Bcurve
    return dict(u=u, a=a, xs=xs, lam=lam, crit=xs / (a + xs), closed=closed, tau2=tau2, Bt=Bt, Bcurve=Bcurve, b2=b2)


print("     u        a          x*/a      |theta'(x*)|  x*/(a+x*)   a^2/(a+x*)/a     tau_2/a        b_2/a      B_t/a    closed form")
rows = []
for u in (0.1, 0.25, 0.5, 1.0, 2.0, 3.0, 4.0, 4.5, 5.0, 6.0, 8.0, 12.0):
    r = cube_tau2(u)
    rows.append(r)
    okc = abs(r["closed"] - r["tau2"]) < 1e-9 * r["a"]
    print("  %6.2f  %.8f  %.6f   %.6f     %.6f    %.9f   %.9f   %.9f  %.5f   %s" % (
        u, r["a"], r["xs"] / r["a"], r["lam"], r["crit"], r["closed"] / r["a"], r["tau2"] / r["a"], r["b2"] / r["a"], r["Bt"] / r["a"],
        "holds" if okc else "FAILS by %.2e a" % ((r["closed"] - r["tau2"]) / r["a"])))
    check("u = %g: tau_2 = b_2 (general identity)" % u, abs(r["tau2"] - r["b2"]) < 2e-9 * r["a"])
    check("u = %g: closed form holds iff |theta'(x*)| <= x*/(a + x*)" % u, okc == (r["lam"] <= r["crit"] + 1e-12))
lo, hi = 4.0, 5.0
for _ in range(60):
    mid = 0.5 * (lo + hi)
    r = cube_tau2(mid)
    if r["lam"] <= r["crit"]:
        lo = mid
    else:
        hi = mid
u0 = 0.5 * (lo + hi)
r = cube_tau2(u0)
print("  threshold slope: the closed form is tau_2 exactly for u <= u_0 = %.6f (there tau_2/a = %.6f); above it" % (u0, r["tau2"] / r["a"]))
print("  a^2/(a + x*) is strictly larger than tau_2 = b_2, which is then the root of B = (1 - Sigma(B, 0)) a on the un-capped curve")
check("the closed form holds at the slopes of the addendum (u = 1/2, 1, 2)", all(abs(x["closed"] - x["tau2"]) < 1e-9 * x["a"] for x in rows if x["u"] in (0.5, 1.0, 2.0)))
check("the closed form FAILS at u = 5, 6, 8, 12", all(x["closed"] - x["tau2"] > 1e-4 * x["a"] for x in rows if x["u"] in (5.0, 6.0, 8.0, 12.0)))
P1 = L.Cube(1.0)
r1 = cube_tau2(1.0)
print("  u = 1: tau_2 = %.12f = %.9f a   (addendum: 0.055517524915 = 0.500410018 a);  x* = %.10f" % (r1["tau2"], r1["tau2"] / r1["a"], r1["xs"]))
check("u = 1: the addendum's value of tau_2", abs(r1["tau2"] - 0.055517524915) < 2e-12)

# ------------------------------------------------------------------------------------------------------------
# E. sup T_2 = R[theta](0+) = tau(theta)   (brute force on R at small rates)
# ------------------------------------------------------------------------------------------------------------
print("E. the identity that A12(c), (d) quote: sup T_{k+1} = R[T_k](0+) = tau(T_k)  -- here k = 1, brute force on R")


def R_theta(theta, a, g, n1=700, n2=500, zooms=5):
    """R[theta](g) = inf_{phi, beta} sup_{gamma >= beta} [min(gamma, mu) + (1 - phi) theta(gamma/(1 - phi))],
    mu = phi theta((g - beta)/phi).  For convex theta the supremum is explicit:
       (1 - phi) * ( x + theta(y0)  if y0 >= x  else  max(y0 + theta(y0), x + theta(x)) ),  x = mu/(1-phi), y0 = beta/(1-phi).
    Minimised over a grid of (phi, beta/g) with zooms; any grid point is an upper bound of R."""
    def val(phi, bg):
        beta = bg * g
        mu = phi * theta((g - beta) / phi)
        x = mu / (1 - phi)
        y0 = beta / (1 - phi)
        k1 = x + theta(y0)
        k2 = np.maximum(y0 + theta(y0), x + theta(np.maximum(x, 1e-300)))
        return (1 - phi) * np.where(y0 >= x, k1, k2)
    plo, phi_hi, blo, bhi = 1e-6, 1 - 1e-6, 1e-9, 1 - 1e-9
    best = (math.inf, 0, 0)
    for z in range(zooms):
        ph = np.linspace(plo, phi_hi, n1)
        bg = np.linspace(blo, bhi, n2)
        PH, BG = np.meshgrid(ph, bg, indexing="ij")
        V = val(PH, BG)
        i, j = np.unravel_index(int(np.argmin(V)), V.shape)
        if V[i, j] < best[0]:
            best = (float(V[i, j]), float(ph[i]), float(bg[j]))
        dp, db = (phi_hi - plo) / n1 * 4, (bhi - blo) / n2 * 4
        plo, phi_hi = max(1e-9, ph[i] - dp), min(1 - 1e-9, ph[i] + dp)
        blo, bhi = max(1e-12, bg[j] - db), min(1 - 1e-12, bg[j] + db)
    return best


def tau_of(theta, a, emax):
    xf = np.geomspace(1e-8 * a, 1e3 * max(a, emax), 2000001)
    return float(np.min(a * np.maximum(a, xf + theta(xf)) / (a + xf)))


cases = [("cube u = 1", (lambda e, P=L.Cube(1.0): P.theta(e)), L.Cube(1.0).a, L.Cube(1.0).eps, cube_tau2(1.0)["closed"]),
         ("cube u = 8", (lambda e, P=L.Cube(8.0): P.theta(e)), L.Cube(8.0).a, L.Cube(8.0).eps, cube_tau2(8.0)["closed"]),
         ("(1 - 3 e)_+", (lambda e: np.maximum(1 - 3 * np.asarray(e, float), 0.0)), 1.0, 1 / 3, None),
         ("exp(-3 e)", (lambda e: np.exp(-3 * np.asarray(e, float))), 1.0, 12.0, None)]
for name, theta, a, emax, closed in cases:
    tau = tau_of(theta, a, emax)
    print("    %-12s tau(theta)/a = %.6f%s" % (name, tau / a, "" if closed is None else "   a^2/(a + x*)/a = %.6f" % (closed / a)))
    vals = []
    for g in (1e-2 * a, 1e-3 * a, 1e-4 * a, 1e-5 * a, 1e-6 * a):
        v, ph, bg = R_theta(theta, a, g)
        t2 = min(v, float(theta(g)))
        vals.append(t2)
        print("        g = %.0e a:  T_2(g)/a = min(theta, R[theta])(g)/a <= %.6f   (phi = %.4f, beta/g = %.4f)   tau - T_2 = %.2e a" % (g / a, t2 / a, ph, bg, (tau - t2) / a))
    inc = all(vals[i] <= vals[i + 1] + 1e-9 * a for i in range(len(vals) - 1))
    check("%s: T_2(g) <= tau(theta) at every rate, increasing to it as g -> 0 (gap %.1e a at g = 1e-6 a)" % (name, (tau - vals[-1]) / a),
          all(v <= tau + 1e-7 * a for v in vals) and inc and (tau - vals[-1]) < 6e-3 * a)
    if closed is not None and closed - tau > 1e-3 * a:
        check("%s: sup T_2 is below the closed form a^2/(a + x*) by %.3f a" % (name, (closed - tau) / a), vals[-1] < closed - 1e-3 * a)

print()
print("time %.0f s" % (time.time() - t00))
print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
