"""Theorem 9(c): the family N(s,t), rebuilt by the referee from the description in Section 6:
the blob of N* with t leaves a_i on the path root..p1 and s leaves d_i on the path root..q1 (bloblet version),
or with clades A (t leaves) and D (s leaves) (clade version)."""
import sys
import rnet, gen

def build(s, t, bloblet=True):
    net = {l: [] for l in ["b", "x", "y", "c"]}
    A = [f"a{i}" for i in range(1, t + 1)]
    D = [f"d{i}" for i in range(1, s + 1)]
    for l in A + D:
        net[l] = []
    net["p1"] = ["b", "h1"]; net["q1"] = ["h1", "q2"]; net["q2"] = ["h2", "c"]
    net["h1"] = ["u"]; net["u"] = ["x", "h2"]; net["h2"] = ["y"]
    if bloblet:
        # root -> wa1 -> wa2 ... -> wat -> p1, leaf a_i at wa_i ; root -> wd1 -> ... -> wds -> q1
        chainA = [f"wa{i}" for i in range(1, t + 1)] + ["p1"]
        chainD = [f"wd{i}" for i in range(1, s + 1)] + ["q1"]
        net["rho"] = [chainA[0], chainD[0]]
        for i in range(t):
            net[chainA[i]] = [A[i], chainA[i + 1]]
        for i in range(s):
            net[chainD[i]] = [D[i], chainD[i + 1]]
        order = A + ["b", "x", "y", "c"] + D[::-1]
    else:
        def cat(leaves, pre):
            top = leaves[0]
            for i, l in enumerate(leaves[1:]):
                net[f"{pre}{i}"] = [top, l]
                top = f"{pre}{i}"
            return top
        ta, td = cat(A, "ca"), cat(D, "cd")
        net["rho"] = ["vab", "vcd"]; net["vab"] = [ta, "p1"]; net["vcd"] = ["q1", td]
        order = A + ["b", "x", "y", "c"] + D
    return net, order

for bloblet in (True, False):
    print("bloblet version" if bloblet else "clade version")
    for s, t in [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1), (2, 3), (3, 2), (3, 3), (4, 4), (2, 5)]:
        net, order = build(s, t, bloblet)
        root, tn, hyb, leaves = rnet.classify(net)
        n = len(leaves)
        assert rnet.is_lsa_network(net)
        po = rnet.planar_circular_order(net)
        galled = rnet.is_galled_def(net)
        lv = rnet.level(net); bl = rnet.is_bloblet(net)
        L, per_tree, Q = rnet.displayed(net)
        d = rnet.nanuq_metric(L, Q)
        al = rnet.alphas(d, order)
        a_xy = al[frozenset(("x", "y"))]
        neg = sum(1 for v in al.values() if v < 0)
        msg = (f"   N({s},{t}): n={n} level={lv} bloblet={bl} galled={galled} OLP={po is not None} "
               f"alpha(xy|rest)={a_xy} #negative alphas (planar order)={neg} min alpha={min(al.values())}")
        if n <= 8:
            good, total = rnet.kalmanson_orders(d, L)
            msg += f" | Kalmanson orders: {len(good)} of {total}"
        print(msg, flush=True)
