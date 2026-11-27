# gen_l2.py -- REVIEW 6, referee's own generator of explicit rooted networks of level <= 2 that are
# outer-labeled planar: trees, level-1 cycles, galled level-2 blobs and nested level-2 blobs, glued along cut
# edges; a nested blob may be entered through the root on the path A, or through a cut edge at ANY b- or
# c-position (b_1, a middle one, b_kB, c_1, c_e).  Records the positions of every nested blob.
import random


class Builder:
    def __init__(self, rng, weights=None):
        self.net, self.cnt, self.rng, self.records = {}, 0, rng, []
        self.weights = weights or {"leaf": 6, "tree": 3, "cycle": 1, "galled2": 1, "nested": 2}

    def node(self, p):
        self.cnt += 1
        nm = f"{p}{self.cnt}"
        self.net[nm] = []
        return nm

    def leaf(self):
        self.cnt += 1
        nm = f"L{self.cnt:03d}"
        self.net[nm] = []
        return nm

    def split_budget(self, budget, parts):
        """random composition of budget into `parts` positive parts"""
        cuts = sorted(self.rng.sample(range(1, budget), parts - 1)) if parts > 1 else []
        return [b - a for a, b in zip([0] + cuts, cuts + [budget])]

    # returns (top node, leaves in planar order)
    def pendant(self, budget, depth, kinds=None):
        rng = self.rng
        opts = []
        w = self.weights
        if budget == 1:
            l = self.leaf()
            return l, [l]
        opts += ["tree"] * w["tree"]
        if budget >= 3 and depth < 4:
            opts += ["cycle"] * w["cycle"]
        if budget >= 4 and depth < 3:
            opts += ["galled2"] * w["galled2"]
        if budget >= 3 and depth < 3:
            opts += ["nested"] * w["nested"]
        kind = rng.choice(kinds) if kinds else rng.choice(opts)
        if kind == "tree":
            v = self.node("v")
            a, b = self.split_budget(budget, 2)
            t1, l1 = self.pendant(a, depth + 1)
            t2, l2 = self.pendant(b, depth + 1)
            self.net[v] += [t1, t2]
            return v, l1 + l2
        if kind == "cycle":
            # cycle with source r, left chain (s positions), right chain (t positions), hybrid with pendant
            maxpos = min(budget - 1, 4)
            npos = rng.randint(1, maxpos) if budget >= 3 else 1
            if npos < 2 and budget >= 3:
                npos = 2                      # at least a 4-cycle counting r... keep it a real cycle
            s = rng.randint(0, npos)
            t = npos - s
            sizes = self.split_budget(budget, npos + 1)
            r, h = self.node("v"), self.node("h")
            left = [self.node("v") for _ in range(s)]
            right = [self.node("v") for _ in range(t)]
            order = []
            chainL = [r] + left + [h]
            chainR = [r] + right + [h]
            if s == 0 and t == 0:
                raise AssertionError
            for u, v in zip(chainL, chainL[1:]):
                self.net[u].append(v)
            for u, v in zip(chainR, chainR[1:]):
                self.net[u].append(v)
            k = 0
            lo = []
            for nd in left:
                p, ls = self.pendant(sizes[k], depth + 1); k += 1
                self.net[nd].append(p); lo += ls
            p, lh = self.pendant(sizes[k], depth + 1); k += 1
            self.net[h].append(p)
            ro = []
            for nd in right:
                p, ls = self.pendant(sizes[k], depth + 1); k += 1
                self.net[nd].append(p); ro.append(ls)
            order = lo + lh
            for ls in reversed(ro):
                order += ls
            return r, order
        if kind == "galled2":
            # r -> u, r -> L1.. -> h1 ; u -> v ; u -> L2.. -> h2 ; v -> R2.. -> h2 ; v -> R1.. -> h1
            nL1, nR1, nL2, nR2 = (rng.randint(0, 1) for _ in range(4))
            while 2 + nL1 + nR1 + nL2 + nR2 > budget:
                nL1, nR1, nL2, nR2 = (rng.randint(0, 1) for _ in range(4))
            sizes = self.split_budget(budget, 2 + nL1 + nR1 + nL2 + nR2)
            r, u, v, h1, h2 = self.node("v"), self.node("v"), self.node("v"), self.node("h"), self.node("h")
            L1 = [self.node("v") for _ in range(nL1)]
            R1 = [self.node("v") for _ in range(nR1)]
            L2 = [self.node("v") for _ in range(nL2)]
            R2 = [self.node("v") for _ in range(nR2)]
            self.net[r].append(u)
            for chain in ([r] + L1 + [h1], [u, v], [u] + L2 + [h2], [v] + R2 + [h2], [v] + R1 + [h1]):
                for a, b in zip(chain, chain[1:]):
                    self.net[a].append(b)
            k = 0
            pend = {}
            for nd in L1 + [h1] + R1 + R2 + [h2] + L2:
                p, ls = self.pendant(sizes[k], depth + 1); k += 1
                self.net[nd].append(p)
                pend[nd] = ls
            order = []
            for nd in L1 + [h1] + R1[::-1] + R2 + [h2] + L2[::-1]:
                order += pend[nd]
            return r, order
        # nested blob entered through a cut edge at a b- or c-position
        for _ in range(200):
            kB, k1, k2 = rng.randint(1, 6), rng.randint(0, 2), rng.randint(0, 2)
            npos = kB + k1 + k2            # positions other than the entry
            if 2 <= npos <= budget:
                break
        else:
            return self.pendant(budget, depth, kinds=["tree"])
        entries = [("b", j) for j in range(1, kB + 1)] + [("c", e) for e in range(1, k2 + 1)]
        return self.nested(kB, k1, k2, rng.choice(entries), budget, depth)

    def nested(self, kB, k1, k2, entry, budget, depth, sizes=None, kinds=None, prebuilt=None):
        rng, net = self.rng, self.net
        h1, h2, t = self.node("h"), self.node("h"), self.node("t")
        vB = {j: self.node("vb") for j in range(1, kB + 1)}
        vX = {a: self.node("vx") for a in range(1, k1 + 1)}
        vC = {e: self.node("vc") for e in range(1, k2 + 1)}
        positions = [("b", j) for j in range(1, kB + 1)] + [("x", a) for a in range(1, k1 + 1)] + \
                    [("c", e) for e in range(1, k2 + 1)] + [("y", 0)]
        others = [p for p in positions if p != entry]
        if sizes is None:
            sz = self.split_budget(budget, len(others)) if rng.random() < 0.5 else None
            if sz is None:                       # mostly ones, a few larger
                sz = [1] * len(others)
                extra = budget - len(others)
                while extra > 0:
                    i = rng.randrange(len(others))
                    g = rng.randint(1, extra)
                    sz[i] += g
                    extra -= g
            sizes = dict(zip(others, sz))
        pend = {}
        for p in others:
            if prebuilt and p in prebuilt:
                pend[p] = prebuilt[p]
            else:
                pend[p] = self.pendant(sizes[p], depth + 1, kinds=(kinds if sizes[p] > 1 else None))
        chainX = [h1] + [vX[a] for a in range(1, k1 + 1)] + [h2]
        for u, v in zip(chainX, chainX[1:]):
            net[u].append(v)
        for name, chain, nodes in (("c", [t] + [vC[e] for e in range(k2, 0, -1)] + [h2], vC),
                                   ("b", [t] + [vB[j] for j in range(kB, 0, -1)] + [h1], vB)):
            if entry[0] == name:
                s = chain.index(nodes[entry[1]])
                for i in range(s, len(chain) - 1):
                    net[chain[i]].append(chain[i + 1])
                for i in range(s, 0, -1):
                    net[chain[i]].append(chain[i - 1])
            else:
                for u, v in zip(chain, chain[1:]):
                    net[u].append(v)
        for a in range(1, k1 + 1):
            net[vX[a]].append(pend[("x", a)][0])
        net[h2].append(pend[("y", 0)][0])
        for j in range(1, kB + 1):
            if entry != ("b", j):
                net[vB[j]].append(pend[("b", j)][0])
        for e in range(1, k2 + 1):
            if entry != ("c", e):
                net[vC[e]].append(pend[("c", e)][0])
        if entry == ("A",):
            top = self.node("r")
            net[top] += [t, h1]
        else:
            net[t].append(h1)
            top = vB[entry[1]] if entry[0] == "b" else vC[entry[1]]
        circ = [("b", j) for j in range(1, kB + 1)] + [("c", e) for e in range(k2, 0, -1)] + [("y", 0)] + \
               [("x", a) for a in range(k1, 0, -1)]
        if entry != ("A",):
            i = circ.index(entry)
            circ = circ[i + 1:] + circ[:i]
        order = []
        for p in circ:
            ls = pend[p][1]
            if rng.random() < 0.5:
                ls = ls[::-1]                    # a pendant subnetwork may be flipped
            order += ls
        self.records.append({"k": (kB, k1, k2), "entry": entry,
                             "pos": {p: (list(pend[p][1]) if p in pend else None) for p in positions}})
        return top, order


