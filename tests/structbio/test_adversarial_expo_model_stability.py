"""Adversarial review STRUCTBIO-REV-0001 — `expo` (enclosures of exp and log), `model.PairModel`
(the published instance) and `stability` (flip gaps assembled from producer output).

``FINDING`` tests fail with the reviewed code and are left red; ``SURVIVED`` and
``CHARACTERISATION`` tests pass.
"""
import itertools
import math
import random
from fractions import Fraction

import numpy as np
import pytest
from mpmath import iv

from metricchain_sb import stability
from metricchain_sb.expo import exp_bounds, log_bounds
from metricchain_sb.mincheck import check_min_certificate
from metricchain_sb.model import PairModel


def _ivq(q):
    q = Fraction(q)
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


# ----------------------------------------------------------------------------------------------
# attacks that the code withstood
# ----------------------------------------------------------------------------------------------

def test_exp_bounds_enclose_exp_at_extreme_rationals_and_precisions():
    """SURVIVED.  1,200 enclosures against rigorous interval arithmetic (120 digits): |q| up to 1e6
    with denominators up to 1e6 and 2**20, arguments of size 1e-40, long denominators, both sides
    of every power of two up to 2**20, precisions from 0 to 300 bits.  (6,012 cases during the
    review, no miss.)"""
    rng = random.Random(7)
    old = iv.dps
    iv.dps = 120

    def points():
        yield from (Fraction(0), Fraction(1), Fraction(-1), Fraction(10 ** 6), Fraction(-10 ** 6))
        for _ in range(295):
            r = rng.random()
            if r < 0.2:
                yield Fraction(rng.randint(-10 ** 6, 10 ** 6), rng.randint(1, 10 ** 6))
            elif r < 0.4:
                yield Fraction(rng.randint(-10 ** 6 * 2 ** 20, 10 ** 6 * 2 ** 20), 2 ** 20)
            elif r < 0.5:
                yield Fraction(rng.choice([-1, 1]), rng.randint(1, 10 ** 40))
            elif r < 0.6:
                yield Fraction(rng.choice([-1, 1]) * rng.randint(1, 10 ** 40), 10 ** 40)
            elif r < 0.7:
                yield rng.choice([-1, 1]) * Fraction(2 ** rng.randint(0, 20)) + Fraction(rng.choice([-1, 0, 1]), 10 ** 30)
            elif r < 0.8:
                yield Fraction(rng.choice([-1, 1]) * 10 ** 6) + Fraction(rng.randint(-5, 5), 7)
            elif r < 0.9:
                yield Fraction(rng.randint(-2000, 2000), rng.randint(1, 50))
            else:
                yield Fraction(rng.randint(-64, 64), 2 ** rng.randint(0, 80))

    try:
        cases = 0
        for q in points():
            for bits in (rng.choice([0, 1, 2, 5, 8, 16]), 64, 80, rng.choice([100, 150, 300])):
                lo, hi = exp_bounds(q, bits)
                truth = iv.exp(_ivq(q))
                assert 0 < lo <= hi
                assert _ivq(lo).b <= truth.a and truth.b <= _ivq(hi).a, (q, bits)
                cases += 1
        assert cases == 1200
    finally:
        iv.dps = old


def test_log_bounds_enclose_log_for_huge_tiny_and_near_one_arguments():
    """SURVIVED.  300 enclosures against interval arithmetic (200 digits): rationals with 300-digit
    numerators and denominators, 10**+-3000, arguments within 1e-60 of 1, and quotients of two
    400-digit integers that agree to 20 digits (where the floating-point guess loses everything);
    the width stays within 4 * 2**-40 * max(1, |log z|)."""
    rng = random.Random(8)
    old = iv.dps
    iv.dps = 200

    def arguments():
        for _ in range(300):
            r = rng.random()
            if r < 0.3:
                yield Fraction(rng.randint(1, 10 ** 30), rng.randint(1, 10 ** 30))
            elif r < 0.5:
                yield Fraction(rng.randint(1, 10 ** 300), rng.randint(1, 10 ** 300))
            elif r < 0.6:
                yield Fraction(10 ** rng.randint(0, 3000)) + rng.randint(0, 5)
            elif r < 0.7:
                yield Fraction(1, 10 ** rng.randint(0, 3000) + rng.randint(0, 5))
            elif r < 0.8:
                yield 1 + Fraction(rng.choice([-1, 1]), 10 ** rng.randint(1, 60))
            elif r < 0.9:
                yield Fraction(10 ** 400 + rng.randint(-10 ** 380, 10 ** 380), 10 ** 400)
            else:
                yield Fraction(rng.randint(1, 2 ** 70), 2 ** rng.randint(0, 2000))

    try:
        for z in arguments():
            lo, hi = log_bounds(z)
            truth = iv.log(_ivq(z))
            assert _ivq(lo).b <= truth.a and truth.b <= _ivq(hi).a, z
            assert hi - lo <= 4 * Fraction(1, 2 ** 40) * max(1, abs(lo))
        with pytest.raises(ValueError):
            log_bounds(Fraction(-1))
    finally:
        iv.dps = old


