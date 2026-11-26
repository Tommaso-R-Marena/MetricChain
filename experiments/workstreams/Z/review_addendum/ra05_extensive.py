#!/usr/bin/env python3
"""RA05 -- section A9 (extensive accuracies): Lemma A9, Lemma A10, Proposition A11 and the table of A9.

 (1) the table  k^2 (M_{W_k, b_k}(g) - theta_hint(g))/c_*^2  with the referee's structural envelope sequence
     (M by bisection on W_k' = 1/g; no grid), against the addendum's table and against the profile of R_REPORT 8a:
     f(zeta)/(2 pi^2), zeta = k g/h, f(zeta) = sup{2z^2 + 2 zeta z cot z, -2y^2 + 2 zeta y coth y} - zeta^2/2, and 2 zeta^2 e^{-zeta}/(2 pi^2).
 (2) Lemma A9:  0 <= t_1(B) - p_i(B) <= t_1(B) lambda_eta^i  for B <= h - eta;  the true multiplier kappa(B) = theta(e_1)/e_1
     against 1 - J'/(B + (1 - t_1) J') and against lambda_eta = hL/(hL + eta).
 (3) Lemma A10: for eta and every k with b_k - h < eta (1 - L)/L: the tangency point B_t(k) is beyond h - eta
     (structural sequence), and, independently of the structural description, on the grid sequence:
     envelope = image on [0, h - eta].  Also W_{k(eta)+i} >= p_{i+1} on [0, h - eta].
 (4) Proposition A11: the recipe of the proof (m, eta, k(eta), k_1) and the inequality
     M_{W_k,b_k}(g) <= theta_hint(g) + g lambda_eta^(k - k_1);  the observed ratio of consecutive defects against the
     multiplier at the line that is tangent to theta_hint at g:  kappa_g = 1 - g/(J(t_g) + (1 - t_g) g),  J'(t_g) = g.
 (5) the number of levels k(n, g) with n (M_k(g) - theta_hint(g)) <= 1, against ln n.
Usage: python3 -B ra05_extensive.py [pair]      pair in {cube1, cube2, gauss}; default cube1
"""
import math
import sys

import numpy as np

import ra_lib as R

which = sys.argv[1] if len(sys.argv) > 1 else "cube1"
P = (R.Gauss() if which == "gauss" else R.Cube(float(which[4:]))).setup()
a, h, L, c2 = P.a, P.h, P.L, P.cstar2
es = P.epsstar
print("# %s: a = %.8f, h = %.8f, L = %.6f, eps* = %.6f, c_*^2 = %.8f" % (P.name, a, h, L, es, c2))
JE = 260
S = R.EnvSeq(P, JE)


def defect(k, g):
    return S.M(k, g)[0] - P.theta_hint(g)


# ---------------------------------------------------------------------------------------------------------------
print("\n== (1) the table of A9:  k^2 (M_{W_k,b_k}(g) - theta_hint(g))/c_*^2 ==")
gs = [0.0, 0.01 * h, 0.1 * h, 0.5 * h, h, 0.25 * es, 0.5 * es, 0.8 * es, 1.0 * es, 1.5 * es]
print("#   k   g = 0        0.01h       0.1h        0.5h        h           0.25eps*    0.5eps*     0.8eps*     eps*        1.5eps*")
neg = 0.0
for k in (1, 2, 3, 5, 10, 20, 40, 80, 160):
    row = []
    for g in gs:
        d = defect(k, g)
        neg = min(neg, d)
        row.append(k * k * d / c2)
    print("  %3d  " % k + "  ".join("%10.3e" % r for r in row))
print("least value of M_k(g) - theta_hint(g) in the table: %.2e  (Proposition A11, left inequality: >= 0 up to rounding)" % neg)
if which == "cube1":
    print("addendum:   k = 2:  1.48  1.47  1.40  1.04  0.55  [0.5eps*: 0.02]")
    print("            k = 5:  1.12  1.07  0.59  0.10  0.017 [1e-4]")
    print("            k = 10: 1.001 0.79  0.30  0.019 4e-4  [< 1e-4]")
    print("            k = 20: 0.996 0.63  0.15  4e-4  < 1e-4")
    print("            k = 40: 0.997 0.50  0.039 < 1e-4")
    print("            k = 80: 0.997 0.35  0.002")


