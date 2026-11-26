"""X-014c: a continuous profile of slopes, binned.

The sites have n different slopes, equally spaced on [u_min, u_max].  Type-aligned nesting needs blocks of one
slope, so the slopes are *binned*: m classes of equal size, every site of a class given the largest slope of its
class.  The binned class contains the original one (a function whose slope at site i is at most u_i has slope at
most the class maximum), so every procedure for the binned class is a procedure for the original, and its
certified bound is a bound for the original.  m = 1 is the homogeneous algorithm with u_max.

Per (n, m): the binned slopes, the asymptotic exponent of the binned class and of the original profile
(h = max_t mean_i F_{u_i}(t), theory report §11.26), and the certified bound of type-aligned nesting with at most
two nested levels (three "levels").

    python experiments/eng/twolevel/hetero_profile.py        # writes results/x014_profile.json
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel import hetero as H  # noqa: E402

LID = math.log(20.0)
PHIS = (0.60, 0.50, 0.40, 0.30, 0.25, 0.20, 0.15, 0.10)


def profile_h(us: np.ndarray) -> tuple[float, float]:
    """max over t in [0, 1] of the mean of F_u(t) over the sites (the profile's asymptotic exponent), and the t."""
    def F(t):
        return float(np.mean((1 - t) * math.log(2) - np.log1p(np.exp(-t * us)) + t * np.log1p(np.exp(-us))))
    lo, hi = 0.0, 1.0
    for _ in range(200):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if F(m1) < F(m2):
            lo = m1
        else:
            hi = m2
    t = 0.5 * (lo + hi)
    return F(t), t


def cell(n: int, m: int, u_min: float, u_max: float, max_levels: int = 2, time_limit: float = 1800.0) -> dict:
    t0 = time.time()
    us = u_min + (u_max - u_min) * (np.arange(n) + 0.5) / n                 # the original profile
    edges = [round(n * k / m) for k in range(m + 1)]
    bins = [(float(us[edges[k + 1] - 1]), edges[k + 1] - edges[k]) for k in range(m)]       # class maximum, class size
    B = H.make_block(bins)
    h_true, t_true = profile_h(us)
    h_bin, _ = profile_h(np.repeat([b[0] for b in bins], [b[1] for b in bins]))
    out = dict(n=n, m=m, u_min=u_min, u_max=u_max, bins=[list(b) for b in bins], h_profile=h_true, t_profile=t_true, h_binned=h_bin, rows=[])
    S = H.HSearch(PHIS)
    S.deadline = t0 + time_limit
    best_all = math.inf
    for k in range(1, max_levels + 1):
        row = dict(nested_levels=k, complete=True)
        try:
            best = None
            for j, kk in H.outer_choices(B, PHIS):
                cut = min(best_all, best.lCmax if best else math.inf) if k > 1 else (best.lCmax if best else math.inf)
                hb = S.top(B, H.top_design(j, kk), LID, k, cutoff=cut)
                if hb is not None:
                    best = hb
            if best is not None:
                best_all = min(best_all, best.lCmax)
                row.update(bound=best.lCmax / n, outer_slope=best.block[best.design.j][0], outer_sites=best.design.k, x_out=best.xout)
            else:
                row.update(bound=best_all / n)
        except TimeoutError:
            row["complete"] = False
        row["seconds"] = time.time() - t0
        out["rows"].append(row)
        if not row["complete"]:
            break
    out["seconds"] = time.time() - t0
    return out


def main() -> int:
    res = []
    for n in (4000, 16000):
        for m in (1, 2, 3, 4, 6):
            r = cell(n, m, 0.5, 2.0)
            res.append(r)
            print(f"n={n} m={m}: h(profile) {r['h_profile']:.5f}  h(binned) {r['h_binned']:.5f}  bounds per site: "
                  + ", ".join(f"{x['nested_levels'] + 1} levels {x.get('bound', float('nan')):.5f}" for x in r["rows"]) + f"  [{r['seconds']:.0f} s]", flush=True)
            (ROOT / "experiments" / "eng" / "twolevel" / "results" / "x014_profile.json").write_text(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
