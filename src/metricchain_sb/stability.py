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

Two constructions proposed by the science division (SCI-REV-0026), each one more certified
minimisation of the same kind — no new kernel rule:

*Leaving a class of states* (`certify_exclusion_gaps`).  A flip between the deposited
conformation and a library state of the same rotamer well is not a change of conformation.
With `exclude[i]` = every state of the well of `x*_i`, the gap is the least energy at which
site `i` is in another well.

*Optimality in every table within a stated error* (`shifted_model`,
`certify_necessary_optimality`).  Let `b >= 0` be an error bound per table entry and call a
*scenario* any table whose every entry lies within `b` of the model's.  Let the shifted model
have the entries `x*` uses raised by `b` and every other entry lowered by `b`.  Then
`x*` minimises every scenario  <=>  `x*` minimises the shifted model: for a competitor `x` the
difference `E'(x) - E'(x*)` is linear in the scenario and is least where the entries only `x*`
uses are raised and those only `x` uses are lowered, and the shifted model takes exactly that
value (entries both use cancel).  Flip or exclusion gaps of the *shifted* model that are
positive certify more: every minimiser of every scenario has site `i` in its state (its
well) — a sufficient condition, not a necessary one (the comparison is against `x*` alone).
The criterion is the classical worst-case-scenario test of optimisation with interval data;
nothing new is claimed.

Producer code (untrusted): each certificate is checked like any other.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import numpy as np

from .gmec import certify_gmec
from .mincert import MinCertificate
from .model import PairModel

__all__ = ["FlipGap", "certify_flip_gaps", "certify_exclusion_gaps", "second_best_gap", "rounding_margin",
           "shifted_model", "NecessaryOptimality", "certify_necessary_optimality"]


@dataclass
class FlipGap:
    site: int
    gap: Fraction | None          # certified: E(x) - E(x*) >= gap whenever x_site is outside the excluded
                                  # states, with equality attained; None if no state is left to go to
    alternative: tuple | None     # a configuration attaining the gap
    certificate: MinCertificate | None   # zero-gap certificate on the box without the excluded states


def certify_exclusion_gaps(model: PairModel, x_star, exclude, **producer_options) -> list:
    """For every site `i` of `exclude` (a mapping site -> states), the certified minimum over the
    configurations whose state at `i` is none of `exclude[i]`, minus `E(x*)`.  A site all of whose
    states are excluded is reported with `gap=None`."""
    x_star = tuple(int(a) for a in x_star)
    e_star = model.energy(x_star)
    out = []
    for i in sorted(exclude):
        banned = {int(a) for a in exclude[i]}
        domains = model.full_domains()
        domains[i] = [a for a in domains[i] if a not in banned]
        if not domains[i]:
            out.append(FlipGap(site=i, gap=None, alternative=None, certificate=None))
            continue
        cert = certify_gmec(model, eps=Fraction(0), domains=domains, **producer_options)
        out.append(FlipGap(site=i, gap=cert.lower_bound_fraction() - e_star, alternative=cert.witness,
                           certificate=cert))
    return out


def certify_flip_gaps(model: PairModel, x_star, sites=None, **producer_options) -> list:
    """One zero-gap certificate per site with more than one state (or per site of `sites`)."""
    x_star = tuple(int(a) for a in x_star)
    chosen = [i for i in (range(model.n) if sites is None else sites) if model.sizes[i] > 1]
    return certify_exclusion_gaps(model, x_star, {i: {x_star[i]} for i in chosen}, **producer_options)


def _error_tables(model: PairModel, b):
    """Per-entry error bounds as integer arrays of the model's shapes (table units)."""
    if isinstance(b, tuple):
        b_unary = [np.asarray(v, dtype=np.int64) for v in b[0]]
        b_pair = {key: np.asarray(b[1][key], dtype=np.int64) for key in model.pair}
    else:
        b_unary = [np.full(k, int(b), dtype=np.int64) for k in model.sizes]
        b_pair = {key: np.full(np.shape(t), int(b), dtype=np.int64) for key, t in model.pair.items()}
    if [len(v) for v in b_unary] != list(model.sizes) or any(
            np.shape(b_pair[key]) != np.shape(t) for key, t in model.pair.items()):
        raise ValueError("error bounds do not have the shapes of the model's tables")
    if any((v < 0).any() for v in b_unary) or any((t < 0).any() for t in b_pair.values()):
        raise ValueError("error bounds must be nonnegative")
    return b_unary, b_pair


