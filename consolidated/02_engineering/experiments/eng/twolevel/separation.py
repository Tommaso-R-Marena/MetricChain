"""X-009: from which size on is Algorithm 2L+ *certified* cheaper than every non-adaptive algorithm?

Requested by the Scientific Discovery Division (SCI-REV-0007 §5 and request R6-E1): recompute its
table with the engineering evaluator, with and without the lowered sample cap, in a window around
each crossover.  Everything here is a finite expression in binomial coefficients:

  ln C_max        the cost bound of Theorem 11.56 with the base family inside (holds in every run on
                  every instance, by the abort rule) -- ``alg2l.lC_max``;
  ln C_max^cap    the same with M_bar replaced by the lowered cap 2 max{e^lam M_dagger, M_ddagger}
                  (THY-RES-0004 §3; K, m_max, delta' unchanged, as in SCI-REV-0007's R6_REPORT §2.9);
  ln LB_na        the non-adaptive lower bound of Theorem 11.45(b) at the certified accuracy x_out:
                  (1 - 2 delta) 2^n / |B(n, R-1)|, R the least radius with D_R > x_out,
                  D_R = n ln(1 + e^-u) - ln sum_j C(n, j) e^{-u max(j, R)};
  plain, hinted   the two-sample bracket in dimension n and the hinted lower bound (as in X-005).

    python experiments/eng/twolevel/separation.py --out experiments/eng/twolevel/results/x009_separation.json
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
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_search  # noqa: E402
from metricchain_eng.twolevel.alg2l import (constants, inner_costs, lC_max, logsumexp, lowered_sample_cap)  # noqa: E402
from metricchain_eng.twolevel.tables import LN2, CubeTables  # noqa: E402

# the science division's published values (SCI-REV-0007 §5 and R6_REPORT §2.9): (u, n) -> (ln C_max, ln LB_na, ln plain, ln hinted), phi = 0.5
THEIRS = {(1.0, 1000): (126.3, 110.9, 149.7, 31.7), (1.0, 1350): (150.8, 149.0, 193.9, 42.0), (1.0, 1400): (154.0, 155.0, 199.9, 43.5),
          (1.0, 2000): (193.1, 221.1, 273.0, 61.1), (1.0, 4000): (320.8, 441.3, 511.1, 120.1), (1.0, 8000): (566.9, 883.1, 976.9, 236.8),
          (1.0, 16000): (1045.1, 1767.6, 1897.4, 470.3), (2.0, 520): (170.1, 169.1, 228.8, 53.4), (2.0, 540): (173.9, 176.5, 236.2, 55.1),
          (2.0, 1000): (264.1, 327.2, 402.7, 100.4), (2.0, 4000): (814.3, 1306.6, 1448.0, 393.2), (0.5, 4500): (136.3, 135.7, 166.8, 37.3),
          (0.5, 4700): (139.6, 141.5, 173.7, 39.0), (0.5, 8000): (197.4, 240.7, 279.9, 64.5), (0.5, 11000): (249.3, 331.1, 375.8, 87.5)}
# their crossovers with the lowered cap (R6_REPORT §2.9): (u, n) -> (ln C_max^cap at phi = 0.55, ln LB_na)
THEIRS_CAP = {(1.0, 1275): (140.56, 140.50), (1.0, 1300): (142.95, 144.00), (2.0, 475): (156.38, 155.60), (2.0, 500): (162.53, 163.78),
              (0.5, 4000): (121.16, 120.61), (0.5, 4150): (124.08, 124.99)}
WINDOWS = {1.0: range(1150, 1501, 10), 2.0: range(420, 601, 5), 0.5: range(3700, 4901, 25)}
BEYOND = {1.0: (1600, 2000, 2800, 4000, 5600, 8000, 11000, 16000), 2.0: (650, 800, 1000, 1400, 2000, 2800, 4000), 0.5: (5200, 6000, 8000, 11000, 16000)}
PHIS = (0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70)


def lLB_na(n: int, u: float, x: float, delta: float, t: CubeTables | None = None) -> tuple[float, int]:
    """(ln LB_na, R) of Theorem 11.45(b)."""
    t = t if t is not None else CubeTables(n, u)
    j = np.arange(n + 1, dtype=float)
    lb = t.lbinom
    # ln sum_j C(n, j) e^{-u max(j, R)} for every R: the part j < R weighs e^{-uR}, the part j >= R weighs e^{-uj}
    lo = np.concatenate([[-np.inf], np.logaddexp.accumulate(lb)])[: n + 1]              # ln sum_{j < R} C(n, j)
    hi = np.logaddexp.accumulate((lb - u * j)[::-1])[::-1]                                # ln sum_{j >= R} C(n, j) e^{-uj}
    D = n * math.log1p(math.exp(-u)) - np.logaddexp(lo - u * j, hi)
    R = int(np.argmax(D > x))
    if not D[R] > x:
        return -math.inf, -1
    return math.log(1 - 2 * delta) + n * LN2 - t.lball_at(R - 1), R


def cost_bounds(n: int, u: float, phi: float, design: dict = run_search.DESIGN) -> dict:
    P, _ = run_search.design_params(n, u, phi, design)
    outer = CubeTables(P.n_o, u)
    C = constants(P, outer)
    lC = inner_costs(P, C)
    lcap = lowered_sample_cap(P, outer, C)
    terms = [0.0, LN2 + lcap]
    for l in range(1, P.L + 1):
        terms.append(min(LN2 + lcap, math.log(C.J + 1) + C.lcnt(P.xs[l - 1], P)) + float(lC[l]))
    return dict(lCmax=lC_max(P, C, lC), lCmax_cap=logsumexp(terms), x_out=C.x_out, r_dag=C.r_dag, K=C.K, n_o=P.n_o)


def row(n: int, u: float, phis=PHIS, design: dict = run_search.DESIGN) -> dict:
    cb = {phi: cost_bounds(n, u, phi, design) for phi in phis}
    x_out = cb[phis[0]]["x_out"]
    t = CubeTables(n, u)
    lb, R = lLB_na(n, u, x_out, design["delta"], t)
    ref = run_search.reference_columns(u, n, x_out, design["delta"])
    best = min(phis, key=lambda p: cb[p]["lCmax"])
    best_cap = min(phis, key=lambda p: cb[p]["lCmax_cap"])
    return dict(u=u, n=n, x_out=x_out, lLB_na=lb, R=R, plain=ref["plain"], hinted=ref["lower"],
                lCmax=cb[best]["lCmax"], phi=best, lCmax_cap=cb[best_cap]["lCmax_cap"], phi_cap=best_cap,
                lCmax_at_half=cb[0.5]["lCmax"] if 0.5 in cb else None,
                lCmax_cap_at_055=cb[0.55]["lCmax_cap"] if 0.55 in cb else None)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    t0 = time.time()
    res = dict(design=run_search.DESIGN, phis=PHIS, validation=[], validation_cap=[], window=[], beyond=[])
    for (u, n), theirs in THEIRS.items():
        r = row(n, u)
        r["theirs"] = theirs
        res["validation"].append(r)
        print(f"u={u} n={n}: lCmax(phi=0.5) {r['lCmax_at_half']:.1f} ({theirs[0]})  LB_na {r['lLB_na']:.1f} ({theirs[1]})  plain {r['plain']:.1f} ({theirs[2]})"
              f"  hinted {r['hinted']:.1f} ({theirs[3]})", flush=True)
    for (u, n), theirs in THEIRS_CAP.items():
        r = row(n, u)
        r["theirs"] = theirs
        res["validation_cap"].append(r)
        print(f"u={u} n={n}: lCmax_cap(phi=0.55) {r['lCmax_cap_at_055']:.2f} ({theirs[0]})  LB_na {r['lLB_na']:.2f} ({theirs[1]})", flush=True)
    for u, ns in WINDOWS.items():
        for n in ns:
            res["window"].append(row(n, u))
        w = [r for r in res["window"] if r["u"] == u]
        first = next((r["n"] for r in w if r["lCmax"] < r["lLB_na"]), None)
        first_cap = next((r["n"] for r in w if r["lCmax_cap"] < r["lLB_na"]), None)
        print(f"u={u}: least n of the window with C_max < LB_na: {first}; with the lowered cap: {first_cap}", flush=True)
    for u, ns in BEYOND.items():
        for n in ns:
            res["beyond"].append(row(n, u))
    res["seconds"] = time.time() - t0
    if args.out:
        Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
