#!/usr/bin/env python3
"""Assistant C -- check the reviewer's printed witness for T^(3)(0) <= 0.5403 a at u = 1 (ladder (1,1,1)):
phi = 0.512, xi1/a = 0.631, xi2/a = 0.107.  Own code from Theorem 11.84(a) with L = 3, r_l = 1, g = 0:
value = max{ phi a + (1-phi) th_na(xi1), min(phi a, (1-phi) xi1) + (1-phi) th_na(xi2),
             min(phi a, (1-phi) xi2) + (1-phi) a },   th_na(x) = min{ f(rho) : k(rho) <= x }.
Because the printed parameters are rounded to three digits, a small polish around them is also reported."""
import math
from scipy.optimize import brentq

u = 1.0
pu = 1 / (1 + math.exp(u))
Lam = math.log(2 / (1 + math.exp(-u)))
f = lambda r: r * math.log(2 * r) + (1 - r) * math.log(2 * (1 - r))
k = lambda r: f(r) + u * r - Lam
a, h = f(pu), f(Lam / u)
eps_star = k(0.5)


def th_na(x):
    if x >= eps_star:
        return 0.0
    return f(brentq(lambda r: k(r) - x, pu, 0.5, xtol=1e-14))


def value(phi, x1, x2):
    return max(phi * a + (1 - phi) * th_na(x1), min(phi * a, (1 - phi) * x1) + (1 - phi) * th_na(x2),
               min(phi * a, (1 - phi) * x2) + (1 - phi) * a)


print(f"u = 1: a = {a:.6f}, h/a = {h / a:.5f}, eps* = {eps_star:.6f}, k(p_u) = {k(pu):.1e}")
v = value(0.512, 0.631 * a, 0.107 * a)
print(f"value at the printed witness (phi, xi1/a, xi2/a) = (0.512, 0.631, 0.107): {v / a:.5f} a")
best = (v, 0.512, 0.631, 0.107)
for i in range(-20, 21):
    for j in range(-20, 21):
        for l in range(-20, 21):
            p, x1, x2 = 0.512 + i * 2e-4, 0.631 + j * 2e-4, 0.107 + l * 2e-4
            w = value(p, x1 * a, x2 * a)
            if w < best[0]:
                best = (w, p, x1, x2)
print(f"best in a box of +-0.004 around it: {best[0] / a:.5f} a at (phi, xi1/a, xi2/a) = ({best[1]:.4f}, {best[2]:.4f}, {best[3]:.4f})")
print(f"two rounds for comparison, T2(0)/a = 0.62432 (reviewer), 0.6243 (ours); three rounds: every admissible ladder is an upper bound")
