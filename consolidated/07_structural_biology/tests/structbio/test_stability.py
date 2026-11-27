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


# ----------------------------------------------------------------------------------------------
# Leaving a whole class of states (a rotamer well), and optimality under entrywise table error.
# Both are constructions proposed by the science division (SCI-REV-0026, section 0 point 1 and
# section 4); each is one more certified minimisation, no new kernel rule.

def _all_energies(model):
    unit = Fraction(1, 2 ** model.scale_bits)
    return {x: model.energy_int(x) * unit for x in itertools.product(*[range(k) for k in model.sizes])}


def test_exclusion_gaps_equal_enumeration_and_a_site_with_no_state_outside_its_class_is_reported():
    from metricchain_sb.stability import certify_exclusion_gaps
    rng = random.Random(23)
    without_alternative = 0
    for seed in range(12):
        model = random_pair_model(seed, n=5, kmax=4, density=1.0, scale_bits=2, kmin=2)
        energies = _all_energies(model)
        x_star = min(energies, key=lambda x: (energies[x], x))
        classes = [[rng.randrange(2) for _ in range(k)] for k in model.sizes]
        exclude = {i: {a for a in range(model.sizes[i]) if classes[i][a] == classes[i][x_star[i]]}
                   for i in range(model.n)}
        gaps = certify_exclusion_gaps(model, x_star, exclude)
        assert [g.site for g in gaps] == list(range(model.n))
        for g in gaps:
            allowed = [e for x, e in energies.items() if x[g.site] not in exclude[g.site]]
            if not allowed:
                assert g.gap is None and g.certificate is None and g.alternative is None
                without_alternative += 1
                continue
            assert g.gap == min(allowed) - energies[x_star]
            result = check_min_certificate(g.certificate)
            assert result.accepted and result.certified_gap == 0
            assert not set(g.certificate.domains[g.site]) & exclude[g.site]
            assert g.alternative[g.site] not in exclude[g.site]
            assert energies[tuple(g.alternative)] - energies[x_star] == g.gap
    assert without_alternative >= 3          # the case occurs in this sample


def _entries_used(model, x):
    used = {("u", i, a) for i, a in enumerate(x)}
    used |= {("p", i, j, x[i], x[j]) for (i, j) in model.pair}
    return used


def test_shifted_model_decides_optimality_in_every_table_within_b():
    """`x*` minimises every table whose entries lie within `b` of the model's  <=>  `x*` minimises
    the shifted model (entries `x*` uses raised by b, all others lowered by b).  Checked against
    the definition: for every competitor, the worst scenario is the one that raises what only
    `x*` uses and lowers what only the competitor uses."""
    from metricchain_sb.stability import certify_necessary_optimality, shifted_model
    outcomes = {True: 0, False: 0}
    for seed in range(40):
        model = random_pair_model(seed, n=4, kmax=3, density=1.0, scale_bits=0, amplitude=30, kmin=2)
        energies = {x: model.energy_int(x) for x in itertools.product(*[range(k) for k in model.sizes])}
        x_star = min(energies, key=lambda x: (energies[x], x))
        used_star = _entries_used(model, x_star)
        for b in (0, 1, 2, 4):
            worst = {x: energies[x] - energies[x_star] - b * len(_entries_used(model, x) ^ used_star) for x in energies}
            truth = all(v >= 0 for v in worst.values())
            shifted = shifted_model(model, x_star, b)
            assert all(shifted.energy_int(x) - shifted.energy_int(x_star) == worst[x] for x in energies)
            verdict = certify_necessary_optimality(model, x_star, b)
            assert verdict.holds is truth
            assert check_min_certificate(verdict.certificate).accepted
            assert verdict.certificate.model is not model and verdict.b == b
            if not truth:                      # the counterexample comes with its scenario
                x = tuple(verdict.counterexample)
                assert worst[x] < 0
                scenario = verdict.scenario()
                assert scenario.energy_int(x) < scenario.energy_int(x_star)
                for (kind, *key) in _entries_used(model, x) | used_star:   # the scenario stays within b
                    pass
                assert _max_entry_difference(model, scenario) <= b
            outcomes[truth] += 1
    assert outcomes[True] >= 20 and outcomes[False] >= 20


def _max_entry_difference(a, b):
    worst = max(abs(int(u) - int(v)) for ua, ub in zip(a.unary, b.unary) for u, v in zip(ua, ub))
    for key in a.pair:
        ta, tb = a.pair_table(*key), b.pair_table(*key)
        worst = max(worst, max(abs(int(u) - int(v)) for ra, rb in zip(ta, tb) for u, v in zip(ra, rb)))
    return worst


def test_no_sampled_scenario_beats_a_necessarily_optimal_configuration():
    from metricchain_sb.model import PairModel
    from metricchain_sb.stability import certify_necessary_optimality
    rng = random.Random(41)
    checked = 0
    for seed in range(60):
        model = random_pair_model(seed, n=4, kmax=3, density=1.0, scale_bits=0, amplitude=60, kmin=2)
        x_star = certify_gmec(model, eps=Fraction(0)).witness
        if not certify_necessary_optimality(model, x_star, 2).holds:
            continue
        checked += 1
        for _ in range(30):
            unary = [[int(v) + rng.randint(-2, 2) for v in u] for u in model.unary]
            pair = {k: [[int(v) + rng.randint(-2, 2) for v in row] for row in model.pair_table(*k)] for k in model.pair}
            scenario = PairModel(unary, pair, scale_bits=0)
            best, _ = brute_force_min(scenario)
            assert scenario.energy_int(x_star) == best
    assert checked >= 10


def test_entrywise_error_bounds_can_differ_from_entry_to_entry():
    from metricchain_sb.stability import shifted_model
    model = random_pair_model(3, n=3, kmax=3, density=1.0, scale_bits=0, amplitude=10, kmin=2)
    x_star = certify_gmec(model, eps=Fraction(0)).witness
    b_unary = [[i + a for a in range(k)] for i, k in enumerate(model.sizes)]
    b_pair = {key: [[1 + a + 2 * c for c in range(model.sizes[key[1]])] for a in range(model.sizes[key[0]])]
              for key in model.pair}
    shifted = shifted_model(model, x_star, (b_unary, b_pair))
    for i, k in enumerate(model.sizes):
        for a in range(k):
            sign = 1 if a == x_star[i] else -1
            assert int(shifted.unary[i][a]) == int(model.unary[i][a]) + sign * b_unary[i][a]
    for (i, j) in model.pair:
        for a in range(model.sizes[i]):
            for c in range(model.sizes[j]):
                sign = 1 if (a, c) == (x_star[i], x_star[j]) else -1
                assert int(shifted.pair_table(i, j)[a][c]) == int(model.pair_table(i, j)[a][c]) + sign * b_pair[(i, j)][a][c]
    with pytest.raises(ValueError):
        shifted_model(model, x_star, -1)
