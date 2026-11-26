"""Checker for "Z" certificates (`metricchain_sb.zcert`): replays the steps in exact integer
arithmetic, encloses the Boltzmann factors of the working model with the certified exponential,
sums the sites out on interval tables, and returns the enclosure it has itself computed.

The checker contains no search and trusts no number of the certificate: margins of prune steps
and residual ranges of relax steps are recomputed here; a claim is accepted only if it contains
the interval computed here.  It imports the data classes of `zcert`, the certified exponential
of `expo` and the interval tables of `itables` — nothing from the producer (`partition`).

Arithmetic.  Steps: Python integers (exact).  Boltzmann factors: `expo.exp_bounds_me` (integer
arithmetic, outward rounded).  Elimination: tier ``exact`` (rationals; exact) or ``float``
(binary64 with outward rounding; assumptions F1–F3 of `itables`).  Logarithms of the final
bounds: `expo.log_bounds` (certified through the exponential).

Population intervals (certificates with ``keep = t``).  Let `c_a = [lo_a, hi_a]` enclose the
sum of the working model over the final box with `x_t = a`, `T_hi = sum_a hi_a`, and `A_lo`,
`A_hi` the accumulated logarithmic factors.  For every state `a` of the final domain of `t`,

    P(x_t = a)  >=  exp(A_lo - A_hi) * lo_a / T_hi          (numerator from below, Z from above),
    P(x_t = a)  <=  1 - sum_{b != a} [lower bound of P(x_t = b)],

and a state of `t` that a prune step removed has population at most
`1 - sum_b [lower bound of P(x_t = b)]`.  Probabilities are those of the Boltzmann distribution
of the published tables *on the root box of the certificate*.

The checker never raises: malformed input, an invalid step, an over-budget table or an
arithmetic overflow is a rejection with a reason.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

from .expo import exp_bounds, exp_bounds_me, log_bounds
from .itables import ExactTables, FloatTables, TableTooLarge
from .zcert import MalformedZCertificate, ZCertificate, validate_structure

__all__ = ["ZResult", "check_partition_certificate"]


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
    except (OverflowError, ArithmeticError) as exc:
        return ZResult(False, f"rejected: arithmetic failure ({exc})")
    except Exception as exc:  # noqa: BLE001  (a rejection is always sound)
        return ZResult(False, f"rejected: {type(exc).__name__} while checking")


def _check(cert: ZCertificate, arithmetic: str, max_entries, exp_bits: int) -> ZResult:
    validate_structure(cert)
    if arithmetic not in ("exact", "float"):
        return ZResult(False, "unknown arithmetic tier")
    tables = ExactTables() if arithmetic == "exact" else FloatTables()
    model, beta = cert.model, cert.beta
    n = model.n
    unit = Fraction(1, 2 ** model.scale_bits)
    D = [list(d) for d in cert.domains]
    H = [[int(v) for v in u.tolist()] for u in model.unary]
    J = {key: [[int(v) for v in row] for row in t.tolist()] for key, t in model.pair.items()}
    nbrs = {i: set(model.neighbors(i)) for i in range(n)}

    def pair_entry(i, j, a, b):
        return J[(i, j)][a][b] if i < j else J[(j, i)][b][a]

    a_lo = Fraction(0)
    a_hi = Fraction(0)
    stats = {"prune": 0, "relax": 0, "largest_table": 0}
    for step in cert.steps:
        if step["op"] == "prune":
            i, r, t = step["site"], step["remove"], step["dominator"]
            if r == t or r not in D[i] or t not in D[i]:
                return ZResult(False, "prune step: dominator and removed state must be distinct states of the current domain")
            margin = H[i][r] - H[i][t]
            for j in nbrs[i]:
                margin += min(pair_entry(i, j, r, s) - pair_entry(i, j, t, s) for s in D[j])
            a_hi += exp_bounds(-beta * margin * unit, exp_bits)[1]        # ln(1 + rho) <= rho <= its upper enclosure
            D[i].remove(r)
            stats["prune"] += 1
        else:
            i, j = step["pair"]
            if (i, j) not in J:
                return ZResult(False, "relax step: the pair has already been relaxed")
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
            a_lo += -beta * r_hi * unit
            a_hi += -beta * r_lo * unit
            stats["relax"] += 1

    # Boltzmann factors of the working model on the working box, as interval tables.
    sizes = {i: len(D[i]) for i in range(n)}
    factors = []
    for i in range(n):
        me = [exp_bounds_me(-beta * H[i][a] * unit, exp_bits) for a in D[i]]
        factors.append(tables.from_me_bounds((i,), [x[0] for x in me], [x[1] for x in me], (sizes[i],)))
    for (i, j), table in J.items():
        me = [exp_bounds_me(-beta * table[a][b] * unit, exp_bits) for a in D[i] for b in D[j]]
        factors.append(tables.from_me_bounds((i, j), [x[0] for x in me], [x[1] for x in me], (sizes[i], sizes[j])))

    def product(parts):
        scope = tuple(sorted(set().union(*[set(p.scope) for p in parts])))
        entries = 1
        for s in scope:
            entries *= sizes[s]
        stats["largest_table"] = max(stats["largest_table"], entries)
        acc = parts[0]
        for p in parts[1:]:
            acc = tables.multiply(acc, p, sizes, max_entries)      # the result lives on the union of the two scopes
        return acc

    for v in cert.order:
        bucket = [f for f in factors if v in f.scope]
        factors = [f for f in factors if v not in f.scope]
        factors.append(tables.sum_out(product(bucket), v))
    final = product(factors)
    lo_list, hi_list = tables.bounds(final)

    full_box = all(sorted(d) == list(range(k)) for d, k in zip(cert.domains, model.sizes))
    z_lo, z_hi = sum(lo_list, Fraction(0)), sum(hi_list, Fraction(0))
    if z_lo <= 0:
        return ZResult(False, "abstained: the lower bound of the partition sum is not positive at this precision",
                       stats=stats)
    ln_lo = log_bounds(z_lo)[0] + a_lo
    ln_hi = log_bounds(z_hi)[1] + a_hi
    result = ZResult(True, "accepted", ln_z_lo=ln_lo, ln_z_hi=ln_hi, slack_lo=a_lo, slack_hi=a_hi,
                     full_box=full_box, keep=cert.keep, stats=stats)
    if cert.keep is not None:
        shrink = exp_bounds(a_lo - a_hi, exp_bits)[0]
        lows = {a: shrink * lo / z_hi for a, lo in zip(D[cert.keep], lo_list)}
        total_low = sum(lows.values(), Fraction(0))
        result.populations = {a: (lows[a], 1 - (total_low - lows[a])) for a in lows}
        result.removed_upper = 1 - total_low
    claim = cert.claim
    if ("ln_z_lo" in claim and claim["ln_z_lo"] > ln_lo) or ("ln_z_hi" in claim and claim["ln_z_hi"] < ln_hi):
        result.accepted = False
        result.reason = "the claimed interval is narrower than the interval the checker computes"
    return result

