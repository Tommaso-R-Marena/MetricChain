"""summary table of the networks tested in Task 3(b)"""
import pickle, sys
from collections import Counter
import rnet
tab = Counter(); tot = 0; status = Counter(); par = 0; maxblob = Counter(); keys = set()
lvl_multi = Counter()
for fn in sys.argv[1:]:
    for net, order, f, st in pickle.load(open(fn, "rb")):
        key = tuple(sorted((v, tuple(sorted(ch))) for v, ch in net.items()))
        if key in keys:
            continue
        keys.add(key)
        tot += 1
        status[st] += 1
        lv = f["level"]
        tab[(f["n"], min(lv, 6))] += 1
        lvl_multi[(min(lv, 6), "bloblet" if f["bloblet"] else ("1 blob + cut edges" if f["nblobs"] == 1 else "multi-blob"),
                   "nonleaf-child" if f["nonleaf_hyb_children"] else "leaf-children")] += 1
        root = rnet.classify(net)[0]
        hyb = set(rnet.classify(net)[2])
        if any(c in hyb for c in net[root]):
            par += 1
print("distinct networks:", tot, "status:", dict(status))
print("leaves x level (level 6 = 6 or 7):")
for n in range(6, 11):
    print("   n=%d:" % n, {l: tab[(n, l)] for l in range(1, 7)})
print("level x structure x hybrid children:")
for k in sorted(lvl_multi):
    print("   ", k, lvl_multi[k])
print("networks whose root has a hybrid child (hybrid edge through the suppressed root):", par)
