"""
numpy_binomial_bias.py -- workstream R6: a numerical trap found while testing my own sampler (test_binomial.py).
numpy's Generator.binomial(n, p) at very large n (>= 1e17) and moderate mean n p (about 60 .. 1e4, the BTPE branch) returns samples
whose mean is too small by up to about 1 %.  Reference: the exact mean n p; a Poisson sample of the same mean (for p <= 1e-13 the
binomial law is within total variation p of the Poisson law); and sums of binomials with n <= 1e15 (which show no bias).
"""
import math, sys
import numpy as np
print("numpy", np.__version__)
N = 400000
for seed in (1, 2):
    rng = np.random.default_rng(seed)
    print("seed", seed, "; N =", N, "draws; z = (mean - n p)/sqrt(n p/N)")
    for mu in (20.0, 31.0, 60.0, 92.2337, 500.0, 4611.686, 50000.0):
        row = []
        for n in (10 ** 15, 10 ** 16, 10 ** 17, 10 ** 18, 2 ** 61):
            x = rng.binomial(n, mu / n, size=N)
            row.append("%+6.1f (%+.2f%%)" % ((x.mean() - mu) / math.sqrt(mu / N), 100 * (x.mean() / mu - 1)))
        y = rng.poisson(mu, size=N)
        # the same law as a sum of 1024 binomials with n/1024 trials each (n = 2^61): no bias expected if the pieces are unbiased
        parts = rng.binomial(2 ** 51, mu / 2 ** 61, size=(N // 100, 1024)).sum(axis=1)
        zs = (parts.mean() - mu) / math.sqrt(mu / (N // 100))
        print("  n p = %9.3f | n = 1e15, 1e16, 1e17, 1e18, 2^61: %s | Poisson: %+5.1f | 1024 pieces of 2^51 trials: %+5.1f" % (
            mu, "  ".join(row), (y.mean() - mu) / math.sqrt(mu / N), zs))
