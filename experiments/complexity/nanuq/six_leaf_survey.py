"""Which tree-generated circular split systems on SIX leaves are displayed by outer-labeled planar networks with
at most k hybrid nodes?   (docs/complexity/NANUQ_HIGHER_LEVELS.md)

Generation: all rooted binary trees on the leaves 0..5 that are planar for the circular order (0,1,...,5), then
repeated hybrid insertion (subdivide an edge a->b by a tree node p, an edge c->d by a hybrid node h, add p->h;
acyclic iff d is not an ancestor-or-equal of a).  A network is kept if every split of every displayed tree is
circular for (0..5) (necessary) and if the network is outer-labeled planar WITH THAT ORDER: the underlying graph
together with the hexagon through the leaves and an apex joined to all leaves is planar (the wheel has a unique
embedding and the connected network, attached to all six rim vertices, must lie in its hexagonal face).
Rooted labelled networks are identified by their unfolding (a complete invariant for binary networks with
distinct leaf labels; here it is only used to avoid repeated work).

For every network: the split system (union of the splits of the trees of all switchings).  Reported: for each
number of hybrid nodes, the systems that occur, by status
    'C6'            in the closure of the twin-tree class (the systems of galled networks, 108),
    'good'          6-locally good but not in C6 (19 systems),
    'pattern, ok'   contains the three 3-splits and misses a 2-split, metric still Kalmanson with exact support (14),
    'NEGATIVE'      a negative split weight at six leaves (3),
    'WRONG SUPPORT' Kalmanson, positive weight on an undisplayed split (6),
with one example network for every dihedral class that is not 6-locally good.

Usage:  python3 six_leaf_survey.py [max number of hybrid nodes [sym]]     (default 2; 3 takes half an hour)
With the second argument "sym" the networks are identified up to the twelve rotations and reflections of the leaf
labels (one representative per class is kept and extended; the systems of a class are the images of the system of
the representative), which makes four hybrid nodes feasible.
"""
import sys
import time
import itertools
import networkx as nx

from splitsys import canon as canon_split, nanuq_2d, alphas_2, split_mask, all_circular_splits, is_trivial
from localcrit import local_ok, dihedral_images, tree_generated_systems
from twin_trees import closure_systems

N = 6
FULL = (1 << N) - 1
INTERVALS = set()
for i in range(N):
    for ln in range(1, N):
        m = 0
        for t in range(ln):
            m |= 1 << ((i + t) % N)
        INTERVALS.add(m)


def planar_trees():
    """rooted binary trees (children dict) on leaves 0..5, planar for the circular order, all root positions"""
    out = []

    def build(lo, hi):                       # all rooted binary trees on the interval of leaves lo..hi-1 (linear order)
        if hi - lo == 1:
            return [lo]
        res = []
        for cut in range(lo + 1, hi):
            for l in build(lo, cut):
                for r in build(cut, hi):
                    res.append((l, r))
        return res

    seen = set()
    for rot in range(N):
        for t in build(0, N):
            # relabel leaves by rotation: leaf q -> (q + rot) % N
            def conv(x):
                return (x + rot) % N if isinstance(x, int) else tuple(sorted((conv(x[0]), conv(x[1])), key=str))
            tt = conv(t)
            if str(tt) in seen:
                continue
            seen.add(str(tt))
            out.append(tt)
    nets = []
    for t in out:
        net, cnt = {}, [0]

        def add(x):
            if isinstance(x, int):
                name = f"L{x}"
                net[name] = []
                return name
            cnt[0] += 1
            name = f"v{cnt[0]}"
            net[name] = [add(x[0]), add(x[1])]
            return name
        root = add(t)
        nets.append((net, root))
    return nets


DIHEDRAL = []
for _r in range(N):
    for _refl in (False, True):
        DIHEDRAL.append({f"L{q}": f"L{(((-q) % N if _refl else q) + _r) % N}" for q in range(N)})


