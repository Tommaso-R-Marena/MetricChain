"""Certificates of two-sided bounds on partition functions ("Z" certificates; capability C2).

Object.  For a :class:`PairModel` with energy `E` (table units `u = 2**-scale_bits`), a rational
inverse temperature `beta` (per energy unit) and a box `B = prod_i D_i`:

    Z(B) = sum_{x in B} exp(-beta * E(x)).

A certificate is a *recipe that a checker replays*; it contains no number that is trusted:

1. ``steps`` — a list, applied in order to a working model `(H, J)` and a working box `D`:

   * ``{"op": "prune", "site": i, "remove": r, "dominator": t}`` — thermal dead-end elimination.
     The checker computes the Goldstein margin on the working model and box,
     `m = H_i(r) - H_i(t) + sum_{j ~ i} min_{s in D_j} (J_ij(r, s) - J_ij(t, s))`; then
     `Z(D without r) <= Z(D) <= (1 + exp(-beta*m)) * Z(D without r)` (the inequality inside the
     theory division's `zprune_sound`, [V], in energy form), and `r` leaves `D_i`.
   * ``{"op": "relax", "pair": [i, j], "f": [...], "g": [...]}`` — product-form relaxation of a
     pair.  With `R(a, b) = J_ij(a, b) - f(a) - g(b)` and `r_lo <= R <= r_hi` on `D_i x D_j`
     (computed by the checker), the pair is removed, `f` and `g` are added to `H_i`, `H_j`, and
     `exp(-beta*r_hi) * Z' <= Z <= exp(-beta*r_lo) * Z'`.  (Paper proof, two lines: every
     configuration's weight changes by a factor in that range.  Item R-3 of STRUCTBIO-REQ-0003;
     label [P], unrefereed.)

2. ``order`` — an elimination order of all sites (all but ``keep``).  Boltzmann factors of the
   working model are enclosed by the certified exponential of `expo` and the sites are summed out
   one at a time on factor tables (bucket elimination): exact for the rational weight tables,
   so the lower tables give a lower bound and the upper tables an upper bound.  (The identity is
   the theory division's `sum_boxFinset_fix`/`Z_sumOut` [V] in spirit; for more than two
   neighbours it is item R-1 of STRUCTBIO-REQ-0003, label [P], unrefereed.)

3. ``keep`` — optionally one site that is not summed out; the checker then reports an enclosure
   of the restricted sums `Z(B, x_keep = a)` and from them population intervals.

4. ``branch`` / ``children`` — conditioning.  Instead of an ``order`` a node may name a site `i`
   (not the kept one) and give, for every state `a` of the working domain of `i`, a child node
   ``{"steps": [...], "order": [...]}`` or ``{"steps": [...], "branch": i', "children": {...}}``.
   The child is checked on the working model with `D_i = {a}`, starting from the state reached
   after this node's steps, and `Z(D) = sum_a Z(D with x_i = a)` (the theory division's
   `WInstance.Z_branch`, [V]).  Conditioning trades one large elimination table for many small
   ones; each child prunes, relaxes and eliminates on its own.

Result.  With `A_lo`, `A_hi` the accumulated logarithmic factors of the steps,

    ln Z(B)  in  [ ln Z'_lo + A_lo ,  ln Z'_hi + A_hi ].

Claims.  The interval is computed by the checker; a certificate needs no claim.  A claim
``{"ln_z_lo": q, "ln_z_hi": q}`` (either bound may be absent) is what the *producer* asserts,
and the checker accepts the certificate iff the interval it computes itself lies inside the
claim: `claim lo <= computed lo` and `computed hi <= claim hi`.  The interval a checker
computes depends, in its last digits, on options that the file does not bind — the arithmetic
tier and the precision `exp_bits` of the exponential.  A producer therefore does not store its
own interval but `outward_claim` of it: both ends moved outward to the grid
`2**-CLAIM_GRID_BITS` nats and then one grid step further, so that every checker whose bounds
differ from the producer's by less than one grid step (the other tier; `exp_bits` between 48 and
96 on instances of the sizes tested) accepts an honest certificate.  The claim is thereby at
most two grid steps (about 2e-6 nats) wider on each side than what the producer computed.
Units: `f`, `g` are integers in table units.

How a certificate is read (review STRUCTBIO-REV-0001).  The checker computes with the
`normalised` copy: every integer a Python `int` (NumPy integers are converted; `bool`, `float`,
`str` are refused), `beta` and the claim rebuilt as rationals of Python integers, and the node
graph copied as a tree in one iterative pass in which a node object that occurs twice (shared
or cyclic) is refused.

Documented limits of the format (tested on both sides in `tests/structbio/test_hardening.py`):

* ``MAX_BRANCH_DEPTH = 500`` — nested conditioning (``branch``) nodes, in memory and in files;
  the evaluator of the checker recurses once per level, and the limit keeps it inside the
  interpreter's default recursion limit;
* numerals of a file have at most `mincert.MAX_INT_DIGITS` = 1000 digits.

Status: the checker implementation is tested against enumeration (`tests/structbio/test_zcert.py`,
`tests/structbio/test_adversarial_zcheck.py`); the rule semantics are [V] for chains and [P] in
general — a result accepted here is label **[CP]**, not [CK], until the rules are machine-checked.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from fractions import Fraction

from .mincert import (MalformedCertificate, _meta_from_text, _natural, _only, _strict_int, _strict_load,
                      tables_sha256)
from .model import PairModel, exact_int, integer_tables

__all__ = ["ZCertificate", "MalformedZCertificate", "normalised", "validate_structure", "snapshot", "outward_claim",
           "dumps", "loads", "MAX_BRANCH_DEPTH", "CLAIM_GRID_BITS"]

MAX_BRANCH_DEPTH = 500
CLAIM_GRID_BITS = 20


class MalformedZCertificate(ValueError):
    pass


@dataclass
class ZCertificate:
    model: PairModel
    beta: Fraction
    domains: list
    steps: list
    order: list
    keep: int | None = None
    claim: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)
    branch: int | None = None          # conditioning site of the root node (then `order` is empty)
    children: dict | None = None       # state -> child node (see the module docstring)

    def root_node(self) -> dict:
        node = {"steps": self.steps}
        if self.branch is None:
            node["order"] = self.order
        else:
            node["branch"], node["children"] = self.branch, self.children
        return node


def outward_claim(ln_z_lo: Fraction, ln_z_hi: Fraction) -> dict:
    """The claim a producer stores for an interval `[ln_z_lo, ln_z_hi]` it has computed: both ends
    rounded outward to the grid ``2**-CLAIM_GRID_BITS`` nats and moved one grid step further out
    (see "Claims" in the module docstring)."""
    grid = 2 ** CLAIM_GRID_BITS
    return {"ln_z_lo": Fraction(math.floor(Fraction(ln_z_lo) * grid) - 1, grid),
            "ln_z_hi": Fraction(math.ceil(Fraction(ln_z_hi) * grid) + 1, grid)}


def _index(v, what: str) -> int:
    try:
        return exact_int(v, what)
    except TypeError as exc:
        raise MalformedZCertificate(str(exc)) from None


def _int_list(vec, message: str) -> list:
    """A new list of Python integers from a list of integers (NumPy integers are converted)."""
    if not isinstance(vec, list):
        raise MalformedZCertificate(message)
    try:
        return [exact_int(v) for v in vec]
    except TypeError:
        raise MalformedZCertificate(message) from None


def _rational(value, what: str) -> Fraction:
    """`value` rebuilt from Python integers.  A `Fraction` made of NumPy integers keeps them, and
    arithmetic with it wraps around at their width."""
    if not isinstance(value, Fraction):
        raise MalformedZCertificate(f"{what} must be a Fraction")
    return Fraction(_index(value.numerator, what), _index(value.denominator, what))


def snapshot(cert: ZCertificate) -> tuple:
    """`(normalised certificate, integer tables of its instance)`, both taken now — what the checker
    and the serialiser compute with."""
    if not isinstance(cert, ZCertificate):
        raise MalformedZCertificate("not a ZCertificate")
    try:
        tables = integer_tables(cert.model)
    except (ValueError, TypeError) as exc:
        raise MalformedZCertificate(f"the instance is not a well-formed PairModel ({exc})") from None
    return normalised(cert, tables), tables


def normalised(cert: ZCertificate, tables=None) -> ZCertificate:
    """The certificate as the checker reads it: a copy made of Python integers, rationals of Python
    integers, lists and dicts only, whose nodes form a tree at most `MAX_BRANCH_DEPTH` branch
    nodes deep (see the module docstring).  Raises :class:`MalformedZCertificate` otherwise.
    The pass is iterative and visits every node once.  `tables` is the `model.integer_tables`
    snapshot of the instance when the caller already holds one."""
    if tables is None:
        return snapshot(cert)[0]
    if not isinstance(cert, ZCertificate):
        raise MalformedZCertificate("not a ZCertificate")
    _, unary, pair = tables
    n, sizes = len(unary), [len(u) for u in unary]
    beta = _rational(cert.beta, "beta")
    if beta < 0:
        raise MalformedZCertificate("beta must be a nonnegative Fraction")
    if not isinstance(cert.domains, list) or len(cert.domains) != n:
        raise MalformedZCertificate(f"domains must list {n} sites")
    domains = []
    for i, d in enumerate(cert.domains):
        message = f"domain of site {i} must be a non-empty duplicate-free list of its states"
        states = _int_list(d, message)
        if not states or len(set(states)) != len(states) or any(not 0 <= a < sizes[i] for a in states):
            raise MalformedZCertificate(message)
        domains.append(states)
    keep = cert.keep
    if keep is not None:
        keep = _index(keep, "keep")
        if not 0 <= keep < n:
            raise MalformedZCertificate("keep must be a site or None")
    expected = sorted(i for i in range(n) if i != keep)
    if not isinstance(cert.claim, dict) or set(cert.claim) - {"ln_z_lo", "ln_z_hi"}:
        raise MalformedZCertificate("claim may hold ln_z_lo and ln_z_hi as Fractions")
    claim = {name: _rational(value, f"claim {name}") for name, value in cert.claim.items()}

    def copy_steps(steps):
        if not isinstance(steps, list):
            raise MalformedZCertificate("steps must be a list")
        out = []
        for step in steps:
            if not isinstance(step, dict):
                raise MalformedZCertificate("a step must be an object")
            op = step.get("op")
            if op == "prune":
                if set(step) - {"op", "site", "remove", "dominator"}:
                    raise MalformedZCertificate("prune: unknown field")
                i = _index(step.get("site"), "prune: site")
                if not 0 <= i < n:
                    raise MalformedZCertificate("prune: site out of range")
                new = {"op": "prune", "site": i}
                for name in ("remove", "dominator"):
                    a = _index(step.get(name), f"prune: {name}")
                    if not 0 <= a < sizes[i]:
                        raise MalformedZCertificate(f"prune: {name} out of range")
                    new[name] = a
            elif op == "relax":
                if set(step) - {"op", "pair", "f", "g"}:
                    raise MalformedZCertificate("relax: unknown field")
                message = "relax: pair must be a listed pair [i, j] with i < j"
                ij = _int_list(step.get("pair"), message)
                if len(ij) != 2 or (ij[0], ij[1]) not in pair:
                    raise MalformedZCertificate(message)
                new = {"op": "relax", "pair": ij}
                for name, site in (("f", ij[0]), ("g", ij[1])):
                    message = f"relax: {name} must list one integer per state of site {site}"
                    new[name] = _int_list(step.get(name), message)
                    if len(new[name]) != sizes[site]:
                        raise MalformedZCertificate(message)
            else:
                raise MalformedZCertificate(f"unknown step {op!r}")
            out.append(new)
        return out

    holder = {}
    seen = set()                                        # identities of the nodes met so far
    stack = [(cert.root_node(), holder, "root", 0)]     # (node, parent, slot, branch nodes above it)
    while stack:
        node, parent, slot, depth = stack.pop()
        if not isinstance(node, dict) or set(node) - {"steps", "order", "branch", "children"}:
            raise MalformedZCertificate("a node is an object with 'steps' and either 'order' or 'branch' and 'children'")
        if id(node) in seen:
            raise MalformedZCertificate("a node occurs twice: the certificate is not a tree")
        seen.add(id(node))
        steps = copy_steps(node.get("steps"))
        if node.get("branch") is None:
            if "children" in node and node["children"] is not None:
                raise MalformedZCertificate("children without a branch site")
            message = "order must list every site other than `keep` exactly once"
            order = _int_list(node.get("order"), message)
            if sorted(order) != expected:
                raise MalformedZCertificate(message)
            parent[slot] = {"steps": steps, "order": order}
        else:
            if depth >= MAX_BRANCH_DEPTH:
                raise MalformedZCertificate(f"branch nodes nested more than {MAX_BRANCH_DEPTH} deep")
            i = _index(node["branch"], "branch")
            if not 0 <= i < n or i == keep:
                raise MalformedZCertificate("branch: a site other than the kept one")
            if node.get("order"):
                raise MalformedZCertificate("a branch node has no elimination order")
            children = node.get("children")
            if not isinstance(children, dict):
                raise MalformedZCertificate("branch: children must be a mapping from states to nodes")
            kids = {}
            for a, child in children.items():
                a = _index(a, "branch: child state")
                if not 0 <= a < sizes[i] or a in kids:
                    raise MalformedZCertificate("branch: child state out of range")
                kids[a] = None                          # keeps the order of the children
                stack.append((child, kids, a, depth + 1))
            parent[slot] = {"steps": steps, "branch": i, "children": kids}
    root = holder["root"]
    return ZCertificate(model=cert.model, beta=beta, domains=domains, steps=root["steps"], order=root.get("order", []),
                        keep=keep, claim=claim, meta=cert.meta, branch=root.get("branch"), children=root.get("children"))


def validate_structure(cert: ZCertificate) -> None:
    """Raise :class:`MalformedZCertificate` unless `cert` is a well-formed certificate of its instance
    (exactly the conditions of `normalised`, whose copy the checker computes with)."""
    normalised(cert)


# ---------------------------------------------------------------------------------------------
# File format `structbio-zcert/1` (detached: the instance is named by its checksum)
# ---------------------------------------------------------------------------------------------

def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _fraction_from_text(text, what: str) -> Fraction:
    """The rational written 'p/q' in canonical form: ASCII digits, at most one leading '-', no
    leading zeros, `q > 0`, lowest terms, at most `MAX_INT_DIGITS` digits each."""
    parts = text.split("/") if isinstance(text, str) else []
    if len(parts) != 2 or not parts[0]:
        raise MalformedZCertificate(f"{what}: expected a rational written 'p/q' with q > 0")
    negative = parts[0][0] == "-"
    try:
        p = _natural(parts[0][1:] if negative else parts[0], what)
        q = _natural(parts[1], what)
    except MalformedCertificate as exc:
        raise MalformedZCertificate(f"{what}: expected a rational written 'p/q' in canonical form ({exc})") from None
    if q == 0 or (negative and p == 0):
        raise MalformedZCertificate(f"{what}: expected a rational written 'p/q' with q > 0")
    value = Fraction(-p if negative else p, q)
    if _fraction_text(value) != text:
        raise MalformedZCertificate(f"{what}: the rational is not in lowest terms / canonical form")
    return value


def _node_to_json(root: dict) -> dict:
    """JSON object of a normalised node tree (children sorted by state), built without recursion."""
    holder = {}
    stack = [(root, holder, "root")]
    while stack:
        node, parent, slot = stack.pop()
        out = {"steps": node["steps"]}
        if node.get("branch") is None:
            out["order"] = node["order"]
        else:
            out["branch"] = node["branch"]
            out["children"] = kids = {}
            for a, child in sorted(node["children"].items()):
                kids[str(a)] = None
                stack.append((child, kids, str(a)))
        parent[slot] = out
    return holder["root"]


def _steps_from_json(steps) -> list:
    out = []
    for step in steps:
        if not isinstance(step, dict):
            raise MalformedZCertificate("a step must be an object")
        if step.get("op") == "prune":
            _only(step, ("op", "site", "remove", "dominator"), "prune step")
            out.append({"op": "prune", "site": _strict_int(step.get("site"), "site"),
                        "remove": _strict_int(step.get("remove"), "remove"),
                        "dominator": _strict_int(step.get("dominator"), "dominator")})
        elif step.get("op") == "relax":
            _only(step, ("op", "pair", "f", "g"), "relax step")
            pair, f, g = step.get("pair"), step.get("f"), step.get("g")
            if not all(isinstance(v, list) for v in (pair, f, g)):
                raise MalformedZCertificate("relax: pair, f and g must be lists")
            out.append({"op": "relax", "pair": [_strict_int(v, "pair") for v in pair],
                        "f": [_strict_int(v, "f") for v in f], "g": [_strict_int(v, "g") for v in g]})
        else:
            raise MalformedZCertificate(f"unknown step {step.get('op')!r}")
    return out


def _node_from_json(doc) -> dict:
    """The node tree of a file, read strictly and without recursion: a node holds ``steps`` and
    either ``order`` or ``branch`` with ``children`` — nothing else, and not both."""
    holder = {}
    stack = [(doc, holder, "root", 0)]                  # (JSON value, parent, slot, branch nodes above it)
    while stack:
        doc, parent, slot, depth = stack.pop()
        if not isinstance(doc, dict) or not isinstance(doc.get("steps"), list):
            raise MalformedZCertificate("a node needs a list of steps")
        steps = _steps_from_json(doc["steps"])
        if "branch" in doc:
            _only(doc, ("steps", "branch", "children"), "branch node")
            if depth >= MAX_BRANCH_DEPTH:
                raise MalformedZCertificate(f"branch nodes nested more than {MAX_BRANCH_DEPTH} deep")
            children = doc.get("children")
            if not isinstance(children, dict):
                raise MalformedZCertificate("branch: children must be an object")
            kids = {}
            parent[slot] = {"steps": steps, "branch": _strict_int(doc["branch"], "branch"), "children": kids}
            for a, child in children.items():
                state = _natural(a, "branch: child key")
                kids[state] = None                      # keeps the order of the children
                stack.append((child, kids, state, depth + 1))
        else:
            _only(doc, ("steps", "order"), "node")
            order = doc.get("order")
            if not isinstance(order, list):
                raise MalformedZCertificate("a leaf node needs an elimination order")
            parent[slot] = {"steps": steps, "order": [_strict_int(v, "order") for v in order]}
    return holder["root"]


def dumps(cert: ZCertificate) -> str:
    """Serialise a Z certificate (detached: the instance is named by `mincert.model_sha256`).
    The certificate is normalised first (:class:`MalformedZCertificate` if it is not well formed)."""
    cert, tables = snapshot(cert)
    doc = {"format": "structbio-zcert/1", "model_sha256": tables_sha256(*tables),
           "beta": _fraction_text(cert.beta), "domains": cert.domains, "keep": cert.keep,
           "claim": {k: _fraction_text(v) for k, v in sorted(cert.claim.items())},
           "root": _node_to_json(cert.root_node()),
           "meta": json.dumps(cert.meta, sort_keys=True)}
    return json.dumps(doc, separators=(",", ":"))


def loads(text: str, model: PairModel) -> ZCertificate:
    """Parse a Z certificate strictly (duplicate keys, unknown fields, non-integer numbers,
    non-canonical rationals and wrong shapes are errors) for the instance `model`, whose checksum
    must be the recorded one.  Raises :class:`MalformedZCertificate` and nothing else, whatever
    the text and whatever is passed as `model`."""
    try:
        return _loads(text, model)
    except MalformedZCertificate:
        raise
    except MalformedCertificate as exc:
        raise MalformedZCertificate(str(exc)) from exc
    except Exception as exc:  # noqa: BLE001  (one exception type for whoever turns it into a rejection)
        raise MalformedZCertificate(f"not a readable certificate ({type(exc).__name__})") from exc


def _loads(text, model) -> ZCertificate:
    doc = _strict_load(text)
    if not isinstance(doc, dict) or doc.get("format") != "structbio-zcert/1":
        raise MalformedZCertificate("unknown format")
    _only(doc, ("format", "model_sha256", "beta", "domains", "keep", "claim", "root", "meta"), "certificate file")
    if not isinstance(model, PairModel):
        raise MalformedZCertificate("the instance supplied is not a PairModel")
    tables = integer_tables(model)
    if tables_sha256(*tables) != doc.get("model_sha256"):
        raise MalformedZCertificate("the instance does not have the checksum recorded in the certificate")
    domains, claim = doc.get("domains"), doc.get("claim")
    if not isinstance(domains, list) or not all(isinstance(d, list) for d in domains) or not isinstance(claim, dict):
        raise MalformedZCertificate("need 'domains' (list of lists) and 'claim' (object)")
    root = _node_from_json(doc.get("root"))
    keep = doc.get("keep")
    cert = ZCertificate(model=model, beta=_fraction_from_text(doc.get("beta"), "beta"),
                        domains=[[_strict_int(a, "domain") for a in d] for d in domains],
                        steps=root["steps"], order=root.get("order", []),
                        keep=None if keep is None else _strict_int(keep, "keep"),
                        claim={k: _fraction_from_text(v, k) for k, v in claim.items()},
                        meta=_meta_from_text(doc.get("meta")),
                        branch=root.get("branch"), children=root.get("children"))
    validate_structure(cert)
    return cert
