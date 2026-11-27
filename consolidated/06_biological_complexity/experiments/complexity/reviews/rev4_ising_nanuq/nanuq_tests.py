"""Referee's tests for the NANUQ additions (Lemma 0, B0, B, Theorem 7 induction, Theorem 9(c)).
Explicit rooted networks only; own generator (hybrid insertion + literal filters)."""
import itertools, random, sys, time
from fractions import Fraction
from collections import Counter
from nanuq_core import *

rng = random.Random(4242)


# ------------------------------------------------------------------ A. anchor: quartet metric of a tree
def test_tree_anchor(trials=200):
    """[HABIMRW] Eq. (6),(7): the quartet metric of a tree is the tree metric of the quartet metrization."""
    bad = 0
    for it in range(trials):
        n = rng.randint(4, 10)
        net = random_tree(["x%d" % i for i in range(n)], rng)
        L = net.leaves()
        (tree,) = tuple(net.displayed_trees())
        d = nanuq_metric(tree, L)
        full = frozenset(L)
        # weights: pendant edge of x: |X1||X2| ; internal edge: |X1||X2| + |X3||X4|
        # get the 4 / 2 blocks from the split system: for split A|B the maximal proper sub-clusters
        splits = [tuple(sp) for sp in tree]
        sides = set()
        for a, b in splits:
            sides.add(a); sides.add(b)

        def parts(side):
            # the two maximal sides strictly inside `side` (children clusters); side has >= 2 leaves
            inner = [s for s in sides if s < side]
            mx = [s for s in inner if not any(s < t for t in inner)]
            return mx

        w = {}
        for a, b in splits:
            if len(a) == 1 or len(b) == 1:
                big = a if len(a) > 1 else b
                p = parts(big)
                assert len(p) == 2, p
                w[frozenset([a, b])] = len(p[0]) * len(p[1])
            else:
                pa, pb = parts(a), parts(b)
                assert len(pa) == 2 and len(pb) == 2
                w[frozenset([a, b])] = len(pa[0]) * len(pa[1]) + len(pb[0]) * len(pb[1])
        for x, y in itertools.combinations(L, 2):
            dist = sum(wt for sp, wt in w.items() if any((x in s) != (y in s) for s in list(sp)[:1]))
            if dist != d[(x, y)]:
                bad += 1
    print("[A] tree anchor (quartet metrization, Eq. 6-7 of the source): %d trees, mismatching trees/pairs: %d" % (trials, bad))


# ------------------------------------------------------------------ B. Lemma 0 against a literal Def. 2.5
def test_lemma0(trials=1500):
    mism = 0
    multi_source = 0
    disconnected = 0
    nsub = 0
    kinds = Counter()
    for it in range(trials):
        n = rng.randint(3, 8)
        k = rng.randint(1, 4)
        mode = rng.choice(["galled-planar", "planar", "any", "any"])
        net = random_network(n, k, rng, galled=(mode == "galled-planar"), planar=(mode != "any"), tries=60)
        if not net.hybrids():
            continue
        kinds[(mode, len(net.hybrids()))] += 1
        L = net.leaves()
        subsets = []
        for size in range(2, min(n, 6) + 1):
            for _ in range(3):
                subsets.append(tuple(sorted(rng.sample(L, size))))
        for Y in set(subsets):
            nsub += 1
            lit, nsrc, conn = net.subnetwork_trees(Y)
            res = net.displayed_trees(Y)
            if nsrc != 1:
                multi_source += 1
            if not conn:
                disconnected += 1
            if lit != res:
                mism += 1
                if mism <= 3:
                    print("   LEMMA 0 MISMATCH", net.ch, Y)
    print("[B] Lemma 0: %d (network, Y) pairs on %d networks; T(N|_Y) != {T|_Y}: %d ; unions with several sources: %d ;"
          " switchings of the union not spanning Y: %d" % (nsub, sum(kinds.values()), mism, multi_source, disconnected))
    print("    networks by (mode, hybrids):", dict(sorted(kinds.items())))


