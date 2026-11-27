"""THY-REQ-0008, question 5: distance entropy of the profile classes of the generic (off-lattice) chain.

For n torsions (N = n + 3 beads) and radii R = rho * N, rho in {1/4, 1/2, 1} / L with L in {1, 1/5}:

    m_c(R)   = number of profile classes within profile distance R of class c (c itself included)
    sigma    = ln(m_c(R)) / n      reported as  median over classes,  mean of ln over classes,
                                   mean of ln weighted by the number of conformations in the class

and the number of pairs per bead within the cutoff (mean over classes, mean over conformations,
maximum).  The profile distance is the l1 distance of sorted truncated squared distances
(P_REPORT Proposition 2).  Output: results/generic_Sc16_entropy.json.

    python experiments/eng/chain_cover/generic_entropy.py --nmin 5 --nmax 13
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.chains.generic_chain import enumerate_generic  # noqa: E402

RHOS = (0.25, 0.5, 1.0, 1.25, 2.5, 5.0)        # {1/4, 1/2, 1} for L = 1 and {5/4, 5/2, 5} for L = 1/5


def analyse(n: int) -> dict:
    t0 = time.time()
    tab = enumerate_generic(n)
    t_enum = time.time() - t0
    N = n + 3
    V = tab.sorted_truncated().astype(np.float64)
    ncl = V.shape[0]
    radii = np.array([rho * N for rho in RHOS])
    counts = np.zeros((ncl, len(RHOS)), dtype=np.int64)
    chunk = max(1, int(2.0e8 // (ncl * V.shape[1] * 8)))          # about 200 MB per block
    for i in range(0, ncl, chunk):
        D = np.abs(V[i:i + chunk, None, :] - V[None, :, :]).sum(axis=2)
        for k, R in enumerate(radii):
            counts[i:i + chunk, k] = (D <= R + 1e-9).sum(axis=1)
    w = tab.count / tab.count.sum()
    below = np.array([len(v) for v in tab.below], dtype=float)
    row = dict(n_torsions=n, n_beads=N, conformations=int(tab.n_conformations), classes=int(ncl),
               ln_classes_per_torsion=math.log(ncl) / n,
               pairs_per_bead=dict(mean_over_classes=float(below.mean() / N), mean_over_conformations=float((below * w).sum() / N),
                                   max=float(below.max() / N)),
               sigma={}, seconds=dict(enumeration=t_enum))
    for k, rho in enumerate(RHOS):
        lm = np.log(counts[:, k].astype(float))
        row["sigma"][f"{rho:g}"] = dict(radius=float(radii[k]), median=float(np.median(lm) / n), mean=float(lm.mean() / n),
                                        mean_weighted=float((lm * w).sum() / n), min=float(lm.min() / n), max=float(lm.max() / n),
                                        median_count=float(np.median(counts[:, k])))
    row["seconds"]["total"] = time.time() - t0
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=5)
    ap.add_argument("--nmax", type=int, default=12)
    args = ap.parse_args()
    out = ROOT / "experiments" / "eng" / "chain_cover" / "results" / "generic_Sc16_entropy.json"
    data = json.loads(out.read_text()) if out.exists() else dict(model="gen", s_cut=16.0, rhos=list(RHOS), rows={})
    for n in range(args.nmin, args.nmax + 1):
        row = analyse(n)
        data["rows"][str(n)] = row
        out.write_text(json.dumps(data, indent=1))
        s = row["sigma"]
        print(f"n={n:2d} conformations={row['conformations']:7d} classes={row['classes']:6d} pairs/bead={row['pairs_per_bead']['mean_over_classes']:.2f} "
              + " ".join(f"sigma({k})={v['mean']:.3f}" for k, v in s.items()) + f"  ({row['seconds']['total']:.0f} s)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
