# c4_collisions_all.py -- REVIEW 6: for ALL networks with three hybrid nodes of the re-enumeration (up to rotation
# and reflection), record per (KEY, INV) the split system and the set of displayed trees, and compare them among the
# networks that share a KEY (i.e. that the survey of the note identifies).
# Usage: python3 c4_collisions_all.py r M   (chunk)   |   python3 c4_collisions_all.py merge M
import sys, pickle, time, itertools
from c1_survey import (N, FULL, DIH, parents, topo_children_first, keys_of, inv_of, system_of, wheel_planar, insertions, image_system)


def tree_sets(net, root, order, par, g):
    hyb = [v for v in net if len(par[v]) == 2]
    out = set()
    for choice in itertools.product((0, 1), repeat=len(hyb)):
        keep = {h: par[h][c] for h, c in zip(hyb, choice)}
        mask, spl = {}, set()
        for v in order:
            ch = net[v]
            if not ch:
                mask[v] = 1 << g[v]
                continue
            m = 0
            for c in ch:
                if c in keep and keep[c] != v:
                    continue
                m |= mask[c]
            mask[v] = m
            if m and m != FULL:
                co = FULL ^ m
                if (m & (m - 1)) and (co & (co - 1)):
                    spl.add(min(m, co))
        out.add(frozenset(spl))
    return frozenset(out)


if sys.argv[1] == "merge":
    M = int(sys.argv[2])
    allk = {}
    for r in range(M):
        part = pickle.load(open(f"coll_{r}_{M}.pkl", "rb"))
        for k, d in part.items():
            allk.setdefault(k, {}).update(d)
    multi = {k: d for k, d in allk.items() if len(d) > 1}
    ninv = sum(len(d) for d in allk.values())
    diff_trees = sum(1 for d in multi.values() if len(set(d.values())) > 1)
    sizes = {}
    for d in multi.values():
        sizes[len(d)] = sizes.get(len(d), 0) + 1
    print(f"k=3 up to rotation/reflection: KEYs {len(allk)}, (KEY,INV) classes {ninv}; KEYs with several INVs {len(multi)} "
          f"(number of INVs per such KEY: {dict(sorted(sizes.items()))}); "
          f"of these, KEYs whose networks do NOT all have the same set of displayed trees: {diff_trees}")
else:
    r, M = int(sys.argv[1]), int(sys.argv[2])
    prev = pickle.load(open("level_2.pkl", "rb"))
    out = {}
    nonplanar = set()
    for idx, (key, (net, root, _, _, _)) in enumerate(sorted(prev.items())):
        if idx % M != r:
            continue
        order0 = topo_children_first(net, root)
        for new in insertions(net, root, order0):
            order = topo_children_first(new, root)
            par = parents(new)
            ks = [keys_of(new, root, order, g)[root] for g in DIH]
            kmin = min(ks)
            cands = [(inv_of(new, root, order, par, g), g) for g, k in zip(DIH, ks) if k == kmin]
            iv, g = min(cands)
            if iv in nonplanar or (kmin in out and iv in out[kmin]):
                continue
            s = system_of(new, root, order, par)
            if s is None or not wheel_planar(new):
                nonplanar.add(iv)
                continue
            # displayed tree sets in the canonical relabelling; if several g give the same (key, inv) take the minimum
            ts = min((sorted(sorted(t) for t in tree_sets(new, root, order, par, gg)) for (ivv, gg) in cands if ivv == iv))
            out.setdefault(kmin, {})[iv] = repr(ts)
    pickle.dump(out, open(f"coll_{r}_{M}.pkl", "wb"))
    print("chunk", r, "done", len(out))