def mask_image(m, ren):
    mm = 0
    for q in range(N):
        if (m >> q) & 1:
            mm |= 1 << int(ren[f"L{q}"][1:])
    return min(mm, FULL ^ mm)


def canonical_key(net, root, par):
    """smallest unfolding key over the twelve dihedral relabellings of the leaves"""
    return min(unfolding_key(net, root, par, ren) for ren in DIHEDRAL)


def unfolding_key(net, root, par, rename=None):
    memo = {}

    def key(v):
        if v in memo:
            return memo[v]
        ch = net[v]
        if not ch:
            r = v if rename is None else rename[v]
        elif len(ch) == 1:
            r = "[" + key(ch[0]) + "]"
        else:
            a, b = key(ch[0]), key(ch[1])
            r = "(" + (a + "," + b if a <= b else b + "," + a) + ")"
        memo[v] = r
        return r
    return key(root)


def parents(net):
    par = {v: [] for v in net}
    for v, ch in net.items():
        for c in ch:
            par[c].append(v)
    return par


def topo(net, root):
    order, seen = [], set()

    def dfs(v):
        if v in seen:
            return
        seen.add(v)
        for c in net[v]:
            dfs(c)
        order.append(v)
    dfs(root)
    return order                              # children before parents


def system_of(net, root, par):
    """set of canonical split masks over all switchings; None if some split is not circular"""
    hyb = [v for v in net if len(par[v]) == 2]
    order = topo(net, root)
    leafbit = {f"L{q}": 1 << q for q in range(N)}
    out = set()
    for choice in itertools.product((0, 1), repeat=len(hyb)):
        keep = {h: par[h][c] for h, c in zip(hyb, choice)}
        mask = {}
        for v in order:
            if v in leafbit:
                mask[v] = leafbit[v]
                continue
            m = 0
            for c in net[v]:
                if c in keep and keep[c] != v:
                    continue
                m |= mask[c]
            mask[v] = m
            if m and m != FULL:
                co = FULL ^ m
                if (m & (m - 1)) and (co & (co - 1)):          # non-trivial split
                    if m not in INTERVALS:
                        return None
                    out.add(min(m, co))
    return frozenset(out)


def planar_with_order(net):
    G = nx.Graph()
    for v, ch in net.items():
        for c in ch:
            G.add_edge(v, c)
    for q in range(N):
        G.add_edge(f"L{q}", f"L{(q + 1) % N}")
        G.add_edge("apex", f"L{q}")
    return nx.check_planarity(G)[0]


def descendants(net, root):
    desc = {}
    for v in topo(net, root):
        s = set()
        for c in net[v]:
            s.add(c)
            s |= desc[c]
        desc[v] = s
    return desc


def insertions(net, root, counter):
    edges = [(a, b) for a in net for b in net[a]]
    desc = descendants(net, root)
    for (a, b) in edges:
        for (c, d) in edges:
            if (a, b) == (c, d):
                continue
            if a == d or a in desc[d]:
                continue
            new = {v: list(ch) for v, ch in net.items()}
            counter[0] += 1
            p, h = f"p{counter[0]}", f"h{counter[0]}"
            # subdivide a->b by p (replace one occurrence), c->d by h
            i = new[a].index(b)
            new[a][i] = p
            new[p] = [b, h]
            j = new[c].index(d)
            new[c][j] = h
            new[h] = [d]
            yield new


def classify_systems():
    T6 = tree_generated_systems(6)
    C6 = set(frozenset(s) for s in closure_systems(6))
    info = {}
    for s in T6:
        nontriv = frozenset(m for m in s if not is_trivial(6, m))
        key = frozenset(min(m, FULL ^ m) for m in nontriv)
        D = nanuq_2d(6, set(s))
        al = alphas_2(6, D)
        neg = min(al.values()) < 0
        wrong = any((v > 0) != (canon_split(6, split_mask(6, i, j)) in s) for (i, j), v in al.items())
        good = local_ok(6, s)[0]
        if frozenset(s) in C6:
            st = "C6"
        elif good:
            st = "good"
        elif neg:
            st = "NEGATIVE"
        elif wrong:
            st = "WRONG SUPPORT"
        else:
            st = "pattern, ok"
        info[key] = (st, s)
    return info


