"""Common helpers for the adversarial review of HIERARCHY_REPORT.md.

Written from scratch by the reviewer; nothing is imported from the author's scripts.
All binomial costs are exact: t_j(d) = ln C(n_j, floor(n_j/2)) - ln C(n_j, d) is computed from
exact integer binomial coefficients (math.comb) and math.log of Python integers.
"""
import math
import numpy as np


def fKL(r):
    """f(r) = KL(r || 1/2), natural logarithm, r in [0, 1]."""
    if r <= 0.0 or r >= 1.0:
        return math.log(2.0)
    return r * math.log(2.0 * r) + (1.0 - r) * math.log(2.0 * (1.0 - r))


def consts(u):
    pu = 1.0 / (1.0 + math.exp(u))
    Lam = math.log(2.0 / (1.0 + math.exp(-u)))
    kap = Lam / u
    a = fKL(pu)
    h = fKL(kap)
    Nu = math.ceil(5.0 / (1.0 - 2.0 * kap))
    return dict(u=u, pu=pu, Lam=Lam, kap=kap, a=a, h=h, Nu=Nu)


def kKL(r, u):
    """k(r) = KL(r || p_u) = f(r) + u r - Lambda_1."""
    Lam = math.log(2.0 / (1.0 + math.exp(-u)))
    return fKL(r) + u * r - Lam


def finv(theta):
    """inverse of f on [0, 1/2] (f is decreasing there); theta in [0, ln 2]."""
    if theta >= math.log(2.0):
        return 0.0
    if theta <= 0.0:
        return 0.5
    lo, hi = 0.0, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if fKL(mid) > theta:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


_tcache = {}


def tcost(n):
    """exact t(d) = ln C(n, n//2) - ln C(n, d), d = 0..n, as a float64 array."""
    if n not in _tcache:
        c = [math.comb(n, d) for d in range(n + 1)]
        lm = math.log(c[n // 2])
        _tcache[n] = np.array([lm - math.log(x) for x in c], dtype=np.float64)
    return _tcache[n]


def lnPmode(n):
    """ln P(mode) for Bin(n, 1/2)."""
    return math.log(math.comb(n, n // 2)) - n * math.log(2.0)
