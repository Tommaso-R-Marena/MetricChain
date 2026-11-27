"""Diamond-lattice chains: an independent enumerator (science division, PI thread).

Model (as in theory report §11.17 / engineering `dia_enum`): beads on the diamond lattice,
bond vectors (±1,±1,±1) with an even number of minus signs on one sublattice and their
negatives on the other; a chain with n torsions has N = n + 3 beads; the first two bonds are
fixed, every later bond is one of the three that do not reverse the previous one; the walk
is self-avoiding.  Torsion state: trans if bond k+2 equals bond k (as a vector), gauche
otherwise.  Squared distances are in units where a bond has squared length 3.

For every self-avoiding conformation we record
  hist[s]   number of bead pairs (i < j, j - i >= 3) at squared distance s, all s
  gauche    number of gauche torsions
  rg2       sum over all pairs i<j of squared distance (so that Rg^2 = rg2 / N^2)
  ree2      squared end-to-end distance
  d2[i,j]   optional: selected individual pair distances
Written for clarity, not speed: plain DFS with incremental pair bookkeeping.
"""
from __future__ import annotations
import sys, itertools
import os
import numpy as np

A_BONDS = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]

def enumerate_chain(n_torsions: int, track_pairs=()):
    """Return dict of arrays, one row per self-avoiding conformation (first two bonds fixed)."""
    N = n_torsions + 3
    pos = [(0, 0, 0)]
    b0 = A_BONDS[0]
    pos.append(tuple(pos[0][k] + b0[k] for k in range(3)))
    b1 = tuple(-v for v in A_BONDS[1])                 # from sublattice B: negatives of A bonds
    pos.append(tuple(pos[1][k] + b1[k] for k in range(3)))
    bonds = [b0, b1]
    occupied = {pos[0]: 0, pos[1]: 1, pos[2]: 2}
    rows_hist = []; rows_g = []; rows_rg2 = []; rows_ree2 = []; rows_pairs = []; rows_pat = []
    maxs = 3 * (N - 1) ** 2 + 1

    # incremental bookkeeping: when bead j is appended, add its pairs with beads 0..j-1
    hist = {}
    state = {"rg2": 0, "g": 0}
    # pairs among the first three beads
    def d2(a, b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2
    base_rg2 = d2(pos[0], pos[1]) + d2(pos[0], pos[2]) + d2(pos[1], pos[2])

    out_hist = []; pat = []

    def rec(j, rg2, g, hist):
        # j = index of the next bead to place (j >= 3)
        if j == N:
            rows_hist.append(dict(hist)); rows_g.append(g); rows_rg2.append(rg2)
            rows_ree2.append(d2(pos[0], pos[-1]))
            rows_pairs.append([d2(pos[a], pos[b]) for (a, b) in track_pairs])
            rows_pat.append(tuple(pat))
            return
        prev = bonds[-1]; prev2 = bonds[-2]
        sign = 1 if (j - 1) % 2 == 0 else -1          # bead j-1 on sublattice A (even) or B (odd)
        for a in A_BONDS:
            b = (sign * a[0], sign * a[1], sign * a[2])
            if b[0] == -prev[0] and b[1] == -prev[1] and b[2] == -prev[2]:
                continue                               # no immediate reversal
            p = (pos[-1][0] + b[0], pos[-1][1] + b[1], pos[-1][2] + b[2])
            if p in occupied:
                continue
            is_trans = (b == prev2)
            add = 0; touched = []
            for i in range(j):
                s = d2(pos[i], p)
                add += s
                if j - i >= 3:
                    hist[s] = hist.get(s, 0) + 1; touched.append(s)
            pos.append(p); bonds.append(b); occupied[p] = j; pat.append(0 if is_trans else 1)
            rec(j + 1, rg2 + add, g + (0 if is_trans else 1), hist)
            pat.pop(); del occupied[p]; bonds.pop(); pos.pop()
            for s in touched:
                hist[s] -= 1
                if hist[s] == 0:
                    del hist[s]

    rec(3, base_rg2, 0, {})
    svals = sorted({s for h in rows_hist for s in h})
    H = np.zeros((len(rows_hist), len(svals)), dtype=np.int32)
    col = {s: k for k, s in enumerate(svals)}
    for r, h in enumerate(rows_hist):
        for s, c in h.items():
            H[r, col[s]] = c
    return {"n_torsions": n_torsions, "N": N, "svals": np.array(svals), "hist": H,
            "gauche": np.array(rows_g, dtype=np.int32), "rg2": np.array(rows_rg2, dtype=np.int64),
            "ree2": np.array(rows_ree2, dtype=np.int64),
            "pairs": np.array(rows_pairs, dtype=np.int64).reshape(len(rows_g), len(track_pairs)),
            "pattern": np.array(rows_pat, dtype=np.int8)}

def short_profile(data, shells=(3, 8, 11)):
    """pair counts at the given squared distances (the engineering division's three shells)."""
    sv = list(data["svals"])
    cols = [data["hist"][:, sv.index(s)] if s in sv else np.zeros(len(data["gauche"]), dtype=np.int32)
            for s in shells]
    return np.stack(cols, axis=1)

def load_eng_table(path):
    rows = []
    meta = {}
    for line in open(path):
        if line.startswith("#"):
            if "conformations=" in line:
                for tok in line[1:].split():
                    k, v = tok.split("="); meta[k] = int(v)
            continue
        rows.append([int(v) for v in line.split()])
    return meta, np.array(rows, dtype=np.int64)

if __name__ == "__main__":
    ENG = os.environ.get("MC_ENG_DATA", "eng_ro/experiments/eng/chain_cover/data")   # see experiments/science/README.md
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    for n in range(1, nmax + 1):
        d = enumerate_chain(n)
        prof = short_profile(d)
        g = d["gauche"]
        # class table: profile -> (count, gmin, count_gmin, gmax)
        table = {}
        for p, gg in zip(map(tuple, prof), g):
            c = table.get(p)
            if c is None:
                table[p] = [1, gg, 1, gg]
            else:
                c[0] += 1
                if gg < c[1]: c[1] = gg; c[2] = 1
                elif gg == c[1]: c[2] += 1
                if gg > c[3]: c[3] = gg
        meta, eng = load_eng_table(f"{ENG}/dia_Sc12_n{n}.txt")
        eng_table = {tuple(r[:3]): list(r[3:]) for r in eng}
        same = (table == {k: [int(x) for x in v] for k, v in eng_table.items()})
        print(f"n={n:2d} N={n+3:2d}: conformations {len(g):8d} (eng {meta['conformations']:8d}), "
              f"classes {len(table):5d} (eng {meta['classes']:5d}), full table identical: {same}")
