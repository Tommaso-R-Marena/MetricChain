"""
P5 -- tables of the report from out/s1_*.json and out/s2_*.json  ->  out/tables.md
usage: python3 -B mk_tables.py
"""
import os, json, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ["L6_H_0.60", "L8_H_0.60", "L12_H_0.60", "S4_H_0.70", "S5_H_0.70", "S6_H_0.70"]
NAME = {"L6_H_0.60": "Leu₆/H τ0.60", "L8_H_0.60": "Leu₈/H τ0.60", "L12_H_0.60": "Leu₁₂/H τ0.60",
        "S4_H_0.70": "Ser₄/H τ0.70", "S5_H_0.70": "Ser₅/H τ0.70", "S6_H_0.70": "Ser₆/H τ0.70"}


def f(x, d=3):
    if x == 0:
        return "0"
    if abs(x) >= 100:
        return f"{x:.0f}"
    if abs(x) >= 10:
        return f"{x:.1f}"
    if abs(x) >= 1:
        return f"{x:.2f}"
    if abs(x) >= 1e-3:
        return f"{x:.{d}g}"
    m, e = f"{x:.1e}".split("e")
    return f"{m}·10^{int(e)}"


def r(x):
    return f"{x:.0f}" if x >= 20 else f"{x:.1f}"


out = []
s1 = {t: json.load(open(os.path.join(HERE, "out", f"s1_{t}.json"))) for t in ORDER if os.path.exists(os.path.join(HERE, "out", f"s1_{t}.json"))}
s2 = {t: json.load(open(os.path.join(HERE, "out", f"s2_{t}.json"))) for t in ORDER if os.path.exists(os.path.join(HERE, "out", f"s2_{t}.json"))}

