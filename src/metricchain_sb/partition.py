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


class _State:
    """Working model and box of the producer (integer tables; copied at every branch)."""

    def __init__(self, model: PairModel, domains):
        self.n = model.n
        self.sizes_full = model.sizes
        self.D = [list(d) for d in domains]
        self.H = [np.array([int(v) for v in u.tolist()], dtype=np.int64) for u in model.unary]
        self.J = {key: np.array([[int(v) for v in row] for row in t.tolist()], dtype=np.int64)
                  for key, t in model.pair.items()}
        self.nbrs = {i: set(model.neighbors(i)) for i in range(model.n)}

    def copy(self) -> "_State":
        other = object.__new__(_State)
        other.n, other.sizes_full = self.n, self.sizes_full
        other.D = [list(d) for d in self.D]
        other.H = [h.copy() for h in self.H]
        other.J = dict(self.J)                       # tables are never modified, only removed
        other.nbrs = {i: set(v) for i, v in self.nbrs.items()}
        return other

    def table(self, i, j):
        return self.J[(i, j)] if i < j else self.J[(j, i)].T


def _node_steps(st: _State, keep, tau_int, theta_int) -> list:
    """Thermal dead-end eliminations, then relaxations, applied to `st`; returns the steps."""
    steps = []
    if tau_int is not None:
        changed = True
        while changed:
            changed = False
            for i in range(st.n):
                Di = np.array(st.D[i])
                if len(Di) <= 1:
                    continue
                margin = st.H[i][Di][:, None] - st.H[i][Di][None, :]
                for j in st.nbrs[i]:
                    A = st.table(i, j)[np.ix_(Di, np.array(st.D[j]))]
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
                st.D[i] = [int(a) for a in Di[alive]]
    if theta_int is not None:
        for (i, j) in sorted(st.J):
            if keep in (i, j):
                continue
            Di, Dj = np.array(st.D[i]), np.array(st.D[j])
            block = st.J[(i, j)][np.ix_(Di, Dj)]
            f = np.rint(block.astype(np.float64).mean(axis=1)).astype(np.int64)
            g = np.rint((block - f[:, None]).astype(np.float64).mean(axis=0)).astype(np.int64)
            R = block - f[:, None] - g[None, :]
            if int(R.max() - R.min()) <= theta_int:
                f_full = np.zeros(st.sizes_full[i], dtype=np.int64)
                g_full = np.zeros(st.sizes_full[j], dtype=np.int64)
                f_full[Di] = f
                g_full[Dj] = g
                steps.append({"op": "relax", "pair": [int(i), int(j)], "f": [int(v) for v in f_full],
                              "g": [int(v) for v in g_full]})
                st.H[i] = st.H[i] + f_full
                st.H[j] = st.H[j] + g_full
                del st.J[(i, j)]
                st.nbrs[i].discard(j)
                st.nbrs[j].discard(i)
    return steps


def _to_int(value, scale):
    if value is None:
        return None
    return int(value * scale) if isinstance(value, float) else int(Fraction(value) * scale)


def certify_partition(model: PairModel, beta: Fraction, domains=None, keep=None, tau=None, theta=None,
                      max_entries: int = 5_000_000, arithmetic: str = "exact", exp_bits: int = 64,
                      max_leaves: int = 1) -> ZCertificate:
    """A checked certificate for `ln Z` over the box (and, with `keep`, for the populations of that
    site).  `tau`, `theta` are in energy units (floats or rationals); see the module docstring.

    When the elimination order found would need a table of more than `max_entries` entries the
    producer conditions on a site (a `branch` node) and plans each sub-box separately, as long as
    the number of leaves stays within `max_leaves` (default 1: no conditioning); otherwise it
    abstains with :class:`PartitionBudgetExceeded`."""
    beta = Fraction(beta)
    scale = 2 ** model.scale_bits
    root_domains = [list(d) for d in (model.full_domains() if domains is None else domains)]
    tau_int, theta_int = _to_int(tau, scale), _to_int(theta, scale)
    leaves = {"count": 0, "largest": 1}

    def plan(st: _State) -> dict:
        steps = _node_steps(st, keep, tau_int, theta_int)
        sizes = {i: len(st.D[i]) for i in range(st.n)}
        order, largest = plan_order(sizes, set(st.J), keep)
        if largest <= max_entries:
            leaves["count"] += 1
            leaves["largest"] = max(leaves["largest"], largest)
            if leaves["count"] > max_leaves:
                raise PartitionBudgetExceeded(f"more than {max_leaves} leaves would be needed")
            return {"steps": steps, "order": order}
        if max_leaves <= 1:
            raise PartitionBudgetExceeded(f"the elimination order found needs a table of {largest} entries "
                                          f"(budget {max_entries}) and conditioning is not allowed")
        # condition on the site whose fixing shrinks the largest table most (a few candidates only)
        degree = {i: sum(1 for (a, b) in st.J if i in (a, b)) for i in range(st.n)}
        candidates = sorted((i for i in range(st.n) if i != keep and sizes[i] > 1),
                            key=lambda i: -(degree[i] * np.log(sizes[i])))[:6]
        if not candidates:
            raise PartitionBudgetExceeded("no site left to condition on")
        best = None
        for i in candidates:
            trial = dict(sizes)
            trial[i] = 1
            _, big = plan_order(trial, {e for e in st.J if i not in e}, keep)
            if best is None or (big, sizes[i]) < best[0]:
                best = ((big, sizes[i]), i)
        site = best[1]
        children = {}
        for a in st.D[site]:
            child = st.copy()
            child.D[site] = [a]
            children[int(a)] = plan(child)
        return {"steps": steps, "branch": int(site), "children": children}

    root = plan(_State(model, root_domains))
    cert = ZCertificate(model=model, beta=beta, domains=root_domains, steps=root["steps"], order=root.get("order", []),
                        keep=keep, branch=root.get("branch"), children=root.get("children"),
                        meta={"producer": "metricchain_sb.partition.certify_partition", "tau": None if tau is None else str(tau),
                              "theta": None if theta is None else str(theta), "planned_largest_table": int(leaves["largest"]),
                              "planned_leaves": int(leaves["count"]), "arithmetic": arithmetic})
    result = check_partition_certificate(cert, arithmetic=arithmetic, max_entries=max_entries, exp_bits=exp_bits)
    if not result.accepted:
        raise PartitionBudgetExceeded(f"the checker did not accept the certificate: {result.reason}")
    cert.claim = {"ln_z_lo": result.ln_z_lo, "ln_z_hi": result.ln_z_hi}
    return cert
