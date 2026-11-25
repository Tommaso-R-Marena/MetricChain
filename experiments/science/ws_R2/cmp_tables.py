#!/usr/bin/env python3
"""R2: compare my class tables (out/walk_N{N}.txt) with the engineering division's
(eng_ro/experiments/eng/chain_cover/data/dia_Sc12_n{n}.txt), row by row.
usage: cmp_tables.py Nmin Nmax
"""
import sys, os
ENG = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro/experiments/eng/chain_cover/data"
HERE = os.path.dirname(os.path.abspath(__file__))
def load_mine(N):
    d = {}
    for line in open(f"{HERE}/out/walk_N{N}.txt"):
        f = line.split()
        d[tuple(map(int, f[:3]))] = tuple(map(int, f[3:7]))
    return d
def load_eng(n):
    d = {}; tot = None
    for line in open(f"{ENG}/dia_Sc12_n{n}.txt"):
        if line.startswith("#"):
            if "conformations=" in line:
                tot = int(line.split("conformations=")[1].split()[0])
            continue
        f = list(map(int, line.split()))
        d[tuple(f[:3])] = tuple(f[3:7])
    return d, tot
if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for N in range(lo, hi + 1):
        if not os.path.exists(f"{HERE}/out/walk_N{N}.txt"):
            continue
        mine = load_mine(N); eng, tot = load_eng(N - 3)
        same = (mine == eng)
        print(f"N={N} n={N-3}: my classes={len(mine)} eng classes={len(eng)} my total={sum(v[0] for v in mine.values())} eng total={tot} identical(count,gmin,count_gmin,gmax)={same}")
        if not same:
            for k in sorted(set(mine) | set(eng)):
                if mine.get(k) != eng.get(k):
                    print("   DIFF", k, mine.get(k), eng.get(k))
