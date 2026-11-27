# c5_random_search.py -- REVIEW 6: a small random search BEYOND the survey of the note: six-leaf rooted binary
# networks, outer-labeled planar for the order (0..5), with 4..KMAX hybrid nodes, built by random insertion
# sequences in which the two subdivided edges MAY COINCIDE (this creates parallel edges, which the survey never
# has, and later insertions into them create the blobs the survey cannot generate).
# Question: does any such network display one of the 36 tree-generated systems that the survey never finds?
# Usage: python3 c5_random_search.py SEED SECONDS KMAX
import sys, time, random, pickle, itertools
import networkx as nx
from c1_survey import N, FULL, INTERVALS, DIH, planar_rooted_trees, image_system

found114 = pickle.load(open("systems_level_3.pkl", "rb"))
assert len(found114) == 114


def parents(net):
    par = {v: [] for v in net}
    for v, ch in net.items():
        for c in ch:
            par[c].append(v)
    return par


def topo(net, root):
    indeg = {v: 0 for v in net}
    for v, ch in net.items():
        for c in ch:
            indeg[c] += 1
    st, out = [root], []
    while st:
        v = st.pop()
        out.append(v)
        for c in net[v]:
            indeg[c] -= 1
            if indeg[c] == 0:
                st.append(c)
    assert len(out) == len(net)
    return out[::-1]                       # children before parents


def system_of(net, root):
    par = parents(net)
    order = topo(net, root)
    hyb = [v for v in net if len(par[v]) == 2]
    out = set()
    trees = set()
    for choice in itertools.product((0, 1), repeat=len(hyb)):
        keep = {h: (par[h][c], c) for h, c in zip(hyb, choice)}
        mask = {}
        spl = set()
        for v in order:
            ch = net[v]
            if not ch:
                mask[v] = 1 << v
                continue
            m = 0
            used = {}
            for c in ch:
                if c in keep:
                    if keep[c][0] != v:
                        continue
                    if par[c][0] == par[c][1]:          # parallel edges: count the child once
                        if used.get(c):
                            continue
                        used[c] = True
                m |= mask[c]
            mask[v] = m
            if m and m != FULL:
                co = FULL ^ m
                if (m & (m - 1)) and (co & (co - 1)):
                    if m not in INTERVALS:
                        return None, None
                    spl.add(min(m, co))
        out |= spl
        trees.add(frozenset(spl))
    return frozenset(out), trees


def wheel_planar(net):
    G = nx.Graph()
    for v, ch in net.items():
        for c in ch:
            G.add_edge(v, c)
    for q in range(N):
        G.add_edge(q, (q + 1) % N)
        G.add_edge("apex", q)
    return nx.check_planarity(G)[0]


def desc_or_self(net, x):
    seen, st = {x}, [x]
    while st:
        v = st.pop()
        for c in net[v]:
            if c not in seen:
                seen.add(c)
                st.append(c)
    return seen


def random_insertion(net, rng, allow_same):
    E = [(a, i) for a in net for i in range(len(net[a]))]          # edge = (tail, slot)
    for _ in range(40):
        (a, i), (c, j) = rng.choice(E), rng.choice(E)
        b, d = net[a][i], net[c][j]
        same = (a, i) == (c, j)
        if same and not allow_same:
            continue
        if not same and a in desc_or_self(net, d):
            continue
        new = {v: list(ch) for v, ch in net.items()}
        p, h = max(net) + 1, max(net) + 2
        if same:
            new[a][i] = p
            new[p] = [h, h]
            new[h] = [b]
        else:
            new[a][i] = p
            new[p] = [b, h]
            new[c][j] = h                                         # (c,j) is a different slot, still pointing to d
            new[h] = [d]
        return {v: tuple(ch) for v, ch in new.items()}
    return None


def main(seed, seconds, kmax):
    rng = random.Random(seed)
    trees0 = planar_rooted_trees()
    t0 = time.time()
    stats = {}
    seen_by_k = {}
    new_systems = {}
    maxtrees = 0
    par_edges = 0
    while time.time() - t0 < seconds:
        net, root = rng.choice(trees0)
        net = dict(net)
        k = 0
        target = rng.randint(4, kmax)
        fails = 0
        had_parallel = False
        while k < target and fails < 60:
            new = random_insertion(net, rng, allow_same=(rng.random() < 0.25))
            if new is None:
                fails += 1
                continue
            s, trees = system_of(new, root)
            if s is None or not wheel_planar(new):
                fails += 1
                continue
            net = new
            k += 1
            had_parallel |= any(len(ch) == 2 and ch[0] == ch[1] for ch in net.values())
            stats[k] = stats.get(k, 0) + 1
            par_edges += had_parallel
            seen_by_k.setdefault(k, set()).add(s)
            maxtrees = max(maxtrees, len(trees))
            if s not in found114 and s not in new_systems:
                new_systems[s] = (k, net, root)
                print("NEW SYSTEM (not among the 114):", sorted(bin(m)[2:].zfill(6) for m in s), "k =", k, net, flush=True)
    print(f"seed {seed}: {seconds}s; networks examined by number of hybrid nodes: {dict(sorted(stats.items()))}; "
          f"networks with a parallel edge somewhere in their history: {par_edges}; "
          f"distinct systems seen by k: { {k: len(v) for k, v in sorted(seen_by_k.items())} }; "
          f"largest number of distinct displayed trees: {maxtrees}; systems outside the 114: {len(new_systems)}")
    pickle.dump(new_systems, open(f"random_new_{seed}.pkl", "wb"))


if __name__ == "__main__":
    main(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]))
