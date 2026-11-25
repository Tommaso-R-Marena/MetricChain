#!/usr/bin/env python3
"""t17 -- the inner minimum at the reported optima by a random search over ALL exit profiles nu in [0,1]^k (no clipping
lemma, no monotonicity) with I -- not the table of v -- in the constraint (Lemma T7), against the clipping solver.
Fixed seed.  usage: python3 t17_random_inner.py"""
import time
import numpy as np
import tlib as T
K = T.Known(T.phi_cw(1.5, 0.0), 1.0)
rng = np.random.default_rng(3)
t0 = time.time()


def brute(lams, mus, B, n1=4_000_000, rounds=6):
    best = (np.inf, None)
    lo = np.zeros(len(mus))
    hi = np.ones(len(mus))
    for r in range(rounds):
        nu = lo + (hi - lo) * rng.random((n1, len(mus)))
        kap = nu @ lams
        ok = (K.u * (np.abs(nu - mus) @ lams) + K.I(kap)) <= B
        mi = np.where(ok, np.maximum(T.hbf(kap) - T.hbf(nu) @ lams, 0), np.inf)
        i = int(np.argmin(mi))
        if mi[i] < best[0]:
            best = (float(mi[i]), nu[i].copy())
        w = (hi - lo) * 0.25
        lo = np.maximum(best[1] - w / 2, 0)
        hi = np.minimum(best[1] + w / 2, 1)
    return best


cases = ((0.0, [0.5, 0.5], [0.70197, 0.29803]),
         (0.02, [0.4296, 0.1408, 0.4296], [0.7226, 0.5, 0.2774]),
         (0.04, [0.3957, 0.1043, 0.1043, 0.3957], [0.7271, 0.5698, 0.4302, 0.2729]),
         (0.05, [0.3743, 0.0807, 0.09, 0.0807, 0.3743], [0.7302, 0.6117, 0.5, 0.3883, 0.2698]))
for e, lams, mus in cases:
    lams = np.array(lams)
    lams = lams / lams.sum()
    mus = np.array(mus)
    B = e + T.alpha_blocks(K, lams, mus)
    Vc, (cl, ch) = T.V_clip(K, lams, mus, B, K.v, ng=2001, zoom=6, full=True)
    vals = [brute(lams, mus, B)[0] for _ in range(3)]
    print(f"e={e}: {len(mus)} blocks, clipping solver {Vc:.7f} (clip [{cl:.4f},{ch:.4f}]); random search with I, three runs (upper bounds of the minimum): "
          f"{np.round(vals, 7)}   [{time.time()-t0:.0f}s]", flush=True)
