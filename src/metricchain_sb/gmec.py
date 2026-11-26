"""Producer of "min" certificates: certified global-minimum-energy conformation (GMEC).

**Untrusted code.**  Everything here is heuristic search: Goldstein dead-end elimination, a
floating-point dual solver (max-product linear programming, MPLP — block coordinate ascent on the
dual of the local-polytope relaxation), iterated conditional modes for incumbents, and depth-first
branch and bound.  Its only obligation is to emit a certificate that the independent checker
(`metricchain_sb.mincheck`, or the theory division's reference checker after
`mincert.to_metricchain_cert1`) accepts; a bug here can cause a rejected certificate or an
abstention, never an unsound acceptance.

Algorithm (theory division, `docs/BLUEPRINT.md` §6.1, `MINCERT`, without the `sum` rule):

    node(D):  dead-end elimination on D           -> prune nodes
              dual bound b from rounded messages  -> leaf if b >= L = U - eps
              otherwise branch on one site and recurse

where `U` is the energy of the best configuration found so far.  The claimed bound is
`L = U - eps` with the final `U`; since `U` only decreases during the search, every leaf emitted
earlier remains valid.
"""
from __future__ import annotations

import time
from fractions import Fraction

import numpy as np

from .mincert import MinCertificate
from .model import PairModel

__all__ = ["certify_gmec", "CertificationBudgetExceeded", "dead_end_elimination", "icm"]

_ENTRY_LIMIT = 2 ** 50


class CertificationBudgetExceeded(RuntimeError):
    """The producer gave up (node or time budget): no certificate was produced — an abstention."""


class _Problem:
    """Integer tables at certificate scale plus float copies for the dual solver."""

    def __init__(self, model: PairModel, message_bits: int):
        mb = 2 ** message_bits
        if model.max_abs_entry() * mb >= _ENTRY_LIMIT:
            raise ValueError("table magnitude times 2**message_bits exceeds the supported integer range; "
                             "clip clash energies or lower message_bits")
        self.model = model
        self.n = model.n
        self.sizes = model.sizes
        self.H = [np.array([int(v) for v in u.tolist()], dtype=np.int64) * mb for u in model.unary]
        self.J = {key: np.array([[int(v) for v in row] for row in t.tolist()], dtype=np.int64) * mb
                  for key, t in model.pair.items()}
        self.Hf = [h.astype(np.float64) for h in self.H]
        self.Jf = {key: t.astype(np.float64) for key, t in self.J.items()}
        self.nbrs = [model.neighbors(i) for i in range(self.n)]
        self.edges = list(self.J)

    def table(self, i, j):
        """Integer table indexed [state of i, state of j]."""
        return self.J[(i, j)] if i < j else self.J[(j, i)].T

    def energy(self, x) -> int:
        e = sum(int(self.H[i][a]) for i, a in enumerate(x))
        for (i, j), t in self.J.items():
            e += int(t[x[i], x[j]])
        return e


def dead_end_elimination(P: _Problem, D: list) -> list:
    """Goldstein singles on the box `D` (list of sorted int arrays, modified in place).

    Returns the eliminations `(site, removed, dominator)` in the order in which they are valid.
    Exact integer arithmetic; a state is removed when its margin against a surviving dominator is
    nonnegative."""
    out = []
    queue = list(range(P.n))
    queued = set(queue)
    while queue:
        i = queue.pop()
        queued.discard(i)
        Di = D[i]
        k = len(Di)
        if k <= 1:
            continue
        margin = P.H[i][Di][:, None] - P.H[i][Di][None, :]           # margin[r, t]
        for j in P.nbrs[i]:
            A = P.table(i, j)[np.ix_(Di, D[j])]
            margin = margin + (A[:, None, :] - A[None, :, :]).min(axis=2)
        np.fill_diagonal(margin, -1)
        alive = np.ones(k, dtype=bool)
        changed = False
        for r in np.argsort(-margin.max(axis=1), kind="stable"):
            if not alive[r]:
                continue
            cand = np.where(alive & (margin[r] >= 0))[0]
            cand = cand[cand != r]
            if cand.size:
                t = cand[np.argmax(margin[r][cand])]
                out.append((i, int(Di[r]), int(Di[t])))
                alive[r] = False
                changed = True
        if changed:
            D[i] = Di[alive]
            for j in P.nbrs[i]:
                if j not in queued:
                    queue.append(j)
                    queued.add(j)
    return out


