"""Review of ENG-RES-0016 §2, "What it gives": the base bracket of a MIXED block is "Proposition K0 with its largest slope,
by inclusion".  Every bound of §5 uses it (the inner blocks of the nested designs are mixed), and no literal run of the
division exercises it: X-014b serves the rungs by oracles, X-011f by enumeration.  Here the two-sample bracket of
K_REPORT §3.2 is run literally on small cubes with site-dependent slopes, with the tables of the uniform cube for

    the largest slope            (the claim),
    the sorted-slope tables      (Lemma N14 and its mirror image: valid as well, and never worse),
    the smallest slope           (negative control: the class is NOT contained in that uniform class).

Family of K_REPORT §3.2: eta = min(1/2, tanh(x/4)), K = ceil(3 (1+eta) eta^-2 ln(4/delta')), r* the largest radius <= d-1
with ln(1 + Gamma''(r')) <= x - ln((1+eta)/(1-eta)) for all r' <= r*, M = ceil(K 2^d / ((1-eta) |B(d, r*)|)); two samples of
size M; t = the K-th largest weight of the first, A^ = the mean of min(w, t) over the second;
L = A^/(1+eta), U = A^/(1-eta) + t 2^-d E_r^ with r^ the least radius with |B(d, r^)| >= 2^d K/((1-eta) M).
Claimed: L <= A <= U and U <= e^x L except with probability delta'.

    python experiments/eng/review_x014/check_k0_mixed.py [--minutes 5]          # writes check_k0_mixed.json
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
DELTA_P = 0.05
BLOCKS = [  # slopes of the block (14-16 sites: below that, enumeration is cheaper than the two samples and nothing is tested)
    (2.0,) * 4 + (0.5,) * 10,
    (3.0,) * 2 + (0.2,) * 12,
    (1.5,) * 4 + (1.0,) * 4 + (0.3,) * 6,
    (4.0,) * 2 + (0.25,) * 12,
    (0.9, 0.7, 0.5, 0.3, 0.1) * 3,
    (6.0,) + (0.05,) * 13,
    (1.0,) * 8 + (0.9,) * 8,
]
ACCURACIES = [1.0, 2.0, 4.0, 8.0, 14.0]
TABLES = ("largest slope (the claim)", "sorted slopes", "CONTROL: smallest slope")


def design(us, x: float, which: int):
    d = len(us)
    etaf = min(0.5, math.tanh(x / 4))
    eta = Fraction(etaf).limit_denominator(10 ** 6)
    if which == 0:
        T = rs.OuterTables(d, max(us), eta)
    elif which == 1:
        T = rs.OuterTables(d, max(us), eta, depth_cost=rs.sorted_depth_cost(us))
    else:
        T = rs.OuterTables(d, min(us), eta)
    budget = x - math.log((1 + etaf) / (1 - etaf))
    rstar = -1
    for r in range(d):
        if budget > 0 and math.log1p(math.exp(T.lG2[r])) <= budget:
            rstar = r
        else:
            break
    if rstar < 0:
        return None
    K = math.ceil(3 * (1 + etaf) / etaf ** 2 * math.log(4 / DELTA_P))
    M = math.ceil(Fraction(K * 2 ** d) / ((1 - eta) * T.ball[rstar]))
    if M > 4_000_000:                                 # the sample is too large for this script (validity does not depend on
        return None                                   # whether enumeration would be cheaper, so M >= 2^d is not excluded)
    return dict(T=T, eta=eta, etaf=etaf, K=K, M=M, rstar=rstar)


def one_run(psi, D, rng):
    d = int(round(math.log2(len(psi))))
    w = -psi                                          # ln of the weights
    lA = float(np.logaddexp.reduce(w) - d * LN2)
    M, K, T, eta, etaf = D["M"], D["K"], D["T"], D["eta"], D["etaf"]
    s1 = w[rng.integers(0, 2 ** d, size=M)]
    s2 = w[rng.integers(0, 2 ** d, size=M)]
    lt = float(np.partition(s1, M - K)[M - K])        # the K-th largest
    lAhat = float(np.logaddexp.reduce(np.minimum(s2, lt)) - math.log(M))
    lL = lAhat - math.log(1 + etaf)
    q = Fraction(K) / ((1 - eta) * M)
    if 2 ** d * q < 1:
        ltail = -math.inf
    else:
        r = T.closing_radius(2 ** d * q)
        if r > d - 1:
            return None
        ltail = lt - d * LN2 + T.lE[r]
    lU = float(np.logaddexp(lAhat - math.log(1 - etaf), ltail))
    return lA, lL, lU


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=5.0)
    args = ap.parse_args()
    rs.limit_memory(2.0)
    t0 = time.time()
    rng = np.random.default_rng(5772)
    rows = []
    jobs = [(bi, x, which) for which in range(3) for bi in range(len(BLOCKS)) for x in ACCURACIES]
    per = args.minutes * 60 / len(jobs)
    for bi, x, which in jobs:
        us = np.array(BLOCKS[bi])
        D = design(list(us), x, which)
        row = dict(slopes=list(BLOCKS[bi]), x=x, tables=TABLES[which])
        if D is None:
            row["skipped"] = "no radius qualifies, or the samples are too large"
            rows.append(row)
            continue
        row.update(K=D["K"], M=D["M"], r_star=D["rstar"], runs=0, invalid=0, too_wide=0, max_width=0.0, class_violation=-math.inf, by_kind={})
        t1 = time.time()
        i = 0
        n_o = max(1, len(us) // 2)                    # only used by the instance generator (which sites the "outer" landscapes live on)
        while time.time() - t1 < per:
            kind = rs.INSTANCE_KINDS[i % len(rs.INSTANCE_KINDS)]
            i += 1
            psi = rs.instance(kind, us, n_o, rng)
            row["class_violation"] = max(row["class_violation"], rs.class_violation(psi, us))
            for _ in range(4):
                res = one_run(psi, D, rng)
                if res is None:
                    continue
                lA, lL, lU = res
                row["runs"] += 1
                bk = row["by_kind"].setdefault(kind, dict(runs=0, invalid=0))
                bk["runs"] += 1
                bad = not (lL <= lA + 1e-9 and lA <= lU + 1e-9)
                row["invalid"] += bad
                bk["invalid"] += bad
                row["too_wide"] += (lU - lL) > x + 1e-9
                row["max_width"] = max(row["max_width"], lU - lL)
        rows.append(row)
    summ = {}
    for r in rows:
        if "skipped" in r:
            continue
        s = summ.setdefault(r["tables"], dict(configurations=0, runs=0, invalid=0, too_wide=0, largest_invalid_fraction_in_a_configuration=0.0,
                                              largest_too_wide_fraction_in_a_configuration=0.0))
        s["configurations"] += 1
        s["runs"] += r["runs"]
        s["invalid"] += r["invalid"]
        s["too_wide"] += r["too_wide"]
        if r["runs"]:
            s["largest_invalid_fraction_in_a_configuration"] = max(s["largest_invalid_fraction_in_a_configuration"], r["invalid"] / r["runs"])
            s["largest_too_wide_fraction_in_a_configuration"] = max(s["largest_too_wide_fraction_in_a_configuration"], r["too_wide"] / r["runs"])
    out = dict(delta_prime=DELTA_P, summary=summ, rows=rows, seconds=time.time() - t0)
    (HERE / "check_k0_mixed.json").write_text(json.dumps(out, indent=1, default=float))
    for k, s in summ.items():
        print(k, json.dumps(s, default=float))
    for r in rows:
        if "skipped" not in r and (r["invalid"] or r["too_wide"]):
            print("   ", r["tables"], r["slopes"], "x", r["x"], "runs", r["runs"], "invalid", r["invalid"], "too wide", r["too_wide"],
                  {k: v for k, v in r["by_kind"].items() if v["invalid"]})
    print(f"[{time.time() - t0:.0f} s]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
