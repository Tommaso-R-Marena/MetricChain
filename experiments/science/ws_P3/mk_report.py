"""
P3: condensed tables for the report, from out/floor_*.json, out/tight_*.json and logs/x04_gamma_*.log.
usage: python3 -B mk_report.py            -> prints the fragments (also written to out/report_tables.md)
       python3 -B mk_report.py --fill R   -> replaces the blocks <!--T:name--> ... <!--/T:name--> in the file R
"""
import json, glob, os, re, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
KT = 0.0019872041 * 300.0
runs = []
for f in sorted(glob.glob(os.path.join(HERE, "out", "floor_*.json"))):
    r = json.load(open(f))
    r["file"] = os.path.basename(f)
    r["siteres"] = "gamma_sites" in r
    mm = re.fullmatch(r"([A-Z]+)[:c]?(\d+)", r["seq"].replace(":", "c"))
    r["res"], r["nres"] = (mm.group(1), int(mm.group(2))) if mm else (r["seq"], r["n"])
    r["G"] = r["Gamma_self"] + r["Gamma_cross"]
    r["wtag"] = "_w" in r["file"]
    runs.append(r)


def f(v, p=3):
    if v is None:
        return "—"
    if v == 0:
        return "0"
    if abs(v) >= 1e4 or abs(v) < 1e-3:
        s = f"{v:.1e}"
        mant, ex = s.split("e")
        return f"{mant}·10^{int(ex)}"
    return f"{v:.{p}g}"


def sel(**kw):
    out = []
    for r in runs:
        ok = True
        for k_, v in kw.items():
            if r.get(k_) != v:
                ok = False
        if ok:
            out.append(r)
    return out


frag = {}
# ------------------------------------------------------------------ totals
en = [r for r in runs if r.get("enum")]
frag["stats"] = (f"{len(runs)} runs of `run_floor.py` ({len(en)} with full enumeration: {sum(int(r['size']) for r in en):,} state checks of `m₋ ≤ E ≤ m₊`, "
                 f"**{sum(r.get('viol_lower', 0) + r.get('viol_upper', 0) for r in en)} violations**; the transfer-matrix `ln Z(m₋)` equals the enumerated one to "
                 f"`{max(abs(r['lnZ_lower_model'] - r['lnZ_lower_enum']) for r in en):.0e}`; the anchor from coordinate descent is the global minimiser of `E` in "
                 f"{sum(1 for r in en if r.get('E_anchor_is_min'))} of {len(en)}; the true `ln Z` lies inside the Hoeffding bracket in "
                 f"{sum(1 for r in en if r.get('truth_in_bracket'))} of {sum(1 for r in en if 'truth_in_bracket' in r)} runs, inside the sample-range bracket in "
                 f"{sum(1 for r in en if r.get('truth_in_range_bracket'))} of {sum(1 for r in en if 'truth_in_range_bracket' in r)}, inside the Bennett bracket in "
                 f"{sum(1 for r in en if r.get('truth_in_bennett_bracket'))} of {sum(1 for r in en if 'truth_in_bennett_bracket' in r)})")
# ------------------------------------------------------------------ tightness of the analysis-only bound
rows = {}
for cls in ("apolar", "polar", "charged"):
    fn = os.path.join(HERE, "out", f"tight_{cls}.json")
    if not os.path.exists(fn):
        continue
    for spec, o in json.load(open(fn)).items():
        seq, bb, tau = spec.split(":")
        mm = re.fullmatch(r"([A-Z]+?)c?(\d+)", seq)
        key = (mm.group(1), bb, tau)
        rows.setdefault(key, []).append((int(mm.group(2)), o))
lines = ["| side chain, backbone, τ | n | triples | measured (P2) max `c_ijk`; Σ | certified by analysis max `ĉ_ijk`; Σ | Σ certified / Σ measured | per triple: min / median / max | self part alone / measured Σ |", "|---|---|---|---|---|---|---|---|"]
order = {"V": 0, "L": 1, "F": 2, "S": 3, "K": 4, "LKSE": 5}
ntr = 0
for key in sorted(rows, key=lambda k_: (order[k_[0]], k_[1], k_[2])):
    lst = sorted(rows[key])
    ntr += sum(o["ntriples"] for _, o in lst)
    ns = ", ".join(str(n) for n, _ in lst)
    rat = [(o["sum_self"] + o["sum_cross"]) / o["sum_meas"] for _, o in lst]
    lines.append(f"| {key[0]}, {key[1]}, {key[2]} | {ns} | {sum(o['ntriples'] for _, o in lst)} | {f(max(o['max_meas'] for _, o in lst))}; {f(lst[-1][1]['sum_meas'])} | "
                 f"{f(max(o['max_bound'] for _, o in lst))}; {f(lst[-1][1]['sum_self'] + lst[-1][1]['sum_cross'])} | {min(rat):.0f}–{max(rat):.0f} | "
                 f"{min(o['ratio_min'] for _, o in lst):.0f} / {np.median([o['ratio_med'] for _, o in lst]):.0f} / {max(o['ratio_max'] for _, o in lst):.0f} | "
                 f"{min(o['sum_self'] / o['sum_meas'] for _, o in lst):.1f}–{max(o['sum_self'] / o['sum_meas'] for _, o in lst):.1f} |")
