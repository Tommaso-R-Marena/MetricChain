#!/usr/bin/env python3
"""Checks for docs/ensemble/ENSEMBLE_REPORT.md, section 4c.4: Propositions E20a (five states, now with exact
computations), Theorem E20b (six generic states on a torus of three angles are never determined by the
multilinear data), Proposition E20c (exceptional configurations of six states that are) and Proposition E20d
(the count of double-point conditions on a torus of r angles).

Real coordinates.  With t_k = tan(phi_k/2) the data span of the multilinear trigonometric means is
    V = { q(t) / prod_k (1 + t_k^2) :  q a polynomial of degree at most 2 in each t_k }        (3^r functions),
and the lift is u(t) = (1, t_1) x ... x (1, t_r)  (the entries of u u^T / prod(1 + t_k^2) span V).  A function in
V is non-negative iff its numerator q is.  So every statement is about polynomials with rational coefficients
at rational points, and ranks are computed exactly (sympy rationals, or modulo a prime for integer matrices:
the rank modulo a prime is a lower bound for the rank over Q).

S1  exact: five rational states on T^3 -- the zero set of the lifted certificate is finite in all eight affine
    charts of (P^1)^3; it consists of six points, the five states and a rational sixth one; the six lifted
    outer products are linearly independent.
S2  exact: six rational states on T^3 -- the twelve conditions "value and derivative along the curve" have rank
    12 on the 27 numerators, and the numerators that vanish on the curve form a space of dimension 15.
S3  numeric: for random six-tuples, a second measure with the same 27 data, carried by the curve away from the
    states (linear programme on a traced sample of the curve).
S4  numeric: an exceptional six-tuple (rank 11) -- the extra numerator is semidefinite on the curve, and
    A*(g_1^2 + g_2^2) + (corrected numerator) is non-negative on the torus with the six states as its only zeros.
S4b numeric: another exceptional six-tuple, on a curve with two real components, where the extra function has
    opposite signs on the two components: no certificate, and a twin exists.
S5  ranks of the conditions "value and full gradient at K states" for r = 2, 3, 4 (modulo a prime, integer states).
S6  numeric: sixteen random states on T^4 -- the unique function with sixteen double points is a saddle at a state.
"""
import itertools
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq, linprog, minimize

ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f"  {name}: {'ok' if cond else 'FAILED'}")


# ------------------------------------------------------------------------------------------------ exact part
t = sp.symbols("t1:4")
R = sp.Rational
# five rational states with pairwise distinct coordinates (t = tan(phi/2)), and a sixth one
FIVE = [(R(-1), R(-7, 3), R(-3, 2)), (R(5, 4), R(3, 2), R(-5, 3)), (R(-9, 4), R(4, 5), R(-9, 4)),
        (R(-1, 2), R(9), R(1)), (R(-9), R(8), R(3, 2))]
SIXTH = (R(4), R(7, 2), R(5, 4))
MONO1 = [sp.Mul(*[t[i] ** a[i] for i in range(3)]) for a in itertools.product([0, 1], repeat=3)]      # lift, 8
MONO2 = [sp.Mul(*[t[i] ** a[i] for i in range(3)]) for a in itertools.product([0, 1, 2], repeat=3)]   # V, 27


def lift_matrix(states):
    return sp.Matrix([[m.subs(dict(zip(t, s))) for m in MONO1] for s in states])


