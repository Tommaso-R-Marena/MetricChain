"""Review of ENG-RES-0016 §2: the one place where the transfer touches validity through the OUTER slope — Lemma K.2
("-ln W is in L_{u_o}(Q_{n_o})") followed by Lemma K.1(a),(b) on the outer cube — tested directly, at EVERY threshold and
not only at those a run of the algorithm happens to visit (bracket-level tests have little power against an error in the
upper tail function: see ``attack.py tuned``).

For an instance psi of the class on Q_{n_o} x Y let W be the table of fibre averages.  For every value s of W:
    D = {W > s}, r the least radius with |B(n_o, r)| >= |D|;   if r <= n_o - 1:   E(W - s)_+ <= s 2^-n_o E_r      (K.1(a))
    S = {W >= s}, k the largest radius with |B(n_o, k)| <= |S|:                   E min(W, s) >= s 2^-n_o T(k)   (K.1(b))
and the largest slope of -ln W along an outer edge is at most u_o (K.2).  Tables: the uniform cube with the outer slope
(the claim), for an outer block of several slopes the sorted-slope tables (Lemma N14 and its mirror image), and as
negative controls tables for half the outer slope / for the slopes sorted the wrong way.

    python experiments/eng/review_x014/check_tail_lemma.py [--minutes 4]        # writes check_tail_lemma.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import review_sim as rs  # noqa: E402

LN2 = math.log(2.0)
SHAPES = [  # (outer slopes, inner slopes)
    ((0.5,) * 8, (2.0, 2.0, 2.0)), ((2.0,) * 7, (0.5, 0.5, 0.5, 0.5)), ((0.05,) * 6, (5.0, 5.0, 5.0)), ((3.0,) * 5, (0.05,) * 4), ((0.3,) * 9, (10.0,)),
    ((1.0,) * 5, (1.0, 1.0, 2.0)), ((1.37,) * 4, (0.83, 2.11, 0.29)), ((0.2,) * 10, (2.0, 0.7)), ((1.5,) * 9, (0.2, 0.2, 0.2)), ((0.7,) * 10, (0.3,)),
    # mixed outer blocks
    ((2.0, 2.0, 0.5, 0.5, 0.5), (1.0, 1.0, 1.0)), ((3.0, 0.2, 0.2, 0.2, 0.2, 0.2), (0.7, 2.0)), ((1.5, 1.5, 1.5, 1.0, 1.0, 0.3, 0.3), (2.5,)),
    ((4.0, 4.0, 0.25, 0.25, 0.25, 0.25), (0.5, 0.5, 0.5)), ((6.0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05), (1.0, 0.2)),
]


def tables_for(outer, which: str):
    m = len(outer)
    if which == "claim":
        T = rs.OuterTables(m, max(outer), Fraction(1, 2), depth_cost=rs.sorted_depth_cost(outer))       # = uniform tables for one slope
    elif which == "half slope":
        T = rs.OuterTables(m, max(outer), Fraction(1, 2), depth_cost=rs.sorted_depth_cost([u / 2 for u in outer]))
    else:                                                    # slopes sorted the wrong way (smallest first); for one slope: 0.8 of it
        srt = sorted(outer) if len(set(outer)) > 1 else [0.8 * u for u in outer]
        cum = [0.0] + list(np.cumsum(srt))
        T = rs.OuterTables(m, srt[0], Fraction(1, 2), depth_cost=lambda i: cum[i] if i <= m else cum[m] + srt[-1] * (i - m))
    return np.array([float(b) for b in T.ball]), np.array(T.lE[:m]), np.array(T.lT)


def check_instance(lW: np.ndarray, m: int, tabs) -> tuple:
    """(largest ratio E(W - s)_+ / bound, largest ratio bound / E min(W, s)) over all thresholds s among the values of W."""
    ball, lE, lT = tabs
    w = np.sort(lW)[::-1]                                     # decreasing
    P = len(w)
    vals, first = np.unique(-w, return_index=True)            # distinct values, decreasing in w; first index of each
    vals = -vals
    up, low = 0.0, 0.0
    cum = np.logaddexp.accumulate(w)                          # ln sum of the i+1 largest
    tot_rev = np.logaddexp.accumulate(w[::-1])[::-1]          # ln sum of w[i:]
    for v, i in zip(vals, first):
        cnt_gt = i                                            # |{W > v}|
        cnt_ge = int(np.searchsorted(-w, -v, side="right"))   # |{W >= v}|
        if cnt_gt > 0:
            r = int(np.searchsorted(ball, cnt_gt, side="left"))
            if r <= m - 1:
                # E (W - v)_+ / v = (sum_{W > v} W)/v/P - cnt/P
                ex = (math.exp(cum[cnt_gt - 1] - v) - cnt_gt) / P
                up = max(up, ex / math.exp(lE[r] - m * LN2))
        if cnt_ge == P:                                       # S = the whole cube: both sides equal s, a trivial equality — not counted
            continue
        k = int(np.searchsorted(ball, cnt_ge, side="right")) - 1
        # E min(W, v)/v = cnt_ge/P + (sum_{W < v} W)/v/P
        rest = math.exp(tot_rev[cnt_ge] - v)
        trunc = (cnt_ge + rest) / P
        low = max(low, math.exp(lT[k] - m * LN2) / trunc)
    return up, low


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=4.0)
    args = ap.parse_args()
    rs.limit_memory(2.0)
    t0 = time.time()
    rng = np.random.default_rng(141421)
    rows = []
    per = args.minutes * 60 / len(SHAPES)
    for outer, inner in SHAPES:
        us = np.array(outer + inner)
        m, n_i = len(outer), len(inner)
        tabs = {w: tables_for(list(outer), w) for w in ("claim", "half slope", "wrong order / 0.8 of the slope")}
        row = dict(outer=list(outer), inner=list(inner), instances=0, thresholds=0, max_outer_slope_of_minus_ln_W_over_allowed=0.0,
                   **{f"{w}: max upper ratio": 0.0 for w in tabs}, **{f"{w}: max lower ratio": 0.0 for w in tabs}, by_kind={})
        idx = np.arange(2 ** m)
        t1 = time.time()
        i = 0
        while time.time() - t1 < per:
            kind = rs.INSTANCE_KINDS[i % len(rs.INSTANCE_KINDS)]
            i += 1
            psi = rs.instance(kind, us, m, rng)
            tab = psi.reshape(2 ** n_i, 2 ** m).T
            lW = np.logaddexp.reduce(-tab, axis=1) - n_i * LN2
            # Lemma K.2: |ln W(a) - ln W(a + e_i)| <= u_i for every outer site i
            for site in range(m):
                row["max_outer_slope_of_minus_ln_W_over_allowed"] = max(row["max_outer_slope_of_minus_ln_W_over_allowed"],
                                                                        float(np.max(np.abs(lW - lW[idx ^ (1 << site)]))) / outer[site])
            row["instances"] += 1
            row["thresholds"] += len(np.unique(lW))
            bk = row["by_kind"].setdefault(kind, [0.0, 0.0])
            for wname, tb in tabs.items():
                up, low = check_instance(lW, m, tb)
                row[f"{wname}: max upper ratio"] = max(row[f"{wname}: max upper ratio"], up)
                row[f"{wname}: max lower ratio"] = max(row[f"{wname}: max lower ratio"], low)
                if wname == "claim":
                    bk[0], bk[1] = max(bk[0], up), max(bk[1], low)
        rows.append(row)
        print(f"outer {list(outer)} inner {list(inner)}: {row['instances']} instances, {row['thresholds']} thresholds; slope of -ln W / allowed <= "
              f"{row['max_outer_slope_of_minus_ln_W_over_allowed']:.6f}; claim: upper {row['claim: max upper ratio']:.6f}, lower {row['claim: max lower ratio']:.6f}; "
              f"half slope: {row['half slope: max upper ratio']:.3f}, {row['half slope: max lower ratio']:.3f}; "
              f"wrong order: {row['wrong order / 0.8 of the slope: max upper ratio']:.3f}, {row['wrong order / 0.8 of the slope: max lower ratio']:.3f}", flush=True)
    summ = dict(shapes=len(rows), instances=sum(r["instances"] for r in rows), thresholds=sum(r["thresholds"] for r in rows),
                claim_max_upper_ratio=max(r["claim: max upper ratio"] for r in rows), claim_max_lower_ratio=max(r["claim: max lower ratio"] for r in rows),
                claim_violations=sum((r["claim: max upper ratio"] > 1 + 1e-9) + (r["claim: max lower ratio"] > 1 + 1e-9) for r in rows),
                max_slope_ratio=max(r["max_outer_slope_of_minus_ln_W_over_allowed"] for r in rows),
                shapes_where_half_slope_tables_are_refuted=sum((r["half slope: max upper ratio"] > 1 + 1e-9) or (r["half slope: max lower ratio"] > 1 + 1e-9) for r in rows),
                shapes_where_the_second_control_is_refuted=sum((r["wrong order / 0.8 of the slope: max upper ratio"] > 1 + 1e-9)
                                                               or (r["wrong order / 0.8 of the slope: max lower ratio"] > 1 + 1e-9) for r in rows))
    (HERE / "check_tail_lemma.json").write_text(json.dumps(dict(summary=summ, rows=rows, seconds=time.time() - t0), indent=1, default=float))
    print(json.dumps(summ, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
