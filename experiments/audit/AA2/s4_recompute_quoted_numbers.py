#!/usr/bin/env python3
"""AA2 audit, script S4 -- independent re-computation of numbers quoted in theory report sections
11.16-11.32 from the formulas printed in the report (own code; nothing imported from the repository).

Every line is  PASS / FAIL  <where in the report>  computed  quoted  .  A FAIL is a candidate error of the
report (or of this script: each FAIL was inspected by hand, see docs/audit/AA2_REPORT.md, part (d)).

Run:  python3 experiments/audit/AA2/s4_recompute_quoted_numbers.py > experiments/audit/AA2/out_s4.txt
"""
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar, minimize, linprog
from scipy.special import gammaln, logsumexp
from scipy.spatial import ConvexHull, HalfspaceIntersection

results = []


def check(where, got, want, tol, note=""):
    ok = abs(got - want) <= tol
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {where:<58s} computed {got:<14.7g} quoted {want:<12.7g} tol {tol:g} {note}")
    return ok


def kl(a, b):
    out = 0.0
    if a > 0:
        out += a * math.log(a / b)
    if a < 1:
        out += (1 - a) * math.log((1 - a) / (1 - b))
    return out


# =============================================================== A. the uniform cube
print("== A. uniform cube (sections 11.16, 11.18, 11.19, 11.24) ==")


class Cube:
    def __init__(self, u):
        self.u = u
        self.pu = 1 / (1 + math.exp(u))
        self.lam1 = math.log(2 / (1 + math.exp(-u)))
        self.rho_h = self.lam1 / u
        self.h = kl(self.rho_h, 0.5)
        self.a = kl(self.pu, 0.5)
        self.estar = math.log(math.cosh(u / 2))

    def theta_na(self, x):
        if x >= self.estar:
            return 0.0
        if x <= 0:
            return self.a
        rho = brentq(lambda r: kl(r, self.pu) - x, self.pu, 0.5)
        return kl(rho, 0.5)

    def finv(self, th):                       # rho <= 1/2 with KL(rho || 1/2) = th
        if th <= 0:
            return 0.5
        return brentq(lambda r: kl(r, 0.5) - th, 1e-300, 0.5)

    def D(self, th):
        return self.u * self.finv(th) - self.lam1


c1 = Cube(1.0)
check("11.18 notation / 11.19: h at u=1", c1.h, 0.029139, 6e-7)
check("11.18 notation / 11.19: a at u=1", c1.a, 0.110944, 6e-7)
check("11.117 table: cube threshold ln cosh(1/2)", c1.estar, 0.120115, 6e-7)
check("11.58a Numbers: h/a at u=1", c1.h / c1.a, 0.2626, 6e-5)
for u, th, tn in ((1.0, 0.0291, 0.1109), (0.5, 0.0077, 0.0303), (2.0, 0.0973, 0.3278)):
    c = Cube(u)
    check(f"11.16 line 4276: theta_hint(0+) at u={u}", c.h, th, 6e-5)
    check(f"11.16 line 4276: theta_na(0+) at u={u}", c.a, tn, 6e-5)
c = Cube(0.05)
check("11.16: ratio a/h -> 4 as u -> 0 (u = 0.05)", c.a / c.h, 4.0, 0.01)

# rate constants (remark after Theorem 11.53) and C_* (Theorem 11.58a(b))
for u, cstar in ((0.5, 4.65), (1.0, 8.64), (2.0, 13.5)):
    c = Cube(u)
    a, h = c.a, c.h
    kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
    cc1 = h * (1 + kappa) / kappa
    cc2 = (a + h) * (2 * a - h) / (h * a) - 2
    rbar = (2 * a - h) / (a - h)
    Cs = 2 * math.sqrt((1 + rbar) * cc1 * (a / h + 4))
    if u == 1.0:
        check("11.53 remark: kappa at u=1", kappa, 0.0427, 6e-5)
        check("11.53 remark: c1 at u=1", cc1, 0.712, 6e-4)
        check("11.53 remark: c1/a at u=1 ('6.4a')", cc1 / a, 6.4, 0.06)
        check("11.53 remark: c2 at u=1", cc2, 6.35, 6e-3)
    check(f"11.58a(b): C_* at u={u}", Cs, cstar, 0.06 if u == 2.0 else 6e-3)

# tau_2 (remark (1) of 11.19) and T^(2)(0) (Theorem 11.84(b))
tau2 = minimize_scalar(lambda ph: max((1 - ph) * c1.a, ph * c1.a + (1 - ph) * c1.theta_na(ph * c1.a / (1 - ph))),
                       bounds=(1e-6, 1 - 1e-6), method="bounded", options={"xatol": 1e-12}).fun
