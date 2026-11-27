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

How a certificate is read (review STRUCTBIO-REV-0001).  Whoever computes with a certificate —
the checker, the converter, the serialiser — first takes its `normalised` copy: every integer
becomes a Python `int` (NumPy integers are converted; `bool`, `float`, `str`, `Fraction` are
refused), every container a plain list, tuple or dict, and the node graph is copied as a tree in
one iterative pass that visits a branch or prune node at most once (a node object that occurs
twice, shared or cyclic, is refused; a leaf may be referred to from several places).  The
instance is read through `model.integer_tables` at the same moment.

Documented limits of this module (each is enforced where it is named and tested on both sides in
`tests/structbio/test_hardening.py`):

* ``MAX_INT_DIGITS = 1000`` — decimal digits of any numeral of a certificate file (JSON integers
  and the numerals inside keys; also used by `zcert`), whatever the interpreter's own limit is;
* ``MAX_FILE_DEPTH = 2000`` — nodes on a path of the tree of a `structbio-mincert/1` file (a
  ``prunes`` node counts once), enforced by `dumps` and by `loads`.  In memory there is no limit:
  the checker is iterative;
* ``MAX_CERT1_NESTING = 5000`` — nesting of the tree that `to_metricchain_cert1` writes (one level
  per prune node, two per branch node); beyond it the converter raises `ConversionTooDeep`.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

from .model import PairModel, exact_int, integer_tables

__all__ = ["MinCertificate", "MalformedCertificate", "ConversionTooDeep", "normalised", "validate_structure", "snapshot",
           "to_metricchain_cert1", "dumps", "loads", "count_nodes", "model_sha256", "tables_sha256",
           "MAX_INT_DIGITS", "MAX_FILE_DEPTH", "MAX_CERT1_NESTING"]

MAX_INT_DIGITS = 1000
MAX_FILE_DEPTH = 2000
MAX_CERT1_NESTING = 5000


class MalformedCertificate(ValueError):
    """The certificate is not a well-formed object of the format (indices out of range, wrong shapes)."""


class ConversionTooDeep(ValueError):
    """The certificate is well formed, but written in the nested format `metricchain-cert/1` its
    tree would be nested more than `MAX_CERT1_NESTING` levels deep — more than the JSON parser of
    the reference checker is known to read.  (Not a `MalformedCertificate`: nothing is wrong
    with the certificate, and `check_min_certificate` judges it.)"""


@dataclass
class MinCertificate:
    model: PairModel
    message_bits: int
    domains: list
    lower_bound: int
    witness: tuple | None           # a tuple (or list) with one state per site, or None
    root: dict
    meta: dict = field(default_factory=dict)

    @property
    def unit_bits(self) -> int:
        return exact_int(self.model.scale_bits, "scale_bits") + exact_int(self.message_bits, "message_bits")

    def lower_bound_fraction(self) -> Fraction:
        """The claimed bound in energy units (computed in Python integers, whatever the fields hold)."""
        return Fraction(exact_int(self.lower_bound, "lower_bound"), 2 ** self.unit_bits)


def _index(v, what: str) -> int:
    try:
        return exact_int(v, what)
    except TypeError as exc:
        raise MalformedCertificate(str(exc)) from None


def _int_vector(vec, length: int, message: str) -> list:
    """A new list of `length` Python integers from a list of integers (NumPy integers are converted)."""
    if not isinstance(vec, list) or len(vec) != length:
        raise MalformedCertificate(message)
    out = list(vec)
    if set(map(type, out)) <= {int}:                    # the usual case, decided at C speed
        return out
    try:
        return [exact_int(v) for v in out]
    except TypeError:
        raise MalformedCertificate(message) from None


def instance_tables(model) -> tuple:
    """`model.integer_tables(model)`, with its refusals reported as :class:`MalformedCertificate`."""
    try:
        return integer_tables(model)
    except (ValueError, TypeError) as exc:
        raise MalformedCertificate(f"the instance is not a well-formed PairModel ({exc})") from None


