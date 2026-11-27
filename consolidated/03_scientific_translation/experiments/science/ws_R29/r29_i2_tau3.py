#!/usr/bin/env python3
"""r29_i2_tau3.py [u]  --  the second level T_2 = min(theta, R[theta]) of the level recursion and tau_3 = tau(T_2), by
direct evaluation with my own code (doubles; no grid interpolation of T_2; cross-checks in 30-digit arithmetic).

 R[theta](g) = inf_{0<phi<1, 0<=beta<=g} F(phi, beta; g),  mu = phi theta((g - beta)/phi),  S(y) = y + theta(y):
     F = (1 - phi) max( S(beta/(1-phi)), S(mu/(1-phi)) )          if beta <= mu      (S convex: the sup over gamma in
     F = mu + (1 - phi) theta(beta/(1 - phi))                      if beta >  mu       [beta, mu] is at an end point)
 minimised by r29rec.Rec2.R_theta: in the coordinates (y1, e) = (finest inner rate, outer rate), nested one-dimensional
 searches -- outer over y1, inner over e with a full scan every time (two earlier versions, a 2-d scan with nested
 golden sections and a moving 2-d zoom, stalled in the kink valley at some rates: NOTES.md).
 EVERY (phi, beta) gives an upper bound of R[theta](g): the minimisation can only err upwards.

 (1) T_2 at the 16 rates of their out_z7_exactness_u1.txt, against their numbers and against M_2 = M_{W_2, b_2}
     (my semi-analytic envelope, r29env.EnvSA);
 (2) tau_3:  with S_2(y) = y + T_2(y):  x2* := the first root of S_2(x) = tau_2;  checks (i) S_2 <= tau_2 on (0, x2*],
     (ii) S_2(x) >= tau_2 (a + x)/(a + x2*) for x >= x2*;  then tau_3 = a tau_2/(a + x2*)   (Proposition A12(a));
 (3) an upper bound UB_3 >= tau_3 that does not depend on the minimisation being converged: T_2(y_i) <= U_i :=
     F(phi_i, beta_i; y_i) for interpolated parameters, T_2 nonincreasing, T_2 <= tau_2, so for a grid 0 < y_1 < ... < y_N
     sup_{y <= y_N} S_2(y) <= max( tau_2 + y_1, max_i (y_{i+1} + U_i) );
 (4) tau(M_2) by the same operator on the majorant (must equal the envelope top b_3: Proposition A12(b));
 (5) rigorous-in-structure lower bounds: the blow-up intercepts of the orbit curves, tau_k >= sup{B : p_k(B) < inf}.
 Controls: (c1) the 2-d scan alone (no refinement) must be ABOVE the refined minimum; (c2) the operator applied to the
 hinted exponent must return it (R[theta_hint] = theta_hint, Theorem 11.53(b)) -- a test of my operator code on a case
 with a known answer;  (c3) a deliberately wrong operator (outer rate g/phi instead of (g - beta)/phi) must
 UNDERCUT the hinted exponent, which no level may do (Theorem 11.53(b)).
"""
import math
import sys

import numpy as np

import r29lib as R
import r29env as E

R.cap_memory()
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
P = E.CubeF(u)
a, es, h = P.a, P.estar, P.h
GR = (math.sqrt(5.0) - 1) / 2


import r29rec

REC1 = r29rec.Rec(P)          # F in the coordinates (phi, beta)
REC = r29rec.Rec2(P)          # the minimiser: nested one-dimensional searches in the coordinates (y1, e)


def theta_s(e):
    return P.theta(e)


def F_vec(phi, beta, g):
    return REC1.F_vec(phi, beta, g)


