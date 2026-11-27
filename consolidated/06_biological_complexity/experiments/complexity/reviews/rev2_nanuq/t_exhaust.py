"""Exhaustive small cases (referee): ALL rooted binary networks obtained from every rooted binary tree shape on
n leaves by at most k hybrid insertions (every target edge x every source edge at every step), keeping at each
step only galled (Def. 2.3(vi)) outer-labeled planar networks.  (Deleting a hybrid edge of a galled OLP network
gives a galled OLP network, so every galled OLP network with a simple rooted partner and <= k hybrids on n
leaves is reached, up to relabelling of leaves.)
usage: python3 t_exhaust.py n k"""
import sys, time
from collections import Counter
import rnet, gen

def shapes(n):
    """all rooted binary tree shapes with n leaves as nested tuples"""
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

def canon_key(net):
    """isomorphism-invariant-ish key: not canonical, just exact identity after sorting"""
    return tuple(sorted((v, tuple(sorted(ch))) for v, ch in net.items()))

n, kmax = int(sys.argv[1]), int(sys.argv[2])
t0 = time.time()
stats = Counter()
cache = {}
fails = []
frontier = [to_net(s) for s in shapes(n)]
print(f"n={n}: {len(frontier)} tree shapes", flush=True)
for k in range(1, kmax + 1):
    new = []
    seen_struct = set()
    for net in frontier:
        E = gen.all_edges(net)
        for tgt in E:
            for src in E:
                cand = gen.insert_hybrid(net, tgt, src, k)
                if cand is None:
                    continue
                stats[(k, "inserted")] += 1
                if not rnet.is_galled_def(cand):
                    continue
                order = rnet.planar_circular_order(cand)
                if order is None:
                    continue
                assert rnet.is_galled_articulation(cand)
                stats[(k, "galled OLP")] += 1
                st, det, sigma, nn = gen.check_fast(cand, order)
                stats[(k, st)] += 1
                f = gen.features(cand)
                stats[(k, "level", f["level"])] += 1
                if st != "ok":
                    fails.append((cand, order, det))
                    print("FAILURE", cand, order, det, flush=True)
                new.append(cand)
    frontier = new
    print(f"   after {k} insertion(s): {dict((kk, v) for kk, v in sorted(stats.items(), key=str) if kk[0] == k)}  [{time.time()-t0:.0f}s]", flush=True)
print("failures:", len(fails))
