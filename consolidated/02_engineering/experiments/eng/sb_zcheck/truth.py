"""References by enumeration: ``ln Z`` and every population on a box, as rigorous Arb balls, plus an mpmath copy.

Independent of every checker: the energy of each configuration is evaluated from the published integer tables, its
Boltzmann factor is an Arb ball (default 400 bits), and the sums are ball sums.  Comparisons of a rational bound
with the truth return ``"yes"`` (certified), ``"no"`` (certified violation) or ``"undecided"``.

Three precautions make the comparisons decisive in the degenerate cases that a careful checker gets *exactly* right:

* ``ln Z = base + excess`` with ``base`` the exact rational logarithm of the largest Boltzmann factor and
  ``excess = ln(M) + log1p(rest / M) >= 0`` (``M`` configurations share the largest factor); a bound is compared with
  ``excess`` after an exact subtraction of ``base``, so that ``ln Z = 1e-400000`` is resolved;
* an upper bound on a population is tested on the complement, ``1 - hi <= 1 - P``, the complement being a sum of
  positive terms, so that a population within ``1e-1000`` of 1 is resolved;
* when every configuration has the same weight, populations are exact rationals and are compared exactly; when the box
  has a single configuration, so is ``ln Z``.
"""
from __future__ import annotations

import itertools
from fractions import Fraction

from flint import arb, ctx, fmpq


class Truth:
    """``base``, ``excess``: ``ln Z = base + excess`` (exact rational, ball); ``ln_z``: their sum as one ball;
    ``pop[i][a]``, ``comp[i][a]``: balls of ``P(x_i = a)`` and of ``1 - P(x_i = a)`` (states outside the box: absent);
    ``pop_exact``, ``ln_z_exact``: exact rationals in the flat cases, else ``None``."""

    def __init__(self, base, excess, ln_z, pop, comp, configs, prec, ln_z_exact=None, pop_exact=None):
        self.base, self.excess, self.ln_z, self.pop, self.comp = base, excess, ln_z, pop, comp
        self.configs, self.prec = configs, prec
        self.ln_z_exact, self.pop_exact = ln_z_exact, pop_exact

    def ln_z_lower_ok(self, lo: Fraction) -> str:
        if self.ln_z_exact is not None:
            return "yes" if lo <= self.ln_z_exact else "no"
        return lower_ok(lo - self.base, self.excess, self.prec)

    def ln_z_upper_ok(self, hi: Fraction) -> str:
        if self.ln_z_exact is not None:
            return "yes" if self.ln_z_exact <= hi else "no"
        return upper_ok(hi - self.base, self.excess, self.prec)

    def ln_z_contains(self, lo: Fraction, hi: Fraction) -> str:
        return _both(self.ln_z_lower_ok(lo), self.ln_z_upper_ok(hi))

    def pop_lower_ok(self, site: int, state: int, lo: Fraction) -> str:
        if lo <= 0:
            return "yes"
        if self.pop_exact is not None:
            return "yes" if lo <= self.pop_exact[site].get(state, Fraction(0)) else "no"
        if state not in self.pop[site]:
            return "no"
        return lower_ok(lo, self.pop[site][state], self.prec)

    def pop_upper_ok(self, site: int, state: int, hi: Fraction) -> str:
        if hi >= 1:
            return "yes"
        if self.pop_exact is not None:
            return "yes" if self.pop_exact[site].get(state, Fraction(0)) <= hi else "no"
        if state not in self.pop[site]:
            return "yes" if hi >= 0 else "no"
        return lower_ok(1 - hi, self.comp[site][state], self.prec)

    def pop_contains(self, site: int, state: int, lo: Fraction, hi: Fraction) -> str:
        return _both(self.pop_lower_ok(site, state, lo), self.pop_upper_ok(site, state, hi))


def _both(a: str, b: str) -> str:
    if a == "no" or b == "no":
        return "no"
    return "yes" if a == "yes" and b == "yes" else "undecided"


def energies(unary, pair, domains):
    """Yield ``(x, E_int)`` for every configuration of the box (table units)."""
    pairs = sorted(pair.items())
    for x in itertools.product(*domains):
        e = 0
        for i, a in enumerate(x):
            e += unary[i][a]
        for (i, j), table in pairs:
            e += table[x[i]][x[j]]
        yield x, e


