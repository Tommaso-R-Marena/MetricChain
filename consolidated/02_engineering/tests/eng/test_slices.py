"""Tests of experiment X-008 (smallest sensitive balls on a type class; THY-REQ-0010 question 2)."""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "slices"))

import ball_exponents as be  # noqa: E402


def test_validation_target_of_the_request():
    v = be.validation_target()
    assert v["size"] == 17 and v["phi"] == pytest.approx(((math.e ** 4 - 1) + 16 * (math.e ** 2 - 1)) / 70, rel=1e-14)


def brute_ball(n, k, c, i0, u):
    """Density and effect of {x in T_k : overlap(x, c) >= i0} by enumeration of T_k and of all pairwise distances."""
    pts = [frozenset(s) for s in itertools.combinations(range(n), k)]
    cset = frozenset(c)
    D = [x for x in pts if len(x & cset) >= i0]
    out = [x for x in pts if len(x & cset) < i0]
    phi = sum(math.expm1(u * min(len(x ^ y) for y in out)) for x in D) / len(pts)
    return len(D) / len(pts), phi


@pytest.mark.parametrize("n,k,m", [(8, 4, 4), (8, 4, 2), (9, 3, 5), (10, 5, 7), (10, 3, 0 + 6)])
def test_distance_to_the_complement_formula(n, k, m):
    """The closed form (distance 2 (i - i0 + 1) to the complement) against brute force on small classes."""
    u = 0.7
    c = tuple(range(m))
    i_lo, i_hi = max(0, m + k - n), min(m, k)
    for i0 in range(i_lo + 1, i_hi + 1):
        w = {i: math.comb(m, i) * math.comb(n - m, k - i) for i in range(i0, i_hi + 1)}
        q = sum(w.values()) / math.comb(n, k)
        phi = sum(w[i] * math.expm1(2 * u * (i - i0 + 1)) for i in w) / math.comb(n, k)
        qb, phib = brute_ball(n, k, c, i0, u)
        assert q == pytest.approx(qb, rel=1e-12) and phi == pytest.approx(phib, rel=1e-12), (i0, q, qb, phi, phib)


@pytest.mark.parametrize("n,kappa", [(20, 0.5), (40, 0.3), (60, 0.4), (100, 0.5)])
def test_float_optimum_equals_exact_optimum(n, kappa):
    k = round(kappa * n)
    f = be.ball_optimum(n, k, 1.0, 1.0)
    e = be.ball_optimum_exact(n, k, 1.0, 1.0)
    assert abs(f["lq"] - e["lq"]) < 1e-9
    assert float(e["q"]) == pytest.approx(math.exp(f["lq"]), rel=1e-9)
