"""Exact side of certified inference over box (density-ratio) classes of Boltzmann weights.

Notation and theorem numbers: docs/engineering/phase2/CERTIFIED_INFERENCE.md.

A *problem* is the convex function of Theorem 4.1,

    Psi(tau, eta) = lin(tau, eta) + sum_j wt_j * ( Lw_j * s_j + Gw_j * max(s_j, 0) ),
    s_j           = f_j - tau - eta . phi_j + h_R(eta),
    lin           = b_f - tau * b_0 - eta . b_phi + h_R(eta) * b_0        (absent unless ``b`` is given),

over a list of points j: all configurations of a finite space (``wt = 1``, ``Lw = l``, ``Gw = u - l``), the cells
of a lumping (Proposition 8.1), or a sample (``wt = 1/n``).  ``Psi(tau, eta) <= 0`` for some ``eta`` certifies
``E_p f <= tau`` for every ensemble of the class whose measured averages lie in the region ``R``; the smallest
such ``tau`` is the upper end of the identified interval.  Nothing in this file is statistical.

Floating point throughout: the numbers returned here are *candidates*; what certifies is the sign of ``psi`` at
the returned ``(tau, eta)``, which callers that need rigour evaluate in interval arithmetic (``certify.py``).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
from scipy import sparse
from scipy.optimize import linprog, minimize

__all__ = ["Box", "Ellipsoid", "Sum", "Problem", "box_problem", "psi", "tau_root", "tau_grad", "solve_upper",
           "interval", "lp_dual_box", "lp_primal_box", "phi_value", "find_inconsistency", "lump",
           "product_joint_law", "cells_from_law", "dh_sup"]


def _vec(x) -> np.ndarray:
    return np.asarray(x, dtype=float).reshape(-1)


# ---------------------------------------------------------------------------------------------
# Observation regions, through their support functions h_R(eta) = sup_{y in R} eta . y
# ---------------------------------------------------------------------------------------------
class Box:
    """{y : |y_i - c_i| <= e_i}.  A point (exact data) is a box with e = 0; no observation is a box with m = 0."""

    def __init__(self, centre=(), half=0.0):
        self.c = _vec(centre)
        self.e = np.broadcast_to(np.asarray(half, dtype=float), self.c.shape).astype(float).copy()
        if np.any(self.e < 0):
            raise ValueError("negative half-width")

    @property
    def m(self) -> int:
        return self.c.size

    def h(self, eta) -> float:
        eta = _vec(eta)
        return float(eta @ self.c + np.abs(eta) @ self.e)

    def grad(self, eta) -> np.ndarray:
        eta = _vec(eta)
        return self.c + np.sign(eta) * self.e

    def enlarged(self, kappa: float) -> "Box":
        return Box(self.c, self.e + kappa)

    def contains(self, y, tol: float = 0.0) -> bool:
        return bool(np.all(np.abs(_vec(y) - self.c) <= self.e + tol))


class Ellipsoid:
    """{y : (y - c)^T cov^+ (y - c) <= radius^2}, cov positive semidefinite: correlated measurement errors."""

    def __init__(self, centre, cov, radius: float = 1.0):
        self.c = _vec(centre)
        self.cov = np.atleast_2d(np.asarray(cov, dtype=float))
        self.radius = float(radius)
        if self.cov.shape != (self.c.size, self.c.size):
            raise ValueError("covariance of the wrong shape")

    @property
    def m(self) -> int:
        return self.c.size

    def h(self, eta) -> float:
        eta = _vec(eta)
        return float(eta @ self.c) + self.radius * math.sqrt(max(float(eta @ self.cov @ eta), 0.0))

    def grad(self, eta) -> np.ndarray:
        eta = _vec(eta)
        q = float(eta @ self.cov @ eta)
        return self.c + (self.radius * (self.cov @ eta) / math.sqrt(q) if q > 0 else 0.0)

    def enlarged(self, kappa: float) -> "Sum":
        return Sum(self, Box(np.zeros(self.m), kappa))

    def contains(self, y, tol: float = 0.0) -> bool:
        d = _vec(y) - self.c
        return bool(d @ np.linalg.pinv(self.cov) @ d <= self.radius ** 2 + tol)


class Sum:
    """Minkowski sum of two regions (an ellipsoid enlarged by a box, for instance)."""

    def __init__(self, a, b):
        if a.m != b.m:
            raise ValueError("regions of different dimension")
        self.a, self.b = a, b

    @property
    def m(self) -> int:
        return self.a.m

    def h(self, eta) -> float:
        return self.a.h(eta) + self.b.h(eta)

    def grad(self, eta) -> np.ndarray:
        return self.a.grad(eta) + self.b.grad(eta)

    def enlarged(self, kappa: float) -> "Sum":
        return Sum(self, Box(np.zeros(self.m), kappa))


# ---------------------------------------------------------------------------------------------
# The problem
# ---------------------------------------------------------------------------------------------
@dataclass
class Problem:
    f: np.ndarray                 # target at the points, (n,)
    phi: np.ndarray               # measured observables at the points, (n, m)
    Lw: np.ndarray                # lower weight of a point (l(x), or l/pi at a sampled point)
    Gw: np.ndarray                # gap u - l (or (u - l)/pi)
    region: object
    wt: np.ndarray | None = None  # multiplicity of a point: 1 for a population, 1/n for a sample
    b: np.ndarray | None = None   # exact part (b_0, b_phi, b_f) of Psi, if any (gap sampling)

    def __post_init__(self):
        self.f = _vec(self.f)
        n = self.f.size
        self.phi = np.asarray(self.phi, dtype=float).reshape(n, -1)
        self.Lw = np.broadcast_to(np.asarray(self.Lw, dtype=float), (n,)).astype(float).copy()
        self.Gw = np.broadcast_to(np.asarray(self.Gw, dtype=float), (n,)).astype(float).copy()
        self.wt = np.ones(n) if self.wt is None else np.broadcast_to(np.asarray(self.wt, dtype=float), (n,)).astype(float).copy()
        if self.b is not None:
            self.b = _vec(self.b)
            if self.b.size != self.m + 2:
                raise ValueError("b must be (b_0, b_phi, b_f)")
        if self.region.m != self.m:
            raise ValueError(f"region of dimension {self.region.m} for {self.m} observables")
        if np.any(self.Lw < 0) or np.any(self.Gw < 0) or np.any(self.wt < 0):
            raise ValueError("weights must be non-negative")

    @property
    def m(self) -> int:
        return self.phi.shape[1]

    def s0(self, eta) -> np.ndarray:
        """The score at tau = 0."""
        eta = _vec(eta)
        return self.f - self.phi @ eta + self.region.h(eta)

    def lin(self, eta) -> tuple[float, float]:
        """(A, C) with lin(tau, eta) = C - A * tau."""
        if self.b is None:
            return 0.0, 0.0
        eta = _vec(eta)
        b0, bphi, bf = self.b[0], self.b[1:-1], self.b[-1]
        return float(b0), float(bf - eta @ bphi + self.region.h(eta) * b0)

    def negated(self) -> "Problem":
        """The same problem for the target -f (lower end of the interval)."""
        b = None if self.b is None else np.concatenate([self.b[:-1], [-self.b[-1]]])
        return replace(self, f=-self.f, b=b)


def box_problem(l, u, f, phi, region) -> Problem:
    """The population problem of the box class l <= w <= u on an enumerated space."""
    l, u = _vec(l), _vec(u)
    if np.any(u < l):
        raise ValueError("u < l somewhere")
    return Problem(f=f, phi=phi, Lw=l, Gw=u - l, region=region)


def psi(P: Problem, tau: float, eta) -> float:
    s = P.s0(eta) - tau
    a, c = P.lin(eta)
    return float((P.wt * (P.Lw * s + P.Gw * np.maximum(s, 0.0))).sum()) + c - a * tau


def tau_root(P: Problem, eta) -> float:
    """inf{tau : Psi(tau, eta) <= 0}, exactly (Psi is piecewise linear, convex and non-increasing in tau).
    -inf if Psi <= 0 for every tau, +inf if for none."""
    s0 = P.s0(eta)
    lw, gw = P.wt * P.Lw, P.wt * P.Gw
    a, c = P.lin(eta)
    a += float(lw.sum())
    c += float(lw @ s0)
    order = np.argsort(-s0, kind="stable")
    ss, gg = s0[order], gw[order]
    cg, cs = np.cumsum(gg), np.cumsum(gg * ss)
    at = np.maximum.accumulate(c + cs - (a + cg) * ss)       # Psi at tau = ss[k]: non-decreasing in k
    k = int(np.searchsorted(at, 0.0, side="right"))           # the breakpoints at which Psi <= 0 are a prefix
    num = c + (cs[k - 1] if k else 0.0)
    den = a + (cg[k - 1] if k else 0.0)
    if den <= 0.0:
        return -math.inf if num <= 0.0 else math.inf
    return float(num / den)


def tau_grad(P: Problem, eta, tau: float | None = None) -> np.ndarray:
    """A subgradient of eta -> tau_root(eta): grad h_R(eta) minus the measured averages of the extremal ensemble."""
    eta = _vec(eta)
    tau = tau_root(P, eta) if tau is None else tau
    s = P.s0(eta) - tau
    om = P.wt * (P.Lw + P.Gw * (s > 0))
    tot, mean = float(om.sum()), om @ P.phi
    if P.b is not None:
        tot, mean = tot + P.b[0], mean + P.b[1:-1]
    return P.region.grad(eta) - mean / tot


def lp_dual_box(P: Problem) -> tuple[float, np.ndarray]:
    """min tau subject to Psi(tau, eta) <= 0, as a linear programme; box regions only.  Exact up to the solver.
    Returns (-inf, eta) when the programme is unbounded: then every tau is certified and the identified set is empty."""
    box = P.region
    if not isinstance(box, Box):
        raise TypeError("lp_dual_box needs a Box region")
    n, m = P.f.size, P.m
    if m == 0:
        return tau_root(P, np.zeros(0)), np.zeros(0)
    lw, gw = P.wt * P.Lw, P.wt * P.Gw
    b0, bphi, bf = (P.b[0], P.b[1:-1], P.b[-1]) if P.b is not None else (0.0, np.zeros(m), 0.0)
    up = (box.c + box.e)[None, :] - P.phi            # coefficient of eta+ in s_j
    dn = (box.e - box.c)[None, :] + P.phi            # coefficient of eta- in s_j
    cost = np.zeros(1 + 2 * m + n)
    cost[0] = 1.0
    rows = sparse.hstack([sparse.csr_matrix(-np.ones((n, 1))), sparse.csr_matrix(up), sparse.csr_matrix(dn),
                          -sparse.identity(n, format="csr")], format="csr")          # s_j - z_j <= 0
    last = np.concatenate([[-(lw.sum() + b0)], lw @ up + (box.c + box.e) * b0 - bphi, lw @ dn + (box.e - box.c) * b0 + bphi, gw])
    res = linprog(cost, A_ub=sparse.vstack([rows, sparse.csr_matrix(last)], format="csr"),
                  b_ub=np.concatenate([-P.f, [-(lw @ P.f + bf)]]),
                  bounds=[(None, None)] + [(0, None)] * (2 * m + n), method="highs")
    if res.status == 3:
        return -math.inf, np.zeros(m)
    if res.status != 0:
        raise RuntimeError(f"linear programme failed: {res.message}")
    eta = res.x[1:1 + m] - res.x[1 + m:1 + 2 * m]
    return tau_root(P, eta), eta


def solve_upper(P: Problem, method: str = "auto") -> tuple[float, np.ndarray]:
    """A pair (tau, eta) with Psi(tau, eta) <= 0 and tau as small as the optimiser finds it.  Whatever the optimiser
    does, tau = tau_root(P, eta), so the pair is a certificate of Theorem 4.1(a) for the points of P."""
    if P.m == 0:
        return tau_root(P, np.zeros(0)), np.zeros(0)
    if method == "auto":
        method = "lp" if isinstance(P.region, Box) and P.f.size <= 20_000 else "descent"      # the programme is exact but slow beyond that
    if method == "lp":
        return lp_dual_box(P)
    best_t, best_e = tau_root(P, np.zeros(P.m)), np.zeros(P.m)

    def fun(e):
        t = tau_root(P, e)
        return t if math.isfinite(t) else (1e300 if t > 0 else -1e300)

    for start in (np.zeros(P.m),):
        r = minimize(fun, start, jac=lambda e: tau_grad(P, e), method="L-BFGS-B")
        r = minimize(fun, r.x, method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-13, maxiter=3000 * P.m))
        r = minimize(fun, r.x, jac=lambda e: tau_grad(P, e), method="L-BFGS-B")
        t = tau_root(P, r.x)
        if t < best_t:
            best_t, best_e = t, np.asarray(r.x, dtype=float)
    return best_t, best_e


def interval(P: Problem, method: str = "auto") -> dict:
    """Both ends of the identified interval of the points of P, with their multipliers; 'empty' if they cross."""
    hi, eta_hi = solve_upper(P, method)
    lo, eta_lo = solve_upper(P.negated(), method)
    lo = -lo
    scale = max([1.0] + [abs(x) for x in (lo, hi) if math.isfinite(x)])
    empty = hi == -math.inf or lo == math.inf or hi < lo - 1e-9 * scale       # every tau certified: no ensemble at all
    return dict(lo=lo, hi=hi, eta_lo=eta_lo, eta_hi=eta_hi, empty=bool(empty))


def lp_primal_box(l, u, f, phi, box: Box):
    """The identified interval by the primal programme (Charnes-Cooper): an independent route used as ground truth
    in tests.  Returns (lo, hi), or None if no ensemble of the class has its measured averages in the box."""
    l, u, f = _vec(l), _vec(u), _vec(f)
    n = f.size
    phi = np.asarray(phi, dtype=float).reshape(n, -1)
    eye = sparse.identity(n, format="csr")
    a_ub = [sparse.hstack([eye, sparse.csr_matrix(-u.reshape(-1, 1))]), sparse.hstack([-eye, sparse.csr_matrix(l.reshape(-1, 1))])]
    b_ub = [np.zeros(n), np.zeros(n)]
    if phi.shape[1]:
        z = np.zeros((phi.shape[1], 1))
        a_ub += [sparse.csr_matrix(np.hstack([phi.T, z])), sparse.csr_matrix(np.hstack([-phi.T, z]))]
        b_ub += [box.c + box.e, -(box.c - box.e)]
    a_eq = sparse.csr_matrix(np.concatenate([np.ones(n), [0.0]])[None, :])
    out = []
    for sign in (1.0, -1.0):
        res = linprog(np.concatenate([sign * f, [0.0]]), A_ub=sparse.vstack(a_ub, format="csr"), b_ub=np.concatenate(b_ub),
                      A_eq=a_eq, b_eq=[1.0], bounds=[(0, None)] * (n + 1), method="highs")
        if res.status == 2:
            return None
        if res.status != 0:
            raise RuntimeError(res.message)
        out.append(sign * res.fun)
    return out[0], out[1]


# ---------------------------------------------------------------------------------------------
# Inconsistency of data and class (Theorem 4.1(e))
# ---------------------------------------------------------------------------------------------
def phi_value(P: Problem, eta) -> float:
    """Phi(eta) = sum [ l t_+ - u t_- ], t = eta . phi - h_R(eta).  A positive value certifies that no ensemble of
    the class has its measured averages in the region."""
    eta = _vec(eta)
    h = P.region.h(eta)
    t = P.phi @ eta - h
    val = float((P.wt * (P.Lw * t - P.Gw * np.maximum(-t, 0.0))).sum())
    if P.b is not None:
        val += float(eta @ P.b[1:-1]) - h * P.b[0]
    return val


def find_inconsistency(P: Problem, seed: int = 0) -> tuple[float, np.ndarray]:
    """The largest Phi(eta) found over unit vectors eta, and the vector.  Phi is concave and positively homogeneous."""
    if P.m == 0:
        return -math.inf, np.zeros(0)

    def fun(e):
        nrm = float(np.linalg.norm(e))
        return 0.0 if nrm == 0 else -phi_value(P, e / nrm)

    rng = np.random.default_rng(seed)
    om = P.wt * (P.Lw + 0.5 * P.Gw)
    guess = (om @ P.phi) / max(float(om.sum()), 1e-300) - (P.region.grad(np.zeros(P.m)))
    starts = [guess, -guess] + [v for i in range(P.m) for v in (np.eye(P.m)[i], -np.eye(P.m)[i])] + [rng.normal(size=P.m) for _ in range(2)]
    best, arg = -math.inf, np.zeros(P.m)
    for s in starts:
        if not np.any(s):
            continue
        r = minimize(fun, s, method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-13, maxiter=2000 * P.m))
        if -r.fun > best:
            best, arg = -r.fun, r.x / np.linalg.norm(r.x)
    return float(best), arg


# ---------------------------------------------------------------------------------------------
# Deterministic reductions (Proposition 8.1) and one-site problems
# ---------------------------------------------------------------------------------------------
def lump(P: Problem) -> Problem:
    """Merge points with equal (phi, f): the problem is unchanged (Proposition 8.1)."""
    key = np.column_stack([P.phi, P.f])
    uniq, inv = np.unique(key, axis=0, return_inverse=True)
    inv = np.asarray(inv).reshape(-1)
    return Problem(f=uniq[:, -1], phi=uniq[:, :-1], Lw=np.bincount(inv, weights=P.wt * P.Lw, minlength=len(uniq)),
                   Gw=np.bincount(inv, weights=P.wt * P.Gw, minlength=len(uniq)), region=P.region, b=P.b)


def product_joint_law(site_probs, site_stats) -> np.ndarray:
    """Law of the integer vector S = sum_i stats_i[x_i] when the sites are independent with laws site_probs[i].
    ``site_stats[i]`` has shape (states of site i, r) with non-negative integer entries.  Returns the array of
    P(S = k) indexed by k: level counts of a product reference, by convolution."""
    stats = [np.asarray(st, dtype=int).reshape(len(p), -1) for p, st in zip(site_probs, site_stats)]
    r = stats[0].shape[1]
    if any(st.shape[1] != r or st.min(initial=0) < 0 for st in stats):
        raise ValueError("statistics must be non-negative integer vectors of one length")
    total = sum(st.max(axis=0) for st in stats)
    law = np.zeros(tuple(int(t) + 1 for t in total))
    law[(0,) * r] = 1.0
    cur = np.zeros(r, dtype=int)
    for probs, st in zip(site_probs, stats):
        new = np.zeros_like(law)
        src = tuple(slice(0, int(c) + 1) for c in cur)
        for pa, sa in zip(probs, st):
            new[tuple(slice(int(s), int(s) + int(c) + 1) for s, c in zip(sa, cur))] += pa * law[src]
        law, cur = new, cur + st.max(axis=0)
    return law


def cells_from_law(law: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(integer statistics of the occupied cells, their probabilities)."""
    idx = np.argwhere(law > 0)
    return idx, law[tuple(idx.T)]


def dh_sup(pi, g, gamma: float) -> tuple[float, np.ndarray]:
    """max E_p g over p proportional to pi * r with max r / min r <= gamma (one site; the threshold rule), and a
    maximising p."""
    pi, g = _vec(pi), _vec(g)
    order = np.argsort(-g, kind="stable")
    best, arg = -math.inf, None
    for k in range(len(g) + 1):
        w = pi.copy()
        w[order[:k]] *= gamma
        val = float(w @ g / w.sum())
        if val > best + 1e-15:
            best, arg = val, w / w.sum()
    return best, arg
