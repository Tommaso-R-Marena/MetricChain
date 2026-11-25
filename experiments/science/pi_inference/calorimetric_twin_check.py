"""Does a mean-energy (calorimetric) oracle lower the worst-case exponent?  (PI thread.)

Cube {0,1}^n, zero known part, residual class: u-Lipschitz in Hamming distance (beta = 1).
Base instance: one visible cone  g0(x) = -u (r1 - d(x,a0))_+  at a known centre a0.
Alternative: g0 plus a hidden cone -u (r1 + s - d(x,a'))_+ at an unknown centre a' whose
support is disjoint from the visible one (idealisation: exact when d(a0,a') >= 2 r1 + 1).
Question: is there s in (-1, 1) with EXACTLY the same mean energy U = E_mu[g] but ln Z larger
by a constant?  If so, an algorithm with an exact U-oracle must still find the hidden cone,
whose support has volume V(n, r1 + 1): the exponent ln 2 - h(rho1) for every rho1 > rho0.

Exact radial sums in log space (mpmath not needed: use logs of binomials).
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp
from scipy.optimize import brentq

def logbinom(n, d):
    return gammaln(n+1) - gammaln(d+1) - gammaln(n-d+1)

def cone_sums(n, u, R):
    """log B and A/B for the cone -u (R - d)_+ :  B = 2^-n sum_d C(n,d) (e^{u(R-d)} - 1),
       A = -2^-n sum_d C(n,d) u (R-d) e^{u(R-d)}   (energy g = -u(R-d), weight e^{-g})."""
    d = np.arange(0, math.ceil(R))            # d < R
    depth = u * (R - d)
    lb = logbinom(n, d) - n*math.log(2)
    logB = logsumexp(lb + depth + np.log1p(-np.exp(-depth)))
    logAneg = logsumexp(lb + np.log(depth) + depth)
    return logB, -math.exp(logAneg - logB)     # (log B, m = A/B)

def study(n, u, rho1):
    r1 = round(rho1 * n)
    logB0, m0 = cone_sums(n, u, r1)
    # base: Z0 = 1 + B0 (in units of 2^n), U0 = A0 / (1 + B0)
    logZ0 = np.logaddexp(0.0, logB0)
    U0 = m0 * math.exp(logB0 - logZ0)
    def dU(s):
        logB, m = cone_sums(n, u, r1 + s)
        logZ = np.logaddexp(logZ0, logB)
        U = (U0 * math.exp(logZ0 - logZ) + m * math.exp(logB - logZ))
        return U - U0
    a, b = dU(-0.999), dU(0.999)
    if a * b > 0:
        return dict(n=n, rho1=rho1, root=None, dU_minus=a, dU_plus=b, logB0=logB0)
    s = brentq(dU, -0.999, 0.999, xtol=1e-13)
    logB, m = cone_sums(n, u, r1 + s)
    dlnZ = np.logaddexp(logZ0, logB) - logZ0
    hb = lambda x: -x*math.log(x) - (1-x)*math.log(1-x)
    return dict(n=n, rho1=rho1, r1=r1, root=s, dlnZ=dlnZ, logB0_per_n=logB0/n, U0_per_n=U0/n,
                exponent=math.log(2) - hb((r1+1)/n))

if __name__ == "__main__":
    u = 1.0
    rho0 = math.log(2/(1+math.exp(-u)))/u
    hb = lambda x: -x*math.log(x) - (1-x)*math.log(1-x)
    print(f"u = {u}: rho0 = {rho0:.5f}, hinted exponent at bounded accuracy ln2 - h(rho0) = {math.log(2)-hb(rho0):.5f}")
    for n in (200, 1000, 5000):
        for rho1 in (rho0 + 0.002, rho0 + 0.01, rho0 + 0.03, 0.45):
            r = study(n, u, rho1)
            if r["root"] is None:
                print(f"n={n:5d} rho1={rho1:.4f}: no sign change  dU(-1)={r['dU_minus']:.3e} dU(+1)={r['dU_plus']:.3e}  log B0 = {r['logB0']:.2f}")
            else:
                print(f"n={n:5d} rho1={rho1:.4f} (r1={r['r1']}): root s*={r['root']:+.6f}  ln Z'-ln Z0 = {r['dlnZ']:.4f}  "
                      f"ln B0/n = {r['logB0_per_n']:+.4f}  U0/n = {r['U0_per_n']:.4f}  cost exponent ln2-h((r1+1)/n) = {r['exponent']:.5f}")
