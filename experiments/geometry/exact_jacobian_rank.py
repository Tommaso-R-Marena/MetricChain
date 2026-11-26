"""Computer-assisted proof of generic local identifiability of K-state ensembles of chains
from averaged squared distances (Theorem H of docs/geometry/ENSEMBLE_RIGIDITY.md).

The map   Phi : (torsions of K states, K-1 free weights)  ->  (mean squared distance on the
pairs of F)   is real-analytic on an irreducible parameter space; if its Jacobian has full
column rank at one point, it has full column rank on a non-empty Zariski-open set, and Phi is
locally injective there (generic local identifiability within the K-state family).

Exactness: the witness has rational torsion half-angle tangents and rational weights; the bond
angle has rational cosine and sine (cos = -5/13) or is tetrahedral (coordinates in Q(sqrt 2)).
The Jacobian is computed in exact arithmetic modulo a prime p; rank_p <= rank over the number
field, so `rank_p = number of parameters` proves full column rank at the witness.

Checked patterns:  complete averaged data (all pairs),  band-limited data |i - j| <= w.
"""
import sys
import random
from fractions import Fraction
from geomlib import Mod, chain_exact, rank_mod_p, tonelli, cross


def setup(geometry):
    if geometry == "rational":
        Mod.p = 2147483629
        return Mod(Fraction(-5, 13)), Mod(Fraction(12, 13))
    Mod.p = 2147483647
    r2 = tonelli(2, Mod.p)
    return Mod(Fraction(-1, 3)), Mod(2 * r2) / 3


def jacobian(K, n, pairs, geometry, seed):
    rnd = random.Random(seed)
    cth, sth = setup(geometry)
    p = Mod.p
    tors = [[Fraction(rnd.randint(-9, 9), rnd.randint(1, 9)) for _ in range(n - 3)] for _ in range(K)]
    wraw = [rnd.randint(1, 9) for _ in range(K)]
    w = [Mod(Fraction(x, sum(wraw))) for x in wraw]
    Xs = [[[c.v for c in pt] for pt in chain_exact(n, t, cth, sth)] for t in tors]
    cols = []
    for k in range(K):
        X = Xs[k]
        for m in range(n - 3):
            ax = [(X[m + 2][c] - X[m + 1][c]) % p for c in range(3)]          # unit bond vector
            dX = [None] * n
            for j in range(m + 3, n):
                rel = [(X[j][c] - X[m + 2][c]) % p for c in range(3)]
                dX[j] = [x % p for x in cross(ax, rel)]
            col = []
            for (i, j) in pairs:
                if j < m + 3 or i >= m + 3:      # both fixed or both moved rigidly
                    col.append(0)
                    continue
                diff = [(X[j][c] - X[i][c]) % p for c in range(3)]
                col.append(2 * w[k].v * sum(diff[c] * dX[j][c] for c in range(3)) % p)
            cols.append(col)
    def d2(X, i, j):
        return sum((X[j][c] - X[i][c]) ** 2 for c in range(3)) % p
    for k in range(K - 1):
        cols.append([(d2(Xs[k], i, j) - d2(Xs[K - 1], i, j)) % p for (i, j) in pairs])
    rows = [[cols[c][r] for c in range(len(cols))] for r in range(len(pairs))]
    return rows, len(cols)


def band_pairs(n, w):
    return [(i, j) for i in range(n) for j in range(i + 3, min(n, i + w + 1))]


def check(K, n, w, geometry):
    pairs = band_pairs(n, w)
    for seed in range(5):
        rows, P = jacobian(K, n, pairs, geometry, seed)
        r = rank_mod_p(rows, Mod.p)
        if r == P:
            return P, len(pairs), r, True
    return P, len(pairs), r, False


if __name__ == "__main__":
    Kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    ok = True
    for geometry in ("rational", "tetrahedral"):
        print(f"== {geometry} bond angle ==")
        print("complete averaged data at n = 2K+3 (K >= 2; the parameter count excludes smaller n)")
        for K in range(2, Kmax + 1):
            n = 2 * K + 3
            P, D, r, good = check(K, n, n, geometry)
            ok &= good
            print(f"  K={K:2d} n={n:3d} parameters={P:4d} data={D:4d} rank_p={r:4d} {'OK' if good else 'FAIL'}", flush=True)
        print("band-limited data, w = K+3, at n = (K^2+3K+4)/2 (the parameter count excludes smaller n and w = K+2)")
        for K in range(1, Kmax + 1):
            n = (K * K + 3 * K + 4) // 2
            P, D, r, good = check(K, n, K + 3, geometry)
            ok &= good
            print(f"  K={K:2d} w={K+3:2d} n={n:3d} parameters={P:4d} data={D:4d} rank_p={r:4d} {'OK' if good else 'FAIL'}", flush=True)
    print("ALL OK" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)
