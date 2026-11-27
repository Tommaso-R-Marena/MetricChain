"""Tests of the block-heterogeneous certified recursion (``metricchain_eng.twolevel.hetero``, experiment X-014)."""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel import certified as cert  # noqa: E402
from metricchain_eng.twolevel import hetero as H  # noqa: E402
from metricchain_eng.twolevel.alg2l import constants as hom_constants  # noqa: E402
from metricchain_eng.twolevel.alg2l import hinted_lower_bound  # noqa: E402
from metricchain_eng.twolevel.tables import cube_constants  # noqa: E402

LID = math.log(20.0)


@pytest.mark.parametrize("u,n,phi", [(1.0, 1000, 0.5), (1.0, 4000, 0.375), (2.0, 2000, 0.4), (0.5, 3000, 0.3)])
def test_one_type_is_the_homogeneous_theory(u, n, phi):
    B = H.make_block([(u, n)])
    k = cert.split(n, phi)[0]
    C = H.constants(B, H.top_design(0, k), LID)
    P = cert.level_params(u, n, cert.top_design(phi), LID)
    C0 = hom_constants(P, cert.tables(P.n_o, u))
    assert (C.J, C.K) == (C0.J, C0.K)
    for a, b in ((C.lM_bar, C0.lM_bar), (C.x_out, C0.x_out), (C.l_inv_delta_p, C0.l_inv_delta_p)):
        assert abs(a - b) < 1e-12
    for depth in (1, 2):
        a = H.HSearch().top(B, H.top_design(0, k), LID, depth).lCmax
        b = cert.Search(u, "wide").top(n, cert.top_design(phi), LID, depth).lCmax
        assert abs(a - b) < 1e-9 * abs(b)
    assert abs(H.hinted_lower_bound(B, 0.8715, 0.05)["lbound"] - hinted_lower_bound(n, u, 0.8715, 0.05)) < 1e-9 * n
    asy = H.asymptotic(B)
    cc = cube_constants(u)
    assert abs(asy["h"] - cc.h) < 1e-10 and abs(asy["a"] - cc.a) < 1e-12


def test_block_bookkeeping():
    B = H.make_block([(0.5, 3), (2.0, 4), (0.5, 2)])
    assert B == ((2.0, 4), (0.5, 5)) and H.dim(B) == 9 and abs(H.omega(B) - 10.5) < 1e-12
    assert H.remove(B, 0, 4) == ((0.5, 5),) and H.remove(B, 1, 2) == ((2.0, 4), (0.5, 3))
    with pytest.raises(ValueError):
        H.remove(B, 0, 5)
    assert abs(H.l2p(B) - (4 * math.log(2 / (1 + math.exp(2.0))) + 5 * math.log(2 / (1 + math.exp(0.5))))) < 1e-12
    # never the whole block as outer block; whole types are offered
    ch = H.outer_choices(B)
    assert all(0 < k < H.dim(B) and k <= B[j][1] for j, k in ch) and (0, 4) in ch and (1, 5) in ch


@pytest.mark.parametrize("eps", [0.05, 0.5, 2.0])
def test_lower_bound_by_brute_force(eps):
    """The smallest dip {d_u < rho} whose excess exceeds e^eps - 1, by a scan of rho over all points of a small cube."""
    B = H.make_block([(1.3, 5), (0.4, 6)])
    n = H.dim(B)
    us = np.array([1.3] * 5 + [0.4] * 6)
    d = np.array(list(itertools.product((0, 1), repeat=n))) @ us
    sizes = []
    for rho in np.linspace(1e-6, d.max() + 1, 20001):
        inside = d < rho
        if np.sum(np.exp(rho - d[inside]) - 1) / 2 ** n > math.expm1(eps):
            sizes.append(int(inside.sum()))
    brute = math.log(0.9) + n * math.log(2) - math.log(min(sizes))
    assert abs(H.hinted_lower_bound(B, eps, 0.05)["lbound"] - brute) < 1e-9


