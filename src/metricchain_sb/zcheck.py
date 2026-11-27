"""Checker for "Z" certificates (`metricchain_sb.zcert`): replays the steps in exact integer
arithmetic, encloses the Boltzmann factors of the working model with the certified exponential,
sums the sites out on interval tables, and returns the enclosure it has itself computed.

The checker contains no search and trusts no number of the certificate: margins of prune steps
and residual ranges of relax steps are recomputed here; a claim is accepted only if it contains
the interval computed here.  It imports the data classes and the normalisation of `zcert`, the
certified exponential of `expo` and the interval tables of `itables` — nothing from the
producer (`partition`).

Arithmetic.  Steps: Python integers and rationals of Python integers, exact — the checker
computes with the `zcert.normalised` copy of the certificate and with the `model.integer_tables`
snapshot of the instance, so no integer of the certificate or of the instance is a fixed-width
NumPy integer, and the neighbour structure is derived here from the pair tables (review
STRUCTBIO-REV-0001, findings 2 and 4).  Boltzmann factors: `expo.exp_bounds_me` (integer
arithmetic, outward rounded).  Elimination: tier ``exact`` (rationals; exact) or ``float``
(binary64 with outward rounding; assumptions F1–F3 of `itables`).  Logarithms of the final
bounds: `expo.log_bounds` (certified through the exponential).

Population intervals (certificates with ``keep = t``).  Every node returns a lower bound
`low_a` on the part of the true sum with `x_t = a` (its own relax factors included; a branch
node adds its children's bounds, whose sub-boxes are disjoint) and an upper bound `Z_hi` on the
true sum over its whole box (prune and relax factors included).  At the root, for every state
`a` that survives in some leaf,

    P(x_t = a)  >=  low_a / Z_hi                             (numerator from below, Z from above),
    P(x_t = a)  <=  1 - sum_{b != a} [lower bound of P(x_t = b)],

and a state of `t` that prune steps removed everywhere has population at most
`1 - sum_b [lower bound of P(x_t = b)]`.  Probabilities are those of the Boltzmann distribution
of the published tables *on the root box of the certificate*.

The range this checker evaluates (finding 6).  An exponential is returned as an exact rational
of about `1.44 * |argument|` bits, so every argument is bounded *before* it is exponentiated,
and what lies outside is rejected with a reason, not computed:

* ``scale_bits <= model.MAX_SCALE_BITS = 1024`` (checked before any power of two is formed);
* ``beta * |entry| <= MAX_EXPONENT = 2**16`` nats for every table entry of the instance (checked
  up front) and of the working model on the box (checked when its weight is needed).  The
  crambin certificates of SB-X-004 reach about 3,400 (entries clipped at 1000 kcal/mol,
  RT = 0.593 kcal/mol, plus the additive parts moved into the one-body tables by relax steps);
* relax step: ``beta * |r| <= MAX_EXPONENT`` for both ends of the residual range; node: the
  accumulated logarithmic factors `|A_lo|`, `|A_hi|` at most ``MAX_EXPONENT``;
* prune step with margin `m`: rejected when ``beta * m < MIN_PRUNE_EXPONENT = -9`` — legal
  mathematics (the rule holds for every `m`) but useless: the step would add more than
  `e**9` (about 8,100) nats to the upper bound, and without a floor a 300-byte certificate
  asks for the exponential of `e**(beta*|m|)`.  Margins between `-9/beta` and 0 are evaluated
  as before.  For ``beta * m > PRUNE_EXPONENT_CAP = 2**13`` the factor `exp(-beta*m)` is
  replaced by the larger `exp(-PRUNE_EXPONENT_CAP)` (below 1e-3557): sound because the
  exponential is monotone, and it keeps the denominators of `A_hi` short (the work of a node
  grows with the square of that length).  Below the cap nothing changes: the bounds of the
  crambin certificates (largest margin about 3,431 nats) are bit for bit what they were;
* ``exp_bits`` in ``EXP_BITS_RANGE``: 16..512 in the float tier (finding 3: the conversion of
  weights to doubles is now correct for every mantissa, and nothing is gained beyond the 53
  bits of a double), 16..1024 in the exact tier;
* branch nodes nested at most `zcert.MAX_BRANCH_DEPTH` deep (the evaluator recurses per level).

Inside these limits the work is polynomial in the size of the certificate and of the numbers
written in it.  The checker never raises: malformed input, an invalid step, an over-budget
table, an argument outside the range above or an arithmetic overflow is a rejection with a reason.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

from .expo import exp_bounds, exp_bounds_me, log_bounds
from .itables import ExactTables, FloatTables, TableTooLarge
from .model import MAX_SCALE_BITS, exact_int
from .zcert import MalformedZCertificate, ZCertificate, snapshot

__all__ = ["ZResult", "check_partition_certificate", "MAX_EXPONENT", "MIN_PRUNE_EXPONENT", "PRUNE_EXPONENT_CAP",
           "EXP_BITS_RANGE"]

MAX_EXPONENT = 2 ** 16              # largest |argument| of an exponential (nats)
MIN_PRUNE_EXPONENT = -9             # smallest beta * margin of a prune step
PRUNE_EXPONENT_CAP = 2 ** 13        # beta * margin above this is bounded by exp(-PRUNE_EXPONENT_CAP)
EXP_BITS_RANGE = {"exact": (16, 1024), "float": (16, 512)}


@dataclass
class ZResult:
    accepted: bool
    reason: str = ""
    ln_z_lo: Fraction | None = None
    ln_z_hi: Fraction | None = None
    slack_lo: Fraction | None = None      # A_lo: accumulated lower logarithmic factor of the steps (nats)
    slack_hi: Fraction | None = None      # A_hi
    full_box: bool | None = None
    keep: int | None = None
    populations: dict = field(default_factory=dict)    # state -> (lo, hi) for the final domain of `keep`
    removed_upper: Fraction | None = None              # upper bound on the population of any removed state of `keep`
    stats: dict = field(default_factory=dict)

    def population(self, state: int):
        if state in self.populations:
            return self.populations[state]
        return Fraction(0), self.removed_upper


def check_partition_certificate(cert: ZCertificate, arithmetic: str = "exact", max_entries: int | None = 5_000_000,
                                exp_bits: int = 64) -> ZResult:
    try:
        return _check(cert, arithmetic, max_entries, exp_bits)
    except MalformedZCertificate as exc:
        return ZResult(False, f"malformed certificate: {exc}")
    except TableTooLarge as exc:
        return ZResult(False, f"abstained: {exc}")
    except RecursionError:
        return ZResult(False, "rejected: nested too deeply for the interpreter's recursion limit")
    except (OverflowError, ArithmeticError) as exc:
        return ZResult(False, f"rejected: arithmetic failure ({exc})")
    except Exception as exc:  # noqa: BLE001  (a rejection is always sound)
        return ZResult(False, f"rejected: {type(exc).__name__} while checking")


class _Reject(Exception):
    """An invalid step or node: the certificate is rejected with this reason."""


def _check(cert: ZCertificate, arithmetic: str, max_entries, exp_bits: int) -> ZResult:
    # the certificate as Python integers and rationals forming a tree, and the instance as it is now
    cert, instance = snapshot(cert)
    if not isinstance(arithmetic, str) or arithmetic not in ("exact", "float"):
        return ZResult(False, "unknown arithmetic tier")
    low, high = EXP_BITS_RANGE[arithmetic]
    try:
        exp_bits = exact_int(exp_bits, "exp_bits")
    except TypeError:
        return ZResult(False, "exp_bits must be an integer")
    if not low <= exp_bits <= high:
        return ZResult(False, f"exp_bits = {exp_bits} is outside the range of the {arithmetic} tier ({low} to {high})")
    if max_entries is not None:
        try:
            max_entries = exact_int(max_entries, "max_entries")
        except TypeError:
            return ZResult(False, "max_entries must be an integer or None")
    scale_bits, unary, pair = instance
    if scale_bits > MAX_SCALE_BITS:
        return ZResult(False, f"scale_bits = {scale_bits} is outside the supported range (at most {MAX_SCALE_BITS})")
    tables = ExactTables() if arithmetic == "exact" else FloatTables()
    beta, keep = cert.beta, cert.keep
    n = len(unary)
    unit = Fraction(1, 2 ** scale_bits)
    largest = max((max(max(u), -min(u)) for u in unary), default=0)
    for rows in pair.values():
        largest = max(largest, max(map(max, rows)), -min(map(min, rows)))
    if beta * largest * unit > MAX_EXPONENT:
        return ZResult(False, f"beta times a table entry exceeds {MAX_EXPONENT}: outside the range this checker evaluates")
    stats = {"prune": 0, "relax": 0, "leaves": 0, "largest_table": 0}
    weight_cache = {}

    def weight_me(energy_int: int):
        """Certified enclosure of exp(-beta * energy), as mantissa/exponent pairs (cached)."""
        hit = weight_cache.get(energy_int)
        if hit is None:
            q = -beta * energy_int * unit
            if abs(q) > MAX_EXPONENT:
                raise _Reject(f"beta times an entry of the working model exceeds {MAX_EXPONENT}: "
                              f"outside the range this checker evaluates")
            hit = weight_cache[energy_int] = exp_bounds_me(q, exp_bits)
        return hit

    def evaluate(node, D, H, J, nbrs):
        """Enclosure `(z_lo, z_hi, lows)` of the sum of the working model over the working box, the
        factors of this node's own steps included; `lows[a]` bounds from below the part with
        `x_keep = a`.  Also returns this node's own logarithmic factors (for reporting)."""
        D = [list(d) for d in D]
        H = [list(h) for h in H]
        J = dict(J)                                   # tables are never modified, only removed
        nbrs = {i: set(v) for i, v in nbrs.items()}

        def pair_entry(i, j, a, b):
            return J[(i, j)][a][b] if i < j else J[(j, i)][b][a]

        a_lo = Fraction(0)
        a_hi = Fraction(0)
        for step in node["steps"]:
            if step["op"] == "prune":
                i, r, t = step["site"], step["remove"], step["dominator"]
                if r == t or r not in D[i] or t not in D[i]:
                    raise _Reject("prune step: dominator and removed state must be distinct states of the current domain")
                margin = H[i][r] - H[i][t]
                for j in nbrs[i]:
                    margin += min(pair_entry(i, j, r, s) - pair_entry(i, j, t, s) for s in D[j])
                q = beta * margin * unit                # beta * m in nats; rho = exp(-q)
                if q < MIN_PRUNE_EXPONENT:
                    raise _Reject(f"prune step: beta times the margin is below {MIN_PRUNE_EXPONENT} (the dominator is "
                                  f"far above the removed state on the box): outside the range this checker evaluates")
                if q > PRUNE_EXPONENT_CAP:
                    q = Fraction(PRUNE_EXPONENT_CAP)    # rho <= exp(-cap): the exponential is monotone
                a_hi += exp_bounds(-q, exp_bits)[1]                         # ln(1 + rho) <= rho <= its upper enclosure
                D[i].remove(r)
                stats["prune"] += 1
            else:
                i, j = step["pair"]
                if (i, j) not in J:
                    raise _Reject("relax step: the pair has already been relaxed")
                f, g = step["f"], step["g"]
                table = J.pop((i, j))
                residual = [table[a][b] - f[a] - g[b] for a in D[i] for b in D[j]]
                r_lo, r_hi = min(residual), max(residual)
                for a in range(len(H[i])):
                    H[i][a] += f[a]
                for b in range(len(H[j])):
                    H[j][b] += g[b]
                nbrs[i].discard(j)
                nbrs[j].discard(i)
                lo_term, hi_term = -beta * r_hi * unit, -beta * r_lo * unit
                if abs(lo_term) > MAX_EXPONENT or abs(hi_term) > MAX_EXPONENT:
                    raise _Reject(f"relax step: beta times the residual range exceeds {MAX_EXPONENT}: "
                                  f"outside the range this checker evaluates")
                a_lo += lo_term
                a_hi += hi_term
                stats["relax"] += 1
        if abs(a_lo) > MAX_EXPONENT or abs(a_hi) > MAX_EXPONENT:
            raise _Reject(f"the accumulated logarithmic factor of a node's steps exceeds {MAX_EXPONENT}: "
                          f"outside the range this checker evaluates")

        if node.get("branch") is not None:
            i = node["branch"]
            z_lo = z_hi = Fraction(0)
            lows = {}
            for a in D[i]:
                child = node["children"].get(a)
                if child is None:
                    raise _Reject(f"branch on site {i} has no child for state {a}")
                D2 = list(D)
                D2[i] = [a]
                c_lo, c_hi, c_lows, _, _ = evaluate(child, D2, H, J, nbrs)
                z_lo += c_lo
                z_hi += c_hi
                for state, value in c_lows.items():
                    lows[state] = lows.get(state, Fraction(0)) + value
        else:
            sizes = {i: len(D[i]) for i in range(n)}
            factors = []
            for i in range(n):
                me = [weight_me(H[i][a]) for a in D[i]]
                factors.append(tables.from_me_bounds((i,), [x[0] for x in me], [x[1] for x in me], (sizes[i],)))
            for (i, j), table in J.items():
                me = [weight_me(table[a][b]) for a in D[i] for b in D[j]]
                factors.append(tables.from_me_bounds((i, j), [x[0] for x in me], [x[1] for x in me],
                                                     (sizes[i], sizes[j])))

            def product(parts):
                scope = set().union(*[set(q.scope) for q in parts])
                entries = 1
                for site in scope:
                    entries *= sizes[site]
                stats["largest_table"] = max(stats["largest_table"], entries)
                acc = parts[0]
                for q in parts[1:]:
                    acc = tables.multiply(acc, q, sizes, max_entries)   # lives on the union of the two scopes
                return acc

            for v in node["order"]:
                bucket = [f for f in factors if v in f.scope]
                factors = [f for f in factors if v not in f.scope]
                factors.append(tables.sum_out(product(bucket), v))
            lo_list, hi_list = tables.bounds(product(factors))
            z_lo, z_hi = sum(lo_list, Fraction(0)), sum(hi_list, Fraction(0))
            lows = dict(zip(D[keep], lo_list)) if keep is not None else {}
            stats["leaves"] += 1

        f_lo = exp_bounds(a_lo, exp_bits)[0]            # |a_lo|, |a_hi| <= MAX_EXPONENT (checked above)
        f_hi = exp_bounds(a_hi, exp_bits)[1]
        return z_lo * f_lo, z_hi * f_hi, {a: v * f_lo for a, v in lows.items()}, a_lo, a_hi

    D0 = [list(d) for d in cert.domains]
    nbrs0 = {i: set() for i in range(n)}                # neighbours, derived here from the pair tables
    for (i, j) in pair:
        nbrs0[i].add(j)
        nbrs0[j].add(i)
    try:
        z_lo, z_hi, lows, a_lo, a_hi = evaluate(cert.root_node(), D0, unary, pair, nbrs0)
    except _Reject as exc:
        return ZResult(False, str(exc), stats=stats)

    full_box = all(sorted(d) == list(range(len(u))) for d, u in zip(cert.domains, unary))
    if z_lo <= 0:
        return ZResult(False, "abstained: the lower bound of the partition sum is not positive at this precision",
                       stats=stats)
    ln_lo = log_bounds(z_lo)[0]
    ln_hi = log_bounds(z_hi)[1]
    flat = cert.branch is None
    result = ZResult(True, "accepted", ln_z_lo=ln_lo, ln_z_hi=ln_hi, slack_lo=a_lo if flat else None,
                     slack_hi=a_hi if flat else None, full_box=full_box, keep=keep, stats=stats)
    if keep is not None:
        pop_lows = {a: v / z_hi for a, v in lows.items()}
        total_low = sum(pop_lows.values(), Fraction(0))
        result.populations = {a: (pop_lows[a], 1 - (total_low - pop_lows[a])) for a in pop_lows}
        result.removed_upper = 1 - total_low
    claim = cert.claim
    if ("ln_z_lo" in claim and claim["ln_z_lo"] > ln_lo) or ("ln_z_hi" in claim and claim["ln_z_hi"] < ln_hi):
        result.accepted = False
        result.reason = "the claimed interval is narrower than the interval the checker computes"
    return result
