"""Profile (annular / soft-label dip) exponents at an additive base gamma, binary labels.

A profile is P = (m, v0, v1): label law M = (1-m, m); core conditional types V_phi(1) = v_phi, both in the
window [pi_0(1), pi_1(1)] (stable cores = Gibbs laws of soft labels gamma_phi in [-u,u]).  The excess mass of the
corresponding generalised dip sits at the core, whose one-body density is c(P) = (1-m) v0 + m v1.
    f(P; e) = min { I(M, V') : sum_phi M(phi) [ u |v'_phi - v_phi| + gamma (v_phi - v'_phi) ] <= e + D(V || pi_gamma | M) }.
Plain dips of centre type m: v0 = pi_0(1), v1 = pi_1(1).
"""
import numpy as np
from scipy.optimize import minimize_scalar, minimize
from sl import *


def f_profile(p, u, gamma, m, v0, v1, e):
    pg = pgam(p, gamma)
    B = e + (1 - m) * kl2(v0, pg) + m * kl2(v1, pg)
    if B <= 0:
        # no slack: the dip is the core itself
        y = (1 - m) * v0 + m * v1
        return (1 - m) * kl2(v0, y) + m * kl2(v1, y) if B == 0 else np.inf
    if m <= 0 or m >= 1 or v0 == v1:
        return 0.0
    # move the two conditional types towards each other; orientation by the sign of v1 - v0
    if v1 > v0:
        a0, a1 = (u - gamma), (u + gamma)       # cost per unit: raise v0', lower v1'
        # x0 = v0' - v0 in [0, min(B/((1-m)a0), ...)], then v1' = v1 - (B - (1-m) a0 x0)/(m a1)
        def I(x0):
            w0 = v0 + x0
            w1 = v1 - (B - (1 - m) * a0 * x0) / (m * a1)
            if w1 <= w0:
                return 0.0
            y = (1 - m) * w0 + m * w1
            return (1 - m) * kl2(w0, y) + m * kl2(w1, y)
        hi = min(B / ((1 - m) * a0) if a0 > 0 else np.inf, v1 - v0, 1 - v0)
    else:
        a0, a1 = (u + gamma), (u - gamma)       # lower v0', raise v1'
        def I(x0):
            w0 = v0 - x0
            w1 = v1 + (B - (1 - m) * a0 * x0) / (m * a1)
            if w1 >= w0:
                return 0.0
            y = (1 - m) * w0 + m * w1
            return (1 - m) * kl2(w0, y) + m * kl2(w1, y)
        hi = min(B / ((1 - m) * a0) if a0 > 0 else np.inf, v0 - v1, v0)
    if I(0.0) == 0.0 or I(hi) == 0.0:
        return 0.0
    res = minimize_scalar(I, bounds=(0.0, hi), method='bounded', options={'xatol': 1e-13})
    return max(min(res.fun, I(0.0), I(hi)), 0.0)


def sup_profiles(p, u, gamma, e, constrained=False, grid=41, refine=True):
    """sup over profiles (optionally with the density constraint c(P) = pi_gamma(1))."""
    _, p0, p1 = site_laws(p, u, 0.0)
    lo, hi = p0[1], p1[1]
    pg = pgam(p, gamma)
    best = (-1.0, None)
    ms = np.linspace(0.01, 0.99, grid)
    vs = np.linspace(lo, hi, grid)
    if not constrained:
        for m in ms:
            for v0 in vs:
                for v1 in vs:
                    val = f_profile(p, u, gamma, m, v0, v1, e)
                    if val > best[0]: best = (val, (m, v0, v1))
        if refine and best[1] is not None:
            def neg(z):
                m, v0, v1 = z
                if not (0 < m < 1 and lo <= v0 <= hi and lo <= v1 <= hi): return 1.0
                return -f_profile(p, u, gamma, m, v0, v1, e)
            res = minimize(neg, best[1], method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-13, 'maxiter': 4000})
            if -res.fun > best[0]: best = (-res.fun, tuple(res.x))
    else:
        g2 = 4 * grid
        for m in np.linspace(0.005, 0.995, g2):
            for v0 in np.linspace(lo, hi, g2):
                v1 = (pg - (1 - m) * v0) / m
                if not (lo <= v1 <= hi): continue
                val = f_profile(p, u, gamma, m, v0, v1, e)
                if val > best[0]: best = (val, (m, v0, v1))
        if refine and best[1] is not None:
            def neg(z):
                m, v0 = z
                if not (0 < m < 1 and lo <= v0 <= hi): return 1.0
                v1 = (pg - (1 - m) * v0) / m
                if not (lo <= v1 <= hi): return 1.0
                return -f_profile(p, u, gamma, m, v0, v1, e)
            res = minimize(neg, best[1][:2], method='Nelder-Mead', options={'xatol': 1e-11, 'fatol': 1e-14, 'maxiter': 4000})
            if -res.fun > best[0]:
                m, v0 = res.x
                best = (-res.fun, (m, v0, (pg - (1 - m) * v0) / m))
    return best


def c_tilt(p, gamma, lam):
    pg = pgam(p, gamma)
    return np.log(1 - pg + pg * np.exp(lam)) - lam * pg


def tilt_bound(p, u, gamma, e, lam_range=3.0, return_lam=False):
    """U(e) = min_lambda R_gamma(e - c_gamma(lambda); field shifted by lambda)."""
    def val(lam):
        pl = 1.0 / (1.0 + np.exp(-(np.log(p / (1 - p)) + lam)))
        return R_gamma(pl, u, gamma, e - c_tilt(p, gamma, lam))
    lams = np.linspace(-lam_range, lam_range, 241)
    vals = [val(l) for l in lams]
    i = int(np.argmin(vals))
    res = minimize_scalar(val, bounds=(lams[max(i - 1, 0)], lams[min(i + 1, 240)]), method='bounded', options={'xatol': 1e-10})
    best = min(res.fun, vals[i]); lam = res.x if res.fun <= vals[i] else lams[i]
    return (best, lam) if return_lam else best