def icm(P: _Problem, D: list, x: list, sweeps: int = 50) -> list:
    """Iterated conditional modes inside the box `D`, exact integer energies; returns a local minimum."""
    x = list(x)
    for _ in range(sweeps):
        changed = False
        for i in range(P.n):
            Di = D[i]
            if len(Di) <= 1:
                continue
            cost = P.H[i][Di].copy()
            for j in P.nbrs[i]:
                cost += P.table(i, j)[Di, x[j]]
            best = int(Di[int(np.argmin(cost))])
            cur = int(np.where(Di == x[i])[0][0])
            if cost[int(np.argmin(cost))] < cost[cur]:
                x[i] = best
                changed = True
        if not changed:
            break
    return x


class _Dual:
    """MPLP messages on a box; `m[(i, j)]` is a float vector over the positions of `D[i]`."""

    def __init__(self, P: _Problem, D: list, warm: dict | None):
        self.P, self.D = P, D
        self.theta = {e: P.Jf[e][np.ix_(D[e[0]], D[e[1]])] for e in P.edges}
        self.m = {}
        for (i, j) in P.edges:
            for (a, b) in ((i, j), (j, i)):
                vec = None if warm is None else warm.get((a, b))
                self.m[(a, b)] = np.zeros(len(D[a])) if vec is None else vec[D[a]].astype(np.float64)
        self.belief = [P.Hf[i][D[i]].copy() for i in range(P.n)]
        for (a, b), vec in self.m.items():
            self.belief[a] += vec

    def sweep(self):
        m, belief = self.m, self.belief
        for (i, j) in self.P.edges:
            bi = belief[i] - m[(i, j)]
            bj = belief[j] - m[(j, i)]
            th = self.theta[(i, j)]
            to_i = (th + bj[None, :]).min(axis=1)
            to_j = (th + bi[:, None]).min(axis=0)
            m[(i, j)] = 0.5 * (to_i - bi)
            m[(j, i)] = 0.5 * (to_j - bj)
            belief[i] = bi + m[(i, j)]
            belief[j] = bj + m[(j, i)]

    def bound(self) -> float:
        b = sum(float(v.min()) for v in self.belief)
        for (i, j) in self.P.edges:
            b += float((self.theta[(i, j)] - self.m[(i, j)][:, None] - self.m[(j, i)][None, :]).min())
        return b

    def run(self, max_sweeps: int, target: float, tol: float) -> float:
        prev = self.bound()
        for it in range(max_sweeps):
            if prev >= target:
                break
            self.sweep()
            cur = self.bound()
            if it >= 3 and cur - prev <= tol * max(1.0, abs(cur)):
                prev = cur
                break
            prev = cur
        return prev

    def full_messages(self) -> dict:
        """Messages as float vectors over *all* states of the source site (zero outside the box)."""
        out = {}
        for (a, b), vec in self.m.items():
            full = np.zeros(self.P.sizes[a])
            full[self.D[a]] = vec
            out[(a, b)] = full
        return out

    def decode(self) -> list:
        return [int(self.D[i][int(np.argmin(self.belief[i]))]) for i in range(self.P.n)]


def _exact_bound(P: _Problem, D: list, mint: dict) -> int:
    """The leaf bound of `mincert` for integer messages `mint` (full-length int64 vectors)."""
    bound = 0
    for i in range(P.n):
        vals = P.H[i][D[i]].copy()
        for j in P.nbrs[i]:
            vec = mint.get((i, j))
            if vec is not None:
                vals += vec[D[i]]
        bound += int(vals.min())
    for (i, j), table in P.J.items():
        T = table[np.ix_(D[i], D[j])]
        mi, mj = mint.get((i, j)), mint.get((j, i))
        if mi is not None:
            T = T - mi[D[i]][:, None]
        if mj is not None:
            T = T - mj[D[j]][None, :]
        bound += int(T.min())
    return bound


