"""Certified enclosures of exp and log at rational points (outward-rounded version of the theory
division's `expLo` / `expHi`, `proofs/Core/Rounding.lean`)."""
import random
from fractions import Fraction

import mpmath
import pytest

from metricchain_sb.expo import exp_bounds, log_bounds

mpmath.mp.dps = 80


def _mp(q: Fraction):
    return mpmath.mpf(q.numerator) / mpmath.mpf(q.denominator)


def test_exp_bounds_enclose_the_exponential_tightly_over_a_wide_range():
    rng = random.Random(1)
    points = [Fraction(0), Fraction(1), Fraction(-1), Fraction(1, 3), Fraction(-1688), Fraction(1500),
              Fraction(-7, 2 ** 20), Fraction(123456789, 2 ** 20)]
    points += [Fraction(rng.randint(-2000 * 2 ** 20, 2000 * 2 ** 20), 2 ** 20) for _ in range(200)]
    points += [Fraction(rng.randint(-10 ** 6, 10 ** 6), rng.randint(1, 10 ** 4)) for _ in range(100)]
    for q in points:
        lo, hi = exp_bounds(q)
        true = mpmath.exp(_mp(q))
        assert 0 < lo <= hi
        assert _mp(lo) <= true <= _mp(hi), q
        assert _mp(hi) / _mp(lo) - 1 < mpmath.mpf(2) ** -60, q


def test_exp_bounds_reproduce_the_blueprint_conformance_value():
    lo, hi = exp_bounds(Fraction(1), bits=40)
    assert Fraction(27182, 10000) <= lo <= hi <= Fraction(27183, 10000)


def test_exp_bounds_stay_valid_at_low_precision():
    for q in (Fraction(-50), Fraction(3, 7), Fraction(40)):
        lo, hi = exp_bounds(q, bits=8)
        assert _mp(lo) <= mpmath.exp(_mp(q)) <= _mp(hi)
        assert _mp(hi) / _mp(lo) - 1 < mpmath.mpf(2) ** -6


def test_log_bounds_enclose_the_logarithm_and_are_checked_through_exp():
    rng = random.Random(2)
    for _ in range(100):
        z = Fraction(rng.randint(1, 10 ** 30), rng.randint(1, 10 ** 30))
        lo, hi = log_bounds(z)
        true = mpmath.log(_mp(z))
        assert _mp(lo) <= true <= _mp(hi)
        assert hi - lo < Fraction(1, 2 ** 30)
    with pytest.raises(ValueError):
        log_bounds(Fraction(0))
