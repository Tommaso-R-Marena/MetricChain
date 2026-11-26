"""Level 2 completely: which outer-labeled planar level-2 networks have a NANUQ metric that is circular
decomposable with support the displayed splits (Theorems 12 and 13 of docs/complexity/NANUQ_LOCAL_CRITERION.md).

The non-galled level-2 blob has positions b_1..b_kB, x_1..x_k1, y, c_1..c_k2 (level2_nongalled.py).  With pendant
subnetworks of sizes beta_j, xi_a, eta, gamma_e at these positions, the claim is:
    every split other than  S* = (leaves at the x- and y-positions) | (leaves at the b- and c-positions)
    has a weight of the correct sign, and (for k1 >= 1, kB >= 2)
        alpha(S*) = beta_1 * G + xi_1 * R - e2(middle),
    where  R = eta + xi_2 + ... + xi_k1,
           G = gamma_1 + ... + gamma_k2 and middle = (beta_2, ..., beta_kB)        if k2 >= 1,
           G = beta_kB                  and middle = (beta_2, ..., beta_{kB-1})    if k2 = 0,
    and e2 is the sum of the products of pairs.

Parts (all exact integer arithmetic):
  X1  every substitution of two tree-generated systems with at least three leaves each, on six points, is
      6-locally good;
  X2  the six-point restrictions of the systems Sigma[k]: 6-locally good, except those isomorphic to Sigma[3,1,1]
      or Sigma[4,1,0], which are "all nine splits except the 2-split {b_2, b_3}" and are globally good;
  X3  the table of local terms of S*, by type of leaf, with the check that the type determines the value;
  T12 all bloblets N[kB,k1,k2] with at most MAXN leaves: only S* can fail, and its weight is the formula;
  T13 random networks made of one or several blobs (non-galled blobs, trees, systems of the class C) glued by
      substitution: only the splits S* of the non-galled blobs can fail, and their weights are the formula;
  ORD the failing bloblets with at most 9 leaves are Kalmanson for no circular order.

Usage:  python3 level2_classification.py [MAXN [number of random networks [seed]]]     (defaults 12, 400, 1)
"""
import sys
import random
from itertools import combinations
from splitsys import *
from local_terms import phi4, phi5, phi6
from localcrit import local_ok, tree_generated_systems, blowup
from twin_trees import compose, closure_systems
from level2_nongalled import system
from kalmanson_only import kalmanson_for_some_order


def trivial_system(n):
    return frozenset(canon(n, 1 << q) for q in range(n))


def tg_systems(n):
    return [trivial_system(3)] if n == 3 else tree_generated_systems(n)


def restrict(n, sigma, Y):
    idx = {yv: k for k, yv in enumerate(Y)}
    m6 = len(Y)
    full = (1 << m6) - 1
    out = set()
    for m in sigma:
        mm = 0
        for yv in Y:
            if (m >> yv) & 1:
                mm |= 1 << idx[yv]
        if mm != 0 and mm != full:
            out.add(canon(m6, mm))
    return frozenset(out)


def e2(vals):
    s = sum(vals)
    return (s * s - sum(v * v for v in vals)) // 2


def formula(beta, xi, eta, gamma):
    """alpha(S*) for k1 >= 1, kB >= 2"""
    R = eta + sum(xi[1:])
    if gamma:
        G, middle = sum(gamma), beta[1:]
    else:
        G, middle = beta[-1], beta[1:-1]
    return beta[0] * G + xi[0] * R - e2(middle)


# ---------------------------------------------------------------------------------------------------------- X1
def part_x1():
    cnt, ok = 0, True
    for n1, n2 in ((3, 5), (4, 4), (5, 3)):
        for s1 in tg_systems(n1):
            for s2 in tg_systems(n2):
                for p in range(n1):
                    for r in range(n2):
                        n, s = compose(n1, s1, p, n2, s2, r)
                        assert n == 6
                        cnt += 1
                        ok &= local_ok(6, s)[0]
    print(f"X1  substitutions of tree-generated systems (3+5, 4+4, 5+3 leaves) on six points: {cnt} cases,"
          f" all 6-locally good: {ok}")
    return ok


