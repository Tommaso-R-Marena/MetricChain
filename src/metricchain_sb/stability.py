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

Producer code (untrusted) and its checkers.  `certify_exclusion_gaps`, `certify_flip_gaps` and
`certify_necessary_optimality` call the producer `gmec.certify_gmec`; a gap or a verdict is more
than a certificate that the min checker accepts — it is a statement about a *particular box* of
a *particular table* (review STRUCTBIO-REV-0001, finding 18: a producer that silently drops one
more state returns an accepted certificate and a gap that is too large).  Two checkers decide
that statement from the claim and the instance alone:

* `check_exclusion_gap(model, x_star, site, excluded, gap)` — the certificate is accepted with
  zero certified gap, is about `model` (instance checksum), its root box is exactly every state
  of every site with exactly the states `excluded` removed at `site`, the gap is the certified
  minimum minus `E(x*)`, and the alternative configuration lies in that box and has that energy;
* `check_necessary_optimality(model, x_star, b, verdict)` — the shifted table is derived again
  from its definition (independently of `shifted_model`), and the certificate is a zero-gap
  certificate of exactly that table (checksum) over every state of every site; `holds`,
  `margin` and the counterexample are what it implies.

Both return `(ok, reason)` and never raise.  The three `certify_*` functions apply the checker
to what they are about to return and raise `StabilityCheckFailed` instead of returning a claim
that fails it; a caller who receives claims from elsewhere applies the checkers itself.

Exact integers: configurations are validated (`PairModel.configuration`; a negative index is not
"the last state"), error bounds must be integers (nothing is truncated), and the shift is
computed in Python integers (no wrap at 2**63, finding 5).
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .gmec import certify_gmec
from .mincert import MinCertificate, model_sha256, tables_sha256
from .mincheck import check_min_certificate
from .model import PairModel, exact_int, integer_tables

__all__ = ["FlipGap", "certify_flip_gaps", "certify_exclusion_gaps", "second_best_gap", "rounding_margin",
           "shifted_model", "NecessaryOptimality", "certify_necessary_optimality", "check_exclusion_gap",
           "check_necessary_optimality", "StabilityCheckFailed"]


class StabilityCheckFailed(RuntimeError):
    """The producer returned a certificate that does not back the claim it was asked for (wrong box,
    wrong table, wrong numbers): no claim is returned.  Not an abstention — a defect of the producer."""


@dataclass
class FlipGap:
    site: int
    gap: Fraction | None          # certified: E(x) - E(x*) >= gap whenever x_site is outside the excluded
                                  # states, with equality attained; None if no state is left to go to
    alternative: tuple | None     # a configuration attaining the gap
    certificate: MinCertificate | None   # zero-gap certificate on the box without the excluded states


def _excluded_states(model: PairModel, exclude) -> dict:
    """`exclude` as a mapping site -> set of states, all of them existing (`ValueError` otherwise)."""
    out = {}
    sizes = model.sizes
    try:
        for site, states in exclude.items():
            i = exact_int(site, "a site")
            banned = {exact_int(a, "a state") for a in states}
            if not 0 <= i < model.n or any(not 0 <= a < sizes[i] for a in banned):
                raise ValueError("exclude must map sites of the model to states of those sites")
            out[i] = banned
    except (TypeError, AttributeError) as exc:
        raise ValueError(f"exclude must map sites to sets of states ({exc})") from None
    return out


