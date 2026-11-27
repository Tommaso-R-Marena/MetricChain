#!/usr/bin/env python3
"""merge R tables of several runs: python3 t09b_merge.py out_tag in_tag1 in_tag2 ..."""
import sys
import numpy as np
rows = np.vstack([np.loadtxt(f"../out/Rtable_{t}.txt") for t in sys.argv[2:]])
rows = rows[np.argsort(rows[:, 0])]
keep = np.r_[True, np.diff(rows[:, 0]) > 1e-12]
rows = rows[keep]
with open(f"../out/Rtable_{sys.argv[1]}.txt", "w") as f:
    f.write("# merged: e, R_H(e), m, a, b, n_mu*(e+R_H(e))\n")
    for r in rows:
        f.write(" ".join(f"{v:.10f}" for v in r) + "\n")
print(len(rows), "rows; R nonincreasing:", bool(np.all(np.diff(rows[:, 1]) <= 1e-9)), "; S=e+R nondecreasing:", bool(np.all(np.diff(rows[:, 0] + rows[:, 1]) >= -1e-9)))
