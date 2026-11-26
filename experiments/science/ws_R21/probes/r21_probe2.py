import sys
sys.path.insert(0, "/home/user/MetricChain/experiments/science/ws_R21")
from r21_common import *
rng = np.random.default_rng(7)
for name in CONSTRUCTION:
    N, E = graph_table()[name]
    C = Constructor(name, N, E)
    Y = rng.standard_normal((2000, N, 2))
    T = sqlen(Y, E)
    d, P = C.defect(T)
    # realised lengths must match all edges
    err = np.max(np.abs(sqlen(P, E) - T), axis=1)
    # non-realisable: random perturbation of one check edge
    T2 = T.copy()
    if C.check:
        k = C.idx[C.check[0]]
        T2[:, k] *= 1.0 + 0.05 * rng.standard_normal(2000)
        d2, _ = C.defect(T2)
    else:
        d2 = np.array([np.nan])
    print(f"{name:9s} check edges {len(C.check):2d}: planted realisable: max defect {d.max():.2e}, max |len err| {err.max():.2e}; "
          f"perturbed check edge: min defect {np.nanmin(d2):.2e}, fraction with defect<1e-9: {np.mean(d2 < 1e-9):.4f}")