check("11.19 remark (1): tau_2/a at u=1 (closed form)", tau2 / c1.a, 0.5004, 6e-5)


def T2(c):
    def obj(v):
        ph, xi = v
        if not (0 < ph < 1) or xi <= 0:
            return 10.0
        return max(ph * c.a + (1 - ph) * c.theta_na(xi), min(ph * c.a, (1 - ph) * xi) + (1 - ph) * c.a)
    best = (10.0, None)
    for ph in np.linspace(0.02, 0.98, 97):
        for xi in np.linspace(0.02 * c.estar, 1.5 * c.estar, 80):
            v = obj((ph, xi))
            if v < best[0]:
                best = (v, (ph, xi))
    res = minimize(obj, best[1], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 4000})
    return min(res.fun, best[0])


for u, want in ((0.05, 0.618), (0.5, 0.620), (1.0, 0.624), (2.0, 0.641), (3.0, 0.665)):
    c = Cube(u)
    check(f"11.84(b): T^(2)(0)/a at u={u}", T2(c) / c.a, want, 1.5e-3 if u == 0.05 else 6e-4)


def theta2star(c):
    def Xi(th, ph1):
        ph2 = 1 - ph1
        top = min(th, ph1 * c.a)
        cs = np.linspace(0.0, top, 400)
        vals = [ph1 * (c.D(x / ph1) + x / ph1) + ph2 * c.D((th - x) / ph2) for x in cs]
        k = int(np.argmin(vals))
        lo_, hi_ = cs[max(k - 1, 0)], cs[min(k + 1, len(cs) - 1)]
        r = minimize_scalar(lambda x: ph1 * (c.D(x / ph1) + x / ph1) + ph2 * c.D((th - x) / ph2),
                            bounds=(lo_, hi_), method="bounded", options={"xatol": 1e-13})
        return min(r.fun, vals[k])
    best = (0.0, None)
    def sup_theta(ph1):
        ph2 = 1 - ph1
        hi_ = ph2 * c.a * (1 - 1e-9)
        if Xi(hi_, ph1) > 0:
            return hi_
        lo_ = c.h
        if Xi(lo_, ph1) <= 0:
            return 0.0
        for _ in range(50):
            mid = 0.5 * (lo_ + hi_)
            if Xi(mid, ph1) > 0:
                lo_ = mid
            else:
                hi_ = mid
        return lo_
    for ph1 in np.linspace(0.40, 0.80, 41):
        th = sup_theta(ph1)
        if th > best[0]:
            best = (th, ph1)
    # refine the outer fraction around the best grid point (step 0.001)
    for ph1 in np.linspace(best[1] - 0.01, best[1] + 0.01, 21):
        th = sup_theta(ph1)
        if th > best[0]:
            best = (th, ph1)
    return best


for u, wa, wh, wphi in ((0.5, 0.349, 1.38, 0.65), (1.0, 0.359, 1.37, 0.64), (2.0, 0.394, 1.33, 0.61), (3.0, 0.440, 1.28, 0.56)):
    c = Cube(u)
    th, ph1 = theta2star(c)
    check(f"11.86 table: theta_2*/a at u={u}", th / c.a, wa, 1.5e-3)
    check(f"11.86 table: theta_2*/h at u={u}", th / c.h, wh, 1.2e-2)
    check(f"11.86 table: best phi_1 at u={u}", ph1, wphi, 0.011)


# remark (1a): the two lower-bound columns of the table (exact binomial sums)
def lb_columns(n, u, eps, delta):
    j = np.arange(n + 1)
    lc = gammaln(n + 1) - gammaln(j + 1) - gammaln(n - j + 1)          # ln C(n, j)
    cum = np.logaddexp.accumulate(lc)                                    # ln |B(n, r)|
    # non-adaptive: least R with D_R > eps
    tot = n * math.log1p(math.exp(-u))
    lcu = lc - u * j
    suf = np.logaddexp.accumulate(lcu[::-1])[::-1]                       # ln sum_{j >= R} C e^{-uj}
    R_found = None
    for R in range(1, n + 1):
        low = cum[R - 1] - u * R
        DR = tot - np.logaddexp(low, suf[R])
        if DR > eps:
            R_found = R
            break
    ln_lb = math.log(1 - 2 * delta) + n * math.log(2) - cum[R_found - 1]
    # hinted: least k with Delta_k > eps;  e^{Delta_k} - 1 = 2^{-n} sum_{j<=k} C(n,j)(e^{u(k+1-j)} - 1)
    k_found = None
    for k in range(0, n + 1):
        xx = u * (k + 1 - j[:k + 1])
        terms = lc[:k + 1] + xx + np.log1p(-np.exp(-xx))                 # ln(e^x - 1) without overflow
        val = logsumexp(terms) - n * math.log(2)                         # ln(e^{Delta_k} - 1)
        if val > math.log(math.expm1(eps)):
            k_found = k
            break
    ln_hint = math.log(1 - 2 * delta) + n * math.log(2) - cum[k_found]
    return ln_lb, ln_hint


