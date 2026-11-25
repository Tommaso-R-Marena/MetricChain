"""Workstream L1 — numerical sanity checks of the *formal statements* (not proofs).

Exact enumeration on F_2^7 with the [7,3] simplex code C (dual = Hamming [7,4,3], so dual
distance 3 and k = 2), plus random instances for the divergence inequalities.
Run:  python3 sanity_numerics.py      (a few seconds; fixed seed)
"""
import itertools, math
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(20261125)
n = 7
X = np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.int64)        # 128 points
idx = {tuple(x): i for i, x in enumerate(X)}
G = np.array([[(j >> b) & 1 for j in range(1, 8)] for b in range(3)])           # 3 x 7 generator
C = np.array([(np.array(m) @ G) % 2 for m in itertools.product([0, 1], repeat=3)])
wt = X.sum(1)

# (1) dual distance
dual_w = [int(u.sum()) for u in X if u.any() and not ((C @ u) % 2).any()]
print("(1) |C| =", len(C), " dual distance =", min(dual_w))

# (2) Lemma 1: random C-invariant probability vector
coset = np.array([min(idx[tuple((x + c) % 2)] for c in C) for x in X])
w = rng.random(len(X)); mu = w[coset]; mu /= mu.sum()
def max_dev(order):
    worst = 0.0
    for S in itertools.combinations(range(n), order):
        for y in itertools.product([0, 1], repeat=order):
            m = mu[(X[:, S] == np.array(y)).all(1)].sum()
            worst = max(worst, abs(m - 2.0 ** (-order)))
    return worst
print("(2) max |marginal - 2^-|S||: order 1: %.2e  order 2: %.2e  order 3: %.2e"
      % (max_dev(1), max_dev(2), max_dev(3)))

# (3) separation inequality and (4) counting, all centres
dH = lambda x, s: int(((x + s) % 2).sum())
worst_sep, worst_F, worst_diff, worst_cnt = np.inf, np.inf, np.inf, np.inf
for s in X[rng.choice(len(X), 6, replace=False)]:
    d1 = np.array([dH(x, s) for x in X], dtype=float)
    dC = np.array([min(dH(x, (s + c) % 2) for c in C) for x in X], dtype=float)
    for u in (0.5, 1.0, 2.0):
        for R in (1.0, 2.0, 3.0, 2.5):
            A, F = np.exp(-u * dC).sum(), np.exp(-u * np.maximum(dC, R)).sum()
            A1, F1 = np.exp(-u * d1).sum(), np.exp(-u * np.maximum(d1, R)).sum()
            worst_F = min(worst_F, len(C) * F1 - F)
            worst_diff = min(worst_diff, (A - F) - (A1 - F1))
            worst_sep = min(worst_sep, (math.log(A) - math.log(F)) - (math.log(A1 / F1) - math.log(len(C))))
for x in X[rng.choice(len(X), 6, replace=False)]:
    for r in (1.0, 2.0, 3.0, 2.5):
        near = sum(1 for s in X if min(dH(x, (s + c) % 2) for c in C) < r)
        worst_cnt = min(worst_cnt, len(C) * int((wt < r).sum()) - near)
print("(3) min slack: |C|F1 - F = %.3e ; (A-F)-(A1-F1) = %.3e ; separation(log) = %.3e"
      % (worst_F, worst_diff, worst_sep))
print("(4) min slack of the centre count |C|*#{wt<r} - #{s: d(x,s+C)<r} =", worst_cnt)

# (5) Theorem 3, point masses: k = 2, t = 1, M_1 = 1 + 7 = 8
unifC = np.zeros(len(X)); unifC[[idx[tuple(c)] for c in C]] = 1 / len(C)
print("(5) M_1 = 8 ; max point mass: random invariant mu: %.4f ; uniform on C: %.4f ; bound 1/8 = %.4f"
      % (mu.max(), unifC.max(), 1 / 8))

# (6) Pinsker and symmetrised Pinsker on random pairs
mp, ms = np.inf, np.inf
for _ in range(20000):
    k = rng.integers(2, 9)
    p = rng.dirichlet(np.full(k, rng.choice([0.2, 1.0, 5.0])))
    q = rng.dirichlet(np.full(k, rng.choice([0.2, 1.0, 5.0])))
    p, q = np.maximum(p, 1e-300), np.maximum(q, 1e-300)
    tv = 0.5 * np.abs(p - q).sum()
    kl_pq, kl_qp = (p * np.log(p / q)).sum(), (q * np.log(q / p)).sum()
    mp, ms = min(mp, kl_pq - 2 * tv ** 2), min(ms, kl_pq + kl_qp - 4 * tv ** 2)
print("(6) min over 20000 random pairs: KL - 2TV^2 = %.3e ; J - 4TV^2 = %.3e" % (mp, ms))

# (7) Theorem 7 on random instances (max-ent refinement by convex minimisation of the dual)
worst_id, worst_tv, worst_J, used = 0.0, 0.0, 0.0, 0
for _ in range(200):
    N, K = int(rng.integers(3, 20)), int(rng.integers(1, 4))
    mu0 = rng.dirichlet(np.ones(N)); Phi = rng.normal(size=(K, N)); lam = rng.normal(size=K)
    beta = float(rng.choice([0.3, 1.0, 3.0])); r = rng.normal(size=N)
    m = mu0 * np.exp(-beta * (lam @ Phi + r)); m /= m.sum()
    target = Phi @ m
    def dual(l):
        return math.log((mu0 * np.exp(-beta * (l @ Phi))).sum()) + beta * (l @ target)
    res = minimize(dual, lam, method="BFGS", options={"gtol": 1e-12})
    v = mu0 * np.exp(-beta * (res.x @ Phi)); v /= v.sum()
    if np.abs(Phi @ v - target).max() > 1e-7:
        continue
    used += 1
    J = (m * np.log(m / v)).sum() + (v * np.log(v / m)).sum()
    tv = 0.5 * np.abs(m - v).sum(); om = beta * (r.max() - r.min())
    worst_id = max(worst_id, abs(J - beta * (v @ r - m @ r)))
    worst_tv = max(worst_tv, tv / (om / 4)); worst_J = max(worst_J, J / (om ** 2 / 4))
print("(7) Theorem 7 on %d of 200 random instances (moments matched to 1e-7): "
      "max |J - beta(E_nu r - E_mu r)| = %.2e ; max TV/(beta*omega/4) = %.4f ; "
      "max J/((beta*omega)^2/4) = %.4f" % (used, worst_id, worst_tv, worst_J))
