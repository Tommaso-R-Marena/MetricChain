"""Certificates of lower bounds on minimum energies ("min" certificates).

Mathematical content (the theory division's kernel `verify`, `proofs/CertificateAlgebra.lean`;
soundness `verify_sound` **[V]**, applied to the `PairInstance` whose table `J i j` is our pair
table for `i < j` and zero for `i > j`): a certificate is a tree over a box `D = prod_i D_i` of
configurations with nodes

* ``leaf``    — a reparameterisation (dual) bound: messages `m[(i, j)][a]` for every listed pair
  `{i, j}` and state `a` of `i`; the bound of the leaf on the box is

      B = sum_i  min_{a in D_i} ( h_i(a) + sum_{j ~ i} m[(i, j)][a] )
        + sum_{i<j listed}  min_{a in D_i, b in D_j} ( J_ij(a, b) - m[(i, j)][a] - m[(j, i)][b] ),

  and the leaf is accepted iff `L <= B`;
* ``branch``  — a case split on the state of one site (every state of its current domain needs a child);
* ``prune``   — Goldstein dead-end elimination of state `r` of site `i` by a dominator `t != r` of
  the current domain: accepted iff `t in D_i`, `t != r` and
  `h_i(r) - h_i(t) + sum_{j ~ i} min_{s in D_j} (J_ij(r, s) - J_ij(t, s)) >= 0`;
  the rest of the certificate is checked on the box without `r`.

Accepted  ==>  `L <= E(x)` for every `x` in the box.

This module holds the in-memory representation, a compact JSON serialisation
(`structbio-mincert/1`), and the exact conversion to the theory division's interchange format
`metricchain-cert/1` (`docs/BLUEPRINT.md` §4.1).  In the compact form a leaf stores only its
messages and a prune stores only `(site, remove, dominator)`: the quantities `u`, `p`, `ell` of the
theory division's format are the *largest* values that satisfy its inequalities and are recomputed
by whoever needs them, so that both formats are accepted for exactly the same claims.

Units: `lower_bound` and all messages are integers in units of
``2**-(model.scale_bits + message_bits)``.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

from .model import PairModel

__all__ = ["MinCertificate", "MalformedCertificate", "validate_structure", "to_metricchain_cert1",
           "dumps", "loads", "count_nodes"]


class MalformedCertificate(ValueError):
    """The certificate is not a well-formed object of the format (indices out of range, wrong shapes)."""


@dataclass
class MinCertificate:
    model: PairModel
    message_bits: int
    domains: list
    lower_bound: int
    witness: tuple | None
    root: dict
    meta: dict = field(default_factory=dict)

    @property
    def unit_bits(self) -> int:
        return self.model.scale_bits + self.message_bits

    def lower_bound_fraction(self) -> Fraction:
        return Fraction(self.lower_bound, 2 ** self.unit_bits)


def _is_int(v) -> bool:
    return isinstance(v, (int, np.integer)) and not isinstance(v, bool)


def validate_structure(cert: MinCertificate) -> None:
    """Raise :class:`MalformedCertificate` unless every index is in range and every vector has its length."""
    model = cert.model
    n, sizes = model.n, model.sizes
    if not _is_int(cert.message_bits) or cert.message_bits < 0:
        raise MalformedCertificate("message_bits must be a natural number")
    if not _is_int(cert.lower_bound):
        raise MalformedCertificate("lower_bound must be an integer (units of 2**-(scale_bits+message_bits))")
    if not isinstance(cert.domains, list) or len(cert.domains) != n:
        raise MalformedCertificate(f"domains must list {n} sites")
    for i, d in enumerate(cert.domains):
        if not isinstance(d, list) or not d:
            raise MalformedCertificate(f"domain of site {i} must be a non-empty list (an empty box certifies nothing)")
        if any((not _is_int(a)) or not 0 <= a < sizes[i] for a in d) or len(set(d)) != len(d):
            raise MalformedCertificate(f"domain of site {i} has a repeated or out-of-range state")
    if cert.witness is not None:
        w = cert.witness
        if len(w) != n or any((not _is_int(a)) or not 0 <= a < sizes[i] for i, a in enumerate(w)):
            raise MalformedCertificate("witness must assign an existing state to every site")

    stack = [cert.root]
    while stack:
        node = stack.pop()
        if not isinstance(node, dict):
            raise MalformedCertificate("certificate node must be an object")
        kind = node.get("node")
        if kind == "leaf":
            if set(node) - {"node", "m"}:
                raise MalformedCertificate("leaf: unknown field")
            m = node.get("m", {})
            if not isinstance(m, dict):
                raise MalformedCertificate("leaf: m must be a mapping")
            for key, vec in m.items():
                if (not isinstance(key, tuple)) or len(key) != 2 or not all(_is_int(t) for t in key):
                    raise MalformedCertificate(f"leaf: message key {key!r} is not an ordered pair of sites")
                i, j = key
                if not (0 <= i < n and 0 <= j < n and i != j) or (min(i, j), max(i, j)) not in model.pair:
                    raise MalformedCertificate(f"leaf: message key {key!r} is not a listed pair of the model")
                if (not isinstance(vec, list)) or len(vec) != sizes[i] or not all(_is_int(v) for v in vec):
                    raise MalformedCertificate(f"leaf: message {key!r} must list one integer per state of site {i}")
        elif kind == "branch":
            if set(node) - {"node", "site", "children"}:
                raise MalformedCertificate("branch: unknown field")
            i = node.get("site")
            if (not _is_int(i)) or not 0 <= i < n:
                raise MalformedCertificate("branch: site out of range")
            ch = node.get("children")
            if not isinstance(ch, dict):
                raise MalformedCertificate("branch: children must be a mapping")
            for a, sub in ch.items():
                if (not _is_int(a)) or not 0 <= a < sizes[i]:
                    raise MalformedCertificate("branch: child state out of range")
                stack.append(sub)
        elif kind == "prune":
            if set(node) - {"node", "site", "remove", "dominator", "rest"}:
                raise MalformedCertificate("prune: unknown field")
            i = node.get("site")
            if (not _is_int(i)) or not 0 <= i < n:
                raise MalformedCertificate("prune: site out of range")
            for name in ("remove", "dominator"):
                a = node.get(name)
                if (not _is_int(a)) or not 0 <= a < sizes[i]:
                    raise MalformedCertificate(f"prune: {name} out of range")
            stack.append(node.get("rest"))
        else:
            raise MalformedCertificate(f"unknown node kind {kind!r}")


def count_nodes(root: dict) -> dict:
    """Number of nodes of each kind and of stored message integers (certificate size statistics)."""
    out = {"leaf": 0, "branch": 0, "prune": 0, "message_integers": 0, "depth": 0}
    stack = [(root, 1)]
    while stack:
        node, depth = stack.pop()
        out["depth"] = max(out["depth"], depth)
        kind = node["node"]
        out[kind] += 1
        if kind == "leaf":
            out["message_integers"] += sum(len(v) for v in node.get("m", {}).values())
        elif kind == "branch":
            stack.extend((c, depth + 1) for c in node["children"].values())
        else:
            stack.append((node["rest"], depth + 1))
    return out


# ---------------------------------------------------------------------------------------------
# Exact conversion to the theory division's format `metricchain-cert/1`
# ---------------------------------------------------------------------------------------------

def _rat(value: Fraction):
    """Canonical JSON rational of `metricchain-cert/1`: an integer, or a string 'p/q' in lowest terms."""
    value = Fraction(value)
    return int(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _min0(values) -> int:
    """Minimum of an iterable of integers, 0 if it is empty.

    A domain can be empty only *below an invalid prune node* (a prune whose dominator is not in the
    current domain removes the last state when the tree is replayed without checking it).  Both
    checkers reject at that prune node and never read what lies below it, so the value emitted
    there is immaterial; it only has to be a number."""
    values = list(values)
    return min(values) if values else 0


def to_metricchain_cert1(cert: MinCertificate) -> dict:
    """The same claim and certificate in the theory division's JSON format (kind ``min``).

    The alphabet size is `k = max_i k_i`; tables are padded with zeros (padded states are outside
    every domain and are never read).  `u`, `p` and `ell` are the largest admissible values, so
    the reference checker accepts the document iff our checker accepts the certificate.
    Raises :class:`MalformedCertificate` for a certificate that is not well formed.
    """
    validate_structure(cert)
    model = cert.model
    n, sizes = model.n, model.sizes
    k = max(sizes)
    unit = 2 ** cert.unit_bits
    tscale = 2 ** model.scale_bits

    def table_entry(v):
        return _rat(Fraction(int(v), tscale))

    h = [[table_entry(model.unary[i][a]) if a < sizes[i] else 0 for a in range(k)] for i in range(n)]
    J = {}
    for (i, j), t in model.pair.items():
        J[f"{i},{j}"] = [[table_entry(t[a, b]) if (a < sizes[i] and b < sizes[j]) else 0 for b in range(k)]
                         for a in range(k)]

    mb = 2 ** cert.message_bits

    def hval(i, a):                      # table values in certificate units (exact integers)
        return int(model.unary[i][a]) * mb

    def jval(i, j, a, b):
        return int(model.pair_table(i, j)[a, b]) * mb

    def convert(node, D):
        # Chains of prune nodes are followed iteratively (they can be thousands long); recursion
        # happens only through branch nodes, whose nesting depth is at most the number of sites.
        chain = []
        while node["node"] == "prune":
            i, r, t = node["site"], node["remove"], node["dominator"]
            ell = {}
            for j in model.neighbors(i):
                ell[str(j)] = _rat(Fraction(_min0(jval(i, j, r, s) - jval(i, j, t, s) for s in D[j]), unit))
            chain.append({"node": "prune", "site": int(i), "remove": int(r), "dominator": int(t), "ell": ell})
            D = list(D)
            D[i] = [s for s in D[i] if s != r]
            node = node["rest"]
        kind = node["node"]
        if kind == "leaf":
            m = node.get("m", {})

            def msg(i, j, a):
                vec = m.get((i, j))
                return 0 if vec is None else int(vec[a])

            u = [_min0(hval(i, a) + sum(msg(i, j, a) for j in model.neighbors(i)) for a in D[i]) for i in range(n)]
            p, mjson = {}, {}
            for (i, j) in model.pair:
                P = _min0(jval(i, j, a, b) - msg(i, j, a) - msg(j, i, b) for a in D[i] for b in D[j])
                half = _rat(Fraction(P, 2 * unit))
                p[f"{i},{j}"] = half
                p[f"{j},{i}"] = half
            for (i, j), vec in m.items():
                mjson[f"{i},{j}"] = [_rat(Fraction(int(vec[a]), unit)) if a < sizes[i] else 0 for a in range(k)]
            out = {"node": "leaf", "u": [_rat(Fraction(v, unit)) for v in u], "p": p, "m": mjson}
        elif kind == "branch":
            i = node["site"]
            children = {}
            for a, sub in node["children"].items():
                D2 = list(D)
                D2[i] = [a]
                children[str(int(a))] = convert(sub, D2)
            out = {"node": "branch", "site": int(i), "children": children}
        else:
            raise MalformedCertificate(f"unknown node kind {kind!r}")
        for step in reversed(chain):
            step["rest"] = out
            out = step
        return out

    claim = {"lower_bound": _rat(Fraction(cert.lower_bound, unit))}
    if cert.witness is not None:
        claim["witness"] = [int(a) for a in cert.witness]
    return {
        "format": "metricchain-cert/1",
        "kind": "min",
        "n": n,
        "k": k,
        "domains": [[int(a) for a in d] for d in cert.domains],
        "instance": {"h": h, "J": J},
        "claim": claim,
        "certificate": convert(cert.root, [list(d) for d in cert.domains]),
    }


# ---------------------------------------------------------------------------------------------
# Compact serialisation `structbio-mincert/1`
# ---------------------------------------------------------------------------------------------

def _model_to_json(model: PairModel) -> dict:
    return {
        "scale_bits": model.scale_bits,
        "unary": [[int(v) for v in u.tolist()] for u in model.unary],
        "pair": {f"{i},{j}": [[int(v) for v in row] for row in t.tolist()] for (i, j), t in model.pair.items()},
        "meta": json.dumps(model.meta, sort_keys=True),      # opaque text: never interpreted by a checker
    }


def _strict_int(value, what: str) -> int:
    """An integer of the file: a JSON integer and nothing else (no float, boolean or string)."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise MalformedCertificate(f"{what}: expected an integer, got {type(value).__name__}")
    return value


