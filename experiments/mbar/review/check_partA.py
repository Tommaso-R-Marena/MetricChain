"""Referee A -- independent checks of Part A (MATHEMATICS.md): A3 (closed-orthant formula, finiteness
criterion, radial limit), A4 (superadditive precision), A5 (three expressions), A6 (efficiency bound,
bound with lower limits), A7 (monotone iteration).  No import of d9mbar.
"""
import numpy as np
import cvxpy as cp
from scipy.sparse.csgraph import connected_components
from scipy.optimize import minimize

rng = np.random.default_rng(20261128)


def rand_model(K, J, zero_prob=0.0, alpha=None):
    while True:
        al = rng.choice([0.5, 1.0, 3.0]) if alpha is None else alpha
        P = rng.dirichlet(np.ones(J) * al, size=K)
        if zero_prob > 0:
            P = np.where(rng.random((K, J)) < zero_prob, 0.0, P)
        if np.all(P.sum(axis=1) > 0):
            return P / P.sum(axis=1, keepdims=True)


def V_direct(P, s, nu):
    """sup_h 2 nu.h - sum_k s_k Var_k(h): J x J linear algebra on the definition (no Laplacian)."""
    m = s @ P
    Q = np.diag(m) - (P.T * s) @ P
    Q = (Q + Q.T) / 2
    w, E = np.linalg.eigh(Q)
    pos = w > 1e-11 * max(w.max(), 1e-300)
    coef = E.T @ nu
    if np.any(np.abs(coef[~pos]) > 1e-8 * max(np.abs(nu).max(), 1e-300)):
        return np.inf, None
    h = E[:, pos] @ (coef[pos] / w[pos])
    return float(np.sum(coef[pos] ** 2 / w[pos])), h


def V_A3c(P, s, nu):
    """Formula (c) of Theorem A3, taken literally."""
    A = s > 0
    m = s[A] @ P[A]
    supp = m > 0
    rho = np.zeros(P.shape[1])
    rho[supp] = nu[supp] / m[supp]
    rhobar = P[A] @ rho
    S = np.diag(s[A])
    pi = s[A][:, None] * P[A] / np.where(supp, m, 1.0)
    L = S - (pi * m) @ pi.T
    Lp = np.linalg.pinv((L + L.T) / 2, rcond=1e-10, hermitian=True)
    return float((rho ** 2) @ m + (S @ rhobar) @ Lp @ (S @ rhobar))


def finite_by_criterion(P, s, nu):
    """Criterion (b) of Theorem A3 (finite support: rho in L2 is automatic)."""
    A = np.where(s > 0)[0]
    m = s[A] @ P[A]
    supp = m > 0
    if np.any(np.abs(nu[~supp]) > 1e-12):
        return False
    adj = (P[A] @ P[A].T) > 0
    ncomp, lab = connected_components(adj, directed=False)
    for cidx in range(ncomp):
        C = (P[A][lab == cidx].sum(axis=0) > 0)
        if abs(nu[C].sum()) > 1e-10:
            return False
    return True


def rand_target(P):
    K, J = P.shape
    if rng.random() < 0.6:
        c = rng.normal(size=K)
        if rng.random() < 0.5:
            c[rng.random(K) < 0.4] = 0.0
        if np.count_nonzero(c) < 2:
            c[:2] = [1.0, -1.0]
        c = c - c.sum() * (c != 0) / np.count_nonzero(c)
        return c @ P
    k = rng.integers(K)
    Aobs = rng.normal(size=J)
    return (Aobs - P[k] @ Aobs) * P[k]


def rand_alloc(K, zero_prob):
    while True:
        s = rng.dirichlet(np.ones(K))
        s = np.where(rng.random(K) < zero_prob, 0.0, s)
        if s.sum() > 0:
            return s / s.sum()


# ---------------------------------------------------------------- A3
print("== A3: formula (c) vs direct definition; finiteness criterion (b); radial limit (a)")
n_fin = n_inf = 0
worst = 0.0
mis = 0
worst_rad = 0.0
for trial in range(6000):
    K, J = int(rng.integers(2, 6)), int(rng.integers(2, 8))
    P = rand_model(K, J, zero_prob=rng.choice([0.0, 0.3, 0.6]), alpha=rng.choice([1.0, 3.0]))
    s = rand_alloc(K, rng.choice([0.0, 0.3, 0.6]))
    nu = rand_target(P)
    if np.abs(nu).max() < 1e-9:      # degenerate target (nu = 0 up to rounding): skip
        continue
    Vd, _ = V_direct(P, s, nu)
    crit = finite_by_criterion(P, s, nu)
    if crit != np.isfinite(Vd):
        mis += 1
        if mis <= 3:
            print("  MISMATCH criterion vs direct", crit, Vd, "\n", P, s, nu)
        continue
    if np.isfinite(Vd):
        n_fin += 1
        Vc = V_A3c(P, s, nu)
        worst = max(worst, abs(Vc - Vd) / max(abs(Vd), 1e-12))
        u = rng.dirichlet(np.ones(K))
        Vr = V_direct(P, s + 1e-9 * u, nu)[0]
        worst_rad = max(worst_rad, abs(Vr - Vd) / max(abs(Vd), 1e-12))
    else:
        n_inf += 1
