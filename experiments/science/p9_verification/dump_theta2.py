#!/usr/bin/env python3
"""Workstream P9's raw stage-2 tables Theta_T for an instance P9 did not store them for, computed through P9's own
library (they are P9's numbers) and written in the format of ws_P9/cache/theta2_*.npz into p9_verification/cache/
(regenerable, not tracked).  P9 stored its raw tables for the twelve-residue peptides only; this script serves the
small enumerated instances and instances beyond twelve residues.  Read by pi_inference/first_order_recovery.py.

Run: python3 -B dump_theta2.py K5 4
     python3 -B dump_theta2.py K20 4 --part 0 2 > dump_theta2_K20_m4_p0of2.log     (subsets i with i mod 2 == 0)
     python3 -B dump_theta2.py K20 4 --probe 6                                     (time six subsets, write nothing)
"""
import os, sys, time, itertools, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P9"))
import p9lib as P9

a = sys.argv[1:]; seq, m = a[0], int(a[1]); t0 = time.time()
part = (int(a[a.index("--part") + 1]), int(a[a.index("--part") + 2])) if "--part" in a else (0, 1)
probe = int(a[a.index("--probe") + 1]) if "--probe" in a else 0
tau = P9.tau_of(seq); tag = P9.tagname(seq, "H", tau)
G, c0, h, J, x0, E0 = P9.setup(seq, "H", tau); n, k = G.ns, list(G.k)
RES = P9.Resolver(P9.ResBound(G, tuple(x0), P9.EnvelopeSup(G), K=m))               # derivative orders up to m, as ws_P9/p9_03_tables.py
subs = list(itertools.combinations(range(n), m)); mine = [j for j in range(len(subs)) if j % part[1] == part[0]]
if probe:
    mine = [mine[q] for q in np.linspace(0, len(mine) - 1, probe).astype(int)]
print(f"=== {seq} on H, tau {tau}: {G.nat} atoms, {n} sites, states per site {k}, anchor {list(x0)}; order {m}: {len(subs)} subsets, this run {len(mine)} "
      f"(part {part[0]} of {part[1]}{', probe' if probe else ''}) [{time.time() - t0:.0f}s setup]", flush=True)
d = dict(idx=np.array(mine), x0=np.array(x0), k=np.array(k)); smax = 0.0; t1 = time.time()
for q, j in enumerate(mine):
    t2 = np.array(RES.theta_both(m, list(subs[j]))[1], dtype=float)
    assert t2.shape == tuple(k[i] - 1 for i in subs[j]) and (t2 > 0).all()
    d[f"t{j}"] = t2; smax += float(t2.max())
    if probe or q % 200 == 0:
        print(f"    subset {j} {subs[j]}: {t2.size} entries, maximum {P9.BETA * float(t2.max()):.3e} kT [{time.time() - t1:.0f}s]", flush=True)
if not probe:
    fn = os.path.join(HERE, "cache", f"theta2_{tag}_m{m}" + (f"_p{part[0]}of{part[1]}" if part[1] > 1 else "") + ".npz")
    np.savez(fn, **d)
    print(f"written cache/{os.path.basename(fn)}: {len(mine)} raw stage-2 tables; sum of their maxima {P9.BETA * smax:.5g} kT; foreign writes refused during P9's import: {len(P9.FOREIGN_WRITES)}", flush=True)
print(f"ALL DONE {time.time() - t0:.0f} s ({(time.time() - t1) / max(len(mine), 1):.2f} s per subset); peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB", flush=True)
