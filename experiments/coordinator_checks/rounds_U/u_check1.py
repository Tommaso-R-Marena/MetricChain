#!/usr/bin/env python3
"""Coordinator's check of workstream U, Corollary U1.2: the two-round upper bound
   T2(0) = min_{phi, xi} max{ phi a + (1-phi) theta_na(xi),  min(phi a, (1-phi) xi) + (1-phi) a }."""
import numpy as np, math
def setup(u):
    pu = 1/(1+math.exp(u)); L1 = math.log(2/(1+math.exp(-u)))
    f = lambda r: r*np.log(2*r) + (1-r)*np.log(2*(1-r))
    k = lambda r: f(r) + u*r - L1
    rho = np.linspace(pu, 0.5, 400001)
    kk, ff = k(rho), f(rho)            # k increasing from 0 on [pu, 1/2], f decreasing
    theta_na = lambda e: np.interp(e, kk, ff)
    a = float(f(pu)); h = float(f(L1/u))
    return a, h, theta_na, float(kk[-1])
for u in (0.05, 0.5, 1.0, 2.0, 3.0):
    a, h, th, estar = setup(u)
    best = (9, None)
    xi = np.linspace(1e-6, estar, 4001)
    tn = th(xi)
    for phi in np.linspace(0.001, 0.999, 1997):
        v = np.maximum(phi*a + (1-phi)*tn, np.minimum(phi*a, (1-phi)*xi) + (1-phi)*a)
        i = int(np.argmin(v))
        if v[i] < best[0]: best = (float(v[i]), (phi, float(xi[i])))
    # the balanced value at xi = h
    print(f"u={u}: a={a:.6f} h={h:.6f} h/a={h/a:.4f}  T2(0)/a = {best[0]/a:.4f} at phi={best[1][0]:.3f}, xi/a={best[1][1]/a:.3f};  (a+h)/(2a) = {(a+h)/(2*a):.4f};  golden ratio {(math.sqrt(5)-1)/2:.4f}")
