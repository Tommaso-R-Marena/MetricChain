"""The coordinator's own checks of the validation campaign (experiments/eng/certinf/), independent of its table
generator `make_tables.py`:

 1. the verdict numbers of the hypotheses H-A, H-B, H-C, H-E, H-F recomputed from the raw rows with separate code;
 2. the exact reference M0 on F3 (ellipsoid region), which the campaign computed by the descent route with no
    independent check (its deviation D10): recomputed by the cutting-plane route, with a lower bound of the
    minimum from a cutting-plane model built here (Kelley), so that the optimality gap of each end is known.

    python experiments/eng/phase2_coord_checks/check_campaign.py [--skip-f3]
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "experiments" / "eng" / "certinf"))
from metricchain_eng import certinf as ci  # noqa: E402
import instances as ins  # noqa: E402

RES = REPO / "experiments" / "eng" / "certinf" / "results"
TOL = 1e-9
NOMINAL = {"0.2": 1.5, "0.55": 3.0, "1.15": 10.0, "1.7": 30.0, "2.3": 100.0, "var": 5.2}


def load():
    rows = []
    for p in sorted(glob.glob(str(RES / "validation" / "*.jsonl"))):
        with open(p) as fh:
            rows += [json.loads(line) for line in fh]
    return rows


def cells(rows, methods):
    out = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r["method"] in methods:
            out[(r["family"], r["target"], r["env"], r["n"])][r["method"]].append(r)
    return out


def med_excess(rs):
    return float(np.median([(r["hi"] - r["V_hi"]) + (r["V_lo"] - r["lo"]) for r in rs]))


def hypotheses(rows):
    res = {}
    # H-A: S3 covers I in every repetition on F1-F3
    s3 = [r for r in rows if r["method"] in ("M1", "M2") and r["family"] in ("F1", "F2", "F3")]
    res["H-A"] = dict(repetitions=len(s3), misses=sum(r["lo"] > r["V_lo"] + TOL or r["hi"] < r["V_hi"] - TOL for r in s3))
    # H-C: miss rate of each certified end of M3, M4, every cell of F1-F4
    worst, ncell = 0.0, 0
    for key, by in cells(rows, ("M3", "M4")).items():
        for m, rs in by.items():
            ncell += 1
            worst = max(worst, np.mean([r["hi"] < r["V_hi"] - TOL for r in rs]), np.mean([r["lo"] > r["V_lo"] + TOL for r in rs]))
    res["H-C"] = dict(cells=ncell, largest_miss_rate_of_an_end=float(worst))
    # H-B: Gamma >= 3, F1-F3: median excess M1 >= 5 x M3 unless M3 trivial; M1 trivial at n = 1000, Gamma >= 10
    below, below_m1_nontrivial, ratios, n_cells, m1_not_trivial_1000 = [], [], [], 0, 0
    for key, by in cells(rows, ("M1", "M3")).items():
        fam, tgt, env, n = key
        if fam not in ("F1", "F2", "F3") or NOMINAL[env] < 3.0:
            continue
        n_cells += 1
        e1, e3 = med_excess(by["M1"]), med_excess(by["M3"])
        m3_trivial = abs(np.median([r["hi"] - r["lo"] for r in by["M3"]]) - 2.0) < TOL
        m1_trivial = all(abs(r["lo"] + 1) < TOL and abs(r["hi"] - 1) < TOL for r in by["M1"])
        ratio = e1 / e3 if e3 > 0 else math.inf
        ratios.append(ratio)
        if ratio < 5 and not m3_trivial:
            below.append((key, round(ratio, 2), m1_trivial))
            if not m1_trivial:
                below_m1_nontrivial.append((key, round(ratio, 2)))
        if n == 1000 and NOMINAL[env] >= 10 and not m1_trivial:
            m1_not_trivial_1000 += 1
    res["H-B"] = dict(cells=n_cells, ratio_min=float(min(ratios)), ratio_median=float(np.median(ratios)), cells_below_5_with_M3_not_trivial=len(below),
                      of_which_M1_is_the_whole_range_in_every_repetition=sum(b[2] for b in below),
                      of_which_M1_is_not_trivial=[(list(k), v) for k, v in below_m1_nontrivial],
                      cells_n1000_gamma_ge_10_where_M1_is_not_trivial=m1_not_trivial_1000)
    # H-E: where M3 is not trivial (whole range in fewer than half of the repetitions): M3 <= M6 <= M5
    viol, n_e = 0, 0
    for key, by in cells(rows, ("M3", "M5", "M6")).items():
        if np.mean([abs(r["hi"] - r["lo"] - 2.0) < TOL for r in by["M3"]]) >= 0.5:
            continue
        n_e += 1
        e3, e5, e6 = med_excess(by["M3"]), med_excess(by["M5"]), med_excess(by["M6"])
        viol += not (e3 <= e6 + TOL and e6 <= e5 + TOL)
    res["H-E"] = dict(cells=n_e, violations=viol)
    # H-F(i): B1 misses an end of I, n = 1000, Gamma >= 10
    rates = {}
    for key, by in cells(rows, ("B1",)).items():
        fam, tgt, env, n = key
        if n == 1000 and NOMINAL[env] >= 10:
            rates["/".join(map(str, key))] = float(np.mean([not (r["lo"] <= r["V_lo"] and r["hi"] >= r["V_hi"]) for r in by["B1"]]))
    res["H-F(i)"] = dict(cells=len(rates), above_5_percent=sum(v > 0.05 for v in rates.values()), largest=max(rates.values()), rates=rates)
    # H-F(ii): B2 inside I; H-F(iii): B3 median width against |I| for Gamma <= 10
    b2 = {k: float(np.mean([r["V_lo"] - TOL <= r["lo"] <= r["V_hi"] + TOL and r["status"] == "ok" for r in by["B2"]]))
          for k, by in cells(rows, ("B2",)).items() if k[0] in ("F1", "F2", "F3")}
    res["H-F(ii)"] = dict(cells=len(b2), min_rate=min(b2.values()), cells_below_0_95=["/".join(map(str, k)) for k, v in b2.items() if v < 0.95])
    b3 = {}
    for key, by in cells(rows, ("B3",)).items():
        fam, tgt, env, n = key
        if fam in ("F1", "F2", "F3") and NOMINAL[env] <= 10:
            r0 = by["B3"][0]
            b3["/".join(map(str, key))] = float(np.median([r["hi"] - r["lo"] for r in by["B3"]]) / (r0["V_hi"] - r0["V_lo"]))
    res["H-F(iii)"] = dict(cells=len(b3), min_ratio=min(b3.values()), cells_below_2={k: round(v, 3) for k, v in b3.items() if v < 2})
    return res


def kelley_gap(P, eta, iters=400):
    """T(eta) minus a lower bound of min T over the cube of half-side 5 max(1, |eta|) around eta: the minimum of a
    cutting-plane model built from values and subgradients of T = tau_root (convex).  Returns (T(eta), gap, interior)."""
    m = len(eta)
    centre, rad = np.asarray(eta, float).copy(), 5.0 * max(1.0, float(np.abs(eta).max()))
    best_x, best = centre.copy(), ci.tau_root(P, centre)
    rows, rhs, x, low = [], [], centre.copy(), -math.inf
    for _ in range(iters):
        fx, g = ci.tau_root(P, x), ci.tau_grad(P, x)
        if fx < best:
            best_x, best = x.copy(), fx
        rows.append(np.concatenate([g, [-1.0]]))
        rhs.append(float(g @ x) - fx)
        r = linprog(np.concatenate([np.zeros(m), [1.0]]), A_ub=np.array(rows), b_ub=np.array(rhs),
                    bounds=[(c - rad, c + rad) for c in centre] + [(None, None)], method="highs")
        if r.status != 0:
            break
        low = r.fun
        if best - low <= 1e-11:
            break
        x = r.x[:m]
    return best, best - low, bool(np.abs(best_x - centre).max() < 0.9 * rad)


def f3_reference():
    I3 = ins.get("F3")
    ctx = json.loads((RES / "contexts.json").read_text())
    out = []
    for tgt in ("stress", "rg2"):
        for rho in ins.RHOS:
            region, _ = ins.data_region(I3, rho)
            l, u = I3.pi * math.exp(-rho), I3.pi * math.exp(rho)
            P = ci.lump(ci.box_problem(l, u, I3.targets[tgt], I3.phi, region))
            stored = ctx[f"F3|{tgt}|{rho:g}"]["m0"]
            rec = dict(target=tgt, rho=rho, stored=[stored["lo"], stored["hi"]])
            for side, prob, sgn in (("hi", P, 1.0), ("lo", P.negated(), -1.0)):
                t_pol, eta = ci.solve_upper(prob, "polish")
                best, gap, interior = kelley_gap(prob, eta)
                rec[side] = dict(polish=sgn * t_pol, kelley_best=sgn * best, gap_to_lower_bound=gap, incumbent_interior=interior,
                                 stored_minus_best=float(sgn * (stored[side] - sgn * best)))
            out.append(rec)
            print("F3 %-6s rho %.2f  hi: stored-best %.2e gap %.1e | lo: stored-best %.2e gap %.1e"
                  % (tgt, rho, rec["hi"]["stored_minus_best"], rec["hi"]["gap_to_lower_bound"], rec["lo"]["stored_minus_best"], rec["lo"]["gap_to_lower_bound"]), flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-f3", action="store_true")
    a = ap.parse_args()
    rows = load()
    hyp = hypotheses(rows)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "rates"} for k, v in hyp.items()}, indent=1))
    out = dict(rows=len(rows), hypotheses=hyp)
    if not a.skip_f3:
        out["f3_reference"] = f3_reference()
    d = Path(__file__).resolve().parent / "results"
    d.mkdir(exist_ok=True)
    (d / "check_campaign.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
