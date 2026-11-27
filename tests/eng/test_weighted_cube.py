"""Tests of the exact vertex enumeration of the weighted cubes and of the block bounds computed from it
(request R10-E1 of the science division; drivers and results in ``experiments/eng/weighted_cube/``).

Layers:
  1. the polytope: dimensions, the vertex criterion against an exact rank test;
  2. the vertex list of the 3-site block (96 vertices) by five independent methods, and smaller cases;
  3. symmetry: canonical members, stabilisers, the kernel against the reference implementation;
  4. the edges at a vertex against an exact rank criterion of adjacency;
  5. chambers of the slope ratio (walls, counts, the vertices shared across a wall);
  6. the block bounds: solvers against independent iterations, the product control, the validation value
     ``a <= 3 x 0.495806`` at ``(p, u) = (0.3, 3)`` in interval arithmetic, and numbers published by the theory
     and science divisions (quoted as constants with their source);
  7. the stored results, when present.

Slow checks (the 4-site blocks with 21 472 vertices against the Parma Polyhedra Library, the uniform 5-cube)
run only with ``WCUBE_SLOW=1``.
"""
from __future__ import annotations

import itertools
import json
import math
import os
import sys
from fractions import Fraction as Fr
from pathlib import Path

import mpmath as mp
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.weighted_cube import chambers as CH  # noqa: E402
from metricchain_eng.weighted_cube import ckernel as CK  # noqa: E402
from metricchain_eng.weighted_cube import exponents as EX  # noqa: E402
from metricchain_eng.weighted_cube import polytope as P  # noqa: E402

RES = ROOT / "experiments" / "eng" / "weighted_cube" / "results"
SLOW = os.environ.get("WCUBE_SLOW") == "1"


@pytest.fixture(scope="session", autouse=True)
def _kernel(tmp_path_factory):
    """Compile the kernel into a temporary directory unless a build directory was chosen by the caller."""
    if not os.environ.get("METRICCHAIN_ENG_BUILD"):
        os.environ["METRICCHAIN_ENG_BUILD"] = str(tmp_path_factory.mktemp("wcube_build"))
    CK.load_library()


@pytest.fixture(scope="session")
def chambers3():
    return CH.walk_chambers(3)[0]


@pytest.fixture(scope="session")
def chambers4():
    return CH.walk_chambers(4)[0]


def kernel_vertices(wts):
    """Full vertex set from the kernel's orbit representatives (expanded with the reference orbit code)."""
    res = CK.enumerate_orbits(wts)
    assert res.complete
    table = P.node_perm_table(len(wts), list(res.perms))
    out = set()
    for rep, st in zip(res.reps, res.stab):
        orb = P.orbit(tuple(int(v) for v in rep), table)
        assert len(orb) * int(st) == res.group_order
        out |= orb
    assert len(out) == res.n_vertices
    return out


# ----------------------------------------------------------------------------- 1. the polytope


def test_dimensions_and_inequalities():
    assert (P.dimension(3), P.n_inequalities(3)) == (7, 24)
    assert (P.dimension(4), P.n_inequalities(4)) == (15, 64)     # as in the request
    assert (P.dimension(5), P.n_inequalities(5)) == (31, 160)    # as in the request
    assert len(P.cube_edges(4)) == 32 and len(P.cube_edges(5)) == 80


def test_vertex_criterion_against_rank():
    """(V): 'tight graph connected' agrees with 'tight constraints have full rank' on vertices, on points of
    edges and on random feasible integer points."""
    wts = (4, 4, 5)
    verts = sorted(P.enumerate_bfs(wts))
    rng = np.random.default_rng(0)
    for v in verts[::5]:
        assert P.is_vertex(v, wts) and P.is_vertex_by_rank(v, wts)
    n_non = 0
    for _ in range(60):
        a, b = verts[rng.integers(len(verts))], verts[rng.integers(len(verts))]
        mid = tuple(x + y for x, y in zip(a, b))          # twice the midpoint: a point of the polytope 2P
        w2 = tuple(2 * w for w in wts)
        assert P.is_feasible(mid, w2)
        assert P.is_vertex(mid, w2) == P.is_vertex_by_rank(mid, w2)
        n_non += not P.is_vertex(mid, w2)
    assert n_non > 30