def normalised(cert: MinCertificate, tables=None) -> MinCertificate:
    """The certificate as a checker reads it: a copy made of Python integers, lists, tuples and
    dicts only, whose `root` is a tree (see the module docstring).

    Raises :class:`MalformedCertificate` unless every index is in range, every vector has its
    length, every integer is an `int` or a NumPy integer, the witness (if any) is a tuple or
    list of one existing state per site, and no branch or prune node occurs twice.  The pass is
    iterative and linear in the size of the object.  `tables` is the `model.integer_tables`
    snapshot of the instance when the caller already holds one."""
    if not isinstance(cert, MinCertificate):
        raise MalformedCertificate("not a MinCertificate")
    _, unary, pair = instance_tables(cert.model) if tables is None else tables
    n, sizes = len(unary), [len(u) for u in unary]
    message_bits = _index(cert.message_bits, "message_bits")
    if message_bits < 0:
        raise MalformedCertificate("message_bits must be a natural number")
    lower_bound = _index(cert.lower_bound, "lower_bound (units of 2**-(scale_bits+message_bits))")
    if not isinstance(cert.domains, list) or len(cert.domains) != n:
        raise MalformedCertificate(f"domains must list {n} sites")
    domains = []
    for i, d in enumerate(cert.domains):
        if not isinstance(d, list) or not d:
            raise MalformedCertificate(f"domain of site {i} must be a non-empty list (an empty box certifies nothing)")
        states = _int_vector(d, len(d), f"domain of site {i} must list states (integers)")
        if any(not 0 <= a < sizes[i] for a in states) or len(set(states)) != len(states):
            raise MalformedCertificate(f"domain of site {i} has a repeated or out-of-range state")
        domains.append(states)
    witness = cert.witness
    if witness is not None:
        message = "witness must be a tuple or list that assigns an existing state to every site"
        if not isinstance(witness, (tuple, list)):
            raise MalformedCertificate(message)
        witness = tuple(_int_vector(list(witness), n, message))
        if any(not 0 <= a < sizes[i] for i, a in enumerate(witness)):
            raise MalformedCertificate(message)

    holder = {}
    seen = set()                                        # identities of the branch and prune nodes met so far
    stack = [(cert.root, holder, "root")]
    while stack:
        node, parent, slot = stack.pop()
        if not isinstance(node, dict):
            raise MalformedCertificate("certificate node must be an object")
        kind = node.get("node")
        if kind == "leaf":
            if set(node) - {"node", "m"}:
                raise MalformedCertificate("leaf: unknown field")
            m = node.get("m", {})
            if not isinstance(m, dict):
                raise MalformedCertificate("leaf: m must be a mapping")
            messages = {}
            for key, vec in m.items():
                if (not isinstance(key, tuple)) or len(key) != 2:
                    raise MalformedCertificate(f"leaf: message key {key!r} is not an ordered pair of sites")
                i, j = _index(key[0], "leaf: message key"), _index(key[1], "leaf: message key")
                if not (0 <= i < n and 0 <= j < n and i != j) or (min(i, j), max(i, j)) not in pair:
                    raise MalformedCertificate(f"leaf: message key {key!r} is not a listed pair of the model")
                if (i, j) in messages:
                    raise MalformedCertificate(f"leaf: message {key!r} is given twice")
                messages[(i, j)] = _int_vector(
                    vec, sizes[i], f"leaf: message {key!r} must list one integer per state of site {i}")
            parent[slot] = {"node": "leaf", "m": messages}
            continue
        if kind not in ("branch", "prune"):
            raise MalformedCertificate(f"unknown node kind {kind!r}")
        if id(node) in seen:
            raise MalformedCertificate("a branch or prune node occurs twice: the certificate is not a tree")
        seen.add(id(node))
        if kind == "branch":
            if set(node) - {"node", "site", "children"}:
                raise MalformedCertificate("branch: unknown field")
            i = _index(node.get("site"), "branch: site")
            if not 0 <= i < n:
                raise MalformedCertificate("branch: site out of range")
            ch = node.get("children")
            if not isinstance(ch, dict):
                raise MalformedCertificate("branch: children must be a mapping")
            children = {}
            for a, sub in ch.items():
                a = _index(a, "branch: child state")
                if not 0 <= a < sizes[i] or a in children:
                    raise MalformedCertificate("branch: child state out of range")
                children[a] = None                      # keeps the order of the children
                stack.append((sub, children, a))
            parent[slot] = {"node": "branch", "site": i, "children": children}
        else:
            if set(node) - {"node", "site", "remove", "dominator", "rest"}:
                raise MalformedCertificate("prune: unknown field")
            i = _index(node.get("site"), "prune: site")
            if not 0 <= i < n:
                raise MalformedCertificate("prune: site out of range")
            new = {"node": "prune", "site": i}
            for name in ("remove", "dominator"):
                a = _index(node.get(name), f"prune: {name}")
                if not 0 <= a < sizes[i]:
                    raise MalformedCertificate(f"prune: {name} out of range")
                new[name] = a
            new["rest"] = None
            parent[slot] = new
            stack.append((node.get("rest"), new, "rest"))
    return MinCertificate(model=cert.model, message_bits=message_bits, domains=domains, lower_bound=lower_bound,
                          witness=witness, root=holder["root"], meta=cert.meta)


