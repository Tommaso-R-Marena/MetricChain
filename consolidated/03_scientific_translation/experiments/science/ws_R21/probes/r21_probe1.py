import sys
sys.path.insert(0, "/home/user/MetricChain/experiments/science/ws_R21")
from r21_common import *
import numpy as np
rng = np.random.default_rng(5)
for name in ["W5", "K5", "K33+e"]:
    N, E = graph_table()[name]
    R = Realiser(N, E)
    Y = rng.standard_normal((400, N, 2))
    Tp = sqlen(Y, E)
    for iters in (120, 400):
        for scale in (1.0, 1.5, 3.0):
            t0 = time.time()
            hits = np.zeros(400, dtype=int)
            S = 20
            for s in range(S):
                Z0 = scale * rng.standard_normal((400, R.n))
                Z, res = R.solve(Tp, Z0, iters=iters)
                hits += res < 1e-9
            print(name, "iters", iters, "scale", scale, "per-start success %.3f" % (hits.sum() / (400 * S)),
                  "min hits/20 = %d" % hits.min(), "targets never found: %d" % np.sum(hits == 0),
                  "quantiles of hits:", np.quantile(hits, [0.01, 0.05, 0.25, 0.5]), "time %.1fs" % (time.time() - t0))