# ------------------------------------------------------------------ C. Lemma B0, D. Lemma B, E. Theorem 7
def degenerate_networks():
    """hand-made degenerate members: 2-blob at the root (parallel edges after root suppression), stacked blobs"""
    out = []
    # r -> a, r -> h, a -> h, a -> x ; h -> c ; c -> y, z      (2-blob {a,h} in the semi-directed network)
    out.append(RNet({"r": ["a", "h"], "a": ["h", "x"], "h": ["c"], "c": ["y", "z"]}, "r"))
    # same with a bigger clade below and a second 2-blob-like triangle below
    out.append(RNet({"r": ["a", "h"], "a": ["h", "x"], "h": ["c"], "c": ["b", "g"], "b": ["g", "y"], "g": ["d"],
                     "d": ["z", "w"]}, "r"))
    # hybrid with leaf child inside a triangle below a hybrid
    out.append(RNet({"r": ["a", "h"], "a": ["h", "x"], "h": ["c"], "c": ["b", "g"], "b": ["g", "y"], "g": ["z"]}, "r"))
    # chain of three 2-/3-blobs
    out.append(RNet({"r": ["a", "h"], "a": ["h", "x"], "h": ["c"], "c": ["b", "y"], "b": ["e", "g"], "e": ["g", "u"],
                     "g": ["f"], "f": ["z", "w"]}, "r"))
    return out


def cut_pieces(net, h):
    c = net.ch[h][0]
    D = net.descendants(c)
    ch1 = {u: list(vs) for u, vs in net.ch.items() if u not in D}
    ch1[h] = ["P*"]
    ch1["P*"] = []
    N1 = RNet(ch1, net.root)
    ch2 = {u: list(net.ch[u]) for u in D}
    ch2["R*root"] = ["R*", c]
    ch2["R*"] = []
    N2 = RNet(ch2, "R*root")
    return N1, N2, D


def test_structure(trials=3000, nmax=11, kmax=6):
    st = Counter()
    seen = set()
    nets = degenerate_networks()
    t0 = time.time()
    for it in range(trials):
        n = rng.randint(3, nmax)
        k = rng.randint(1, kmax)
        nets.append(random_network(n, k, rng, galled=True, planar=True, tries=80))
    for net in nets:
        if not net.hybrids():
            continue
        key = canonical_key(net)
        if key in seen:
            continue
        seen.add(key)
        assert net.is_valid() and net.is_galled()
        order = net.planar_order()
        assert order is not None
        st["networks"] += 1
        lev, nb = net.level()
        st["level>=3"] += lev >= 3
        st["multi-blob"] += nb >= 2
        L = net.leaves()
        n = len(L)
        # parallel edges after root suppression: root's children u,h with u -> h
        r1, r2 = net.ch[net.root]
        if (r2 in net.ch[r1] and len(net.par[r2]) == 2) or (r1 in net.ch[r2] and len(net.par[r1]) == 2):
            st["2-blob at the root (parallel edges)"] += 1
        S = net.split_system()
        # ---- Lemma B0
        for h in net.hybrids():
            c = net.ch[h][0]
            st["hybrid nodes"] += 1
            if len(net.par[c]) == 2:
                st["B0 FAIL: child of hybrid is hybrid"] += 1
            if not net.is_bridge(h, c):
                st["B0 FAIL: edge below hybrid not a cut edge"] += 1
        # ---- Theorem 7 (n >= 4), NANUQ metric from the definition
        if n >= 4:
            nonneg, supp, mn, bad = check_conclusion(S, order)
            st["Theorem 7 checked"] += 1
            if not (nonneg and supp):
                st["THEOREM 7 FAIL"] += 1
                print("  THEOREM 7 FAILS", net.ch)
        # ---- Lemma B
        for h in net.hybrids():
            c = net.ch[h][0]
            if not net.ch[c]:
                continue
            st["cuts"] += 1
            N1, N2, D = cut_pieces(net, h)
            ok1, ok2 = N1.is_valid(), N2.is_valid()
            if not ok1:
                st["B FAIL: N1 not a valid LSA network"] += 1
            if not ok2:
                st["B FAIL: N2 not a valid LSA network"] += 1
            if not (ok1 and ok2):
                continue
            L1, L2 = N1.leaves(), N2.leaves()
            st["N1 with 2 leaves"] += len(L1) == 2
            st["N1 with 3 leaves"] += len(L1) == 3
            st["N2 with 2 leaves"] += len(L2) == 2
            st["N2 with 3 leaves"] += len(L2) == 3
            if len(L1) < 2 or len(L2) < 2:
                st["B FAIL: piece with < 2 leaves"] += 1
            if not N1.is_galled() or not N2.is_galled():
                st["B FAIL: piece not galled"] += 1
            # induced circular orders
            Dl = [x for x in order if x in D]
            idx = [i for i, x in enumerate(order) if x in D]
            # leaves of D must be consecutive on the circle
            pos = sorted(idx)
            gaps = sum(1 for a, b in zip(pos, pos[1:] + [pos[0] + n]) if b - a > 1)
            if gaps > 1:
                st["B FAIL: leaves below the cut not consecutive"] += 1
                continue
            # rotate so that the D-interval is contiguous
            start = next(i for i in range(n) if order[i] in D and order[i - 1] not in D) if len(Dl) < n else 0
            rot = order[start:] + order[:start]
            o2 = rot[:len(Dl)] + ["R*"]
            o1 = ["P*"] + rot[len(Dl):]
            if not N1.admits_order(o1) or not N2.admits_order(o2):
                st["B FAIL: piece not outer-labeled planar for the induced order"] += 1
            if not (N1.mu() < net.mu() and N2.mu() < net.mu()):
                st["B FAIL: mu does not decrease"] += 1
            S1, S2 = N1.split_system(), N2.split_system()
            if substitute(S1, L1, "P*", S2, L2, "R*") != S:
                st["B FAIL: substitution identity"] += 1
            # displayed trees: joined trees
            T1, T2 = N1.displayed_trees(), N2.displayed_trees()
            joined = set()
            for a in T1:
                for b in T2:
                    joined.add(frozenset(substitute(a, L1, "P*", b, L2, "R*")))
            if joined != net.displayed_trees():
                st["B FAIL: displayed trees are not the joined trees"] += 1
    print("[C/D/E] galled outer-labeled planar networks (explicit DAGs):")
    for k_, v in sorted(st.items()):
        print("    %-55s %d" % (k_, v))
    print("    time %.0f s" % (time.time() - t0))


