"""Variants of the non-galled family: small parameters, and bloblet versions (extra leaves attached along the
cycle instead of pendant clades)."""
from netcalc import *

def build(s, t, bloblet=False):
    A = [f"a{i}" for i in range(1, t + 1)]
    D = [f"d{i}" for i in range(1, s + 1)]
    net = {l: [] for l in A + D + ["b", "x", "y", "c"]}
    if not bloblet:
        def cat(leaves, prefix):
            top = leaves[0]
            for i, l in enumerate(leaves[1:]):
                node = f"{prefix}{i}"
                net[node] = [top, l]
                top = node
            return top
        topA = cat(A, "nA")
        topD = cat(D, "nD")
        net["rho"] = ["vab", "vcd"]
        net["vab"] = [topA, "p1"]
        net["vcd"] = ["q1", topD]
    else:
        # path  rho -> wa1 -> wa2 -> ... -> p1  with leaf a_i hanging at wa_i (a1 nearest the root),
        # and   rho -> wd1 -> ... -> q1   with leaf d_i hanging at wd_i
        prev = "rho"
        net["rho"] = []
        for i, a in enumerate(A):
            node = f"wa{i}"
            net[prev].append(node) if prev != "rho" else net["rho"].append(node)
            net[node] = [a]
            prev = node
        net[prev].append("p1")
        prev = "rho"
        for i, dd in enumerate(D):
            node = f"wd{i}"
            net[prev].append(node)
            net[node] = [dd]
            prev = node
        net[prev].append("q1")
    net["p1"] = ["b", "h1"]
    net["q1"] = ["h1", "q2"]
    net["q2"] = ["h2", "c"]
    net["h1"] = ["u"]
    net["u"] = ["x", "h2"]
    net["h2"] = ["y"]
    order = A + ["b", "x", "y", "c"] + (D if not bloblet else D[::-1])
    return net, order

def run(s, t, bloblet):
    net, planar_order = build(s, t, bloblet)
    root, hyb = validate(net)
    comps, levels = blobs_and_level(net)
    L = leaves_of(net)
    n = len(L)
    emb = outer_labeled_planar_order(net)
    d, splits = nanuq_metric(net)
    w = split_weights(d, planar_order)
    neg = {tuple(sorted(U)): str(a) for U, a in w.items() if a < 0}
    # bloblet test: number of bridges of the semi-directed network equals n
    msg = f"{'bloblet ' if bloblet else 'clades  '}N({s},{t}): n={n} levels={levels} galled={is_galled(net)} planar={emb is not None} neg(planar order)={neg}"
    if n <= 9:
        good = kalmanson_orders(d, L)
        msg += f"  #Kalmanson orders={len(good)}"
    print(msg, flush=True)

for bl in (False, True):
    for s, t in [(1, 2), (2, 1), (1, 3), (3, 1), (2, 2), (3, 3)]:
        run(s, t, bl)
