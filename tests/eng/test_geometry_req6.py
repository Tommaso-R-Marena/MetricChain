"""Tests of the certified computations for GEOMETRY-REQ-0006 (experiments/eng/geometry_req6; the
request and the definitions are at commit 288b2de of research/geometric-inference).

Layers:
  1. the ball arithmetic the certificates rely on (directions of rounding, comparisons);
  2. the chain model: the multi-affine forms against an independent transcription of the NeRF
     recursion (mpmath, 60 digits) on a full interpolation grid; unit bonds and the bond angle;
     the structural facts (even in theta, no monomial with both end torsions);
  3. the trusted primitives: hulls of arcs, ranges of forms, the bounds H_upper and G_upper against
     sampling, the Gershgorin enclosure, the Krawczyk test (positive and negative cases),
     tilings;
  4. the certificates of (Q-a) (reduced and direct) and (Q-b) on instance A, recomputed and
     compared with the stored records; the stored list of excluded boxes re-checked;
  5. soundness: boxes that contain points above the threshold are never excluded; perturbed
     inputs are not certified;
  6. the controls of the request (runner-up claimed global, wrong sign, semidefinite stress,
     flat realisation, six atoms).

Needs python-flint (Arb), numpy, scipy, mpmath.  Runs in well under a minute.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

import pytest

flint = pytest.importorskip("flint")
np = pytest.importorskip("numpy")
mpmath = pytest.importorskip("mpmath")

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "eng" / "geometry_req6"
sys.path.insert(0, str(EXP))

import gr6_common as common  # noqa: E402
import gr6_controls as controls  # noqa: E402
import gr6_kernel as kernel  # noqa: E402
import gr6_model as model  # noqa: E402
import gr6_qa_proof as QA  # noqa: E402
import gr6_qb_proof as QB  # noqa: E402
import gr6_records as records  # noqa: E402
import gr6_search as search  # noqa: E402
from flint import arb, ctx  # noqa: E402

RESULTS = EXP / "results"
SILENT = lambda *a: None  # noqa: E731


@pytest.fixture(autouse=True)
def _precision():
    old = ctx.prec
    kernel.set_precision()
    yield
    ctx.prec = old


@pytest.fixture(scope="module")
def inst_a():
    kernel.set_precision()
    rec, obj = records.certificate_record(common.INSTANCE_A, log=SILENT)
    return rec, obj


def exact(x):
    """(mid, rad) of a ball as exact Fractions."""
    return kernel.to_fraction(x.mid()), kernel.to_fraction(x.rad())


# ------------------------------------------------------------------ 1. ball arithmetic
def test_lower_upper_round_outwards():
    rng = random.Random(1)
    for _ in range(300):
        x = arb(Fr(rng.randint(-10 ** 9, 10 ** 9), rng.randint(1, 10 ** 9)).numerator) / rng.randint(1, 10 ** 9)
        x = x * arb(rng.randint(1, 7)).sqrt() + arb(0, 10.0 ** -rng.randint(1, 40))
        mid, rad = exact(x)
        lo, hi = x.lower(), x.upper()
        assert lo.is_exact() and hi.is_exact()
        assert kernel.to_fraction(lo) <= mid - rad and kernel.to_fraction(hi) >= mid + rad
        assert kernel.to_fraction(x.abs_upper()) >= max(abs(mid - rad), abs(mid + rad))
        assert kernel.to_fraction(abs(x).upper()) >= max(abs(mid - rad), abs(mid + rad))


def test_comparisons_are_certain():
    a, b = arb(0, 1), arb(0.5, 0.25)
    assert not (a < b) and not (b < a) and not (a <= b) and not (a >= b)       # overlapping balls
    assert arb(0, 1) < 2 and not (arb(0, 1) < 1)
    assert arb(1) < arb(2) and arb(1) <= arb(1) and not (arb(1) < arb(1))
    assert arb(0.5, 0.25).contains_integer() is False and arb(0.5, 0.75).contains_integer() is True
    # (a radius is stored rounded up: arb(0, 1) is slightly larger than [-1, 1])
    assert arb(0, 1).contains_interior(arb(0.5, 0.25)) and not arb(0, 1).contains_interior(arb(0.5, 0.51))
    assert not arb(0, 1).contains_interior(arb(0, 1)) and arb(0, 1).contains(arb(0, 1))
    u = arb(2).union(arb(3))
    assert u.lower() <= 2 and u.upper() >= 3
    z = arb(0, 1e-3)
    assert z.upper() >= 1e-3 and z.lower() <= -1e-3


def test_rational_balls_and_trigonometry():
    mpmath.mp.prec = 400
    for num, den in [(1, 3), (37, 60), (-5, 7), (123456789, 2 ** 40), (7, 3), (-11, 4)]:
        q = Fr(num, den)
        b = kernel.ball(q)
        mid, rad = exact(b)
        assert abs(mid - q) <= rad
        _, c, s = kernel.point(q)
        for val, ref in ((c, mpmath.cos(mpmath.pi * num / den)), (s, mpmath.sin(mpmath.pi * num / den))):
            mid, rad = exact(val)
            assert abs(mpmath.mpf(mid.numerator) / mid.denominator - ref) <= mpmath.mpf(rad.numerator) / rad.denominator + mpmath.mpf(2) ** -380
    # a ball argument: the enclosure contains the values at points of the ball
    t = arb(Fr(1, 3).numerator) / 3 + arb(0, 1e-3)
    _, c, s = kernel.point(t)
    for d in (-1e-3, -3e-4, 0.0, 9e-4, 1e-3):
        x = mpmath.mpf(1) / 3 + d
        assert c.contains(arb(float(mpmath.cos(mpmath.pi * x)))) or abs(float(c.mid()) - float(mpmath.cos(mpmath.pi * x))) < float(c.rad())
        assert abs(float(s.mid()) - float(mpmath.sin(mpmath.pi * x))) <= float(s.rad())


def test_decimal_rounding_directions():
    x = Fr(1, 3)
    assert common.dec_down(x, 5) == "0.33333" and common.dec_up(x, 5) == "0.33334"
    assert common.dec_down(-x, 5) == "-0.33334" and common.dec_up(-x, 5) == "-0.33333"
    assert common.dec_down(Fr(5, 4), 3) == "1.250" and common.dec_up(Fr(5, 4), 3) == "1.250"
    lo, hi = common.enclosure(arb(2).sqrt(), 20)
    assert Fr(lo) ** 2 < 2 < Fr(hi) ** 2 and Fr(hi) - Fr(lo) <= Fr(2, 10 ** 20)


# ------------------------------------------------------------------ 2. the chain model
def nerf_mp(taus):
    """Independent transcription of the NeRF recursion of geomlib.chain (mpmath)."""
    mp = mpmath.mp
    th = mp.pi * 37 / 60
    X = [mpmath.matrix([0, 0, 0]), mpmath.matrix([1, 0, 0])]
    X.append(X[1] + mpmath.matrix([-mp.cos(th), mp.sin(th), 0]))

    def cross(u, v):
        return mpmath.matrix([u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]])

    for i in range(3, len(taus) + 3):
        a, b, c = X[i - 3], X[i - 2], X[i - 1]
        bc = (c - b) / mpmath.norm(c - b)
        nrm = cross(b - a, bc)
        nrm = nrm / mpmath.norm(nrm)
        m = cross(nrm, bc)
        t = mp.pi * mpmath.mpf(taus[i - 3].numerator) / taus[i - 3].denominator
        X.append(c - mp.cos(th) * bc + mp.sin(th) * (mp.cos(t) * m + mp.sin(t) * nrm))
    return X


def test_forms_agree_with_nerf_on_an_interpolation_grid():
    """A multi-affine trigonometric polynomial in 4 angles is determined by its values on the
    grid {0, 2/3, 4/3}^4 (tau units): the forms agree there with the NeRF chain to 50 digits,
    for every pair of atoms (and at shifted points)."""
    mpmath.mp.dps = 60
    chain = model.Chain(7)
    forms = {(i, j): chain.sqdist(i, j) for i in range(7) for j in range(i + 1, 7)}
    grid = [Fr(0), Fr(2, 3), Fr(4, 3)]
    points = [(a, b, c, d) for a in grid for b in grid for c in grid for d in grid]
    points += [(Fr(1, 7), Fr(-3, 11), Fr(5, 13), Fr(9, 17)), (Fr(-19, 23), Fr(1, 29), Fr(-2, 3), Fr(31, 37))]
    worst = 0
    for taus in points:
        X = nerf_mp(taus)
        P = [kernel.point(t) for t in taus]
        for (i, j), form in forms.items():
            ref = sum((X[i][k] - X[j][k]) ** 2 for k in range(3))
            val = kernel.ma_eval(form, P)
            mid, rad = exact(val)
            err = abs(mpmath.mpf(mid.numerator) / mid.denominator - ref)
            worst = max(worst, err)
            assert err < mpmath.mpf(10) ** -50 and rad < Fr(1, 10 ** 50)
    assert worst < mpmath.mpf(10) ** -50


def circle(t):
    """The rational point of the unit circle with half-angle tangent t."""
    t = Fr(t)
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def nerf_exact(C, S, cs):
    """The NeRF recursion in exact rational arithmetic: bond angle (C, S) and torsions (c_k, s_k)
    rational points of the circle.  The normal (b - a) x bc of two unit bond vectors at the bond
    angle has length S, so every normalisation is exact."""
    def cross(u, v):
        return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]

    X = [[Fr(0)] * 3, [Fr(1), Fr(0), Fr(0)], [1 - C, S, Fr(0)]]
    for i in range(3, len(cs) + 3):
        a, b, c = X[i - 3], X[i - 2], X[i - 1]
        bc = [c[k] - b[k] for k in range(3)]
        assert sum(x * x for x in bc) == 1
        nrm = [x / S for x in cross([b[k] - a[k] for k in range(3)], bc)]
        assert sum(x * x for x in nrm) == 1
        m = cross(nrm, bc)
        ct, st = cs[i - 3]
        X.append([c[k] - C * bc[k] + S * (ct * m[k] + st * nrm[k]) for k in range(3)])
    return X


def test_forms_agree_exactly_with_nerf_at_rational_points():
    """The construction of the forms is the same code for any point (C, S) of the unit circle; with
    rational bond angles and rational torsion points the squared distances of the exact NeRF
    chain equal the values of the forms, exactly (Fractions), for every pair of atoms."""
    rng = random.Random(7)
    checked = 0
    for tb in (Fr(3, 2), Fr(5, 3), Fr(7, 5), Fr(2), Fr(9, 4), Fr(11, 7), Fr(13, 6), Fr(4, 3)):
        C, S = circle(tb)
        assert C < 0 < S
        chain = model.Chain(7, cos_sin=(C, S))
        forms = {(i, j): chain.sqdist(i, j) for i in range(7) for j in range(i + 1, 7)}
        for _ in range(12):
            cs = [circle(Fr(rng.randint(-40, 40), rng.randint(1, 9))) for _ in range(4)]
            X = nerf_exact(C, S, cs)
            for (i, j), form in forms.items():
                ref = sum((X[i][k] - X[j][k]) ** 2 for k in range(3))
                val = sum(coef * np.prod([Fr(1) if a == 0 else cs[m][a - 1] for m, a in enumerate(alpha)])
                          for alpha, coef in form.items())
                assert val == ref
                checked += 1
        # the same structure as with the bond angle of 111 degrees
        assert {key: sorted(f) for key, f in forms.items()} == \
            {key: sorted(model.Chain(7).sqdist(*key)) for key in forms}
    assert checked == 8 * 12 * 21


def test_bonds_angles_and_structure():
    chain = model.Chain(7)
    C, S = model.bond_angle_cos_sin()
    assert (C * C + S * S - 1).contains(0) and C < 0 and S > 0
    assert abs(float(C) - np.cos(np.deg2rad(111))) < 1e-15
    zero = (0, 0, 0, 0)
    for i in range(6):
        f = chain.sqdist(i, i + 1)
        assert list(f) == [zero] and f[zero].is_exact() and f[zero] == 1          # unit bonds, exactly
    for i in range(5):
        f = chain.sqdist(i, i + 2)
        assert list(f) == [zero] and (f[zero] - (2 - 2 * C)).contains(0) and f[zero].rad() < 1e-50
    # |x_j - x_i|^2 depends only on the torsions i .. j-3, and is even
    for i in range(7):
        for j in range(i + 1, 7):
            f = chain.sqdist(i, j)
            assert not model.odd_sine_monomials(f)
            for alpha in f:
                assert all(a == 0 for m, a in enumerate(alpha) if not i <= m <= j - 3)
    form = chain.energy(common.INSTANCE_A["pairs"], common.INSTANCE_A["couplings"])
    assert len(form) == 21 and not model.odd_sine_monomials(form)
    assert not [alpha for alpha in form if alpha[0] and alpha[3]]
    # a pair spanning both end torsions defeats the reduction (and is detected)
    with pytest.raises(ValueError):
        QA.reduce_ends(chain.sqdist(0, 6))


def test_float_chain_and_request_numbers():
    inst = common.INSTANCE_A
    X = model.nerf_chain(inst["theta_request"])
    assert np.allclose([np.linalg.norm(X[i + 1] - X[i]) for i in range(6)], 1.0, atol=1e-14)
    ang = [np.degrees(np.arccos(np.dot(X[i] - X[i + 1], X[i + 2] - X[i + 1]))) for i in range(5)]
    assert np.allclose(ang, 111.0, atol=1e-10)
    c, info = search.couplings(inst["theta_request"], inst["pairs"])
    assert max(abs(float(r) - x) for r, x in zip(inst["couplings"], c)) <= 5.0000001e-7     # the rounding
    assert abs(search.energy_float(inst["theta_request"], inst["pairs"], c) - 1.170181) < 1e-6   # the request's value
    assert abs(info["stress_singular_values_tail"][1]) < 1e-12 < info["stress_singular_values_tail"][0]
    ev = np.array(info["stress_eigenvalues_signed"])
    assert (ev > 1e-6).sum() == 1 and (ev < -1e-6).sum() == 2                       # indefinite stress
    assert np.allclose(info["hessian_eigenvalues"], [-1.098214, -0.318926, -0.255551, -0.020449], atol=2e-5)
    # the derivative of a form
    form = model.Chain(7).energy(inst["pairs"], inst["couplings"])
    fun, _ = search.form_float(form)
    t = np.array([0.3, -1.1, 2.0, 0.7])
    for k in range(4):
        dfun, _ = search.form_float(model.derivative(form, k))
        e = np.eye(4)[k] * 1e-6
        assert abs(dfun(t) - (fun(t + e) - fun(t - e)) / 2e-6) < 1e-8


# ------------------------------------------------------------------ 3. trusted primitives
def test_arc_hull_contains_the_arc():
    rng = random.Random(2)
    for _ in range(100):
        lo = Fr(rng.randint(-4000, 4000), 1000)
        hi = lo + Fr(rng.randint(1, 500), 1000)
        (_, x0, y0), (_, x1, y1), (_, xq, yq) = kernel.arc_hull(lo, hi)
        det = (x1 - x0) * (yq - y0) - (xq - x0) * (y1 - y0)
        for k in range(9):
            _, x, y = kernel.point(lo + (hi - lo) * Fr(k, 8))
            l1 = ((x - x0) * (yq - y0) - (xq - x0) * (y - y0)) / det
            l2 = ((x1 - x0) * (y - y0) - (x - x0) * (y1 - y0)) / det
            assert all(v > -1e-40 for v in (l1, l2, 1 - l1 - l2))                    # barycentric coordinates >= 0
    assert len(kernel.arc_hull(Fr(1, 3), Fr(1, 3))) == 1
    with pytest.raises(AssertionError):
        kernel.arc_hull(Fr(0), Fr(3, 5))                                             # more than a quarter turn


def _random_box(rng, width_range=(1, 300)):
    box = []
    for _ in range(4):
        lo = Fr(rng.randint(-1000, 1000), 1000)
        box.append((lo, lo + Fr(rng.randint(*width_range), 1000)))
    return box


def test_ranges_and_upper_bounds_against_sampling(inst_a):
    form = inst_a[1]["form"]
    fun, h = search.form_float(form)
    T, tabs = QA.dense(form), QA.tables(QA.reduce_ends(form))
    grad0 = model.derivative(form, 0)
    g0, _ = search.form_float(grad0)
    rng = random.Random(3)
    nrng = np.random.default_rng(3)
    for trial in range(30):
        box = _random_box(rng)
        hulls = [kernel.arc_hull(lo, hi) for lo, hi in box]
        ub = QA.H_upper(T, hulls)
        lo_r, hi_r = kernel.ma_range(form, hulls)
        assert abs(float(ub - hi_r)) < 1e-50                                         # two implementations of the same bound
        lo_g, hi_g = kernel.ma_range(grad0, hulls)
        gub = QA.G_upper(tabs, hulls[1], hulls[2])
        width = max(float(hi - lo) for lo, hi in box) * np.pi
        samples = np.array([[float(lo) + (float(hi) - float(lo)) * u for (lo, hi), u in zip(box, row)]
                            for row in np.vstack([nrng.uniform(0, 1, (60, 4)), nrng.integers(0, 2, (20, 4))])]) * np.pi
        vals = np.array([fun(t) for t in samples])
        assert float(lo_r) - 1e-12 <= vals.min() and vals.max() <= float(ub) + 1e-12
        gv = np.array([g0(t) for t in samples])
        assert float(lo_g) - 1e-12 <= gv.min() and gv.max() <= float(hi_g) + 1e-12
        assert vals.max() <= float(gub) + 1e-12                                      # H <= G <= G_upper on the cylinder
        # second-order sharpness: the excess over the sampled range is O(width^2)
        assert float(ub) - vals.max() < 4.0 * width ** 2 + 1e-9
    # a degenerate box: the bounds are the value at the point
    pt = [(Fr(1, 5),) * 2, (Fr(-1, 3),) * 2, (Fr(7, 9),) * 2, (Fr(-2, 7),) * 2]
    hulls = [kernel.arc_hull(lo, hi) for lo, hi in pt]
    val = kernel.ma_eval(form, [kernel.point(lo) for lo, _ in pt])
    assert val.contains(QA.H_upper(T, hulls)) or (QA.H_upper(T, hulls) - val.upper()) == 0
    # H_upper against the maximum over all 81 vertex tuples, on wide boxes, with every position of
    # the maximising vertex exercised (in particular the apex of each of the four arcs)
    from itertools import product
    apex = [0, 0, 0, 0]
    for trial in range(150):
        box = _random_box(rng, (100, 500))
        hulls = [kernel.arc_hull(lo, hi) for lo, hi in box]
        best, arg = None, None
        for idx in product(range(3), repeat=4):
            v = kernel.ma_eval(form, [hulls[m][i] for m, i in enumerate(idx)]).upper()
            if best is None or best < v:
                best, arg = v, idx
        assert abs(float(QA.H_upper(T, hulls) - best)) < 1e-50
        for m in range(4):
            apex[m] += arg[m] == 2
    assert min(apex) >= 3


def test_G_is_the_partial_maximum(inst_a):
    """G(theta_1, theta_2) = max over theta_0, theta_3 of H (the reduction (R)); the maximum over
    the end torsions is computed from the full coefficient table, not from the reduced forms."""
    form = inst_a[1]["form"]
    red = QA.reduce_ends(form)
    fun, h = search.form_float(form)
    nrng = np.random.default_rng(5)
    grid = np.linspace(-np.pi, np.pi, 181)
    Pg = np.stack([np.ones_like(grid), np.cos(grid), np.sin(grid)])
    for _ in range(40):
        t1, t2 = nrng.uniform(-np.pi, np.pi, 2)
        P = [None, kernel.point(arb(t1) / arb.pi()), kernel.point(arb(t2) / arb.pi()), None]
        a, v1, v2, w1, w2 = [float(kernel.ma_eval(red[k], P).mid()) for k in ("A", "V1", "V2", "W1", "W2")]
        G = a + np.hypot(v1, v2) + np.hypot(w1, w2)
        p1, p2 = np.array([1.0, np.cos(t1), np.sin(t1)]), np.array([1.0, np.cos(t2), np.sin(t2)])
        best = np.einsum("abcd,ai,b,c,dl->il", h, Pg, p1, p2, Pg).max()
        assert best <= G + 1e-12 and G - best < 5e-4                                  # H <= G, nearly attained on a grid
        assert abs(fun([np.arctan2(v2, v1), t1, t2, np.arctan2(w2, w1)]) - G) < 1e-12  # attained at the polar angles


def test_sym_eig_enclosure():
    M = [[arb(2), arb(1)], [arb(1), arb(2)]]
    Q = np.linalg.eigh(np.array([[2.0, 1.0], [1.0, 2.0]]))[1]
    eig = sorted(kernel.sym_eig_enclosure(M, Q), key=lambda iv: float(iv[0]))
    assert eig[0][0] <= 1 <= eig[0][1] and eig[1][0] <= 3 <= eig[1][1]
    assert float(eig[0][1] - eig[0][0]) < 1e-14 and kernel.pairwise_disjoint(eig)
    # with a poor Q the enclosure is wide but still valid
    eig = kernel.sym_eig_enclosure(M, [[1.0, 0.0], [0.0, 1.0]])
    assert all(lo <= 1 and hi >= 3 for lo, hi in eig) and not kernel.pairwise_disjoint(eig)
    # an interval matrix that contains a singular matrix is not certified definite
    M = [[arb(-1, 0.6), arb(1)], [arb(1), arb(-2)]]
    eig = kernel.sym_eig_enclosure(M, np.linalg.eigh(np.array([[-1.0, 1.0], [1.0, -2.0]]))[1])
    assert not all(hi < 0 for _, hi in eig)
    # random symmetric matrices: the true eigenvalues lie in the union of the intervals
    nrng = np.random.default_rng(7)
    for _ in range(20):
        A = nrng.normal(size=(4, 4))
        A = (A + A.T) / 2
        Mb = [[arb(float(A[i, j])) + arb(0, 1e-6) for j in range(4)] for i in range(4)]
        eig = kernel.sym_eig_enclosure(Mb, np.linalg.eigh(A)[1])
        for lam in np.linalg.eigvalsh(A):
            assert any(float(lo) - 1e-12 <= lam <= float(hi) + 1e-12 for lo, hi in eig)
    with pytest.raises(ZeroDivisionError):
        kernel.sym_eig_enclosure([[arb(1), arb(0)], [arb(0), arb(1)]], [[1.0, 2.0], [2.0, 4.0]])


def test_krawczyk_positive_and_negative():
    def f(z):
        return [z[0] * z[0] + z[1] * z[1] - 4, z[0] - z[1]]

    def jac(z):
        return [[2 * z[0], 2 * z[1]], [arb(1), arb(-1)]]

    c = arb(2).sqrt().mid()
    ok, K = kernel.krawczyk(f, jac, [c, c], 2.0 ** -40)
    assert ok and all(k.contains(arb(2).sqrt()) or k.overlaps(arb(2).sqrt()) for k in K)
    assert all(float(k.rad()) < 1e-20 for k in K)
    # no zero in the box
    ok, K = kernel.krawczyk(f, jac, [arb(1.5), arb(1.5)], 2.0 ** -10)
    assert not ok and K is None
    # a double zero (singular Jacobian): never certified
    ok, K = kernel.krawczyk(lambda z: [z[0] * z[0]], lambda z: [[2 * z[0]]], [arb(0)], 2.0 ** -20)
    assert not ok
    ok, K = kernel.krawczyk(lambda z: [z[0] * z[0]], lambda z: [[2 * z[0]]], [arb(2.0 ** -30)], 2.0 ** -20)
    assert not ok
    with pytest.raises(AssertionError):
        kernel.krawczyk(f, jac, [arb(2).sqrt(), arb(2).sqrt()], 2.0 ** -40)           # the centre must be exact


def test_direction_halfwidth_contains_the_polar_angles(inst_a):
    form = inst_a[1]["form"]
    red = QA.reduce_ends(form)
    nrng = np.random.default_rng(13)
    rng = random.Random(13)
    done = 0
    for _ in range(60):
        lo1, lo2 = Fr(rng.randint(-1000, 1000), 1000), Fr(rng.randint(-1000, 1000), 1000)
        w = Fr(rng.randint(1, 40), 1000)
        sides = [(lo1, lo1 + w), (lo2, lo2 + w)]
        hulls = [[None], kernel.arc_hull(*sides[0]), kernel.arc_hull(*sides[1]), [None]]
        mid = [None, kernel.point((lo1 + lo1 + w) / 2), kernel.point((lo2 + lo2 + w) / 2), None]
        for names in (("V1", "V2"), ("W1", "W2")):
            f1, f2 = (float(kernel.ma_eval(red[k], mid).mid()) for k in names)
            tau0 = Fr(int(round(np.arctan2(f2, f1) / np.pi * 2 ** 30)), 2 ** 30)
            rho = QA.direction_halfwidth(red[names[0]], red[names[1]], tau0, hulls)
            if rho is None:
                continue
            done += 1
            worst = 0.0
            for u1, u2 in np.vstack([nrng.uniform(0, 1, (40, 2)), [[0, 0], [0, 1], [1, 0], [1, 1]]]):
                P = [None, kernel.point(arb(float(lo1 + w * Fr(float(u1))))), kernel.point(arb(float(lo2 + w * Fr(float(u2))))), None]
                g1, g2 = (float(kernel.ma_eval(red[k], P).mid()) for k in names)
                dev = abs(np.angle(np.exp(1j * (np.arctan2(g2, g1) - float(tau0) * np.pi)))) / np.pi
                worst = max(worst, dev)
            assert worst <= float(rho) * (1 + 1e-9) and float(rho) < 4 * worst + 1e-3
    assert done > 60
    # a box on which V passes through zero is refused
    fun = lambda t1, t2: np.hypot(*[float(kernel.ma_eval(red[k], [None, kernel.point(arb(t1)), kernel.point(arb(t2)), None]).mid())
                                    for k in ("V1", "V2")])  # noqa: E731
    from scipy.optimize import minimize
    z = minimize(lambda x: fun(x[0], x[1]), [0.1, 0.1], method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-14)).x
    assert fun(z[0], z[1]) < 1e-6
    sides = [(Fr(float(z[0])) - Fr(1, 100), Fr(float(z[0])) + Fr(1, 100)), (Fr(float(z[1])) - Fr(1, 100), Fr(float(z[1])) + Fr(1, 100))]
    hulls = [[None], kernel.arc_hull(*sides[0]), kernel.arc_hull(*sides[1]), [None]]
    assert QA.direction_halfwidth(red["V1"], red["V2"], Fr(1, 3), hulls) is None


def test_local_step_requires_every_box_to_be_covered(inst_a):
    form, centre, r = inst_a[1]["form"], inst_a[1]["centre"], inst_a[1]["result"]
    local = lambda sides, c: QA.local_certificate(form, sides, c)  # noqa: E731
    select = lambda c: c[1:3]  # noqa: E731
    groups, ok = QA._local_step(local, r["unresolved"], centre, select)
    assert ok and len(groups) == 2
    level = r["unresolved"][0][0]
    stray = (level, 5, 5)
    assert stray not in r["unresolved"]
    groups, ok = QA._local_step(local, r["unresolved"] + [stray], centre, select)
    assert not ok and len(groups) == 3
    # only one of the two neighbourhoods: not accepted either
    half = [b for b in r["unresolved"] if QA.inside(b, r["groups"][0]["sides"])]
    assert not QA._local_step(local, half, centre, select)[1]


def test_singular_values_of_flat_and_spatial_configurations():
    flat = [[arb(x) for x in row] for row in [[0, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [0, 2, 1, 0], [3, 1, 2, 0], [1, 3, 5, 0]]]
    sig, disjoint, smallest = QB.singular_values(flat)
    assert sig is None and not smallest > 0
    full = [[arb(x) for x in row] for row in [[0, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [0, 2, 1, 0], [3, 1, 2, 1], [1, 3, 5, 0]]]
    sig, disjoint, smallest = QB.singular_values(full)
    ref = np.linalg.svd(np.array([[float(x) for x in row] for row in full]) - np.mean([[float(x) for x in row] for row in full], 0), compute_uv=False)
    assert smallest > 0 and abs(float(smallest) - ref[3]) < 1e-9
    assert sorted(round(float(lo), 9) for lo, _ in sig) == sorted(round(x, 9) for x in ref)


def test_tilings_and_groups():
    roots = QA.root_boxes(3, 2)
    assert len(roots) == 64 and QA.is_partition(roots)
    kids = QA.children(roots[5])
    assert len(kids) == 4 and QA.is_partition([b for b in roots if b != roots[5]] + kids)
    assert not QA.is_partition(roots[:-1])                                           # a hole
    assert not QA.is_partition(roots + kids[:1])                                     # an overlap
    assert not QA.is_partition(roots[:-1] + [roots[0]])                              # a repetition
    assert QA.is_partition(QA.root_boxes(2, 4)) and len(QA.children((2, 0, 1, 2, 3))) == 16
    assert QA.grid_arc(3, 0) == (Fr(-1), Fr(-3, 4)) and QA.grid_arc(3, 7) == (Fr(3, 4), Fr(1))
    # groups across the seam: boxes 0 and 7 of level 3 touch through theta = +-pi
    groups = QA.clusters([(3, 0, 2), (3, 7, 2), (3, 3, 5)])
    assert len(groups) == 2
    for sides, members in groups:
        assert all(QA.inside(b, sides) for b in members)
    seam = next(sides for sides, members in groups if len(members) == 2)
    assert seam[0][1] - seam[0][0] == Fr(1, 2)
    assert QA.inside((4, 0, 4), seam) and not QA.inside((3, 1, 2), seam)
    assert QA.point_inside([Fr(-7, 8), Fr(-3, 8)], seam) and not QA.point_inside([Fr(0), Fr(0)], seam)
    assert QA.interiors_meet((3, 0, 2), seam) and not QA.interiors_meet((3, 1, 2), seam)


# ------------------------------------------------------------------ 4. the certificates on instance A
def test_qa_reduced_certificate(inst_a):
    rec, obj = inst_a
    r = obj["result"]
    assert rec["certified"] and r["certified"] and r["distinct"]
    assert rec["branch_and_bound"]["tiling_checked"] and QA.is_partition(r["excluded"] + r["unresolved"])
    assert rec["branch_and_bound"]["boxes_examined"] < 2000
    # the unresolved boxes lie in the two boxes B', which carry the local certificates
    assert len(r["groups"]) == 2
    for b in r["unresolved"]:
        assert any(QA.inside(b, g["sides"]) for g in r["groups"])
    plus, minus = records.plus_local(r), next(g for g in r["groups"] if g["sign"] == -1)["local"]
    assert all(hi < 0 for _, hi in plus["hessian_eig_enclosure"])
    # the enclosures: maximiser close to the request's torsions, mirror image, value
    theta = [float(k.mid()) * np.pi for k in plus["K"]]
    assert np.allclose(theta, common.INSTANCE_A["theta_request"], atol=1e-4)
    assert all((kp + km).contains(0) for kp, km in zip(plus["K"], minus["K"]))
    assert plus["H"].overlaps(minus["H"]) and float(plus["H"].rad()) < 1e-40
    assert Fr(rec["maximum"][0]) < Fr(rec["maximum"][1]) and abs(Fr(rec["maximum"][0]) - Fr("1.170178163968538")) < Fr(1, 10 ** 14)
    assert Fr(rec["lower_bound_L"]) <= Fr(rec["maximum"][1])
    # the float cross-check: the rounded couplings are the stress of the framework at the maximiser
    assert rec["float_at_maximiser"]["stress_on_F_vs_couplings_direction_error"] < 1e-12
    ev = np.array(rec["float_at_maximiser"]["stress_matrix_eigenvalues"])
    assert (ev > 1e-6).sum() == 1 and (ev < -1e-6).sum() == 2


def test_qa_value_by_an_independent_evaluation(inst_a):
    """H at the certified maximiser, recomputed from the NeRF chain in mpmath."""
    mpmath.mp.dps = 50
    rec, obj = inst_a
    K = records.plus_local(obj["result"])["K"]
    taus = [kernel.to_fraction(k.mid()) for k in K]
    X = nerf_mp(taus)
    H = sum(mpmath.mpf(c.numerator) / c.denominator * sum((X[i][k] - X[j][k]) ** 2 for k in range(3))
            for (i, j), c in zip(common.INSTANCE_A["pairs"], common.INSTANCE_A["couplings"]))
    lo, hi = (mpmath.mpf(x) for x in rec["maximum"])
    assert lo - mpmath.mpf(10) ** -35 <= H <= hi + mpmath.mpf(10) ** -35


def test_qa_direct_certificate(inst_a):
    form, centre = inst_a[1]["form"], inst_a[1]["centre"]
    rd = QA.certify_direct(form, centre, [8, 10, 12, 14], log=SILENT)
    assert rd["certified"] and rd["distinct"]
    assert QA.is_partition(rd["excluded"] + rd["unresolved"])
    assert all(len(b) == 5 for b in rd["excluded"]) and len(rd["groups"]) == 2
    for b in rd["unresolved"]:
        assert any(QA.inside(b, g["sides"]) for g in rd["groups"])
    # both certificates enclose the same maximiser and maximum
    pr, pd = records.plus_local(inst_a[1]["result"]), records.plus_local(rd)
    assert all(a.overlaps(b) for a, b in zip(pr["K"], pd["K"])) and pr["H"].overlaps(pd["H"])
    assert rd["lower_bound"] == inst_a[1]["result"]["lower_bound"]


def test_stored_qa_record_and_recheck_of_the_excluded_boxes(inst_a):
    stored = json.loads((RESULTS / "qa_instance_A.json").read_text())
    rec, obj = inst_a
    assert stored["certified"] is True and stored["direct"]["certified"] is True
    assert stored["couplings"] == [common.fr(c) for c in common.INSTANCE_A["couplings"]]
    for key in ("maximum", "maximiser_radians", "lower_bound_L", "centre_tau"):
        assert stored[key] == rec[key]
    assert stored["direct"]["maximum"] == stored["maximum"]
    assert stored["direct"]["branch_and_bound"]["tiling_checked"] and stored["branch_and_bound"]["tiling_checked"]
    # the stored certificate R, re-verified box by box: tiling, bound on every excluded box, the
    # unresolved boxes inside the boxes B' of the stored local certificates
    excluded = [tuple(b) for b in stored["branch_and_bound"]["excluded"]]
    unresolved = [tuple(b) for b in stored["branch_and_bound"]["unresolved"]]
    assert QA.is_partition(excluded + unresolved)
    tabs, grid = QA.tables(QA.reduce_ends(obj["form"])), QA.Grid()
    L = kernel.ball(Fr(stored["lower_bound_L"]))
    assert L <= obj["result"]["lower_bound"]                       # the stored decimal is rounded down
    assert all(QA.G_upper(tabs, grid.hull(b[0], b[1]), grid.hull(b[0], b[2])) < obj["result"]["lower_bound"] for b in excluded)
    sides = [[(Fr(lo), Fr(hi)) for lo, hi in g["group_box_tau"]] for g in stored["groups"]]
    assert all(any(QA.inside(b, s) for s in sides) for b in unresolved)
    for g in stored["groups"]:
        assert g["local"]["ok"] and all(Fr(hi) < 0 for _, hi in g["local"]["hessian_spectrum_on_B"])
    # the second maximum of the stored record
    out = stored["outside"]
    assert out["certified"] is True and abs(Fr(out["second_maximum"][0]) - Fr("1.154989405716968")) < Fr(1, 10 ** 14)
    assert abs(Fr(out["margin"][0]) - Fr("0.015188758251570")) < Fr(1, 10 ** 14)
    assert out["branch_and_bound"]["tiling_checked"]


def test_second_maximum(inst_a):
    form, centre = inst_a[1]["form"], inst_a[1]["centre"]
    other, _ = search.refine_critical(form, [1.1266, -2.7945, -1.9188, 0.1084])
    r2 = QA.certify_outside(form, centre, other, 6, [8, 10, 12], log=SILENT)
    assert r2["certified"]
    assert QA.is_partition(r2["excluded"] + r2["hill"] + r2["unresolved"])
    two = records.plus_local(r2)
    assert abs(float(two["H"].mid()) - 1.154989405716968) < 1e-13
    margin = records.plus_local(inst_a[1]["result"])["H"] - two["H"]
    assert margin > 0.0151 and margin < 0.0152
    # with the unrounded couplings the float value of the request is recovered
    c, _ = search.couplings(common.INSTANCE_A["theta_request"], common.INSTANCE_A["pairs"])
    assert abs(search.energy_float([float(x) * np.pi for x in other], common.INSTANCE_A["pairs"], c) - 1.154995) < 2e-6


def test_qb_certificate(inst_a):
    rec, obj = inst_a
    inst = common.INSTANCE_A
    n, edges = inst["n"], model.statewise_pairs(inst["n"]) + inst["pairs"]
    assert len(edges) == 16 and len(QB.gauge_unknowns(n)) == 18
    K = records.plus_local(obj["result"])["K"]
    targets = records.length_targets(obj["chain"], edges, K)
    assert all(float(t.rad()) < 1e-35 for t in targets)
    cert, resid = records.certify_candidate(n, edges, targets, records.CANDIDATE_A, log=SILENT)
    assert cert["ok"] and resid < 1e-45 and cert["sigma_disjoint"]
    assert cert["sigma_min_lower"] > 0.238 and cert["sigma_min_lower"] < 0.239
    Y = cert["Y"]
    assert Y[4][3] == Fr(9, 20).numerator / arb(20) or (Y[4][3] - arb(9) / 20).contains(0)
    assert all((QB.sq_length(Y, i, j) - t).contains(0) for (i, j), t in zip(edges, targets))
    # float cross-check of the singular values, and non-congruence with the chain on a free pair
    Yf = np.array([[float(Y[i][a].mid()) for a in range(4)] for i in range(n)])
    sv = np.linalg.svd(Yf - Yf.mean(0), compute_uv=False)
    assert abs(sv[3] - float(cert["sigma_min_lower"])) < 1e-9
    P = [kernel.point(t) for t in K]
    diff = QB.sq_length(Y, 0, 3) - kernel.ma_eval(obj["chain"].sqdist(0, 3), P)
    assert diff < -0.17
    stored = json.loads((RESULTS / "qb_instance_A.json").read_text())
    assert stored["certified"] is True and stored["pins"] == {"y_4[3]": "9/20", "y_5[3]": "3/4"}
    assert Fr(stored["sigma_4_lower_bound"]) <= kernel.to_fraction(cert["sigma_min_lower"])
    assert stored["maximiser_radians"] == rec["maximiser_radians"]


# ------------------------------------------------------------------ 5. soundness
def test_no_point_above_the_threshold_is_excluded(inst_a):
    """With thresholds below the maximum, every sampled point with G >= threshold (resp.
    H >= threshold) lies in an unresolved box, never in an excluded one."""
    form = inst_a[1]["form"]
    fun, h = search.form_float(form)
    red = QA.reduce_ends(form)
    tabs, grid = QA.tables(red), QA.Grid()
    A, V, W = h[0, :, :, 0], h[1:, :, :, 0], h[0, :, :, 1:].transpose(2, 0, 1)

    def G(t1, t2):
        P1 = np.stack([np.ones_like(t1), np.cos(t1), np.sin(t1)], -1)
        P2 = np.stack([np.ones_like(t2), np.cos(t2), np.sin(t2)], -1)
        a = np.einsum("bc,nb,nc->n", A, P1, P2)
        v = np.einsum("kbc,nb,nc->kn", V, P1, P2)
        w = np.einsum("kbc,nb,nc->kn", W, P1, P2)
        return a + np.hypot(v[0], v[1]) + np.hypot(w[0], w[1])

    nrng = np.random.default_rng(11)
    pts = nrng.uniform(-np.pi, np.pi, (20000, 2))
    vals = G(pts[:, 0], pts[:, 1])
    for threshold in (1.05, 1.16):
        excluded = []
        QA.branch_and_bound(lambda b: QA.G_upper(tabs, grid.hull(b[0], b[1]), grid.hull(b[0], b[2])),
                            arb(threshold), QA.root_boxes(3, 2), 6, excluded=excluded)
        assert excluded
        ex = set(excluded)
        for (t1, t2), v in zip(pts, vals):
            if v >= threshold:
                for level in range(3, 7):
                    n = 2 ** level
                    box = (level, min(int((t1 / np.pi + 1) / 2 * n), n - 1), min(int((t2 / np.pi + 1) / 2 * n), n - 1))
                    assert box not in ex
    # the direct bound at the root level of the 4-torus
    T = QA.dense(form)
    excluded = []
    QA.branch_and_bound(lambda b: QA.H_upper(T, [grid.hull(b[0], j) for j in b[1:]]),
                        arb(0.9), QA.root_boxes(3, 4), 3, excluded=excluded)
    ex = set(excluded)
    assert 100 < len(ex) < 4096
    pts = nrng.uniform(-np.pi, np.pi, (4000, 4))
    hits = 0
    for t in pts:
        if fun(t) >= 0.9:
            hits += 1
            assert (3,) + tuple(min(int((x / np.pi + 1) / 2 * 8), 7) for x in t) not in ex
    assert hits > 20


def test_brute_force_grid_finds_no_violation(inst_a):
    """Floating-point evaluation of H on a grid of 60^4 points (not a proof; an independent
    attempt at falsification): no value above the certified maximum; the points above the
    certified second maximum all lie over the hill region N of the stored record."""
    rec, obj = inst_a
    _, h = search.form_float(obj["form"])
    n = 60
    t = -np.pi + 2 * np.pi * (np.arange(n) + 0.5) / n
    P = np.stack([np.ones(n), np.cos(t), np.sin(t)])                 # 3 x n
    vals = np.einsum("abcd,ai,bj,ck,dl->ijkl", h, P, P, P, P, optimize=True)
    hmax = float(Fr(rec["maximum"][0]))
    assert vals.max() < hmax and vals.max() > hmax - 0.01
    stored = json.loads((RESULTS / "qa_instance_A.json").read_text())["outside"]
    level = stored["hill_level"]
    hill = {tuple(b) for b in stored["hill"]}
    second = float(Fr(stored["second_maximum"][1]))
    idx = np.argwhere(vals > second)
    assert len(idx) > 100
    for i, j, k, l in idx:
        box = (level, int((t[j] / np.pi + 1) / 2 * 2 ** level), int((t[k] / np.pi + 1) / 2 * 2 ** level))
        assert box in hill
    # the best grid point is close to +-theta^
    best = np.array([t[i] for i in np.unravel_index(vals.argmax(), vals.shape)])
    centre = np.array(rec["centre_radians_float"])
    assert min(np.abs(best - centre).max(), np.abs(best + centre).max()) < 2 * np.pi / n


def test_boxes_with_known_answers(inst_a):
    rec, obj = inst_a
    form, centre, r = obj["form"], obj["centre"], obj["result"]
    tabs, grid, T = QA.tables(QA.reduce_ends(form)), QA.Grid(), QA.dense(form)
    L = r["lower_bound"]
    for level in range(3, 13):                                    # the boxes that contain the maximiser are kept
        n = 2 ** level
        j = [int((float(c) + 1) / 2 * n) for c in centre]
        assert not QA.G_upper(tabs, grid.hull(level, j[1]), grid.hull(level, j[2])) < L
        assert not QA.H_upper(T, [grid.hull(level, x) for x in j]) < L
    # a box around the minimum of G is excluded, with a bound close to the sampled values
    ub = QA.G_upper(tabs, kernel.arc_hull(Fr(-1, 100), Fr(1, 100)), kernel.arc_hull(Fr(-1, 100), Fr(1, 100)))
    assert ub < L and float(ub) < 1.0
    # the local step refuses a box on which the Hessian is not definite
    wide = [(c - Fr(1, 20), c + Fr(1, 20)) for c in centre]
    d = QA.concavity_certificate(form, wide, centre)
    assert not d["ok"] and "negative definite" in d["failed"]
    tight = [(c - Fr(1, 2000), c + Fr(1, 2000)) for c in centre]
    assert QA.concavity_certificate(form, tight, centre)["ok"]


def test_perturbed_inputs_are_not_certified(inst_a):
    form, centre = inst_a[1]["form"], inst_a[1]["centre"]
    # an approximate maximiser that is 1e-9 off: the Krawczyk box of radius 2^-80 holds no critical point
    off = [c + Fr(1, 10 ** 9) for c in centre]
    off = [Fr(round(c * 2 ** 150), 2 ** 150) for c in off]
    r = QA.certify(form, off, [8, 10, 12], log=SILENT)
    assert not r["certified"]
    assert any("Krawczyk" in (g["local"] or {}).get("failed", "") for a in r["attempts"] for g in a["groups"])
    # other couplings (the fifth one changed in the second decimal), same claimed maximiser
    c2 = list(common.INSTANCE_A["couplings"])
    c2[4] += Fr(1, 50)
    form2 = model.Chain(7).energy(common.INSTANCE_A["pairs"], c2)
    assert not QA.certify(form2, centre, [6, 7], log=SILENT)["certified"]


# ------------------------------------------------------------------ 6. the controls of the request
def test_control_runner_up_and_wrong_sign():
    a1 = controls.control_a1(SILENT, start=[1.1266, -2.7945, -1.9188, 0.1084])
    assert a1["passed"] and not a1["certified"] and a1["refutation"] is not None
    assert Fr(a1["refutation"]["H_lower_bound"]) > Fr(a1["claimed_value"][1])
    assert a1["unresolved_boxes_away_from_the_claimed_maximiser"] > 2000
    a2 = controls.control_a2(SILENT)
    assert a2["passed"] and a2["unresolved_boxes_at_level_6"] == 4 ** 6


def test_control_semidefinite_stress():
    a3, b1 = controls.control_psd(SILENT, trials=12)
    # (Q-a) holds for the universally rigid control (and is certified) ...
    assert a3["passed"] and a3["certified"]
    ev = np.array(a3["float_at_maximiser"]["stress_matrix_eigenvalues"])
    assert (np.abs(ev) > 1e-6).sum() == 3 and ((ev < -1e-6).sum() == 3 or (ev > 1e-6).sum() == 3)
    # ... while (Q-b) is not: no candidate, and the Krawczyk test refuses the forced ones
    assert b1["passed"] and not b1["certified"] and b1["search_candidate"] is None
    assert b1["forced_candidates"]["flat"]["certified"] is False
    assert b1["forced_candidates"]["lifted"]["certified"] is False
    assert b1["lifted_least_squares_residual"] > 1e-4


def test_control_flat_and_six_atoms():
    b2 = controls.control_b2(SILENT)
    assert b2["passed"] and not b2["certified"]
    b3 = controls.control_six(controls.SIX_SEMIDEFINITE, False, SILENT, trials=12)
    assert b3["passed"] and not b3["certified"]
    ev = np.array(b3["stress_eigenvalues_float"])
    assert (ev > 1e-6).sum() == 2 or (ev < -1e-6).sum() == 2
    b4 = controls.control_six(controls.SIX_INDEFINITE, True, SILENT, trials=12)
    assert b4["passed"] and b4["certified"]
    assert Fr(b4["search_candidate"]["sigma_4_lower_bound"]) > Fr(1, 10)


def test_stored_controls_record():
    stored = json.loads((RESULTS / "controls.json").read_text())
    assert stored["all_passed"] is True
    expected = {"A1_runner_up_claimed_global": False, "A2_wrong_sign": False, "A3_semidefinite_stress_Qa": True,
                "B1_semidefinite_stress_Qb": False, "B2_flat_instance_A": False, "B3_six_atoms_semidefinite": False,
                "B4_six_atoms_indefinite": True}
    for name, value in expected.items():
        assert stored[name]["certified"] is value and stored[name]["passed"] is True