def test_B0_nonplanar(trials=1500):
    """Lemma B0 does not assume planarity: galled networks, planar or not"""
    st = Counter()
    seen = set()
    for it in range(trials):
        n = rng.randint(3, 9)
        k = rng.randint(1, 6)
        net = random_network(n, k, rng, galled=True, planar=False, tries=80)
        key = canonical_key(net)
        if key in seen or not net.hybrids():
            continue
        seen.add(key)
        st["networks"] += 1
        st["non-planar"] += net.planar_order() is None
        for h in net.hybrids():
            c = net.ch[h][0]
            st["hybrid nodes"] += 1
            if len(net.par[c]) == 2:
                st["B0 FAIL child hybrid"] += 1
            if not net.is_bridge(h, c):
                st["B0 FAIL not a cut edge"] += 1
    # converse sanity: non-galled networks where the edge below a hybrid is NOT a cut edge do exist
    ng = 0
    for it in range(300):
        net = random_network(rng.randint(4, 7), rng.randint(2, 3), rng, galled=False, planar=False, tries=40)
        if not net.is_galled():
            if any(not net.is_bridge(h, net.ch[h][0]) for h in net.hybrids()):
                ng += 1
    print("[C'] Lemma B0 on galled networks without planarity filter:", dict(st),
          "; non-galled controls with a non-cut edge below a hybrid:", ng)


# ------------------------------------------------------------------ F. Theorem 9
def family(s, t, version="bloblet", clade_shape="caterpillar", rng_=None):
    ch = {}
    # blob core
    ch["p1"] = ["b", "h1"]
    ch["q1"] = ["h1", "q2"]
    ch["q2"] = ["h2", "c"]
    ch["h1"] = ["u"]
    ch["u"] = ["x", "h2"]
    ch["h2"] = ["y"]
    A = ["a%d" % i for i in range(1, t + 1)]
    Dn = ["d%d" % i for i in range(1, s + 1)]

    def clade(names, tag):
        # returns root node of a clade on the given leaves
        if len(names) == 1:
            return names[0]
        if clade_shape == "caterpillar":
            top = names[0]
            for i, x in enumerate(names[1:]):
                node = "%scl%d" % (tag, i)
                ch[node] = [top, x]
                top = node
            return top
        else:
            k = rng_.randint(1, len(names) - 1)
            l, r = clade(names[:k], tag + "L"), clade(names[k:], tag + "R")
            node = "%scl_%s_%d" % (tag, names[0], len(names))
            ch[node] = [l, r]
            return node

    if version == "bloblet":
        # a_1 nearest the root, a_t nearest p1 ; d_1 nearest q1
        top = "p1"
        for i in range(t, 0, -1):
            node = "w%d" % i
            ch[node] = ["a%d" % i, top]
            top = node
        left = top
        top = "q1"
        for j in range(1, s + 1):
            node = "v%d" % j
            ch[node] = [top, "d%d" % j]
            top = node
        right = top
    else:
        left = "p1"
        if t:
            ch["wA"] = [clade(A, "A"), "p1"]
            left = "wA"
        right = "q1"
        if s:
            ch["wD"] = ["q1", clade(Dn, "D")]
            right = "wD"
    ch["rho"] = [left, right]
    order = A + ["b", "x", "y", "c"] + Dn
    return RNet(ch, "rho"), order