print(f"  finite {n_fin}, infinite {n_inf}, criterion mismatches {mis}, "
      f"max rel |formula(c) - direct| = {worst:.2e}, radial-limit rel diff (t=1e-9) = {worst_rad:.2e}")

# contrast on sampled states: (c) equals c^T L^+ c - sum c^2/s
worst = 0.0
for trial in range(500):
    K, J = int(rng.integers(2, 6)), int(rng.integers(3, 8))
    P = rand_model(K, J)
    s = rng.dirichlet(np.ones(K))
    c = rng.normal(size=K); c -= c.mean()
    m = s @ P
    pi = s[:, None] * P / m
    L = np.diag(s) - (pi * m) @ pi.T
    Vh = c @ np.linalg.pinv((L + L.T) / 2, rcond=1e-10, hermitian=True) @ c - np.sum(c ** 2 / s)
    Vc = V_A3c(P, s, c @ P)
    worst = max(worst, abs(Vh - Vc) / max(Vc, 1e-9 * np.sum(c ** 2 / s)))
print(f"  interior contrasts: max rel |c^T L^+ c - sum c^2/s - formula(c)| = {worst:.2e}")

# ---------------------------------------------------------------- A4
print("== A4: superadditivity 1/V(s+t) >= 1/V(s) + 1/V(t) on the closed orthant (1/inf = 0)")
worst = -np.inf
cnt = 0
for trial in range(8000):
    K, J = int(rng.integers(2, 6)), int(rng.integers(2, 8))
    P = rand_model(K, J, zero_prob=rng.choice([0.0, 0.4]), alpha=rng.choice([1.0, 3.0]))
    s, t = rand_alloc(K, rng.choice([0.0, 0.4])), rand_alloc(K, rng.choice([0.0, 0.4]))
    t = t * rng.uniform(0.05, 5)
    nu = rand_target(P)
    I = lambda a: (lambda v: 0.0 if not np.isfinite(v) else (np.inf if v <= 0 else 1 / v))(V_direct(P, a, nu)[0])
    Is, It, Ist = I(s), I(t), I(s + t)
    if not np.isfinite(Ist) or Ist == 0:
        continue
    cnt += 1
    worst = max(worst, (Is + It - Ist) / Ist)
print(f"  {cnt} pairs, max relative violation (I(s)+I(t)-I(s+t))/I(s+t) = {worst:.2e}")
# adversarial local search on a few models
worst_adv = -np.inf
for trial in range(25):
    K, J = int(rng.integers(2, 5)), int(rng.integers(3, 7))
    P = rand_model(K, J, alpha=1.0)
    nu = rand_target(P)

    def negviol(x):
        s, t = np.abs(x[:K]) + 1e-9, np.abs(x[K:]) + 1e-9
        Vs, Vt, Vst = V_direct(P, s, nu)[0], V_direct(P, t, nu)[0], V_direct(P, s + t, nu)[0]
        if not all(np.isfinite([Vs, Vt, Vst])) or min(Vs, Vt, Vst) <= 0:
            return 0.0
        return -((1 / Vs + 1 / Vt - 1 / Vst) * Vst)
    res = minimize(negviol, rng.uniform(0.05, 1, 2 * K), method="Nelder-Mead",
                   options=dict(maxiter=4000, xatol=1e-10, fatol=1e-14))
    worst_adv = max(worst_adv, -res.fun)
print(f"  adversarial search (25 models): max relative violation = {worst_adv:.2e}")

# ---------------------------------------------------------------- A5 / A6 / A7
print("== A5: min_s V = dual^2/B = groupnorm^2/B ; A6: efficiency bounds ; A7: monotone step")
sqrt = np.sqrt


def cvx_Vstar(P, c, a, B, lo=None):
    K, J = P.shape
    r, t = cp.Variable((K, J)), cp.Variable(K)
    sq = sqrt(P)
    cons = [cp.sum(cp.multiply(P, r), axis=1) == 0, cp.sum(cp.multiply(P, r), axis=0) == -(c @ P),
            a @ t == B, t >= (np.zeros(K) if lo is None else lo)]
    obj = sum(cp.quad_over_lin(cp.multiply(sq[k], r[k]), t[k]) for k in range(K))
    pr = cp.Problem(cp.Minimize(obj), cons)
    pr.solve(solver=cp.CLARABEL)
    return pr.value, t.value