for u, n, wlb, whint in ((1.0, 1000, 110.90, 31.69), (1.0, 1350, 149.02, 42.02), (1.0, 1400, 155.02, 43.49),
                         (2.0, 540, 176.48, 55.08), (0.5, 4700, 141.54, 38.97)):
    ln_lb, ln_hint = lb_columns(n, u, 0.8715, 0.05)
    check(f"11.19 (1a) table: ln LB, u={u}, n={n}", ln_lb, wlb, 6e-3)
    check(f"11.19 (1a) table: ln hinted LB, u={u}, n={n}", ln_hint, whint, 6e-3)
ln_lb, _ = lb_columns(16000, 1.0, 0.8715, 0.05)
check("11.19 (1a): ln LB at n=16 000, u=1", ln_lb, 1767.6, 6e-2)
ln_lb, _ = lb_columns(6400, 1.0, 0.25 * c1.estar * 6400, 0.05)
check("11.16: non-adaptive LB exponent, n=6400, eps1=estar/4, delta=.05", ln_lb / 6400, 0.0293, 6e-5)
check("11.45(d): 'e^{188}' at n = 6400", ln_lb, 188.0, 0.6)
print()

# =============================================================== B. a field
print("== B. a field as known part (section 11.20) ==")


def Fgame(gam, t, theta, u):
    lam, lp, lm = theta + gam, theta + u, theta - u
    C = lambda x: 2 * math.cosh(x / 2)
    if t <= 0:
        return 0.0
    num = math.sinh(t * (lp - lam) / 2) * C(lm) ** t + math.sinh(t * (lam - lm) / 2) * C(lp) ** t
    return math.log(num / math.sinh(t * u)) - t * math.log(C(lam))


def Fstar(t, theta, u):
    r = minimize_scalar(lambda g: -Fgame(g, t, theta, u), bounds=(-u, u), method="bounded", options={"xatol": 1e-12})
    return -r.fun, r.x


def field_numbers(theta, u):
    R0 = -minimize_scalar(lambda t: -Fgame(0.0, t, theta, u), bounds=(1e-6, 1 - 1e-6), method="bounded",
                          options={"xatol": 1e-12}).fun
    r = minimize_scalar(lambda t: -Fstar(t, theta, u)[0], bounds=(1e-6, 1 - 1e-6), method="bounded", options={"xatol": 1e-12})
    Rmax, tstar = -r.fun, r.x
    gstar = Fstar(tstar, theta, u)[1]
    p = 1 / (1 + math.exp(theta))
    lg = math.log(p / (1 - p))
    a0, a1 = 1 / (1 + math.exp(-(lg - u))), 1 / (1 + math.exp(-(lg + u)))
    rstar = brentq(lambda r_: kl(a0, r_) - kl(a1, r_), a0, a1)
    acap = kl(a0, rstar)
    plain = max(kl(a0, p), kl(a1, p))
    return R0, Rmax, gstar, acap, plain, p, rstar


tab = {0.0: (.0973, .0973, 0.0, .3278, .3278), 0.5: (.0929, .0938, -.170, .3162, .4078), 1.0: (.0811, .0839, -.330, .2836, .4621),
       2.0: (.0487, .0542, -.583, .1841, .4338), 3.0: (.0230, .0272, -.734, .0928, .2732)}
rstars = {0.5: (0.3775, 0.4308), 1.0: (0.2689, 0.3607), 2.0: (0.1192, 0.2225), 3.0: (0.0474, 0.1124)}
for theta, (w0, wmax, wg, wa, wplain) in tab.items():
    R0, Rmax, gstar, acap, plain, p, rstar = field_numbers(theta, 2.0)
    check(f"11.65 table u=2, theta={theta}: R_0(0+)", R0, w0, 6e-5)
    check(f"11.65 table u=2, theta={theta}: R^max(0+)", Rmax, wmax, 6e-5)
    check(f"11.65 table u=2, theta={theta}: gamma*", gstar, wg, 2e-3)
    check(f"11.65 table u=2, theta={theta}: a", acap, wa, 6e-5)
    check(f"11.65 table u=2, theta={theta}: plain Monte Carlo from pi", plain, wplain, 6e-5)
    if theta in rstars:
        check(f"11.61 product samplers: p at theta={theta}", p, rstars[theta][0], 6e-5)
        check(f"11.61 product samplers: r* at theta={theta}", rstar, rstars[theta][1], 6e-5)
