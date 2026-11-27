"""An independent checker of the structural-biology division's "min" certificates (format ``structbio-mincert/1``),
written by the Computational Research Division from the *format description* in the docstring of
``src/metricchain_sb/mincert.py`` at that division's commit 720e0ec -- not from its checker ``mincheck.py``.

Differences of construction, on purpose:

* plain Python integers and lists only (no numpy, hence no fixed-width arithmetic anywhere);
* a strict loader for the JSON form: duplicate keys, non-integers where integers are required (floats, strings,
  booleans), non-canonical keys ("0, 1", "01"), unknown fields and a wrong ``model_sha256`` are *rejected*; the
  division's ``loads`` converts or ignores them (report: ``REPORT.md`` of this directory);
* besides the verdict it returns the largest lower bound the certificate proves (the least leaf bound when the
  tree is structurally valid), so that a claimed bound can be compared with it exactly.

Semantics implemented (box D = prod_i D_i; tables h_i, J_ij in units 2^-scale_bits; messages and the claimed bound
L in units 2^-(scale_bits + message_bits); mb = 2^message_bits):

  leaf     B = sum_i min_{a in D_i} [ mb h_i(a) + sum_{j ~ i} m_(i,j)(a) ]
             + sum_{i<j listed} min_{a in D_i, b in D_j} [ mb J_ij(a, b) - m_(i,j)(a) - m_(j,i)(b) ];   valid iff L <= B
  branch   on site i: every state of the current D_i has a child, checked on the box with D_i = {a}
  prune    (i, r, t): t in D_i, t != r, and
             mb (h_i(r) - h_i(t)) + sum_{j ~ i} min_{s in D_j} mb (J_ij(r, s) - J_ij(t, s)) >= 0;
           the rest is checked on the box without r

Accepted  ==>  L <= mb * E(x) for every x of the box.  (Soundness of exactly these rules is the theory division's
machine-checked ``verify_sound``; this file is one more implementation of them, tested against enumeration.)
"""
from __future__ import annotations

import hashlib
import json

__all__ = ["Malformed", "check_plain", "strict_loads", "brute_force_min_box", "plain_from_object"]


class Malformed(ValueError):
    pass


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _need(cond: bool, msg: str) -> None:
    if not cond:
        raise Malformed(msg)


def validate_plain(c: dict) -> None:
    """``c``: dict(scale_bits, unary, pair, message_bits, domains, lower_bound, root) of plain Python objects;
    ``pair`` and message keys are tuples (i, j) of ints."""
    _need(_is_int(c["scale_bits"]) and c["scale_bits"] >= 0, "scale_bits")
    _need(_is_int(c["message_bits"]) and 0 <= c["message_bits"] <= 4096, "message_bits")
    _need(_is_int(c["lower_bound"]), "lower_bound")
    unary = c["unary"]
    _need(isinstance(unary, list) and len(unary) >= 1, "unary")
    for u in unary:
        _need(isinstance(u, list) and len(u) >= 1 and all(_is_int(v) for v in u), "unary table")
    n = len(unary)
    sizes = [len(u) for u in unary]
    for key, t in c["pair"].items():
        _need(isinstance(key, tuple) and len(key) == 2 and all(_is_int(v) for v in key), "pair key")
        i, j = key
        _need(0 <= i < j < n, "pair key order or range")
        _need(isinstance(t, list) and len(t) == sizes[i] and all(isinstance(r, list) and len(r) == sizes[j] and all(_is_int(v) for v in r) for r in t),
              "pair table shape")
    D = c["domains"]
    _need(isinstance(D, list) and len(D) == n, "domains")
    for i, d in enumerate(D):
        _need(isinstance(d, list) and len(d) >= 1 and all(_is_int(a) and 0 <= a < sizes[i] for a in d) and len(set(d)) == len(d), "domain")


