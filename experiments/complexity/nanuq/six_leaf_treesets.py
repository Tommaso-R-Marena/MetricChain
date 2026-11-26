"""Exploration for the open question of docs/complexity/NANUQ_HIGHER_LEVELS.md, section 2.3: which SETS OF DISPLAYED
TREES (not only which split systems) do six-leaf outer-labeled planar networks have?

Same generator as six_leaf_survey.py (rooted labelled networks, hybrid insertion, planarity for the order 0..5).
Result of `python3 six_leaf_treesets.py 2` (50 s): 14 / 71 / 245 distinct tree sets with at most 0 / 1 / 2 hybrid nodes
(1 tree: 14; 2 trees: 57 of the 91 pairs; 3 trees: 78; 4 trees: 96).  Three hybrid nodes take about half an hour.
An exploration, not a result: nothing in the notes depends on it.

Usage: python3 six_leaf_treesets.py [max number of hybrid nodes]     (default 2)
"""
import sys, itertools, time
ARGS = sys.argv[1:]; sys.argv = [sys.argv[0]]          # six_leaf_survey reads sys.argv when imported as a script only
import six_leaf_survey as S

N, FULL, INTERVALS = S.N, S.FULL, S.INTERVALS

def treeset_of(net, root, par):
    hyb = [v for v in net if len(par[v]) == 2]
    order = S.topo(net, root)
    leafbit = {f"L{q}": 1 << q for q in range(N)}
    trees = set()
    for choice in itertools.product((0, 1), repeat=len(hyb)):
        keep = {h: par[h][c] for h, c in zip(hyb, choice)}
        mask, tr = {}, set()
        for v in order:
            if v in leafbit:
                mask[v] = leafbit[v]; continue
            m = 0
            for c in net[v]:
                if c in keep and keep[c] != v:
                    continue
                m |= mask[c]
            mask[v] = m
            if m and m != FULL:
                co = FULL ^ m
                if (m & (m - 1)) and (co & (co - 1)):
                    if m not in INTERVALS:
                        return None
                    tr.add(min(m, co))
        trees.add(frozenset(tr))
    return frozenset(trees)

def main(kmax):
    t0 = time.time()
    level = {}
    for net, root in S.planar_trees():
        par = S.parents(net)
        level[S.unfolding_key(net, root, par)] = (net, root)
    counter = [0]
    seen = {}
    for key, (net, root) in level.items():
        ts = treeset_of(net, root, S.parents(net))
        seen.setdefault(ts, 0)
    print(f"k=0: {len(level)} networks, distinct tree sets so far {len(seen)}", flush=True)
    for k in range(1, kmax + 1):
        nxt, keys = {}, set()
        for key, (net, root) in level.items():
            for new in S.insertions(net, root, counter):
                par = S.parents(new)
                ts = treeset_of(new, root, par)
                if ts is None:
                    continue
                ukey = S.unfolding_key(new, root, par)
                if ukey in keys:
                    continue
                if not S.planar_with_order(new):
                    continue
                keys.add(ukey)
                seen.setdefault(ts, k)
                if k < kmax:
                    nxt[ukey] = (new, root)
        level = nxt
        sizes = {}
        for ts in seen:
            sizes[len(ts)] = sizes.get(len(ts), 0) + 1
        print(f"k={k}: {len(keys)} networks, distinct tree sets so far {len(seen)}; by number of trees {dict(sorted(sizes.items()))}  [{time.time()-t0:.0f}s]", flush=True)
    return seen

main(int(ARGS[0]) if ARGS else 2)