def enumerate_truth(unary, pair, scale_bits: int, beta: Fraction, domains, prec: int = 400) -> Truth:
    """Any sign of ``beta``.  Raises ``ValueError`` on an empty box or when a ball loses its sign (out of range)."""
    old = ctx.prec
    try:
        num, den = -beta.numerator, beta.denominator
        if scale_bits >= 0:
            den <<= scale_bits
        else:
            num <<= -scale_bits
        rows = list(energies(unary, pair, domains))
        if not rows:
            raise ValueError("empty box")
        e_ref = min(e for _, e in rows) if num <= 0 else max(e for _, e in rows)     # the largest Boltzmann factor
        base = Fraction(num * e_ref, den)
        n = len(unary)
        cache = {}
        ctx.prec = prec + 32
        rest = arb(0)
        top = 0
        part = [dict((a, arb(0)) for a in domains[i]) for i in range(n)]
        count = [dict((a, 0) for a in domains[i]) for i in range(n)]
        for x, e in rows:
            w = cache.get(e)
            if w is None:
                q = Fraction(num * (e - e_ref), den)                                  # <= 0
                if q == 0:
                    w = arb(1)
                else:
                    ctx.prec = prec + 32 + max(0, (abs(q.numerator) // q.denominator).bit_length())
                    w = arb(fmpq(q.numerator, q.denominator)).exp()
                    ctx.prec = prec + 32
                    if not (w.is_finite() and w.lower() > 0):
                        raise ValueError("a Boltzmann factor is out of the range of the multiprecision library")
                cache[e] = w
            if e == e_ref or num == 0:
                top += 1
            else:
                rest += w
            for i, a in enumerate(x):
                part[i][a] += w
                count[i][a] += 1
        configs = len(rows)
        total = arb(top) + rest
        excess = arb(top).log() + (rest / top).log1p()
        ln_z = arb(fmpq(base.numerator, base.denominator)) + excess
        pop = [dict((a, s / total) for a, s in part[i].items()) for i in range(n)]
        comp = []
        for i in range(n):
            row = {}
            for a in part[i]:
                others = arb(0)
                for b, s in part[i].items():
                    if b != a:
                        others += s
                row[a] = others / total
            comp.append(row)
        ln_z_exact = pop_exact = None
        if top == configs:                                                            # every weight is the same
            pop_exact = [dict((a, Fraction(c, configs)) for a, c in count[i].items()) for i in range(n)]
            if configs == 1:
                ln_z_exact = base
        return Truth(base, excess, ln_z, pop, comp, configs, prec, ln_z_exact, pop_exact)
    finally:
        ctx.prec = old


def lower_ok(bound: Fraction, ball, prec: int = 400) -> str:
    """``bound <= value``, for the value enclosed by ``ball``?"""
    old = ctx.prec
    try:
        ctx.prec = prec + 64
        d = ball - arb(fmpq(bound.numerator, bound.denominator))
        if d.lower() >= 0:
            return "yes"
        if d.upper() < 0:
            return "no"
        return "undecided"
    finally:
        ctx.prec = old


def upper_ok(bound: Fraction, ball, prec: int = 400) -> str:
    """``value <= bound``?"""
    old = ctx.prec
    try:
        ctx.prec = prec + 64
        d = arb(fmpq(bound.numerator, bound.denominator)) - ball
        if d.lower() >= 0:
            return "yes"
        if d.upper() < 0:
            return "no"
        return "undecided"
    finally:
        ctx.prec = old


def ball_text(ball, digits: int = 40) -> str:
    return ball.str(digits, radius=False)


def mp_ln_z(unary, pair, scale_bits: int, beta: Fraction, domains, dps: int = 80):
    """The same enumeration with mpmath (not rigorous; an independent library for cross-checks).  Returns
    ``(ln Z as an mpf, [{state: population as an mpf}])``; the largest term is factored out first."""
    import mpmath
    with mpmath.workdps(dps + 10):
        scale = mpmath.mpf(2) ** (-scale_bits)
        b = mpmath.mpf(beta.numerator) / beta.denominator
        rows = list(energies(unary, pair, domains))
        e_ref = min(e for _, e in rows) if beta >= 0 else max(e for _, e in rows)
        z = mpmath.mpf(0)
        part = [dict((a, mpmath.mpf(0)) for a in domains[i]) for i in range(len(unary))]
        for x, e in rows:
            w = mpmath.exp(-b * scale * (e - e_ref))
            z += w
            for i, a in enumerate(x):
                part[i][a] += w
        ln_z = mpmath.log(z) - b * scale * e_ref
        pop = [dict((a, s / z) for a, s in part[i].items()) for i in range(len(unary))]
        return +ln_z, [dict((a, +v) for a, v in row.items()) for row in pop]
