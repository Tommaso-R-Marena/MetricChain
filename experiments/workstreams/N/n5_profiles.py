#!/usr/bin/env python3
"""Workstream N, check 5: the exponent level (N_REPORT section 3) and the non-sharp tail functions of section 4.

  P1  the cube: the tail profile w(theta) = lim (1/m) ln Xi_m(e^{-m theta}) from exact tables (m up to 12800) against
      u rho - Lambda_1 (theta <= a), -theta (theta >= a); the uniform one-sided statement (U) of N_REPORT 2.8.
  P2  Proposition N7: the pair defined from w -- theta_hint = w^{-1}, theta_na = (w + id)^{-1} -- satisfies the fields of
      the Lean structure HintPair; J(t) = min_theta [theta + t w(theta)] equals Lambda(tu) - t Lambda(u); the two dual
      formulas theta_hint(e) = max_{t<=1}[J(t) - te], theta_na(x) = sup_{tau<1} (J(tau) - tau x)/(1 - tau).
  P3  profiles without the shear condition (P1) of Proposition N7: the transport profile of N_REPORT 4(e) on the cube;
      the identity theta_na(e + theta_hint(e)) = theta_hint(e) fails, and the closing level is the atom.
  P4  valid, non-sharp tail functions on the cube against the truth: ball-volume (inradius) and transport profiles.
  P5  heterogeneous families (two kinds of binary sites, slopes u_1, u_2): Proposition N8 (no split of the sites
      undercuts the hinted exponent) on random splits; the best outer block at two levels is not proportional.
  P6  the sorted-slope Harper bound at the exponential scale against the true heterogeneous profile.

Run:  python3 n5_profiles.py > out_n5_profiles.txt       (about half a minute)
"""
import math
import sys
import time

import numpy as np

t0 = time.time()
fails = 0
LN2 = math.log(2.0)


def kl(x, y):
    s = 0.0
    if x > 0:
        s += x * math.log(x / y)
    if x < 1:
        s += (1 - x) * math.log((1 - x) / (1 - y))
    return s


def Lam(v):
    return math.log(2.0 / (1.0 + math.exp(-v)))


def rho_of_theta(th):
    """rho in [0, 1/2] with KL(rho || 1/2) = th (th in [0, ln 2])"""
    lo, hi = 0.0, 0.5
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if kl(mid, 0.5) > th:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


class CubeProfile:
    def __init__(self, u):
        self.u = u
        self.p = 1 / (1 + math.exp(u))
        self.a = kl(self.p, 0.5)
        self.L1 = Lam(u)
        self.E = math.log(math.cosh(u / 2))
        self.h = kl(self.L1 / u, 0.5)

    def w(self, th):
        return self.u * rho_of_theta(th) - self.L1 if th <= self.a else -th

    def x(self, th):
        return self.w(th) + th

    def theta_hint(self, e):          # w^{-1}:  u rho - L1 = e
        r = (self.L1 + e) / self.u
        return kl(min(r, 0.5), 0.5) if e >= -self.a else -e

    def theta_na(self, x):            # (w + id)^{-1}: KL(rho || p_u) = x, rho in [p_u, 1/2]
        if x >= self.E:
            return 0.0
        lo, hi = self.p, 0.5
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if kl(mid, self.p) <= x:
                lo = mid
            else:
                hi = mid
        return kl(lo, 0.5)

    def J(self, t):
        return Lam(t * self.u) - t * self.L1


print("=" * 110)
print("P1. the tail profile of the cube from exact tables; the uniform one-sided statement (U)")
print("=" * 110)


def log_tables(m, u):
    j = np.arange(m + 1, dtype=float)
    lg = np.array([math.lgamma(k + 1.0) for k in range(m + 1)])
    lC = lg[m] - lg - lg[::-1]
    lB = np.logaddexp.accumulate(lC)
    lF = u * (j + 1) + np.logaddexp.accumulate(lC - u * j)
    lE = lF + np.log1p(-np.exp(lB - lF))
    return lB, lE