def validate_structure(cert: MinCertificate) -> None:
    """Raise :class:`MalformedCertificate` unless `cert` is a well-formed certificate of its instance
    (exactly the conditions of `normalised`, whose copy the checkers compute with)."""
    normalised(cert)


def snapshot(cert: MinCertificate) -> tuple:
    """`(normalised certificate, integer tables of its instance)`, both taken now — what the checker,
    the converter and the serialiser compute with."""
    if not isinstance(cert, MinCertificate):
        raise MalformedCertificate("not a MinCertificate")
    tables = instance_tables(cert.model)
    return normalised(cert, tables), tables


def count_nodes(root: dict) -> dict:
    """Number of nodes of each kind and of stored message integers (certificate size statistics).
    For the tree of a certificate that has been validated (it does not look for repeated nodes)."""
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
    the reference checker accepts the document iff our checker accepts the certificate — for
    every certificate inside the integer range our checker supports (`mincheck`: the reference
    checker computes in rationals and has no such range).

    The traversal is iterative: it does not depend on the interpreter's recursion limit, whatever
    the shape of the tree (a hand-built tree may branch on one site again and again).  The
    *output*, however, is nested one JSON level per prune node and two per branch node, and a
    reader takes only so many levels: measured with CPython 3.13 on Linux, `json` writes and
    parses 9,997 nested objects, and the reference checker judges chains of up to 9,993 prune
    nodes and up to 3,330 nested branch nodes (beyond that it answers "nested too deeply").  A
    certificate whose converted tree would be nested more than `MAX_CERT1_NESTING` = 5000 levels
    — 5,000 consecutive eliminations, or 2,500 nested branch nodes — is therefore not converted:
    :class:`ConversionTooDeep`.  (The stored development certificates need at most 1,332 levels;
    as files of the compact format they are at most 6 nodes deep.)

    Raises :class:`MalformedCertificate` for a certificate that is not well formed.
    """
    cert, tables = snapshot(cert)
    scale_bits, unary, pair = tables
    n, sizes = len(unary), [len(u) for u in unary]
    k = max(sizes, default=0)
    unit = 2 ** (scale_bits + cert.message_bits)
    tscale = 2 ** scale_bits
    mb = 2 ** cert.message_bits
    nbrs = [[] for _ in range(n)]                       # derived from the tables, in increasing order
    for (i, j) in pair:
        nbrs[i].append(j)
        nbrs[j].append(i)

    def table_entry(v):
        return _rat(Fraction(v, tscale))

    h = [[table_entry(unary[i][a]) if a < sizes[i] else 0 for a in range(k)] for i in range(n)]
    J = {}
    for (i, j), t in pair.items():
        J[f"{i},{j}"] = [[table_entry(t[a][b]) if (a < sizes[i] and b < sizes[j]) else 0 for b in range(k)]
                         for a in range(k)]

    def hval(i, a):                      # table values in certificate units (exact integers)
        return unary[i][a] * mb

    def jval(i, j, a, b):
        return (pair[(i, j)][a][b] if i < j else pair[(j, i)][b][a]) * mb

    holder = {}
    stack = [(cert.root, [list(d) for d in cert.domains], holder, "certificate", 1)]
    while stack:
        node, D, parent, slot, level = stack.pop()
        if level > MAX_CERT1_NESTING:
            raise ConversionTooDeep(f"the converted certificate would be nested more than {MAX_CERT1_NESTING} levels "
                                    f"deep (one level per prune node, two per branch node)")
        kind = node["node"]
        if kind == "prune":
            i, r, t = node["site"], node["remove"], node["dominator"]
            ell = {}
            for j in nbrs[i]:
                ell[str(j)] = _rat(Fraction(_min0(jval(i, j, r, s) - jval(i, j, t, s) for s in D[j]), unit))
            out = {"node": "prune", "site": i, "remove": r, "dominator": t, "ell": ell, "rest": None}
            parent[slot] = out
            D = list(D)
            D[i] = [s for s in D[i] if s != r]
            stack.append((node["rest"], D, out, "rest", level + 1))
        elif kind == "leaf":
            m = node["m"]

            def msg(i, j, a):
                vec = m.get((i, j))
                return 0 if vec is None else vec[a]

            u = [_min0(hval(i, a) + sum(msg(i, j, a) for j in nbrs[i]) for a in D[i]) for i in range(n)]
            p, mjson = {}, {}
            for (i, j) in pair:
                P = _min0(jval(i, j, a, b) - msg(i, j, a) - msg(j, i, b) for a in D[i] for b in D[j])
                half = _rat(Fraction(P, 2 * unit))
                p[f"{i},{j}"] = half
                p[f"{j},{i}"] = half
            for (i, j), vec in m.items():
                mjson[f"{i},{j}"] = [_rat(Fraction(vec[a], unit)) if a < sizes[i] else 0 for a in range(k)]
            parent[slot] = {"node": "leaf", "u": [_rat(Fraction(v, unit)) for v in u], "p": p, "m": mjson}
        else:
            i = node["site"]
            children = {}
            parent[slot] = {"node": "branch", "site": i, "children": children}
            for a, sub in node["children"].items():
                D2 = list(D)
                D2[i] = [a]
                children[str(a)] = None                 # keeps the order of the children
                stack.append((sub, D2, children, str(a), level + 2))

    claim = {"lower_bound": _rat(Fraction(cert.lower_bound, unit))}
    if cert.witness is not None:
        claim["witness"] = list(cert.witness)
    return {
        "format": "metricchain-cert/1",
        "kind": "min",
        "n": n,
        "k": k,
        "domains": [list(d) for d in cert.domains],
        "instance": {"h": h, "J": J},
        "claim": claim,
        "certificate": holder["certificate"],
    }


# ---------------------------------------------------------------------------------------------
# Compact serialisation `structbio-mincert/1`
# ---------------------------------------------------------------------------------------------

def _tables_to_json(scale_bits: int, unary: list, pair: dict) -> dict:
    return {"scale_bits": scale_bits, "unary": unary,
            "pair": {f"{i},{j}": rows for (i, j), rows in pair.items()}}


def tables_sha256(scale_bits: int, unary: list, pair: dict) -> str:
    """Checksum of an instance given by its `model.integer_tables` (canonical JSON of scale and
    tables, without metadata)."""
    doc = _tables_to_json(scale_bits, unary, pair)
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def model_sha256(model: PairModel) -> str:
    """Checksum of the published instance as it is now (canonical JSON of scale and tables, without
    metadata).  `ValueError` / `TypeError` for an object that is not an integer `PairModel`."""
    return tables_sha256(*integer_tables(model))


def _strict_int(value, what: str) -> int:
    """An integer of the file: a JSON integer and nothing else (no float, boolean or string)."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise MalformedCertificate(f"{what}: expected an integer, got {type(value).__name__}")
    return value


