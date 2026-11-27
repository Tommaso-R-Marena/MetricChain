#!/usr/bin/env python3
"""ER4 (internal AI review) -- Proposition E20a, exact check, written from the definitions.

Claim under test (report, commit b654396, lines 2122-2145): for ONE rational five-tuple on T^3 the secant
4-plane of the five lifted points meets the Segre threefold in finitely many points of (P^1)^3 (all of it:
points at infinity included); by semicontinuity this gives finiteness for general five-tuples.

Method (independent of the author's Groebner computation).  Homogeneous coordinates (x_k : y_k) on each P^1,
lift U = (x_1,y_1) x (x_2,y_2) x (x_3,y_3) in Q^8.  Let n_1, n_2, n_3 span the orthogonal complement of the five
lifts.  A point lies in the secant plane iff n_j . U = 0, j = 1,2,3.  For fixed (x_3 : y_3) these are three
linear conditions on the 4-vector v = (x_1,y_1) x (x_2,y_2):  M(x_3,y_3) v = 0, M a 3 x 4 matrix of linear forms.
If rank M = 3 the kernel is spanned by the vector m of signed 3 x 3 minors (cubic forms), and it is
decomposable iff  Q := m_00 m_11 - m_01 m_10 = 0, a binary sextic.
  * Q identically zero            -> a point over every (x_3 : y_3): the intersection is infinite.
  * Q not zero: only the roots of Q carry points.  Over a root with rank M = 3: one point.  Over a root with
    rank M = 2 (then a multiple root): the kernel is a line of P^3 and meets the quadric {v_00 v_11 = v_01 v_10}
    in two points, or lies in it (infinite).  Rank <= 1: infinite.
So finiteness is decided exactly.  If Q has six distinct roots in P^1 there are exactly six points.
Everything is exact (sympy rationals).

Also: (B) the same for further random rational five-tuples; (ii) the six rank-one matrices at the six zeros are
linearly independent; (iii) the sixth point is a real point; (C) degenerate five-tuples for which the
intersection is NOT finite (the exceptional set is not empty), and what they look like.
"""
import itertools
import random
import sys

import sympy as sp

X3, Y3 = sp.symbols("x3 y3")
S_, T_ = sp.symbols("s_ t_")
IDX = list(itertools.product([0, 1], repeat=3))


def lift(pt):
    """pt = ((x1,y1),(x2,y2),(x3,y3)) -> vector of length 8"""
    return [pt[0][a] * pt[1][b] * pt[2][c] for (a, b, c) in IDX]


def sextic(N):
    """N: three vectors of length 8.  Returns the binary sextic Q(x3,y3), the minor vector and M."""
    M = sp.zeros(3, 4)
    for j in range(3):
        for col, (a, b) in enumerate(itertools.product([0, 1], repeat=2)):
            M[j, col] = N[j][IDX.index((a, b, 0))] * X3 + N[j][IDX.index((a, b, 1))] * Y3
    minors = []
    for col in range(4):
        sub = M.extract([0, 1, 2], [c for c in range(4) if c != col])
        minors.append(sp.expand((-1) ** col * sub.det()))
    Q = sp.expand(minors[0] * minors[3] - minors[1] * minors[2])
    return Q, minors, M


def point_from_vector(v, third):
    """v = (v00, v01, v10, v11) decomposable and non-zero -> point of (P^1)^3"""
    p2 = (v[0], v[1]) if (v[0] != 0 or v[1] != 0) else (v[2], v[3])
    p1 = (v[0], v[2]) if (v[0] != 0 or v[2] != 0) else (v[1], v[3])
    return (p1, p2, third)


