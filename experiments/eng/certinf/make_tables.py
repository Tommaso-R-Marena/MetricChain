"""Regenerates every table of REPORT.md from the stored results (results/*.json, results/*.jsonl).

    python experiments/eng/certinf/make_tables.py --write    # writes REPORT.md (template: report_template.py)
    python experiments/eng/certinf/make_tables.py            # prints the filled report instead
    python experiments/eng/certinf/make_tables.py --print    # prints the generated blocks only

Definitions used (fixed before the results were read; see REPORT.md "Readings"):
  covers I        lo <= V- + 1e-9 and hi >= V+ - 1e-9
  excess          (hi - V+) + (V- - lo): the total excess of an interval over I (per end: hi - V+, V- - lo)
  miss of an end  the end is 'certified' and lies strictly inside I by more than 1e-9
  trivial         the interval is the whole declared range [-1, 1]
"""
from __future__ import annotations

import glob
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
TOL = 1e-9
# Gamma thresholds of the protocol refer to the nominal envelopes Gamma = e^{2 rho} ~ 1.5, 3, 10, 30, 100
# (e^{1.1} = 3.004, e^{2.3} = 9.974): comparisons use a 1 % tolerance.
DELTA = 0.05


def _mn(xs):
    xs = list(xs)
    return min(xs) if xs else math.nan


def load_jsonl(pattern):
    rows = []
    for p in sorted(glob.glob(str(pattern))):
        with open(p) as fh:
            rows += [json.loads(line) for line in fh if line.strip()]
    return rows


def fmt(x, nd=3):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "–"
    if isinstance(x, (bool, np.bool_)):
        return "yes" if x else "no"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if abs(x) >= 1e4 or (abs(x) < 1e-3 and x != 0):
        return f"{x:.2e}"
    return f"{x:.{nd}f}"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(fmt(v) if not isinstance(v, str) else v for v in r) + " |")
    return "\n".join(out)


def env_key(e):
    return 99.0 if e == "var" else float(e)


# ------------------------------------------------------------------------------------------------ cell statistics
def cell_stats(rows):
    a = lambda k: np.array([r[k] for r in rows], dtype=float)  # noqa: E731
    lo, hi, Vl, Vh, tr = a("lo"), a("hi"), a("V_lo"), a("V_hi"), a("true")
    method = rows[0]["method"]
    st = [r["status"] for r in rows]
    s = dict(reps=len(rows), gamma=rows[0]["gamma"], V_lo=Vl[0], V_hi=Vh[0], true=tr[0], I_w=Vh[0] - Vl[0])
    if method == "B2":
        ok = np.array([x == "ok" for x in st])
        inside = ok & (lo >= Vl - TOL) & (lo <= Vh + TOL)
        s.update(inside_I=inside.mean(), fail=1 - ok.mean(), med_value=np.median(lo), med_kish=np.median(a("kish")),
                 abs_err_true=np.median(np.abs(lo - tr)))
        return s
    valid = np.array([x not in ("empty",) for x in st])
    cov = valid & (lo <= Vl + TOL) & (hi >= Vh - TOL)
    covt = valid & (lo <= tr + TOL) & (hi >= tr - TOL)
    w = np.where(valid, hi - lo, 0.0)
    eh, el = hi - Vh, Vl - lo
    ex = np.where(valid, eh + el, np.nan)
    sth = np.array([r["st_hi"] for r in rows])
    stl = np.array([r["st_lo"] for r in rows])
    miss_hi = (sth == "certified") & (hi < Vh - TOL)
    miss_lo = (stl == "certified") & (lo > Vl + TOL)
    if method in ("B1", "B3"):
        miss_hi = valid & (hi < Vh - TOL) | ~valid
        miss_lo = valid & (lo > Vl + TOL) | ~valid
    trivial = (hi >= 1 - TOL) & (lo <= -1 + TOL)
    s.update(cov_I=cov.mean(), cov_true=covt.mean(), med_w=np.median(w), p90_w=np.quantile(w, 0.9),
             med_ex=np.nanmedian(ex) if valid.any() else math.nan, p90_ex=np.nanquantile(ex, 0.9) if valid.any() else math.nan,
             med_ex_hi=np.median(eh), p90_ex_hi=np.quantile(eh, 0.9), med_ex_lo=np.median(el), p90_ex_lo=np.quantile(el, 0.9),
             triv_hi=np.mean(sth == "trivial"), triv_lo=np.mean(stl == "trivial"), trivial=trivial.mean(),
             abstain=np.mean(np.array(st) == "abstain"), void=np.mean(np.array(st) == "void"),
             inconsistent=np.mean(np.array(st) == "inconsistent"), empty=np.mean(~valid),
             miss_hi=miss_hi.mean(), miss_lo=miss_lo.mean(),
             t_pre=np.nanmedian(a("t_pre")), t_samp=np.nanmedian(a("t_samp")),
             t_opt=np.nanmedian(a("t_opt")) if not np.all(np.isnan(a("t_opt"))) else math.nan,
             t_cert=np.nanmedian(a("t_cert")) if not np.all(np.isnan(a("t_cert"))) else math.nan,
             t_total=np.nanmedian(a("t_total")) if "t_total" in rows[0] else math.nan)
    if method in ("M1", "M2"):
        s["med_kappa"] = np.median(a("kappa"))
    return s


