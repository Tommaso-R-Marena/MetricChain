# c1_survey.py -- REVIEW 6, referee's own re-enumeration for NANUQ_HIGHER_LEVELS.md section 2.
# Rooted binary networks on leaves 0..5, outer-labeled planar for the circular order (0,...,5), obtained from the
# rooted planar trees by k hybrid insertions (two different edges a->b, c->d, d not an ancestor-or-equal of a).
# Own code throughout (trees, insertion, planarity by the wheel test, switchings, split systems).
# Two identifications of networks are computed side by side:
#   KEY  the "unfolding with hybrid nodes marked" (the identification the authors use),
#   INV  a refinement: the multiset over nodes of (bottom-up key, top-down context), an isomorphism invariant that
#        separates networks which only differ in how equal-looking nodes are wired.
# If #INV > #KEY at some level, the unfolding key identifies non-isomorphic networks.
# Usage: python3 c1_survey.py KMAX [sym]
import sys, time, itertools, hashlib
import networkx as nx

N = 6
FULL = (1 << N) - 1
INTERVALS = set()
for i in range(N):
    for ln in range(1, N):
        m = 0
        for t in range(ln):
            m |= 1 << ((i + t) % N)
        INTERVALS.add(m)
DIH = []
for r in range(N):
    for refl in (0, 1):
        DIH.append(tuple((((-q) % N if refl else q) + r) % N for q in range(N)))


def planar_rooted_trees():
    """all rooted binary trees whose clusters are intervals of the circular order; nested tuples, canonical"""
    def build(seq):
        if len(seq) == 1:
            return [seq[0]]
        res = []
        for cut in range(1, len(seq)):
            for l in build(seq[:cut]):
                for r in build(seq[cut:]):
                    res.append((l, r))
        return res

    def canon(t):
        if isinstance(t, int):
            return t
        a, b = canon(t[0]), canon(t[1])
        return (a, b) if repr(a) <= repr(b) else (b, a)
    seen = {}
    for rot in range(N):
        seq = [(rot + i) % N for i in range(N)]
        for t in build(seq):
            c = canon(t)
            seen[repr(c)] = c
    nets = []
    for c in seen.values():
        net, cnt = {}, [N]

        def add(x):
            if isinstance(x, int):
                net[x] = ()
                return x
            me = cnt[0]
            cnt[0] += 1
            net[me] = (add(x[0]), add(x[1]))
            return me
        root = add(c)
        nets.append((net, root))
    return nets


def parents(net):
    par = {v: [] for v in net}
    for v, ch in net.items():
        for c in ch:
            par[c].append(v)
    return par


def topo_children_first(net, root):
    order, seen = [], set()
    st = [(root, 0)]
    while st:
        v, i = st.pop()
        if i == 0:
            if v in seen:
                continue
            seen.add(v)
        ch = net[v]
        if i < len(ch):
            st.append((v, i + 1))
            if ch[i] not in seen:
                st.append((ch[i], 0))
        else:
            order.append(v)
    return order


def keys_of(net, root, order, ren=None):
    key = {}
    for v in order:
        ch = net[v]
        if not ch:
            key[v] = str(v if ren is None else ren[v])
        elif len(ch) == 1:
            key[v] = "[" + key[ch[0]] + "]"
        else:
            a, b = key[ch[0]], key[ch[1]]
            key[v] = "(" + (a + "," + b if a <= b else b + "," + a) + ")"
    return key


def inv_of(net, root, order, par, ren=None):
    key = keys_of(net, root, order, ren)
    up = {}
    for v in reversed(order):                 # parents before children
        if v == root:
            up[v] = "R"
        else:
            up[v] = "{" + "|".join(sorted(up[p] + "^" + key[p] for p in par[v])) + "}"
    return key[root], hashlib.md5("#".join(sorted(key[v] + "@" + up[v] for v in net)).encode()).hexdigest()   # deterministic across processes


def system_of(net, root, order, par):
    hyb = [v for v in net if len(par[v]) == 2]
    out = set()
    for choice in itertools.product((0, 1), repeat=len(hyb)):
        keep = {h: par[h][c] for h, c in zip(hyb, choice)}
        mask = {}
        for v in order:
            ch = net[v]
            if not ch:
                mask[v] = 1 << v
                continue
            m = 0
            for c in ch:
                if c in keep and keep[c] != v:
                    continue
                m |= mask[c]
            mask[v] = m
            if m and m != FULL:
                co = FULL ^ m
                if (m & (m - 1)) and (co & (co - 1)):
                    if m not in INTERVALS:
                        return None
                    out.add(min(m, co))
    return frozenset(out)


