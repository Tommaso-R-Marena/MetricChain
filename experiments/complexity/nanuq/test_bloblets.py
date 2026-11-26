import sys, time
from splitsys import *
from networks import *

def run(n, k, maxshow=3):
    t0 = time.time()
    cache = {}
    counts = {"invalid": 0, "ok": 0, "neg": 0, "support": 0}
    nnet = 0
    shown = 0
    for N, t, pairs, sigma, per_tree, leafmap in gen_bloblets(n, k):
        nnet += 1
        if sigma not in cache:
            cache[sigma] = check(n, set(sigma))
        st, det = cache[sigma]
        counts[st] += 1
        if st != "ok" and shown < maxshow:
            shown += 1
            hyb = sorted(leafmap[p] for p in pairs)
            print("   FAIL", st, "tree", t, "pairs", pairs, "hybrid leaves", hyb, "detail", det,
                  "nontrivial splits", sorted(all_circular_splits(n)[m] for m in sigma if not is_trivial(n, m)))
    print(f"n={n} k={k}: networks={nnet} distinct split systems={len(cache)} {counts}  [{time.time()-t0:.1f}s]", flush=True)

if __name__ == "__main__":
    k = int(sys.argv[1])
    for n in map(int, sys.argv[2:]):
        run(n, k)