def certify_exclusion_gaps(model: PairModel, x_star, exclude, **producer_options) -> list:
    """For every site `i` of `exclude` (a mapping site -> states), the certified minimum over the
    configurations whose state at `i` is none of `exclude[i]`, minus `E(x*)`.  A site all of whose
    states are excluded is reported with `gap=None`.  Every gap returned has passed
    `check_exclusion_gap`; `StabilityCheckFailed` if the producer's certificate does not."""
    x_star = model.configuration(x_star)
    exclude = _excluded_states(model, exclude)
    e_star = model.energy(x_star)
    out = []
    for i in sorted(exclude):
        banned = exclude[i]
        domains = model.full_domains()
        domains[i] = [a for a in domains[i] if a not in banned]
        if not domains[i]:
            out.append(FlipGap(site=i, gap=None, alternative=None, certificate=None))
            continue
        cert = certify_gmec(model, eps=Fraction(0), domains=domains, **producer_options)
        gap = FlipGap(site=i, gap=cert.lower_bound_fraction() - e_star, alternative=cert.witness, certificate=cert)
        ok, reason = check_exclusion_gap(model, x_star, i, banned, gap)
        if not ok:
            raise StabilityCheckFailed(f"site {i}: the producer's certificate does not back the gap ({reason})")
        out.append(gap)
    return out


def certify_flip_gaps(model: PairModel, x_star, sites=None, **producer_options) -> list:
    """One zero-gap certificate per site with more than one state (or per site of `sites`)."""
    x_star = model.configuration(x_star)
    chosen = [i for i in (range(model.n) if sites is None else sites) if model.sizes[i] > 1]
    return certify_exclusion_gaps(model, x_star, {i: {x_star[i]} for i in chosen}, **producer_options)


def check_exclusion_gap(model: PairModel, x_star, site, excluded, gap) -> tuple:
    """`(ok, reason)`: is `gap` the certified least energy, minus `E(x*)`, of the configurations of
    `model` whose state at `site` is none of `excluded`?  See the module docstring for what is
    verified.  Never raises: anything that cannot be read is a refusal with a reason."""
    try:
        return _check_exclusion_gap(model, x_star, site, excluded, gap)
    except Exception as exc:  # noqa: BLE001  (a refusal is always sound)
        return False, f"refused: {type(exc).__name__} while checking ({exc})"


def _check_exclusion_gap(model, x_star, site, excluded, gap) -> tuple:
    checksum = tables_sha256(*integer_tables(model))         # of the instance as it is now
    x_star = model.configuration(x_star)
    site = exact_int(site, "site")
    banned = _excluded_states(model, {site: excluded})[site]
    if not isinstance(gap, FlipGap):
        return False, "not a FlipGap"
    if gap.site != site:
        return False, f"the claim is about site {gap.site!r}, not about site {site}"
    box = model.full_domains()
    box[site] = [a for a in box[site] if a not in banned]
    if not box[site]:
        if gap.gap is None and gap.alternative is None and gap.certificate is None:
            return True, "ok"
        return False, "every state of the site is excluded: there is no configuration and no gap to certify"
    if gap.gap is None or gap.certificate is None:
        return False, "a state of the site is left, but no gap or no certificate is given"
    result = check_min_certificate(gap.certificate)
    if not result.accepted:
        return False, f"the certificate is rejected by the min checker ({result.reason})"
    if result.model_sha256 != checksum:
        return False, "the certificate is about another instance (instance checksum differs)"
    if result.certified_gap != 0:
        return False, "the certificate does not have zero certified gap: its bound is not shown to be attained"
    if [sorted(exact_int(a) for a in d) for d in gap.certificate.domains] != box:
        return False, ("the box of the certificate is not every state of every site with exactly the excluded "
                       "states removed at the site")
    if result.lower_bound - model.energy(x_star) != gap.gap:
        return False, "the gap is not the certified minimum of the box minus E(x*)"
    try:
        alternative = model.configuration(gap.alternative)
    except ValueError:
        return False, "the alternative is not a configuration of the instance"
    if alternative[site] in banned or model.energy(alternative) != result.lower_bound:
        return False, "the alternative does not lie in the box or does not have the certified minimum energy"
    return True, "ok"


