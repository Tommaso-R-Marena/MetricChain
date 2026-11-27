"""Second hypothesis of Theorem F' (docs/geometry/ENSEMBLE_RIGIDITY.md, section 5.4):
every 3K + 1 consecutive points of the stacked configuration of K generic chains are affinely
independent.  Exact check at rational witnesses (rank modulo a prime after exact evaluation;
a rank modulo p is a lower bound for the rank over Q), together with the conic condition (CC)
at n = n0(K), for K = 1 .. Kmax (default 4), two bond geometries.

The same check was first made by the referee of GEOMETRY-REV-0001 (finding m8) with
independent code.  Usage: exact_general_position.py [Kmax]
"""
import sys
from geomlib import Mod, rank_mod_p
from exact_conic_rank import witness, conic_rows


def check(K, geometry, seed=0, extra=0):
    """extra = 0: windows of 3K + 1 points (the hypothesis).  extra = 1 asks for 3K + 2 affinely
    independent points in dimension 3K, which is impossible (used as a planted error)."""
    n = -(-(9 * K * K + K + 8) // 4)
    dim = 3 * K * (3 * K + 1) // 2
    for s in range(seed, seed + 5):
        tors, Z = witness(K, n, geometry, s)
        p = Mod.p
        cc = rank_mod_p(conic_rows(Z, True, p), p) == dim - (K - 1)
        m = 3 * K + extra
        worst = m
        for i in range(n - m):
            rows = [[(Z[i + a][c] - Z[i][c]) % p for c in range(3 * K)] for a in range(1, m + 1)]
            worst = min(worst, rank_mod_p(rows, p))
        if cc and worst == m:
            return n, s, True
    return n, s, False


if __name__ == "__main__":
    Kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    ok = True
    for geometry in ("rational", "tetrahedral"):
        for K in range(1, Kmax + 1):
            n, s, good = check(K, geometry)
            ok &= good
            print(f"{geometry:11s} K={K} n={n:3d}: (CC) and every {3*K+1} consecutive stacked points "
                  f"affinely independent: {'OK' if good else 'FAIL'} (seed {s})", flush=True)
    print("ALL OK" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)
