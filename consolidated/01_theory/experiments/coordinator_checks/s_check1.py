#!/usr/bin/env python3
"""Coordinator spot checks of workstream S, part 1: finite inequalities on exhaustive data.
(a) own enumeration for N <= NMAX beads: classes (h3,h8,h11) -> gmin;
(b) optional: the class tables of the other division (directory given as argv[2]) up to 27 beads.
Checks: Proposition 4.1 (three inequalities, finite form), Theorem 4.2 (eleven rows, finite form
c.h <= bN + 4M + c3 + 2c8), Proposition 4.5 (surface term), and reports the largest value of c.h - bN per row
for the two extra rows of Theorem 4.2' and of the three gauche inequalities (limit statements: no finite constant
was claimed, so these are reported, not asserted)."""
import sys, os, re
from fractions import Fraction as Fr
from s_lat import *

ROWS = [((-1, 0, 0), 0, Fr(1, 2)), ((4, -1, 0), 0, 5), ((6, -1, 0), 1, 6), ((-2, 1, 0), 3, 2), ((-1, 1, -1), 0, 3),
        ((-1, 2, -1), 3, 4), ((-4, 2, -1), 2, 6), ((3, 4, -3), 5, 6), ((6, -2, 1), 2, 6), ((0, -1, 2), 7, 1),
        ((-3, 0, 2), 9, 3)]
ROWS2_EXTRA = [((-3, 2, -1), 2), ((-3, 4, -3), 2)]
GAUCHE = [((-5, 0, 2), 8), ((0, -1, 2), 7), ((-4, 1, 1), 7)]   # q >= c.p - b


def classes_own(N):
    cl = {}
    for w in enum_walks(N):
        h3, h8, h11, g = profile(w)
        k = (h3, h8, h11)
        if k not in cl or g < cl[k]:
            cl[k] = g
    return cl


def classes_file(path):
    cl = {}
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        f = line.split()
        cl[(int(f[0]), int(f[1]), int(f[2]))] = int(f[4])
    return cl


def check(N, cl, src):
    worst = {}
    for (h, g) in cl.items():
        h3, h8, h11 = h
        # Proposition 4.1
        assert h8 >= 4 * h3 - 2 and h8 >= 6 * h3 - N - 4 and h8 <= 2 * h3 + 3 * N + 3 and h3 >= 0, (N, h)
        # Theorem 4.2, finite form
        for i, (c, b, M) in enumerate(ROWS):
            lhs = c[0] * h3 + c[1] * h8 + c[2] * h11
            rhs = b * N + 4 * M + c[0] + 2 * c[1]
            assert lhs <= rhs, (N, h, c)
            worst[i] = max(worst.get(i, -10 ** 9), lhs - b * N)
        # Proposition 4.5
        assert 9 * h3 + 4 * h8 + h11 <= 35 * N - 17.6 * N ** (2 / 3) + 17 + 1e-9, (N, h)
        assert h3 <= N - 2 ** (-2 / 3) * N ** (2 / 3) + 1 + 1e-9 and h8 <= 5 * N - 3 * N ** (2 / 3) + 2 + 1e-9
    ext = [max(c[0] * h[0] + c[1] * h[1] + c[2] * h[2] - b * N for h in cl) for (c, b) in ROWS2_EXTRA]
    gau = [max(c[0] * h[0] + c[1] * h[1] + c[2] * h[2] - b * N - g for h, g in cl.items()) for (c, b) in GAUCHE]
    mx = max(9 * h[0] + 4 * h[1] + h[2] for h in cl)
    kN = (1 - mx / (35 * N)) * N ** (1 / 3)
    print(f"N={N:2d} [{src}] classes={len(cl):5d}  all finite inequalities hold;  max ||N^x||_1/N = {mx/N:7.3f}  k_N = {kN:.3f}"
          f"  | Thm 4.2' extra rows: max(c.h - bN) = {ext}  | gauche rows: max(c.h - bN - gmin) = {gau}")
    return worst


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    own = {}
    for N in range(4, nmax + 1):
        own[N] = classes_own(N)
        check(N, own[N], "own enumeration")
    if len(sys.argv) > 2:
        d = sys.argv[2]
        for n in range(1, 25):
            p = os.path.join(d, f"dia_Sc12_n{n}.txt")
            if not os.path.exists(p):
                continue
            cl = classes_file(p)
            N = n + 3
            if N in own:
                assert cl == own[N], f"class table differs at N={N}"
            check(N, cl, "other division's table" + (" = own" if N in own else ""))
    print("PART 1 OK")


if __name__ == "__main__":
    main()
