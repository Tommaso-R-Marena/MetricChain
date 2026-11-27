"""Coordinator's independent check of a finding of workstream R6 (R6_REPORT.md, finding m8): numpy's
Generator.binomial(n, p) is biased for n of order 1e17 and more when the mean n*p is between about 60 and 1e4
(the BTPE branch; the inversion branch, mean <= 30, is not affected).  Own code; a Poisson sampler is the control.
Usage: python3 numpy_binomial_bias_check.py     (seconds)"""
import numpy as np, math
print("numpy", np.__version__)
rng = np.random.default_rng(12345)
N = 400_000
for (n, mean) in [(2**61, 92.0), (10**18, 500.0), (10**17, 500.0), (10**16, 500.0), (10**15, 500.0), (2**61, 20.0), (2**61, 1e5), (10**12, 92.0)]:
    p = mean/n
    x = rng.binomial(n, p, size=N).astype(float)
    m = x.mean(); se = x.std(ddof=1)/math.sqrt(N)
    y = rng.poisson(mean, size=N).astype(float)
    print(f"n={n:.3e} np={mean:g}: binomial mean {m:.4f} (rel. dev. {100*(m-mean)/mean:+.3f} %, z = {(m-mean)/se:+.1f}); "
          f"var/mean {x.var(ddof=1)/mean:.4f}; Poisson control mean {y.mean():.4f} (z = {(y.mean()-mean)/(y.std(ddof=1)/math.sqrt(N)):+.1f})")
