"""The block bounds of the Markov recursion (theory workstream Y, Proposition F, block form) computed from the
exact vertex set of the weighted cube.

Model.  Binary symmetric chain with flip probability ``p < 1/2`` (``K = ln((1-p)/p)``), residuals that are
``u``-Lipschitz in the Hamming distance.  For a block of ``L`` sites:

* slopes ``(u, ..., u, u*)`` with ``u*`` the fixed point of ``x = u + g(x)``,
  ``g(x) = ln[((1-p) e^x + p) / (p e^x + 1 - p)]`` (the last site of the block carries ``u*``);
* block law ``pi(x) = prod_{i=0}^{L-1} P(x_{i-1}, x_i)`` with ``x_{-1} = 0`` (the law of the block given the
  letter before it; by the flip symmetry of the chain the choice of that letter does not matter);
* Gibbs laws ``pi_phi = pi e^{-phi} / E_pi e^{-phi}``, ``phi`` in the Lipschitz polytope;
* site function ``F*(t) = max_M G_t(M) = min_Q max_phi -ln sum_x pi_phi(x)^t Q(x)^(1-t)`` (``0 < t < 1``),
  ``G_t(M) = -t ln sum_x (sum_phi M(phi) pi_phi(x)^t)^(1/t)``;
* capacity ``cap = max_M I(M; phi -> pi_phi) = min_Q max_phi KL(pi_phi || Q)``.

For every probability vector ``Q`` the maximum over the whole polytope of ``KL(pi_phi || Q)`` and of
``-ln sum_x pi_phi^t Q^(1-t)`` is attained at a vertex: in the variables ``v = e^{-phi}`` the class is the
polyhedral cone ``{v > 0 : v(y) <= e^{w_i} v(x)}``, the normalised weights ``pi v / sum pi v`` range over a
polytope, ``KL(. || Q)`` is convex and ``sum_x (.)^t Q^(1-t)`` concave on it, and the extreme rays of the cone
are the images of the vertices of the polytope of ``phi`` (tight constraints of corank one).  So with the
complete vertex list ``max_{vertices} ...`` is an upper bound of ``cap`` resp. ``F*(t)``; with any ``M``
supported on vertices ``I(M)`` resp. ``G_t(M)`` is a lower bound.  Proposition F of the theory division's
workstream Y (an input here) gives

    a_inf <= cap / L,        h_inf = sup_t F_inf(t) <= sup_t F*(t) / L.

Solvers work on a small working set of vertices (Blahut-Arimoto / Arimoto iterations with a Newton polish on
the active set) and are closed by scans over ALL vertices (column generation); the value of a scan at the final
centre ``Q`` is the upper bound whatever the state of the solver.  Floating-point values are re-evaluated in
interval arithmetic by the ``iv_*`` functions.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction

import mpmath as mp
import numpy as np
from mpmath import iv

from . import chambers as ch

# ----------------------------------------------------------------------------- the model (floating point)


def g_slack(x: float, p: float) -> float:
    return math.log(((1 - p) * math.exp(x) + p) / (p * math.exp(x) + 1 - p))


def ustar(p: float, u: float) -> float:
    """Fixed point of ``x = u + g(x)`` (a contraction: ``0 < g' <= 1 - 2p``)."""
    x = u
    for _ in range(400):
        x_new = u + g_slack(x, p)
        if abs(x_new - x) < 1e-16 * max(1.0, abs(x)):
            return x_new
        x = x_new
    return x


def block_flips(L: int) -> np.ndarray:
    """``flips[x]`` = number of sites ``i`` of the block with ``x_i != x_{i-1}``, where ``x_{-1} = 0``."""
    n = 1 << L
    out = np.zeros(n, dtype=np.int64)
    for x in range(n):
        prev = 0
        for i in range(L):
            b = (x >> i) & 1
            out[x] += b != prev
            prev = b
    return out


def block_law_log(L: int, p: float) -> np.ndarray:
    f = block_flips(L)
    return f * math.log(p) + (L - f) * math.log(1 - p)


def cube_F(t: float, u: float) -> float:
    return t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))


def cube_exponents(u: float):
    """``(h, t*, a, E)`` of the uniform cube with slope ``u`` (closed forms)."""
    hh = u / 2
    E = math.log(math.cosh(hh))
    a = hh * math.tanh(hh) - E
    ts = math.atanh(E / hh) / hh
    return cube_F(ts, u), ts, a, E


def gibbs_rows(A: np.ndarray, B: np.ndarray, u: float, us: float, logpi: np.ndarray) -> np.ndarray:
    """Rows ``pi_phi`` for ``phi = u A + us B``."""
    lw = logpi[None, :] - (u * A.astype(np.float64) + us * B.astype(np.float64))
    lw -= lw.max(axis=1, keepdims=True)
    W = np.exp(lw)
    return W / W.sum(axis=1, keepdims=True)


