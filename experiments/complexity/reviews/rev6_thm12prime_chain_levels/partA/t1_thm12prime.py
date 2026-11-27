# t1_thm12prime.py -- REVIEW 6: Theorem 12' on explicit rooted networks built by gen_l2.py.
# Definition-level checks (no use of the position records):
#   D1  the constructed circular order C is an outer-labeled planar order (wheel test), level <= 2, valid network;
#   D2  if some split weight alpha for C is negative, an exact search over ALL circular orders finds no Kalmanson
#       order;  if none is negative the metric is Kalmanson for C (trivially) -- counted.
# Proof-level checks (use the records of the nested blobs):
#   P1  the negative splits are exactly critical splits S* of recorded nested blobs (Theorem 12(a)), and the
#       weight equals the formula of Theorem 12(b);
#   P2  for every negative S*: B1 = leaf after the x/y block, Cc = leaf before it; for ALL Z (middle b-positions),
#       Y (at y), X1 (at x_1): the three strict four-point inequalities of the proof;
#   P3  every split other than S* that separates {Y,X1} from {B1,Cc} has weight exactly 0; and the splits used in
#       (1)-(3) of the proof have positive weight.
import sys, random, itertools, time
import numpy as np
import networkx as nx
from rn import Net, alphas, is_kalmanson, kalmanson_search
from gen_l2 import random_network, targeted_network


def wheel_ok(N, order):
    H = nx.Graph(N.ugraph())
    n = len(order)
    for i in range(n):
        H.add_edge(order[i], order[(i + 1) % n])
        H.add_edge(("apex",), order[i])
    return nx.check_planarity(H)[0]


def e2(v):
    s = sum(v)
    return (s * s - sum(x * x for x in v)) // 2


def formula(beta, xi, eta, gamma):
    R = eta + sum(xi[1:])
    if gamma:
        G, mid = sum(gamma), beta[1:]
    else:
        G, mid = beta[-1], beta[1:-1]
    return beta[0] * G + xi[0] * R - e2(mid)