out.append("<!--T:step1_abs-->")
out.append("| instance (states) | m | subsets | self | cross | **total** | cross regrouped: residue × residue | rigid × rigid | atom × residue | atom × rigid | best pair-by-pair (cross part) | P3's bound (cross part) | P3's bound, all = Γ_m | true remainder `g − I_{m−1}g` |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for t, d in s1.items():
    for m, s in d["sums"].items():
        rem = d["remainder"][m]
        out.append(f"| {NAME[t]} ({d['nstates']}) | {m} | {d['nsubsets'][m]} | {f(s['self'])} | {f(s['cross'])} | **{f(s['total'])}** | {f(s['ggx_residue'])} | {f(s['ggx_rigid'])} | "
                   f"{f(s['agx_residue'])} | {f(s['agx_rigid'])} | {f(s['pair_cross'])} | {f(s['P3_cross'])} | {f(s['P3'])} | [{f(rem[0], 2)}, {f(rem[1], 2)}] |")
out.append("<!--/T:step1_abs-->")
out.append("")
out.append("<!--T:step1_ratio-->")
out.append("| instance | m | P3 `Γ_m` / total | best pair-by-pair / total | atom × united group | atom × residue | atom × all partners | united × united | rigid × rigid | residue × residue | residue × all | best pair-by-pair / (atom × residue) | best pair-by-pair / (residue × residue) | P3 / best pair-by-pair |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for t, d in s1.items():
    for m, s in d["sums"].items():
        T = s["total"]
        gu = r(s["gg_united"] / T) if "gg_united" in s else "—"
        out.append(f"| {NAME[t]} | {m} | {r(s['P3'] / T)} | {r(s['pair'] / T)} | {r(s['ag_united'] / T)} | {r(s['ag_residue'] / T)} | {r(s['atom'] / T)} | {gu} | {r(s['gg_rigid'] / T)} | "
                   f"{r(s['gg_residue'] / T)} | {r(s['grp_residue'] / T)} | {r(s['pair'] / s['ag_residue'])} | {r(s['pair'] / s['gg_residue'])} | {r(s['P3'] / s['pair'])} |")
out.append("<!--/T:step1_ratio-->")
out.append("")
out.append("<!--T:step1_checks-->")
tot_states = 0; tot_chk = 0; tot_viol = 0
rmin, rmax = np.inf, 0
for t, d in s1.items():
    ps = d["per_subset"]
    rat = np.array([ps["P3"][k] / ps["total"][k] for k in ps["P3"] if ps["total"][k] > 0])
    rat2 = np.array([ps["P3"][k] / ps["pair"][k] for k in ps["P3"] if ps["pair"][k] > 0])
    out.append(f"| {NAME[t]} | {d['nstates']} | {len(ps['total'])} | {d['checks']['n']} | {d['checks']['violations']} | {rat.min():.1f} – {rat.max():.0f} | {rat2.min():.2f} – {rat2.max():.1f} |")
    tot_states += d["nstates"]; tot_chk += d["checks"]["n"]; tot_viol += d["checks"]["violations"]
    rmin = min(rmin, rat.min()); rmax = max(rmax, rat.max())
out.append(f"| all | {tot_states} | | {tot_chk} | {tot_viol} | {rmin:.1f} – {rmax:.0f} | |")
out.append("<!--/T:step1_checks-->")
out.append("")
out.append("<!--T:step2-->")
out.append("| instance | m | **remainder** `sup_x\\|g − I_{m−1}g\\|`: truth | all charges positive | sign pattern found | **(C) every sign-blind bound of the remainder / truth ≥** | P3's `Γ_m` | `Γ_m` / (pattern found) | **sums over subsets** `Σ_T c_T`: truth | (B) best single pattern found | (A) `Σ_T` best pattern per subset | best pair-by-pair `Σ_T PP_T` | P3 `Σ_T ĉ_T` | **(B) / truth ≥** | **(A) / truth ≥** | P3 / (A) ≤ | pair-by-pair / (A) ≤ |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for t, d in s2.items():
    for m, o in d["orders"].items():
        B = max(o["onepattern_sum"], o["allplus_sum"])
        out.append(f"| {NAME[t]} | {m} | {f(o['rem_true'])} | {f(o['rem_allplus'])} | {f(o['rem_LS'])} | **{r(o['rem_LS'] / o['rem_true'])}** | {f(o['Gamma'])} | {r(o['Gamma'] / o['rem_LS'])} | "
                   f"{f(o['truth_sum'])} | {f(B)} | {f(o['LS_sum'])}{'' if o.get('per_subset_search', True) else ' †'} | {f(o['pair_sum'])} | {f(o['P3_sum'])} | **{r(B / o['truth_sum'])}** | **{r(o['LS_sum'] / o['truth_sum'])}**{'' if o.get('per_subset_search', True) else ' †'} | "
                   f"{r(o['P3_sum'] / o['LS_sum'])} | {r(o['pair_sum'] / o['LS_sum'])} |")
out.append("<!--/T:step2-->")
out.append("")
out.append("<!--T:step2_checks-->")
a = b = c = e = 0
for t, d in s2.items():
    mx = max(o["Gamma"] / o["rem_true"] for o in d["orders"].values())
    out.append(f"| {NAME[t]} | {d['nstates']} | {d['chain_checks']['n']} | {d['chain_checks']['violations']} | {d['state_checks']['n']} | {d['state_checks']['violations']} | {d['state_checks']['min_ratio']:.1f} | {mx:.0f} |")
    a += d["chain_checks"]["n"]; b += d["chain_checks"]["violations"]; c += d["state_checks"]["n"]; e += d["state_checks"]["violations"]
out.append(f"| all | | {a} | {b} | {c} | {e} | | |")
out.append("<!--/T:step2_checks-->")
open(os.path.join(HERE, "out", "tables.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))

# ----------------------------------------------------------------------------- P3's pipeline on the helix (floor_p3copy.py)
fl = []
for fn in sorted(glob.glob(os.path.join(HERE, "out", "floor_*.json"))):
    d = json.load(open(fn))
    fl.append(d)
fl.sort(key=lambda d: (d["n"], d["m"]))
rows = ["", "<!--T:floor-->",
        "| instance | assignments | m | ball: evaluations (% of the domain) | `Γ_m` kcal/mol; largest `γ_i` (`k_BT`) | deterministic bracket of `ln Z(E)` | width (nats) | exact `ln Z(E)` (enumeration) | sandwich violations / states checked | cost number `Z(m₋)/Z(E) − 1` | Hoeffding bracket, δ = 0.05 (N) | width | Bennett bracket (certified `b`, `s²`) width | mean number of sites off the anchor; distinct sampled states | wall time (s) |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for d in fl:
    G6 = d["Gamma_self"] + d["Gamma_cross"]
    gmax = max(d["gamma_sites"]) / 0.596161 if "gamma_sites" in d else float("nan")
    enum = d.get("enum", False)
    lz = f"{d['lnZ_E']:.6f}" if enum else "—"
    viol = f"{d['viol_lower'] + d['viol_upper']} / {int(d['size'])}" if enum else "not enumerated"
    cost = f"{d['cost']:.3g}" if enum else "—"
    hb = f"[{d['bracket_lo']:.4f}, {d['bracket_hi']:.4f}] ({d['N']})" if "bracket_lo" in d else "—"
    hw = f"{d['bracket_hi'] - d['bracket_lo']:.4f}" if "bracket_lo" in d else "—"
    bw = f"{d['bennett_bracket_hi'] - d['bennett_bracket_lo']:.3f}" if "bennett_bracket_lo" in d else "—"
    ms = f"{d['mean_changed_sites']:.2f}; {d['distinct_samples']}" if "mean_changed_sites" in d else "—"
    rows.append(f"| Leu{d['n']}/H τ0.60 | {int(d['size'])} | {d['m']} | {d['nball']} ({100 * d['nball'] / d['size']:.3g}) | {G6:.3f}; {gmax:.2f} | "
                f"[{d['lnZ_upper_model']:.4f}, {d['lnZ_lower_model']:.4f}] | {d['lnZ_lower_model'] - d['lnZ_upper_model']:.3f} | {lz} | {viol} | {cost} | {hb} | {hw} | {bw} | {ms} | {d['seconds']:.0f} |")
rows.append("<!--/T:floor-->")
open(os.path.join(HERE, "out", "tables.md"), "a").write("\n".join(rows) + "\n")
print("\n".join(rows))

# ----------------------------------------------------------------------------- ranges quoted in the text
def rng_(fn, sel=lambda t: True, orders=("3", "4", "5", "6")):
    v = [fn(d["sums"][m]) for t, d in s1.items() if sel(t) for m in d["sums"] if m in orders]
    return f"{min(v):.2f} – {max(v):.1f}" if v else "n/a"


leu = lambda t: t.startswith("L"); ser = lambda t: t.startswith("S")
G4 = ["residue", "rigid", "peptide", "united"]
lines = ["", "<!--T:ranges-->"]
for nm, sel in (("Leu", leu), ("Ser", ser), ("all", lambda t: True)):
    lines.append(f"{nm}: pair/ag_residue {rng_(lambda s: s['pair'] / s['ag_residue'], sel)}; pair/ag (all four groupings) "
                 f"{min(float(rng_(lambda s, g=g: s['pair'] / s['ag_' + g], sel).split(' – ')[0]) for g in G4):.2f} – {max(float(rng_(lambda s, g=g: s['pair'] / s['ag_' + g], sel).split(' – ')[1]) for g in G4):.1f}; "
                 f"pair_cross/agx_residue {rng_(lambda s: s['pair_cross'] / s['agx_residue'], sel)}; pair/gg_residue {rng_(lambda s: s['pair'] / s['gg_residue'], sel)}; "
                 f"pair/gg_rigid {rng_(lambda s: s['pair'] / s['gg_rigid'], sel)}; pair_cross/ggx_residue {rng_(lambda s: s['pair_cross'] / s['ggx_residue'], sel)}")
    lines.append(f"{nm}: ag_residue/total {rng_(lambda s: s['ag_residue'] / s['total'], sel)}; ag (all groupings)/total "
                 f"{min(float(rng_(lambda s, g=g: s['ag_' + g] / s['total'], sel).split(' – ')[0]) for g in G4):.2f} – {max(float(rng_(lambda s, g=g: s['ag_' + g] / s['total'], sel).split(' – ')[1]) for g in G4):.1f}; "
                 f"atom/total {rng_(lambda s: s['atom'] / s['total'], sel)}; gg_residue/total {rng_(lambda s: s['gg_residue'] / s['total'], sel)}; gg_rigid/total {rng_(lambda s: s['gg_rigid'] / s['total'], sel)}; "
                 f"grp_residue/total {rng_(lambda s: s['grp_residue'] / s['total'], sel)}; pair/total {rng_(lambda s: s['pair'] / s['total'], sel)}; P3/total {rng_(lambda s: s['P3'] / s['total'], sel)}; "
                 f"P3/pair {rng_(lambda s: s['P3'] / s['pair'], sel)}; pair/atom {rng_(lambda s: s['pair'] / s['atom'], sel)}; atom/grp_residue {rng_(lambda s: s['atom'] / s['grp_residue'], sel)}; "
                 f"self/total {rng_(lambda s: s['self'] / s['total'], sel)}; cross/total {rng_(lambda s: s['cross'] / s['total'], sel)}; (self+cross)/total {rng_(lambda s: (s['self'] + s['cross']) / s['total'], sel)}")
    v = [(o["rem_LS"] / o["rem_true"], o["LS_sum"] / o["truth_sum"], max(o["onepattern_sum"], o["allplus_sum"]) / o["truth_sum"], o["Gamma"] / o["rem_LS"], o["P3_sum"] / o["LS_sum"], o["pair_sum"] / o["LS_sum"], o["Gamma"] / o["rem_true"])
         for t, d in s2.items() if sel(t) for o in d["orders"].values()]
    if v:
        a_ = np.array(v)
        lines.append(f"{nm}: (C) {a_[:, 0].min():.1f} – {a_[:, 0].max():.0f}; (A) {a_[:, 1].min():.1f} – {a_[:, 1].max():.0f}; (B) {a_[:, 2].min():.1f} – {a_[:, 2].max():.0f}; "
                     f"Gamma/(C pattern) {a_[:, 3].min():.1f} – {a_[:, 3].max():.0f}; P3/(A) {a_[:, 4].min():.1f} – {a_[:, 4].max():.0f}; pair/(A) {a_[:, 5].min():.2f} – {a_[:, 5].max():.2f}; Gamma/true remainder {a_[:, 6].min():.0f} – {a_[:, 6].max():.0f}")
lines.append("<!--/T:ranges-->")
open(os.path.join(HERE, "out", "tables.md"), "a").write("\n".join(lines) + "\n")
print("\n".join(lines))