# ----------------------------------------------------------------------------- solvers on an explicit set of rows
#
# Both problems are solved in their DUAL form, a convex programme in few variables (the centre Q) with one
# linear constraint per row:
#
#   capacity:  minimise  C + ln sum_x e^{lam_x}   subject to  C >= sum_x W_phi(x) ln W_phi(x) - W_phi . lam
#              (Q = e^lam / sum e^lam; the constraint says KL(W_phi || Q) <= C);
#   Renyi t :  minimise  ||y||_q, q = 1/(1-t),     subject to  sum_x W_phi(x)^t y_x >= 1,  y >= 0
#              (Q proportional to y^q; then  -ln sum_x W_phi^t Q^(1-t) <= ln ||y||_q  for every row).
#
# scipy's SLSQP (an active-set SQP method) is used; it copes with degenerate optima (more active rows than
# states), where the multiplicative iterations are slow.  A weight vector M is then recovered on the active
# rows by non-negative least squares from the stationarity condition (Q_M = Q), and a Newton step on "all
# active rows have the same value" removes what is left of the solver's tolerance.  Whatever the solver does,
# the two numbers returned are a valid bracket for the given rows: ``lower`` is the primal value at the returned
# M, ``upper`` the largest dual value at the centre Q_M built from M.  The multiplicative iterations
# (Blahut-Arimoto, Arimoto) are kept as an independent solver and as the fall-back.


def _capacity_eval(W, negH, M):
    Q = M @ W
    kl = negH - W @ np.log(Q)
    return Q, kl, float(M @ kl), float(kl.max())


def _renyi_eval(Wt, t, M):
    s = M @ Wt
    r = s ** (1.0 / t)
    R = float(r.sum())
    Q = r / R
    c = Wt @ Q ** (1.0 - t)
    return Q, c, r, R, -t * math.log(R), -math.log(float(c.min()))


def renyi_jacobian(Wt, t, M):
    """``d c_phi / d M_psi`` for ``c_phi = sum_x W_phi(x)^t Q_M(x)^(1-t)``, ``Q_M`` proportional to
    ``(sum_phi M W_phi^t)^(1/t)`` (used by the Newton step; exposed for the tests)."""
    Q, c, r, R, _, _ = _renyi_eval(Wt, t, M)
    core = (Wt * r ** (1.0 - 2.0 * t)) @ Wt.T
    return ((1.0 - t) / t) * (R ** (t - 1.0) * core - np.outer(c, c) * R ** (-t))


def _equalise(S, Ms, residual_jac, max_iter: int = 40):
    """Newton's method for ``vals(Ms) = const, sum Ms = 1`` on the rows ``S`` (no change of the support).
    Returns the new weights, or None if it does not converge or leaves the simplex."""
    for _it in range(max_iter):
        vals, J0 = residual_jac(S, Ms)
        mean = float(Ms @ vals)
        res = vals - mean
        if np.abs(res).max() < 4e-15 * max(1.0, abs(mean)):
            return Ms
        k = len(S)
        J = np.zeros((k + 1, k + 1))
        J[:k, :k] = J0
        J[:k, k] = -1.0
        J[k, :k] = 1.0
        try:
            delta = np.linalg.lstsq(J, -np.concatenate([res, [0.0]]), rcond=1e-13)[0]
        except np.linalg.LinAlgError:
            return None
        Ms = Ms + delta[:k]
        if not np.all(np.isfinite(Ms)) or Ms.min() <= 0:
            return None
        Ms = Ms / Ms.sum()
    return None


def _best(cands):
    return min(cands, key=lambda d: d["upper"] - d["lower"])


def capacity_iterate(W: np.ndarray, M: np.ndarray | None = None, iters: int = 2000):
    """Blahut-Arimoto iterations ``M <- M exp(KL(W_phi || Q_M))`` (independent of the SQP solver)."""
    m = W.shape[0]
    negH = np.einsum("ij,ij->i", W, np.log(W))
    M = np.full(m, 1.0 / m) if M is None else np.maximum(M, 1e-300) / np.maximum(M, 1e-300).sum()
    best = None
    for _ in range(iters):
        Q, kl, lo, up = _capacity_eval(W, negH, M)
        if best is None or up - lo < best["upper"] - best["lower"]:
            best = dict(lower=lo, upper=up, M=M.copy(), Q=Q.copy())
        M = M * np.exp(kl - up)
        M = M / M.sum()
    return best


def renyi_iterate(W: np.ndarray, t: float, M: np.ndarray | None = None, iters: int = 2000):
    """Arimoto's iterations ``M <- M c^(-t/(1-t))``, ``c_phi = sum_x W_phi^t Q_M^(1-t)``."""
    m = W.shape[0]
    Wt = W ** t
    M = np.full(m, 1.0 / m) if M is None else np.maximum(M, 1e-300) / np.maximum(M, 1e-300).sum()
    best = None
    for _ in range(iters):
        Q, c, r, R, lo, up = _renyi_eval(Wt, t, M)
        if best is None or up - lo < best["upper"] - best["lower"]:
            best = dict(lower=lo, upper=up, M=M.copy(), Q=Q.copy())
        M = M * (c / c.min()) ** (-t / (1.0 - t))
        M = M / M.sum()
    return best