def _natural(text, what: str) -> int:
    """The natural number written by a key of the file, which must be in canonical form: ASCII
    digits only (`str.isdigit` alone also admits characters such as SUPERSCRIPT TWO, which `int`
    cannot read), no sign, no leading zero, at most `MAX_INT_DIGITS` digits."""
    if not (isinstance(text, str) and text.isascii() and text.isdigit() and len(text) <= MAX_INT_DIGITS
            and (text == "0" or text[0] != "0")):
        raise MalformedCertificate(f"{what}: {text!r} is not a canonical natural number")
    return int(text)


def _strict_pair_key(key, what: str):
    parts = key.split(",") if isinstance(key, str) else []
    if len(parts) != 2:
        raise MalformedCertificate(f"{what}: key {key!r} is not of the canonical form 'i,j'")
    return _natural(parts[0], what), _natural(parts[1], what)


def _bounded_int(literal: str) -> int:
    """An integer literal of the file, at most `MAX_INT_DIGITS` digits long (the limit is ours:
    the interpreter's own limit on integer conversion can be switched off, and is by the
    reference checker)."""
    if len(literal) - literal.startswith("-") > MAX_INT_DIGITS:
        raise MalformedCertificate(f"an integer of more than {MAX_INT_DIGITS} digits")
    return int(literal)


