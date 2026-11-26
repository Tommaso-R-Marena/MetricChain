#!/usr/bin/env python3
"""ER3 review, E19(f): the Gaussian control against theory.

For a cloud of N independent Gaussian points in dimension D the frequency with which K random points span a face
has a sharp transition at K = rho_W^+(D/N) D (Vershik-Sporyshev; Donoho-Tanner).  The curve is computed here from
the statistical dimension of the descent cone of the non-negative l1 problem (Amelunxen-Lotz-McCoy-Tropp):
    D/N = inf_{tau >= 0}  kappa (1 + tau^2) + (1 - kappa) E (g - tau)_+^2 ,   kappa = K/N ,
which reproduces the tabulated value rho_W^+(1/2) = 0.5581 of Donoho-Tanner.  The small-delta asymptote quoted in
the report is rho ~ 1/(2 ln(1/delta)), i.e. K ~ D/(2 ln(N/D)).
"""
import numpy as np
from math import comb
from scipy.optimize import brentq
from scipy.special import erfcx
from scipy.stats import norm


def curve_point(tau):
    """(delta, kappa) on the transition curve, parametrised by the optimal tau (stationarity in tau gives
    kappa tau = (1 - kappa) E (g - tau)_+ ).  Mills ratio through erfcx, so that tiny delta is reachable."""
    phi = norm.pdf(tau); mills = np.sqrt(np.pi / 2) * erfcx(tau / np.sqrt(2))      # Phi(-tau) = phi * mills
    psi = phi * (1 - tau * mills)                                                  # E (g - tau)_+
    second = phi * ((1 + tau * tau) * mills - tau)                                 # E (g - tau)_+^2
    kappa = psi / (tau + psi)
    return kappa * (1 + tau * tau) + (1 - kappa) * second, kappa


def rho_weak(delta):
    tau = brentq(lambda t: np.log(curve_point(t)[0]) - np.log(delta), 1e-9, 36.0, xtol=1e-13)
    return curve_point(tau)[1] / delta


print(f"check: rho_W^+(1/2) = {rho_weak(0.5):.4f}   (Donoho-Tanner: .5581)")
print("four-body data (the sizes of E19(e),(f)); 'control' = the division's Gaussian runs, 'cube' = its cube runs")
for n, control, cube in ((8, 78, 76), (10, 142, 152), (12, 214, 233)):
    N = 2 ** (n - 1); D = sum(comb(n - 1, j) for j in range(1, 5))
    r = rho_weak(D / N)
    print(f"   n = {n}: N = {N}, D = {D}, delta = D/N = {D / N:.3f}: theory rho_W^+ D = {r * D:.1f}; control {control}; cube {cube}; "
          f"asymptote D/(2 ln(N/D)) = {D / (2 * np.log(N / D)):.1f}")
print("pair data")
for n, control, cube in ((12, 11, 13), (14, 11.5, 16), (20, None, None), (40, None, None), (100, None, None), (400, None, None)):
    N = 2.0 ** (n - 1); D = n * (n - 1) // 2
    r = rho_weak(D / N)
    print(f"   n = {n}: delta = {D / N:.2e}: theory rho_W^+ D = {r * D:.1f} = {r * D / n:.3f} n; control {control}; cube {cube}; "
          f"asymptote D/(2 ln(N/D)) = {D / (2 * np.log(N / D)):.1f}; n/(4 ln 2) = {n / (4 * np.log(2)):.1f}")
print("four-body data, larger n: theory for the Gaussian cloud against the lift dimension L_2 and the bound 2 D_odd of E19(d)")
for n in (12, 16, 20, 30, 40, 60):
    N = 2.0 ** (n - 1); D = sum(comb(n - 1, j) for j in range(1, 5)); L2 = 1 + (n - 1) + comb(n - 1, 2)
    Dodd = (n - 1) + comb(n - 1, 3)
    r = rho_weak(D / N) if D / N < 1 else float("nan")
    print(f"   n = {n}: delta = {D / N:.2e}: Gaussian threshold {r * D:.0f} = {r * D / L2:.2f} L_2 = {r * D / (2 * Dodd):.3f} x 2 D_odd; "
          f"n^3/(48 ln 2) = {n ** 3 / (48 * np.log(2)):.0f}")
