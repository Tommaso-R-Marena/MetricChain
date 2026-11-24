#!/usr/bin/env python3
"""
Reference implementation of the MetricChain certificate checkers (format `metricchain-cert/1`,
docs/BLUEPRINT.md §4-§5) in exact rational arithmetic.

This file is NOT part of the trusted base: the trusted checkers are the Lean definitions
`verify`, `verifyITop` (with its special cases `verifyRTop` / `verifyRLowerTop`), `zverifyTop` and
their soundness theorems.  It exists so that an implementation team has (a) an executable reading
of the JSON schema, (b) the conformance vectors that the Lean kernel evaluates
(`triangle_verified`, `triangle_rejects`, `biased_verified`, `triangleResidual_verifiedTop`,
`inconsistentResidual_rejected`, `inconsistentResidual_lowerTop`, `negativeEnvelope_rejected`,
`triangleInterval_verified`, `inconsistentInterval_rejected`, `triangleZ_exactTop`,
`triangleZ_coarse`, `negativeW_rejected`), and (c) a fuzzer that checks soundness against brute
force on random instances and random (mostly invalid) certificates.

File-level checks (all part of the top-level Lean kernels, or of the well-formedness that Lean
enforces by typing):
  * well-formedness: every site index lies in [0, n), every state in [0, k), tables have the
    declared shapes, domains are duplicate-free (`validate`); malformed files are rejected;
  * residual: anchors carry interval data `lo <= residual(x) <= hi` (`hi` optional; `value` is
    shorthand for `lo = hi`, to be used only for exactly rational residuals).  The data must be
    consistent: `c >= 0` and `lo_p - hi_q <= sum_i c_i [x_p,i != x_q,i]` for all ordered pairs of
    anchors of which the second has an upper value (Lean `IProblem.Consistent`, which is exactly
    non-emptiness of the residual class, `IProblem.consistent_iff_nonempty`).  An upper bound on
    the optimum is reported only from anchors that have an upper value;
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
# Well-formedness (in Lean these conditions are enforced by the types `Fin n`, `Fin k`)
# ----------------------------------------------------------------------------------------------

class Malformed(ValueError):
    pass


def _need(cond, msg):
    if not cond:
        raise Malformed(msg)


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _rat(v, what):
    try:
        return q(v)
    except Exception as exc:  # noqa: BLE001
        raise Malformed(f"{what}: not a rational ({v!r})") from exc


def _site(v, n, what):
    _need(_is_int(v) and 0 <= v < n, f"{what}: site index {v!r} outside [0, {n})")


def _state(v, k, what):
    _need(_is_int(v) and 0 <= v < k, f"{what}: state {v!r} outside [0, {k})")


def _pair_key(key, n, what):
    try:
        i, j = (int(t) for t in key.split(",")) if isinstance(key, str) else key
    except Exception as exc:  # noqa: BLE001
        raise Malformed(f"{what}: bad pair key {key!r}") from exc
    _need(_is_int(i) and _is_int(j) and 0 <= i < n and 0 <= j < n and i != j,
          f"{what}: pair key {key!r} is not an ordered pair of distinct sites")
    return i, j


def _site_key(key, n, what):
    try:
        j = int(key)
    except Exception as exc:  # noqa: BLE001
        raise Malformed(f"{what}: bad site key {key!r}") from exc
    _site(j, n, what)


def _tables(one, two, n, k, what):
    _need(isinstance(one, list) and len(one) == n, f"{what}: one-body table must have {n} rows")
    for row in one:
        _need(isinstance(row, list) and len(row) == k, f"{what}: one-body rows must have {k} entries")
        for v in row:
            _rat(v, what)
    _need(isinstance(two or {}, dict), f"{what}: two-body tables must be an object")
    for key, tab in (two or {}).items():
        _pair_key(key, n, what)
        _need(isinstance(tab, list) and len(tab) == k
              and all(isinstance(r, list) and len(r) == k for r in tab),
              f"{what}: two-body table {key!r} must be {k} x {k}")
        for r in tab:
            for v in r:
                _rat(v, what)


def _pair_scalars(d, n, what):
    _need(isinstance(d or {}, dict), f"{what}: must be an object")
    for key, v in (d or {}).items():
        _pair_key(key, n, what)
        _rat(v, what)


def _branch(node, n, k, rec, what):
    _site(node.get("site"), n, what)
    ch = node.get("children")
    _need(isinstance(ch, dict), f"{what}: children must be an object")
    for key, sub in ch.items():
        try:
            a = int(key)
        except Exception as exc:  # noqa: BLE001
            raise Malformed(f"{what}: bad child key {key!r}") from exc
        _state(a, k, what)
        rec(sub)


def _validate_min(node, n, k):
    _need(isinstance(node, dict), "certificate node must be an object")
    kind = node.get("node")
    if kind == "leaf":
        u = node.get("u")
        _need(isinstance(u, list) and len(u) == n, f"leaf: u must have {n} entries")
        for v in u:
            _rat(v, "leaf u")
        _pair_scalars(node.get("p"), n, "leaf p")
        _need(isinstance(node.get("m") or {}, dict), "leaf m must be an object")
        for key, row in (node.get("m") or {}).items():
            _pair_key(key, n, "leaf m")
            _need(isinstance(row, list) and len(row) == k, f"leaf m: rows must have {k} entries")
            for v in row:
                _rat(v, "leaf m")
    elif kind == "branch":
        _branch(node, n, k, lambda sub: _validate_min(sub, n, k), "branch")
    elif kind == "prune":
        _site(node.get("site"), n, "prune")
        _state(node.get("remove"), k, "prune remove")
        _state(node.get("dominator"), k, "prune dominator")
        _need(isinstance(node.get("ell") or {}, dict), "prune ell must be an object")
        for key, v in (node.get("ell") or {}).items():
            _site_key(key, n, "prune ell")
            _rat(v, "prune ell")
        _validate_min(node.get("rest"), n, k)
    elif kind == "sum":
        parts = node.get("parts")
        _need(isinstance(parts, list) and len(parts) == 2, "sum: exactly two parts")
        for pt in parts:
            _need(isinstance(pt, dict) and isinstance(pt.get("instance"), dict), "sum: part needs an instance")
            _tables(pt["instance"].get("h"), pt["instance"].get("J", {}), n, k, "sum part")
            _rat(pt.get("bound"), "sum bound")
            _validate_min(pt.get("certificate"), n, k)
    else:
        raise Malformed(f"unknown node {kind!r}")


def _validate_residual(node, n, k):
    _need(isinstance(node, dict), "certificate node must be an object")
    kind = node.get("node")
    if kind == "anchor":
        _need(_is_int(node.get("index")) and node["index"] >= 0, "anchor: index must be a natural number")
        _validate_min(node.get("cert"), n, k)
    elif kind == "branch":
        _branch(node, n, k, lambda sub: _validate_residual(sub, n, k), "branch")
    elif kind == "prune":
        _site(node.get("site"), n, "prune")
        _state(node.get("remove"), k, "prune remove")
        _state(node.get("dominator"), k, "prune dominator")
        for key, v in (node.get("ell") or {}).items():
            _site_key(key, n, "prune ell")
            _rat(v, "prune ell")
        _validate_residual(node.get("rest"), n, k)
    else:
        raise Malformed(f"unknown node {kind!r}")


def _validate_partition(node, n, k):
    _need(isinstance(node, dict), "certificate node must be an object")
    kind = node.get("node")
    if kind == "leaf":
        _pair_scalars(node.get("lo"), n, "leaf lo")
        _pair_scalars(node.get("hi"), n, "leaf hi")
    elif kind == "branch":
        _branch(node, n, k, lambda sub: _validate_partition(sub, n, k), "branch")
    elif kind == "prune":
        _site(node.get("site"), n, "prune")
        _state(node.get("remove"), k, "prune remove")
        _state(node.get("dominator"), k, "prune dominator")
        _rat(node.get("q0"), "prune q0")
        for key, v in (node.get("q") or {}).items():
            _site_key(key, n, "prune q")
            _rat(v, "prune q")
        _validate_partition(node.get("rest"), n, k)
    else:
        raise Malformed(f"unknown node {kind!r}")


def validate(doc):
    """Raise `Malformed` unless every index of the file is in range and every table has its shape."""
    _need(isinstance(doc, dict) and doc.get("format") == "metricchain-cert/1", "unknown format")
    n, k, kind = doc.get("n"), doc.get("k"), doc.get("kind")
    _need(_is_int(n) and n >= 0 and _is_int(k) and k >= 0, "n and k must be natural numbers")
    D = doc.get("domains")
    _need(isinstance(D, list) and len(D) == n, f"domains must list {n} sites")
    for d in D:
        _need(isinstance(d, list), "each domain must be a list")
        for a in d:
            _state(a, k, "domain")
        _need(len(set(d)) == len(d), "domains must not repeat a state")
    inst = doc.get("instance")
    _need(isinstance(inst, dict), "instance must be an object")
    _need(isinstance(doc.get("claim", {}), dict), "claim must be an object")
    if kind == "min":
        _tables(inst.get("h"), inst.get("J", {}), n, k, "instance")
        _rat(doc.get("claim", {}).get("lower_bound"), "claim.lower_bound")
        w = doc.get("claim", {}).get("witness")
        if w is not None:
            _need(isinstance(w, list) and len(w) == n, "witness must assign a state to every site")
            for a in w:
                _state(a, k, "witness")
        _validate_min(doc.get("certificate"), n, k)
    elif kind == "residual":
        _tables(inst.get("h"), inst.get("J", {}), n, k, "instance")
        c = inst.get("c")
        _need(isinstance(c, list) and len(c) == n, f"c must have {n} entries")
        for v in c:
            _rat(v, "c")
        _need(isinstance(inst.get("anchors"), list), "anchors must be a list")
        for a in inst["anchors"]:
            _need(isinstance(a, dict), "anchor must be an object")
            x = a.get("x")
            _need(isinstance(x, list) and len(x) == n, "anchor: x must assign a state to every site")
            for v in x:
                _state(v, k, "anchor")
            if "value" in a:
                _need("lo" not in a and "hi" not in a, "anchor: give either value or lo/hi, not both")
                _rat(a["value"], "anchor value")
            else:
                _need("lo" in a, "anchor: needs value, or lo (and optionally hi)")
                _rat(a["lo"], "anchor lo")
                if "hi" in a:
                    _rat(a["hi"], "anchor hi")
        _rat(doc.get("claim", {}).get("lower_bound"), "claim.lower_bound")
        _validate_residual(doc.get("certificate"), n, k)
    elif kind == "partition":
        _tables(inst.get("w"), inst.get("W", {}), n, k, "instance")
        for key in ("lo", "hi"):
            if key in doc.get("claim", {}):
                _rat(doc["claim"][key], f"claim.{key}")
        _validate_partition(doc.get("certificate"), n, k)
    else:
        raise Malformed(f"unknown kind {kind!r}")


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


def interval_consistent(c, anchors) -> bool:
    """Lean `IProblem.Consistent`.  `anchors` is a list of (x, lo, hi) with hi possibly None:
    c >= 0 and lo_p - hi_q <= sum_i c_i [x_p,i != x_q,i] for all ordered pairs with hi_q given."""
    if any(ci < 0 for ci in c):
        return False
    for xa, lo_a, _ in anchors:
        for xb, _, hi_b in anchors:
            if hi_b is not None and lo_a - hi_b > sum((c[i] for i in range(len(c)) if xa[i] != xb[i]), Q(0)):
                return False
    return True


def residual_consistent(c, anchors) -> bool:
    """Lean `RProblem.Consistent` (exact values): the interval criterion with lo = hi."""
    return interval_consistent(c, [(x, v, v) for x, v in anchors])


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
    try:
        validate(doc)
    except Malformed as exc:
        return dict(accepted=False, reason=f"malformed input: {exc}")
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
        anchors = []
        for a in inst["anchors"]:
            if "value" in a:
                lo = hi = q(a["value"])
            else:
                lo, hi = q(a["lo"]), (q(a["hi"]) if "hi" in a else None)
            anchors.append((a["x"], lo, hi))
        L = q(doc["claim"]["lower_bound"])
        if any(ci < 0 for ci in c):
            return dict(accepted=False, reason="negative envelope constant")
        if not interval_consistent(c, anchors):
            return dict(accepted=False, reason="inconsistent residual data (empty residual class)")
        ok = verify_residual(doc["certificate"], I, c, [(x, lo) for x, lo, _ in anchors], D, L)
        out = dict(accepted=ok, lower_bound=str(L))
        if ok:
            inbox = [energy(I, x) + hi for x, _, hi in anchors
                     if hi is not None and all(x[i] in D[i] for i in range(n))]
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
    # the same values published as lower bounds only (Lean: inconsistentResidual_lowerTop)
    docs["residual_lower_only"] = dict(
        format="metricchain-cert/1", kind="residual", n=3, k=2, domains=full,
        instance=dict(tri, c=["1/4"] * 3, anchors=[dict(x=anc, lo="0"), dict(x=anc2, lo="10")]),
        claim=dict(lower_bound="41/4"), certificate=bad_cert)
    # interval data (Lean: triangleInterval_verified): g(0,1,0) in [-9/64, -7/64]
    docs["residual_interval"] = dict(
        format="metricchain-cert/1", kind="residual", n=3, k=2, domains=full,
        instance=dict(tri, c=["1/4"] * 3, anchors=[dict(x=anc, lo="-9/64", hi="-7/64")]),
        claim=dict(lower_bound="7/64"),
        certificate={"node": "anchor", "index": 0, "cert": exhaustive(anchored(Itri, [Q(1, 4)] * 3, anc))})
    # rounded but incompatible evaluations (Lean: inconsistentInterval_rejected)
    docs["residual_interval_inconsistent_reject"] = dict(
        format="metricchain-cert/1", kind="residual", n=3, k=2, domains=full,
        instance=dict(tri, c=["1/4"] * 3, anchors=[dict(x=anc, lo="-1/64", hi="1/64"),
                                                   dict(x=anc2, lo="639/64", hi="641/64")]),
        claim=dict(lower_bound="0"), certificate=bad_cert)
    # malformed: an anchor configuration outside the state range (unrepresentable in Lean)
    docs["residual_bad_anchor_reject"] = dict(
        format="metricchain-cert/1", kind="residual", n=3, k=2, domains=full,
        instance=dict(tri, c=["1/4"] * 3, anchors=[dict(x=[7, 7, 7], value="100")]),
        claim=dict(lower_bound="401/4"),
        certificate={"node": "anchor", "index": 0, "cert": exhaustive(anchored(Itri, [Q(1, 4)] * 3, anc))})
    docs["residual_negative_c_reject"] = dict(
        format="metricchain-cert/1", kind="residual", n=3, k=2, domains=full,
        instance=dict(tri, c=["-10", "1/4", "1/4"], anchors=[dict(x=anc, lo="0")]),
        claim=dict(lower_bound="-100"),
        certificate={"node": "anchor", "index": 0,
                     "cert": exhaustive(anchored(Itri, [Q(-10), Q(1, 4), Q(1, 4)], anc))})
    # negative factor (Lean: negativeW): two sites, one state each
    docs["partition_negative_reject"] = dict(
        format="metricchain-cert/1", kind="partition", n=2, k=1, domains=[[0]] * 2,
        instance={"w": [["-1"], ["1"]], "W": {"0,1": [["2"]], "1,0": [["2"]]}}, claim={},
        certificate={"node": "leaf", "lo": {"0,1": "1", "1,0": "1"}, "hi": {"0,1": "3", "1,0": "3"}})
    # malformed: a negative state in a domain (Python would silently index from the end)
    docs["partition_bad_domain_reject"] = dict(
        format="metricchain-cert/1", kind="partition", n=1, k=1, domains=[[0, -1]],
        instance={"w": [["1"]], "W": {}}, claim={}, certificate={"node": "leaf", "lo": {}, "hi": {}})
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
    "residual_lower_only": dict(accepted=True, lower_bound="41/4", upper_bound=None),
    "residual_interval": dict(accepted=True, lower_bound="7/64", upper_bound="57/64"),
    "residual_interval_inconsistent_reject": dict(accepted=False),
    "residual_bad_anchor_reject": dict(accepted=False),
    "residual_negative_c_reject": dict(accepted=False),
    "partition_negative_reject": dict(accepted=False),
    "partition_bad_domain_reject": dict(accepted=False),
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
                 res_interval_consistent=0, z_accepted=0, z_rejected=0)

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
        # interval data around the true values: a legitimate producer is never judged inconsistent
        iv = [(x, v - Q(rnd.randint(0, 3), 8), v + Q(rnd.randint(0, 3), 8)) for x, v in anchors]
        if not interval_consistent(c, iv):
            return False, dict(reason="interval anchors of an admissible residual judged inconsistent"), stats
        stats["res_interval_consistent"] += 1
        # corrupted anchor data must be judged inconsistent (exact and interval form)
        if len(anchors) == 2:
            (xa, va), (xb, vb) = anchors
            dab = sum((c[i] for i in range(n) if xa[i] != xb[i]), Q(0))
            corrupt = [(xa, vb + dab + Q(1, 4)), (xb, vb)]
            if residual_consistent(c, corrupt):
                return False, dict(reason="corrupted anchors judged consistent"), stats
            eps = Q(1, 16)
            corrupt_iv = [(xa, vb + dab + Q(1, 4) - eps, vb + dab + Q(1, 4) + eps), (xb, vb - eps, vb + eps)]
            if interval_consistent(c, corrupt_iv):
                return False, dict(reason="corrupted interval anchors judged consistent"), stats
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