def grid():
    rows = load_jsonl(RES / "validation" / "*.jsonl")
    cells = defaultdict(list)
    for r in rows:
        cells[(r["family"], r["target"], r["env"], r["n"], r["method"])].append(r)
    return {k: cell_stats(v) for k, v in cells.items()}, rows


def ckeys(S, method=None, fams=("F1", "F2", "F3", "F4")):
    ks = [k for k in S if (method is None or k[4] == method) and k[0] in fams]
    return sorted(ks, key=lambda k: (k[0], k[1], env_key(k[2]), k[3], k[4]))


# ------------------------------------------------------------------------------------------------ hypotheses
def hypotheses(S, ctxs, struct, sens):
    H = []
    F13 = ("F1", "F2", "F3")
    # H-A
    misses, total = 0, 0
    worst = []
    for m in ("M1", "M2"):
        for k in ckeys(S, m, F13):
            total += S[k]["reps"]
            mm = int(round((1 - S[k]["cov_I"]) * S[k]["reps"]))
            misses += mm
            if mm:
                worst.append("/".join(map(str, k)))
    H.append(("H-A", "M1 and M2 cover I in every repetition on F1-F3; refuted by one miss",
              "holds" if misses == 0 else "refuted", f"{misses} misses in {total} repetitions" + (f" ({', '.join(worst[:4])})" if worst else "")))
    # H-B
    bad, ratios, triv_fail, n_cells = [], [], [], 0
    for k in ckeys(S, "M1", F13):
        g = S[k]["gamma"]
        if g < 3 * 0.99:
            continue
        k3 = k[:4] + ("M3",)
        if k3 not in S:
            continue
        n_cells += 1
        e1, e3 = S[k]["med_ex"], S[k3]["med_ex"]
        r = e1 / e3 if e3 > 0 else math.inf
        ratios.append(r)
        m3_trivial = S[k3]["med_w"] >= 2 - 1e-9
        if r < 5 and not m3_trivial:
            bad.append(f"{k[0]}/{k[1]}/env {k[2]}/n {k[3]}: ratio {r:.2f}")
        if k[3] == 1000 and g >= 10 * 0.99 and S[k]["trivial"] < 1:
            triv_fail.append(f"{k[0]}/{k[1]}/env {k[2]}: M1 trivial in {S[k]['trivial']:.2f}")
    fin = [r for r in ratios if math.isfinite(r)]
    out = "refuted" if bad or triv_fail else "holds"
    H.append(("H-B", "for Gamma >= 3, every n, F1-F3: median excess M1 >= 5 x M3 (unless M3 trivial), and M1 trivial at n = 10^3 for Gamma >= 10",
              out, f"{n_cells} cells; ratio min {_mn(fin):.2f}, median {np.median(fin) if fin else math.nan:.2f}; {len(bad)} cells with ratio < 5 and M3 not trivial"
              + (f" (e.g. {'; '.join(bad[:3])})" if bad else "") + f"; M1 not always trivial at n=10^3, Gamma>=10: {len(triv_fail)} cells"
              + (f" (e.g. {'; '.join(triv_fail[:2])})" if triv_fail else "")))
    # H-C
    over, worst_rate, nc = [], 0.0, 0
    for m in ("M3", "M4"):
        for k in ckeys(S, m):
            nc += 1
            reps = S[k]["reps"]
            thr = DELTA / 2 + 3 * math.sqrt(DELTA / 2 * (1 - DELTA / 2) / reps)
            for side in ("miss_hi", "miss_lo"):
                worst_rate = max(worst_rate, S[k][side])
                if S[k][side] > thr + 1e-12:
                    over.append(f"{'/'.join(map(str, k))} {side} {S[k][side]:.3f} > {thr:.3f}")
    H.append(("H-C", "miss rate of each certified end of M3, M4 <= delta/2 + 3 sqrt(delta/2 (1 - delta/2)/reps) in every cell",
              "refuted" if over else "holds", f"{nc} cells (F1-F4); largest miss rate {worst_rate:.3f}; threshold {DELTA / 2 + 3 * math.sqrt(DELTA / 2 * (1 - DELTA / 2) / 100):.3f} at 100 reps, "
              f"{DELTA / 2 + 3 * math.sqrt(DELTA / 2 * (1 - DELTA / 2) / 30):.3f} at 30" + (f"; over: {'; '.join(over[:4])}" if over else "")))
    # H-D
    d = sens.get("d", [])
    if d:
        nstar, info = hd_nstar(d)
        H.append(("H-D", "F1 (nnn_corr), least n with median excess of M3 < 0.05 grows like Gamma^gamma, 0.7 <= gamma <= 1.3",
                  info["outcome"], info["text"]))
    else:
        H.append(("H-D", "…", "not decided", "sweep not run"))
    # H-E
    viol, ncell = [], 0
    for k in ckeys(S, "M3"):
        if S[k]["trivial"] >= 0.5:
            continue
        k5, k6 = k[:4] + ("M5",), k[:4] + ("M6",)
        if k5 not in S or k6 not in S:
            continue
        ncell += 1
        e3, e5, e6 = S[k]["med_ex"], S[k5]["med_ex"], S[k6]["med_ex"]
        if not (e3 <= e6 + 1e-12 and e6 <= e5 + 1e-12):
            viol.append(f"{k[0]}/{k[1]}/env {k[2]}/n {k[3]}: M3 {e3:.4f}, M6 {e6:.4f}, M5 {e5:.4f}")
    H.append(("H-E", "where M3 is not trivial: median excess M3 <= M6 <= M5", "refuted" if viol else "holds",
              f"{ncell} cells; {len(viol)} violations" + (f" (e.g. {'; '.join(viol[:3])})" if viol else "")))
    # H-F
    c1 = [(k, max(S[k]["miss_hi"], S[k]["miss_lo"]), 1 - S[k]["cov_I"]) for k in ckeys(S, "B1", F13) if k[3] == 1000 and S[k]["gamma"] >= 10 * 0.99]
    hit = [c for c in c1 if c[2] > 0.05]
    best = max(c1, key=lambda c: c[2]) if c1 else None
    t1 = "holds" if hit else ("refuted" if c1 else "not decided")
    H.append(("H-F(i)", "B1's nominal 95 % interval misses an end of I in > 5 % of repetitions in >= 1 cell at n = 10^3, Gamma >= 10",
              t1, f"{len(c1)} cells run; {len(hit)} with miss rate > 0.05" + (f"; largest {best[2]:.3f} ({best[0][0]}/{best[0][1]}/env {best[0][2]})" if best else "")))
    c2 = [(k, S[k]["inside_I"]) for k in ckeys(S, "B2", F13)]
    low = [c for c in c2 if c[1] < 0.95]
    H.append(("H-F(ii)", "B2's number lies inside I in >= 95 % of repetitions (consistent data), every cell F1-F3",
              "refuted" if low else "holds", f"{len(c2)} cells; min rate {_mn([c[1] for c in c2]):.3f}; {len(low)} cells below 0.95"
              + (f" (e.g. {', '.join(f'{c[0][0]}/{c[0][1]}/env {c[0][2]}/n {c[0][3]}: {c[1]:.2f}' for c in low[:3])})" if low else "")))
    c3 = [(k, S[k]["med_w"] / S[k]["I_w"] if S[k]["I_w"] > 0 else math.inf) for k in ckeys(S, "B3", F13) if S[k]["gamma"] <= 10 * 1.01]
    low3 = [c for c in c3 if c[1] < 2]
    H.append(("H-F(iii)", "B3's interval on the pool at least twice as wide as I (median width) for Gamma <= 10 on F1-F3",
              "refuted" if low3 else "holds", f"{len(c3)} cells; min ratio {_mn([c[1] for c in c3]):.2f}; {len(low3)} cells below 2"
              + (f" (e.g. {', '.join(f'{c[0][0]}/{c[0][1]}/env {c[0][2]}/n {c[0][3]}: {c[1]:.2f}' for c in low3[:3])})" if low3 else "")))
    # H-G
    r5, bad5, bad4, n4 = [], [], [], 0
    for key, c in ctxs.items():
        fam, tgt, env = key.split("|")
        Iw = c["m0"]["hi"] - c["m0"]["lo"]
        w5 = c["b5"]["hi"] - c["b5"]["lo"]
        w4 = c["b4"]["hi"] - c["b4"]["lo"]
        if fam in F13:
            n4 += 1
            if not w4 > w5 + 1e-12:
                bad4.append(f"{key}: B4 {w4:.3f} vs B5 {w5:.3f}")
            if c["gamma"] >= 3 * 0.99:
                rr = w5 / Iw if Iw > 0 else math.inf
                r5.append(rr)
                if rr < 1.5:
                    bad5.append(f"{key}: {rr:.2f}")
    H.append(("H-G", "B5 width >= 1.5 |I| on F1-F3 for Gamma >= 3; B4 wider than B5 in every cell",
              "refuted" if bad5 or bad4 else "holds", f"B5/|I|: min {_mn(r5):.2f} over {len(r5)} cells, {len(bad5)} below 1.5"
              + (f" ({'; '.join(bad5[:3])})" if bad5 else "") + f"; B4 not wider than B5 in {len(bad4)} of {n4} cells"
              + (f" ({'; '.join(bad4[:3])})" if bad4 else "")))
    # H-H
    c = sens.get("c", [])
    if c:
        det = defaultdict(list)
        for r in c:
            det[(r["family"], r["env"], r["disp"])].append(r["inc"] == "certified")
        dets = {k: float(np.mean(v)) for k, v in det.items()}
        lowd = [(k, v) for k, v in dets.items() if k[2] >= 0.2 and v < 0.9]
        fa = [(k, v) for k, v in dets.items() if k[2] == 0 and v > 0.05]
        H.append(("H-H", "displacement >= 0.2, Gamma <= 3, n = 10^4: detection >= 90 %; consistent data: false alarms <= 5 %",
                  "refuted" if lowd or fa else "holds",
                  f"min detection at displacement >= 0.2: {min(v for k, v in dets.items() if k[2] >= 0.2):.2f}; max false-alarm rate {max(v for k, v in dets.items() if k[2] == 0):.2f}"
                  + (f"; low detection: {', '.join(f'{k[0]}/rho {k[1]}/d {k[2]}: {v:.2f}' for k, v in lowd[:4])}" if lowd else "")))
    else:
        H.append(("H-H", "…", "not decided", "not run"))
    # H-I
    a = sens.get("a", [])
    if a:
        cells = defaultdict(list)
        for r in a:
            cells[(r["family"], r["target"], r["env"])].append(not (r["lo"] <= r["true"] + TOL and r["hi"] >= r["true"] - TOL))
        rates = {k: float(np.mean(v)) for k, v in cells.items()}
        mx = max(rates.items(), key=lambda kv: kv[1])
        H.append(("H-I", "true half-width 2 rho, declared rho: M3 misses the true value in > 10 % of repetitions in >= 1 cell",
                  "holds" if mx[1] > 0.10 else "refuted",
                  f"largest miss rate {mx[1]:.2f} ({mx[0][0]}/{mx[0][1]}/rho {mx[0][2]}); cells above 0.10: {sum(v > 0.10 for v in rates.values())} of {len(rates)}"))
    else:
        H.append(("H-I", "…", "not decided", "not run"))
    # H-J
    if struct:
        f5 = struct["F5"]
        diffs = [r["diff"] for r in f5["rows"] if "diff" in r]
        t200 = max(r["t"] for r in f5["big"] if r["nsite"] == 200)
        hull_bad = [h for h in f5["hull"] if h["nsite"] >= 20 and h["gap_to_range"] > 1e-3]
        ok = max(diffs) <= 1e-6 and t200 < 10 and not hull_bad
        H.append(("H-J", "F5: Cor. 9.3 = programme at 8, 12 sites to 1e-6; 200 sites in < 10 s; box hull within 1e-3 of the range from 20 sites (slope 0.5)",
                  "holds" if ok else "refuted", f"max |Cor. 9.3 - programme| {max(diffs):.2e} over {len(diffs)} cases; largest time at 200 sites {t200:.2f} s; "
                  f"hull gap at 20 sites {[h['gap_to_range'] for h in f5['hull'] if h['nsite'] == 20][0]:.2e}, cells >= 20 sites above 1e-3: {len(hull_bad)}"))
        f4 = struct["F4"]["rows"]
        tmax = max(r["t_counts"] + r["t_lp"] for r in f4)
        cov = []
        for k in ckeys(S, "M3", ("F4",)):
            if k[3] == 100000 and S[k]["gamma"] <= 3 * 1.01:
                cov.append((k[2], S[k]["cov_I"], S[k]["med_ex"]))
        ok = tmax < 60 and all(c[1] >= 1 - DELTA and c[2] < 0.05 for c in cov) and cov
        H.append(("H-K", "F4: exact interval by level counts < 60 s; M3 at n = 10^5 covers I with median excess < 0.05 for Gamma <= 3",
                  "holds" if ok else "refuted", f"exact: largest time {tmax:.2f} s; M3 at n=10^5: " + "; ".join(f"rho {c[0]}: coverage {c[1]:.2f}, median excess {c[2]:.4f}" for c in cov)))
    return H


