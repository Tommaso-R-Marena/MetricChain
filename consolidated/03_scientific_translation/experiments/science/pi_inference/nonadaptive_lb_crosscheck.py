"""Coordinator's independent computation of one column of workstream R6's separation table (R6_REPORT.md,
Corollary R6.2): the non-adaptive lower bound of theory report Theorem 11.45(b) at a bounded accuracy,

    LB_na = (1 - 2 delta) 2^n / |B(n, R-1)|,   R = least radius such that flattening the cone u*d(x,b) below R
                                                lowers ln Z by more than x_out,

and the hinted lower bound of Theorem 11.25(a), (1 - 2 delta) 2^n/|B(n,k)| with k the least radius whose dip
(depth u(k+1), supported on B(n,k)) raises ln Z of the zero function by more than x_out.
Own code (log-sum-exp over binomial coefficients); nothing imported from experiments/science/ws_R6.

Usage: python3 nonadaptive_lb_crosscheck.py      (seconds)
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp

def lb(n, u, x_out, delta):
    j = np.arange(0, n + 1); lc = gammaln(n + 1) - gammaln(j + 1) - gammaln(n - j + 1)
    lZcone = n*math.log1p(math.exp(-u))
    R_na = None
    for R in range(0, n + 1):
        lZflat = logsumexp(lc - u*np.maximum(j, R))
        if lZcone - lZflat > x_out: R_na = R; break
    ln_na = math.log(1 - 2*delta) + n*math.log(2) - logsumexp(lc[:R_na])            # |B(n, R-1)|
    k_h = None
    for k in range(0, n + 1):
        # Delta_k = ln(1 + 2^-n sum_{j<=k} C(n,j)(e^{u(k+1-j)} - 1))
        a = u*(k + 1 - j[:k + 1])                                                    # ln(e^a - 1) = a + ln(1 - e^-a), no overflow
        le = logsumexp(lc[:k + 1] + a + np.log1p(-np.exp(-a))) - n*math.log(2)
        if (le if le > 700 else math.log1p(math.exp(le))) > x_out: k_h = k; break
    ln_h = math.log(1 - 2*delta) + n*math.log(2) - logsumexp(lc[:k_h + 1])           # |B(n, k)|
    return R_na, ln_na, k_h, ln_h

if __name__ == "__main__":
    for (u, n) in [(1.0, 1000), (1.0, 1350), (1.0, 1400), (2.0, 540), (0.5, 4700)]:
        R, ln_na, k, ln_h = lb(n, u, 0.872, 0.05)
        print(f"u={u} n={n}: R={R}  ln LB_na = {ln_na:.1f}   |  hinted: k={k}  ln LB_hint = {ln_h:.1f}")
