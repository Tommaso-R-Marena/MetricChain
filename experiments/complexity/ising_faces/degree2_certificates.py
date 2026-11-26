"""Degree-2 certificates (Proposition 13 of docs/complexity/ISING_GROUND_SETS.md).

Claim: a set V of states is exactly the ground-state set of some pair energy that has a sum-of-squares certificate of
degree 2 (E - E0 = x^T Q x on the cube with Q positive semidefinite) if and only if the span L of V contains no sign
vector other than +-V; and then Q = I - P_L (the projector onto the orthogonal complement of L) works.

Checks (exact rational arithmetic):
  (1) for random V whose span contains no other sign vector: Q = I - P_L is rational, positive semidefinite by
      construction (Q^2 = Q = Q^T verified), E(x) = x^T Q x vanishes exactly on +-V among ALL states (n <= 14);
  (2) for V whose span contains another sign vector y: every psd Q with Q x^k = 0 has Q y = 0 (linear algebra:
      y in L), illustrated with Q = I - P_L: E(y) = 0;
  (3) random instances: how often does the span of K uniform random sign vectors of length n contain another sign
      vector?  (The note proves: probability <= 2^(K-n) + C(n,K) 2^K (3/4)^(n-K).)

Usage: python3 degree2_certificates.py
"""
import itertools
import random
from fractions import Fraction
from math import comb

from span_algorithm import sign_vectors_in_span, rref


def projector_complement(V):
    """I - P_L for L = span(V), exact.  P_L = B^T (B B^T)^{-1} B with B a basis of L (rows)."""
    B, _ = rref(V)
    r, n = len(B), len(B[0])
    G = [[sum(B[i][c] * B[j][c] for c in range(n)) for j in range(r)] for i in range(r)]
    # invert G by Gauss-Jordan over Q
    A = [row[:] + [Fraction(int(i == j)) for j in range(r)] for i, row in enumerate(G)]
    for c in range(r):
        p = next(i for i in range(c, r) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        inv = 1 / A[c][c]
        A[c] = [v * inv for v in A[c]]
        for i in range(r):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    Ginv = [row[r:] for row in A]
    # P = B^T Ginv B
    GB = [[sum(Ginv[i][k] * B[k][c] for k in range(r)) for c in range(n)] for i in range(r)]
    P = [[sum(B[k][a] * GB[k][b] for k in range(r)) for b in range(n)] for a in range(n)]
    return [[Fraction(int(a == b)) - P[a][b] for b in range(n)] for a in range(n)]


def quad(Q, x):
    n = len(x)
    return sum(Q[a][b] * x[a] * x[b] for a in range(n) for b in range(n))


def canon(v):
    return tuple(v) if v[0] > 0 else tuple(-t for t in v)


if __name__ == "__main__":
    rng = random.Random(4)
    # (1), (2)
    ok1 = ok2 = True
    n1 = n2 = 0
    while n1 < 40 or n2 < 15:
        n = rng.randint(5, 11)
        K = rng.randint(2, min(6, n - 1))
        V = list({canon([rng.choice((1, -1)) for _ in range(n)]) for _ in range(K)})
        if len(V) < 2:
            continue
        if rng.random() < 0.5 and len(V) >= 3:
            # plant a combination to make extra sign vectors likely: replace one state by a product-type relation
            a, b, c = V[0], V[1], V[2]
            d = canon([a[i] * b[i] * c[i] for i in range(n)])
            if d not in V:
                V.append(d)
        extra = [y for y in sign_vectors_in_span(V) if y not in set(V)]
        Q = projector_complement(V)
        idem = all(sum(Q[a][k] * Q[k][b] for k in range(n)) == Q[a][b] for a in range(n) for b in range(n))
        sym = all(Q[a][b] == Q[b][a] for a in range(n) for b in range(n))
        zeros = [x for x in ((1,) + r for r in itertools.product((1, -1), repeat=n - 1)) if quad(Q, x) == 0]
        if not extra:
            n1 += 1
            ok1 &= idem and sym and sorted(zeros) == sorted(V)
        else:
            n2 += 1
            ok2 &= idem and sym and sorted(zeros) == sorted(set(V) | set(extra))
    print(f"(1) {n1} sets whose span has no other sign vector: x^T (I - P_L) x vanishes exactly on V among all states: {ok1}")
    print(f"(2) {n2} sets whose span has other sign vectors: the zero set of x^T (I - P_L) x is V plus exactly these: {ok2}")
    # (3)
    TRIALS = 60
    print(f"(3) span of K uniform random sign vectors of length n: fraction of {TRIALS} trials with another sign vector,")
    print("    and the bound 2^(K-n) + C(n,K) 2^K (3/4)^(n-K) (meaningful only when < 1):")
    for n, K in ((12, 3), (12, 6), (12, 9), (12, 11), (16, 4), (16, 8), (16, 12), (40, 2), (60, 3), (100, 5), (200, 10)):
        if K <= 12 and n <= 16:
            hits = 0
            for _ in range(TRIALS):
                V = list({canon([rng.choice((1, -1)) for _ in range(n)]) for _ in range(K)})
                hits += any(y not in set(V) for y in sign_vectors_in_span(V))
            frac = f"{hits / TRIALS:.3f}"
        else:
            frac = "not simulated"
        bound = 2.0 ** (K - n) + comb(n, K) * 2.0 ** K * 0.75 ** (n - K)
        print(f"    n = {n:3d}, K = {K:2d}: observed {frac}; bound {bound:.3g}")
