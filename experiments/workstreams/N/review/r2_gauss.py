#!/usr/bin/env python3
"""Referee's checks of N_REPORT section 5.1 (Theorem N9, Propositions N10, N11) -- own code, nothing imported from
the workstream.

 G-A  closed forms of Xi_L, Theta_L against quadrature of their integral definitions
 G-B  (TU), (TL) for random L-Lipschitz functions on R^1 (piecewise linear, slopes in [-L, L]) by quadrature
 G-C  (TU) for dips on non-half-space sets in R^2 and radial sets in R^n (balls, complements of balls, strips):
      the half-space must be extremal
 G-D  the profile inequalities of section 5.1
 G-E  Proposition N10(b): E min(V, e^{Lt}) for V = e^{L a_1}; the quantile t_x; the bound on K/((1+eta) p(t_x - 0))
 G-F  Proposition N10(b) / Theorem N1': my own implementation of the unbounded variant of Algorithm A on the
      linear instance (outer law N(0,1), oracle brackets): validity, levels <= J, M_max against the bound
 G-G  Proposition N11: hit fraction (exact cap measure against e^{-n s^2/2}), the effect of the ball dip by
      two-dimensional quadrature against the proved lower bound and against the half-space
"""
import math
import sys
import time

import numpy as np
from scipy import integrate, special, stats

Phi = stats.norm.cdf
phi = stats.norm.pdf
Phinv = stats.norm.ppf
INF = float("inf")
bad = 0


def Xi(L, q):
    """e^{L^2/2 - Lt} Phi(L - t) - Phi(-t),  t = Phi^{-1}(1 - q)   (log-space for large arguments)"""
    if q >= 1:
        return INF
    t = -Phinv(q)
    return math.exp(L * L / 2 - L * t + special.log_ndtr(L - t)) - q


def Theta(L, p):
    """p + e^{Lc + L^2/2} Phi(-c - L),  c = Phi^{-1}(p)"""
    if p >= 1:
        return 1.0
    c = Phinv(p)
    return p + math.exp(L * c + L * L / 2 + special.log_ndtr(-c - L))


def ThetaBar(L, p):
    return max(p, Theta(L, p))


