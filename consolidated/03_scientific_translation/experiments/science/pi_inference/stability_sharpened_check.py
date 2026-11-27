"""Coordinator's check of workstream M's two sharpenings of Theorem 7 (SM_REPORT.md section 8, S1):
   KL(mu||nu) <= w^2/8,   TV(mu,nu) <= tanh(w/4),   J <= w*tanh(w/4),      w = beta*osc(r),
and of the pinned-marginal identity  Z = w(x*) / prod_i mu(x*_i | x*_{<i})  (self-reducibility).
Own code; random instances as in maxent_stability_check.py.
"""
import math, itertools
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(99)

def kl(p, q):
    return float(np.sum(p*(np.log(p) - np.log(q))))

def maxent(mu0, phi, m):
    if phi.shape[1] == 0: return mu0.copy()
    def dual(l):
        a = np.log(mu0) - phi @ l; mx = a.max(); lz = mx + np.log(np.exp(a-mx).sum()); p = np.exp(a-lz)
        return lz + l @ m, m - p @ phi
    res = minimize(lambda l: dual(l)[0], np.zeros(phi.shape[1]), jac=lambda l: dual(l)[1], method="BFGS",
                   options={"gtol": 1e-12, "maxiter": 5000})
    a = np.log(mu0) - phi @ res.x; a -= a.max(); p = np.exp(a); return p/p.sum()

w1 = w2 = w3 = 0.0; used = 0
for trial in range(3000):
    N = int(rng.integers(2, 30)); K = int(rng.integers(0, min(N-1, 5)+1))
    mu0 = rng.dirichlet(np.ones(N)); mu0 = np.maximum(mu0, 1e-6); mu0 /= mu0.sum()
    phi = rng.normal(size=(N, K)); lam = rng.normal(size=K)
    w = float(rng.choice([0.1, 0.5, 1.0, 2.0, 4.0, 8.0]))
    r = rng.uniform(size=N) if rng.uniform() < 0.5 else (rng.uniform(size=N) < 0.5).astype(float)
    if r.max() == r.min(): continue
    r = (r - r.min())/(r.max() - r.min())*w
    a = np.log(mu0) - phi @ lam - r; a -= a.max(); mu = np.exp(a); mu /= mu.sum()
    nu = maxent(mu0, phi, mu @ phi)
    if K and np.max(np.abs(nu @ phi - mu @ phi)) > 1e-7: continue
    if min(mu.min(), nu.min()) < 1e-200: continue
    used += 1
    tv = 0.5*np.abs(mu-nu).sum(); J = kl(mu, nu) + kl(nu, mu)
    assert kl(mu, nu) <= w*w/8 + 1e-8 and tv <= math.tanh(w/4) + 1e-8 and J <= w*math.tanh(w/4) + 1e-8
    w1 = max(w1, kl(mu, nu)/(w*w/8)); w2 = max(w2, tv/math.tanh(w/4)); w3 = max(w3, J/(w*math.tanh(w/4)))
print(f"{used} instances: max KL/(w^2/8) = {w1:.4f}; max TV/tanh(w/4) = {w2:.4f}; max J/(w tanh(w/4)) = {w3:.4f}")
for w in (0.5, 2.0, 8.0):
    mu = np.array([1.0, math.exp(-w)]); mu /= mu.sum(); nu = np.array([.5, .5])
    print(f"two points, w={w}: TV = {0.5*np.abs(mu-nu).sum():.6f}, tanh(w/4) = {math.tanh(w/4):.6f}")

# pinned marginals: Z from n conditional one-body marginals and one evaluation
n = 10; X = np.array(list(itertools.product([0, 1], repeat=n)))
g = rng.normal(size=len(X)); wts = np.exp(-g); Z = wts.sum(); mu = wts/Z
xs = X[rng.integers(len(X))]
prod = 1.0; mask = np.ones(len(X), bool)
for i in range(n):
    cond = mu[mask]; sel = X[mask][:, i] == xs[i]
    prod *= cond[sel].sum()/cond.sum(); mask &= (X[:, i] == xs[i])
idx = int("".join(map(str, xs)), 2)
print(f"pinned marginals: Z = {Z:.10f}; w(x*)/prod of conditional marginals = {wts[idx]/prod:.10f}")