# ----------------------------------------------------------------------------- 2. vertex lists, independent methods


@pytest.mark.parametrize("wts,count", [((4, 4, 5), 96), ((2, 2, 3), 96), ((4, 4, 9), 72), ((1, 1, 1), 38), ((1, 1, 2), 68),
                                       ((4, 5), 8), ((1, 1), 6), ((3, 2), 8), ((1,), 2)])
def test_small_cases_all_methods(wts, count):
    """The 96 vertices of the 3-site block (and smaller cases) by: BFS over the polytope graph, BFS over orbits,
    DFS over attachment orders, brute force over bases with exact rank tests, the kernel, and (if installed)
    the Parma Polyhedra Library.  All vertex sets are identical."""
    bfs = P.enumerate_bfs(wts)
    assert len(bfs) == count
    assert all(P.is_vertex(v, wts) for v in bfs)
    assert P.enumerate_dfs(wts) == bfs
    assert P.enumerate_bases(wts) == bfs
    reps, total = P.enumerate_bfs_orbits(wts)
    assert total == count
    assert kernel_vertices(wts) == bfs
    if P.ppl_available():
        assert P.enumerate_ppl(wts) == bfs


def test_request_validation_count():
    """'L = 3 gives 96 vertices' (request) and '72 where u* > 2u' (science report), for the weights (u, u, u*)."""
    assert len(P.enumerate_bfs((100, 100, 127))) == 96      # u*/u = 1.27 as at (p, u) = (0.3, 3)
    assert len(P.enumerate_bfs((100, 100, 275))) == 72      # u*/u = 2.75 as at (p, u) = (0.1, 1)
    assert CK.enumerate_orbits((100, 100, 127)).n_vertices == 96


@pytest.mark.skipif(not P.ppl_available(), reason="pplpy not installed")
@pytest.mark.parametrize("wts,count", [((10, 10, 10, 31), 2888), ((10, 10, 10, 21), 3160)])
def test_four_sites_against_ppl(wts, count):
    """Two chambers of the 4-site block: kernel (orbits) against the double-description code of PPL."""
    ppl = P.enumerate_ppl(wts)
    assert len(ppl) == count
    assert kernel_vertices(wts) == ppl


@pytest.mark.skipif(not (SLOW and P.ppl_available()), reason="slow (set WCUBE_SLOW=1) or pplpy not installed")
@pytest.mark.parametrize("wts,count", [((4, 4, 4, 5), 21472), ((5, 5, 5, 8), 21184)])
def test_four_sites_large_chambers_against_ppl(wts, count):
    ppl = P.enumerate_ppl(wts)
    assert len(ppl) == count
    assert kernel_vertices(wts) == ppl


def test_uniform_cube_counts():
    """Height functions of the cube (known sequence 2, 6, 38, 990, 395094): the kernel at equal weights."""
    for L, count in ((1, 2), (2, 6), (3, 38), (4, 990)):
        assert CK.enumerate_orbits((1,) * L).n_vertices == count


@pytest.mark.skipif(not SLOW, reason="slow (set WCUBE_SLOW=1): 80 s")
def test_uniform_five_cube():
    res = CK.enumerate_orbits((1,) * 5)
    assert res.complete and res.n_vertices == 395094


def test_four_sites_kernel_against_reference():
    """Kernel and reference implementation give the same orbit representatives, stabilisers and degrees."""
    wts = (10, 10, 10, 31)
    reps, total = P.enumerate_bfs_orbits(wts)
    res = CK.enumerate_orbits(wts)
    assert total == res.n_vertices == 2888
    got = {tuple(int(v) for v in r): (int(s), int(d)) for r, s, d in zip(res.reps, res.stab, res.deg)}
    assert got == reps
    assert CK.enumerate_orbits((4, 4, 4, 5)).n_vertices == 21472
    assert CK.enumerate_orbits((5, 5, 5, 8)).n_vertices == 21184


