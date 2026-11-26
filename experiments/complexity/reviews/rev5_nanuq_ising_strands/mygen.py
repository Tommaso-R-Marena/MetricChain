# mygen.py -- REVIEWER'S OWN CODE: generators of explicit rooted binary networks
# (hybrid-arc insertion into trees; no use of the note's structure lemmas)
import random, itertools
from mynet import Net


def random_tree_children(n, rng):
    """random rooted binary tree on leaves 0..n-1 as a children dict; root 'r0'"""
    ch = {'r0': [0, 1]}
    cnt = [0]
    def newnode():
        cnt[0] += 1
        return 'i%d' % cnt[0]
    edges = [('r0', 0), ('r0', 1)]
    for x in range(2, n):
        k = rng.randrange(len(edges) + 1)
        if k == len(edges):          # new root above
            # find current root
            root = [u for u in ch if all(u not in vs for vs in ch.values())][0]
            nr = newnode()
            ch[nr] = [root, x]
            edges += [(nr, root), (nr, x)]
        else:
            u, v = edges[k]
            w = newnode()
            ch[u][ch[u].index(v)] = w
            ch[w] = [v, x]
            edges[k] = (u, w)
            edges += [(w, v), (w, x)]
    root = [u for u in ch if all(u not in vs for vs in ch.values())][0]
    return ch, root


def edge_list(ch, root):
    """list of edges as (u, index of child in ch[u]); plus the virtual root edge (None, None)"""
    out = []
    for u, vs in ch.items():
        for k in range(len(vs)):
            out.append((u, k))
    return out


class Counter:
    def __init__(self):
        self.c = 0
    def new(self, pre):
        self.c += 1
        return '%s%d' % (pre, self.c)


def insert_arc(ch, root, e1, e2, cnt):
    """subdivide edge e1 by a new node u, edge e2 by a new node v, add the arc u -> v.
    e1 may be the virtual root edge (None): then a new root is created above the root.
    e1 == e2: u is placed above v on the same edge (parallel edges result).
    returns (children dict, root) -- a new dict; no validity test here."""
    ch = {a: list(b) for a, b in ch.items()}
    u = cnt.new('t')
    v = cnt.new('h')
    if e1 is None:
        a2, k2 = e2
        c2 = ch[a2][k2]
        ch[a2][k2] = v
        ch[v] = [c2]
        ch[u] = [root, v]
        return ch, u
    a1, k1 = e1
    a2, k2 = e2
    if e1 == e2:
        c = ch[a1][k1]
        ch[a1][k1] = u
        ch[u] = [v, v]
        ch[v] = [c]
        return ch, root
    c1 = ch[a1][k1]
    c2 = ch[a2][k2]
    ch[a1][k1] = u
    ch[u] = [c1, v]
    ch[a2][k2] = v
    ch[v] = [c2]
    return ch, root


def tree_shapes(n):
    """all rooted binary tree shapes with n leaves (leaves labelled 0..n-1 arbitrarily),
    as (children dict, root)"""
    memo = {}
    def shapes(k):
        if k in memo:
            return memo[k]
        if k == 1:
            res = ['L']
        else:
            res = []
            for a in range(1, k // 2 + 1):
                b = k - a
                for i, s in enumerate(shapes(a)):
                    for j, t in enumerate(shapes(b)):
                        if a == b and j < i:
                            continue
                        res.append((s, t))
        memo[k] = res
        return res
    out = []
    for s in shapes(n):
        ch = {}
        cnt = [0, 0]
        def build(t):
            if t == 'L':
                x = cnt[0]; cnt[0] += 1
                return x
            cnt[1] += 1
            name = 'i%d' % cnt[1]
            a = build(t[0]); b = build(t[1])
            ch[name] = [a, b]
            return name
        root = build(s)
        out.append((ch, root))
    return out