check("11.61: plain MC / a, largest ratio in the table ('up to 2.9')",
      max(field_numbers(th, 2.0)[4] / field_numbers(th, 2.0)[3] for th in (0.5, 1.0, 2.0, 3.0)), 2.9, 0.06)


def site_numbers(p, u):
    theta = math.log((1 - p) / p)
    E = max(Fstar(t, theta, u)[0] / t for t in (1e-5, 2e-5))             # limit t -> 0
    E = Fstar(1e-6, theta, u)[0] / 1e-6
    r = minimize_scalar(lambda t: -Fstar(t, theta, u)[0], bounds=(1e-6, 1 - 1e-6), method="bounded", options={"xatol": 1e-12})
    h = -r.fun
    a = field_numbers(theta, u)[3]
    return theta, E, h, a


theta, E, h, a = site_numbers(0.3, 1.0)
check("11.103 example table, site 'bin': E", E, 0.103131, 3e-6)
check("11.103 example table, site 'bin': a", a, 0.095301, 6e-7)
check("11.103 example table, site 'bin': h = R^(0)", h, 0.025034, 6e-7)
Rhat = lambda e: -minimize_scalar(lambda t: -(Fstar(t, theta, 1.0)[0] - t * e), bounds=(1e-6, 1 - 1e-6), method="bounded",
                                  options={"xatol": 1e-12}).fun
check("11.103 example table, 'bin': R^(0.3E)  (= 11.109a 'R^max = 0.012210')", Rhat(0.3 * 0.103131), 0.012209, 1.5e-6)
tna = lambda x: -minimize_scalar(lambda t: -(Fstar(t, theta, 1.0)[0] - t * x) / (1 - t), bounds=(1e-6, 1 - 1e-4), method="bounded",
                                 options={"xatol": 1e-12}).fun
check("11.103 example table, 'bin': theta_na(0.3E)", tna(0.3 * 0.103131), 0.019941, 1.5e-6)
check("11.25 'what the corollary does not say': R^max(0) at p=0.3, u=1", h, 0.025034, 6e-7)
theta, E, h, a = site_numbers(0.1, 2.0)
check("D49 item 11 / 11.20: threshold E at p=0.1, u=2", E, 0.212295, 3e-6)
Rhat2 = -minimize_scalar(lambda t: -(Fstar(t, theta, 2.0)[0] - t * 0.3 * 0.212295), bounds=(1e-6, 1 - 1e-6), method="bounded",
                         options={"xatol": 1e-12}).fun
check("11.20 Numbers: R^max(0.3E) at p=0.1, u=2", Rhat2, 0.023270, 1.5e-6)
print()

# =============================================================== C. slices
print("== C. slices (section 11.25, Theorem 11.90 numbers at u = 1) ==")


def slice_numbers(kap, u):
    def F(m, ell):
        x1, x2 = kap + ell / (2 * m), kap - ell / (2 * (1 - m))
        if not (0 <= x1 <= 1 and 0 <= x2 <= 1):
            return math.inf
        return m * kl(x1, kap) + (1 - m) * kl(x2, kap)

    def ellmax(m):
        return min(2 * m * (1 - kap), 2 * (1 - m) * kap)

    def psi_and_arg(m, s):
        r = minimize_scalar(lambda ell: -(s * ell - F(m, ell)), bounds=(0.0, ellmax(m)), method="bounded", options={"xatol": 1e-13})
        return -r.fun, r.x

    def V0(m):                                   # hinted value at e = 0
        ps, _ = psi_and_arg(m, u)
        return F(m, ps / u)

    def N0(m):                                   # non-adaptive value at X = 0+
        _, ell = psi_and_arg(m, u)
        return F(m, ell)
    grid = np.linspace(0.02, 0.98, 97)
    mb = max(grid, key=V0)
    r1 = minimize_scalar(lambda m: -V0(m), bounds=(max(mb - 0.02, 1e-3), min(mb + 0.02, 1 - 1e-3)), method="bounded", options={"xatol": 1e-10})
    mb2 = max(grid, key=N0)
    r2 = minimize_scalar(lambda m: -N0(m), bounds=(max(mb2 - 0.02, 1e-3), min(mb2 + 0.02, 1 - 1e-3)), method="bounded", options={"xatol": 1e-10})
    return -r1.fun, r1.x, -r2.fun, r2.x


for kap, wR, wm, wN, wm2 in ((0.5, 0.029139, 0.500, 0.110944, 0.5), (0.45, 0.028856, 0.477, 0.109898, 0.471),
                             (0.4, 0.028005, 0.454, 0.106755, 0.442), (0.3, 0.024588, 0.408, 0.094080, 0.383),
                             (0.2, 0.018842, 0.362, 0.072574, 0.325), (0.1, 0.010688, 0.316, 0.041588, 0.266)):
    R, m1, N, m2 = slice_numbers(kap, 1.0)
    check(f"11.90 numbers: R^kappa(0), kappa={kap}", R, wR, 1.5e-6)
    check(f"11.90 numbers: best centre type for R, kappa={kap}", m1, wm, 2e-3)
    check(f"11.90 numbers: N^kappa(0+), kappa={kap}", N, wN, 1.5e-6)
    check(f"11.90 numbers: centre type for N, kappa={kap}", m2, wm2, 2e-3)