def test_limits_are_respected():
    res = CK.enumerate_orbits((4, 4, 4, 5), max_vertices=5000)
    assert not res.complete and CK.STATUS[res.status] == "stopped: vertex limit"
    assert 5000 < res.n_vertices <= 21472 and res.n_processed < len(res.reps)
    res = CK.enumerate_orbits((4, 4, 4, 5), max_orbits=20)
    assert not res.complete and CK.STATUS[res.status] == "stopped: orbit limit"


# ----------------------------------------------------------------------------- 3. symmetry


def test_symmetry_group_and_canonical_members():
    wts = (4, 4, 4, 5)
    perms = P.weight_preserving_perms(wts)
    assert len(perms) == 6 and P.group_order(4, len(perms)) == 192
    table = P.node_perm_table(4, perms)
    res = CK.enumerate_orbits(wts)
    rng = np.random.default_rng(3)
    for k in rng.choice(len(res.reps), size=12, replace=False):
        v = tuple(int(x) for x in res.reps[k])
        key, stab = P.canonical(v, table)
        assert key == v and stab == res.stab[k]                       # representatives are canonical
        orb = P.orbit(v, table)
        assert len(orb) * stab == 192
        for w in list(orb)[:6]:
            assert P.is_vertex(w, wts)                                # the group maps vertices to vertices
            assert P.canonical(w, table)[0] == key                    # and all images share the canonical member
            assert CK.canonical(w, wts) == (key, stab)                # kernel = reference
    # the group does not contain permutations that move the weighted site
    assert all(s[3] == 3 for s in perms)


# ----------------------------------------------------------------------------- 4. the edges at a vertex


def _common_tight_rank(v, w, wts):
    """Rank of the constraints that are tight at both vertices (exact)."""
    L = len(wts)
    n = 1 << L
    rows = []
    for (x, y, i) in P.cube_edges(L):
        d1, d2 = v[y] - v[x], w[y] - w[x]
        if abs(d1) == wts[i] and d1 == d2:
            r = [Fr(0)] * (n - 1)
            if x:
                r[x - 1] -= 1
            if y:
                r[y - 1] += 1
            rows.append(r)
    return P._rank(rows, n - 1) if rows else 0


@pytest.mark.parametrize("wts", [(4, 4, 5), (4, 4, 9), (1, 1, 1)])
def test_edges_against_rank_criterion(wts):
    """(E): the neighbours produced from the tight digraph are exactly the vertices that share a face of
    dimension one with the vertex (common tight constraints of rank dim - 1)."""
    verts = sorted(P.enumerate_bfs(wts))
    dim = P.dimension(len(wts))
    for v in verts[::3]:
        nb = set(P.neighbours(v, wts))
        assert len(nb) == len(P.edge_sets(v, wts))
        by_rank = {w for w in verts if w != v and _common_tight_rank(v, w, wts) == dim - 1}
        assert nb == by_rank
        kn = {tuple(int(x) for x in row) for row in CK.neighbours(v, wts)}
        assert kn == nb


def test_closure_spot_check_four_sites():
    """Reference neighbours of kernel vertices of the 4-site block stay inside the kernel's vertex set."""
    wts = (5, 5, 5, 8)
    res = CK.enumerate_orbits(wts)
    table = P.node_perm_table(4, list(res.perms))
    keys = {tuple(int(v) for v in r) for r in res.reps}
    rng = np.random.default_rng(5)
    for k in rng.choice(len(res.reps), size=10, replace=False):
        v = tuple(int(x) for x in res.reps[k])
        nbs = P.neighbours(v, wts)
        assert len(nbs) == res.deg[k]
        for w in nbs:
            assert CK.canonical(w, wts)[0] in keys


# ----------------------------------------------------------------------------- 5. chambers


