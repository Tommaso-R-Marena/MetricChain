"""
P6: tables for the report from out/sandwich_*.json, out/sampler_*.json, out/reach_*.json  ->  out/tables.md
usage: python3 -B p6_05_tables.py
"""
import os, json, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def fmt(v, d=3):
    if v is None:
        return "—"
    if v == 0:
        return "0"
    a = abs(v)
    if a >= 1e4 or a < 1e-3:
        e = int(math.floor(math.log10(a)))
        return f"{v / 10 ** e:.{max(d - 2, 1)}f}·10^{e}"
    return f"{v:.{d}g}"


def br(lo, hi, d=4):
    """bracket rounded OUTWARD to d decimals"""
    q = 10 ** d
    return f"[{math.floor(lo * q) / q:.{d}f}, {math.ceil(hi * q) / q:.{d}f}]"


def name(r):
    return f"{r['seq']}/{r['bb']} τ{r['tau']:.2f}" + ("" if r["kind"] == "gbn2" else f" ({r['kind'].upper()})")


def order_key(r):
    seq = r["seq"]
    return (r["kind"], seq[0] if ":" not in seq else "Z", r["bb"], r["n"])


runs = []
for fn in sorted(glob.glob(os.path.join(OUT, "sandwich_*.json"))):
    r = json.load(open(fn))
    r["_file"] = os.path.basename(fn)
    runs.append(r)
enum = sorted([r for r in runs if r["enum"]], key=order_key)
lines = []
P = lines.append

# ---------------------------------------------------------------- totals
tot_states = sum(r["state_checks"] for r in enum); tot_viol = sum(r["violations"] for r in enum)
tot_rem = sum(r["remainder_checks"] for r in enum); tot_rv = sum(r["remainder_violations"] for r in enum)
n_inst = len(enum); n_runs = sum(len(r["orders"]) for r in enum)
n_models = sum(2 * len(R["bands"]) for r in enum for R in r["orders"].values())
strict = sum(F.get("viol_lower_strict", 0) + F.get("viol_upper_strict", 0) for r in enum for R in r["orders"].values() for RW in R["bands"].values() for k_, F in RW.items() if k_ in ("S", "B"))
inside = sum(int(F["truth_inside"]) for r in enum for R in r["orders"].values() for RW in R["bands"].values() for k_, F in RW.items() if k_ in ("S", "B"))
dp = max(F["dp_vs_enum"] for r in enum for R in r["orders"].values() for RW in R["bands"].values() for k_, F in RW.items() if k_ in ("S", "B"))
rat = {}
for r in enum:
    for R in r["orders"].values():
        for nm, v in R.get("remainder", {}).items():
            if v["ratio_min"] == v["ratio_min"]:
                a = rat.setdefault(nm, [math.inf, 0.0, 0])
                a[0] = min(a[0], v["ratio_min"]); a[1] = max(a[1], v["ratio_max"]); a[2] += v["viol"]
        for w, RW in R["bands"].items():
            v = RW.get("remainder_banded")
            if v and v["ratio_min"] == v["ratio_min"] and int(w) < r["n"] - 1:
                a = rat.setdefault("banded (w < n−1)", [math.inf, 0.0, 0])
                a[0] = min(a[0], v["ratio_min"]); a[1] = max(a[1], v["ratio_max"]); a[2] += v["viol"]
p3 = [(RW["p3_repro"]["dlo"], RW["p3_repro"]["dup"]) for r in runs for R in r["orders"].values() for RW in R["bands"].values() if "p3_repro" in RW]
P("<!--T:totals-->")
P(f"{n_inst} enumerated instances, {n_runs} (instance, order) pairs, {n_models} sandwiches (form × band × order); "
  f"**{tot_states:,} checks of `m₋ ≤ E` and `E ≤ m₊`** (two per state and sandwich), **violations: {tot_viol}** (with P3's tolerance 10⁻⁹ kcal/mol; "
  f"with tolerance zero: {strict}); the enumerated `ln Z(E)` lies inside `[ln Z(m₊), ln Z(m₋)]` in {inside} of {n_models}; transfer matrix against enumeration: `≤ {fmt(dp, 2)}`; "
  f"**{tot_rem:,} checks of `|g − I_(m−1) g| ≤ penalty`** (one per state and penalty function), violations: {tot_rv}; "
  f"P3's own `ln Z(m₋)`, `ln Z(m₊)` (site form) reproduced in {len(p3)} runs with largest difference {fmt(max(max(a, b) for a, b in p3), 2) if p3 else '—'}.")
