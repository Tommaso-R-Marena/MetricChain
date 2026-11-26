#!/usr/bin/env python3
"""The ball of radius M around the anchor of SEQ on backbone BB, evaluated once and stored in the coordinator's cache
(pi_inference/serine_helix_reach_cache/ball_<tag>_M<M>.npz, not tracked): keys `states` (as pwmodel.ball_states lists
them, uint8), `vals` (the solvent term g, kcal/mol), `anchor`.  Read by first_order_recovery.py.
Run: python3 -B ball_cache.py K20 H 3 > ball_cache_K20_H_M3.log
"""
import os, sys, time, resource
import numpy as np
import nested_sampler as NS
L, pw = NS.L, NS.pw


def main():
    seq, bb, M = sys.argv[1], sys.argv[2], int(sys.argv[3]); t0 = time.time()
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    blocks, tot = pw.ball_states(k, x0, M); st = np.concatenate([b for _, b in blocks], axis=0); assert len(st) == tot and max(k) < 256
    print(f"=== {seq} on {bb}, tau {tau}: {G.nat} atoms, {n} sites, states per site {k}, anchor {x0}; ball of radius {M}: {tot} states", flush=True)
    vals = np.empty(tot); step = 256
    for s in range(0, tot, step):
        vals[s:s + step] = G.bulk_energy(st[s:s + step])
        if (s // step) % 200 == 0: print(f"    {s} of {tot} [{time.time() - t0:.0f}s]", flush=True)
    fn = os.path.join(NS.CACHE, f"ball_{tag}_M{M}.npz")
    np.savez(fn, states=st.astype(np.uint8), vals=vals, anchor=np.array(x0))
    pick = np.random.default_rng(3).choice(tot, size=300, replace=False)
    dev = float(np.abs(G.bulk_energy(st[pick]) - vals[pick]).max())
    print(f"written {os.path.relpath(fn, os.path.dirname(os.path.abspath(__file__)))}: {tot} values, range [{vals.min():.4f}, {vals.max():.4f}] kcal/mol; 300 re-evaluated: largest deviation {dev:.1e}", flush=True)
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB", flush=True)


if __name__ == "__main__":
    main()