K = lambda x: x * math.tanh(x) - math.log(math.cosh(x))
check("11.91 proof: -K(u/2) at u=1 ('-0.11')", -K(0.5), -0.11, 6e-3)
check("Lemma 11.89: ln 2 - h(sigma(s)) = K(s/2) at s=1", math.log(2) + (lambda q: q * math.log(q) + (1 - q) * math.log(1 - q))(1 / (1 + math.exp(-1.0))), K(0.5), 1e-12)
print()

# =============================================================== D. alphabets
print("== D. alphabets (section 11.26, Proposition 11.103) ==")
Psi = lambda k, s: math.log((math.exp(s) + k - 1) / k) - s / k


def hk(k, u):
    return -minimize_scalar(lambda t: -(t * Psi(k, u) - Psi(k, t * u)), bounds=(0.0, 1.0), method="bounded", options={"xatol": 1e-13}).fun


def ak(k, u):
    pk = math.exp(u) / (math.exp(u) + k - 1)
    q = (1 - pk) / (k - 1)
    H = -pk * math.log(pk) - (k - 1) * q * math.log(q)
    return math.log(k) - H


check("11.103(d): h_2 at u=0.5", hk(2, 0.5), 0.007673, 6e-7)
check("11.103(d): h_3 at u=0.5", hk(3, 0.5), 0.007425, 6e-7)
check("11.103(d): a_2 at u=0.3", ak(2, 0.3), 0.011125, 6e-7)
check("11.103(d): a_3 at u=0.3", ak(3, 0.3), 0.010582, 6e-7)
check("11.103(e): h_2 = h_3 exactly at e^u = 2", hk(2, math.log(2)) - hk(3, math.log(2)), 0.0, 1e-11)
check("11.103(e): h_3 = h_4 exactly at e^u = 6", hk(3, math.log(6)) - hk(4, math.log(6)), 0.0, 1e-11)
check("11.103(e): h_4 = h_5 exactly at e^u = 12", hk(4, math.log(12)) - hk(5, math.log(12)), 0.0, 1e-11)
ucross = brentq(lambda u: ak(2, u) - ak(3, u), 0.3, 0.8)
check("11.103(d): a_2 = a_3 at u = 0.5194", ucross, 0.5194, 6e-5)
check("11.103(e): q=4, u=1: h_2", hk(2, 1.0), 0.029139, 6e-7)
check("11.103(e): q=4, u=1: a_4", ak(4, 1.0), 0.117993, 6e-7)
check("11.103(e): q=4, u=1: E_2", Psi(2, 1.0), 0.120115, 6e-7)
check("11.103(d): E of the uniform three-letter law at u=1", Psi(3, 1.0), 0.119499, 6e-7)
check("11.103(d)/(b): h of the uniform three-letter law at u=1", hk(3, 1.0), 0.030654, 6e-7)
check("11.103(d): a of the uniform three-letter law at u=1", ak(3, 1.0), 0.123284, 6e-7)
check("11.103(f): cube h/(u^2/32) at u=0.1", hk(2, 0.1) / (0.01 / 32), 0.9993, 6e-5)
for u, w in ((0.5, 5.0), (1.0, 1.9), (2.0, 5.8)):
    check(f"11.103(f): uniform 3-letter site below the ceiling u^2/32 at u={u} (%)", 100 * (1 - hk(3, u) / (u * u / 32)), w, 0.06)
check("11.103(f): the same as u -> 0 (u = 0.01), '11 %'", 100 * (1 - hk(3, 0.01) / (1e-4 / 32)), 11.0, 0.3)
c = Cube(1.0)
theta = 0.3 * c.a
rho = brentq(lambda r: kl(r, 0.5) - theta, 1e-9, 0.5)
check("11.99: E_sp(theta) - theta at theta = 0.3a, cube u=1 ('-0.008')", kl(rho, c.pu) - theta, -0.008, 6e-4)
print()