def f_profile(z):
    """f(zeta) = sup{2x^2 + 2 zeta x cot x : 0 < x < pi} or sup{-2y^2 + 2 zeta y coth y : y > 0}, minus zeta^2/2"""
    best = -math.inf
    xs = np.linspace(1e-6, math.pi - 1e-6, 200001)
    best = max(best, float(np.max(2 * xs ** 2 + 2 * z * xs / np.tan(xs))))
    ys = np.linspace(1e-6, max(10.0, 3 * z), 400001)
    best = max(best, float(np.max(-2 * ys ** 2 + 2 * z * ys / np.tanh(ys))))
    return best - z * z / 2


print("\n# against the profile (Proposition S of R_REPORT, a sketch, stated for T_k):  f(zeta)/(2 pi^2),  zeta = k g/h")
print("#  zeta    f/(2pi^2)   2 zeta^2 e^-zeta/(2pi^2)   computed at (k, g = zeta h/k):  k = 10        20          40          80          160         260")
for z in (0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0):
    comp = ["%10.3e" % (k * k * defect(k, z * h / k) / c2) for k in (10, 20, 40, 80, 160, 260)]
    print("  %5.2f   %9.3e     %9.3e                                          %s" % (z, f_profile(z) / (2 * math.pi ** 2), 2 * z * z * math.exp(-z) / (2 * math.pi ** 2), "  ".join(comp)))

# ---------------------------------------------------------------------------------------------------------------
print("\n== (2) Lemma A9 ==")
worst_ratio, worst_low, worst_kappa, worst_form = -math.inf, math.inf, -math.inf, 0.0
for eta_h in (0.5, 0.2, 0.1, 0.03, 0.01, 0.003):
    eta = eta_h * h
    lam = h * L / (h * L + eta)
    wr, wk = -math.inf, -math.inf
    for B in np.linspace(0.0, h - eta, 41)[1:]:
        t1 = P.t1(B)
        orb = P.orbit(B, 400)
        for i, p in enumerate(orb):
            d = t1 - p
            worst_low = min(worst_low, d)
            bound = t1 * lam ** i
            if bound > 1e-13:
                wr = max(wr, d / bound)
        # the multiplier at the fixed point: theta(e1)/e1 with e1 = J + (1 - t1) J', theta(e1) = J - t1 J'
        Jp = P.dJ(t1)
        e1 = B + (1 - t1) * Jp
        th1 = B - t1 * Jp
        kap = th1 / e1
        worst_form = max(worst_form, abs(P.theta(e1) - th1) / h, abs(kap - (1 - Jp / (B + (1 - t1) * Jp))),
                         abs(P.sigma_grad(B, t1)[2] - kap))
        wk = max(wk, kap / lam)
    worst_ratio = max(worst_ratio, wr)
    worst_kappa = max(worst_kappa, wk)
    Bq = h - eta
    t1q = P.t1(Bq)
    Jpq = P.dJ(t1q)
    print("eta = %.3f h: lambda_eta = %.6f;  max over B <= h - eta, i <= 400 of (t_1 - p_i)/(t_1 lambda^i) = %.4f (<= 1);  max kappa(B)/lambda_eta = %.4f (<= 1);  kappa(h - eta) = %.6f, J'(t_1(h-eta)) = %.4e >= eta/L = %.4e"
          % (eta_h, lam, wr, wk, 1 - Jpq / (Bq + (1 - t1q) * Jpq), Jpq, eta / L))
print("least value of t_1 - p_i: %.2e (>= 0 up to rounding);  consistency of theta(e_1) = J - t_1 J', kappa formula, dSigma/ds at the fixed point: %.2e"
      % (worst_low, worst_form))

