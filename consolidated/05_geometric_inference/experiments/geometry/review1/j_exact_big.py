"""Replication of Theorem C(b) for K = 5..12 (cos = -5/13, unit bonds; and cos = -3/5 with
unequal rational bonds), with the referee's exact builder (see j_exact.py)."""
import sys, random, time
from fractions import Fraction as Fr
from j_exact import conic_rank
rnd = random.Random(2026)
Kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
for name, (c, s), kind in (("cos=-5/13 unit bonds", (Fr(5, 13), Fr(12, 13)), "unit"),
                           ("cos=-3/5 unequal bonds", (Fr(3, 5), Fr(4, 5)), "unequal")):
    for K in range(5, Kmax + 1):
        m = 3 * K
        dim = m * (m + 1) // 2
        DK = dim - (K - 1)
        n0 = -(-(9 * K * K + K + 8) // 4)
        out = []
        t0 = time.time()
        for n in (n0 - 1, n0):
            bonds = [Fr(1)] * (n - 1) if kind == "unit" else [Fr(rnd.randint(5, 14), 8) for _ in range(n - 1)]
            r, _ = conic_rank(K, n, c, s, bonds, rnd)
            out.append((n, r, min(DK, 2 * n - 3)))
        print(f"{name}: K={K:2d} D_K={DK} n0={n0}: " + "; ".join(f"n={n}: rank {r} (expected {w})" for n, r, w in out)
              + f"   [{time.time()-t0:.0f}s]", flush=True)