def hd_nstar(d):
    by = defaultdict(lambda: defaultdict(list))
    gam = {}
    for r in d:
        by[r["env"]][r["n"]].append(r["excess"])
        gam[r["env"]] = r["gamma"]
    pts, lines = [], []
    for env in sorted(by):
        ns = sorted(by[env])
        med = [float(np.median(by[env][n])) for n in ns]
        hit = [i for i, m in enumerate(med) if m < 0.05]
        if hit:
            i = hit[0]
            if i == 0:
                ni = ns[0]
                cens = "<="
            else:      # log-linear interpolation between the last grid point above and the first below the target
                n0, n1, m0, m1 = ns[i - 1], ns[i], med[i - 1], med[i]
                t = (math.log(m0) - math.log(0.05)) / (math.log(m0) - math.log(m1)) if m1 > 0 else 1.0
                ni = math.exp(math.log(n0) + t * (math.log(n1) - math.log(n0)))
                cens = ""
            pts.append((gam[env], ni, ns[i]))
            lines.append(f"Gamma {gam[env]:.1f}: n* {cens}{ni:.0f} (grid {ns[i]}; median excess {med[i]:.4f})")
        else:
            lines.append(f"Gamma {gam[env]:.1f}: not reached by n = {ns[-1]} (median excess {med[-1]:.4f})")
    if len(pts) < len(by):
        out = "not decided"
    else:
        out = None
    if len(pts) >= 2:
        x = np.log([p[0] for p in pts])
        y = np.log([p[1] for p in pts])
        g = float(np.polyfit(x, y, 1)[0])
        yg = np.log([p[2] for p in pts])
        gg = float(np.polyfit(x, yg, 1)[0])
        lines.append(f"fitted gamma {g:.2f} (interpolated n*), {gg:.2f} (grid n*), over {len(pts)} envelopes")
        if out is None:
            out = "holds" if 0.7 <= g <= 1.3 else "refuted"
    else:
        out = "not decided"
    return pts, dict(outcome=out, text="; ".join(lines))


