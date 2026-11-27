#!/usr/bin/env python3
"""Coordinator's own solvers for the single-letter problem of workstream T (function-of-type known parts).

Profile: blocks j = 1..k with weights lam_j, block types mu_j.
  MI(nu)   = h(nu_bar) - sum_j lam_j h(nu_j),   dist(nu, mu) = sum_j lam_j |nu_j - mu_j|,   alpha(mu) = MI(mu) + I(mu_bar),
  r_mu(e)  = min{ MI(nu) : u dist(nu, mu) + I(nu_bar) <= e + alpha(mu) }.
Two independent inner solvers:
  slow:  for every exit type kappa' on a grid, the convex programme  min MI  s.t. nu_bar = kappa', dist <= (B - I(kappa'))/u
         by SLSQP in the variables (p, q) >= 0, nu = mu + p - q   (no clipping lemma, no table of v);
  fast:  clippings nu_j = clip(mu_j, c_lo, c_hi), the largest u-Lipschitz minorant v in the constraint, bisection in c_hi for
         every c_lo on a grid, golden-section refinement  (uses Lemma T6 and Lemma T7 of the workstream's report).
Their agreement on random profiles is a numerical test of those two lemmas."""
import numpy as np
from scipy.optimize import minimize, minimize_scalar

def hb(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -(x * np.log(x) + (1 - x) * np.log1p(-x))

class Model:
    def __init__(self, phi, u, K=200001):
        self.u = u
        self.kap = np.linspace(0, 1, K)
        raw = phi(self.kap) - hb(self.kap)
        self.Ik = raw - raw.min()
        v = self.Ik.copy(); dk = self.kap[1] - self.kap[0]
        for i in range(1, K): v[i] = min(v[i], v[i - 1] + u * dk)
        for i in range(K - 2, -1, -1): v[i] = min(v[i], v[i + 1] + u * dk)
        self.vk = v
        self.phi = phi
        self.rawmin = raw.min()
    def I(self, x): return np.interp(x, self.kap, self.Ik)
    def Iex(self, x): return self.phi(x) - hb(x) - self.rawmin
    def v(self, x): return np.interp(x, self.kap, self.vk)

def curie_weiss(bJ, bB):
    return lambda k: -(bJ / 2) * (2 * k - 1) ** 2 - bB * (2 * k - 1)

def MI(lam, nu):
    nu = np.asarray(nu, float)
    return hb((nu * lam).sum(axis=-1)) - (hb(nu) * lam).sum(axis=-1)

def alpha(M, lam, mu):
    return float(MI(lam, mu) + M.Iex((mu * lam).sum()))

# ------------------------------------------------------------------ fast solver (clipping, v in the constraint)
def r_fast(M, lam, mu, B, G=3000, need_arg=False):
    """min MI(clip(mu; c_lo, c_hi)) s.t. u dist + v(type) <= B."""
    lam = np.asarray(lam, float); mu = np.asarray(mu, float)
    def g_and_mi(clo, chi):
        nu = np.clip(mu[None, :], clo[:, None], chi[:, None])
        d = (np.abs(nu - mu[None, :]) * lam).sum(axis=1)
        t = (nu * lam).sum(axis=1)
        return M.u * d + M.v(t) - B, MI(lam, nu)
    def best_for(clo):
        # smallest feasible c_hi >= c_lo (g nonincreasing in c_hi)
        lo = clo.copy(); hi = np.ones_like(clo)
        g_hi, _ = g_and_mi(clo, hi)
        feas = g_hi <= 0
        g_lo, mi_lo = g_and_mi(clo, lo)
        full = g_lo <= 0          # complete clipping feasible: MI = 0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            gm, _ = g_and_mi(clo, mid)
            ok = gm <= 0
            hi = np.where(ok, mid, hi); lo = np.where(ok, lo, mid)
        _, mi = g_and_mi(clo, hi)
        mi = np.where(full, 0.0, mi)
        return np.where(feas, mi, np.inf), hi
    clo = np.linspace(0, 1, G)
    val, chi = best_for(clo)
    if not np.isfinite(val).any():
        return (np.inf, None) if need_arg else np.inf
    # refine around every local minimum of the scan
    best = np.inf; arg = None
    # local minima of the scan.  Runs of consecutive candidates (plateaus: no clipping from below, or the zero region of
    # complete clippings) count once -- otherwise a plateau fills all the slots and the other exit is never refined (the error
    # the workstream reports in its section 11, item 9(i)); no tolerance in the comparison (a tolerance of 1e-15 once dropped
    # the zero region: values of 5e-17 next to exact zeros).
    cand = [i for i in range(G) if np.isfinite(val[i]) and (i == 0 or not np.isfinite(val[i - 1]) or val[i] <= val[i - 1])
            and (i == G - 1 or val[i] <= val[i + 1])]
    runs = []
    for i in cand:
        if runs and i == runs[-1][-1] + 1: runs[-1].append(i)
        else: runs.append([i])
    reps = []
    for r_ in sorted(runs, key=lambda r_: val[r_[0]])[:8]:
        reps.append(r_[0])
        if r_[-1] != r_[0]: reps.append(r_[-1])
    idx = reps
    for i in idx:
        a = clo[max(i - 2, 0)]; b = clo[min(i + 2, G - 1)]
        f = lambda c: float(best_for(np.array([c]))[0][0])
        if b > a:
            r = minimize_scalar(f, bounds=(a, b), method="bounded", options={"xatol": 1e-13})
            cand = [(r.fun, r.x), (val[i], clo[i])]
        else:
            cand = [(val[i], clo[i])]
        for (fv, c) in cand:
            if fv < best:
                best = fv; arg = (c, float(best_for(np.array([c]))[1][0]))
    return (best, arg) if need_arg else best

# ------------------------------------------------------------------ slow solver (generic; I in the constraint)
def r_slow(M, lam, mu, B, nk=400, kgrid=None):
    lam = np.asarray(lam, float); mu = np.asarray(mu, float); k = len(mu)
    best = np.inf; arg = None
    ks = np.linspace(1e-4, 1 - 1e-4, nk) if kgrid is None else kgrid
    for kp in ks:
        rad = (B - float(M.Iex(kp))) / M.u
        if rad < abs(kp - (mu * lam).sum()) - 1e-12:
            continue
        # variables p, q >= 0: nu = mu + p - q
        def f(z):
            nu = np.clip(mu + z[:k] - z[k:], 1e-12, 1 - 1e-12)
            return float(MI(lam, nu))
        cons = [{"type": "eq", "fun": lambda z: float(((mu + z[:k] - z[k:]) * lam).sum() - kp)},
                {"type": "ineq", "fun": lambda z: float(rad - ((z[:k] + z[k:]) * lam).sum())}]
        bounds = [(0, 1 - m) for m in mu] + [(0, m) for m in mu]
        # start: move every block proportionally towards kp
        mb = (mu * lam).sum()
        if kp >= mb:
            z0 = np.concatenate([(1 - mu) * (kp - mb) / max(1 - mb, 1e-12), np.zeros(k)])
        else:
            z0 = np.concatenate([np.zeros(k), mu * (mb - kp) / max(mb, 1e-12)])
        try:
            r = minimize(f, z0, bounds=bounds, constraints=cons, method="SLSQP", options={"maxiter": 300, "ftol": 1e-14})
        except Exception:
            continue
        z = r.x
        if abs(cons[0]["fun"](z)) < 1e-9 and cons[1]["fun"](z) > -1e-9 and r.fun < best:
            best = float(r.fun); arg = (kp, mu + z[:k] - z[k:])
    return best, arg

def r_of_e(M, lam, mu, e, **kw):
    return r_fast(M, lam, mu, e + alpha(M, lam, mu), **kw)
