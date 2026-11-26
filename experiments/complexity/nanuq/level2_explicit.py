"""Theorem 12 of docs/complexity/NANUQ_LOCAL_CRITERION.md tested on EXPLICIT ROOTED NETWORKS.

Uses only netcalc.py (explicit DAG -> switchings -> displayed trees -> quartets -> NANUQ metric of Def. 4.1); nothing
of the split-system programs, in particular not the four-tree description of the nested blob (level2_nongalled.py).

A random network of level <= 2 is built from
  * nested level-2 blobs: theta graph with branch nodes h1 (hybrid; paths A, B enter, path C leaves) and t, second
    hybrid h2 inside C, no position on A; positions b_1..b_kB on B (b_1 next to h1), x_1..x_k1 on C between h1 and
    h2 (x_1 next to h1), y below h2, c_1..c_k2 on C between h2 and t (c_1 next to h2); the blob is entered through
    the root placed on A, or through a cut edge at a b-position or a c-position;
  * level-1 cycles, trees and leaves as pendant subnetworks.
For every nested blob with k1 >= 1 and kB >= 2 the weight of the split
      S* = (leaves at the x- and y-positions) | (all other leaves)
is compared with       beta_1 * G + xi_1 * R - e2(middle)        (sizes of the positions; see the note),
and every other circular split must have weight >= 0, positive exactly when it is displayed.

Usage: python3 level2_explicit.py [number of networks [seed [max leaves]]]     (defaults 300, 1, 11)
"""
import random
import sys
from netcalc import validate, leaves_of, nanuq_metric, split_weights, outer_labeled_planar_order, blobs_and_level, \
    is_galled


def e2(vals):
    s = sum(vals)
    return (s * s - sum(v * v for v in vals)) // 2


def formula(beta, xi, eta, gamma):
    R = eta + sum(xi[1:])
    if gamma:
        G, middle = sum(gamma), beta[1:]
    else:
        G, middle = beta[-1], beta[1:-1]
    return beta[0] * G + xi[0] * R - e2(middle)


class Builder:
    def __init__(self, rng):
        self.net, self.cnt, self.rng, self.records = {}, 0, rng, []

    def node(self, prefix):
        self.cnt += 1
        name = f"{prefix}{self.cnt}"
        self.net[name] = []
        return name

    def leaf(self):
        self.cnt += 1
        name = f"L{self.cnt:03d}"
        self.net[name] = []
        return name

    # ---- pendant subnetworks: return (top node, leaves in planar order) -------------------------------------
    def pendant(self, budget, depth):
        rng = self.rng
        kinds = ["leaf"] * 5
        if budget >= 2:
            kinds += ["tree"] * 2
        if budget >= 3 and depth < 3:
            kinds += ["cycle"]
        if budget >= 4 and depth < 2:
            kinds += ["nested"] * 2
        kind = rng.choice(kinds)
        if kind == "leaf":
            l = self.leaf()
            return l, [l]
        if kind == "tree":
            v = self.node("v")
            left = rng.randint(1, budget - 1)
            t1, l1 = self.pendant(left, depth + 1)
            t2, l2 = self.pendant(budget - left, depth + 1)
            self.net[v] += [t1, t2]
            return v, l1 + l2
        if kind == "cycle":
            r, a, b, h = self.node("v"), self.node("v"), self.node("v"), self.node("h")
            p1, l1 = self.pendant(1, depth + 1)
            p3, l3 = self.pendant(max(1, budget - 2), depth + 1)
            p2, l2 = self.pendant(1, depth + 1)
            self.net[r] += [a, b]
            self.net[a] += [p1, h]
            self.net[b] += [h, p2]
            self.net[h] += [p3]
            return r, l1 + l3 + l2
        # nested blob entered through a cut edge at a b- or c-position
        while True:
            kB, k1, k2 = rng.randint(1, 4), rng.randint(0, 2), rng.randint(0, 2)
            npos = kB + k1 + k2 + 1 - 1            # positions other than the entry
            if 2 <= npos <= budget:
                break
        entries = [("b", j) for j in range(1, kB + 1)] + [("c", e) for e in range(1, k2 + 1)]
        return self.nested(kB, k1, k2, rng.choice(entries), budget, depth)

    # ---- the nested blob ------------------------------------------------------------------------------------
    def nested(self, kB, k1, k2, entry, budget, depth):
        rng, net = self.rng, self.net
        h1, h2, t = self.node("h"), self.node("h"), self.node("t")
        vB = {j: self.node("vb") for j in range(1, kB + 1)}
        vX = {a: self.node("vx") for a in range(1, k1 + 1)}
        vC = {e: self.node("vc") for e in range(1, k2 + 1)}
        positions = [("b", j) for j in range(1, kB + 1)] + [("x", a) for a in range(1, k1 + 1)] + \
                    [("c", e) for e in range(1, k2 + 1)] + [("y", 0)]
        others = [p for p in positions if p != entry]
        extra = budget - len(others)
        pend = {}
        for p in others:
            give = rng.randint(0, extra) if extra > 0 and rng.random() < 0.35 else 0
            extra -= give
            pend[p] = self.pendant(1 + give, depth + 1)
        chainX = [h1] + [vX[a] for a in range(1, k1 + 1)] + [h2]
        for u, v in zip(chainX, chainX[1:]):
            net[u].append(v)
        for a in range(1, k1 + 1):
            net[vX[a]].append(pend[("x", a)][0])
        net[h2].append(pend[("y", 0)][0])
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
            for idx, nd in nodes.items():
                if entry != (name, idx):
                    net[nd].append(pend[(name, idx)][0])
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
            order += pend[p][1]
        self.records.append({"k": (kB, k1, k2), "entry": entry,
                             "b": [pend.get(("b", j), (None, None))[1] for j in range(1, kB + 1)],
                             "x": [pend[("x", a)][1] for a in range(1, k1 + 1)],
                             "c": [pend.get(("c", e), (None, None))[1] for e in range(1, k2 + 1)],
                             "y": pend[("y", 0)][1]})
        return top, order


