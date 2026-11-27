# c9_theoremA.py -- REVIEW 6: Theorem A(a),(d) of NANUQ_HIGHER_LEVELS.md on explicit networks of ARBITRARY level.
# Random outer-labeled planar rooted binary networks (random tree + random hybrid insertions, no bound on the level),
# 7..10 leaves.  For every six-subset Y of the leaves: if the restriction of Split(T(N)) to Y is NOT 6-locally good
# (definition of section 3 of the main note, own implementation in c7_step1_fact.py), then the six leaves must lie at
# six different positions of ONE blob (position of a leaf w.r.t. a blob = the node of the blob through which the leaf
# is attached).  Also counted: restrictions that are good although the six leaves sit at six positions of one blob.
import sys, random, itertools, time
sys.path.insert(0, "../partA")
import networkx as nx
from rn import Net
from t3_mutation import random_tree, add_hybrid
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from c7_step1_fact import locally_good


def positions(N):
    """for every blob (2-edge-connected component with >= 2 nodes): dict leaf -> attachment node"""
    G = nx.Graph(N.ugraph())
    out = []
    for blob in N.blobs():
        H = G.copy()
        H.remove_edges_from([(u, v) for u, v in G.edges() if u in blob and v in blob])
        pos = {}
        for comp in nx.connected_components(H):
            att = [v for v in comp if v in blob]
            assert len(att) == 1, "a pendant part attached at several nodes"
            for v in comp:
                if v in N.leaves:
                    pos[v] = att[0]
        out.append(pos)
    return out


def main(count, seed, maxn, maxh):
    rng = random.Random(seed)
    st = dict(networks=0, six_subsets=0, not_good=0, not_good_explained=0, good_but_six_positions=0, level_hist={}, VIOLATIONS=0)
    t0 = time.time()
    while st["networks"] < count:
        n0 = rng.randint(7, maxn)
        net = random_tree(rng, n0)
        k = rng.randint(2, maxh)
        good = True
        for c in range(k):
            if not add_hybrid(net, rng, c + 1):
                good = False
                break
        if not good:
            continue
        N = Net(net)
        if not N.valid():
            continue
        C = N.planar_order()
        if C is None:
            continue
        lev = N.level()
        if lev < 2:
            continue
        st["networks"] += 1
        st["level_hist"][lev] = st["level_hist"].get(lev, 0) + 1
        idx = {x: i for i, x in enumerate(C)}
        disp = N.displayed_splits(C)
        pos = positions(N)
        sides = [frozenset(idx[x] for x in next(iter(sp))) for sp in disp]
        for Y in itertools.combinations(range(N.n), 6):
            st["six_subsets"] += 1
            Yset = set(Y)
            S = set()
            for a in sides:
                m = 0
                for q, y in enumerate(Y):
                    if y in a:
                        m |= 1 << q
                if bin(m).count("1") in (2, 3, 4):
                    S.add(min(m, 63 ^ m))
            S = frozenset(S)
            leaves = [C[y] for y in Y]
            six_pos = any(len({p[l] for l in leaves}) == 6 for p in pos)
            if not locally_good(S):
                st["not_good"] += 1
                if six_pos:
                    st["not_good_explained"] += 1
                else:
                    st["VIOLATIONS"] += 1
                    print("VIOLATION of Theorem A(a):", net, leaves)
            elif six_pos:
                st["good_but_six_positions"] += 1
    print(f"seed {seed}: {time.time()-t0:.0f}s", st)


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    count, seed, maxn, maxh = (a + [300, 1, 9, 6][len(a):])[:4]
    main(count, seed, maxn, maxh)
