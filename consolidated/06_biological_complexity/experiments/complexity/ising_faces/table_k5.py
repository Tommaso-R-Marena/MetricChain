"""Table for K = 5: orbits of sets T of column types in {+,-}^4 (first state normalised to all +) under the
symmetry group (permutations and global sign changes of the five states; order 1920), with the exact decision
for one representative per orbit.   usage: python3 table_k5.py [max_types]"""
import itertools, sys, time
from collections import Counter
import numpy as np
from faces import decide

K = 5
TYPES = [(1,) + t for t in itertools.product((1, -1), repeat=K - 1)]
NT = len(TYPES)


def symmetries():
    out = set()
    for perm in itertools.permutations(range(K)):
        for signs in itertools.product((1, -1), repeat=K):
            img = []
            for t in TYPES:
                col = tuple(signs[k] * t[perm[k]] for k in range(K))
                if col[0] < 0:
                    col = tuple(-c for c in col)
                img.append(TYPES.index(col))
            out.add(tuple(img))
    return sorted(out)


def products_constant(T):
    """list of the subsets of states (size 4, as index tuples) whose componentwise product is constant on T."""
    out = []
    for r in (4,):
        for S in itertools.combinations(range(K), r):
            vals = {int(np.prod([TYPES[i][k] for k in S])) for i in T}
            if len(vals) == 1:
                out.append(S)
    return out


if __name__ == "__main__":
    maxm = int(sys.argv[1]) if len(sys.argv) > 1 else NT
    G = symmetries()
    print(f"group order {len(G)}", flush=True)
    seen = bytearray(1 << NT)
    reps = []
    for mask in range(1, 1 << NT):
        if seen[mask]:
            continue
        T = [i for i in range(NT) if (mask >> i) & 1]
        orb = set()
        for g in G:
            m2 = 0
            for i in T:
                m2 |= 1 << g[i]
            orb.add(m2)
        for o in orb:
            seen[o] = 1
        reps.append((len(T), mask, len(orb)))
    reps.sort()
    print(f"{len(reps)} orbits of non-empty type sets", flush=True)
    tot = Counter()
    rows = []
    t0 = time.time()
    for m, mask, size in reps:
        if m > maxm:
            continue
        T = [i for i in range(NT) if (mask >> i) & 1]
        status, cert = decide([TYPES[i] for i in T])
        pc = products_constant(T) if status != "degenerate" else []
        tot[status] += size
        rows.append((m, mask, size, status, len(pc)))
        print(f"   m={m:2d} orbit size {size:4d} mask {mask:5d}: {status:10s} #4-subsets with constant product: {len(pc)}"
              f"   [{time.time()-t0:.0f}s]", flush=True)
    print("totals over type sets:", dict(tot))
    bad = [r for r in rows if r[3] == "no" and r[4] == 0]
    good = [r for r in rows if r[3] == "yes" and r[4] > 0]
    print("non-exposed orbits WITHOUT a 4-subset of constant product:", len(bad), [(r[0], r[1]) for r in bad][:20])
    print("exposed orbits WITH a 4-subset of constant product:", len(good), [(r[0], r[1]) for r in good][:20])