# =============================================================== E. box classes
print("== E. box classes (section 11.30) ==")
delta, rho_m, eps = 0.05, 3.0, 0.2
Ncentre = math.ceil(math.log(1 / delta) * max(1, math.expm1(rho_m) / math.expm1(eps / 2), (1 - math.exp(-rho_m)) / (1 - math.exp(-eps / 2))))
check("11.111: 544 evaluations at the centre (rho=3, eps=0.2, delta=0.05)", Ncentre, 544, 0)
Ngen = math.ceil(math.log(1 / delta) * max(1, 2 * math.expm1(rho_m) / math.expm1(eps / 2), 2 * (1 - math.exp(-rho_m)) / (1 - math.exp(-eps / 2))))
check("11.111: 1088 evaluations by the general count", Ngen, 1088, 0, "(computed from the display of 11.110(c))")
qv = min(math.expm1(0.1) / math.expm1(rho_m), 1 - math.exp(-0.1))
check("11.111 'what the hint buys': 545 without a hint", math.ceil(math.log(1 / delta) / qv) + 1, 545, 0)
check("11.111: n from which the box bound is smaller (0.0291 n = ln 1088)", math.log(1088) / 0.0291, 240, 1.0)
L = lambda w: math.log(math.expm1(w) / w) - 1 + w / math.expm1(w)
W = lambda b, s2: math.log((b * b * math.exp(-s2 / b) + s2 * math.exp(b)) / (b * b + s2))
check("11.110(f): L(3.7)", L(3.7), 1.46, 6e-3)
check("11.110(f): W(3.7, 0.036^2)", W(3.7, 0.036 ** 2), 3.4e-3, 6e-5)
check("11.110(a): L(w) <= w^2/8 at w = 1 (difference)", 1 / 8 - L(1.0), 0.0, 1.0, "(sign only)")
check("11.114: e^8 - 1 '~ 2980'", math.expm1(8), 2980, 1.0)
check("11.114: cost number for ln Z '0.11'", (1 - 1e-6) * math.expm1(0.1) + 1e-6 * math.expm1(8), 0.11, 6e-3)
for Dl, w in ((0.0605, 0.94), (1.0, 0.37), (3.0, 0.05)):
    check(f"11.113(d): factor e^-Delta at Delta={Dl}", math.exp(-Dl), w, 6e-3)
check("11.113 illustration: width from 50 000 samples (nats)", math.expm1(0.0605) * math.sqrt(2 * math.log(2 / 0.05) / 50000), 7.6e-4, 6e-6)
check("11.113 illustration: width from 1 200 samples (nats)", math.expm1(0.0605) * math.sqrt(2 * math.log(2 / 0.05) / 1200), 5e-3, 2e-4)
check("11.112(f): ln mu change of a 100 kT dip on mass 1e-6 ('86')", math.log(1e-6 * math.expm1(100)), 86, 0.6)
check("11.113a: kappa(delta) at delta = 0.1", math.sqrt(math.log(2 / 0.1) / math.log(6 / 0.1)), 0.855, 6e-4)
check("11.113a: kappa(delta) at delta = 0.05", math.sqrt(math.log(2 / 0.05) / math.log(6 / 0.05)), 0.878, 6e-4)
check("11.113a: kappa(delta) at delta = 0.01", math.sqrt(math.log(2 / 0.01) / math.log(6 / 0.01)), 0.910, 6e-4)
kap = math.sqrt(math.log(2 / 0.05) / math.log(6 / 0.05))
check("11.113a: ((sqrt(1+4 kappa) - 1)/2)^2 at delta = 0.05", ((math.sqrt(1 + 4 * kap) - 1) / 2) ** 2, 0.316, 6e-4)
check("11.113a: factor sqrt(ln(6/delta)/ln(2/delta)) at delta=0.05", 1 / kap, 1.14, 6e-3)
print()

# =============================================================== F. the chain
print("== F. a nearest-neighbour chain (section 11.32) ==")
EF = lambda p, u: math.log((1 - p) * math.cosh(u / 2) + math.sqrt((1 - p) ** 2 * math.sinh(u / 2) ** 2 + p * p))
for p, w in ((0.4, 0.1691), (0.3, 0.2324), (0.2, 0.3108)):
    check(f"11.117 table: E_inf = E_F at p={p}, u=1", EF(p, 1.0), w, 6e-5)
check("11.117(a): threshold ratio at p=0.3 ('1.935')", EF(0.3, 1.0) / math.log(math.cosh(0.5)), 1.935, 6e-4)
check("11.117(c): E_F(0.7, 1)", EF(0.7, 1.0), 0.0540, 6e-5)
for p, w in ((0.4, 1.218), (0.3, 1.526), (0.2, 1.981), (0.1, 2.750)):
    us = brentq(lambda x: x - 1.0 - math.log(((1 - p) * math.exp(x) + p) / (p * math.exp(x) + 1 - p)), 1.0, 10.0)
    check(f"11.116(d): one-sided slack u* at u=1, p={p}", us, w, 6e-4)
    check(f"11.116(d): u* < u + K at p={p} (margin)", 1.0 + math.log((1 - p) / p) - us, 1.0, 1.0, "(sign only)")