def test_dip_is_in_the_class_and_has_the_stated_excess():
    """f_c(x) = -(rho - d_u(x, c))_+ is u-Lipschitz coordinate by coordinate, vanishes outside the dip, and raises the
    average of e^-f by exactly the excess the bound uses."""
    us = np.array([1.3, 1.3, 0.4, 0.4, 0.4, 0.9])
    n = len(us)
    X = np.array(list(itertools.product((0, 1), repeat=n)))
    c = X[37]
    d = np.abs(X - c) @ us
    for rho in (0.5, 1.7, 3.0):
        f = -np.maximum(rho - d, 0.0)
        idx = {tuple(x): i for i, x in enumerate(X)}
        for i, x in enumerate(X):
            for s in range(n):
                y = x.copy()
                y[s] ^= 1
                assert abs(f[i] - f[idx[tuple(y)]]) <= us[s] + 1e-12
        assert np.all(f[d >= rho] == 0)
        excess = np.mean(np.exp(-f)) - 1
        assert abs(excess - np.sum(np.exp(rho - d[d < rho]) - 1) / 2 ** n) < 1e-12


def test_asymptotic_exponent_shares_one_slope():
    B = H.make_block([(2.0, 1), (0.5, 3)])
    asy = H.asymptotic(B)
    # h = max_t sum lambda F_j(t) <= sum lambda max_t F_j(t)
    assert asy["h"] <= asy["h_average"] + 1e-12
    grid = np.linspace(0, 1, 20001)
    brute = max(0.25 * H.site_F(2.0, t) + 0.75 * H.site_F(0.5, t) for t in grid)
    assert abs(asy["h"] - brute) < 1e-9
    assert abs(asy["a"] - (0.25 * cube_constants(2.0).a + 0.75 * cube_constants(0.5).a)) < 1e-12


def test_type_aligned_bound_is_consistent_and_beats_inclusion_on_a_mixed_block():
    B = H.make_block([(2.0, 500), (0.5, 1500)])
    n = H.dim(B)
    S = H.HSearch()
    best = None
    for j, k in H.outer_choices(B):
        hb = S.top(B, H.top_design(j, k), LID, 2, cutoff=best.lCmax if best else math.inf)
        if hb is not None:
            best = hb
    hom = min(cert.Search(2.0, "wide").top(n, cert.top_design(phi), LID, 2).lCmax for phi in (0.4, 0.3, 0.25))
    assert best.lCmax < hom                                        # the homogeneous algorithm with u_max is admissible, and worse
    assert best.lCmax > H.hinted_lower_bound(B, best.xout, 0.05)["lbound"]      # and nothing is below the lower bound
    assert abs(best.xout - 0.8715) < 1e-3
    # the stored bound is the theorem's formula applied to the stored server costs
    C = best.C
    terms = np.concatenate([[0.0, math.log(2) + C.lM_bar], C.lmult() + best.lC[1:]])
    assert abs(np.logaddexp.reduce(terms) - best.lCmax) < 1e-9 * best.lCmax
    for l, s in enumerate(best.servers, start=1):
        if isinstance(s, H.HBound):
            assert s.xout <= C.xs[l] + 1e-9 and s.block == C.inner


# ---------------------------------------------------------------------------------------------
# Mixed outer blocks: the sorted-slope tables
# ---------------------------------------------------------------------------------------------
def _brute_sorted(comp):
    """E_r and T(k) of the sorted-slope bounds straight from their definitions."""
    slopes = sorted([u for u, n in comp for _ in range(n)], reverse=True)
    m = len(slopes)
    U = [0.0]
    for s in slopes:
        U.append(U[-1] + s)
    binom = [math.comb(m, j) for j in range(m + 1)]
    ball = [sum(binom[: r + 1]) for r in range(m + 1)]
    E = [math.fsum((math.exp(U[j]) - math.exp(U[j - 1])) * ball[r + 1 - j] for j in range(1, min(r + 1, m) + 1)) for r in range(m + 1)]
    T = [math.fsum(binom[j] * math.exp(-U[max(j - k, 0)]) for j in range(m + 1)) for k in range(m + 1)]
    return E, T, U


@pytest.mark.parametrize("comp", [((2.0, 3), (0.5, 4)), ((1.3, 1), (0.9, 2), (0.2, 6)), ((4.0, 10), (1.0, 30)), ((0.7, 12),)])
def test_mixed_tables_equal_their_definition(comp):
    comp = H.make_block(comp)
    Tm = H.MixedTables(m=H.dim(comp), u=H.umax(comp), comp=comp)
    E, T, _ = _brute_sorted(comp)
    assert np.allclose(Tm.lE, np.log(E), rtol=0, atol=1e-9)
    assert np.allclose(Tm.lT, np.log(T), rtol=0, atol=1e-9)
    if len(comp) == 1:                                           # one slope: the tables of the uniform cube
        Tc = cert.tables(H.dim(comp), comp[0][0])
        m = H.dim(comp)
        # radii r <= m - 1 only: at r = m the uniform table counts a depth m + 1 that no set has, and no caller uses it
        for a, b in ((Tm.lE[:m], Tc.lE[:m]), (Tm.lT, Tc.lT), (Tm.lGt[:m], Tc.lGt[:m]), (Tm.lball, Tc.lball)):
            assert np.allclose(a, b, rtol=0, atol=1e-9)


