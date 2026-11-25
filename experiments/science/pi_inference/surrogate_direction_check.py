#!/usr/bin/env python3
"""Benchmark B10 (hypothesis H11), planted control only -- coordinator's script.

Truth on {0,1}^n (n = 12, exact enumeration): an additive bulk plus a narrow basin of depth d on a Hamming
ball of radius 1 far from the bulk.  Surrogates: product measures (additive energies) fitted in three ways
  V  variational / Gibbs-Bogoliubov: minimise D_1(pi || pi_g) over product measures (mean field)
  S  least squares of an additive energy under the uniform measure ("fit on a reference sample")
  L  likelihood / moment matching: minimise D_1(pi_g || pi) over product measures (the true marginals)
For each: root-mean-square error of the fit under the surrogate's own measure, the variational gap
D_1(pi||pi_g), and the divergences of the truth from the surrogate D_1, D_2, D_inf (addendum A17), with the
certified costs e^{D_2}/eps^2 (Chebyshev bracket, no hint) and e^{D_inf}/eps (spot check with a hint).
Everything is an exact sum; no sampling.
"""
import math, json
import numpy as np
from scipy.optimize import minimize

n = 12
X = np.arange(2**n)
bits = ((X[:, None] >> np.arange(n)) & 1).astype(float)
wt = bits.sum(1)

def gibbs(E):
    w = np.exp(-(E - E.min())); return w / w.sum()

def product_measure(m):         # m_i = P(x_i = 1)
    return np.exp(bits @ np.log(m) + (1 - bits) @ np.log(1 - m))

def additive_energy(m):         # energy whose Gibbs measure is the product measure with marginals m
    return -(bits @ np.log(m) + (1 - bits) @ np.log(1 - m))

def renyi(pg, pi, p):
    w = pg / pi
    if p == 1: return float(np.sum(pg * np.log(w)))
    if math.isinf(p): return float(np.log(w.max()))
    return float(np.log(np.sum(pi * w**p)) / (p - 1))

rows = []
eps = 0.1
for h, d in ((2.2, 20.0), (2.2, 24.0), (1.5, 14.0), (3.0, 30.0)):
    bulk = h * wt                                   # bulk near the all-zeros corner, P(x_i=1) = 1/(1+e^h)
    a_dist = n - wt                                 # distance to the all-ones corner
    g = bulk - d * (a_dist <= 1)                    # basin: ball of radius 1 around all-ones
    pg = gibbs(g)
    wb = float(pg[a_dist <= 1].sum())               # true weight of the basin
    # --- V: mean field, started from the bulk (the fit a practitioner gets)
    def F(z):
        m = 1 / (1 + np.exp(-z)); pi = product_measure(m)
        return float(np.sum(pi * (g + np.log(pi))))          # E_pi g - S(pi) = D_1(pi||pi_g) - ln Z_g
    z0 = np.full(n, -h)
    zV = minimize(F, z0, method="L-BFGS-B").x
    mV = 1 / (1 + np.exp(-zV))
    # --- S: least squares additive fit under the uniform measure
    A = np.hstack([np.ones((2**n, 1)), bits])
    coef = np.linalg.lstsq(A, g, rcond=None)[0]
    mS = 1 / (1 + np.exp(coef[1:]))                 # Gibbs measure of the fitted additive energy
    # --- L: moment matching
    mL = pg @ bits
    for name, m in (("V variational", mV), ("S least squares", mS), ("L likelihood", mL)):
        pi = product_measure(m)
        ghat = additive_energy(m)
        r = g - ghat
        rc = r - float(pi @ r)
        rms = math.sqrt(float(pi @ rc**2))
        gap = float(np.sum(pi * np.log(pi / pg)))            # D_1(pi || pi_g)
        D1, D2, Dinf = renyi(pg, pi, 1), renyi(pg, pi, 2.0), renyi(pg, pi, math.inf)
        rows.append(dict(h=h, d=d, basin_weight=wb, fit=name, rms_under_surrogate=rms, variational_gap=gap,
                         D1=D1, D2=D2, Dinf=Dinf,
                         log10_cost_chebyshev=(D2 - 2 * math.log(eps)) / math.log(10),
                         log10_cost_hinted=(Dinf - math.log(eps)) / math.log(10),
                         surrogate_mass_on_basin=float(pi[a_dist <= 1].sum())))
print(f"n = {n}; accuracy eps = {eps}; costs as log10 of the number of evaluations")
print(f"{'h':>4} {'d':>4} {'basin wt':>9}  {'fit':<16} {'RMS(pi)':>9} {'D1(pi||pi_g)':>13} {'D1(pi_g||pi)':>13} {'D2':>7} {'Dinf':>7} "
      f"{'lg cost e^D2/eps^2':>19} {'lg cost e^Dinf/eps':>19} {'pi(basin)':>10}")
for r in rows:
    print(f"{r['h']:4.1f} {r['d']:4.0f} {r['basin_weight']:9.3f}  {r['fit']:<16} {r['rms_under_surrogate']:9.2e} {r['variational_gap']:13.3f} "
          f"{r['D1']:13.3f} {r['D2']:7.2f} {r['Dinf']:7.2f} {r['log10_cost_chebyshev']:19.1f} {r['log10_cost_hinted']:19.1f} {r['surrogate_mass_on_basin']:10.2e}")
json.dump(rows, open("surrogate_direction_check.json", "w"), indent=1)
print(f"for comparison: enumeration costs log10(2^n) = {n * math.log10(2):.1f}")
