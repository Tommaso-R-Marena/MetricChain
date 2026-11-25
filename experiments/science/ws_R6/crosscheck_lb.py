"""
crosscheck_lb.py -- workstream R6: the two lower bounds of everyn.py recomputed with a different arithmetic (float64 logs, scipy gammaln /
logsumexp) and directly from the definitions (no shared tables): k* = least k with Delta_k > eps; R = least R with D_R > eps.
"""
import sys, json, numpy as np
from scipy.special import gammaln, logsumexp

def lower_bounds(n, u, eps, delta):
    j = np.arange(n + 1)
    lc = gammaln(n + 1) - gammaln(j + 1) - gammaln(n - j + 1)        # ln C(n,j)
    lball = np.logaddexp.accumulate(lc)                               # ln |B(n,r)|
    # hinted: Delta_k = ln(1 + 2^-n sum_{j<=k} C(n,j)(e^{u(k+1-j)} - 1))
    def Delta(k):
        y = u * (k + 1 - j[:k + 1])
        t = lc[:k + 1] + y + np.log1p(-np.exp(-y))                    # ln(e^y - 1) without overflow
        v = logsumexp(t) - n * np.log(2)
        return np.logaddexp(0.0, v)                                    # ln(1 + e^v)
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if Delta(mid) > eps: hi = mid
        else: lo = mid + 1
    kstar = lo
    ln_hint = np.log(1 - 2 * delta) + n * np.log(2) - lball[kstar]
    # non-adaptive: D_R = n ln(1+e^-u) - ln sum_j C(n,j) e^{-u max(j,R)}
    def D(R):
        return n * np.log1p(np.exp(-u)) - logsumexp(lc - u * np.maximum(j, R))
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if D(mid) > eps: hi = mid
        else: lo = mid + 1
    Rmin = lo
    ln_na = np.log(1 - 2 * delta) + n * np.log(2) - (lball[Rmin - 1] if Rmin >= 1 else 0.0)
    return kstar, ln_hint, Rmin, ln_na

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    worst = 0.0
    rows = 0
    for u in (1.0, 2.0, 0.5):
        for l in open(os.path.join(here, "data", "separation_K64_u%g.jsonl" % u)):
            o = json.loads(l)
            ks, lh, Rm, lna = lower_bounds(o["n"], o["u"], o["x_out"], 0.05)
            d1, d2 = abs(lh - o["ln_hint"]), abs(lna - o["ln_na"])
            worst = max(worst, d1, d2)
            rows += 1
            if ks != o["kstar"] or Rm != o["Rmin"] or max(d1, d2) > 1e-6:
                print("MISMATCH", o["n"], o["u"], ks, o["kstar"], Rm, o["Rmin"], d1, d2)
    print("rows compared:", rows, "| largest |difference| of ln(lower bound) between the two computations: %.2e" % worst)
    for (u, n) in [(1.0, 1400), (2.0, 540), (0.5, 4700)]:
        ks, lh, Rm, lna = lower_bounds(n, u, 0.8715438800633535, 0.05)
        print("u=%g n=%d: k*=%d ln LB_hint=%.3f | R=%d (R/n=%.4f, p_u=%.4f) ln LB_na=%.3f" % (u, n, ks, lh, Rm, Rm / n, 1 / (1 + np.exp(u)), lna))
