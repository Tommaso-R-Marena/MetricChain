"""(j) Independent EXACT replication (referee's own exact chain builder; rational arithmetic,
rank over F_p after an exact evaluation in Q -- rank_p <= rank_Q):

 * Theorem C(b): rank of the conic system = D_K at n0(K) (and D_K - deficit below), for
   bond-angle cosine -5/13 (authors' geometry), -3/5 and -7/25 (new), unit and unequal
   rational bond lengths, K = 1..Kmax;
 * Theorem D(b): a rational 7-atom chain in R^4 (Householder frames instead of quaternions)
   with no quadric through its 11 edge directions; rank over Q.
 * Theorem F' hypothesis: every 3K+1 consecutive stacked points affinely independent, exact.
"""
import sys
import random
from fractions import Fraction as Fr
import numpy as np

P = 2147483647                                    # 2^31 - 1


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def exact_chain(tans, c, s, bonds):
    """Frame propagation in Q.  tans: rational half-angle tangents of the n-3 torsions;
    (c, s) = (cos, sin) of the exterior angle alpha (rational point of the circle)."""
    n = len(bonds) + 1
    Fm = [[Fr(1), Fr(0), Fr(0)], [Fr(0), Fr(1), Fr(0)], [Fr(0), Fr(0), Fr(1)]]
    Rz = [[c, -s, Fr(0)], [s, c, Fr(0)], [Fr(0), Fr(0), Fr(1)]]
    X = [[Fr(0)] * 3, [bonds[0], Fr(0), Fr(0)]]
    for a in range(1, n - 1):
        if a >= 2:
            t = tans[a - 2]
            ct, st = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        else:
            ct, st = Fr(1), Fr(0)
        Rx = [[Fr(1), Fr(0), Fr(0)], [Fr(0), ct, -st], [Fr(0), st, ct]]
        Fm = matmul(matmul(Fm, Rx), Rz)
        X.append([X[a][i] + bonds[a] * Fm[i][0] for i in range(3)])
    return X


def to_mod(x):
    return x.numerator % P * pow(x.denominator % P, -1, P) % P


def rank_mod(rows):
    A = np.array(rows, dtype=np.int64) % P
    nr, nc = A.shape
    r = 0
    for col in range(nc):
        piv = np.nonzero(A[r:, col])[0]
        if len(piv) == 0:
            continue
        p = piv[0] + r
        if p != r:
            A[[r, p]] = A[[p, r]]
        A[r] = A[r] * pow(int(A[r, col]), -1, P) % P
        others = np.nonzero(A[:, col])[0]
        for i in others:
            if i != r:
                A[i] = (A[i] - A[i, col] * A[r]) % P
        r += 1
        if r == nr:
            break
    return r


def conic_rank(K, n, c, s, bonds, rnd):
    Xs = [exact_chain([Fr(rnd.randint(-12, 12), rnd.randint(1, 11)) for _ in range(n - 3)], c, s, bonds) for _ in range(K)]
    # exact check of the constraints (in Q)
    for X in Xs:
        for a in range(n - 1):
            assert sum((X[a + 1][i] - X[a][i]) ** 2 for i in range(3)) == bonds[a] ** 2
        for a in range(n - 2):
            assert sum((X[a + 2][i] - X[a][i]) ** 2 for i in range(3)) == bonds[a] ** 2 + bonds[a + 1] ** 2 + 2 * bonds[a] * bonds[a + 1] * c
    Z = [[to_mod(Xs[k][i][j]) for k in range(K) for j in range(3)] for i in range(n)]      # unweighted stack
    m = 3 * K
    rows = []
    for (i, j) in [(a, a + 1) for a in range(n - 1)] + [(a, a + 2) for a in range(n - 2)]:
        e = [(Z[j][t] - Z[i][t]) % P for t in range(m)]
        rows.append([e[a] * e[b] % P * (1 if a == b else 2) % P for a in range(m) for b in range(a, m)])
    return rank_mod(rows), Z


def part_C(Kmax):
    print("Theorem C(b), exact (rank over F_p of the exactly evaluated system):")
    rnd = random.Random(99)
    ok = True
    for name, (c, s) in (("cos(bond angle) = -5/13", (Fr(5, 13), Fr(12, 13))),
                         ("cos(bond angle) = -3/5", (Fr(3, 5), Fr(4, 5))),
                         ("cos(bond angle) = -7/25", (Fr(7, 25), Fr(24, 25))),
                         ("cos(bond angle) = +3/5 (acute, 53.1 deg)", (Fr(-3, 5), Fr(4, 5)))):
        for kind in ("unit bonds", "unequal rational bonds"):
            for K in range(1, Kmax + 1):
                m = 3 * K
                dim = m * (m + 1) // 2
                DK = dim - (K - 1)
                n0 = -(-(9 * K * K + K + 8) // 4)
                res = []
                for n in (n0 - 1, n0, n0 + 1):
                    bonds = [Fr(1)] * (n - 1) if kind == "unit bonds" else [Fr(rnd.randint(5, 14), 8) for _ in range(n - 1)]
                    best = 0
                    for attempt in range(3):
                        r, _ = conic_rank(K, n, c, s, bonds, rnd)
                        best = max(best, r)
                    want = min(DK, 2 * n - 3)
                    res.append((n, best, want))
                    ok &= (best == want)
                print(f"   {name:42s} {kind:22s} K={K}: D_K={DK}, n0={n0}: " +
                      "; ".join(f"n={n}: rank {r} (expected {w_})" for n, r, w_ in res))
    print("   ALL AS PREDICTED" if ok else "   MISMATCH FOUND")


def frac_rank(rows):
    A = [list(r) for r in rows]
    r = 0
    for col in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][col] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        A[r] = [x / A[r][col] for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][col] != 0:
                f = A[i][col]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
        if r == len(A):
            break
    return r


