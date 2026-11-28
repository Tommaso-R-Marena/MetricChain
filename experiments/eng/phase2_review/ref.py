"""Independent reference computations for the review of CERTIFIED_INFERENCE.md (REVIEW_A).

Nothing here imports the division's library.  Everything is for tiny enumerated spaces.

Conventions (as in the note): X finite, envelope 0 <= l <= u, observables phi (N x m), target f (N,),
region R a box [ylo, yhi] or a general polyhedron {y : A y <= c}.
"""
from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import linprog, minimize, minimize_scalar


# --------------------------------------------------------------------------------------
# Primal: exact identified interval by a linear programme (Charnes-Cooper transformation)
# --------------------------------------------------------------------------------------

def primal_extreme(l, u, phi, f, A=None, c=None, sense=+1):
    """sup (sense=+1) or inf (sense=-1) of E_p f over p in P(l,u) with A E_p phi <= c.

    Variables: omega (N) = normalised weights, t >= 0 = 1/sum(w).  Constraints
    t*l <= omega <= t*u, sum omega = 1, A (phi^T omega) <= c.
    Returns the optimal value, or None if the identified set is empty.
    """
    l = np.asarray(l, float)
    u = np.asarray(u, float)
    f = np.asarray(f, float)
    N = len(l)
    phi = np.asarray(phi, float).reshape(N, -1)
    rows = []
    rhs = []
    # t*l - omega <= 0
    for x in range(N):
        r = np.zeros(N + 1)
        r[x] = -1.0
        r[N] = l[x]
        rows.append(r)
        rhs.append(0.0)
    # omega - t*u <= 0
    for x in range(N):
        r = np.zeros(N + 1)
        r[x] = 1.0
        r[N] = -u[x]
        rows.append(r)
        rhs.append(0.0)
    if A is not None and phi.shape[1] > 0:
        A = np.asarray(A, float)
        c = np.asarray(c, float)
        for k in range(A.shape[0]):
            r = np.zeros(N + 1)
            r[:N] = phi @ A[k]
            rows.append(r)
            rhs.append(c[k])
    A_eq = np.zeros((1, N + 1))
    A_eq[0, :N] = 1.0
    obj = np.zeros(N + 1)
    obj[:N] = -sense * f
    res = linprog(obj, A_ub=np.array(rows), b_ub=np.array(rhs), A_eq=A_eq, b_eq=[1.0],
                  bounds=[(0, None)] * (N + 1), method="highs")
    if res.status == 2:
        return None
    if res.status != 0:
        raise RuntimeError(f"linprog status {res.status}: {res.message}")
    return float(sense * (-res.fun))


def box_region(ylo, yhi):
    """Polyhedral description A y <= c of the box [ylo, yhi]."""
    ylo = np.atleast_1d(np.asarray(ylo, float))
    yhi = np.atleast_1d(np.asarray(yhi, float))
    m = len(ylo)
    A = np.vstack([np.eye(m), -np.eye(m)])
    c = np.concatenate([yhi, -ylo])
    return A, c


def primal_interval(l, u, phi, f, A=None, c=None):
    hi = primal_extreme(l, u, phi, f, A, c, +1)
    if hi is None:
        return None
    lo = primal_extreme(l, u, phi, f, A, c, -1)
    return lo, hi


def threshold_max(l, u, f):
    """m = 0: sup of E_p f over P(l,u) by enumerating threshold sets (DeRobertis-Hartigan)."""
    l = np.asarray(l, float)
    u = np.asarray(u, float)
    f = np.asarray(f, float)
    best = -np.inf
    for thr in np.concatenate([np.unique(f), [np.inf]]):
        for strict in (True, False):
            up = (f > thr) if strict else (f >= thr)
            w = np.where(up, u, l)
            if w.sum() > 0:
                best = max(best, float((w * f).sum() / w.sum()))
    return best


# --------------------------------------------------------------------------------------
# Dual of the note (section 4): Psi, its root in tau, minimisation over eta
# --------------------------------------------------------------------------------------

def h_box(eta, ylo, yhi):
    eta = np.atleast_1d(np.asarray(eta, float))
    return float(np.sum(np.where(eta >= 0, eta * yhi, eta * ylo)))


def h_ball(eta, y0, rad):
    eta = np.atleast_1d(np.asarray(eta, float))
    return float(eta @ np.atleast_1d(y0) + rad * np.linalg.norm(eta))


