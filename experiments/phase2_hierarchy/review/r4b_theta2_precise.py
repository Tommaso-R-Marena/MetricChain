"""Precision check of theta_2^*(u) at u = 2 and u = 4 (the report's section-6 table prints 0.12916 and 0.29417;
the reviewer's first pass gave 0.12918 and 0.29415).  theta_2^* solves  root of Xi(., phi1) = (1 - phi1) a  in phi1."""
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from rv_common import consts, fKL, kKL, finv

LN2 = math.log(2.0)


def Xi_exact(theta, phi1, u):
    c = consts(u)
    phi2 = 1 - phi1

    def E(z):
        rem = theta - phi1 * fKL(z)
        if rem < 0:
            return 1e9
        rho = 0.0 if rem >= phi2 * LN2 else finv(rem / phi2)
        return phi1 * kKL(z, u) + phi2 * (u * rho - c['Lam'])

    zs = np.linspace(c['pu'], 0.5, 4001)
    v = np.array([E(z) for z in zs])
    i = int(np.argmin(v))
    res = minimize_scalar(E, bounds=(zs[max(i - 1, 0)], zs[min(i + 1, 4000)]), method='bounded', options={'xatol': 1e-13})
    return min(res.fun, v[i])


for u in (2.0, 4.0):
    c = consts(u)

    def root(phi1):
        return brentq(lambda t: Xi_exact(t, phi1, u), c['h'], phi1 * c['a'] + (1 - phi1) * LN2 - 1e-9, xtol=1e-12)

    phi = brentq(lambda p: root(p) - (1 - p) * c['a'], 0.3, 0.8, xtol=1e-9)
    th = (1 - phi) * c['a']
    print('u=%g: best phi1 = %.6f, theta2* = %.6f, theta2*/a = %.5f, theta2*/h = %.5f, Xi at theta2*: %.2e' % (u, phi, th, th / c['a'], th / c['h'], Xi_exact(th, phi, u)))
