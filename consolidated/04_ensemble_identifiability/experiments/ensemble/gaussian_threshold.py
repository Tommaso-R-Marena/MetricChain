#!/usr/bin/env python3
"""The weak-neighbourliness threshold of a Gaussian cloud at the sizes of the cube computations of
docs/ensemble/ENSEMBLE_REPORT.md, section 4c.3 (f).

For N independent Gaussian points in dimension D, K random points span a face of the convex hull with a sharp
transition at K = rho_W^+(D/N) D (Vershik-Sporyshev; Donoho-Tanner).  The curve is computed from the statistical
dimension of the descent cone of the non-negative l1 problem (Amelunxen-Lotz-McCoy-Tropp),
    D/N = inf_{tau >= 0}  kappa (1 + tau^2) + (1 - kappa) E (g - tau)_+^2 ,     kappa = K/N ,
as in the internal review ER3 (docs/ensemble/reviews/ER3_scripts/er3_dt_curve.py, whose method this is); this
script adds the size n = 14.  Not part of run_all.py: its output is stored in output_threshold.txt.
"""
from math import comb

import numpy as np
from scipy.optimize import brentq
from scipy.special import erfcx
from scipy.stats import norm


def curve_point(tau):
    phi = norm.pdf(tau)
    mills = np.sqrt(np.pi / 2) * erfcx(tau / np.sqrt(2))          # Phi(-tau) = phi * mills
    psi = phi * (1 - tau * mills)                                  # E (g - tau)_+
    second = phi * ((1 + tau * tau) * mills - tau)                 # E (g - tau)_+^2
    kappa = psi / (tau + psi)
    return kappa * (1 + tau * tau) + (1 - kappa) * second, kappa


def rho_weak(delta):
    tau = brentq(lambda s: np.log(curve_point(s)[0]) - np.log(delta), 1e-9, 36.0, xtol=1e-13)
    return curve_point(tau)[1] / delta


if __name__ == "__main__":
    print(f"check: rho_W^+(1/2) = {rho_weak(0.5):.4f}   (Donoho-Tanner: .5581)")
    print("data of even order <= 4 on the cube: N = 2^(n-1) states modulo the flip, D = number of non-constant features")
    for n in (8, 10, 12, 14):
        N = 2 ** (n - 1)
        D = sum(comb(n - 1, j) for j in range(1, 5))
        L2 = 1 + (n - 1) + comb(n - 1, 2)
        print(f"   n = {n}: N = {N}, D = {D}, D/N = {D / N:.3f}: Gaussian threshold {rho_weak(D / N) * D:.1f};"
              f" lift dimension {L2}; 2 D_odd = {2 * ((n - 1) + comb(n - 1, 3))}")
