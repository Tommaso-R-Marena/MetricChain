#!/usr/bin/env python3
"""ER4 (internal AI review) -- Theorem E20b, exact checks written from the definitions (no sympy; own Gaussian
elimination over fractions.Fraction).

For six rational states on T^3 (t_k = tan(phi_k/2) rational, so cos phi_k, sin phi_k rational):
  H1  the six lifts u(t) = (1,t_1) x (1,t_2) x (1,t_3) are linearly independent;
  H2  with n_1, n_2 a basis of the orthogonal complement and G_j = n_j . u(t):  grad G_1 x grad G_2 != 0 at every state;
  R   the twelve linear forms  f -> f(p_k),  f -> d_tau f(p_k)  have rank 12 on V (dimension 27);
  I   dim I_0 = 15, where I_0 = { L_1 G_1 + L_2 G_2 : L_i tri-affine };  I_0 lies in the common kernel.
R is computed twice, in two different bases of V:
  (t)   numerators: monomials t^e, e in {0,1,2}^3, with the tangent  grad_t G_1 x grad_t G_2;
  (phi) the 27 trigonometric products of {1, cos, sin}, with the tangent expressed in the angles
        (tau_phi,k = 2 tau_t,k / (1 + t_k^2));  all entries are rational.
The two ranks must agree (the forms differ by an invertible triangular change).

Instances: the two of the report (check S2), 30 random ones of my own, and structured ones:
  * a six-tuple for which a member of the pencil a G_1 + b G_2 is the product of a function of one angle and a
    function of the other two (the report's proof says that no combination is "independent of an angle");
  * six-tuples with a common factor (hypothesis H2 must then fail);
  * a six-tuple with a state at infinity of the t-chart (phi = pi) handled by rotating the angles.
"""
import itertools
import random
import sys
from fractions import Fraction as Fr

E1 = list(itertools.product([0, 1], repeat=3))        # exponents of the lift
E2 = list(itertools.product([0, 1, 2], repeat=3))     # exponents of the numerators of V


# ------------------------------------------------------------------ exact linear algebra
def rref(rows):
    A = [list(r) for r in rows]
    piv = []
    r = 0
    ncol = len(A[0]) if A else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == len(A):
            break
    return A[:r], piv


def rank(rows):
    return len(rref(rows)[1])


def nullspace(rows, ncol):
    R, piv = rref(rows)
    free = [c for c in range(ncol) if c not in piv]
    basis = []
    for f in free:
        v = [Fr(0)] * ncol
        v[f] = Fr(1)
        for i, p in enumerate(piv):
            v[p] = -R[i][f]
        basis.append(v)
    return basis


# ------------------------------------------------------------------ polynomials as dicts exponent -> coefficient
def lift(t):
    return [t[0] ** a * t[1] ** b * t[2] ** c for (a, b, c) in E1]


def poly_from_vec(n):
    return {e: n[i] for i, e in enumerate(E1) if n[i] != 0}