# ---------------------------------------------------------------------------------------------------------------
print("\n== (3) Lemma A10 ==")
viol, ncase, margin = 0, 0, math.inf
for eta_h in (0.9, 0.5, 0.2, 0.1, 0.03, 0.01, 0.003, 0.001):
    eta = eta_h * h
    ks = [k for k in range(1, JE + 1) if S.b[k] - h < eta * (1 - L) / L]
    if not ks:
        print("eta = %.3f h: no level k <= %d with b_k - h < eta(1-L)/L" % (eta_h, JE))
        continue
    keta = ks[0]
    mn = min(S.Bt[k] - (h - eta) for k in ks)
    ncase += len(ks)
    viol += sum(1 for k in ks if S.Bt[k] <= h - eta)
    margin = min(margin, mn / h)
    # W_{k(eta)+i} >= p_{i+1} on [0, h - eta]
    xs = np.linspace(0.0, h - eta, 60)[1:]
    w2 = -math.inf
    for i in (0, 1, 2, 5, 10, 30):
        if keta + i <= JE:
            Wk = S.Wvec(keta + i, xs)
            pi = np.array([P.orbit(x, i + 1)[-1] for x in xs])
            w2 = max(w2, float(np.max(pi - Wk)))
    print("eta = %.3f h: k(eta) = %3d;  min over k >= k(eta) of (B_t(k) - (h - eta))/h = %.4f (> 0);  min over all k >= 2 of (B_t(k) - h)/h = %.2e;  max of p_{i+1} - W_{k(eta)+i} on [0, h-eta]: %.2e (<= 0)"
          % (eta_h, keta, mn / h, min(S.Bt[k] - h for k in range(2, JE + 1)) / h, w2))
print("levels with the hypothesis of Lemma A10: %d;  violations of B_t(k) > h - eta: %d" % (ncase, viol))
print("B_t(1)/h = %.4f (the first curve is cut below h: Lemma A10 needs its hypothesis);  B_t(k) > h for all 2 <= k <= %d: %s"
      % (S.Bt[1] / h, JE, all(S.Bt[k] > h for k in range(2, JE + 1))))
# independently of the structural description: on the grid sequence, envelope = image on [0, h - eta]
G = R.GridEnv(P, 30, 8000, "quad")
print("grid sequence (definition; quadratic grid 8000): max |envelope - image| on [0, h - eta] at the levels with the hypothesis")
for eta_h in (0.9, 0.5, 0.1):
    eta = eta_h * h
    w = 0.0
    kk = [k for k in range(1, 31) if G.b[k] - h < eta * (1 - L) / L]
    for k in kk:
        x, W = G.curves[k]
        xp, Wp = G.curves[k - 1]
        img = np.minimum(1.0, P.sigma_vec(x, np.interp(x, xp, Wp)))
        msk = x <= h - eta
        w = max(w, float(np.max(np.abs(W[msk] - img[msk]))))
    print("   eta = %.2f h: levels %d..30: %.2e" % (eta_h, kk[0] if kk else -1, w))

# ---------------------------------------------------------------------------------------------------------------
print("\n== (4) Proposition A11 ==")
print("# the recipe of the proof: m = theta_hint(g) - (h - L g); eta with (L - t_1(h - eta)) g <= m/3; k(eta); k_1 >= k(eta) with b_k - h <= m/3 and g lambda^(k - k(eta)) <= m/3")
for g_h in (2.0, 1.0, 0.5, 0.25):
    g = g_h * h
    m = P.theta_hint(g) - (h - L * g)
    # the largest eta (bisection): (L - t1(h - eta)) g <= m/3
    lo, hi = 0.0, h
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if (L - P.t1(h - mid)) * g <= m / 3:
            lo = mid
        else:
            hi = mid
    eta = lo
    lam = h * L / (h * L + eta)
    ks = [k for k in range(1, JE + 1) if S.b[k] - h < eta * (1 - L) / L]
    if not ks:
        print("g = %.2f h: m = %.3e, eta = %.3e h, lambda_eta = %.5f:  k(eta) > %d (not reached)" % (g_h, m, eta / h, lam, JE))
        continue
    keta = ks[0]
    k1 = next((k for k in range(keta, JE + 1) if S.b[k] - h <= m / 3 and g * lam ** (k - keta) <= m / 3), None)
    if k1 is None:
        print("g = %.2f h: m = %.3e, eta = %.3e h, lambda_eta = %.5f, k(eta) = %d:  k_1 > %d (not reached)" % (g_h, m, eta / h, lam, keta, JE))
        continue
    w = -math.inf
    for k in range(k1, JE + 1):
        w = max(w, defect(k, g) - g * lam ** (k - k1))
    print("g = %.2f h: m = %.3e (%.3f of theta_hint''(0) g^2/2), eta = %.4f h, lambda_eta = %.5f, k(eta) = %d, k_1 = %d;  max over k_1 <= k <= %d of [M_k(g) - theta_hint(g) - g lambda^(k-k_1)] = %.2e (<= 0)"
          % (g_h, m, m / (0.5 * P.vartheta * g * g), eta / h, lam, keta, k1, JE, w))

