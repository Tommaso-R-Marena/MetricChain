#!/usr/bin/env python3
"""Referee replication 6: the 'dip-packing exponent with a field' quoted in section 2.4 (3) of the report
(0.0253 at p = 0.3, u = 1; 0.0489 at p = 0.1, u = 2), computed in two independent ways:

 (i)  the closed form of theory report Theorem 11.59(b): max over gamma and t of
      F(gamma,t) = ln{[sinh(t(l+ - l)/2) C(l-)^t + sinh(t(l - l-)/2) C(l+)^t]/sinh(t u)} - t ln C(l),
      l = theta + gamma, l+- = theta +- u, C(x) = 2 cosh(x/2), theta = ln((1-p)/p);
 (ii) the referee's own large-deviation formula for centres of one type m around the baseline exp(-gamma|x|):
      exponent = max_{t>=0, s} min_{a in {0,1}} [ h2(m) + s m - ln( e^{t l(a,0)} + e^{s + t l(a,1)} ) ],
      l(a,c) = ln(k'(a,c)/s_c)  (relative cone normalised at its centre / its mass), maximised over m and gamma.
      [(ii) with s fixed at logit(m) is the Chernoff form  -ln rho_t(m;gamma)  of Theorem 11.109a(c).]
Run: python3 -B r6_class_exponent_field.py
"""
import math
import numpy as np
from scipy.optimize import minimize


def F_closed(theta, u, gam, t):
    lam, lp, lm = theta + gam, theta + u, theta - u
    C = lambda x: 2 * math.cosh(x / 2)
    num = math.sinh(t * (lp - lam) / 2) * C(lm) ** t + math.sinh(t * (lam - lm) / 2) * C(lp) ** t
    return math.log(num / math.sinh(t * u)) - t * math.log(C(lam))


def setup(p, u, gam):
    lp = math.log(p / (1 - p)) - gam
    pp = 1 / (1 + math.exp(-lp))
    z0, z1 = math.exp(-(u - gam)), math.exp(-(u + gam))
    s0, s1 = (1 - pp) + pp * z0, pp + (1 - pp) * z1
    return pp, z0, z1, s0, s1


def single_type(p, u, gam, m):
    pp, z0, z1, s0, s1 = setup(p, u, gam)
    l = {(0, 0): -math.log(s0), (0, 1): math.log(z1 / s1), (1, 0): math.log(z0 / s0), (1, 1): -math.log(s1)}
    h2m = -m * math.log(m) - (1 - m) * math.log(1 - m)

    def Fa(a, t, s):
        return h2m + s * m - np.logaddexp(t * l[(a, 0)], s + t * l[(a, 1)])
    # maximise v subject to v <= F0, v <= F1, t >= 0  (concave programme)
    best = 0.0
    for t0 in (0.3, 0.6, 1.0):
        x0 = np.array([t0, math.log(m / (1 - m)), 0.0])
        cons = [{'type': 'ineq', 'fun': lambda z: Fa(0, z[0], z[1]) - z[2]},
                {'type': 'ineq', 'fun': lambda z: Fa(1, z[0], z[1]) - z[2]},
                {'type': 'ineq', 'fun': lambda z: z[0]}]
        res = minimize(lambda z: -z[2], x0, constraints=cons, method='SLSQP', options={'ftol': 1e-13, 'maxiter': 500})
        if res.success:
            v = min(Fa(0, res.x[0], res.x[1]), Fa(1, res.x[0], res.x[1])) if res.x[0] >= 0 else 0.0
            best = max(best, float(v))
    return best


if __name__ == "__main__":
    for (p, u) in [(0.5, 1.0), (0.3, 1.0), (0.1, 2.0)]:
        theta = math.log((1 - p) / p)
        # (i)
        bi = (-1, None, None)
        for gam in np.linspace(-0.999 * u, 0.999 * u, 1999):
            for t in np.linspace(0.01, 0.99, 99):
                v = F_closed(theta, u, gam, t)
                if v > bi[0]:
                    bi = (v, gam, t)
        # sign convention check: the same with theta -> -theta must give the same maximum (bit flip)
        bi2 = max(F_closed(-theta, u, gam, t) for gam in np.linspace(-0.999 * u, 0.999 * u, 400) for t in np.linspace(0.01, 0.99, 99))
        # (ii)
        bii = (-1, None, None)
        for gam in np.linspace(-0.95 * u, 0.95 * u, 39):
            for m in np.linspace(0.02, 0.98, 49):
                v = single_type(p, u, gam, m)
                if v > bii[0]:
                    bii = (v, gam, m)
        # refine (ii) near its maximiser
        g0, m0 = bii[1], bii[2]
        for gam in np.linspace(g0 - 0.05 * u, g0 + 0.05 * u, 21):
            for m in np.linspace(max(0.01, m0 - 0.02), min(0.99, m0 + 0.02), 21):
                if abs(gam) < u:
                    v = single_type(p, u, gam, m)
                    if v > bii[0]:
                        bii = (v, gam, m)
        print(f"p={p} u={u}: (i) Theorem 11.59 closed form: max F = {bi[0]:.6f} at gamma={bi[1]:+.4f}, t={bi[2]:.2f} (with -theta: {bi2:.6f});"
              f"  (ii) referee's single-type exponent: {bii[0]:.6f} at gamma={bii[1]:+.4f}, type m={bii[2]:.3f}")
