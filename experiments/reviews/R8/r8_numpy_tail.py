#!/usr/bin/env python3
"""Referee R8 -- numpy's samplers in the far tail (the remark of the report's section 6.8).
(1) binomial(2^59, p) for tiny p with the Generator API and with the legacy RandomState API;
(2) multinomial(2^59, shells of Q_300): lower-tail and upper-tail shells against their exact expectations."""
import math
import numpy as np

print("numpy", np.__version__)
N = 1 << 59
g = np.random.default_rng(3)
rs = np.random.RandomState(3)
print("binomial(2^59, p): expected mean | Generator.binomial | legacy RandomState.binomial   (4000 draws each)")
for p in (1e-15, 1e-16, 9e-17, 3e-17, 1e-17, 1e-18, 1e-19, 1e-20):
    x = g.binomial(N, p, size=4000)
    y = rs.binomial(N, p, size=4000)
    print("  p = %-7g  %10.4g | %10.4g | %10.4g" % (p, N * p, x.mean(), y.mean()))
m = 300
C = [math.comb(m, j) for j in range(m + 1)]
pv = np.array([c / 2.0 ** m for c in C])
z = g.multinomial(N, pv, size=300)
print("Generator.multinomial(2^59, shells of Q_300), 300 draws: shell, expected count, observed mean")
for d in (75, 78, 81, 84, 216, 219, 222, 225):
    print("  %3d  %10.4g  %10.4g" % (d, N * pv[d], z[:, d].mean()))
print("  sum over shells >= 216: expected %.5g, observed %.5g" % (N * pv[216:].sum(), z[:, 216:].sum(axis=1).mean()))