def main():
    global bad
    t0 = time.time()
    rng = np.random.default_rng(7)
    # ----------------------------------------------------------------------------------------------------------
    print("G-A  closed forms against quadrature of  int_0^inf L e^{Lr} Phi(-t-r) dr  and  int_0^inf L e^{-Lr} Phi(c+r) dr")
    worst = 0.0
    for L in (0.3, 1.0, 2.5, 4.0, 6.0):
        for q in (1e-8, 1e-4, 0.02, 0.3, 0.7, 0.97):
            t = -Phinv(q)
            num, _ = integrate.quad(lambda r: L * math.exp(L * r + special.log_ndtr(-t - r)), 0, 60, limit=400, epsabs=0, epsrel=1e-12)
            worst = max(worst, abs(num / Xi(L, q) - 1))
            c = Phinv(q)
            num2, _ = integrate.quad(lambda r: L * math.exp(-L * r) * Phi(c + r), 0, 80, limit=400, epsabs=0, epsrel=1e-12)
            num2 += math.exp(-L * 80)          # the remainder of the integral (Phi = 1 there)
            worst = max(worst, abs(num2 / Theta(L, q) - 1))
    print("     30 pairs (L, q): largest relative difference %.2e" % worst)
    bad += worst > 1e-8
    # attained by half-lines: E(e^{L(x-t)_+} - 1) and E e^{-L(x-c)_+}
    worst = 0.0
    for L in (1.0, 3.0):
        for t in (-1.0, 0.5, 2.0):
            ex, _ = integrate.quad(lambda x: (math.exp(L * (x - t)) - 1) * phi(x), t, t + 40, limit=400, epsrel=1e-12)
            worst = max(worst, abs(ex / Xi(L, Phi(-t)) - 1))
            lo = Phi(t) + integrate.quad(lambda x: math.exp(-L * (x - t)) * phi(x), t, t + 40, limit=400, epsrel=1e-12)[0]
            worst = max(worst, abs(lo / Theta(L, Phi(t)) - 1))
    print("     half-line dips attain both functions: largest relative difference %.2e" % worst)
    bad += worst > 1e-8
    # ----------------------------------------------------------------------------------------------------------
    print("G-B  (TU), (TL) on R^1: random piecewise-linear psi with slopes in [-L, L], V = e^{-psi}; EXACT integration")
    print("     (on a linear piece psi = alpha + sigma x:  int e^{-psi} phi = e^{-alpha + sigma^2/2} [Phi(x + sigma)])")

    def dPhi(lo, hi):
        """Phi(hi) - Phi(lo) without cancellation"""
        if hi <= lo:
            return 0.0
        if lo >= 0:
            return special.ndtr(-lo) - special.ndtr(-hi)
        return special.ndtr(hi) - special.ndtr(lo)

    worstU, worstL, nlev = 0.0, INF, 0
    for rep in range(400):
        L = float(rng.choice([0.5, 1.0, 2.0, 3.0]))
        nk = int(rng.integers(1, 25))
        knots = np.sort(rng.uniform(-5, 5, nk))
        kind = rep % 4
        if kind == 0:
            slopes = rng.uniform(-L, L, nk + 1)
        elif kind == 1:
            slopes = rng.choice([-L, L], nk + 1)
        elif kind == 2:
            slopes = rng.choice([-L, 0.0, L], nk + 1, p=[0.3, 0.4, 0.3])
        else:                                    # a half-line dip with one kink, both signs
            slopes = np.zeros(nk + 1)
            slopes[rng.integers(0, nk + 1):] = -L if rep % 8 < 4 else L
        # pieces: (-inf, k_0], [k_0, k_1], ..., [k_{n-1}, inf);  psi(k_0) = 0
        ends = np.concatenate(([-INF], knots, [INF]))
        vals = np.zeros(nk)                      # psi at the knots
        for i in range(1, nk):
            vals[i] = vals[i - 1] + slopes[i] * (knots[i] - knots[i - 1])
        alphas = np.empty(nk + 1)                # psi(x) = alpha_i + slopes_i x on piece i
        alphas[0] = vals[0] - slopes[0] * knots[0]
        for i in range(1, nk + 1):
            alphas[i] = vals[i - 1] - slopes[i] * knots[i - 1]

        def moments(c, strict):
            """exact masses and integrals of e^{-psi} over {psi < c} (strict) or {psi <= c}, and over the complement"""
            mass = integ = cmass = cinteg = 0.0
            for i in range(nk + 1):
                lo, hi, al, sg = ends[i], ends[i + 1], alphas[i], slopes[i]
                if sg == 0:
                    inside = (al < c) if strict else (al <= c)
                    cut = hi if inside else lo            # inside part = [lo, cut]
                    parts = ((lo, cut, True), (cut, hi, False))
                elif sg > 0:                     # psi < c  <=>  x < (c - al)/sg
                    cut = min(max((c - al) / sg, lo), hi)
                    parts = ((lo, cut, True), (cut, hi, False))
                else:
                    cut = min(max((c - al) / sg, lo), hi)
                    parts = ((cut, hi, True), (lo, cut, False))
                for (a_, b_, ins) in parts:
                    if b_ <= a_:
                        continue
                    mm = dPhi(a_, b_)
                    ii = math.exp(-al + sg * sg / 2) * dPhi(a_ + sg, b_ + sg)
                    if ins:
                        mass += mm
                        integ += ii
                    else:
                        cmass += mm
                        cinteg += ii
            return mass, integ, cmass, cinteg

        def Xi2(q, qc):                          # Xi_L with t = Phi^{-1}(1-q) taken from the smaller of q, 1-q
            t = -Phinv(q) if q <= 0.5 else Phinv(qc)
            return math.exp(L * L / 2 - L * t + special.log_ndtr(L - t)) - q

        def Theta2(pp, pc):
            c_ = Phinv(pp) if pp <= 0.5 else -Phinv(pc)
            return pp + math.exp(L * c_ + L * L / 2 + special.log_ndtr(-c_ - L))

        for c in rng.uniform(vals.min() - 4 * L, vals.max() + 4 * L, 40):
            s_ = math.exp(-c)
            q, integ, qc, cinteg = moments(c, True)          # {V > s} and {V <= s}
            if q > 1e-13 and qc > 1e-13:
                r_ = (integ - s_ * q) / (s_ * Xi2(q, qc))
                if r_ > worstU:
                    worstU, whereU = r_, (L, q, qc, kind)
            pb, integ2, pc, cinteg2 = moments(c, False)      # {V >= s} and {V < s}
            if pb > 1e-13 and pc > 1e-13:
                r_ = (cinteg2 + s_ * pb) / (s_ * Theta2(pb, pc))
                if r_ < worstL:
                    worstL, whereL = r_, (L, pb, pc, kind)
                nlev += 1
    print("     worst cases (L, mass, complementary mass, kind): upper %s   lower %s" % (str(whereU), str(whereL)))
    print("     400 functions, %d levels: largest E(V-s)+/(s Xi_L(p(s))) = %.10f   smallest E min(V,s)/(s Theta_L(pbar(s))) = %.10f" % (nlev, worstU, worstL))
    bad += (worstU > 1 + 1e-9) + (worstL < 1 - 1e-9)
    # ----------------------------------------------------------------------------------------------------------
    print("G-C  dips e^{L dist(x, D^c)} on sets D that are not half-spaces: excess / Xi_L(gamma(D))  (must be <= 1)")
    worst = 0.0
    for L in (1.0, 2.5):
        for n in (2, 3, 10, 50):
            ch = stats.chi(n)
            for R in (0.5 * math.sqrt(n), math.sqrt(n), 1.5 * math.sqrt(n) + 1):
                # D = {|x| > R}: dist(x, D^c) = |x| - R
                q = ch.sf(R)
                ex = integrate.quad(lambda r: math.expm1(L * (r - R)) * ch.pdf(r), R, R + 60, limit=400)[0]
                worst = max(worst, ex / Xi(L, q))
                # D = {|x| < R}: dist(x, D^c) = R - |x|
                q = ch.cdf(R)
                ex = integrate.quad(lambda r: math.expm1(L * (R - r)) * ch.pdf(r), 0, R, limit=400)[0]
                worst = max(worst, ex / Xi(L, q))
        # strip D = {|x_1| < a} and its complement, in any dimension
        for a in (0.3, 1.0, 2.0):
            q = 2 * Phi(a) - 1
            ex = 2 * integrate.quad(lambda x: math.expm1(L * (a - x)) * phi(x), 0, a)[0]
            worst = max(worst, ex / Xi(L, q))
            q = 2 * Phi(-a)
            ex = 2 * integrate.quad(lambda x: math.expm1(L * (x - a)) * phi(x), a, a + 50, limit=400)[0]
            worst = max(worst, ex / Xi(L, q))
    print("     balls, complements of balls (n = 2, 3, 10, 50), strips and their complements: largest ratio %.6f" % worst)
    bad += worst > 1 + 1e-9
    # lower function: S a ball or the complement of a ball
    worstL = INF
    for L in (1.0, 2.5):
        for n in (2, 10, 50):
            ch = stats.chi(n)
            for R in (0.6 * math.sqrt(n), math.sqrt(n), 1.4 * math.sqrt(n)):
                p = ch.cdf(R)                         # S = {|x| <= R}
                val = p + integrate.quad(lambda r: math.exp(-L * (r - R)) * ch.pdf(r), R, R + 60, limit=400)[0]
                worstL = min(worstL, val / Theta(L, p))
                p = ch.sf(R)                          # S = {|x| >= R}
                val = p + integrate.quad(lambda r: math.exp(-L * (R - r)) * ch.pdf(r), 0, R, limit=400)[0]
                worstL = min(worstL, val / Theta(L, p))
    print("     lower function, S a ball or the complement of a ball: smallest ratio %.6f (must be >= 1)" % worstL)
    bad += worstL < 1 - 1e-9
    # ----------------------------------------------------------------------------------------------------------
    print("G-D  profile inequalities:  e^{(L-t)^2/2} [0<=t<=L]  <=  1 + Xi_L(q)/q  <=  3(1+t) e^{(L-t)_+^2/2} [t>=0]")
    v1 = v2 = 0
    for L in np.linspace(0.1, 12, 60):
        for t in np.linspace(0, 20, 401):
            q = Phi(-t)
            lhs = math.exp(L * L / 2 - L * t + special.log_ndtr(L - t) - special.log_ndtr(-t))      # 1 + Xi/q
            if lhs > 3 * (1 + t) * math.exp(max(L - t, 0) ** 2 / 2) * (1 + 1e-9):
                v1 += 1
            if t <= L and lhs < math.exp((L - t) ** 2 / 2) * (1 - 1e-9):
                v2 += 1
    print("     violations on a grid of 24 060 pairs: upper %d, lower %d" % (v1, v2))
    bad += v1 + v2
    # the limit Xi_L(q)/q ~ L/(t - L) for t >> L
    L = 2.0
    print("     Xi_L(q)/q against L/(t-L), L = 2:  " + "  ".join("t=%g: %.4f / %.4f" % (t, math.exp(L * L / 2 - L * t + special.log_ndtr(L - t) - special.log_ndtr(-t)) - 1, L / (t - L)) for t in (4, 8, 16, 30)))
    # ----------------------------------------------------------------------------------------------------------
    print("G-E  Proposition N10(b), V = e^{L a_1}, A = e^{L^2/2}")
    v = 0
    for L in np.linspace(0.2, 10, 50):
        for t in np.linspace(0, L, 101):
            val = Phi(t - L) + math.exp(L * t - L * L / 2 + special.log_ndtr(-t))        # E min(V, e^{Lt}) / A
            num = integrate.quad(lambda x: min(math.exp(L * x), math.exp(L * t)) * phi(x), -40, 40, limit=800, points=[t])[0] / math.exp(L * L / 2) if (L < 6 and abs(t - L / 2) < 1e-9) else val
            if abs(num / val - 1) > 1e-7 or val > math.exp(-(L - t) ** 2 / 2) * (1 + 1e-12):
                v += 1
    print("     E min(V, e^{Lt}) = A[Phi(t-L) + e^{Lt-L^2/2}Phi(-t)] <= A e^{-(L-t)^2/2} on 0 <= t <= L: violations %d of 5050" % v)
    bad += v
    print("     L    x_out   t_x (exact root)   L - sqrt(2 x_out)   1/p(t_x) = 1/Phi(-t_x)   2 e^{(L-sqrt(2x))^2/2}   ratio")
    for L in (2.0, 3.0, 5.0, 8.0):
        for frac in (0.1, 0.5, 0.9):
            x = frac * L * L / 2
            f = lambda t: math.log(Phi(t - L) + math.exp(L * t - L * L / 2 + special.log_ndtr(-t))) + x
            lo, hi = -40.0, 40.0
            for _ in range(200):
                mid = (lo + hi) / 2
                if f(mid) < 0:
                    lo = mid
                else:
                    hi = mid
            tx = hi
            lhs = 1 / Phi(-tx)
            rhs = 2 * math.exp((L - math.sqrt(2 * x)) ** 2 / 2)
            print("     %-4g %-7.3f %-18.4f %-19.4f %-24.4g %-24.4g %.3g" % (L, x, tx, L - math.sqrt(2 * x), lhs, rhs, lhs / rhs))
            bad += (lhs < rhs) + (tx < L - math.sqrt(2 * x))
    # ----------------------------------------------------------------------------------------------------------
    print("G-F  Theorem N1' / Proposition N10(b): own implementation of the unbounded variant on V = e^{L a}, a ~ N(0,1)")
    print("     (reference point 0: ell0 = E e^{-L|x|}, u0 = E e^{L|x|}; rung 0 = a valid bracket of ratio Phi(L)/Phi(-L))")
    for (L, lam, eta, etap, theta, nu1, b) in [(2.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.1), (3.0, 0.5, 0.5, 0.5, 2.0, 1.0, 0.25),
                                               (3.5, 1.0, 0.5, 1.0, 20.0, 1.0, 0.5), (2.0, 0.25, 0.25, 0.25, 0.3, 4.0, 0.1)]:
        res = run_unbounded(rng, L, lam, eta, etap, theta, nu1, b, delta=0.05, nrep=12)
        print("     " + res)
    # ----------------------------------------------------------------------------------------------------------
    print("G-G  Proposition N11")
    # cap measure: sigma_{n-1}(omega_1 >= s) = (1/2) I_{1-s^2}((n-1)/2, 1/2)
    worst = 0.0
    for n in (2, 3, 5, 10, 30, 100, 1000, 10000, 100000):
        for s in np.linspace(0.0, 0.999, 500):
            cap = 0.5 * special.betainc((n - 1) / 2, 0.5, 1 - s * s)
            worst = max(worst, cap / math.exp(-n * s * s / 2))
    print("     cap bound sigma(omega_1 >= s) <= e^{-n s^2/2}: largest ratio on a grid (n = 2 .. 1e5) = %.4f" % worst)
    bad += worst > 1 + 1e-12
    worst = 0.0
    for k in list(range(1, 2000)) + [10 ** 4, 10 ** 5, 10 ** 6]:
        worst = max(worst, stats.chi2.median(k) / k)
    print("     median(chi^2_k)/k, k = 1..1999, 1e4, 1e5, 1e6: largest %.6f (must be < 1)" % worst)
    bad += worst >= 1
    print("     L    t     n        hypothesis n >= max(4t^2, L T^2 t)   hit bound e^{-t^2/2}  max hit fraction   effect A(g)-1   proved bound   half-space   effect/half-space")
    for (L, t, n) in [(1.0, 0.5, 6), (1.0, 1.0, 6), (2.0, 1.0, 22), (2.0, 2.0, 44), (3.0, 1.0, 56), (3.0, 1.0, 1000), (3.0, 1.0, 10000),
                      (3.0, 3.0, 165), (4.0, 2.0, 224), (5.0, 2.5, 500), (3.0, 1.0, 30)]:
        T = L + 1.2816
        hyp = n >= max(4 * t * t, L * T * T * t)
        r0 = n / t
        rho = math.sqrt(n * n / (t * t) - n)
        # hit fraction of a point at radius r: P(omega_1 > (r^2+n)/(2 r r0)); maximal at r = sqrt(n)
        hits = []
        for r in np.linspace(0.05 * math.sqrt(n), 6 * math.sqrt(n), 4000):
            s = (r * r + n) / (2 * r * r0)
            hits.append(0.5 * special.betainc((n - 1) / 2, 0.5, 1 - s * s) if s < 1 else 0.0)
        # effect: E[e^{L (rho - |x - r0 e1|)_+} - 1], x_1 ~ N(0,1), S = |x_perp|^2 ~ chi^2_{n-1}
        ch2 = stats.chi2(n - 1)

        def inner(x1):
            smax = rho * rho - (x1 - r0) ** 2
            if smax <= 0:
                return 0.0
            f = lambda S: math.expm1(L * (rho - math.sqrt((x1 - r0) ** 2 + S))) * ch2.pdf(S)
            pts = [p_ for p_ in (n - 1 - 6 * math.sqrt(2 * n), n - 1.0, n - 1 + 6 * math.sqrt(2 * n)) if 0 < p_ < smax]
            return integrate.quad(f, 0, smax, limit=400, points=pts if pts else None)[0]

        eff = integrate.quad(lambda x1: inner(x1) * phi(x1), -12, min(r0 + rho, 40.0), limit=400, points=[t - 2, t, t + 2, L, L + 3])[0]
        proved = 0.112 * math.exp(L * L / 2 - L * t) - 0.5 * Phi(-t)
        half = Xi(L, Phi(-t))
        print("     %-4g %-5g %-8d %-36s %-21.4g %-18.4g %-15.5g %-14.5g %-12.5g %.4f"
              % (L, t, n, "yes" if hyp else "NO", math.exp(-t * t / 2), max(hits), eff, proved, half, eff / half))
        bad += (max(hits) > math.exp(-t * t / 2)) + (hyp and eff < proved)
    print("violations: %d   (%.1f s)" % (bad, time.time() - t0))
    return 1 if bad else 0


