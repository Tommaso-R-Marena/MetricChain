#!/usr/bin/env python3
"""Referee R8 -- Proposition K5(b), the necessary condition "never below h" at accuracy zero: an attempt to
break it numerically (item 10 of the brief).  Own code.
With the smallest admissible inner exponent function T = theta_hint (0 beyond eps*), T(0) = h:
  (1) two-rung bound of Theorem K2(a):  B2(phi, xi) = max{ phi a + (1-phi) theta_hint(xi), (1-phi)(xi + h) }
  (2) R_phi[theta_hint](0) = sup_{gamma>=0} [ min(gamma, phi a) + (1-phi) theta_hint(gamma/(1-phi)) ]
  (3) the general ladder bound (3.1) with random ladders 2u = xi_0 > xi_1 > ... > xi_{L-1} > 0
are minimised over their parameters; each minimum must be >= h.  Also (4): the same with T = theta_hint
replaced by anything larger can only increase the bounds (monotone), so this is the worst case."""
import math, sys, time
import numpy as np
t0 = time.time()
def H(r):
    r = np.clip(r, 1e-300, 1 - 1e-16)
    return -(r * np.log(r) + (1 - r) * np.log(1 - r))
worst_all = 1e9
for u in (0.1, 0.3, 0.5, 1.0, 2.0, 4.0, 8.0):
    pu = 1 / (1 + math.exp(u)); lam1 = math.log(2 / (1 + math.exp(-u))); est = math.log(math.cosh(u / 2))
    a = math.log(2) - float(H(pu)); h = math.log(2) - float(H(lam1 / u))
    def th(e):
        e = np.asarray(e, dtype=float)
        return np.where(e >= est, 0.0, np.maximum(math.log(2) - H(np.minimum((lam1 + e) / u, 0.5)), 0.0))
    # (1) two rungs
    phis = np.concatenate((np.linspace(1e-6, 1 - 1e-6, 4001), np.exp(np.linspace(math.log(1e-9), math.log(1e-2), 500))))
    xis = np.concatenate((np.exp(np.linspace(math.log(1e-9 * est), math.log(4 * u), 3000)), np.linspace(0, 2 * est, 3000)[1:]))
    P, X = np.meshgrid(phis, xis, indexing='ij')
    B2 = np.maximum(P * a + (1 - P) * th(X), (1 - P) * (X + h))
    m1 = float(B2.min()); i1 = np.unravel_index(int(B2.argmin()), B2.shape)
    # (2) R_phi[theta_hint](0): sup over gamma in [0, phi a] of gamma + (1-phi) theta_hint(gamma/(1-phi)), and gamma=0: (1-phi) h
    m2 = 1e9; arg2 = None
    for phi in phis[::4]:
        gam = np.linspace(0, phi * a, 4000)
        v = float(np.max(gam + (1 - phi) * th(gam / (1 - phi))))
        v = max(v, (1 - phi) * h)
        if v < m2: m2, arg2 = v, phi
    # (3) random ladders in (3.1)
    rng = np.random.default_rng(int(u * 1000) + 5)
    m3 = 1e9
    for trial in range(60000):
        L = int(rng.integers(1, 9))
        phi = float(rng.choice([rng.uniform(1e-4, 1 - 1e-4), 10 ** rng.uniform(-6, -1)]))
        if L > 1:
            hi = float(rng.choice([2 * u, est, a, 10 * est])) * 0.999
            xi = np.sort(np.exp(rng.uniform(math.log(1e-8 * est), math.log(hi), L - 1)))[::-1]
            xi = np.concatenate(([2 * u], xi))
            if not np.all(np.diff(xi) < 0): continue
        else:
            xi = np.array([2 * u])
        terms = [phi * a]
        for l in range(1, L):
            terms.append(min(phi * a, (1 - phi) * xi[l - 1]) + (1 - phi) * float(th(xi[l])))
        terms.append(min(phi * a, (1 - phi) * xi[L - 1]) + (1 - phi) * h)
        m3 = min(m3, max(terms))
    w = min(m1, m2, m3) - h
    worst_all = min(worst_all, w / h)
    print("u=%4.1f  h=%.6f a=%.6f | min two-rung bound - h = %+.3e (at phi=%.3g, xi=%.3g) | min_phi R_phi[theta_hint](0) - h = %+.3e (phi=%.3g) | min over 60000 random ladders of (3.1) - h = %+.3e"
          % (u, h, a, m1 - h, P[i1], X[i1], m2 - h, arg2, m3 - h))
print("smallest (bound - h)/h over all searches: %+.3e   (negative would contradict Proposition K5(b))  [%.0f s]" % (worst_all, time.time() - t0))
