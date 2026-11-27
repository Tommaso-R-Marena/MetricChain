# chk.py -- REVIEW 6: the checks of t1_thm12prime.py as a function (same logic), for other drivers.
import itertools
import numpy as np
import networkx as nx
from rn import Net, alphas, is_kalmanson, kalmanson_search


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


def new_stats():
    return dict(networks=0, with_negative=0, negative_splits=0, searched=0, quintuples=0, kalm_for_C=0,
                zero_crit=0, nonleaf_pos_neg=0, nested_blobs=0, max_n=0, several_neg=0,
                other_sep_splits_checked=0, neg_blob_inside_pos={})


def check(net, order, records, st, searchmax, verbose=False):
    N = Net(net)
    n = N.n
    assert N.valid(), "invalid network"
    assert sorted(order) == N.leaves
    assert N.level() <= 2, "level > 2"
    assert wheel_ok(N, order), "constructed order is not an outer-labeled planar order"
    st["networks"] += 1
    st["max_n"] = max(st["max_n"], n)
    st["nested_blobs"] += len(records)
    D6 = N.nanuq6(order)
    al = alphas(D6, list(range(n)))
    neg = {k: v for k, v in al.items() if v < 0}
    disp = N.displayed_splits(order)
    idx = {x: i for i, x in enumerate(order)}
    full = frozenset(range(n))

    def side(i, j):
        return frozenset(range(i + 1, j + 1))
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
        inside = set(lvd[("y", 0)])
        for a in range(1, k1 + 1):
            inside |= set(lvd[("x", a)])
        U = frozenset(idx[x] for x in inside)
        beta = [len(lvd[("b", j)]) for j in range(1, kB + 1)]
        gamma = [len(lvd[("c", e)]) for e in range(1, k2 + 1)]
        xi = [len(lvd[("x", a)]) for a in range(1, k1 + 1)]
        pred = formula(beta, xi, len(lvd[("y", 0)]), gamma)
        crit[U] = (pred, rc, lvd)
    for (i, j), v in al.items():
        U = side(i, j)
        key = U if U in crit else (full - U if (full - U) in crit else None)
        isdisp = frozenset((frozenset(order[q] for q in U), frozenset(order[q] for q in full - U))) in disp
        if key is not None:
            if v != 6 * crit[key][0]:
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
        return True
    st["with_negative"] += 1
    st["negative_splits"] += len(neg)
    st["several_neg"] += len(neg) > 1
    if n <= searchmax:
        st["searched"] += 1
        r = kalmanson_search(D6)
        if r is not None:
            print("COUNTEREXAMPLE TO THEOREM 12': Kalmanson order found", [order[i] for i in r], net); return False
    for U, (pred, rc, lvd) in crit.items():
        if pred >= 0:
            continue
        kB, k1, k2 = rc["k"]
        st["nonleaf_pos_neg"] += any(len(lvd[p]) > 1 for p in rc["pos"])
        m = len(U)
        s = next(i for i in range(n) if i in U and (i - 1) % n not in U)
        block = [(s + i) % n for i in range(m)]
        assert set(block) == set(U)
        Cc, B1 = (s - 1) % n, (s + m) % n
        ys = [idx[x] for x in lvd[("y", 0)]]
        x1s = [idx[x] for x in lvd[("x", 1)]]
        if not (block[0] in ys and block[-1] in x1s):
            if block[0] in x1s and block[-1] in ys:
                Cc, B1 = B1, Cc
            else:
                print("block structure wrong"); return False
        b1s = [idx[x] for x in lvd[("b", 1)]]
        ccs = [idx[x] for x in (lvd[("c", 1)] if k2 >= 1 else lvd[("b", kB)])]
        assert B1 in b1s and Cc in ccs, "B1/Cc not at b_1 / c_1 (b_kB)"
        M = range(2, kB + 1) if k2 >= 1 else range(2, kB)
        zs = [idx[x] for j in M for x in lvd[("b", j)]]
        assert zs and B1 not in zs and Cc not in zs
        d = D6
        for Y in ys:
            for X1 in x1s:
                p1 = d[B1, Cc] + d[Y, X1]
                if not (p1 > d[B1, Y] + d[Cc, X1] and p1 > d[B1, X1] + d[Cc, Y]):
                    print("(1) FAILS"); return False
                if p1 - d[B1, Y] - d[Cc, X1] != -6 * pred:
                    print("identity for (1) FAILS"); return False
                for (i, j), v in al.items():
                    Us = side(i, j)
                    a_in = (Y in Us, X1 in Us, B1 in Us, Cc in Us)
                    if a_in in ((True, True, False, False), (False, False, True, True)):
                        if Us != U and (full - Us) != U:
                            st["other_sep_splits_checked"] += 1
                            if v != 0:
                                print("P3 FAILS"); return False
                for Z in zs:
                    st["quintuples"] += 1
                    p2 = d[B1, Cc] + d[Z, Y]
                    p3 = d[B1, Cc] + d[Z, X1]
                    if not (p2 > d[B1, Z] + d[Cc, Y] and p2 > d[B1, Y] + d[Z, Cc]):
                        print("(2) FAILS"); return False
                    if not (p3 > d[B1, Z] + d[Cc, X1] and p3 > d[B1, X1] + d[Z, Cc]):
                        print("(3) FAILS"); return False
    return True
