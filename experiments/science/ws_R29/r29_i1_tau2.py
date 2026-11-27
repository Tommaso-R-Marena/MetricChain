#!/usr/bin/env python3
"""r29_i1_tau2.py [u ...]  --  the exponent of two nested levels at vanishing accuracy, tau_2, for the cube pair.

 (A) multiprecision (40 digits, mpmath; not rigorous):
       x*      the positive root of theta_na(x) = a - x  (through rho*: 2 KL(rho||1/2) + u rho - Lambda(u) - a = 0),
       cf      the closed form a^2/(a + x*) of Z_ADDENDUM A6a / Theorem 11.58e(e),
       direct  min_x  a max(a, x + theta(x))/(a + x)   (Proposition A12(a) with T = theta; a 1-d minimisation),
       brute   inf_phi sup_gamma [min(gamma, phi a) + (1 - phi) theta(gamma/(1 - phi))] on a plain grid in doubles
               (no use of convexity or of A12) -- a control of the reduction;
       cond    the condition under which cf = direct:  theta'(x*) >= -x*/(a + x*)   (re-derived in R29_REPORT section 2).
 (B) rigorous enclosure of tau_2 with my interval arithmetic (r29lib.DI), valid when the interval version of `cond`
     is verified:  rho* by bisection on rigorous signs, x* by monotonicity, a^2/(a + x*).
 (C) a scan over the slope u: for which u is the closed form the value of the level formula?
 PREDICTION (written before the first run): at u = 1/2, 1, 2 `cond` holds and cf = direct = their 0.055517524915 (u = 1);
 for large u (from my hand computation at u = 10) `cond` fails and direct < cf.
"""
import math
import sys
from fractions import Fraction as Fr

import r29lib as R

R.cap_memory()
import mpmath  # noqa: E402

us = sys.argv[1:] if len(sys.argv) > 1 else ["1", "2", "1/2"]


def tau2_mp(P):
    mp = mpmath
    G = lambda r: 2 * P.th_of(r) + P.u * r - P.lam1 - P.a          # = theta + e - a along rho; G(p_u) = 0
    # G is convex with G(p_u) = 0, G'(p_u) = -u < 0, G(1/2) = eps* - a
    if G(P.half) <= 0:
        return None
    lo, hi = P.pu, P.half
    # move lo to a point with G < 0
    lo = P.pu + (P.half - P.pu) * mp.mpf(10) ** -6
    assert G(lo) < 0
    for _ in range(int(mp.mp.prec) + 10):
        mid = (lo + hi) / 2
        if G(mid) < 0:
            lo = mid
        else:
            hi = mid
    rs = (lo + hi) / 2
    xs = P.e_of(rs)
    cf = P.a ** 2 / (P.a + xs)
    ell = mp.log((1 - rs) / rs)
    thp = -ell / (P.u - ell)                                         # theta'(x*)
    cond = thp + xs / (P.a + xs)                                     # >= 0  <=>  the minimum is at x*
    # direct: minimise F(x) = a max(a, x + theta(x))/(a + x) over x in (0, 3 eps*]; beyond eps*, F = a x/(a + x) increases
    def F(x):
        return P.a * max(P.a, x + P.theta(x)) / (P.a + x)
    # the minimum is at x* (kink) or at the interior point where d/dx [(x + theta)/(a + x)] = 0 beyond x*
    # parametrise by rho in [rho*, 1/2]:  x = e(rho), theta = th(rho)
    def Fr_(r):
        x = P.e_of(r)
        return P.a * (x + P.th_of(r)) / (P.a + x)
    best, rb = Fr_(rs), rs
    N = 2000
    for i in range(N + 1):
        r = rs + (P.half - rs) * i / N
        v = Fr_(r)
        if v < best:
            best, rb = v, r
    if rb != rs:                                                     # refine by golden section around rb
        lo2, hi2 = max(rs, rb - (P.half - rs) / N), min(P.half, rb + (P.half - rs) / N)
        gr = (mp.sqrt(5) - 1) / 2
        x1, x2 = hi2 - gr * (hi2 - lo2), lo2 + gr * (hi2 - lo2)
        f1, f2 = Fr_(x1), Fr_(x2)
        for _ in range(int(2.2 * mp.mp.prec)):
            if f1 < f2:
                hi2, x2, f2 = x2, x1, f1
                x1 = hi2 - gr * (hi2 - lo2)
                f1 = Fr_(x1)
            else:
                lo2, x1, f1 = x1, x2, f2
                x2 = lo2 + gr * (hi2 - lo2)
                f2 = Fr_(x2)
        rb = (lo2 + hi2) / 2
        best = min(best, Fr_(rb))
    return dict(rho_star=rs, x_star=xs, cf=cf, cond=cond, direct=best, rho_min=rb, x_min=P.e_of(rb), thp=thp)


