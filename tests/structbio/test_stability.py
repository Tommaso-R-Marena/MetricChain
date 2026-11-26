"""Certified stability of a global minimum: minima over restricted boxes, per-site flip gaps."""
import itertools
import json
import random
from fractions import Fraction

import pytest

from metricchain_sb.gmec import certify_gmec
from metricchain_sb.mincert import to_metricchain_cert1
from metricchain_sb.mincheck import check_min_certificate
from metricchain_sb.model import brute_force_min
from metricchain_sb.synthetic import random_pair_model


def test_certificate_on_a_restricted_box_matches_enumeration_over_that_box(reference_checker):
    rng = random.Random(11)
    for seed in range(12):
        model = random_pair_model(seed, n=5, kmax=4, density=0.8, scale_bits=2, kmin=2)
        domains = [sorted(rng.sample(range(k), rng.randint(1, k))) for k in model.sizes]
        emin, _ = brute_force_min(model, domains)
        cert = certify_gmec(model, eps=Fraction(0), domains=domains)
        assert cert.domains == domains
        result = check_min_certificate(cert)
        assert result.accepted, result.reason
        assert result.lower_bound == Fraction(emin, 2 ** model.scale_bits) == result.witness_energy
        assert all(cert.witness[i] in domains[i] for i in range(model.n))
        assert reference_checker.check_text(json.dumps(to_metricchain_cert1(cert)))["accepted"] is True


def test_flip_gaps_equal_enumerated_gaps_and_their_minimum_is_the_gap_to_the_second_best():
    from metricchain_sb.stability import certify_flip_gaps, second_best_gap
    for seed in range(10):
        model = random_pair_model(seed, n=5, kmax=3, density=0.9, scale_bits=1, kmin=1)
        unit = Fraction(1, 2 ** model.scale_bits)
        base = certify_gmec(model, eps=Fraction(0))
        x_star, e_star = base.witness, model.energy(base.witness)
        energies = {x: model.energy_int(x) * unit for x in itertools.product(*[range(k) for k in model.sizes])}
        gaps = certify_flip_gaps(model, x_star)
        assert [g.site for g in gaps] == [i for i, k in enumerate(model.sizes) if k > 1]
        for g in gaps:
            truth = min(e for x, e in energies.items() if x[g.site] != x_star[g.site]) - e_star
            assert g.gap == truth
            assert check_min_certificate(g.certificate).accepted
            assert x_star[g.site] not in g.certificate.domains[g.site]
            assert g.alternative[g.site] != x_star[g.site] and model.energy(g.alternative) - e_star == truth
        others = sorted(e for x, e in energies.items() if x != x_star)
        if others:
            assert second_best_gap(gaps) == others[0] - e_star


def test_a_gap_above_twice_the_rounding_margin_protects_the_minimiser_against_rounding():
    from metricchain_sb.stability import certify_flip_gaps, rounding_margin, second_best_gap
    rng = random.Random(5)
    protected = 0
    for seed in range(40):
        model = random_pair_model(seed, n=4, kmax=3, density=1.0, scale_bits=0, amplitude=40, kmin=2)
        margin = rounding_margin(model)
        assert margin == Fraction(model.n + len(model.pair), 2)
        x_star = certify_gmec(model, eps=Fraction(0)).witness
        gap = second_best_gap(certify_flip_gaps(model, x_star))
        if gap <= 2 * margin:
            continue
        protected += 1
        for _ in range(20):                      # any "float" tables within half a grid step of the integers
            du = [[rng.uniform(-0.5, 0.5) for _ in range(k)] for k in model.sizes]
            dp = {key: [[rng.uniform(-0.5, 0.5) for _ in range(t.shape[1])] for _ in range(t.shape[0])]
                  for key, t in model.pair.items()}

            def energy(x):
                e = sum(float(model.unary[i][a]) + du[i][a] for i, a in enumerate(x))
                return e + sum(float(t[x[i], x[j]]) + dp[(i, j)][x[i]][x[j]] for (i, j), t in model.pair.items())

            best = min(itertools.product(*[range(k) for k in model.sizes]), key=energy)
            assert best == x_star
    assert protected >= 5
