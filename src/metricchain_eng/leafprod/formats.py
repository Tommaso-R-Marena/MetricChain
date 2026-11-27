"""Sizes and checking costs of a certificate in the dense format, and in a sparse variant of it.

The format of the checker is dense: a table ``J_ij`` for every pair of sites, and in every leaf certificate
a number ``P2_ij`` for every pair and a message vector for every ordered pair, whether the pair interacts or
not.  A *sparse variant* (hypothetical: no checker for it exists here) would list the interacting pairs
(the edges) once and store tables, pair terms and messages for them only; the inequalities of the other
pairs read ``0 <= 0`` and need not be evaluated, and a site's sum runs over its neighbours only.

``costs(instance, certificate)`` counts both, with the cost convention of the checker's report (a term of
(S) is one addition per message in the sum and one comparison; a term of (P) two additions and one
comparison; (T) one addition per term but one, and one comparison).
"""
from __future__ import annotations

from .model import Model


def leaf_boxes(certificate):
    """The paths (tuples of ``(site, state)``) of the leaf nodes of a certificate's tree."""
    out, stack = [], [(certificate["tree"], ())]
    while stack:
        node, path = stack.pop()
        if "leaf" in node:
            out.append(path)
        else:
            site = node["site"]
            for state, child in node["children"].items():
                stack.append((child, path + ((site, int(state)),)))
    return out


def per_leaf_integers(model):
    """``(dense, sparse)`` numbers of integers of one leaf certificate."""
    n = model.n
    return n + n * (n - 1) // 2 + (n - 1) * model.S, n + model.ne + model.M


def instance_integers(model):
    n, k = model.n, model.k.tolist()
    total = sum(k)
    dense = total + (total * total - sum(v * v for v in k)) // 2
    return dense, total + int(model.joff[model.ne])


def box_ops(model, path):
    """``(dense, sparse)`` additions plus comparisons of the leaf rule on the box of ``path``."""
    n, k = model.n, model.k.tolist()
    d = list(k)
    for i, _ in path:
        d[i] = 1
    s1 = sum(d)
    s2 = (s1 * s1 - sum(v * v for v in d)) // 2
    dense = n * s1 + 3 * s2 + n + n * (n - 1) // 2
    site_adds = sum(d[i] * len(model.nbrs[i]) for i in range(n))
    pair_terms = sum(d[int(model.eu[e])] * d[int(model.ev[e])] for e in range(model.ne))
    sparse = site_adds + s1 + 3 * pair_terms + n + model.ne
    return dense, sparse


def leaf_nodes(certificate):
    """``(leaf index, path)`` of the leaf nodes of a certificate's tree."""
    out, stack = [], [(certificate["tree"], ())]
    while stack:
        node, path = stack.pop()
        if "leaf" in node:
            out.append((node["leaf"], path))
        else:
            site = node["site"]
            for state, child in node["children"].items():
                stack.append((child, path + ((site, int(state)),)))
    return out


def costs(instance, certificate):
    """Integers and checker operations of ``certificate`` in the dense format and in the sparse variant.

    Two more counts concern the dense format as it is.  ``message_integers_never_read``: entries
    ``m_ij(a)`` with ``a`` outside every box the leaf certificate is used on (the format wants a vector over
    the whole alphabet; no inequality reads these).  ``check_ops_split_rule``: the operations if every leaf
    certificate were checked once, on the smallest box that contains the boxes of the nodes naming it,
    instead of once per node -- what a rule "these states | the others" in the tree would allow.  It is
    counted only if that is sound for the certificate at hand, i.e. if the nodes naming a leaf differ in
    one site at most (true for the certificates of this producer); otherwise it is ``None``.
    """
    model = instance if isinstance(instance, Model) else Model(instance)
    n, k = model.n, model.k.tolist()
    nodes = leaf_nodes(certificate)
    leaves = len(certificate["leaves"])
    dense_leaf, sparse_leaf = per_leaf_integers(model)
    dense_inst, sparse_inst = instance_integers(model)
    dense_ops = sparse_ops = 0
    fixed = [dict() for _ in range(leaves)]              # per leaf certificate: site -> states it is fixed to
    free = [set() for _ in range(leaves)]                # sites that are free in a box of the certificate
    paths = [[] for _ in range(leaves)]
    for t, path in nodes:
        a, b = box_ops(model, path)
        dense_ops += a
        sparse_ops += b
        paths[t].append(path)
        on_path = dict(path)
        for i, state in on_path.items():
            fixed[t].setdefault(i, set()).add(state)
        free[t].update(i for i in range(n) if i not in on_path)
    never_read = 0
    split_ops = 0
    for t in range(leaves):
        used = [k[i] if i in free[t] else len(fixed[t][i]) for i in range(n)]
        never_read += (n - 1) * sum(k[i] - used[i] for i in range(n))
        if split_ops is not None:
            sites = {frozenset(i for i, _ in path) for path in paths[t]}
            varying = [i for i in fixed[t] if i not in free[t] and len(fixed[t][i]) > 1]
            if len(sites) == 1 and len(varying) <= 1:
                s1 = sum(used)
                s2 = (s1 * s1 - sum(v * v for v in used)) // 2
                split_ops += n * s1 + 3 * s2 + n + n * (n - 1) // 2
            else:
                split_ops = None
    return {"leaf_boxes": len(nodes), "leaf_certificates": leaves,
            "dense": {"instance_integers": dense_inst, "cert_integers": leaves * dense_leaf, "check_ops": dense_ops,
                      "message_integers": leaves * (n - 1) * model.S, "message_integers_never_read": never_read,
                      "check_ops_split_rule": split_ops},
            "sparse": {"instance_integers": sparse_inst, "cert_integers": leaves * sparse_leaf, "check_ops": sparse_ops}}
