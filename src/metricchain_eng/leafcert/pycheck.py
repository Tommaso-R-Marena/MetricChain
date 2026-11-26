"""Plain-Python checker of "shares at the leaves" certificates (Python integers only).

Second implementation, written from the same text as ``leafcert.c`` (science division, ``P7_REPORT.md``
§5.1-5.3 at commit ``2b4ccdf``) and deliberately built differently so that the two can cross-check:

* it reads the object of the JSON file directly (tables addressed by the keys ``"i,j"`` of the file), with
  its own validation -- it shares no code with ``loader.validate`` or with the encoder of the C checker;
* the tree is first flattened into the list of its leaf nodes, each with the path that defines its box,
  and a box is a list of lists of states (the C checker recurses and keeps one array ``fixed[site]``);
* operations are counted from the number of terms evaluated (the C checker increments a counter per
  operation), and on acceptance the total is compared with the closed formula in the sizes of the boxes.

What is checked (``D`` the box of a leaf node: ``D_i = {a}`` if the path fixes site ``i`` to ``a``, the whole
alphabet ``{0..k_i-1}`` otherwise; ``(U, P2, m)`` the leaf certificate the node refers to), in this order:

    (S)  for every site i and every a in D_i:              U_i   <= H_i(a) + sum_{j != i} m_ij(a)
    (P)  for every pair i < j, a in D_i, b in D_j:         P2_ij <= J_ij(a, b) - m_ij(a) - m_ji(b)
    (T)                                                     L     <= sum_i U_i + sum_{i<j} P2_ij

Leaf nodes are visited depth first with the children of a branch in increasing order of the state; the
first inequality that fails in this order is reported.  Cost convention (the one of the table in §5.2 of
the report): a term of (S) is ``n - 1`` additions and one comparison, a term of (P) two additions and one
comparison, (T) ``n + n(n-1)/2 - 1`` additions and one comparison.
"""
from __future__ import annotations

_TOP = frozenset(("H", "J", "L", "tree", "leaves"))
_TOP_MAY = frozenset(("shape", "label", "variant", "instance", "tag", "tau", "split", "order", "unit_log2", "ref",
                      "n_leaf_certificates", "n_leaf_boxes", "depth", "note"))
_LEAF = frozenset(("U", "P2", "m"))
_LEAF_MAY = frozenset(("kind", "box", "LB", "bf_min", "nstates"))


class Malformed(Exception):
    """The object is not a well-formed certificate."""


def _need(condition, message):
    if not condition:
        raise Malformed(message)


def _integers(values):
    """Every element is an ``int`` (``bool`` is not)."""
    return not values or set(map(type, values)) == {int}


def _vector(x, length):
    return type(x) is list and len(x) == length and _integers(x)


class Tables:
    """The instance and the leaf certificates of a file, addressed as in the text:
    ``H[i][a]``, ``J[i, j][a][b]`` (i < j), ``leaves[t] = (U, P2, m)`` with ``U[i]``, ``P2[i, j]`` (i < j),
    ``m[i, j][a]`` (i != j)."""

    def __init__(self, obj):
        _need(type(obj) is dict, "the certificate is not an object")
        keys = set(obj)
        _need(_TOP <= keys, f"missing key(s) {sorted(_TOP - keys)}")
        _need(keys <= _TOP | _TOP_MAY, f"unexpected key(s) {sorted(map(repr, keys - _TOP - _TOP_MAY))[:6]}")
        H = obj["H"]
        _need(type(H) is list and len(H) >= 1, "H is not a non-empty list")
        for i, row in enumerate(H):
            _need(type(row) is list and len(row) >= 1, f"H[{i}] is not a non-empty list (empty domain?)")
            _need(_integers(row), f"H[{i}] has an entry that is not an integer")
        self.k = k = [len(row) for row in H]
        self.n = n = len(k)
        if "shape" in obj:
            s = obj["shape"]
            _need(type(s) is list and _integers(s) and s == k, "shape disagrees with H")
        self.pairs = pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        ordered = [(i, j) for i in range(n) for j in range(n) if i != j]
        J = obj["J"]
        pair_keys = {f"{i},{j}" for i, j in pairs}
        ordered_keys = {f"{i},{j}" for i, j in ordered}
        _need(type(J) is dict and J.keys() == pair_keys, "J does not have exactly the keys i,j with i < j")
        self.H = H
        self.J = {}
        for i, j in pairs:
            table = J[f"{i},{j}"]
            _need(type(table) is list and len(table) == k[i] and all(_vector(row, k[j]) for row in table),
                  f"J[{i},{j}] is not a {k[i]} x {k[j]} table of integers")
            self.J[i, j] = table
        self.L = obj["L"]
        _need(type(self.L) is int, "L is not an integer")
        leaves = obj["leaves"]
        _need(type(leaves) is list and len(leaves) >= 1, "leaves is not a non-empty list")
        self.leaves = []
        for t, leaf in enumerate(leaves):
            _need(type(leaf) is dict, f"leaves[{t}] is not an object")
            lk = set(leaf)
            _need(_LEAF <= lk <= _LEAF | _LEAF_MAY, f"leaves[{t}] has missing or unexpected keys")
            _need(_vector(leaf["U"], n), f"leaves[{t}].U is not a list of {n} integers")
            P2, m = leaf["P2"], leaf["m"]
            _need(type(P2) is dict and P2.keys() == pair_keys and _integers(list(P2.values())),
                  f"leaves[{t}].P2 is not an integer per pair i < j")
            _need(type(m) is dict and m.keys() == ordered_keys,
                  f"leaves[{t}].m does not have exactly the keys i,j with i != j")
            for i, j in ordered:
                _need(_vector(m[f"{i},{j}"], k[i]), f"leaves[{t}].m[{i},{j}] is not a list of {k[i]} integers")
            self.leaves.append((leaf["U"], {(i, j): P2[f"{i},{j}"] for i, j in pairs},
                                {(i, j): m[f"{i},{j}"] for i, j in ordered}))
        self.integers_per_leaf = n + len(pairs) + (n - 1) * sum(k)
        self.instance_integers = sum(k) + sum(k[i] * k[j] for i, j in pairs)