def Psi(tau, eta, l, u, phi, f, hR):
    """Psi(tau, eta) = sum_x [u s_+ - l s_-],  s = f - tau - eta.phi + h_R(eta)."""
    N = len(l)
    phi = np.asarray(phi, float).reshape(N, -1)
    eta = np.atleast_1d(np.asarray(eta, float))
    s = f - tau - phi @ eta + hR(eta) if phi.shape[1] else f - tau
    return float(np.sum(u * np.maximum(s, 0) - l * np.maximum(-s, 0)))


def tau_root_exact(cvals, l, u):
    """inf{tau : sum_x u (c_x - tau)_+ - l (c_x - tau)_- <= 0}, exactly (piecewise linear).

    If sum(l) = 0 the function is >= 0 and vanishes for tau >= max{c_x : u_x > 0}.
    """
    cvals = np.asarray(cvals, float)
    l = np.asarray(l, float)
    u = np.asarray(u, float)
    if l.sum() <= 0:
        sup = cvals[u > 0]
        return float(sup.max()) if len(sup) else -np.inf
    order = np.argsort(cvals)
    cs = cvals[order]
    ls = l[order]
    us = u[order]
    # g(tau) = sum_{c>tau} u (c - tau) - sum_{c<tau} l (tau - c); decreasing, piecewise linear.
    def g(tau):
        d = cs - tau
        return float(np.sum(us * np.maximum(d, 0) - ls * np.maximum(-d, 0)))
    # find the interval of breakpoints containing the root
    vals = np.array([g(t) for t in cs])
    if vals[0] <= 0:
        # root at or below the smallest c: slope there is -sum(u)
        tot = us.sum()
        return float(cs[0] + vals[0] / tot) if tot > 0 else float(cs[0])
    k = int(np.max(np.where(vals > 0)[0]))
    if k == len(cs) - 1:
        # root above the largest c: slope -sum(l)
        return float(cs[-1] + vals[-1] / ls.sum())
    # root in (cs[k], cs[k+1]]: linear there with slope -(sum_{i>k} u + sum_{i<=k} l)
    slope = us[k + 1:].sum() + ls[:k + 1].sum()
    return float(cs[k] + vals[k] / slope)


def tau_star(eta, l, u, phi, f, hR):
    N = len(l)
    phi = np.asarray(phi, float).reshape(N, -1)
    eta = np.atleast_1d(np.asarray(eta, float))
    cvals = f - phi @ eta + hR(eta) if phi.shape[1] else np.asarray(f, float)
    return tau_root_exact(cvals, l, u)


def dual_upper(l, u, phi, f, hR, m, starts=None, seed=0):
    """inf_eta tau*(eta) by multi-start derivative-free minimisation (tau* is convex in eta)."""
    if m == 0:
        return tau_star(np.zeros(0), l, u, phi, f, hR), np.zeros(0)
    fun = lambda e: tau_star(e, l, u, phi, f, hR)
    rng = np.random.default_rng(seed)
    best = (np.inf, None)
    if m == 1:
        for scale in (1.0, 10.0, 100.0, 1e3, 1e4):
            res = minimize_scalar(lambda e: fun([e]), bounds=(-scale, scale), method="bounded",
                                  options={"xatol": 1e-12})
            if res.fun < best[0]:
                best = (float(res.fun), np.array([res.x]))
        return best
    if starts is None:
        starts = [np.zeros(m)] + [rng.normal(size=m) * s for s in (1.0, 5.0, 25.0) for _ in range(3)]
    for x0 in starts:
        res = minimize(fun, x0, method="Nelder-Mead",
                       options={"xatol": 1e-11, "fatol": 1e-13, "maxiter": 20000, "maxfev": 40000})
        for _ in range(3):
            res = minimize(fun, res.x, method="Nelder-Mead",
                           options={"xatol": 1e-12, "fatol": 1e-14, "maxiter": 20000, "maxfev": 40000})
        if res.fun < best[0]:
            best = (float(res.fun), res.x.copy())
    return best


