"""Producer of "Z" certificates (capability C2): certified enclosures of partition functions and
of per-state populations.

**Untrusted code.**  It chooses thermal dead-end eliminations, the pairs to relax with their
additive parts, and an elimination order; the checker (`zcheck`) recomputes every bound.  A bug
here can cost tightness or cause an abstention, never an unsound interval.

Heuristics (none of them is claimed to be good):

* thermal dead-end elimination: remove state `r` of site `i` when some surviving `t` has a
  Goldstein margin of at least `tau` (energy units) on the current box;
* relaxation: for every pair, the row-plus-column additive fit `f(a) + g(b)` of its table on the
  current box (rounded to table units); the pair is relaxed when the oscillation of the rest is
  at most `theta` (energy units).  Pairs of the kept site are never relaxed;
* elimination order: greedy by the size of the table that eliminating a site would create.

`tau = None` and `theta = None` switch the two rules off; the result is then exact up to the
width of the certified exponential.  The producer abstains (`PartitionBudgetExceeded`) when its
order would create a table with more than `max_entries` entries.
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np

from .model import PairModel
from .zcert import ZCertificate
from .zcheck import check_partition_certificate

__all__ = ["certify_partition", "PartitionBudgetExceeded", "plan_order"]


class PartitionBudgetExceeded(RuntimeError):
    """No certificate within the table budget — an abstention."""


def plan_order(sizes: dict, edges: set, keep=None):
    """Greedy elimination order and the size of the largest table it creates.

    `sizes[i]` = number of states of site `i` on the working box; `edges` = set of pairs `(i, j)`
    that still carry a table.  The kept site is in every table of its neighbours and is never
    eliminated."""
    adj = {i: set() for i in sizes}
    for (i, j) in edges:
        adj[i].add(j)
        adj[j].add(i)
    order, largest = [], 1
    todo = set(sizes) - ({keep} if keep is not None else set())
    while todo:
        def cost(v):
            c = sizes[v]
            for u in adj[v]:
                c *= sizes[u]
            return (c, v)
        v = min(todo, key=cost)
        largest = max(largest, cost(v)[0])
        nb = adj.pop(v)
        for u in nb:
            adj[u].discard(v)
            adj[u] |= (nb - {u})
        todo.discard(v)
        order.append(v)
    return order, largest


def certify_partition(model: PairModel, beta: Fraction, domains=None, keep=None, tau=None, theta=None,
                      max_entries: int = 5_000_000, arithmetic: str = "exact", exp_bits: int = 64) -> ZCertificate:
    """A checked certificate for `ln Z` over the box (and, with `keep`, for the populations of that
    site).  `tau`, `theta` are in energy units (floats or rationals); see the module docstring."""
    beta = Fraction(beta)
    n = model.n
    scale = 2 ** model.scale_bits
    D = [list(d) for d in (model.full_domains() if domains is None else domains)]
    H = [np.array([int(v) for v in u.tolist()], dtype=np.int64) for u in model.unary]
    J = {key: np.array([[int(v) for v in row] for row in t.tolist()], dtype=np.int64) for key, t in model.pair.items()}
    nbrs = {i: set(model.neighbors(i)) for i in range(n)}

    def table(i, j):
        return J[(i, j)] if i < j else J[(j, i)].T

    steps = []
    if tau is not None:
        tau_int = int(Fraction(tau) * scale) if not isinstance(tau, float) else int(tau * scale)
        changed = True
        while changed:
            changed = False
            for i in range(n):
                Di = np.array(D[i])
                if len(Di) <= 1:
                    continue
                margin = H[i][Di][:, None] - H[i][Di][None, :]
                for j in nbrs[i]:
                    A = table(i, j)[np.ix_(Di, np.array(D[j]))]
                    margin = margin + (A[:, None, :] - A[None, :, :]).min(axis=2)
                np.fill_diagonal(margin, np.iinfo(np.int64).min // 4)
                alive = np.ones(len(Di), dtype=bool)
                for r in np.argsort(-margin.max(axis=1), kind="stable"):
                    cand = np.where(alive & (margin[r] >= tau_int))[0]
                    cand = cand[cand != r]
                    if cand.size and alive[r]:
                        t = cand[np.argmax(margin[r][cand])]
                        steps.append({"op": "prune", "site": int(i), "remove": int(Di[r]), "dominator": int(Di[t])})
                        alive[r] = False
                        changed = True
                D[i] = [int(a) for a in Di[alive]]

    edges = set(J)
    if theta is not None:
        theta_int = int(Fraction(theta) * scale) if not isinstance(theta, float) else int(theta * scale)
        for (i, j) in sorted(J):
            if keep in (i, j):
                continue
            Di, Dj = np.array(D[i]), np.array(D[j])
            A = J[(i, j)][np.ix_(Di, Dj)].astype(np.float64)
            f = np.rint(A.mean(axis=1)).astype(np.int64)
            g = np.rint((A - f[:, None]).mean(axis=0)).astype(np.int64)
            R = J[(i, j)][np.ix_(Di, Dj)] - f[:, None] - g[None, :]
            if int(R.max() - R.min()) <= theta_int:
                f_full = [0] * model.sizes[i]
                g_full = [0] * model.sizes[j]
                for a, v in zip(Di.tolist(), f.tolist()):
                    f_full[a] = int(v)
                for b, v in zip(Dj.tolist(), g.tolist()):
                    g_full[b] = int(v)
                steps.append({"op": "relax", "pair": [i, j], "f": f_full, "g": g_full})
                edges.discard((i, j))

    sizes = {i: len(D[i]) for i in range(n)}
    order, largest = plan_order(sizes, edges, keep)
    if largest > max_entries:
        raise PartitionBudgetExceeded(f"the elimination order found needs a table of {largest} entries "
                                      f"(budget {max_entries})")
    cert = ZCertificate(model=model, beta=beta, domains=[list(d) for d in (model.full_domains() if domains is None else domains)],
                        steps=steps, order=order, keep=keep,
                        meta={"producer": "metricchain_sb.partition.certify_partition", "tau": None if tau is None else str(tau),
                              "theta": None if theta is None else str(theta), "planned_largest_table": int(largest),
                              "arithmetic": arithmetic})
    result = check_partition_certificate(cert, arithmetic=arithmetic, max_entries=max_entries, exp_bits=exp_bits)
    if not result.accepted:
        raise PartitionBudgetExceeded(f"the checker did not accept the certificate: {result.reason}")
    cert.claim = {"ln_z_lo": result.ln_z_lo, "ln_z_hi": result.ln_z_hi}
    return cert