def wheel_planar(net):
    G = nx.Graph()
    for v, ch in net.items():
        for c in ch:
            G.add_edge(v, c)
    for q in range(N):
        G.add_edge(q, (q + 1) % N)
        G.add_edge("apex", q)
    return nx.check_planarity(G)[0]


def insertions(net, root, order):
    desc = {}
    for v in order:
        s = set()
        for c in net[v]:
            s.add(c)
            s |= desc[c]
        desc[v] = s
    edges = [(a, b) for a in net for b in net[a]]
    nxt = max(net) + 1
    for (a, b) in edges:
        for (c, d) in edges:
            if (a, b) == (c, d):
                continue
            if a == d or a in desc[d]:
                continue
            new = dict(net)
            p, h = nxt, nxt + 1
            new[a] = tuple(p if x == b else x for x in net[a])
            new[p] = (b, h)
            cc = new[c]                       # c may be a (already changed) or p? (c,d) is an old edge; if c == a use the new tuple
            new[c] = tuple(h if x == d else x for x in cc)
            new[h] = (d,)
            yield new


def image_system(s, g):
    out = set()
    for m in s:
        mm = 0
        for q in range(N):
            if (m >> q) & 1:
                mm |= 1 << g[q]
        out.add(min(mm, FULL ^ mm))
    return frozenset(out)


def main(kmax, sym):
    t0 = time.time()
    level = {}
    invs = set()
    systems = {}
    for net, root in planar_rooted_trees():
        order = topo_children_first(net, root)
        par = parents(net)
        if sym:
            cands = [inv_of(net, root, order, par, g) for g in DIH]
            k = min(c[0] for c in cands)
            iv = min(cands)
        else:
            k, h = inv_of(net, root, order, par)
            iv = (k, h)
        level[k] = (net, root)
        invs.add(iv)
    def record(net, root, order, par, k):
        s = system_of(net, root, order, par)
        if sym:
            for g in DIH:
                systems.setdefault(image_system(s, g), k)
        else:
            systems.setdefault(s, k)
        return s
    labelled = 0
    for key, (net, root) in level.items():
        order = topo_children_first(net, root)
        par = parents(net)
        record(net, root, order, par, 0)
        if sym:
            labelled += len({inv_of(net, root, order, par, g) for g in DIH})
    print(f"k=0: networks by KEY {len(level)}, by INV {len(invs)}" + (f", labelled (sum of orbit sizes) {labelled}" if sym else "") +
          f"; systems so far {len(systems)}  [{time.time()-t0:.0f}s]", flush=True)
    for k in range(1, kmax + 1):
        nxt, invs = {}, set()
        nonplanar = set()
        labelled = 0
        for key, (net, root) in level.items():
            order0 = topo_children_first(net, root)
            for new in insertions(net, root, order0):
                order = topo_children_first(new, root)
                par = parents(new)
                if sym:
                    cands = [inv_of(new, root, order, par, g) for g in DIH]
                    kk = min(c[0] for c in cands)
                    iv = min(cands)
                else:
                    kk, h = inv_of(new, root, order, par)
                    iv = (kk, h)
                if kk in nxt:
                    if iv not in invs:
                        # same KEY as a kept network, different INV: is it planar too?
                        if iv in nonplanar:
                            continue
                        if system_of(new, root, order, par) is not None and wheel_planar(new):
                            invs.add(iv)
                        else:
                            nonplanar.add(iv)
                    continue
                if iv in nonplanar:
                    continue
                s = system_of(new, root, order, par)
                if s is None or not wheel_planar(new):
                    nonplanar.add(iv)
                    continue
                nxt[kk] = (new, root)
                invs.add(iv)
                record(new, root, order, par, k)
                if sym:
                    labelled += len({inv_of(new, root, order, par, g)[0] for g in DIH})
        level = nxt
        print(f"k={k}: networks by KEY {len(level)}, by INV {len(invs)}" + (f", labelled by KEY (sum of orbit sizes) {labelled}" if sym else "") +
              f"; systems so far {len(systems)}  [{time.time()-t0:.0f}s]", flush=True)
    return systems


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    sym = len(sys.argv) > 2 and sys.argv[2] == "sym"
    systems = main(kmax, sym)
    import pickle
    pickle.dump(systems, open(f"systems_k{kmax}{'_sym' if sym else ''}.pkl", "wb"))