lam = 0.4
var4 = 4 + 2 * sum((4 - k) * lam ** k for k in range(1, 4))
check("11.117(b): Var(sum s)/n at n=4, p=0.3", var4 / 4, 1.792, 6e-4)
check("11.117(b): structure factor (1-p)/p at p=0.3", 0.7 / 0.3, 2.33, 6e-3)
lam = -0.4
check("11.117(b): antiferromagnet, n=3, p=0.7: Var(sum s)/4", (3 + 2 * (2 * lam + lam ** 2)) / 4, 0.43, 6e-3)
check("11.117(b): antiferromagnet, staggered: 1.23", (3 + 2 * (2 * abs(lam) + lam ** 2)) / 4, 1.23, 6e-3)
check("11.117(d) table: cube a at u=3", Cube(3.0).a, 0.5023, 6e-5)
check("11.117(d) table: cube a at u=4", Cube(4.0).a, 0.6031, 6e-5)
check("11.117(d) table: cube h at u=4", Cube(4.0).h, 0.2393, 6e-5)
check("11.117(d): ratio 0.4958/0.5023", 0.4958 / Cube(3.0).a, 0.987, 6e-4)
check("11.117(d): ratio 0.4675/0.5023", 0.4675 / Cube(3.0).a, 0.931, 6e-4)
check("11.117(d): ratio 0.5097/0.6031", 0.5097 / Cube(4.0).a, 0.845, 6e-4)
check("11.117(d): ratio 0.2331/0.2393", 0.2331 / Cube(4.0).h, 0.974, 6e-4)
check("11.117(a): h_inf larger by 38 % (0.0401/0.029139 - 1)", 100 * (0.0401 / c1.h - 1), 38, 0.6)
check("11.117(a): ... to 54 % (0.0450/0.029139 - 1)", 100 * (0.0450 / c1.h - 1), 54, 0.6)
check("11.117(a): a_inf larger by 14 % (0.1264/0.110944 - 1)", 100 * (0.1264 / c1.a - 1), 14, 0.6)
check("11.117(a): ... to 27 % (0.1409/0.110944 - 1)", 100 * (0.1409 / c1.a - 1), 27, 0.6)
print()

# =============================================================== G. the lattice chain
print("== G. limit shape of the lattice chain (section 11.22) ==")
norm = lambda v: 5 * abs(v[0]) + 3 * abs(v[0] + v[1]) + abs(v[0] + v[1] + v[2]) + abs(v[3])
check("11.68: beta = norm of (1,9,14;1)", norm((1, 9, 14, 1)), 60, 0)
check("11.68: beta' = norm of (1,3,6;1)", norm((1, 3, 6, 1)), 28, 0)
check("11.69: R = norm of the box corner (1,5,6;1)", norm((1, 5, 6, 1)), 36, 0)
check("11.69: 168 = beta + 3R", 60 + 3 * 36, 168, 0)
check("11.69b(c): norm of A <= (1,6,10;1)", norm((1, 6, 10, 1)), 44, 0)
check("11.69b(c): norm of B <= (0,3,4;0)", norm((0, 3, 4, 0)), 16, 0)
check("11.69b(d): 108 = 15 + 54 + 36 + 3", 5 * 3 + 3 * 18 + 36 + 3, 108, 0)
check("11.69a: c = 2 sqrt(beta (d+1)(beta'+R)) for bridges", 2 * math.sqrt(60 * 5 * (28 + 36)), 277, 0.6)
check("11.69b: 216*14 + 108", 216 * 14 + 108, 3132, 0)
check("11.73: coefficient 9*2^(-2/3) + 4*3", 9 * 2 ** (-2 / 3) + 12, 17.6, 0.08)
check("11.73 (Bezdek): coefficient 9*2^(-2/3) + 4*4.617", 9 * 2 ** (-2 / 3) + 4 * 4.617, 24.1, 0.06)
check("11.73: constant 9 + 8 + 4*3.1", 9 + 8 + 4 * 3.1, 29.4, 0.01)
check("11.73 (Bezdek): 3 (18 pi)^(1/3)/pi", 3 * (18 * math.pi) ** (1 / 3) / math.pi, 3.665, 6e-4)
Nhalf = brentq(lambda N: 17.6 * N ** (-1 / 3) - 17 / N - 0.5, 1e3, 1e6)
check("11.73 'when the shape is resolved': N <= 43 512", Nhalf, 43512, 60)
Nq = brentq(lambda N: 17.6 * N ** (-1 / 3) - 17 / N - 0.25, 1e3, 1e7)
check("11.73: >= 1/4 for N <= 3.4e5", Nq, 3.4e5, 1.2e4)
Nb = brentq(lambda N: 24.1 * N ** (-1 / 3) - 29.4 / N - 0.5, 1e3, 1e7)
check("11.73: with Bezdek's constant, N <= 1.1e5", Nb, 1.1e5, 6e3)
check("11.73: proved k >= 0.50 (17.6/35)", 17.6 / 35, 0.50, 6e-3)
check("11.73: k >= 0.689 with Bezdek (24.1/35)", 24.1 / 35, 0.689, 6e-4)
for frac, w in ((0.5, 47), (0.8, 730), (0.9, 5800)):
    check(f"11.73: beads needed for {int(100 * frac)} % of the bulk extent (k = 1.8)", (1.8 / (1 - frac)) ** 3, w, 0.02 * w)
