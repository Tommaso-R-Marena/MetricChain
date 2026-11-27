#!/usr/bin/env python3
"""Conditional covering exponent (Proposition U6): a target ball B(s, kappa n) whose centre s is uniform on the sphere
of radius sigma n around a known point x_1.  A query at distance t n from x_1 hits with probability
    count(t)/C(n, sigma n),   count(t) = sum_{i >= (t+sigma-kappa) n/2} C(tn, i) C((1-t)n, sigma n - i).
Exact evaluation of  min_t ln(C(n, sigma n)/count(t))  against the lower bound ln(C(n, sigma n)/|B(n, kappa n)|) and
the exponent n (h(sigma) - h(kappa)) = n (KL(kappa||1/2) - KL(sigma||1/2)); best t against (sigma-kappa)/(1-2 kappa).
usage: cond_cover.py
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp


def lC(n, k):
    k = np.asarray(k, dtype=float)
    return np.where((k >= 0) & (k <= n), gammaln(n + 1) - gammaln(np.clip(k, 0, n) + 1) - gammaln(n - np.clip(k, 0, n) + 1), -np.inf)


def H(x):
    return -x * math.log(x) - (1 - x) * math.log(1 - x) if 0 < x < 1 else 0.0


for (sig, kap) in ((0.5, 0.2), (0.4, 0.2), (0.3, 0.1), (0.45, 0.38), (0.35, 0.27), (0.2, 0.2), (0.15, 0.25)):
    for n in (200, 800, 3200):
        S, K = round(sig * n), round(kap * n)
        best = (1e18, None)
        for T in range(0, n + 1):
            i = np.arange(max(0, math.ceil((T + S - K) / 2)), min(T, S) + 1)
            if len(i) == 0:
                continue
            cnt = logsumexp(lC(T, i) + lC(n - T, S - i))
            cost = float(lC(n, S) - cnt)
            if cost < best[0]:
                best = (cost, T)
        lower = float(lC(n, S) - logsumexp(lC(n, np.arange(0, K + 1))))
        pred = max(0.0, H(S / n) - H(K / n))
        tstar = max(0.0, (sig - kap) / (1 - 2 * kap)) if kap < 0.5 else 0.0
        print(f"sigma={sig} kappa={kap} n={n}: min_t cost/n = {best[0]/n:.5f} at t={best[1]/n:.3f} (predicted t* = {tstar:.3f}); "
              f"counting lower bound/n = {max(lower,0)/n:.5f}; h(sigma)-h(kappa) = {pred:.5f}")
