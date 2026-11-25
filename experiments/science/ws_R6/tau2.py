"""
tau2.py -- workstream R6: independent evaluation of the two-level exponent at bounded accuracy,
  tau_2 = inf_phi sup_{gamma >= 0} [ min(gamma, phi a) + (1-phi) theta_na(gamma/(1-phi)) ]      (Prop. 11.57(b) with T = theta_na, T(0) = a),
of the identity theta_na(e + theta_hint(e)) = theta_hint(e) (11.18.1), and of Prop. 11.57(c) (no level below h) on a grid.
"""
import numpy as np
from scipy.optimize import brentq

def kl(r, q):
    r = np.clip(r, 1e-300, 1 - 1e-16)
    return r * np.log(r / q) + (1 - r) * np.log((1 - r) / (1 - q))

for u in (0.5, 1.0, 2.0):
    pu = 1 / (1 + np.exp(u)); lam1 = np.log(2 / (1 + np.exp(-u))); estar = np.log(np.cosh(u / 2))
    a = kl(pu, 0.5); h = kl(lam1 / u, 0.5)
    rho = np.linspace(pu, 0.5, 200001)
    xs = kl(rho, pu)            # increasing from 0 to eps*
    th = kl(rho, 0.5)           # theta_na at those accuracies
    def theta_na(x):
        return np.where(x >= estar, 0.0, np.interp(x, xs, th))
    def theta_hint(e):
        return np.where(e >= estar, 0.0, kl((lam1 + e) / u, 0.5))
    # identity (11.18.1)
    e = np.linspace(0, estar * 0.999, 2001)
    err = np.max(np.abs(theta_na(e + theta_hint(e)) - theta_hint(e)))
    # tau_2
    best = (9, None)
    for phi in np.linspace(0.02, 0.98, 4801):
        g = np.linspace(0, phi * a, 4001)
        val = np.max(g + (1 - phi) * theta_na(g / (1 - phi)))
        if val < best[0]:
            best = (val, phi)
    # Prop 11.57(c): sup_gamma [min(gamma, phi a) + (1-phi) theta_hint(gamma/(1-phi))] >= h for every phi
    worst = 9
    for phi in np.linspace(0.001, 0.999, 999):
        g = np.linspace(0, 3 * a, 6001)
        val = np.max(np.minimum(g, phi * a) + (1 - phi) * theta_hint(g / (1 - phi)))
        worst = min(worst, val - h)
    print("u=%.1f: a=%.5f h=%.5f h/a=%.4f eps*=%.5f | max error of theta_na(e+theta_hint(e)) = theta_hint(e): %.1e | tau_2/a = %.4f at phi = %.3f | min_phi (bracket with T=theta_hint) - h = %+.2e"
          % (u, a, h, h / a, estar, err, best[0] / a, best[1], worst))
