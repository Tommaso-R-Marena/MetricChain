# mylemma0.py -- REVIEWER'S OWN CODE: literal Definition 2.5 (union of up-down paths, suppress
# degree-2 nodes, then switchings of the result) against "restrict the displayed trees" (Lemma 0).
import itertools, random, sys
from mynet import Net
from mygen import random_tree_children, edge_list, insert_arc, Counter


def all_dipaths(net, a, targets):
    """all directed paths (as node tuples) from a to nodes in targets"""
    out = []
    def rec(v, path):
        if v in targets:
            out.append(tuple(path))
        for k, c in enumerate(net.ch[v]):
            # parallel edges give the same node path; edges are recorded as (v,c,k) separately below
            rec(c, path + [c])
    rec(a, [a])
    return out


def union_updown(net, Y):
    """edge multiset U (as set of (u,v,k), k = index of v among children of u) of all up-down paths
    between two different leaves of Y in the rooted partner"""
    Yset = set(Y)
    U = set()
    for a in net.nodes:
        if not net.ch[a]:
            continue
        # directed edge-paths from a
        paths = []
        def rec(v, epath, nodes):
            if v in Yset:
                paths.append((tuple(epath), frozenset(nodes), v))
            for k, c in enumerate(net.ch[v]):
                rec(c, epath + [(v, c, k)], nodes | {c})
        rec(a, [], {a})
        for p1, p2 in itertools.combinations(paths, 2):
            if p1[2] == p2[2]:
                continue
            if p1[1] & p2[1] == {a}:
                # two paths from a to different leaves sharing only the apex a (node-disjoint otherwise);
                # with parallel edges a->c, a->c the node sets intersect in c, so that is excluded
                U.update(p1[0]); U.update(p2[0])
    return U


def subnet_trees(net, Y):
    """displayed trees of N|_Y computed literally: switchings of the union U of up-down paths
    (hybrid nodes of N|_Y = nodes with two entering edges in U); each tree as a frozenset of splits of Y"""
    U = union_updown(net, Y)
    nodes = set()
    par = {}
    for (u, v, k) in U:
        nodes.add(u); nodes.add(v)
        par.setdefault(v, []).append((u, k))
    roots = [v for v in nodes if v not in par]
    hyb = [v for v in nodes if len(par.get(v, [])) == 2]
    Ys = sorted(Y, key=str)
    idx = {y: i for i, y in enumerate(Ys)}
    full = (1 << len(Ys)) - 1
    trees = set()
    info = {'roots': roots, 'nhyb': len(hyb)}
    for choice in itertools.product((0, 1), repeat=len(hyb)):
        pm = {}
        for v in nodes:
            if v in par:
                pm[v] = par[v][0][0]
        for h, c in zip(hyb, choice):
            pm[h] = par[h][c][0]
        # clusters
        cl = {v: 0 for v in nodes}
        for y in Ys:
            cl[y] = 1 << idx[y]
        # order nodes by a topological order of the full network
        for v in reversed(net.topo()):
            if v in pm:
                cl[pm[v]] |= cl[v]
        sp = set()
        for v in nodes:
            m = cl[v]
            if m and m != full:
                if m & 1:
                    m = full ^ m
                sp.add(m)
        trees.add(frozenset(sp))
    return trees, info


def restricted_trees(net, Y):
    L = net.leaves
    Ys = sorted(Y, key=str)
    pos = [L.index(y) for y in Ys]
    full = (1 << len(Ys)) - 1
    out = set()
    for t in net.displayed_trees():
        sp = set()
        for m in t:
            r = 0
            for i, p in enumerate(pos):
                if (m >> p) & 1:
                    r |= 1 << i
            if r and r != full:
                if r & 1:
                    r = full ^ r
                sp.add(r)
        out.add(frozenset(sp))
    return out


def lsa(net, Y):
    """least stable ancestor of Y, by the definition"""
    Yset = set(Y)
    best = None
    stable = []
    for v in net.nodes:
        if v in Yset and len(Yset) > 1:
            continue
        # v is stable iff no leaf of Y is reachable from the root avoiding v
        if v == net.root:
            stable.append(v); continue
        if not (net.reach_avoiding(v) & Yset):
            stable.append(v)
    # lowest = the one that is a descendant of all others: maximal position in a topological order
    topo = net.topo()
    return max(stable, key=topo.index)


if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rng = random.Random(seed)
    nets = tested = mism = 0
    bad_root = 0
    by_hyb = {}
    while nets < N:
        n = rng.randint(4, 8)
        ch, root = random_tree_children(n, rng)
        cnt = Counter()
        k = rng.randint(1, 4)
        for _ in range(k):
            E = edge_list(ch, root)
            e1 = rng.choice(E + [None])
            e2 = rng.choice(E)
            ch, root = insert_arc(ch, root, e1, e2, cnt)
        net = Net(ch, root)
        if not net.is_valid():
            continue
        nets += 1
        by_hyb[k] = by_hyb.get(k, 0) + 1
        L = net.leaves
        for size in range(2, min(n, 6) + 1):
            subs = list(itertools.combinations(L, size))
            rng.shuffle(subs)
            for Y in subs[:12]:
                t1, info = subnet_trees(net, Y)
                t2 = restricted_trees(net, Y)
                tested += 1
                if t1 != t2:
                    mism += 1
                    print("MISMATCH", net.ch, net.root, Y)
                if len(info['roots']) != 1 or info['roots'][0] != lsa(net, Y):
                    bad_root += 1
                    print("ROOT PROBLEM", net.ch, net.root, Y, info, lsa(net, Y))
    print("seed", seed, "networks", nets, "by number of hybrid nodes", by_hyb, "subsets tested", tested,
          "mismatches T(N|Y) vs {T|Y}:", mism, " U has a unique source = LSA(Y) violated:", bad_root)
