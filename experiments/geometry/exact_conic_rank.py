"""Computer-assisted proof of the generic conic condition (Theorem C of
docs/geometry/ENSEMBLE_RIGIDITY.md).

For K conformations of a chain with n atoms (unit bonds, a fixed bond angle), let z be the
*unweighted* stacked configuration in R^{3K} (the dimension of the space N(z) of quadrics
through the statewise-constrained edge directions does not depend on the weights).  N(z)
always contains the (K-1)-dimensional space of trivial quadrics sum_k s_k E_k, sum_k s_k = 0,
so   rank(conic matrix) <= dim Sym(3K) - (K-1).
This script exhibits, for each K, an explicit rational witness at which equality holds at
n = n0(K) = ceil((9K^2+K+8)/4)  (bond lengths and bond angles fixed) and at
n - 1 = N0(K) = (9K^2+K+2)/2 bonds (bond lengths only, "freely jointed").

Rigour: the witness has rational torsion half-angle tangents; all coordinates lie in
Q (bond angle with rational cos and sin) or in Q(sqrt 2) (tetrahedral angle).  The rank is
computed after reduction modulo a prime p (with sqrt 2 mapped to a square root of 2 mod p).
A ring homomorphism to a field cannot increase the rank, so
      rank_p  <=  rank_Q  <=  dim Sym(3K) - (K-1),
and rank_p = dim Sym(3K) - (K-1) proves the claim at the witness; the set of torsion vectors
at which the rank is maximal is then a non-empty Zariski-open subset of the torus.
"""
import sys
import random
from fractions import Fraction
from geomlib import Mod, chain_exact, rank_mod_p, tonelli


def witness(K, n, geometry, seed):
    rnd = random.Random(seed)
    if geometry == "rational":            # cos = -5/13, sin = 12/13   (112.62 degrees)
        Mod.p = 2147483629
        cth, sth = Mod(Fraction(-5, 13)), Mod(Fraction(12, 13))
    elif geometry == "tetrahedral":       # cos = -1/3, sin = 2 sqrt(2)/3   (109.47 degrees)
        Mod.p = 2147483647                # 2^31 - 1 = 7 mod 8, so 2 is a square
        r2 = tonelli(2, Mod.p)
        cth, sth = Mod(Fraction(-1, 3)), Mod(2 * r2) / 3
    else:
        raise ValueError(geometry)
    tors = [[Fraction(rnd.randint(-9, 9), rnd.randint(1, 9)) for _ in range(n - 3)]
            for _ in range(K)]
    Xs = [chain_exact(n, t, cth, sth) for t in tors]
    Z = [[Xs[k][i][j].v for k in range(K) for j in range(3)] for i in range(n)]
    return tors, Z


def conic_rows(Z, angles, p):
    m = len(Z[0])
    rows = []
    edges = [[(Z[i + 1][c] - Z[i][c]) % p for c in range(m)] for i in range(len(Z) - 1)]
    if angles:
        edges += [[(Z[i + 2][c] - Z[i][c]) % p for c in range(m)] for i in range(len(Z) - 2)]
    for e in edges:
        rows.append([(e[i] * e[j] * (1 if i == j else 2)) % p
                     for i in range(m) for j in range(i, m)])
    return rows


def check(K, geometry, angles, seed=0):
    dim = 3 * K * (3 * K + 1) // 2
    target = dim - (K - 1)
    if angles:
        n = -(-(9 * K * K + K + 8) // 4)
    else:
        n = (9 * K * K + K + 2) // 2 + 1
    for s in range(seed, seed + 5):       # a few seeds: a witness only has to exist
        tors, Z = witness(K, n, geometry, s)
        r = rank_mod_p(conic_rows(Z, angles, Mod.p), Mod.p)
        if r == target:
            return n, dim, r, s, True
    return n, dim, r, s, False


if __name__ == "__main__":
    Kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    ok = True
    for geometry in ("rational", "tetrahedral"):
        for angles in (True, False):
            for K in range(1, Kmax + 1):
                n, dim, r, s, good = check(K, geometry, angles)
                ok &= good
                print(f"{geometry:11s} {'bond+angle' if angles else 'bonds only':10s} K={K:2d} "
                      f"n={n:4d} dimSym={dim:4d} rank_p={r:4d} target={dim-(K-1):4d} "
                      f"seed={s} {'OK' if good else 'FAIL'}", flush=True)
    print("ALL OK" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)
