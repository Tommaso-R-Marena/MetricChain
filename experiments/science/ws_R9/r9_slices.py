#!/usr/bin/env python3
"""R9, item 1 (SCI-REV-0001 M2): Theorem 11.90(a) at NEGATIVE accuracies, own numerical test.
Slice of density kappa, slope u, accuracy e < 0.  For random profiles with 3..5 blocks that are feasible (e + MI >= 0):
  r_mu(e) = min{ MI(nu) : mean(nu) = kappa, u * sum_j lam_j |nu_j - mu_j| <= e + MI(mu) }   (convex programme, SLSQP with
  auxiliary variables for the absolute values; several starts; the inner minimum can only be OVER-estimated by a
  solver, which would produce false violations — every apparent violation is re-solved from more starts)
against the two-block supremum R2(e) = sup_m sup_{shells} (closed evaluation on the ray of a binary centre).
Also: the value -e of the profiles with zero budget, and a mixture whose two-point components are infeasible."""
import math, sys
import numpy as np
from scipy.optimize import minimize
sys.dont_write_bytecode = True
from r9_minor import KL, F, lrange, shell_value

rng = np.random.default_rng(11)

def MI(lam, mu, k):
    return float(sum(l * KL(x, k) for l, x in zip(lam, mu)))

def r_profile(lam, mu, k, u, e, nstart=6):
    J = len(lam)
    budget = e + MI(lam, mu, k)
    if budget < -1e-12:
        return None
    if budget <= 1e-12:
        return MI(lam, mu, k)
    def obj(z):
        nu = z[:J]
        return sum(l * KL(min(max(x, 1e-12), 1 - 1e-12), k) for l, x in zip(lam, nu))
    cons = [{"type": "eq", "fun": lambda z: float(np.dot(lam, z[:J]) - k)},
            {"type": "ineq", "fun": lambda z: budget - u * float(np.dot(lam, z[J:]))}]
    for j in range(J):
        cons.append({"type": "ineq", "fun": (lambda z, j=j: z[J + j] - (z[j] - mu[j]))})
        cons.append({"type": "ineq", "fun": (lambda z, j=j: z[J + j] + (z[j] - mu[j]))})
    best = MI(lam, mu, k)                                     # nu = mu is feasible
    for s in range(nstart):
        if s == 0:
            nu0 = np.array(mu, float)
        else:
            w = rng.uniform(0, 1)
            nu0 = (1 - w) * np.array(mu) + w * k              # towards the constant profile
        z0 = np.concatenate([nu0, np.abs(nu0 - np.array(mu)) + 1e-9])
        res = minimize(obj, z0, method="SLSQP", constraints=cons, bounds=[(1e-9, 1 - 1e-9)] * J + [(0, 1)] * J,
                       options={"ftol": 1e-14, "maxiter": 600})
        z = res.x
        feas = abs(np.dot(lam, z[:J]) - k) < 1e-8 and u * float(np.dot(lam, np.abs(z[:J] - np.array(mu)))) <= budget + 1e-8
        if feas:
            best = min(best, obj(z))
    return best

def R2(k, u, e, ngrid_m=97, ngrid_l=4001):
    best = 0.0 if e >= 0 else -e
    for m in np.linspace(0.02, 0.98, ngrid_m):
        lo, hi = lrange(m, k)
        ls = np.linspace(0, hi * (1 - 1e-9), ngrid_l)
        for l in ls:
            if e + F(l, m, k) >= 0:
                v = shell_value(l, m, k, u, e)
                if v > best: best = v
    return best

P = lambda *a: (print(*a), sys.stdout.flush())
tot = viol = 0
for (k, u, e) in ((0.3, 1.0, -0.03), (0.3, 1.0, -0.1), (0.5, 1.0, -0.05), (0.2, 2.0, -0.05), (0.4, 0.5, -0.02), (0.5, 3.0, -0.2)):
    hk = -k * math.log(k) - (1 - k) * math.log(1 - k)
    r2 = R2(k, u, e)
    worst = -1; n = 0; nzero = 0
    for trial in range(60):
        J = int(rng.integers(3, 6))
        for attempt in range(200):
            lam = rng.dirichlet(np.ones(J))
            mu = rng.beta(0.4, 0.4, size=J)                   # spread block densities, so that MI is large enough
            # shift to mean kappa by mixing with a point mass profile
            mbar = float(np.dot(lam, mu))
            if mbar > k: mu = mu * (k / mbar)
            else: mu = 1 - (1 - mu) * ((1 - k) / (1 - mbar))
            if e + MI(lam, mu, k) >= 0:
                break
        else:
            continue
        r = r_profile(lam, mu, k, u, e)
        if r is None: continue
        n += 1; tot += 1
        if r > r2 + 2e-6:
            r = r_profile(lam, mu, k, u, e, nstart=40)
            if r > r2 + 2e-6:
                viol += 1
        worst = max(worst, r - r2)
    # zero-budget profile: the ray of the centre m = kappa at F = -e
    lo, hi = lrange(k, k)
    from scipy.optimize import brentq
    l0 = brentq(lambda l: F(l, k, k) + e, 0, hi * (1 - 1e-12))
    v0 = shell_value(l0, k, k, u, e)
    P(f"(kappa, u, e) = ({k}, {u}, {e}): h(kappa) = {hk:.4f}; two-block supremum R2 = {r2:.6f} (-e = {-e});  {n} random feasible profiles with 3-5 blocks:"
      f" max (r_mu - R2) = {worst:+.2e};  shell of the centre m = kappa with F = -e: value {v0:.6f}")
P(f"total: {tot} profiles, violations of r_mu(e) <= R2(e) (beyond 2e-6): {viol}")
# a feasible mixture with infeasible two-point components (the phenomenon behind M2)
k, e = 0.3, -0.1
lamA, muA = [0.5, 0.5], [0.05, 0.55]          # two-point law with mean 0.3, MI small?
lamB, muB = [0.7, 0.3], [0.0001, 0.9997]      # nearly pure profile
for nm, lam, mu in (("A", lamA, muA), ("B", lamB, muB)):
    P(f"two-point law {nm}: mean {np.dot(lam, mu):.4f}, MI = {MI(lam, mu, k):.4f}, feasible at e = {e}: {e + MI(lam, mu, k) >= 0}")
mix = 0.5
lam = [mix * l for l in lamA] + [(1 - mix) * l for l in lamB]; mu = muA + muB
P(f"their equal mixture (4 blocks): mean {np.dot(lam, mu):.4f}, MI = {MI(lam, mu, k):.4f}, feasible: {e + MI(lam, mu, k) >= 0}"
  f" — a feasible law with an infeasible two-point component")
