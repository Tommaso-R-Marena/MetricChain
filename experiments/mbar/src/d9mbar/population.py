"""Exact population quantities of multistate (MBAR) estimation on finite supports.

Division 9, written independently of the handoff's reference code (which is kept unchanged under
experiments/mbar/handoff/).  Float64; nothing here is interval arithmetic.

Model: K states, a finite support of J points, P[k, x] = probability of point x under state k
(rows sum to one).  s = sample amounts (>= 0, need not sum to one; s_k = 0 means 'unsampled').
A target is a signed measure nu on the support with total mass 0 -- the derivative of the estimand
along a perturbation h of the base measure is  int h dnu:
    contrast c (sum c = 0) of free energies f_k = -log Z_k :  nu = sum_k c_k P_k   (sign immaterial)
    expectation E_k[A]                                      :  nu = (A - E_k A) P_k
The efficiency bound / MBAR asymptotic variance with n_k = s_k independent samples is V_nu(s),
homogeneous of degree -1.  Routes, mathematically equal (docs/mbar/MATHEMATICS.md, part A):

  variance          : int rho^2 dm + (S rhobar)^T L_A^+ (S rhobar),  rho = dnu/dm        (stable,
                      allows zeros; the route used everywhere)                [Theorem A3]
  variance_formula  : c^T L(s)^+ c - sum c_k^2/s_k        (contrasts, s > 0; cancels badly as
                      s_k -> 0, kept as a cross-check)                        [handoff A1]
  variance_dual     : b^T Q(s)^+ b,  Q = diag(m) - sum_k s_k P_k P_k^T        [Theorem A2]
  variance_qp       : min of sum_k E_k r_k^2/s_k over the affine set F_c, via its KKT system,
                      with no reference to L                                  [Theorem A1]
"""
from __future__ import annotations

import numpy as np

__all__ = [
    "laplacian", "gauge_pinv", "contrast_measure", "observable_measure", "variance", "solve_dual",
    "state_variances", "variance_formula", "variance_dual", "variance_qp", "optimal_allocation",
    "elfving_value", "efficient_rounding", "efficiency_lower_bound",
]

_FLOOR = 1e-11      # states with s_k <= _FLOOR * sum(s) are treated as exactly unsampled


def _check(P, s, c=None, allow_zero=True):
    P = np.asarray(P, float)
    s = np.asarray(s, float)
    if P.ndim != 2 or s.shape != (P.shape[0],):
        raise ValueError("shape")
    if np.any(P < 0) or not np.allclose(P.sum(axis=1), 1.0, atol=1e-9):
        raise ValueError("rows of P must be probability vectors")
    if np.any(s < 0) or (not allow_zero and np.any(s <= 0)) or s.sum() <= 0:
        raise ValueError("sample amounts must be nonnegative and not all zero")
    if c is not None:
        c = np.asarray(c, float)
        if c.shape != s.shape or abs(c.sum()) > 1e-9 * max(1.0, np.abs(c).max()):
            raise ValueError("contrast must sum to zero")
    return P, s, c


def laplacian(P, s):
    """Overlap Laplacian L(s) = S - E_m[pi pi^T], m = sum_k s_k P_k, pi_k = s_k P_k / m."""
    P, s, _ = _check(P, s)
    m = s @ P
    act = m > 0
    A = s[:, None] * P[:, act]
    return np.diag(s) - (A / m[act]) @ A.T


def gauge_pinv(L, rtol=1e-12):
    """Pseudo-inverse on the gauge space 1^perp of a connected Laplacian; raises if disconnected."""
    K = L.shape[0]
    Jm = np.full((K, K), 1.0 / K)
    M = (L + L.T) / 2 + Jm
    w = np.linalg.eigvalsh(M)
    if w[0] <= rtol * max(1.0, w[-1]):
        raise ValueError("overlap graph disconnected or numerically unresolved")
    return np.linalg.inv(M) - Jm


def contrast_measure(P, c):
    c = np.asarray(c, float)
    if abs(c.sum()) > 1e-9 * max(1.0, np.abs(c).max()):
        raise ValueError("contrast must sum to zero")
    return np.asarray(P, float).T @ c


def observable_measure(P, k, A):
    """Target measure of the expectation E_k[A]: (A - E_k A) P_k."""
    P = np.asarray(P, float)
    A = np.asarray(A, float)
    return (A - P[k] @ A) * P[k]


