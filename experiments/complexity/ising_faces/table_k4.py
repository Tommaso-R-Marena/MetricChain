"""Complete table for K = 4: for every non-empty set T of column types in {+,-}^3 (the first state is
normalised to all +, the types are the triples (a_i, b_i, c_i)), are the four states 1, a, b, c exactly the
ground states of some Ising pair energy on a system whose set of column types is T?
Types are numbered 0..7 by the bits (a = -, b = -, c = -)."""
import itertools, sys
from collections import Counter, defaultdict
from faces import decide

TYPES = [(1,) + t for t in itertools.product((1, -1), repeat=3)]       # index = bits of (a,b,c)


def symmetries():
    """the group acting on type sets: permutations of the four states and global sign changes of states."""
    out = set()
    for perm in itertools.permutations(range(4)):
        for signs in itertools.product((1, -1), repeat=4):
            img = []
            for t in TYPES:
                col = tuple(signs[k] * t[perm[k]] for k in range(4))
                if col[0] < 0:
                    col = tuple(-c for c in col)
                img.append(TYPES.index(col))
            out.add(tuple(img))
    return sorted(out)


def rank(types):
    import numpy as np
    return int(np.linalg.matrix_rank(np.array(types, dtype=float)))


if __name__ == "__main__":
    G = symmetries()
    seen = {}
    orbits = []
    results = Counter()
    for r in range(1, 9):
        for T in itertools.combinations(range(8), r):
            if T in seen:
                continue
            orb = {tuple(sorted(g[i] for i in T)) for g in G}
            status, cert = decide([TYPES[i] for i in T])
            for o in orb:
                seen[o] = status
            orbits.append((T, len(orb), status, rank([TYPES[i] for i in T])))
    # independent pass: decide every one of the 255 sets directly and compare with the orbit value
    for r in range(1, 9):
        for T in itertools.combinations(range(8), r):
            status, cert = decide([TYPES[i] for i in T])
            assert status == seen[T], (T, status, seen[T])
            results[status] += 1
    print(f"symmetry group order {len(G)}; {len(orbits)} orbits of non-empty type sets; all 255 sets decided directly")
    print("totals:", dict(results))
    name = lambda i: "".join("+" if s > 0 else "-" for s in TYPES[i][1:])
    print("| types present (a b c) | #types | orbit size | rank of the columns | exposed? |")
    print("|---|---|---|---|---|")
    for T, size, status, rk in orbits:
        print(f"| {' '.join(name(i) for i in T)} | {len(T)} | {size} | {rk} | {status} |")
