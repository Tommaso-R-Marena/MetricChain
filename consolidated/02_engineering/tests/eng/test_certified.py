"""Tests of the certified-cost recursion (``metricchain_eng.twolevel.certified``) and of the driver of X-011."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "twolevel"))

from metricchain_eng.twolevel import certified as cert  # noqa: E402
from metricchain_eng.twolevel.alg2l import constants  # noqa: E402
from metricchain_eng.twolevel.meanrun import lC_max  # noqa: E402
from metricchain_eng.twolevel.tables import cube_constants  # noqa: E402

U = 1.0
A = cube_constants(U).a
LID = math.log(20.0)


def test_vectorised_base_bracket_cost_equals_scalar():
    rng = np.random.default_rng(7)
    for d in (50, 137, 1000, 3000):
        for lid in (3.0, 40.0, 900.0):
            xs = np.concatenate([rng.uniform(0.3, 2.5, 15), rng.uniform(2.0, 2 * d, 40), [4 * math.atanh(0.5), 2.2]])
            v = cert.k0_lcost_vec(d, U, xs, lid)
            s = np.array([cert.k0_lcost(d, U, float(x), lid)[0] for x in xs])
            assert np.array_equal(v, s)


def test_base_bracket_cost_is_the_one_of_the_three_level_driver():
    import three_levels

    for d, x, lid in ((600, 5.0, 30.0), (600, 300.0, 30.0), (2400, 0.5, 200.0), (60, 100.0, 5.0)):
        assert cert.k0_lcost(d, U, x, lid)[0] == three_levels.k0_flat(d, U, x, lid)[0]


@pytest.mark.parametrize("n,phi,two,three", [(1000, 0.5, 1.1384, 1.1384), (4000, 0.375, 0.8553, 0.6106), (4000, 0.5, 0.7262, 0.7261)])
def test_published_certified_bounds(n, phi, two, three):
    """Theory branch, experiments/coordinator_checks/three_levels_certified (out_4000.txt and README), u = 1."""
    R = cert.Recursion(U, "searched")
    D = cert.top_design(phi)
    assert abs(R.top(n, D, LID, 1).lCmax / (n * A) - two) < 6e-5
    assert abs(R.top(n, D, LID, 2).lCmax / (n * A) - three) < 6e-5


@pytest.mark.parametrize("n,phi", [(1000, 0.5), (1400, 0.45), (4000, 0.375), (4000, 0.3)])
def test_pruned_search_equals_plain_recursion(n, phi):
    """Same candidate lists (cert3's descent replaced by the full list in both): the pruned search must return the
    same minimum as the recursion that evaluates everything."""
    D = cert.top_design(phi)

    class Plain(cert.Recursion):
        def _best_level(self, d, x, lid, depth, cutoff):
            best = None
            for Dc in cert.theory_candidates(self.u, d, x):
                lb = self._try(d, x, lid, depth, Dc, math.inf)
                if lb is not None and (best is None or lb.lCmax < best.lCmax):
                    best = lb
            return best

    for depth in (1, 2):
        plain = Plain(U, "searched").top(n, D, LID, depth).lCmax
        pruned = cert.Search(U, "theory").top(n, D, LID, depth).lCmax
        assert abs(plain - pruned) < 1e-9 * abs(plain)


def test_search_is_nonincreasing_in_depth_and_consistent():
    n = 2000
    S = cert.Search(U, "theory")
    prev = math.inf
    for depth in (1, 2, 3):
        best = min(S.top(n, cert.top_design(phi), LID, depth).lCmax for phi in (0.5, 0.45, 0.4))
        assert best <= prev + 1e-9
        prev = best
    lb = S.top(n, cert.top_design(0.45), LID, 3)
    # the stored bound is the theorem's formula applied to the stored server costs
    P = cert.level_params(U, n, lb.design, LID)
    C = constants(P, cert.tables(P.n_o, U))
    assert abs(lC_max(P, C, lb.lC) - lb.lCmax) < 1e-9 * lb.lCmax
    # every nested server is certified for the accuracy of its rung and costs no more than the base bracket there
    for l, s in enumerate(lb.servers, start=1):
        if isinstance(s, cert.LevelBound):
            assert s.xout <= lb.xs[l] + 1e-9
            assert s.lCmax < cert.k0_lcost(lb.n_i, U, lb.xs[l], lb.l_inv_delta_p)[0]


def test_cutoff_only_prunes():
    """A cutoff above the value changes nothing; a cutoff below it returns None."""
    n, D = 2000, cert.top_design(0.45)
    S = cert.Search(U, "theory")
    full = S.top(n, D, LID, 2).lCmax
    assert abs(S.top(n, D, LID, 2, cutoff=full + 1.0).lCmax - full) < 1e-9
    assert S.top(n, D, LID, 2, cutoff=full - 1e-6) is None


def test_table_cache_is_bounded_and_transparent():
    old = cert.TABLES_BUDGET
    try:
        v1 = cert.Search(U, "theory").top(1400, cert.top_design(0.45), LID, 2).lCmax
        cert.TABLES_BUDGET = 3000            # forces evictions on every access pattern
        cert._tables.clear()
        cert._k0cache.clear()
        cert._tables_total = 0
        v2 = cert.Search(U, "theory").top(1400, cert.top_design(0.45), LID, 2).lCmax
        assert v1 == v2
        assert sum(k[0] for k in cert._tables) <= 3000 + 1400
    finally:
        cert.TABLES_BUDGET = old
        cert._tables.clear()
        cert._k0cache.clear()
        cert._tables_total = 0


def test_design_run_lies_between_flat_cost_and_bound():
    import nested_bench as nb

    r = nb.instance_cell(U, 1000, 0.5, "theory", 2, budget=120, budget_general=60)
    assert r["flat_ok"]
    assert r["flat_instance"] <= r["worst_flat_fibres"] + 1e-9
    for key in ("worst_flat_fibres", "worst_B", "worst_A"):
        assert r["flat_instance"] - 1e-9 <= r[key] <= r["certified"] + 1e-9
    assert all(s["violations"] == 0 for s in r["searches"])
    assert r["lower_bound"] < r["flat_instance"]


def test_two_level_cells_reproduce_eng_res_0014():
    """ENG-RES-0014, table three_worst, n = 1000 at the outer fraction 0.50: flat 0.9839 (the referee's number too)."""
    import nested_bench as nb

    r = nb.instance_cell(U, 1000, 0.5, "theory", 1, readings=(), budget=10, budget_general=10)
    assert abs(r["flat_instance"] - 0.9839) < 6e-5
    assert abs(r["certified"] - 1.1384) < 6e-5