def _strict_load(text: str):
    """Parse JSON so that a file has one reading: duplicate keys, floating-point literals, the
    non-standard constants NaN / Infinity and integers of more than `MAX_INT_DIGITS` digits are
    errors."""
    if not isinstance(text, str):
        raise MalformedCertificate("a certificate file is text")

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
        return json.loads(text, object_pairs_hook=no_duplicates, parse_float=no_float, parse_constant=no_float,
                          parse_int=_bounded_int)
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
        meta = json.loads(text, parse_int=_bounded_int)
    except (ValueError, RecursionError) as exc:
        raise MalformedCertificate("meta is not JSON text") from exc
    if not isinstance(meta, dict):
        raise MalformedCertificate("meta must hold a JSON object")
    return meta


def _only(doc: dict, allowed: tuple, what: str) -> None:
    """Unknown fields are errors: a misspelt or misplaced field must not go unnoticed."""
    extra = sorted(set(doc) - set(allowed))
    if extra:
        raise MalformedCertificate(f"{what}: unknown field {extra[0]!r}")


def _model_from_json(doc: dict) -> PairModel:
    if not isinstance(doc, dict) or not isinstance(doc.get("unary"), list) or not isinstance(doc.get("pair"), dict):
        raise MalformedCertificate("embedded instance: need 'unary' (list) and 'pair' (object)")
    _only(doc, ("scale_bits", "unary", "pair", "meta"), "embedded instance")
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


def _tree_text(root: dict) -> str:
    """Compact JSON text of a normalised certificate tree, written without recursion.  A chain of
    prune nodes is written as one flat node
    ``{"node": "prunes", "steps": [[site, remove, dominator], ...], "rest": ...}``.  The text is
    what `json.dumps(..., separators=(",", ":"))` writes for the nested object; a tree deeper than
    `MAX_FILE_DEPTH` nodes is refused (`loads` would not read it back)."""
    parts = []
    stack = [(root, 1)]                                 # a node with its depth in the file, or a piece of text
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            parts.append(item)
            continue
        node, depth = item
        closing = ""
        if node["node"] == "prune":
            steps = []
            while node["node"] == "prune":
                steps.append([node["site"], node["remove"], node["dominator"]])
                node = node["rest"]
            parts.append('{"node":"prunes","steps":' + json.dumps(steps, separators=(",", ":")) + ',"rest":')
            closing = "}"
            depth += 1
        if depth > MAX_FILE_DEPTH:
            raise MalformedCertificate(f"certificate nested more than {MAX_FILE_DEPTH} nodes deep: "
                                       f"deeper than a structbio-mincert/1 file may be")
        if node["node"] == "leaf":
            leaf = {"node": "leaf", "m": {f"{i},{j}": vec for (i, j), vec in node["m"].items()}}
            parts.append(json.dumps(leaf, separators=(",", ":")) + closing)
        else:
            parts.append('{"node":"branch","site":%d,"children":{' % node["site"])
            stack.append("}}" + closing)
            children = list(node["children"].items())
            for index in range(len(children) - 1, -1, -1):
                state, child = children[index]
                stack.append((child, depth + 1))
                stack.append(("," if index else "") + '"%d":' % state)
    return "".join(parts)