def capacity_solve(W: np.ndarray, Q0: np.ndarray | None = None, tol: float = 1e-13):
    """``max_M I(M; W)`` over the rows of ``W``: returns ``dict(lower, upper, M, Q)`` with ``lower = I(M)`` and
    ``upper = max_rows KL(W_phi || Q_M)`` (a duality bracket for THIS set of rows)."""
    from scipy.optimize import minimize, nnls
    from scipy.special import logsumexp

    m, n = W.shape
    negH = np.einsum("ij,ij->i", W, np.log(W))
    if Q0 is None:
        Q0 = W.mean(axis=0)
    lam0 = np.log(Q0 / Q0.sum())
    z0 = np.concatenate([lam0, [float((negH - W @ lam0).max())]])
    Acon = np.hstack([W, np.ones((m, 1))])

    def obj(z):
        return z[n] + logsumexp(z[:n])

    def gobj(z):
        return np.concatenate([np.exp(z[:n] - logsumexp(z[:n])), [1.0]])

    cands = []
    try:
        res = minimize(obj, z0, jac=gobj, method="SLSQP", options=dict(ftol=1e-15, maxiter=1000),
                       constraints=[{"type": "ineq", "fun": lambda z: Acon @ z - negH, "jac": lambda z: Acon}])
        lam = res.x[:n] - logsumexp(res.x[:n])
        Q = np.exp(lam)
        kl = negH - W @ lam
        for slack in (1e-9, 1e-7, 1e-5):
            act = np.flatnonzero(kl >= kl.max() - slack * max(1.0, abs(kl.max())))
            x, _ = nnls(W[act].T, Q, maxiter=50 * len(act) + 200)
            if x.sum() <= 0:
                continue
            M = np.zeros(m)
            M[act] = x / x.sum()
            Qm, klm, lo, up = _capacity_eval(W, negH, M)
            cands.append(dict(lower=lo, upper=up, M=M, Q=Qm))
            if up - lo < tol:
                break
            S = np.flatnonzero(M > 0)

            def residual_jac(S_, Ms):
                Ws = W[S_]
                Qs = Ms @ Ws
                return negH[S_] - Ws @ np.log(Qs), -(Ws / Qs) @ Ws.T

            Ms = _equalise(S, M[S], residual_jac)
            if Ms is not None:
                M2 = np.zeros(m)
                M2[S] = Ms
                Qm, klm, lo, up = _capacity_eval(W, negH, M2)
                cands.append(dict(lower=lo, upper=up, M=M2, Q=Qm))
                if up - lo < tol:
                    break
    except Exception:
        pass
    if not cands or _best(cands)["upper"] - _best(cands)["lower"] > max(tol, 1e-9):
        start = _best(cands)["M"] + 1e-6 / m if cands else None
        cands.append(capacity_iterate(W, start, iters=20000))
    return _best(cands)


def renyi_solve(W: np.ndarray, t: float, Q0: np.ndarray | None = None, tol: float = 1e-13):
    """``F*(t)`` over the rows of ``W``: ``dict(lower, upper, M, Q)``, ``lower = G_t(M)``,
    ``upper = max_rows -ln sum_x W^t Q_M^(1-t)``."""
    from scipy.optimize import minimize, nnls

    m, n = W.shape
    Wt = W ** t
    q = 1.0 / (1.0 - t)
    if Q0 is None:
        Q0 = W.mean(axis=0)
    y0 = (Q0 / Q0.sum()) ** (1.0 - t)
    y0 = y0 / float((Wt @ y0).min())

    def obj(y):
        return float((y ** q).sum() ** (1.0 / q))

    def gobj(y):
        nrm = (y ** q).sum() ** (1.0 / q)
        return (y / nrm) ** (q - 1.0)

    cands = []
    try:
        res = minimize(obj, y0, jac=gobj, method="SLSQP", bounds=[(1e-14, None)] * n,
                       options=dict(ftol=1e-15, maxiter=1000),
                       constraints=[{"type": "ineq", "fun": lambda y: Wt @ y - 1.0, "jac": lambda y: Wt}])
        y = np.maximum(res.x, 1e-14)
        Q = y ** q
        Q = Q / Q.sum()
        c = Wt @ Q ** (1.0 - t)
        for slack in (1e-9, 1e-7, 1e-5):
            act = np.flatnonzero(c <= c.min() * (1.0 + slack))
            x, _ = nnls(Wt[act].T, Q ** t, maxiter=50 * len(act) + 200)
            if x.sum() <= 0:
                continue
            M = np.zeros(m)
            M[act] = x / x.sum()
            Qm, cm, r, R, lo, up = _renyi_eval(Wt, t, M)
            cands.append(dict(lower=lo, upper=up, M=M, Q=Qm))
            if up - lo < tol:
                break
            S = np.flatnonzero(M > 0)

            def residual_jac(S_, Ms):
                Ws = Wt[S_]
                return _renyi_eval(Ws, t, Ms)[1], renyi_jacobian(Ws, t, Ms)

            Ms = _equalise(S, M[S], residual_jac)
            if Ms is not None:
                M2 = np.zeros(m)
                M2[S] = Ms
                Qm, cm, r, R, lo, up = _renyi_eval(Wt, t, M2)
                cands.append(dict(lower=lo, upper=up, M=M2, Q=Qm))
                if up - lo < tol:
                    break
    except Exception:
        pass
    if not cands or _best(cands)["upper"] - _best(cands)["lower"] > max(tol, 1e-9):
        start = _best(cands)["M"] + 1e-6 / m if cands else None
        cands.append(renyi_iterate(W, t, start, iters=20000))
    return _best(cands)


