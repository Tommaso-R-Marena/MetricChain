"""Tables and summary sentences of X-011 (nested runs designed by certified cost), X-011c (designs against cones) and
X-014 (site-dependent slopes), generated from the stored artifacts.

    python experiments/eng/twolevel/make_tables_x011.py                      # print every block
    python experiments/eng/twolevel/make_tables_x011.py --write  FILE.md     # replace the blocks of FILE.md
    python experiments/eng/twolevel/make_tables_x011.py --verify FILE.md     # exit status 1 if a block of FILE.md differs

A block is ``<!-- TABLE:name -->`` ... ``<!-- /TABLE:name -->`` (the mechanism of ``make_tables.py``).
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"


def jl(name: str) -> list[dict]:
    p = RESULTS / name
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()] if p.exists() else []


def f4(x) -> str:
    return "—" if x is None else f"{x:.4f}"


# ---------------------------------------------------------------------------------------------
# X-011a: certified bounds
# ---------------------------------------------------------------------------------------------
def bounds_blocks() -> dict[str, str]:
    rows = jl("x011_certified1.jsonl")
    if not rows:
        return {}
    by = {(r["n"], r["family"]): r for r in rows}
    sizes = sorted({r["n"] for r in rows})
    kmax = max(len(r["rows"]) for r in rows)

    def best(r, k):
        """(value, fraction, complete) of at most k nested levels: the least bound found with 1..k levels."""
        val, phi, complete = None, None, True
        for x in r["rows"][:k]:
            complete = complete and x["complete"]
            if x["best"] is not None and (val is None or x["best"] < val - 1e-12):
                val, phi = x["best"], x["best_phi"]
        if len(r["rows"]) < k:
            complete = False
        return val, phi, complete

    head = "| `n` | lower bound, every algorithm | base bracket alone (not adaptive) | " + " | ".join(
        f"{k + 1} levels" for k in range(1, kmax + 1)) + " | levels after which nothing improves |"
    lines = [head, "|---|---|---|" + "---|" * kmax + "---|"]
    sat = {}
    excess = {}
    for n in sizes:
        cells = []
        final = {}
        for k in range(1, kmax + 1):
            parts = []
            for fam in ("theory", "wide"):
                r = by.get((n, fam))
                if r is None:
                    parts.append("…")
                    continue
                v, phi, complete = best(r, k)
                final[(fam, k)] = (v, complete)
                parts.append((f"{v:.4f}" if v is not None else "—") + ("" if complete else "*"))
            cells.append(parts[0] if parts[0] == parts[1] else f"{parts[0]} / {parts[1]}")
        r0 = by.get((n, "theory")) or by.get((n, "wide"))
        # saturation: the least k after which no family improves by more than 1e-4 (only where the rows are complete)
        vals = [min((final[(fam, k)][0] for fam in ("theory", "wide") if (fam, k) in final and final[(fam, k)][0] is not None), default=None)
                for k in range(1, kmax + 1)]
        done = [all(final.get((fam, k), (None, False))[1] for fam in ("theory", "wide")) for k in range(1, kmax + 1)]
        ksat = None
        for k in range(1, kmax + 1):
            if all(done[:kmax]) and all(vals[j] is not None and vals[j] > vals[kmax - 1] - 1e-4 for j in range(k - 1, kmax)):
                ksat = k
                break
        sat[n] = ksat
        vbest = min(v for v in vals if v is not None)
        na = n * r0["a"]
        excess[n] = ((vbest - r0["lower_bound"]) * na, vbest / r0["lower_bound"], vbest, all(done))
        lines.append(f"| {n} | {r0['lower_bound']:.4f} | {r0['base_bracket']:.4f} | " + " | ".join(cells) + f" | {('%d' % (ksat + 1)) if ksat else 'not determined (unfinished)'} |")
    blocks = {"x011_bounds": "\n".join(lines)}
    r0 = rows[0]
    blocks["x011_bounds_caption"] = (
        f"`ln(bound)/(n a)`, `u = 1` (`a = {r0['a']:.5f}`; the exponent of every algorithm is `h/a = {r0['h_over_a']:.4f}` in these units, enumeration costs "
        f"`{r0['enumeration']:.3f}`).  \"`k` levels\" = `k − 1` nested runs of Algorithm 2L⁺ above base brackets, every server chosen by certified cost; "
        "the least bound over 18 outer fractions of the top level.  Where two numbers are given: candidate family \"theory\" / family \"wide\".  "
        "An asterisk: the search did not finish within its time limit — the number is the best bound found, an upper bound of the minimum over the family.")
    lines = ["| `n` | best certified bound | lower bound | ratio | excess in nats | excess / `√(n ln n)` |", "|---|---|---|---|---|---|"]
    for n in sizes:
        ex, ratio, vbest, complete = excess[n]
        r0 = by.get((n, "theory")) or by.get((n, "wide"))
        lines.append(f"| {n} | {vbest:.4f}{'' if complete else '*'} | {r0['lower_bound']:.4f} | {ratio:.2f} | {ex:.0f} | {ex / math.sqrt(n * math.log(n)):.2f} |")
    blocks["x011_excess"] = "\n".join(lines)
    return blocks


# ---------------------------------------------------------------------------------------------
# X-011b: the designs run on instances
# ---------------------------------------------------------------------------------------------
def referee_numbers() -> dict:
    """The flat-tuned designs of X-010 (ENG-RES-0014, table three_worst), minimised over the outer fraction:
    n -> dict(flat2, B2, A2, flat3, B3, A3)."""
    rows = jl("x010_three_levels.jsonl")
    if not rows:
        return {}
    two_flat = {(r["n"], r["phi"]): r["worst2_flat_fibres"] for r in jl("x010_two_levels_flat_fibres.jsonl")}

    def best_by_cell(rs):
        out = {}
        for r in rs:
            k = (r["n"], r["phi"])
            if k not in out or r["worst3_cone_fibres"] > out[k]:
                out[k] = r["worst3_cone_fibres"]
        return out
    cone = jl("x010_three_levels_cone.jsonl")
    k0_3 = best_by_cell([r for r in cone if r["oracle"] == "k0"])
    any_3 = best_by_cell([r for r in cone if r["oracle"] != "k0"])
    k0_2 = best_by_cell(jl("x010_two_levels_cone.jsonl"))
    out = defaultdict(lambda: defaultdict(list))
    for r in rows:
        k = (r["n"], r["phi"])
        d = out[r["n"]]
        d["flat2"].append(r["flat2"])
        d["flat3"].append(r["flat3"])
        b2 = [v for v in (two_flat.get(k), k0_2.get(k)) if v is not None]
        if b2:
            d["B2"].append(max(b2))
        d["A2"].append(r["worst2"])
        b3 = max([r["worst3_flat_fibres"]] + ([k0_3[k]] if k in k0_3 else []))
        d["B3"].append(b3)
        if k in any_3:
            d["A3"].append(max(b3, any_3[k]))
    return {n: {key: min(v) for key, v in d.items()} for n, d in out.items()}


def runs_blocks() -> dict[str, str]:
    rows = jl("x011_instances1.jsonl")
    if not rows:
        return {}
    blocks = {}
    ref = referee_numbers()
    cells = defaultdict(list)
    for r in rows:
        cells[(r["n"], r["nested_levels"])].append(r)

    def Bp(r):          # reading (B) as in ENG-RES-0014: the algorithm as built on flat or cone fibres
        return max(r["worst_flat_fibres"], r["worst_B"]) if "worst_flat_fibres" in r else r["worst_B"]

    def Ap(r):          # reading (A): also with base brackets placed at an end of their promise
        return max(Bp(r), r["worst_A"])

    # cone fibres of intermediate slope, run for the selected designs only (X-011e)
    extra = defaultdict(dict)
    for r in jl("x011_fibre_slopes.jsonl"):
        extra[(r["n"], r["nested_levels"], r["phi"])][r["slope"]] = r
    lines = ["| `n` | levels | selected design: certified bound (outer fraction) | flat instance | worst outer landscape found with flat fibres | with cone fibres of slope "
             "`¼u` / `½u` / `¾u` / `u`, base brackets' own answers | (A): base brackets at an end of their promise | largest of these |", "|---|---|---|---|---|---|---|---|"]
    selected = {}
    for (n, k) in sorted(cells):
        if n not in (1000, 4000, 16000):
            continue
        sel = min(cells[(n, k)], key=lambda r: r["certified"])
        ex = extra.get((n, k, sel["phi"]), {})
        cones = [ex[s]["worst_B"] if s in ex else None for s in (0.25, 0.5, 0.75)] + [sel["worst_B"]]
        a_all = max([sel["worst_A"]] + [ex[s]["worst_A"] for s in ex])
        b_all = max([sel["worst_flat_fibres"]] + [c for c in cones if c is not None])
        selected[(n, k)] = dict(sel=sel, B=b_all, A=max(a_all, b_all), slopes=len(ex))
        lines.append(f"| {n} | {k + 1} | {sel['certified']:.4f} ({sel['phi']:g}) | {sel['flat_instance']:.4f} | {sel['worst_flat_fibres']:.4f} | "
                     + " / ".join("—" if c is None else f"{c:.4f}" for c in cones) + f" | {a_all:.4f} | {max(a_all, b_all):.4f} |")
    blocks["x011_runs"] = "\n".join(lines)
    lines = ["| `n` | levels | servers by certified cost, least over ten fractions: (B) | (A) | servers chosen at the flat fibre (ENG-RES-0014), least over its fractions: flat instance | (B) | (A) |",
             "|---|---|---|---|---|---|---|"]
    h4 = []
    for (n, k) in sorted(cells):
        if n not in (1000, 4000, 16000) or k > 2:
            continue
        rs = cells[(n, k)]
        minB = min(rs, key=Bp)
        minA = min(rs, key=Ap)
        rf = ref.get(n, {})
        key = {1: "2", 2: "3"}[k]
        fl, fb, fa = rf.get(f"flat{key}"), rf.get(f"B{key}"), rf.get(f"A{key}")
        lines.append(f"| {n} | {k + 1} | {Bp(minB):.4f} ({minB['phi']:g}) | {Ap(minA):.4f} ({minA['phi']:g}) | {f4(fl)} | {f4(fb)} | {f4(fa)} |")
        if k == 2 and n in (4000, 16000):
            s = selected[(n, k)]
            h4.append((n, Bp(minB), Ap(minA), fb, fa, s["sel"]["flat_instance"], fl, s["B"], s["A"], s["slopes"]))
    blocks["x011_runs_min"] = "\n".join(lines)
    parts = []
    for n, b, a_, fb, fa, flat_sel, fl, sb, sa, ns in h4:
        parts.append(f"`n = {n}`: least worst instance found `{b:.4f}` (B), `{a_:.4f}` (A) for servers chosen by certified cost, against `{f4(fb)}` (B)"
                     + (f", `{f4(fa)}` (A)" if fa is not None else " (reading (A) was not run for it)") + " for servers chosen at the flat fibre"
                     + (f"; with the {ns} further fibre slopes the selected design reaches `{sb:.4f}` (B), `{sa:.4f}` (A)" if ns else "")
                     + f"; at the flat instance `{flat_sel:.4f}` against `{f4(fl)}`")
    blocks["x011_h4"] = "Three levels, " + "; ".join(parts) + "."
    # tightness of the certificate at the selected design
    lines = ["| `n` | levels | certified bound of the selected design | worst instance found, (A) | bound minus worst found | worst found / flat instance: (B), (A) |", "|---|---|---|---|---|---|"]
    for (n, k) in sorted(cells):
        rs = [r for r in cells[(n, k)] if "worst_A" in r]
        if not rs:
            continue
        sel = min(rs, key=lambda r: r["certified"])
        worst = Ap(sel) if "worst_flat_fibres" in sel else max(sel["worst_B"], sel["worst_A"])
        wb = Bp(sel)
        if (n, k) in selected:
            worst, wb = selected[(n, k)]["A"], selected[(n, k)]["B"]
        lines.append(f"| {n} | {k + 1} | {sel['certified']:.4f} ({sel['phi']:g}) | {worst:.4f} | {sel['certified'] - worst:.4f} | "
                     f"{wb / sel['flat_instance']:.3f}, {worst / sel['flat_instance']:.3f} |")
    blocks["x011_tightness"] = "\n".join(lines)
    # consistency (H5) and the reversal
    n_search = sum(len(r["searches"]) for r in rows)
    viol = sum(s["violations"] for r in rows for s in r["searches"])
    not_ok = sum(1 for r in rows for s in r["searches"] if not s["servers_ok"])
    above = sum(1 for r in rows for key in ("worst_flat_fibres", "worst_B", "worst_A") if key in r and r[key] > r["certified"] + 1e-9)
    gap = [(r["certified"] - max(r.get(key, -1) for key in ("worst_flat_fibres", "worst_B", "worst_A")), r) for r in rows]
    gmin = min(gap, key=lambda t: t[0])
    blocks["x011_consistency"] = (
        f"{len(rows)} designs run, {n_search} searches, {sum(s['n_eval'] for r in rows for s in r['searches']):,} mean runs: {above} searched costs above the certified bound "
        f"of their design; {viol} runs with a violated claim of Theorem 11.56; {not_ok} searches with a nested run that did not close on its fibre.  The smallest distance "
        f"between a bound and the worst instance found is `{gmin[0]:.4f}` (`n = {gmin[1]['n']}`, {gmin[1]['nested_levels'] + 1} levels, outer fraction `{gmin[1]['phi']:g}`).")
    below = [r for r in rows if r["nested_levels"] >= 2 and r["levels_used"] >= 2 and r["worst_B"] < r["flat_instance"] - 1e-9]
    nested = [r for r in rows if r["nested_levels"] >= 2 and r["levels_used"] >= 2]
    two = [r for r in rows if r["levels_used"] == 1 and "worst_flat_fibres" in r]
    below2 = [r for r in two if r["worst_B"] < r["flat_instance"] - 1e-9]
    if nested:
        worst = min(below, key=lambda r: r["worst_B"] - r["flat_instance"]) if below else None
        blocks["x011_reversal"] = (
            f"Of the {len(nested)} designs with at least one nested run, {len(below)} cost **less on cone fibres than at the flat instance** whatever outer landscape the "
            f"search tried (largest difference `{(worst['flat_instance'] - worst['worst_B']):.4f}` at `n = {worst['n']}`, {worst['nested_levels'] + 1} levels, outer fraction "
            f"`{worst['phi']:g}`: flat instance `{worst['flat_instance']:.4f}`, worst found with cone fibres `{worst['worst_B']:.4f}`); of the {len(two)} two-level designs, "
            f"{len(below2)}." if below else f"None of the {len(nested)} designs with a nested run costs less on cone fibres than at the flat instance.")
    # R16-THY-1(b)
    lines = ["| `n` | outer fraction | certified bound of two levels | flat instance | worst instance found, cone fibres with the base brackets' own answers | any fibre, base brackets at an end of their promise |",
             "|---|---|---|---|---|---|"]
    r16 = []
    for n in (8000, 32000, 64000):
        rs = sorted(cells.get((n, 1), []), key=lambda r: -r["phi"])
        for r in rs:
            lines.append(f"| {n} | {r['phi']:g} | {r['certified']:.4f} | {r['flat_instance']:.4f} | {r['worst_B']:.4f} | {r['worst_A']:.4f} |")
        if rs:
            b = min(rs, key=lambda r: r["worst_B"])
            a_ = min(rs, key=lambda r: r["worst_A"])
            r16.append((n, len(rs), b["worst_B"], b["phi"], a_["worst_A"], a_["phi"]))
    if r16:
        blocks["x011_r16"] = "\n".join(lines)
        blocks["x011_r16_summary"] = "; ".join(
            f"`n = {n}` ({cnt} of 6 fractions): `{b:.4f}` at `{pb:g}` with the base brackets' own answers, `{a_:.4f}` at `{pa:g}` with any valid placement"
            for n, cnt, b, pb, a_, pa in r16) + "."
    return blocks


# ---------------------------------------------------------------------------------------------
# X-011c: designs against global cones
# ---------------------------------------------------------------------------------------------
def cone_blocks() -> dict[str, str]:
    p = RESULTS / "x011_portfolio.json"
    if not p.exists():
        return {}
    data = json.loads(p.read_text())
    blocks = {}
    lines = ["| `n` | designs | at the flat instance: least cost | on the worst cone, the best single design (min–max) | which, and its worst slope | "
             "worst cone for a portfolio (max–min), and its slope | cost of dovetailing, `ln(4·designs)/(n a)` |", "|---|---|---|---|---|---|---|"]
    for m in data:
        for name in ("flat-tuned only", "certified, three levels", "certified only", "all designs"):
            g = m["games"][name]
            label = {"flat-tuned only": "three levels, servers chosen at the flat fibre", "certified, three levels": "three levels, servers by certified cost",
                     "certified only": "two to four levels, by certified cost", "all designs": "all of these"}[name]
            lines.append(f"| {m['n']} | {label} ({g['designs']}) | {g['best_at_flat']:.4f} | {g['minmax']:.4f} | {g['minmax_design'].split(',')[-1].strip()}"
                         f"{', ' + g['minmax_design'].split(',')[1].strip() if name != 'flat-tuned only' and name != 'certified, three levels' else ''}; slope {g['minmax_slope']:g} | "
                         f"{g['maxmin']:.4f} at slope {g['maxmin_slope']:g} | {g['dovetail_overhead']:.4f} |")
    blocks["x011_cones"] = "\n".join(lines)
    lines = ["| `n` | rule | " + " | ".join(f"slope {s:g}" for s in data[0]["slopes"]) + " |", "|---|---|" + "---|" * len(data[0]["slopes"])]
    for m in data:
        for rule, k, label in (("flat", 2, "chosen at the flat fibre"), ("certified", 2, "by certified cost")):
            idx = [r for r in m["rows"] if r["rule"] == rule and r["nested_levels"] == k]
            env = [min(r["cost"][i] for r in idx) for i in range(len(m["slopes"]))]
            lines.append(f"| {m['n']} | {label} | " + " | ".join(f"{v:.3f}" for v in env) + " |")
    blocks["x011_cone_profiles"] = "\n".join(lines)
    ok = all(all(r["ok"]) for m in data for r in m["rows"])
    blocks["x011_cones_caption"] = (
        f"Global cones `ψ(x) = s·u·|x|`, `u = 1`; mean-run model; base brackets give their own answers; {len(data[0]['rows'])} designs per size "
        f"(14 outer fractions; flat-tuned three levels, and two, three and four levels by certified cost in the family \"theory\"); "
        f"{'every run closed with no violated claim' if ok else 'SOME RUNS DID NOT CLOSE'}.")
    return blocks


# ---------------------------------------------------------------------------------------------
# X-014: site-dependent slopes
# ---------------------------------------------------------------------------------------------
def hetero_blocks() -> dict[str, str]:
    rows = jl("x014_hetero1.jsonl") or jl("x014_hetero.jsonl")
    blocks = {}
    if rows:
        def best(r, key, k):
            vals = [x[key] for x in r["rows"][:k] if x.get(key) is not None]
            return min(vals) if vals else None
        lines = ["| `(u_H, u_L)` | heavy sites | `n` | exponent `h` (asymptotic) | lower bound at this `n` | homogeneous algorithm with `u_H`: 2 / 3 / 4 levels | "
                 "type-aligned nesting: 2 / 3 / 4 levels | top outer block of the best design | aligned / homogeneous | aligned / lower bound |", "|---|---|---|---|---|---|---|---|---|---|"]
        stats = dict(cells=0, h1_fail=[], ratio16=[], nonadd=[], lb_excess=defaultdict(dict), incomplete=0)
        for r in sorted(rows, key=lambda r: (-r["uH"], -r["uL"], r["frac"], r["n"])):
            hom = [best(r, "homogeneous", k) for k in (1, 2, 3)]
            ali = [best(r, "type_aligned", k) for k in (1, 2, 3)]
            done = all(x["complete"] for x in r["rows"]) and len(r["rows"]) == 3
            stats["cells"] += 1
            stats["incomplete"] += not done
            tree = next((x["tree"] for x in reversed(r["rows"]) if x.get("tree")), None)
            asy = r["asymptotic"]
            lines.append(f"| ({r['uH']:g}, {r['uL']:g}) | {r['frac']:g} | {r['n']} | {asy['h']:.5f} | {r['lower_bound']:.5f} | "
                         + " / ".join(f4(v)[:7] if v is None else f"{v:.4f}" for v in hom) + " | " + " / ".join("—" if v is None else f"{v:.4f}" for v in ali)
                         + f" | {(str(tree['outer_sites']) + ' sites of slope ' + format(tree['outer_slope'], 'g')) if tree else '—'} | "
                         + (f"{ali[2] / hom[2]:.2f}" if ali[2] and hom[2] else "—") + " | " + (f"{ali[2] / r['lower_bound']:.2f}" if ali[2] else "—") + (" |" if done else "* |"))
            for k in (2, 3):
                if ali[k - 1] is not None and hom[k - 1] is not None and ali[k - 1] > hom[k - 1] + 1e-12:
                    stats["h1_fail"].append((r["uH"], r["uL"], r["frac"], r["n"], k + 1, ali[k - 1], hom[k - 1]))
            if r["n"] == 16000 and ali[2]:
                stats["ratio16"].append(ali[2] / r["lower_bound"])
            stats["nonadd"].append(abs(asy["h_average"] - asy["h"]) / asy["h"])
            stats["lb_excess"][(r["uH"], r["uL"], r["frac"])][r["n"]] = r["lower_bound"] - asy["h"]
        blocks["x014_table"] = "\n".join(lines)
        mono = sum(1 for d in stats["lb_excess"].values() if len(d) >= 2 and all(d[a_] > d[b] > 0 for a_, b in zip(sorted(d), sorted(d)[1:])))
        full = sum(1 for d in stats["lb_excess"].values() if len(d) >= 2)
        blocks["x014_summary"] = (
            f"{stats['cells']} cells stored ({stats['incomplete']} with a search that reached its time limit, marked *).  "
            f"H1: the type-aligned bound is above the homogeneous one in {len(stats['h1_fail'])} cell-levels"
            + (" (" + "; ".join(f"`({a_:g}, {b:g})`, heavy {f:g}, `n = {n}`, {lv} levels: {x:.4f} against {y:.4f}" for a_, b, f, n, lv, x, y in stats["h1_fail"][:6]) + ")" if stats["h1_fail"] else "")
            + f".  H2: the lower bound exceeds `h` and the excess shrinks with `n` in {mono} of {full} mixtures.  "
            + (f"H3: at `n = 16 000` the ratio of the best type-aligned bound to the lower bound lies between `{min(stats['ratio16']):.2f}` and `{max(stats['ratio16']):.2f}` "
               f"({len(stats['ratio16'])} cells).  " if stats["ratio16"] else "H3: no cell at `n = 16 000` is stored yet.  ")
            + f"H4: `h` differs from the average of the one-type exponents by at most `{100 * max(stats['nonadd']):.3f}` per cent.")
    # the maximiser of a single site type, t_j = ln((1 - rho)/rho)/u with rho = Lambda_1(u)/u
    def tstar(u):
        rho = math.log(2 / (1 + math.exp(-u))) / u
        return math.log((1 - rho) / rho) / u
    slopes = (0.25, 0.5, 1.0, 2.0, 4.0)
    blocks["x014_tstar"] = ("| slope `u` | " + " | ".join(f"{u:g}" for u in slopes) + " |\n|---|" + "---|" * len(slopes) + "\n| maximising `t` of a chain of that type alone | "
                            + " | ".join(f"{tstar(u):.3f}" for u in slopes) + " |")
    p = RESULTS / "x014_literal.json"
    if p.exists():
        d = json.loads(p.read_text())
        lines = ["| what | outer block | inner slopes | parameters | runs | closed | bracket misses the truth | wider than certified | aborted | over the cost bound | false certificate | widest bracket (certified accuracy) |",
                 "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        tot = defaultdict(int)
        for r in d["results"]:
            lines.append(f"| {r['what']} | {r['n_o']} sites of slope {r['u_o']:g} | {', '.join(format(u, 'g') for u in r['inner_slopes'])} | {r['design']['name']} | {r['runs']} | "
                         f"{r['closed']} | {r['invalid']} | {r['too_wide']} | {r['aborted']} | {r['over_budget']} | {r['bad_certificates']} | {r['max_width']:.3f} ({r['x_out']:.3f}) |")
            if r["what"] == "theorem's constants":
                for key in ("runs", "closed", "invalid", "too_wide", "aborted", "over_budget", "bad_certificates"):
                    tot[key] += r[key]
        blocks["x014_literal"] = "\n".join(lines)
        ctrl = [r for r in d["results"] if r["what"] != "theorem's constants"]
        blocks["x014_literal_summary"] = (
            f"With the theorem's constants: {tot['runs']:,} literal runs on cubes of {min(r['n_o'] + len(r['inner_slopes']) for r in d['results'])}–"
            f"{max(r['n_o'] + len(r['inner_slopes']) for r in d['results'])} sites, {tot['closed']:,} closed, {tot['invalid']} brackets that miss the truth, "
            f"{tot['too_wide']} wider than the certified accuracy, {tot['aborted']} aborted, {tot['over_budget']} above the cost bound, {tot['bad_certificates']} false certificates.  "
            f"Negative controls: " + "; ".join(f"{r['what'].replace('negative control: ', '')} ({r['n_o']} outer sites of slope {r['u_o']:g}): {r['invalid']} of {r['runs']} brackets miss the truth, "
                                                f"{r['aborted']} aborted, {r['bad_certificates']} false certificates" for r in ctrl) + ".")
    return blocks


def rung_blocks() -> dict[str, str]:
    p = RESULTS / "x011_rungs.json"
    if not p.exists():
        return {}
    d = json.loads(p.read_text())
    blocks = {}

    def g(v):
        return "—" if v is None else f"{v:.3f}"
    for key, des in zip(("flat", "cert"), d["designs"]):
        flat, cone = des["runs"]
        lines = ["| rung | accuracy | server | its cost: flat fibre / cone fibre / certified | share of the promised width used: flat / cone | "
                 "calls × cost at this rung: flat fibres / cone fibres |", "|---|---|---|---|---|---|"]
        top_f = max((r["term"] for r in flat["rungs"] if r["term"] is not None))
        top_c = max((r["term"] for r in cone["rungs"] if r["term"] is not None))
        for rf, rc in zip(flat["rungs"], cone["rungs"]):
            if rf["l"] % 3 == 1 or rf["l"] >= 36:
                tf = ("**" + g(rf["term"]) + "**") if rf["term"] == top_f else g(rf["term"])
                tc = ("**" + g(rc["term"]) + "**") if rc["term"] == top_c else g(rc["term"])
                lines.append(f"| {rf['l']} | {rf['x']:.3g} | {rf['server']} | {g(rf['cost'])} / {g(rc['cost'])} / {g(rf['certified_cost'])} | "
                             f"{rf['used']:.2f} / {rc['used']:.2f} | {tf} / {tc} |")
        blocks[f"x011_rungs_{key}"] = "\n".join(lines)
        blocks[f"x011_rungs_{key}_caption"] = (
            f"`u = {d['u']:g}`, `n = {d['n']}`, three levels, {des['name']}, outer fraction `{des['phi']:g}`; flat outer landscape; in units of `n a`.  Whole run: "
            f"`{flat['cost']:.4f}` with flat fibres, `{cone['cost']:.4f}` with cone fibres; certified bound `{des['certified']:.4f}`.  "
            "A dash: the rung is not reached.  Bold: the largest term.")
    return blocks


def build() -> dict[str, str]:
    blocks = {}
    for fn in (bounds_blocks, runs_blocks, rung_blocks, cone_blocks, hetero_blocks):
        blocks.update(fn())
    return blocks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", type=Path)
    ap.add_argument("--verify", type=Path)
    args = ap.parse_args()
    blocks = build()
    target = args.write or args.verify
    if target is None:
        for k, v in blocks.items():
            print(f"### {k}\n{v}\n")
        return 0
    text = target.read_text()
    new = text
    for name, body in blocks.items():
        pat = re.compile(rf"(<!-- TABLE:{re.escape(name)} -->\n)(?:.*?\n)?(<!-- /TABLE:{re.escape(name)} -->)", re.S)
        new = pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), new)
    if args.verify:
        print("tables in", target.name, "match the artifacts" if new == text else "DIFFER from the artifacts")
        return 0 if new == text else 1
    target.write_text(new)
    print("updated", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