def _tree_from_json(doc) -> dict:
    """The certificate tree of a file, read strictly and without recursion: unknown fields are
    errors, a ``prunes`` node has at least one step and is not followed directly by another one
    (so a chain of eliminations has one spelling), and the tree is at most `MAX_FILE_DEPTH`
    nodes deep."""
    holder = {}
    stack = [(doc, holder, "root", 1, False)]           # (JSON value, parent, slot, depth, parent is a 'prunes' node)
    while stack:
        doc, parent, slot, depth, after_prunes = stack.pop()
        if not isinstance(doc, dict):
            raise MalformedCertificate("certificate node must be an object")
        if depth > MAX_FILE_DEPTH:
            raise MalformedCertificate(f"certificate nested more than {MAX_FILE_DEPTH} nodes deep")
        kind = doc.get("node")
        if kind == "leaf":
            _only(doc, ("node", "m"), "leaf")
            messages = doc.get("m", {})
            if not isinstance(messages, dict):
                raise MalformedCertificate("leaf: m must be an object")
            m = {}
            for key, vec in messages.items():
                if not isinstance(vec, list):
                    raise MalformedCertificate("leaf: a message must be a list")
                if not set(map(type, vec)) <= {int}:
                    raise MalformedCertificate("leaf message: expected integers")
                m[_strict_pair_key(key, "leaf message")] = vec
            parent[slot] = {"node": "leaf", "m": m}
        elif kind == "branch":
            _only(doc, ("node", "site", "children"), "branch")
            children = doc.get("children")
            if not isinstance(children, dict):
                raise MalformedCertificate("branch: children must be an object")
            out = {}
            parent[slot] = {"node": "branch", "site": _strict_int(doc.get("site"), "branch site"), "children": out}
            for a, child in children.items():
                state = _natural(a, "branch: child key")
                out[state] = None                       # keeps the order of the children
                stack.append((child, out, state, depth + 1, False))
        elif kind == "prunes":
            _only(doc, ("node", "steps", "rest"), "prunes")
            if after_prunes:
                raise MalformedCertificate("a 'prunes' node must not be followed directly by another one")
            steps = doc.get("steps")
            if not isinstance(steps, list) or not steps or not all(isinstance(t, list) and len(t) == 3 for t in steps):
                raise MalformedCertificate("prunes: steps must be a non-empty list of [site, remove, dominator]")
            for site, remove, dominator in steps:
                node = {"node": "prune", "site": _strict_int(site, "prune site"),
                        "remove": _strict_int(remove, "prune remove"),
                        "dominator": _strict_int(dominator, "prune dominator"), "rest": None}
                parent[slot] = node
                parent, slot = node, "rest"
            stack.append((doc.get("rest"), parent, slot, depth + 1, True))
        else:
            raise MalformedCertificate(f"unknown node kind {kind!r}")
    return holder["root"]