def test_chambers_three_sites(chambers3):
    assert [(c.lo, c.hi, c.n_vertices, c.n_orbits) for c in chambers3] == [(Fr(1), Fr(2), 96, 8), (Fr(2), None, 72, 7)]


def test_chambers_four_sites(chambers4):
    got = [(c.lo, c.hi, c.n_vertices, c.n_orbits) for c in chambers4]
    assert got == [(Fr(1), Fr(3, 2), 21472, 191), (Fr(3, 2), Fr(2), 21184, 189), (Fr(2), Fr(3), 3160, 56),
                   (Fr(3), None, 2888, 52)]
    # the unbounded chamber: pairs of height functions of the 3-cube with one sign of contact
    assert chambers4[-1].n_vertices == 2 * 38 ** 2
    # across a wall the surviving symbolic vertices are the same on both sides (two independent enumerations)
    for c1, c2 in zip(chambers4[:-1], chambers4[1:]):
        s1 = int(c1.orbit_sizes[~c1.at_hi].sum())
        s2 = int(c2.orbit_sizes[~c2.at_lo].sum())
        assert s1 == s2
        k1 = {CK.canonical(tuple(int(v) for v in CH.evaluate(a[None], b[None], 1009, 2003)[0]), (1009,) * 3 + (2003,))[0]
              for a, b in zip(c1.A[~c1.at_hi], c1.B[~c1.at_hi])}
        k2 = {CK.canonical(tuple(int(v) for v in CH.evaluate(a[None], b[None], 1009, 2003)[0]), (1009,) * 3 + (2003,))[0]
              for a, b in zip(c2.A[~c2.at_lo], c2.B[~c2.at_lo])}
        assert k1 == k2


def test_chamber_is_independent_of_the_ratio_used(chambers4):
    """Two different rational ratios inside one chamber give the same symbolic vertices."""
    c = chambers4[0]
    other = CH.chamber_at(4, 97, 139)          # 139/97 = 1.43..., also in (1, 3/2)
    assert (other.lo, other.hi, other.n_vertices) == (c.lo, c.hi, c.n_vertices)
    table = CH.group_table(4)
    assert CH.multiset_checksum(c.A, c.B, table) == CH.multiset_checksum(other.A, other.B, table)


def test_symbolic_vertices_are_vertices_throughout_the_chamber(chambers3):
    """Every symbolic vertex evaluated at other rational ratios of its chamber is a vertex there, and the count
    at those ratios (independent enumeration) is the chamber's count; on the wall the count differs."""
    c = chambers3[0]
    table = CH.group_table(3)
    A, B, _ = CH.expand_orbits(c.A, c.B, table)
    for (Q, Pn) in ((7, 9), (10, 19), (50, 51)):
        wts = (Q, Q, Pn)
        vals = {tuple(int(v) for v in row) for row in CH.evaluate(A, B, Q, Pn)}
        assert vals == P.enumerate_bfs(wts)
    assert len(P.enumerate_bfs((1, 1, 2))) == 68          # on the wall r = 2
    with pytest.raises(AssertionError):
        CH.chamber_at(3, 1, 2)                               # the checks refuse a ratio on a wall


def test_parity_of_symbolic_vertices(chambers4):
    """A(x) = number of unit letters of x and B(x) = last letter of x, modulo 2 (used for the unbounded chamber)."""
    x = np.arange(16)
    unit = np.array([bin(v & 7).count("1") for v in x])
    last = x >> 3
    for c in chambers4:
        assert ((c.A.astype(int) - unit[None, :]) % 2 == 0).all()
        assert ((c.B.astype(int) - last[None, :]) % 2 == 0).all()
        assert np.all(c.A[:, 0] == 0) and np.all(c.B[:, 0] == 0)


