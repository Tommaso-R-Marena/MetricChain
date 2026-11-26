#!/usr/bin/env python3
"""ER2: E15T(a), the sentence "for a nearest-neighbour reference on a tree ordered with parents first, h_i depends
on the parent of i only".  h_i(x_<i) = mu*(e_i = 0 | e_<i).  Checked on random trees with 5 and 6 sites (random
couplings K >= 0 in the e-variables, random fields and slopes), every order in which each site comes after
its parent; and one order that violates 'parents first' as a control."""
import itertools
import numpy as np
rng = np.random.default_rng(1504)


def h_table(E, mustar, order):
    out = []
    for pos, i in enumerate(order):
        prev = list(order[:pos]); tab = {}
        for e in itertools.product((0, 1), repeat=len(prev)):
            same = np.all(E[:, prev] == np.array(e), axis=1) if prev else np.ones(len(E), dtype=bool)
            tab[e] = mustar[same & (E[:, i] == 0)].sum() / mustar[same].sum()
        out.append((i, prev, tab))
    return out


worst = 0.0; cnt = 0; control = 0.0
for n in (5, 6):
    E = np.array(list(itertools.product((0, 1), repeat=n)))
    for _ in range(6):
        parent = [-1] + [int(rng.integers(i)) for i in range(1, n)]            # random recursive tree rooted at 0
        K = np.zeros((n, n))
        for i in range(1, n):
            K[parent[i], i] = abs(rng.normal()) * 1.5
        th = rng.normal(size=n); bs = rng.uniform(0.3, 2.0, size=n)
        lp = np.array([sum(K[i, j] * e[i] * e[j] for i in range(n) for j in range(n)) + (th - bs) @ e for e in E])
        mustar = np.exp(lp - lp.max()); mustar /= mustar.sum()
        for order in itertools.permutations(range(n)):
            pos = {v: k for k, v in enumerate(order)}
            if any(pos[parent[i]] > pos[i] for i in range(1, n)):
                continue
            for i, prev, tab in h_table(E, mustar, order):
                if parent[i] < 0:
                    continue
                pp = prev.index(parent[i])
                for val in (0, 1):
                    vs = [v for e, v in tab.items() if e[pp] == val]
                    worst = max(worst, max(vs) - min(vs))
            cnt += 1
        # control: put a leaf's parent AFTER the leaf's sibling subtree is conditioned on -- order with a child before its parent
        order = tuple(range(n - 1, -1, -1))
        for i, prev, tab in h_table(E, mustar, order):
            if not prev:
                continue
            for q in prev:
                pp = prev.index(q)
                for val in (0, 1):
                    vs = [v for e, v in tab.items() if e[pp] == val]
                    control = max(control, max(vs) - min(vs))
print(f"{cnt} (tree, parents-first order) pairs on 5 and 6 sites: largest variation of h_i at a fixed state of the parent = {worst:.2e}")
print(f"control (reverse order, children first): largest variation of h_i at a fixed state of one conditioning site = {control:.2e}")
