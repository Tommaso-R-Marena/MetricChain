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

A claim `{"ln_z_lo": q, "ln_z_hi": q}` is accepted iff it contains the interval the checker
computes.  Units: `f`, `g` are integers in table units.

Status: the checker implementation is tested against enumeration (`tests/structbio/test_zcert.py`);
the rule semantics are [V] for chains and [P] in general — a result accepted here is label
**[CP]**, not [CK], until the rules are machine-checked.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

from .model import PairModel

__all__ = ["ZCertificate", "MalformedZCertificate", "validate_structure"]


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


def _is_int(v) -> bool:
    return isinstance(v, (int, np.integer)) and not isinstance(v, bool)


def validate_structure(cert: ZCertificate) -> None:
    model = cert.model
    n, sizes = model.n, model.sizes
    if not isinstance(cert.beta, Fraction) or cert.beta < 0:
        raise MalformedZCertificate("beta must be a nonnegative Fraction")
    if not isinstance(cert.domains, list) or len(cert.domains) != n:
        raise MalformedZCertificate(f"domains must list {n} sites")
    for i, d in enumerate(cert.domains):
        if not isinstance(d, list) or not d or len(set(d)) != len(d) \
                or any((not _is_int(a)) or not 0 <= a < sizes[i] for a in d):
            raise MalformedZCertificate(f"domain of site {i} must be a non-empty duplicate-free list of its states")
    if cert.keep is not None and ((not _is_int(cert.keep)) or not 0 <= cert.keep < n):
        raise MalformedZCertificate("keep must be a site or None")
    expected = sorted(i for i in range(n) if i != cert.keep)

    def check_steps(steps):
        if not isinstance(steps, list):
            raise MalformedZCertificate("steps must be a list")
        for step in steps:
            if not isinstance(step, dict):
                raise MalformedZCertificate("a step must be an object")
            op = step.get("op")
            if op == "prune":
                if set(step) - {"op", "site", "remove", "dominator"}:
                    raise MalformedZCertificate("prune: unknown field")
                i = step.get("site")
                if (not _is_int(i)) or not 0 <= i < n:
                    raise MalformedZCertificate("prune: site out of range")
                for name in ("remove", "dominator"):
                    a = step.get(name)
                    if (not _is_int(a)) or not 0 <= a < sizes[i]:
                        raise MalformedZCertificate(f"prune: {name} out of range")
            elif op == "relax":
                if set(step) - {"op", "pair", "f", "g"}:
                    raise MalformedZCertificate("relax: unknown field")
                pair = step.get("pair")
                if (not isinstance(pair, list)) or len(pair) != 2 or not all(_is_int(v) for v in pair) \
                        or (pair[0], pair[1]) not in model.pair:
                    raise MalformedZCertificate("relax: pair must be a listed pair [i, j] with i < j")
                for name, site in (("f", pair[0]), ("g", pair[1])):
                    vec = step.get(name)
                    if (not isinstance(vec, list)) or len(vec) != sizes[site] or not all(_is_int(v) for v in vec):
                        raise MalformedZCertificate(f"relax: {name} must list one integer per state of site {site}")
            else:
                raise MalformedZCertificate(f"unknown step {op!r}")

    stack = [cert.root_node()]
    while stack:
        node = stack.pop()
        if not isinstance(node, dict) or set(node) - {"steps", "order", "branch", "children"}:
            raise MalformedZCertificate("a node is an object with 'steps' and either 'order' or 'branch' and 'children'")
        check_steps(node.get("steps"))
        if node.get("branch") is None:
            order = node.get("order")
            if "children" in node and node["children"] is not None:
                raise MalformedZCertificate("children without a branch site")
            if not isinstance(order, list) or not all(_is_int(v) for v in order) or sorted(order) != expected:
                raise MalformedZCertificate("order must list every site other than `keep` exactly once")
        else:
            i = node["branch"]
            if (not _is_int(i)) or not 0 <= i < n or i == cert.keep:
                raise MalformedZCertificate("branch: a site other than the kept one")
            if node.get("order"):
                raise MalformedZCertificate("a branch node has no elimination order")
            children = node.get("children")
            if not isinstance(children, dict):
                raise MalformedZCertificate("branch: children must be a mapping from states to nodes")
            for a, child in children.items():
                if (not _is_int(a)) or not 0 <= a < sizes[i]:
                    raise MalformedZCertificate("branch: child state out of range")
                stack.append(child)
    if not isinstance(cert.claim, dict) or set(cert.claim) - {"ln_z_lo", "ln_z_hi"} \
            or not all(isinstance(v, Fraction) for v in cert.claim.values()):
        raise MalformedZCertificate("claim may hold ln_z_lo and ln_z_hi as Fractions")