for u in (0.5, 1.0, 2.0):
    cp = CubeProfile(u)
    line = []
    for m in (100, 400, 1600, 12800):
        lB, lE = log_tables(m, u)
        # at q = |B(r)|/2^m:  theta = -(1/m) ln q,  (1/m) ln Xi = (lE[r] - m ln 2)/m ; Gamma~(r) = E_r/|B(r-1)| bounds Xi(q)/q on the step
        r = np.arange(1, (m - 1) // 2 + 1)                    # balls of measure <= 1/2 (theta > 0; see N_REPORT 2.8, (U))
        theta_lo = -(lB[r - 1] - m * LN2) / m                 # the smallest q of the step (largest theta)
        lgam = (lE[r] - lB[r - 1]) / m                        # sup over the step of (1/m) ln(Xi(q)/q)
        xbar = np.array([cp.x(min(th, LN2)) for th in theta_lo])
        dev_U = float(np.max(lgam - xbar))                    # one-sided: (1/m) ln(Xi/q) <= xbar(theta) + dev
        theta_b = -(lB[r] - m * LN2) / m
        wm = (lE[r] - m * LN2) / m
        wlim = np.array([cp.w(min(th, LN2)) for th in theta_b])
        dev_w = float(np.max(np.abs(wm - wlim)))
        line.append("m=%5d: sup|w_m - w| = %.4f, sup[(1/m)ln(Xi/q) - x(theta)] = %.4f (%.2f ln m/m)" % (m, dev_w, dev_U, dev_U * m / math.log(m)))
    print("  u=%.1f  " % u + ";  ".join(line))

print()
print("=" * 110)
print("P2. Proposition N7 for the cube profile: HintPair fields, J, the dual formulas")
print("=" * 110)
for u in (0.5, 1.0, 2.0, 4.0):
    cp = CubeProfile(u)
    # (P1): x = w + id nonincreasing, strictly decreasing on [0, a]; (P2): w convex
    ths = np.linspace(0, LN2, 4001)
    wv = np.array([cp.w(th) for th in ths])
    xv = wv + ths
    mono = bool(np.all(np.diff(xv) <= 1e-12))
    conv = bool(np.all(np.diff(wv, 2) >= -1e-9))
    # HintPair fields
    worst_ident = 0.0
    worst_mono = 0.0
    prev = None
    ok_lower = True
    for e in np.linspace(1e-4, cp.E * 0.9999, 600):
        th = cp.theta_hint(e)
        worst_ident = max(worst_ident, abs(cp.theta_na(e + th) - th))
        if prev is not None:
            worst_mono = max(worst_mono, prev - (e + th))
        prev = e + th
        ok_lower &= th >= cp.h - e - 1e-12
    na_h = abs(cp.theta_na(cp.h) - cp.h)
    # J(t) = min_theta [theta + t w(theta)] against Lambda(tu) - t Lambda(u)
    worstJ = 0.0
    for t in np.linspace(0, 1, 51):
        Jnum = float(np.min(ths + t * wv))
        worstJ = max(worstJ, abs(Jnum - cp.J(t)))
    # dual formulas
    ts = np.linspace(0, 1, 20001)
    Jt = np.array([cp.J(t) for t in ts])
    worst_dual_h, worst_dual_na = 0.0, 0.0
    for e in np.linspace(0, cp.E * 0.999, 40):
        worst_dual_h = max(worst_dual_h, abs(float(np.max(Jt - ts * e)) - cp.theta_hint(e)))
    for xx in np.linspace(cp.E * 0.01, cp.E * 0.999, 40):
        val = float(np.max((Jt[:-1] - ts[:-1] * xx) / (1 - ts[:-1])))
        worst_dual_na = max(worst_dual_na, abs(val - cp.theta_na(xx)))
    okall = mono and conv and worst_ident < 1e-9 and worst_mono < 1e-12 and ok_lower and na_h < 1e-9 and worstJ < 1e-4 \
        and worst_dual_h < 1e-6 and worst_dual_na < 1e-5
    fails += not okall
    print("  u=%.1f: a=%.5f h=%.5f E=%.5f | shear monotone %s, w convex %s | identity %.1e, e + theta_hint nondecreasing %s, "
          "theta_hint >= h - e %s, theta_na(h) = h %.1e | J: %.1e | theta_hint = max_t[J - te]: %.1e, theta_na = sup (J - tau x)/(1-tau): %.1e"
          % (u, cp.a, cp.h, cp.E, mono, conv, worst_ident, worst_mono < 1e-12, ok_lower, na_h, worstJ, worst_dual_h, worst_dual_na))

print()
print("=" * 110)
print("P3. a profile without the shear condition: the transport (bounded-differences) profile on the cube")
print("    w_T(theta) = sup_x [u x - max(theta, 2 x^2)] = u^2/8 (theta <= u^2/8),  u sqrt(theta/2) - theta (theta >= u^2/8)")
print("=" * 110)
for u in (0.5, 1.0):
    wT = lambda th: u * u / 8 if th <= u * u / 8 else u * math.sqrt(th / 2) - th
    # numerically from the definition
    xs = np.linspace(0, 1.0, 40001)                          # depth/(m u), up to the diameter
    worst = max(abs(float(np.max(u * xs - np.maximum(th, 2 * xs * xs))) - wT(th)) for th in np.linspace(0, LN2, 60))
    # relative tail x_T = w_T + theta: increasing
    ths = np.linspace(0, LN2, 2001)
    xT = np.array([wT(th) + th for th in ths])
    inc = bool(np.all(np.diff(xT) >= -1e-12))
    # the pair defined from w_T: theta_hint_T(e) = inf{theta: w_T(theta) <= e}; closing exponent = inf{theta: x_T(theta') <= x for all theta' >= theta}
    e = 0.0
    th_h = next(th for th in ths if wT(th) <= e) if wT(LN2) <= e else float('nan')
    xx = e + (th_h if th_h == th_h else LN2)
    closing = next((th for i, th in enumerate(ths) if np.all(xT[i:] <= xx)), LN2)       # LN2: only below the atom
    cp = CubeProfile(u)
    print("  u=%.1f: formula against the definition %.1e;  relative tail exponent x_T = w_T + theta increasing in theta: %s  (range %.4f .. %.4f);"
          % (u, worst, inc, xT[0], xT[-1]))
    print("        threshold E_T = u^2/8 = %.4f (true %.4f);  theta_hint,T(0) = u^2/2 = %.4f (true h = %.4f; enumeration ln 2 = %.4f)"
          % (u * u / 8, cp.E, th_h, cp.h, LN2))
    print("        closing exponent at the accuracy x = e + theta_hint,T(e), e = 0 (x = %.4f; relative tail at the atom scale %.4f > x): %.4f = ln 2,"
          " i.e. only below the atom; the identity theta_na(e + theta_hint(e)) = theta_hint(e) holds: %s"
          % (xx, xT[-1], closing, abs(closing - th_h) < 1e-3))
    fails += worst > 1e-4 or not inc

print()
print("=" * 110)
print("P4. valid tail functions on the cube that are not sharp: exponents against the truth")
print("    ball-volume: Xi(q) <= q (e^{u r_in(q)} - 1), r_in = radius of the largest ball of measure <= q:  w_in(theta) = u rho(theta) - theta")
print("=" * 110)
print("  %4s | %9s %9s %9s | %9s %9s %9s | %9s %9s" % ("u", "h true", "h ball", "h transp", "E true", "E ball", "E transp", "na(E/2)", "na ball"))
for u in (0.25, 0.5, 1.0, 2.0):
    cp = CubeProfile(u)
    # ball-volume profile: w_in(theta) = u rho(theta) - theta; theta_hint_in(0): u rho = KL(rho||1/2)
    lo, hi = 1e-9, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if u * mid - kl(mid, 0.5) < 0:
            lo = mid
        else:
            hi = mid
    h_in = kl(lo, 0.5)
    E_in = u * 0.5
    x_half = cp.E / 2
    na_true = cp.theta_na(x_half)
    na_in = kl(min(x_half / u, 0.5), 0.5)            # x_in(theta) = u rho(theta) = x
    print("  %4.2f | %9.5f %9.5f %9.5f | %9.5f %9.5f %9.5f | %9.5f %9.5f   %s"
          % (u, cp.h, h_in, u * u / 2, cp.E, E_in, u * u / 8, na_true, na_in,
             "(transport bound above enumeration: vacuous)" if u * u / 2 >= LN2 else ""))
    fails += not (h_in >= cp.h and u * u / 2 >= cp.h and E_in >= cp.E and u * u / 8 >= cp.E - 1e-12 and na_in >= na_true)

print()
print("=" * 110)
print("P5. heterogeneous families: two kinds of binary sites (uniform measure), slopes u_1, u_2, fractions lambda_1, lambda_2")
print("    J_beta = beta_1 J_{u_1} + beta_2 J_{u_2};  Rhat_beta(e) = max_t [J_beta(t) - te];  Theta_na^beta(x) = sup_tau (J_beta(tau) - tau x)/(1 - tau)")
print("=" * 110)
TS = np.linspace(0, 1, 4001)


class Hetero:
    def __init__(self, us):
        self.us = us
        self.Jk = [np.array([Lam(t * u) - t * Lam(u) for t in TS]) for u in us]
        self.ak = [kl(1 / (1 + math.exp(u)), 0.5) for u in us]
        self.Ek = [math.log(math.cosh(u / 2)) for u in us]

    def Jb(self, beta):
        return sum(b * J for b, J in zip(beta, self.Jk))

    def Rhat(self, beta, e):
        return float(np.max(self.Jb(beta) - TS * e))

    def Tna(self, beta, x):
        if x <= 0:
            return sum(b * a for b, a in zip(beta, self.ak))
        J = self.Jb(beta)
        return max(0.0, float(np.max((J[:-1] - TS[:-1] * x) / (1 - TS[:-1]))))

    def a(self, beta):
        return sum(b * a for b, a in zip(beta, self.ak))


# sanity: one kind reproduces the cube
H1 = Hetero([1.0])
cp = CubeProfile(1.0)
d1 = max(abs(H1.Tna([1.0], xx) - cp.theta_na(xx)) for xx in np.linspace(0.005, 0.11, 12))
d2 = max(abs(H1.Rhat([1.0], e) - cp.theta_hint(e)) for e in np.linspace(0.0, 0.11, 12))
print("  one kind, u = 1: sup-formulas against the cube's functions: theta_na %.1e, theta_hint %.1e" % (d1, d2))
fails += d1 > 1e-5 or d2 > 1e-6
# the homogeneous two-level value at accuracy 0 (K_REPORT: tau_2/a = 0.5004 at u = 1)
# S(x) = x + theta_na(x) is nondecreasing, so the supremum over gamma sits at gamma = phi a (and at gamma -> 0)
t2 = min(max(phi * cp.a + (1 - phi) * cp.theta_na(phi * cp.a / (1 - phi)), (1 - phi) * cp.a) for phi in np.linspace(0.3, 0.7, 40001))
print("  one kind, u = 1: tau_2/a = %.4f  (K_REPORT, erratum SCI-REV-0014: 0.5004)" % (t2 / cp.a))
fails += abs(t2 / cp.a - 0.5004) > 1e-4

rng = np.random.default_rng(5)
for us, lam in [([2.0, 0.5], [0.5, 0.5]), ([3.0, 1.0], [0.3, 0.7]), ([1.5, 0.25], [0.5, 0.5])]:
    H = Hetero(us)
    # Proposition N8: for every split alpha + beta = lambda, 0 < B < G:  sup_{gamma >= B} [min(gamma, mu) + Rhat_beta(gamma)] >= Rhat_lambda(G)
    worst = float('inf')
    for rep in range(400):
        alpha = [rng.uniform(0, l) for l in lam]
        beta = [l - a for l, a in zip(lam, alpha)]
        Etot = sum(l * E for l, E in zip(lam, H.Ek))
        G = rng.uniform(0.01, 1.0) * Etot
        B = rng.uniform(0.01, 0.99) * G
        mu = H.Tna(alpha, G - B)
        g0 = max(B, mu)
        lhs = min(g0, mu) + H.Rhat(beta, g0)            # the value at gamma = max(B, mu) (a lower bound of the supremum)
        worst = min(worst, lhs - H.Rhat(lam, G))
    # two levels at accuracy 0: tau_2(alpha) = sup_{gamma >= 0} [min(gamma, a_alpha) + Theta_na^{beta}(gamma)], general against proportional
    a_tot = H.a(lam)
    gam = np.linspace(0, 1.2 * a_tot, 301)

    def tau2(alpha):
        beta = [l - a for l, a in zip(lam, alpha)]
        aa = H.a(alpha)
        cand = [g for g in gam if g > 0] + [aa * f for f in (0.9, 0.97, 0.99, 1.0, 1.01, 1.03, 1.1) if aa > 0]
        return max(max(min(g, aa) + H.Tna(beta, g) for g in cand), H.a(beta))

    best_prop = min((tau2([phi * l for l in lam]), phi) for phi in np.linspace(0.05, 0.95, 91))
    best_gen = (float('inf'), None)
    for f1 in np.linspace(0.0, 1.0, 41):
        for f2 in np.linspace(0.0, 1.0, 41):
            if f1 + f2 == 0 or (f1 == 1 and f2 == 1):
                continue
            v = tau2([f1 * lam[0], f2 * lam[1]])
            if v < best_gen[0]:
                best_gen = (v, (f1, f2))
    h_tot = H.Rhat(lam, 0.0)
    print("  slopes %s fractions %s:  a = %.5f, h = %.5f;  Proposition N8 on 400 random splits: min [bracket - Rhat] = %.2e [>= 0]"
          % (us, lam, a_tot, h_tot, worst))
    print("      two levels at accuracy 0:  proportional split: tau_2 = %.5f (%.4f a) at phi = %.2f;   best split: tau_2 = %.5f (%.4f a) with "
          "the outer block taking %.0f%% of the sites of slope %.2f and %.0f%% of the sites of slope %.2f"
          % (best_prop[0], best_prop[0] / a_tot, best_prop[1], best_gen[0], best_gen[0] / a_tot, 100 * best_gen[1][0], us[0],
             100 * best_gen[1][1], us[1]))
    fails += worst < -1e-6 or best_gen[0] > best_prop[0] + 1e-9 or best_gen[0] < h_tot - 1e-9

print()
print("=" * 110)
print("P6. the sorted-slope Harper bound at the exponential scale (two kinds in equal parts, u_1 > u_2): its profile is")
print("    w_s(theta) = max_{rho' <= rho(theta)} [U(rho - rho') - KL(rho'||1/2)],  U(x) = u_1 x (x <= 1/2), against the true profile Rhat^{-1}")
print("=" * 110)
for us in ([2.0, 0.5], [1.5, 1.0], [1.0, 0.25]):
    H = Hetero(us)
    lam = [0.5, 0.5]
    rg = np.linspace(1e-6, 0.5, 4001)
    klr = np.array([kl(r, 0.5) for r in rg])

    def U(xx):
        return us[0] * np.minimum(xx, 0.5) + us[1] * np.maximum(xx - 0.5, 0)

    def w_sorted(i):           # at rho = rg[i]
        return float(np.max(U(rg[i] - rg[:i + 1]) - klr[:i + 1]))
    # hinted exponent of the bound at accuracy 0: the smallest theta = KL(rho) with w_sorted <= 0
    i0 = next(i for i in range(len(rg)) if w_sorted(i) > 0)
    h_sorted = klr[i0 - 1]
    cpmax = CubeProfile(us[0])
    print("  slopes %s:  h (true, Theorem 11.101) = %.5f;  from the sorted-slope bound: %.5f;  homogeneous cube with the larger slope: %.5f"
          % (us, H.Rhat(lam, 0.0), h_sorted, cpmax.h))
    fails += h_sorted < H.Rhat(lam, 0.0) - 1e-6

print()
print("failed checks:", fails, "   time %.1f s" % (time.time() - t0))
sys.exit(1 if fails else 0)