# ---------------------------------------------------------------------------------------------------------- X2
def part_x2(maxn=10):
    two = lambda k: canon(6, 0b000011 << k) if k < 5 else canon(6, 0b100001)
    all9 = set(m for m in all_circular_splits(6) if not is_trivial(6, m))
    ok = True
    seen = {}
    n_restr = 0
    for tot in range(5, maxn):
        for kB in range(tot + 1):
            for k1 in range(tot - kB + 1):
                k2 = tot - kB - k1
                n, names, sigma, trees = system(kB, k1, k2)
                for Y in combinations(range(n), 6):
                    n_restr += 1
                    r6 = restrict(n, sigma, Y)
                    sides = [names[q][0] for q in Y]
                    sub = (sides.count("b"), sides.count("x"), sides.count("c")) if "y" in sides else None
                    good = local_ok(6, r6)[0]
                    key = (sub, good)
                    seen[key] = seen.get(key, 0) + 1
                    if sub in ((3, 1, 1), (4, 1, 0)):
                        # the restriction: all nine splits except the 2-split of the second and third b-leaf
                        bs = [k for k, q in enumerate(Y) if names[q][0] == "b"]
                        pair = (1 << bs[1]) | (1 << bs[2])
                        expect = frozenset((all9 - {canon(6, pair)}) | set(trivial_system(6)))
                        ok &= (r6 == expect) and (check(6, r6)[0] == "ok") and not good
                    else:
                        ok &= good
    bad = sorted(k for k in seen if not k[1])
    print(f"X2  {n_restr} six-point restrictions of the systems Sigma[k] with at most {maxn} leaves: 6-locally good"
          f" except the sub-configurations {sorted(set(k[0] for k in bad))}, which are 'all nine splits except"
          f" the 2-split of the 2nd and 3rd b-leaf' and are globally good: {ok}")
    return ok


# ---------------------------------------------------------------------------------------------------------- X3
def star_split(n2, pos):
    U = [q for q in range(n2) if pos[q][0] in "bc"]
    V = [q for q in range(n2) if pos[q][0] in "yx"]
    return U, V


def part_x3():
    """local terms of S* by type; every position carries a clade of m leaves (m = 2 and m = 3)."""
    from collections import defaultdict
    t4, t5, t6 = set(), defaultdict(set), defaultdict(set)
    decomposition_ok = True
    for (kB, k1, k2) in [(2, 1, 1), (3, 2, 2), (4, 3, 3), (2, 1, 0), (3, 2, 0), (4, 2, 0), (5, 1, 0), (2, 3, 1), (2, 3, 0), (3, 3, 0)]:
        for m in (2, 3):
            n, names, sigma, trees = system(kB, k1, k2)
            if n * m > 24 or (m == 3 and n > 6):
                continue
            n2, s2 = blowup(n, sigma, [m] * n)
            s2 = set(s2)
            pos = [(names[p][0], names[p][1]) for p in range(n) for _ in range(m)]
            U, V = star_split(n2, pos)
            u1, up, v1, vq = U[0], U[-1], V[0], V[-1]

            def typ(q):
                s, i = pos[q]
                if s == "b":
                    return "b1" if i == 1 else ("bK" if (k2 == 0 and i == kB) else "b")
                if s == "c":
                    return "c1" if i == 1 else "c"
                if s == "x":
                    return "x1" if i == 1 else "x"
                return "y"
            tag = "k2>=1" if k2 else "k2=0"
            tot = phi4(s2, n2, u1, up, v1, vq)
            t4.add((tag, tot))
            for z in U[1:-1]:
                v = phi5(s2, n2, u1, z, up, v1, vq)
                t5[(tag, typ(z))].add(v)
                tot += v
            for z in V[1:-1]:
                v = phi5(s2, n2, v1, z, vq, u1, up)
                t5[(tag, typ(z))].add(v)
                tot += v
            for side in (U, V):
                inner = side[1:-1]
                for a in range(len(inner)):
                    for b in range(a + 1, len(inner)):
                        z, w = inner[a], inner[b]
                        v = phi6(s2, n2, u1, z, w, up, v1, vq)
                        same = pos[z] == pos[w]
                        t6[(tag, typ(z), typ(w), "same position" if same else "different positions")].add(v)
                        tot += v
            D = nanuq_2d(n2, s2)
            al = alphas_2(n2, D)
            i, j = sorted((U[-1], V[-1]))
            decomposition_ok &= (2 * tot == al[(i, j)])
            beta = [m] * kB
            decomposition_ok &= (al[(i, j)] == 2 * formula([m] * kB, [m] * k1, m, [m] * k2))
    unique = all(len(v) == 1 for v in t5.values()) and all(len(v) == 1 for v in t6.values()) and len(t4) == 2
    print("X3  local terms of S* (twice the values of the note), by type of leaf:")
    print("      2*Phi4:", sorted(t4))
    for tag in ("k2>=1", "k2=0"):
        print(f"      [{tag}] 2*Phi5:", {k[1]: next(iter(v)) for k, v in sorted(t5.items()) if k[0] == tag})
        print(f"      [{tag}] 2*Phi6, different positions:",
              {k[1] + "," + k[2]: next(iter(v)) for k, v in sorted(t6.items()) if k[0] == tag and k[3].startswith("diff")})
        print(f"      [{tag}] 2*Phi6, same position:",
              sorted(set(next(iter(v)) for k, v in t6.items() if k[0] == tag and k[3].startswith("same"))))
    print("      the type determines the value:", unique, "| Proposition 2 and the formula reproduce alpha(S*):",
          decomposition_ok)
    return unique and decomposition_ok


