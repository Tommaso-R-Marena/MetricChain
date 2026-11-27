"""Producer of "shares at the leaves" certificates (the format checked by ``metricchain_eng.leafcert``).

    from metricchain_eng.leafprod import produce
    result = produce({"H": H, "J": J}, time_limit=60, max_leaves=100_000)     # certify L = min E
    result.status, result.L, result.certificate, result.x, result.stats

An instance is the integer tables ``H[i][a]`` and ``J["i,j"][a][b]`` (``i < j``; pairs may be omitted, they are
zero tables) of the energy ``E(x) = sum_i H_i(x_i) + sum_{i<j} J_ij(x_i, x_j)``.  ``produce`` searches for a
branching tree and integer messages at its leaves such that the checker accepts the claim ``E(x) >= L`` for
all ``x``: by default with ``L`` the minimum of ``E`` (found on the way, with a state that attains it), or
with a given ``L``.  It reports ``"certified"`` only after BOTH engines of the checker have accepted the
assembled object; the certificate contains integers only (floating point, where a linear programme is
used, proposes messages and never enters the certificate).

``result.status``:

``"certified"``   ``result.certificate`` is accepted by both engines for ``result.L``; ``result.optimal`` says
                  whether ``result.x`` attains ``L`` (then ``L = min E``; always so when no ``L`` was given).
``"limit"``       not certified within the limits; ``result.reason`` names the limit (``"time"``, ``"leaves"``,
                  ``"cert_integers"``, ``"check_ops"``).  ``result.best_bound`` is the best lower bound; it is
                  certified (``result.bound_checked``, with ``result.certificate`` for that weaker bound) if
                  ``partial=True`` and the partial certificate -- the leaves found, plus the open nodes with
                  their parents' messages -- stays within twice ``max_cert_integers`` and ``max_check_ops``
                  (it may have more leaf boxes than ``max_leaves``); otherwise it is the search's own word.
``"refuted"``     an ``L`` was given and ``result.x`` has energy ``result.energy < L``.
``"rejected"``    the assembled certificate was NOT accepted by both engines (``result.checks``): a defect of
                  this producer, reported and never hidden.
``"solved"``      only with ``certificate=False``: the search is complete, nothing was assembled or checked.

How a leaf is made valid whatever the search did: the search proposes integer messages; ``U`` and ``P2`` of
the leaf are then computed as the exact minima of the two brackets of the leaf rule over the box the leaf
is used on (``kernel.c: lp_eval``), so (S) and (P) hold by construction and only (T), the comparison with
``L``, decides.  The checker repeats all of it with its own code.

Modules: ``model`` (sparse integer form of an instance), ``kernel.c`` / ``ckernel`` (integer message passing,
exact evaluation; ``pykernel`` is the same in plain Python), ``lpbound`` (the linear programme of the
relaxation, rounded), ``search`` (branch and bound, branching rules, shared leaves), ``exact`` (enumeration
and dynamic programming: test oracles and baselines), ``families`` (seeded instance generators), ``formats``
(sizes and checking costs in the dense format and in a sparse variant).
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np

from ..leafcert import check
from .model import InstanceError, Model
from .search import BOUNDS, BRANCHINGS, LEAF, OPEN, ORDERS, Cert, ProducerError, Search

__all__ = ["produce", "Result", "InstanceError", "ProducerError", "checker_ops", "root_relaxation"]

CHECKER_MAX_INTS = 1 << 26       # LC_MAX_INTS of leafcert.c: integers of the instance; of the leaf certificates


@dataclass
class Result:
    """Outcome of :func:`produce` (see the module docstring for ``status``)."""
    status: str
    L: int | None                    # the bound certified (status "certified"), else None
    certificate: dict | None         # the object in the checker's format (for ``best_bound`` if status "limit")
    x: list | None                   # the best state found
    energy: int | None               # its energy (an upper bound of min E)
    optimal: bool                    # certified and energy == L
    best_bound: int | None           # best lower bound of min E obtained
    bound_checked: bool              # ``best_bound`` is certified by ``certificate`` (both engines accepted)
    reason: str                      # one line
    stats: dict = field(default_factory=dict)
    checks: dict = field(default_factory=dict)      # per engine: the checker's result as a dict

    def __bool__(self):
        return self.status == "certified"


class _Dense:
    """Writes sparse leaf certificates in the dense form of the format."""

    def __init__(self, model):
        n = model.n
        self.model = model
        self.pair_keys = [f"{i},{j}" for i in range(n) for j in range(i + 1, n)]
        index = lambda i, j: i * n - i * (i + 1) // 2 + (j - i - 1)        # noqa: E731
        self.edge_pos = np.array([index(int(model.eu[e]), int(model.ev[e])) for e in range(model.ne)], dtype=np.int64)
        self.ordered = []
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                e = model.edge_index.get((min(i, j), max(i, j)))
                if e is None:
                    self.ordered.append((f"{i},{j}", -1, -1, int(model.k[i])))
                else:
                    start = int(model.moff[e]) + (0 if i < j else int(model.k[j]))
                    self.ordered.append((f"{i},{j}", start, start + int(model.k[i]), int(model.k[i])))

    def leaf(self, m, U, P):
        p2 = np.zeros(len(self.pair_keys), dtype=np.int64)
        if self.model.ne:
            p2[self.edge_pos] = P
        flat = m.tolist()
        return {"U": U.tolist(), "P2": dict(zip(self.pair_keys, p2.tolist())),
                "m": {key: (flat[s:t] if s >= 0 else [0] * k) for key, s, t, k in self.ordered}}


def _tree_json(root, index_of_open):
    out = {}
    stack = [(root, out)]
    while stack:
        node, slot = stack.pop()
        if node.kind == LEAF:
            slot["leaf"] = node.a
        elif node.kind == OPEN:
            slot["leaf"] = index_of_open[id(node)]
        else:
            slot["site"] = node.a
            kids = slot["children"] = {}
            for a, child in enumerate(node.b):
                kids[str(a)] = sub = {}
                stack.append((child, sub))
    return out


def _assemble(model, kernel, search, certs, L, ref, index_of_open):
    """The certificate object.  ``U`` and ``P2`` of every leaf are recomputed here as exact minima over the
    box the leaf is used on, whatever the search believed."""
    dense = _Dense(model)
    H, J = model.dense_tables()
    leaves = []
    for cert in certs:
        dlen, dom = model.box(cert.path, None if cert.site is None else (cert.site, cert.states))
        total, U, P, _ = kernel.eval(dlen, dom, cert.m)
        if total < L:
            raise ProducerError(f"a leaf certificate evaluates to {total} < L = {L} on its box")
        leaves.append(dense.leaf(cert.m, U, P))
    obj = {"H": H, "J": J, "L": int(L), "leaves": leaves, "tree": _tree_json(search.root, index_of_open)}
    if ref is not None:
        obj["ref"] = [int(v) for v in ref]
    return obj


def _verify(obj, timings):
    """Both engines of the checker; ``(accepted by both with identical counts, {engine: result dict})``."""
    out = {}
    for engine in ("c", "python"):
        t0 = time.perf_counter()
        res = check(obj, engine=engine)
        timings[f"check_{engine}"] = time.perf_counter() - t0
        out[engine] = res.to_dict()
    ok = (out["c"]["verdict"] == "accept" and out["python"]["verdict"] == "accept"
          and out["c"]["counts"] == out["python"]["counts"] and out["c"]["bound"] == out["python"]["bound"])
    return ok, out


def checker_ops(counts):
    """Additions plus comparisons of a checker result's ``counts``."""
    return counts["additions"] + counts["comparisons"]