def s1_five_states():
    print("S1  five rational states on T^3 (Proposition E20a), exact")
    states = [list(x) for x in FIVE]
    U = lift_matrix(states)
    check("the five lifts are linearly independent", U.rank() == 5)
    N = U.nullspace()
    eqs = [sum(n[i] * MONO1[i] for i in range(8)) for n in N]                 # three tri-affine equations
    # the eight affine charts of (P^1)^3: in a chart where coordinate k is replaced by s_k = 1/t_k the
    # equation becomes  s_k * e(1/s_k)  (again tri-affine)
    finite = []
    main_basis = None
    for chart in itertools.product([0, 1], repeat=3):
        ce = []
        for e in eqs:
            for k in range(3):
                if chart[k]:
                    e = sp.expand(sp.together(e.subs(t[k], 1 / t[k]) * t[k]))
            ce.append(sp.expand(e))
        G = sp.groebner(ce, *t, order="lex")
        finite.append(G.is_zero_dimensional)
        if chart == (0, 0, 0):
            main_basis = G
    check("the zero set of the lifted certificate is finite in all eight charts", all(finite))
    uni = [p for p in main_basis.exprs if p.free_symbols == {t[2]}]
    deg = sp.Poly(uni[0], t[2]).degree() if uni else None
    check("it has six points in the main chart (a univariate polynomial of degree 6 in the lex basis)", deg == 6)
    roots = sp.roots(sp.Poly(uni[0], t[2]))
    rational_roots = [r for r in roots if r.is_rational]
    check("all six are rational: the five states and a sixth point", len(rational_roots) == 6)
    ghost_t3 = [r for r in rational_roots if r not in [s[2] for s in states]]
    sol = sp.solve([e.subs(t[2], ghost_t3[0]) for e in eqs], [t[0], t[1]], dict=True) if len(ghost_t3) == 1 else []
    ghost = None
    for s in sol:
        cand = [s[t[0]], s[t[1]], ghost_t3[0]]
        if all(sp.simplify(e.subs(dict(zip(t, cand)))) == 0 for e in eqs) and cand not in states:
            ghost = cand
    check("the sixth point is found exactly", ghost is not None)
    print("    the sixth zero (t-coordinates):", ghost)
    six = states + [ghost]
    outer = sp.Matrix([[a * b for a in row for b in row] for row in lift_matrix(six).tolist()])
    check("the six lifted outer products are linearly independent (rank 6)", outer.rank() == 6)
    return ghost


def six_state_ranks(states):
    U = lift_matrix(states)
    assert U.rank() == 6
    N = U.nullspace()
    g = [sum(n[i] * MONO1[i] for i in range(8)) for n in N]
    grads = [[sp.diff(gj, ti) for ti in t] for gj in g]
    rows, smooth = [], True
    for s in states:
        sub = dict(zip(t, s))
        g1 = sp.Matrix([d.subs(sub) for d in grads[0]])
        g2 = sp.Matrix([d.subs(sub) for d in grads[1]])
        tau = g1.cross(g2)
        smooth &= any(x != 0 for x in tau)
        rows.append([m.subs(sub) for m in MONO2])
        rows.append([sum(tau[i] * sp.diff(m, t[i]).subs(sub) for i in range(3)) for m in MONO2])
    M = sp.Matrix(rows)
    prods = [sp.expand(m * gj) for gj in g for m in MONO1]
    P = sp.Matrix([[sp.Poly(p, *t).coeff_monomial(m) for m in MONO2] for p in prods])
    return smooth, M.rank(), P.rank(), (M * P.T).is_zero_matrix


def s2_six_states(ghost):
    print("S2  six rational states on T^3 (Theorem E20b), exact")
    inst = [
        [list(x) for x in FIVE] + [list(SIXTH)],
        [[R(4), R(1), R(-1, 2)], [R(0), R(4, 5), R(-3)], [R(0), R(1, 5), R(4, 5)],
         [R(-1), R(0), R(6, 5)], [R(3, 5), R(-2), R(-1, 2)], [R(2), R(2, 5), R(2)]],
    ]
    for i, states in enumerate(inst):
        smooth, rk, dimI, inker = six_state_ranks(states)
        print(f"    instance {i + 1}: rank of the 12 tangential conditions {rk}; dimension of the numerators "
              f"vanishing on the curve {dimI}")
        check(f"instance {i + 1}: the curve is smooth at the six states", smooth)
        check(f"instance {i + 1}: rank 12, dimension 15, and the 15 lie in the kernel", rk == 12 and dimI == 15 and inker)


# ---------------------------------------------------------------------------------------------- numeric part
def half(p):
    return np.array([np.cos(p / 2), np.sin(p / 2)])


def dhalf(p):
    return 0.5 * np.array([-np.sin(p / 2), np.cos(p / 2)])


def w(phi):
    """homogeneous real lift (cos(phi_k/2), sin(phi_k/2)) x ...: proportional to u(t)"""
    v = np.array([1.0])
    for p in phi:
        v = np.kron(v, half(p))
    return v


def dw(phi, k):
    v = np.array([1.0])
    for j, p in enumerate(phi):
        v = np.kron(v, dhalf(p) if j == k else half(p))
    return v


