#!/usr/bin/env python3
"""Threshold E of the field case (theory report 11.20): E = lim_{t->0} F*(t)/t = largest chord gap of g(x) = ln 2cosh(x/2)
over the window of fields [theta - u, theta + u], theta = ln((1-p)/p);  and R^max(e) = max_t [F*(t) - t e] from the closed form."""
import numpy as np, math
from scipy.optimize import minimize_scalar
def F(gam, t, p, u):
    q = 1 - p
    Zg = q + p * math.exp(-gam)
    L0 = -math.log(q + p * math.exp(-u)); L1 = -math.log(p + q * math.exp(-u))
    return (-t * math.log(Zg) + math.log((1 - math.exp(-t * (u + gam))) * math.exp(-t * L0) + (1 - math.exp(-t * (u - gam))) * math.exp(-t * (L1 + gam)))
            - math.log(1 - math.exp(-2 * t * u)))
def Fstar(t, p, u):
    r = minimize_scalar(lambda g: -F(g, t, p, u), bounds=(-u + 1e-9, u - 1e-9), method="bounded", options={"xatol": 1e-13})
    return -r.fun
def Rmax(e, p, u):
    r = minimize_scalar(lambda t: -(Fstar(t, p, u) - t * e), bounds=(1e-6, 1 - 1e-9), method="bounded", options={"xatol": 1e-12})
    return max(0.0, -r.fun)
def E_chord(p, u):
    th = math.log((1 - p) / p)
    g = lambda x: math.log(2 * math.cosh(x / 2))
    a, b = th - u, th + u
    r = minimize_scalar(lambda s: -(g(a) + (s - a) * (g(b) - g(a)) / (b - a) - g(s)), bounds=(a, b), method="bounded", options={"xatol": 1e-13})
    return -r.fun
for p, u in ((0.1, 2.0), (0.3, 1.0), (0.5, 1.0)):
    E = E_chord(p, u)
    print(f"p={p} u={u}: E (chord gap) = {E:.6f};  F*(t)/t at t = 1e-4: {Fstar(1e-4, p, u)/1e-4:.6f}, at 1e-6: {Fstar(1e-6, p, u)/1e-6:.6f};  "
          f"R^max(0) = {Rmax(0.0, p, u):.6f}, R^max(0.3E) = {Rmax(0.3*E, p, u):.6f}, R^max(0.999E) = {Rmax(0.999*E, p, u):.2e}, R^max(1.001E) = {Rmax(1.001*E, p, u):.2e}")
print("at the value of the published request: R^max(0.3 * 0.21227) =", f"{Rmax(0.3*0.21227, 0.1, 2.0):.6f}")