def root_relaxation(instance):
    """Value of the pairwise relaxation of the whole domain (floating point; ``None`` if the solver failed)."""
    from .lpbound import LPBound
    model = Model(instance)
    sol = LPBound(model).solve(*model.box())
    return None if sol is None else sol["value"]


def produce(instance, L=None, *, time_limit=60.0, max_leaves=100_000, bound="mp", branching="strong", order="best",
            seed=0, certificate=True, partial=True, share=True, max_cert_integers=CHECKER_MAX_INTS,
            max_check_ops=None, kernel="c", restarts=None, sweeps=200, patience=5, root_sweeps=2000,
            root_patience=20, wmode=0, strong_candidates=3, strong_sweeps=2):
    """Produce a certificate for ``E(x) >= L`` on the whole domain of ``instance``.

    ``L``                 the bound to certify; ``None``: the minimum of ``E`` (optimality certificate).
    ``time_limit``        seconds for the search (assembling and checking what it found come on top and are
                          reported in ``stats``).
    ``max_leaves``        largest number of leaf boxes (leaf nodes of the tree).  The search stops as soon as the
                          finished tree is known to exceed this or one of the two limits below (open nodes
                          are counted with what they will need at least).
    ``bound``             leaf messages from ``"mp"`` (integer message passing), ``"lp"`` (the linear programme,
                          rounded) or ``"hybrid"`` (message passing; where it fails, the programme, rounded and
                          polished by message passing).
    ``branching``         the site to branch on, among the free sites that lie on a cycle of free sites:
                          ``"maxdeg"`` (most free neighbours there, then smallest alphabet, then lowest index),
                          ``"maxdom"`` (largest alphabet, then most free neighbours, then lowest index),
                          ``"margin"`` (the site whose two best states the node's messages separate least),
                          ``"strong"`` (re-optimise the children of the ``strong_candidates`` best sites of
                          ``"maxdeg"`` for ``strong_sweeps`` sweeps; take the site whose weakest child is
                          strongest), ``"frac"`` (the site whose marginal in the programme is farthest from a
                          vertex; needs ``"lp"`` or ``"hybrid"``).
    ``order``             ``"best"`` (smallest known bound first) or ``"dfs"``.
    ``seed``              seed of the random restarts of the local search; everything else is deterministic.
    ``certificate``       ``False``: search only (plain branch and bound; nothing is stored, assembled or
                          checked, and the status is ``"solved"`` instead of ``"certified"``).
    ``partial``           on a limit, assemble and check a certificate for the best bound reached.
    ``share``             let children of a node share leaf certificates.
    ``max_cert_integers`` largest number of integers in the leaf certificates (default: the limit of the C
                          engine of the checker, ``2^26``).
    ``max_check_ops``     largest number of additions plus comparisons the checker will have to perform.
    ``kernel``            ``"c"`` or ``"python"`` (the reference implementation, slow).
    """
    t_start = time.perf_counter()
    if bound not in BOUNDS:
        raise ValueError(f"bound must be one of {BOUNDS}")
    if branching not in BRANCHINGS:
        raise ValueError(f"branching must be one of {BRANCHINGS}")
    if branching == "frac" and bound == "mp":
        raise ValueError("branching='frac' needs the linear programme: bound='lp' or 'hybrid'")
    if order not in ORDERS:
        raise ValueError(f"order must be one of {ORDERS}")
    if L is not None and type(L) is not int:
        raise ValueError("L must be an integer or None")
    if kernel not in ("c", "python"):
        raise ValueError("kernel must be 'c' or 'python'")
    model = Model(instance)
    n = model.n
    instance_integers = model.S + sum(int(model.k[i]) * int(model.k[j]) for i in range(n) for j in range(i + 1, n))
    if certificate and instance_integers > CHECKER_MAX_INTS:
        raise InstanceError(f"the dense instance has {instance_integers} integers; the checker's C engine stops at 2^26")
    if kernel == "c":
        from .ckernel import Kernel
    else:
        from .pykernel import Kernel
    ker = Kernel(model)
    lp = None
    if bound != "mp":
        from .lpbound import LPBound
        lp = LPBound(model)
    if restarts is None:
        restarts = 20 + 2 * n
    search = Search(model, ker, lp, L=L, bound=bound, branching=branching, order=order,
                    deadline=t_start + float(time_limit), max_leaves=max_leaves,
                    max_cert_integers=min(max_cert_integers, CHECKER_MAX_INTS) if certificate else float("inf"),
                    max_check_ops=max_check_ops if certificate else None, seed=seed, keep=certificate, share=share,
                    restarts=restarts, sweeps=sweeps, patience=patience, root_sweeps=root_sweeps,
                    root_patience=root_patience, wmode=wmode, strong_candidates=strong_candidates,
                    strong_sweeps=strong_sweeps)
    search.run()
    t_search = time.perf_counter()
    stats = dict(search.stats)
    stats.update({"n": n, "edges": model.ne, "states": int(model.S), "bound": bound, "branching": branching,
                  "order": order, "seed": seed, "kernel": kernel, "instance_integers": instance_integers,
                  "ints_per_leaf": search.ints_per_leaf, "leaf_boxes": search.leaf_boxes,
                  "leaf_certificates": search.ncerts, "depth": search.depth, "check_ops": search.check_ops,
                  "cert_integers": search.ncerts * search.ints_per_leaf, "open_nodes": search.open_nodes,
                  "open_sets": search.open_sets, "open_check_ops": search.open_ops,
                  "time_search": t_search - t_start,
                  "time_assemble": 0.0, "time_check_c": 0.0, "time_check_python": 0.0, "stop": search.stop,
                  "missing_pairs": model.missing_pairs})
    x = None if search.x is None else [int(v) for v in search.x]
    energy = None if x is None else model.energy(x)
    if energy is not None and energy != search.ub:
        raise ProducerError("the C kernel and the Python evaluation disagree on the energy of a state")

    def finish(status, L_out, cert, best, checked, reason, checks=None):
        stats["time_total"] = time.perf_counter() - t_start
        return Result(status=status, L=L_out, certificate=cert, x=x, energy=energy,
                      optimal=bool(status in ("certified", "solved") and L_out == energy), best_bound=best,
                      bound_checked=checked, reason=reason, stats=stats, checks=checks or {})

    if search.stop == "refuted":
        return finish("refuted", None, None, None, False, f"a state of energy {energy} < L = {L} exists")

    timings = {}
    if search.stop is None:                                  # the tree is complete
        target = search.target()
        if not certificate:
            return finish("solved", target, None, target, False, "search complete; no certificate was built")
        t0 = time.perf_counter()
        obj = _assemble(model, ker, search, search.certs, target, x if energy == target else None, {})
        stats["time_assemble"] = time.perf_counter() - t0
        ok, checks = _verify(obj, timings)
        stats["time_check_c"], stats["time_check_python"] = timings["check_c"], timings["check_python"]
        if not ok:
            return finish("rejected", None, obj, None, False, "the checker did not accept the certificate", checks)
        counts = checks["python"]["counts"]
        if (counts["leaf_boxes"], counts["leaf_certificates"], counts["depth"], counts["cert_integers"],
                checker_ops(counts)) != (search.leaf_boxes, search.ncerts, search.depth,
                                         search.ncerts * search.ints_per_leaf, search.check_ops):
            raise ProducerError("the checker's counts differ from the producer's bookkeeping")
        return finish("certified", target, obj, target, True, "accepted by both engines of the checker", checks)

    # a limit was hit: the open nodes are certified, weakly, by their parents' messages
    groups = search.open_groups()
    open_est = [child.est for _, kids in groups for child in kids if child.est is not None]
    root_open = any(parent is None for parent, _ in groups)
    best = None if root_open else min(open_est + [search.target()])
    reason = f"not certified within the limits ({search.stop})"
    extra_ops = sum(search._box_ops(child.path) for _, kids in groups for child in kids)
    fits = ((search.ncerts + len(groups)) * search.ints_per_leaf <= min(2 * max_cert_integers, CHECKER_MAX_INTS)
            and (max_check_ops is None or search.check_ops + extra_ops <= 2 * max_check_ops))
    if not (certificate and partial and fits):
        return finish("limit", None, None, best, False, reason)
    t0 = time.perf_counter()
    certs = list(search.certs)
    index_of_open = {}
    for parent, kids in groups:
        if parent is None:
            certs.append(Cert(model.zero_messages(), (), None, None, 0))
        else:
            certs.append(Cert(kids[0].start, parent.path, parent.a, sorted(child.path[-1][1] for child in kids), 0))
        for child in kids:
            index_of_open[id(child)] = len(certs) - 1
    totals = []
    for cert in certs[len(search.certs):]:
        dlen, dom = model.box(cert.path, None if cert.site is None else (cert.site, cert.states))
        totals.append(ker.eval(dlen, dom, cert.m)[0])
    best = min(totals + [search.target()])
    obj = _assemble(model, ker, search, certs, best, x if energy == best else None, index_of_open)
    stats["time_assemble"] = time.perf_counter() - t0
    ok, checks = _verify(obj, timings)
    stats["time_check_c"], stats["time_check_python"] = timings["check_c"], timings["check_python"]
    if not ok:
        return finish("rejected", None, obj, None, False, "the checker did not accept the partial certificate", checks)
    return finish("limit", None, obj, best, True, reason + f"; certified bound {best}", checks)
