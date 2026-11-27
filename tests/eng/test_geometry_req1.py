"""Tests of the exact computations for GEOMETRY-REQ-0001, items 1 and 3
(experiments/eng/geometry_req1; request and definitions at commit d84a43b of
research/geometric-inference).

Layers:
  1. the witnesses: determinism, chain constraints (unit bonds, bond-angle cosine -5/13, the
     prescribed dihedral angles), all exact;
  2. item 1, linear part: the forced solutions, the ranks of the linear systems for n = 9..12, the
     quadrics of rank 2 at infinity;
  3. item 1, the minors: the symbolic minors against independently computed determinants; the
     certificate for n = 10 (seven vanishing columns and rank 63 modulo two primes, which together
     PROVE rank 63 over Q, hence the monomial structure of the ideal, hence "exactly two reduced
     affine points"); n = 11, 12; the excess at n = 9; reducedness by two criteria;
  4. item 3: the ranks for K = 2 and K = 3, the exact derivative against the closed formula;
  5. the stored result files against recomputation; the interval certificates of the real
     positive semidefinite solutions at n = 9 (needs python-flint).

Everything except layer 5 and the cross-checks marked "flint" runs on the standard library
(fractions, integers).  Slow extras: GEOMREQ1_SLOW=1.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "eng" / "geometry_req1"
sys.path.insert(0, str(EXP))

import enslib as el  # noqa: E402
import item3_ranks as i3  # noqa: E402

P1 = 2305843009213693951        # 2^61 - 1
P2 = 4611686018427387847        # 2^62 - 57
SLOW = os.environ.get("GEOMREQ1_SLOW") == "1"

MAIN_TANGENTS_N10 = [["3/7", "-8/5", "7/8", "3/5", "1", "9/4", "7/3"],
                     ["0", "-6/5", "8/3", "0", "-7/6", "2/3", "-1"]]
ENG0_TANGENTS_N10 = [["-1/2", "-3", "11/7", "-4/3", "-3/7", "-3/5", "-5"],
                     ["10", "12", "-10/7", "1/4", "2", "8/3", "-5/3"]]
EXCLUDED = [(4, 0, 0, 0, 0), (0, 4, 0, 0, 0), (0, 0, 4, 0, 0),
            (1, 0, 3, 0, 0), (0, 1, 3, 0, 0), (0, 0, 3, 1, 0), (0, 0, 3, 0, 1)]


def unit(v, i):
    return tuple(1 if a == i else 0 for a in range(v))


def det_int(M):
    """Determinant of a small integer matrix by cofactor expansion (independent of enslib)."""
    n = len(M)
    if n == 1:
        return M[0][0]
    tot = 0
    for j in range(n):
        if M[0][j]:
            tot += (-1) ** j * M[0][j] * det_int([row[:j] + row[j + 1:] for row in M[1:]])
    return tot


def build(kind, n, index, adapted=True):
    tans = (el.geometry_witness_tangents if kind == "geometry" else el.eng_witness_tangents)(2, n, index)
    chains, z = el.ensemble(tans)
    fams = el.rank2_families_at_infinity(z)
    first = []
    if adapted and n == 10:
        first = [el.sym_outer(fams[0]["ann_lambda"][0], fams[0]["ann_mu"][0])]
    mats, rank, dimN = el.pencil_basis(z, first=first)
    return {"tans": tans, "chains": chains, "z": z, "fams": fams, "mats": mats, "rank": rank,
            "dimN": dimN, "v": len(mats), "minors": el.all_4x4_minors(mats)}


@pytest.fixture(scope="module")
def cache():
    store = {}

    def get(kind, n, index):
        key = (kind, n, index)
        if key not in store:
            store[key] = build(kind, n, index)
        return store[key]
    return get


# ------------------------------------------------------------------------------------ 1. witnesses
def test_primes_are_prime():
    sympy = pytest.importorskip("sympy")
    assert sympy.isprime(P1) and sympy.isprime(P2) and sympy.isprime(i3.P_GEOMETRY)
    assert P1 == 2 ** 61 - 1 and P2 == 2 ** 62 - 57


def test_witnesses_are_pinned():
    got = el.geometry_witness_tangents(2, 10, 0)
    assert [[str(t) for t in row] for row in got] == MAIN_TANGENTS_N10
    got = el.eng_witness_tangents(2, 10, 0)
    assert [[str(t) for t in row] for row in got] == ENG0_TANGENTS_N10
    # our own witnesses avoid the special torsions 0, 90, 180 degrees and repeated values
    flat = [abs(t) for row in got for t in row]
    assert 0 not in flat and 1 not in flat and len(set(flat)) == len(flat)
    # large ensembles are served by the second rule and terminate
    big = el.eng_witness_tangents(4, 39, 0)
    assert len(big) == 4 and all(len(r) == 36 for r in big)
    assert all(t != 0 and abs(t) != 1 for r in big for t in r)


@pytest.mark.parametrize("kind,index", [("geometry", 0), ("geometry", 1), ("eng", 0), ("eng", 1)])
@pytest.mark.parametrize("n", [9, 10, 12])
def test_chain_constraints_exact(kind, index, n):
    tans = (el.geometry_witness_tangents if kind == "geometry" else el.eng_witness_tangents)(2, n, index)
    for row in tans:
        x = el.chain_from_tangents(row)
        assert len(x) == n and el.check_chain(x)
        for i in range(n - 1):
            assert sum((x[i + 1][c] - x[i][c]) ** 2 for c in range(3)) == 1
        for i in range(n - 2):
            assert sum((x[i + 2][c] - x[i][c]) ** 2 for c in range(3)) == Fr(36, 13)
        # the dihedral angle of atoms m..m+3, recomputed from the coordinates
        for m, t in enumerate(row):
            c, s = el.circle_point(t)
            cosn, sinn, den2 = el.dihedral_cos_sin(x, m)
            assert den2 == el.SIN ** 4
            assert cosn == c * el.SIN ** 2 and sinn == s * el.SIN ** 2


def test_mutated_bond_angle_is_detected():
    x = el.chain_from_tangents([Fr(1, 2), Fr(3)], cos=Fr(-3, 5), sin=Fr(4, 5))
    assert not el.check_chain(x) and el.check_chain(x, cos=Fr(-3, 5))


# ------------------------------------------------------------------------------------ 2. linear part
@pytest.mark.parametrize("n", [9, 10, 11, 12])
def test_forced_solutions_satisfy_the_system_exactly(n):
    chains, z = el.ensemble(el.geometry_witness_tangents(2, n, 0))
    E = [el.block_projection(2, k) for k in range(2)]
    w = [Fr(1, 3), Fr(2, 3)]
    for e, l2 in el.edge_vectors(z):
        a, b = e[:3], e[3:]
        # unweighted: e^T E_k e = l^2
        assert el.quad_form(E[0], e) == l2 and el.quad_form(E[1], e) == l2
        # weighted (request): e_w = (sqrt(w1) a, sqrt(w2) b); |e_w|^2 = w1|a|^2 + w2|b|^2 and
        # e_w^T (E_k / w_k) e_w = |block k of e|^2: both equal l^2, exactly
        assert w[0] * el.dot(a, a) + w[1] * el.dot(b, b) == l2
        assert el.dot(a, a) == l2 and el.dot(b, b) == l2
    assert len(el.edge_vectors(z)) == 2 * n - 3


def test_weighted_system_with_square_roots():
    sp = pytest.importorskip("sympy")
    chains, z = el.ensemble(el.geometry_witness_tangents(2, 10, 0))
    w = [sp.Rational(1, 3), sp.Rational(2, 3)]
    D = sp.diag(*[sp.sqrt(w[k]) for k in (0, 0, 0, 1, 1, 1)])
    for k in range(2):
        P = sp.Matrix(6, 6, lambda i, j: (1 / w[k]) if (i == j and i // 3 == k) else 0)
        for e, l2 in el.edge_vectors(z)[:6] + el.edge_vectors(z)[9:13]:
            ew = D * sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in e])
            assert sp.simplify((ew.T * P * ew)[0] - (ew.T * ew)[0]) == 0
            assert sp.simplify((ew.T * ew)[0] - sp.Rational(l2.numerator, l2.denominator)) == 0


@pytest.mark.parametrize("n,rank", [(9, 15), (10, 17), (11, 19), (12, 20)])
def test_linear_system_ranks(n, rank):
    for kind, index in (("geometry", 0), ("eng", 0)):
        tans = (el.geometry_witness_tangents if kind == "geometry" else el.eng_witness_tangents)(2, n, index)
        chains, z = el.ensemble(tans)
        A, b = el.linear_system(z)
        assert len(A) == 2 * n - 3 and len(A[0]) == 21
        assert el.rank_bareiss(A) == rank == el.rank_mod_p(A, P1)
        assert el.rank_exact(A) == rank


def test_rank_routines_agree_on_random_matrices():
    rnd = random.Random(5)
    for _ in range(30):
        r, c, k = rnd.randint(1, 7), rnd.randint(1, 7), rnd.randint(0, 4)
        base = [[Fr(rnd.randint(-5, 5), rnd.randint(1, 4)) for _ in range(c)] for _ in range(min(k, r))]
        rows = [[sum(rnd.randint(-3, 3) * b[j] for b in base) for j in range(c)] for _ in range(r)] if base \
            else [[Fr(0)] * c for _ in range(r)]
        rk = len(el.rref_fraction(rows)[1])
        assert el.rank_bareiss(rows) == rk == el.rank_exact(rows) == el.rank_mod_p(rows, P1)
        ker, piv, free = el.nullspace_fraction(rows)
        assert len(ker) == c - rk
        assert all(sum(a * x for a, x in zip(row, v)) == 0 for row in rows for v in ker)


def test_rank2_quadrics_at_infinity(cache):
    # n = 10: exactly one, the product of the hyperplanes through atoms 0..5 and 4..9
    d = cache("geometry", 10, 0)
    fams = d["fams"]
    assert [(f["lambda_bonds"], f["mu_bonds"], f["dimension"]) for f in fams] == \
        [([0, 1, 2, 3, 4], [4, 5, 6, 7, 8], 0)]
    lam, mu = fams[0]["ann_lambda"][0], fams[0]["ann_mu"][0]
    z = d["z"]
    assert all(el.dot(lam, [z[i][c] - z[0][c] for c in range(6)]) == 0 for i in range(6))
    assert all(el.dot(mu, [z[i][c] - z[4][c] for c in range(6)]) == 0 for i in range(4, 10))
    N = el.sym_outer(lam, mu)
    assert el.in_conic_space(N, z) and el.rank_bareiss(N) == 2
    # signature (1, 1): the non-zero eigenvalues of lam mu^T + mu lam^T are lam.mu +- |lam||mu|
    assert el.dot(lam, mu) ** 2 < el.dot(lam, lam) * el.dot(mu, mu)
    # it is not a combination of E_1, E_2 and it is the third basis element of the adapted pencil
    assert d["mats"][2] == [[int(x) for x in row] for row in el.sym_from_vec(
        el.primitive_integer_vector([N[i][j] for (i, j) in el.sym_index(6)]), 6)]
    # n = 9: two lines and two isolated points; n = 11: nothing
    f9 = el.rank2_families_at_infinity(el.ensemble(el.geometry_witness_tangents(2, 9, 0))[1])
    assert sorted(f["dimension"] for f in f9) == [0, 0, 1, 1]
    z9 = el.ensemble(el.geometry_witness_tangents(2, 9, 0))[1]
    for f in f9:
        for la in f["ann_lambda"]:
            for m_ in f["ann_mu"]:
                S = el.sym_outer(la, m_)
                assert el.in_conic_space(S, z9) and el.rank_bareiss(S) == 2
    assert el.rank2_families_at_infinity(el.ensemble(el.geometry_witness_tangents(2, 11, 0))[1]) == []
    # the bonds span Q^6, so there is no quadric of rank 1 and the lists above are the whole locus
    # of rank <= 2 at infinity
    for fn, idxs in ((el.geometry_witness_tangents, range(5)), (el.eng_witness_tangents, range(3))):
        for index in idxs:
            for n in (9, 10, 11, 12):
                assert el.bonds_span(el.ensemble(fn(2, n, index))[1])
    assert not el.bonds_span(el.ensemble(el.geometry_witness_tangents(2, 6, 0))[1])     # 5 bonds


def test_pencil_basis_and_homogenising_coordinate(cache):
    d = cache("geometry", 10, 0)
    mats, z = d["mats"], d["z"]
    assert d["rank"] == 17 and d["dimN"] == 4 and d["v"] == 5
    idx = el.sym_index(6)
    assert el.rank_bareiss([[M[i][j] for (i, j) in idx] for M in mats]) == 5
    # e^T (sum x_i B_i) e = (x_0 + x_1) |e|^2: B_0, B_1 give |e|^2, the others 0
    for e, l2 in el.edge_vectors(z):
        vals = [el.quad_form(M, e) for M in mats]
        assert vals[0] == l2 and vals[1] == l2 and all(x == 0 for x in vals[2:])


# ------------------------------------------------------------------------------------ 3. minors
@pytest.mark.parametrize("n", [10, 11])
def test_minors_against_determinants(cache, n):
    d = cache("geometry", n, 0)
    mats, v = d["mats"], d["v"]
    rnd = random.Random(n)
    assert len(d["minors"]) == 120
    for _ in range(3):
        x = [rnd.randint(-3, 3) for _ in range(v)]
        P = [[sum(x[a] * mats[a][i][j] for a in range(v)) for j in range(6)] for i in range(6)]
        for (I, J), f in rnd.sample(d["minors"], 25):
            assert el.peval(f, x) == det_int([[P[i][j] for j in J] for i in I])
    # all polynomials are quartic forms
    assert all(sum(e) == 4 for _, f in d["minors"] for e in f)


def test_n10_certificate_is_a_proof(cache):
    """Seven coefficients of every minor vanish (exact), so rank_Q <= 63; the rank modulo a prime
    is 63, so rank_Q >= 63.  Hence the minors span exactly the 63 other quartic monomials."""
    for kind, index in (("geometry", 0), ("geometry", 1), ("eng", 0)):
        d = cache(kind, 10, index)
        polys = [f for _, f in d["minors"]]
        assert d["rank"] == 17 and d["v"] == 5
        assert all(f.get(e, 0) == 0 for f in polys for e in EXCLUDED)
        rows = el.dense_rows(polys, 5, 4)
        assert len(rows[0]) == 70
        assert el.rank_mod_p(rows, P1) == 63
        assert el.rank_mod_p(rows, P2) == 63
        # the conclusion used for the affine ideal, re-checked directly modulo p:
        h = {unit(5, 0): 1, unit(5, 1): 1}
        h2 = el.pmul(h, h)
        h3 = el.pmul(h2, h)
        targets = [el.pmul(h3, {unit(5, k): 1}) for k in (2, 3, 4)] + [el.pmul(h2, {(1, 1, 0, 0, 0): 1})]
        assert all(e not in EXCLUDED for t in targets for e in t)
        assert el.rank_mod_p(rows + el.dense_rows(targets, 5, 4), P1) == 63


def test_n10_rank_over_Q_with_flint(cache):
    flint = pytest.importorskip("flint")
    d = cache("geometry", 10, 0)
    rows = el.dense_rows([f for _, f in d["minors"]], 5, 4)
    assert int(flint.fmpz_mat(rows).rank()) == 63


def test_monomial_ideal_combinatorics():
    """I(Y) = (x0x1, x0x3, x0x4, x1x3, x1x4, x3^2, x3x4, x4^2, x0^2 x2, x1^2 x2) is the ideal of
    E_1 = e_0, E_2 = e_1 (reduced) and of the first-order neighbourhood of N_inf = e_2; the seven
    excluded monomials are exactly the quartic monomials outside it, and it is generated in degree
    <= 4 from its quartic part upward."""
    gens = [(1, 1, 0, 0, 0), (1, 0, 0, 1, 0), (1, 0, 0, 0, 1), (0, 1, 0, 1, 0), (0, 1, 0, 0, 1),
            (0, 0, 0, 2, 0), (0, 0, 0, 1, 1), (0, 0, 0, 0, 2), (2, 0, 1, 0, 0), (0, 2, 1, 0, 0)]

    def in_ideal(m):
        return any(all(a >= b for a, b in zip(m, g)) for g in gens)

    def in_intersection(m):
        # I(e_0) ∩ I(e_1) ∩ I(e_2)^2 for monomials
        return (any(m[i] for i in (1, 2, 3, 4)) and any(m[i] for i in (0, 2, 3, 4))
                and m[0] + m[1] + m[3] + m[4] >= 2)

    for dgr in range(1, 8):
        for m in el.monomials(5, dgr):
            assert in_ideal(m) == in_intersection(m)
    quartics = el.monomials(5, 4)
    assert sorted(m for m in quartics if not in_ideal(m)) == sorted(EXCLUDED)
    # generated in degree 4 from degree 4 on, and Hilbert function 7 in every degree >= 2
    for dgr in range(5, 8):
        mons = el.monomials(5, dgr)
        for m in mons:
            if in_ideal(m):
                assert any(m[i] and in_ideal(tuple(a - (1 if b == i else 0) for b, a in enumerate(m)))
                           for i in range(5))
        assert sum(1 for m in mons if not in_ideal(m)) == 7
    assert sum(1 for m in quartics if not in_ideal(m)) == 7
    # dehomogenisation at h = x0 + x1 = 1: x2, x3, x4 and x0 x1 = x1 (1 - x1)
    h = {unit(5, 0): 1, unit(5, 1): 1}
    h3 = el.pmul(el.pmul(h, h), h)
    for k in (2, 3, 4):
        assert all(in_ideal(e) for e in el.pmul(h3, {unit(5, k): 1}))
    assert all(in_ideal(e) for e in el.pmul(el.pmul(h, h), {(1, 1, 0, 0, 0): 1}))


def test_forced_points_reduced_two_ways(cache):
    # tangent-space criterion (exact): N -> N_22 and N -> N_11 are injective on N(z)
    for n, dim in ((9, 6), (10, 4), (11, 2), (12, 1)):
        z = el.ensemble(el.geometry_witness_tangents(2, n, 0))[1]
        assert el.forced_point_tangent_ranks(z) == (dim, dim, dim)
    # Jacobian criterion on the minors at n = 10: the affine Jacobian at E_1 = e_0 has the rows
    # (coefficients of x0^3 x_j, j = 1..4), at E_2 = e_1 the rows (coefficients of x1^3 x_j)
    d = cache("geometry", 10, 0)
    polys = [f for _, f in d["minors"]]

    def cubic_times(i, j):
        return tuple((3 if a == i else 0) + (1 if a == j else 0) for a in range(5))

    J1 = [[f.get(cubic_times(0, j), 0) for j in (1, 2, 3, 4)] for f in polys]
    J2 = [[f.get(cubic_times(1, j), 0) for j in (0, 2, 3, 4)] for f in polys]
    assert el.rank_mod_p(J1, P1) == 4 and el.rank_mod_p(J2, P1) == 4       # so rank 4 over Q


def test_generic_linear_sections_reproduce_the_classical_degree():
    """Control on pencils that do not come from chains: the symmetric 6 x 6 matrices of rank <= 3
    form a Cohen-Macaulay variety of codimension 6 and degree 112 with h-vector
    (1, 6, 21, 56, 21, 6, 1).  A generic 6-dimensional pencil is an Artinian reduction (Hilbert
    function 1, 6, 21, 56, 21, 6, 1, 0), a generic 5-dimensional pencil misses the variety
    (the minors span all 70 quartics).  The chain pencil at n = 10 has Hilbert function 7 instead."""
    pytest.importorskip("flint")
    import item1_pencil as pen
    rnd = random.Random(2026)

    def randsym():
        M = [[0] * 6 for _ in range(6)]
        for i in range(6):
            for j in range(i, 6):
                M[i][j] = M[j][i] = rnd.randint(-50, 50)
        return M

    six = {4: 21, 5: 6, 6: 1, 7: 0} if SLOW else {4: 21, 5: 6, 6: 1}
    for v, expect in ((5, {4: 0, 5: 0}), (6, six)):
        polys = [f for _, f in el.all_4x4_minors([randsym() for _ in range(v)])]
        assert pen.hilbert_function_mod_p(polys, v, sorted(expect), P1) == expect
    assert 1 + 6 + 21 + 56 + 21 + 6 + 1 == 112


@pytest.mark.parametrize("n,v,nmon", [(11, 3, 15), (12, 2, 5)])
def test_n11_n12_two_reduced_points(cache, n, v, nmon):
    d = cache("geometry", n, 0)
    assert d["v"] == v
    polys = [f for _, f in d["minors"]]
    rows = el.dense_rows(polys, v, 4)
    assert len(rows[0]) == nmon
    # vanishing at the two forced points bounds the rank by nmon - 2; equality modulo p proves it
    assert all(f.get(tuple(4 if a == i else 0 for a in range(v)), 0) == 0 for f in polys for i in (0, 1))
    assert el.rank_mod_p(rows, P1) == nmon - 2
    assert d["fams"] == []


def test_n9_has_further_solutions(cache):
    d = cache("geometry", 9, 0)
    assert d["rank"] == 15 and d["v"] == 7
    rows = el.dense_rows([f for _, f in d["minors"]], 7, 4)
    assert len(rows[0]) == 210
    # a zero-dimensional linear section of the rank <= 3 locus would have 105 independent minors
    assert el.rank_mod_p(rows, P1) == 104


def test_planted_error_is_detected(cache):
    """Dropping the last constraint pair (the n = 9 pencil read as if it were n = 10) or using a
    non-adapted basis must break the n = 10 certificate."""
    plain = build("geometry", 10, 0, adapted=False)
    polys = [f for _, f in plain["minors"]]
    assert not all(f.get(e, 0) == 0 for f in polys for e in EXCLUDED)
    assert el.rank_mod_p(el.dense_rows(polys, 5, 4), P1) == 63          # the rank is intrinsic
    d9 = cache("geometry", 9, 0)
    assert el.rank_mod_p(el.dense_rows([f for _, f in d9["minors"]], 7, 4), P1) != 210 - 7


# ------------------------------------------------------------------------------------ 4. item 3
def test_tangent_derivative_against_closed_formula():
    """d x_j / d t_m = (2 / (1 + t_m^2)) u_{m+1} x (x_j - x_{m+2}) for j >= m + 3, 0 otherwise."""
    for tans in (el.geometry_witness_tangents(2, 9, 0)[0], el.eng_witness_tangents(2, 8, 1)[1]):
        x = el.chain_from_tangents(tans)
        ders = i3.chain_tangent_derivatives(tans)
        n = len(x)
        for m, t in enumerate(tans):
            axis = tuple(x[m + 2][c] - x[m + 1][c] for c in range(3))
            fac = 2 / (1 + Fr(t) ** 2)
            for j in range(n):
                if j < m + 3:
                    assert ders[m][j] == (0, 0, 0)
                else:
                    rel = tuple(x[j][c] - x[m + 2][c] for c in range(3))
                    assert ders[m][j] == tuple(fac * c for c in el.cross(axis, rel))


def test_tangent_derivative_against_difference_quotient():
    """The exact derivative is the limit of exact difference quotients: for a rational map of t
    the symmetric quotient with step eps differs from the derivative by O(eps^2)."""
    tans = [Fr(1, 2), Fr(-3), Fr(2, 3), Fr(5, 4)]
    ders = i3.chain_tangent_derivatives(tans)
    for m in range(len(tans)):
        errs = []
        for eps in (Fr(1, 10 ** 3), Fr(1, 10 ** 6)):
            up = el.chain_from_tangents([t + (eps if i == m else 0) for i, t in enumerate(tans)])
            dn = el.chain_from_tangents([t - (eps if i == m else 0) for i, t in enumerate(tans)])
            errs.append(max(abs((up[j][c] - dn[j][c]) / (2 * eps) - ders[m][j][c])
                            for j in range(len(up)) for c in range(3)))
        assert errs[0] < Fr(1, 10 ** 4) and errs[1] < Fr(1, 10 ** 10) and errs[1] < errs[0] / 10 ** 4


def test_item3_K2_ranks():
    # (a) conic system: 21 x 21 of rank 20 at n = 12; 19 x 21 of rank 19 at n = 11
    for fn, idx in ((el.eng_witness_tangents, 0), (el.geometry_witness_tangents, 0)):
        for n, rows, rank in ((12, 21, 20), (11, 19, 19)):
            C = el.conic_matrix(el.ensemble(fn(2, n, idx))[1])
            assert (len(C), len(C[0])) == (rows, 21)
            assert el.rank_bareiss(C) == rank == el.rank_mod_p(C, P1) == el.rank_exact(C)
    # (b) Jacobians
    tans, w = el.eng_witness_tangents(2, 7, 0), i3.eng_weights(2, 0)
    assert w == [Fr(1, 3), Fr(2, 3)]
    J = i3.jacobian(tans, w, i3.all_pairs(7))
    assert (len(J), len(J[0])) == (21, 9) and el.rank_bareiss(J) == 9
    # rows of pairs at separation 1 and 2 vanish identically
    assert all(all(x == 0 for x in row) for row, (i, j) in zip(J, i3.all_pairs(7)) if j - i <= 2)
    Jb = i3.jacobian(tans, w, i3.band_pairs(7, 5))
    assert (len(Jb), len(Jb[0])) == (9, 9) and el.rank_bareiss(Jb) == 9
    Jc = i3.jacobian(tans, w, i3.band_pairs(7, 4))
    assert (len(Jc), len(Jc[0])) == (7, 9) and el.rank_bareiss(Jc) == 7
    tans6 = el.eng_witness_tangents(2, 6, 0)
    J6 = i3.jacobian(tans6, w, i3.all_pairs(6))
    assert len(J6[0]) == 7 and el.rank_bareiss(J6) == 6
    # their witness (re-derived), same numbers
    tg, wg = i3.geometry_jacobian_witness(2, 7, 0)
    assert sum(wg) == 1 and all(x > 0 for x in wg)
    assert el.rank_bareiss(i3.jacobian(tg, wg, i3.band_pairs(7, 5))) == 9
    assert el.rank_bareiss(i3.jacobian(tg, wg, i3.all_pairs(7))) == 9


def test_item3_weight_columns_are_differences_of_distance_matrices():
    tans, w = el.eng_witness_tangents(3, 9, 0), i3.eng_weights(3, 0)
    chains = [el.chain_from_tangents(t) for t in tans]
    pairs = i3.band_pairs(9, 9)
    J = i3.jacobian(tans, w, pairs)
    for row, (i, j) in zip(J, pairs):
        d = [sum((ch[j][c] - ch[i][c]) ** 2 for c in range(3)) for ch in chains]
        assert row[-2:] == [d[0] - d[2], d[1] - d[2]]
        # M_ij is linear in the weights: the torsion columns scale with w_k
    J2 = i3.jacobian(tans, [Fr(1, 3)] * 3, pairs)
    for row, row2 in zip(J, J2):
        for k in range(3):
            for m in range(6):
                assert row[6 * k + m] * Fr(1, 3) == row2[6 * k + m] * w[k]


def test_item3_K3_ranks():
    # conic: 43 x 45 of rank 43 at n = 23; 41 x 45 of rank 41 at n = 22 (integer configuration:
    # same rank, smaller numbers for the pure-Python elimination)
    for n, rows, rank in ((23, 43, 43), (22, 41, 41)):
        z = el.ensemble(el.eng_witness_tangents(3, n, 0))[1]
        zi, dens = el.integer_configuration(z)
        C = el.conic_matrix(zi)
        assert (len(C), len(C[0])) == (rows, 45)
        assert el.rank_mod_p(C, P1) == rank == el.rank_mod_p(el.conic_matrix(z), P1)
        assert el.rank_bareiss(C) == rank
    tans, w = el.eng_witness_tangents(3, 9, 0), i3.eng_weights(3, 0)
    J = i3.jacobian(tans, w, i3.band_pairs(9, 9))
    assert (len(J), len(J[0])) == (21, 20) and el.rank_bareiss(J) == 20
    tans, w = el.eng_witness_tangents(3, 11, 0), i3.eng_weights(3, 0)
    Jb = i3.jacobian(tans, w, i3.band_pairs(11, 6))
    assert (len(Jb), len(Jb[0])) == (26, 26) and el.rank_bareiss(Jb) == 26
    Jc = i3.jacobian(tans, w, i3.band_pairs(11, 5))
    assert (len(Jc), len(Jc[0])) == (21, 26) and el.rank_mod_p(Jc, P1) == 21


def test_integer_configuration_preserves_the_conic_rank():
    z = el.ensemble(el.geometry_witness_tangents(2, 11, 3))[1]
    zi, dens = el.integer_configuration(z)
    assert all(isinstance(x, int) for p in zi for x in p) and all(d > 0 for d in dens)
    assert all(zi[i][c] == z[i][c] * dens[c] for i in range(len(z)) for c in range(6))
    assert el.rank_bareiss(el.conic_matrix(zi)) == el.rank_bareiss(el.conic_matrix(z)) == 19


# ------------------------------------------------------------------------------------ 5. stored results
def _load(name):
    path = EXP / "results" / name
    if not path.exists():
        pytest.skip("result file %s not present" % name)
    return json.loads(path.read_text())


def test_stored_pencil_results(cache):
    data = _load("item1_pencil.json")
    assert data["geometry_commit"] == "d84a43b"
    by = {(r["witness"], r["n"]): r for r in data["results"]}
    assert len(by) == 32
    expect = {9: (15, 104, 210), 10: (17, 63, 70), 11: (19, 13, 15), 12: (20, 3, 5)}
    for (wit, n), r in by.items():
        rank, span, nmon = expect[n]
        assert r["chain_constraints_exact"] and r["forced_points"]["reduced"]
        assert r["linear_system"]["rank"] == rank
        assert r["minors"]["span_rank_over_Q"] == span and r["minors"]["quartic_monomials"] == nmon
        assert set(r["minors"]["span_rank_mod_p"].values()) == {span}
        assert r["minors_vanish_at_forced_points"]
        if n == 10:
            c = r["n10_certificate"]
            assert c["all_minors_have_zero_coefficient_on_excluded_monomials"]
            assert c["J4_is_the_span_of_the_63_other_quartic_monomials"] and c["targets_in_Q_span_of_minors"]
            assert [f["projective_dimension_of_family"] for f in r["rank2_quadrics_in_N"]] == [0]
        if n in (11, 12):
            assert r["two_reduced_points_only"] and r["rank2_quadrics_in_N"] == []
        if n == 9:
            assert sorted(f["projective_dimension_of_family"] for f in r["rank2_quadrics_in_N"]) == [0, 0, 1, 1]
            for hf in r["hilbert_function_mod_p"].values():
                assert all(hf[str(dg)] == 12 * dg + 58 for dg in (4, 5, 6) if str(dg) in hf)
    # the stored lists of rank-2 quadrics at infinity are the ones the current code computes
    for (wit, n), r in by.items():
        kind, index = wit.rsplit("_", 1)[0].replace("_seed", ""), int(wit.rsplit("_", 1)[1])
        tans = (el.geometry_witness_tangents if kind == "geometry" else el.eng_witness_tangents)(2, n, index)
        assert r["tangents"] == [[str(t) for t in row] for row in tans]
        fams = el.rank2_families_at_infinity(el.ensemble(tans)[1])
        assert r["rank2_quadrics_in_N"] == [
            {"lambda_bonds": f["lambda_bonds"], "mu_bonds": f["mu_bonds"],
             "projective_dimension_of_family": f["dimension"]} for f in fams]
    rem = {x["n"]: sorted(f["projective_dimension_of_family"] for f in x["families"])
           for x in data["remark_rank2_quadrics_K3"]}
    assert rem == {15: [0, 0, 0, 0, 0, 1, 1], 16: [0], 17: []}
    # the stored main witness and its point at infinity are the ones recomputed here
    r = by[("geometry_seed_0", 10)]
    assert r["tangents"] == MAIN_TANGENTS_N10
    d = cache("geometry", 10, 0)
    lam, mu = d["fams"][0]["ann_lambda"][0], d["fams"][0]["ann_mu"][0]
    assert r["point_at_infinity"]["lambda"] == [str(x) for x in lam]
    assert r["point_at_infinity"]["mu"] == [str(x) for x in mu]
    assert r["n10_certificate"]["basis_matrices"]["B3"] == [[str(x) for x in row] for row in d["mats"][3]]
    assert r["chains"] == [[[str(c) for c in atom] for atom in ch] for ch in d["chains"]]


def test_stored_item3_results():
    data = _load("item3_ranks.json")
    assert data["claims_not_confirmed"] == [] and data["all_Q_ranks_equal_both_modular_ranks"]
    conic = {(s["K"], s["n"]): s for s in data["summary"] if s["claim"].startswith("conic")}
    for K, n0, DK in ((2, 12, 20), (3, 23, 43), (4, 39, 75)):
        assert set(conic[(K, n0)]["eng_ranks_Q"]) == {DK}
        assert set(conic[(K, n0)]["geometry_seed_ranks_Q"]) == {DK}
        assert set(conic[(K, n0 - 1)]["eng_ranks_Q"]) == {2 * (n0 - 1) - 3}
    full = [s for s in data["summary"] if "full column rank" in s["claim"]]
    assert sorted((s["K"], s["n"], s["target"]) for s in full) == \
        [(2, 7, 9), (2, 7, 9), (3, 9, 20), (3, 11, 26), (4, 11, 35), (4, 16, 55)]
    assert all(s["confirmed"] and s["first_geometry_seed_reaching_target_mod_2147483629"] == 0 for s in full)
    # recompute one stored number of each kind
    assert el.rank_bareiss(el.conic_matrix(el.ensemble(el.eng_witness_tangents(2, 12, 2))[1])) == 20


def test_affine_pipeline_mod_p_n10_and_n11(cache):
    """The pipeline that finds 48 affine points at n = 9 finds exactly the two forced ones at
    n = 10 and n = 11 (modulo a prime; needs python-flint)."""
    pytest.importorskip("flint")
    pytest.importorskip("numpy")
    import item1_affine_solutions as aff
    for n in (10, 11):
        d = cache("geometry", n, 0)
        info, ops = aff.affine_part_mod_p([f for _, f in d["minors"]], d["v"], P1)
        assert info["affine_degree_m"] == 2 and info["stable"] and info["affine_scheme_reduced_mod_p"]
        assert info["operators_commute"] and info["forced_points_among_roots"]
        assert aff.rank3_check_mod_p(d["mats"], ops, P1)
        assert info["HF_degree_7"] == (7 if n == 10 else 2)


@pytest.mark.skipif(not SLOW, reason="slow (set GEOMREQ1_SLOW=1): 40 s")
def test_affine_pipeline_mod_p_n9(cache):
    pytest.importorskip("flint")
    import item1_affine_solutions as aff
    d = cache("geometry", 9, 0)
    info, ops = aff.affine_part_mod_p([f for _, f in d["minors"]], d["v"], P1)
    assert info["HF_degree_7"] == 142 and info["affine_degree_m"] == 48
    assert info["rank_of_h^k_S_(7-k)_in_A_7"] == {"1": 65, "2": 50, "3": 48, "4": 48}
    assert info["affine_scheme_reduced_mod_p"] and aff.rank3_check_mod_p(d["mats"], ops, P1)


def test_stored_n9_solutions_recertified():
    """The stored real positive semidefinite solutions at n = 9 are re-certified from their 30
    stored digits by a fresh Krawczyk test in ball arithmetic, with the exact rational data."""
    pytest.importorskip("flint")
    np = pytest.importorskip("numpy")
    import item1_affine_solutions as aff
    path = EXP / "results" / "item1_affine_solutions.json"
    if not path.exists():
        path = EXP / "results" / "item1_affine_solutions_quick.json"
    if not path.exists():
        pytest.skip("no stored affine solutions")
    data = json.loads(path.read_text())
    r = next(x for x in data["results"] if x["witness"] == "geometry_seed_0" and x["n"] == 9)
    assert r["affine_solutions_mod_p"] == 48 and r["non_forced_affine_solutions_mod_p"] == 46
    c = r["certified"]
    assert c["non_forced_certified"] == 46 and c["matches_modular_count"] and c["boxes_pairwise_disjoint"]
    assert (c["real"], c["non_real"]) == (28, 18)
    assert (c["real_positive_semidefinite"], c["real_not_semidefinite"], c["real_undecided"]) == (4, 24, 0)
    assert c["forced_points_recovered"] == ["E_1", "E_2"]
    z = el.ensemble(el.geometry_witness_tangents(2, 9, 0))[1]
    psd = [s for s in r["solutions"] if s.get("definiteness", "").startswith("positive")]
    assert len(psd) == 4
    cands = [(np.array([[float(x) for x in row] for row in s["P"]], dtype=complex), 0) for s in psd]
    again = aff.certify_all(z, cands)
    assert len(again) == 4
    for s in again:
        assert s["certified"] and s["real"] and s["forced_point"] is None
        assert s["definiteness"].startswith("positive") and s["signs_tr_e2_det_of_S"] == [1, 1, 1]
    assert aff.pairwise_disjoint(again)
    # each stored P satisfies the 15 linear equations to the stored precision (exact rationals
    # for the data, 30 decimal digits for P), and has numerical rank 3
    A, b = el.linear_system(z)
    idx = el.sym_index(6)
    for s in psd:
        P = [[Fr(x) for x in row] for row in s["P"]]
        vec = [P[i][j] for (i, j) in idx]
        scale = max(abs(x) for x in vec)
        assert all(abs(sum(a * x for a, x in zip(row, vec)) - rhs) < Fr(1, 10 ** 24) * (1 + scale)
                   for row, rhs in zip(A, b))
        sv = np.linalg.svd(np.array([[float(x) for x in row] for row in P]), compute_uv=False)
        assert sv[2] > 1e-3 and sv[3] < 1e-12


def test_n9_functionals_at_infinity(cache):
    """Ingredient (2) of the exact count at n = 9: the 130 functionals built from the rank-2
    locus at infinity have rank 94 modulo p, the Hessian kernels have dimension 8 = 28 - 20, and
    every functional annihilates h^3 S_4 and (sampled) products of a cubic monomial and a minor."""
    flint = pytest.importorskip("flint")
    pytest.importorskip("numpy")
    pytest.importorskip("scipy")
    import item1_n9_exact_count as ec
    d = cache("geometry", 9, 0)
    polys = [f for _, f in d["minors"]]
    rows, info = ec.functionals_at_infinity(d["z"], d["mats"], polys, P1)
    assert info["lines"] == 2 and info["isolated_points"] == 2
    assert info["hessian_kernel_dimensions"] == [8, 8] and info["hessian_ranks_mod_p"] == [20, 20]
    assert len(rows) == 2 * (8 + 49) + 16
    assert int(flint.nmod_mat(rows, P1).rank()) == 94
    mons = el.monomials(7, 7)
    pos = {e: i for i, e in enumerate(mons)}

    def pairing(poly):
        vec = [0] * len(mons)
        for e, c in poly.items():
            vec[pos[e]] = c % P1
        return [sum(a * b for a, b in zip(row, vec)) % P1 for row in rows]

    rnd = random.Random(9)
    h = {unit(7, 0): 1, unit(7, 1): 1}
    h3 = el.pmul(el.pmul(h, h), h)
    for m4 in rnd.sample(el.monomials(7, 4), 12):
        assert not any(pairing(el.pmul(h3, {m4: 1})))
    for _ in range(12):
        f = rnd.choice(polys)
        m3 = rnd.choice(el.monomials(7, 3))
        assert not any(pairing(el.pmul({m3: 1}, f)))
    # a functional that does NOT belong to the list is detected: evaluation at a random point
    x = [rnd.randrange(1, P1) for _ in range(7)]
    ev = []
    for e in mons:
        val = 1
        for xi, a in zip(x, e):
            val = val * pow(xi, a, P1) % P1
        ev.append(val)
    f = polys[0]
    m3 = (1, 1, 1, 0, 0, 0, 0)
    prod = el.pmul({m3: 1}, f)
    assert sum(ev[pos[e]] * (c % P1) for e, c in prod.items()) % P1 != 0


def test_stored_n9_exact_count():
    data = _load("item1_n9_exact_count.json")
    assert data["geometry_commit"] == "d84a43b"
    expect = {"geometry_seed_0": (28, 4, 24, 18), "geometry_seed_1": (24, 8, 16, 22)}
    names = [r["witness"] for r in data["results"]]
    assert set(expect) <= set(names) and "geometry_seed_0_n10_without_last_atom" in names
    for r in data["results"]:
        assert r["proved"] and r["forced_points_reduced"]
        assert r["step1_macaulay_rank_mod_p"] == 1574 and r["step1_dim_W_at_most"] == 142
        s2, s3 = r["step2"], r["step3"]
        assert s2["rank_mod_p"] == 94 and s2["functionals"] == 130
        assert s2["guard_all_annihilate_J7_mod_p"] and s2["guard_all_annihilate_h3_S4_mod_p"]
        assert s3["points"] == 48 and s3["non_forced"] == 46 and s3["boxes_pairwise_disjoint"]
        assert s3["evaluations_independent_on_cubics"] and s3["all_non_forced_of_rank_3"]
        assert s3["real"] + s3["non_real"] == 46 and s3["real_undecided"] == 0
        assert s3["real_positive_semidefinite"] + s3["real_not_semidefinite"] == s3["real"]
        if r["witness"] in expect:
            assert (s3["real"], s3["real_positive_semidefinite"], s3["real_not_semidefinite"],
                    s3["non_real"]) == expect[r["witness"]]
        if r["witness"] == "geometry_seed_0_n10_without_last_atom":
            x = r["extension_to_n10"]
            assert x["only_forced_points_survive"] and x["non_forced_solutions"] == 46
            assert r["tangents"] == [row[:6] for row in MAIN_TANGENTS_N10]


def test_stored_affine_solutions_all_witnesses():
    data = _load("item1_affine_solutions.json")
    expect = {"geometry_seed_0": (28, 4), "geometry_seed_1": (24, 8), "geometry_seed_2": (26, 6),
              "eng_0": (16, 2), "eng_1": (32, 6)}
    seen = set()
    for r in data["results"]:
        if r["n"] == 9:
            c = r["certified"]
            assert r["affine_solutions_mod_p"] == 48 and c["non_forced_certified"] == 46
            assert c["matches_modular_count"] and c["boxes_pairwise_disjoint"] and c["all_of_rank_3"]
            assert c["real"] + c["non_real"] == 46 and c["neither_certified_real_nor_non_real"] == 0
            assert (c["real"], c["real_positive_semidefinite"]) == expect[r["witness"]]
            assert c["real_undecided"] == 0
            seen.add(r["witness"])
        else:
            assert r["affine_solutions_mod_p"] == 2 and "certified" not in r
        for info in r["modular"].values():
            assert info["affine_scheme_reduced_mod_p"] and info["operators_commute"]
            assert info["all_affine_points_have_rank_3"] and info["stable"]
    assert seen == set(expect)


def test_krawczyk_rejects_a_shifted_box():
    """The interval certificate is not vacuous: around a refined solution the test passes; around
    a point shifted by 1e-12 (box radius about 1e-18) it must fail; a box around a real solution
    cannot be certified for a wrong system (one right-hand side changed)."""
    flint = pytest.importorskip("flint")
    np = pytest.importorskip("numpy")
    import item1_affine_solutions as aff
    data = _load("item1_affine_solutions.json")
    r = next(x for x in data["results"] if x["witness"] == "geometry_seed_0" and x["n"] == 9)
    s = next(x for x in r["solutions"] if x.get("definiteness", "").startswith("positive")
             and x["chart"] == "12")
    z = el.ensemble(el.geometry_witness_tangents(2, 9, 0))[1]
    P0 = np.array([[float(v) for v in row] for row in s["P"]], dtype=complex)
    x, cond = aff.polish_float(P0, z, "12")
    C = aff.Certifier(z, "12")
    xr = C.refine(x)
    ok, X = C.krawczyk(xr, True)
    assert ok
    shifted = list(xr)
    shifted[0] = flint.acb(shifted[0].real.mid() + flint.arb("1e-12"), 0)
    bad, _ = C.krawczyk(shifted, True)
    assert not bad
    C.l2[3] = C.l2[3] + flint.acb(flint.arb("1e-9"))      # a different system
    worse, _ = C.krawczyk(xr, True)
    assert not worse
