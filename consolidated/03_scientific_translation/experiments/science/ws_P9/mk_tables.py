#!/usr/bin/env python3
"""P9 -- the tables of the report, generated from the JSON files of COMPLETED runs (out/*.json), so that no number of a
table is typed by hand.  Writes report_parts/gen_*.md; mk_report.py concatenates the parts into
docs/science/workstreams/P9_REPORT.md.   usage: python3 -B mk_tables.py"""
import os, json, glob, math, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out"); PARTS = os.path.join(HERE, "report_parts")
os.makedirs(PARTS, exist_ok=True)


def J(name):
    fn = os.path.join(OUT, name)
    return json.load(open(fn)) if os.path.exists(fn) else None


def g(x, d=4):
    if x is None or (isinstance(x, float) and x != x):
        return "—"
    return f"{x:.{d}g}"


def ball_of(tag, m):
    """the ball size as printed by the bracket runs themselves ('ball of radius M: N values')."""
    for f in sorted(glob.glob(os.path.join(HERE, "logs", f"brackets_{tag}_m{m}_w7*.log"))):
        mm = re.search(r"ball of radius \d+: (\d+) values", open(f).read())
        if mm:
            return f"{int(mm.group(1)):,}".replace(",", " ")
    return "?"


NAMES = {"K4": "Lys₄", "K5": "Lys₅", "LKSEc5": "LKSE:5", "K12": "Lys₁₂", "LKSEc12": "(LKSE)₃"}
SRC = {"ref": "P8's constants 'SAb' (the coordinator's recipe)", "sab": "P8's constants 'SAb', my chains", "cJ1": "joint maxima of stage 1 (constants)",
       "cJ2": "joint maxima of stage 2 (constants)", "s1": "resolved, stage 1", "s2": "**resolved, stage 2**"}

