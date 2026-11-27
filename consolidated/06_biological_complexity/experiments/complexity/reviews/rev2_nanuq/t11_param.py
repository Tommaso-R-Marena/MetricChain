"""Sanity check (NOT a full audit) of Theorem 11, which was added to the working paper during this review.
Parametric quartet distance d_rho, rho = (c, s, a, o), computed from explicit networks with the referee's code:
  one displayed quartet on {x,y,z,w}: rho_c for its cherries, rho_s for the other pairs;
  two displayed (planar) quartets:    rho_a for pairs that are a cherry in one of them, rho_o for the two others.
"""
import sys, pickle, random
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import rnet, gen

CH = {0: ((0, 1), (2, 3)), 1: ((0, 2), (1, 3)), 2: ((0, 3), (1, 2))}

def param_metric(n, quads, Qsets, rho):
    c, s, a, o = rho
    D = [[F(0) if x == y else F(2 * n - 4) for y in range(n)] for x in range(n)]
    for q, qs in zip(quads, Qsets):
        assert len(qs) in (1, 2)
        for i, j in combinations(range(4), 2):
            k = sum(1 for t in qs if (i, j) in CH[t])
            if len(qs) == 1:
                val = c if k == 1 else s
            else:
                val = a if k == 1 else o
            D[q[i]][q[j]] += 2 * val
            D[q[j]][q[i]] += 2 * val
    return D

def verdict(net, order, rho):
    L, per_tree, quads, Qsets = gen.displayed_fast(net)
    n = len(L)
    D = param_metric(n, quads, Qsets, rho)
    pos = {l: i for i, l in enumerate(order)}
    full = (1 << n) - 1
    sigma = set()
    for sp in per_tree:
        for m in sp:
            mm = 0
            for i, l in enumerate(L):
                if (m >> i) & 1:
                    mm |= 1 << pos[l]
            sigma.add(mm if not (mm & 1) else full ^ mm)
    li = [L.index(l) for l in order]
    neg = supp = False
    for i in range(n):
        for j in range(i + 1, n):
            al = (D[li[i]][li[j]] + D[li[(i + 1) % n]][li[(j + 1) % n]]
                  - D[li[i]][li[(j + 1) % n]] - D[li[(i + 1) % n]][li[j]])
            m = 0
            for p in range(i + 1, j + 1):
                m |= 1 << p
            m = m if not (m & 1) else full ^ m
            if al < 0:
                neg = True
            if (al > 0) != (m in sigma):
                supp = True
    return "neg" if neg else ("support" if supp else "ok")

if __name__ == "__main__":
    # (c) the 8-leaf level-1 witness of the working paper
    NET = {"r": ["c1", "c2"], "c1": ["k1", "c0"], "k1": ["l1", "l1b"], "c0": ["l0", "h"],
           "c2": ["k2", "c3"], "k2": ["l2", "l2b"], "c3": ["l3", "h"], "h": ["kx"], "kx": ["l4", "l5"],
           "l0": [], "l1": [], "l1b": [], "l2": [], "l2b": [], "l3": [], "l4": [], "l5": []}
    ORDER = ["l0", "l1", "l1b", "l2", "l2b", "l3", "l4", "l5"]
    print("witness: LSA", rnet.is_lsa_network(NET), "| level", rnet.level(NET), "| galled", rnet.is_galled_def(NET),
          "| OLP order", rnet.planar_circular_order(NET))
    L, per_tree, quads, Qsets = gen.displayed_fast(NET)
    for name, rho in (("NANUQ", (F(0), F(1), F(1, 2), F(1))), ("Modified NANUQ", (F(1, 2), F(1), F(1, 2), F(1)))):
        D = param_metric(8, quads, Qsets, rho)
        d = {(x, y): D[i][j] for i, x in enumerate(L) for j, y in enumerate(L)}
        al = rnet.alphas(d, ORDER)
        good, total = rnet.kalmanson_orders(d, L)
        print(f"   {name}: alpha(l4 l5 | rest) = {al[frozenset(('l4', 'l5'))]}, min alpha = {min(al.values())}, "
              f"verdict (planar order) = {verdict(NET, ORDER, rho)}, Kalmanson orders: {len(good)} of {total}")

    # sufficiency / necessity spot checks on the referee's networks
    rng = random.Random(1)
    nets = []
    for fn in sys.argv[1:]:
        nets += pickle.load(open(fn, "rb"))
    rng.shuffle(nets)
    nets = nets[:12000]
    leafchild = [t for t in nets if t[2]["nonleaf_hyb_children"] == 0]
    print("networks used:", len(nets), "| with all hybrids having leaf children:", len(leafchild))
    tests = [
        ("in cone (a): NANUQ (0,1,1/2,1)", (F(0), F(1), F(1, 2), F(1))),
        ("in cone (a): (1/5,1,7/10,1)", (F(1, 5), F(1), F(7, 10), F(1))),
        ("in cone (a), boundary c+s=2a: (1/2,1,3/4,1)", (F(1, 2), F(1), F(3, 4), F(1))),
        ("in cone (a): (0,1,9/10,1)", (F(0), F(1), F(9, 10), F(1))),
        ("in cone (a), scaled: (1,3,5/2,3)", (F(1), F(3), F(5, 2), F(3))),
        ("Modified NANUQ (1/2,1,1/2,1): in (b), not in (a)", (F(1, 2), F(1), F(1, 2), F(1))),
        ("outside: o != s (0,1,1/2,11/10)", (F(0), F(1), F(1, 2), F(11, 10))),
        ("outside: o != s (0,1,1/2,9/10)", (F(0), F(1), F(1, 2), F(9, 10))),
        ("outside: a = s (0,1,1,1)", (F(0), F(1), F(1), F(1))),
        ("outside: 2a < s (0,1,2/5,1)", (F(0), F(1), F(2, 5), F(1))),
        ("outside (b): c > a (7/10,1,3/5,1)", (F(7, 10), F(1), F(3, 5), F(1))),
    ]
    for name, rho in tests:
        c_all = Counter(verdict(net, order, rho) for net, order, f, st in nets)
        c_leaf = Counter(verdict(net, order, rho) for net, order, f, st in leafchild[:6000])
        print(f"   {name}: all networks {dict(c_all)} | leaf-child networks {dict(c_leaf)}", flush=True)
