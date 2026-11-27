#!/usr/bin/env python3
"""Coordinator check of referee R9's finding m4 (product samplers with a field), with own code.

A non-adaptive algorithm whose points are i.i.d. from Bernoulli(r)^n cannot distinguish the cone u*d(., s) around a
constant centre s (all zeros or all ones) from its truncation u*max(d(., s), rho*n) unless a point falls into the ball
of radius rho*n, whose sampler measure is e^{-n KL(rho || r_s)}; the two instances differ by x*n in ln A when
KL(rho || eta_s) = x, rho > eta_s (eta_s = Gibbs mean distance of the cone).  Hence the exponent of such a sampler is at
least max(phi_0, phi_1), phi_s(x) = KL(rho_s(x) || r_s)  [= min{KL(y || r_s) : KL(y || eta_s) <= x}].
Here: (1) the tilt identity u*rho + KL(rho||p_s) = Lambda_s + KL(rho||eta_s) that makes the two instances differ by x*n;
(2) the exact finite-n version (binomial sums) of the lower bound at n = 2000; (3) the referee's corrected table
against theta_na from the pair formula."""
import math, sys, os
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln, logsumexp

T = np.linspace(1e-4, 1.0, 4001)


def Fstar(p, u, ngam=1601):
    """F*(t) = max over |gamma| <= u of the closed-form game function (theory report, Theorem 11.59(b)) on the grid T"""
    q = 1 - p
    L0 = -math.log(q + p * math.exp(-u)); L1 = -math.log(p + q * math.exp(-u))
    gam = np.linspace(-u * (1 - 1e-9), u * (1 - 1e-9), ngam)
    G, TT = np.meshgrid(gam, T, indexing="ij")
    Fv = (-TT * np.log(q + p * np.exp(-G)) + np.log((1 - np.exp(-TT * (u + G))) * np.exp(-TT * L0)
          + (1 - np.exp(-TT * (u - G))) * np.exp(-TT * (L1 + G))) - np.log(1 - np.exp(-2 * TT * u)))
    return Fv.max(axis=0)


def Rfun(Fv, e):
    return max(0.0, float((Fv - T * e).max()))


def theta_from_pair(Fv, x):
    lo, hi = -5.0, 5.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if mid + Rfun(Fv, mid) < x:
            lo = mid
        else:
            hi = mid
    return Rfun(Fv, hi)


def kl(x, y):
    x = min(max(x, 1e-300), 1 - 1e-16)
    return x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))


def consts(p, u):
    q = 1 - p
    # centre s = 0: a point differs from the centre where x_i = 1: prior probability p, Gibbs eta_0 = p e^-u / (q + p e^-u)
    # centre s = 1: differs where x_i = 0: prior q, Gibbs eta_1 = q e^-u / (p + q e^-u)
    lam0 = -math.log(q + p * math.exp(-u)); lam1 = -math.log(p + q * math.exp(-u))
    eta0 = p * math.exp(-u) / (q + p * math.exp(-u)); eta1 = q * math.exp(-u) / (p + q * math.exp(-u))
    return (p, eta0, lam0), (q, eta1, lam1)


def phi(prior_r, eta, x):
    """KL(rho || prior_r) with rho in (eta, prior_r) solving KL(rho || eta) = x (0 if the ball already has full measure)"""
    if prior_r <= eta or kl(prior_r, eta) <= x:
        return 0.0
    rho = brentq(lambda y: kl(y, eta) - x, eta, prior_r)
    return kl(rho, prior_r)


def sampler_exponent(p, u, r, x):
    (p0, eta0, _), (p1, eta1, _) = consts(p, u)
    return max(phi(r, eta0, x), phi(1 - r, eta1, x))


def main():
    # (1) tilt identity
    worst = 0
    rng = np.random.default_rng(3)
    for _ in range(2000):
        p = rng.uniform(.02, .98); u = rng.uniform(.2, 5); rho = rng.uniform(.001, .999)
        for (ps, eta, lam) in consts(p, u):
            worst = max(worst, abs(u * rho + kl(rho, ps) - lam - kl(rho, eta)))
    print(f"(1) tilt identity  u rho + KL(rho||p_s) = Lambda_s + KL(rho||eta_s): max error {worst:.1e}")
    assert worst < 1e-12
    # (3) table
    print("(3) exponents at accuracy x (per site): theta_na | best single r | plain pi   [referee: .1033 (r=.185) .2743; .0451 (r=.170) .1430; .0244 (r=.319) .0348]")
    for (p, u, frac) in [(0.1, 2.0, 0.05), (0.1, 2.0, 0.25), (0.3, 1.0, 0.25)]:
        Fv = Fstar(p, u)
        E = float((Fv / T).max())
        x = frac * E
        th = theta_from_pair(Fv, x)
        rs = np.linspace(0.01, 0.6, 1181)
        vals = [sampler_exponent(p, u, r, x) for r in rs]
        i = int(np.argmin(vals))
        plain = sampler_exponent(p, u, p, x)
        print(f"   p={p}, u={u}, x={frac}E={x:.5f}: theta_na = {th:.4f} | best r = {rs[i]:.3f}: {vals[i]:.4f} | plain pi: {plain:.4f}"
              f"   (best single r exceeds theta_na by {100 * (vals[i] / th - 1):.1f} %)")
        assert vals[i] > th
    # (2) exact finite-n lower bound for plain pi at p=0.1,u=2, x = 0.05E, centre 0^n, n = 2000
    p, u = 0.1, 2.0
    Fv = Fstar(p, u); E = float((Fv / T).max()); x = 0.05 * E
    n = 2000
    k = np.arange(n + 1)
    lb = gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)
    best = None
    for (name, ps) in (("0^n", p), ("1^n", 1 - p)):
        lpi = lb + k * math.log(ps) + (n - k) * math.log(1 - ps)            # law of the distance to the centre under pi
        lnA = logsumexp(lpi - u * k)
        for r in range(1, n):
            lnA_tr = logsumexp(lpi - u * np.maximum(k, r))
            if lnA - lnA_tr > x * n:                                       # the two instances differ by more than x n
                qball = logsumexp(lpi[:r])                                 # they differ on the ball d < r only
                ex = -qball / n
                if best is None or ex > best[0]:
                    best = (ex, name, r)
                break
    print(f"(2) exact, n={n}, p={p}, u={u}, x=0.05E: plain Monte Carlo from pi needs at least (1-2 delta) e^(n*{best[0]:.4f}) points "
          f"(centre {best[1]}, radius {best[2]}); single-letter value {sampler_exponent(p, u, p, x):.4f}")
    print("R9 m4 CHECK OK")


if __name__ == "__main__":
    main()