def pmul(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            out[e] = out.get(e, 0) + c1 * c2
    return {e: c for e, c in out.items() if c != 0}


def peval(p, t):
    return sum(c * t[0] ** e[0] * t[1] ** e[1] * t[2] ** e[2] for e, c in p.items())


def pdiff(p, k):
    out = {}
    for e, c in p.items():
        if e[k] > 0:
            e2 = list(e)
            e2[k] -= 1
            out[tuple(e2)] = out.get(tuple(e2), 0) + c * e[k]
    return out


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def mono_val(e, t):
    return t[0] ** e[0] * t[1] ** e[1] * t[2] ** e[2]


def mono_der(e, t, k):
    if e[k] == 0:
        return Fr(0)
    v = Fr(e[k]) * t[k] ** (e[k] - 1)
    for j in range(3):
        if j != k:
            v *= t[j] ** e[j]
    return v


def trig(t):
    """(1, cos, sin) and derivatives (0, -sin, cos) of the angle with tan(phi/2) = t"""
    d = 1 + t * t
    c, s = (1 - t * t) / d, 2 * t / d
    return [Fr(1), c, s], [Fr(0), -s, c]


def analyse(states):
    """states: six triples of Fractions.  Returns a dict of exact facts."""
    out = {}
    L = [lift(s) for s in states]
    out["rank_lifts"] = rank(L)
    if out["rank_lifts"] != 6:
        return out
    N = nullspace(L, 8)
    assert len(N) == 2
    G = [poly_from_vec(n) for n in N]
    dG = [[pdiff(g, k) for k in range(3)] for g in G]
    taus = []
    for s in states:
        g1 = [peval(dG[0][k], s) for k in range(3)]
        g2 = [peval(dG[1][k], s) for k in range(3)]
        taus.append(cross(g1, g2))
    out["smooth_at_states"] = all(any(x != 0 for x in tau) for tau in taus)
    # (t) numerators
    rows_t = []
    for s, tau in zip(states, taus):
        rows_t.append([mono_val(e, s) for e in E2])
        rows_t.append([sum(tau[k] * mono_der(e, s, k) for k in range(3)) for e in E2])
    out["rank_R_t"] = rank(rows_t)
    # (phi) trigonometric basis
    rows_p = []
    for s, tau in zip(states, taus):
        tr = [trig(x) for x in s]
        tau_phi = [2 * tau[k] / (1 + s[k] ** 2) for k in range(3)]
        rows_p.append([tr[0][0][b[0]] * tr[1][0][b[1]] * tr[2][0][b[2]] for b in E2])
        row = []
        for b in E2:
            v = Fr(0)
            for k in range(3):
                term = tau_phi[k]
                for j in range(3):
                    term *= tr[j][1][b[j]] if j == k else tr[j][0][b[j]]
                v += term
            row.append(v)
        rows_p.append(row)
    out["rank_R_phi"] = rank(rows_p)
    # I_0
    prods = []
    for g in G:
        for e in E1:
            p = pmul({e: Fr(1)}, g)
            prods.append([p.get(m, Fr(0)) for m in E2])
    out["dim_I0"] = rank(prods)
    out["I0_in_kernel"] = all(sum(a * b for a, b in zip(r, p)) == 0 for r in rows_t for p in prods)
    out["dim_W"] = 27 - out["rank_R_t"]
    # the pencil: is some member a G_1 + b G_2 divisible by a factor depending on one angle only
    # (in the t-chart: independent of t_k, or of the form (t_k - c) * H)?  Decided for the given basis only when
    # asked by the caller (structured instances).
    out["N"] = N
    return out


# ------------------------------------------------------------------ homogeneous version (no point at infinity)
# variables (x_1,y_1,x_2,y_2,x_3,y_3) with (x_k : y_k) = (cos(phi_k/2) : sin(phi_k/2)); polynomials as dicts over
# exponent 6-tuples.  d/dphi_k acts as (1/2)(-y_k d/dx_k + x_k d/dy_k).  With unnormalised rational coordinates all
# rows below are positive multiples of the true ones, so ranks and the tangent direction are unchanged.
def hmono(e):
    """e in {0,1,2}^3 (or {0,1}^3 with deg 1): monomial prod x_k^(deg-e_k) y_k^(e_k) as an exponent 6-tuple"""
    return e


def hpoly_lift_basis():
    return [tuple(v for a in e for v in (1 - a, a)) for e in E1]          # multilinear monomials


def hpoly_V_basis():
    return [tuple(v for a in e for v in (2 - a, a)) for e in E2]          # bidegree (2,2,2) monomials


def heval(p, pt):
    """pt = ((x1,y1),(x2,y2),(x3,y3))"""
    flat = [c for xy in pt for c in xy]
    tot = Fr(0)
    for e, c in p.items():
        v = c
        for i in range(6):
            if e[i]:
                v *= flat[i] ** e[i]
        tot += v
    return tot


def hD(p, k):
    """(1/2)(-y_k d/dx_k + x_k d/dy_k) p"""
    out = {}
    ix, iy = 2 * k, 2 * k + 1
    for e, c in p.items():
        if e[ix] > 0:                       # -y d/dx
            e2 = list(e)
            e2[ix] -= 1
            e2[iy] += 1
            out[tuple(e2)] = out.get(tuple(e2), 0) - c * e[ix] * Fr(1, 2)
        if e[iy] > 0:                       # x d/dy
            e2 = list(e)
            e2[iy] -= 1
            e2[ix] += 1
            out[tuple(e2)] = out.get(tuple(e2), 0) + c * e[iy] * Fr(1, 2)
    return {e: c for e, c in out.items() if c != 0}


def hmul(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            out[e] = out.get(e, 0) + c1 * c2
    return {e: c for e, c in out.items() if c != 0}


def analyse_h(states):
    """states: six triples of rational pairs (x_k, y_k)."""
    LB, VB = hpoly_lift_basis(), hpoly_V_basis()
    out = {}
    L = [[heval({m: Fr(1)}, s) for m in LB] for s in states]
    out["rank_lifts"] = rank(L)
    if out["rank_lifts"] != 6:
        return out
    N = nullspace(L, 8)
    G = [{m: n[i] for i, m in enumerate(LB) if n[i] != 0} for n in N]
    taus = []
    for s in states:
        g1 = [heval(hD(G[0], k), s) for k in range(3)]
        g2 = [heval(hD(G[1], k), s) for k in range(3)]
        taus.append(cross(g1, g2))
    out["smooth_at_states"] = all(any(x != 0 for x in tau) for tau in taus)
    rows = []
    for s, tau in zip(states, taus):
        rows.append([heval({m: Fr(1)}, s) for m in VB])
        rows.append([sum(tau[k] * heval(hD({m: Fr(1)}, k), s) for k in range(3)) for m in VB])
    out["rank_R_t"] = out["rank_R_phi"] = rank(rows)
    prods = []
    for g in G:
        for m in LB:
            p = hmul({m: Fr(1)}, g)
            prods.append([p.get(v, Fr(0)) for v in VB])
    out["dim_I0"] = rank(prods)
    out["I0_in_kernel"] = all(sum(a * b for a, b in zip(r, p)) == 0 for r in rows for p in prods)
    out["dim_W"] = 27 - out["rank_R_t"]
    out["N"] = N
    out["G"] = G
    return out


def fmt(o):
    if o.get("rank_lifts") != 6:
        return f"lifts rank {o.get('rank_lifts')} (hypothesis H1 fails)"
    return (f"lifts rank 6; curve smooth at the states: {o['smooth_at_states']}; rank of (R): {o['rank_R_t']} "
            f"(numerators) / {o['rank_R_phi']} (trigonometric basis); dim I_0 = {o['dim_I0']}; I_0 in the kernel: "
            f"{o['I0_in_kernel']}; dim W = {o['dim_W']}")


def main():
    ok = True
    F = Fr
    print("A. the two rational six-tuples of the report (check S2)")
    inst1 = [(F(-1), F(-7, 3), F(-3, 2)), (F(5, 4), F(3, 2), F(-5, 3)), (F(-9, 4), F(4, 5), F(-9, 4)),
             (F(-1, 2), F(9), F(1)), (F(-9), F(8), F(3, 2)), (F(4), F(7, 2), F(5, 4))]
    inst2 = [(F(4), F(1), F(-1, 2)), (F(0), F(4, 5), F(-3)), (F(0), F(1, 5), F(4, 5)),
             (F(-1), F(0), F(6, 5)), (F(3, 5), F(-2), F(-1, 2)), (F(2), F(2, 5), F(2))]
    for name, st in [("instance 1", inst1), ("instance 2", inst2)]:
        o = analyse(st)
        print(f"    {name}: {fmt(o)}")
        ok &= (o["rank_lifts"] == 6 and o["smooth_at_states"] and o["rank_R_t"] == 12 == o["rank_R_phi"]
               and o["dim_I0"] == 15 and o["I0_in_kernel"])
    print("    remark: instance 2 has two states with the same first angle (t_1 = 0) -- it is not 'pairwise distinct"
          " coordinates', and the hypotheses hold all the same")

    print("B. 30 random rational six-tuples of my own (numerators -12..12, denominators 1..6, pairwise distinct angles)")
    rng = random.Random(1127)
    tally = {}
    n = 0
    while n < 30:
        cols = []
        good = True
        for k in range(3):
            vals = set()
            while len(vals) < 6:
                vals.add(F(rng.randint(-12, 12), rng.randint(1, 6)))
            cols.append(rng.sample(sorted(vals), 6))
        st = [tuple(cols[k][i] for k in range(3)) for i in range(6)]
        o = analyse(st)
        key = (o.get("rank_lifts"), o.get("smooth_at_states"), o.get("rank_R_t"), o.get("rank_R_phi"), o.get("dim_I0"),
               o.get("I0_in_kernel"))
        tally[key] = tally.get(key, 0) + 1
        n += 1
    for key, v in tally.items():
        print(f"    (lifts, smooth, rank R (t), rank R (phi), dim I_0, I_0 in kernel) = {key}: {v} instances")
    ok &= tally == {(6, True, 12, 12, 15, True): 30}

    print("C. a six-tuple with a reducible member of the pencil: G = (t_1 - 1) * H(t_2, t_3)")
    # states 1,2 on {t_1 = 1}; states 3..6 with (t_2,t_3) on the curve H = t_2 t_3 - 2 t_2 + 3 t_3 + 1 = 0,
    # i.e. t_3 = (2 t_2 - 1)/(t_2 + 3)
    def on_H(t2):
        return (2 * t2 - 1) / (t2 + 3)
    stC = [(F(1), F(2), F(-3)), (F(1), F(-1, 2), F(5)),
           (F(-2), F(1), on_H(F(1))), (F(3), F(-2), on_H(F(-2))), (F(1, 2), F(4), on_H(F(4))), (F(-5), F(1, 3), on_H(F(1, 3)))]
    o = analyse(stC)
    print(f"    {fmt(o)}")
    # verify that (t_1 - 1) * H is in the span of G_1, G_2
    H = {(0, 1, 1): F(1), (0, 1, 0): F(-2), (0, 0, 1): F(3), (0, 0, 0): F(1)}
    red = pmul({(1, 0, 0): F(1), (0, 0, 0): F(-1)}, H)
    vec = [red.get(e, F(0)) for e in E1]
    in_span = rank(o["N"] + [vec]) == 2
    print(f"    the reducible form (t_1 - 1)*H vanishes at the six states: {all(peval(red, s) == 0 for s in stC)};"
          f" it is in the pencil: {in_span}")
    print("    -> all hypotheses of E20b hold although a combination of g_1, g_2 has a factor depending on one angle;"
          " in the chart in which that factor is at infinity the combination is 'independent of an angle'")
    ok &= (o["rank_lifts"] == 6 and in_span)
    resC = (o["smooth_at_states"], o["rank_R_t"], o["dim_I0"])
    print(f"    (smooth, rank R, dim I_0) = {resC}")
    # the same six-tuple in the chart where the first angle is rotated so that t_1 = 1 becomes infinity cannot be
    # written with finite t; instead put the special value at t_1 = 0 and use the substitution t_1 -> 1/t_1 for the
    # form: G = t_1 * H is then the image of 'H, independent of t_1' under the change of chart.

    print("D. six-tuples with a common factor of G_1, G_2 (the theorem's hypotheses must fail)")
    # all six states on {H(t_2,t_3) = 0}: then (1)*H and t_1*H both vanish: common factor H; the curve is H = 0 x circle?
    stD = [(F(k), F(t2), on_H(F(t2))) for k, t2 in zip([1, -2, 3, F(1, 2), -5, 4], [1, -2, 4, F(1, 3), 2, -1])]
    o = analyse(stD)
    print(f"    six states on the surface H(t_2,t_3) = 0: {fmt(o)}")
    ok &= (o["rank_lifts"] != 6 or not o["smooth_at_states"] or o["rank_R_t"] < 12)

    print("E. degenerate six-tuples: which hypothesis fails")
    cases = {
        "two states sharing two angles": [(F(1), F(2), F(3)), (F(1), F(2), F(-1)), (F(0), F(1, 2), F(5)),
                                          (F(-2), F(3), F(1, 3)), (F(4), F(-1), F(2)), (F(-3), F(5), F(-2))],
        "three states sharing one angle": [(F(1), F(2), F(3)), (F(1), F(-2), F(-1)), (F(1), F(1, 2), F(5)),
                                           (F(-2), F(3), F(1, 3)), (F(4), F(-1), F(2)), (F(-3), F(5), F(-2))],
        "two states sharing one angle": [(F(1), F(2), F(3)), (F(1), F(-2), F(-1)), (F(0), F(1, 2), F(5)),
                                         (F(-2), F(3), F(1, 3)), (F(4), F(-1), F(2)), (F(-3), F(5), F(-2))],
        "two pairs sharing one angle each": [(F(1), F(2), F(3)), (F(1), F(-2), F(-1)), (F(0), F(1, 2), F(5)),
                                             (F(-2), F(1, 2), F(1, 3)), (F(4), F(-1), F(2)), (F(-3), F(5), F(-2))],
    }
    for name, st in cases.items():
        o = analyse(st)
        print(f"    {name}: {fmt(o)}")
    print("F. homogeneous coordinates (cos(phi/2) : sin(phi/2)) -- no chart, states with phi = pi allowed")
    def h(t):
        return (Fr(1), Fr(t))
    o = analyse_h([tuple(h(c) for c in st) for st in inst1])
    print(f"    report's instance 1, homogeneous computation: {fmt(o)}")
    ok &= (o["rank_R_t"] == 12 and o["dim_I0"] == 15 and o["smooth_at_states"])
    # the literal form of C: two states with phi_1 = pi (x_1 = 0), four states with (phi_2, phi_3) on the curve
    # H = 0.  Then x_1 * H is a multilinear form vanishing at the six states; in the t-chart of the report its
    # numerator is H(t_2, t_3): a combination of g_1, g_2 that is independent of the first angle.
    INF = (Fr(0), Fr(1))
    stF = [(INF, h(2), h(-3)), (INF, h(Fr(-1, 2)), h(5)),
           (h(-2), h(1), h(on_H(F(1)))), (h(3), h(-2), h(on_H(F(-2)))), (h(Fr(1, 2)), h(4), h(on_H(F(4)))),
           (h(-5), h(Fr(1, 3)), h(on_H(F(1, 3))))]
    o = analyse_h(stF)
    print(f"    two states at phi_1 = pi, four on H(t_2,t_3) = 0: {fmt(o)}")
    LB = hpoly_lift_basis()
    # x_1 * H in the multilinear basis: H = t2 t3 - 2 t2 + 3 t3 + 1 -> y2 y3 - 2 y2 x3 + 3 x2 y3 + x2 x3, times x_1
    xH = {(1, 0, 0, 1, 0, 1): Fr(1), (1, 0, 0, 1, 1, 0): Fr(-2), (1, 0, 1, 0, 0, 1): Fr(3), (1, 0, 1, 0, 1, 0): Fr(1)}
    vanish = all(heval(xH, st) == 0 for st in stF)
    vec = [xH.get(m, Fr(0)) for m in LB]
    in_span = rank(o["N"] + [vec]) == 2
    print(f"    x_1*H vanishes at the six states: {vanish}; it is a combination of g_1, g_2: {in_span}; in the t-chart"
          " its numerator H(t_2,t_3) does not depend on t_1")
    print("    => the hypotheses of E20b (independent lifts, smooth at the states, (R)) do NOT imply that 'no"
          " combination of g_1, g_2 is independent of an angle'; dim I_0 = 15 holds all the same")
    ok &= (o["rank_lifts"] == 6 and o["smooth_at_states"] and o["rank_R_t"] == 12 and o["dim_I0"] == 15 and vanish
           and in_span)
    # a six-tuple with one state at infinity in every angle, random otherwise
    stG = [(INF, INF, INF), (h(1), h(2), h(-1)), (h(-3), h(Fr(1, 2)), h(4)), (h(Fr(2, 3)), h(-5), h(Fr(1, 4))),
           (h(5), h(Fr(-1, 3)), h(-2)), (h(Fr(-1, 2)), h(3), h(Fr(7, 2)))]
    o = analyse_h(stG)
    print(f"    one state at (pi, pi, pi), five others: {fmt(o)}")
    ok &= (o["rank_R_t"] == 12 and o["dim_I0"] == 15)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
