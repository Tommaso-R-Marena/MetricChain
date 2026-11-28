"""Ratio-constrained (bounded-influence) classes of weights, and geometric stress observables.

Section 9 of docs/engineering/phase2/CERTIFIED_INFERENCE.md.  The class is

    { p proportional to pi * r :  r >= 0,  r(x) <= C_e * r(y) for every ordered pair e = (x, y) of ``edges`` },

i.e. the residual energy -ln r is Lipschitz for the costs ln C.  The theory division's class of u-Lipschitz
residuals on the cube is the case of the Hamming graph with C = exp(u).
"""
from __future__ import annotations

import math

import numpy as np
from scipy import sparse
from scipy.optimize import linprog, minimize

from .core import Box, dh_sup, _vec

__all__ = ["hypercube", "lp_ratio_class", "additive_interval", "projection_stress", "stress_values", "sq_distances"]


def hypercube(n: int):
    """(states as an array of 0/1 of shape (2^n, n), ordered pairs (x, y) of neighbours, the site each pair flips)."""
    idx = np.arange(1 << n)
    states = ((idx[:, None] >> np.arange(n)[None, :]) & 1).astype(float)
    x = np.repeat(idx, n)
    site = np.tile(np.arange(n), 1 << n)
    return states, np.column_stack([x, x ^ (1 << site)]), site


def lp_ratio_class(pi, edges, C, f, phi=None, box: Box | None = None):
    """The identified interval over a ratio-constrained class, by the primal linear programme (variables: the
    normalised weights w = pi * r).  Returns (lo, hi), or None if no ensemble of the class meets the box."""
    pi, f = _vec(pi), _vec(f)
    n = pi.size
    edges = np.asarray(edges, dtype=int).reshape(-1, 2)
    C = np.broadcast_to(np.asarray(C, dtype=float), (len(edges),))
    k = len(edges)
    a = sparse.csr_matrix((np.concatenate([1.0 / pi[edges[:, 0]], -C / pi[edges[:, 1]]]),
                           (np.concatenate([np.arange(k), np.arange(k)]), np.concatenate([edges[:, 0], edges[:, 1]]))), shape=(k, n))
    a_ub, b_ub = [a], [np.zeros(k)]
    if phi is not None and box is not None and box.m:
        phi = np.asarray(phi, dtype=float).reshape(n, -1)
        a_ub += [sparse.csr_matrix(phi.T), sparse.csr_matrix(-phi.T)]
        b_ub += [box.c + box.e, -(box.c - box.e)]
    out = []
    for sign in (1.0, -1.0):
        res = linprog(sign * f, A_ub=sparse.vstack(a_ub, format="csr"), b_ub=np.concatenate(b_ub),
                      A_eq=sparse.csr_matrix(np.ones((1, n))), b_eq=[1.0], bounds=[(0, None)] * n, method="highs")
        if res.status == 2:
            return None
        if res.status != 0:
            raise RuntimeError(res.message)
        out.append(sign * res.fun)
    return out[0], out[1]


def additive_interval(site_pi, site_u, f_sites, phi_sites=None, region=None) -> dict:
    """Corollary 9.3: product reference, influence at most site_u[i] at site i, additive target f = sum_i f_i(x_i)
    and additive measured observables phi = sum_i phi_i(x_i).  Exact at any number of sites:

        V+ = inf_eta [ h_R(eta) + sum_i max{ E_{p_i}(f_i - eta . phi_i) : p_i in the one-site class } ].

    ``f_sites[i]`` has shape (states of site i,), ``phi_sites[i]`` shape (states of site i, m)."""
    nsite = len(site_pi)
    gam = [math.exp(u) for u in np.broadcast_to(np.asarray(site_u, dtype=float), (nsite,))]
    m = 0 if phi_sites is None or region is None else region.m
    phis = [np.zeros((len(p), 0)) for p in site_pi] if m == 0 else [np.asarray(ph, dtype=float).reshape(len(p), m) for p, ph in zip(site_pi, phi_sites)]

    def upper(fs):
        def value_grad(eta):
            val, mean = (region.h(eta) if m else 0.0), np.zeros(m)
            for pi, g, ph, ga in zip(site_pi, fs, phis, gam):
                v, p = dh_sup(pi, _vec(g) - ph @ eta, ga)
                val += v
                mean += p @ ph
            return val, ((region.grad(eta) - mean) if m else np.zeros(0))

        if m == 0:
            return value_grad(np.zeros(0))[0], np.zeros(0)
        r = minimize(lambda e: value_grad(e)[0], np.zeros(m), jac=lambda e: value_grad(e)[1], method="L-BFGS-B")
        r = minimize(lambda e: value_grad(e)[0], r.x, method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-13, maxiter=3000 * m))
        return float(value_grad(r.x)[0]), np.asarray(r.x, dtype=float)

    hi, eta_hi = upper(f_sites)
    lo, eta_lo = upper([-_vec(g) for g in f_sites])
    return dict(lo=-lo, hi=hi, eta_lo=eta_lo, eta_hi=eta_hi, empty=bool(hi < -lo - 1e-9))


# ---------------------------------------------------------------------------------------------
# Geometric stress observables (the geometry division's Theorems F and G)
# ---------------------------------------------------------------------------------------------
def projection_stress(z) -> np.ndarray:
    """The projection Omega of R^n onto the orthogonal complement of span(1, columns of z), for a reference
    configuration z of n points.  Omega is positive semidefinite, Omega 1 = 0, and tr(X^T Omega X) = 0 exactly for
    the affine images of z: a stress matrix in the sense of the geometry division's Theorem G."""
    z = np.asarray(z, dtype=float)
    q, _ = np.linalg.qr(np.column_stack([np.ones(len(z)), z]))
    return np.eye(len(z)) - q @ q.T


def stress_values(X, omega) -> np.ndarray:
    """tr(X_k^T Omega X_k) = -1/2 sum_{i != j} Omega_ij |x_i - x_j|^2 for configurations X of shape (K, n, dim):
    a linear function of the squared distances, non-negative when Omega is a positive semidefinite stress."""
    X = np.asarray(X, dtype=float)
    return np.einsum("kia,ij,kja->k", X, omega, X)


def sq_distances(X) -> np.ndarray:
    """Squared distances |x_i - x_j|^2, shape (K, n, n)."""
    X = np.asarray(X, dtype=float)
    d = X[:, :, None, :] - X[:, None, :, :]
    return np.einsum("kija,kija->kij", d, d)