def test_valid_at_agrees_with_feasibility(chambers3, chambers4):
    """The rigorous selection of the symbolic vertices that exist at a given ratio (used for the 5-site block
    where the enumeration stops), tested at rational ratios against plain feasibility."""
    for c in (chambers3[0], chambers4[1]):
        L = c.L
        for r in (Fr(11, 10), Fr(7, 4), Fr(5, 2)):
            mask = CH.valid_at(c.A, c.B, lambda lo, hi: lo < r and (hi is None or r < hi))
            Q, Pn = r.denominator, r.numerator
            wts = (Q,) * (L - 1) + (Pn,)
            feas = np.array([P.is_feasible(tuple(int(v) for v in row), wts) for row in CH.evaluate(c.A, c.B, Q, Pn)])
            strict = np.array([P.tight_graph_connected(tuple(int(v) for v in row), wts) for row in CH.evaluate(c.A, c.B, Q, Pn)])
            assert not (mask & ~feas).any()                       # accepted rows are feasible
            assert mask.sum() > 0 or not c.contains(r)
            if c.contains(r):
                assert mask.all() and feas.all() and strict.all()


def test_validity_intervals(chambers3):
    c = chambers3[0]
    for a, b in zip(c.A, c.B):
        lo, hi = CH.validity_interval(a, b)
        assert lo <= c.lo and (hi is None or hi >= c.hi)
    # the vertices that end at the wall r = 2 from below are infeasible just above it
    for a, b in zip(c.A[c.at_hi], c.B[c.at_hi]):
        N = CH.evaluate(a[None], b[None], 100, 201)[0]
        assert not P.is_feasible(tuple(int(v) for v in N), (100, 100, 201))


# ----------------------------------------------------------------------------- 6. block bounds


def test_solvers_against_plain_iterations():
    rng = np.random.default_rng(11)
    for trial in range(4):
        m, n = 30, 6
        W = rng.dirichlet(np.ones(n) * 0.7, size=m)
        sol = EX.capacity_solve(W)
        ba = EX.capacity_iterate(W, iters=4000)
        assert sol["upper"] - sol["lower"] < 1e-11
        assert ba["lower"] <= sol["upper"] + 1e-12 and sol["lower"] <= ba["upper"] + 1e-12   # brackets intersect
        assert abs(sol["lower"] - ba["lower"]) < 1e-5
        t = [0.2, 0.5, 0.8, 0.35][trial]
        sr = EX.renyi_solve(W, t)
        ar = EX.renyi_iterate(W, t, iters=4000)
        assert sr["upper"] - sr["lower"] < 1e-11
        assert ar["lower"] <= sr["upper"] + 1e-12 and sr["lower"] <= ar["upper"] + 1e-12
        # monotonicity used by the interval rule: F*/t nonincreasing, F*/(1-t) nondecreasing
        s2 = EX.renyi_solve(W, t + 0.1)
        assert sr["lower"] / t >= s2["lower"] / (t + 0.1) - 1e-10
        assert sr["lower"] / (1 - t) <= s2["lower"] / (0.9 - t) + 1e-10


def test_renyi_jacobian_against_differences():
    rng = np.random.default_rng(2)
    W = rng.dirichlet(np.ones(5), size=4)
    t = 0.37
    Wt = W ** t
    M = rng.dirichlet(np.ones(4))
    J = EX.renyi_jacobian(Wt, t, M)
    eps = 1e-6
    for j in range(4):
        d = np.zeros(4)
        d[j] = eps
        num = (EX._renyi_eval(Wt, t, M + d)[1] - EX._renyi_eval(Wt, t, M - d)[1]) / (2 * eps)
        assert np.allclose(J[:, j], num, atol=1e-8)


def test_product_control_uniform_cube():
    """p = 1/2 (independent sites, u* = u): three sites as one super-site with its 38 vertices give the per-site
    exponents of the cube (the product theorem of the theory report; a test of vertex list and solvers)."""
    u = 1.3
    verts = np.array(sorted(P.enumerate_bfs((1, 1, 1))), dtype=np.int8)
    logpi = np.full(8, -3 * math.log(2))
    W = EX.gibbs_rows(verts, np.zeros_like(verts), u, 0.0, logpi)
    hc, tc, ac, Ec = EX.cube_exponents(u)
    cap = EX.capacity_solve(W)
    assert abs(cap["lower"] / 3 - ac) < 1e-10 and cap["upper"] - cap["lower"] < 1e-11
    f = EX.renyi_solve(W, tc)
    assert abs(f["lower"] / 3 - hc) < 1e-10
    assert abs(EX.ustar(0.5, u) - u) < 1e-14