# ----------------------------------------------------------------------------- the block problem and its scans


def _row_keys(A: np.ndarray, B: np.ndarray):
    both = np.ascontiguousarray(np.concatenate([A, B], axis=1))
    return [both[i].tobytes() for i in range(both.shape[0])]


@dataclass
class WorkingSet:
    A: np.ndarray
    B: np.ndarray
    keys: dict = field(default_factory=dict)

    @classmethod
    def empty(cls, n: int):
        return cls(np.zeros((0, n), dtype=np.int8), np.zeros((0, n), dtype=np.int8), {})

    def add(self, A: np.ndarray, B: np.ndarray) -> int:
        """Append the rows that are not yet present; returns how many were new."""
        new = []
        for i, k in enumerate(_row_keys(A, B)):
            if k not in self.keys:
                self.keys[k] = len(self.keys)
                new.append(i)
        if new:
            self.A = np.concatenate([self.A, A[new]])
            self.B = np.concatenate([self.B, B[new]])
        return len(new)

    def __len__(self):
        return self.A.shape[0]


class BlockProblem:
    """The block of ``L`` sites at ``(p, u)`` with the vertex set of a chamber (stored by orbits).

    ``explicit=(A_all, B_all)`` switches the scans from the C kernel to plain numpy over an explicit list of
    all vertices (used to cross-check the kernel)."""

    def __init__(self, chamber: ch.Chamber, p: float, u: float, explicit=None):
        self.chamber = chamber
        self.L = chamber.L
        self.n = 1 << self.L
        self.p = float(p)
        self.u = float(u)
        self.us = ustar(self.p, self.u)
        if not chamber.contains(Fraction(self.us / self.u)):
            raise ValueError("u*/u is not in this chamber")
        self.logpi = block_law_log(self.L, self.p)
        self.table = ch.group_table(self.L)
        self.explicit = explicit
        self.n_scans = 0

    def rows(self, A, B) -> np.ndarray:
        return gibbs_rows(A, B, self.u, self.us, self.logpi)

    def scan_kl(self, lnQ: np.ndarray, K: int = 128):
        """The ``K`` largest values of ``KL(pi_phi || Q)`` over all vertices, with the vertices."""
        self.n_scans += 1
        if self.explicit is not None:
            A, B = self.explicit
            W = self.rows(A, B)
            kl = np.einsum("ij,ij->i", W, np.log(W) - lnQ[None, :])
            idx = np.argsort(-kl)[:K]
            return kl[idx], A[idx], B[idx]
        from . import ckernel

        val, rep, g, _, _ = ckernel.scan_kl(self.L, self.table, self.chamber.A, self.chamber.B, self.logpi, self.u,
                                            self.us, lnQ, K=K)
        Ar, Br = ch.image_rows(self.chamber.A, self.chamber.B, self.table, rep, g)
        return val, Ar, Br

    def scan_renyi(self, ts, Qs, K: int = 64):
        """For every order ``ts[j]`` and centre ``Qs[j]`` the ``K`` largest values of
        ``-ln sum_x pi_phi^t Q^(1-t)`` over all vertices, with the vertices."""
        self.n_scans += 1
        ts = np.asarray(ts, dtype=np.float64)
        Qs = np.asarray(Qs, dtype=np.float64)
        out = []
        if self.explicit is not None:
            A, B = self.explicit
            W = self.rows(A, B)
            for t, Q in zip(ts, Qs):
                v = -np.log((W ** t) @ (Q ** (1.0 - t)))
                idx = np.argsort(-v)[:K]
                out.append((v[idx], A[idx], B[idx]))
            return out
        from . import ckernel

        pq = np.exp(ts[:, None] * self.logpi[None, :] + (1.0 - ts[:, None]) * np.log(Qs))
        for j0 in range(0, len(ts), 64):
            sl = slice(j0, j0 + 64)
            vals, reps, gs = ckernel.scan_renyi(self.L, self.table, self.chamber.A, self.chamber.B, self.logpi, self.u,
                                                self.us, ts[sl], pq[sl], K=K)
            for v, r, g in zip(vals, reps, gs):
                Ar, Br = ch.image_rows(self.chamber.A, self.chamber.B, self.table, r, g)
                out.append((v, Ar, Br))
        return out


