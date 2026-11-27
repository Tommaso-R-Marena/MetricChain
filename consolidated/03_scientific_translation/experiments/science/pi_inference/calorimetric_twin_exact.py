"""Exact version of calorimetric_twin_check.py: overlapping cones, no idealisation.

g'(x) = min( -u (r1 - d(x,a0))_+ , -u (r1 + s - d(x,a'))_+ ),  d(a0,a') = D.
The joint law of (d(x,a0), d(x,a')) for uniform x:  with t = number of the D positions where
a0 != a' at which x agrees with a', and q = number of the n-D common positions at which x
differs from both:  d(x,a0) = t + q,  d(x,a') = D - t + q,  multiplicity C(D,t) C(n-D,q).
Z and U = E_mu[g'] are computed exactly (log-sum-exp over the (t,q) grid).
"""
import math, sys
import numpy as np
from scipy.special import gammaln, logsumexp
from scipy.optimize import brentq

def logbinom(n, d):
    return gammaln(n+1) - gammaln(d+1) - gammaln(n-d+1)

def ZU(n, u, r1, D, R2):
    """log Z (units 2^n) and U for g' with second radius R2 (R2 = None: base instance only)."""
    t = np.arange(D+1)[:, None]; q = np.arange(n-D+1)[None, :]
    lm = logbinom(D, t) + logbinom(n-D, q) - n*math.log(2)
    d0 = t + q; d1 = D - t + q
    depth = u * np.maximum(r1 - d0, 0)
    if R2 is not None:
        depth = np.maximum(depth, u * np.maximum(R2 - d1, 0))
    logZ = logsumexp(lm + depth)
    pos = depth > 0
    U = -math.exp(logsumexp((lm + depth + np.log(np.where(pos, depth, 1.0)))[pos]) - logZ)
    return logZ, U

def study(n, u, rho1, D):
    r1 = round(rho1*n)
    logZ0, U0 = ZU(n, u, r1, D, None)
    f = lambda s: ZU(n, u, r1, D, r1 + s)[1] - U0
    a, b = f(-0.999), f(0.999)
    if a*b > 0:
        return f"n={n} rho1={rho1:.4f} D={D}: no sign change (dU(-1)={a:.3e}, dU(+1)={b:.3e}), ln Z0 = {logZ0:.2f}"
    s = brentq(f, -0.999, 0.999, xtol=1e-13)
    logZ, U = ZU(n, u, r1, D, r1 + s)
    return (f"n={n} rho1={rho1:.4f} D={D}: root s*={s:+.6f}, U'-U0 = {U-U0:+.2e}, ln Z'-ln Z0 = {logZ-logZ0:.4f}, "
            f"ln Z0 = {logZ0:.2f}, U0/n = {U0/n:.4f}")

if __name__ == "__main__":
    u = 1.0; rho0 = math.log(2/(1+math.exp(-u)))/u
    for n in (400, 1000):
        for rho1 in (rho0 + 0.01, rho0 + 0.03):
            for D in (n//2, int(0.45*n), int(0.3*n)):
                print(study(n, u, rho1, D), flush=True)