# ---------------------------------------------------------------------------------------------------------- T12
def part_t12(maxn):
    ok, cnt, fails, zeros = True, 0, 0, 0
    for tot in range(3, maxn):
        for kB in range(tot + 1):
            for k1 in range(tot - kB + 1):
                k2 = tot - kB - k1
                n, names, sigma, trees = system(kB, k1, k2)
                D = nanuq_2d(n, sigma)
                al = alphas_2(n, D)
                star = None
                if k1 >= 1 and kB >= 2:
                    m = 0
                    for q in range(n):
                        if names[q][0] in "yx":
                            m |= 1 << q
                    star = canon(n, m)
                cnt += 1
                for (i, j), v in al.items():
                    cm = canon(n, split_mask(n, i, j))
                    if cm == star:
                        pred = formula([1] * kB, [1] * k1, 1, [1] * k2)
                        ok &= (v == 2 * pred)
                        fails += pred < 0
                        zeros += pred == 0
                    else:
                        ok &= v >= 0 and ((v > 0) == (cm in sigma))
    print(f"T12 all {cnt} bloblets N[kB,k1,k2] with 4..{maxn} leaves: every split other than S* has the correct sign and"
          f" alpha(S*) = k1 + k2 - C(kB-1,2)  resp.  k1 + 1 - C(kB-2,2): {ok}   (negative: {fails}, zero: {zeros})")
    return ok


# ---------------------------------------------------------------------------------------------------------- T13
def random_tree_system(rng, m):
    """split system of a random binary tree that is planar for the order 0..m-1"""
    out = set(trivial_system(m))

    def rec(lo, hi):                      # leaves lo..hi-1
        if hi - lo <= 1:
            return
        mask = 0
        for q in range(lo, hi):
            mask |= 1 << q
        if 2 <= hi - lo <= m - 2:
            out.add(canon(m, mask))
        cut = rng.randint(lo + 1, hi - 1)
        rec(lo, cut)
        rec(cut, hi)
    rec(0, m)
    return frozenset(out)


def compose_maps(n1, s1, p, n2, s2, r):
    n, s = compose(n1, s1, p, n2, s2, r)
    new1 = lambda q: q if q < p else q + n2 - 2
    new2 = lambda q: p + ((q - r - 1) % n2)
    block2 = frozenset(new2(q) for q in range(n2) if q != r)
    rest1 = frozenset(new1(q) for q in range(n1) if q != p)
    map1 = {q: (block2 if q == p else frozenset([new1(q)])) for q in range(n1)}
    map2 = {q: (rest1 if q == r else frozenset([new2(q)])) for q in range(n2)}
    return n, s, map1, map2


def map_record(rec, mp):
    f = lambda S: frozenset().union(*[mp[q] for q in S])
    return {"b": [f(S) for S in rec["b"]], "x": [f(S) for S in rec["x"]], "c": [f(S) for S in rec["c"]],
            "y": f(rec["y"])}


