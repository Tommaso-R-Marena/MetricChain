"""Theorem 11, necessity spot checks with larger deviations / larger networks (sanity check only)."""
import sys, pickle, random
from fractions import Fraction as F
from collections import Counter
import rnet, gen
from t11_param import verdict, param_metric

def sunlet(n):
    """n-sunlet: cycle v0..v_{n-1}, leaf x_i at v_i, hybrid at v0 (parents v1 and v_{n-1}); root on the edge
    v_k - v_{k+1}, k = n//2"""
    net = {f"x{i}": [] for i in range(n)}
    k = n // 2
    net["rho"] = [f"v{k}", f"v{k+1}"]
    for i in range(k, 1, -1):
        net[f"v{i}"] = [f"x{i}", f"v{i-1}"]
    net["v1"] = ["x1", "v0"]
    for i in range(k + 1, n - 1):
        net[f"v{i}"] = [f"x{i}", f"v{i+1}"]
    net[f"v{n-1}"] = [f"x{n-1}", "v0"]
    net["v0"] = ["x0"]
    return net, [f"x{i}" for i in range(n)]

for n in (10, 14):
    net, order = sunlet(n)
    assert rnet.is_lsa_network(net) and rnet.level(net) == 1 and rnet.is_bloblet(net)
    rho = (F(0), F(1), F(2, 5), F(1))
    L, per_tree, quads, Qsets = gen.displayed_fast(net)
    D = param_metric(n, quads, Qsets, rho)
    d = {(x, y): D[i][j] for i, x in enumerate(L) for j, y in enumerate(L)}
    al = rnet.alphas(d, order)
    a_h = al[frozenset(o for o in order if o != "x0")] if frozenset(o for o in order if o != "x0") in al else al[frozenset(["x0"])]
    pred = 2 * (n - 2 + ((n - 3) + (n - 3) * (n - 4) // 2) * (2 * rho[2] - rho[1]))
    print(f"{n}-sunlet, rho=(0,1,2/5,1): alpha(trivial split of the hybrid leaf) = {a_h}; formula of the paper: {pred}")

nets = []
for fn in sys.argv[1:]:
    nets += pickle.load(open(fn, "rb"))
random.Random(3).shuffle(nets)
nets = nets[:5000]
for name, rho in [("o > s strongly: (0,1,1/2,2)", (F(0), F(1), F(1, 2), F(2))),
                  ("o < s strongly: (0,1,1/2,3/5)", (F(0), F(1), F(1, 2), F(3, 5))),
                  ("c + s > 2a strongly: (3/5,1,3/5,1) [c <= a, so inside (b)]", (F(3, 5), F(1), F(3, 5), F(1)))]:
    c_all = Counter(verdict(net, order, rho) for net, order, f, st in nets)
    c_leaf = Counter(verdict(net, order, rho) for net, order, f, st in nets if f["nonleaf_hyb_children"] == 0)
    print(f"   {name}: all networks {dict(c_all)} | leaf-child networks {dict(c_leaf)}", flush=True)
