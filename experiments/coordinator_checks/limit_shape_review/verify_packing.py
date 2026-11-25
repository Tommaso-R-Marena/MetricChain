#!/usr/bin/env python3
"""Assistant B — exact verification of the reviewer's four packings (N3 of SCI-REV-0002) with OWN code.

Proved points of K^br:  four exact ones (rod, row of stems, crystal: Proposition 11.72(d); helix: N1, checked in
n1_helix.py) and the ten bridges verified from coordinates by verify_witness.py (wit/verified.json), each
with delta = 168/(N+3) (Theorem 11.69, norm ||dp||_c + |dg|).  The vertex list is built HERE from my own verified
counts; the reviewer's file out/rigorous_packing_vertices.txt is only used to fix the ORDER of the columns of the
weight files, and every row of it must coincide exactly with one of my points.

For every stored packing (one line of weights per point): lambda >= 0, sum = 1, and for all pairs
     L ||p_k - p_l||_c  >  e (g_k + g_l) + 2 eps1 + max(L, e) (d_k + d_l),    e = 1,
with (p, g) = sum lambda_i q_i, d = sum lambda_i delta_i, everything in Fractions.
"""
import os, sys, json, itertools
from fractions import Fraction as Fr
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.join(HERE, "reviewer_packings")


def cnorm(d):
    return 5 * abs(d[0]) + 3 * abs(d[0] + d[1]) + abs(d[0] + d[1] + d[2])


def my_points():
    pts = [(Fr(0), Fr(0), Fr(0), Fr(0), Fr(0)), (Fr(1, 2), Fr(2), Fr(3, 2), Fr(0), Fr(0)),
           (Fr(1), Fr(5), Fr(6), Fr(0), Fr(0)), (Fr(0), Fr(0), Fr(1), Fr(1), Fr(0))]
    ver = json.load(open(os.path.join(HERE, "wit", "verified.json")))
    for name, r in sorted(ver.items()):
        assert r["ok"]
        N = r["N"]
        pts.append(tuple(Fr(c, N) for c in r["hg"]) + (Fr(168, N + 3),))
    return pts


if __name__ == "__main__":
    mine = my_points()
    V = [tuple(Fr(t) for t in line.split()) for line in open(os.path.join(SCI, "rigorous_packing_vertices.txt"))
         if not line.startswith("#")]
    assert len(V) == 14 and len(mine) == 14
    assert sorted(V) == sorted(mine), "the reviewer's vertex list differs from my verified points"
    assert V[:4] == mine[:4]
    print("vertex list: the reviewer's 14 rows coincide exactly with my 4 exact points + 10 verified bridges; largest delta =",
          float(max(v[4] for v in V)))
    e = Fr(1)
    for tag, L, e1, claimed in (("L1_e12", Fr(1), Fr(1, 2), 116), ("L1_e14", Fr(1), Fr(1, 4), 451),
                                ("L15_e12", Fr(1, 5), Fr(1, 2), 8), ("L15_e14", Fr(1, 5), Fr(1, 4), 19)):
        P = []
        for line in open(os.path.join(SCI, f"rigorous_packing_{tag}.txt")):
            if line.startswith("#"):
                continue
            lam = [Fr(t) for t in line.split()]
            assert len(lam) == 14 and all(x >= 0 for x in lam) and sum(lam) == 1
            P.append(tuple(sum(lam[i] * V[i][k] for i in range(14)) for k in range(5)))
        assert len(set(P)) == len(P)
        worst = None
        ok = True
        for a, b in itertools.combinations(P, 2):
            lhs = L * cnorm([a[k] - b[k] for k in range(3)])
            rhs = e * (a[3] + b[3]) + 2 * e1 + max(L, e) * (a[4] + b[4])
            if not lhs > rhs:
                ok = False
            m = lhs - rhs
            if worst is None or m < worst:
                worst = m
        # how many of the points use the helix / the finite bridges, and how many have g = 0 and d = 0 (inside T0)
        nT0 = sum(1 for q in P if q[3] == 0 and q[4] == 0)
        print(f"(L, eps1) = ({L}, {e1}): {len(P)} points (claimed {claimed}); weights valid; pairwise condition holds exactly: {ok}; "
              f"smallest margin lhs - rhs = {float(worst):.6f}; points with g = 0 and d = 0 (in T0): {nT0}", flush=True)