# ------------------------------------------------------------------------------------------------ result tables
def main_tables(S):
    blocks = {}
    hdr = ["fam", "target", "env", "Γ", "n", "method", "reps", "cov I", "cov true", "med w", "p90 w", "med ex", "p90 ex",
           "med ex+", "p90 ex+", "med ex−", "p90 ex−", "triv", "miss+", "miss−", "incons"]
    for fam in ("F1", "F2", "F3", "F4"):
        rows = []
        for k in ckeys(S, None, (fam,)):
            if k[4] == "B2":
                continue
            s = S[k]
            rows.append([k[0], k[1], str(k[2]), s["gamma"], k[3], k[4], s["reps"], s["cov_I"], s["cov_true"], s["med_w"], s["p90_w"],
                         s["med_ex"], s["p90_ex"], s["med_ex_hi"], s["p90_ex_hi"], s["med_ex_lo"], s["p90_ex_lo"], s["trivial"],
                         s["miss_hi"], s["miss_lo"], s["inconsistent"]])
        blocks[f"grid_{fam}"] = table(hdr, rows)
    # compact summary: median excess per method
    ms = ["M1", "M2", "M3", "M4", "M5", "M6", "B1", "B3"]
    rows = []
    seen = sorted({k[:4] for k in S}, key=lambda k: (k[0], k[1], env_key(k[2]), k[3]))
    for c in seen:
        s3 = S.get(c + ("M3",))
        rows.append([c[0], c[1], str(c[2]), s3["gamma"] if s3 else math.nan, c[3], s3["V_lo"], s3["V_hi"]] +
                    [S[c + (m,)]["med_ex"] if c + (m,) in S else math.nan for m in ms])
    blocks["excess_summary"] = table(["fam", "target", "env", "Γ", "n", "V−", "V+"] + [f"{m} med ex" for m in ms], rows)
    # B2
    rows = []
    for k in ckeys(S, "B2"):
        s = S[k]
        rows.append([k[0], k[1], str(k[2]), s["gamma"], k[3], s["reps"], s["V_lo"], s["V_hi"], s["true"], s["med_value"], s["inside_I"], s["fail"], s["med_kish"]])
    blocks["b2"] = table(["fam", "target", "env", "Γ", "n", "reps", "V−", "V+", "true", "med B2", "B2 in I", "fail", "med Kish ESS"], rows)
    # timings
    rows = []
    for k in ckeys(S):
        if k[2] not in ("1.15",) or k[1] not in ("nnn_corr", "pair_pop", "stress", "ones_first20"):
            continue
        s = S[k]
        rows.append([k[0], k[1], k[3], k[4], s.get("t_pre", math.nan), s.get("t_samp", math.nan), s.get("t_opt", math.nan),
                     s.get("t_cert", math.nan), s.get("t_total", math.nan)])
    blocks["timings"] = table(["fam", "target", "n", "method", "preproc s", "sampling s", "optim s", "certif s", "M3 total s"], rows)
    return blocks


