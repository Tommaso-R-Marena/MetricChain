"""R8 shared helpers (own code).  Units beta = 1; the class is |g(x)-g(y)| <= u d_H(x,y) on {0,1}^n."""
import math
import numpy as np
from scipy.special import gammaln, logsumexp

LN2 = math.log(2.0)


def hb(p):
    """binary entropy (nats), scalar"""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1 - p) * math.log1p(-p)


def hinv(s):
    """inverse of the binary entropy on [0, 1/2]"""
    if s >= LN2:
        return 0.5
    lo, hi = 0.0, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if hb(mid) < s:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def sig(u):
    return 1.0 / (1.0 + math.exp(u))


def rho0(u):
    return math.log(2.0 / (1.0 + math.exp(-u))) / u


def a_of(u):
    return LN2 - hb(sig(u))


def sigma2(u, eps1):
    return hinv(hb(sig(u)) + eps1)


def theta_hint(u, eps1):
    r = rho0(u) + eps1 / u
    return LN2 - hb(r) if r < 0.5 else 0.0


def theta_pl(u, eps1, rho1=None):
    """plateau-twin exponent  ln2 - h(rho1 - sigma_u + sigma2(eps1))  (rho1 = rho0 by default)"""
    r1 = rho0(u) if rho1 is None else rho1
    r = r1 - sig(u) + sigma2(u, eps1)
    return LN2 - hb(r) if r < 0.5 else 0.0


def eps1c(u):
    return hb(0.5 - rho0(u) + sig(u)) - hb(sig(u))


def lnC(n):
    """array of ln C(n,k), k = 0..n"""
    k = np.arange(n + 1)
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def ln_ball(n, r, lc=None):
    """ln |B(n,r)| = ln sum_{k<=r} C(n,k);  r may be -1 (empty: -inf)"""
    if r < 0:
        return -np.inf
    if lc is None:
        lc = lnC(n)
    r = min(int(r), n)
    return float(logsumexp(lc[: r + 1]))


def ln_ball_table(n):
    lc = lnC(n)
    return np.logaddexp.accumulate(lc)


def basin_stats(n, u, r1):
    """visible basin g0 = -u (r1 - d)_+ on a flat background: ln Z0, U0, S0 (exact radial sums)."""
    lc = lnC(n)
    d = np.arange(n + 1)
    g = -u * np.maximum(r1 - d, 0)
    lw = lc - g
    lnZ = float(logsumexp(lw))
    p = np.exp(lw - lnZ)
    U = float((p * g).sum())
    return lnZ, U, lnZ + U


def radial_stats(n, g):
    """exact ln Z, U, S for a radial function given by its values g[d], d = 0..n"""
    lc = lnC(n)
    lw = lc - g
    lnZ = float(logsumexp(lw))
    p = np.exp(lw - lnZ)
    U = float((p * g).sum())
    return lnZ, U, lnZ + U