C = [lambda p: 1.0 + 0 * p, np.cos, np.sin]
dC = [lambda p: 0.0 * p, lambda p: -np.sin(p), np.cos]
ddC = [lambda p: 0.0 * p, lambda p: -np.cos(p), lambda p: -np.sin(p)]


def basis(r):
    return list(itertools.product(range(3), repeat=r))


B27 = basis(3)


def F(phi, B=B27):
    return np.array([np.prod([C[b[k]](phi[k]) for k in range(len(phi))]) for b in B])


def dF(phi, B=B27):
    r = len(phi)
    out = np.zeros((r, len(B)))
    for i, b in enumerate(B):
        vals = [C[b[k]](phi[k]) for k in range(r)]
        ders = [dC[b[k]](phi[k]) for k in range(r)]
        for a in range(r):
            out[a, i] = np.prod([ders[k] if k == a else vals[k] for k in range(r)])
    return out


def wrap(d):
    return (d + np.pi) % (2 * np.pi) - np.pi


def null2(P):
    return np.linalg.svd(np.array([w(p) for p in P]))[2][6:]


def gval(N, phi):
    return N @ w(phi)


def gjac(N, phi):
    return np.array([[N[j] @ dw(phi, k) for k in range(3)] for j in range(2)])


def tangent(N, phi):
    G = gjac(N, phi)
    tv = np.cross(G[0], G[1])
    return tv / np.linalg.norm(tv)


def Mmat(N, P):
    rows = []
    for p in P:
        rows.append(F(p))
        rows.append(tangent(N, p) @ dF(p))
    return np.array(rows)


def project(N, phi):
    for _ in range(40):
        res = gval(N, phi)
        if np.linalg.norm(res) < 1e-14:
            break
        phi = phi - np.linalg.lstsq(gjac(N, phi), res, rcond=None)[0]
    return phi


def trace(N, start, h=0.01, maxsteps=200000):
    """the connected component through `start` of the real curve {g_1 = g_2 = 0} on the torus"""
    pts = [start.copy()]
    phi = start.copy()
    tprev = tangent(N, phi)
    for step in range(maxsteps):
        tv = tangent(N, phi)
        if tv @ tprev < 0:
            tv = -tv
        phi = project(N, phi + h * tv)
        tprev = tv
        pts.append(phi.copy())
        if step > 10 and np.linalg.norm(wrap(phi - start)) < 0.8 * h:
            break
    return np.array(pts)


def components(N, P, rng, extra=40):
    comps = []

    def known(pt):
        return any(np.min(np.linalg.norm(wrap(c - pt), axis=1)) < 0.03 for c in comps)

    starts = [p for p in P] + [project(N, rng.uniform(-np.pi, np.pi, 3)) for _ in range(extra)]
    for st in starts:
        if np.linalg.norm(gval(N, st)) > 1e-10 or known(st):
            continue
        comps.append(trace(N, st))
    return comps


def least_mass_on_states(comps, P, step=2, radius=0.02):
    """Among measures on (a sample of the real curve, without the points closer than `radius` to a state)
    together with the six states that have the 27 data of the uniform ensemble on the states: the least mass
    on the states.  One means: no other such measure (on the sample); less than one: a twin."""
    pts = np.vstack([c[::step] for c in comps])
    far = np.array([min(np.linalg.norm(wrap(pt - p)) for p in P) > radius for pt in pts])
    pts = pts[far]
    cols = np.array([F(pt) for pt in pts] + [F(p) for p in P]).T
    y = np.mean([F(p) for p in P], axis=0)
    cost = np.concatenate([np.zeros(len(pts)), np.ones(6)])
    res = linprog(cost, A_eq=cols, b_eq=y, bounds=[(0, None)] * cols.shape[1], method="highs")
    return (res.fun if res.status == 0 else np.nan), res


def s3_twins():
    print("S3  six random states on T^3: a second measure on the curve, away from the states (linear programme)")
    found, worst = 0, 0.0
    trials = 10
    for seed in range(trials):
        rng = np.random.default_rng(1000 + seed)
        P = rng.uniform(-np.pi, np.pi, size=(6, 3))
        N = null2(P)
        comps = components(N, P, rng)
        least, res = least_mass_on_states(comps, P)
        worst = max(worst, least)
        if res.status == 0 and least < 1e-6:
            found += 1
    print(f"    a measure with the same 27 data and no mass on the six states: in {found}/{trials} instances"
          f" (largest value of the least mass on the states: {worst:.2e})")
    check("a twin on the curve in every instance", found == trials)


