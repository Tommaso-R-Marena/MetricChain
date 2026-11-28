"""Sample-based multistate estimation: an MBAR solver, the fitted (NPMLE) distributions, plug-in
variances at arbitrary allocations, and pilot-based allocation.  Division 9; float64.

Data convention: U[n, k] = reduced potential -log q_k(x_n) of pooled sample n in state k
(+inf allowed: q_k(x_n) = 0), labels[n] = state that produced sample n.
"""
from __future__ import annotations

import numpy as np
from scipy.sparse.csgraph import connected_components
from scipy.special import logsumexp

from . import population as pop

__all__ = ["support_strongly_connected", "minimize_lse", "mbar", "fitted_distributions",
           "plugin_variance", "pilot_allocation", "integer_counts"]


def _validate(U, labels):
    U = np.asarray(U, float)
    labels = np.asarray(labels, int)
    if U.ndim != 2 or U.shape[0] != labels.shape[0] or U.shape[0] == 0 or U.shape[1] < 2:
        raise ValueError("shape")
    K = U.shape[1]
    if labels.min() < 0 or labels.max() >= K or np.isnan(U).any() or np.isneginf(U).any():
        raise ValueError("invalid labels or energies")
    if not np.all(np.isfinite(U[np.arange(len(U)), labels])):
        raise ValueError("a sample has infinite energy in its own state")
    return U, labels, K


def support_strongly_connected(U, labels, states=None):
    """E1 of the handoff (Vardi's condition): a unique finite optimiser exists iff the directed graph
    i -> j (some draw of state i has q_j > 0) restricted to the sampled states is strongly connected."""
    U, labels, K = _validate(U, labels)
    sampled = np.unique(labels) if states is None else np.asarray(states)
    G = np.array([[np.any(np.isfinite(U[labels == i, j])) for j in sampled] for i in sampled])
    return connected_components(G, directed=True, connection="strong")[0] == 1


def minimize_lse(A, target, f0=None, tol=1e-11, maxit=200, constraint=None):
    """Minimise  Psi(f) = mean_n LSE_j(A[n, j] + f_j) - target.f  over the gauge sum(f[cols]) = 0,
    where cols = columns with target > 0 or any finite entry.  Optionally subject to
    constraint = (c, theta):  c.f = theta.  Damped Newton on the gauge space.
    Returns (f, value, info).  Columns that are -inf everywhere are fixed at 0."""
    A = np.asarray(A, float)
    N, K = A.shape
    t = np.asarray(target, float)
    live = np.isfinite(A).any(axis=0)
    f = np.zeros(K) if f0 is None else np.asarray(f0, float).copy()
    f[~live] = 0.0
    idx = np.where(live)[0]
    k = len(idx)
    Jm = np.full((k, k), 1.0 / k)
    cvec = None
    if constraint is not None:
        cvec, theta = np.asarray(constraint[0], float)[idx], float(constraint[1])
        # start from a feasible point
        f[idx] += cvec * (theta - cvec @ f[idx]) / (cvec @ cvec)

    def psi(fv):
        return float(logsumexp(A[:, idx] + fv, axis=1).mean() - t[idx] @ fv)

    fv = f[idx] - f[idx].mean() if cvec is None else f[idx]
    val = psi(fv)
    info = dict(converged=False, iterations=0, grad=np.inf)
    for it in range(maxit):
        Z = A[:, idx] + fv
        p = np.exp(Z - logsumexp(Z, axis=1)[:, None])
        g = p.mean(axis=0) - t[idx]
        H = np.diag(p.mean(axis=0)) - p.T @ p / N
        if cvec is None:
            d = -np.linalg.solve(H + Jm, g)
            gnorm = float(np.max(np.abs(g)))
        else:
            # KKT step: minimise g.d + d.H.d/2  s.t. c.d = 0, 1.d = 0 (gauge)
            C = np.vstack([cvec, np.ones(k)])
            M = np.block([[H + 1e-14 * np.eye(k), C.T], [C, np.zeros((2, 2))]])
            sol = np.linalg.lstsq(M, np.concatenate([-g, [0.0, 0.0]]), rcond=None)[0]
            d = sol[:k]
            lam = sol[k:]
            gnorm = float(np.max(np.abs(g + C.T @ lam)))
        dec = -(g @ d)                      # Newton decrement: Psi - min Psi ~ dec / 2
        info.update(iterations=it + 1, grad=gnorm, decrement=float(dec), step=float(np.max(np.abs(d))))
        if gnorm < tol or dec < 1e-14:
            # at the minimum to the precision of the objective; `step` estimates the error of f
            info["converged"] = True
            break
        step = 1.0
        while step > 1e-12:
            new = fv + step * d
            nv = psi(new)
            if np.isfinite(nv) and nv <= val - 1e-4 * step * dec:
                break
            step /= 2
        else:
            break
        fv, val = new, nv
    f[idx] = fv
    info["value"] = val
    return f, val, info