def solve_dual(P, s, nu, rtol=1e-10):
    """The dual maximiser h of  2 int h dnu - sum_k s_k Var_k(h)  and the value V_nu(s).

    Returns (V, h, supp): h is defined on supp = {m_A > 0} (nan elsewhere); V = +inf when the target
    is not estimable from the sampled states (nu charges points outside supp, or its mass on some
    connected component of the sampled overlap graph is nonzero)."""
    P, s, _ = _check(P, s)
    nu = np.asarray(nu, float)
    J = P.shape[1]
    act = s > _FLOOR * s.sum()
    sa, Pa = s[act], P[act]
    m = sa @ Pa
    supp = m > 0
    h = np.full(J, np.nan)
    scale = max(np.abs(nu).max(), 1e-300)
    if np.any(np.abs(nu[~supp]) > 1e-9 * scale):
        return float("inf"), h, supp
    ms, nus = m[supp], nu[supp]
    rho = nus / ms
    pi = sa[:, None] * Pa[:, supp] / ms              # K_A x J'
    L = np.diag(sa) - (pi * ms) @ pi.T
    L = (L + L.T) / 2
    srho = pi @ nus                                    # s_j E_j[rho]
    w, E = np.linalg.eigh(L)
    pos = w > rtol * max(w[-1], 1e-300)
    coef = E.T @ srho
    if np.any(np.abs(coef[~pos]) > 1e-8 * max(np.abs(srho).max(), scale * 1e-3, 1e-300)):
        return float("inf"), h, supp                   # not estimable across components
    beta = E[:, pos] @ (coef[pos] / w[pos])
    h[supp] = rho + beta @ pi
    V = float(ms @ rho**2 + srho @ beta)
    return V, h, supp


def variance(P, s, nu):
    """V_nu(s) on the closed orthant (the stable route)."""
    return solve_dual(P, s, nu)[0]


def state_variances(P, s, nu):
    """g_k = Var_{p_k}(h) for every state k (sampled or not); -g is the gradient of V_nu at s
    (Theorem A2).  g_k = +inf if state k has mass where h is undefined (outside the sampled support)."""
    P = np.asarray(P, float)
    V, h, supp = solve_dual(P, s, nu)
    if not np.isfinite(V):
        return np.full(P.shape[0], np.inf)
    h0 = np.where(supp, h, 0.0)
    mu = P @ h0
    g = P @ h0**2 - mu**2
    outside = P[:, ~supp].sum(axis=1) > 1e-12
    g[outside] = np.inf
    return np.maximum(g, 0.0)


def variance_formula(P, s, c):
    """Handoff formula c^T L^+ c - sum c_k^2/s_k (needs s > 0)."""
    P, s, c = _check(P, s, c, allow_zero=False)
    v = gauge_pinv(laplacian(P, s)) @ c
    return float(c @ v - np.sum(c * c / s))


def variance_dual(P, s, c, rtol=1e-10):
    """sup_h { 2 sum_k c_k E_k h - sum_k s_k Var_k h } = b^T Q^+ b as a J x J problem."""
    P, s, c = _check(P, s, c)
    b = P.T @ c
    m = s @ P
    Q = np.diag(m) - (P.T * s) @ P
    w, E = np.linalg.eigh((Q + Q.T) / 2)
    pos = w > rtol * max(1.0, w[-1])
    coef = E.T @ b
    if np.any(np.abs(coef[~pos]) > 1e-8 * max(1.0, np.abs(b).max())):
        return float("inf")
    return float(np.sum(coef[pos] ** 2 / w[pos]))


def variance_qp(P, s, c):
    """min sum_k (1/s_k) sum_x P[k,x] r[k,x]^2 over r with E_k r_k = 0 and
    sum_k P[k,x] r[k,x] = -sum_k c_k P[k,x]  (needs s > 0).  Independent of L."""
    P, s, c = _check(P, s, c, allow_zero=False)
    K, J = P.shape
    idx = [(k, x) for k in range(K) for x in range(J) if P[k, x] > 0]
    A = np.zeros((K + J, len(idx)))
    wgt = np.zeros(len(idx))
    for i, (k, x) in enumerate(idx):
        A[k, i] = P[k, x]
        A[K + x, i] = P[k, x]
        wgt[i] = P[k, x] / s[k]
    rhs = np.concatenate([np.zeros(K), -(c @ P)])
    G = (A / wgt) @ A.T
    lam = np.linalg.lstsq(G, rhs, rcond=None)[0]
    r = (A.T @ lam) / wgt
    if np.max(np.abs(A @ r - rhs)) > 1e-7 * max(1.0, np.abs(rhs).max()):
        raise ValueError("affine set F_c is empty (disconnected overlap)")
    return float(np.sum(wgt * r * r))


