"""Tables of experiment X-005 (Algorithm 2L+ on adversarial instances), generated from the stored
results so that no number in a message is typed by hand.

    python experiments/eng/twolevel/make_tables.py                 # print every block
    python experiments/eng/twolevel/make_tables.py --write  docs/collaboration/responses/engineering/ENG-RES-0008.md
    python experiments/eng/twolevel/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0008.md

A block in a document is delimited by ``<!-- TABLE:name -->`` and ``<!-- /TABLE:name -->``.
Inputs: ``results/x005_cost.jsonl``, ``results/x005_claims.jsonl``, ``results/x005_converge.jsonl``
(one JSON object per (u, n, phi) cell, written by ``modal_jobs/twolevel_app.py``).  All costs
are natural logarithms of numbers of evaluations, divided by ``n a`` (a = KL(p_u || 1/2), the
exponent of the plain bracket), as in the theory division's table (K_REPORT §6.4).
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
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE))

import run_search  # noqa: E402
from metricchain_eng.twolevel.alg2l import tau2  # noqa: E402
from metricchain_eng.twolevel.tables import cube_constants  # noqa: E402

RESULTS = HERE / "results"


def load(name: str) -> list[dict]:
    path = RESULTS / f"x005_{name}.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def worst(cell: dict, family: str | None = None, oracle: str | None = None) -> float:
    """Largest ln(cost) found in a cell (searches with objective "cost"), flat instance included."""
    vals = [s["best_value"] for s in cell["searches"] if s["objective"] == "cost"
            and (family is None or s["family"] == family) and (oracle is None or s["oracle"] == oracle)]
    if family is None:
        vals += [cell["flat"][o]["lcost"] for o in cell["flat"] if oracle is None or o == oracle]
    return max(vals)


def flat_cost(cell: dict) -> float:
    return cell["flat"]["bottom"]["lcost"]          # the convention of the theory division's table


def by_un(cells: list[dict]) -> dict:
    out = defaultdict(dict)
    for c in cells:
        out[(c["u"], c["n"])][c["phi"]] = c
    return out


def f3(x: float) -> str:
    return f"{x:.3f}"


def build() -> dict[str, str]:
    blocks: dict[str, str] = {}
    cost = load("cost")
    grid = by_un(cost)
    us = sorted({u for u, _ in grid})
    ref_cache: dict = {}

    def ref(u, n, x_out):
        if (u, n) not in ref_cache:
            ref_cache[(u, n)] = run_search.reference_columns(u, n, x_out)
        return ref_cache[(u, n)]

    # ---- the main table: flat-tuned phi against the worst instance, and the minimax phi --------------------
    summary = {}
    for u in us:
        c = cube_constants(u)
        t2 = tau2(u)[0]
        lines = [f"`u = {u:g}`: `a = {c.a:.5f}`, `τ₂/a = {t2 / c.a:.4f}`, `h/a = {c.h / c.a:.4f}`.", "",
                 "| `n` | plain bracket | flat instance, best `φ` for it | worst instance found at that `φ` | best `φ` against the worst instance | flat instance at that `φ` | cap `C_max` at that `φ` | hinted lower bound |",
                 "|---|---|---|---|---|---|---|---|"]
        for (uu, n) in sorted(grid):
            if uu != u:
                continue
            cells = grid[(uu, n)]
            if len(cells) < len(run_search.PHIS):
                continue
            na = n * c.a
            phi_flat = min(cells, key=lambda p: flat_cost(cells[p]))
            phi_mm = min(cells, key=lambda p: worst(cells[p]))
            cf, cm = cells[phi_flat], cells[phi_mm]
            r = ref(u, n, cf["constants"]["x_out"])
            summary[(u, n)] = dict(claimed_mm=cm["claimed_exponent"] / c.a, sample_mm=max(
                                       s["best_run"]["lM_max"] for s in cm["searches"] if s["objective"] == "cost") / (cm["n_o"] * c.a),
                                   plain=r["plain"] / na, lower=r["lower"] / na, phi_flat=phi_flat, flat=flat_cost(cf) / na,
                                   worst_at_flat=worst(cf) / na, phi_mm=phi_mm, minimax=worst(cm) / na,
                                   flat_at_mm=flat_cost(cm) / na, cap_at_mm=cm["constants"]["lCmax"] / na,
                                   cap_at_flat=cf["constants"]["lCmax"] / na)
            s = summary[(u, n)]
            lines.append(f"| {n} | {f3(s['plain'])} | {f3(s['flat'])} (`φ = {phi_flat:.2f}`) | {f3(s['worst_at_flat'])} | "
                         f"**{f3(s['minimax'])}** (`φ = {phi_mm:.2f}`) | {f3(s['flat_at_mm'])} | {f3(s['cap_at_mm'])} | {f3(s['lower'])} |")
        blocks[f"main_u{u:g}"] = "\n".join(lines)

    # ---- by how much the flat-instance table understates the worst case ----------------------------------
    lines = ["| `u` | `n ≤ 2000`: least … largest ratio | `n = 8000` | `n = 64 000` | `n = 128 000` |", "|---|---|---|---|---|"]
    for u in us:
        rat = {n: summary[(uu, n)]["minimax"] / summary[(uu, n)]["flat"] for (uu, n) in summary if uu == u}
        small = [v for n, v in rat.items() if n <= 2000]
        if small and all(k in rat for k in (8000, 64000, 128000)):
            lines.append(f"| {u:g} | {min(small):.2f} … {max(small):.2f} | {rat[8000]:.2f} | {rat[64000]:.2f} | {rat[128000]:.2f} |")
    blocks["inflation"] = "\n".join(lines)

    # ---- the mechanism: flat instance against the worst one, at the outer fraction tuned for the flat instance ----
    lines = ["| `u` | `n` | `φ` | instance | evaluations `/(n a)` | sample `ln M/(n_o a)` | closing radius (`r†`, `p_u n_o`) | levels left populated / negligible | `ln` of the ratio of the two costs |",
             "|---|---|---|---|---|---|---|---|---|"]
    for u in us:
        cu = cube_constants(u)
        for n in (1000, 8000, 64000):
            cells = grid.get((u, n), {})
            if len(cells) < len(run_search.PHIS):
                continue
            phi = min(cells, key=lambda p: flat_cost(cells[p]))
            c = cells[phi]
            na, noa = n * cu.a, c["n_o"] * cu.a
            fl = c["flat"]["bottom"]
            s = max((s for s in c["searches"] if s["objective"] == "cost"), key=lambda s: s["best_value"])
            w = s["best_run"]
            rr = f"({c['constants']['r_dag']}, {cu.p_u * c['n_o']:.0f})"
            lines.append(f"| {u:g} | {n} | {phi:.2f} | flat | {fl['lcost'] / na:.3f} | {fl['lM_max'] / noa:.3f} | {fl['r_close']} {rr} | {fl['npop']} / {fl['nneg']} | |")
            lines.append(f"| | | | worst found | {w['lcost'] / na:.3f} | {w['lM_max'] / noa:.3f} | {w['r_close']} {rr} | {w['npop']} / {w['nneg']} | {w['lcost'] - fl['lcost']:.1f} |")
    blocks["mechanism"] = "\n".join(lines)

    # ---- crossover with the plain bracket ------------------------------------------------------------------
    lines = ["| `u` | least `n` of the grid with flat-tuned two levels below the plain bracket (flat instance) | the same against the worst instance, `φ` tuned for the flat instance | the same against the worst instance, `φ` tuned against it |",
             "|---|---|---|---|"]
    for u in us:
        ns = sorted(n for (uu, n) in summary if uu == u)

        def first(key):
            ok = [n for n in ns if summary[(u, n)][key] < summary[(u, n)]["plain"]]
            if not ok:
                return "none"
            n0 = ok[0]
            stays = all(summary[(u, n)][key] < summary[(u, n)]["plain"] for n in ns if n >= n0)
            return f"{n0}" + ("" if stays else " (not monotone)")
        lines.append(f"| {u:g} | {first('flat')} | {first('worst_at_flat')} | {first('minimax')} |")
    blocks["crossover"] = "\n".join(lines)

    # ---- distance to the asymptotic claim ------------------------------------------------------------------
    lines = ["| `u` | `n` | best `φ` against the worst instance | worst found `/(n a)` | exponent claimed for this `φ` and ladder, `/a` | difference | difference × `√n` | difference in absolute units (`× a`) | `ln(C_max)/(n a)` minus worst found |",
             "|---|---|---|---|---|---|---|---|---|"]
    for u in us:
        c = cube_constants(u)
        for n in sorted(n for (uu, n) in summary if uu == u):
            s = summary[(u, n)]
            d = s["minimax"] - s["claimed_mm"]
            lines.append(f"| {u:g} | {n} | {s['phi_mm']:.2f} | {f3(s['minimax'])} | {s['claimed_mm']:.4f} | {d:+.3f} | {d * math.sqrt(n):.1f} | {d * c.a:.4f} | {s['cap_at_mm'] - s['minimax']:.3f} |")
    blocks["trend"] = "\n".join(lines)

    # ---- the whole phi-profile at three sizes ---------------------------------------------------------------
    lines = ["| `u` | `n` | quantity | " + " | ".join(f"`φ = {p:.2f}`" for p in run_search.PHIS) + " |", "|---|---|---|" + "---|" * len(run_search.PHIS)]
    for u in us:
        c = cube_constants(u)
        for n in (1000, 8000, 64000):
            cells = grid.get((u, n), {})
            if len(cells) < len(run_search.PHIS):
                continue
            na = n * c.a
            lines.append(f"| {u:g} | {n} | flat | " + " | ".join(f3(flat_cost(cells[p]) / na) for p in run_search.PHIS) + " |")
            lines.append(f"| | | worst found | " + " | ".join(f3(worst(cells[p]) / na) for p in run_search.PHIS) + " |")
            lines.append(f"| | | cap `C_max` | " + " | ".join(f3(cells[p]["constants"]["lCmax"] / na) for p in run_search.PHIS) + " |")
    blocks["phi_profile"] = "\n".join(lines)

    # ---- claims under optimisation pressure ----------------------------------------------------------------
    claims = load("claims")
    conv = load("converge")
    every = cost + claims + conv
    n_eval = sum(s["n_eval"] for c in every for s in c["searches"])
    n_viol = sum(s["n_violations"] for c in every for s in c["searches"])
    not_closed = sum(s["extremes"]["not_closed"] for c in every for s in c["searches"])
    keys = [("cost_over_cap", "`ln(cost) − ln(C_max)`", "≤ 0 (claim (vi): no abort for cost)"),
            ("slack_v", "the count (v): `ln[M_j^neg p(s_j e^{−x})] − ln[(1+η)/(1−η) e^λ ν e^x]`, max over levels and rungs", "≤ 0"),
            ("slack_vi", "claim (vi) per level: `ln[M_j p(s_j e^{−x_{l−1}})] − ln cnt(x_{l−1})`", "≤ 0"),
            ("slack_iv_Mneg", "claim (iv): `ln M_j^neg − ln[(1+η) e^λ ν₀ M†]`", "≤ 0"),
            ("slack_iv_Mbar", "claim (iv): `ln M_j − ln M̄`", "≤ 0"),
            ("slack_iv_M", "claim (iv): `ln M_j − ln max(K, 2 M_j^neg)`", "≤ 0"),
            ("slack_width", "width: `ln(U/L) − x_out`", "≤ 0"),
            ("slack_valid_lower", "validity: `ln L − ln A`", "≤ 0"),
            ("slack_valid_upper", "validity: `ln A − ln U`", "≤ 0"),
            ("margin_iii", "claim (iii): `ln q_j − ln π†` over levels left (minimum)", "> 0")]
    lines = [f"Instances evaluated: **{n_eval:,}** (jobs M-008, M-009, M-010 together); runs that did not close within the level and sample caps: **{not_closed}**; "
             f"runs violating a claim: **{n_viol}**.", "",
             "| quantity | claimed | extreme over all instances, `u = ½` | `u = 1` | `u = 2` |", "|---|---|---|---|---|"]
    for key, label, claim in keys:
        row = []
        for u in (0.5, 1.0, 2.0):
            vals = [s["extremes"][key] for c in every if c["u"] == u for s in c["searches"] if math.isfinite(s["extremes"][key])]
            if not vals:
                row.append("—")
            else:
                v = min(vals) if key == "margin_iii" else max(vals)
                row.append(f"{v:+.1e}" if abs(v) < 5e-4 else f"{v:+.3f}")
        lines.append(f"| {label} | {claim} | " + " | ".join(row) + " |")
    blocks["claims"] = "\n".join(lines)

    def extreme(key, fn=max):
        vals = [s["extremes"][key] for c in every for s in c["searches"] if math.isfinite(s["extremes"][key])]
        return fn(vals)

    if every:
        ok = n_viol == 0 and not_closed == 0
        blocks["headline_counts"] = (f"In {n_eval:,} mean runs every run closed and no claim of Theorem 11.56 was violated." if ok else
                                     f"In {n_eval:,} mean runs {n_viol} violated a claim and {not_closed} did not close.")
        top_v = max(s["extremes"]["slack_v"] for c in every for s in c["searches"] if s["oracle"] == "top")
        bot_v = max(s["extremes"]["slack_v"] for c in every for s in c["searches"] if s["oracle"] == "bottom")
        over_dag = max(s["extremes"]["lM_max"] - c["constants"]["lM_dag"] for c in every for s in c["searches"])
        blocks["closest"] = (f"The closest approaches: the count (v) reaches {100 * math.exp(top_v):.0f} % of its bound under the inner behaviour \"top\" "
                             f"({100 * math.exp(bot_v):.0f} % under \"bottom\"); the number of evaluations stays a factor `e^{{{-extreme('cost_over_cap'):.1f}}}` "
                             f"below `C_max`; the sample never exceeds `{math.exp(over_dag):.1f}·M†`, a factor `e^{{{-extreme('slack_iv_Mbar'):.1f}}}` below the bound `M̄`.")

    # ---- which family, which oracle ------------------------------------------------------------------------
    gain_gen = []
    gain_de = []
    orc_top = 0
    n_cells = 0
    for c in cost:
        na = c["n"] * c["a"]
        mono = worst(c, "monotone")
        gen = worst(c, "general")
        gain_gen.append((gen - mono) / na)
        seeds = max(s["seeds_best"] for s in c["searches"] if s["objective"] == "cost")
        gain_de.append((worst(c) - max(seeds, max(c["flat"][o]["lcost"] for o in c["flat"]))) / na)
        orc_top += worst(c, oracle="top") > worst(c, oracle="bottom") + 1e-9
        n_cells += 1
    if n_cells:
        lines = [f"Cells: {n_cells}.",
                 f"* General (non-monotone) profiles against monotone ones: the best general instance exceeds the best monotone one by at most "
                 f"`{max(gain_gen):+.4f}·n a` (largest shortfall `{min(gain_gen):+.4f}·n a`).",
                 f"* Differential evolution against the structured starting points (flat, cones, plateau-then-cone, cone-then-flat): the search improved "
                 f"on the best starting point by at most `{max(gain_de):+.4f}·n a`; in {sum(g < 1e-4 for g in gain_de)} of {n_cells} cells by less than `0.0001·n a`.",
                 f"* The oracle \"top\" gives the larger cost in {orc_top} of {n_cells} cells, \"bottom\" (or a tie) in the others."]
        blocks["families"] = "\n".join(lines)

    # ---- which structured instance is the worst ----------------------------------------------------------
    sp = RESULTS / "x005_seeds.json"
    if sp.exists():
        seeds = json.loads(sp.read_text())
        mm = {(u, n): min(cells, key=lambda p: worst(cells[p])) for (u, n), cells in grid.items() if len(cells) == len(run_search.PHIS)}
        fl = {(u, n): min(cells, key=lambda p: flat_cost(cells[p])) for (u, n), cells in grid.items() if len(cells) == len(run_search.PHIS)}
        types = ["flat", "cone", "cone of slope u/2", "cone then flat", "plateau then cone"]

        def count(rows):
            return {t: sum(r["best_seed"]["type"] == t for r in rows) for t in types}
        all_rows = seeds
        mm_rows = [r for r in seeds if mm.get((r["u"], r["n"])) == r["phi"]]
        fl_rows = [r for r in seeds if fl.get((r["u"], r["n"])) == r["phi"]]
        right = [r for r in seeds if (r["u"], r["n"]) in mm and r["phi"] > mm[(r["u"], r["n"])]]
        left = [r for r in seeds if (r["u"], r["n"]) in mm and r["phi"] < mm[(r["u"], r["n"])]]
        lines = ["| cells | number | " + " | ".join(types) + " | largest gain of the search over the best structured point (`·n a`) |", "|---|---|" + "---|" * (len(types) + 1)]
        for name, rows in (("all", all_rows), ("`φ` below the best `φ` against the worst instance", left), ("at that `φ`", mm_rows),
                           ("`φ` above it", right), ("at the `φ` that is best for the flat instance", fl_rows)):
            cnt = count(rows)
            lines.append(f"| {name} | {len(rows)} | " + " | ".join(str(cnt[t]) for t in types) + f" | {max(r['gain_of_search'] for r in rows):.4f} |")
        blocks["seed_types"] = "\n".join(lines)
        bins = ((0.0, 0.85, "below 0.85"), (0.85, 0.95, "0.85–0.95"), (0.95, 1.05, "0.95–1.05"), (1.05, 1.2, "1.05–1.2"), (1.2, 9.9, "above 1.2"))
        lines = ["| maximiser | cells | radius of the change of slope, in units of the critical radius `Λ₁ n_o / u`: " + " | ".join(b[2] for b in bins) + " |",
                 "|---|---|" + "---|" * len(bins)]
        for t in ("cone then flat", "plateau then cone"):
            rr = [r["best_seed"]["radius_over_critical"] for r in seeds if r["best_seed"]["type"] == t]
            lines.append(f"| {t} | {len(rr)} | " + " | ".join(str(sum(lo <= x < hi for x in rr)) for lo, hi, _ in bins) + " |")
        blocks["seed_radii"] = "\n".join(lines)
        ref = defaultdict(int)
        for r in seeds:
            ref[r["best_seed"]["reference_fraction"]] += 1
        blocks["seed_reference"] = ("Reference point of the best structured instance: at the median distance from the centre in "
                                    f"{ref[0.5]} cells, at the centre in {ref[0.0]}, at the antipode in {ref[1.0]}; inner behaviour \"bottom\" in "
                                    f"{sum(r['best_seed']['oracle'] == 'bottom' for r in seeds)} cells, \"top\" in {sum(r['best_seed']['oracle'] == 'top' for r in seeds)}.")

    # ---- convergence check ---------------------------------------------------------------------------------
    if conv:
        base = {(c["u"], c["n"], c["phi"]): c for c in cost}
        lines = ["| `u` | `n` | `φ` | seed | budget (monotone / general) | worst found `/(n a)` | in job M-008 (seed 1, smaller budget) |", "|---|---|---|---|---|---|---|"]
        for c in sorted(conv, key=lambda c: (c["n"], c["phi"], c["seed"])):
            na = c["n"] * c["a"]
            b = base.get((c["u"], c["n"], c["phi"]))
            lines.append(f"| {c['u']:g} | {c['n']} | {c['phi']:.2f} | {c['seed']} | {c['budget']} / {c['budget_general']} | {worst(c) / na:.4f} | "
                         f"{(worst(b) / na):.4f} |" if b else "—")
        blocks["converge"] = "\n".join(lines)

    # ---- X-006: literal runs with real fluctuations ----------------------------------------------------------
    for xp, pre in ((RESULTS / "x006_sampled.jsonl", "sampled"), (RESULTS / "x006_preview.jsonl", "preview")):
        if not xp.exists():
            continue
        runs6 = [json.loads(line) for line in xp.read_text().splitlines() if line.strip()]
        full = [r for r in runs6 if r["k_scale"] == 1.0]
        n_full = sum(r["runs"] - r["skipped"] for r in full)
        bad_full = sum(r["good_event_failed"] + r["invalid"] + r["width_violations"] + r["claim_violations_on_good_event"] + r["aborted"] for r in full)
        blocks[pre + "_headline"] = (
            f"With the theorem's `K` ({min(r['K'] for r in full)}–{max(r['K'] for r in full)}): **{n_full:,} literal runs** on {len({r['profile'] for r in full})} landscapes, "
            f"three sizes and three inner behaviours; runs in which the good event failed, a bracket was invalid, the width bound was exceeded, a claim "
            f"was violated or the run aborted: **{bad_full}**."
            + (f"  With no failure in {n_full:,} runs, the frequency of each of these events is below `{3.0 / n_full:.1e}` at 95 % confidence (pooled over cases)." if bad_full == 0 and n_full else ""))
        lines = ["| `u` | `n_o` | `K` (scale) | runs | good event failed | bracket invalid | of these on the good event | width bound exceeded | another claim violated on the good event | aborted | mean `ln(evaluations)` minus mean run: bottom / top |",
                 "|---|---|---|---|---|---|---|---|---|---|---|"]
        for (u, n_o) in sorted({(r["u"], r["n_o"]) for r in runs6}):
            for scale in sorted({r["k_scale"] for r in runs6}, reverse=True):
                rows = [r for r in runs6 if r["u"] == u and r["n_o"] == n_o and r["k_scale"] == scale]
                if not rows:
                    continue
                tot = sum(r["runs"] - r["skipped"] for r in rows)

                def diff(orc):
                    v = [r["lqueries_mean"] - r["mean_run_lcost"] for r in rows if r["oracle"] == orc and "lqueries_mean" in r]
                    return f"{sum(v) / len(v):+.2f}" if v else "—"
                dd = f"{diff('bottom')} / {diff('top')}" if scale == 1.0 else "—"     # the mean run uses the theorem's K
                ks = sorted({r["K"] for r in rows})
                lines.append(f"| {u:g} | {n_o} | {ks[0]}" + (f"–{ks[-1]}" if len(ks) > 1 else "") + f" ({'1' if scale == 1 else '1/' + str(round(1 / scale))}) | {tot:,} | "
                             f"{sum(r['good_event_failed'] for r in rows):,} | {sum(r['invalid'] for r in rows):,} | {sum(r['invalid_on_good_event'] for r in rows)} | "
                             f"{sum(r['width_violations'] for r in rows)} | {sum(r['claim_violations_on_good_event'] for r in rows)} | {sum(r['aborted'] for r in rows)} | {dd} |")
        blocks[pre] = "\n".join(lines)
        # landscapes on which the good event fails first
        small = [r for r in runs6 if r["k_scale"] < 1.0]
        if small:
            by_prof = defaultdict(lambda: [0, 0, 0])
            for r in small:
                t = by_prof[r["profile"]]
                t[0] += r["runs"] - r["skipped"]
                t[1] += r["good_event_failed"]
                t[2] += r["invalid"]
            lines = ["| landscape | runs with `K` scaled down | good event failed | bracket invalid |", "|---|---|---|---|"]
            for name, t in sorted(by_prof.items(), key=lambda kv: -kv[1][1] / max(kv[1][0], 1)):
                lines.append(f"| {name} | {t[0]:,} | {t[1]:,} ({100 * t[1] / max(t[0], 1):.0f} %) | {t[2]:,} ({100 * t[2] / max(t[0], 1):.2f} %) |")
            blocks[pre + "_profiles"] = "\n".join(lines)

    # ---- the maximising instances ----------------------------------------------------------------------------
    lines = ["| `u` | `n` | `φ` | family / oracle | cost `/(n a)` | closing | sample `ln M/(n_o a)` | `r` of closure (`r†`, `p_u n_o`) | reference at radius | profile: (from, to, slope/`u`) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for u in us:
        cu = cube_constants(u)
        for n in (1000, 64000):
            cells = grid.get((u, n), {})
            if len(cells) < len(run_search.PHIS):
                continue
            phi_flat = min(cells, key=lambda p: flat_cost(cells[p]))
            phi_mm = min(cells, key=lambda p: worst(cells[p]))
            for phi in sorted({phi_flat, phi_mm}):
                c = cells[phi]
                s = max((s for s in c["searches"] if s["objective"] == "cost"), key=lambda s: s["best_value"])
                run = s["best_run"]
                prof = [(a, b, round(sl, 2)) for a, b, sl in s["profile"] if b - a > 1][:6]
                lines.append(f"| {u:g} | {n} | {phi:.2f} | {s['family']} / {s['oracle']} | {s['best_value'] / (n * c['a']):.3f} | {run['status'].replace('closed-', '')} | "
                             f"{run['lM_max'] / (c['n_o'] * c['a']):.3f} | {run['r_close']} ({c['constants']['r_dag']}, {cu.p_u * c['n_o']:.0f}) | {s['d0']} | `{prof}` |")
    blocks["maximisers"] = "\n".join(lines)
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