# the polytopes of Proposition 11.72: rows (c3, c8, c11; b)
rows1 = [(-1, 0, 0, 0), (4, -1, 0, 0), (6, -1, 0, 1), (-2, 1, 0, 3), (-1, 1, -1, 0), (-1, 2, -1, 3), (-4, 2, -1, 2),
         (3, 4, -3, 5), (6, -2, 1, 2), (0, -1, 2, 7), (-3, 0, 2, 9)]
rows2 = [r for r in rows1 if r != (-4, 2, -1, 2)] + [(-3, 2, -1, 2), (-3, 4, -3, 2)]


def polytope(rows):
    A = np.array([r[:3] for r in rows], float)
    b = np.array([r[3] for r in rows], float)
    nrm = np.linalg.norm(A, axis=1)
    res = linprog([0, 0, 0, -1], A_ub=np.hstack([A, nrm[:, None]]), b_ub=b, bounds=[(None, None)] * 3 + [(0, None)], method="highs")
    centre = res.x[:3]
    hs = HalfspaceIntersection(np.hstack([A, -b[:, None]]), centre)
    hull = ConvexHull(hs.intersections)
    verts = sorted({tuple(np.round(v, 9) + 0.0) for v in hs.intersections[hull.vertices]})
    return hull.volume, verts


v1, verts1 = polytope(rows1)
v2, verts2 = polytope(rows2)
check("11.72(b): vol K_1", v1, 3.2269, 6e-5)
check("11.72(b): number of vertices of K_1", len(verts1), 12, 0)
check("11.72(c): vol K_2", v2, 3.125, 1e-9)
check("11.72(c): number of vertices of K_2", len(verts2), 12, 0)
listed = sorted([(0, 0, 0), (0, 0, 2), (0, 1, 4), (0, 2, 2), (0, 2, 4.5), (0, 3, 4), (0, 3, 4.5), (0.5, 2, 1.5), (0.5, 2, 3),
                 (0.5, 3.5, 3.5), (0.5, 4, 4.5), (1, 5, 6)])
same = len(verts2) == len(listed) and all(max(abs(a - b) for a, b in zip(x, y)) < 1e-7 for x, y in zip(verts2, listed))
check("11.72(c): the 12 listed vertices are the vertices of K_2", float(same), 1.0, 0)
check("11.72: K_1 as a share of the bulk box (%)", 100 * v1 / 30, 10.8, 0.06)
check("11.72: K_2 as a share of the bulk box (%)", 100 * v2 / 30, 10.4, 0.06)
tet = abs(np.linalg.det(np.array([(0.5, 2, 1.5), (1, 5, 6), (0, 0, 1)], float))) / 6
check("11.72(d): volume of the tetrahedron rod-row-crystal-helix", tet, 1 / 12, 1e-12)
check("11.72(e): 37 401/166 199", 37401 / 166199, 0.225, 6e-4)
check("11.71: ratio of the ends of the bracket [116, 3627] ('a factor 31')", 3627 / 116, 31, 0.5)
print()

# =============================================================== H. where asymptotic error terms bite
print("== H. sizes at which the proved error terms are below the exponents (computational reading; no quoted value) ==")
for label, expo in (("u=1 cube exponent h = 0.0291", 0.029139), ("u=2, theta=1: R^max = 0.0839", 0.0839), ("u=2, theta=0 a = 0.3278", 0.3278)):
    nmin = (2 / expo) ** 8
    print(f"INFO  Theorem 11.63: omega_n = 2 n^(-1/8) <= exponent ({label}) needs n >= {nmin:.2e}")
for q in (2, 3, 4, 20):
    for expo in (0.05, 0.3):
        nmin = (q / expo) ** (2 * q + 2)
        print(f"INFO  Theorem 11.97(c): q_max n^(-1/(2 q_max + 2)) <= {expo} with q_max = {q} needs n >= {nmin:.2e}")
print()
print(f"SUMMARY: {sum(results)} of {len(results)} checks PASS, {len(results) - sum(results)} FAIL")
