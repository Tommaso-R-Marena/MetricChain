"""Analysis 1: per-torsion bounded-difference constants c_i of every residual, exactly on the
enumerated grids; dependence on position, chain length and clash threshold.
usage: python3 an1_constants.py [alphabet n ...]   (default: everything in data/)"""
import sys, os, json, re
import numpy as np
from analysis_lib import *

np.set_printoptions(precision=2, suppress=True, linewidth=220)
jobs = []
if len(sys.argv) > 1:
    a = sys.argv[1:]
    jobs = [(a[i], int(a[i + 1])) for i in range(0, len(a), 2)]
else:
    for fn in sorted(os.listdir(os.path.join(HERE, "data"))):
        mt = re.match(r"grid_(A\d|U\d+)_n(\d+)(_part0of\d+)?\.npz", fn)
        if mt:
            jobs.append((mt.group(1), int(mt.group(2))))
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
_p = os.path.join(HERE, "out", "an1_constants.json")
results = json.load(open(_p)) if os.path.exists(_p) else {}
for alphabet, n in jobs:
    d = load(alphabet, n)
    R = residuals(d)
    names = site_names(n)
    print(f"\n================ {alphabet}  n = {n} residues, {d['m']} torsion sites, {d['k']}^{d['m']} = {d['k']**d['m']} conformations")
    for tau in (0.0, 0.6, 0.7, 0.8):
        mask = d["clash"] > tau
        print(f"--- clash threshold tau = {tau}: {int(mask.sum())} conformations ({100*mask.mean():.1f} %)")
        for name in R:
            if name in ("f", "coul", "coul+GB") and tau != 0.7:
                continue
            g = R[name]
            c, rms, arg = first_order(g, mask)
            C = residue_constants(g, mask)
            rng_ = float(g[mask].max() - g[mask].min())
            results[f"{alphabet}|{n}|{tau}|{name}"] = dict(c=c.tolist(), rms=rms.tolist(), C_res=C.tolist(), range=rng_,
                                                           std=float(g[mask].std()), nconf=int(mask.sum()))
            if tau in (0.0, 0.7):
                print(f"  {name:10s} range {rng_:7.2f}  std {g[mask].std():6.2f} | c_i (kcal/mol): {c}  | max {c.max():.2f} = {c.max()/KT300:.1f} kT; rms flip: {rms.max():.2f}; residue C_r: {C}")
json.dump(results, open(os.path.join(HERE, "out", "an1_constants.json"), "w"), indent=0)
