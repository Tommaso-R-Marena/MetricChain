"""t09: hinted lower bound at g = 0 with exact HAMMING balls (1-D sums; n up to 64000).
Dip of depth u(r+1) on B(s,r), s of weight k:   e^{effect} - 1 = sum_{d<=r} P_pi(d(X,s)=d)(e^{u(r+1-d)}-1)
     = e^{u(r+1) - Lam(s)} P_cone(d <= r) - P_pi(d <= r),      Lam(s) = k L1 + (n-k) L0,
where under the cone law d = Bin(k, eta1) + Bin(n-k, eta0).  We use the lower value
     effect >= u(r+1) - Lam(s) + ln P_cone(d <= r) + ln(1 - e^{-(that)})        (P_pi(d<=r) <= 1),
so every reported ball is certified sensitive.  Largest type density of B(s,r): hypergeometric tails.
Exponent: n^{-1} ln(1/maxdens) of the smallest sensitive ball."""
import math, sys, time, numpy as np
from scipy.stats import hypergeom, binom
from flib import *

def cone_logcdf(n, k, st):
    """ln P_cone(d <= r) for all r (accurate where it is not astronomically small)"""
    a = binom.pmf(np.arange(k + 1), k, st.eta1)
    b = binom.pmf(np.arange(n - k + 1), n - k, st.eta0)
    ia = np.nonzero(a > a.max() * 1e-40)[0]; ib = np.nonzero(b > b.max() * 1e-40)[0]
    conv = np.convolve(a[ia[0]:ia[-1] + 1], b[ib[0]:ib[-1] + 1])
    pm = np.zeros(n + 1)
    lo = ia[0] + ib[0]
    pm[lo:lo + len(conv)] = conv
    with np.errstate(divide="ignore"):
        return np.log(np.minimum(np.cumsum(pm), 1.0))

def effect_lower(lc, r, n, k, st):
    x = st.u * (r + 1) - (k * st.L1 + (n - k) * st.L0) + lc[r]
    if x <= 0:
        return 0.0
    return x + math.log1p(-math.exp(-x))

def max_logdens(n, k, r):
    t = np.arange(n + 1)
    imax = np.floor((r - t + k) / 2.0)
    lc = hypergeom.logcdf(imax, n, k, n - t)
    lc = np.where(imax < np.maximum(0, k - t), -np.inf, lc)
    return float(np.nanmax(lc))

p, u, frac = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
st = Site(p, u)
E = max(thr_additive(p, u, g) for g in np.linspace(-u, u, 401))
e1 = frac * E
r0, _ = R_additive(p, u, 0.0, e1)
val, m0, rho0 = hint0_rd(st, e1, nm=200001)
print(f"p={p} u={u} eps1={e1:.6f}: R_0={r0:.6f}, m*={m0:.4f}, rho*={rho0:.4f}")
rows = []
for n in [int(x) for x in sys.argv[4].split(",")]:
    t0 = time.time()
    best = (-1, None, None)
    for dm in (-0.04, -0.02, -0.01, 0.0, 0.01, 0.02, 0.04):
        k = int(round((m0 + dm) * n))
        lc = cone_logcdf(n, k, st)
        lo, hi = 0, n
        while hi - lo > 1:                       # smallest r with effect > eps
            mid = (lo + hi) // 2
            if effect_lower(lc, mid, n, k, st) > e1 * n:
                hi = mid
            else:
                lo = mid
        ex = -max_logdens(n, k, hi) / n
        if ex > best[0]:
            best = (ex, k, hi)
    rows.append((n, best[0]))
    print(f"  n={n}: exponent {best[0]:.6f} (k/n={best[1]/n:.4f}, r/n={best[2]/n:.4f})  excess over R_0: {best[0]-r0:.6f} = {(best[0]-r0)*n/math.log(n):.3f} ln(n)/n   [{time.time()-t0:.1f}s]", flush=True)