def _strict_pair_key(key, what: str):
    parts = key.split(",") if isinstance(key, str) else []
    if len(parts) != 2 or not all(t.isdigit() and str(int(t)) == t for t in parts):
        raise MalformedCertificate(f"{what}: key {key!r} is not of the canonical form 'i,j'")
    return int(parts[0]), int(parts[1])


def _strict_load(text: str):
    """Parse JSON so that a file has one reading: duplicate keys, floating-point literals and
    the non-standard constants NaN / Infinity are errors."""
    def no_duplicates(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise MalformedCertificate(f"duplicate key {key!r}")
            out[key] = value
        return out

    def no_float(literal):
        raise MalformedCertificate(f"non-integer number {literal!r}")

    try:
        return json.loads(text, object_pairs_hook=no_duplicates, parse_float=no_float, parse_constant=no_float)
    except MalformedCertificate:
        raise
    except (ValueError, RecursionError) as exc:
        raise MalformedCertificate(f"not valid JSON ({type(exc).__name__})") from exc


def _meta_from_text(text) -> dict:
    """Metadata travel as one opaque JSON string, so that the strictly parsed part of a file
    contains integers only; metadata are provenance and are never read by a checker."""
    if text is None:
        return {}
    if not isinstance(text, str):
        raise MalformedCertificate("meta must be a string holding JSON text")
    try:
        meta = json.loads(text)
    except ValueError as exc:
        raise MalformedCertificate("meta is not JSON text") from exc
    if not isinstance(meta, dict):
        raise MalformedCertificate("meta must hold a JSON object")
    return meta


def _model_from_json(doc: dict) -> PairModel:
    if not isinstance(doc, dict) or not isinstance(doc.get("unary"), list) or not isinstance(doc.get("pair"), dict):
        raise MalformedCertificate("embedded instance: need 'unary' (list) and 'pair' (object)")
    unary = []
    for i, row in enumerate(doc["unary"]):
        if not isinstance(row, list):
            raise MalformedCertificate("embedded instance: unary rows must be lists")
        unary.append(np.array([_strict_int(v, f"unary[{i}]") for v in row], dtype=object))
    pair = {}
    for key, table in doc["pair"].items():
        i, j = _strict_pair_key(key, "embedded instance")
        if not isinstance(table, list) or not all(isinstance(r, list) for r in table):
            raise MalformedCertificate("embedded instance: pair tables must be lists of lists")
        arr = np.empty((len(table), len(table[0]) if table else 0), dtype=object)
        for a, r in enumerate(table):
            if len(r) != arr.shape[1]:
                raise MalformedCertificate("embedded instance: ragged pair table")
            for b, v in enumerate(r):
                arr[a, b] = _strict_int(v, f"pair[{key}]")
        pair[(i, j)] = arr
    try:
        return PairModel(unary=unary, pair=pair, scale_bits=_strict_int(doc.get("scale_bits"), "scale_bits"),
                         meta=_meta_from_text(doc.get("meta")))
    except (ValueError, TypeError) as exc:
        raise MalformedCertificate(f"embedded instance: {exc}") from exc


def _node_to_json(node: dict) -> dict:
    """Compact JSON of a certificate tree.  A chain of prune nodes is written as one flat node
    ``{"node": "prunes", "steps": [[site, remove, dominator], ...], "rest": ...}`` so that the
    nesting depth of the file is bounded by the number of nested branch nodes."""
    steps = []
    while node["node"] == "prune":
        steps.append([int(node["site"]), int(node["remove"]), int(node["dominator"])])
        node = node["rest"]
    if node["node"] == "leaf":
        out = {"node": "leaf", "m": {f"{i},{j}": [int(v) for v in vec] for (i, j), vec in node.get("m", {}).items()}}
    else:
        out = {"node": "branch", "site": int(node["site"]),
               "children": {str(int(a)): _node_to_json(c) for a, c in node["children"].items()}}
    return {"node": "prunes", "steps": steps, "rest": out} if steps else out


def _node_from_json(doc: dict) -> dict:
    if not isinstance(doc, dict):
        raise MalformedCertificate("certificate node must be an object")
    kind = doc.get("node")
    if kind == "leaf":
        m = {}
        messages = doc.get("m", {})
        if not isinstance(messages, dict):
            raise MalformedCertificate("leaf: m must be an object")
        for key, vec in messages.items():
            if not isinstance(vec, list):
                raise MalformedCertificate("leaf: a message must be a list")
            m[_strict_pair_key(key, "leaf message")] = [_strict_int(v, "leaf message") for v in vec]
        return {"node": "leaf", "m": m}
    if kind == "branch":
        children = doc.get("children")
        if not isinstance(children, dict):
            raise MalformedCertificate("branch: children must be an object")
        out = {}
        for a, c in children.items():
            if not (isinstance(a, str) and a.isdigit() and str(int(a)) == a):
                raise MalformedCertificate(f"branch: child key {a!r} is not a canonical natural number")
            out[int(a)] = _node_from_json(c)
        return {"node": "branch", "site": _strict_int(doc.get("site"), "branch site"), "children": out}
    if kind == "prunes":
        node = _node_from_json(doc.get("rest"))
        if node["node"] == "prune":
            raise MalformedCertificate("a 'prunes' node must not be followed directly by another one")
        steps = doc.get("steps")
        if not isinstance(steps, list) or not all(isinstance(t, list) and len(t) == 3 for t in steps):
            raise MalformedCertificate("prunes: steps must be a list of [site, remove, dominator]")
        for site, remove, dominator in reversed(steps):
            node = {"node": "prune", "site": _strict_int(site, "prune site"),
                    "remove": _strict_int(remove, "prune remove"),
                    "dominator": _strict_int(dominator, "prune dominator"), "rest": node}
        return node
    raise MalformedCertificate(f"unknown node kind {kind!r}")


def model_sha256(model: PairModel) -> str:
    """Checksum of the published instance (canonical JSON of scale and tables, without metadata)."""
    doc = _model_to_json(model)
    doc.pop("meta")
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def dumps(cert: MinCertificate, include_model: bool = True) -> str:
    """Serialise a certificate.  With ``include_model=False`` the file is *detached*: it names the
    instance by `model_sha256` only, and `loads` needs the instance (e.g. from `modelio.load_model`)."""
    doc = {"format": "structbio-mincert/1"}
    if include_model:
        doc["model"] = _model_to_json(cert.model)
    doc.update({
        "model_sha256": model_sha256(cert.model),
        "message_bits": int(cert.message_bits),
        "domains": [[int(a) for a in d] for d in cert.domains],
        "claim": {"lower_bound": int(cert.lower_bound),
                  "witness": None if cert.witness is None else [int(a) for a in cert.witness]},
        "certificate": _node_to_json(cert.root),
        "meta": json.dumps(cert.meta, sort_keys=True),
    })
    return json.dumps(doc, separators=(",", ":"))


def loads(text: str, model: PairModel | None = None) -> MinCertificate:
    """Parse a certificate file, strictly: duplicate keys, non-integer numbers and wrong types are
    errors (:class:`MalformedCertificate`), so that a file has exactly one reading.  For a detached
    file the instance must be supplied and must have the checksum recorded in the file; an embedded
    instance must have its recorded checksum too."""
    doc = _strict_load(text)
    if not isinstance(doc, dict) or doc.get("format") != "structbio-mincert/1":
        raise MalformedCertificate("unknown format")
    if "model" in doc:
        model = _model_from_json(doc["model"])
    elif model is None:
        raise MalformedCertificate("detached certificate: the instance must be supplied")
    if model_sha256(model) != doc.get("model_sha256"):
        raise MalformedCertificate("the instance does not have the checksum recorded in the certificate")
    claim = doc.get("claim")
    domains = doc.get("domains")
    if not isinstance(claim, dict) or not isinstance(domains, list) or not all(isinstance(d, list) for d in domains):
        raise MalformedCertificate("need 'claim' (object) and 'domains' (list of lists)")
    witness = claim.get("witness")
    if witness is not None and not isinstance(witness, list):
        raise MalformedCertificate("witness must be a list or null")
    return MinCertificate(model=model, message_bits=_strict_int(doc.get("message_bits"), "message_bits"),
                          domains=[[_strict_int(a, "domain") for a in d] for d in domains],
                          lower_bound=_strict_int(claim.get("lower_bound"), "lower_bound"),
                          witness=None if witness is None else tuple(_strict_int(a, "witness") for a in witness),
                          root=_node_from_json(doc.get("certificate")), meta=_meta_from_text(doc.get("meta")))
