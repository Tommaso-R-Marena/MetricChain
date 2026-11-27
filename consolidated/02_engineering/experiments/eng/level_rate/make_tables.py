"""Tables of the independent check of Theorem R, generated from results/*.json (nothing is typed by hand).

    python experiments/eng/level_rate/make_tables.py            # prints the tables, writes results/summary.json
    python experiments/eng/level_rate/make_tables.py --verify   # also re-computes a sample of the entries

Notation: C = 2 pi^2 h^2 vartheta is the limit of k^2 (tau_k - h) claimed by Theorem R;
r_k = k^2 (x_k - h)/C for a sequence x_k:
  LB   x_k = B_inf(k), the proved lower bound of tau_k from the line dynamics (double precision evaluation);
  UB   x_k = M_k(0), the upper bound of tau_k from convex majorants (floating point with a margin);
  GEN  x_k = tau_k from the recursion on a grid without structural assumptions (an approximation).
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lr_cases as C  # noqa: E402
import lr_recursion as R  # noqa: E402

KS = [2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 60, 80, 100, 120, 160]


def _load(name):
    try:
        return C.load(name)
    except FileNotFoundError:
        return None


def case_summary(case: str) -> dict | None:
    lines = _load(f"lines_{case}.json")
    if lines is None:
        return None
    # the finest upper-bound run available, and the next coarser one (for the resolution check)
    avail = [n for n in (16000, 8000, 4000) if (C.RES / f"upper_{case}_N{n}.json").exists()]
    n_hi = avail[0] if avail else 0
    n_lo = avail[1] if len(avail) > 1 else 0
    cst = lines["constants"]
    h = float(cst["h"])
    const = float(cst["constant"]) if cst.get("constant") not in (None, "+inf", "inf") else None
    out = dict(case=case, name=lines["name"], constants=cst, rows={}, large_k={})
    if const:
        out["constant_over_a"] = const / float(cst["a"])
    up_hi = _load(f"upper_{case}_N{n_hi}.json") if n_hi else None
    up_lo = _load(f"upper_{case}_N{n_lo}.json") if n_lo else None
    out["N_upper"], out["N_upper_coarse"] = n_hi, n_lo
    gens = {n: _load(f"general_{case}_N{n}.json") for n in (1000, 2000)}
    theirs = C.THEIRS.get(case, {})
    for k in KS:
        row = {}
        ln = lines["lines"].get(str(k))
        if ln:
            row["LB"] = float(ln["B"])
        for tag, up in (("UB", up_hi), ("UB_lo", up_lo)):
            if up and str(k) in up["tau_upper"]:
                row[tag] = float(up["tau_upper"][str(k)])
        for n, gen in gens.items():
            if gen and str(k) in gen["tau"]:
                row[f"GEN{n}"] = float(gen["tau"][str(k)])
        for tag in ("LB", "UB", "UB_lo", "GEN1000", "GEN2000"):
            if tag in row:
                row["k2_" + tag] = k * k * (row[tag] - h)
                if const:
                    row["r_" + tag] = k * k * (row[tag] - h) / const
        if "UB" in row and "UB_lo" in row:
            row["UB_resolution_diff"] = row["UB_lo"] - row["UB"]
            row["UB_resolution_diff_rel"] = (row["UB_lo"] - row["UB"]) / (row["UB"] - h)
            # extrapolation in the grid size assuming an error proportional to 1/N^2 (an approximation, not a bound)
            row["UBx"] = row["UB"] - (row["UB_lo"] - row["UB"]) / ((n_hi / n_lo) ** 2 - 1)
            row["k2_UBx"] = k * k * (row["UBx"] - h)
            if const:
                row["r_UBx"] = k * k * (row["UBx"] - h) / const
        for key, tag in (("lines_lb", "theirs_LB"), ("grid_recursion", "theirs_grid")):
            if k in theirs.get(key, {}):
                row[tag] = theirs[key][k]
                if const:
                    row["r_" + tag] = k * k * (theirs[key][k] - h) / const
        if row:
            out["rows"][str(k)] = row
    for k, ln in lines["lines"].items():
        if int(k) > 160:
            out["large_k"][k] = dict(LB=float(ln["B"]), k2_LB=ln["k2_excess"], r_LB=ln.get("ratio"))
    if const:
        fits = {}
        for tag in ("LB", "UB", "UB_lo", "UBx"):
            for ks in ((20, 40, 80), (40, 80, 160)):
                try:
                    rs = [out["rows"][str(k)]["r_" + tag] for k in ks]
                except KeyError:
                    continue
                r_inf, alpha, beta = R.richardson_limit(ks, rs)
                fits[f"{tag}_{ks[0]}_{ks[1]}_{ks[2]}"] = dict(r_inf=r_inf, alpha=alpha, beta=beta)
        lk = sorted(int(k) for k in out["large_k"])
        if len(lk) >= 3:
            ks = lk[-3:]
            rs = [out["large_k"][str(k)]["r_LB"] for k in ks]
            r_inf, alpha, beta = R.richardson_limit(ks, rs)
            fits[f"LB_{ks[0]}_{ks[1]}_{ks[2]}"] = dict(r_inf=r_inf, alpha=alpha, beta=beta)
        out["richardson"] = fits
        for tag in ("UB", "LB"):
            row = out["rows"].get("160", {})
            if "r_" + tag in row:
                out[f"shift_c_{tag}_at_160"] = 160 * (1 / math.sqrt(row["r_" + tag]) - 1)   # x_k ~ h + C/(k + c)^2
    # local exponents d ln(x_k - h)/d ln k between consecutive doublings (Theorem R: -2)
    expo = {}
    for tag in ("LB", "UB"):
        for k1, k2 in ((20, 40), (40, 80), (80, 160)):
            r1, r2 = out["rows"].get(str(k1), {}), out["rows"].get(str(k2), {})
            if tag in r1 and tag in r2:
                expo[f"{tag}_{k1}_{k2}"] = math.log((r2[tag] - h) / (r1[tag] - h)) / math.log(k2 / k1)
    for k1, k2 in ((320, 640), (640, 1280), (1280, 2560), (2560, 5120)):
        if str(k1) in out["large_k"] and str(k2) in out["large_k"]:
            expo[f"LB_{k1}_{k2}"] = math.log((out["large_k"][str(k2)]["LB"] - h) / (out["large_k"][str(k1)]["LB"] - h)) / math.log(k2 / k1)
    out["local_exponents"] = expo
    if up_hi:
        out["upper_run"] = dict(N=up_hi["N"], K=up_hi["K"], n_above_total=up_hi["n_above_total"],
                                seconds=up_hi["seconds"],
                                all_raw_values_convex=all(lv["n_hull"] == up_hi["N"] + 1 for lv in up_hi["levels"]))
    if up_lo:
        out["upper_run_lo"] = dict(N=up_lo["N"], K=up_lo["K"], n_above_total=up_lo["n_above_total"],
                                   seconds=up_lo["seconds"])
    for n, gen in gens.items():
        if gen:
            lv = gen["levels"]
            out[f"general_run_N{n}"] = dict(
                K=gen["K"], seconds=gen["seconds"],
                S_quasiconvex_at_every_level=all(x["S_quasiconvex_in"] for x in lv),
                largest_concave_corner_over_a=max(x["max_concavity_in"] for x in lv) / gen["a"],
                max_fraction_regime2=max(x["frac_regime2_among_improved"] for x in lv),
                blind_search_lowest_vs_balance_over_a=min(x["scan_minus_balance_min"] for x in lv),
                blind_search_largest_miss_over_a=max(x["scan_minus_balance_max"] for x in lv),
                general_minus_upper_min_over_a=(min(x["general_minus_upper_min_over_a"] for x in gen["comparison_with_upper_bound_same_grid"])
                                                if gen["comparison_with_upper_bound_same_grid"] else None),
                general_minus_upper_max_over_a=(max(x["general_minus_upper_max_over_a"] for x in gen["comparison_with_upper_bound_same_grid"])
                                                if gen["comparison_with_upper_bound_same_grid"] else None))
    for key in ("H1_check", "certified_lower_bounds", "mpmath_check", "gauss_exact_1e9", "passage_time_s_t_0.55"):
        if key in lines:
            out[key] = lines[key]
    # the closed form of tau_2 (THEORY_REPORT 11.19 remark (1)) against the upper bound at k = 2
    if const and "UB" in out["rows"].get("2", {}):
        t2 = R.tau2_closed(C.make(case))
        out["tau2_closed_form"] = t2
        out["tau2_upper_minus_closed_over_a"] = (out["rows"]["2"]["UB"] - t2) / float(cst["a"])
        out["tau_over_a_upper"] = {k: out["rows"][k]["UB"] / float(cst["a"]) for k in ("2", "3", "4", "5", "6", "40")
                                   if "UB" in out["rows"].get(k, {})}
        out["tau_over_a_lower"] = {k: out["rows"][k]["LB"] / float(cst["a"]) for k in ("2", "3", "4", "5", "6", "40")
                                   if "LB" in out["rows"].get(k, {})}
    return out


def fmt(v, spec):
    return format(v, spec) if v is not None else "-"


def print_case(s: dict):
    cst = s["constants"]
    print(f"\n=== {s['case']}: {s['name']}")
    line = "  ".join(f"{k}={float(cst[k]):.9g}" for k in ("a", "E", "h", "L", "vartheta", "constant") if k in cst and cst[k] not in ("+inf", "inf"))
    print("   " + line + (f"  constant/a={s['constant_over_a']:.6f}" if "constant_over_a" in s else ""))
    print(f"   upper bounds: N = {s.get('N_upper')} (coarse: {s.get('N_upper_coarse')})")
    print("   k    LB (lines)       UB (convex)      UB_lo-UB   r_LB     r_UB     r_UBx    r_GEN1000 r_GEN2000 | theirs: r_LB  r_grid")
    for k in KS:
        row = s["rows"].get(str(k))
        if not row:
            continue
        print(f"  {k:4d}  {fmt(row.get('LB'), '.12f')}  {fmt(row.get('UB'), '.12f')}  {fmt(row.get('UB_resolution_diff'), '9.1e')}"
              f"  {fmt(row.get('r_LB'), '.5f')}  {fmt(row.get('r_UB'), '.5f')}  {fmt(row.get('r_UBx'), '.5f')}  {fmt(row.get('r_GEN1000'), '.5f')}"
              f"   {fmt(row.get('r_GEN2000'), '.5f')}  | {fmt(row.get('r_theirs_LB'), '.5f')} {fmt(row.get('r_theirs_grid'), '.5f')}")
    if s["large_k"]:
        print("   large k (LB only): " + "  ".join(f"{k}: {v['r_LB']:.6f}" for k, v in sorted(s["large_k"].items(), key=lambda kv: int(kv[0])) if v["r_LB"]))
    for name, f in s.get("richardson", {}).items():
        print(f"   Richardson {name}: r_inf={f['r_inf']:.5f}  alpha={f['alpha']:.3f}")
    for tag in ("UB", "LB"):
        if f"shift_c_{tag}_at_160" in s:
            print(f"   shift c at k=160 ({tag}): {s[f'shift_c_{tag}_at_160']:.4f}")
    if s.get("local_exponents"):
        print("   local exponents: " + "  ".join(f"{k}: {v:.4f}" for k, v in s["local_exponents"].items()))
    if "tau2_closed_form" in s:
        print(f"   tau_2 closed form = {s['tau2_closed_form']:.12f}; (UB_2 - closed form)/a = {s['tau2_upper_minus_closed_over_a']:.2e};"
              f" tau_k/a <= " + ", ".join(f"{k}: {v:.5f}" for k, v in s["tau_over_a_upper"].items()))
    for key in ("upper_run", "upper_run_lo", "general_run_N1000", "general_run_N2000"):
        if key in s:
            print(f"   {key}: {s[key]}")
    if "H1_check" in s:
        hc = s["H1_check"]
        print(f"   (H1): F concave on grid: {hc['F_concave_on_grid']} (max second difference {hc['max_second_difference_of_F']:.4g});"
              f" J from theta_na - F: max |.| = {max(abs(v) for v in hc['J_from_theta_minus_F']):.1e};"
              f" J'' at L by differences {hc['second_difference_of_J_from_theta_at_L']} vs F''(L) = {hc['F2_at_L_mpmath']:.8g};"
              f" vartheta from theta_na {hc['vartheta_from_theta_na']:.7g} vs {hc['vartheta_from_F']:.7g}")
    if "certified_lower_bounds" in s:
        print("   certified (interval arithmetic): " + "  ".join(
            f"tau_{k} >= {v['B_certified']} [{'proved' if v['proved'] else 'NOT proved'}]"
            for k, v in sorted(s["certified_lower_bounds"].items(), key=lambda kv: int(kv[0]))))


def verify(summary: dict) -> None:
    """Re-compute a sample of the entries from scratch (cheap ones) and compare."""
    import lr_lines as LN
    import numpy as np
    for case, s in summary["cases"].items():
        if case in C.NEGATIVE:
            continue
        pair = C.make(case)
        for k in ("3", "20"):
            row = s["rows"].get(k)
            if row and "LB" in row:
                b = float(LN.b_inf(pair, int(k)))
                assert abs(b - row["LB"]) <= 1e-13 * max(1.0, abs(b)), (case, k, b, row["LB"])
        assert abs(float(pair.constants()["constant"]) - float(s["constants"]["constant"])) <= 1e-12 * float(pair.constants()["constant"])
        if "UB" in s["rows"].get("3", {}):
            ub = R.ConvexUpperBound(pair, N=2000, n_theta=50_000)
            ub.run(3)
            # a coarser grid gives a (slightly) larger upper bound
            assert 0 <= ub.M[0] - s["rows"]["3"]["UB"] <= 2e-6 * pair.a, (case, ub.M[0], s["rows"]["3"]["UB"])
        print(f"verified: {case}")
    _ = np


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args(argv)
    import numpy
    import mpmath
    summary = dict(pinned_theory_commit=C.PINNED, cases={},
                   versions=dict(python=sys.version.split()[0], numpy=numpy.__version__, mpmath=mpmath.__version__))
    for group, cases in (("validation", C.VALIDATION), ("new", C.NEW), ("stress", C.STRESS), ("negative", C.NEGATIVE)):
        for case in cases:
            s = case_summary(case)
            if s is None:
                continue
            s["group"] = group
            summary["cases"][case] = s
            print_case(s)
    pu = _load("propU.json")
    if pu:
        summary["propU"] = pu
        print("\n=== Proposition U / Lemma L on random convex slope functions")
        for case, v in pu["pairs"].items():
            print(f"   {case}: {v}")
    for extra in ("negative_controls.json", "fourletter.json", "bb_certificate.json"):
        ex = _load(extra)
        if ex:
            summary[extra[:-5]] = ex
    C.dump("summary.json", summary)
    if args.verify:
        verify(summary)


if __name__ == "__main__":
    main()