def additive_rows(L: int):
    """The ``2^L`` site-wise labels ``phi_sigma(x) = sum_i w_i [x_i != sigma_i]`` in symbolic form."""
    n = 1 << L
    A = np.zeros((n, n), dtype=np.int8)
    B = np.zeros((n, n), dtype=np.int8)
    for sg in range(n):
        for x in range(n):
            d = x ^ sg
            A[sg, x] = bin(d & ((1 << (L - 1)) - 1)).count("1")
            B[sg, x] = (d >> (L - 1)) & 1
    return A - A[:, :1], B - B[:, :1]


def capacity_bound(prob: BlockProblem, K: int = 256, tol: float = 1e-12, max_rounds: int = 60, ws: WorkingSet | None = None):
    """Capacity of the block by column generation.  Returns a dict with ``lower = I(M)`` (a valid lower bound of
    the capacity), ``upper = max over ALL vertices of KL(pi_phi || Q)`` at the final centre (a valid upper
    bound), ``Q``, the support with its weights, and the top of the last scan (for the certificates)."""
    ws = WorkingSet.empty(prob.n) if ws is None else ws
    if len(ws) == 0:
        ws.add(*additive_rows(prob.L))
    Q = None
    out = None
    for rnd in range(max_rounds):
        W = prob.rows(ws.A, ws.B)
        sol = capacity_solve(W, Q, tol=tol / 10)
        Q = sol["Q"]
        vals, At, Bt = prob.scan_kl(np.log(Q), K)
        out = dict(lower=sol["lower"], upper=float(vals[0]), Q=Q, M=sol["M"], rounds=rnd + 1, top_vals=vals, top_A=At,
                   top_B=Bt)
        if vals[0] - sol["lower"] <= tol:
            break
        viol = vals > sol["lower"] + tol / 10
        if ws.add(At[viol], Bt[viol]) == 0:
            break
    M = out["M"]
    sup = M > 0
    out.update(support_A=ws.A[: len(M)][sup], support_B=ws.B[: len(M)][sup], support_M=M[sup] / M[sup].sum(),
               working_set=ws)
    return out


def renyi_bounds(prob: BlockProblem, ts, ws: WorkingSet | None = None, warm: dict | None = None, K: int = 64,
                 tol: float = 1e-10, max_rounds: int = 60):
    """``F*(t)`` of the block for all ``t`` in ``ts``: dict ``t -> dict(lower, upper, Q, M, ...)`` where ``upper``
    is the maximum over ALL vertices at the final centre.  ``ws`` (shared working set) and ``warm`` (centres by
    ``t``) are updated in place."""
    ws = WorkingSet.empty(prob.n) if ws is None else ws
    warm = {} if warm is None else warm
    ts = [float(t) for t in ts]
    if len(ws) == 0:
        ws.add(*additive_rows(prob.L))
    res = {}
    todo = list(ts)
    for rnd in range(max_rounds):
        A_ws, B_ws = ws.A, ws.B          # the rows the solutions of this round refer to
        W = prob.rows(A_ws, B_ws)
        sols = {}
        for t in todo:
            Q0 = warm.get(t)
            if Q0 is None and warm:
                Q0 = warm[min(warm, key=lambda s: abs(s - t))]
            sols[t] = renyi_solve(W, t, Q0, tol=tol / 10)
            warm[t] = sols[t]["Q"]
        scans = prob.scan_renyi(todo, [sols[t]["Q"] for t in todo], K)
        nxt = []
        for t, (vals, At, Bt) in zip(todo, scans):
            M = sols[t]["M"]
            sup = M > 0
            res[t] = dict(lower=sols[t]["lower"], upper=float(vals[0]), Q=sols[t]["Q"], support_A=A_ws[sup],
                          support_B=B_ws[sup], support_M=M[sup] / M[sup].sum(), top_vals=vals, top_A=At, top_B=Bt)
            if vals[0] - sols[t]["lower"] > tol:
                viol = vals > sols[t]["lower"] + tol / 10
                if ws.add(At[viol], Bt[viol]) > 0:
                    nxt.append(t)
        todo = nxt
        if not todo:
            break
    return res


def interval_bound(t1: float, B1: float, t2: float, B2: float) -> float:
    """``sup_{t1 <= t <= t2} F(t)`` for any ``F`` with ``F(t)/t`` nonincreasing, ``F(t)/(1-t)`` nondecreasing,
    ``F(t1) <= B1``, ``F(t2) <= B2``:  ``F(t) <= min(t B1/t1, (1-t) B2/(1-t2))``, maximised over the interval."""
    a1 = B1 / t1
    a2 = B2 / (1.0 - t2)
    tx = a2 / (a1 + a2)
    if tx <= t1:
        return a2 * (1.0 - t1)
    if tx >= t2:
        return a1 * t2
    return a1 * a2 / (a1 + a2)


