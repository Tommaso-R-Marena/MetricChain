"""Analysis 2: mixed second differences c_ij and the functional ANOVA of each residual.
usage: python3 an2_second_order.py alphabet n [alphabet n ...]"""
import sys, os, json
import numpy as np
from analysis_lib import *

np.set_printoptions(precision=2, suppress=True, linewidth=250)
a = sys.argv[1:]
jobs = [(a[i], int(a[i + 1])) for i in range(0, len(a), 2)]
TAU = 0.7
res_path = os.path.join(HERE, "out", "an2_second_order.json")
results = json.load(open(res_path)) if os.path.exists(res_path) else {}
for alphabet, n in jobs:
    d = load(alphabet, n)
    R = residuals(d)
    m = d["m"]; k = d["k"]
    mask = d["clash"] > TAU
    print(f"\n================ {alphabet} n = {n}: {m} torsion sites, clash-free (tau={TAU}) {int(mask.sum())} of {k**m}")
    for name in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff19SB-ff14SB", "ff99SB-ff14SB", "OBC2-GBn2", "f"):
        if name not in R:
            continue
        g = R[name]
        C, Rm = second_order(g, mask)
        c1, _, _ = first_order(g, mask)
        # by separation
        bysep = {}
        for s in range(1, m):
            vals = [C[i, i + s] for i in range(m - s)]
            bysep[s] = (float(np.max(vals)), float(np.mean(vals)))
        rowsum = 0.5 * C.sum(axis=1)
        dob = np.tanh(C / (4 * KT300)).sum(axis=1)
        results[f"{alphabet}|{n}|{name}"] = dict(C=C.tolist(), rms=Rm.tolist(), c1=c1.tolist(), bysep={str(s): v for s, v in bysep.items()},
                                                rowsum_half=rowsum.tolist(), dobrushin=dob.tolist())
        print(f"--- {name}: first-order c_i max {c1.max():.2f};  second-order c_ij: max {C.max():.2f} kcal/mol = {C.max()/KT300:.1f} kT")
        print("    max c_ij by separation |i-j| = 1..: " + " ".join(f"{bysep[s][0]:.2f}" for s in range(1, m)))
        print("    mean c_ij by separation:           " + " ".join(f"{bysep[s][1]:.2f}" for s in range(1, m)))
        print(f"    half row sums (1/2) sum_j c_ij: {rowsum}")
        print(f"    Dobrushin-type row sums sum_j tanh(beta c_ij/4): max {dob.max():.2f} (Theorem 11.33(a) needs < 1)")
        if name in ("GB", "ff03-ff14SB") and n <= 4:
            print("    full matrix c_ij:"); print(C)
    # ANOVA of GB etc. on the FULL product grid is polluted by overlapping conformations for n >= 4;
    # do it only where the clash-free domain is the full product or nearly so (reported), else on
    # the sub-product of states that never clash locally.
    for name in ("GB", "coul+GB", "ff03-ff14SB"):
        g = R[name]
        if mask.mean() > 0.999:
            an = anova(g)
            tot = an["var_total"]
            print(f"--- ANOVA {name} (full product, uniform weights): variance {tot:.3f} (kcal/mol)^2; fraction by order 1..: "
                  + " ".join(f"{v/tot:.4f}" for v in an["by_order"][1:]))
json.dump(results, open(res_path, "w"), indent=0)