def test_second_best_gap_of_an_incomplete_list_of_sites_is_silently_too_large():
    """CHARACTERISATION (documented precondition, not enforced).  `second_best_gap` needs the gaps of
    all sites with more than one state; given the gaps of one site it returns a number that is not
    the gap to the second-best configuration, without a warning: a `FlipGap` list does not record
    which sites it covers."""
    model = PairModel(unary=[np.array([0, 7, 9]), np.array([0, 1])], pair={(0, 1): np.array([[0, 0], [0, 0], [0, 0]])},
                      scale_bits=0)
    x_star = (0, 0)
    energies = sorted(model.energy(x) for x in itertools.product(range(3), range(2)))
    assert energies[1] - energies[0] == 1
    every = stability.certify_flip_gaps(model, x_star)
    assert stability.second_best_gap(every) == 1
    partial = stability.certify_flip_gaps(model, x_star, sites=[0])
    assert all(check_min_certificate(g.certificate).accepted for g in partial)
    assert stability.second_best_gap(partial) == 7


# ----------------------------------------------------------------------------------------------
# findings (these tests fail with the reviewed code)
# ----------------------------------------------------------------------------------------------

@pytest.mark.parametrize("q", [Fraction(10 ** 6), Fraction(-10 ** 6), Fraction(-2 ** 20 + 1)])
def test_exp_bounds_width_is_two_to_minus_bits_as_documented(q):
    """FINDING (documentation).  `exp_bounds_me` promises a relative width of "about 2**-bits for
    bits <= 80".  The width is in fact about max(2**-(bits + 14), 2**(k - 101)) with
    k = 6 + bit length of |q|: 2**-94 at q = 1 but 2**-74.5 at |q| = 1e6 (bits = 80), 2**-45 at
    2**60, 2**-5 at 2**100, and vacuous beyond 2**105 — nothing warns of it, the Z checker then
    abstains because its lower bound vanishes."""
    bits = 80
    lo, hi = exp_bounds(q, bits)
    width = math.log2(hi / lo - 1)
    assert width <= -(bits - 2), f"relative width 2**{width:.1f} at q = {float(q):.6g}, documented about 2**-{bits}"


@pytest.mark.parametrize("case", ["Fraction entries", "float in an object array", "string as pair key", "floats as pair key"])
def test_pair_model_refuses_what_it_would_have_to_truncate(case):
    """FINDING (silent truncation in the published instance).  Tables "must be integers ... use
    from_float to round" and a float array is refused, but an object array is passed through
    `int()`: 7/2 becomes 3, -7/2 becomes -3 and 1.9 becomes 1 without a word.  Pair keys go through
    `int()` too: the string "01" is read as the pair (0, 1) and (0.9, 1.9) as (0, 1)."""
    table = [[0, 1], [2, 3]]
    with pytest.raises((TypeError, ValueError)):
        if case == "Fraction entries":
            model = PairModel(unary=[np.array([Fraction(7, 2), Fraction(-7, 2)], dtype=object)], pair={}, scale_bits=0)
        elif case == "float in an object array":
            model = PairModel(unary=[np.array([1.9, 2 ** 70], dtype=object)], pair={}, scale_bits=0)
        elif case == "string as pair key":
            model = PairModel(unary=[[0, 1], [0, 1]], pair={"01": table}, scale_bits=0)
        else:
            model = PairModel(unary=[[0, 1], [0, 1]], pair={(0.9, 1.9): table}, scale_bits=0)
        pytest.fail(f"accepted; stored tables {[u.tolist() for u in model.unary]}, pairs {sorted(model.pair)}")