def sup_bound(grid) -> float:
    """Upper bound of ``sup_{0<t<1} F(t)`` from ``grid = [(t, B(t)), ...]`` (sorted), ``F(t) <= B(t)`` there:
    interval rule between grid points; below the first point ``F(t) <= (1-t) B/(1-t_first) <= B/(1-t_first)``,
    above the last ``F(t) <= t B/t_last <= B/t_last``."""
    best = max(grid[0][1] / (1.0 - grid[0][0]), grid[-1][1] / grid[-1][0])
    for (t1, B1), (t2, B2) in zip(grid[:-1], grid[1:]):
        best = max(best, interval_bound(t1, B1, t2, B2))
    return best


def h_bound(prob: BlockProblem, rel_tol: float = 2e-4, t_lo: float = 0.05, t_hi: float = 0.95, coarse: float = 0.05,
            max_points: int = 400, K: int = 48, tol: float = 1e-10, ws: WorkingSet | None = None):
    """``sup_t F*(t)`` of the block with an adaptively refined grid: returns ``dict(lower, upper, t_best, grid)``
    where ``lower = max_t G_t(M_t)`` over the grid, ``upper`` = the interval rule applied to the scan values,
    refined until ``upper <= lower (1 + rel_tol)`` (or ``max_points``).  Per block, not per site."""
    ws = WorkingSet.empty(prob.n) if ws is None else ws
    warm = {}
    nc = int(round((t_hi - t_lo) / coarse))
    ts = [round(t_lo + k * (t_hi - t_lo) / nc, 12) for k in range(nc + 1)]
    data = {}
    new = ts
    while True:
        data.update(renyi_bounds(prob, new, ws=ws, warm=warm, K=K, tol=tol))
        grid = sorted((t, d["upper"]) for t, d in data.items())
        lower = max(d["lower"] for d in data.values())
        t_best = max(data, key=lambda t: data[t]["lower"])
        target = lower * (1.0 + rel_tol)
        new = []
        for (t1, B1), (t2, B2) in zip(grid[:-1], grid[1:]):
            if interval_bound(t1, B1, t2, B2) > target:
                new.append(0.5 * (t1 + t2))
        tails = max(grid[0][1] / (1.0 - grid[0][0]), grid[-1][1] / grid[-1][0])
        if tails > target:
            raise RuntimeError("tail bound exceeds the target: widen [t_lo, t_hi]")
        if not new or len(data) + len(new) > max_points:
            break
    return dict(lower=lower, upper=sup_bound(grid), t_best=t_best, grid=[(t, data[t]["lower"], data[t]["upper"]) for t, _ in grid],
                data=data, working_set=ws)


# ----------------------------------------------------------------------------- interval arithmetic (mpmath.iv)


def _iv_frac(x) -> "iv.mpf":
    fr = Fraction(x) if not isinstance(x, Fraction) else x
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)


def iv_lo(x) -> "mp.mpf":
    """Lower end point of an interval as an (exact) mpf."""
    return mp.make_mpf(x._mpi_[0])


def iv_hi(x) -> "mp.mpf":
    """Upper end point of an interval as an (exact) mpf."""
    return mp.make_mpf(x._mpi_[1])


def _iv_cosh(x):
    e = iv.exp(x)
    return (e + 1 / e) / 2


def _iv_tanh(x):
    e2 = iv.exp(2 * x)
    return (e2 - 1) / (e2 + 1)


def ustar_enclosure(p: Fraction, u: Fraction, dps: int = 40):
    """Rigorous enclosure ``(lo, hi)`` of the fixed point ``u*``: ``x -> u + g(x) - x`` is strictly decreasing
    (``g' <= 1 - 2p < 1``); its sign is evaluated in interval arithmetic at the two ends."""
    old = mp.mp.dps, iv.dps
    mp.mp.dps = dps + 10
    iv.dps = dps + 10
    try:
        pf, uf = mp.mpf(p.numerator) / p.denominator, mp.mpf(u.numerator) / u.denominator
        x = uf
        for _ in range(100000):
            xn = uf + mp.log(((1 - pf) * mp.e ** x + pf) / (pf * mp.e ** x + 1 - pf))
            if abs(xn - x) < mp.mpf(10) ** (-(dps + 5)):
                x = xn
                break
            x = xn
        delta = mp.mpf(10) ** (-dps)
        lo, hi = x - delta, x + delta
        pi_, ui_ = _iv_frac(p), _iv_frac(u)

        def resid(xv):
            xi = iv.mpf(xv)
            e = iv.exp(xi)
            return ui_ + iv.log(((1 - pi_) * e + pi_) / (pi_ * e + 1 - pi_)) - xi

        if not (iv_lo(resid(lo)) > 0 and iv_hi(resid(hi)) < 0):
            raise AssertionError("enclosure of u* failed")
        return lo, hi
    finally:
        mp.mp.dps, iv.dps = old


