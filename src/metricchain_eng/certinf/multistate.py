"""Certified inference from multistate (stratified) samples.

Draws come from several states q_1 .. q_K (unnormalised densities; f*_j = -ln Z_j unknown).  The statements
of ``certify`` need one expectation under the target state k; here it is taken under the sampling mixture
m = sum_j s_j p_j, with the unknown density ratio p_k / m enclosed between two computable functions
(Theorem M1 of docs/engineering/phase2/MBAR_INTEGRATION.md: uncertainty of the free energies acts as an
enlargement of the envelope).  Also: the exact effect of an energy error shared by two states on their
free-energy difference (Proposition M2).

Written from the mathematics; no code of another division is used or imported.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp

from .certify import Bound, _smallest_tau

__all__ = ["kl_bounds", "mbar_fit", "bridge_intervals", "closure", "lr_intervals", "weight_envelopes",
           "certify_upper_pooled", "shared_error_extremes", "shared_error_bound", "total_variation"]

BETS = 0.9 * 2.0 ** -np.arange(16)          # the fixed bets of ``certify`` (fractions of 1 / big)


# ---------------------------------------------------------------------------------------------
# Free energies: a centre (any) and simultaneous intervals (certified)
# ---------------------------------------------------------------------------------------------
def kl_bounds(y: float, n: int, t: float) -> tuple[float, float]:
    """All mu in [0, 1] with n kl(y || mu) <= t, kl the Bernoulli relative entropy.  For the average y of n
    independent draws with values in [0, 1] and E(average) = mu this interval misses mu with probability at most
    2 exp(-t) (Chernoff-Hoeffding; the draws need not be identically distributed).  The ends are rounded outwards
    by the bisection."""
    if n <= 0 or not (0.0 <= y <= 1.0) or not t >= 0:
        return 0.0, 1.0
    c = t / n

    def kl(mu: float) -> float:
        a = 0.0 if y <= 0 else (y * math.log(y / mu) if mu > 0 else math.inf)
        b = 0.0 if y >= 1 else ((1 - y) * math.log((1 - y) / (1 - mu)) if mu < 1 else math.inf)
        return a + b

    lower, upper = 0.0, 1.0
    if y > 0:
        a, b = 0.0, y
        for _ in range(100):
            mid = 0.5 * (a + b)
            if kl(mid) <= c:
                b = mid
            else:
                a = mid
        lower = a
    if y < 1:
        a, b = y, 1.0
        for _ in range(100):
            mid = 0.5 * (a + b)
            if kl(mid) <= c:
                a = mid
            else:
                b = mid
        upper = b
    return lower, upper


def mbar_fit(logq: np.ndarray, counts, weights=None) -> np.ndarray:
    """A solution f of the multistate estimating equations  mean_n pi_j(f, x_n) = s_j  on pooled draws
    (logq[n, j] = ln q_j(x_n); counts[j] draws came from state j; f = 0 at the first sampled state; nan at states
    without draws).  ``weights``: multiplicities of the rows when equal draws are stored once (they sum to the
    number of draws).  Used only as a centre: every certified statement of this module holds for any centre."""
    counts = np.asarray(counts, dtype=float)
    act = np.flatnonzero(counts > 0)
    s = counts[act] / counts.sum()
    lq = np.asarray(logq, dtype=float)[:, act]
    ls = np.log(s)
    w = np.full(len(lq), 1.0 / len(lq)) if weights is None else np.asarray(weights, dtype=float) / float(np.sum(weights))

    def obj(g):
        f = np.concatenate([[0.0], g])
        a = ls + f + lq
        lse = logsumexp(a, axis=1)
        pi = np.exp(a - lse[:, None])
        return float(w @ lse - s @ f), (w @ pi - s)[1:]

    f = np.full(len(counts), np.nan)
    if len(act) == 1:
        f[act] = 0.0
        return f
    res = minimize(obj, np.zeros(len(act) - 1), jac=True, method="BFGS", options=dict(gtol=1e-9, maxiter=500))
    f[act] = np.concatenate([[0.0], res.x])
    return f


def bridge_intervals(logq: np.ndarray, labels: np.ndarray, a: np.ndarray, alpha: float, edges=None):
    """Simultaneous intervals  lo[i, j] <= f*_j - f*_i <= hi[i, j]  (f* = -ln Z), failing with probability at most
    alpha, from draws logq[n, :] of the states labels[n].  ``a`` is any finite vector fixed independently of these
    draws (nan: the state is left out).  With w_l(x) = e^{a_l} q_l(x) / sum_r e^{a_r} q_r(x) in [0, 1],

        E_i[w_j] / E_j[w_i] = e^{a_j - a_i} Z_j / Z_i,

    and each of the two averages gets a Chernoff-Hoeffding interval (``kl_bounds``).  Pairs without an edge, or
    whose intervals reach zero, are left unbounded on the corresponding side."""
    logq = np.asarray(logq, dtype=float)
    K = logq.shape[1]
    act = [k for k in range(K) if np.isfinite(a[k])]
    pos = {k: p for p, k in enumerate(act)}
    if edges is None:
        edges = [(i, j) for q, i in enumerate(act) for j in act[q + 1:]]
    lo, hi = np.full((K, K), -np.inf), np.full((K, K), np.inf)
    np.fill_diagonal(lo, 0.0)
    np.fill_diagonal(hi, 0.0)
    if not edges or not 0 < alpha < 1:
        return lo, hi
    t = math.log(4 * len(edges) / alpha)
    lw = np.asarray(a, dtype=float)[act] + logq[:, act]
    w = np.exp(lw - logsumexp(lw, axis=1)[:, None])
    for i, j in edges:
        mi, mj = labels == i, labels == j
        ni, nj = int(mi.sum()), int(mj.sum())
        if ni == 0 or nj == 0:
            continue
        A_l, A_u = kl_bounds(float(w[mi, pos[j]].mean()), ni, t)
        B_l, B_u = kl_bounds(float(w[mj, pos[i]].mean()), nj, t)
        base = a[j] - a[i]
        l = base + math.log(B_l) - math.log(A_u) if (B_l > 0 and A_u > 0) else -math.inf
        u = base + math.log(B_u) - math.log(A_l) if (A_l > 0 and B_u > 0) else math.inf
        lo[i, j], hi[i, j] = l, u
        lo[j, i], hi[j, i] = -u, -l
    return lo, hi


def closure(lo: np.ndarray, hi: np.ndarray, tol: float = 1e-9):
    """All consequences of the difference constraints lo[i, j] <= f_j - f_i <= hi[i, j] (shortest paths), as a
    tightened pair (lo, hi); None if the constraints contradict each other."""
    D = np.minimum(hi, -lo.T)                     # D[i, j] >= f_j - f_i
    for k in range(len(D)):
        D = np.minimum(D, D[:, [k]] + D[[k], :])
    if np.any(np.diag(D) < -tol):
        return None
    np.fill_diagonal(D, 0.0)
    return -D.T, D


def _label_objective(f, lq, ls, s, w):
    """l(f) = sum_n w_n ln sum_j s_j e^{f_j} q_j(x_n) - s . f (w sums to one), with gradient and Hessian: minus the
    logarithm of the label likelihood prod_n pi_{label(n)}(f, x_n), per draw and up to a constant."""
    a = ls + f + lq
    lse = logsumexp(a, axis=1)
    pi = np.exp(a - lse[:, None])
    pbar = w @ pi
    return float(w @ lse - s @ f), pbar - s, np.diag(pbar) - (pi.T * w) @ pi


def _min_tilted(f, d, lq, ls, s, w, iters=200, tol=1e-11, reach=40.0):
    """inf_f [ l(f) - d . f ] for a zero-sum d, by damped Newton from f in the gauge f[0] fixed.  Returns
    (a floating-point lower estimate of the infimum, the minimiser), or (-inf, f) whenever the search cannot
    vouch for its result: a step that is not a descent direction, a point more than ``reach`` away from the
    start (softmax saturated, Hessian numerically singular), no convergence, or a residual gradient that is
    not small.  The caller treats -inf as 'no bound from this multiplier', which is the safe direction.

    The estimate is the value reached minus the Newton decrement minus (largest residual gradient) x (the
    reach in every coordinate): by convexity g(y) >= g(f) + grad . (y - f), so this is below g at every point
    within ``reach`` of f, where the minimiser of an accepted run lies."""
    f0 = f.copy()
    f = f.copy()
    val, g, H = _label_objective(f, lq, ls, s, w)
    val -= d @ f
    g = g - d
    for _ in range(iters):
        try:
            step = np.linalg.solve(H[1:, 1:], -g[1:])
        except np.linalg.LinAlgError:
            return -math.inf, f0
        dec = float(-g[1:] @ step)
        if not (math.isfinite(dec) and dec >= 0.0 and np.all(np.isfinite(step))):
            return -math.inf, f0                                   # not a descent direction: Hessian unusable here
        res = float(np.max(np.abs(g[1:])))
        if dec < tol and res < 1e-7:
            return val - dec - res * reach * len(f) - 1e-13, f
        t = 1.0
        while True:
            fn = f.copy()
            fn[1:] += t * step
            vn, gn, Hn = _label_objective(fn, lq, ls, s, w)
            vn -= d @ fn
            if math.isfinite(vn) and vn <= val - 0.25 * t * dec:
                break
            t *= 0.5
            if t < 1e-12:
                return -math.inf, f0
        f, val, g, H = fn, vn, gn - d, Hn
        if float(np.max(np.abs(f - f0))) > reach:
            return -math.inf, f0
    return -math.inf, f0


def lr_intervals(logq: np.ndarray, counts, f_ref: np.ndarray, alpha: float, k: int, weights=None):
    """Simultaneous intervals  lo[k, j] <= f*_j - f*_k <= hi[k, j]  for all sampled j, failing with probability at
    most alpha, from the likelihood-ratio region of the label likelihood

        C = { f : l(f) <= l(f_ref) + ln(1/alpha) / N },    l(f) = (1/N) sum_n ln sum_j s_j e^{f_j} q_j(x_n) - s . f,

    for a reference f_ref fixed independently of these draws (the pilot's fit).  exp(N (l(f*) - l(f_ref))) is the
    ratio of the label likelihoods at f_ref and at the truth; its expectation under a stratified sample is at most
    one (the per-state expectations b_j satisfy sum_j n_j b_j = N, and the weighted geometric mean is below the
    arithmetic one), so f* lies in C with probability 1 - alpha by Markov's inequality.  The region is convex; each
    end is computed from above by Lagrangian duality,  max_C c.f <= mu (level - inf_f [l(f) - (c/mu).f])  for every
    mu > 0, so an inexact search over mu only loosens the bound.  Entries not involving k are left unbounded.

    (The e-value property is Theorem B1 of the certified-MBAR division, machine-checked there for finite support;
    this implementation and the three-line argument above are ours.)"""
    logq = np.asarray(logq, dtype=float)
    counts = np.asarray(counts, dtype=float)
    K = logq.shape[1]
    lo, hi = np.full((K, K), -np.inf), np.full((K, K), np.inf)
    np.fill_diagonal(lo, 0.0)
    np.fill_diagonal(hi, 0.0)
    act = np.flatnonzero(counts > 0)
    N = float(counts.sum())
    if not (0 < alpha < 1) or len(act) < 2 or not counts[k] > 0 or not np.all(np.isfinite(np.asarray(f_ref, dtype=float)[act])):
        return lo, hi
    s = counts[act] / N
    ls = np.log(s)
    lq = logq[:, act]
    w = np.full(len(lq), 1.0 / len(lq)) if weights is None else np.asarray(weights, dtype=float) / float(np.sum(weights))
    fr = np.asarray(f_ref, dtype=float)[act]
    level = _label_objective(fr, lq, ls, s, w)[0] + math.log(1.0 / alpha) / N
    l_hat, f_hat = _min_tilted(fr, np.zeros(len(act)), lq, ls, s, w)
    if not math.isfinite(l_hat):
        return lo, hi                                              # no finite fit near the reference: nothing is claimed
    l_fit = _label_objective(f_hat, lq, ls, s, w)[0]              # f_hat is a point of the region (l_fit <= level)
    if not l_fit <= level:
        return lo, hi
    gap = max(level - l_hat, 1e-300)
    H = _label_objective(f_hat, lq, ls, s, w)[2]
    kk = int(np.flatnonzero(act == k)[0])

    def top(c):
        """An upper bound of max over C of c . f (c sums to zero)."""
        neg = np.flatnonzero(c < 0)
        mu_min = float(np.max(-c[neg] / s[neg])) * (1 + 1e-9)     # s + c/mu must stay positive
        try:
            r = float(c[1:] @ np.linalg.solve(H[1:, 1:], c[1:]))  # quadratic model: mu* = sqrt(r / (2 gap))
        except np.linalg.LinAlgError:
            r = math.nan
        guess = math.sqrt(r / (2 * gap)) if (math.isfinite(r) and r > 0) else 10 * mu_min
        best, start, worse = math.inf, f_hat, 0
        grid = guess * np.exp(np.linspace(2.5, -2.5, 41))         # from the largest multiplier (closest to the fit) down
        for mu in grid[grid > mu_min * (1 + 1e-6)]:
            v, fm = _min_tilted(start, c / mu, lq, ls, s, w)
            if not math.isfinite(v):
                break                                              # smaller multipliers are harder still
            u = mu * (level - v)
            if not (math.isfinite(u) and u >= c @ f_hat - 1e-9):   # a bound below a point of the region: reject
                break
            worse = worse + 1 if u >= best else 0
            best = min(best, u)
            start = fm
            if worse >= 3:                                         # convex in the multiplier: the minimum is passed
                break
        return best

    for jj, j in enumerate(act):
        if j == k:
            continue
        c = np.zeros(len(act))
        c[jj], c[kk] = 1.0, -1.0
        up, down = top(c), -top(-c)
        if not down <= up:                                         # cannot happen for valid bounds: claim nothing
            up, down = math.inf, -math.inf
        hi[k, j], lo[k, j] = up, down
        lo[j, k], hi[j, k] = -up, -down
    return lo, hi


# ---------------------------------------------------------------------------------------------
# Theorem M1: the density ratio of the target state against the sampling mixture, enclosed
# ---------------------------------------------------------------------------------------------
def weight_envelopes(logq: np.ndarray, counts, f0: np.ndarray, k: int, lo: np.ndarray, hi: np.ndarray, lam=1.0, ups=1.0):
    """(L, U) at points with log-densities logq[n, :] such that, whenever lo[i, j] <= f*_j - f*_i <= hi[i, j] for
    all pairs of sampled states,

        L(x) <= lam(x) p_k(x) / m(x)      and      ups(x) p_k(x) / m(x) <= U(x),

    m = sum_j s_j p_j the mixture of the sampled states in the proportions s = counts / sum(counts).  f0 is any
    centre.  With h = f* - f0:  p_k/m = W0 / sum_j omega_j e^{h_j - h_k},  W0 = e^{f0_k} q_k / sum_j s_j e^{f0_j} q_j
    and omega_j = s_j e^{f0_j} q_j / sum_r s_r e^{f0_r} q_r.  U <= sup(ups) / s_k always."""
    counts = np.asarray(counts, dtype=float)
    s = counts / counts.sum()
    if not s[k] > 0:
        raise ValueError("the target state must be among the sampled states")
    act = np.flatnonzero(counts > 0)
    kk = int(np.flatnonzero(act == k)[0])
    la = np.log(s[act]) + f0[act] + np.asarray(logq, dtype=float)[:, act]
    lom = la - logsumexp(la, axis=1)[:, None]                     # ln omega_j(x)
    w0 = np.exp(lom[:, kk]) / s[k]
    d0 = f0[act] - f0[k]
    hlo, hhi = lo[k, act] - d0, hi[k, act] - d0                   # h_j - h_k lies in [hlo_j, hhi_j]
    hlo[kk] = hhi[kk] = 0.0
    dead = np.isneginf(lom)
    with np.errstate(invalid="ignore"):
        t_lo = np.where(dead, -np.inf, lom + hhi[None, :])        # terms of 1 / rho_lo
        t_hi = np.where(dead | np.isneginf(hlo)[None, :], -np.inf, lom + hlo[None, :])   # terms of 1 / rho_hi
    rho_lo = np.exp(-logsumexp(t_lo, axis=1))
    rho_hi = np.exp(-logsumexp(t_hi, axis=1))
    return w0 * rho_lo * lam, w0 * rho_hi * ups


def _log_wealth_w(z: np.ndarray, big: float, w: np.ndarray) -> float:
    """``certify.log_wealth`` for draws stored with multiplicities w: ln mean_k prod_n (1 - lam_k z_n)^{w_n}."""
    if big <= 0:
        return math.inf if np.all(z <= 0) and np.any((z < 0) & (w > 0)) else 0.0
    lam = BETS / big
    return float(logsumexp(np.log1p(-np.outer(lam, z)) @ w) - math.log(len(lam)))


def certify_upper_pooled(s0: np.ndarray, L: np.ndarray, U: np.ndarray, big: float, tau_lo: float, tau_hi: float,
                         delta: float, weights=None) -> Bound:
    """The smallest tau in [tau_lo, tau_hi] at which the product test rejects 'sum_n E z_n(tau) >= 0', where
    z_n(tau) = U_n (s0_n - tau)_+ - L_n (tau - s0_n)_+ at independent draws (not necessarily identically
    distributed: a stratified sample of several states).  ``big`` must be fixed independently of these draws and
    must bound U(x) (s0(x) - tau_lo)_+ over the whole configuration space; a draw above it voids the statement.
    s0 = f - eta . phi + h_R(eta) is the score at tau = 0 (s0 = f without measured averages).  ``weights``:
    multiplicities, when equal draws are stored once (the same statement, computed faster)."""
    s0, L, U = (np.asarray(v, dtype=float) for v in (s0, L, U))
    hi_end = float(tau_hi)
    if not (0.0 < delta < 1.0) or not (math.isfinite(big) and big >= 0 and tau_lo <= tau_hi):
        return Bound(hi_end, "void", "the level, the declared bound or the bracket cannot be used")
    if not (np.all(np.isfinite(s0)) and np.all(np.isfinite(L)) and np.all(np.isfinite(U))):
        return Bound(hi_end, "void", "a drawn value is not a finite number")
    if np.any(L < 0) or np.any(L > U * (1 + 1e-12)):
        return Bound(hi_end, "void", "a drawn pair violates 0 <= L <= U")
    if s0.size and float(np.max(U * np.maximum(s0 - tau_lo, 0.0))) > big * (1 + 1e-12):
        return Bound(hi_end, "void", "a drawn value exceeds the declared bound")

    def zfun(tau):
        return U * np.maximum(s0 - tau, 0.0) - L * np.maximum(tau - s0, 0.0)

    target = math.log(1.0 / delta)
    if weights is None:
        n_valid = int(s0.size)
        tau = _smallest_tau(zfun, big, float(tau_lo), hi_end, target)
    else:                                                          # equal draws stored once, with multiplicities
        w = np.asarray(weights, dtype=float)
        if w.shape != s0.shape or np.any(w < 0) or not np.all(np.isfinite(w)):
            return Bound(hi_end, "void", "the multiplicities cannot be used")
        n_valid = int(round(float(w.sum())))
        a, b = float(tau_lo), hi_end
        if not _log_wealth_w(zfun(b), big, w) >= target:
            tau = None
        elif _log_wealth_w(zfun(a), big, w) >= target:
            tau = a
        else:
            for _ in range(60):
                mid = 0.5 * (a + b)
                if _log_wealth_w(zfun(mid), big, w) >= target:
                    b = mid
                else:
                    a = mid
            tau = b
    if tau is None:
        return Bound(hi_end, "trivial", "the draws certify nothing below the upper end of the bracket", n_valid=n_valid)
    return Bound(float(tau), "certified", "", n_valid=n_valid)


# ---------------------------------------------------------------------------------------------
# Proposition M2: an energy error shared by two states
# ---------------------------------------------------------------------------------------------
def total_variation(p_i: np.ndarray, p_j: np.ndarray) -> float:
    return float(0.5 * np.abs(np.asarray(p_i, dtype=float) - np.asarray(p_j, dtype=float)).sum())


def shared_error_bound(tv: float, eps: float) -> float:
    """| (f_j - f_i)(true) - (f_j - f_i)(model) | <= ln(1 + (e^{2 eps} - 1) TV(p_i, p_j)) when both reduced energies
    carry the same error d(x) in [-eps, eps]."""
    return math.log1p(math.expm1(2 * eps) * tv)


def shared_error_extremes(p_i: np.ndarray, p_j: np.ndarray, eps: float) -> tuple[float, float]:
    """Exact range of  -ln( E_j e^{-d} / E_i e^{-d} )  over all d: X -> [-eps, eps] on a finite space: the change of
    f_j - f_i caused by an error d shared by the two states.  The extremes are attained at d = -/+ eps on a level
    set of p_j / p_i (a linear-fractional programme over a box)."""
    p_i, p_j = np.asarray(p_i, dtype=float), np.asarray(p_j, dtype=float)
    keep = (p_i > 0) | (p_j > 0)
    p_i, p_j = p_i[keep], p_j[keep]
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(p_i > 0, p_j / p_i, np.inf)
    order = np.argsort(-ratio, kind="stable")
    ci = np.concatenate([[0.0], np.cumsum(p_i[order])])          # mass of the t points with the largest ratio
    cj = np.concatenate([[0.0], np.cumsum(p_j[order])])
    up, dn = math.exp(eps), math.exp(-eps)
    with np.errstate(divide="ignore", invalid="ignore"):
        r_max = np.max((up * cj + dn * (1 - cj)) / (up * ci + dn * (1 - ci)))    # large weight where p_j/p_i is large
        r_min = np.min((dn * cj + up * (1 - cj)) / (dn * ci + up * (1 - ci)))
    return -math.log(r_max), -math.log(r_min)
