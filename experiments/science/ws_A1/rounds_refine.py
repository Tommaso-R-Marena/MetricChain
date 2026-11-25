import math, numpy as np
from scipy.optimize import brentq, minimize_scalar
LN2 = math.log(2)
def kl(a, b):
    o = 0.0
    if a > 0: o += a * math.log(a / b)
    if a < 1: o += (1 - a) * math.log((1 - a) / (1 - b))
    return o
def finv(t):
    if t <= 0: return 0.5
    if t >= LN2: return 0.0
    return brentq(lambda r: kl(r, 0.5) - t, 1e-300, 0.5, xtol=1e-15)
for u in (1.0, 2.0, 3.0):
    pu = 1 / (1 + math.exp(u)); Lam = math.log(2 / (1 + math.exp(-u)))
    a = kl(pu, 0.5); h = kl(Lam / u, 0.5)
    D = lambda t: u * finv(t) - Lam
    xna = lambda t: D(t) + t
    def Xi(theta, phi1):
        phi2 = 1 - phi1
        cmax = min(theta, phi1 * a)
        g = lambda c: phi1 * xna(c / phi1) + phi2 * D((theta - c) / phi2)
        cs = np.linspace(0.0, cmax, 2000)
        v = [g(c) for c in cs]
        k = int(np.argmin(v))
        lo, hi = cs[max(k - 1, 0)], cs[min(k + 1, 1999)]
        return min(v[k], minimize_scalar(g, bounds=(lo, hi), method="bounded", options={"xatol": 1e-14}).fun)
    def val(phi1):
        phi2 = 1 - phi1
        top = phi2 * a * (1 - 1e-10)
        if top <= h or Xi(h, phi1) <= 0: return 0.0
        if Xi(top, phi1) > 0: return top
        return brentq(lambda t: Xi(t, phi1), h, top, xtol=1e-11)
    grid = np.linspace(0.50, 0.70, 201)
    vals = [val(p) for p in grid]
    k = int(np.argmax(vals))
    print("u=%.1f: theta2*/a = %.5f at phi1 = %.3f; theta2*/h = %.4f; (phi2 a)/a at optimum = %.5f; binding 'theta<phi2 a': %s"
          % (u, vals[k] / a, grid[k], vals[k] / h, 1 - grid[k], abs(vals[k] - (1 - grid[k]) * a) < 1e-6))