class IvBlock:
    """Interval-arithmetic model of the block at exact rational ``(p, u)``: ``u*`` as an enclosure, the block law,
    tables of ``exp(-u a)`` and ``exp(-u* b)``.  Every method returns ``mpmath.iv`` intervals that contain the
    exact real value."""

    def __init__(self, L: int, p, u, dps: int = 30):
        self.L = L
        self.n = 1 << L
        self.p = Fraction(p)
        self.u = Fraction(u)
        self.dps = dps
        iv.dps = dps
        lo, hi = ustar_enclosure(self.p, self.u, dps=dps + 5)
        iv.dps = dps
        self.us_lo, self.us_hi = lo, hi
        self.us = iv.mpf([lo, hi])
        self.ui = _iv_frac(self.u)
        self.pi_ = _iv_frac(self.p)
        self.ratio = self.us / self.ui
        f = block_flips(L)
        lp, lq = iv.log(self.pi_), iv.log(1 - self.pi_)
        self.logpi = [int(f[x]) * lp + int(L - f[x]) * lq for x in range(self.n)]
        self.pi = [self.pi_ ** int(f[x]) * (1 - self.pi_) ** int(L - f[x]) for x in range(self.n)]
        self._ea = {}
        self._eb = {}

    def in_chamber(self, lo: Fraction, hi: Fraction | None) -> bool:
        """Rigorous: is ``lo < u*/u < hi``?"""
        r = self.ratio * lo.denominator - lo.numerator          # > 0 iff ratio > lo
        ok = iv_lo(r) > 0
        if hi is not None:
            ok = ok and iv_hi(self.ratio * hi.denominator - hi.numerator) < 0
        return bool(ok)

    def weights(self, A, B):
        """Unnormalised Gibbs weights ``pi(x) exp(-u A(x) - u* B(x))`` and their logarithms."""
        w, lw = [], []
        for x in range(self.n):
            a, b = int(A[x]), int(B[x])
            if a not in self._ea:
                self._ea[a] = iv.exp(-self.ui * a)
            if b not in self._eb:
                self._eb[b] = iv.exp(-self.us * b)
            w.append(self.pi[x] * self._ea[a] * self._eb[b])
            lw.append(self.logpi[x] - self.ui * a - self.us * b)
        return w, lw

    def gibbs(self, A, B):
        w, lw = self.weights(A, B)
        Z = sum(w[1:], w[0])
        lZ = iv.log(Z)
        return [wx / Z for wx in w], [l - lZ for l in lw]

    def centre(self, Q):
        """Exact normalisation of a positive float vector: ``(Q~, ln Q~)`` with ``Q~ = Q / sum Q``."""
        q = [iv.mpf(float(v)) for v in Q]
        s = sum(q[1:], q[0])
        return [v / s for v in q], [iv.log(v) - iv.log(s) for v in q]

    def kl(self, A, B, lnQ):
        """``KL(pi_phi || Q~)``."""
        P, lP = self.gibbs(A, B)
        acc = P[0] * (lP[0] - lnQ[0])
        for x in range(1, self.n):
            acc += P[x] * (lP[x] - lnQ[x])
        return acc

    def kl_max(self, A_all, B_all, Q):
        """The largest upper end point of ``KL(pi_phi || Q~)`` over the given vertices and the row where it
        occurs, entirely in interval arithmetic (terms are cached by ``(x, A(x), B(x))``)."""
        _, lnQ = self.centre(Q)
        cache = {}
        best, arg = None, -1
        n = self.n
        for i in range(len(A_all)):
            a_row, b_row = A_all[i], B_all[i]
            Z = S = None
            for x in range(n):
                key = (x, int(a_row[x]), int(b_row[x]))
                e = cache.get(key)
                if e is None:
                    a, b = key[1], key[2]
                    if a not in self._ea:
                        self._ea[a] = iv.exp(-self.ui * a)
                    if b not in self._eb:
                        self._eb[b] = iv.exp(-self.us * b)
                    w = self.pi[x] * self._ea[a] * self._eb[b]
                    e = (w, w * (self.logpi[x] - self.ui * a - self.us * b - lnQ[x]))
                    cache[key] = e
                Z = e[0] if Z is None else Z + e[0]
                S = e[1] if S is None else S + e[1]
            val = iv_hi(S / Z - iv.log(Z))
            if best is None or val > best:
                best, arg = val, i
        return best, arg

    def renyi_max(self, A_all, B_all, t, Q):
        """The largest upper end point of ``-ln sum_x pi_phi^t Q~^(1-t)`` over the given vertices (interval
        arithmetic throughout), and the row where it occurs."""
        ti = _iv_frac(Fraction(t))
        _, lnQ = self.centre(Q)
        cache = {}
        best, arg = None, -1
        n = self.n
        for i in range(len(A_all)):
            a_row, b_row = A_all[i], B_all[i]
            Z = S = None
            for x in range(n):
                key = (x, int(a_row[x]), int(b_row[x]))
                e = cache.get(key)
                if e is None:
                    a, b = key[1], key[2]
                    lw = self.logpi[x] - self.ui * a - self.us * b
                    e = (iv.exp(lw), iv.exp(ti * lw + (1 - ti) * lnQ[x]))
                    cache[key] = e
                Z = e[0] if Z is None else Z + e[0]
                S = e[1] if S is None else S + e[1]
            val = iv_hi(ti * iv.log(Z) - iv.log(S))
            if best is None or val > best:
                best, arg = val, i
        return best, arg

    def renyi(self, A, B, t, lnQ):
        """``-ln sum_x pi_phi(x)^t Q~(x)^(1-t)`` for an exact rational (or float, taken exactly) ``t``."""
        ti = _iv_frac(Fraction(t))
        _, lP = self.gibbs(A, B)
        acc = iv.exp(ti * lP[0] + (1 - ti) * lnQ[0])
        for x in range(1, self.n):
            acc += iv.exp(ti * lP[x] + (1 - ti) * lnQ[x])
        return -iv.log(acc)

    def mutual_information(self, rows_A, rows_B, M):
        """``I(M)`` for the weights ``M`` (positive floats, normalised exactly) on the given vertices."""
        m = [iv.mpf(float(v)) for v in M]
        s = sum(m[1:], m[0])
        m = [v / s for v in m]
        laws = [self.gibbs(a, b) for a, b in zip(rows_A, rows_B)]
        Q = [sum((m[k] * laws[k][0][x] for k in range(1, len(m))), m[0] * laws[0][0][x]) for x in range(self.n)]
        lQ = [iv.log(v) for v in Q]
        acc = iv.mpf(0)
        for k, (P, lP) in enumerate(laws):
            for x in range(self.n):
                acc += m[k] * P[x] * (lP[x] - lQ[x])
        return acc

    def G(self, rows_A, rows_B, M, t):
        """``G_t(M) = -t ln sum_x (sum_phi M pi_phi^t)^(1/t)``."""
        ti = _iv_frac(Fraction(t))
        m = [iv.mpf(float(v)) for v in M]
        s = sum(m[1:], m[0])
        m = [v / s for v in m]
        laws = [self.gibbs(a, b)[1] for a, b in zip(rows_A, rows_B)]
        tot = iv.mpf(0)
        for x in range(self.n):
            inner = iv.mpf(0)
            for k in range(len(m)):
                inner += m[k] * iv.exp(ti * laws[k][x])
            tot += iv.exp(iv.log(inner) / ti)
        return -ti * iv.log(tot)