def efficiency_lower_bound(P, s, nu, cost=None, budget=None, lower=None):
    """Certified lower bound on V*/V(s), V* = min over {t >= lower, cost.t = budget} (Theorem A6):
         lower = 0 :  V*/V(s) >= (V(s)/B) / max_k (g_k/a_k)                 (Elfving / Kiefer bound)
         general   :  V*/V(s) >= 2 - [g.lower + (B - a.lower) max_k g_k/a_k] / V(s)
    Computable from any allocation; bounds what re-allocation can still gain."""
    P = np.asarray(P, float)
    s = np.asarray(s, float)
    a = np.ones(len(s)) if cost is None else np.asarray(cost, float)
    B = float(a @ s) if budget is None else float(budget)
    lo = np.zeros(len(s)) if lower is None else np.asarray(lower, float)
    V = variance(P, s, nu)
    g = state_variances(P, s, nu)
    if not np.isfinite(V) or not np.all(np.isfinite(g)):
        return 0.0
    top = float(np.max(g / a))
    lin = 2.0 - (g @ lo + (B - a @ lo) * top) / V
    return float(max(lin, (V / B) / top)) if not lo.any() else float(lin)


def optimal_allocation(P, target, cost=None, budget=1.0, lower=None, s0=None, iters=20000,
                       tol=1e-9, objective=None, kind=None):
    """Minimise V(s) over {s >= lower, cost.s = budget}.

    `target`: a contrast (length K, sum 0), a target measure (length J), or a list of either, combined
    by objective in {'sum', 'max'} (A-type and minimax criteria).  When K == J the reading must be
    given: kind='measure' or kind='contrast'.
    Method: iterated Neyman allocation (Fellman's multiplicative rule) s_k <- s_k sqrt(g_k/a_k),
    g_k = Var_k(h_s), renormalised, with water-filling for the lower bounds and a floor so that a
    coordinate driven to zero can come back.  For one target each step does not increase V
    (Proposition A7).  Stops when the certified efficiency bound exceeds 1 - tol.
    Returns (s, V, info); info['efficiency_lower_bound'] certifies V*/V(s) (for 'sum'/'single')."""
    P = np.asarray(P, float)
    K, J = P.shape
    a = np.ones(K) if cost is None else np.asarray(cost, float)
    lo = np.zeros(K) if lower is None else np.asarray(lower, float)
    if np.any(a <= 0) or a @ lo > budget * (1 + 1e-12):
        raise ValueError("infeasible budget/lower bounds")

    def as_measure(t):
        t = np.asarray(t, float)
        if kind == "measure" or (kind is None and t.shape == (J,) and K != J):
            if t.shape != (J,):
                raise ValueError("a target measure must have one entry per support point")
            return t
        if kind == "contrast" or (kind is None and t.shape == (K,) and K != J):
            return contrast_measure(P, t)
        # K == J and no `kind`: the two readings cannot be told apart (found by a test: a measure
        # was silently re-read as a contrast).  Refuse rather than guess.
        raise ValueError("ambiguous target: pass kind='measure' or kind='contrast'")

    tlist = target if isinstance(target, (list, tuple)) else [target]
    nus = [as_measure(t) for t in tlist]
    mode = objective or ("sum" if len(nus) > 1 else "single")
    floor = 1e-9 * budget / a.sum()

    def val_grad(s):
        se = np.where(s > 10 * floor, s, 0.0)
        vals = np.array([variance(P, se, nu) for nu in nus])
        grads = np.array([state_variances(P, se, nu) for nu in nus])
        if mode in ("single", "sum"):
            return float(vals.sum()), grads.sum(axis=0), vals
        j = int(np.argmax(vals))
        return float(vals[j]), grads[j], vals

    def eff(V, g):
        if not np.isfinite(V) or not np.all(np.isfinite(g)):
            return -np.inf
        top = float(np.max(g / a))
        lin = 2.0 - (g @ lo + (budget - a @ lo) * top) / V
        return max(lin, (V / budget) / top) if not lo.any() else lin

    s = np.full(K, budget / a.sum()) if s0 is None else np.asarray(s0, float).copy()
    s = np.maximum(s, np.maximum(lo, floor))
    s *= budget / (a @ s)
    step, best, it = 0.5, None, 0
    for it in range(iters):
        V, g, vals = val_grad(s)
        e = eff(V, g) if mode != "max" else -np.inf
        if best is None or V < best[0]:
            best = (V, s.copy(), g, e, vals)
        if 1 - e < tol:
            break
        if not np.all(np.isfinite(g)):
            g = np.where(np.isfinite(g), g, 10 * np.nanmax(np.where(np.isfinite(g), g, 0)) + 1.0)
        t = np.maximum(s, floor) * (np.maximum(g, 0) / a) ** step
        free = np.ones(K, bool)
        new = t
        for _ in range(K + 1):
            rem = budget - a[~free] @ lo[~free]
            scale = rem / max(a[free] @ t[free], 1e-300)
            new = np.where(free, t * scale, lo)
            viol = free & (new < lo - 1e-15)
            if not viol.any():
                break
            free &= ~viol
        s = np.maximum(new, np.maximum(lo, floor))
        if mode == "max" and it % 50 == 49:
            step = max(step * 0.9, 0.05)
    V, s, g, e, vals = best
    s = np.where(s > 10 * floor, s, lo)
    if (a @ s) > 0:
        s = lo + (s - lo) * (budget - a @ lo) / max(a @ (s - lo), 1e-300)
    V = val_grad(s)[0]                                  # the value AT the returned allocation
    return s, V, dict(iterations=it + 1, kkt_gap=float(1 - e), efficiency_lower_bound=float(e),
                      multiplier=V / budget, state_variances=g, values=vals, mode=mode)


