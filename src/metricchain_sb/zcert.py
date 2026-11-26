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
    if not isinstance(cert.order, list) or not all(_is_int(v) for v in cert.order) or sorted(cert.order) != expected:
        raise MalformedZCertificate("order must list every site other than `keep` exactly once")
    if not isinstance(cert.steps, list):
        raise MalformedZCertificate("steps must be a list")
    for step in cert.steps:
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
    if not isinstance(cert.claim, dict) or set(cert.claim) - {"ln_z_lo", "ln_z_hi"} \
            or not all(isinstance(v, Fraction) for v in cert.claim.values()):
        raise MalformedZCertificate("claim may hold ln_z_lo and ln_z_hi as Fractions")