print("\n# observed geometric rate: D_k = M_k(g) - theta_hint(g);  ratio D_{k+1}/D_k against kappa_g = 1 - g/(J(t_g) + (1 - t_g) g), J'(t_g) = g, and exp(-g/h)")
for g_h in (0.1, 0.25, 0.5, 1.0, 2.0, 0.9 * es / h):
    g = g_h * h
    # t_g: J'(t) = g on [0, L]
    lo, hi = 0.0, L
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if P.dJ(mid) > g:
            lo = mid
        else:
            hi = mid
    tg = 0.5 * (lo + hi)
    kap = 1.0 - g / (P.J(tg) + (1 - tg) * g)
    Ds = [defect(k, g) for k in range(1, JE + 1)]
    ratios = []
    for k in range(1, JE):
        if Ds[k] > 1e-13 * a and Ds[k - 1] > 1e-13 * a:
            ratios.append((k, Ds[k] / Ds[k - 1]))
    tail = ratios[-6:]
    print("g = %.3f h (intercept of the tangent line: %.4f h, slope t_g = %.4f):  kappa_g = %.5f, exp(-g/h) = %.5f;  observed ratios at k = %s: %s"
          % (g_h, P.J(tg) / h, tg, kap, math.exp(-g / h), [r[0] + 1 for r in tail], " ".join("%.5f" % r[1] for r in tail)))

print("\n# rates at and beyond eps* (theta_hint = 0): the first k with M_{W_k,b_k}(g) = 0 exactly")
for g_e in (1.0, 1.2, 1.5, 2.0, 4.0):
    g = g_e * es
    k0 = next((k for k in range(1, JE + 1) if S.M(k, g)[0] <= 0.0), None)
    print("   g = %.1f eps*: M_k(g) = 0 from k = %s on;  M_1(g)/a = %.3e, M_2(g)/a = %.3e, M_3(g)/a = %.3e" % (g_e, k0, S.M(1, g)[0] / a, S.M(2, g)[0] / a, S.M(3, g)[0] / a))

# ---------------------------------------------------------------------------------------------------------------
print("\n== (5) the number of levels with n (M_k(g) - theta_hint(g)) <= 1 ==")
print("#   g/h      n = 1e4   1e6   1e8   1e10   1e12      slope dk/d(ln n) between 1e8 and 1e12     1/ln(1/kappa_g)     h/g")
for g_h in (0.1, 0.25, 0.5, 1.0, 2.0):
    g = g_h * h
    row = []
    for ex in (4, 6, 8, 10, 12):
        n = 10.0 ** ex
        k = next((k for k in range(1, JE + 1) if n * defect(k, g) <= 1.0), None)
        row.append(k)
    lo, hi = 0.0, L
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if P.dJ(mid) > g:
            lo = mid
        else:
            hi = mid
    tg = 0.5 * (lo + hi)
    kap = 1.0 - g / (P.J(tg) + (1 - tg) * g)
    sl = (row[4] - row[2]) / (4 * math.log(10.0)) if row[4] and row[2] else float("nan")
    print("  %6.3f    %s      %8.3f                              %8.3f          %8.3f"
          % (g_h, "  ".join("%4s" % r for r in row), sl, 1.0 / math.log(1.0 / kap), h / g))
