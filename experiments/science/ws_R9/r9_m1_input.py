#!/usr/bin/env python3
"""R9, sampled minor finding m1 of SCI-REV-0001 as rewritten in Lemma 11.89: in the capacity-achieving joint law of an
asymmetric binary channel written as an Ising pair P(b,x) ∝ exp(J b x + h1 b + h2 x), the optimal input field satisfies
-h2 < h1 < 0 (for h2 > 0), and the input DISTRIBUTION has mu = E B > 0 ('in every case computed [N]').  Own check."""
import math
import numpy as np
from scipy.optimize import minimize_scalar
rng = np.random.default_rng(2)
def MIv(J, h1, h2):
    w = np.array([[math.exp(J * b * x + h1 * b + h2 * x) for x in (1, -1)] for b in (1, -1)])
    Pm = w / w.sum()
    pb, px = Pm.sum(1), Pm.sum(0)
    return float((Pm * np.log(Pm / np.outer(pb, px))).sum()), float(pb[0] - pb[1])
bad_field = bad_mu = 0; minmu = 1.0; n = 0
for _ in range(3000):
    J = 10 ** rng.uniform(-1.5, 0.7); h2 = 10 ** rng.uniform(-2, 0.7)
    r = minimize_scalar(lambda h1: -MIv(J, h1, h2)[0], bounds=(-h2 - 5, 5), method="bounded", options={"xatol": 1e-12})
    h1 = r.x
    I, mu = MIv(J, h1, h2)
    n += 1
    if not (-h2 < h1 < 0): bad_field += 1
    if not mu > 0: bad_mu += 1
    minmu = min(minmu, mu)
print(f"{n} random (J, h2 > 0): optimal input field outside (-h2, 0): {bad_field};  mu = E B <= 0: {bad_mu};  smallest mu: {minmu:.3e}")
