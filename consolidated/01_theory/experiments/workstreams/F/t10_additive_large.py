"""t10: hinted lower bound at the additive instance gamma|x| with exact SLACK balls (1-D sums; n up to 64000).
Class: field p, constant u; instance residual gamma|x| (|gamma| <= u); slack to the centre s (weight k):
    s_gamma(x, s) = u d(x,s) + gamma(|s| - |x|) = (u+gamma) i + (u-gamma) j,   i = #(1->0), j = #(0->1).
Dip h = (c - s_gamma(., s))_+ : admissible, supported on D_c = {s_gamma(., s) < c}, and
    E_{pi_gamma} e^h >= e^{c - Lam_gamma(s)} P_cone(s_gamma < c),   Lam_gamma(s) = k L1 + (n-k) L0 + gamma k + n ln Z_gamma
(the tilted law is the cone law pi_s for every gamma).  Largest type density of D_c: hypergeometric tails.
Reported: n^{-1} ln(1/maxdens) of the smallest certified-sensitive slack ball, against R_gamma(eps1).
usage: python3 t10_additive_large.py p u frac n1,n2,... [both|star|zero]"""
import math, sys, time, numpy as np
from scipy.stats import hypergeom, binom
from flib import *

def cone_prob_below(n, k, st, gam, c):
    """P_cone( (u+gam) i + (u-gam) j < c ),  i ~ Bin(k, eta1), j ~ Bin(n-k, eta0)"""
    u = st.u
    mi, si = k * st.eta1, math.sqrt(k * st.eta1 * (1 - st.eta1)) + 1
    ii = np.arange(max(0, int(mi - 45 * si)), min(k, int(mi + 45 * si)) + 1)
    pi_ = binom.pmf(ii, k, st.eta1)
    # j < (c - (u+gam) i)/(u-gam)
    jmax = np.ceil((c - (u + gam) * ii) / (u - gam) - 1e-12) - 1          # largest integer strictly below
    cj = binom.cdf(jmax, n - k, st.eta0)
    cj = np.where(jmax < 0, 0.0, cj)
    return float((pi_ * cj).sum())

def max_logdens(n, k, st, gam, c):
    u = st.u
    t = np.arange(n + 1)
    imax = np.ceil((c - (u - gam) * (t - k)) / (2 * u) - 1e-12) - 1       # i < [c - (u-gam)(t-k)]/(2u)
    lc = hypergeom.logcdf(imax, n, k, n - t)
    lc = np.where(imax < np.maximum(0, k - t), -np.inf, lc)
    return float(np.nanmax(lc))

p, u, frac = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
st = Site(p, u)
E = max(thr_additive(p, u, g) for g in np.linspace(-u, u, 401))
e1 = frac * E
r0, _ = R_additive(p, u, 0.0, e1)
rmax, gstar = R_max(p, u, e1, ngam=41, nt=401)
aH = maxmin_precise(st, "H", e1)
mstar = aH[1]
print(f"p={p} u={u} eps1={e1:.6f}: R_0={r0:.6f}; hardest additive instance gamma*={gstar:+.5f}: R={rmax:.6f}, centre type m*={mstar:.4f}")
which = sys.argv[5] if len(sys.argv) > 5 else "both"
cases = []
if which in ("both", "star"):
    cases.append((gstar, rmax, "gamma*"))
if which in ("both", "zero"):
    cases.append((0.0, r0, "gamma=0 (slack ball = Hamming ball)"))
for gam, target, label in cases:
    print(" instance", label)
    mm = mstar if gam != 0.0 else hint0_rd(st, e1, nm=200001)[1]
    for n in [int(x) for x in sys.argv[4].split(",")]:
        t0 = time.time()
        best = (-1, None, None)
        lnZ = math.log(st.q + st.p * math.exp(-gam))
        for dm in (-0.04, -0.02, -0.01, 0.0, 0.01, 0.02, 0.04):
            k = int(round((mm + dm) * n))
            Lam = k * st.L1 + (n - k) * st.L0 + gam * k + n * lnZ
            def sens(c):
                pr = cone_prob_below(n, k, st, gam, c)
                if pr <= 0: return False
                x = c - Lam + math.log(pr)
                return x > 0 and x + math.log1p(-math.exp(-x)) > e1 * n
            lo, hi = 0.0, 2 * u * n
            while hi - lo > 1e-3:
                mid = (lo + hi) / 2
                if sens(mid): hi = mid
                else: lo = mid
            ex = -max_logdens(n, k, st, gam, hi) / n
            if ex > best[0]:
                best = (ex, k, hi)
        print(f"  n={n}: exponent {best[0]:.6f} (k/n={best[1]/n:.4f}, c/n={best[2]/n:.4f})  excess over the formula: {best[0]-target:.6f} = {(best[0]-target)*n/math.log(n):.3f} ln(n)/n   [{time.time()-t0:.1f}s]", flush=True)
