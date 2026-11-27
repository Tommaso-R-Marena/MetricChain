#!/usr/bin/env python3
"""G1 check (workstream S).  Independent enumeration of self-avoiding diamond-lattice chains.

For every conformation with n torsions (N = n+3 beads; first two bonds fixed by symmetry) compute
  (A) the profile by its definition: pairs (p,q), q-p >= 3, squared distance in {3,8,11}  (O(N^2) loop),
      and the gauche count from the torsion states (bond-index rule: torsion j trans iff i_{j+2} = i_j);
  (B) the profile from the SITE SET only: e_d(S) = number of unordered pairs of occupied sites at squared
      distance d, h3 = e3-(N-1), h8 = e8-(N-2), h11 = e11, and the gauche count as #{i : |x_{i+3}-x_i|^2 = 11}.
Assert (A) == (B) for every conformation, build the class table (count, gmin, count_gmin, gmax) and compare
it line by line with the class table of the other division (path given on the command line).

usage: g1_check.py NMAX DATA_DIR
"""
import sys, itertools, collections

A = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]

def walks(n):
    """yield bead lists of all self-avoiding chains with n torsions, bonds 0,1 fixed to +a0, -a1."""
    N = n + 3
    pos = [(0, 0, 0), A[0], (A[0][0] - A[1][0], A[0][1] - A[1][1], A[0][2] - A[1][2])]
    idx = [0, 1]
    occ = set(pos)
    def rec():
        m = len(idx)            # index of the bond to be added
        if len(pos) == N:
            yield list(pos), list(idx)
            return
        sgn = 1 if m % 2 == 0 else -1
        x, y, z = pos[-1]
        for i in range(4):
            if i == idx[-1]:
                continue
            p = (x + sgn * A[i][0], y + sgn * A[i][1], z + sgn * A[i][2])
            if p in occ:
                continue
            occ.add(p); pos.append(p); idx.append(i)
            yield from rec()
            occ.discard(p); pos.pop(); idx.pop()
    yield from rec()

def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2

# displacement tables for the site-set count: all integer vectors with squared length 3, 8, 11
DISP = {d: [v for v in itertools.product(range(-3, 4), repeat=3) if sum(c * c for c in v) == d] for d in (3, 8, 11)}

def main():
    nmax = int(sys.argv[1]); data = sys.argv[2]
    for n in range(1, nmax + 1):
        N = n + 3
        table = {}
        nconf = 0
        for pos, idx in walks(n):
            nconf += 1
            # (A) definition
            hA = [0, 0, 0]
            for p in range(N):
                for q in range(p + 3, N):
                    s = d2(pos[p], pos[q])
                    if s == 3: hA[0] += 1
                    elif s == 8: hA[1] += 1
                    elif s == 11: hA[2] += 1
                    assert s not in (1, 2, 4, 5, 6, 7, 9, 10), "non-lattice distance"
            gA = sum(1 for j in range(n) if idx[j + 2] != idx[j])
            # chain neighbours: separation 1 -> 3, separation 2 -> 8, separation 3 -> 11 (gauche) or 19 (trans)
            assert all(d2(pos[p], pos[p + 1]) == 3 for p in range(N - 1))
            assert all(d2(pos[p], pos[p + 2]) == 8 for p in range(N - 2))
            assert all(d2(pos[p], pos[p + 3]) in (11, 19) for p in range(N - 3))
            # (B) site set only
            S = set(pos)
            e = {}
            for d in (3, 8, 11):
                c = 0
                for (x, y, z) in S:
                    for (a, b, cc) in DISP[d]:
                        if (x + a, y + b, z + cc) in S:
                            c += 1
                e[d] = c // 2
            hB = [e[3] - (N - 1), e[8] - (N - 2), e[11]]
            gB = sum(1 for i in range(N - 3) if d2(pos[i], pos[i + 3]) == 11)
            assert hA == hB and gA == gB, (pos, hA, hB, gA, gB)
            key = tuple(hA)
            t = table.get(key)
            if t is None:
                table[key] = [1, gA, 1, gA]
            else:
                t[0] += 1
                if gA < t[1]: t[1] = gA; t[2] = 1
                elif gA == t[1]: t[2] += 1
                if gA > t[3]: t[3] = gA
        # compare with the other division's class table
        ref = {}
        with open(f"{data}/dia_Sc12_n{n}.txt") as f:
            for line in f:
                if line.startswith('#'): continue
                a = list(map(int, line.split()))
                ref[tuple(a[:3])] = a[3:]
        same = (ref == {k: v for k, v in table.items()})
        print(f"n={n:2d} N={N:2d} conformations={nconf:8d} classes={len(table):4d}  (A)==(B) for all: yes   "
              f"class table identical to the other division's: {'yes' if same else 'NO'}")
        assert same

if __name__ == "__main__":
    main()
