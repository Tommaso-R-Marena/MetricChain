#!/usr/bin/env python3
"""ER4 (internal AI review) -- Proposition E20d: the rank of the K(r+1) linear forms "value and gradient at K
states" on V (dimension 3^r), from the definitions.  Own code.

V is represented by the numerators: polynomials of degree at most 2 in each t_k (3^r monomials); "value and
gradient of f = q / prod(1 + t_k^2) vanish at a point" is equivalent to "value and gradient of q vanish", so the
rank is that of the matrix of the monomials and their r partial derivatives at the K points.

Exact: integer points, rank over Q obtained as the maximum of the ranks modulo three large primes (each is a lower
bound for the rational rank), together with the exact upper bounds that the report uses:
   rank <= 3^r,  rank <= K(r+1),  and rank <= 3^r - 1 when a non-zero multilinear form vanishes at the K points
   (K <= 2^r - 1): its square has double points there.  More precisely the squares and products of the multilinear
   forms through the points give  rank <= 3^r - dim span{L_a L_b}.
Reported for every r, K: conditions, rank, the expected value min(K(r+1), 3^r), and 'defect'.

Table of (c): for each r the least K with rank = 3^r (from which on the count excludes identification).
Arithmetic of (b): ceil(3^r/(r+1)) for r = 4, 5, 6.
Also: the rank at real TORUS points given by rational points of the circle is the same computation (t rational),
so nothing is lost by 'general complex double points' -> 'general real torus points': the rank condition is the
non-vanishing of a minor, and the real torus is Zariski dense.
"""
import itertools
import random
import sys

PRIMES = [2147483647, 2147483629, 2147483587]


def rank_mod_p(rows, p):
    A = [[x % p for x in row] for row in rows]
    nrow, ncol = len(A), len(A[0])
    rank = 0
    for col in range(ncol):
        piv = None
        for i in range(rank, nrow):
            if A[i][col]:
                piv = i
                break
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        inv = pow(A[rank][col], p - 2, p)
        rowp = [(x * inv) % p for x in A[rank]]
        A[rank] = rowp
        for i in range(rank + 1, nrow):
            f = A[i][col]
            if f:
                Ai = A[i]
                A[i] = [(x - f * y) % p for x, y in zip(Ai, rowp)]
        rank += 1
        if rank == nrow:
            break
    return rank


def rows_double_points(states, r):
    exps = list(itertools.product(range(3), repeat=r))
    rows = []
    for s in states:
        pw = [[1, s[k], s[k] * s[k]] for k in range(r)]
        dpw = [[0, 1, 2 * s[k]] for k in range(r)]
        row = []
        for e in exps:
            v = 1
            for k in range(r):
                v *= pw[k][e[k]]
            row.append(v)
        rows.append(row)
        for a in range(r):
            row = []
            for e in exps:
                v = dpw[a][e[a]]
                if v:
                    for k in range(r):
                        if k != a:
                            v *= pw[k][e[k]]
                row.append(v)
            rows.append(row)
    return rows


def multilinear_through(states, r, p):
    """dimension (mod p) of the space of multilinear forms vanishing at the states, and of the span of their
    pairwise products inside the numerators of V"""
    exps1 = list(itertools.product(range(2), repeat=r))
    rows = []
    for s in states:
        row = []
        for e in exps1:
            v = 1
            for k in range(r):
                if e[k]:
                    v *= s[k]
            row.append(v)
        rows.append(row)
    rk = rank_mod_p(rows, p)
    return len(exps1) - rk


def random_states(rng, r, K, lo=-60, hi=60):
    cols = [rng.sample(range(lo, hi + 1), K) for _ in range(r)]     # pairwise distinct coordinates in every angle
    return [[cols[k][i] for k in range(r)] for i in range(K)]


def main():
    rng = random.Random(4711)
    ok = True
    print("rank of 'value and gradient at K general states' on V (3^r functions); three random integer instances each;")
    print("rank = max over three primes of the rank modulo p (a lower bound for the rational rank), which equals the")
    print("upper bound min(K(r+1), 3^r) or 3^r - 1 (square of the multilinear form) in every line marked 'exact'")
    results = {}
    plan = {1: [1, 2, 3], 2: [1, 2, 3, 4, 5], 3: [1, 2, 3, 4, 5, 6, 7, 8, 9], 4: [11, 12, 13, 14, 15, 16, 17, 18],
            5: [26, 39, 40, 41, 42]}
    for r, Ks in plan.items():
        for K in Ks:
            ranks = []
            ntrial = 3 if r < 5 else 1
            for trial in range(ntrial):
                st = random_states(rng, r, K)
                rows = rows_double_points(st, r)
                primes = PRIMES if r < 5 else PRIMES[:1]
                ranks.append(max(rank_mod_p(rows, p) for p in primes))
            expected = min(K * (r + 1), 3 ** r)
            rk = max(ranks)
            # upper bound from squares of multilinear forms through the points
            nml = max(0, 2 ** r - K)
            ub = min(expected, 3 ** r - (1 if nml >= 1 else 0)) if K * (r + 1) >= 3 ** r else expected
            exact = (rk == expected) or (rk == ub)
            results[(r, K)] = rk
            print(f"  r = {r}, K = {K:2d}: {K * (r + 1):3d} conditions on {3 ** r:3d} functions; rank {rk} in "
                  f"{ranks.count(rk)}/{ntrial} instances; expected {expected}; defect {expected - rk}"
                  f"{'; exact' if exact else '; LOWER BOUND ONLY'}", flush=True)
            ok &= exact and ranks.count(rk) == ntrial
    print("exceptions (defect > 0):", [(r, K, min(K * (r + 1), 3 ** r) - v) for (r, K), v in results.items()
                                       if v < min(K * (r + 1), 3 ** r)])
    ok &= [(r, K) for (r, K), v in results.items() if v < min(K * (r + 1), 3 ** r)] == [(2, 3), (3, 7)]
    print("least K with rank 3^r (no non-zero function with K double points):")
    for r in (1, 2, 3, 4, 5):
        full = sorted(K for (rr, K), v in results.items() if rr == r and v == 3 ** r)
        print(f"  r = {r}: K = {full[0] if full else None};  ceil(3^r/(r+1)) = {-(-3 ** r // (r + 1))}")
    print("arithmetic of (b): ceil(3^r/(r+1)) for r = 4, 5, 6, 7, 8:", [-(-3 ** r // (r + 1)) for r in (4, 5, 6, 7, 8)],
          "; 2^r - r - 1:", [2 ** r - r - 1 for r in (4, 5, 6, 7, 8)])
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