def exact_tables(ctxs):
    rows = []
    for key in sorted(ctxs, key=lambda k: (k.split("|")[0], k.split("|")[1], env_key(k.split("|")[2]))):
        c = ctxs[key]
        fam, tgt, env = key.split("|")
        m0 = c["m0"]
        pr = m0.get("primal")
        dprim = max(abs(pr[0] - m0["lo"]), abs(pr[1] - m0["hi"])) if pr else math.nan
        chk = m0["extremal_check"]
        gap = max(abs(chk["hi"]["primal_value"] - m0["hi"]), abs(chk["lo"]["primal_value"] - m0["lo"]))
        rows.append([fam, tgt, env, c["gamma"], m0["lo"], m0["hi"], c["true"], m0["n_cells"], m0["t"], dprim, gap,
                     chk["hi"]["in_region"] and chk["lo"]["in_region"], c["b5"]["lo"], c["b5"]["hi"], c["b4"]["lo"], c["b4"]["hi"]])
    return table(["fam", "target", "env", "Γ", "V− (M0)", "V+ (M0)", "true", "cells", "M0 s", "|M0 − primal|", "extremal gap", "extremal in R",
                  "B5 lo", "B5 hi", "B4 lo", "B4 hi"], rows)


def sens_tables(sens):
    blocks = {}
    a = sens.get("a", [])
    if a:
        cells = defaultdict(list)
        for r in a:
            cells[(r["family"], r["target"], r["env"])].append(r)
        rows = []
        for k in sorted(cells):
            rs = cells[k]
            miss = np.mean([not (r["lo"] <= r["true"] + TOL and r["hi"] >= r["true"] - TOL) for r in rs])
            covI = np.mean([r["lo"] <= r["V_lo"] + TOL and r["hi"] >= r["V_hi"] - TOL for r in rs]) if not rs[0]["I_empty"] else math.nan
            rows.append([k[0], k[1], k[2], rs[0]["gamma"], len(rs), rs[0]["true"], rs[0]["V_lo"], rs[0]["V_hi"], rs[0]["I_empty"], miss, covI,
                         np.mean([r["inc"] == "certified" for r in rs]), np.mean([r["st_lo"] == r["st_hi"] == "certified" and r["lo"] > r["hi"] for r in rs])])
        blocks["sens_a"] = table(["fam", "target", "declared ρ", "Γ", "reps", "true value", "V− (declared class)", "V+", "I empty", "M3 misses true",
                                  "M3 covers I", "incons. fires", "ends cross"], rows)
    b = sens.get("b", [])
    if b:
        cells = defaultdict(list)
        for r in b:
            cells[(r["variant"], r["env"])].append(r)
        rows = []
        for k in sorted(cells, key=lambda k: (k[1], ["full", "one", "none", "uninformative"].index(k[0]))):
            rs = cells[k]
            lo, hi = np.array([r["lo"] for r in rs]), np.array([r["hi"] for r in rs])
            Vl, Vh = rs[0]["V_lo"], rs[0]["V_hi"]
            rows.append([k[0], k[1], rs[0]["gamma"], len(rs), Vl, Vh, Vh - Vl, np.median(hi - lo), np.median((hi - Vh) + (Vl - lo)),
                         np.mean((lo <= Vl + TOL) & (hi >= Vh - TOL))])
        blocks["sens_b"] = table(["observation", "ρ", "Γ", "reps", "V−", "V+", "|I|", "M3 med width", "M3 med excess", "M3 covers I"], rows)
    c = sens.get("c", [])
    if c:
        ex = {(r["family"], r["env"], r["disp"]): r for r in sens.get("c_exact", [])}
        cells = defaultdict(list)
        for r in c:
            cells[(r["family"], r["env"], r["disp"])].append(r)
        rows = []
        for k in sorted(cells):
            rs = cells[k]
            e = ex.get(k, {})
            rows.append([k[0], k[1], rs[0]["gamma"], k[2], len(rs), e.get("inconsistent", math.nan), e.get("exact_phi", math.nan),
                         np.mean([r["inc"] == "certified" for r in rs]), np.median([r["t"] for r in rs])])
        blocks["sens_c"] = table(["fam", "ρ", "Γ", "displacement", "reps", "exactly inconsistent", "exact Φ", "certificate fires", "med s"], rows)
    d = sens.get("d", [])
    if d:
        by = defaultdict(list)
        for r in d:
            by[(r["env"], r["n"])].append(r)
        rows = []
        for k in sorted(by):
            rs = by[k]
            exs = np.array([r["excess"] for r in rs])
            rows.append([k[0], rs[0]["gamma"], k[1], len(rs), np.median(exs), np.quantile(exs, 0.9),
                         np.mean([r["lo"] <= r["V_lo"] + TOL and r["hi"] >= r["V_hi"] - TOL for r in rs]), np.median([r["t"] for r in rs])])
        blocks["sens_d"] = table(["ρ", "Γ", "n", "reps", "M3 med excess", "p90 excess", "covers I", "med s"], rows)
    return blocks


