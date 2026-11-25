"""Tests of the engineering implementation of Algorithm 2L+ (theory report §11.19; experiment X-005).

Four layers:
  1. the cube tables against the definitions evaluated by brute force (exact integers);
  2. the C kernel against the Python reference implementation on random instances;
  3. numbers published by the theory division (workstream K's stored outputs at theory commit
     63efc69), quoted here as constants with their source: the implementation was written from the
     text of the report, so agreement on these is a test of both;
  4. properties that must hold on every run (the claims of Theorem 11.56 on the mean run), and
     mutations that must break them.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "twolevel"))

from metricchain_eng.twolevel.adversary import Family, Search  # noqa: E402
from metricchain_eng.twolevel.alg2l import (Params, base_family, claimed_exponent, constants, hinted_lower_bound,  # noqa: E402
                                            inner_costs, tau2)
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.meanrun import Instance, Law, _forward_window_max, mean_run, radial_law  # noqa: E402
from metricchain_eng.twolevel.tables import LN2, CubeTables, brute_tables, cube_constants, theta_hint, theta_na  # noqa: E402
import run_search  # noqa: E402


# ------------------------------------------------------------------------------------------------ 1. tables
@pytest.mark.parametrize("m", [1, 2, 3, 5, 8, 13, 21, 34, 60])
@pytest.mark.parametrize("u", [0.25, 1.0, 4.0])
def test_tables_against_brute_force(m, u):
    for eta in (0.05, 0.25, 0.5):
        t, b = CubeTables(m, u), brute_tables(m, u, eta)
        assert np.max(np.abs(t.lball - np.log(np.array(b["ball"], dtype=float)))) < 1e-11
        assert np.max(np.abs(t.lE - np.log(b["E"]))) < 1e-11
        assert np.max(np.abs(t.lT - np.log(b["T"]))) < 1e-11
        assert np.max(np.abs(t.lGt - np.log(b["Gt"]))) < 1e-11
        assert list(t.kappa(eta)) == b["kappa"]
        assert np.max(np.abs(t.lG2(eta) - np.log(b["G2"]))) < 1e-11
    balls = b["ball"]
    for cnt in sorted(set([1, 2, 3, 2 ** m - 1, 2 ** m] + balls + [x + 1 for x in balls if x < 10 ** 7]
                          + [x - 1 for x in balls if 1 < x < 10 ** 7])):
        if not 1 <= cnt <= 2 ** m:
            continue
        exact = min(r for r in range(m + 1) if balls[r] >= cnt)
        lq = math.log(cnt) - m * LN2 if cnt < 2 ** m else 0.0
        l1mq = math.log(2 ** m - cnt) - m * LN2 if cnt < 2 ** m else -math.inf
        assert t.radius(lq, l1mq) == exact
        if 100 * cnt <= 99 * 2 ** m:          # the documented precondition of kball
            assert t.kball(math.log(cnt)) == max(k for k in range(m + 1) if balls[k] <= max(1, cnt))


def test_radius_of_the_whole_cube_is_exact():
    """q = 1 must give radius m: a tail lemma applied at a smaller radius would be the closure gap of D45."""
    m = 5000
    t = CubeTables(m, 1.0)
    assert t.radius(0.0) == m
    assert t.radius(math.log(0.999999)) < m
    # q = 1 - |B(m, c)| / 2^m is indistinguishable from 1 as a logarithm; with ln(1 - q) supplied the radius is exact
    for c in (0, 7, 100, 2000):
        assert t.radius(-1e-300, float(t.lball[c]) - m * LN2) == m - c - 1
    assert t.radius(-1e-300, -math.inf) == m


def test_cube_constants_and_exponents():
    c = cube_constants(1.0)
    assert c.a == pytest.approx(0.11094, abs=5e-6) and c.h == pytest.approx(0.02914, abs=5e-6)     # K_REPORT out_flat_cost_bounded.txt
    assert theta_na(1.0, c.h) == pytest.approx(c.h, abs=1e-9)        # shear law: theta_na(e + R(e)) = R(e) at e = 0
    assert theta_hint(1.0, 0.0) == pytest.approx(c.h)
    assert theta_na(1.0, c.eps_star) == 0.0 and theta_na(1.0, 0.0) == c.a
    assert tau2(1.0)[0] / c.a == pytest.approx(0.5006, abs=2e-4)     # K_REPORT §6.4
    assert tau2(2.0)[0] / cube_constants(2.0).a == pytest.approx(0.5057, abs=2e-4)


def test_forward_window_max():
    rng = np.random.default_rng(0)
    for _ in range(50):
        a = rng.normal(size=int(rng.integers(1, 60)))
        w = int(rng.integers(1, 70))
        want = np.array([a[j:j + w].max() for j in range(a.size)])
        assert np.array_equal(_forward_window_max(a, w), want)


# ------------------------------------------------------------------------------------------------ 2. kernel = reference
def _random_case(rng):
    u = float(rng.choice([0.5, 1.0, 2.0]))
    n = int(rng.choice([24, 60, 150, 400]))
    n_o = int(rng.integers(max(2, n // 5), max(3, 4 * n // 5)))
    n_i = n - n_o
    b = float(rng.choice([0.25, 0.5, 1.0, 3.0]))
    theta = float(rng.choice([0.05, 0.1, 0.5, 2.0, 20.0]))
    rates = sorted(set(float(x) for x in rng.uniform(0.0, 2 * u, size=int(rng.integers(0, 12)))), reverse=True)
    xs = [2 * u * n_i] + [r * n_i for r in rates if b < r * n_i < 2 * u * n_i] + [b]
    P = Params(n=n, n_o=n_o, u=u, lam=float(rng.uniform(0.2, 1.0)), eta=float(rng.choice([0.05, 0.25, 0.5])),
               etap=float(rng.choice([0.05, 0.1, 0.5, 1.0])), theta=theta,
               nu1=float(rng.choice([1.0, max(1.0, 2 * math.exp(u) * n_o / theta)])), b=b, delta=0.05, xs=tuple(xs))
    return P


def _random_instance(rng, P, tabs):
    c = cube_constants(P.u)
    n_o, n_i, u = P.n_o, P.n_i, P.u
    d = np.arange(n_o + 1, dtype=float)
    kind = int(rng.integers(0, 5))
    if kind == 0:
        F = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, size=n_o))])
    elif kind == 1:
        F = np.concatenate([[0.0], np.cumsum(rng.uniform(0, u, size=n_o))])
    elif kind == 2:
        F = u * np.maximum(d, rng.integers(0, n_o))
    elif kind == 3:
        F = -u * np.maximum(rng.integers(0, n_o) - d, 0)
    else:
        F = np.zeros(n_o + 1)
    c_in = float(rng.uniform(-n_i * c.Lambda1, n_i * (u - c.Lambda1)))
    return Instance(radial_law(F, tabs, shift=c_in), psi0=float(F[int(rng.integers(0, n_o + 1))]), t0=u * n_i + c_in)


FIELDS = ("status", "j_stop", "r_close", "npop", "nneg", "lM_last", "lM_max", "lL", "lU", "lA", "min_pop_radius",
          "slack_valid_lower", "slack_valid_upper", "slack_width", "margin_iii", "slack_iv_M", "slack_iv_Mneg",
          "slack_iv_Mbar", "slack_v", "slack_vi", "lcost")


def _same(a, b):
    if isinstance(a, (str, int)):
        return a == b
    if math.isnan(a) or math.isnan(b):
        return math.isnan(a) and math.isnan(b)
    if math.isinf(a) or math.isinf(b):
        return a == b
    return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))


def test_c_kernel_equals_python_reference():
    rng = np.random.default_rng(2026)
    n_runs = 0
    for _ in range(60):
        P = _random_case(rng)
        tabs = CubeTables(P.n_o, P.u)
        harper, enforce = bool(rng.random() < 0.8), bool(rng.random() < 0.8)
        grid = (0.5, 2.0, 8.0)
        ev = Evaluator(P, tabs, harper=harper, enforce_abort=enforce, count_grid=grid)
        for _ in range(3):
            inst = _random_instance(rng, P, tabs)
            for oracle in ("bottom", "top"):
                Rp = mean_run(P, tabs, inst, oracle, C=ev.C, lC=ev.lC, harper=harper, count_grid=grid, enforce_abort=enforce)
                Rc = ev.run(inst, oracle)
                for f in FIELDS:
                    assert _same(getattr(Rp, f), getattr(Rc, f)), (f, getattr(Rp, f), getattr(Rc, f))
                fin = np.isfinite(Rp.lcalls)
                assert np.array_equal(fin, np.isfinite(Rc.lcalls)) and np.allclose(Rp.lcalls[fin], Rc.lcalls[fin], rtol=1e-9, atol=1e-9)
                n_runs += 1
    assert n_runs == 360


# ------------------------------------------------------------------------------------------------ 3. published numbers
# Source: experiments/workstreams/K/out_flat_cost_bounded.txt at theory commit 63efc69 (K_REPORT §6.4).
# (u, n, phi) -> (ln(cost)/n, closing radius, r_dagger, populated levels, negligible levels, ln M_last / n)
PUBLISHED_FLAT = {
    (1.0, 250, 0.85): (0.18840, 76, 39, 1253, 1, 0.08471),
    (1.0, 1000, 0.80): (0.07780, 255, 180, 5003, 223, 0.06706),
    (1.0, 4000, 0.65): (0.06082, 775, 636, 20003, 1042, 0.05804),
    (2.0, 500, 0.75): (0.22513, 64, 23, 5003, 395, 0.20346),
    (2.0, 2000, 0.60): (0.18283, 180, 103, 20003, 1571, 0.16910),
}
PUBLISHED_PLAIN_AND_LOWER = {      # same file: (u, n) -> (plain bracket ln(cost)/n, hinted lower bound /n) at accuracy 0.872
    (1.0, 250): (0.21361, 0.03688), (1.0, 1000): (0.14970, 0.03169), (2.0, 500): (0.44306, 0.10357),
}


@pytest.mark.parametrize("key", sorted(PUBLISHED_FLAT))
def test_published_flat_cost(key):
    u, n, phi = key
    P, _ = run_search.design_params(n, u, phi)
    ev = Evaluator(P)
    flat = Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=u * P.n_i)
    R = ev.run(flat, "bottom")
    cost, r, rdag, npop, nneg, lm = PUBLISHED_FLAT[key]
    assert (R.r_close, ev.C.r_dag, R.npop, R.nneg) == (r, rdag, npop, nneg)
    assert R.lcost / n == pytest.approx(cost, abs=1.5e-5)
    assert R.lM_last / n == pytest.approx(lm, abs=1.5e-5)
    assert ev.C.x_out == pytest.approx(0.872, abs=5e-4)
    assert not R.violations()
    if n <= 1000:                              # the Python reference gives the same record
        Rp = mean_run(P, ev.outer, flat, "bottom", C=ev.C, lC=ev.lC)
        assert Rp.lcost == pytest.approx(R.lcost, rel=1e-12) and (Rp.r_close, Rp.npop, Rp.nneg) == (r, npop, nneg)


@pytest.mark.parametrize("key", sorted(PUBLISHED_PLAIN_AND_LOWER))
def test_published_plain_bracket_and_lower_bound(key):
    u, n = key
    P, _ = run_search.design_params(n, u, 0.5)
    x_out = constants(P, CubeTables(P.n_o, u)).x_out
    ref = run_search.reference_columns(u, n, x_out)
    plain, lower = PUBLISHED_PLAIN_AND_LOWER[key]
    assert ref["plain"] / n == pytest.approx(plain, abs=1.5e-5)
    assert ref["lower"] / n == pytest.approx(lower, abs=1.5e-5)


# Source: experiments/workstreams/K/out_radial_trajectory.txt at 63efc69 (K_REPORT §6.6), u = 0.5, n_o = 1000, oracle "bottom",
# b = 0.5, lambda = 0.5, eta = 0.25, eta' = theta = 0.1:  profile -> (closure, radius, ln M/(n_o a), width, populated, negligible)
PUBLISHED_RADIAL = {
    "flat": ("unpopulated", 430, 0.6431, 1.255, 1001, 1),
    "cone": ("populated", 347, 1.9241, 1.533, 1154, 0),
    "cone slope u/2": ("unpopulated", 388, 1.1692, 1.517, 1057, 0),
    "2-periodic": ("unpopulated", 430, 0.6431, 1.333, 1002, 0),
}


def test_published_radial_trajectories():
    u, n_o = 0.5, 1000
    c = cube_constants(u)
    tabs = CubeTables(n_o, u)
    P = Params(n=n_o, n_o=n_o, u=u, lam=0.5, eta=0.25, etap=0.1, theta=0.1, nu1=2 * math.exp(u) * n_o / 0.1, b=0.5,
               delta=0.05, xs=(0.0,) * 7)
    ev = Evaluator(P, tabs)
    d = np.arange(n_o + 1, dtype=float)
    profiles = {"flat": 0 * d, "cone": u * d, "cone slope u/2": 0.5 * u * d, "2-periodic": (u / 2) * (-1.0) ** d}
    for name, F in profiles.items():
        R = ev.run(Instance(radial_law(F, tabs), psi0=float(F[n_o // 2])), "bottom")
        kind, r, lm, width, npop, nneg = PUBLISHED_RADIAL[name]
        assert (R.status, R.r_close, R.npop, R.nneg) == ("closed-" + kind, r, npop, nneg), name
        assert R.lM_last / (n_o * c.a) == pytest.approx(lm, abs=1.5e-4) and R.width == pytest.approx(width, abs=1.5e-3)
        assert not R.violations()


# ------------------------------------------------------------------------------------------------ 4. claims and mutations
def test_claims_hold_on_random_instances_and_cost_is_below_the_cap():
    rng = np.random.default_rng(7)
    seen = 0
    for _ in range(40):
        P = _random_case(rng)
        tabs = CubeTables(P.n_o, P.u)
        ev = Evaluator(P, tabs, count_grid=(0.5, 2.0, 8.0))
        for _ in range(5):
            inst = _random_instance(rng, P, tabs)
            for oracle in ("bottom", "top"):
                R = ev.run(inst, oracle)
                assert R.violations() == [], (P, R.violations())
                seen += 1
    assert seen == 400


def test_mutation_without_the_harper_term_breaks_a_claim():
    """Without the Harper term in the lower bound, populated levels are left at radii <= r_dagger or the sample
    exceeds its bound (K_REPORT §2.5, mutation "noharper").  The check must be able to see that."""
    broken = 0
    for u, n_o in ((0.5, 1000), (1.0, 1000), (2.0, 1000)):
        tabs = CubeTables(n_o, u)
        P = Params(n=n_o, n_o=n_o, u=u, lam=0.5, eta=0.25, etap=0.1, theta=0.1, nu1=2 * math.exp(u) * n_o / 0.1, b=0.5,
                   delta=0.05, xs=(0.0,) * 7)
        ev = Evaluator(P, tabs, harper=False, enforce_abort=False)
        F = u * np.arange(n_o + 1, dtype=float)
        R = ev.run(Instance(radial_law(F, tabs), psi0=float(F[n_o // 2])), "bottom")
        broken += bool(R.violations())
    assert broken >= 1


def test_wrong_reference_value_is_rejected():
    tabs = CubeTables(40, 1.0)
    P = Params(n=60, n_o=40, u=1.0, lam=0.5, eta=0.25, etap=0.1, theta=0.1, nu1=1.0, b=0.5, delta=0.05, xs=(40.0, 0.5))
    F = np.arange(41, dtype=float)
    with pytest.raises(ValueError):
        Evaluator(P, tabs).run(Instance(radial_law(F, tabs), psi0=500.0, t0=20.0), "bottom")


def test_search_finds_an_instance_worse_than_flat():
    """The finding of X-005 in miniature: at n = 1000, u = 1 and the outer fraction that is best for the flat
    instance (0.8), a radial instance costs e^{0.6 a n} times more than the flat one, and stays below C_max."""
    u, n, phi = 1.0, 1000, 0.8
    c = cube_constants(u)
    P, _ = run_search.design_params(n, u, phi)
    ev = Evaluator(P)
    flat = ev.run(Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=u * P.n_i), "bottom")
    S = Search(Family(ev, k=8, monotone=True), "bottom", "cost")
    res = S.run(budget=0, seed=1)                 # the structured starting points only
    assert flat.lcost / (n * c.a) == pytest.approx(0.701, abs=1e-3)
    assert res.best_value / (n * c.a) > 1.30
    assert res.best_value < ev.lCmax and not res.violations


def test_claimed_exponent_formula():
    """(3.1) of K_REPORT with a fine ladder and phi = 1/2 is close to tau_2; never below the hinted exponent."""
    for u in (0.5, 1.0, 2.0):
        c = cube_constants(u)
        rates = tuple(2 * u * 0.97 ** i for i in range(1, 400))
        t2, phi = tau2(u)
        assert claimed_exponent(u, phi, rates) == pytest.approx(t2, rel=0.03)
        assert all(claimed_exponent(u, p, rates) >= c.h for p in (0.1, 0.3, 0.5, 0.7, 0.9))
        assert hinted_lower_bound(4000, u, 0.872, 0.05) / 4000 >= c.h


# ------------------------------------------------------------------------------------------------ 5. literal simulation
from metricchain_eng.twolevel.simulate import simulate, stable_multinomial  # noqa: E402
import run_sampled  # noqa: E402


def test_stable_multinomial_samples_far_tail_cells():
    """Cells of mass 1e-15 at 2^55 draws: the mean count must be right (numpy's multinomial loses such cells)."""
    rng = np.random.default_rng(5)
    lp = np.log(np.array([0.5, 0.3, 0.2 - 3e-15, 2e-15, 1e-15]))
    tot = np.zeros(5)
    reps = 400
    for _ in range(reps):
        c = stable_multinomial(rng, 2 ** 55, lp)
        assert int(c.sum()) == 2 ** 55
        tot += c
    for cell, mass in ((3, 2e-15), (4, 1e-15)):
        mean, expect = tot[cell] / reps, 2 ** 55 * mass
        assert abs(mean - expect) < 5 * math.sqrt(expect / reps)


@pytest.mark.parametrize("size", [(0.5, 300, 6), (1.0, 120, 6), (2.0, 48, 6)])
def test_literal_runs_agree_with_the_mean_run_and_satisfy_the_claims(size):
    """The step-by-step simulation (random outer sample, deterministic oracle) and the mean-run evaluator share
    only the cube tables.  With the theorem's K the counts concentrate, so both must stop at the same level with
    the same sample size, and ln(evaluations) must agree; every claim of Theorem 11.56 must hold on each run."""
    u, n_o, n_i = size
    P = run_sampled.params(u, n_o, n_i)
    ev = Evaluator(P)
    rng = np.random.default_rng(11)
    profs = run_sampled.profiles(u, n_o, ev.C.r_dag, ev.outer)
    for name in ("flat", "cone", "dip R=1.0 Lambda1 n_o/u", "plateau below r_dag+1, cone above", "random monotone"):
        F = profs[name]
        psi0, t0 = float(F[n_o // 2]), u * n_i
        for oracle in ("bottom", "top"):
            Rm = ev.run(Instance(radial_law(F, ev.outer), psi0=psi0, t0=t0), oracle)
            same_level = 0
            for _ in range(3):
                Rs = simulate(P, ev.outer, ev.C, F, psi0, t0, 0.0, oracle, rng, lC=ev.lC, lCmax=ev.lCmax)
                assert Rs.status.startswith("closed") and Rs.valid and Rs.good_event and Rs.violations == [], (name, oracle, Rs.status, Rs.violations)
                assert abs(Rs.lqueries - Rm.lcost) < 0.75, (name, oracle, Rs.lqueries, Rm.lcost)      # within a factor 2 (one doubling)
                same_level += (Rs.j_stop == Rm.j_stop and abs(math.log(Rs.M_max) - Rm.lM_max) < 1e-9)
            assert same_level >= 2, (name, oracle)


def test_literal_run_with_random_oracle_and_small_K_stays_within_the_width_bound():
    """U <= e^{x_out} L holds whenever the algorithm stops through the closure test, on or off the good event."""
    u, n_o, n_i = 1.0, 120, 6
    P = run_sampled.params(u, n_o, n_i)
    ev = Evaluator(P)
    rng = np.random.default_rng(3)
    F = run_sampled.profiles(u, n_o, ev.C.r_dag, ev.outer)["cone"]
    off_good_event = 0
    for _ in range(20):
        Rs = simulate(P, ev.outer, ev.C, F, float(F[n_o // 2]), u * n_i, 0.0, "random", rng, lC=ev.lC, K_override=15)
        assert Rs.status.startswith("closed") and "width" not in Rs.violations
        off_good_event += not Rs.good_event
    assert off_good_event >= 10          # with K = 15 the Chernoff events of the proof do fail