def flatten(tree, k, nleaves):
    """The leaf nodes of the tree in the order of the traversal: a list of ``(leaf index, path)`` with
    ``path`` the tuple of the ``(site, state)`` pairs fixed on the way down.  Checks that every branch has
    exactly one child per state of a site not fixed before, and that every leaf certificate is used."""
    n = len(k)
    nodes, pending = [], [(tree, ())]
    while pending:
        node, path = pending.pop()
        _need(type(node) is dict, "a node of the tree is not an object")
        keys = set(node)
        if keys == {"leaf"}:
            t = node["leaf"]
            _need(type(t) is int and 0 <= t < nleaves, f"leaf index {t!r} is not in 0..{nleaves - 1}")
            nodes.append((t, path))
        elif keys == {"site", "children"}:
            site, children = node["site"], node["children"]
            _need(type(site) is int and 0 <= site < n, f"branch site {site!r} is not in 0..{n - 1}")
            _need(all(site != s for s, _ in path), f"branch on site {site}, already fixed by an ancestor")
            _need(type(children) is dict, "children is not an object")
            wanted = {str(a) for a in range(k[site])}
            have = set(children)
            _need(wanted <= have, f"branch on site {site}: no child for state(s) {sorted(wanted - have)[:6]}")
            _need(have <= wanted, f"branch on site {site}: child(ren) {sorted(map(repr, have - wanted))[:6]} "
                                  f"for something that is not a state of the site")
            for a in range(k[site] - 1, -1, -1):
                pending.append((children[str(a)], path + ((site, a),)))
        else:
            raise Malformed("a node of the tree is neither {leaf} nor {site, children}")
    unused = sorted(set(range(nleaves)) - {t for t, _ in nodes})
    _need(not unused, f"leaf certificate(s) {unused[:6]} not referenced by the tree")
    return nodes


def box_of(path, k):
    """The box of a leaf node as a list of lists of states."""
    fixed = dict(path)
    return [[fixed[i]] if i in fixed else list(range(k[i])) for i in range(len(k))]


def first_violation(tab, t, box, L):
    """Evaluate leaf certificate ``t`` on ``box`` for the bound ``L``.  Returns ``(failure, site_terms,
    pair_terms, total_done)``: ``failure`` is ``None`` or the first inequality that fails, as a dict; the
    three numbers say how many terms of (S), of (P) and whether (T) were evaluated."""
    n, H, J = tab.n, tab.H, tab.J
    U, P2, m = tab.leaves[t]
    site_terms = pair_terms = 0
    for i in range(n):
        others = [m[i, j] for j in range(n) if j != i]
        for a in box[i]:
            value = H[i][a]
            for vec in others:
                value += vec[a]
            site_terms += 1
            if not U[i] <= value:
                return ({"inequality": "site", "i": i, "a": a, "j": None, "b": None, "lhs": U[i], "rhs": value},
                        site_terms, pair_terms, False)
    for i, j in tab.pairs:
        table, mij, mji, bound = J[i, j], m[i, j], m[j, i], P2[i, j]
        for a in box[i]:
            row, ma = table[a], mij[a]
            for b in box[j]:
                value = row[b] - ma - mji[b]
                pair_terms += 1
                if not bound <= value:
                    return ({"inequality": "pair", "i": i, "a": a, "j": j, "b": b, "lhs": bound, "rhs": value},
                            site_terms, pair_terms, False)
    total = 0
    for value in U:
        total += value
    for pair in tab.pairs:
        total += P2[pair]
    if not L <= total:
        return ({"inequality": "total", "i": None, "a": None, "j": None, "b": None, "lhs": L, "rhs": total},
                site_terms, pair_terms, True)
    return None, site_terms, pair_terms, True