# ---------------------------------------------------------------------------------------------
# File format `structbio-zcert/1` (detached: the instance is named by its checksum)
# ---------------------------------------------------------------------------------------------

def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _fraction_from_text(text, what: str) -> Fraction:
    parts = text.split("/") if isinstance(text, str) else []
    if len(parts) != 2 or not all(t.lstrip("-").isdigit() for t in parts) or int(parts[1]) <= 0:
        raise MalformedZCertificate(f"{what}: expected a rational written 'p/q' with q > 0")
    value = Fraction(int(parts[0]), int(parts[1]))
    if _fraction_text(value) != text:
        raise MalformedZCertificate(f"{what}: the rational is not in lowest terms / canonical form")
    return value


def _node_to_json(node: dict) -> dict:
    out = {"steps": [dict(step) for step in node["steps"]]}
    if node.get("branch") is None:
        out["order"] = [int(v) for v in node["order"]]
    else:
        out["branch"] = int(node["branch"])
        out["children"] = {str(int(a)): _node_to_json(child) for a, child in sorted(node["children"].items())}
    return out


def _node_from_json(doc) -> dict:
    from .mincert import MalformedCertificate, _strict_int      # shared strict helpers
    if not isinstance(doc, dict) or not isinstance(doc.get("steps"), list):
        raise MalformedZCertificate("a node needs a list of steps")
    try:
        steps = []
        for step in doc["steps"]:
            if not isinstance(step, dict):
                raise MalformedZCertificate("a step must be an object")
            if step.get("op") == "prune":
                steps.append({"op": "prune", "site": _strict_int(step.get("site"), "site"),
                              "remove": _strict_int(step.get("remove"), "remove"),
                              "dominator": _strict_int(step.get("dominator"), "dominator")})
            elif step.get("op") == "relax":
                pair, f, g = step.get("pair"), step.get("f"), step.get("g")
                if not all(isinstance(v, list) for v in (pair, f, g)):
                    raise MalformedZCertificate("relax: pair, f and g must be lists")
                steps.append({"op": "relax", "pair": [_strict_int(v, "pair") for v in pair],
                              "f": [_strict_int(v, "f") for v in f], "g": [_strict_int(v, "g") for v in g]})
            else:
                raise MalformedZCertificate(f"unknown step {step.get('op')!r}")
        if "branch" in doc:
            children = doc.get("children")
            if not isinstance(children, dict):
                raise MalformedZCertificate("branch: children must be an object")
            kids = {}
            for a, child in children.items():
                if not (isinstance(a, str) and a.isdigit() and str(int(a)) == a):
                    raise MalformedZCertificate(f"branch: child key {a!r} is not a canonical natural number")
                kids[int(a)] = _node_from_json(child)
            return {"steps": steps, "branch": _strict_int(doc["branch"], "branch"), "children": kids}
        order = doc.get("order")
        if not isinstance(order, list):
            raise MalformedZCertificate("a leaf node needs an elimination order")
        return {"steps": steps, "order": [_strict_int(v, "order") for v in order]}
    except MalformedCertificate as exc:
        raise MalformedZCertificate(str(exc)) from exc


def dumps(cert: ZCertificate) -> str:
    """Serialise a Z certificate (detached: the instance is named by `mincert.model_sha256`)."""
    import json
    from .mincert import model_sha256
    doc = {"format": "structbio-zcert/1", "model_sha256": model_sha256(cert.model),
           "beta": _fraction_text(cert.beta), "domains": [[int(a) for a in d] for d in cert.domains],
           "keep": None if cert.keep is None else int(cert.keep),
           "claim": {k: _fraction_text(v) for k, v in sorted(cert.claim.items())},
           "root": _node_to_json(cert.root_node()),
           "meta": json.dumps(cert.meta, sort_keys=True)}
    return json.dumps(doc, separators=(",", ":"))


def loads(text: str, model: PairModel) -> ZCertificate:
    """Parse a Z certificate strictly (duplicate keys, non-integer numbers, non-canonical rationals
    and wrong shapes are errors) for the instance `model`, whose checksum must be the recorded one."""
    from .mincert import MalformedCertificate, _meta_from_text, _strict_int, _strict_load, model_sha256
    try:
        doc = _strict_load(text)
        if not isinstance(doc, dict) or doc.get("format") != "structbio-zcert/1":
            raise MalformedZCertificate("unknown format")
        if set(doc) - {"format", "model_sha256", "beta", "domains", "keep", "claim", "root", "meta"}:
            raise MalformedZCertificate("unknown field")
        if model_sha256(model) != doc.get("model_sha256"):
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
    except MalformedCertificate as exc:
        raise MalformedZCertificate(str(exc)) from exc
    validate_structure(cert)
    return cert
