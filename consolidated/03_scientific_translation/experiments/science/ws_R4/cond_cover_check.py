#!/usr/bin/env python3
"""R4 -- Proposition 11.88(a) (conditional covering) by exact counting; own code.

Target: ball B(s, K), centre s uniform on the sphere of radius S around a known point x1.
 dual  : every point hits with probability <= |B(n,K)|/C(n,S)  ->  cost >= C(n,S)/|B(n,K)|
 primal: a point x at distance t from x1 hits for exactly
           hits(t) = sum_{i >= (t+S-K)/2} C(t,i) C(n-t,S-i)   centres (i = |T cap S-set|, d(x,s) = t+S-2i <= K)
         so points uniform on the best sphere cost C(n,S)/max_t hits(t).
 claim : both exponents -> f(kappa) - f(sigma) = H(sigma) - H(kappa)   (kappa < sigma <= 1/2).
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp


def lc(n, k):
    k = np.asarray(k, dtype=float)
    out = gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)
    return np.where((k < 0) | (k > n), -np.inf, out)


def H(x):
    return -x * math.log(x) - (1 - x) * math.log(1 - x)


print("# sigma kappa   n     dual/n     primal/n (best t/n; t*=(s-k)/(1-2k))   H(sigma)-H(kappa)")
for (sig, kap) in [(0.45, 0.38), (0.5, 0.3), (0.4, 0.2), (0.3, 0.27), (0.5, 0.45), (0.35, 0.1), (0.3, 0.4)]:
    for n in (200, 800, 3200):
        S, K = int(round(sig * n)), int(round(kap * n))
        lnball = float(logsumexp(lc(n, np.arange(K + 1))))
        dual = (float(lc(n, S)) - lnball) / n
        best = (-np.inf, None)
        for t in range(0, n + 1):
            imin = max(0, math.ceil((t + S - K) / 2), S - (n - t))
            imax = min(t, S)
            if imin > imax:
                continue
            i = np.arange(imin, imax + 1)
            lh = float(logsumexp(lc(t, i) + lc(n - t, S - i)))
            if lh > best[0]:
                best = (lh, t)
        primal = (float(lc(n, S)) - best[0]) / n
        tstar = (sig - kap) / (1 - 2 * kap) if sig > kap else 0.0
        print(f"{sig:.2f} {kap:.2f} {n:5d}  {max(dual,0):.5f}   {max(primal,0):.5f} ({best[1]/n:.3f}; {tstar:.3f})"
              f"      {max(H(sig)-H(kap),0):.5f}")
