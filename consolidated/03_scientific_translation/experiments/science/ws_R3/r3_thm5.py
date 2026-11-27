#!/usr/bin/env python3
"""R3 — sanity check of Theorem 5 (two-sided perturbation bracket) and its sampled form.
beta = 1; cube with uniform mu0; random members g of the class with single-flip bound c = b."""
import math
import numpy as np
from r3_thm2 import random_class_member

rng = np.random.default_rng(5)
worst_id = 0.0; viol = 0; fails = 0; trials = 0; inst = 0
n, delta, Ns = 10, 0.1, 25
for b in (0.3, 1.0, 2.5):
    for _ in range(150):
        g = random_class_member(n, b, rng)
        Nst = 1 << n
        Eg0 = g.mean()
        w = np.exp(-(g - g.min())); mug = w / w.sum()
        U = float(mug @ g)
        lnratio = math.log(w.mean()) - g.min()              # ln(Z_g/Z_0)
        mu0 = np.full(Nst, 1 / Nst)
        kl0g = float(np.sum(mu0 * (np.log(mu0) - np.log(mug)))); klg0 = float(np.sum(mug * (np.log(mug) - np.log(mu0))))
        worst_id = max(worst_id, abs((Eg0 - U) - (kl0g + klg0)))
        viol += not (-Eg0 <= lnratio + 1e-9 and lnratio <= -U + 1e-9)
        inst += 1
        tau = math.sqrt(n * b * b * math.log(1 / delta) / (2 * Ns))
        for rep in range(200):
            xs = rng.integers(0, Nst, size=Ns)
            lower = -(g[xs].mean() + tau)
            fails += lower > lnratio + 1e-12
            trials += 1
print(f"{inst} instances (n={n}): bracket violations {viol}; max |width - J| = {worst_id:.1e}")
print(f"sampled lower end (N={Ns}, delta={delta}): empirical failure rate {fails / trials:.4f} over {trials} trials (must be <= {delta})")
# the corollary at g = 0: N = n b^2 ln(1/delta)/(2 eps^2)
for nn, b, eps in ((1000, 1.0, 0.5), (1000, 1.0, 50.0)):
    print(f"corollary: n={nn}, b={b}, eps={eps}: N = {nn * b * b * math.log(1 / delta) / (2 * eps * eps):.3f} evaluations"
          f"  (extensive accuracy eps = {eps / nn:.3f} n needs less than one sample: a single evaluation suffices)")
