"""Certified stability of a global minimum (capability C1b).

For a configuration `x*` and a site `i`, the *flip gap* is

    gap_i = min { E(x) : x_i != x*_i } - E(x*),

the least energy it costs for site `i` to leave its state.  It is certified by one `min`
certificate on the box in which the state `x*_i` is removed from the domain of site `i` and
every other site keeps its full domain (kernel semantics as in `mincert`: accepted implies
`E(x) >= bound` on that box, `verify_sound` [V]), together with a witness of that box whose
energy equals the bound.  Because the boxes `{x_i != x*_i}` cover every configuration other
than `x*`, the smallest flip gap is the gap to the second-best configuration.

What the numbers mean.  They are properties of the published integer tables.  A positive
`min_i gap_i` certifies that `x*` is the *unique* minimiser, and any perturbation of the tables
that changes the energy of every configuration by less than half that gap leaves `x*` optimal —
in particular the rounding of float tables to the integer grid, whose effect on a configuration's
energy is at most `(n + number of pairs) * 2**-(scale_bits + 1)`.  A small gap at a site says the
model does not determine that site's state; it says nothing about the protein.

Producer code (untrusted): each certificate is checked like any other.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .gmec import certify_gmec
from .mincert import MinCertificate
from .model import PairModel

__all__ = ["FlipGap", "certify_flip_gaps", "second_best_gap", "rounding_margin"]


@dataclass
class FlipGap:
    site: int
    gap: Fraction                 # certified: E(x) - E(x*) >= gap whenever x_site != x*_site, with equality attained
    alternative: tuple            # a configuration attaining the gap
    certificate: MinCertificate   # zero-gap certificate on the box without the state x*_site


def certify_flip_gaps(model: PairModel, x_star, sites=None, **producer_options) -> list:
    """One zero-gap certificate per site with more than one state (or per site of `sites`)."""
    x_star = tuple(int(a) for a in x_star)
    e_star = model.energy(x_star)
    out = []
    for i in (range(model.n) if sites is None else sites):
        if model.sizes[i] <= 1:
            continue
        domains = model.full_domains()
        domains[i] = [a for a in domains[i] if a != x_star[i]]
        cert = certify_gmec(model, eps=Fraction(0), domains=domains, **producer_options)
        out.append(FlipGap(site=i, gap=cert.lower_bound_fraction() - e_star, alternative=cert.witness,
                           certificate=cert))
    return out


def second_best_gap(gaps) -> Fraction:
    """Energy of the best configuration other than `x*`, minus `E(x*)` (needs the gaps of *all* sites
    that have more than one state)."""
    if not gaps:
        raise ValueError("no site has an alternative state")
    return min(g.gap for g in gaps)


def rounding_margin(model: PairModel) -> Fraction:
    """Largest possible change of a configuration's energy when float tables are rounded to the
    grid `2**-scale_bits`: half a grid step for each of the `n + number of pairs` table entries."""
    return Fraction(model.n + len(model.pair), 2 ** (model.scale_bits + 1))