def check_plain(c: dict) -> dict:
    """Verdict and the largest provable bound.  Returns dict(accepted, reason, proves) where ``proves`` is the least
    leaf bound (None if the tree is structurally invalid: a missing child, a prune that fails)."""
    try:
        validate_plain(c)
    except (Malformed, KeyError, TypeError) as exc:
        return dict(accepted=False, reason=f"malformed: {exc}", proves=None)
    unary, pair = c["unary"], c["pair"]
    n = len(unary)
    sizes = [len(u) for u in unary]
    mb = 2 ** c["message_bits"]
    nbrs = [[] for _ in range(n)]
    for (i, j) in pair:
        nbrs[i].append(j)
        nbrs[j].append(i)

    def J(i, j, a, b):
        return pair[(i, j)][a][b] if i < j else pair[(j, i)][b][a]

    least = None
    stack = [(c["root"], [list(d) for d in c["domains"]])]
    try:
        while stack:
            node, D = stack.pop()
            _need(isinstance(node, dict), "node")
            kind = node.get("node")
            if kind == "leaf":
                _need(set(node) <= {"node", "m"}, "leaf field")
                m = node.get("m", {})
                _need(isinstance(m, dict), "leaf m")
                for key, vec in m.items():
                    _need(isinstance(key, tuple) and len(key) == 2 and all(_is_int(v) for v in key), "message key")
                    i, j = key
                    _need(0 <= i < n and 0 <= j < n and i != j and (min(i, j), max(i, j)) in pair, "message key not a listed pair")
                    _need(isinstance(vec, list) and len(vec) == sizes[i] and all(_is_int(v) for v in vec), "message vector")
                B = 0
                for i in range(n):
                    B += min(mb * unary[i][a] + sum(m[(i, j)][a] for j in nbrs[i] if (i, j) in m) for a in D[i])
                for (i, j) in pair:
                    mi, mj = m.get((i, j)), m.get((j, i))
                    B += min(mb * pair[(i, j)][a][b] - (mi[a] if mi is not None else 0) - (mj[b] if mj is not None else 0)
                             for a in D[i] for b in D[j])
                least = B if least is None else min(least, B)
            elif kind == "branch":
                _need(set(node) <= {"node", "site", "children"}, "branch field")
                i = node.get("site")
                _need(_is_int(i) and 0 <= i < n, "branch site")
                ch = node.get("children")
                _need(isinstance(ch, dict), "children")
                for a in ch:
                    _need(_is_int(a) and 0 <= a < sizes[i], "child state")
                for a in D[i]:
                    if a not in ch:
                        return dict(accepted=False, reason=f"branch on site {i}: no child for state {a}", proves=None)
                    D2 = list(D)
                    D2[i] = [a]
                    stack.append((ch[a], D2))
            elif kind == "prune":
                _need(set(node) <= {"node", "site", "remove", "dominator", "rest"}, "prune field")
                i, r, t = node.get("site"), node.get("remove"), node.get("dominator")
                _need(_is_int(i) and 0 <= i < n, "prune site")
                _need(_is_int(r) and 0 <= r < sizes[i] and _is_int(t) and 0 <= t < sizes[i], "prune state")
                if t == r or t not in D[i]:
                    return dict(accepted=False, reason="prune: the dominator is not another state of the current domain", proves=None)
                margin = mb * (unary[i][r] - unary[i][t]) + sum(min(mb * (J(i, j, r, s) - J(i, j, t, s)) for s in D[j]) for j in nbrs[i])
                if margin < 0:
                    return dict(accepted=False, reason="prune: dominance fails", proves=None)
                D2 = list(D)
                D2[i] = [s for s in D[i] if s != r]
                stack.append((node.get("rest"), D2))
            else:
                raise Malformed(f"node kind {kind!r}")
    except (Malformed, KeyError, TypeError) as exc:
        return dict(accepted=False, reason=f"malformed: {exc}", proves=None)
    ok = c["lower_bound"] <= least
    return dict(accepted=ok, reason="accepted" if ok else "a leaf bound is below the claim", proves=least)


def brute_force_min_box(c: dict) -> int:
    """min over the root box of mb * E(x), by enumeration (exact)."""
    import itertools
    unary, pair = c["unary"], c["pair"]
    mb = 2 ** c["message_bits"]
    best = None
    for x in itertools.product(*c["domains"]):
        e = sum(unary[i][a] for i, a in enumerate(x)) + sum(t[x[i]][x[j]] for (i, j), t in pair.items())
        best = e if best is None or e < best else best
    return mb * best