def struct_tables(st):
    blocks = {}
    f4 = st["F4"]
    blocks["f4"] = table(["ρ", "Γ", "cells", "Σ prob", "level counts s", "V− (LP)", "V+ (LP)", "LP s", "V− (descent)", "V+ (descent)", "descent s", "true"],
                         [[r["rho"], r["gamma"], r["n_cells"], r["prob_sum"], r["t_counts"], r["lo"], r["hi"], r["t_lp"], r["lo_descent"],
                           r["hi_descent"], r["t_descent"], r["true"]] for r in f4["rows"]]) + \
        f"\n\nLevel counts against enumeration (12 sites): max difference {fmt(f4['small_check_maxdiff'])}."
    f5 = st["F5"]
    blocks["f5_small"] = table(["sites", "slope", "target", "data", "programme lo", "programme hi", "programme s", "Cor. 9.3 lo", "Cor. 9.3 hi", "Cor. 9.3 s", "|diff|"],
                               [[r["nsite"], r["slope"], r["target"], r["data"], r["lp_lo"], r["lp_hi"], r["t_lp"], r.get("add_lo", math.nan),
                                 r.get("add_hi", math.nan), r.get("t_add", math.nan), r.get("diff", math.nan)] for r in f5["rows"]])
    blocks["f5_big"] = table(["sites", "slope", "target", "lo", "hi", "s", "true", "covers true"],
                             [[r["nsite"], r["slope"], r["target"], r["lo"], r["hi"], r["t"], r["true"], r["covers_true"]] for r in f5["big"]])
    blocks["f5_hull"] = table(["sites", "hull lo", "hull hi", "gap to [−1,1]", "class lo (closed form)", "class hi", "Cor. 9.3 lo", "Cor. 9.3 hi"],
                              [[h["nsite"], h["hull_lo"], h["hull_hi"], h["gap_to_range"], h["class_lo"], h["class_hi"], h["add_lo"], h["add_hi"]] for h in f5["hull"]]) + \
        f"\n\nFull-cube check of the hull at 8 sites (256 states): [{fmt(f5['hull_full_check'][0], 6)}, {fmt(f5['hull_full_check'][1], 6)}]."
    blocks["f6"] = table(["control", "lo (l = 0)", "hi", "stored", "primal programme", "|diff|", "s"],
                         [[r["id"], r["lo"], r["hi"], f"[{r['expected_str'][0]}, {r['expected_str'][1]}]",
                           f"[{fmt(r['primal'][0], 6)}, {fmt(r['primal'][1], 6)}]" if r["primal"] else "–", r["diff"], r["t"]] for r in st["F6"]])
    return blocks


