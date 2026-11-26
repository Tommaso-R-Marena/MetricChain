import sys, time
from splitsys import *
from multiblob import *

def run(n, maxblob=None):
    if maxblob is None:
        maxblob = n
    t0 = time.time()
    systems = network_systems(n, maxblob)
    counts = {"invalid": 0, "ok": 0, "neg": 0, "support": 0}
    bad = []
    for s in systems:
        st, det = check(n, set(s))
        counts[st] += 1
        if st != "ok" and len(bad) < 5:
            bad.append((sorted(all_circular_splits(n)[m] for m in s if not is_trivial(n, m)), st, det))
    print(f"n={n} maxblob={maxblob}: distinct displayed split systems of networks in N: {len(systems)}  {counts} [{time.time()-t0:.1f}s]", flush=True)
    for b in bad:
        print("   FAIL", b)

if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        run(n)