def plain_from_object(cert) -> dict:
    """The plain form of an in-memory certificate of the reviewed package (data extraction only; no validation:
    whatever the object holds is copied, so that malformed objects stay malformed)."""
    model = cert.model

    def ints(seq):
        return [v if isinstance(v, bool) else (int(v) if hasattr(v, "__index__") else v) for v in seq]

    def conv(node):
        if not isinstance(node, dict):
            return node
        out = dict(node)
        if "m" in out and isinstance(out["m"], dict):
            out["m"] = {tuple(ints(k)) if isinstance(k, tuple) else k: (ints(v) if isinstance(v, list) else v) for k, v in out["m"].items()}
        if "children" in out and isinstance(out["children"], dict):
            out["children"] = {(int(a) if hasattr(a, "__index__") and not isinstance(a, bool) else a): conv(ch) for a, ch in out["children"].items()}
        if "rest" in out:
            out["rest"] = conv(out["rest"])
        for k in ("site", "remove", "dominator"):
            if k in out and hasattr(out[k], "__index__") and not isinstance(out[k], bool):
                out[k] = int(out[k])
        return out

    return dict(scale_bits=model.scale_bits, unary=[[int(v) for v in u.tolist()] for u in model.unary],
                pair={(int(i), int(j)): [[int(v) for v in row] for row in t.tolist()] for (i, j), t in model.pair.items()},
                message_bits=cert.message_bits, domains=[ints(d) if isinstance(d, list) else d for d in cert.domains] if isinstance(cert.domains, list) else cert.domains,
                lower_bound=int(cert.lower_bound) if hasattr(cert.lower_bound, "__index__") and not isinstance(cert.lower_bound, bool) else cert.lower_bound,
                root=conv(cert.root))


# ---------------------------------------------------------------------------------------------
# Strict loader of the JSON form
# ---------------------------------------------------------------------------------------------

def _no_duplicates(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise Malformed(f"duplicate key {k!r}")
        seen[k] = v
    return seen


def _reject_constant(name):
    raise Malformed(f"non-finite number {name}")


def _key_pair(text: str) -> tuple:
    parts = text.split(",")
    _need(len(parts) == 2, f"pair key {text!r}")
    out = []
    for s in parts:
        _need(s.isdigit() and (s == "0" or not s.startswith("0")), f"non-canonical key {text!r}")
        out.append(int(s))
    return tuple(out)


def _key_state(text: str) -> int:
    _need(text.isdigit() and (text == "0" or not text.startswith("0")), f"non-canonical state key {text!r}")
    return int(text)


def strict_loads(text: str) -> dict:
    """The plain form of a ``structbio-mincert/1`` document, or ``Malformed``.  Checks the checksum of the model."""
    try:
        doc = json.loads(text, object_pairs_hook=_no_duplicates, parse_constant=_reject_constant)
    except Malformed:
        raise
    except Exception as exc:
        raise Malformed(f"not JSON: {exc}") from None
    _need(isinstance(doc, dict), "document")
    _need(set(doc) == {"format", "model", "model_sha256", "message_bits", "domains", "claim", "certificate", "meta"}, "top-level fields")
    _need(doc["format"] == "structbio-mincert/1", "format")
    model = doc["model"]
    _need(isinstance(model, dict) and set(model) == {"scale_bits", "unary", "pair", "meta"}, "model fields")
    _need(isinstance(model["pair"], dict), "pair")
    pair = {}
    for k, t in model["pair"].items():
        pair[_key_pair(k)] = t
    canon = {"scale_bits": model["scale_bits"], "unary": model["unary"], "pair": model["pair"]}
    digest = hashlib.sha256(json.dumps(canon, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    _need(doc["model_sha256"] == digest, "model_sha256 does not match the model in the document")
    claim = doc["claim"]
    _need(isinstance(claim, dict) and set(claim) <= {"lower_bound", "witness"} and "lower_bound" in claim, "claim fields")

    def node(d):
        _need(isinstance(d, dict), "node")
        kind = d.get("node")
        if kind == "leaf":
            _need(set(d) <= {"node", "m"}, "leaf field")
            m = d.get("m", {})
            _need(isinstance(m, dict), "leaf m")
            return {"node": "leaf", "m": {_key_pair(k): v for k, v in m.items()}}
        if kind == "branch":
            _need(set(d) == {"node", "site", "children"} and isinstance(d["children"], dict), "branch fields")
            return {"node": "branch", "site": d["site"], "children": {_key_state(a): node(ch) for a, ch in d["children"].items()}}
        if kind == "prune":
            _need(set(d) == {"node", "site", "remove", "dominator", "rest"}, "prune fields")
            return {"node": "prune", "site": d["site"], "remove": d["remove"], "dominator": d["dominator"], "rest": node(d["rest"])}
        raise Malformed(f"node kind {kind!r}")

    return dict(scale_bits=model["scale_bits"], unary=model["unary"], pair=pair, message_bits=doc["message_bits"],
                domains=doc["domains"], lower_bound=claim["lower_bound"], root=node(doc["certificate"]))
