"""P3: tables for the report from out/floor_*.json.   usage: python3 -B mk_tables.py > out/tables.md"""
import json, glob, os, re, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
KT = 0.0019872041 * 300.0
runs = [json.load(open(f)) | {"file": os.path.basename(f)} for f in sorted(glob.glob(os.path.join(HERE, "out", "floor_*.json")))]
for r in runs:
    r["siteres"] = "gamma_sites" in r
    mm = re.fullmatch(r"([A-Z]+)[:c]?(\d+)", r["seq"].replace(":", "c"))
    r["res"], r["nres"] = (mm.group(1), int(mm.group(2))) if mm else (r["seq"], r["n"])


def fmt(v, p=3):
    if v is None:
        return "—"
    if abs(v) >= 1e4 or (abs(v) < 1e-3 and v != 0):
        return f"{v:.1e}"
    return f"{v:.{p}g}"


def key(r):
    return (r["kind"], r["res"], r["bb"], r["tau"], r["nres"], r["m"])


viol = sum(r.get("viol_lower", 0) + r.get("viol_upper", 0) for r in runs)
nst = sum(int(r["size"]) for r in runs if r.get("enum"))
nen = sum(1 for r in runs if r.get("enum"))
inb = sum(1 for r in runs if r.get("enum") and r.get("truth_in_bracket"))
inb2 = sum(1 for r in runs if r.get("enum") and r.get("truth_in_range_bracket"))
nsamp = sum(1 for r in runs if r.get("enum") and "truth_in_bracket" in r)
print(f"runs: {len(runs)}; enumerated runs: {nen} with {nst} state checks in total; violations of m_- <= E <= m_+: {viol}; "
      f"true ln Z inside the Hoeffding bracket in {inb} of {nsamp} runs, inside the sample-range bracket in {inb2} of {nsamp}; "
      f"largest |lnZ(m_-) DP - enumeration| = {max(abs(r['lnZ_lower_model'] - r['lnZ_lower_enum']) for r in runs if r.get('enum')):.1e}\n")
for sr, title in ((False, "Constant remainder bound: m_-/+ = (expansion to order m-1, pairwise form) -/+ Gamma_m"),
                  (True, "Site penalties: m_-/+ = (expansion to order m-1, pairwise form) -/+ sum_i gamma_i [x_i != x0_i]")):
    print(f"### {title}\n")
    print("| instance | \\|X\\| | m | ball (evals; % of X) | Gamma_m kcal/mol (kT) | sum max\\|d_T\\|, order 3; 4 | exact g − I_{m−1}g | rho exact / certified (kT) | cost Z(m_-)/Z(E) − 1 | deterministic bracket (nats) | Hoeffding / range bracket (nats), N | truth inside |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted([r for r in runs if r["siteres"] == sr and r["kind"] == "gbn2"], key=key):
        G = r["Gamma_self"] + r["Gamma_cross"]
        ex = f"[{fmt(r['rem_min'], 2)}, {fmt(r['rem_max'], 2)}]" if r.get("enum") else "—"
        rho = f"{fmt(r['rho_exact'] / KT)} / {fmt(r['rho_cert'] / KT)}" if r.get("enum") else f"— / {fmt(r['rho_cert'] / KT)}"
        cost = fmt(r["cost"]) if r.get("enum") else "—"
        hb = f"{fmt(r['bracket_hi'] - r['bracket_lo'])} / {fmt(r['range_bracket_hi'] - r['range_bracket_lo'])}, {r['N']}" if "bracket_lo" in r else "—"
        tr = ("yes" if r.get("truth_in_bracket") and r.get("truth_in_range_bracket") else "NO") if r.get("enum") and "truth_in_bracket" in r else "—"
        print(f"| {r['seq']}/{r['bb']} τ{r['tau']:.2f} | {fmt(r['size'])} | {r['m']} | {r['nball']}; {100 * r['nball'] / r['size']:.2g} | {fmt(G)} ({fmt(G / KT)}) | "
              f"{fmt(r.get('sum_absd3'))}; {fmt(r.get('sum_absd4'))} | {ex} | {rho} | {cost} | {fmt(r['lnZ_lower_model'] - r['lnZ_upper_model'])} | {hb} | {tr} |")
    print()
print("### One-site oscillations of the remainder g − I_{m−1}g: certified c_i <= 2 m gamma_i against exact (enumeration); sum of squares in (kT)^2\n")
print("| instance | m | max certified c_i (kT) | sum_i c_i^2 certified (kT^2) | max exact c_i (kT) | sum_i c_i^2 exact (kT^2) |")
print("|---|---|---|---|---|---|")
for r in sorted([r for r in runs if r["siteres"] and r["kind"] == "gbn2"], key=key):
    c = 2 * r["m"] * np.array(r["gamma_sites"]) / KT
    e = np.array(r["osc_rem"]) / KT if "osc_rem" in r else None
    print(f"| {r['seq']}/{r['bb']} τ{r['tau']:.2f} | {r['m']} | {fmt(c.max())} | {fmt(float((c ** 2).sum()))} | "
          + (f"{fmt(e.max())} | {fmt(float((e ** 2).sum()))} |" if e is not None else "— | — |"))