def random_network(rng, maxleaves):
    B = Builder(rng)
    if rng.random() < 0.6:
        while True:
            kB, k1, k2 = rng.randint(0, 6), rng.randint(0, 3), rng.randint(0, 3)
            if 4 <= kB + k1 + k2 + 1 <= maxleaves:
                break
        top, order = B.nested(kB, k1, k2, ("A",), maxleaves, 0)
    else:
        top = B.node("r")
        left = rng.randint(1, maxleaves - 4)
        t1, l1 = B.pendant(left, 0)
        t2, l2 = B.pendant(maxleaves - left, 0)
        B.net[top] += [t1, t2]
        order = l1 + l2
    return B.net, order, B.records


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    maxleaves = int(sys.argv[3]) if len(sys.argv) > 3 else 11
    rng = random.Random(seed)
    done = ok = 0
    stats = {"nested blobs": 0, "critical splits": 0, "critical <= 0": 0, "not galled": 0, "max leaves": 0,
             "several blobs": 0, "other splits checked": 0}
    allok = True
    while done < count:
        net, order, records = random_network(rng, maxleaves)
        L = leaves_of(net)
        if len(L) < 5 or not records:
            continue
        validate(net)
        comps, levels = blobs_and_level(net)
        assert max(levels) <= 2
        assert outer_labeled_planar_order(net) is not None
        done += 1
        stats["max leaves"] = max(stats["max leaves"], len(L))
        stats["not galled"] += not is_galled(net)
        stats["several blobs"] += len(comps) > 1
        d, splits = nanuq_metric(net)
        Lset = frozenset(L)
        for s in splits:                       # every displayed split is an interval of the order used
            A = next(iter(s))
            idx = sorted(order.index(l) for l in A)
            comp = sorted(order.index(l) for l in Lset - A)
            assert idx == list(range(idx[0], idx[-1] + 1)) or comp == list(range(comp[0], comp[-1] + 1))
        w = split_weights(d, order)
        special = {}
        for rc in records:
            kB, k1, k2 = rc["k"]
            stats["nested blobs"] += 1
            inside = set(rc["y"])
            for lst in rc["x"]:
                inside |= set(lst)
            named = set(inside)
            for lst in rc["b"] + rc["c"]:
                if lst is not None:
                    named |= set(lst)
            outside = len(L) - len(named)       # size of the entry position, if any
            beta = [len(lst) if lst is not None else outside for lst in rc["b"]]
            gamma = [len(lst) if lst is not None else outside for lst in rc["c"]]
            xi = [len(lst) for lst in rc["x"]]
            if k1 >= 1 and kB >= 2:
                special[frozenset(inside)] = formula(beta, xi, len(rc["y"]), gamma)
        for U, a in w.items():
            V = Lset - U
            key = U if U in special else (V if V in special else None)
            disp = frozenset([U, V]) in splits
            if key is not None:
                stats["critical splits"] += 1
                stats["critical <= 0"] += special[key] <= 0
                good = (a == special[key]) and disp
            else:
                stats["other splits checked"] += 1
                good = a >= 0 and ((a > 0) == disp)
            if not good:
                allok = False
                print("MISMATCH", sorted(U), a, special.get(key), disp, [r["k"] for r in records])
    print(f"{count} explicit rooted networks of level <= 2 (seed {seed}): {stats}")
    print("only the critical splits can fail, and their weights equal the formula:", allok)