frag["tight"] = "\n".join(lines) + f"\n\n(Σ columns: the longest chain of the row.  {ntr} triples in all.)"
# ------------------------------------------------------------------ Gamma_m by n
gam = {}
for r in runs:
    if r["kind"] == "gbn2":
        gam.setdefault((r["res"], r["bb"], r["tau"]), {}).setdefault(r["nres"], {})[r["m"]] = r["G"]
for fn in glob.glob(os.path.join(HERE, "logs", "x04_gamma_*.log")):
    for line in open(fn):
        mm = re.match(r"([A-Z]+?)(\d+):(\w+):([\d.]+): atoms", line)
        if not mm:
            continue
        key = (mm.group(1), mm.group(3), float(mm.group(4)))
        for g_ in re.finditer(r"Gamma_(\d) = ([\d.e+-]+)", line):
            gam.setdefault(key, {}).setdefault(int(mm.group(2)), {})[int(g_.group(1))] = float(g_.group(2))
lines = ["| side chain, backbone, τ | n | Γ₃ | Γ₄ | Γ₅ | Γ₆ | Γ₃/Γ₄, Γ₄/Γ₅, Γ₅/Γ₆ |", "|---|---|---|---|---|---|---|"]
for key in sorted(gam, key=lambda k_: (order.get(k_[0], 9), k_[1], k_[2])):
    for n in sorted(gam[key]):
        g_ = gam[key][n]
        if n < 6 and key[0] in ("V", "L"):
            continue
        rat = ", ".join(f"{g_[m] / g_[m + 1]:.0f}" for m in (3, 4, 5) if m in g_ and m + 1 in g_)
        lines.append(f"| {key[0]}, {key[1]}, {key[2]:.2f} | {n} | " + " | ".join(f(g_.get(m)) for m in (3, 4, 5, 6)) + f" | {rat} |")
frag["gamma"] = "\n".join(lines)


# ------------------------------------------------------------------ floors
def floor_table(siteres, kind="gbn2"):
    lines = ["| instance | \\|X\\| | m | ball: evaluations (% of X) | Γ_m (kT) | `ρ = max(E − m₋)` exact; certified (kT) | cost number `Z(m₋)/Z(E) − 1` | deterministic bracket `ln Z(m₋) − ln Z(m₊)` (nats) | Hoeffding; sample-range bracket (nats) |", "|---|---|---|---|---|---|---|---|---|"]
    rr = [r for r in runs if r["siteres"] == siteres and r["kind"] == kind and not r["wtag"]]
    for r in sorted(rr, key=lambda r: (order.get(r["res"], 9), r["bb"], r["tau"], r["nres"], r["m"])):
        rho = f"{f(r['rho_exact'] / KT)}; {f(r['rho_cert'] / KT)}" if r.get("enum") else f"—; {f(r['rho_cert'] / KT)}"
        hb = f"{f(r['bracket_hi'] - r['bracket_lo'])}; {f(r['range_bracket_hi'] - r['range_bracket_lo'])}" if "bracket_lo" in r else "—"
        cost = f(r["cost"]) if r.get("enum") else (f"≈ {f(1.0 / r['Wbar'] - 1.0)} (sampled)" if "Wbar" in r else "—")
        lines.append(f"| {r['seq']}/{r['bb']} τ{r['tau']:.2f} | {f(r['size'])} | {r['m']} | {r['nball']} ({100 * r['nball'] / r['size']:.2g}) | {f(r['G'] / KT)} | {rho} | {cost} | "
                     f"{f(r['lnZ_lower_model'] - r['lnZ_upper_model'])} | {hb} |")
    return "\n".join(lines)