def _error_tables(model: PairModel, b):
    """Per-entry error bounds as lists of Python integers of the model's shapes (table units):
    `(b_unary, b_pair)` with `b_pair[(i, j)]` a list of rows.  `ValueError` unless every bound
    is a nonnegative integer (a float bound is refused, not truncated)."""
    sizes = model.sizes
    try:
        if isinstance(b, tuple):
            if len(b) != 2 or set(b[1]) != set(model.pair):
                raise ValueError("error bounds: need (b_unary, b_pair) with one table per table of the model")
            b_unary = [[exact_int(v, "an error bound") for v in row] for row in b[0]]
            b_pair = {key: [[exact_int(v, "an error bound") for v in row] for row in b[1][key]] for key in model.pair}
        else:
            value = exact_int(b, "the error bound")
            b_unary = [[value] * k for k in sizes]
            b_pair = {(i, j): [[value] * sizes[j] for _ in range(sizes[i])] for (i, j) in model.pair}
    except TypeError as exc:
        raise ValueError(f"error bounds must be integers in table units ({exc})") from None
    if [len(v) for v in b_unary] != sizes or any(
            len(b_pair[(i, j)]) != sizes[i] or any(len(row) != sizes[j] for row in b_pair[(i, j)])
            for (i, j) in model.pair):
        raise ValueError("error bounds do not have the shapes of the model's tables")
    if any(v < 0 for row in b_unary for v in row) or any(v < 0 for t in b_pair.values() for row in t for v in row):
        raise ValueError("error bounds must be nonnegative")
    return b_unary, b_pair


def _moved(model: PairModel, x, b_unary, b_pair, sign_used: int, sign_other: int, only=None) -> PairModel:
    """The model with entries used by `x` moved by `sign_used * b` and the others by `sign_other * b`;
    with `only`, a set of entries (as produced by `_entries`), every entry outside it is left alone.
    Computed in Python integers: exact for entries and bounds of any size."""
    _, unary, pair = integer_tables(model)
    if only is None:                                         # every entry moves: by `sign_other`, the used ones by `sign_used`
        for i, row in enumerate(unary):
            unary[i] = [v + sign_other * e for v, e in zip(row, b_unary[i])]
            unary[i][x[i]] += (sign_used - sign_other) * b_unary[i][x[i]]
        for (i, j), table in pair.items():
            bound = b_pair[(i, j)]
            for a, row in enumerate(table):
                table[a] = [v + sign_other * e for v, e in zip(row, bound[a])]
            table[x[i]][x[j]] += (sign_used - sign_other) * bound[x[i]][x[j]]
    else:
        for entry in only:
            if entry[0] == "u":
                _, i, a = entry
                unary[i][a] += (sign_used if a == x[i] else sign_other) * b_unary[i][a]
            else:
                _, i, j, a, c = entry
                pair[(i, j)][a][c] += (sign_used if (a, c) == (x[i], x[j]) else sign_other) * b_pair[(i, j)][a][c]
    return PairModel(unary, pair, scale_bits=model.scale_bits)


def _entries(model: PairModel, x) -> set:
    return {("u", i, a) for i, a in enumerate(x)} | {("p", i, j, x[i], x[j]) for (i, j) in model.pair}


def shifted_model(model: PairModel, x_star, b) -> PairModel:
    """The model with every entry `x*` uses raised by its error bound and every other entry lowered
    by its error bound.  `b`: one nonnegative integer (table units, all entries), or a pair
    `(b_unary, b_pair)` of integer tables of the model's shapes.  `ValueError` for a configuration
    or a bound that is not one; the result is exact whatever the magnitudes (a table beyond the
    range the min checker supports is refused by `certify_necessary_optimality`)."""
    x_star = model.configuration(x_star)
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
    """Decide, with a certificate, whether `x*` minimises every table within `b` of the model.  The
    verdict returned has passed `check_necessary_optimality` (`StabilityCheckFailed` otherwise).
    `ValueError` when the shifted table is outside the integer range the producer and the min
    checker support."""
    x_star = model.configuration(x_star)
    shifted = shifted_model(model, x_star, b)
    cert = certify_gmec(shifted, eps=Fraction(0), witness=x_star, **producer_options)
    margin = cert.lower_bound_fraction() - shifted.energy(x_star)
    holds = margin == 0
    verdict = NecessaryOptimality(holds=holds, b=b, certificate=cert,
                                  counterexample=None if holds else tuple(cert.witness), margin=margin,
                                  _model=model, _x_star=x_star)
    ok, reason = check_necessary_optimality(model, x_star, b, verdict)
    if not ok:
        raise StabilityCheckFailed(f"the producer's certificate does not back the verdict ({reason})")
    return verdict


