#!/usr/bin/env python3
"""Is the call that dump_theta2.py makes the one workstream P9 made?  For a twelve-residue instance P9 stored its raw
stage-2 tables itself (ws_P9/cache/theta2_*.npz, written by ws_P9/p9_03_tables.py --keeptabs).  This script computes
the tables of N random subsets (and the first and the last) through the call of dump_theta2.py -- P9's Resolver on
ResBound(..., K=m) -- and compares them entry by entry with P9's own file.  It justifies using dump_theta2.py for an
instance for which P9 stored nothing (Lys20).  It checks that the two code paths agree, not that the tables are right
(for that: resolved_check12.py, and check (4) of pi_inference/first_order_recovery.py).

Run: python3 -B dump_theta2_check.py K12 4 16 > dump_theta2_check_K12_m4.log
"""
import os, sys, time, itertools, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P9"))
import p9lib as P9

a = sys.argv[1:]; seq, m, N = a[0], int(a[1]), int(a[2]); t0 = time.time()
tau = P9.tau_of(seq); tag = P9.tagname(seq, "H", tau)
G, c0, h, J, x0, E0 = P9.setup(seq, "H", tau); n, k = G.ns, list(G.k)
RES = P9.Resolver(P9.ResBound(G, tuple(x0), P9.EnvelopeSup(G), K=m))
subs = list(itertools.combinations(range(n), m))
fn = os.path.join(HERE, "..", "ws_P9", "cache", f"theta2_{tag}_m{m}.npz"); z = np.load(fn)
print(f"=== {seq} on H, tau {tau}: {n} sites, order {m}: {len(subs)} subsets; workstream P9's own tables: ws_P9/cache/{os.path.basename(fn)} ({len(z.files) - 1} tables)", flush=True)
pick = sorted(set(np.random.default_rng(7).choice(len(subs), size=N, replace=False).tolist() + [0, len(subs) - 1]))
dev = rel = 0.0; nent = 0; ctrl = 0
for j in pick:
    t2 = np.array(RES.theta_both(m, list(subs[j]))[1], dtype=float); ref = np.array(z[f"t{j}"], dtype=float)
    assert t2.shape == ref.shape == tuple(k[i] - 1 for i in subs[j])
    dev = max(dev, float(np.abs(t2 - ref).max())); rel = max(rel, float((np.abs(t2 - ref) / ref).max())); nent += t2.size
    other = np.array(z[f"t{(j + 1) % len(subs)}"], dtype=float)                       # control: the table of the next subset must differ
    ctrl += int(other.shape != ref.shape or float(np.abs(other - ref).max()) > 1e-12)
print(f"{len(pick)} subsets, {nent} entries: largest absolute difference between the call of dump_theta2.py and P9's stored table {dev:.3e} kcal/mol, largest relative difference {rel:.3e}; "
      f"control (the stored table of the next subset in place of the right one): differs in {ctrl} of {len(pick)}", flush=True)
assert dev == 0.0 or rel < 1e-12
print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB", flush=True)