def iv_cube(u, dps: int = 30):
    """Enclosures ``(h, a, E)`` of the exponents of the uniform cube with rational slope ``u``."""
    iv.dps = dps
    hh = _iv_frac(Fraction(u)) / 2
    E = iv.log(_iv_cosh(hh))
    a = hh * _iv_tanh(hh) - E
    # h = max_t [t E - ln cosh(t hh)], strictly concave in t; the maximiser solves tanh(t hh) = E / hh, and the
    # value of the function on an enclosure of the maximiser encloses the maximum
    y = E / hh
    ts = iv.log((1 + y) / (1 - y)) / 2 / hh
    h = ts * E - iv.log(_iv_cosh(ts * hh))
    return h, a, E


def certify_upper(ivb: IvBlock, kind: str, Q, top_vals, top_A, top_B, t=None, margin: float = 1e-7,
                  screen_error: float = 1e-9):
    """Upper bound of the maximum over ALL vertices of the objective at the centre ``Q``, from a scan:

    * the scan (floating point) returned its largest values ``top_vals`` (decreasing) with their vertices;
    * every vertex whose scan value is within ``margin`` of the largest is re-evaluated in interval arithmetic;
    * all the others have scan value ``<= top - margin``, hence true value ``<= top - margin + screen_error``
      provided the scan is accurate to ``screen_error``.  (The scan forms, in IEEE double precision, sums of at
      most 32 terms ``pi(x) e^{-phi(x)}`` and their weighted versions from tabulated exponentials, with
      ``|phi| <= 60`` and logarithmic factors below 200 in modulus: recursive summation and one unit in the last
      place for ``exp`` and ``log`` give an absolute error below ``1e-11``; the default allows ``1e-9``.  This
      is an analysis of the kernel's arithmetic, not an interval computation.)

    Returns ``(upper bound as mpf, number re-evaluated)``.  Raises if the scan's list does not reach below
    ``top - margin`` (then more candidates are needed)."""
    top = float(top_vals[0])
    near = [i for i, v in enumerate(top_vals) if v >= top - margin]
    if len(near) == len(top_vals):
        raise RuntimeError("all scan candidates are within the margin: increase K")
    if kind == "kl":
        best, _ = ivb.kl_max([top_A[i] for i in near], [top_B[i] for i in near], Q)
    else:
        best, _ = ivb.renyi_max([top_A[i] for i in near], [top_B[i] for i in near], t, Q)
    rest = mp.mpf(top) - mp.mpf(margin) + mp.mpf(screen_error)
    return max(best, rest), len(near)