def test_mixed_tables_large_block_is_stable():
    """Against the definition in exact rational arithmetic is too slow at this size; check the equal-slope limit and
    monotonicity instead: E_r increases with r, T(k) increases with k, and both lie between the uniform tables of the
    smallest and of the largest slope."""
    comp = H.make_block([(2.0, 1500), (0.5, 2500)])
    Tm = H.MixedTables(m=4000, u=2.0, comp=comp)
    lo, hi = cert.tables(4000, 0.5), cert.tables(4000, 2.0)
    assert np.all(np.diff(Tm.lE) > 0) and np.all(np.diff(Tm.lT) >= -1e-9)
    assert np.all(Tm.lE <= hi.lE + 1e-9) and np.all(Tm.lE >= lo.lE - 1e-9)
    assert np.all(Tm.lT >= hi.lT - 1e-9) and np.all(Tm.lT <= lo.lT + 1e-9)


def test_sorted_slope_tail_bounds_hold_for_every_set_of_a_small_mixed_cube():
    """Both tail inequalities at their extremal functions, for *every* subset of a 4-site cube with two slopes:
    the largest E(V - s)_+/s over the class given {V > s} = D is 2^-m sum_{x in D} (e^{rho(x, D^c)} - 1), and the
    smallest E min(V, t)/t given {V >= t} = S is 2^-m sum_x e^{-rho(x, S)}."""
    us = np.array([1.7, 1.7, 0.4, 0.4])
    comp = H.make_block([(1.7, 2), (0.4, 2)])
    m = 4
    Tm = H.MixedTables(m=m, u=1.7, comp=comp)
    X = np.array(list(itertools.product((0, 1), repeat=m)))
    dist = np.abs(X[:, None, :] - X[None, :, :]) @ us                # weighted distance between all pairs
    ball = np.exp(Tm.lball)
    for mask in range(1, 2 ** (2 ** m) - 1):
        inD = np.array([(mask >> i) & 1 for i in range(2 ** m)], dtype=bool)
        size = int(inD.sum())
        # upper tail: D = {V > s}
        r = int(np.searchsorted(ball, size - 1e-9))                  # least r with |B(m, r)| >= |D|
        if r <= m - 1:
            rho = dist[np.ix_(inD, ~inD)].min(axis=1)
            assert np.sum(np.expm1(rho)) <= math.exp(Tm.lE[r]) * (1 + 1e-12)
        # lower tail: S = {V >= t}
        k = int(np.searchsorted(ball, size + 1e-9, side="right")) - 1    # largest k with |B(m, k)| <= |S|
        rho_s = np.where(inD, 0.0, dist[:, inD].min(axis=1))
        assert np.sum(np.exp(-rho_s)) >= math.exp(Tm.lT[k]) * (1 - 1e-12)


def test_mixed_blocks_generalise_aligned_ones():
    B = H.make_block([(2.0, 900), (0.5, 1100)])
    # a composition of one type gives the constants of the aligned design
    Da = H.top_design(0, 400)
    Dm = H.top_design(0, 0, comp=((2.0, 400),))
    Ca, Cm = H.constants(B, Da, LID), H.constants(B, Dm, LID)
    assert (Ca.J, Ca.K, Ca.inner) == (Cm.J, Cm.K, Cm.inner) and abs(Ca.lM_bar - Cm.lM_bar) < 1e-12
    # the union of the two families is at least as good as either
    def best(blocks):
        S = H.HSearch(blocks=blocks)
        vals = [S.top(B, H.top_design(j, k, comp=c), LID, 2) for j, k, c in H.top_choices(B, blocks=blocks)]
        return min(v.lCmax for v in vals if v is not None)
    a, mx, both = best("aligned"), best("mixed"), best("both")
    assert both <= min(a, mx) + 1e-9
    # proportional splits of a two-type block are genuinely mixed, and the inner block is what is left
    comp = H.proportional_comps(B)[0]
    assert len(comp) == 2 and H.remove_comp(B, comp) == H.make_block([(u, n - dict(comp)[u]) for u, n in B])