P("")
P("| penalty function | violations of `|remainder| ≤ penalty` | smallest ratio penalty/|remainder| | largest ratio |")
P("|---|---|---|---|")
for nm in ("envelope", "pair", "banded (w < n−1)", "site"):
    if nm in rat:
        P(f"| {nm} | {rat[nm][2]} | {fmt(rat[nm][0])} | {fmt(rat[nm][1])} |")
P("<!--/T:totals-->")
P("")

# ---------------------------------------------------------------- pair sums against enumeration
P("<!--T:pairsums-->")
P("| instance | m | subsets enumerated | pairs | `Γ_m` (kcal/mol) | max abs. difference of `G_ij` | of `S_i` | relative to `Γ_m` | smallest `G_ij` |")
P("|---|---|---|---|---|---|---|---|---|")
worst = 0.0; nsub = 0; npair = 0; ncase = 0
for r in enum:
    for m, R in sorted(r["orders"].items()):
        c = R.get("pairsum_check")
        if not c:
            continue
        worst = max(worst, c["rel_to_Gamma"]); nsub += c["n_subsets"]; npair += c["n_pairs"]; ncase += 1
        P(f"| {name(r)} | {m} | {c['n_subsets']} | {c['n_pairs']} | {fmt(R['Gamma'])} | {fmt(c['dG_max'], 2)} | {fmt(c['dS_max'], 2)} | {fmt(c['rel_to_Gamma'], 2)} | {fmt(c['G_min'], 3)} |")
P("")
P(f"Totals: {ncase} (instance, order) cases, {nsub:,} subsets enumerated, {npair:,} pair sums compared; largest difference relative to `Γ_m`: {fmt(worst, 2)}.")
P("<!--/T:pairsums-->")
P("")

# ---------------------------------------------------------------- widths
P("<!--T:widths-->")
P("| instance | \\|X\\| | m | ball | `Γ_m` (kT) | width, site form (P3), all pairs in band | width, **pair form** | gain | band 2: site → banded pair | band 1: site → banded pair | cost number `Z(m₋)/Z(E) − 1`: site → pair | exact remainder / envelope: min ratio |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|")
BETA = 1.0 / (0.0019872041 * 300.0)
for r in enum:
    for m, R in sorted(r["orders"].items()):
        n = r["n"]
        bs = R["bands"]
        full = bs.get(str(n - 1))
        if full is None:
            continue
        def pairw(w):
            b = bs.get(str(w))
            if b is None or w >= n - 1:
                return "—"
            return f"{fmt(b['S']['width'])} → {fmt(b['B']['width'])}"
        env = R.get("remainder", {}).get("envelope", {}).get("ratio_min")
        P(f"| {name(r)} | {fmt(r['size'], 3)} | {m} | {R['nball']} | {fmt(R['Gamma'] * BETA)} | {fmt(full['S']['width'])} | **{fmt(full['B']['width'])}** | "
          f"{fmt(full['S']['width'] / full['B']['width'], 2)} | {pairw(2)} | {pairw(1)} | {fmt(full['S']['cost_lower'])} → {fmt(full['B']['cost_lower'])} | {fmt(env) if env else '—'} |")
P("<!--/T:widths-->")
P("")

# ---------------------------------------------------------------- big instances
P("<!--T:big-->")
for r in runs:
    if r["enum"]:
        continue
    P(f"**{name(r)}** ({r['natoms']} atoms, {r['n']} sites, |X| = {fmt(r['size'])}; file `{r['_file']}`)")
    P("")
    P("(brackets rounded outward to four decimals)")
    P("")
    P("| m | evaluations of `g` (ball) | `Γ_m` kcal/mol | band w | site form (P3): certified bracket of `ln Z(E)` | width | **banded pair form**: certified bracket | **width** | gain |")
    P("|---|---|---|---|---|---|---|---|---|")
    for m, R in sorted(r["orders"].items()):
        for w, RW in sorted(R["bands"].items(), key=lambda kv: -int(kv[0])):
            S, B = RW["S"], RW["B"]
            P(f"| {m} | {R['nball']} | {fmt(R['Gamma'])} | {w} | {br(S['lnZ_up'], S['lnZ_lo'])} | {S['width']:.4f} | {br(B['lnZ_up'], B['lnZ_lo'])} | **{B['width']:.4f}** | {S['width'] / B['width']:.2f} |")
    P("")