def test_interval_rule():
    u = 2.0
    F = lambda t: EX.cube_F(t, u)          # satisfies both monotonicity properties
    hc = EX.cube_exponents(u)[0]
    for step in (0.05, 0.01, 0.002):
        ts = np.arange(step, 1.0, step)
        grid = [(float(t), F(float(t))) for t in ts]
        b = EX.sup_bound(grid)
        assert hc <= b <= hc * (1 + 1.5 * step) + 1e-12
    assert EX.interval_bound(0.3, F(0.3), 0.4, F(0.4)) >= max(F(t) for t in np.linspace(0.3, 0.4, 101))


def test_scans_kernel_against_numpy(chambers3, chambers4):
    rng = np.random.default_rng(7)
    for chs, L, (p, u) in ((chambers3, 3, (0.3, 3.0)), (chambers4, 4, (0.1, 1.0)), (chambers4, 4, (0.2, 2.5))):
        us = EX.ustar(p, u)
        c = next(c for c in chs if c.contains(Fr(us / u)))
        table = CH.group_table(L)
        A, B, sizes = CH.expand_orbits(c.A, c.B, table)
        assert int(sizes.sum()) == c.n_vertices and np.array_equal(sizes, c.orbit_sizes)
        pk = EX.BlockProblem(c, p, u)
        pe = EX.BlockProblem(c, p, u, explicit=(A, B))
        Q = rng.dirichlet(np.ones(1 << L))
        v1, A1, B1 = pk.scan_kl(np.log(Q), 40)
        v2, _, _ = pe.scan_kl(np.log(Q), 40)
        assert np.allclose(v1, v2, rtol=0, atol=1e-12)
        assert len({a.tobytes() + b.tobytes() for a, b in zip(A1, B1)}) == 40      # no vertex twice
        W = pk.rows(A1, B1)
        assert np.allclose(np.einsum("ij,ij->i", W, np.log(W) - np.log(Q)[None, :]), v1, atol=1e-12)
        ts = [0.15, 0.5, 0.9]
        for (a, _, _), (b, _, _) in zip(pk.scan_renyi(ts, [Q] * 3, 30), pe.scan_renyi(ts, [Q] * 3, 30)):
            assert np.allclose(a, b, rtol=0, atol=1e-12)


def test_validation_value_in_interval_arithmetic(chambers3):
    """Request: 'validation: L = 3 gives 96 vertices and a <= 3 x 0.495806 at (0.3, 3)'.
    Capacity of the 3-site block per site, bracketed in interval arithmetic over ALL 96 vertices."""
    ivb = EX.IvBlock(3, Fr(3, 10), Fr(3), dps=30)
    inside = [c for c in chambers3 if ivb.in_chamber(c.lo, c.hi)]
    assert len(inside) == 1 and inside[0].n_vertices == 96
    c = inside[0]
    prob = EX.BlockProblem(c, 0.3, 3.0)
    cap = EX.capacity_bound(prob)
    A, B, _ = CH.expand_orbits(c.A, c.B, CH.group_table(3))
    upper = ivb.kl_max(A, B, cap["Q"])[0] / 3
    lower = EX.iv_lo(ivb.mutual_information(cap["support_A"], cap["support_B"], cap["support_M"])) / 3
    assert lower <= upper and upper - lower < mp.mpf("1e-12")
    assert mp.mpf("0.49580552459") < lower and upper < mp.mpf("0.49580552460")
    assert abs(upper - mp.mpf("0.495806")) < mp.mpf("5e-7")          # the science division's printed value
    assert upper < EX.iv_lo(EX.iv_cube(Fr(3))[1])                     # below the cube's 0.502282
    # the screened certificate gives the same bound
    v, k = EX.certify_upper(ivb, "kl", cap["Q"], cap["top_vals"], cap["top_A"], cap["top_B"])
    assert abs(v / 3 - upper) < mp.mpf("1e-15") and k >= 1


