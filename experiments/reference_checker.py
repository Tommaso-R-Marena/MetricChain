#!/usr/bin/env python3
"""
Reference implementation of the MetricChain certificate checkers (format `metricchain-cert/1`,
docs/BLUEPRINT.md §4-§5) in exact rational arithmetic.

This file is NOT part of the trusted base: the trusted checkers are the Lean definitions
`verify`, `verifyRTop` / `verifyRLowerTop`, `zverifyTop` with their soundness theorems.  It exists
so that an implementation team has (a) an executable reading of the JSON schema, (b) the
conformance vectors that the Lean kernel evaluates (`triangle_verified`, `triangle_rejects`,
`biased_verified`, `triangleResidual_verifiedTop`, `inconsistentResidual_rejected`,
`inconsistentResidual_lowerTop`, `negativeEnvelope_rejected`, `triangleZ_exactTop`,
`triangleZ_coarse`, `negativeW_rejected`), and (c) a fuzzer that checks soundness against brute
force on random instances and random (mostly invalid) certificates.

Side conditions checked at file level (they are part of the top-level Lean kernels):
  * residual, `anchor_semantics = "exact"` (default): `c >= 0` and pairwise compatibility of the
    anchor values with the envelope (Lean `RProblem.Consistent`, which is exactly non-emptiness of
    the residual class, `RProblem.consistent_iff_nonempty`);
  * residual, `anchor_semantics = "lower"` (values are certified lower bounds, e.g. rounded-down
    floats): `c >= 0` only (Lean `verifyRLowerTop`); no upper bound is reported;
  * partition: all factors nonnegative (Lean `zverifyTop`).

Usage:
    python3 experiments/reference_checker.py --selftest [--quick]
    python3 experiments/reference_checker.py CERT.json
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
from fractions import Fraction as Q

# ----------------------------------------------------------------------------------------------
# Parsing
# ----------------------------------------------------------------------------------------------


def q(v) -> Q:
    if isinstance(v, Q):
        return v
    if isinstance(v, int):
        return Q(v)
    if isinstance(v, str):
        return Q(v)
    raise TypeError(f"rationals must be integers or strings 'p/q', got {v!r}")


class Tables:
    """Sparse tables: one-body `h[i][a]`, two-body `J[(i,j)][a][b]`; unlisted pairs take `default`."""

    def __init__(self, n, k, one, two, default):
        self.n, self.k, self.default = n, k, Q(default)
        self.one = [[q(v) for v in row] for row in one]
        self.two = {}
        for key, tab in two.items():
            i, j = (int(s) for s in key.split(",")) if isinstance(key, str) else key
            assert i != j, "diagonal pair tables are ignored by the kernel; do not list them"
            self.two[(i, j)] = [[q(v) for v in row] for row in tab]

    def pair(self, i, j, a, b) -> Q:
        t = self.two.get((i, j))
        return self.default if t is None else t[a][b]


def pairmap(d, default=Q(0)):
    out = {}
    for key, v in (d or {}).items():
        i, j = (int(s) for s in key.split(",")) if isinstance(key, str) else key
        out[(i, j)] = v
    return out, default


# ----------------------------------------------------------------------------------------------
# kind = "min"  (Lean: Cert, verify, verify_sound)
# ----------------------------------------------------------------------------------------------

def energy(I: Tables, x) -> Q:
    e = sum((I.one[i][x[i]] for i in range(I.n)), Q(0))
    for i in range(I.n):
        for j in range(I.n):
            if i != j:
                e += I.pair(i, j, x[i], x[j])
    return e


def link(I: Tables, i, r, t, j, s) -> Q:
    return I.pair(i, j, r, s) + I.pair(j, i, s, r) - I.pair(i, j, t, s) - I.pair(j, i, s, t)


def leaf_ok(I: Tables, D, L: Q, node) -> bool:
    n = I.n
    u = [q(v) for v in node["u"]]
    p, _ = pairmap(node.get("p"))
    m, _ = pairmap(node.get("m"))

    def msg(i, j, a):
        row = m.get((i, j))
        return Q(0) if row is None else q(row[a])

    def pp(i, j):
        return q(p.get((i, j), 0))

    for i in range(n):
        for a in D[i]:
            if not u[i] <= I.one[i][a] + sum((msg(i, j, a) for j in range(n) if j != i), Q(0)):
                return False
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for a in D[i]:
                for b in D[j]:
                    if not 2 * pp(i, j) <= I.pair(i, j, a, b) + I.pair(j, i, b, a) - msg(i, j, a) - msg(j, i, b):
                        return False
    total = sum(u, Q(0)) + sum((pp(i, j) for i in range(n) for j in range(n) if i != j), Q(0))
    return L <= total


def prune_ok(I: Tables, D, node, margin: Q) -> bool:
    i, r, t = node["site"], node["remove"], node["dominator"]
    ell = {int(j): q(v) for j, v in (node.get("ell") or {}).items()}
    if t not in D[i] or t == r:
        return False
    for j in range(I.n):
        if j == i:
            continue
        for s in D[j]:
            if not ell.get(j, Q(0)) <= link(I, i, r, t, j, s):
                return False
    return margin <= I.one[i][r] - I.one[i][t] + sum((ell.get(j, Q(0)) for j in range(I.n) if j != i), Q(0))


def with_site(D, i, states):
    D2 = list(D)
    D2[i] = list(states)
    return D2


def verify_min(node, I: Tables, D, L: Q) -> bool:
    kind = node["node"]
    if kind == "leaf":
        return leaf_ok(I, D, L, node)
    if kind == "branch":
        i = node["site"]
        ch = {int(a): c for a, c in node["children"].items()}
        return all(a in ch and verify_min(ch[a], I, with_site(D, i, [a]), L) for a in D[i])
    if kind == "prune":
        if not prune_ok(I, D, node, Q(0)):
            return False
        i, r = node["site"], node["remove"]
        return verify_min(node["rest"], I, with_site(D, i, [s for s in D[i] if s != r]), L)
    if kind == "sum":
        parts = node["parts"]
        assert len(parts) == 2
        I1, I2 = (Tables(I.n, I.k, pt["instance"]["h"], pt["instance"].get("J", {}), 0) for pt in parts)
        L1, L2 = q(parts[0]["bound"]), q(parts[1]["bound"])
        for i in range(I.n):
            for a in D[i]:
                if not I1.one[i][a] + I2.one[i][a] <= I.one[i][a]:
                    return False
        for i in range(I.n):
            for j in range(I.n):
                if i == j:
                    continue
                for a in D[i]:
                    for b in D[j]:
                        if not I1.pair(i, j, a, b) + I2.pair(i, j, a, b) <= I.pair(i, j, a, b):
                            return False
        if not L <= L1 + L2:
            return False
        return verify_min(parts[0]["certificate"], I1, D, L1) and verify_min(parts[1]["certificate"], I2, D, L2)
    raise ValueError(f"unknown node {kind!r}")


# ----------------------------------------------------------------------------------------------
# kind = "residual"  (Lean: RCert, verifyR, verifyR_sound)
# ----------------------------------------------------------------------------------------------

def anchored(I: Tables, c, x) -> Tables:
    one = [[I.one[i][s] - (Q(0) if s == x[i] else c[i]) for s in range(I.k)] for i in range(I.n)]
    A = Tables(I.n, I.k, one, {}, 0)
    A.two = I.two
    return A


def residual_consistent(c, anchors) -> bool:
    """Lean `RProblem.Consistent`: c >= 0 and v_a - v_b <= sum_i c_i [a_i != b_i] for all anchor pairs."""
    if any(ci < 0 for ci in c):
        return False
    for xa, va in anchors:
        for xb, vb in anchors:
            if va - vb > sum((c[i] for i in range(len(c)) if xa[i] != xb[i]), Q(0)):
                return False
    return True


def verify_residual(node, I: Tables, c, anchors, D, L: Q) -> bool:
    kind = node["node"]
    if kind == "anchor":
        idx = node["index"]
        if not 0 <= idx < len(anchors):
            return False
        x, v = anchors[idx]
        return verify_min(node["cert"], anchored(I, c, x), D, L - v)
    if kind == "branch":
        i = node["site"]
        ch = {int(a): cc for a, cc in node["children"].items()}
        return all(a in ch and verify_residual(ch[a], I, c, anchors, with_site(D, i, [a]), L) for a in D[i])
    if kind == "prune":
        i, r = node["site"], node["remove"]
        if not prune_ok(I, D, node, c[i]):
            return False
        return verify_residual(node["rest"], I, c, anchors, with_site(D, i, [s for s in D[i] if s != r]), L)
    raise ValueError(f"unknown node {kind!r}")


# ----------------------------------------------------------------------------------------------
# kind = "partition"  (Lean: ZCert, zverify, zverify_sound)
# ----------------------------------------------------------------------------------------------

def weight(I: Tables, x) -> Q:
    w = Q(1)
    for i in range(I.n):
        w *= I.one[i][x[i]]
    for i in range(I.n):
        for j in range(I.n):
            if i != j:
                w *= I.pair(i, j, x[i], x[j])
    return w


def zverify(node, I: Tables, D):
    """Returns (lo, hi) or None."""
    kind = node["node"]
    n = I.n
    if kind == "leaf":
        lo, _ = pairmap(node.get("lo"))
        hi, _ = pairmap(node.get("hi"))
        plo = phi = Q(1)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                l, h = q(lo.get((i, j), 1)), q(hi.get((i, j), 1))
                if l < 0:
                    return None
                for a in D[i]:
                    for b in D[j]:
                        if not (l <= I.pair(i, j, a, b) <= h):
                            return None
                plo *= l
                phi *= h
        S = Q(1)
        for i in range(n):
            S *= sum((I.one[i][a] for a in set(D[i])), Q(0))
        return S * plo, S * phi
    if kind == "branch":
        i = node["site"]
        ch = {int(a): c for a, c in node["children"].items()}
        lo = hi = Q(0)
        for a in dict.fromkeys(D[i]):  # distinct states, in order
            if a not in ch:
                return None
            r = zverify(ch[a], I, with_site(D, i, [a]))
            if r is None:
                return None
            lo += r[0]
            hi += r[1]
        return lo, hi
    if kind == "prune":
        i, r, t = node["site"], node["remove"], node["dominator"]
        q0 = q(node["q0"])
        qs = {int(j): q(v) for j, v in (node.get("q") or {}).items()}
        if t not in D[i] or t == r or q0 < 0 or not I.one[i][r] <= q0 * I.one[i][t]:
            return None
        rho = q0
        for j in range(n):
            if j == i:
                continue
            qj = qs.get(j, Q(1))
            if qj < 0:
                return None
            for s in D[j]:
                if not I.pair(i, j, r, s) * I.pair(j, i, s, r) <= qj * (I.pair(i, j, t, s) * I.pair(j, i, s, t)):
                    return None
            rho *= qj
        rest = zverify(node["rest"], I, with_site(D, i, [s for s in D[i] if s != r]))
        if rest is None:
            return None
        return rest[0], (1 + rho) * rest[1]
    raise ValueError(f"unknown node {kind!r}")


# ----------------------------------------------------------------------------------------------
# File-level driver
# ----------------------------------------------------------------------------------------------

def check_file(doc) -> dict:
    assert doc["format"] == "metricchain-cert/1"
    n, k, D = doc["n"], doc["k"], [list(d) for d in doc["domains"]]
    inst = doc["instance"]
    kind = doc["kind"]
    if kind == "min":
        I = Tables(n, k, inst["h"], inst.get("J", {}), 0)
        L = q(doc["claim"]["lower_bound"])
        ok = verify_min(doc["certificate"], I, D, L)
        out = dict(accepted=ok, lower_bound=str(L))
        if ok and "witness" in doc["claim"]:
            w = doc["claim"]["witness"]
            if all(w[i] in D[i] for i in range(n)):
                out["witness_energy"] = str(energy(I, w))
                out["certified_gap"] = str(energy(I, w) - L)
        return out
    if kind == "residual":
        I = Tables(n, k, inst["h"], inst.get("J", {}), 0)
        c = [q(v) for v in inst["c"]]
        anchors = [(a["x"], q(a["value"])) for a in inst["anchors"]]
        L = q(doc["claim"]["lower_bound"])
        semantics = inst.get("anchor_semantics", "exact")
        if semantics not in ("exact", "lower"):
            raise ValueError(f"unknown anchor_semantics {semantics!r}")
        if any(ci < 0 for ci in c):
            return dict(accepted=False, reason="negative envelope constant")
        if semantics == "exact" and not residual_consistent(c, anchors):
            return dict(accepted=False, reason="inconsistent residual data (empty residual class)")
        ok = verify_residual(doc["certificate"], I, c, anchors, D, L)
        out = dict(accepted=ok, lower_bound=str(L))
        if ok and semantics == "exact":
            inbox = [energy(I, x) + v for x, v in anchors if all(x[i] in D[i] for i in range(n))]
            if inbox:
                out["upper_bound"] = str(min(inbox))
        return out
    if kind == "partition":
        I = Tables(n, k, inst["w"], inst.get("W", {}), 1)
        nonneg = all(v >= 0 for row in I.one for v in row) and all(v >= 0 for t in I.two.values() for row in t for v in row)
        r = zverify(doc["certificate"], I, D) if nonneg else None
        if not nonneg:
            return dict(accepted=False, reason="negative factor")
        if r is None:
            return dict(accepted=False)
        claim = doc.get("claim", {})
        ok = (q(claim["lo"]) <= r[0] if "lo" in claim else True) and (r[1] <= q(claim["hi"]) if "hi" in claim else True)
        return dict(accepted=ok, lo=str(r[0]), hi=str(r[1]))
    raise ValueError(kind)


# ----------------------------------------------------------------------------------------------
# Conformance vectors (identical to the kernel-evaluated Lean examples)
# ----------------------------------------------------------------------------------------------

def triangle_J(val_equal, val_other):
    tab = [[val_equal if a == b else val_other for b in range(2)] for a in range(2)]
    return {"0,1": tab, "0,2": tab, "1,2": tab}


def triangle_leaf(a):
    ind = lambda cond: "1" if cond else "0"  # noqa: E731
    return {"node": "leaf", "u": ["0", "1", "0"], "p": {},
            "m": {"1,0": [ind(s == a) for s in range(2)], "2,0": [ind(s == a) for s in range(2)],
                  "1,2": [ind(s != a) for s in range(2)], "2,1": ["-1" if s == a else "0" for s in range(2)]}}


def conformance_docs():
    full = [[0, 1]] * 3
    tri = {"h": [["0", "0"]] * 3, "J": triangle_J("1", "0")}
    cert = {"node": "branch", "site": 0, "children": {"0": triangle_leaf(0), "1": triangle_leaf(1)}}
    docs = {}
    docs["triangle_min"] = dict(format="metricchain-cert/1", kind="min", n=3, k=2, domains=full, instance=tri,
                                claim=dict(lower_bound="1", witness=[0, 1, 0]), certificate=cert)
    docs["triangle_min_reject"] = dict(docs["triangle_min"], claim=dict(lower_bound="2"))
    biased = {"h": [["3", "0"], ["0", "0"], ["0", "0"]], "J": triangle_J("1", "0")}
    docs["biased_dee"] = dict(format="metricchain-cert/1", kind="min", n=3, k=2, domains=full, instance=biased,
                              claim=dict(lower_bound="1", witness=[1, 0, 1]),
                              certificate={"node": "prune", "site": 0, "remove": 0, "dominator": 1,
                                           "ell": {"1": "-1", "2": "-1"}, "rest": triangle_leaf(1)})
    # residual: c = 1/4, anchor (0,1,0) with value -1/8; exhaustive certificate of the anchored instance
    anc = [0, 1, 0]

    def exhaustive(I):
        def leaf(x):
            p = {f"{i},{j}": str((I.pair(i, j, x[i], x[j]) + I.pair(j, i, x[j], x[i])) / 2)
                 for i in range(3) for j in range(3) if i != j}
            return {"node": "leaf", "u": [str(I.one[i][x[i]]) for i in range(3)], "p": p, "m": {}}
        return {"node": "branch", "site": 0, "children": {str(a): {"node": "branch", "site": 1, "children": {
            str(b): {"node": "branch", "site": 2, "children": {str(c): leaf((a, b, c)) for c in range(2)}}
            for b in range(2)}} for a in range(2)}}

    Itri = Tables(3, 2, tri["h"], tri["J"], 0)
    docs["triangle_residual"] = dict(
        format="metricchain-cert/1", kind="residual", n=3, k=2, domains=full,
        instance=dict(tri, c=["1/4"] * 3, anchors=[dict(x=anc, value="-1/8")]),
        claim=dict(lower_bound="1/8"),
        certificate={"node": "anchor", "index": 0, "cert": exhaustive(anchored(Itri, [Q(1, 4)] * 3, anc))})
    # inconsistent residual data (Lean: inconsistentResidual): anchors at Hamming distance 1, values 0 and 10
    anc2 = [1, 1, 0]
    bad = dict(tri, c=["1/4"] * 3, anchors=[dict(x=anc, value="0"), dict(x=anc2, value="10")])
    bad_cert = {"node": "anchor", "index": 1, "cert": exhaustive(anchored(Itri, [Q(1, 4)] * 3, anc2))}
    docs["residual_inconsistent_reject"] = dict(
        format="metricchain-cert/1", kind="residual", n=3, k=2, domains=full, instance=bad,
        claim=dict(lower_bound="41/4"), certificate=bad_cert)
    docs["residual_lower_semantics"] = dict(
        format="metricchain-cert/1", kind="residual", n=3, k=2, domains=full,
        instance=dict(bad, anchor_semantics="lower"), claim=dict(lower_bound="41/4"), certificate=bad_cert)
    docs["residual_negative_c_reject"] = dict(
        format="metricchain-cert/1", kind="residual", n=3, k=2, domains=full,
        instance=dict(tri, c=["-10", "1/4", "1/4"], anchors=[dict(x=anc, value="0")], anchor_semantics="lower"),
        claim=dict(lower_bound="-100"),
        certificate={"node": "anchor", "index": 0,
                     "cert": exhaustive(anchored(Itri, [Q(-10), Q(1, 4), Q(1, 4)], anc))})
    # negative factor (Lean: negativeW): two sites, one state each
    docs["partition_negative_reject"] = dict(
        format="metricchain-cert/1", kind="partition", n=2, k=1, domains=[[0]] * 2,
        instance={"w": [["-1"], ["1"]], "W": {"0,1": [["2"]], "1,0": [["2"]]}}, claim={},
        certificate={"node": "leaf", "lo": {"0,1": "1", "1,0": "1"}, "hi": {"0,1": "3", "1,0": "3"}})
    wtri = {"w": [["1", "1"]] * 3, "W": triangle_J("1/2", "1")}
    Iw = Tables(3, 2, wtri["w"], wtri["W"], 1)

    def zexh():
        def leaf(x):
            tab = {f"{i},{j}": str(Iw.pair(i, j, x[i], x[j])) for i in range(3) for j in range(3) if i != j}
            return {"node": "leaf", "lo": tab, "hi": tab}
        return {"node": "branch", "site": 0, "children": {str(a): {"node": "branch", "site": 1, "children": {
            str(b): {"node": "branch", "site": 2, "children": {str(c): leaf((a, b, c)) for c in range(2)}}
            for b in range(2)}} for a in range(2)}}

    docs["triangle_partition_exact"] = dict(format="metricchain-cert/1", kind="partition", n=3, k=2, domains=full,
                                            instance=wtri, claim=dict(lo="13/4", hi="13/4"), certificate=zexh())
    docs["triangle_partition_coarse"] = dict(
        format="metricchain-cert/1", kind="partition", n=3, k=2, domains=full, instance=wtri,
        claim=dict(lo="1", hi="8"),
        certificate={"node": "leaf", "lo": {"0,1": "1/2", "0,2": "1/2", "1,2": "1/2"}, "hi": {}})
    return docs


EXPECTED = {
    "triangle_min": dict(accepted=True, certified_gap="0"),
    "triangle_min_reject": dict(accepted=False),
    "biased_dee": dict(accepted=True, certified_gap="0"),
    "triangle_residual": dict(accepted=True, lower_bound="1/8", upper_bound="7/8"),
    "residual_inconsistent_reject": dict(accepted=False),
    "residual_lower_semantics": dict(accepted=True, lower_bound="41/4", upper_bound=None),
    "residual_negative_c_reject": dict(accepted=False),
    "partition_negative_reject": dict(accepted=False),
    "triangle_partition_exact": dict(accepted=True, lo="13/4", hi="13/4"),
    "triangle_partition_coarse": dict(accepted=True, lo="1", hi="8"),
}


# ----------------------------------------------------------------------------------------------
# Fuzzing against brute force
# ----------------------------------------------------------------------------------------------

def fuzz(seed, rounds):
    import random
    rnd = random.Random(seed)
    stats = dict(min_accepted=0, min_rejected=0, res_accepted=0, res_lower_accepted=0, res_inconsistent=0,
                 z_accepted=0, z_rejected=0)

    def rq(lo=-3, hi=3, den=4):
        return Q(rnd.randint(lo * den, hi * den), den)

    for _ in range(rounds):
        n, k = rnd.randint(2, 4), rnd.randint(2, 3)
        h = [[rq() for _ in range(k)] for _ in range(n)]
        J = {(i, j): [[rq() for _ in range(k)] for _ in range(k)]
             for i in range(n) for j in range(n) if i != j and rnd.random() < 0.6}
        I = Tables(n, k, h, J, 0)
        D = [sorted(rnd.sample(range(k), rnd.randint(1, k))) for _ in range(n)]
        box = list(itertools.product(*D))
        true_min = min(energy(I, x) for x in box)

        def rand_leaf():
            m = {f"{i},{j}": [str(rq(-2, 2)) for _ in range(k)] for i in range(n) for j in range(n)
                 if i != j and rnd.random() < 0.5}
            return {"node": "leaf", "u": [str(rq(-4, 2)) for _ in range(n)],
                    "p": {f"{i},{j}": str(rq(-3, 1)) for i in range(n) for j in range(n) if i != j and rnd.random() < 0.7},
                    "m": m}

        def exact_leaf(Dloc):
            # dual-feasible leaf with zero messages: u = min h, p = half the min of the symmetrised pair
            # (a random invalid prune may have emptied a domain: any value is then a valid bound)
            u = [str(min((I.one[i][a] for a in Dloc[i]), default=Q(0))) for i in range(n)]
            p = {f"{i},{j}": str(min((I.pair(i, j, a, b) + I.pair(j, i, b, a) for a in Dloc[i] for b in Dloc[j]),
                                     default=Q(0)) / 2)
                 for i in range(n) for j in range(n) if i != j}
            return {"node": "leaf", "u": u, "p": p, "m": {}}

        def rand_cert(Dloc, depth):
            r = rnd.random()
            if depth == 0 or r < 0.25:
                return exact_leaf(Dloc) if rnd.random() < 0.7 else rand_leaf()
            if r < 0.7:
                i = rnd.randrange(n)
                return {"node": "branch", "site": i,
                        "children": {str(a): rand_cert(with_site(Dloc, i, [a]), depth - 1) for a in range(k)}}
            i = rnd.randrange(n)
            r_, t_ = rnd.randrange(k), rnd.randrange(k)
            ell = {str(j): str(min([link(I, i, r_, t_, j, s) for s in Dloc[j]] or [Q(0)]) - (0 if rnd.random() < 0.8 else rq(0, 1)))
                   for j in range(n) if j != i}
            return {"node": "prune", "site": i, "remove": r_, "dominator": t_, "ell": ell,
                    "rest": rand_cert(with_site(Dloc, i, [s for s in Dloc[i] if s != r_]), depth - 1)}

        cert = rand_cert(D, rnd.randint(0, n + 1))
        for L in (true_min - 2, true_min - Q(1, 2), true_min, true_min + Q(1, 4), true_min + 2):
            if verify_min(cert, I, D, L):
                stats["min_accepted"] += 1
                if L > true_min:
                    return False, dict(reason="UNSOUND accept (min)", L=str(L), true_min=str(true_min)), stats
            else:
                stats["min_rejected"] += 1

        # residual: random admissible residual (additive, bounded differences c), one or two anchors
        c = [Q(rnd.randint(0, 4), 4) for _ in range(n)]
        signs = [[rnd.choice([0, 1]) for _ in range(k)] for _ in range(n)]

        def g(x):
            return sum((c[i] * signs[i][x[i]] for i in range(n)), Q(0))

        anchors = [(list(x), g(x)) for x in rnd.sample(box, min(len(box), rnd.randint(1, 2)))]
        true_res = min(energy(I, x) + g(x) for x in box)
        rc = {"node": "anchor", "index": rnd.randrange(len(anchors)), "cert": None}
        Ia = anchored(I, c, anchors[rc["index"]][0])
        saveI = I
        I = Ia  # exact_leaf / rand_cert close over I
        rc["cert"] = rand_cert(D, rnd.randint(0, n))
        I = saveI
        if not residual_consistent(c, anchors):
            return False, dict(reason="exact anchors of an admissible residual judged inconsistent"), stats
        for L in (true_res - 2, true_res - Q(1, 4), true_res, true_res + Q(1, 4)):
            if verify_residual(rc, I, c, anchors, D, L):
                stats["res_accepted"] += 1
                if L > true_res:
                    return False, dict(reason="UNSOUND accept (residual)", L=str(L), true=str(true_res)), stats
        # lower-bound semantics: publish rounded-down anchor values; soundness w.r.t. the same true residual
        low = [(x, v - Q(rnd.randint(0, 3), 8)) for x, v in anchors]
        for L in (true_res - 2, true_res - Q(1, 2), true_res, true_res + Q(1, 4)):
            if verify_residual(rc, I, c, low, D, L):
                stats["res_lower_accepted"] += 1
                if L > true_res:
                    return False, dict(reason="UNSOUND accept (residual, lower semantics)", L=str(L),
                                       true=str(true_res)), stats
        # corrupted anchor data: whenever the data are inconsistent, brute force confirms that no residual
        # with bounded differences c interpolates them (checked through the McShane criterion on the anchors
        # themselves: consistency is necessary for any interpolant).
        if len(anchors) == 2:
            (xa, va), (xb, vb) = anchors
            dab = sum((c[i] for i in range(n) if xa[i] != xb[i]), Q(0))
            corrupt = [(xa, vb + dab + Q(1, 4)), (xb, vb)]
            if residual_consistent(c, corrupt):
                return False, dict(reason="corrupted anchors judged consistent"), stats
            stats["res_inconsistent"] += 1

        # partition
        w = [[Q(rnd.randint(0, 8), 4) for _ in range(k)] for _ in range(n)]
        W = {(i, j): [[Q(rnd.randint(1, 8), 4) for _ in range(k)] for _ in range(k)]
             for i in range(n) for j in range(n) if i != j and rnd.random() < 0.6}
        Iw = Tables(n, k, w, W, 1)
        Zt = sum((weight(Iw, x) for x in box), Q(0))

        def zleaf(Dloc):
            lo = {f"{i},{j}": str(min((Iw.pair(i, j, a, b) for a in Dloc[i] for b in Dloc[j]), default=Q(1))
                                  * (1 if rnd.random() < 0.9 else Q(3, 2)))
                  for i in range(n) for j in range(n) if i != j}
            hi = {f"{i},{j}": str(max((Iw.pair(i, j, a, b) for a in Dloc[i] for b in Dloc[j]), default=Q(1)))
                  for i in range(n) for j in range(n) if i != j}
            return {"node": "leaf", "lo": lo, "hi": hi}

        def zcert(Dloc, depth):
            r = rnd.random()
            if depth == 0 or r < 0.3:
                return zleaf(Dloc)
            i = rnd.randrange(n)
            if r < 0.75:
                return {"node": "branch", "site": i,
                        "children": {str(a): zcert(with_site(Dloc, i, [a]), depth - 1) for a in range(k)}}
            r_, t_ = rnd.randrange(k), rnd.randrange(k)
            qs = {}
            for j in range(n):
                if j == i:
                    continue
                ratios = [(Iw.pair(i, j, r_, s) * Iw.pair(j, i, s, r_)) / (Iw.pair(i, j, t_, s) * Iw.pair(j, i, s, t_))
                          for s in Dloc[j]]
                qs[str(j)] = str(max(ratios or [Q(1)]) * (1 if rnd.random() < 0.85 else Q(1, 2)))
            q0 = Iw.one[i][r_] / Iw.one[i][t_] if Iw.one[i][t_] > 0 else Q(5)
            return {"node": "prune", "site": i, "remove": r_, "dominator": t_, "q0": str(q0), "q": qs,
                    "rest": zcert(with_site(Dloc, i, [s for s in Dloc[i] if s != r_]), depth - 1)}

        res = zverify(zcert(D, rnd.randint(0, n + 1)), Iw, D)
        if res is None:
            stats["z_rejected"] += 1
        else:
            stats["z_accepted"] += 1
            if not (res[0] <= Zt <= res[1]):
                return False, dict(reason="UNSOUND interval (partition)", lo=str(res[0]), hi=str(res[1]), Z=str(Zt)), stats
    return True, {}, stats


def selftest(quick):
    ok = True
    for name, doc in conformance_docs().items():
        doc = json.loads(json.dumps(doc))  # exercise the JSON round trip
        out = check_file(doc)
        good = all(out.get(key) == val for key, val in EXPECTED[name].items())
        ok &= good
        print(f"[{'ok' if good else 'MISMATCH'}] conformance {name}: {out}")
    passed, info, stats = fuzz(seed=11, rounds=150 if quick else 1500)
    ok &= passed
    print(f"[{'ok' if passed else 'FAIL'}] soundness fuzz vs brute force: {stats} {info}")
    if (stats["min_accepted"] == 0 or stats["z_accepted"] == 0 or stats["res_accepted"] == 0
            or stats["res_lower_accepted"] == 0 or stats["res_inconsistent"] == 0):
        ok = False
        print("[FAIL] fuzzer never produced an accepted certificate (test would be vacuous)")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--dump", type=str, default=None, help="write the conformance vectors as JSON files into DIR")
    args = ap.parse_args()
    if args.dump:
        os.makedirs(args.dump, exist_ok=True)
        for name, doc in conformance_docs().items():
            with open(os.path.join(args.dump, name + ".json"), "w") as fh:
                json.dump(doc, fh, indent=1)
        print(f"wrote {len(conformance_docs())} conformance vectors to {args.dump}")
        return 0
    if args.selftest:
        return 0 if selftest(args.quick) else 1
    if args.cert:
        with open(args.cert) as fh:
            print(json.dumps(check_file(json.load(fh)), indent=1))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