P("<!--/T:big-->")
P("")

# ---------------------------------------------------------------- reach
P("<!--T:reach-->")
P("| instance | atoms | log10 \\|X\\| | m | evaluations | `Γ_m` kcal/mol | band | site form: bracket; width | banded pair form: bracket; **width** | independent estimate (uncertified); inside? | sampled check: states, violations |")
P("|---|---|---|---|---|---|---|---|---|---|---|")
for fn in sorted(glob.glob(os.path.join(OUT, "reach_*.json"))):
    r = json.load(open(fn))
    for w, RW in sorted(r["bands"].items(), key=lambda kv: -int(kv[0])):
        S, B = RW["S"], RW["B"]
        ref = r.get("ref")
        ins = "—" if ref is None else f"{ref:.4f}; {'yes' if B['lnZ_up'] <= ref <= B['lnZ_lo'] else 'NO'}"
        sm = r.get("sample")
        sms = "—" if not sm else f"{sm['N']} ({sm['distinct']} distinct), {sm['viol_lower'] + sm['viol_upper']}"
        P(f"| {r['seq']}/{r['bb']} τ{r['tau']:.2f} | {r['natoms']} | {r['log10_size']:.1f} | {r['m']} | {r['nball']} | {fmt(r['Gamma'])} | {w} | "
          f"{br(S['lnZ_up'], S['lnZ_lo'])}; {S['width']:.4f} | {br(B['lnZ_up'], B['lnZ_lo'])}; **{B['width']:.4f}** | {ins} | {sms} |")
P("<!--/T:reach-->")
P("")

# ---------------------------------------------------------------- sampler
P("<!--T:sampler-->")
P("| instance | m | form | band | deterministic bracket; width D | acceptance rate (exact; observed) | proposals | N accepted | distinct states evaluated | mean W | certified bracket (δ = 0.05) | width | `(e^D − 1)·2t` |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for fn in sorted(glob.glob(os.path.join(OUT, "sampler_*.json"))):
    if "sampler_enum_" in fn:
        continue
    r = json.load(open(fn))
    for NN, b in sorted(r["brackets"].items(), key=lambda kv: int(kv[0])):
        frac = int(NN) / r["N"]
        P(f"| {r['seq']}/{r['bb']} | {r['m']} | {'site (P3)' if r['form'] == 'S' else 'banded pair'} | {r['w']} | {br(r['lnZ_up'], r['lnZ_lo'])}; {r['D']:.4f} | "
          f"{r['acc_rate_exact']:.4f}; {r['emp_acc']:.4f} | {r['proposals'] if int(NN) == r['N'] else '(prefix)'} | {NN} | {r['distinct'] if int(NN) == r['N'] else '—'} | {b['Wmean']:.4f} | "
          f"{br(b['lo'], b['hi'], 5)} | {fmt(b['width'], 3)} | {fmt(b['predicted_width_bound'], 3)} |")
P("")
P("| enumerated instance | m | form | band | states | W range | W outside [0,1] | exact `E_q W` | identity: difference of `ln Z` | repetitions | N | truth inside | mean width | rms error of the point estimate |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for fn in sorted(glob.glob(os.path.join(OUT, "sampler_enum_*.json"))):
    r = json.load(open(fn))
    e, c = r["enum"], r["coverage"]
    P(f"| {r['seq']}/{r['bb']} | {r['m']} | {'site (P3)' if r['form'] == 'S' else 'banded pair'} | {r['w']} | {e['states']} | [{fmt(e['W_min'])}, {fmt(e['W_max'])}] | {e['n_outside']} | {e['EqW']:.6f} | "
      f"{fmt(e['identity_dev'], 2)} | {c['reps']} | {c['N']} | {c['inside']} of {c['reps']} | {fmt(c['mean_width'])} | {fmt(c['rms_err'])} |")
P("<!--/T:sampler-->")
open(os.path.join(OUT, "tables.md"), "w").write("\n".join(lines) + "\n")
print(f"{len(lines)} lines -> out/tables.md; enumerated instances {n_inst}, runs {n_runs}, sandwiches {n_models}, state checks {tot_states}, violations {tot_viol}")