# Published numbers, quoted with their source (theory division, docs/workstreams/Y_REPORT.md at 8ff0667, table
# 6.3 "DP: a <= (L = 3)" and "DP: h <= (L = 1, 2, 3)" at u = 1; science division, SCI-REV-0010 at 2b4ccdf, table
# of section 2).  Our values are computed from the definitions; agreement tests both.
PUBLISHED_A_L3 = {("0.4", "1"): 0.12970, ("0.3", "1"): 0.15401, ("0.2", "1"): 0.17747, ("0.1", "1"): 0.19678,
                  ("0.3", "3"): 0.495806, ("0.3", "4"): 0.591982, ("0.3", "6"): 0.671581, ("0.2", "2.5"): 0.408174,
                  ("0.2", "3"): 0.467509, ("0.2", "4"): 0.559986, ("0.1", "2"): 0.323641, ("0.1", "3"): 0.432593,
                  ("0.1", "4"): 0.509682}
PUBLISHED_H_GRIDMAX_U1 = {("0.3", 1): 0.05484, ("0.3", 2): 0.05180, ("0.3", 3): 0.04902, ("0.1", 1): 0.09157,
                          ("0.1", 2): 0.08299, ("0.1", 3): 0.07542}


def test_published_capacities_three_sites(chambers3):
    for (p, u), val in PUBLISHED_A_L3.items():
        us = EX.ustar(float(p), float(u))
        c = next(c for c in chambers3 if c.contains(Fr(us / float(u))))
        cap = EX.capacity_bound(EX.BlockProblem(c, float(p), float(u)))
        assert cap["upper"] - cap["lower"] < 1e-10
        digits = len(str(val).split(".")[1])
        assert abs(cap["upper"] / 3 - val) <= 0.51 * 10 ** (-digits), (p, u, cap["upper"] / 3, val)


def test_published_h_values():
    for (p, L), val in PUBLISHED_H_GRIDMAX_U1.items():
        chs = CH.walk_chambers(L)[0] if L > 1 else [CH.chamber_at(1, 101, 153)]
        us = EX.ustar(float(p), 1.0)
        c = next(c for c in chs if c.contains(Fr(us)))
        hb = EX.h_bound(EX.BlockProblem(c, float(p), 1.0), rel_tol=2e-3)
        assert abs(hb["lower"] / L - val) < 6e-6, (p, L, hb["lower"] / L)
        assert hb["lower"] <= hb["upper"] <= hb["lower"] * 1.0021


def test_interval_helpers():
    lo, hi = EX.ustar_enclosure(Fr(3, 10), Fr(1))
    assert lo < mp.mpf(EX.ustar(0.3, 1.0)) + mp.mpf("1e-12") and hi > mp.mpf(EX.ustar(0.3, 1.0)) - mp.mpf("1e-12")
    assert hi - lo < mp.mpf("1e-30")
    assert abs(float(lo) - 1.5261) < 1e-4                    # theory report: u* = 1.526 at p = 0.3, u = 1
    h, a, E = EX.iv_cube(Fr(1))
    hc, tc, ac, Ec = EX.cube_exponents(1.0)
    assert abs(float(EX.iv_lo(h)) - hc) < 1e-14 and abs(float(EX.iv_lo(a)) - ac) < 1e-14
    assert abs(hc - 0.0291391) < 1e-7 and abs(ac - 0.1109441) < 1e-7      # theory report, section 2


# ----------------------------------------------------------------------------- 7. stored results


