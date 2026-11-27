# t3_mutation.py -- REVIEW 6: a test of the STATEMENT of Theorem 12' that uses no description of blobs or positions.
# Start from a random rooted binary tree, or from an explicit nested bloblet, and apply random operations
#   * add a leaf on a random edge,
#   * insert a hybrid edge between two random edges (acyclic),
# keep the result if it is a valid rooted binary network (root = LSA), of level <= 2, and outer-labeled planar
# (planarity with an apex joined to all leaves; the circular order C is read from the embedding).
# Claim tested: if some split weight alpha for C is negative, NO circular order makes d_N Kalmanson (exact search).
import sys, random, time
import numpy as np
from rn import Net, alphas, is_kalmanson, kalmanson_search
from gen_l2 import Builder


def edges(net):
    return [(u, v) for u in net for v in net[u]]


def ancestors_or_self(net, x):
    par = {}
    for u in net:
        for v in net[u]:
            par.setdefault(v, []).append(u)
    seen = {x}
    st = [x]
    while st:
        v = st.pop()
        for u in par.get(v, []):
            if u not in seen:
                seen.add(u)
                st.append(u)
    return seen


def add_leaf(net, rng, cnt):
    u, v = rng.choice(edges(net))
    p, l = f"p{cnt}", f"M{cnt}"
    net[u][net[u].index(v)] = p
    net[p] = [v, l] if rng.random() < 0.5 else [l, v]
    net[l] = []


def add_hybrid(net, rng, cnt):
    E = edges(net)
    for _ in range(50):
        (a, b), (c, d) = rng.sample(E, 2)
        if d in ancestors_or_self(net, a):
            continue
        p, h = f"q{cnt}", f"g{cnt}"
        net[a][net[a].index(b)] = p
        net[p] = [b, h]
        # (c,d) may have been (a,b)?  no: two different edges; but c could be == a with d != b, handled by index
        cc = c
        if (c, d) == (a, b):
            continue
        net[cc][net[cc].index(d)] = h
        net[h] = [d]
        return True
    return False


def random_tree(rng, n):
    net = {"r": ["t0", "t1"], "t0": [], "t1": []}
    cnt = 2
    cat = rng.random() < 0.6
    while sum(1 for v in net if not net[v]) < n:
        leaves = [v for v in net if not net[v]]
        x = leaves[-1] if cat and rng.random() < 0.8 else rng.choice(leaves)
        a, b = f"t{cnt}", f"t{cnt+1}"
        cnt += 2
        net[x] = [a, b]
        net[a], net[b] = [], []
    return net


def main(count, seed, maxn):
    rng = random.Random(seed)
    st = dict(kept=0, negative=0, searched=0, kalm_C=0, hyb_hist={}, n_hist={}, neg_n_hist={}, neg_hyb_hist={},
              neg_count_hist={}, nonplanar_or_invalid=0)
    t0 = time.time()
    seen = set()
    while st["kept"] < count:
        if rng.random() < 0.5:
            n0 = rng.randint(6, maxn)
            net = random_tree(rng, n0)
            ops = ["h"] * rng.randint(2, 4)
        else:
            B = Builder(rng)
            for _ in range(100):
                kB, k1, k2 = rng.randint(3, 6), rng.randint(1, 2), rng.randint(0, 2)
                if kB + k1 + k2 + 1 <= maxn:
                    break
            top, order = B.nested(kB, k1, k2, ("A",), kB + k1 + k2 + 1, 0, sizes=None)
            net = B.net
            ops = ["l"] * rng.randint(0, 3) + ["h"] * rng.randint(0, 2)
            rng.shuffle(ops)
        cnt = 0
        good = True
        for op in ops:
            cnt += 1
            if op == "l":
                add_leaf(net, rng, cnt)
            else:
                if not add_hybrid(net, rng, cnt):
                    good = False
                    break
        if not good:
            continue
        N = Net(net)
        if N.n > maxn or N.n < 6 or not N.valid() or N.level() > 2:
            st["nonplanar_or_invalid"] += 1
            continue
        C = N.planar_order()
        if C is None:
            st["nonplanar_or_invalid"] += 1
            continue
        st["kept"] += 1
        nh = len(N.hyb)
        st["hyb_hist"][nh] = st["hyb_hist"].get(nh, 0) + 1
        st["n_hist"][N.n] = st["n_hist"].get(N.n, 0) + 1
        D6 = N.nanuq6(C)
        al = alphas(D6, list(range(N.n)))
        neg = [k for k, v in al.items() if v < 0]
        # displayed splits must be circular for C (sanity of the order read from the embedding)
        idx = {x: i for i, x in enumerate(C)}
        for sp in N.displayed_splits(C):
            A = next(iter(sp))
            pos = sorted(idx[x] for x in A)
            comp = sorted(set(range(N.n)) - set(pos))
            assert pos == list(range(pos[0], pos[-1] + 1)) or comp == list(range(comp[0], comp[-1] + 1))
        if not neg:
            st["kalm_C"] += 1
            continue
        st["negative"] += 1
        st["neg_n_hist"][N.n] = st["neg_n_hist"].get(N.n, 0) + 1
        st["neg_hyb_hist"][nh] = st["neg_hyb_hist"].get(nh, 0) + 1
        st["neg_count_hist"][len(neg)] = st["neg_count_hist"].get(len(neg), 0) + 1
        st["searched"] += 1
        r = kalmanson_search(D6)
        if r is not None:
            print("COUNTEREXAMPLE: Kalmanson order", [C[i] for i in r], "for network", net, "planar order", C)
            return False
    print(f"seed {seed}, max leaves {maxn}, {time.time()-t0:.0f}s")
    for k, v in st.items():
        print("  ", k, ":", dict(sorted(v.items())) if isinstance(v, dict) else v)
    print("no circular order found for any network with a negative weight: True")
    return True


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    count, seed, maxn = (a + [2000, 1, 11][len(a):])[:3]
    sys.exit(0 if main(count, seed, maxn) else 1)
