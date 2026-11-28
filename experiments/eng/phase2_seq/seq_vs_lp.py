"""How loose is the sequential bound of Proposition 9.6?  Bounded-influence class on a cube of 10 binary sites with a
product reference, against the exact programme over all 1024 configurations.

    python experiments/eng/phase2_seq/seq_vs_lp.py        # writes results/seq_vs_lp.json and prints a table
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from metricchain_eng import certinf as ci  # noqa: E402

n = 10
rng = np.random.default_rng(2026)
states, edges, site = ci.hypercube(n)
p1 = rng.uniform(0.25, 0.75, n)
pi = np.prod(np.where(states == 1, p1, 1 - p1), axis=1)
site_pi = [[1 - p, p] for p in p1]
stats = [[[0, 0], [1, 0]] if i < 5 else [[0, 0], [0, 1]] for i in range(n)]
s1, s2 = states[:, :5].sum(axis=1).astype(int), states[:, 5:].sum(axis=1).astype(int)
k1, k2 = np.meshgrid(np.arange(6), np.arange(6), indexing="ij")
targets = {"monotone: at least six ones": (k1 + k2 >= 6).astype(float),
           "additive: fraction of ones": (k1 + k2) / 10.0,
           "difference of the two blocks, absolute": np.abs(k1 - k2) / 5.0,
           "window: exactly two ones in block 1": (k1 == 2).astype(float),
           "product: (S1/5)(1 - S2/5)": (k1 / 5.0) * (1 - k2 / 5.0)}
rows = []
for u in (0.3, 0.7):
    C = np.full(len(edges), np.exp(u))
    for data in ("none", "mean of S2/5 in a box"):
        box = ci.Box([float(pi @ s2) / 5 + 0.05], 0.03) if data != "none" else None
        phi_x = (s2 / 5.0)[:, None] if box else None
        phi_k = (k2 / 5.0)[..., None] if box else None
        for name, tg in targets.items():
            lp = ci.lp_ratio_class(pi, edges, C, tg[s1, s2], phi_x, box)
            sq = ci.sequential_interval(site_pi, u, stats, tg, phi_k, box)
            rows.append(dict(slope=u, data=data, target=name, lp_lo=lp[0], lp_hi=lp[1], seq_lo=sq["lo"], seq_hi=sq["hi"],
                             width_exact=lp[1] - lp[0], width_seq=sq["hi"] - sq["lo"], sound=bool(sq["lo"] <= lp[0] + 1e-7 and sq["hi"] >= lp[1] - 1e-7)))
Path(__file__).resolve().parent.joinpath("results", "seq_vs_lp.json").write_text(json.dumps(rows, indent=1))
print("| slope | data | target | exact interval (programme) | sequential bound | width ratio |")
print("|---|---|---|---|---|---|")
for r in rows:
    print(f"| {r['slope']} | {r['data']} | {r['target']} | [{r['lp_lo']:.4f}, {r['lp_hi']:.4f}] | [{r['seq_lo']:.4f}, {r['seq_hi']:.4f}] | {r['width_seq'] / r['width_exact']:.3f} |")
print("sound in every row:", all(r["sound"] for r in rows))