def test_theorem9():
    # N* exactly as printed
    Nstar = RNet({"rho": ["w1", "w3"], "w1": ["a1", "w2"], "w2": ["a2", "p1"], "p1": ["b", "h1"],
                  "w3": ["d", "q1"], "q1": ["h1", "q2"], "q2": ["h2", "c"], "h1": ["u"], "u": ["x", "h2"],
                  "h2": ["y"]}, "rho")
    order = ["a1", "a2", "b", "x", "y", "c", "d"]
    print("[F] N*: valid", Nstar.is_valid(), "| galled", Nstar.is_galled(), "| level,blobs", Nstar.level(),
          "| admits the stated order", Nstar.admits_order(order), "| displayed trees", len(Nstar.displayed_trees()))
    S = Nstar.split_system()
    d = nanuq_metric(S, order)
    M = [[int(d[(x, y)]) for y in order] for x in order]
    printed = [[0, 21, 23, 26, 26, 23, 21], [21, 0, 17, 24, 26, 27, 25], [23, 17, 0, 20, 24, 29, 27],
               [26, 24, 20, 0, 20, 24, 26], [26, 26, 24, 20, 0, 20, 24], [23, 27, 29, 24, 20, 0, 17],
               [21, 25, 27, 26, 24, 17, 0]]
    print("    NANUQ matrix equals the printed matrix:", M == printed)
    a = d[("b", "y")] + d[("x", "c")] - d[("b", "c")] - d[("x", "y")]
    sp = frozenset([frozenset(["x", "y"]), frozenset(["a1", "a2", "b", "c", "d"])])
    print("    alpha({x,y}|rest) =", a, "; split displayed:", sp in S)
    # (b) all 360 circular orders
    L = order
    first = L[0]
    cnt_bad = 0
    tot = 0
    seen = set()
    for perm in itertools.permutations(L[1:]):
        o = [first] + list(perm)
        if tuple([first] + list(reversed(perm))) in seen:
            continue
        seen.add(tuple(o))
        tot += 1
        neg = False
        for i, j, sp_ in circ_splits(o):
            if alpha(d, o, i, j) < 0:
                neg = True
                break
        cnt_bad += neg
    print("    circular orders: %d, with some negative alpha: %d" % (tot, cnt_bad))
    # literal Def 2.5 check on N* (all 35 four-sets)
    mism = 0
    for Y in itertools.combinations(L, 4):
        lit, nsrc, conn = Nstar.subnetwork_trees(Y)
        if lit != Nstar.displayed_trees(Y) or nsrc != 1:
            mism += 1
    print("    N*: quarnets by the literal Def. 2.5 vs restricted displayed trees, mismatches:", mism)
    # (c) the family, both versions
    r2 = random.Random(7)
    bad = 0
    rows = []
    for version in ("bloblet", "clade", "clade-random"):
        for s in range(0, 8):
            for t in range(0, 8):
                if version == "clade-random":
                    net, o = family(s, t, "clade", "random", r2)
                else:
                    net, o = family(s, t, version)
                assert net.is_valid() and net.admits_order(o), (version, s, t)
                assert not net.is_galled()
                S_ = net.split_system()
                assert len(net.displayed_trees()) == 4 or (s + t == 0)
                d_ = nanuq_metric(S_, o)
                a_ = d_[("b", "y")] + d_[("x", "c")] - d_[("b", "c")] - d_[("x", "y")]
                want = 2 - (s + t) * (s + t - 1) // 2 if version == "bloblet" else 2 - s * t
                spl = frozenset([frozenset(["x", "y"]), frozenset(o) - {"x", "y"}])
                if a_ != want or spl not in S_:
                    bad += 1
                    print("     MISMATCH", version, s, t, a_, want)
                rows.append((version, s, t, a_))
    print("    family N(s,t), 0<=s,t<=7, bloblet / clade (caterpillar) / clade (random shapes): %d values, mismatches %d"
          % (len(rows), bad))
    # the six local numbers through the small members (Prop. 2 gives alpha/2 = Phi4 + sum Phi5' + sum Phi6')
    val = {(v, s, t): a for v, s, t, a in rows}
    print("    alpha/2 for (s,t) = (0,0),(1,0),(0,1),(2,0),(0,2),(1,1): bloblet",
          [val[("bloblet", s, t)] / 2 for s, t in [(0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]],
          " clade", [val[("clade", s, t)] / 2 for s, t in [(0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]])


if __name__ == "__main__":
    which = sys.argv[1:] or ["A", "B", "C", "F"]
    if "A" in which: test_tree_anchor()
    if "F" in which: test_theorem9()
    if "B" in which: test_lemma0()
    if "C" in which:
        test_structure()
        test_B0_nonplanar()