def s4_exceptional():
    print("S4  an exceptional configuration of six states on T^3 (Proposition E20c)")
    rng = np.random.default_rng(2)
    P = rng.uniform(-np.pi, np.pi, size=(6, 3))
    N = null2(P)
    M0 = Mmat(N, P)
    sv0 = np.linalg.svd(M0, compute_uv=False)
    Vt = np.linalg.svd(M0)[2]
    Bc = Vt[:12].T                                # complement of the numerators vanishing on the curve
    curve = trace(N, P[5])

    def D(pt):
        Pm = P.copy()
        Pm[5] = pt
        return np.linalg.det(Mmat(N, Pm) @ Bc)

    vals = np.array([D(pt) for pt in curve])
    idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
    exc = None
    for i in idx:
        a, d = curve[i], wrap(curve[i + 1] - curve[i])
        u = brentq(lambda s: D(project(N, a + s * d)), 0, 1, xtol=1e-14)
        pt = project(N, a + u * d)
        Pm = P.copy()
        Pm[5] = pt
        lifts = np.linalg.svd(np.array([w(p) for p in Pm]), compute_uv=False)[-1]
        if lifts > 1e-3:                           # the other root has dependent lifts (five states and their sixth zero)
            exc = Pm
    check("a configuration with independent lifts at which the determinant of the 12 conditions changes sign",
          exc is not None)
    Ms = Mmat(N, exc)
    sv = np.linalg.svd(Ms, compute_uv=False)
    print(f"    generic starting configuration: smallest singular value of the 12 conditions {sv0[11]:.4f};"
          f" exceptional configuration: singular value 11 is {sv[10]:.4f}, singular value 12 is"
          f" {'below 1e-12' if sv[11] < 1e-12 else format(sv[11], '.1e')}")
    check("rank 11 at the exceptional configuration", sv[11] < 1e-12 and sv[10] > 1e-2)
    print("    the exceptional sixth state (angles): " + ", ".join(f"{x:.6f}" for x in wrap(exc[5])))
    q0 = Bc @ np.linalg.svd(Ms @ Bc)[2][-1]
    comps = components(N, exc, rng)
    onc = np.concatenate([[F(pt) @ q0 for pt in c] for c in comps])
    q0 = q0 * np.sign(onc.sum())
    pts = np.vstack(comps)
    onc = np.array([F(pt) @ q0 for pt in pts])
    dist = np.array([min(np.linalg.norm(wrap(pt - p)) for p in exc) for pt in pts])
    print(f"    real components of the curve: {len(comps)}; the extra function on the curve: minimum"
          f" {'above -1e-9' if onc.min() > -1e-9 else format(onc.min(), '.1e')},"
          f" minimum at distance > 0.1 from the states {onc[dist > 0.1].min():.4f}, maximum {onc.max():.4f}")
    check("the extra numerator is non-negative on the curve and positive away from the states",
          onc.min() > -1e-9 and onc[dist > 0.1].min() > 1e-3)
    # determined among measures on the curve: the least mass that a measure on (sample of the curve + states)
    # with the data of the uniform ensemble can put on the six states is one
    least, res = least_mass_on_states(comps, exc)
    print(f"    least mass on the six states among measures on the sampled curve with the same data: {least:.6f}")
    check("no other measure on the sampled curve has the data", res.status == 0 and least > 1 - 1e-6)
    # a certificate on the whole torus
    rs = np.random.default_rng(7)
    smp = rs.uniform(-np.pi, np.pi, size=(400, 3))
    Fs = np.array([F(x) for x in smp])

    def coeffs(fun):
        return np.linalg.lstsq(Fs, np.array([fun(x) for x in smp]), rcond=None)[0]

    Lc = coeffs(lambda x: np.sum(gval(N, x) ** 2))
    rows, rhs = [], []
    for p in exc:
        G = gjac(N, p)
        ab = np.linalg.lstsq(G.T, dF(p) @ q0, rcond=None)[0]
        rows.append(np.concatenate([w(p), np.zeros(8)]))
        rhs.append(-ab[0])
        rows.append(np.concatenate([np.zeros(8), w(p)]))
        rhs.append(-ab[1])
    ell = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)[0]
    ic = coeffs(lambda x: (ell[:8] @ w(x)) * gval(N, x)[0] + (ell[8:] @ w(x)) * gval(N, x)[1])
    qt = q0 + ic
    grad = max(np.linalg.norm(dF(p) @ qt) for p in exc)
    A = 100.0
    fc = A * Lc + qt

    def hess(p, h=1e-4):
        H = np.zeros((3, 3))
        for a in range(3):
            e = np.zeros(3)
            e[a] = h
            H[:, a] = (dF(p + e) @ fc - dF(p - e) @ fc) / (2 * h)
        return (H + H.T) / 2

    eig = min(np.linalg.eigvalsh(hess(p))[0] for p in exc)
    gr = np.linspace(-np.pi, np.pi, 49)[:-1]
    X = np.array(np.meshgrid(gr, gr, gr, indexing="ij")).reshape(3, -1).T
    V0 = np.stack([C[b[0]](X[:, 0]) * C[b[1]](X[:, 1]) * C[b[2]](X[:, 2]) for b in B27], axis=1) @ fc
    best = V0.min()
    far_min = np.inf
    for i in np.argsort(V0)[:60]:
        res = minimize(lambda x: F(x) @ fc, X[i], jac=lambda x: dF(x) @ fc, method="BFGS", options={"gtol": 1e-12})
        best = min(best, res.fun)
        d = min(np.linalg.norm(wrap(res.x - p)) for p in exc)
        if d > 1e-3:
            far_min = min(far_min, res.fun)
    away = "none: all 60 end at a state" if not np.isfinite(far_min) else f"smallest value {far_min:.4f}"
    print(f"    certificate f = {A:.0f}*(g_1^2 + g_2^2) + h: gradient of h at the states below 1e-9: {grad < 1e-9};"
          f" smallest Hessian eigenvalue of f at the states {eig:.4f}; global minimum of f on the torus"
          f" {'above -1e-9' if best > -1e-9 else format(best, '.1e')} (grid of 48^3 points and 60 local refinements);"
          f" local minima away from the states: {away}")
    check("f is non-negative on the torus, with non-degenerate zeros at the six states and no other zero found",
          best > -1e-9 and eig > 1e-3 and grad < 1e-9 and (not np.isfinite(far_min) or far_min > 1e-4))


