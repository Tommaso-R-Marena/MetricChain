"""Survey (referee): outer-labeled planar NON-galled networks from random hybrid insertion.
How often does the conclusion of Theorem 4.7 fail, in which way, and what is the smallest number of leaves?"""
import random, sys
from collections import Counter
import rnet, gen, css
from t9c_family import build

net, order = build(1, 1, True)
print("N(1,1):", gen.check_fast(net, order)[:2])

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 77)
target = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
stats = Counter()
examples = {}
seen = set()
cnt = 0
bad6 = set()
while cnt < target:
    n = rng.choice([4, 5, 5, 6, 6, 6, 7, 7, 8]); k = rng.choice([2, 2, 2, 3, 3, 4])
    net = gen.grow(n, k, rng)
    if net is None:
        continue
    if rnet.is_galled_def(net):
        continue
    order = rnet.planar_circular_order(net)
    if order is None:
        continue
    key = tuple(sorted((v, tuple(sorted(ch))) for v, ch in net.items()))
    if key in seen:
        continue
    seen.add(key)
    cnt += 1
    f = gen.features(net)
    st, det, sigma, nn = gen.check_fast(net, order)
    cls = (f["n"], f["level"], "bloblet" if f["bloblet"] else "multi")
    stats[(cls, st)] += 1
    if st != "ok" and (f["n"], st) not in examples:
        examples[(f["n"], st)] = (net, order, det, f)
    if st != "ok" and f["n"] == 6:
        bad6.add(css.dihedral_canon(6, frozenset(sigma)))
print("non-galled outer-labeled planar networks tested:", cnt)
agg = Counter()
for (cls, st), c in sorted(stats.items()):
    agg[(cls[0], st)] += c
print("by (leaves, status):", dict(sorted(agg.items())))
lv2 = Counter()
for (cls, st), c in stats.items():
    if cls[1] == 2:
        lv2[(cls[0], cls[2], st)] += c
print("level-2 only, by (leaves, bloblet?, status):", dict(sorted(lv2.items())))
for k in sorted(examples):
    net, order, det, f = examples[k]
    print("example", k, f, "\n    order", order, "\n    detail", {kk: str(v) for kk, v in det.items()}, "\n    net", net)
print("distinct 6-leaf failing systems (dihedral classes):", len(bad6))
