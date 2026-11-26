"""Certified enclosures of partition functions and of per-state populations (capability C2).

Ground truth: exhaustive enumeration with 60-digit arithmetic on instances small enough to
enumerate.  Every certified interval must contain it; one miss is a bug."""
import copy
import itertools
import random
from fractions import Fraction

import mpmath
import numpy as np
import pytest

from metricchain_sb.partition import PartitionBudgetExceeded, certify_partition
from metricchain_sb.synthetic import random_pair_model
from metricchain_sb.zcert import ZCertificate
from metricchain_sb.zcheck import check_partition_certificate

mpmath.mp.dps = 60
BETA = Fraction(1000, 593)


def _mp(q):
    q = Fraction(q)
    return mpmath.mpf(q.numerator) / mpmath.mpf(q.denominator)


def truth(model, beta, domains=None):
    """(ln Z, {site: {state: population}}) over the box, by enumeration in high precision."""
    domains = model.full_domains() if domains is None else domains
    unit = Fraction(1, 2 ** model.scale_bits)
    z = mpmath.mpf(0)
    marg = [dict.fromkeys(d, mpmath.mpf(0)) for d in domains]
    for x in itertools.product(*domains):
        w = mpmath.exp(-_mp(beta * model.energy_int(x) * unit))
        z += w
        for i, a in enumerate(x):
            marg[i][a] += w
    return mpmath.log(z), [{a: v / z for a, v in m.items()} for m in marg]


def models():
    out = []
    for seed in range(10):
        rng = random.Random(seed)
        out.append(random_pair_model(seed, n=rng.randint(2, 6), kmax=rng.randint(2, 4), density=rng.choice([0.5, 1.0]),
                                     scale_bits=rng.choice([2, 5]), amplitude=rng.choice([6, 40]), kmin=1))
    return out


@pytest.mark.parametrize("arithmetic", ["exact", "float"])
def test_exact_elimination_encloses_ln_z_tightly(arithmetic):
    for model in models():
        lnz, _ = truth(model, BETA)
        cert = certify_partition(model, BETA, tau=None, theta=None, arithmetic=arithmetic)
        res = check_partition_certificate(cert, arithmetic=arithmetic)
        assert res.accepted, res.reason
        assert _mp(res.ln_z_lo) <= lnz <= _mp(res.ln_z_hi)
        assert res.ln_z_hi - res.ln_z_lo < Fraction(1, 10 ** 9)
        assert not cert.steps                       # nothing pruned, nothing relaxed: the width is arithmetic only


@pytest.mark.parametrize("arithmetic", ["exact", "float"])
def test_relaxed_and_pruned_certificates_still_enclose_ln_z_and_report_their_width(arithmetic):
    widths = []
    for model in models():
        lnz, _ = truth(model, BETA)
        unit = Fraction(1, 2 ** model.scale_bits)
        cert = certify_partition(model, BETA, tau=3 * unit * 2 ** model.scale_bits, theta=4 * unit * 2 ** model.scale_bits,
                                 arithmetic=arithmetic)
        res = check_partition_certificate(cert, arithmetic=arithmetic)
        assert res.accepted, res.reason
        assert _mp(res.ln_z_lo) <= lnz <= _mp(res.ln_z_hi)
        assert res.ln_z_hi - res.ln_z_lo <= res.slack_hi - res.slack_lo + Fraction(1, 10 ** 9)
        widths.append((len(cert.steps), res.ln_z_hi - res.ln_z_lo))
    assert any(n > 0 and w > Fraction(1, 100) for n, w in widths)      # the test really exercises the two rules


@pytest.mark.parametrize("arithmetic", ["exact", "float"])
def test_population_intervals_contain_the_enumerated_marginals(arithmetic):
    for model in models()[:6]:
        _, marg = truth(model, BETA)
        for site in range(model.n):
            for (tau, theta) in ((None, None), (30, 2)):
                cert = certify_partition(model, BETA, keep=site, tau=tau, theta=theta, arithmetic=arithmetic)
                res = check_partition_certificate(cert, arithmetic=arithmetic)
                assert res.accepted, res.reason
                for a in range(model.sizes[site]):
                    lo, hi = res.population(a)
                    assert _mp(lo) <= marg[site][a] <= _mp(hi), (site, a)
                    if tau is None:
                        assert hi - lo < Fraction(1, 10 ** 9)


def test_a_box_restriction_gives_the_conditional_ensemble():
    model = models()[3]
    domains = [[0] if i % 2 else list(range(k)) for i, k in enumerate(model.sizes)]
    lnz, marg = truth(model, BETA, domains)
    free = [i for i, d in enumerate(domains) if len(d) > 1]
    cert = certify_partition(model, BETA, domains=domains, keep=free[0] if free else None, tau=None, theta=None)
    res = check_partition_certificate(cert)
    assert res.accepted and _mp(res.ln_z_lo) <= lnz <= _mp(res.ln_z_hi)
    if free:
        for a in domains[free[0]]:
            lo, hi = res.population(a)
            assert _mp(lo) <= marg[free[0]][a] <= _mp(hi)


def test_claims_narrower_than_what_the_checker_computes_and_invalid_steps_are_rejected():
    model = models()[5]
    cert = certify_partition(model, BETA, tau=None, theta=None)
    good = check_partition_certificate(cert)
    assert good.accepted
    bad = copy.deepcopy(cert)
    bad.claim["ln_z_lo"] = good.ln_z_hi + Fraction(1, 1000)          # claims more than is certified
    assert not check_partition_certificate(bad).accepted
    bad = copy.deepcopy(cert)
    k = model.sizes[0]
    if k > 1:
        bad.steps.insert(0, {"op": "prune", "site": 0, "remove": 0, "dominator": 0})   # dominator equals removed
        assert not check_partition_certificate(bad).accepted
    bad = copy.deepcopy(cert)
    bad.order = bad.order[:-1]                                                        # a site is never eliminated
    assert not check_partition_certificate(bad).accepted


def test_arbitrary_relaxation_vectors_cannot_make_the_checker_unsound():
    """The checker recomputes the residual bounds itself, so a certificate may propose any `f`, `g`."""
    rng = random.Random(4)
    for model in models()[:6]:
        if not model.pair:
            continue
        lnz, _ = truth(model, BETA)
        cert = certify_partition(model, BETA, tau=None, theta=None)
        (i, j) = sorted(model.pair)[0]
        bad = copy.deepcopy(cert)
        bad.steps = [{"op": "relax", "pair": [i, j], "f": [rng.randint(-50, 50) for _ in range(model.sizes[i])],
                      "g": [rng.randint(-50, 50) for _ in range(model.sizes[j])]}]
        bad.claim = {}
        res = check_partition_certificate(bad)
        assert res.accepted and _mp(res.ln_z_lo) <= lnz <= _mp(res.ln_z_hi)


def test_the_producer_abstains_when_a_table_would_exceed_the_budget():
    model = random_pair_model(3, n=7, kmax=4, density=1.0, scale_bits=2, kmin=3)
    with pytest.raises(PartitionBudgetExceeded):
        certify_partition(model, BETA, tau=None, theta=None, max_entries=50)
