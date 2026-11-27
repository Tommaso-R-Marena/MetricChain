#!/usr/bin/env python3
"""R3 — guarded adversarial search for the one-sided divergences in Theorem 7(v):
maximise KL(mu|nu) and KL(nu|mu) over (mu0, Phi, r) at fixed omega = osc(r) (beta = 1).
Instances in which nu or mu underflows (min < 1e-200) or the moments are not matched to 1e-9
are rejected: in r3_thm7.py one unguarded run returned KL = inf through underflow of nu, which
is a floating-point artefact (KL(mu|nu) <= J <= omega tanh(omega/4) is a theorem)."""
import math, warnings
import numpy as np
from scipy.optimize import minimize
from r3_thm7 import instance
warnings.filterwarnings("ignore")
rng = np.random.default_rng(7)
for om in (2.0, 8.0):
    best = {"klmn": 0.0, "klnm": 0.0, "tv": 0.0, "J": 0.0}
    for N, K in ((2, 0), (3, 1), (4, 2)):
        for restart in range(4):
            def unpack(z):
                a = z[:N]; mu0 = np.exp(a - a.max()); mu0 /= mu0.sum()
                Phi = np.tanh(z[N:N + K * N]).reshape(K, N) * 3
                rr = 1 / (1 + np.exp(-z[N + K * N:]))
                r = (rr - rr.min()) / max(rr.max() - rr.min(), 1e-12) * om
                return mu0, Phi, r
            def neg(z, which):
                mu0, Phi, r = unpack(z)
                if mu0.min() < 1e-9:
                    return 0.0
                o = instance(mu0, Phi, r)
                if o["res"] > 1e-9 or o["nu"].min() < 1e-200 or o["mu"].min() < 1e-200 or not np.isfinite(o[which]):
                    return 0.0
                if abs(o["id_i"]) > 1e-7:
                    return 0.0
                return -o[which]
            z0 = rng.normal(size=N + K * N + N)
            for which in best:
                res = minimize(neg, z0, args=(which,), method="Nelder-Mead", options=dict(maxiter=500, xatol=1e-8, fatol=1e-11))
                best[which] = max(best[which], -res.fun)
    t = math.tanh(om / 4)
    ps = np.linspace(1e-6, 1 - 1e-6, 400001); q = math.exp(-om)
    muA = ps / (ps + (1 - ps) * q)
    kmn = (muA * np.log(muA / ps) + (1 - muA) * np.log((1 - muA) / (1 - ps))).max()
    knm = (ps * np.log(ps / muA) + (1 - ps) * np.log((1 - ps) / (1 - muA))).max()
    print(f"w={om}: best TV {best['tv']:.6f} (tanh(w/4) = {t:.6f}); best J {best['J']:.5f} (w tanh(w/4) = {om * t:.5f}); "
          f"best KL(mu|nu) {best['klmn']:.5f} (no-feature sup {kmn:.5f}); best KL(nu|mu) {best['klnm']:.5f} (no-feature sup {knm:.5f})", flush=True)
