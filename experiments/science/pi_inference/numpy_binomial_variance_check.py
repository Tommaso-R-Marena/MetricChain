#!/usr/bin/env python3
"""Coordinator's check after ENG-RES-0013 section 1.1 (the engineering division measured the defect of numpy's binomial
sampler from n = 1e15 on, in the VARIANCE before the mean; our SCI-REV-0007 said "nothing detected at n <= 1e16" from a
test of the mean, and our own guard in ws_R6/r6lib.py switches to a Poisson draw only for n > 2^50 = 1.126e15).
Question: is there a window below 2^50 in which numpy's sampler is already defective here?
Mean and variance of Generator.binomial(n, mean/n) against the exact values (mean, mean(1 - p)); z-scores.
Run:  python3 numpy_binomial_variance_check.py > numpy_binomial_variance_check.log    (about a minute)
"""
import math, time
import numpy as np
t0 = time.time(); N = 4_000_000
rng = np.random.default_rng(20261126)
print(f"numpy {np.__version__}; {N} draws per cell; z-score of the sample mean / of the sample variance (|z| > 5 marked)")
ns = [10**14, 2 * 10**14, 5 * 10**14, 7 * 10**14, 9 * 10**14, 10**15, 2**50 - 1, 2**50, 2**50 + 1, 3 * 10**15, 2**52, 2**53, 2**53 + 1, 10**16]
means = [29, 60, 92, 500, 5000]
print("| n | " + " | ".join(f"mean {m}" for m in means) + " |"); bad = []
for n in ns:
    cells = []
    for m in means:
        p = m / n
        x = rng.binomial(n, p, size=N).astype(float)
        var = m * (1 - p)
        zm = (x.mean() - m) / math.sqrt(var / N)
        # variance of the sample variance of a binomial ~ (mu4 - var^2)/N, mu4 = var(1 + 3 var - 6 p(1-p))... use the normal/Poisson form var^2 (2 + 1/var)/N
        zv = (x.var(ddof=1) - var) / math.sqrt(var * var * (2.0 + 1.0 / var) / N)
        flag = " **" if max(abs(zm), abs(zv)) > 5 else ""
        cells.append(f"{zm:+.1f} / {zv:+.1f}{flag}")
        if flag: bad.append((n, m, zm, zv, x.var(ddof=1) / var - 1))
    print(f"| {n:.4g} | " + " | ".join(cells) + " |", flush=True)
print("cells with |z| > 5 (n, mean, z of mean, z of variance, relative error of the variance):")
for b in bad: print(f"   n = {b[0]:.6g} (2^{math.log2(b[0]):.3f}), mean {b[1]}: {b[2]:+.1f}, {b[3]:+.1f}, {100 * b[4]:+.2f} %")
print(f"smallest n with a marked cell: {min((b[0] for b in bad), default=None)}; 2^50 = {2**50}")
print(f"ALL DONE {time.time() - t0:.0f} s")
