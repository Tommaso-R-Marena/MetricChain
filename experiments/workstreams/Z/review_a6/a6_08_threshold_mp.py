#!/usr/bin/env python3
"""a6_08_threshold_mp.py  --  the closed form tau_2 = a^2/(a + x*) of A6a for the cube, in 40-digit arithmetic
(mpmath `mp`, not intervals; a cross-check of part D of a6_01_prop_a12.py that shares no code with it).

For the cube, in the parameter rho (x = KL(rho || p_u), theta(x) = KL(rho || 1/2), rho in [p_u, 1/2]):
  x* : the root of x + theta(x) = a beyond the minimum of x + theta(x);   lambda* = |theta'(x*)| = l/(u - l), l = ln((1-rho)/rho);
  the closed form holds iff lambda* <= x*/(a + x*);
  tau_2 = min over rho of a max(a, x + theta)/(a + x)  (golden section beyond x*; the function is unimodal there).
"""
from mpmath import mp, mpf, log, exp, sqrt

mp.dps = 40
half = mpf(1) / 2
FAIL = []


def check(name, ok, info=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", name, info))
    if not ok:
        FAIL.append(name)


def kl(r, p):
    return r * log(r / p) + (1 - r) * log((1 - r) / (1 - p))


def data(u):
    u = mpf(u)
    pu = 1 / (1 + exp(u))
    a = kl(pu, half)
    f = lambda r: kl(r, pu) + kl(r, half) - a                   # noqa: E731   x + theta(x) - a at the parameter rho
    lo, hi = 1 / (1 + exp(u / 2)), half                          # the minimum of x + theta(x) is at l = u/2
    if f(hi) < 0:                                                # x + theta(x) < a up to eps*: x* = a (theta = 0 there)
        return u, pu, a, None, a, mpf(0)
    for _ in range(140):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    rs = (lo + hi) / 2
    ell = log((1 - rs) / rs)
    return u, pu, a, rs, kl(rs, pu), ell / (u - ell)


def tau2(u):
    u, pu, a, rs, xs, lam = data(u)
    F = lambda r: a * max(a, kl(r, pu) + kl(r, half)) / (a + kl(r, pu))   # noqa: E731
    if rs is None:
        return a * a / (a + xs)
    lo, hi = rs, half
    gr = (sqrt(5) - 1) / 2
    x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
    f1, f2 = F(x1), F(x2)
    for _ in range(220):
        if f1 < f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - gr * (hi - lo)
            f1 = F(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + gr * (hi - lo)
            f2 = F(x2)
    return min(F((lo + hi) / 2), F(rs), F(half))


print("# cube: is tau_2 = a^2/(a + x*)?   40-digit arithmetic")
print("#    u        lambda* = |theta'(x*)|     x*/(a + x*)        a^2/(a + x*) / a          tau_2 / a            closed form")
for us in ("0.5", "1", "2", "4", "4.5", "5", "6", "8", "12"):
    u, pu, a, rs, xs, lam = data(us)
    closed = a * a / (a + xs)
    t2 = tau2(us)
    holds = abs(closed - t2) < mpf(10) ** -25 * a
    print("  %5s   %s   %s   %s   %s   %s" % (us, mp.nstr(lam, 12), mp.nstr(xs / (a + xs), 12), mp.nstr(closed / a, 15), mp.nstr(t2 / a, 15),
                                              "holds" if holds else "FAILS by %s a" % mp.nstr((closed - t2) / a, 4)))
    check("u = %s: the closed form holds iff lambda* <= x*/(a + x*)" % us, holds == (lam <= xs / (a + xs)))


def g(u):
    u, pu, a, rs, xs, lam = data(u)
    return lam - xs / (a + xs)


lo, hi = mpf(4), mpf(5)
for _ in range(110):
    mid = (lo + hi) / 2
    if g(mid) < 0:
        lo = mid
    else:
        hi = mid
u0 = (lo + hi) / 2
u, pu, a, rs, xs, lam = data(u0)
print("  threshold slope u_0 = %s;  there tau_2/a = %s, lambda* = %s" % (mp.nstr(u0, 15), mp.nstr(a / (a + xs), 12), mp.nstr(lam, 10)))
check("u_0 = 4.6535196 (a6_01, double precision: 4.653520)", abs(u0 - mpf("4.65351961849582")) < mpf(10) ** -10)
u, pu, a, rs, xs, lam = data("5")
check("u = 5: tau_2 = 0.602893472 a < a^2/(a + x*) = 0.604053203 a", abs(tau2("5") / a - mpf("0.602893471993")) < mpf(10) ** -10 and abs(a / (a + xs) - mpf("0.604053203153")) < mpf(10) ** -10)
print()
print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