def check_necessary_optimality(model: PairModel, x_star, b, verdict) -> tuple:
    """`(ok, reason)`: is `verdict` the answer to "does `x*` minimise every table within `b` of
    `model`?", backed by its certificate?  The shifted table is derived here again.  See the
    module docstring for what is verified.  Never raises."""
    try:
        return _check_necessary_optimality(model, x_star, b, verdict)
    except Exception as exc:  # noqa: BLE001  (a refusal is always sound)
        return False, f"refused: {type(exc).__name__} while checking ({exc})"


def _check_necessary_optimality(model, x_star, b, verdict) -> tuple:
    x_star = model.configuration(x_star)
    # The shifted table, derived here from its definition (not taken from the verdict, and not
    # through `shifted_model`, which made the table the producer was given): every entry x* uses
    # is raised by its bound, every other entry is lowered by it.
    scale_bits, unary, pair = integer_tables(model)
    b_unary, b_pair = _error_tables(model, b)
    for i, row in enumerate(unary):
        unary[i] = [v + (e if a == x_star[i] else -e) for a, (v, e) in enumerate(zip(row, b_unary[i]))]
    for (i, j), table in pair.items():
        used = (x_star[i], x_star[j])
        pair[(i, j)] = [[v + (e if (a, c) == used else -e) for c, (v, e) in enumerate(zip(row, b_pair[(i, j)][a]))]
                        for a, row in enumerate(table)]

    def shifted_energy(x) -> Fraction:
        units = sum(unary[i][a] for i, a in enumerate(x)) + sum(t[x[i]][x[j]] for (i, j), t in pair.items())
        return Fraction(units, 2 ** scale_bits)

    if not isinstance(verdict, NecessaryOptimality):
        return False, "not a NecessaryOptimality verdict"
    result = check_min_certificate(verdict.certificate)
    if not result.accepted:
        return False, f"the certificate is rejected by the min checker ({result.reason})"
    if result.model_sha256 != tables_sha256(scale_bits, unary, pair):
        return False, "the certificate is not about the shifted table of this model, x* and b (instance checksum differs)"
    if not result.full_box:
        return False, "the certificate is not over the full box (every state of every site)"
    if result.certified_gap != 0:
        return False, "the certificate does not have zero certified gap: its bound is not shown to be attained"
    margin = result.lower_bound - shifted_energy(x_star)     # minimum of the shifted table minus E'(x*): never positive
    if verdict.margin != margin:
        return False, "the margin is not the certified minimum of the shifted table minus the shifted energy of x*"
    if not isinstance(verdict.holds, bool) or verdict.holds != (margin == 0):
        return False, "`holds` is not what the certificate implies (it holds iff the margin is zero)"
    if verdict.holds:
        if verdict.counterexample is not None:
            return False, "x* is optimal in every scenario, yet a counterexample is given"
    else:
        try:
            counterexample = model.configuration(verdict.counterexample)
        except ValueError:
            return False, "the counterexample is not a configuration of the instance"
        if shifted_energy(counterexample) != result.lower_bound:
            return False, "the counterexample does not attain the certified minimum of the shifted table"
    # the verdict's own record of its question (used by `scenario`) must be this question
    same_model = verdict._model is model or (isinstance(verdict._model, PairModel)
                                             and model_sha256(verdict._model) == model_sha256(model))
    if not same_model or verdict._x_star != x_star or _error_tables(model, verdict.b) != _error_tables(model, b):
        return False, "the verdict records another model, x* or b than the ones it is checked against"
    return True, "ok"


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