def certify_gmec(model: PairModel, eps: Fraction = Fraction(0), witness=None, message_bits: int = 12,
                 max_nodes: int = 100_000, max_sweeps: int = 300, tol: float = 1e-12,
                 time_limit: float | None = None, domains=None) -> MinCertificate:
    """Find a configuration `x*` and a certificate that `E(x) >= E(x*) - eps` for every `x`.

    `eps` is an exact rational in energy units (`0` asks for a proof of exact optimality).
    `domains` restricts the claim to a box (a non-empty list of states per site); the witness
    then lies in that box and the certificate is about that box only.
    Raises :class:`CertificationBudgetExceeded` (an abstention) when `max_nodes` branch-and-bound
    nodes or `time_limit` seconds do not suffice.
    """
    P = _Problem(model, message_bits)
    n = P.n
    unit = 2 ** (model.scale_bits + message_bits)
    eps_int = int(Fraction(eps) * unit)          # floor: the certified gap never exceeds eps
    if eps_int < 0:
        raise ValueError("eps must be nonnegative")
    t0 = time.monotonic()
    state = {"nodes": 0, "sweeps": 0}

    if domains is None:
        domains = [list(range(k)) for k in P.sizes]
    domains = [sorted(int(a) for a in d) for d in domains]
    if len(domains) != n or any((not d) or d[0] < 0 or d[-1] >= k or len(set(d)) != len(d)
                                for d, k in zip(domains, P.sizes)):
        raise ValueError("domains must give a non-empty, duplicate-free list of existing states for every site")
    D0 = [np.array(d, dtype=np.int64) for d in domains]
    if witness is not None and any(int(a) not in d for a, d in zip(witness, domains)):
        witness = None                       # a witness outside the box is of no use
    if witness is None:
        dual = _Dual(P, D0, None)
        dual.run(max_sweeps=min(max_sweeps, 50), target=np.inf, tol=tol)
        best_x = icm(P, D0, dual.decode())
    else:
        best_x = icm(P, D0, list(witness))
    best = {"x": tuple(best_x), "U": P.energy(best_x)}

    def consider(x):
        e = P.energy(x)
        if e < best["U"]:
            best["U"], best["x"] = e, tuple(x)

    def solve(D: list, warm: dict | None) -> dict:
        state["nodes"] += 1
        if state["nodes"] > max_nodes:
            raise CertificationBudgetExceeded(f"more than {max_nodes} branch-and-bound nodes")
        if time_limit is not None and time.monotonic() - t0 > time_limit:
            raise CertificationBudgetExceeded(f"time limit of {time_limit} s reached")
        D = [d.copy() for d in D]
        prunes = dead_end_elimination(P, D)

        def wrap(node):
            for (i, r, t) in reversed(prunes):
                node = {"node": "prune", "site": i, "remove": r, "dominator": t, "rest": node}
            return node

        if all(len(d) == 1 for d in D):
            consider([int(d[0]) for d in D])
            return wrap({"node": "leaf", "m": {}})

        dual = _Dual(P, D, warm)
        dual.run(max_sweeps=max_sweeps, target=float(best["U"] - eps_int) + 2.0 * len(P.edges) + 1.0, tol=tol)
        full = dual.full_messages()
        mint = {key: np.rint(vec).astype(np.int64) for key, vec in full.items()}
        consider(icm(P, D, dual.decode()))
        if _exact_bound(P, D, mint) >= best["U"] - eps_int:
            return wrap({"node": "leaf", "m": {key: [int(v) for v in vec] for key, vec in mint.items()
                                              if np.any(vec != 0)}})

        # branch on the most ambiguous site: smallest gap between its two best reparameterised unaries
        gaps = []
        for i in range(n):
            if len(D[i]) > 1:
                part = np.partition(dual.belief[i], 1)
                gaps.append((float(part[1] - part[0]), -len(D[i]), i))
        i = min(gaps)[2]
        order = np.argsort(dual.belief[i], kind="stable")
        children = {}
        for pos in order:
            a = int(D[i][pos])
            D2 = list(D)
            D2[i] = np.array([a], dtype=np.int64)
            children[a] = solve(D2, full)
        return wrap({"node": "branch", "site": i, "children": children})

    root = solve(D0, None)
    lower = best["U"] - eps_int
    meta = {"producer": "metricchain_sb.gmec.certify_gmec", "eps": str(Fraction(eps)),
            "bnb_nodes": state["nodes"], "seconds": round(time.monotonic() - t0, 3),
            "message_bits": message_bits, "max_sweeps": max_sweeps}
    return MinCertificate(model=model, message_bits=message_bits, domains=domains,
                          lower_bound=int(lower), witness=tuple(int(a) for a in best["x"]), root=root, meta=meta)