def random_piece(rng, budget, depth):
    """(n, sigma, records): a random system with at most `budget` leaves; records describe its non-galled blobs"""
    kind = rng.choice(["ng", "ng", "tree", "galled"]) if depth < 3 else rng.choice(["tree", "galled"])
    if budget < 4:
        kind = "tree"
    if kind == "ng":
        while True:
            kB, k1, k2 = rng.randint(1, 5), rng.randint(0, 3), rng.randint(0, 3)
            if 4 <= kB + k1 + k2 + 1 <= max(4, min(budget, 9)):
                break
        n, names, sigma, trees = system(kB, k1, k2)
        ix = {nm: q for q, nm in enumerate(names)}
        rec = {"b": [frozenset([ix[("b", i)]]) for i in range(1, kB + 1)],
               "x": [frozenset([ix[("x", i)]]) for i in range(1, k1 + 1)],
               "c": [frozenset([ix[("c", i)]]) for i in range(1, k2 + 1)],
               "y": frozenset([ix[("y", 0)]])}
        s, recs = frozenset(sigma), [rec]
    elif kind == "tree":
        n = rng.randint(3, max(3, min(budget, 5)))
        s, recs = random_tree_system(rng, n), []
    else:
        n = rng.randint(4, max(4, min(budget, 6)))
        s, recs = rng.choice(sorted(closure_systems(n), key=sorted)), []
    # substitute pendant pieces at some leaves, from the last leaf to the first
    for q in range(n - 1, -1, -1):
        room = budget - n
        if room >= 2 and rng.random() < 0.45:
            n2, s2, recs2 = random_piece(rng, min(room + 1, 7), depth + 1)
            r = rng.randrange(n2)
            n, s, map1, map2 = compose_maps(n, s, q, n2, s2, r)
            recs = [map_record(rc, map1) for rc in recs] + [map_record(rc, map2) for rc in recs2]
    return n, s, recs


def part_t13(count, seed, budget=15):
    rng = random.Random(seed)
    ok, done, with_ng, n_star, n_fail, maxleaves = True, 0, 0, 0, 0, 0
    while done < count:
        n, s, recs = random_piece(rng, budget, 0)
        if n < 6:
            continue
        done += 1
        maxleaves = max(maxleaves, n)
        s = set(s)
        D = nanuq_2d(n, s)
        al = alphas_2(n, D)
        special = {}
        for rc in recs:
            kB, k1 = len(rc["b"]), len(rc["x"])
            if k1 >= 1 and kB >= 2:
                m = 0
                for S in rc["x"] + [rc["y"]]:
                    for q in S:
                        m |= 1 << q
                pred = formula([len(S) for S in rc["b"]], [len(S) for S in rc["x"]], len(rc["y"]),
                               [len(S) for S in rc["c"]])
                cm = canon(n, m)
                if cm in special and special[cm] != pred:
                    ok = False
                special[cm] = pred
        with_ng += bool(special)
        for (i, j), v in al.items():
            cm = canon(n, split_mask(n, i, j))
            if cm in special:
                n_star += 1
                ok &= (v == 2 * special[cm])
                n_fail += special[cm] <= 0
                ok &= cm in s
            else:
                ok &= v >= 0 and ((v > 0) == (cm in s))
    print(f"T13 {count} random glued networks (up to {maxleaves} leaves; {with_ng} with a non-galled blob having k1 >= 1,"
          f" kB >= 2; {n_star} splits S*, of which {n_fail} have weight <= 0): only the splits S* can fail and their"
          f" weights equal the formula: {ok}")
    return ok


# ---------------------------------------------------------------------------------------------------------- ORD
def part_ord(maxn=9):
    ok, cnt = True, 0
    for tot in range(5, maxn):
        for kB in range(2, tot + 1):
            for k1 in range(1, tot - kB + 1):
                k2 = tot - kB - k1
                if formula([1] * kB, [1] * k1, 1, [1] * k2) >= 0:
                    continue
                n, names, sigma, trees = system(kB, k1, k2)
                D = nanuq_2d(n, sigma)
                cnt += 1
                ok &= kalmanson_for_some_order(n, D) is None
    print(f"ORD the {cnt} bloblets with at most {maxn} leaves and alpha(S*) < 0 are Kalmanson for no circular order: {ok}")
    return ok


if __name__ == "__main__":
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    res = [part_x1(), part_x2(), part_x3(), part_t12(maxn), part_t13(count, seed), part_ord()]
    print("ALL OK" if all(res) else "FAILURE")
