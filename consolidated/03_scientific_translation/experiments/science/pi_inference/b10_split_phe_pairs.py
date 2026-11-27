#!/usr/bin/env python3
"""Benchmark B10 / addendum A17 (12), item 25: WHICH PAIRS does a model of independent residues miss for
poly-phenylalanine on PPII?  -- coordinator's script.

b10_split_charged.py found that for Phe4 and Phe6 on PPII neither independent residues nor a nearest-neighbour chain
is close to the solvated ensemble (D_2 = 0.086 / 0.079 and 0.334 / 0.328), while the pairwise model with all pairs is
(1e-4).  Here: exponential families on the clash-free domain X_tau with site tables plus pair tables for ONE sequence
separation s = 1, 2, 3 (and for sets of separations), fitted by maximum likelihood (convex); exact sums.
For comparison the same on the strand and the helix.
Run:  python3 -u b10_split_phe_pairs.py > b10_split_phe_pairs.log      (one core, under a minute)
"""
import os, sys, math, json, time
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2")); sys.path.insert(0, HERE)
import anlib
from b10_fit_directions import Family, BETA
from b10_floor_fit import divs
from b10_split_charged import fit_ml, TAU


class FamilySep(Family):
    """site tables plus pair tables for the pairs (i, i + s), s in seps; restricted to the states of maskflat"""
    def __init__(self, shape, seps, maskflat):
        self.shape = shape; self.n = n = len(shape); N = int(np.prod(shape))
        idx = np.indices(shape).reshape(n, N)[:, maskflat]
        self.cols = [idx[i].astype(np.int64) for i in range(n)]; self.sizes = [shape[i] for i in range(n)]
        for s in seps:
            for i in range(n - s):
                self.cols.append((idx[i] * shape[i + s] + idx[i + s]).astype(np.int64)); self.sizes.append(shape[i] * shape[i + s])
        self.off = np.concatenate([[0], np.cumsum(self.sizes)]); self.P = int(self.off[-1]); self.N = int(maskflat.sum()); self._A = None


t0 = time.time(); rows = []
print("# instance states | D_2 [D_inf] of the maximum-likelihood fit with site tables and pair tables at separations: none | 1 | 2 | 3 | 1,2 | 1,3 | 2,3 | 1,2,3", flush=True)
for n, bb in ((4, "P2"), (6, "P2"), (4, "E"), (6, "E"), (8, "E"), (4, "H"), (6, "H"), (8, "H")):
    tag = f"fb_F{n}_{bb}_R3_t0.60"
    d = anlib.load_fb(tag); mask = d["s2min"] > TAU; mf = mask.ravel()
    g = (d["tors"] + d["lj"] + d["coul"] + d["gb"])[mask]
    bg = BETA * (g - g.min()); lpg = -bg - logsumexp(-bg)
    res = dict(name=f"F{n}_{bb}", states=int(mf.sum())); cells = []
    for seps in ((), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)):
        seps = tuple(s for s in seps if s < n)
        fam = FamilySep(d["shape"], seps, mf)
        th, gn = fit_ml(fam, lpg); d2, di = divs(fam, lpg, th)
        res["D2_" + ",".join(map(str, seps))] = d2; res["Dinf_" + ",".join(map(str, seps))] = di; res["grad"] = max(res.get("grad", 0.0), gn)
        cells.append(f"{d2:9.2e} [{di:5.2f}]")
    rows.append(res)
    print(f"{res['name']:6s} {res['states']:6d} | " + " | ".join(cells) + f" || max |grad| {res['grad']:.1e}", flush=True)
json.dump(rows, open(os.path.join(HERE, "b10_split_phe_pairs.json"), "w"), indent=1)
print(f"ALL DONE {len(rows)} instances, {time.time() - t0:.0f} s")