def cvx_dual(P, c, a, B):
    K, J = P.shape
    h = cp.Variable(J)
    sq = sqrt(P)
    cons = [cp.norm(cp.multiply(sq[k], h - P[k] @ h), 2) <= sqrt(a[k]) for k in range(K)]
    pr = cp.Problem(cp.Maximize((c @ P) @ h), cons)
    pr.solve(solver=cp.CLARABEL)
    return pr.value ** 2 / B


def cvx_group(P, c, a, B):
    K, J = P.shape
    r = cp.Variable((K, J))
    sq = sqrt(P)
    cons = [cp.sum(cp.multiply(P, r), axis=1) == 0, cp.sum(cp.multiply(P, r), axis=0) == -(c @ P)]
    pr = cp.Problem(cp.Minimize(sum(sqrt(a[k]) * cp.norm(cp.multiply(sq[k], r[k]), 2) for k in range(K))), cons)
    pr.solve(solver=cp.CLARABEL)
    return pr.value ** 2 / B


def state_vars(P, h):
    mu = P @ h
    return P @ h ** 2 - mu ** 2


w5 = 0.0
min_slack_i = np.inf      # V*/V(s) - bound(i)  must be >= 0
min_slack_lo = np.inf     # V*_lo/V(s) - bound_lo must be >= 0
tight_i = []
nbdry = 0
for trial in range(60):
    K, J = int(rng.integers(2, 6)), int(rng.integers(3, 8))
    P = rand_model(K, J, zero_prob=rng.choice([0.0, 0.25]), alpha=1.0)
    if connected_components((P @ P.T) > 0, directed=False)[0] != 1:
        continue
    c = rng.normal(size=K); c -= c.mean()
    a = rng.uniform(0.3, 5, K) if trial % 2 else np.ones(K)
    B = float(rng.uniform(0.5, 20))
    Vst, tst = cvx_Vstar(P, c, a, B)
    d, g = cvx_dual(P, c, a, B), cvx_group(P, c, a, B)
    w5 = max(w5, abs(d - Vst) / Vst, abs(g - Vst) / Vst)
    nbdry += int(np.min(tst) < 1e-6 * B)
    nu = c @ P
    for rep in range(8):
        s = rng.dirichlet(np.ones(K) * rng.choice([0.3, 1, 5]))
        s = s * B / (a @ s)
        V, h = V_direct(P, s, nu)
        gk = state_vars(P, h)
        bi = (V / B) / np.max(gk / a)
        min_slack_i = min(min_slack_i, Vst / V - bi)
        tight_i.append((Vst / V) / bi)
        lo = rng.uniform(0, 1, K) * s * rng.choice([0.0, 0.5, 1.0])
        if rep % 2:
            lo = rng.dirichlet(np.ones(K)) * B / a.sum() * rng.uniform(0, 0.9)
        Vlo, _ = cvx_Vstar(P, c, a, B, lo=lo)
        blo = 2 - (gk @ lo + (B - a @ lo) * np.max(gk / a)) / V
        min_slack_lo = min(min_slack_lo, Vlo / V - blo)
print(f"  A5: max rel disagreement of the three expressions = {w5:.2e}; optimal design on the boundary in {nbdry} models")
print(f"  A6(i): min over cases of [V*/V(s) - bound] = {min_slack_i:.3e}  (must be >= 0); "
      f"median (V*/V)/bound = {np.median(tight_i):.3f}")
print(f"  A6 lower limits: min of [V*_lo/V(s) - bound_lo] = {min_slack_lo:.3e}  (must be >= 0)")

worst_step = -np.inf
eq_cases = 0
for trial in range(4000):
    K, J = int(rng.integers(2, 6)), int(rng.integers(3, 8))
    P = rand_model(K, J, zero_prob=rng.choice([0.0, 0.3]), alpha=1.0)
    c = rng.normal(size=K); c -= c.mean()
    a = rng.uniform(0.2, 5, K)
    s = rand_alloc(K, rng.choice([0.0, 0.3]))
    nu = c @ P
    V, h = V_direct(P, s, nu)
    if not np.isfinite(V) or V <= 0:
        continue
    B = a @ s
    hh = np.where((s @ P) > 0, h, 0.0)
    gk = np.maximum(state_vars(P, hh), 0)
    sp = s * np.sqrt(gk / a)
    if sp.sum() == 0:
        continue
    sp = sp * B / (a @ sp)
    Vp = V_direct(P, sp, nu)[0]
    worst_step = max(worst_step, (Vp - V) / V)
print(f"  A7: max relative increase (V(s+) - V(s))/V(s) over random s incl. boundary = {worst_step:.2e}")