def s4b_exceptional_without_certificate():
    print("S4b an exceptional configuration at which the extra function changes sign between the two real components")
    rng = np.random.default_rng(0)
    P = rng.uniform(-np.pi, np.pi, size=(6, 3))
    N = null2(P)
    Bc = np.linalg.svd(Mmat(N, P))[2][:12].T
    curve = trace(N, P[5])

    def D(pt):
        Pm = P.copy()
        Pm[5] = pt
        return np.linalg.det(Mmat(N, Pm) @ Bc)

    vals = np.array([D(pt) for pt in curve])
    idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
    exc = None
    for i in idx:
        a, d = curve[i], wrap(curve[i + 1] - curve[i])
        u = brentq(lambda s: D(project(N, a + s * d)), 0, 1, xtol=1e-14)
        Pm = P.copy()
        Pm[5] = project(N, a + u * d)
        if np.linalg.svd(np.array([w(p) for p in Pm]), compute_uv=False)[-1] > 0.1:
            exc = Pm
    check("an exceptional configuration (rank 11, independent lifts) is found", exc is not None
          and np.linalg.svd(Mmat(N, exc), compute_uv=False)[11] < 1e-12)
    q0 = Bc @ np.linalg.svd(Mmat(N, exc) @ Bc)[2][-1]
    comps = components(N, exc, rng)
    ranges = [(min(F(pt) @ q0 for pt in c), max(F(pt) @ q0 for pt in c)) for c in comps]
    signs = sorted(int(np.sign(lo + hi)) for lo, hi in ranges)
    print(f"    real components of the curve: {len(comps)}; signs of the extra function on them: {signs}")
    check("two components, and the extra function is non-negative on one and non-positive on the other",
          len(comps) == 2 and signs == [-1, 1] and all(min(abs(lo), abs(hi)) < 1e-9 for lo, hi in ranges))
    least, res = least_mass_on_states(comps, exc)
    print(f"    least mass on the six states among measures on the sampled curve with the same data: {least:.6f}")
    check("a twin exists: the ensemble is not determined although the rank is 11", res.status == 0 and least < 1 - 1e-3)