@pytest.mark.skipif(not (RES / "orbits_L5_0.npz").exists(), reason="results not generated")
def test_five_sites_scan_kernel_against_numpy():
    """The scans of the 5-site block (24 permutations, 32 nodes): kernel against numpy on the explicit orbits of
    a few stored representatives of the chamber (3, 4)."""
    z = np.load(RES / "orbits_L5_0.npz")
    lo, hi = Fr(int(z["lo"][0]), int(z["lo"][1])), Fr(int(z["hi"][0]), int(z["hi"][1]))
    assert (lo, hi) == (Fr(3), Fr(4))
    rng = np.random.default_rng(9)
    idx = np.sort(rng.choice(len(z["A"]), size=8, replace=False))
    A, B = z["A"][idx], z["B"][idx]
    CH.check_symbolic(A, B, int(z["r0"][1]), int(z["r0"][0]))
    table = CH.group_table(5)
    Aall, Ball, sizes = CH.expand_orbits(A, B, table)
    stab = z["stab"][idx].astype(np.int64)
    assert np.array_equal(sizes, 1536 // stab)
    sub = CH.Chamber(5, lo, hi, int(z["r0"][1]), int(z["r0"][0]), A, B, stab, z["deg"][idx], int(sizes.sum()),
                     np.zeros(8, dtype=bool), np.zeros(8, dtype=bool))
    p, u = 0.1, 0.5                                   # u*/u = 3.62
    pk = EX.BlockProblem(sub, p, u)
    pe = EX.BlockProblem(sub, p, u, explicit=(Aall, Ball))
    Q = rng.dirichlet(np.ones(32))
    v1, A1, B1 = pk.scan_kl(np.log(Q), 60)
    v2, _, _ = pe.scan_kl(np.log(Q), 60)
    assert np.allclose(v1, v2, rtol=0, atol=1e-12)
    assert len({a.tobytes() + b.tobytes() for a, b in zip(A1, B1)}) == 60
    for (a, _, _), (b, _, _) in zip(pk.scan_renyi([0.3, 0.6], [Q] * 2, 40), pe.scan_renyi([0.3, 0.6], [Q] * 2, 40)):
        assert np.allclose(a, b, rtol=0, atol=1e-12)


@pytest.mark.skipif(not (RES / "chambers_L4.json").exists(), reason="results not generated")
def test_stored_chambers(chambers3, chambers4):
    for L, chs in ((3, chambers3), (4, chambers4)):
        rec = json.loads((RES / f"chambers_L{L}.json").read_text())
        assert rec["dimension"] == (1 << L) - 1 and rec["inequalities"] == L * (1 << L)
        assert len(rec["chambers"]) == len(chs)
        table = CH.group_table(L)
        for e, c in zip(rec["chambers"], chs):
            assert (e["lo"], e["hi"]) == (str(c.lo), "inf" if c.hi is None else str(c.hi))
            assert e["n_vertices"] == c.n_vertices and e["n_orbits"] == c.n_orbits
            z = np.load(RES / e["file"])
            CH.check_symbolic(z["A"], z["B"], int(z["r0"][1]), int(z["r0"][0]))
            # same ratio r0, hence the same canonical representatives as a fresh enumeration
            assert (int(z["r0"][0]), int(z["r0"][1])) == (c.P, c.Q)
            assert np.array_equal(z["A"], c.A) and np.array_equal(z["B"], c.B) and np.array_equal(z["stab"], c.stab)
            assert CH.multiset_checksum(z["A"], z["B"], table) == (e["sha256_multiset"], c.n_vertices)


def test_the_parma_library_does_not_leave_the_process_in_another_rounding_mode():
    """pplpy switches the process to upward rounding when it is imported; ``polytope`` must put it back after the
    import and after every call (the library is optional: without it there is nothing to restore)."""
    assert P.rounding_is_to_nearest()
    if not P.ppl_available():
        pytest.skip("pplpy not installed")
    assert P.rounding_is_to_nearest()
    wts = [2, 2, 3]                                   # the library takes integral coefficients
    assert P.enumerate_ppl(wts) == P.enumerate_bfs(wts)
    assert P.rounding_is_to_nearest()
    assert np.float64(1.0) + np.float64(2.0 ** -53) == 1.0
