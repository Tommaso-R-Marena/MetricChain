# t4_named_splits.py -- REVIEW 6: the three displayed splits named in the proof of Theorem 12' (steps (1)-(3)):
#   S_a = (leaves at y and the c-positions) | (b- and x-positions)          [k2 >= 1]
#         (leaves at y and b_kB) | (others)                                  [k2 = 0]          -- split of T_3
#   S_b(i) = (y, x-positions, b_1..b_i) | (others),  1 <= i < j                               -- split of T_1
#   S_c(i) = (b_1..b_i) | (others),  i >= j,  i <= kB if k2 >= 1,  i < kB if k2 = 0          -- arm of T_2, T_4
# For explicit rooted networks N[kB,k1,k2] with pendant subnetworks of sizes 1..3 (random kinds) and every kind of
# entry: each of these splits is displayed (computed from the switchings), is not S*, and has POSITIVE weight;
# and the four trees T_1..T_4 of the note, read as split systems on positions, equal the displayed splits of the
# bloblet (all sizes 1).
import random, itertools, sys
import numpy as np
from rn import Net, alphas
from gen_l2 import Builder

rng = random.Random(4)


def cat_splits(seq):
    out = set()
    n = len(seq)
    for i in range(2, n - 1):
        out.add(frozenset(seq[:i]))
    return out


def arms_splits(arms):
    out = set()
    allp = [p for a in arms for p in a]
    nonempty = [a for a in arms if a]
    for a in arms:
        for i in range(2, len(a) + 1):
            if len(allp) - i >= 2:
                out.add(frozenset(a[:i]))
    return out


def norm(s, allp):
    s = frozenset(s)
    c = frozenset(allp) - s
    return frozenset((s, c))


checked = 0
tree_ok = 0
for kB in range(2, 7):
    for k1 in range(1, 3):
        for k2 in range(0, 3):
            b = [("b", j) for j in range(1, kB + 1)]
            x = [("x", a) for a in range(1, k1 + 1)]
            c = [("c", e) for e in range(1, k2 + 1)]
            y = ("y", 0)
            allp = b + x + c + [y]
            # --- the four trees of the note vs the explicit bloblet
            B = Builder(rng)
            top, order = B.nested(kB, k1, k2, ("A",), len(allp), 0, sizes={p: 1 for p in allp})
            N = Net(B.net)
            pos = B.records[-1]["pos"]
            leaf_of = {p: pos[p][0] for p in allp}
            T1 = cat_splits(c + b[::-1] + x + [y])
            T2 = arms_splits([b, c, [y] + x[::-1]])
            T3 = cat_splits([y] + c + b[::-1] + x)
            T4 = arms_splits([b, [y] + c, x[::-1]])
            note = {norm(s, allp) for s in (T1 | T2 | T3 | T4) if 2 <= len(s) <= len(allp) - 2}
            disp = {frozenset(frozenset(next(p for p in allp if leaf_of[p] == l) for l in side) for side in sp)
                    for sp in N.displayed_splits() if min(len(s) for s in sp) >= 2}
            assert note == disp, ("four trees differ from the switchings", kB, k1, k2)
            tree_ok += 1
            # --- named splits, with sizes and entries
            entries = [("A",)] + b + c
            for entry in entries:
                for rep in range(3):
                    B = Builder(rng)
                    others = [p for p in allp if p != entry]
                    sizes = {p: rng.choice([1, 1, 2, 3]) for p in others}
                    out_n = rng.choice([1, 2, 3])
                    if entry == ("A",):
                        top, order = B.nested(kB, k1, k2, entry, sum(sizes.values()), 0, sizes=sizes)
                    else:
                        top = B.node("r")
                        t1, l1 = B.pendant(out_n, 1)
                        t2, l2 = B.nested(kB, k1, k2, entry, sum(sizes.values()), 1, sizes=sizes)
                        B.net[top] += [t1, t2]
                        order = l1 + l2
                    rc = [r for r in B.records if r["k"] == (kB, k1, k2) and r["entry"] == entry][-1]
                    N = Net(B.net)
                    if N.n > 16:
                        continue
                    named = set()
                    for p, ls in rc["pos"].items():
                        if ls is not None:
                            named |= set(ls)
                    outside = [l for l in order if l not in named]
                    lv = {p: (rc["pos"][p] if rc["pos"][p] is not None else outside) for p in allp}
                    D6 = N.nanuq6(order)
                    al = alphas(D6, list(range(N.n)))
                    idx = {l: i for i, l in enumerate(order)}
                    wt = {}
                    for (i, j), v in al.items():
                        U = frozenset(range(i + 1, j + 1))
                        wt[U] = v
                        wt[frozenset(range(N.n)) - U] = v
                    disp = N.displayed_splits(order)
                    full = frozenset(order)

                    def chk(posset, what):
                        global checked
                        S = frozenset(l for p in posset for l in lv[p])
                        assert frozenset((S, full - S)) in disp, ("not displayed", what, kB, k1, k2, entry)
                        assert wt[frozenset(idx[l] for l in S)] > 0, ("weight not positive", what, kB, k1, k2, entry)
                        checked += 1
                    star = frozenset(x + [y])
                    Sa = [y] + c if k2 >= 1 else [y, b[-1]]
                    assert frozenset(Sa) != star
                    chk(Sa, "S_a")
                    M = range(2, kB + 1) if k2 >= 1 else range(2, kB)
                    for j in M:
                        for i in range(1, j):
                            chk([y] + x + b[:i], "S_b")
                        for i in range(j, (kB if k2 >= 1 else kB - 1) + 1):
                            chk(b[:i], "S_c")
print(f"four trees of the note = displayed splits of the explicit bloblet for {tree_ok} triples (kB,k1,k2)")
print(f"named splits of the proof: displayed and of positive weight in all {checked} cases")