def run_unbounded(rng, L, lam, eta, etap, theta, nu1, b, delta, nrep):
    """Theorem N1' on (R, N(0,1)), V(a) = e^{La}; tail functions Xi_L, Theta_L; returns a summary line"""
    global bad
    A = math.exp(L * L / 2)
    ell0 = 2 * math.exp(L * L / 2) * Phi(-L)
    u0 = 2 * math.exp(L * L / 2) * Phi(L)
    x0 = math.log(Phi(L) / Phi(-L))
    xs = [x0, x0 / 3, b] if x0 / 3 > b else [x0, b]
    Lr = len(xs) - 1
    ceta = (1 - eta) / (1 + eta)
    # closing level: Xi(q) <= theta nu1 q and Xi(q) <= theta ThetaBar(ceta q) for all q < pi_*  (log grid from below)
    qs = np.exp(np.linspace(math.log(1e-14), 0, 4001))[:-1]
    pi_star = None
    for q in qs:
        if Xi(L, q) <= theta * nu1 * q and Xi(L, q) <= theta * ThetaBar(L, ceta * q):
            pi_star = q
        else:
            break
    if pi_star is None:
        return "L=%g: no closing level on the grid" % L
    pi_star *= 0.999
    s0 = ell0
    J = math.floor((math.log(u0 / s0) + b + lam + math.log((1 + eta) / ((1 - eta) * pi_star))) / lam)
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * nu0 / ((1 - eta) * pi_star)))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * (J + 1) * (m_max + 1) * (Lr + 2) / delta))
    nu = K * nu0
    Mbar = 2 * (1 + eta) * math.exp(lam) * nu0 * K / ((1 - eta) * pi_star)
    x_out = math.log(1 + math.exp(b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta))
    bound = 2 * K / (1 + eta) * math.exp((L - math.sqrt(2 * x_out)) ** 2 / 2) if x_out < L * L / 2 else None
    inval = wbad = over = 0
    Mmaxs, levs, widths = [], [], []
    for rep in range(nrep):
        mode = rep % 3
        a = np.empty(0)
        Lo = np.empty(0)
        Up = np.empty(0)
        rung = np.empty(0, dtype=np.int64)

        def bracket(vals, x):
            xi_ = rng.random(len(vals)) if mode == 0 else (np.ones(len(vals)) if mode == 1 else np.zeros(len(vals)))
            return vals * np.exp(-xi_ * x), vals * np.exp((1 - xi_) * x)

        ell, Sig, usum = ell0, 0.0, 0.0
        j, Mmax, stop = 0, 0, None
        while stop is None:
            if j > J:
                stop = 'abort-J'
                break
            sj = s0 * math.exp(j * lam)
            Mneg = nu * sj / (ell * math.exp(b))
            M = K
            while True:
                if M > K * 2 ** m_max or M > 3e7:
                    stop = 'abort-M'
                    break
                if len(a) < M:
                    nv = np.exp(L * rng.standard_normal(M - len(a)))
                    l0, u0_ = bracket(nv, xs[0])
                    a = np.concatenate([a, nv]); Lo = np.concatenate([Lo, l0]); Up = np.concatenate([Up, u0_])
                    rung = np.concatenate([rung, np.zeros(len(nv), dtype=np.int64)])
                Mmax = max(Mmax, M)
                while True:
                    idx = np.nonzero((Up[:M] > sj) & (Lo[:M] <= sj * math.exp(-b)))[0]
                    if len(idx) == 0:
                        break
                    rung[idx] += 1
                    for l in np.unique(rung[idx]):
                        sub = idx[rung[idx] == l]
                        nl, nu_ = bracket(a[sub], xs[min(l, Lr)])
                        Lo[sub] = np.maximum(Lo[sub], nl); Up[sub] = np.minimum(Up[sub], nu_)
                Nh = int(np.count_nonzero(Up[:M] > sj))
                q = min(1.0, max(Nh, K) / ((1 - eta) * M))
                pop = Nh >= K
                if pop:
                    plow = Nh / ((1 + eta) * M)
                    ell = max(ell, sj * math.exp(-b) * ThetaBar(L, plow))
                tl = sj * Xi(L, q)
                if tl <= theta * math.exp(b) * ell:
                    Lret = max(ell, Sig + ((1 - math.exp(-lam)) * math.exp(-b) * sj * plow if pop else 0.0))
                    Uret = s0 + usum + tl
                    stop = 'closed'
                    break
                if pop:
                    Sig += (1 - math.exp(-lam)) * math.exp(-b) * sj * plow
                    usum += sj * math.expm1(lam) * q
                    break
                if M >= Mneg:
                    usum += sj * math.expm1(lam) * q
                    break
                M *= 2
            j += 1
        if stop != 'closed':
            over += 1
            continue
        inval += not (Lret <= A <= Uret)
        wbad += Uret > math.exp(x_out) * Lret * (1 + 1e-12)
        Mmaxs.append(Mmax); levs.append(j - 1); widths.append(Uret / Lret)
    viol = inval + wbad + over + (bound is not None and len(Mmaxs) > 0 and min(Mmaxs) < bound)
    bad += viol
    return ("L=%g theta=%g: pi_*=%.3g (t-L=%.2f) J=%d K=%d Mbar=%.3g x_out=%.3f | runs %d closed %d invalid %d width-bad %d | "
            "levels <= %d | M_max min %d, N10(b) bound %s | U/L max %.3f"
            % (L, theta, pi_star, -Phinv(pi_star) - L, J, K, Mbar, x_out, nrep, len(Mmaxs), inval, wbad,
               max(levs) if levs else -1, min(Mmaxs) if Mmaxs else -1, ("%.4g" % bound) if bound else "n/a (x_out >= L^2/2)",
               max(widths) if widths else float('nan')))


if __name__ == "__main__":
    sys.exit(main())