# ------------------------------------------------------------------- S5: double-point conditions modulo a prime
PRIME = 2147483647


def rank_mod_p(rows, p=PRIME):
    A = [[int(x) % p for x in row] for row in rows]
    rank, col, ncol = 0, 0, len(A[0])
    while rank < len(A) and col < ncol:
        piv = next((i for i in range(rank, len(A)) if A[i][col]), None)
        if piv is None:
            col += 1
            continue
        A[rank], A[piv] = A[piv], A[rank]
        inv = pow(A[rank][col], p - 2, p)
        A[rank] = [(x * inv) % p for x in A[rank]]
        for i in range(len(A)):
            if i != rank and A[i][col]:
                f = A[i][col]
                A[i] = [(x - f * yv) % p for x, yv in zip(A[i], A[rank])]
        rank += 1
        col += 1
    return rank


def double_point_rows(states, r):
    exps = list(itertools.product(range(3), repeat=r))
    rows = []
    for s in states:
        rows.append([int(np.prod([s[k] ** e[k] for k in range(r)], dtype=object)) for e in exps])
        for a in range(r):
            row = []
            for e in exps:
                if e[a] == 0:
                    row.append(0)
                else:
                    v = e[a] * s[a] ** (e[a] - 1)
                    for k in range(r):
                        if k != a:
                            v *= s[k] ** e[k]
                    row.append(int(v))
            rows.append(row)
    return rows


def s5_double_points():
    print("S5  conditions 'value and full gradient at K states' on the 3^r numerators (integer states; rank modulo"
          " 2^31 - 1, a lower bound for the rank over Q)")
    rng = np.random.default_rng(5)
    table = {}
    for r, Ks in [(2, [2, 3, 4]), (3, [5, 6, 7, 8]), (4, [12, 16, 17])]:
        for K in Ks:
            # integer states with pairwise distinct coordinates in every angle
            cols = [rng.choice(np.arange(-40, 41), size=K, replace=False) for _ in range(r)]
            states = [[int(cols[k][i]) for k in range(r)] for i in range(K)]
            table[(r, K)] = rank_mod_p(double_point_rows(states, r))
            print(f"    r = {r}, K = {K:2d}: {K * (r + 1):2d} conditions on {3 ** r} numerators, rank {table[(r, K)]}")
    check("r = 2: three double points impose 8 conditions, not 9 (the square of the bilinear form through them)",
          table[(2, 3)] == 8 and table[(2, 4)] == 9)
    check("r = 3: six double points impose 24 conditions, seven impose 26 (not 27), eight impose 27",
          table[(3, 6)] == 24 and table[(3, 7)] == 26 and table[(3, 8)] == 27)
    check("r = 4: sixteen double points impose 80 conditions, seventeen impose 81: no numerator is left",
          table[(4, 16)] == 80 and table[(4, 17)] == 81)


def s6_sixteen_states():
    print("S6  sixteen random states on T^4: the unique function of the data span with sixteen double points")
    B = basis(4)
    trials, indefinite = 12, 0
    for seed in range(trials):
        rng = np.random.default_rng(600 + seed)
        P = rng.uniform(-np.pi, np.pi, size=(16, 4))
        M = np.vstack([np.vstack([F(p, B)[None, :], dF(p, B)]) for p in P])
        sv = np.linalg.svd(M, compute_uv=False)
        assert sv[79] > 1e-8 * sv[0]                       # rank 80: the function is unique up to a factor
        q0 = np.linalg.svd(M)[2][-1]
        mixed = 0
        for p in P:
            H = np.zeros((4, 4))
            for a in range(4):
                e = np.zeros(4)
                e[a] = 1e-4
                H[:, a] = (dF(p + e, B) @ q0 - dF(p - e, B) @ q0) / 2e-4
            ev = np.linalg.eigvalsh((H + H.T) / 2)
            mixed += int(ev[0] < -1e-6 and ev[-1] > 1e-6)
        indefinite += int(mixed > 0)
    print(f"    its Hessian has eigenvalues of both signs at some state in {indefinite}/{trials} instances")
    check("so it is not semidefinite in any of them: sixteen states were never determined", indefinite == trials)


if __name__ == "__main__":
    ghost = s1_five_states()
    s2_six_states(ghost)
    s3_twins()
    s4_exceptional()
    s4b_exceptional_without_certificate()
    s5_double_points()
    s6_sixteen_states()
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