def random_network(rng, maxleaves, mode=None):
    B = Builder(rng)
    mode = mode or rng.choice(["A", "A", "cut", "cut", "cut", "generic"])
    n = rng.randint(7, maxleaves)
    if mode == "A":
        for _ in range(1000):
            kB, k1, k2 = rng.randint(3, 7), rng.randint(1, 3), rng.randint(0, 3)
            if kB + k1 + k2 + 1 <= n:
                break
        top, order = B.nested(kB, k1, k2, ("A",), n, 0)
    elif mode == "cut":
        for _ in range(1000):
            kB, k1, k2 = rng.randint(3, 7), rng.randint(1, 3), rng.randint(0, 3)
            if kB + k1 + k2 + 1 <= n:
                break
        entries = [("b", j) for j in range(1, kB + 1)] + [("c", e) for e in range(1, k2 + 1)]
        entry = rng.choice(entries)
        npos = kB + k1 + k2
        out = rng.randint(1, n - npos)
        top = B.node("r")
        t1, l1 = B.pendant(out, 1)
        t2, l2 = B.nested(kB, k1, k2, entry, n - out, 1)
        B.net[top] += [t1, t2]
        order = l1 + l2
    else:
        top = B.node("r")
        a = rng.randint(1, n - 1)
        t1, l1 = B.pendant(a, 0)
        t2, l2 = B.pendant(n - a, 0)
        B.net[top] += [t1, t2]
        order = l1 + l2
    return B.net, order, B.records, mode