# ---------------------------------------------------------------- validation
lines = ["| instance (states; blocks) | order | subsets | stage | V1: block comparisons; violations; smallest bound/exact | V2: whole function, violations; smallest bound/remainder | V3, V4: violations over all table forms (envelope ≤ table; remainder ≤ table; chain) | Boltzmann mean of the envelope / of the remainder | control W1 (minimum over the states): violations at block level; whole function | control W2 (wrong rotamer): block level; whole function | controls on the tables, 'envelope ≤ table' violated: fewest over the forms (W1; W2) | control W4 (far parts dropped), 'envelope ≤ table' violated: fewest over the banded forms |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
tot = dict(v1=0, v2=0, v3=0, viol=0); rng_ = {}


def upd(key, v):
    lo_, hi_ = rng_.get(key, (v, v)); rng_[key] = (min(lo_, v), max(hi_, v))


for tag, stem in (("K4", "validate_K4_H_0.70"), ("K5", "validate_K5_H_0.70"), ("LKSEc5", "validate_LKSEc5_H_0.60")):
    d = J(stem + ".json"); lf = os.path.join(HERE, "logs", stem + ".log")
    if d is None or not os.path.exists(lf) or "ALL DONE" not in open(lf).read():
        continue
    L_ = open(lf).read()
    S_ = int(re.search(r", (\d+) states, anchor", L_).group(1)); nB_ = int(re.search(r"for (\d+) blocks", L_).group(1))
    for m, row in d["orders"].items():
        for s in (1, 2):
            r = row[f"stage{s}"]; forms = {k: v for k, v in r.items() if isinstance(v, dict) and "env_viol" in v}
            ve = sum(v["env_viol"] for v in forms.values()); vr = sum(v["R_viol"] for v in forms.values()); vc = sum(v["chain_viol"] for v in forms.values())
            c1 = min(v["controls"][0][0] for v in forms.values()); c2 = min(v["controls"][1][0] for v in forms.values())
            c4 = [v["controls"][2][0] for v in forms.values() if len(v["controls"]) > 2]
            ratio = r["mean_env_kT"] / max(r["mean_R_kT"], 1e-300)
            lines.append(f"| {NAMES[tag]} ({S_}; {nB_}) | {m} | {row['subsets']} | {s} | {nB_ * S_}; {r['V1_viol']}; **{r['V1_min_ratio']:.4f}** | {r['V2_viol']}; {r['V2_min_ratio']:.2f} | {ve}; {vr}; {vc} ({len(forms)} forms) | "
                         f"{ratio:.0f} | {r['ctl_min_block']}; {r['ctl_min_whole']} | {r['ctl_roll_block']}; {r['ctl_roll_whole']} | {c1}; {c2} | {min(c4) if c4 else '—'} |")
            tot["viol"] += r["V1_viol"] + r["V2_viol"] + ve + vr + vc; tot["v1"] += nB_ * S_; tot["v2"] += S_; tot["v3"] += 2 * len(forms) * S_
            for key, v in (("V1", r["V1_min_ratio"]), ("V2", r["V2_min_ratio"]), ("mean", ratio), ("c1b", r["ctl_min_block"]), ("c1w", r["ctl_min_whole"]), ("c2b", r["ctl_roll_block"]), ("c2w", r["ctl_roll_whole"]), ("c1t", c1), ("c2t", c2)):
                upd((s, key), v)
            if c4:
                upd((s, "c4t"), min(c4))
summ = [f"\nIn all: {tot['v1']} block-level comparisons (V1), {tot['v2']} whole-function checks (V2), {tot['v3']} table checks (V3: two inequalities per form and state); **violations of V1–V4: {tot['viol']}**.", "", "Ranges over the rows:", ""]
for s in (1, 2):
    R_ = lambda k_: rng_[(s, k_)]
    summ.append(f"* stage {s}: smallest block ratio {R_('V1')[0]:.4f}–{R_('V1')[1]:.4f}; smallest whole-function ratio {R_('V2')[0]:.1f}–{R_('V2')[1]:.1f}; Boltzmann mean of the envelope over that of the remainder {R_('mean')[0]:.0f}–{R_('mean')[1]:.0f}; "
                f"control W1 at block level {R_('c1b')[0]}–{R_('c1b')[1]} violations, against the whole function {R_('c1w')[0]}–{R_('c1w')[1]}; control W2 at block level {R_('c2b')[0]}–{R_('c2b')[1]}, against the whole function {R_('c2w')[0]}–{R_('c2w')[1]}; "
                f"controls on the tables ('envelope ≤ table'): W1 at least {R_('c1t')[0]}, W2 at least {R_('c2t')[0]}, W4 at least {R_('c4t')[0]} violations in every form and row.")
open(os.path.join(PARTS, "gen_validation.md"), "w").write("\n".join(lines) + "\n" + "\n".join(summ) + "\n")

# ---------------------------------------------------------------- brackets
def bracket_table(tag, m, w, labels):
    rows = {}; w0 = None
    for lab in labels:
        d = J(f"brackets_{tag}_m{m}_w{w}" + (f"_{lab}" if lab else "") + ".json")
        if d is None:
            continue
        rows.update(d["rows"]); w0 = d["width_zero"]
    return rows, w0


def fmt_rows(rows, enum=False):
    out = ["| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | " + ("violated at any state; exact `ln Z` inside | " if enum else "") + "exact samples of the floor: sites off the anchor (mean); violations |",
           "|---|---|---|---|---|---|---|" + ("---|" if enum else "")]
    for key in sorted(rows, key=lambda k_: ("SBTW".index(k_.split(":")[1]), ["ref", "sab", "cJ1", "cJ2", "s1", "s2"].index(k_.split(":")[0]))):
        r = rows[key]; src, form = key.split(":")
        fl = f"{r['nfloor']} samples: {r['floor_off']:.2f}; {r['floor_viol']}" if "floor_viol" in r else "—"
        en = f"{r['viol_all']}; {'yes' if r['inside'] else 'NO'} | " if enum else ""
        out.append(f"| {SRC[src]} | {form} | `[{r['lnZ_lo']:.6f}, {r['lnZ_hi']:.6f}]` | **{g(r['width'])}** | {g(r['first_order'])} | {r['viol_gibbs']} | {en}{fl} |")
    return "\n".join(out)


txt = []
for tag, m, w, labels, enum, title in (("K12_H_0.70", 4, 7, ["A", "B"], False, "Lys₁₂, order 4, band 7 (ball 96 366)"),
                                       ("K12_H_0.70", 5, 7, ["A", "B"], False, "Lys₁₂, order 5, band 7 (ball 1 621 056)"),
                                       ("LKSEc12_H_0.60", 5, 7, ["A", "B"], False, "(LKSE)₃, order 5, band 7 (ball 3 471 783)"),
                                       ("LKSEc12_H_0.60", 4, 7, ["X"], False, "(LKSE)₃, ORDER 4, band 7 (ball 181 268) — an order at which no certificate had been attempted"),
                                       ("K12_H_0.70", 3, 7, ["X"], False, "Lys₁₂, ORDER 3, band 7 (ball 3 841)"),
                                       ("LKSEc12_H_0.60", 3, 7, ["X"], False, "(LKSE)₃, ORDER 3, band 7 (ball 6 083)"),
                                       ("S12_H_0.70", 5, 7, ["X"], False, "Ser₁₂, order 5, band 7 (ball 481 506)"),
                                       ("LKSEc5_H_0.60", 4, 2, [""], True, "LKSE:5 (14 508 states, enumerated), order 4, band 2"),
                                       ("LKSEc5_H_0.60", 5, 2, [""], True, "LKSE:5 (enumerated), order 5, band 2"),
                                       ("K5_H_0.70", 4, 2, [""], True, "Lys₅ (115 248 states, enumerated), order 4, band 2"),
                                       ("K5_H_0.70", 4, 3, [""], True, "Lys₅ (enumerated), order 4, band 3"),
                                       ("K5_H_0.70", 5, 3, [""], True, "Lys₅ (enumerated), order 5, band 3")):
    rows, w0 = bracket_table(tag, m, w, labels)
    if not rows:
        continue
    title = re.sub(r"\(ball [\d ]+\)", lambda _: f"(ball {ball_of(tag, m)})", title)
    txt.append(f"**{title}** — the models with all penalties zero (what the reductions cost; not a sandwich): {g(w0)} nats.\n\n" + fmt_rows(rows, enum) + "\n")
    open(os.path.join(PARTS, f"gen_brackets_{tag.split('_')[0].lower()}_m{m}_w{w}.md"), "w").write(txt[-1])
open(os.path.join(PARTS, "gen_brackets.md"), "w").write("\n".join(txt))

# ---------------------------------------------------------------- gain: sites and forms
txt = []
for tag, m, title in (("K12_H_0.70", 4, "Lys₁₂, order 4"), ("K12_H_0.70", 5, "Lys₁₂, order 5"), ("LKSEc12_H_0.60", 5, "(LKSE)₃, order 5")):
    d = J(f"gain_{tag}_m{m}_w7.json")
    if d is None:
        continue
    t = [f"**{title}** — site form `γ_i(b) = (1/m) Σ_{{T∋i}} max{{Θ_T : x_i = b}}` against the state-independent `γ_i^SAb = (1/m) Σ_{{T∋i}} ĉ_T^SAb`.\n",
         "| site | states | visits off the anchor (pooled Gibbs sample, 1 920 states) | `βγ_i^SAb` | stage 1: max over `b`, Boltzmann-typical, min over `b` (ratios to `γ_i^SAb`) | **stage 2**: max, typical, min |", "|---|---|---|---|---|---|"]
    for r in d["sites"]:
        c = [f"{r[f'stage{s}']['max']:.3f}, {g(r[f'stage{s}']['typical'], 3)}, {r[f'stage{s}']['min']:.3f}" for s in (1, 2)]
        t.append(f"| {r['site']} | {r['k']} | {r['visits']} | {g(r['gSAb_kT'])} | {c[0]} | {c[1]} |")
    t.append("\nFirst-order numbers `2β⟨pen⟩` on the check sample (seed 777) [the estimate `ln⟨e^{β pen}⟩ − ln⟨e^{−β pen}⟩`; the largest `β·pen` on the sample] — uncertified estimates:\n")
    t += ["| form | P8's constants SAb | joint maxima of stage 2 as constants | resolved, stage 1 | **resolved, stage 2** | stage 2 / SAb |", "|---|---|---|---|---|---|"]
    for form in "SBTW":
        R = d["forms"][form]; c = lambda n_: f"{g(R[n_]['777']['first'], 3)} [{g(R[n_]['777']['expo'], 3)}; {g(R[n_]['777']['largest'], 3)}]"
        t.append(f"| {form} | {c('SAb')} | {c('cJ2')} | {c('s1')} | {c('s2')} | {g(R['s2']['777']['first'] / max(R['SAb']['777']['first'], 1e-300), 3)} |")
    E = d["envelope"]; c = lambda n_: f"{g(E[n_]['777']['first'], 3)} / {g(E[n_]['4242']['first'], 3)}"
    t.append(f"\nEnvelope `Σ_{{T⊆S(x)}}`, `2β⟨env⟩` on the two samples (777 / 4242): P8's constants {c('SAb')}; joint maxima of stage 2 {c('cJ2')}; resolved stage 1 {c('s1')}; **resolved stage 2 {c('s2')}**.\n")
    txt.append("\n".join(t))
open(os.path.join(PARTS, "gen_gain.md"), "w").write("\n\n".join(txt) + "\n")
# ---------------------------------------------------------------- by rotamer
txt = []
for tag, m, title in (("K12_H_0.70", 4, "Lys₁₂, order 4"), ("LKSEc12_H_0.60", 5, "(LKSE)₃, order 5")):
    d = J(f"gain_{tag}_m{m}_w7.json")
    if d is None:
        continue
    t = [f"{title}: for every non-anchor rotamer `b` of a site, in the order of the domain: frequency in the pooled Gibbs sample / `γ_i(b)/γ_i^SAb` stage 1 / stage 2", "", "```"]
    for r in d["sites"]:
        t.append(f"site {r['site']:2d}: " + "  ".join(f"{f_:.3f}/{r1:.2f}/{r2:.3f}" for f_, r1, r2 in zip(r["freq_by_state"], r["stage1"]["by_state"], r["stage2"]["by_state"])))
    t.append("```")
    txt.append("\n".join(t))
open(os.path.join(PARTS, "gen_rotamers.md"), "w").write("\n\n".join(txt) + "\n")

# ---------------------------------------------------------------- constants and checks at twelve residues
import re
rows = ["| peptide, order | subsets | `βΓ_m`: P8's 'Sb' | P8's 'SAb' | joint maximum, stage 1 `Σ ĉ^{J,1}` | **joint maximum, stage 2 `Σ ĉ^{J,2}`** | sum of the medians over the states: stage 1; stage 2 | sum of the minima: stage 1; stage 2 | `ĉ^{J,2}/ĉ^{SAb}` per subset: min, median, max | seconds per subset; peak RSS (MB) |", "|---|---|---|---|---|---|---|---|---|---|"]
for tag, m, name, lg in (("K12_H_0.70", 3, "Lys₁₂, 3", "tables_K12_H_0.70_m3_w7.log"), ("K12_H_0.70", 4, "Lys₁₂, 4", "tables_K12_H_0.70_m4_w7.log"), ("K12_H_0.70", 5, "Lys₁₂, 5", "tables_K12_H_0.70_m5_w7.log"),
                         ("LKSEc12_H_0.60", 3, "(LKSE)₃, 3", "tables_LKSEc12_H_0.60_m3_w7.log"), ("LKSEc12_H_0.60", 4, "(LKSE)₃, 4", "tables_LKSEc12_H_0.60_m4_w7.log"),
                         ("LKSEc12_H_0.60", 5, "(LKSE)₃, 5", "tables_LKSEc12_H_0.60_m5_w7_merge.log"), ("S12_H_0.70", 5, "Ser₁₂, 5", "tables_S12_H_0.70_m5_w7.log")):
    fn = os.path.join(HERE, "logs", lg)
    if not os.path.exists(fn):
        continue
    L_ = open(fn).read()
    if "ALL DONE" not in L_:
        continue
    a_ = re.search(r"--- (\d+) subsets of order \d+\.  Gamma_\d in kT:  P8's Sb ([\d.e+-]+), P8's SAb ([\d.e+-]+) \| stage 1: joint maximum ([\d.e+-]+), median over the states ([\d.e+-]+), minimum ([\d.e+-]+) \| stage 2: joint maximum ([\d.e+-]+), median ([\d.e+-]+), minimum ([\d.e+-]+)", L_)
    b_ = re.search(r"stage 2: joint maximum / SAb per subset: min ([\d.]+), median ([\d.]+), max ([\d.]+)", L_)
    parts_ = [os.path.join(HERE, "logs", f) for f in sorted(os.listdir(os.path.join(HERE, "logs"))) if f.startswith(lg.replace("_merge.log", "_p")) and f.endswith(".log")] if "merge" in lg else [fn]
    sps = []; rss = []
    for f in parts_:
        t_ = open(f).read(); c_ = re.findall(r"\(([\d.]+) s per subset\)", t_); r_ = re.search(r"peak RSS (\d+) MB", t_)
        if c_: sps.append(float(c_[-1]))
        if r_: rss.append(int(r_.group(1)))
    rows.append(f"| {name} | {a_.group(1)} | {g(float(a_.group(2)), 5)} | {g(float(a_.group(3)), 5)} | {g(float(a_.group(4)), 5)} | **{g(float(a_.group(7)), 5)}** | {g(float(a_.group(5)))}; {g(float(a_.group(8)))} | {g(float(a_.group(6)))}; {g(float(a_.group(9)))} | {b_.group(1)}, {b_.group(2)}, {b_.group(3)} | {', '.join(f'{v:.2f}' for v in sps)}; {max(rss) if rss else '—'} |")
open(os.path.join(PARTS, "gen_constants.md"), "w").write("\n".join(rows) + "\n")

rows = ["| peptide, order | (a) EVERY state with exactly `m` sites off the anchor: states; violations; smallest and median bound / exact term | (a) controls: minimum over the states; wrong rotamer (violations) | (c) random states with exactly `m` sites off (where no ball of radius `m` exists): states; violations; smallest and median ratio; controls (minimum; wrong rotamer) | (b) uniformly random states, `m … 12` sites off: states; violations; smallest envelope / remainder | (b) control, wrong rotamer (violations) |", "|---|---|---|---|---|---|"]
for tag, m, name in (("K12_H_0.70", 3, "Lys₁₂, 3"), ("K12_H_0.70", 4, "Lys₁₂, 4"), ("K12_H_0.70", 5, "Lys₁₂, 5"), ("LKSEc12_H_0.60", 3, "(LKSE)₃, 3"), ("LKSEc12_H_0.60", 4, "(LKSE)₃, 4"), ("LKSEc12_H_0.60", 5, "(LKSE)₃, 5"), ("S12_H_0.70", 5, "Ser₁₂, 5")):
    d = J(f"check12_{tag}_m{m}.json"); dc = J(f"check12_{tag}_m{m}_shell.json")
    if d is None and dc is None:
        continue
    a_ = (d or {}).get("a"); b_ = (d or {}).get("b"); c_ = (dc or {}).get("c")
    ca = f"{a_['states']}; {a_['viol']}; {a_['min_ratio']:.2f}, {a_['median_ratio']:.0f}" if a_ else "—"
    cc = f"{a_['ctl_min']}; {a_['ctl_roll']}" if a_ else "—"
    c3 = f"{c_['states']}; {c_['viol']}; {c_['min_ratio']:.2f}, {c_['median_ratio']:.0f}; {c_['ctl_min']}; {c_['ctl_roll']}" if c_ else "—"
    cb = f"{b_['states']}; {b_['viol']}; {b_['min_ratio']:.1f}" if b_ else "—"
    rows.append(f"| {name} | {ca} | {cc} | {c3} | {cb} | {b_['ctl_roll'] if b_ else '—'} |")
open(os.path.join(PARTS, "gen_check12.md"), "w").write("\n".join(rows) + "\n")
# ---------------------------------------------------------------- predictions (typed from NOTES.md, where they were written before the models) against outcomes (JSON)
PRED = [  # (instance tag, m, key, predicted text as written in NOTES.md, point, low, high)  -- low/high None where only a point value was written
    ("K12_H_0.70", 4, "zero", "0.007", 0.007, None, None), ("K12_H_0.70", 4, "s1:T", "0.75 (0.6–0.9)", 0.75, 0.6, 0.9), ("K12_H_0.70", 4, "s2:T", "0.15 (0.13–0.18; at worst 0.5)", 0.15, 0.13, 0.18),
    ("K12_H_0.70", 4, "s2:B", "0.25", 0.25, None, None), ("K12_H_0.70", 4, "s2:S", "3 (2.5–4)", 3.0, 2.5, 4.0), ("K12_H_0.70", 4, "sab:W", "0.02 (0.012–0.03)", 0.02, 0.012, 0.03),
    ("K12_H_0.70", 4, "s2:W", "0.0075 (0.0073–0.0080)", 0.0075, 0.0073, 0.0080),
    ("K12_H_0.70", 5, "s1:T", "0.045 (0.043–0.048)", 0.045, 0.043, 0.048), ("K12_H_0.70", 5, "s2:T", "0.0165 (0.016–0.0175)", 0.0165, 0.016, 0.0175), ("K12_H_0.70", 5, "s2:B", "0.021", 0.021, None, None),
    ("K12_H_0.70", 5, "s2:S", "0.11", 0.11, None, None), ("K12_H_0.70", 5, "sab:W", "0.0072", 0.0072, None, None), ("K12_H_0.70", 5, "s2:W", "0.00713", 0.00713, None, None),
    ("LKSEc12_H_0.60", 5, "s1:T", "3.3 (2.8–3.8)", 3.3, 2.8, 3.8), ("LKSEc12_H_0.60", 5, "s2:T", "0.25 (0.22–0.35)", 0.25, 0.22, 0.35), ("LKSEc12_H_0.60", 5, "s2:B", "0.4 (0.33–0.5)", 0.4, 0.33, 0.5),
    ("LKSEc12_H_0.60", 5, "s2:S", "4 (3.5–6)", 4.0, 3.5, 6.0), ("LKSEc12_H_0.60", 5, "sab:W", "0.15 (0.1–0.4)", 0.15, 0.1, 0.4), ("LKSEc12_H_0.60", 5, "s2:W", "0.0168 (0.0167–0.0175)", 0.0168, 0.0167, 0.0175),
    ("LKSEc12_H_0.60", 4, "zero", "0.017", 0.017, None, None), ("LKSEc12_H_0.60", 4, "s2:W", "0.02 (0.018–0.03), with a 40 % risk of more than 1", 0.02, 0.018, 0.03), ("LKSEc12_H_0.60", 4, "s2:T", "3 (1.2–8)", 3.0, 1.2, 8.0),
    ("LKSEc12_H_0.60", 4, "s1:W", "more than 5", None, 5.0, 1e9),
    ("K12_H_0.70", 3, "s2:W", "0.12 (0.08–0.3), with a 50 % risk of more than 1", 0.12, 0.08, 0.3), ("K12_H_0.70", 3, "s2:T", "more than 2", None, 2.0, 1e9), ("LKSEc12_H_0.60", 3, "s2:W", "more than 2", None, 2.0, 1e9)]
NM = {"K12_H_0.70": "Lys₁₂", "LKSEc12_H_0.60": "(LKSE)₃"}
WHAT = {"zero": "reductions alone (all penalties zero)", "s1:T": "T, stage 1", "s2:T": "T, stage 2", "s2:B": "B, stage 2", "s2:S": "S, stage 2", "sab:W": "W, P8's constants", "s2:W": "W, stage 2", "s1:W": "W, stage 1"}
rows = ["| instance, order | what | predicted bracket (nats), written before the models | found | found / predicted | inside the range I gave? |", "|---|---|---|---|---|---|"]
for tag, m, key, txt_, pt_, lo_, hi_ in PRED:
    rr = {}; w0 = None
    for f in sorted(glob.glob(os.path.join(OUT, f"brackets_{tag}_m{m}_w7*.json"))):
        d = json.load(open(f)); rr.update(d["rows"]); w0 = d["width_zero"]
    val = w0 if key == "zero" else (rr[key]["width"] if key in rr else None)
    if val is None:
        rows.append(f"| {NM[tag]}, {m} | {WHAT[key]} | {txt_} | not run | — | — |"); continue
    ratio = f"{val / pt_:.2f}" if pt_ else "—"
    verdict = "(no range given)" if lo_ is None else ("yes" if lo_ <= val <= hi_ else "**no**")
    rows.append(f"| {NM[tag]}, {m} | {WHAT[key]} | {txt_} | **{g(val)}** | {ratio} | {verdict} |")
open(os.path.join(PARTS, "gen_predictions.md"), "w").write("\n".join(rows) + "\n")
# ---------------------------------------------------------------- the levers side by side: widths only
rows = ["| instance, order (ball) | penalty | S | B | T (equal shares: the form of the reference) | W (one in-window sub-tuple per subset) | reductions alone |", "|---|---|---|---|---|---|---|"]
NM2 = dict(NM, **{"S12_H_0.70": "Ser₁₂"})
for tag, m in (("K12_H_0.70", 5), ("K12_H_0.70", 4), ("K12_H_0.70", 3), ("LKSEc12_H_0.60", 5), ("LKSEc12_H_0.60", 4), ("LKSEc12_H_0.60", 3), ("S12_H_0.70", 5)):
    rr = {}; w0 = None
    for f in sorted(glob.glob(os.path.join(OUT, f"brackets_{tag}_m{m}_w7*.json"))):
        d = json.load(open(f)); rr.update(d["rows"]); w0 = d["width_zero"]
    if not rr:
        continue
    for src, label in ((("ref", "sab"), "P8's constants"), (("cJ2",), "joint maxima of stage 2 (constants)"), (("s1",), "resolved, stage 1"), (("s2",), "**resolved, stage 2**")):
        cells = []
        for form in "SBTW":
            v = None
            for s_ in src:
                if f"{s_}:{form}" in rr:
                    v = rr[f"{s_}:{form}"]
            cells.append("not run" if v is None else (f"**{g(v['width'])}**" if src == ("s2",) else g(v["width"])) + (f" (floor: {v['floor_off']:.1f} sites off)" if "floor_off" in v else ""))
        if all(c == "not run" for c in cells):
            continue
        rows.append(f"| {NM2[tag]}, {m} ({ball_of(tag, m)}) | {label} | " + " | ".join(cells) + f" | {g(w0)} |")
open(os.path.join(PARTS, "gen_levers.md"), "w").write("\n".join(rows) + "\n")

# ---------------------------------------------------------------- consistency with the coordinator's sampled intervals (their numbers, addendum A17 (18))
SAMPLED = {"K12_H_0.70": (517.128526, 517.128559, "Lys₁₂"), "LKSEc12_H_0.60": (655.592089, 655.632643, "(LKSE)₃")}
sent = []
for tag, (a_, b_, nm) in SAMPLED.items():
    n_all = n_in = n_ov = 0; narrow = None
    for f in sorted(glob.glob(os.path.join(OUT, f"brackets_{tag}_m*_w7*.json"))):
        d = json.load(open(f))
        for key, r in d["rows"].items():
            n_all += 1; n_in += int(r["lnZ_lo"] <= a_ and b_ <= r["lnZ_hi"]); n_ov += int(r["lnZ_lo"] <= b_ and a_ <= r["lnZ_hi"])
            if narrow is None or r["width"] < narrow[0]:
                narrow = (r["width"], r["lnZ_lo"], r["lnZ_hi"], d["m"], key)
    if n_all:
        sent.append(f"{nm}: sampled interval `[{a_:.6f}, {b_:.6f}]` (width {g(b_ - a_, 2)}); of my {n_all} certified brackets (all orders, all rows) {n_in} contain it and {n_ov} overlap it"
                    + (f"; the narrowest, `[{narrow[1]:.6f}, {narrow[2]:.6f}]` (order {narrow[3]}, {narrow[4]}), is {'inside it' if (a_ <= narrow[1] and narrow[2] <= b_) else 'not inside it'}" if n_in < n_all else ""))
open(os.path.join(PARTS, "gen_sampled.md"), "w").write(".  ".join(sent) + ".\n")
# ---------------------------------------------------------------- run times and memory of the bracket runs (from the last lines of their logs)
items = []
for f in sorted(glob.glob(os.path.join(HERE, "logs", "brackets_*_w7_*.log"))):
    t_ = open(f).read(); mm = re.search(r"ALL DONE (\d+) s; peak RSS (\d+) MB", t_)
    if mm:
        items.append(f"`{os.path.basename(f)[9:-4]}`: {mm.group(1)} s, {mm.group(2)} MB")
open(os.path.join(PARTS, "gen_times_brackets.md"), "w").write("; ".join(items) + "\n")
# ---------------------------------------------------------------- named numbers for the prose: templates report_parts/tpl_<name>.md -> gen_<name>.md
V = {}
SHORT = {"K12_H_0.70": "K12", "LKSEc12_H_0.60": "LKSE", "S12_H_0.70": "S12", "K5_H_0.70": "K5", "LKSEc5_H_0.60": "LKSE5"}
for f in sorted(glob.glob(os.path.join(OUT, "brackets_*.json"))):
    d = json.load(open(f)); base = os.path.basename(f)[9:-5]
    tag = next(t for t in SHORT if base.startswith(t)); pre = f"{SHORT[tag]}_{d['m']}" + (f"w{d['w']}" if d["w"] != 7 else "")
    V[f"{pre}_zero"] = g(d["width_zero"])
    for key, r in d["rows"].items():
        k_ = f"{pre}_{key.replace(':', '_')}"
        V[k_] = g(r["width"]); V[k_ + "_lo"] = f"{r['lnZ_lo']:.6f}"; V[k_ + "_hi"] = f"{r['lnZ_hi']:.6f}"; V[k_ + "_raw"] = r["width"]
        if "floor_off" in r:
            V[k_ + "_floor"] = f"{r['floor_off']:.1f}"


for f in sorted(glob.glob(os.path.join(OUT, "nested_sampler_*.json"))):
    d = json.load(open(f)); pre = f"NS_{'LKSE' if d['seq'].startswith('LKSE') else d['seq']}_{d['m']}"
    V[pre + "_D"] = g(d["D"]); V[pre + "_lo"] = f"{d['lnZ_up']:.6f}"; V[pre + "_hi"] = f"{d['lnZ_lo']:.6f}"; V[pre + "_secs"] = f"{d['seconds']:.0f}"; V[pre + "_rss"] = f"{d['peak_rss_mb'] / 1000:.1f}"
    r = d.get("run")
    if r:
        V[pre + "_Nf"] = f"{r['Nf']:,}".replace(",", " "); V[pre + "_draws"] = f"{r['floor_draws']:,}".replace(",", " "); V[pre + "_acc"] = str(r["accepted"]); V[pre + "_N"] = str(r["N"])
        V[pre + "_distinct"] = f"{r['distinct_proposals']:,}".replace(",", " "); V[pre + "_env"] = g(r["envelope_bracket_est"], 3); V[pre + "_viol_in"] = str(r["viol_inner"]); V[pre + "_viol_out"] = str(r["viol_outer"])
        V[pre + "_clip"] = str(r["clip"]); V[pre + "_bad"] = str(r["bad"]); V[pre + "_rho"] = g(r["mean_rho"], 3); V[pre + "_b"] = g(r["mean_b"], 4)
        for kk in ("thy_H", "two_H", "one_H", "thy_EB", "two_EB", "one_EB"):
            b_ = r["brackets"][kk]; V[f"{pre}_{kk}_lo"] = f"{b_['lo']:.6f}"; V[f"{pre}_{kk}_hi"] = f"{b_['hi']:.6f}"; V[f"{pre}_{kk}_w"] = g(b_["hi"] - b_["lo"], 2); V[f"{pre}_{kk}_pt"] = f"{b_['point']:.6f}"
        V[pre + "_rssmb"] = f"{d['peak_rss_mb']:.0f}"; V[pre + "_evald"] = str(r["distinct_evaluated"])
        rat_ = [(r["plain"]["H" if kk.endswith("_H") else "EB"]["hi"] - r["plain"]["H" if kk.endswith("_H") else "EB"]["lo"]) / (r["brackets"][kk]["hi"] - r["brackets"][kk]["lo"]) for kk in r["brackets"]]
        V[pre + "_plain_min"] = g(min(rat_), 2); V[pre + "_plain_max"] = f"{max(rat_):.0f}"
        V[pre + "_evalshare"] = f"{100 * r['brackets']['thy_H']['eval_part'] / r['brackets']['thy_H']['half_W']:.0f}"
        V[pre + "_inside"] = str(sum(d["lnZ_up"] <= b_["lo"] and b_["hi"] <= d["lnZ_lo"] for b_ in r["brackets"].values())); V[pre + "_nkinds"] = str(len(r["brackets"]))
        V[pre + "_inside_coord"] = str(sum(655.592089 <= b_["lo"] and b_["hi"] <= 655.632643 for b_ in r["brackets"].values()))
NSF = {}
for f in sorted(glob.glob(os.path.join(OUT, "nested_sampler_*.json"))):
    d = json.load(open(f)); NSF[(d["seq"], d["m"])] = d
if ("LKSE:12", 5) in NSF and ("LKSE:12", 4) in NSF and NSF[("LKSE:12", 5)].get("run") and NSF[("LKSE:12", 4)].get("run"):
    a_, b_ = NSF[("LKSE:12", 5)], NSF[("LKSE:12", 4)]; kinds_ = list(a_["run"]["brackets"])
    V["NS_NEST"] = str(sum(b_["run"]["brackets"][k]["lo"] <= a_["run"]["brackets"][k]["lo"] and a_["run"]["brackets"][k]["hi"] <= b_["run"]["brackets"][k]["hi"] for k in kinds_))
    V["NS_NEST_OUTER"] = "contains" if (b_["lnZ_up"] <= a_["lnZ_up"] and a_["lnZ_lo"] <= b_["lnZ_lo"]) else "DOES NOT contain"
    V["NS_CROSS"] = str(sum(a_["lnZ_up"] <= x_["lo"] and x_["hi"] <= a_["lnZ_lo"] for x_ in b_["run"]["brackets"].values()))


def ratio(a_, b_, d_=2):
    x = V[a_ + "_raw"] / V[b_ + "_raw"]
    return f"{x:.0f}" if x >= 100 else g(x, d_)


class Strict(dict):
    def __missing__(self, key):
        if key.startswith("R__"):                        # {R__a__b} -> ratio of two named widths, 2 significant digits
            _, a_, b_ = key.split("__")
            return ratio(a_, b_)
        raise KeyError(key)


enum_items = []; enum_ok = True; enum_rows = 0
for f in sorted(glob.glob(os.path.join(OUT, "brackets_K5_*.json")) + glob.glob(os.path.join(OUT, "brackets_LKSEc5_*.json"))):
    d = json.load(open(f)); rows_ = d["rows"]; nm_ = "Lys₅" if "K5_" in os.path.basename(f) else "LKSE:5"
    ok_ = all(r.get("viol_all") == 0 and r.get("inside") is True and r["viol_gibbs"] == 0 for r in rows_.values())
    enum_ok = enum_ok and ok_; enum_rows += len(rows_)
    enum_items.append(f"{nm_}, order {d['m']}, band {d['w']}: {len(rows_)} rows, " + ("no violation at any state, exact value inside every bracket" if ok_ else "**A VIOLATION OR THE EXACT VALUE OUTSIDE**"))
V["ENUM_SENTENCE"] = "; ".join(enum_items); V["ENUM_ROWS"] = str(enum_rows); V["ENUM_OK"] = "no violation at any state and the exact value inside, in every row" if enum_ok else "**NOT ALL ROWS PASS**"
open(os.path.join(PARTS, "gen_enum_sentence.md"), "w").write(f"**{V['ENUM_OK']}** ({V['ENUM_ROWS']} sandwiches in all: {V['ENUM_SENTENCE']})")
V["VAL_V1"] = f"{tot['v1']:,}".replace(",", " "); V["VAL_V2"] = f"{tot['v2']:,}".replace(",", " "); V["VAL_V3"] = f"{tot['v3']:,}".replace(",", " ")
for f in sorted(glob.glob(os.path.join(PARTS, "txt_*.md"))):          # short sentences typed after the runs, with their own named numbers
    try:
        V[os.path.basename(f)[4:-3].upper()] = open(f).read().strip().format_map(Strict(V))
    except KeyError as e:
        print(f"TEXT {os.path.basename(f)}: number not available yet: {e}")
for f in sorted(glob.glob(os.path.join(PARTS, "tpl_*.md"))):
    name = os.path.basename(f)[4:]
    try:
        text_ = open(f).read().format_map(Strict(V))
        open(os.path.join(PARTS, "gen_" + name), "w").write(text_)
    except KeyError as e:
        print(f"TEMPLATE {name}: number not available yet: {e}")
        open(os.path.join(PARTS, "gen_" + name), "w").write(f"**[NOT YET GENERATED: {name} — number {e} missing]**\n")
print("generated:", sorted(os.listdir(PARTS)))
