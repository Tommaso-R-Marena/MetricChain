#!/usr/bin/env python3
"""Scan of the three-round hidden gain Xi_3 (small-slope limit) at theta = h = 1/4 and nearby, including small phi1."""
import numpy as np
from lbr_gauss import xi3, xi2
print("Xi_3(theta = 0.25) for small phi1; rows phi1, columns phi3 (phi2 = 1 - phi1 - phi3)")
p3s = (0.26, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
print("        " + " ".join(f"p3={p:.2f}" for p in p3s))
for p1 in (0.0005, 0.002, 0.01, 0.03, 0.06, 0.1, 0.2):
    row = []
    for p3 in p3s:
        p2 = 1 - p1 - p3
        row.append("   --   " if p2 <= 1e-4 else f"{xi3(0.25, (p1, p2, p3), N=241):+.5f}")
    print(f"p1={p1:.4f} " + " ".join(row))
print("largest theta with Xi_3 > 0 (over a grid of fractions):")
best = (0, None)
for p1 in (0.002, 0.01, 0.03, 0.06, 0.1, 0.15, 0.2, 0.3):
    for p3 in np.linspace(0.2, 0.95, 16):
        p2 = 1 - p1 - p3
        if p2 <= 1e-3:
            continue
        lo, hi = 0.05, min(0.6, p3 * 0.99999)
        if xi3(lo, (p1, p2, p3), N=121) <= 0:
            continue
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            if xi3(mid, (p1, p2, p3), N=121) > 0:
                lo = mid
            else:
                hi = mid
        if lo > best[0]:
            best = (lo, (p1, p2, p3))
print(best)
print("sanity: Xi_3 at theta = 0.1, phi = (0.01, 0.01, 0.98):", xi3(0.1, (0.01, 0.01, 0.98), N=241), " (D(0.1) = 1 - 2 sqrt(0.1) = %.4f)" % (1 - 2 * 0.1 ** 0.5))