def cost(n, site_terms, pair_terms, total_done):
    """(additions, comparisons) of the terms evaluated, in the convention of the module docstring."""
    additions = (n - 1) * site_terms + 2 * pair_terms
    comparisons = site_terms + pair_terms
    if total_done:
        additions += n + n * (n - 1) // 2 - 1
        comparisons += 1
    return additions, comparisons


def box_cost(n, sizes):
    """Closed formula for a leaf that passes on a box with ``sizes[i]`` states of site ``i``."""
    s1 = sum(sizes)
    s2 = (s1 * s1 - sum(d * d for d in sizes)) // 2
    return cost(n, s1, s2, True)


def verify(obj):
    """Check the object of a certificate file.  Returns a dict with the keys ``accepted``, ``kind`` (``None``,
    ``"format"`` or ``"inequality"``), ``reason``, ``failure`` (the first failing inequality with its
    location, or ``None``), ``bound`` and ``counts``."""
    try:
        tab = Tables(obj)
        nodes = flatten(obj["tree"], tab.k, len(tab.leaves))
    except Malformed as exc:
        return {"accepted": False, "kind": "format", "reason": str(exc), "failure": None, "bound": None, "counts": None}
    n, k, L = tab.n, tab.k, tab.L
    counts = {"leaf_certificates": len(tab.leaves), "leaf_boxes": len(nodes),
              "depth": max(len(path) for _, path in nodes),
              "cert_integers": len(tab.leaves) * tab.integers_per_leaf, "instance_integers": tab.instance_integers,
              "additions": 0, "comparisons": 0}
    closed_add = closed_cmp = 0
    for visit, (t, path) in enumerate(nodes):
        box = box_of(path, k)
        failure, site_terms, pair_terms, total_done = first_violation(tab, t, box, L)
        add, cmp_ = cost(n, site_terms, pair_terms, total_done)
        counts["additions"] += add
        counts["comparisons"] += cmp_
        if failure is not None:
            failure = {"inequality": failure["inequality"], "visit": visit, "leaf": t, "path": [list(p) for p in path],
                       "i": failure["i"], "a": failure["a"], "j": failure["j"], "b": failure["b"],
                       "lhs": failure["lhs"], "rhs": failure["rhs"]}
            return {"accepted": False, "kind": "inequality", "reason": describe(failure), "failure": failure,
                    "bound": L, "counts": counts}
        add, cmp_ = box_cost(n, [len(dom) for dom in box])
        closed_add += add
        closed_cmp += cmp_
    if (closed_add, closed_cmp) != (counts["additions"], counts["comparisons"]):       # cannot happen
        raise AssertionError("operation counts disagree with the closed formula")
    return {"accepted": True, "kind": None, "reason": "all inequalities hold", "failure": None, "bound": L, "counts": counts}


def describe(failure):
    """One line for a failing inequality."""
    where = "leaf node %d (leaf certificate %d, path %s)" % (
        failure["visit"], failure["leaf"], " ".join(f"x{s}={a}" for s, a in failure["path"]) or "root")
    if failure["inequality"] == "site":
        return (f"{where}: U_{failure['i']} = {failure['lhs']} > {failure['rhs']} = H_{failure['i']}({failure['a']}) "
                f"+ sum_j m_{failure['i']}j({failure['a']})")
    if failure["inequality"] == "pair":
        i, j, a, b = failure["i"], failure["j"], failure["a"], failure["b"]
        return f"{where}: P2_{i},{j} = {failure['lhs']} > {failure['rhs']} = J_{i},{j}({a},{b}) - m_{i},{j}({a}) - m_{j},{i}({b})"
    return f"{where}: L = {failure['lhs']} > {failure['rhs']} = sum U + sum P2"
