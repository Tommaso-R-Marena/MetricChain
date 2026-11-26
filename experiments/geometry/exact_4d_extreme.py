"""Exact witness for Theorem D(b): a chain with 7 atoms in R^4 (unit bonds, 1-3 distance
squared 36/13, i.e. the bond angle with cosine -5/13) whose 11 statewise-constrained edge
directions lie on no quadric cone of R^4.  Its Gram matrix is therefore an extreme point of
the spectrahedron S of all Hilbert-space chains with these bond data, has rank 4, and cannot
be the mean of Gram matrices of chains in R^3: the set K of ensemble-averaged squared-distance
matrices is strictly smaller than its semidefinite relaxation S for n >= 7.

Construction (all rational): unit quaternions.  For a unit quaternion u the quaternions
u*i, u*j, u*k are orthonormal and orthogonal to u; the next bond direction is
    u' = (5/13) u + (12/13) (a u*i + b u*j + c u*k),   (a, b, c) a rational point of S^2,
so that u.u' = 5/13 and |u + u'|^2 = 36/13.
The rank of the 11 x 10 system "e^T S e = 0" is computed in exact rational arithmetic.
"""
from fractions import Fraction as F
import sys


def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
            a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
            a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def s2(s, t):
    """Rational point of the unit sphere by inverse stereographic projection."""
    s, t = F(s), F(t)
    den = 1 + s * s + t * t
    return (2 * s / den, 2 * t / den, (s * s + t * t - 1) / den)


def rank_rational(rows):
    A = [list(r) for r in rows]
    r = 0
    for c in range(len(A[0])):
        piv = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        A[r] = [x / A[r][c] for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r


def witness():
    I, J, Kq = (F(0), F(1), F(0), F(0)), (F(0), F(0), F(1), F(0)), (F(0), F(0), F(0), F(1))
    U = [(F(1), F(0), F(0), F(0))]
    params = [(1, 2), (-1, 3), (2, -1), (1, -3), (3, 2)]
    for (s, t) in params:
        u = U[-1]
        a, b, c = s2(F(s, 2), F(t, 3))
        ui, uj, uk = qmul(u, I), qmul(u, J), qmul(u, Kq)
        v = tuple(a * ui[m] + b * uj[m] + c * uk[m] for m in range(4))
        U.append(tuple(F(5, 13) * u[m] + F(12, 13) * v[m] for m in range(4)))
    return U


def main():
    U = witness()
    dot = lambda p, q: sum(x * y for x, y in zip(p, q))
    assert all(dot(u, u) == 1 for u in U), "bond lengths"
    assert all(dot(U[a], U[a + 1]) == F(5, 13) for a in range(5)), "bond angles"
    edges = list(U) + [tuple(U[a][m] + U[a + 1][m] for m in range(4)) for a in range(5)]
    assert all(dot(e, e) == F(36, 13) for e in edges[6:])
    idx = [(i, j) for i in range(4) for j in range(i, 4)]
    rows = [[e[i] * e[j] * (1 if i == j else 2) for (i, j) in idx] for e in edges]
    r = rank_rational(rows)
    # the bond vectors span R^4 (so the Gram matrix has rank 4)
    span = rank_rational([list(u) for u in U])
    print(f"7-atom chain in R^4: {len(edges)} edge directions, rank of the quadric system = {r} "
          f"(dim Sym(4) = 10), rank of the bond vectors = {span}")
    ok = (r == 10 and span == 4)
    print("OK: no quadric through the edge directions; rank-4 extreme point of S" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