def tau2_brute_double(u, nphi=4001, ngam=6001):
    """plain grid in doubles of inf_phi sup_gamma [min(gamma, phi a) + (1 - phi) theta(gamma/(1 - phi))]"""
    import numpy as np
    pu = 1 / (1 + math.exp(u))
    a = pu * math.log(2 * pu) + (1 - pu) * math.log(2 * (1 - pu))
    es = 0.5 * math.log(0.5 / pu) + 0.5 * math.log(0.5 / (1 - pu))

    def theta(e):
        e = np.asarray(e, dtype=float)
        lo = np.full(e.shape, pu)
        hi = np.full(e.shape, 0.5)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            kl = mid * np.log(mid / pu) + (1 - mid) * np.log((1 - mid) / (1 - pu))
            big = kl > e
            hi = np.where(big, mid, hi)
            lo = np.where(big, lo, mid)
        r = 0.5 * (lo + hi)
        out = r * np.log(2 * r) + (1 - r) * np.log(2 * (1 - r))
        return np.where(e >= es, 0.0, np.where(e <= 0, a, out))
    best = (math.inf, None)
    for phi in np.linspace(0.001, 0.999, nphi):
        gam = np.linspace(0.0, 3.0 * phi * a, ngam)
        v = float(np.max(np.minimum(gam, phi * a) + (1 - phi) * theta(gam / (1 - phi))))
        if v < best[0]:
            best = (v, float(phi))
    return best, a


def tau2_rigorous(u_fr, verbose=True):
    """rigorous enclosure [lo, hi] (Fractions) of a^2/(a + x*), and whether `cond` is verified rigorously"""
    C = R.CubeDI(u_fr)
    U = R.DI.of(u_fr)
    two = R.DI.of(2)
    # Lambda(u) = ln(2/(1 + e^-u)) = ln(2 e^u/(1 + e^u))
    LAM = (two * C.EU / (R.DI.of(1) + C.EU)).log()

    def Gsign(rho):
        """rigorous sign of G(rho) = 2 KL(rho||1/2) + u rho - Lambda(u) - a at an exact rational rho: -1, +1, or 0 (undecided)"""
        E, TH = C.pair_enclosures(rho)
        g = TH * two + U * R.DI.of(rho) - LAM - C.A
        return -1 if g.hi < 0 else (1 if g.lo > 0 else 0)
    bits = 220
    pu_hi = R.ceil_dyadic(C.PU.hi_fr(), bits)
    lo = pu_hi + (Fr(1, 2) - pu_hi) / 2 ** 20
    hi = Fr(1, 2)
    if Gsign(lo) != -1 or Gsign(hi) != 1:
        return None
    for _ in range(bits):
        mid = (lo + hi) / 2
        s = Gsign(mid)
        if s == -1:
            lo = mid
        elif s == 1:
            hi = mid
        else:
            break
    # G is convex on (p_u, 1/2) with G(p_u) = 0 and G < 0 just right of p_u: exactly one root in (lo0, 1/2), and it lies in [lo, hi]
    Elo, _ = C.pair_enclosures(lo)
    Ehi, _ = C.pair_enclosures(hi)
    x_lo, x_hi = Elo.lo_fr(), Ehi.hi_fr()                         # e(rho) is increasing on [p_u, 1/2]
    a_lo, a_hi = C.A.lo_fr(), C.A.hi_fr()
    t_lo = a_lo * a_lo / (a_lo + x_hi)                             # a^2/(a + x) is increasing in a, decreasing in x
    t_hi = a_hi * a_hi / (a_hi + x_lo)
    # cond: 1 - l/(u - l) >= a/(a + x*),  l = ln((1 - rho*)/rho*) <= ln((1 - lo)/lo)
    ell = ((R.DI.of(1) - R.DI.of(lo)) / R.DI.of(lo)).log()        # upper bound of l: decreasing in rho
    lhs = R.DI.of(1) - ell / (U - ell)                             # lower bound through its .lo  (needs u > l)
    rhs_hi = a_hi / (a_hi + x_lo)                                  # a/(a + x) is increasing in a, decreasing in x
    cond_ok = (U - ell).lo > 0 and lhs.lo_fr() >= rhs_hi
    return dict(lo=t_lo, hi=t_hi, cond_ok=cond_ok, rho_lo=lo, rho_hi=hi, x_lo=x_lo, x_hi=x_hi, a_lo=a_lo, a_hi=a_hi)


