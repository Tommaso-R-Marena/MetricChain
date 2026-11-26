"""Exhaustive (referee): ALL outer-labeled planar rooted binary networks with exactly two hybrid nodes on n
leaves (every tree shape, every pair of insertions; planarity is hereditary under deleting a hybrid edge, so
filtering by planarity after each insertion loses nothing).  Which of them violate the conclusion of
Theorem 4.7 / Theorem 7, and are the violators all non-galled?
usage: python3 t_exhaust_ng.py n"""
import sys, time
from collections import Counter
import rnet, gen

def shapes(n):
    if n == 1:
        return ["L"]
    out = []
    for a in range(1, n // 2 + 1):
        b = n - a
        for s in shapes(a):
            for t in shapes(b):
                if a == b and repr(s) > repr(t):
                    continue
                out.append((s, t))
    return out

def to_net(shape):
    net = {}
    cnt = [0, 0]
    def rec(s):
        if s == "L":
            name = f"L{cnt[0]}"; cnt[0] += 1
            net[name] = []
            return name
        name = f"t{cnt[1]}"; cnt[1] += 1
        a, b = rec(s[0]), rec(s[1])
        net[name] = [a, b]
        return name
    rec(shape)
    return net

n = int(sys.argv[1])
t0 = time.time()
stats = Counter()
ex = {}
frontier = []
for s in shapes(n):
    net = to_net(s)
    E = gen.all_edges(net)
    for tgt in E:
        for src in E:
            c = gen.insert_hybrid(net, tgt, src, 1)
            if c is not None and rnet.planar_circular_order(c) is not None:
                frontier.append(c)
print(f"n={n}: one-hybrid OLP networks (with repetitions): {len(frontier)}", flush=True)
for net in frontier:
    E = gen.all_edges(net)
    for tgt in E:
        for src in E:
            c = gen.insert_hybrid(net, tgt, src, 2)
            if c is None:
                continue
            order = rnet.planar_circular_order(c)
            if order is None:
                stats["non-planar"] += 1
                continue
            g = rnet.is_galled_def(c)
            st, det, sigma, nn = gen.check_fast(c, order)
            lv = rnet.level(c)
            bl = rnet.is_bloblet(c)
            stats[("galled" if g else "non-galled", f"level {lv}", st)] += 1
            if st != "ok":
                stats[("VIOLATION", "galled" if g else "non-galled", "bloblet" if bl else "not bloblet", st)] += 1
                ex.setdefault(("bloblet" if bl else "not bloblet", st), (c, order, det))
print(f"n={n}: two-hybrid networks examined (with repetitions) [{time.time()-t0:.0f}s]")
for k, v in sorted(stats.items(), key=str):
    print("   ", k, v)
for k, (c, order, det) in ex.items():
    print("example", k, order, {kk: str(v) for kk, v in det.items()}, c)
