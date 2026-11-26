"""Exhaustive check of the 3-PARTITION / bin-packing reduction to multi-strand NN MFE on tiny instances.

Instance: template  G^B (A G^B)^(m-1)  and item strands C^{a_i}, sum a_i = m*B.
Energy models tested (all of NN type, exterior loops = 0):
   'stack'  : every stack -1, every other nick-free loop 0
   'random' : every stack -sigma (sigma>0 integer), every bulge/interior/multi loop a random non-negative
              integer depending on the loop's shape
Claim: min over connected unpseudoknotted structures of the loop energy equals -sigma*M, M = sum (a_i - 1),
iff the items can be packed perfectly into the m blocks; otherwise it is >= -sigma*(M-1).
Also reports the number of labelled structures attaining -sigma*M and compares it with the number of
ordered perfect packings (labelled items)."""
import sys, random, itertools, time
from ref_enum import *

def count_labelled_tilings(items, m, B):
    """number of ways to arrange the labelled items into m ordered blocks, each block an ordered sequence of
    items with total length exactly B."""
    n = len(items)
    cnt = 0
    for perm in itertools.permutations(range(n)):
        # cut the permutation greedily into blocks of sum exactly B
        tot = 0; ok = True; blocks = 0
        for i in perm:
            tot += items[i]
            if tot == B:
                blocks += 1; tot = 0
            elif tot > B:
                ok = False; break
        if ok and tot == 0 and blocks == m:
            cnt += 1
    return cnt

def run(items, m, B, model="stack", seed=0, sigma=1):
    rng = random.Random(seed)
    cache = {}
    def loop_energy(kind, face, seq):
        if kind == "exterior":
            return 0
        if kind == "stack":
            return -sigma
        if kind == "hairpin":
            raise AssertionError("hairpin impossible in this instance")
        if model == "stack":
            return 0
        key = (kind, tuple(face["segs"]))
        if key not in cache:
            cache[key] = rng.randint(0, 3)
        return cache[key]
    template = "A".join(["G" * B] * m)
    strands = [template] + ["C" * a for a in items]
    M = sum(a - 1 for a in items)
    t0 = time.time()
    best = None; nbest = 0; total = 0
    seen = set()
    for order, lab, e, kinds in enumerate_structures(strands, loop_energy, connected_only=True):
        total += 1
        assert lab not in seen   # each labelled connected structure occurs under exactly one ordering
        seen.add(lab)
        if best is None or e < best:
            best, nbest = e, 1
        elif e == best:
            nbest += 1
    til = count_labelled_tilings(items, m, B)
    feasible = til > 0
    ok = (best == -sigma * M) == feasible and (feasible or best >= -sigma * (M - 1)) and (not feasible or nbest == til)
    print(f"items={items} m={m} B={B} model={model} sigma={sigma}: connected structures={total} "
          f"MFE={best} target={-sigma*M} #MFE-structures={nbest} labelled tilings={til} "
          f"{'OK' if ok else 'MISMATCH'} [{time.time()-t0:.1f}s]", flush=True)
    return ok

if __name__ == "__main__":
    allok = True
    cases = [([1, 2, 1, 2], 2, 3), ([2, 2, 2], 2, 3), ([3, 1, 1, 1], 2, 3), ([3, 3], 2, 3), ([1, 1, 1, 3], 2, 3),
             ([2, 2, 1, 1], 2, 3)]
    for items, m, B in cases:
        allok &= run(items, m, B, "stack")
        allok &= run(items, m, B, "random", seed=1, sigma=2)
    print("ALL OK" if allok else "SOME MISMATCH")
