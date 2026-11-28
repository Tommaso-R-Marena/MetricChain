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


def minimize_lse(A, target, f0=None, tol=1e-10, maxit=300, constraint=None, steptol=1e-8):
    """Minimise  Psi(f) = mean_n LSE_j(A[n, j] + f_j) - target.f  over the gauge sum(f) = 0 of the
    live columns (those with a finite entry), optionally subject to constraint = (c, theta): c.f = theta.
    `target` must be a probability vector on the live columns (it always is in this package).
    Returns (f, value, info).  Columns that are -inf everywhere are fixed at 0.

    Design, after the referee's finding (REVIEW_A.md, E1: a Newton iteration started at f = 0 on
    energies that differ by state-dependent constants met a numerically zero Hessian, and a negative
    "decrement" from a meaningless solve was read as convergence):
      * the default starting point is equivariant under per-state energy offsets (every column's
        largest logit is 0) and is followed by a few steps of generalised iterative scaling,
        f_j += log(target_j / mean_n pi_j), each of which decreases Psi by at least KL(target || mean pi);
      * Newton steps are computed with Levenberg-Marquardt regularisation, increased until the linear
        solve is consistent and the step is a descent direction; Armijo backtracking on Psi, and near
        the precision floor of Psi a full step is accepted if it at least halves the gradient;
      * info['converged'] is True only if the gradient is below `tol`, or an UNREGULARISED Newton
        system was solved consistently and its solution -- the estimated distance to the minimiser --
        is below `steptol`.  Nothing else counts as convergence; no exception of the linear algebra
        escapes."""
    A = np.asarray(A, float)
    N, K = A.shape
    t = np.asarray(target, float)
    live = np.isfinite(A).any(axis=0)
    idx = np.where(live)[0]
    k = len(idx)
    f = np.zeros(K)
    info = dict(converged=False, iterations=0, grad=np.inf, step=np.inf, regularisation=0.0, gis_steps=0)
    if k == 0:
        info["value"] = np.nan
        return f, np.nan, info
    tl = t[idx]
    # Internal coordinates: f = shift + fv with shift_j = -max_n A[n, j], so that every column of
    # the shifted logits has maximum 0.  The problem is then invariant under per-state energy
    # offsets (they are absorbed in `shift`), and no large numbers are added and subtracted inside
    # the iteration.
    shift = -np.max(A[:, idx], axis=0)
    Al = A[:, idx] + shift
    logN = np.log(N)
    val_const = float(tl @ shift)                      # Psi(f) = Psi_shifted(fv) - target.shift

    def stats(fv):
        Z = Al + fv
        lse = logsumexp(Z, axis=1)
        logp = Z - lse[:, None]
        return logp, float(lse.mean() - tl @ fv)

    cvec = theta = None
    if constraint is not None:
        cvec, theta = np.asarray(constraint[0], float)[idx], float(constraint[1])
        if not np.any(cvec != 0):
            raise ValueError("constraint vector vanishes on the live columns")
    if cvec is not None:
        theta = theta - float(cvec @ shift)            # the constraint in internal coordinates
    if f0 is None:
        fv = np.zeros(k)
    else:
        fv = np.asarray(f0, float)[idx] - shift
        fv = np.where(np.isfinite(fv), fv, 0.0)
    fv = fv - fv.mean()
    if cvec is not None:
        fv = fv + cvec * (theta - cvec @ fv) / (cvec @ cvec)
    if k == 1:
        logp, val = stats(fv)
        f[idx] = fv + shift
        info.update(converged=True, grad=0.0, step=0.0, value=val - val_const)
        return f, val - val_const, info

    gis_ok = cvec is None and np.all(tl >= 0) and abs(tl.sum() - 1.0) < 1e-9

    def gis(fv, logp):
        logpbar = logsumexp(logp, axis=0) - logN
        new = fv + np.where(tl > 0, np.log(np.where(tl > 0, tl, 1.0)) - logpbar, 0.0)
        return new - new.mean()

    logp, val = stats(fv)
    if gis_ok and f0 is None:
        for _ in range(25):
            g0 = np.exp(logsumexp(logp, axis=0) - logN) - tl
            if np.max(np.abs(g0)) < 1e-3:
                break
            new = gis(fv, logp)
            logp_new, val_new = stats(new)
            if not np.isfinite(val_new) or val_new > val:
                break
            fv, logp, val = new, logp_new, val_new
            info["gis_steps"] += 1

    Jm = np.full((k, k), 1.0 / k)
    eye = np.eye(k)
    C = None if cvec is None else np.vstack([cvec, np.ones(k)])

    def newton_system(H, g, lam):
        """Step d and projected gradient for regularisation lam; None if the solve is not usable."""
        try:
            if C is None:
                M = H + lam * eye + Jm
                d = np.linalg.solve(M, -g)
                resid = np.max(np.abs(M @ d + g))
                gproj = g
            else:
                M = np.block([[H + lam * eye, C.T], [C, np.zeros((2, 2))]])
                rhs = np.concatenate([-g, [0.0, 0.0]])
                sol = np.linalg.lstsq(M, rhs, rcond=None)[0]
                d, resid = sol[:k], np.max(np.abs(M @ sol - rhs))
                gproj = g + C.T @ sol[k:]
        except np.linalg.LinAlgError:
            return None
        if not (np.all(np.isfinite(d)) and np.isfinite(resid)):
            return None
        if resid > 1e-7 * (np.max(np.abs(g)) + 1e-300) + 1e-13:
            return None
        return d, gproj

    def grad_hess(logp):
        pm = np.exp(logp)
        pbar = pm.mean(axis=0)
        return pbar - tl, np.diag(pbar) - pm.T @ pm / N

    def armijo(d, dec):
        step = 1.0
        while step > 1e-7:
            new = fv + step * d
            logp_new, val_new = stats(new)
            if np.isfinite(val_new) and val_new <= val - 1e-4 * step * dec:
                return new, logp_new, val_new
            step /= 2
        return None

    for it in range(maxit):
        g, H = grad_hess(logp)
        scale = max(float(np.trace(H)) / k, 1e-300)
        s0 = newton_system(H, g, 0.0)
        if s0 is not None:
            gnorm, snorm = float(np.max(np.abs(s0[1]))), float(np.max(np.abs(s0[0])))
        else:
            gnorm, snorm = (float(np.max(np.abs(g))) if C is None else np.inf), np.inf
        info.update(iterations=it + 1, grad=gnorm, step=snorm)
        if gnorm <= tol or snorm <= steptol:
            info["converged"] = True
            break
        moved = None
        if s0 is not None:
            d0 = s0[0]
            dec = -(g @ d0)
            if dec > 0:
                moved = armijo(d0, dec)
            if moved is None:
                # Precision floor of Psi (its value can no longer certify a decrease): take the full
                # Newton step if the Newton step at the new point is at most half as long.
                new = fv + d0
                logp_new, val_new = stats(new)
                if np.isfinite(val_new):
                    s2 = newton_system(*grad_hess(logp_new)[::-1], 0.0)
                    if s2 is not None and float(np.max(np.abs(s2[0]))) <= 0.5 * snorm:
                        moved = (new, logp_new, val_new)
        if moved is None:                               # regularised (Levenberg-Marquardt) steps
            lam = max(1e-6 * scale, 1e-12)
            for _ in range(40):
                sl = newton_system(H, g, lam)
                if sl is not None and g @ sl[0] < 0:
                    moved = armijo(sl[0], -(g @ sl[0]))
                    if moved is not None:
                        info["regularisation"] = lam
                        break
                lam *= 10.0
        if moved is None and gis_ok:                    # monotone fallback
            new = gis(fv, logp)
            logp_new, val_new = stats(new)
            if np.isfinite(val_new) and val_new < val:
                moved = (new, logp_new, val_new)
        if moved is None:
            break
        fv, logp, val = moved
        if C is None:
            fv = fv - fv.mean()
    f[idx] = fv + shift
    info["value"] = val - val_const
    return f, val - val_const, info


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
    A = A - A[np.arange(N), labels][:, None]           # per-sample constants removed (own-state logit = 0)
    f, val, info = minimize_lse(A, n / N, f0=f0, tol=tol)
    if not info["converged"]:
        raise RuntimeError(f"MBAR Newton did not converge (max |grad| = {info['grad']:.2e})")
    # The gradient criterion can be met while the last Newton step is still long: an objective that is
    # numerically flat in some direction (extremely weak overlap).  The value is then accurate but the
    # minimiser is not determined to working precision along that direction; say so.
    info["ill_conditioned"] = not (info["step"] <= 1e-4)
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