def mbar(U, labels, f0=None, tol=1e-11, check_support=True):
    """MBAR / Vardi NPMLE / reverse logistic regression estimate of f_k = -log Z_k (gauge f[0] = 0)
    for the sampled states; unsampled states are filled in from the fitted base measure.
    Raises ValueError if the unique finite optimiser does not exist."""
    U, labels, K = _validate(U, labels)
    n = np.bincount(labels, minlength=K)
    N = n.sum()
    if check_support and not support_strongly_connected(U, labels):
        raise ValueError("directed support graph of the sampled states is not strongly connected")
    with np.errstate(divide="ignore"):
        logw = np.log(n / N)
    A = logw[None, :] - U
    f, val, info = minimize_lse(A, n / N, f0=f0, tol=tol)
    if not info["converged"]:
        raise RuntimeError(f"MBAR Newton did not converge (max |grad| = {info['grad']:.2e})")
    # unsampled states: Z_k = int q_k dG_hat,  G_hat({x_n}) = 1 / sum_j n_j exp(f_j - U[n, j])
    samp = n > 0
    logg = -logsumexp(np.log(n[samp])[None, :] + f[samp][None, :] - U[:, samp], axis=1)
    for k in np.where(~samp)[0]:
        f[k] = -logsumexp(logg - U[:, k])
    f = f - f[np.where(samp)[0][0]]
    info["counts"] = n
    return f, info


def fitted_distributions(U, labels, f=None):
    """P_hat[k, n] = fitted probability of pooled point n under state k (rows sum to 1), from the
    NPMLE of the base measure.  Works for sampled and unsampled states (finite energies somewhere)."""
    U, labels, K = _validate(U, labels)
    if f is None:
        f, _ = mbar(U, labels)
    n = np.bincount(labels, minlength=K)
    samp = n > 0
    logg = -logsumexp(np.log(n[samp])[None, :] + f[samp][None, :] - U[:, samp], axis=1)
    logP = logg[None, :] - U.T
    logP -= logsumexp(logP, axis=1)[:, None]
    return np.exp(logP)


def plugin_variance(U, labels, target, counts=None, f=None, P=None):
    """Plug-in variance of the MBAR estimate of a contrast (length-K vector) at sample counts
    `counts` (default: the actual counts) -- the fitted distributions inserted in V (part A).
    At the actual counts this is the standard MBAR asymptotic variance estimate."""
    U, labels, K = _validate(U, labels)
    if P is None:
        P = fitted_distributions(U, labels, f)
    n = np.bincount(labels, minlength=K).astype(float) if counts is None else np.asarray(counts, float)
    return pop.variance(P, n, pop.contrast_measure(P, np.asarray(target, float)))


def integer_counts(extra, budget, cost):
    """Largest-remainder rounding of nonnegative real `extra` to integers with cost.n <= budget."""
    extra = np.maximum(np.asarray(extra, float), 0.0)
    cost = np.asarray(cost, float)
    n = np.floor(extra + 1e-9).astype(int)
    left = budget - cost @ n
    order = np.argsort(-(extra - n))
    progress = True
    while progress:
        progress = False
        for k in order:
            if cost[k] <= left + 1e-9:
                n[k] += 1
                left -= cost[k]
                progress = True
                break
        order = np.argsort(-(extra - n))
    return n


def pilot_allocation(U, labels, target, total_budget, cost=None, safeguard=0.25, objective=None):
    """Second-stage allocation from pilot data only (no population quantity).

    Fits MBAR to the pilot, inserts the fitted distributions in V, minimises the plug-in V over
    allocations that keep the pilot samples (s >= pilot counts) and spend `total_budget` in total,
    then mixes the additional samples with a cost-uniform split:  extra = (1 - safeguard) * plug-in
    + safeguard * uniform.  The mixture guarantees V(final) <= V(uniform final)/safeguard whatever
    the pilot says (Proposition A9).  Returns (extra_counts, info)."""
    U, labels, K = _validate(U, labels)
    a = np.ones(K) if cost is None else np.asarray(cost, float)
    n0 = np.bincount(labels, minlength=K).astype(float)
    spent = float(a @ n0)
    if total_budget <= spent:
        raise ValueError("pilot already exhausts the budget")
    rem = total_budget - spent
    uniform_extra = np.full(K, rem / a.sum())
    info = dict(pilot_counts=n0.astype(int), fallback=None)
    try:
        f, _ = mbar(U, labels)
        P = fitted_distributions(U, labels, f)
        tl = target if isinstance(target, (list, tuple)) else [target]
        nus = [pop.contrast_measure(P, np.asarray(t, float)) for t in tl]
        s, V, oinfo = pop.optimal_allocation(P, nus if len(nus) > 1 else nus[0], cost=a,
                                             budget=total_budget, lower=n0, objective=objective,
                                             iters=3000, tol=1e-6)
        if not np.isfinite(V):
            raise ValueError("plug-in variance infinite")
        plug_extra = np.maximum(s - n0, 0.0)
        plug_extra *= rem / max(a @ plug_extra, 1e-300)
        info.update(plugin_allocation=s, plugin_variance=V, f_pilot=f,
                    efficiency_lower_bound=oinfo["efficiency_lower_bound"],
                    plugin_variance_uniform=float(sum(pop.variance(P, n0 + uniform_extra, nu) for nu in nus)))
    except (ValueError, RuntimeError, np.linalg.LinAlgError) as err:   # fail closed: uniform
        plug_extra = uniform_extra
        info["fallback"] = repr(err)
    extra = (1 - safeguard) * plug_extra + safeguard * uniform_extra
    counts = integer_counts(extra, rem, a)
    info["extra_real"] = extra
    return counts, info
