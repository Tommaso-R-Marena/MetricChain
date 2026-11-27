"""Tests of the independent check of the theory division's "Theorem R" (rate of the level recursion).

Everything is computed from the mathematical statements (experiments/eng/level_rate/lr_*.py); the reference
numbers marked "theirs" are transcribed from the pinned commit of the theory branch (lr_cases.PINNED).
Default run: about 40 s.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "level_rate"))

import lr_cases as C  # noqa: E402
import lr_lines as LN  # noqa: E402
import lr_multiletter as ML  # noqa: E402
import lr_pairs as P  # noqa: E402
import lr_recursion as R  # noqa: E402
import run_propU as PU  # noqa: E402

GAUSS = P.GaussPair()
CUBE = P.cube(1.0)
THETA_SMALL = {}


def theta_tab(pair, n=20000):
    key = (pair.name, n)
    if key not in THETA_SMALL:
        THETA_SMALL[key] = R.build_theta(pair, n)
    return THETA_SMALL[key]


# ---------------------------------------------------------------------------------------------------------------
# closed forms
# ---------------------------------------------------------------------------------------------------------------
def test_cube_constants_three_ways():
    """Game function, Kullback-Leibler formulas of 11.16, and the numbers of the report (u = 1)."""
    kl = P.CubeKL(1.0)
    assert CUBE.a == pytest.approx(kl.a, rel=1e-13)
    assert CUBE.h == pytest.approx(kl.h, rel=1e-13)
    assert CUBE.E == pytest.approx(kl.E, rel=1e-13)
    assert CUBE.L == pytest.approx(math.log((1 - kl.rho_h) / kl.rho_h) / 1.0, rel=1e-13)
    assert CUBE.vartheta == pytest.approx(kl.hint2, rel=1e-12)             # 1/(u^2 rho_h (1 - rho_h))
    assert CUBE.constant == pytest.approx(kl.constant, rel=1e-12)
    th = C.THEIRS["cube_u1"]
    assert CUBE.constant == pytest.approx(th["constant"], abs=5e-8)         # theirs: 0.0711473
    assert CUBE.constant / CUBE.a == pytest.approx(th["constant_over_a"], abs=5e-6)   # theirs: 0.64129 a
    assert CUBE.h == pytest.approx(th["h"], abs=5e-9) and CUBE.a == pytest.approx(th["a"], abs=5e-9)
    assert CUBE.L == pytest.approx(th["L"], abs=5e-7) and CUBE.vartheta == pytest.approx(th["vartheta"], abs=1.5e-6)


def test_theta_na_curve_against_kl_definition_and_shear_law():
    kl = P.CubeKL(1.0)
    x = np.array([1e-9, 1e-6, 1e-3, 0.01, 0.05, 0.1, 0.119])
    assert np.allclose(CUBE.theta_na(x), kl.theta_na(x), rtol=0, atol=1e-13)
    e = np.array([0.0, 0.01, 0.05, 0.1])
    assert np.allclose(CUBE.theta_hint(e), kl.theta_hint(e), rtol=0, atol=1e-14)
    # (11.18.1): theta_na(e + theta_hint(e)) = theta_hint(e); in particular theta_na(h) = h
    assert np.allclose(kl.theta_na(e + kl.theta_hint(e)), kl.theta_hint(e), rtol=0, atol=1e-14)
    assert float(CUBE.theta_na(np.array(CUBE.h))) == pytest.approx(CUBE.h, abs=1e-15)


def test_gauss_pair():
    x = np.array([0.0, 0.01, 0.25, 0.7, 1.0, 2.0])
    xc, thc = GAUSS.curve(np.array([0.3, 0.5, 0.9]))
    assert np.allclose(thc, (1 - np.sqrt(xc)) ** 2, atol=1e-15)
    assert np.allclose(GAUSS.theta_na(x), np.where(x < 1, (1 - np.sqrt(np.minimum(x, 1))) ** 2, 0))
    assert GAUSS.constant == pytest.approx(math.pi**2 / 16, rel=1e-14)
    assert (GAUSS.h, GAUSS.L, GAUSS.vartheta, GAUSS.a) == pytest.approx((0.25, 0.5, 0.5, 1.0))
    for t in (0.1, 0.5, 0.8):                     # J(t) = t - t^2 from theta_na itself
        assert GAUSS.dual_J_from_theta(t) == pytest.approx(t - t * t, abs=1e-12)


@pytest.mark.parametrize("pair", [CUBE, P.product2(2.0, 0.5, 0.25), P.biased_cube(0.3, 1.0)], ids=lambda p: p.name)
def test_vartheta_from_theta_na_itself(pair):
    """vartheta = -1/F''(L) = theta''(h)/(1 + |theta'(h)|)^3 = theta_hint''(0), by finite differences."""
    h, L = pair.h, pair.L
    e = 2e-4 * h
    th = pair.theta_na(np.array([h - 2 * e, h - e, h, h + e, h + 2 * e]))
    d1 = (th[3] - th[1]) / (2 * e)
    d2 = (-th[4] + 16 * th[3] - 30 * th[2] + 16 * th[1] - th[0]) / (12 * e * e)
    assert th[2] == pytest.approx(h, abs=1e-14)
    assert d1 == pytest.approx(-L / (1 - L), rel=1e-6)
    assert d2 / (1 + abs(d1)) ** 3 == pytest.approx(pair.vartheta, rel=1e-5)
    hh = pair.theta_hint(np.array([0.0, e, 2 * e]))
    assert (hh[2] - 2 * hh[1] + hh[0]) / (e * e) == pytest.approx(pair.vartheta, rel=2e-3)
    assert (hh[1] - hh[0]) / e == pytest.approx(-L, rel=1e-3)


def test_product_game_function_is_the_formula_of_theorem_11_98():
    pr = P.product2(4.0, 1.0, 0.25)
    for t in (0.1, 0.37, 0.5, 0.93):
        tot = 0.0
        for lam, u in ((0.25, 4.0), (0.75, 1.0)):
            p = 1 / (1 + math.exp(u))
            tot += lam * ((1 - t) * math.log(2) - math.log(p**t + (1 - p) ** t))
        assert float(pr.F(np.array(t))) == pytest.approx(tot, rel=1e-13)
        assert float(pr.F_mp(t)) == pytest.approx(tot, rel=1e-13)
    # a and E add over site types (Theorem 11.98(c))
    assert pr.a == pytest.approx(0.25 * P.cube(4.0).a + 0.75 * P.cube(1.0).a, rel=1e-13)
    assert pr.E == pytest.approx(0.25 * P.cube(4.0).E + 0.75 * P.cube(1.0).E, rel=1e-13)
    # derivative and second derivative
    t = np.array([0.2, 0.6])
    eps = 1e-6
    assert np.allclose((pr.F(t + eps) - pr.F(t - eps)) / (2 * eps), pr.dF(t), rtol=1e-8)
    assert np.allclose((pr.dF(t + eps) - pr.dF(t - eps)) / (2 * eps), pr.d2F(t), rtol=1e-7)
    assert float(pr.constants()["d2"]) == pytest.approx(float(pr.d2F(np.array(pr.L))), rel=1e-12)


def test_biased_site_renyi_form_against_cosh_form():
    """Two formulas of the report for the biased cube: Theorem 11.99 (Renyi capacity, in closed form here)
    and Theorem 11.59(b) maximised over the residual field."""
    for p, u in ((0.3, 1.0), (0.1, 2.0)):
        for t in (0.2, 0.5, 0.8):
            f_float, _ = P._biased_terms(p, u, np.array(t))
            f_cosh = P.biased_F_cosh(p, u, t)
            assert float(f_float) == pytest.approx(float(f_cosh), rel=1e-12)
            assert float(P._mp_biased(p, u, t)) == pytest.approx(float(f_cosh), rel=1e-12)
    b = P.biased_cube(0.3, 1.0)
    # THEORY_REPORT 11.26, worked example "bin" (pi = (0.7, 0.3), u = 1): E, a, h
    assert (b.E, b.a, b.h) == pytest.approx((0.103131, 0.095301, 0.025034), abs=6e-7)
    # F' of the double-precision formula against mpmath
    for t in (1e-6, 0.3, 0.9, 1 - 1e-7):
        _, d = P._biased_terms(0.3, 1.0, np.array(t))
        assert float(d) == pytest.approx(float(mp.diff(lambda s: P._mp_biased(0.3, 1.0, s), t)), abs=1e-13)
    # p = 1/2 is the symmetric site
    f_half, _ = P._biased_terms(0.5, 1.3, np.array([0.3, 0.7]))
    assert np.allclose(f_half, P._sym_terms(1.3, np.array([0.3, 0.7]))[0], rtol=1e-13)


def test_biased_cube_vartheta_differs_from_the_theory_divisions_value():
    """A finding of this check, pinned as a test: for the biased cube p = 0.3, u = 1 the second derivative of
    F* at its maximum from two independent closed forms gives vartheta = 4.93944, where the theory division's
    output file prints 4.954673 (0.3 % larger)."""
    b = P.biased_cube(0.3, 1.0)
    old = mp.mp.dps
    mp.mp.dps = 30
    try:
        d2_cosh = mp.diff(lambda s: P.biased_F_cosh(0.3, 1.0, s, dps=30), b.constants()["L"], 2, h=mp.mpf("1e-5"))
    finally:
        mp.mp.dps = old
    assert float(-1 / d2_cosh) == pytest.approx(b.vartheta, rel=1e-8)
    assert b.vartheta == pytest.approx(4.939435, abs=2e-6)
    assert abs(b.vartheta / C.THEIRS["biased_p0.3_u1"]["vartheta"] - 1) > 2.5e-3


# ---------------------------------------------------------------------------------------------------------------
# the slope map and the lines
# ---------------------------------------------------------------------------------------------------------------
def test_slope_map_two_routes_and_gauss_closed_form():
    for B, s in ((0.3, 0.1), (0.26, 0.45), (0.25, 0.5), (0.4, 0.0)):
        sig = float(LN.sigma_dual(GAUSS, B, s)[0])
        assert sig == pytest.approx(B * (1 - s) / (1 - s - B), rel=1e-13)       # R_REPORT section 2
        assert LN.sigma_def(GAUSS, B, s) == pytest.approx(sig, rel=1e-10)
    pr = P.product2(2.0, 0.5, 0.5)
    rng = np.random.default_rng(3)
    for pair in (CUBE, pr):
        for _ in range(6):
            s = rng.uniform(0, 0.6)
            B = rng.uniform(0.2, 0.95) * (1 - s) * pair.a
            sig = float(LN.sigma_dual(pair, B, s)[0])
            assert LN.sigma_def(pair, B, s) == pytest.approx(sig, rel=1e-9)
    # irregular points
    assert not np.isfinite(LN.sigma_dual(GAUSS, 0.7, 0.4)[0])
    # fixed point with multiplier one at (h, L)
    assert float(LN.sigma_dual(CUBE, CUBE.h, CUBE.L)[0]) == pytest.approx(CUBE.L, abs=1e-7)


def test_gauss_exact_lower_bounds_reproduce_the_reports_numbers():
    th = C.THEIRS["gauss"]
    for k in (2, 3, 10, 40):
        n = LN.gauss_exact(k)
        assert n == th["exact_lb_1e9"][k]
        assert LN.gauss_survives_exact(Fraction(n, 10**9), k)
        assert not LN.gauss_survives_exact(Fraction(n + 1, 10**9), k)
    for k, r in ((10, 1.0151), (40, 1.0010)):
        b = Fraction(th["exact_lb_1e9"][k], 10**9)
        assert float((k + 0.5) ** 2 * (b - Fraction(1, 4))) / (math.pi**2 / 16) >= r


def test_gauss_closed_form_of_section_10():
    assert float(LN.gauss_closed_form_root(2)) == pytest.approx((3 - math.sqrt(5)) / 2, rel=1e-14)
    for k in (3, 7, 40, 160):
        assert LN.b_inf(GAUSS, k) == pytest.approx(float(LN.gauss_closed_form_root(k)), rel=1e-13)
    # ... and its expansion 1/4 + (pi^2/16)/(k + 1/2)^2 (1 + O(k^-2))
    k = 2000
    assert (k + 0.5) ** 2 * (float(LN.gauss_closed_form_root(k, 40)) - 0.25) == pytest.approx(math.pi**2 / 16, rel=1e-6)


def test_cube_lines_reproduce_the_reports_numbers_and_are_certified():
    th = C.THEIRS["cube_u1"]["lines_lb"]
    for k in (2, 3, 10, 40):
        assert LN.b_inf(CUBE, k) == pytest.approx(th[k], abs=6e-11)
    assert LN.b_inf(CUBE, 1) == CUBE.a
    # mpmath agrees with double precision
    assert float(LN.b_inf_mp(CUBE, 10, dps=30, digits=14)) == pytest.approx(LN.b_inf(CUBE, 10), rel=1e-13)
    # interval arithmetic: the 10-decimal value of the report is proved, the next decimal is not provable
    assert LN.certify_lower(CUBE, "0.0297934159", 10)
    assert not LN.certify_lower(CUBE, "0.0297934160", 10)


def test_passage_time_of_lemma_PT():
    cstar = math.pi * GAUSS.h * math.sqrt(2 * GAUSS.vartheta)
    for e, ref in ((1e-2, 0.764), (1e-3, 0.906), (1e-4, 0.968)):        # theirs
        n = LN.passage_time(GAUSS, e * GAUSS.h, GAUSS.L + 0.05)
        assert math.sqrt(e * GAUSS.h) * n / cstar == pytest.approx(ref, abs=6e-4)


# ---------------------------------------------------------------------------------------------------------------
# the recursion
# ---------------------------------------------------------------------------------------------------------------
def test_tau2_closed_forms():
    assert R.tau2_closed(GAUSS) == pytest.approx(0.5, abs=1e-12)
    t2 = R.tau2_closed(CUBE)
    assert t2 / CUBE.a == pytest.approx(0.50041, abs=5e-6)                  # theirs: 0.5004 a ("0.500 a")
    ub = R.ConvexUpperBound(CUBE, N=600, theta=theta_tab(CUBE))
    ub.step()
    assert ub.M[0] == pytest.approx(t2, rel=2e-6) and ub.M[0] >= t2 - 1e-12      # an upper bound, and close


def test_upper_bound_and_lines_sandwich_gauss():
    ub = R.ConvexUpperBound(GAUSS, N=600, theta=theta_tab(GAUSS))
    prev = ub.M[0]
    for k in range(2, 9):
        rec = ub.step()
        assert rec["n_above"] == 0                                           # R1[M_k] <= M_k on the grid
        assert rec["n_hull"] == ub.N + 1                                     # the raw values are convex
        assert rec["tau"] <= prev + 1e-12
        prev = rec["tau"]
        assert LN.b_inf(GAUSS, k) <= rec["tau"]                              # lower bound <= upper bound
        if k in (3, 6):
            # Proposition A: every line B - p_k(B) x with p_k(B) finite lies below T_k, hence below M_k
            for B in np.linspace(0.02, 0.999 * LN.b_inf(GAUSS, k), 25):
                pk = LN.orbit(GAUSS, float(B), k)[-1]
                assert np.isfinite(pk)
                assert np.all(ub.M[:-1] >= B - pk * ub.x[:-1] - 1e-9)
    taus = ub.taus()
    assert taus[2] == pytest.approx(0.5, abs=1e-9)
    assert 0.3552 < taus[3] < 0.35524                 # below the theory division's grid value 0.35593
    assert taus[3] < C.THEIRS["gauss"]["grid_recursion"][3] - 5e-4
    assert taus[3] > 1 / (2 * math.sqrt(2))           # R_REPORT section 5, remark (2): tau_3 >= 1/(2 sqrt 2)


def test_cube_three_levels():
    ub = R.ConvexUpperBound(CUBE, N=800, theta=theta_tab(CUBE))
    ub.run(4)
    t = ub.taus()
    assert 0.3611 < t[3] / CUBE.a < 0.3613            # theirs: tau_3 = 0.361 a
    assert 0.3106 < t[4] / CUBE.a < 0.3108            # theirs: 0.311 a
    assert LN.b_inf(CUBE, 3) < t[3] and LN.b_inf(CUBE, 4) < t[4]


def test_general_recursion_agrees_with_convex_upper_bound():
    """The recursion without structural assumptions against the convex scheme on the same grid."""
    th = theta_tab(GAUSS)
    gen = R.GeneralRecursion(GAUSS, N=120, theta=th, p_grid=np.arange(-30.0, 30.01, 1.0),
                             q_grid=np.arange(-30.0, 10.01, 1.0))
    ub = R.ConvexUpperBound(GAUSS, N=120, theta=th)
    for k in range(2, 4):
        rg = gen.step()
        ub.step()
        d = gen.T - ub.M
        assert d.max() <= 1e-9 and d.min() >= -2e-4            # chords above the sqrt-interpolant, never below
        assert rg["S_quasiconvex_in"]
        assert rg["frac_regime2_among_improved"] == 0.0
        assert rg["scan_minus_balance_min"] >= -1e-6           # the blind search finds nothing lower
        assert rg["max_concavity_in"] <= 1e-9
    assert gen.T[0] == pytest.approx(ub.M[0], abs=2e-5)        # tau_3 on a coarse grid (N = 120)


def test_hinted_exponent_is_a_fixed_point():
    """Theorem 11.53(b): R[theta_hint] = theta_hint.  Here: R1 of the chords of theta_hint on a grid."""
    for pair in (GAUSS, CUBE):
        ub = R.ConvexUpperBound(pair, N=2000, theta=theta_tab(pair))
        M = np.asarray(pair.theta_hint(ub.x), dtype=float)
        M[-1] = 0.0
        ub.Mf.set(M)
        g = pair.E * np.array([0.01, 0.1, 0.3, 0.6, 0.9])
        r, _ = ub.apply(g)
        assert np.all(np.abs(r - pair.theta_hint(g)) <= 2e-6 * pair.a)
        v0, _ = ub.apply_zero()
        assert v0 == pytest.approx(pair.h, abs=2e-6 * pair.a)


def test_tent_pair_converges_in_one_level():
    """F(t) = h (1 - |2t - 1|): theta(x) = 2h - x, theta_hint(e) = h - e/2, and R[theta] = theta_hint exactly
    (hand computation: H1 = (1 - phi) a for every admissible phi <= (a + g)/(2a))."""

    class Tent:
        name = "tent"
        a, E, h = 0.5, 0.5, 0.25

        def theta_na(self, x):
            return np.maximum(0.5 - np.asarray(x, dtype=float), 0.0)

    ub = R.ConvexUpperBound(Tent(), N=1000, n_theta=1000)
    ub.step()
    assert np.all(np.abs(ub.M - np.maximum(0.25 - ub.x / 2, 0.0)) <= 1e-9)
    assert ub.M[0] == pytest.approx(0.25, abs=1e-9)


def test_proposition_U_on_random_convex_slope_functions():
    rng = np.random.default_rng(7)
    th = theta_tab(GAUSS)
    for _ in range(4):
        res = PU.prop_u_case(GAUSS, th, rng, N=3000)
        assert np.max(res["r"] - res["U"]) <= 2e-4            # Proposition U (up to the grid)
        assert np.min(res["r"] - res["Llow"]) >= -1e-9        # Lemma L


def test_kinked_pair_has_rate_one_over_k():
    """Proposition K of R_REPORT: tau_k - 1/4 >= 1/(16 (k + 2)) for theta = max(1 - 3e, 1/2 - e, 0)."""
    kp = P.KinkedPair()
    for k in (2, 5, 20):
        assert LN.b_inf(kp, k) - 0.25 >= 1 / (16 * (k + 2)) - 1e-12


def test_uniform_hamming_site_is_a_maximum_of_concave_branches():
    """F* = max_s Phi_s for q equally likely letters (lr_multiletter.py): the numbers of THEORY_REPORT 11.26,
    Proposition 11.103(b), (d), (e), and the Renyi programme of Theorem 11.99 solved over all vertices."""
    s3, s4 = ML.UniformHammingSite(3, 1.0, n_grid=2001), ML.UniformHammingSite(4, 1.0, n_grid=2001)
    assert (s3.h, s3.E, s3.a) == pytest.approx((0.03065363, 0.119499, 0.123284), abs=6e-7)
    assert (s4.h, s4.a, s4.E) == pytest.approx((0.029139, 0.117993, 0.120115), abs=6e-7)
    assert s4.h == pytest.approx(CUBE.h, rel=1e-13)              # h = h_2: pairs of letters, i.e. the cube
    assert float(s4.Fstar(np.array(0.3))) == pytest.approx(ML.renyi_direct(4, 1.0, 0.3, restarts=2), abs=1e-10)
    # the branches of single letters and of pairs cross, so F* is not concave and theta_na has a kink
    t = np.linspace(0.01, 0.99, 197)
    d = s4.parts[0].F(t) - s4.parts[1].F(t)
    assert d.min() < 0 < d.max()
    assert s4.envelope_differs
    # at u = 1 the maximum is on the branch of pairs and is quadratic there: (H1) holds with the cube's constants
    assert s4.branch_h[1] > s4.branch_h[0] > s4.branch_h[2]
    # at e^u = 3 the two branches are mirror images, Phi_1(t) = Phi_2(1 - t): two maximisers, J is flat between
    # them, theta_na has a kink at h and hypothesis (H1) of Theorem R fails
    u3 = math.log(3.0)
    p1, p2 = ML.SubsetDip(4, 1, u3), ML.SubsetDip(4, 2, u3)
    assert np.allclose(p1.F(t), p2.F(1 - t), rtol=0, atol=1e-15)
    assert p1.h == pytest.approx(p2.h, rel=1e-13) and p1.L + p2.L == pytest.approx(1.0, abs=1e-12)
    crit = ML.UniformHammingSite(4, u3, n_grid=4001)
    la, lb = crit.flat_top(1e-9)
    assert la == pytest.approx(p2.L, abs=2e-3) and lb == pytest.approx(p1.L, abs=2e-3) and lb - la > 0.02
    for k in (5, 20):                                   # Proposition K: tau_k - h >= (L_b - L_a) h/(k + 2)
        assert LN.b_inf(crit, k) - crit.h >= (p1.L - p2.L) * crit.h / (k + 2) * (1 - 1e-3)


def test_result_files_are_consistent_with_the_code():
    """If results have been produced, re-compute a few of their numbers."""
    path = C.RES / "lines_cube_u1.json"
    if not path.exists():
        pytest.skip("results not produced")
    res = C.load("lines_cube_u1.json")
    assert res["pinned_theory_commit"] == C.PINNED
    for k in (2, 7, 33):
        assert float(res["lines"][str(k)]["B"]) == pytest.approx(LN.b_inf(CUBE, k), rel=1e-12)
    assert float(res["constants"]["constant"]) == pytest.approx(CUBE.constant, rel=1e-12)
