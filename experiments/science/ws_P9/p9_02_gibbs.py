#!/usr/bin/env python3
"""P9 step 2 -- two Gibbs samples of the true ensemble exp(-beta (f + g)) with the coordinator's sampler
(pi_inference/window_model_occ.gibbs_sample, imported read-only), with the seeds of the coordinator's
occ_reduction_test.py: 4242 (guides the occupancy-aware reductions, and here the choice of sub-tuples) and 777 (the
sample on which sandwiches and first-order numbers are checked).  UNCERTIFIED samples: nothing valid depends on them.
Stored with their energies in ws_P9/cache/gibbs_<tag>_seed<seed>.npz.
usage: python3 -B p9_02_gibbs.py SEQ      writes logs/gibbs_<tag>.log"""
import sys
from p9lib import *

seq = sys.argv[1]; bb = "H"; tau = tau_of(seq); tag = tagname(seq, bb, tau)
log = Log(os.path.join(LOGS, f"gibbs_{tag}.log"))
log(f"=== p9_02_gibbs {seq} on {bb}, tau {tau}; started {now()}")
G, c0, h, J, x0, E0 = setup(seq, bb, tau); n, k = G.ns, list(G.k)
log(f"    {G.nat} atoms, {n} sites, states per site {k}, anchor {x0}")
for seed in (4242, 777):
    t1 = time.time()
    X = gibbs_sample(pw, G, c0, h, J, x0, k, BETA, np.random.default_rng(seed))
    g = np.concatenate([G.bulk_energy(X[s:s + 256]) for s in range(0, len(X), 256)]); f = pw.f_energy(X, c0, h, J)
    np.savez(os.path.join(MYCACHE, f"gibbs_{tag}_seed{seed}.npz"), X=X.astype(np.int16), g=g, f=f, anchor=np.array(x0))
    off = X != np.array(x0)[None]
    log(f"    seed {seed}: {len(X)} states (8 chains, 120 sweeps each after 30) [{time.time() - t1:.0f}s]; sites off the anchor: mean {off.sum(1).mean():.2f}, largest {int(off.sum(1).max())}; "
        f"frequencies by site: " + " ".join(f"{v:.2f}" for v in off.mean(0)) + "; distribution of the number of sites off the anchor: "
        + " ".join(f"{s_}:{int((off.sum(1) == s_).sum())}" for s_ in range(n + 1) if (off.sum(1) == s_).any()))
log.done()