def misc_tables(S, raw):
    blocks = {}
    mem = load_jsonl(RES / "memory.jsonl")
    if mem:
        blocks["memory"] = table(["method", "cell", "baseline RSS MiB", "peak RSS MiB", "increase MiB", "wall s"],
                                 [[m["method"], m["cell"], m["base_rss_kib"] / 1024, m["peak_rss_kib"] / 1024,
                                   (m["peak_rss_kib"] - m["base_rss_kib"]) / 1024, m["wall"]] for m in mem])
    chk = [r["s3_check"] for r in raw if "s3_check" in r]
    blocks["s3check"] = f"Lumped S3 against `ci.s3_interval` on the raw draws: {len(chk)} comparisons, max |difference| {fmt(max(chk) if chk else math.nan)}."
    walls = {}
    for p in RES.glob("*_wall.json"):
        walls[p.stem] = json.loads(p.read_text())["wall"]
    grid_wall, grid_cpu = 0.0, 0.0
    for p in sorted(RES.glob("validation_log_part*.txt")):
        el = re.findall(r"\] \S+ ([0-9.]+)s  \(elapsed ([0-9]+)s\)", p.read_text())
        if el:
            grid_wall += float(el[-1][1])
            grid_cpu += sum(float(a) for a, _ in el)
    rows = [["grid (run_validation.py)", grid_wall, grid_cpu]] + [[k, v, math.nan] for k, v in sorted(walls.items())]
    tot = grid_wall + sum(walls.values())
    blocks["compute"] = table(["run", "wall s", "worker CPU s (sum of chunk times)"], rows) + \
        f"\n\nTotal wall of the recorded runs: {tot:.0f} s ({tot / 3600:.2f} h).  Grid rows: {len(raw)}."
    return blocks


PROVENANCE = [   # (result files, producing run, start of the producing process, UTC; boundary = library change at 02:35:33 UTC 28 Nov)
    ("results/validation/*.jsonl except F3_B3_recomputed.jsonl", "run_validation.py grid (two invocations; the second resumed)", "2026-11-28 00:55:39 and 01:08:26"),
    ("results/sens_c.jsonl, sens_c_exact.json", "run_sensitivity.py c", "2026-11-28 02:34:28"),
    ("results/sens_a.jsonl, sens_b.jsonl, sens_d.jsonl", "run_sensitivity.py a, b, d", "after 02:47 (see results/run_starts.txt)"),
    ("results/contexts.json, structure.json, memory.jsonl", "run_validation.py --contexts / --memory, run_structure.py", "after the sensitivity runs (see results/run_starts.txt)"),
    ("results/validation/F3_B3_recomputed.jsonl", "rerun_b3_f3.py", "after the above"),
    ("results/superseded/B3_F3_pre_fix.jsonl", "the grid's B3 rows on F3, moved there by rerun_b3_f3.py", "2026-11-28 00:55-02:34"),
]