def pilot_allocation(U, labels, target, total_budget, cost=None, safeguard=0.25, objective=None,
                     safeguard_mode="equal_counts"):
    """Second-stage allocation from pilot data only (no population quantity).

    Fits MBAR to the pilot, inserts the fitted distributions in V, minimises the plug-in V over
    allocations that keep the pilot samples (s >= pilot counts) and spend `total_budget` in total,
    then mixes the additional samples with a naive split u of the remaining budget (equal counts, or
    equal cost per state):  extra = (1 - safeguard) * plug-in + safeguard * u.
    Guarantee (Proposition A9): for the real-valued mixture, V(final) <= V(pilot + u)/safeguard
    whatever the pilot says.  For the INTEGER counts returned here the same bound holds when every
    pilot count n0_k satisfies (1 - safeguard) * n0_k >= 1 (two samples per state for safeguard 1/4);
    it can fail for a pilot with a state sampled once or not at all (REVIEW_A.md, O5).
    Returns (extra_counts, info)."""
    U, labels, K = _validate(U, labels)
    a = np.ones(K) if cost is None else np.asarray(cost, float)
    n0 = np.bincount(labels, minlength=K).astype(float)
    spent = float(a @ n0)
    if total_budget <= spent:
        raise ValueError("pilot already exhausts the budget")
    rem = total_budget - spent
    # the allocation the plug-in part is mixed with: equal counts (default), or equal cost per state
    # (n_k ~ 1/a_k), which is the better naive rule when costs differ (VALIDATION.md, section 3)
    uniform_extra = np.full(K, rem / a.sum()) if safeguard_mode == "equal_counts" else rem / (K * a)
    info = dict(pilot_counts=n0.astype(int), fallback=None)
    try:
        f, _ = mbar(U, labels)
        P = fitted_distributions(U, labels, f)
        tl = target if isinstance(target, (list, tuple)) else [target]
        nus = [pop.contrast_measure(P, np.asarray(t, float)) for t in tl]
        s, V, oinfo = pop.optimal_allocation(P, nus if len(nus) > 1 else nus[0], cost=a,
                                             budget=total_budget, lower=n0, objective=objective, kind="measure",
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