@pytest.mark.parametrize("function", ["energy_int", "certify_flip_gaps", "shifted_model"])
def test_negative_state_indices_are_refused(function):
    """FINDING (silent misreading).  A state index -1 is taken by NumPy as "the last state".
    `energy_int((-1, -1))` returns the energy of the last states; `certify_flip_gaps` with such an
    `x*` uses that energy but removes nothing from the domain (no state equals -1), so each
    "flip gap" is the minimum over the *full* box minus E(x*); `shifted_model` raises the pair
    entry of the last states and lowers every unary entry.  (The min checker itself validates the
    witness and is not affected.)"""
    model = PairModel(unary=[np.array([0, 5]), np.array([5, 0])], pair={(0, 1): np.array([[10, 10], [0, 10]])},
                      scale_bits=0)
    with pytest.raises((ValueError, IndexError)):
        if function == "energy_int":
            out = model.energy_int((-1, -1))
        elif function == "certify_flip_gaps":
            out = [(g.site, g.gap, g.certificate.domains) for g in stability.certify_flip_gaps(model, (-1, -2))]
        else:
            out = [u.tolist() for u in stability.shifted_model(model, (-1, -1), 1).unary]
        pytest.fail(f"accepted a negative state index and returned {out}")


def test_a_flip_gap_is_backed_by_a_certificate_on_the_flip_box():
    """FINDING (the claim is weaker than it appears; needs a faulty producer to bite).  `FlipGap.gap`
    is documented as certified, but nothing in `stability` — and nothing in the driver, which
    records only `accepted` — compares the box of the returned certificate with the box
    `{x_i != x*_i}` the gap is about.  A producer that silently drops one more state returns a
    certificate that the checker rightly accepts (it is true on the smaller box), that passes the
    existing test (`x*_i` is not in the box), and whose gap is 10 where the flip gap is 1."""
    model = PairModel(unary=[np.array([0, 10, 1]), np.array([0, 5])], pair={(0, 1): np.array([[0, 0], [0, 0], [0, 0]])},
                      scale_bits=0)
    x_star = (0, 0)
    true_gap = min(model.energy(x) for x in itertools.product(range(3), range(2)) if x[0] != 0) - model.energy(x_star)
    assert true_gap == 1
    honest = stability.certify_gmec

    def drops_a_state(model, eps=Fraction(0), domains=None, **options):
        domains = [list(d) for d in domains]
        for i, d in enumerate(domains):
            if len(d) > 1:
                domains[i] = d[:-1]
                break
        return honest(model, eps=eps, domains=domains, **options)

    stability.certify_gmec = drops_a_state
    try:
        (gap,) = stability.certify_flip_gaps(model, x_star, sites=[0])
    except Exception:                       # a refusal would be the right behaviour
        return
    finally:
        stability.certify_gmec = honest
    result = check_min_certificate(gap.certificate)
    assert result.accepted and x_star[0] not in gap.certificate.domains[0]      # every existing check passes
    assert gap.certificate.domains == [[1, 2], [0, 1]] and gap.gap == true_gap, (
        f"reported flip gap {gap.gap} (true {true_gap}) on the box {gap.certificate.domains}; "
        f"certificate accepted={result.accepted}, full_box={result.full_box}")


def test_shifted_model_does_not_wrap_at_the_edge_of_int64():
    """FINDING (false verdict of a derived claim; table entries and error bounds near 2**63; new code,
    looked at only briefly).  `stability._moved` adds the error bounds in int64: an entry 2**63 - 1
    raised by 2**63 - 1 becomes -2.  `certify_necessary_optimality` then reports `holds = True`,
    with a certificate that the checker accepts (it is true of the wrapped tables), for an `x*`
    whose energy is 2**63 - 1 while the other state has energy 5.  NumPy emits a RuntimeWarning."""
    import warnings
    big = 2 ** 63 - 1
    model = PairModel(unary=[np.array([big, 5], dtype=object)], pair={}, scale_bits=0)
    bound = ([[big, 0]], {})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            shifted = stability.shifted_model(model, (0,), bound)
            verdict = stability.certify_necessary_optimality(model, (0,), bound)
        except (ValueError, OverflowError):
            return                              # refusing the range would be the right behaviour
    assert [int(v) for v in shifted.unary[0]] == [2 * big, 5] and verdict.holds is False, (
        f"shifted tables {shifted.unary[0].tolist()} (expected {[2 * big, 5]}); holds={verdict.holds}, "
        f"certificate accepted={check_min_certificate(verdict.certificate).accepted}")
