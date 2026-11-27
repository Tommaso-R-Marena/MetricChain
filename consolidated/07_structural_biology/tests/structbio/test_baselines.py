"""Baselines are *uncertified* solvers used for comparison and as independent oracles."""
import pytest

from metricchain_sb.model import brute_force_min
from metricchain_sb.synthetic import random_pair_model

pytoulbar2 = pytest.importorskip("pytoulbar2")


def test_toulbar2_minimum_equals_exhaustive_enumeration():
    from metricchain_sb.baselines.toulbar2 import solve_gmec
    for seed in range(15):
        model = random_pair_model(seed, n=5, kmax=4, density=0.8, scale_bits=3)
        emin, _ = brute_force_min(model)
        result = solve_gmec(model)
        assert result.energy_int == emin
        assert model.energy_int(result.x) == emin
        assert result.seconds >= 0


def test_contact_model_generator_is_deterministic_and_has_the_documented_structure():
    import numpy as np
    from metricchain_sb.synthetic import random_contact_model
    a = random_contact_model(seed=7, n=12, kmax=5)
    b = random_contact_model(seed=7, n=12, kmax=5)
    c = random_contact_model(seed=8, n=12, kmax=5)
    assert a.sizes == b.sizes and all(np.array_equal(x, y) for x, y in zip(a.unary, b.unary))
    assert all(np.array_equal(a.pair[k], b.pair[k]) for k in a.pair)
    assert any(not np.array_equal(a.unary[i], c.unary[i]) for i in range(12) if a.sizes[i] == c.sizes[i]) or a.sizes != c.sizes
    assert len(a.pair) == 12 * 11 // 2                       # every pair has a table (no cutoff)
    assert all(int(u[0]) == 0 for u in a.unary)              # state 0 is the reference state
    strong = set(map(tuple, a.meta["strong_pairs"]))
    assert 0 < len(strong) < len(a.pair)
    osc = {k: int(t.max() - t.min()) for k, t in a.pair.items()}
    weakest_strong = min(osc[k] for k in strong)
    strongest_weak = max(osc[k] for k in a.pair if k not in strong)
    assert weakest_strong > strongest_weak                   # a sparse strong graph inside a dense weak one