def analyse(states_t):
    """states_t: five triples of rationals (t-coordinates).
    Returns dict: rank_lifts, finite (True/False/None=undecided), npoints (distinct, over Q-rational roots only when
    all roots are rational), zeros (list of points), etc."""
    pts = [tuple((sp.Integer(1), sp.Rational(c)) for c in s) for s in states_t]
    L = [lift(p) for p in pts]
    out = {"rank_lifts": sp.Matrix(L).rank()}
    if out["rank_lifts"] != 5:
        return out
    N = [list(v) for v in sp.Matrix(L).nullspace()]
    Q, minors, M = sextic(N)
    if Q == 0:
        out.update(finite=False, reason="sextic identically zero")
        return out
    q_aff = sp.Poly(Q.subs(X3, 1), Y3)
    mult_inf = 6 - q_aff.degree()
    roots = sp.roots(q_aff, filter="Q")                       # rational roots with multiplicities
    nrat = sum(roots.values()) + mult_inf
    out["all_roots_rational"] = (nrat == 6)
    out["distinct_roots"] = len(roots) + (1 if mult_inf else 0)
    g = sp.gcd(q_aff, q_aff.diff(Y3))
    out["squarefree"] = (g.degree() == 0 and mult_inf <= 1)
    if not out["all_roots_rational"]:
        out.update(finite=None, reason="irrational roots (not analysed)")
        return out
    zeros, finite = [], True
    places = [((sp.Integer(1), r), mlt) for r, mlt in roots.items()]
    if mult_inf:
        places.append(((sp.Integer(0), sp.Integer(1)), mult_inf))
    for third, mlt in places:
        M0 = M.subs({X3: third[0], Y3: third[1]})
        rk = M0.rank()
        if rk == 3:
            v = [m.subs({X3: third[0], Y3: third[1]}) for m in minors]
            zeros.append(point_from_vector(v, third))
        elif rk == 2:
            ker = M0.nullspace()
            a, b = ker[0], ker[1]
            v = [S_ * a[i] + T_ * b[i] for i in range(4)]
            quad = sp.expand(v[0] * v[3] - v[1] * v[2])
            if quad == 0:
                finite = False
                out["reason"] = "a kernel line inside the quadric (a line of the Segre variety in the plane)"
                break
            pq = sp.Poly(quad.subs(S_, 1), T_)
            sols = []
            if pq.degree() < 2:                                # a root at s = 0
                sols.append((sp.Integer(0), sp.Integer(1)))
            for rr, mm in sp.roots(pq).items():
                sols.append((sp.Integer(1), rr))
            for (s0, t0) in sols:
                vv = [sp.nsimplify(sp.expand(x.subs({S_: s0, T_: t0}))) for x in v]
                zeros.append(point_from_vector(vv, third))
        else:
            finite = False
            out["reason"] = "rank of M at most one at a root"
            break
    out["finite"] = finite
    if not finite:
        return out
    # verify, convert
    tz = []
    for z in zeros:
        Lz = lift(z)
        assert all(sp.simplify(sum(n[i] * Lz[i] for i in range(8))) == 0 for n in N)
        tz.append(tuple(sp.simplify(p[1] / p[0]) if p[0] != 0 else sp.oo for p in z))
    out["zeros"], out["zeros_t"] = zeros, tz
    given = [tuple(sp.Rational(c) for c in s) for s in states_t]
    out["extra"] = [z for z in tz if z not in given]
    out["all_given_found"] = all(gv in tz for gv in given)
    out["all_real"] = all(all((c == sp.oo) or c.is_real for c in z) for z in tz)
    if len(set(tz)) == 6 and all(all(c == sp.oo or c.is_rational for c in z) for z in tz):
        Lz = [lift(z) for z in zeros]
        outer = sp.Matrix([[a * b for a in v for b in v] for v in Lz])
        out["rank_outer"] = outer.rank()
        sixth = [z for z, t in zip(zeros, tz) if t not in given]
        if len(sixth) == 1:
            A = sp.Matrix(L).T
            sol = (A.T * A).solve(A.T * sp.Matrix(lift(sixth[0])))
            assert A * sol == sp.Matrix(lift(sixth[0]))
            out["n_nonzero_coeffs"] = sum(1 for c in sol if c != 0)
    return out