def dihedral_class(key):
    """canonical representative of a system (set of min-masks) under rotations and reflections"""
    best = None
    for r in range(N):
        for refl in (False, True):
            img = set()
            for m in key:
                mm = 0
                for q in range(N):
                    if (m >> q) & 1:
                        t = (-q) % N if refl else q
                        mm |= 1 << ((t + r) % N)
                img.add(min(mm, FULL ^ mm))
            t = tuple(sorted(img))
            if best is None or t < best:
                best = t
    return best


def describe(net, root):
    return "; ".join(f"{v}: {', '.join(ch)}" for v, ch in net.items() if ch)


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    SYM = len(sys.argv) > 2 and sys.argv[2] == "sym"
    keyfun = canonical_key if SYM else unfolding_key
    t0 = time.time()
    info = classify_systems()
    counter = [0]
    level = {}
    for net, root in planar_trees():
        par = parents(net)
        level[keyfun(net, root, par)] = (net, root)
    print(f"rooted planar trees{' up to rotation and reflection' if SYM else ''}: {len(level)}", flush=True)
    seen_systems = {}
    examples = {}
    def record(net, root, par, k, stats):
        sysk = system_of(net, root, par)
        st, _ = info[sysk]
        stats[st] = stats.get(st, 0) + 1
        if SYM:
            for ren in DIHEDRAL:
                img = frozenset(mask_image(m, ren) for m in sysk)
                if img not in seen_systems:
                    seen_systems[img] = k
        if sysk not in seen_systems:
            seen_systems[sysk] = k
        if st not in ("C6", "good"):
            cls = dihedral_class(sysk)
            if (st, cls) not in examples:
                examples[(st, cls)] = (k, describe(net, root))

    def report(k, count, stats):
        by_status = {}
        for sysk, kk in seen_systems.items():
            st = info[sysk][0]
            by_status[st] = by_status.get(st, 0) + 1
        print(f"hybrid nodes = {k}: {count} rooted {'networks up to rotation and reflection' if SYM else 'labelled networks'}  {stats}   |  distinct systems so far, by "
              f"status: {dict(sorted(by_status.items()))}  (total {len(seen_systems)} of {len(info)})   "
              f"[{time.time() - t0:.0f}s]", flush=True)

    stats = {}
    for key, (net, root) in level.items():
        record(net, root, parents(net), 0, stats)
    report(0, len(level), stats)
    for k in range(1, kmax + 1):
        last = (k == kmax)
        nxt = {}
        keys = set()
        stats = {}
        done = 0
        for key, (net, root) in level.items():
            done += 1
            if last and done % 5000 == 0:
                print(f"   ... {done} of {len(level)} parents, {len(keys)} networks so far [{time.time() - t0:.0f}s]", flush=True)
            for new in insertions(net, root, counter):
                par = parents(new)
                sysk = system_of(new, root, par)
                if sysk is None:
                    continue
                ukey = keyfun(new, root, par)
                if ukey in keys:
                    continue
                if not planar_with_order(new):
                    continue
                keys.add(ukey)
                record(new, root, par, k, stats)
                if not last:
                    nxt[ukey] = (new, root)
        report(k, len(keys), stats)
        level = nxt
    print()
    print("examples of networks whose six-leaf system is not 6-locally good (one per dihedral class):")
    for (st, cls), (k, desc) in sorted(examples.items(), key=lambda kv: (kv[1][0], kv[0][0])):
        missing = sorted(set(min(m, FULL ^ m) for m in all_circular_splits(6) if not is_trivial(6, m)) - set(cls))
        print(f"  [{st}] first seen with {k} hybrid nodes; missing splits (masks) {[bin(m)[2:].zfill(6) for m in missing]}")
        print(f"       {desc}")
