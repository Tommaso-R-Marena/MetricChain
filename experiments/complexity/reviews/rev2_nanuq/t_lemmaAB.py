"""Independent tests of Lemma A, Lemma B, Lemma 7(iii) on explicit networks produced by hybrid insertion.

 (1) Lemma 7(iii)+A+B: every restriction to 6 leaves of Split(T(N)), N galled outer-labeled planar, lies in C_6
     (the referee's own C_6, css.C_class(6)); if all hybrids have leaf children, it lies in A_6.
 (2) Lemma B: for a hybrid h with non-leaf child c, build the pieces N_1 (subnetwork below c replaced by a leaf p)
     and N_2 (subnetwork below c, with a new leaf r above c) as explicit rooted networks and compare
     Split(T(N)) with the substitution of Split(T(N_1)), Split(T(N_2)) (label-based).  Also: are the pieces valid
     LSA networks, galled, outer-labeled planar?
 (3) which of the 108 systems of C_6 are realised by generated 6-leaf networks.
usage: python3 t_lemmaAB.py file1.pkl [file2.pkl ...]
"""
import sys, pickle, random
from itertools import combinations
from collections import Counter
import rnet, gen, css

C6 = css.C_class(6)
A6 = css.A_class(6)
C5, A5 = css.C_class(5), css.A_class(5)
rng = random.Random(5)

def cut_pieces(net, h):
    c = net[h][0]
    below = gen.descendants_or_self(net, c)
    n1 = {v: list(ch) for v, ch in net.items() if v not in below}
    n1[h] = ["__p__"]
    n1["__p__"] = []
    n2 = {v: list(net[v]) for v in below}
    n2["__root2__"] = ["__r__", c]
    n2["__r__"] = []
    return n1, n2

def splits_of(net):
    leaves, per_tree, Q = rnet.displayed(net)
    return leaves, set().union(*per_tree)

cache = {}
stats = Counter()
realised6 = set()
lemmaB = Counter()
total_nets = 0
for fn in sys.argv[1:]:
    nets = pickle.load(open(fn, "rb"))
    for net, order, f, st in nets:
        total_nets += 1
        n = f["n"]
        status, det, sigma, nn = gen.check_fast(net, order)
        key = (n, frozenset(sigma))
        allleaf = f["nonleaf_hyb_children"] == 0
        if n == 6:
            realised6.add(frozenset(sigma))
        if (key, allleaf) not in cache:
            subsets = list(combinations(range(n), 6))
            if len(subsets) > 40:
                subsets = rng.sample(subsets, 40)
            okC = okA = True
            for Y in subsets:
                r = css.restrict(n, sigma, Y)
                if r not in C6:
                    okC = False
                if r not in A6:
                    okA = False
            cache[(key, allleaf)] = (okC, okA, len(subsets))
        okC, okA, cnt = cache[(key, allleaf)]
        stats["nets"] += 1
        stats["restrictions_tested"] += cnt
        if not okC:
            stats["RESTRICTION_NOT_IN_C6"] += 1
            print("NOT IN C6:", net)
        if allleaf:
            stats["nets_all_leaf_children"] += 1
            if not okA:
                stats["LEAFCHILD_RESTRICTION_NOT_IN_A6"] += 1
                print("NOT IN A6:", net)
        # Lemma B on a sample
        if f["nonleaf_hyb_children"] > 0 and lemmaB["tested"] < 4000 and rng.random() < 0.25:
            root, tn, hybrids, leaves = rnet.classify(net)
            Lset = set(leaves)
            cand = [h for h in hybrids if net[h][0] not in Lset]
            h = rng.choice(cand)
            n1, n2 = cut_pieces(net, h)
            lemmaB["tested"] += 1
            for name, piece in (("N1", n1), ("N2", n2)):
                try:
                    rnet.classify(piece)
                    valid = True
                except ValueError as e:
                    valid = False
                lemmaB[name + "_valid_binary"] += valid
                if valid:
                    lemmaB[name + "_LSA"] += rnet.is_lsa_network(piece)
                    lemmaB[name + "_galled"] += rnet.is_galled_def(piece)
                    lemmaB[name + "_OLP"] += rnet.planar_circular_order(piece) is not None
                    nl = len(rnet.classify(piece)[3])
                    lemmaB[name + f"_leaves_{min(nl, 4)}{'+' if nl >= 4 else ''}"] += 1
            L, S = splits_of(net)
            L1, S1 = splits_of(n1)
            L2, S2 = splits_of(n2)
            X1 = frozenset(L1) - {"__p__"}
            X2 = frozenset(L2) - {"__r__"}
            comp = set()
            for s in S1:
                A, B = tuple(s)
                if "__p__" in B:
                    A, B = B, A
                A2 = (A - {"__p__"}) | X2
                if A2 and B:
                    comp.add(frozenset((frozenset(A2), frozenset(B))))
            for s in S2:
                A, B = tuple(s)
                if "__r__" in B:
                    A, B = B, A
                A2 = (A - {"__r__"}) | X1
                if A2 and B:
                    comp.add(frozenset((frozenset(A2), frozenset(B))))
            if comp == S:
                lemmaB["identity_ok"] += 1
            else:
                lemmaB["IDENTITY_FAILS"] += 1
                print("LEMMA B IDENTITY FAILS", net, h)
print("networks:", total_nets, dict(stats))
print("distinct (n, split system) pairs:", len({k for k, _ in cache}))
print("Lemma B:", dict(lemmaB))
print("6-leaf systems realised by generated networks:", len(realised6), "| all in C_6:", realised6 <= C6,
      "| C_6 systems not realised:", len(C6 - realised6), "| in A_6:", len(realised6 & A6))
