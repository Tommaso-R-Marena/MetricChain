#!/usr/bin/env python3
"""Workstream P9's raw stage-2 tables Theta_T for a SMALL instance, computed through P9's own library (they are P9's
numbers) and stored in the format of ws_P9/cache/theta2_*.npz -- P9 stored its raw tables only for the twelve-residue
peptides.  Written into p9_verification/cache/ (regenerable, not tracked); read by pi_inference/first_order_recovery.py.
Run: python3 -B dump_theta2.py K5 4
"""
import os, sys, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P9"))
import p9lib as P9

seq, m = sys.argv[1], int(sys.argv[2]); tau = P9.tau_of(seq); tag = P9.tagname(seq, "H", tau)
G, c0, h, J, x0, E0 = P9.setup(seq, "H", tau); n, k = G.ns, list(G.k)
RES = P9.Resolver(P9.ResBound(G, tuple(x0), P9.EnvelopeSup(G), K=n))
subs = list(itertools.combinations(range(n), m)); d = dict(idx=np.arange(len(subs)), x0=np.array(x0), k=np.array(k))
for j, T in enumerate(subs):
    t2 = np.array(RES.theta_both(m, list(T))[1], dtype=float)
    assert t2.shape == tuple(k[i] - 1 for i in T) and (t2 > 0).all()
    d[f"t{j}"] = t2
np.savez(os.path.join(HERE, "cache", f"theta2_{tag}_m{m}.npz"), **d)
print(f"{seq}: {len(subs)} raw stage-2 tables of order {m} written; sum of their maxima {P9.BETA * sum(float(d[f't{j}'].max()) for j in range(len(subs))):.5g} kT; foreign writes refused during P9's import: {len(P9.FOREIGN_WRITES)}")