def main():
    ok = True
    R = sp.Rational
    print("A. the author's rational five-tuple (report check S1)")
    FIVE = [(R(-1), R(-7, 3), R(-3, 2)), (R(5, 4), R(3, 2), R(-5, 3)), (R(-9, 4), R(4, 5), R(-9, 4)),
            (R(-1, 2), R(9), R(1)), (R(-9), R(8), R(3, 2))]
    o = analyse(FIVE)
    print(f"    lifts rank {o['rank_lifts']}; sextic squarefree in P^1: {o['squarefree']}; distinct roots "
          f"{o['distinct_roots']}; all rational: {o['all_roots_rational']}; intersection finite: {o['finite']}; "
          f"points: {len(o['zeros'])}")
    print("    the sixth zero (t-coordinates):", o["extra"])
    stored = (R(18235067499, 12017196881), R(167269954148, 19784421235), R(458968156077, 323733747838))
    print("    equal to the sixth zero in the author's stored output:", tuple(o["extra"][0]) == stored)
    print("    rank of the six lifted outer products:", o.get("rank_outer"),
          "; non-zero coefficients of the sixth lift on the five:", o.get("n_nonzero_coeffs"))
    ok &= bool(o["finite"] and o["squarefree"] and len(o["zeros"]) == 6 and o["all_given_found"]
               and tuple(o["extra"][0]) == stored and o.get("rank_outer") == 6 and o.get("n_nonzero_coeffs", 0) >= 2)

    print("B. 120 random rational five-tuples of my own (numerators -9..9, denominators 1..5)")
    rng = random.Random(20261127)
    cnt = {"total": 0, "finite": 0, "infinite": 0, "undecided": 0, "six_distinct": 0, "outer6": 0,
           "coeff>=2": 0, "infinite_degenerate": 0, "infinite_other": 0, "finite_fewer_than_6": 0,
           "all_real": 0}
    for trial in range(120):
        st = [tuple(R(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(3)) for _ in range(5)]
        if len(set(st)) < 5:
            continue
        o = analyse(st)
        if o["rank_lifts"] != 5:
            continue
        cnt["total"] += 1
        shared2 = any(sum(1 for k in range(3) if a[k] == b[k]) >= 2 for a, b in itertools.combinations(st, 2))
        # three states sharing one angle: their lifts span a plane of the P^3 = {that angle} x P^3, which meets the
        # quadric surface P^1 x P^1 in a conic -- infinitely many zeros as well
        shared2 = shared2 or any(max(sum(1 for b in st if b[k] == a[k]) for a in st) >= 3 for k in range(3))
        if o["finite"] is None:
            cnt["undecided"] += 1
        elif o["finite"]:
            cnt["finite"] += 1
            n = len(set(o["zeros_t"]))
            cnt["all_real"] += int(o["all_real"])
            if n == 6:
                cnt["six_distinct"] += 1
                cnt["outer6"] += int(o.get("rank_outer") == 6)
                cnt["coeff>=2"] += int(o.get("n_nonzero_coeffs", 0) >= 2)
            else:
                cnt["finite_fewer_than_6"] += 1
        else:
            cnt["infinite"] += 1
            cnt["infinite_degenerate" if shared2 else "infinite_other"] += 1
    print("    " + "; ".join(f"{k}: {v}" for k, v in cnt.items()))
    print("    ('degenerate' = two states share two angles, or three states share one angle)")
    ok &= cnt["undecided"] == 0 and cnt["infinite_other"] == 0 and cnt["outer6"] == cnt["six_distinct"]

    print("C. degenerate five-tuples (the exceptional set of 'general' is not empty)")
    deg1 = [(R(1), R(2), R(3)), (R(1), R(2), R(-1)), (R(0), R(1, 2), R(5)), (R(-2), R(3), R(1, 3)), (R(4), R(-1), R(2))]
    o = analyse(deg1)
    print("    two states sharing two angles: finite =", o.get("finite"), "--", o.get("reason"))
    ok &= o.get("finite") is False
    deg2 = [(R(1), R(2), R(3)), (R(1), R(-2), R(-1)), (R(1), R(1, 2), R(5)), (R(1), R(3), R(1, 3)), (R(4), R(-1), R(2))]
    o = analyse(deg2)
    print("    four states sharing one angle: lifts rank", o.get("rank_lifts"), "finite =", o.get("finite"), "--",
          o.get("reason"))
    deg3 = [(R(1), R(2), R(3)), (R(1), R(-2), R(-1)), (R(1), R(1, 2), R(5)), (R(-3), R(3), R(1, 3)), (R(4), R(-1), R(2))]
    o = analyse(deg3)
    print("    three states sharing one angle: lifts rank", o.get("rank_lifts"), "finite =", o.get("finite"), "--",
          o.get("reason"), "; points:", len(o.get("zeros", [])), "; distinct:", len(set(o.get("zeros_t", []))))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