def dual_upper_lp_box(l, u, phi, f, ylo, yhi):
    """The same dual written as a linear programme (box region):
    min tau  s.t.  sum_x [u a_x - l b_x] <= 0,  a_x - b_x = f_x - tau - eta.phi_x + eta+.yhi - eta-.ylo.
    Returns (value, eta) or (None, None) when infeasible / unbounded."""
    l = np.asarray(l, float)
    u = np.asarray(u, float)
    N = len(l)
    phi = np.asarray(phi, float).reshape(N, -1)
    m = phi.shape[1]
    ylo = np.atleast_1d(np.asarray(ylo, float))
    yhi = np.atleast_1d(np.asarray(yhi, float))
    # variables: tau (free), eta+ (m), eta- (m), a (N), b (N)
    nv = 1 + 2 * m + 2 * N
    obj = np.zeros(nv)
    obj[0] = 1.0
    A_eq = np.zeros((N, nv))
    b_eq = np.asarray(f, float).copy()
    for x in range(N):
        A_eq[x, 0] = 1.0                       # + tau
        A_eq[x, 1:1 + m] = phi[x] - yhi          # + eta+ . (phi - yhi)
        A_eq[x, 1 + m:1 + 2 * m] = -(phi[x] - ylo)   # - eta- . (phi - ylo)
        A_eq[x, 1 + 2 * m + x] = 1.0             # + a
        A_eq[x, 1 + 2 * m + N + x] = -1.0        # - b
    A_ub = np.zeros((1, nv))
    A_ub[0, 1 + 2 * m:1 + 2 * m + N] = u
    A_ub[0, 1 + 2 * m + N:] = -l
    bounds = [(None, None)] + [(0, None)] * (2 * m + 2 * N)
    res = linprog(obj, A_ub=A_ub, b_ub=[0.0], A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if res.status != 0:
        return None, None
    eta = res.x[1:1 + m] - res.x[1 + m:1 + 2 * m]
    return float(res.fun), eta


# --------------------------------------------------------------------------------------
# Zonotope support functions and exact Hausdorff distance in small dimension
# --------------------------------------------------------------------------------------

def candidate_directions(V):
    """Vertices of the arrangement {lam.v_x = 0} u {lam_i = 0} on the l1 unit sphere (d = 2, 3, 4).

    A positively homogeneous piecewise-linear function with kinks only on these hyperplanes
    attains its extrema over the l1 sphere at these points.
    """
    V = np.asarray(V, float)
    d = V.shape[1]
    H = np.vstack([V, np.eye(d)])
    # remove duplicate / proportional normals
    Hn = H / np.linalg.norm(H, axis=1, keepdims=True)
    keep = []
    for i, h in enumerate(Hn):
        if not any(abs(abs(h @ Hn[j]) - 1.0) < 1e-12 for j in keep):
            keep.append(i)
    H = Hn[keep]
    out = []
    for combo in itertools.combinations(range(len(H)), d - 1):
        M = H[list(combo)]
        # null space of M (dimension 1 if the rows are independent)
        _, sv, vt = np.linalg.svd(M)
        if sv[-1] < 1e-10:
            continue
        lam = vt[-1]
        n1 = np.abs(lam).sum()
        out.append(lam / n1)
        out.append(-lam / n1)
    return np.array(out)


def hausdorff_linf_over_G(V, q, counts):
    """d_{H,inf}(K, K_hat)/G = sup_{|lam|_1 <= 1} | E_q (lam.v)_+ - (1/L) sum_j (lam.v(X_j))_+ |, exact."""
    L = counts.sum()
    coeff = q - counts / L
    lam = candidate_directions(V)
    vals = np.maximum(lam @ V.T, 0.0) @ coeff
    return float(np.max(np.abs(vals)))


def s3_L(eps, d, delta):
    return 2.0 / eps ** 2 * (d * np.log(1 + 8.0 / eps) + np.log(2.0 / delta))


def s3_eps_from_L(L, d, delta):
    """Smallest eps with L >= (2/eps^2)[d ln(1+8/eps) + ln(2/delta)] (bisection)."""
    lo, hi = 1e-9, 1e6
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        if s3_L(mid, d, delta) <= L:
            hi = mid
        else:
            lo = mid
    return hi


def thm31_eps_from_L(L, d, delta):
    return 2 * np.sqrt(2 * np.log(2 * d) / L) + np.sqrt(np.log(2 / delta) / (2 * L))


def thm31_L(eps, d, delta):
    return (2 * np.sqrt(2 * np.log(2 * d)) + np.sqrt(np.log(2 / delta) / 2)) ** 2 / eps ** 2