def elfving_value(P, c, cost=None, budget=1.0):
    """Both sides of the Elfving-type identity (Theorem A5) by a generic conic solver:
       primal  (1/B) (min_{r in F_c} sum_k sqrt(a_k) ||r_k||_{L2(p_k)})^2
       dual    (1/B) (max { sum_k c_k E_k h : Var_k(h) <= a_k for all k })^2
    Returns (primal, dual, s_primal); s_primal is the allocation read off the primal solution."""
    import cvxpy as cp
    P = np.asarray(P, float)
    K, J = P.shape
    a = np.ones(K) if cost is None else np.asarray(cost, float)
    c = np.asarray(c, float)
    r = cp.Variable((K, J))
    sq = np.sqrt(P)
    cons = [cp.sum(cp.multiply(P, r), axis=1) == 0, cp.sum(cp.multiply(P, r), axis=0) == -(c @ P)]
    cons += [r[k, x] == 0 for k in range(K) for x in range(J) if P[k, x] == 0]
    obj = cp.sum([np.sqrt(a[k]) * cp.norm(cp.multiply(sq[k], r[k]), 2) for k in range(K)])
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=cp.CLARABEL)
    norms = np.array([np.linalg.norm(sq[k] * r.value[k]) for k in range(K)])
    sp = norms / np.sqrt(a)
    sp = sp * budget / (a @ sp)
    h = cp.Variable(J)
    dcons = []
    for k in range(K):
        Qk = np.diag(P[k]) - np.outer(P[k], P[k])
        w, E = np.linalg.eigh(Qk)
        root = E[:, w > 1e-14] * np.sqrt(w[w > 1e-14])
        dcons.append(cp.norm(root.T @ h, 2) <= np.sqrt(a[k]))
    dprob = cp.Problem(cp.Maximize((P.T @ c) @ h), dcons)
    dprob.solve(solver=cp.CLARABEL)
    return float(prob.value**2 / budget), float(dprob.value**2 / budget), sp


def efficient_rounding(s, budget, cost=None):
    """Integer counts with cost.n <= budget and V(n) <= V(s) B/(B - sum a) for any continuous
    allocation s with cost.s = B (Proposition A8): n_k = ceil(s_k (B - sum a)/B)."""
    s = np.asarray(s, float)
    a = np.ones_like(s) if cost is None else np.asarray(cost, float)
    B = float(budget)
    if B <= a.sum():
        raise ValueError("budget too small to round")
    cont = s * (B - a.sum()) / (a @ s)
    n = np.ceil(cont - 1e-12).astype(int)
    assert a @ n <= B * (1 + 1e-12)
    return n