def _moved(model: PairModel, x, b_unary, b_pair, sign_used: int, sign_other: int, only=None) -> PairModel:
    """The model with entries used by `x` moved by `sign_used * b` and the others by `sign_other * b`;
    with `only`, a set of entries (as produced by `_entries`), every entry outside it is left alone."""
    unary = []
    for i, u in enumerate(model.unary):
        new = np.asarray(u, dtype=np.int64).copy()
        for a in range(len(new)):
            if only is None or ("u", i, a) in only:
                new[a] += (sign_used if a == x[i] else sign_other) * int(b_unary[i][a])
        unary.append(new)
    pair = {}
    for (i, j), t in model.pair.items():
        new = np.asarray(t, dtype=np.int64).copy()
        if only is None:
            new -= -sign_other * b_pair[(i, j)]
            new[x[i], x[j]] += (sign_used - sign_other) * int(b_pair[(i, j)][x[i], x[j]])
        else:
            for (kind, *key) in only:
                if kind == "p" and (key[0], key[1]) == (i, j):
                    a, c = key[2], key[3]
                    new[a, c] += (sign_used if (a, c) == (x[i], x[j]) else sign_other) * int(b_pair[(i, j)][a, c])
        pair[(i, j)] = new
    return PairModel(unary, pair, scale_bits=model.scale_bits)


def _entries(model: PairModel, x) -> set:
    return {("u", i, a) for i, a in enumerate(x)} | {("p", i, j, x[i], x[j]) for (i, j) in model.pair}


def shifted_model(model: PairModel, x_star, b) -> PairModel:
    """The model with every entry `x*` uses raised by its error bound and every other entry lowered
    by its error bound.  `b`: one nonnegative integer (table units, all entries), or a pair
    `(b_unary, b_pair)` of integer tables of the model's shapes."""
    x_star = tuple(int(a) for a in x_star)
    b_unary, b_pair = _error_tables(model, b)
    return _moved(model, x_star, b_unary, b_pair, +1, -1)


@dataclass
class NecessaryOptimality:
    holds: bool                   # x* minimises every table within b of the model (entrywise)
    b: object                     # the error bound as given
    certificate: MinCertificate   # zero-gap certificate of the minimum of the shifted model
    counterexample: tuple | None  # if not `holds`: a configuration that beats x* in some scenario
    margin: Fraction              # min over x of (worst-scenario E'(x) - E'(x*)); 0 iff `holds`
    _model: PairModel = None
    _x_star: tuple = None

    def scenario(self) -> PairModel:
        """A table within `b` of the model in which `counterexample` has lower energy than `x*`."""
        if self.holds:
            raise ValueError("x* is optimal in every scenario; there is no counterexample")
        b_unary, b_pair = _error_tables(self._model, self.b)
        star, other = _entries(self._model, self._x_star), _entries(self._model, self.counterexample)
        raised = _moved(self._model, self._x_star, b_unary, b_pair, +1, 0, only=star - other)
        return _moved(raised, self.counterexample, b_unary, b_pair, -1, 0, only=other - star)


def certify_necessary_optimality(model: PairModel, x_star, b, **producer_options) -> NecessaryOptimality:
    """Decide, with a certificate, whether `x*` minimises every table within `b` of the model."""
    x_star = tuple(int(a) for a in x_star)
    shifted = shifted_model(model, x_star, b)
    cert = certify_gmec(shifted, eps=Fraction(0), witness=x_star, **producer_options)
    margin = cert.lower_bound_fraction() - shifted.energy(x_star)
    holds = margin == 0
    return NecessaryOptimality(holds=holds, b=b, certificate=cert,
                               counterexample=None if holds else tuple(cert.witness), margin=margin,
                               _model=model, _x_star=x_star)


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
