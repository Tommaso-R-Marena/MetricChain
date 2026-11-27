#!/usr/bin/env python3
"""Two rounds, upper bound (Corollary U1.2): two levels, two rungs, both inner procedures one-round brackets.

    T^(2)(0) = min_{0<phi<1, xi>0} max{ phi*a + (1-phi)*theta_na(xi) ,  min(phi*a, (1-phi)*xi) + (1-phi)*a }.

Direct fine minimisation (no rounding), for several u and for the small-slope limit, where the value is
((sqrt 5 - 1)/2) a at xi = ((3 - sqrt 5)/2) a.  Also: the lower bound theta_2* of Theorem U3 (from lb2_exponent.py
values, recomputed here for u in the list) and the interval [theta_2*, T^(2)(0)].
usage: ub2_closed.py
"""
import math
import numpy as np
from scipy.optimize import minimize_scalar
from ulib import Cube
from lb2_exponent import theta_star_cube, theta_star_gauss


def value(a, th_na, xi_max):
    best = (9e9, None, None)
    for xi in np.linspace(xi_max * 1e-4, xi_max * 0.9999, 4000):
        t = th_na(xi)
        # for fixed xi the two terms cross at phi = (a + xi - t)/(2a + xi - t) (if (1-phi) xi <= phi a there)
        phi = (a + xi - t) / (2 * a + xi - t)
        v = max(phi * a + (1 - phi) * t, min(phi * a, (1 - phi) * xi) + (1 - phi) * a)
        if v < best[0]:
            best = (v, phi, xi)
    # local refinement over phi for the best xi
    v0, phi0, xi0 = best
    for phi in np.linspace(max(0.01, phi0 - 0.05), min(0.99, phi0 + 0.05), 2001):
        for xi in np.linspace(max(1e-9, xi0 * 0.97), min(xi_max, xi0 * 1.03), 61):
            t = th_na(xi)
            v = max(phi * a + (1 - phi) * t, min(phi * a, (1 - phi) * xi) + (1 - phi) * a)
            if v < best[0]:
                best = (v, phi, xi)
    return best


if __name__ == "__main__":
    v, phi, xi = value(1.0, lambda x: (1 - math.sqrt(x)) ** 2, 1.0)
    tl, _ = max((theta_star_gauss(p) for p in np.linspace(0.5, 0.75, 251)), key=lambda z: z[0])
    print(f"small-slope limit: T^(2)(0)/a = {v:.6f} at phi = {phi:.4f}, xi/a = {xi:.4f}   [(sqrt5-1)/2 = {(math.sqrt(5)-1)/2:.6f}, "
          f"(3-sqrt5)/2 = {(3-math.sqrt(5))/2:.4f}];  theta_2*/a = {tl:.4f};  h/a = 0.25")
    for u in (0.5, 1.0, 2.0, 3.0):
        c = Cube(u)
        v, phi, xi = value(c.a, c.theta_na, c.eps_star)
        tl = max(theta_star_cube(c, p)[0] for p in np.linspace(0.5, 0.7, 41))
        print(f"u={u}: a={c.a:.6f} h/a={c.h/c.a:.4f} | T^(2)(0)/a = {v/c.a:.4f} at phi={phi:.3f}, xi/eps*={xi/c.eps_star:.3f} | theta_2*/a >= {tl/c.a:.4f} "
              f"| (a+h)/(2a) = {(c.a+c.h)/(2*c.a):.4f}")