def part_D():
    print("Theorem D(b), exact: rational 7-atom chains in R^4 (Householder construction)")
    rnd = random.Random(7)
    for name, (g, sg) in (("gamma = 5/13 (authors' geometry)", (Fr(5, 13), Fr(12, 13))), ("gamma = 3/5", (Fr(3, 5), Fr(4, 5)))):
        for trial in range(3):
            # rational unit vector in R^4
            w = [Fr(rnd.randint(-5, 5)) for _ in range(4)]
            while all(x == 0 for x in w):
                w = [Fr(rnd.randint(-5, 5)) for _ in range(4)]
            # Householder reflection H = I - 2 w w^T / (w^T w) is a rational orthogonal matrix
            def house(w):
                ww = sum(x * x for x in w)
                return [[(Fr(1) if i == j else Fr(0)) - 2 * w[i] * w[j] / ww for j in range(4)] for i in range(4)]
            Q = house(w)                                   # columns: orthonormal rational frame
            u = [Q[i][0] for i in range(4)]
            U = [u]
            for a in range(5):
                # rational point (p, q, r) of S^2 by stereographic projection
                s1, t1 = Fr(rnd.randint(-6, 6), rnd.randint(1, 5)), Fr(rnd.randint(-6, 6), rnd.randint(1, 5))
                den = 1 + s1 * s1 + t1 * t1
                pqr = [2 * s1 / den, 2 * t1 / den, (s1 * s1 + t1 * t1 - 1) / den]
                v = [sum(Q[i][j + 1] * pqr[j] for j in range(3)) for i in range(4)]     # unit, orthogonal to u
                unew = [g * u[i] + sg * v[i] for i in range(4)]
                # new rational orthonormal frame with first column unew: reflect e_1 -> unew
                wv = [(Fr(1) if i == 0 else Fr(0)) - unew[i] for i in range(4)]
                if all(x == 0 for x in wv):
                    Q = [[Fr(1) if i == j else Fr(0) for j in range(4)] for i in range(4)]
                else:
                    Q = house(wv)
                    assert [Q[i][0] for i in range(4)] == unew
                u = unew
                U.append(u)
            dot = lambda a, b: sum(x * y for x, y in zip(a, b))
            assert all(dot(x, x) == 1 for x in U) and all(dot(U[a], U[a + 1]) == g for a in range(5))
            edges = U + [[U[a][i] + U[a + 1][i] for i in range(4)] for a in range(5)]
            rows = [[e[a] * e[b] * (1 if a == b else 2) for a in range(4) for b in range(a, 4)] for e in edges]
            r = frac_rank(rows)
            span = frac_rank(U)
            # 6-atom sub-chain: 9 edges, rank at most 9 < 10
            edges6 = U[:5] + [[U[a][i] + U[a + 1][i] for i in range(4)] for a in range(4)]
            r6 = frac_rank([[e[a] * e[b] * (1 if a == b else 2) for a in range(4) for b in range(a, 4)] for e in edges6])
            print(f"   {name}, trial {trial}: 11 edge directions, rank over Q of the quadric system = {r} (dim Sym(4) = 10); "
                  f"bond vectors span R^{span}; first 6 atoms: rank {r6} of 10")


def part_F(Kmax=4):
    print("Theorem F' hypothesis, exact: every 3K+1 consecutive points of the stacked configuration affinely independent")
    rnd = random.Random(5)
    c, s = Fr(5, 13), Fr(12, 13)
    for K in range(1, Kmax + 1):
        n0 = -(-(9 * K * K + K + 8) // 4)
        n = n0
        bonds = [Fr(1)] * (n - 1)
        r, Z = conic_rank(K, n, c, s, bonds, rnd)
        m = 3 * K
        okall = True
        for i in range(n - m):
            rows = [[(Z[i + a][t] - Z[i][t]) % P for t in range(m)] for a in range(1, m + 1)]
            okall &= (rank_mod(rows) == m)
        print(f"   K={K} n={n}: conic rank {r}; all {n - m} windows of {m + 1} consecutive stacked points affinely independent (mod p): {okall}")


if __name__ == "__main__":
    Kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    part_C(Kmax)
    part_D()
    part_F(min(Kmax, 4))