frag["floor_const"] = floor_table(False)
frag["floor_site"] = floor_table(True)
frag["obc2"] = floor_table(False, "obc2") + "\n\n" + floor_table(True, "obc2")
# ------------------------------------------------------------------ the instance beyond enumeration
lines = ["| run | band w | m | ball evaluations (fraction of X) | Γ_m kcal/mol; max γ_i | deterministic bracket of `ln Z(E)` | width | N | Hoeffding bracket (δ = 0.05) | width | Bennett bracket (certified b, s²) | width | Gibbs–Bogoliubov lower bound | wall time (s) |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
big = [r for r in runs if r["size"] > 3e6]
for r in sorted(big, key=lambda r: (r["seq"], r["bb"], r["m"], r["w"])):
    bb_ = f"[{r['bennett_bracket_lo']:.4f}, {r['bennett_bracket_hi']:.4f}] | {f(r['bennett_bracket_hi'] - r['bennett_bracket_lo'])}" if "bennett_bracket_lo" in r else "— | —"
    lines.append(f"| {r['seq']}/{r['bb']} | {r['w']} | {r['m']} | {r['nball']} ({r['nball'] / r['size']:.1e}) | {f(r['G'])}; {f(max(r['gamma_sites'])) if r['siteres'] else '—'} | "
                 f"[{r['lnZ_upper_model']:.4f}, {r['lnZ_lower_model']:.4f}] | {f(r['lnZ_lower_model'] - r['lnZ_upper_model'])} | {r['N']} | "
                 f"[{r['bracket_lo']:.4f}, {r['bracket_hi']:.4f}] | {f(r['bracket_hi'] - r['bracket_lo'])} | {bb_} | {r['gibbs_bogoliubov_lower']:.4f} | {r['seconds']:.0f} |")
frag["big"] = "\n".join(lines)
# ------------------------------------------------------------------ Bennett inputs
lines = ["| instance | m | band | model | `b_cert` | `b` enum. | `s²_cert` | `Var r` enum. | `W(b_cert, s²_cert)` (nats) | `W` with enum. `b, s²` | true gap `K` | sampled: mean r; var r; min r (N) |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
bn = [r for r in runs if r["siteres"] and r["kind"] == "gbn2" and "bennett" in r]
for r in sorted(bn, key=lambda r: (order.get(r["res"], 9), r["bb"], r["tau"], r["nres"], r["m"], r["w"])):
    for nm, lab in (("lower", "m₋"), ("mid", "m₀")):
        bd = r["bennett"][nm]
        e_ = "b_enum" in bd
        smp = f"{f(r['r_mean'])}; {f(r['r_var'])}; {f(r['r_min'])} ({r['N']})" if nm == "lower" and "r_mean" in r else "—"
        lines.append(f"| {r['seq']}/{r['bb']} τ{r['tau']:.2f} | {r['m']} | {r['w']} | {lab} | {f(bd['b_cert'])} | {f(bd['b_enum']) if e_ else '—'} | {f(bd['s2_cert'])} | "
                     f"{f(bd['s2_enum']) if e_ else '—'} | {f(bd['W_cert'])} | {f(bd['W_enum']) if e_ else '—'} | {f(bd['K_true']) if e_ else '—'} | {smp} |")
frag["bennett"] = "\n".join(lines)
# ------------------------------------------------------------------ one-site oscillations
lines = ["| instance | m | max certified `c_i = 2mγ_i` (kT) | `Σ_i c_i²` certified (kT²) | max exact `c_i` (kT) | `Σ_i c_i²` exact (kT²) |", "|---|---|---|---|---|---|"]
for r in sorted([r for r in runs if r["siteres"] and r["kind"] == "gbn2" and not r["wtag"]], key=lambda r: (order.get(r["res"], 9), r["bb"], r["tau"], r["nres"], r["m"])):
    c = 2 * r["m"] * np.array(r["gamma_sites"]) / KT
    e_ = np.array(r["osc_rem"]) / KT if "osc_rem" in r else None
    lines.append(f"| {r['seq']}/{r['bb']} τ{r['tau']:.2f} | {r['m']} | {f(float(c.max()))} | {f(float((c ** 2).sum()))} | "
                 + (f"{f(float(e_.max()))} | {f(float((e_ ** 2).sum()))} |" if e_ is not None else "— | — |"))
frag["osc"] = "\n".join(lines)

if "--fill" in sys.argv:
    path = sys.argv[sys.argv.index("--fill") + 1]
    txt = open(path).read()
    for name, body in frag.items():
        pat = re.compile(r"<!--T:" + name + r"-->.*?<!--/T:" + name + r"-->", re.S)
        if pat.search(txt):
            txt = pat.sub(lambda m_: f"<!--T:{name}-->\n{body}\n<!--/T:{name}-->", txt)
    tmp = path + ".tmp"
    open(tmp, "w").write(txt)
    os.replace(tmp, path)
    print("filled", [n for n in frag if f"<!--T:{n}-->" in txt])
else:
    out = "\n\n".join(f"#### {k_}\n\n{v}" for k_, v in frag.items())
    open(os.path.join(HERE, "out", "report_tables.md"), "w").write(out + "\n")
    print(out)