def dumps(cert: MinCertificate, include_model: bool = True) -> str:
    """Serialise a certificate.  With ``include_model=False`` the file is *detached*: it names the
    instance by `model_sha256` only, and `loads` needs the instance (e.g. from `modelio.load_model`).

    The certificate is normalised first (:class:`MalformedCertificate` if it is not well formed)
    and written without recursion; a tree deeper than `MAX_FILE_DEPTH` nodes is refused."""
    cert, tables = snapshot(cert)
    fields = [("format", '"structbio-mincert/1"')]
    if include_model:
        model_doc = _tables_to_json(*tables)
        model_doc["meta"] = json.dumps(cert.model.meta, sort_keys=True)      # opaque text: never interpreted by a checker
        fields.append(("model", json.dumps(model_doc, separators=(",", ":"))))
    claim = {"lower_bound": cert.lower_bound, "witness": None if cert.witness is None else list(cert.witness)}
    fields += [("model_sha256", json.dumps(tables_sha256(*tables))),
               ("message_bits", json.dumps(cert.message_bits)),
               ("domains", json.dumps(cert.domains, separators=(",", ":"))),
               ("claim", json.dumps(claim, separators=(",", ":"))),
               ("certificate", _tree_text(cert.root)),
               ("meta", json.dumps(json.dumps(cert.meta, sort_keys=True)))]
    return "{" + ",".join(f'"{name}":{text}' for name, text in fields) + "}"


def loads(text: str, model: PairModel | None = None) -> MinCertificate:
    """Parse a certificate file, strictly: duplicate keys, unknown fields, non-integer numbers,
    non-canonical keys and wrong types are errors, so that a file has exactly one reading.

    The instance.  For a detached file the instance must be supplied and must have the checksum
    recorded in the file; an embedded instance must have its recorded checksum too.  When the
    file embeds an instance *and* one is supplied, the two must be the same instance (equal
    checksums) — a file about other tables than the caller's is refused, never returned.

    Raises :class:`MalformedCertificate` and nothing else, whatever the text: deep nesting,
    numerals of more than `MAX_INT_DIGITS` digits and every other failure of the parser are
    reported as malformed.  Indices are checked against the instance by `normalised` (that is,
    by the checker), not here."""
    try:
        return _loads(text, model)
    except MalformedCertificate:
        raise
    except Exception as exc:  # noqa: BLE001  (one exception type for whoever turns it into a rejection)
        raise MalformedCertificate(f"not a readable certificate ({type(exc).__name__})") from exc


def _loads(text, model) -> MinCertificate:
    doc = _strict_load(text)
    if not isinstance(doc, dict) or doc.get("format") != "structbio-mincert/1":
        raise MalformedCertificate("unknown format")
    _only(doc, ("format", "model", "model_sha256", "message_bits", "domains", "claim", "certificate", "meta"),
          "certificate file")
    if model is not None and not isinstance(model, PairModel):
        raise MalformedCertificate("the instance supplied is not a PairModel")
    if "model" in doc:
        embedded = _model_from_json(doc["model"])
        checksum = model_sha256(embedded)
        if model is None:
            model = embedded
        elif model_sha256(model) != checksum:
            raise MalformedCertificate("the file embeds another instance than the one supplied: "
                                       "it is a certificate about other tables")
    elif model is None:
        raise MalformedCertificate("detached certificate: the instance must be supplied")
    else:
        checksum = model_sha256(model)
    if checksum != doc.get("model_sha256"):
        raise MalformedCertificate("the instance does not have the checksum recorded in the certificate")
    claim = doc.get("claim")
    domains = doc.get("domains")
    if not isinstance(claim, dict) or not isinstance(domains, list) or not all(isinstance(d, list) for d in domains):
        raise MalformedCertificate("need 'claim' (object) and 'domains' (list of lists)")
    _only(claim, ("lower_bound", "witness"), "claim")
    witness = claim.get("witness")
    if witness is not None and not isinstance(witness, list):
        raise MalformedCertificate("witness must be a list or null")
    return MinCertificate(model=model, message_bits=_strict_int(doc.get("message_bits"), "message_bits"),
                          domains=[[_strict_int(a, "domain") for a in d] for d in domains],
                          lower_bound=_strict_int(claim.get("lower_bound"), "lower_bound"),
                          witness=None if witness is None else tuple(_strict_int(a, "witness") for a in witness),
                          root=_tree_from_json(doc.get("certificate")), meta=_meta_from_text(doc.get("meta")))