def main(count, seed, maxleaves, searchmax, targeted=0):
    rng = random.Random(seed)
    st = dict(networks=0, with_negative=0, negative_splits=0, searched=0, quintuples=0, kalm_for_C=0,
              zero_crit=0, entry_neg={}, nonleaf_pos_neg=0, nested_blobs=0, max_n=0, several_neg=0,
              other_sep_splits_checked=0, modes={})
    t0 = time.time()
    while st["networks"] < count:
        if targeted:
            net, order, records, mode = targeted_network(rng, maxleaves, rng.choice(["A", "b1", "bmid", "bkB", "c1", "ce"]))
        else:
            net, order, records, mode = random_network(rng, maxleaves)
        N = Net(net)
        n = N.n
        if n < 7 or not N.valid():
            if not N.valid():
                print("INVALID network generated", net); return False
            continue
        assert sorted(order) == N.leaves
        assert N.level() <= 2, "level > 2"
        assert wheel_ok(N, order), "constructed order is not an outer-labeled planar order"
        st["networks"] += 1
        st["modes"][mode] = st["modes"].get(mode, 0) + 1
        st["max_n"] = max(st["max_n"], n)
        st["nested_blobs"] += len(records)
        D6 = N.nanuq6(order)                     # indices = positions in the circular order C
        al = alphas(D6, list(range(n)))          # 6*alpha
        neg = {k: v for k, v in al.items() if v < 0}
        disp = N.displayed_splits(order)
        idx = {x: i for i, x in enumerate(order)}

        def side(i, j):                          # split S_ij: U = positions i+1..j
            return frozenset(range(i + 1, j + 1))
        # ---- P1
        crit = {}
        for rc in records:
            kB, k1, k2 = rc["k"]
            if not (k1 >= 1 and kB >= 2):
                continue
            pos = rc["pos"]
            named = set()
            for p, ls in pos.items():
                if ls is not None:
                    named |= set(ls)
            outside = [x for x in order if x not in named]
            lvd = {p: (pos[p] if pos[p] is not None else outside) for p in pos}
            lv = lvd.__getitem__          # (a lambda here would capture the loop variables by reference)
            inside = set(lv(("y", 0)))
            for a in range(1, k1 + 1):
                inside |= set(lv(("x", a)))
            U = frozenset(idx[x] for x in inside)
            beta = [len(lv(("b", j))) for j in range(1, kB + 1)]
            gamma = [len(lv(("c", e))) for e in range(1, k2 + 1)]
            xi = [len(lv(("x", a))) for a in range(1, k1 + 1)]
            pred = formula(beta, xi, len(lv(("y", 0))), gamma)
            crit[U] = (pred, rc, lv)
        full = frozenset(range(n))
        for (i, j), v in al.items():
            U = side(i, j)
            key = U if U in crit else (full - U if (full - U) in crit else None)
            isdisp = frozenset((frozenset(order[q] for q in U), frozenset(order[q] for q in full - U))) in disp
            if key is not None:
                if v != 6 * crit[key][0]:        # al = 6*alpha (D6 = 6d); Theorem 12(b) gives alpha itself
                    print("FORMULA MISMATCH", v, crit[key][0], crit[key][1]["k"], crit[key][1]["entry"]); return False
                if not isdisp:
                    print("critical split not displayed"); return False
            else:
                if v < 0 or ((v > 0) != isdisp):
                    print("THEOREM 12(a) VIOLATED", (i, j), v, isdisp, net, order); return False
        if not neg:
            st["kalm_for_C"] += 1
            assert is_kalmanson(D6, list(range(n)))
            st["zero_crit"] += sum(1 for U in crit if crit[U][0] == 0)
            continue
        st["with_negative"] += 1
        st["negative_splits"] += len(neg)
        st["several_neg"] += len(neg) > 1
        # ---- D2: all circular orders
        if n <= searchmax:
            st["searched"] += 1
            r = kalmanson_search(D6)
            if r is not None:
                print("COUNTEREXAMPLE TO THEOREM 12': Kalmanson order found", [order[i] for i in r], net); return False
        # ---- P2, P3
        for U, (pred, rc, lv) in crit.items():
            if pred >= 0:
                continue
            kB, k1, k2 = rc["k"]
            ent = rc["entry"]
            st["entry_neg"][ent[0] + (str(ent[1]) if len(ent) > 1 else "") + f"/kB{kB}k2{k2}"] = \
                st["entry_neg"].get(ent[0] + (str(ent[1]) if len(ent) > 1 else "") + f"/kB{kB}k2{k2}", 0) + 1
            st["nonleaf_pos_neg"] += any(len(lv(p)) > 1 for p in rc["pos"])
            m = len(U)
            s = next(i for i in range(n) if i in U and (i - 1) % n not in U)
            block = [(s + i) % n for i in range(m)]
            assert set(block) == set(U)
            Cc, B1 = (s - 1) % n, (s + m) % n
            ys = [idx[x] for x in lv(("y", 0))]
            x1s = [idx[x] for x in lv(("x", 1))]
            # the block must start with a y-leaf and end with an x_1-leaf, or the mirror image
            if not (block[0] in ys and block[-1] in x1s):
                if block[0] in x1s and block[-1] in ys:
                    Cc, B1 = B1, Cc
                else:
                    print("block structure wrong"); return False
            b1s = [idx[x] for x in lv(("b", 1))]
            ccs = [idx[x] for x in (lv(("c", 1)) if k2 >= 1 else lv(("b", kB)))]
            assert B1 in b1s and Cc in ccs, "B1/Cc not at b_1 / c_1 (b_kB)"
            M = range(2, kB + 1) if k2 >= 1 else range(2, kB)
            zs = [idx[x] for j in M for x in lv(("b", j))]
            assert zs and B1 not in zs and Cc not in zs
            d = D6
            for Y in ys:
                for X1 in x1s:
                    p1 = d[B1, Cc] + d[Y, X1]
                    if not (p1 > d[B1, Y] + d[Cc, X1] and p1 > d[B1, X1] + d[Cc, Y]):
                        print("(1) FAILS"); return False
                    if p1 - d[B1, Y] - d[Cc, X1] != -6 * pred:
                        print("identity for (1) FAILS", p1 - d[B1, Y] - d[Cc, X1], pred); return False
                    # P3: every circular split separating {Y,X1} from {B1,Cc}, other than S*, has weight 0
                    for (i, j), v in al.items():
                        Us = side(i, j)
                        a_in = (Y in Us, X1 in Us, B1 in Us, Cc in Us)
                        if a_in in ((True, True, False, False), (False, False, True, True)):
                            if Us != U and (full - Us) != U:
                                st["other_sep_splits_checked"] += 1
                                if v != 0:
                                    print("P3 FAILS: another split separating {Y,X1} from {B1,Cc} has weight", v); return False
                    for Z in zs:
                        st["quintuples"] += 1
                        p2 = d[B1, Cc] + d[Z, Y]
                        p3 = d[B1, Cc] + d[Z, X1]
                        if not (p2 > d[B1, Z] + d[Cc, Y] and p2 > d[B1, Y] + d[Z, Cc]):
                            print("(2) FAILS"); return False
                        if not (p3 > d[B1, Z] + d[Cc, X1] and p3 > d[B1, X1] + d[Z, Cc]):
                            print("(3) FAILS"); return False
    print(f"seed {seed}, max leaves {maxleaves}, all-order search up to {searchmax} leaves; {time.time()-t0:.0f}s")
    for k, v in st.items():
        print("  ", k, ":", v)
    print("ALL CHECKS PASSED")
    return True


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    count, seed, maxleaves, searchmax, targeted = (a + [300, 1, 11, 11, 0][len(a):])[:5]
    sys.exit(0 if main(count, seed, maxleaves, searchmax, targeted) else 1)