def targeted_network(rng, maxleaves, entry_kind):
    """A nested blob with prescribed kind of entry and compound pendant subnetworks at y, x_1 and at the entry.
    entry_kind in {"A", "b1", "bmid", "bkB", "c1", "ce"}.  Sizes are chosen so that the critical weight is
    often negative."""
    B = Builder(rng, weights={"leaf": 1, "tree": 3, "cycle": 2, "galled2": 1, "nested": 2})
    for _ in range(10000):
        kB, k1, k2 = rng.randint(4, 7), rng.randint(1, 2), rng.randint(0, 2)
        if entry_kind in ("c1",) and k2 < 1:
            continue
        if entry_kind == "ce" and k2 < 2:
            continue
        positions = [("b", j) for j in range(1, kB + 1)] + [("x", a) for a in range(1, k1 + 1)] + \
                    [("c", e) for e in range(1, k2 + 1)] + [("y", 0)]
        entry = {"A": ("A",), "b1": ("b", 1), "bkB": ("b", kB), "c1": ("c", 1), "ce": ("c", k2),
                 "bmid": ("b", rng.randint(2, kB - 1))}[entry_kind]
        sizes = {p: 1 for p in positions}
        sizes[("y", 0)] = rng.choice([1, 2, 2, 3])
        sizes[("x", 1)] = rng.choice([1, 2, 2, 3])
        for j in range(2, kB + 1):
            if rng.random() < 0.3:
                sizes[("b", j)] = rng.choice([2, 3])
        out = 0
        if entry != ("A",):
            out = rng.choice([1, 2, 2, 3, 4])
            sizes[entry] = out
        tot = sum(sizes.values())
        if tot > maxleaves or tot < 7:
            continue
        beta = [sizes[("b", j)] for j in range(1, kB + 1)]
        gamma = [sizes[("c", e)] for e in range(1, k2 + 1)]
        xi = [sizes[("x", a)] for a in range(1, k1 + 1)]
        R = sizes[("y", 0)] + sum(xi[1:])
        if gamma:
            G, mid = sum(gamma), beta[1:]
        else:
            G, mid = beta[-1], beta[1:-1]
        s = sum(mid)
        val = beta[0] * G + xi[0] * R - (s * s - sum(v * v for v in mid)) // 2
        if val < 0 or rng.random() < 0.15:
            break
    else:
        raise RuntimeError("no parameters")
    if entry == ("A",):
        top, order = B.nested(kB, k1, k2, entry, tot, 0, sizes=dict(sizes))
    else:
        inner_sizes = {p: v for p, v in sizes.items() if p != entry}
        top = B.node("r")
        t1, l1 = B.pendant(out, 1)
        t2, l2 = B.nested(kB, k1, k2, entry, tot - out, 1, sizes=inner_sizes)
        B.net[top] += [t1, t2]
        order = l1 + l2
    return B.net, order, B.records, "T:" + entry_kind