def golden(f, lo, hi, iters=70):
    x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
    f1, f2 = f(x1), f(x2)
    for _ in range(iters):
        if f1 < f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - GR * (hi - lo)
            f1 = f(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + GR * (hi - lo)
            f2 = f(x2)
    xm = 0.5 * (lo + hi)
    return xm, f(xm)


def R_theta(g, full=False, **kw):
    return REC.R_theta(g, full=full)


def T2(g):
    return REC.T2(g)


print("# cube u = %g: a = %.13f  h = %.13f  eps* = %.13f" % (u, a, h, es))
Pm = R.CubeMP(str(u) if u != 0.5 else "1/2", dps=30)
import mpmath  # noqa: E402

# ---- tau_2 (closed form valid at u <= 4.65; see r29_i1_tau2.py)
lo, hi = 1e-9 * es, es
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if mid + theta_s(mid) < a:
        lo = mid
    else:
        hi = mid
xs1 = 0.5 * (lo + hi)
tau2 = a * a / (a + xs1)
print("(0) tau_2 = a^2/(a + x*) = %.15f = %.12f a   (x* = %.13f)" % (tau2, tau2 / a, xs1))

# ---- semi-analytic envelope: W_1, W_2 and the tops
env = E.EnvSA(P, 3)
envmp = E.EnvSA(Pm, 3)
b2, b3 = env.b[2], env.b[3]
print("    envelope tops (semi-analytic): b_2 = %.15f, b_3 = %.15f = %.9f a;   mp: b_2 = %s, b_3 = %s" % (b2, b3, b3 / a, mpmath.nstr(envmp.b[2], 18), mpmath.nstr(envmp.b[3], 18)))

# ---- (1) T_2 at their rates
their = {0.0010: (0.1041732996, 0.0522553962, 0.5006, 0.4462, 0.0553974102), 0.0030: (0.0993461485, 0.0499936318, 0.5034, 0.4110, 0.0551571812),
         0.0100: (0.0902323797, 0.0458555137, 0.5127, 0.3508, 0.0543163796), 0.0300: (0.0763761895, 0.0398151847, 0.5416, 0.2481, 0.0519140895),
         0.0600: (0.0638800148, 0.0344739573, 0.5849, 0.1600, 0.0483106543), 0.1000: (0.0525374834, 0.0295522827, 0.6355, 0.0998, 0.0435060740),
         0.1500: (0.0423026900, 0.0249262149, 0.6900, 0.0598, 0.0375003486), 0.2000: (0.0345152903, 0.0212155198, 0.7365, 0.0378, 0.0314946233),
         0.3000: (0.0231964696, 0.0153877298, 0.8117, 0.0163, 0.0194831726), 0.4000: (0.0153699414, 0.0109243554, 0.8696, 0.0071, 0.0113309197),
         0.5000: (0.0097889744, 0.0074194587, 0.9144, 0.0028, 0.0076138049), 0.6000: (0.0058127614, 0.0046821020, 0.9482, 0.0010, 0.0047591681),
         0.7000: (0.0030598327, 0.0026149712, 0.9739, 0.0001, 0.0026341026), 0.8000: (0.0012811358, 0.0011561751, 0.9887, 0.0000, 0.0011592681),
         0.9000: (0.0003033388, 0.0002886242, 0.9974, 0.0000, 0.0002886322), 0.9500: (0.0000739261, 0.0000721403, 0.9994, 0.0000, 0.0000721401)}
print("(1) T_2 = min(theta, R[theta]) against their table (out_z7_exactness_u1.txt) and against my M_2:")
print("      g/eps* | theta(g) | my R[theta](g) | (phi, beta/g) | scan only (control c1: must be >= refined) | theirs R | mine - theirs | my M_2(g) | (M_2 - T_2)/a mine | theirs M_2 - my M_2")
c1_bad = 0
worst_gain = 0.0
neg_gap = 0
for q in sorted(their):
    g = q * es
    r, p_, b_, scan = R_theta(g, full=True)
    th = theta_s(g)
    t2 = min(th, r)
    m2 = float(env.M(2, g))
    if scan < r - 1e-15:
        c1_bad += 1
    worst_gain = max(worst_gain, scan - r)
    if m2 - t2 < 0:
        neg_gap += 1
    if u == 1.0:
        tt = their[q]
        print("    %8.4f | %.10f | %.10f | (%.4f, %.4f) | %.10f | %.10f | %+.2e | %.10f | %+.3e | %+.2e"
              % (q, th, r, p_, b_ / g, scan, tt[1], r - tt[1], m2, (m2 - t2) / a, tt[4] - m2), flush=True)
    else:
        print("    %8.4f | %.10f | %.10f | (%.4f, %.4f) | %.10f | - | - | %.10f | %+.3e | -" % (q, th, r, p_, b_ / g, scan, m2, (m2 - t2) / a), flush=True)
print("    control c1: scan below the refined minimum in %d of 16 cases [must be 0]; largest gain of the refinement %.2e" % (c1_bad, worst_gain))
print("    rates with M_2 < T_2 in doubles (Proposition A8 asks for T_2 <= M_2): %d" % neg_gap)
# where the maximising line of M_2 lies on the uncapped orbit part of W_2 (B <= both tangent points), the lower bound
# T_2 >= B - p_2(B) g of Theorem 11.53a(c) meets the upper bound: T_2 = M_2 exactly.  Check in 30 digits:
def F_mp_(phi, beta, g):
    phi, beta, g = mpmath.mpf(phi), mpmath.mpf(beta), mpmath.mpf(g)
    mu = phi * Pm.theta((g - beta) / phi)
    y1 = beta / (1 - phi)
    t1 = Pm.theta(y1)
    if beta <= mu:
        y2 = mu / (1 - phi)
        return (1 - phi) * max(y1 + t1, y2 + Pm.theta(y2))
    return mu + (1 - phi) * t1
for q in (0.8, 0.9, 0.95):
    g = q * es
    r, p_, b_ = R_theta(g)
    Ump = F_mp_(p_, b_, g)
    M2mp = envmp.M(2, mpmath.mpf(g))
    print("    g = %.2f eps*: F at my minimiser (30 digits) = %s;  M_2(g) (30 digits) = %s;  F - M_2 = %s  (T_2 <= F; A8: T_2 <= M_2)"
          % (q, mpmath.nstr(Ump, 16), mpmath.nstr(M2mp, 16), mpmath.nstr(Ump - M2mp, 3)), flush=True)
print("    tangent points of the envelope: Bt_1 = %.6f a, Bt_2 = %.6f a" % (env.Bt[1] / a, env.Bt[2] / a))

# ---- controls c2, c3: the operator on the hinted exponent
def th_hint(x):
    r_ = (P.lam1 + x) / P.u
    return 0.0 if r_ >= 0.5 else E.CubeF.kl(r_, 0.5)


def R_general(T, g, mode="ok", nphi=120, nb=40, ng=400):
    """brute force of R[T](g) for a general nonincreasing T (callable on arrays): grid over (phi, beta), sup over a gamma grid"""
    best = math.inf
    for phi in np.linspace(0.0, 1.0, nphi + 2)[1:-1]:
        for beta in np.linspace(0.0, g, nb + 1)[1:]:
            mu = phi * theta_s(((g - beta) if mode == "ok" else g) / phi)
            gam = np.concatenate([np.linspace(beta, max(mu, beta) * 1.0000001 + 1e-15, ng), np.linspace(max(mu, beta), 4 * es, 40)])
            v = np.minimum(gam, mu) + (1 - phi) * T(gam / (1 - phi))
            best = min(best, float(np.max(v)))
    return best


thv = np.vectorize(th_hint)
c2 = c3 = 0.0
for q in (0.1, 0.3, 0.6):
    g = q * es
    r_ok = R_general(thv, g)
    r_bad = R_general(thv, g, mode="bad")
    c2 = max(c2, abs(r_ok - th_hint(g)) / a)
    c3 = max(c3, (th_hint(g) - r_bad) / a)
print("    control c2: |R[theta_hint] - theta_hint|/a at g = 0.1, 0.3, 0.6 eps* (brute force, grid error expected ~1e-3): %.2e  [must be small]" % c2)
print("    control c3: wrong operator (outer rate g/phi): largest undercut (theta_hint - R_wrong[theta_hint])/a = %.2e  [must be clearly positive]" % c3)

# ---- (2) tau_3
def S2(y):
    return y + T2(y)


# shape on a grid
ys = np.concatenate([np.geomspace(1e-9, 0.02, 40), np.linspace(0.025, 1.0, 118)]) * es
S2v = np.array([S2(float(y)) for y in ys])
k_first = int(np.argmax(S2v >= tau2))
print("(2) S_2(y) = y + T_2(y) on %d rates: S_2 < tau_2 up to y = %.5f eps*, S_2 >= tau_2 from y = %.5f eps* on" % (len(ys), ys[k_first - 1] / es, ys[k_first] / es))
lo, hi = float(ys[k_first - 1]), float(ys[k_first])
flo, fhi = S2(lo) - tau2, S2(hi) - tau2
for _ in range(60):
    mid = 0.5 * (lo + hi)
    fm = S2(mid) - tau2
    if fm < 0:
        lo = mid
    else:
        hi = mid
    if hi - lo < 1e-15:
        break
x2 = 0.5 * (lo + hi)
tau3 = a * tau2 / (a + x2)
phi3 = x2 / (a + x2)
viol_i = int(np.sum(S2v[:k_first] > tau2 + 1e-14))
viol_ii = int(np.sum(S2v[k_first:] < tau2 * (a + ys[k_first:]) / (a + x2) - 1e-13))
print("    x2* = %.12f = %.8f eps*  (first root of S_2 = tau_2);  T_2(x2*) = %.12f;  phi_3 = x2*/(a + x2*) = %.8f" % (x2, x2 / es, T2(x2), phi3))
print("    check (i)  S_2 <= tau_2 on the grid below x2*: %d violations of %d;   check (ii) S_2(x) >= tau_2 (a+x)/(a+x2*) above: %d violations of %d" % (viol_i, k_first, viol_ii, len(ys) - k_first))
print("    tau_3 = a tau_2/(a + x2*) = %.13f = %.9f a      [theirs: 0.0400717432 = 0.361189 a at phi = 0.278215]" % (tau3, tau3 / a))
print("    b_3 - tau_3 = %.6e = %.6e a      [theirs: 2.112e-03 a]" % (b3 - tau3, (b3 - tau3) / a))
# cross-check of T_2(x2*) in 30-digit arithmetic at the minimiser found in doubles, and local optimality there
r, p_, b_ = R_theta(x2)
def F_mp(phi, beta, g):
    phi, beta, g = mpmath.mpf(phi), mpmath.mpf(beta), mpmath.mpf(g)
    mu = phi * Pm.theta((g - beta) / phi)
    y1 = beta / (1 - phi)
    t1 = Pm.theta(y1)
    if beta <= mu:
        y2 = mu / (1 - phi)
        return (1 - phi) * max(y1 + t1, y2 + Pm.theta(y2))
    return mu + (1 - phi) * t1
fmp = F_mp(p_, b_, x2)
print("    at x2*: minimiser (phi, beta/g) = (%.10f, %.10f); F in doubles %.15f, in 30 digits %s; difference %.1e" % (p_, b_ / x2, r, mpmath.nstr(fmp, 18), float(fmp - r)))
loc = min(float(F_mp(p_ * (1 + dp), b_ * (1 + db), x2)) for dp in (-1e-4, 0, 1e-4) for db in (-1e-4, 0, 1e-4) if (dp, db) != (0, 0))
print("    local optimality (30 digits): min of F at the 8 neighbours (+-1e-4 relative) minus F at the minimiser = %+.2e  [>= 0]" % (loc - float(fmp)))

# ---- (3) the upper bound UB_3
ynodes = np.concatenate([np.geomspace(1e-12, 0.9 * x2, 48), np.linspace(0.91 * x2, x2, 12)])
pars = [R_theta(float(y)) for y in ynodes]
pn = np.array([p[1] for p in pars])
bn = np.array([p[2] for p in pars]) / ynodes
yfine = np.concatenate([np.geomspace(1e-12, 0.9 * x2, 6000)[:-1], np.linspace(0.9 * x2, x2, 40001)])
pf = np.interp(np.log(yfine), np.log(ynodes), pn)
bf = np.interp(np.log(yfine), np.log(ynodes), bn) * yfine
U = F_vec(pf, bf, yfine)
U = np.minimum(U, tau2)                                  # T_2 <= tau_2 everywhere (proved in R29_REPORT, section 2)
cell = yfine[1:] + U[:-1]                                # bound of S_2 on [y_i, y_{i+1}]
run = np.maximum.accumulate(cell)                         # run[k-1] >= sup of S_2 over [y_0, y_k]
supb = np.maximum(run, tau2 + yfine[0])                   # ... over (0, y_k]   (S_2 <= tau_2 + y_0 on (0, y_0])
ub_all = a * supb / (a + yfine[1:])                       # tau_3 <= a sup_{y <= x} S_2(y)/(a + x) for every x = y_k
kbest = int(np.argmin(ub_all))
UB3 = float(ub_all[kbest])
x_ub = float(yfine[kbest + 1])
print("(3) upper bound that does not rely on the minimisation being converged (grid of %d rates, T_2 <= F at interpolated parameters):" % len(yfine))
print("    sup_{y <= x} S_2(y) <= tau_2 + %.2e for x = %.12f (= x2* - %.2e);" % (float(supb[kbest]) - tau2, x_ub, x2 - x_ub))
print("    UB_3 = %.13f = %.9f a;   UB_3 - tau_3 = %.2e a;   b_3 - UB_3 = %.6e a  (> 0: tau_3 < b_3)" % (UB3, UB3 / a, (UB3 - tau3) / a, (b3 - UB3) / a))

# ---- (4) the same operator on the majorant M_2 (must give b_3)
def tauM(x):
    return a * (x + float(env.M(2, x))) / (a + x)
xm, tm = golden(tauM, 1e-6, es, iters=80)
print("(4) tau(M_2) = min_x a (x + M_2(x))/(a + x) = %.13f = %.9f a at x = %.8f;  b_3 = %.13f;  difference %.2e a   [theirs on a grid: 0.363303 a]" % (tm, tm / a, xm, b3, (tm - b3) / a))

# ---- (5) lower bounds from the orbit curves
def blow_up(k):
    """sup{B : p_k(B) < inf}: the root of p_{k-1}(B) = 1 - B/a"""
    def p(j, B):
        s = 0.0
        for _ in range(j):
            s = P.Sigma(B, s)
            if s == math.inf:
                return math.inf
        return s
    lo, hi = 0.0, a
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if p(k - 1, mid) < 1 - mid / a:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
lb2, lb3 = blow_up(2), blow_up(3)
print("(5) orbit-curve lower bounds (Theorem 11.53a(c)): tau_2 >= %.12f = %.8f a;  tau_3 >= %.12f = %.8f a" % (lb2, lb2 / a, lb3, lb3 / a))
print("    ordering  lower bound <= tau_k <= b_k:  k = 2: %.9f <= %.9f <= %.9f : %s;   k = 3: %.9f <= %.9f <= %.9f : %s"
      % (lb2 / a, tau2 / a, b2 / a, lb2 <= tau2 <= b2 + 1e-15, lb3 / a, tau3 / a, b3 / a, lb3 <= tau3 <= b3))
R.finish("r29_i2_tau3 u=%g" % u)