def provenance_block():
    def when(t):
        m = re.findall(r"(\d{2}):(\d{2}):(\d{2})", t)
        if not m:
            return "after"
        h, mi, se = map(int, m[-1])
        return "before" if (h, mi, se) < (2, 35, 33) else "after"
    return table(["result files", "produced by", "process start (UTC)", "relative to the library change"],
                 [[a, b, c, when(c)] for a, b, c in PROVENANCE])


def b3_rerun_block():
    old = load_jsonl(RES / "superseded" / "B3_F3_pre_fix.jsonl")
    new = load_jsonl(RES / "validation" / "F3_B3_recomputed.jsonl")
    if not old or not new:
        return "not run"
    idx = {(r["target"], r["env"], r["rep"]): r for r in new}
    cells = defaultdict(list)
    for r in old:
        q = idx.get((r["target"], r["env"], r["rep"]))
        if q:
            cells[(r["target"], r["env"])].append((r, q))
    rows = []
    for k in sorted(cells, key=lambda k: (k[0], env_key(k[1]))):
        pr = cells[k]
        Iw = pr[0][0]["V_hi"] - pr[0][0]["V_lo"]
        wo = np.array([a["hi"] - a["lo"] for a, _ in pr])
        wn = np.array([b["hi"] - b["lo"] for _, b in pr])
        d = np.array([max(abs(a["hi"] - b["hi"]), abs(a["lo"] - b["lo"])) for a, b in pr])
        rows.append([k[0], k[1], len(pr), Iw, np.median(wo), np.median(wn), np.median(wo) / Iw, np.median(wn) / Iw,
                     np.median(wo - wn), float(d.max()), np.mean(wn > wo + 1e-9)])
    below_old = sum(r[6] < 2 for r in rows)
    below_new = sum(r[7] < 2 for r in rows)
    note = (f"\n\nH-F(iii) on the F3 cells: median width below 2|I| in {below_old} of {len(rows)} cells with the superseded values, "
            f"{below_new} of {len(rows)} with the recomputed values (the hypothesis table uses the recomputed values; "
            "the F1, F2 cells are unaffected).")
    return note.strip() + "\n\n" + table(["target", "env", "reps", "|I|", "med width pre-fix (superseded)", "med width recomputed", "ratio pre-fix", "ratio recomputed",
                  "med width change", "max end change", "fraction recomputed wider"], rows)


def gather():
    S, raw = grid()
    ctxs = json.loads((RES / "contexts.json").read_text()) if (RES / "contexts.json").exists() else {}
    struct = json.loads((RES / "structure.json").read_text()) if (RES / "structure.json").exists() else None
    sens = {}
    for w in "abcd":
        p = RES / f"sens_{w}.jsonl"
        if p.exists():
            sens[w] = load_jsonl(p)
    if (RES / "sens_c_exact.json").exists():
        sens["c_exact"] = json.loads((RES / "sens_c_exact.json").read_text())
    blocks = {}
    H = hypotheses(S, ctxs, struct, sens)
    blocks["hypotheses"] = table(["hypothesis", "criterion (as read)", "outcome", "the numbers"], [list(h) for h in H])
    blocks.update(main_tables(S))
    if ctxs:
        blocks["exact"] = exact_tables(ctxs)
    blocks.update(sens_tables(sens))
    if struct:
        blocks.update(struct_tables(struct))
    blocks.update(misc_tables(S, raw))
    blocks["b3_rerun"] = b3_rerun_block()
    blocks["provenance"] = provenance_block()
    return blocks


def fill(text, blocks):
    for k, v in blocks.items():
        pat = re.compile(rf"(<!-- GEN:{k} -->\n).*?(<!-- /GEN:{k} -->)", re.S)
        if pat.search(text):
            text = pat.sub(lambda m: m.group(1) + v + "\n" + m.group(2), text)
    return text


def main():
    """--print: the blocks; --report: the whole report on stdout; --write: (re)write REPORT.md from the template in
    report_template.py (or refresh the blocks of an existing REPORT.md)."""
    blocks = gather()
    if "--print" in sys.argv:
        for k, v in blocks.items():
            print(f"### {k}\n{v}\n")
        return
    from report_template import TEMPLATE
    rp = HERE / "REPORT.md"
    text = fill(rp.read_text() if rp.exists() and "--fresh" not in sys.argv else TEMPLATE, blocks)
    if "--write" in sys.argv:
        rp.write_text(text)
    else:
        print(text)
    missing = [k for k in blocks if f"<!-- GEN:{k} -->" not in text]
    if missing:
        print("blocks without a place in the report:", missing, file=sys.stderr)


if __name__ == "__main__":
    main()