print("# tau_2 of the cube pair: closed form, direct minimisation, brute force, rigorous enclosure")
for us_ in us:
    ufr = Fr(us_)
    P = R.CubeMP(ufr, dps=40)
    r = tau2_mp(P)
    print("u = %s:  a = %s   eps* = %s   h/a = %s" % (us_, mpmath.nstr(P.a, 22), mpmath.nstr(P.estar, 15), mpmath.nstr(P.h / P.a, 12)))
    print("   (A) x* = %s (rho* = %s);  closed form a^2/(a+x*) = %s = %s a" % (mpmath.nstr(r["x_star"], 20), mpmath.nstr(r["rho_star"], 15), mpmath.nstr(r["cf"], 22), mpmath.nstr(r["cf"] / P.a, 15)))
    print("       direct min_x a max(a, x+theta)/(a+x)   = %s = %s a   at x = %s;   direct - cf = %s" % (mpmath.nstr(r["direct"], 22), mpmath.nstr(r["direct"] / P.a, 15), mpmath.nstr(r["x_min"], 12), mpmath.nstr(r["direct"] - r["cf"], 3)))
    print("       cond = theta'(x*) + x*/(a+x*) = %s  (>= 0: the minimum is at x*);  theta'(x*) = %s" % (mpmath.nstr(r["cond"], 8), mpmath.nstr(r["thp"], 8)))
    (bv, bphi), a_d = tau2_brute_double(float(ufr))
    print("       brute force grid (doubles, 4001 x 6001): %.10f = %.8f a at phi = %.4f   [control of the reduction; grid error ~1e-4 a]" % (bv, bv / a_d, bphi))
    rg = tau2_rigorous(ufr)
    if rg is None:
        print("   (B) rigorous enclosure: not available")
    else:
        print("   (B) rigorous: tau_2(cf) in [%s, %s], width %.2e;  cond verified rigorously: %s" % (mpmath.nstr(mpmath.mpf(rg["lo"].numerator) / rg["lo"].denominator, 30), mpmath.nstr(mpmath.mpf(rg["hi"].numerator) / rg["hi"].denominator, 30), float(rg["hi"] - rg["lo"]), rg["cond_ok"]))
        mid = mpmath.mpf(rg["lo"].numerator) / rg["lo"].denominator
        print("       mp value inside the rigorous enclosure: %s" % (mpmath.mpf(rg["lo"].numerator) / rg["lo"].denominator - mpmath.mpf(10) ** -38 <= r["cf"] <= mpmath.mpf(rg["hi"].numerator) / rg["hi"].denominator + mpmath.mpf(10) ** -38))

print("# (C) scan over the slope: is the closed form the value of the level formula?  (cond >= 0)")
print("#   u | a | x*/a | cf/a | direct/a | cond | (cf - direct)/a")
prev = None
for us_ in ["1/8", "1/4", "1/2", "1", "2", "3", "7/2", "4", "9/2", "5", "6", "8", "10", "14"]:
    P = R.CubeMP(Fr(us_), dps=30)
    r = tau2_mp(P)
    if r is None:
        print("  %5s | no root" % us_)
        continue
    print("  %5s | %s | %s | %s | %s | %+.4e | %.3e" % (us_, mpmath.nstr(P.a, 10), mpmath.nstr(r["x_star"] / P.a, 8), mpmath.nstr(r["cf"] / P.a, 10), mpmath.nstr(r["direct"] / P.a, 10), float(r["cond"]), float((r["cf"] - r["direct"]) / P.a)))
# the threshold slope by bisection on cond
lo, hi = mpmath.mpf(2), mpmath.mpf(10)
mpmath.mp.dps = 30
for _ in range(60):
    mid = (lo + hi) / 2
    P = R.CubeMP(str(mid), dps=30)
    r = tau2_mp(P)
    if r["cond"] >= 0:
        lo = mid
    else:
        hi = mid
print("# threshold slope u0 with cond = 0: u0 = %s  (closed form valid for u <= u0, false above)" % mpmath.nstr((lo + hi) / 2, 12))
R.finish("r29_i1_tau2")
