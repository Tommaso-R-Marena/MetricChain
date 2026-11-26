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

import numpy as np
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

    # ---- how fast does the excess decay?  (added after SCI-REV-0008: "about like 1/sqrt(n)" was not what the data show) ----
    lines = ["| `u` | sizes fitted | least-squares slope of `ln(excess)` against `ln n` | local slopes between consecutive sizes (least, largest) | fit `A/√n + B/n`: `A`, `B` | largest relative residual of that fit |",
             "|---|---|---|---|---|---|"]
    slopes_all = []
    for u in us:
        pts = [(n, summary[(u, n)]["minimax"] - summary[(u, n)]["claimed_mm"]) for n in sorted(n for (uu, n) in summary if uu == u)]
        pts = [(n, d) for n, d in pts if d > 0]
        if len(pts) < 4:
            continue
        x = np.log([n for n, _ in pts])
        y = np.log([d for _, d in pts])
        slope = float(np.polyfit(x, y, 1)[0])
        local = [float((y[i + 1] - y[i]) / (x[i + 1] - x[i])) for i in range(len(pts) - 1)]
        M = np.array([[n ** -0.5, 1.0 / n] for n, _ in pts])
        dv = np.array([d for _, d in pts])
        # relative least squares: every size has the same weight
        coef, *_ = np.linalg.lstsq(M / dv[:, None], np.ones(len(pts)), rcond=None)
        res = float(np.max(np.abs(M @ coef / dv - 1)))
        slopes_all.append(slope)
        lines.append(f"| {u:g} | {pts[0][0]}–{pts[-1][0]} ({len(pts)}) | {slope:.2f} | {min(local):.2f}, {max(local):.2f} | {coef[0]:.2f}, {coef[1]:.0f} | {100 * res:.0f} % |")
    blocks["trend_fit"] = "\n".join(lines)
    if slopes_all:
        blocks["trend_fit_summary"] = (f"Fitted over all sizes of the grid, the excess over the claimed exponent decays like `n^(−p)` with `p` between "
                                       f"{-max(slopes_all):.2f} and {-min(slopes_all):.2f} for the three slopes — faster than `1/√n`.")

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
    # ---- the same control at the two largest sizes (job M-013; SCI-REV-0008 R7-ENG-4) --------------------------
    c2p = RESULTS / "x005_converge2.jsonl"
    conv2 = [json.loads(line) for line in c2p.read_text().splitlines() if line.strip()] if c2p.exists() else []
    if conv2:
        base = {(c["u"], c["n"], c["phi"]): c for c in cost}
        lines = ["| `u` | `n` | `φ` | seed | budget (monotone / general) | worst found `/(n a)` | in job M-008 (seed 1, budget) | change `·(n a)` | change in absolute exponent units (`× a`) | claims violated |",
                 "|---|---|---|---|---|---|---|---|---|---|"]
        changes = []
        for c in sorted(conv2, key=lambda c: (c["u"], c["n"], c["seed"])):
            na = c["n"] * c["a"]
            b = base[(c["u"], c["n"], c["phi"])]
            ch = (worst(c) - worst(b)) / na
            changes.append((ch, ch * c["a"], c))
            lines.append(f"| {c['u']:g} | {c['n']} | {c['phi']:.2f} | {c['seed']} | {c['budget']} / {c['budget_general']} | {worst(c) / na:.5f} | {worst(b) / na:.5f} ({b['budget']} / {b['budget_general']}) | "
                         f"{ch:+.5f} | {ch * c['a']:+.6f} | {sum(s['n_violations'] for s in c['searches'])} |")
        blocks["converge2"] = "\n".join(lines)
        up = max(changes, key=lambda t: t[0])
        blocks["converge2_summary"] = (
            f"{len(conv2)} of 12 tasks of the control at the two largest sizes are stored.  With three times the budget and two other seeds the worst instance found changes by "
            f"between `{min(t[0] for t in changes):+.5f}` and `{up[0]:+.5f}` in units of `n a` — at most `{max(abs(t[1]) for t in changes):.6f}` in the exponent itself, against the "
            f"`0.01` of the request's rule; the largest increase is at `u = {up[2]['u']:g}`, `n = {up[2]['n']}`, seed {up[2]['seed']}.  Claims of Theorem 11.56 violated in these searches: "
            f"{sum(s['n_violations'] for c in conv2 for s in c['searches'])}.")

    # ---- X-006: literal runs with real fluctuations ----------------------------------------------------------
    for xp, pre in ((RESULTS / "x006_sampled.jsonl", "sampled"), (RESULTS / "x006_preview.jsonl", "preview"), (RESULTS / "x006b_sampled.jsonl", "sampledb")):
        if not xp.exists():
            continue
        # the invalid inner behaviour "dear" (X-006b) is reported in its own block: validity means nothing there
        runs6 = [r for r in (json.loads(line) for line in xp.read_text().splitlines() if line.strip()) if r["oracle"] != "dear"]
        full = [r for r in runs6 if r["k_scale"] == 1.0]
        if not full:
            continue
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
        # worst case per value of K
        lines = ["| `K` scale | cases | runs per case | largest fraction of runs with the good event failed (landscape, inner behaviour, `u`) | largest fraction of runs with an invalid bracket (landscape, inner behaviour, `u`) | cases with at least one invalid bracket |",
                 "|---|---|---|---|---|---|"]
        for scale in sorted({r["k_scale"] for r in runs6}, reverse=True):
            rows = [r for r in runs6 if r["k_scale"] == scale]
            g = max(rows, key=lambda r: r["good_event_failed"] / r["runs"])
            v = max(rows, key=lambda r: r["invalid"] / r["runs"])

            def tag(r, key):
                f = r[key] / r["runs"]
                return f"{100 * f:.1f} % ({r['profile']}, {r['oracle']}, {r['u']:g})" if r[key] else "0"
            lines.append(f"| {'1' if scale == 1 else '1/' + str(round(1 / scale))} | {len(rows)} | {rows[0]['runs']:,} | {tag(g, 'good_event_failed')} | {tag(v, 'invalid')} | "
                         f"{sum(r['invalid'] > 0 for r in rows)} |")
        blocks[pre + "_worst"] = "\n".join(lines)
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

    blocks.update(x006b_blocks())

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


def _scale(s: float) -> str:
    return "1" if s == 1 else "1/" + str(round(1 / s))


def x010_blocks() -> dict[str, str]:
    """X-010 (three levels), X-005b (instances that are not products), the recheck of the classification rule."""
    blocks: dict[str, str] = {}
    fp = RESULTS / "x010_three_levels_flat.json"
    if fp.exists():
        d = json.loads(fp.read_text())
        rows = d["rows"]
        lines = ["| `n` | `φ₁` | two levels: here (referee) | three levels: here (referee) | `C_max` of three levels with flat middle costs: here (referee) | rungs served by the middle level: here (referee) | width of the returned bracket |",
                 "|---|---|---|---|---|---|---|"]
        same = tot = 0
        for r in sorted(rows, key=lambda r: (r["n"], r["phi"])):
            ref = r["referee"]
            mine = (round(r["two"], 4), round(r["three"], 4), round(r["cmax3"], 4))
            same += sum(abs(m - t) < 5e-5 for m, t in zip(mine, ref[:3])) + int(r["served"] == ref[3])
            tot += 4
            lines.append(f"| {r['n']} | {r['phi']:.2f} | {r['two']:.4f} ({ref[0]:.4f}) | {r['three']:.4f} ({ref[1]:.4f}) | {r['cmax3']:.4f} ({ref[2]:.4f}) | {r['served']} ({ref[3]}) | {r['width']:.3f} |")
        blocks["three_flat"] = "\n".join(lines)
        blocks["three_flat_summary"] = (f"{same} of {tot} published numbers of the referee's three-level table (`u = 1`; {len(rows)} rows: two levels, three levels, "
                                        f"the cost bound, the number of rungs served by the middle level) are reproduced to the digit given; "
                                        f"the longest row takes {max(r['seconds'] for r in rows):.0f} s here.")
    wp = RESULTS / "x010_three_levels.jsonl"
    rows = [json.loads(line) for line in wp.read_text().splitlines() if line.strip()] if wp.exists() else []
    if rows:
        def load(name):
            pth = RESULTS / name
            return [json.loads(line) for line in pth.read_text().splitlines() if line.strip()] if pth.exists() else []
        two_flat = {(r["n"], r["phi"]): r["worst2_flat_fibres"] for r in load("x010_two_levels_flat_fibres.jsonl")}
        cone_rows = load("x010_three_levels_cone.jsonl")
        cone = {}
        for r in cone_rows:
            k = (r["n"], r["phi"])
            if k not in cone or r["worst3_cone_fibres"] > cone[k]["worst3_cone_fibres"]:
                cone[k] = r
        n_variants = len({(r["slope"], r["oracle"]) for r in cone_rows})

        def real3(r):                                         # the largest cost of three levels found on a real instance
            k = (r["n"], r["phi"])
            return max(r["worst3_flat_fibres"], cone[k]["worst3_cone_fibres"]) if k in cone else r["worst3_flat_fibres"]

        def fmt(v):
            return "—" if v is None else f"{v:.4f}"
        lines = ["| `n` | `φ₁` | two levels: flat | two levels, (B): worst outer landscape, flat fibres | two levels, (A): worst found | three levels: flat | "
                 "three levels, (B): worst outer landscape, flat fibres | three levels, (A): the largest of the six runs with cone fibres (slope of the cone, placement by the base brackets) | "
                 "three levels: middle level charged its cost bound | certified `C_max` of three levels |",
                 "|---|---|---|---|---|---|---|---|---|---|"]
        for r in sorted(rows, key=lambda r: (r["n"], r["phi"])):
            k = (r["n"], r["phi"])
            c = cone.get(k)
            lines.append(f"| {r['n']} | {r['phi']:.2f} | {r['flat2']:.4f} | {fmt(two_flat.get(k))} | {r['worst2']:.4f} | {r['flat3']:.4f} | {r['worst3_flat_fibres']:.4f} | "
                         + (f"{c['worst3_cone_fibres']:.4f} ({c['slope']:g}`u`, {c['oracle']})" if c else "—")
                         + f" | {r['worst3_capped_middle']:.4f} | {r['cmax3_certified']:.4f} |")
        blocks["three_worst"] = "\n".join(lines)
        lines = ["| `n` | two levels: flat | two levels, (B) | two levels, (A) | three levels: flat | three levels, (B) | **three levels, (A)** | "
                 "three levels: middle level charged its cost bound | certified `C_max` of three levels | hinted lower bound |",
                 "|---|---|---|---|---|---|---|---|---|---|"]
        summ = []
        for n in sorted({r["n"] for r in rows}):
            rs = [r for r in rows if r["n"] == n]

            def best(f):
                r = min(rs, key=f)
                return f(r), r["phi"]

            def cell(f):
                v, ph = best(f)
                return f"{v:.4f} ({ph:.2f})"
            have2 = all((r["n"], r["phi"]) in two_flat for r in rs)
            lines.append(f"| {n} | {cell(lambda r: r['flat2'])} | " + (cell(lambda r: two_flat[(r['n'], r['phi'])]) if have2 else "—") + f" | {cell(lambda r: r['worst2'])} | "
                         f"{cell(lambda r: r['flat3'])} | {cell(lambda r: r['worst3_flat_fibres'])} | **{cell(real3)}** | {cell(lambda r: r['worst3_capped_middle'])} | "
                         f"{cell(lambda r: r['cmax3_certified'])} | {rs[0]['lower']:.4f} |")
            summ.append((n, best(lambda r: r["flat2"])[0], best(lambda r: r["worst2"])[0], best(lambda r: r["flat3"])[0], best(real3)[0],
                         best(lambda r: r["worst3_capped_middle"])[0], sum((r["n"], r["phi"]) in cone for r in rs), len(rs),
                         best(lambda r: two_flat[(r["n"], r["phi"])])[0] if have2 else None, best(lambda r: r["worst3_flat_fibres"])[0]))
        blocks["three_worst_best"] = "\n".join(lines)
        lines = ["| `n` | three levels over two levels at the flat instance | the same under (B) | the same under (A) | flat → worst, two levels: (B), (A) | "
                 "flat → worst, three levels: (B), (A) | three levels with the middle level at its bound over two levels (A) |", "|---|---|---|---|---|---|---|"]
        for (n, f2, w2, f3, w3, cap, nc, nt, w2b, w3b) in summ:
            lines.append(f"| {n} | {f3 / f2:.2f} | " + (f"{w3b / w2b:.2f}" if w2b else "—") + f" | {w3 / w2:.2f}" + ("" if nc == nt else f" (cone fibres in {nc} of {nt} cells)")
                         + " | " + (f"{w2b / f2:.2f}" if w2b else "—") + f", {w2 / f2:.2f} | {w3b / f3:.2f}, {w3 / f3:.2f} | {cap / w2:.2f} |")
        blocks["three_worst_ratios"] = "\n".join(lines)
        nviol = sum(s["violations"] for r in rows for s in r["searches"])
        nsearch = sum(len(r["searches"]) for r in rows)
        neval = sum(s["n_eval"] for r in rows for s in r["searches"]) + sum(r["n_eval"] for r in cone_rows) + sum(r["n_eval"] for r in load("x010_two_levels_flat_fibres.jsonl"))
        blocks["three_worst_summary"] = (
            f"{len(rows)} cells; {nsearch + 2 * len(cone_rows) + 2 * len(two_flat):,} searches, {neval:,} mean runs of the outer level; searches in which a claim of Theorem 11.56 was "
            f"violated by the outer run: {nviol + sum(r['outer_violations'] for r in cone_rows)}.  Cone fibres: {len(cone_rows)} runs ({n_variants} combinations of slope and inner behaviour "
            f"per cell); middle-level runs on a cone that did not close or violated a claim: {sum(r['middle_runs_not_closed_or_violating'] for r in cone_rows)}; the largest ratio of a "
            f"middle run's cost on a cone to its cost on the flat fibre at the same rung: `e^{{{max((r['largest_middle_cost_ratio'] for r in cone_rows), default=0.0):.1f}}}`."
            if cone_rows else
            f"{len(rows)} cells, {nsearch} searches, {neval:,} mean runs; searches in which a claim of Theorem 11.56 was violated by the outer run: {nviol}.")
        if cone_rows:
            lines = ["| `n` | slope of the cone fibres | inner behaviour of the base brackets | cells in which this combination gives the largest three-level cost among the cone runs | "
                     "largest excess over the flat-fibre run of the same cell (units of `n a`) |", "|---|---|---|---|---|"]
            base = {(r["n"], r["phi"]): r["worst3_flat_fibres"] for r in rows}
            for n in sorted({r["n"] for r in cone_rows}):
                for (sl, orc) in sorted({(r["slope"], r["oracle"]) for r in cone_rows}):
                    rs = [r for r in cone_rows if r["n"] == n and r["slope"] == sl and r["oracle"] == orc]
                    wins = sum(cone[(r["n"], r["phi"])] is r for r in rs)
                    lines.append(f"| {n} | {sl:g}`u` | {orc} | {wins} of {len(rs)} | `{max(r['worst3_cone_fibres'] - base[(r['n'], r['phi'])] for r in rs):+.4f}` |")
            blocks["three_cone"] = "\n".join(lines)
    npth = RESULTS / "x005_nonproduct_bound.json"
    if npth.exists():
        d = json.loads(npth.read_text())
        lines = ["| `u` | cells | largest increase of a cell's worst cost when every fibre may sit anywhere in its trivial bracket (`ln`; in units of `n a`) | "
                 "largest gap of that bound over the product cost at a single stored instance (`ln`; in units of `n a`) |", "|---|---|---|---|"]
        for u in sorted(d["by_u"], key=float):
            b = d["by_u"][u]
            inc = b["worst_increase_at"]["increase"] if b["worst_increase_at"] else 0.0
            lines.append(f"| {u} | {b['cells']} | `{inc:.1e}`; `{b['max_worst_increase_over_na']:.1e}` | `{b['max_gap']:.2g}`; `{b['max_gap_over_na']:.2g}` |")
        blocks["nonproduct"] = "\n".join(lines)
        blocks["nonproduct_summary"] = (f"{len(d['cells'])} cells of job M-008, the stored maximisers of {len(d['cells']) * 4:,} searches: with the refinement windows replaced by their "
                                        f"union over all feasible places of a fibre, the largest increase of a cell's worst cost is "
                                        f"`{max((b['worst_increase_at']['increase'] if b['worst_increase_at'] else 0.0) for b in d['by_u'].values()):.1e}` in the logarithm; "
                                        f"bounds above `C_max`: {d['above_Cmax']}.")
    rp = RESULTS / "x005_recheck_classification.json"
    if rp.exists():
        d = json.loads(rp.read_text())["jobs"]
        tot = sum(j["searches"] for j in d.values())
        blocks["recheck_classification"] = (
            f"All {tot:,} stored maximisers of X-005 re-evaluated with the generalised evaluator: in a corner of the classification rule: "
            f"{sum(j['in_corner'] for j in d.values())}; cost changed by the exact rule: {sum(j['changed'] for j in d.values())}; claims violated under the exact rule: "
            f"{sum(j['violations_exact'] for j in d.values())}; the convention of the published runs reproduces the stored value in "
            f"{sum(j['legacy_reproduces_stored'] for j in d.values()):,} of {tot:,} searches (the others are the rounding-decided ties of ENG-MSG-0003 §5, "
            f"largest difference `{max(j['max_abs_legacy_minus_stored'] for j in d.values()):.2f}` in the logarithm).")
    ap_ = RESULTS / "x005_anyplacement.jsonl"
    rows = [json.loads(line) for line in ap_.read_text().splitlines() if line.strip()] if ap_.exists() else []
    cp = RESULTS / "x005_cost.jsonl"
    if rows and cp.exists():
        prod = {(c["u"], c["n"], c["phi"]): max(s["best_value"] for s in c["searches"]) for c in (json.loads(line) for line in cp.read_text().splitlines())}
        lines = ["| `u` | cells | largest excess of the placement-free bound (searched) over the worst product instance (searched), in units of `n a` | where | "
                 "cells in which the bound exceeds the product worst by more than `0.001 n a` | smallest (most negative) difference |", "|---|---|---|---|---|---|"]
        alld = []
        for u in sorted({r["u"] for r in rows}):
            ds = []
            for r in rows:
                if r["u"] != u:
                    continue
                na = r["n"] * r["a"]
                b = max(s["best_value"] for s in r["searches"])
                ds.append(((b - prod[(r["u"], r["n"], r["phi"])]) / na, r["n"], r["phi"]))
            alld += ds
            top = max(ds)
            lines.append(f"| {u:g} | {len(ds)} | `{top[0]:+.5f}` | `n = {top[1]}`, `φ = {top[2]:.2f}` | {sum(d[0] > 1e-3 for d in ds)} | `{min(ds)[0]:+.5f}` |")
        blocks["anyplacement"] = "\n".join(lines)
        blocks["anyplacement_summary"] = (f"{len(rows)} cells (the sizes up to `n = {max(r['n'] for r in rows):,}`).  Searching the placement-free bound directly raises the worst case found by at most "
                                          f"`{max(d[0] for d in alld):+.5f}` in units of `n a` (`n = {max(alld)[1]}`, `φ = {max(alld)[2]:.2f}`); in {sum(d[0] > 1e-3 for d in alld)} cells by more than `0.001`.")
    return blocks


def x009_blocks() -> dict[str, str]:
    """X-009: C_max of Theorem 11.56 against the non-adaptive lower bound (SCI-REV-0007 R6-E1)."""
    sp = RESULTS / "x009_separation.json"
    if not sp.exists():
        return {}
    d = json.loads(sp.read_text())
    blocks: dict[str, str] = {}
    diffs = []
    for r in d["validation"]:
        mine = (r["lCmax_at_half"], r["lLB_na"], r["plain"], r["hinted"])
        diffs += [abs(round(m, 1) - t) for m, t in zip(mine, r["theirs"])]
    dcap = []
    for r in d["validation_cap"]:
        dcap += [abs(round(r["lCmax_cap_at_055"], 2) - r["theirs"][0]), abs(round(r["lLB_na"], 2) - r["theirs"][1])]
    blocks["separation_validation"] = (
        f"All {len(diffs)} numbers of the table of SCI-REV-0007 §5 / `R6_REPORT.md` §2.9 ({len(d['validation'])} sizes; `ln C_max` at `φ = 0.5`, `ln LB_na`, the plain "
        f"bracket, the hinted lower bound) are reproduced to the digit given: {sum(x < 1e-9 for x in diffs)} of {len(diffs)} identical after rounding to one decimal"
        + (f" (largest difference {max(diffs):.1f})" if max(diffs) > 1e-9 else "")
        + f".  The {len(dcap)} numbers of its table with the lowered cap (`φ = 0.55`): {sum(x < 1e-9 for x in dcap)} of {len(dcap)} identical after rounding to two decimals"
        + (f" (largest difference {max(dcap):.2f})" if max(dcap) > 1e-9 else "") + ".")
    lines = ["| `u` | cost bound | sizes examined | least size with the bound below `LB_na` (margin in `ln`, best `φ`) | larger sizes at which it is above again | below at every examined size from | "
             "their first grid size |", "|---|---|---|---|---|---|---|"]
    theirs = {(1.0, "lCmax"): 1400, (2.0, "lCmax"): 540, (0.5, "lCmax"): 4700, (1.0, "lCmax_cap"): 1300, (2.0, "lCmax_cap"): 500, (0.5, "lCmax_cap"): 4150}
    for u in (0.5, 1.0, 2.0):
        w = sorted([r for r in d["window"] if r["u"] == u] + [r for r in d["beyond"] if r["u"] == u], key=lambda r: r["n"])
        for key, name, pk in (("lCmax", "`C_max` (Theorem 11.56)", "phi"), ("lCmax_cap", "`C_max` with the lowered cap", "phi_cap")):
            ok = [r for r in w if r[key] < r["lLB_na"]]
            first = ok[0]
            bad_later = [r["n"] for r in w if r["n"] > first["n"] and not r[key] < r["lLB_na"]]
            stable = min(r["n"] for r in w if all(q[key] < q["lLB_na"] for q in w if q["n"] >= r["n"]))
            lines.append(f"| {u:g} | {name} | {w[0]['n']}–{w[-1]['n']} ({len(w)}) | **{first['n']}** ({first['lLB_na'] - first[key]:.2f}, {first[pk]:.2f}) | "
                         f"{', '.join(map(str, bad_later)) if bad_later else 'none'} | **{stable}** | {theirs[(u, key)]} |")
    blocks["separation_window"] = "\n".join(lines)
    lp = RESULTS / "x005_lowered_cap.json"
    if lp.exists():
        lc = json.loads(lp.read_text())["jobs"]
        runs = sum(j["runs"] for j in lc.values())
        w = max(lc.values(), key=lambda j: j["max_l_over_cap"])
        blocks["lowered_cap_x005"] = (
            f"All {runs:,} stored instances of X-005 re-evaluated (the maximisers of {runs - 2 * sum(j['runs'] for j in lc.values()) // 6:,} searches under every objective, "
            f"and the flat instances): samples at or above the lowered cap: **{sum(j['above_lowered_cap'] for j in lc.values())}**; samples above `M†`: "
            f"{sum(j['above_M_dagger'] for j in lc.values())}; the largest sample is `{math.exp(max(j['max_l_over_M_dagger'] for j in lc.values())):.2f}·M†`, which is "
            f"{w['worst']['sample_over_cap']:.3f} of the lowered cap there (`u = {w['worst']['u']:g}`, `n = {w['worst']['n']}`, `φ = {w['worst']['phi']:.2f}`).  Over the cells the "
            f"lowered cap is between `{math.exp(min(j['min_l_cap_over_M_dagger'] for j in lc.values())):.1f}·M†` and `{math.exp(max(j['max_l_cap_over_M_dagger'] for j in lc.values())):.0f}·M†`, "
            f"and the theorem's `M̄` is at least `{math.exp(min(j['min_l_Mbar_over_cap'] for j in lc.values())):.0f}` times larger than it.")
    return blocks


def x006b_blocks() -> dict[str, str]:
    """X-006b: the sampler defect, the exposure of job M-011, old against new, the invalid inner behaviour, the lowered cap."""
    blocks: dict[str, str] = {}
    bp = RESULTS / "x006b_binomial_bias.json"
    if bp.exists():
        d = json.loads(bp.read_text())
        g = d["grid"]
        means = [m for m in sorted({r["mean"] for r in g}) if m in (29.0, 60.0, 92.0, 500.0, 5000.0, 1e5, 1e7)]
        lines = ["| trials `n` | " + " | ".join(f"mean {m:g}" for m in means) + " |", "|---|" + "---|" * len(means)]
        for n in sorted({r["n"] for r in g}):
            cells = []
            for m in means:
                r = next(x for x in g if x["n"] == n and x["mean"] == m)
                bad = max(abs(r["numpy_z_mean"]), abs(r["numpy_z_var"])) > 5
                cells.append(("**" if bad else "") + f"{r['numpy_z_mean']:+.1f} / {r['numpy_z_var']:+.1f}" + (f" ({100 * r['numpy_rel_mean']:+.2f} %)**" if bad else ""))
            lines.append(f"| `{n:.3g}` | " + " | ".join(cells) + " |")
        blocks["binomial_bias"] = "\n".join(lines)
        ez = [abs(r["exact_z_mean"]) for r in g] + [abs(r["exact_z_var"]) for r in g]
        worst = max(g, key=lambda r: max(abs(r["exact_z_mean"]), abs(r["exact_z_var"])))
        nb = sum(max(abs(r["numpy_z_mean"]), abs(r["numpy_z_var"])) > 5 for r in g)
        small = [r for r in g if r["n"] <= 10 ** 14]
        rc = d.get("recheck", [])
        blocks["binomial_summary"] = (
            f"numpy {d['numpy']}, {g[0]['draws']:,} draws per cell.  numpy's sampler: {nb} of {len(g)} cells have a z-score above 5 in absolute value, all of them at "
            f"`n ≥ {min(r['n'] for r in g if max(abs(r['numpy_z_mean']), abs(r['numpy_z_var'])) > 5):.0e}`; the largest relative error of the mean is "
            f"`{100 * min(r['numpy_rel_mean'] for r in g):+.2f} %` (`n = {min(g, key=lambda r: r['numpy_rel_mean'])['n']:.3g}`, mean {min(g, key=lambda r: r['numpy_rel_mean'])['mean']:g}); "
            f"at `n ≤ 10¹⁴` the largest z-score is {max(max(abs(r['numpy_z_mean']), abs(r['numpy_z_var'])) for r in small):.1f} in {2 * len(small)} scores.  "
            f"The exact sampler on the same grid: largest z-score **{max(ez):.1f}** in {len(ez)} scores (cell `n = {worst['n']:.3g}`, mean {worst['mean']:g}, branch "
            f"`{worst['exact_branch']}`)"
            + (f"; that cell is numpy's own sampler at `n = 2³¹`, and {len(rc)} further streams of {rc[0]['draws']:,} draws each give z-scores of the mean between "
               f"{min(r['z_mean'] for r in rc):+.1f} and {max(r['z_mean'] for r in rc):+.1f} — a fluctuation" if rc and worst["exact_branch"] == "numpy" else "")
            + f".  Chi-square tests of the Poissonisation step against the exact law, {len(d['chi_square'])} cases from `n = 12` to `n = 2⁶¹`: p-values between "
            f"{min(c['p_value'] for c in d['chi_square']):.2f} and {max(c['p_value'] for c in d['chi_square']):.2f}.")
    blocks.update(x009_blocks())
    blocks.update(x010_blocks())
    xb, xa = RESULTS / "x006b_sampled.jsonl", RESULTS / "x006_sampled.jsonl"
    if not (xb.exists() and xa.exists()):
        return blocks
    new_all = [json.loads(line) for line in xb.read_text().splitlines() if line.strip()]
    old = [json.loads(line) for line in xa.read_text().splitlines() if line.strip()]
    new = [r for r in new_all if r["oracle"] != "dear"]
    dear = [r for r in new_all if r["oracle"] == "dear"]
    key = lambda r: (r["u"], r["n_o"], r["profile"], r["oracle"], r["k_scale"])       # noqa: E731
    oldm = {key(r): r for r in old}
    pairs = [(oldm[key(r)], r) for r in new if key(r) in oldm]
    sizes = sorted({(r["u"], r["n_o"]) for r in new})
    scales = sorted({r["k_scale"] for r in new}, reverse=True)
    # exposure: the largest block from which a shell count is drawn is half the largest sample
    lines = ["| `u` | `n_o` | `K` scale | largest sample of a run | largest block drawn from | cases with a block of `10¹⁵` points or more |", "|---|---|---|---|---|---|"]
    for (u, n_o) in sizes:
        for sc in scales:
            rows = [r for r in new if (r["u"], r["n_o"], r["k_scale"]) == (u, n_o, sc)]
            if rows:
                mm = max(r["M_max"] for r in rows)
                lines.append(f"| {u:g} | {n_o} | {_scale(sc)} | `{mm:.1e}` | `{mm / 2:.1e}` | {sum(r['M_max'] / 2 >= 1e15 for r in rows)} of {len(rows)} |")
    blocks["exposure"] = "\n".join(lines)
    exposed = [(a, b) for a, b in pairs if b["M_max"] / 2 >= 1e15]
    clean = [(a, b) for a, b in pairs if b["M_max"] / 2 < 1e15]

    def z2(x1, n1, x2, n2):
        pp = (x1 + x2) / (n1 + n2)
        return 0.0 if pp in (0.0, 1.0) else (x1 / n1 - x2 / n2) / math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    lines = ["| `u` | `n_o` | `K` scale | runs (each version) | good event failed: numpy sampler → exact sampler | z | bracket invalid: numpy → exact | z | invalid on the good event (both) | largest per-case z (good event, invalid) |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for (u, n_o) in sizes:
        for sc in scales:
            pr = [(a, b) for a, b in pairs if (b["u"], b["n_o"], b["k_scale"]) == (u, n_o, sc)]
            if not pr:
                continue
            n1 = sum(a["runs"] - a["skipped"] for a, _ in pr)
            n2 = sum(b["runs"] - b["skipped"] for _, b in pr)
            g1, g2 = sum(a["good_event_failed"] for a, _ in pr), sum(b["good_event_failed"] for _, b in pr)
            i1, i2 = sum(a["invalid"] for a, _ in pr), sum(b["invalid"] for _, b in pr)
            zc = [(abs(z2(a["good_event_failed"], a["runs"], b["good_event_failed"], b["runs"])), abs(z2(a["invalid"], a["runs"], b["invalid"], b["runs"]))) for a, b in pr]
            lines.append(f"| {u:g} | {n_o} | {_scale(sc)} | {n1:,}" + ("" if n1 == n2 else f" / {n2:,}") + f" | {g1:,} → {g2:,} | {z2(g1, n1, g2, n2):+.1f} | {i1:,} → {i2:,} | {z2(i1, n1, i2, n2):+.1f} | "
                         f"{sum(a['invalid_on_good_event'] for a, _ in pr) + sum(b['invalid_on_good_event'] for _, b in pr)} | {max(z[0] for z in zc):.1f}, {max(z[1] for z in zc):.1f} |")
    blocks["sampled_compare"] = "\n".join(lines)
    allz = [abs(z2(a[k], a["runs"], b[k], b["runs"])) for a, b in pairs for k in ("good_event_failed", "invalid")]
    nz = [z for z in allz if z > 0]
    fullp = [(a, b) for a, b in pairs if b["k_scale"] == 1.0]
    blocks["sampled_compare_summary"] = (
        f"{len(pairs)} cases were run with both samplers ({len(exposed)} of them drew from blocks of `10¹⁵` points or more, {len(clean)} did not).  "
        f"With the theorem's `K`: numpy sampler {sum(a['good_event_failed'] + a['invalid'] for a, _ in fullp)} failures of the good event or invalid brackets in "
        f"{sum(a['runs'] for a, _ in fullp):,} runs, exact sampler {sum(b['good_event_failed'] + b['invalid'] for _, b in fullp)} in {sum(b['runs'] for _, b in fullp):,}.  "
        f"Over all cases and both statistics, {len(nz)} per-case comparisons are not 0 against 0; their largest two-sample z-score is {max(nz) if nz else 0.0:.1f}, "
        f"and {sum(z > 3 for z in nz)} exceed 3 (expected by chance among {len(nz)}: {len(nz) * 0.0027:.1f}).")
    # the invalid inner behaviour
    if dear:
        lines = ["| `u` | `n_o` | `n_i` | cost of the last rung `ln C_L` | `ln C_max` | cases | runs | closed | stopped by the query budget | stopped otherwise | runs above `C_max` | largest `ln(evaluations) − ln C_max` |",
                 "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        import run_sampled
        from metricchain_eng.twolevel.ckernel import Evaluator
        for (u, n_o, n_i) in sorted({(r["u"], r["n_o"], r["n_i"]) for r in dear}):
            rows = [r for r in dear if (r["u"], r["n_o"], r["n_i"]) == (u, n_o, n_i)]
            ev = Evaluator(run_sampled.params(u, n_o, n_i))
            budget = sum(r["abort_reasons"].get("abort-query budget", 0) for r in rows)
            lines.append(f"| {u:g} | {n_o} | {n_i} | {float(ev.lC[-1]):.1f} | {ev.lCmax:.1f} | {len(rows)} | {sum(r['runs'] for r in rows):,} | {sum(r['closed'] for r in rows):,} | {budget:,} | "
                         f"{sum(r['aborted'] for r in rows) - budget} | {sum(r['cost_bound_exceeded'] for r in rows)} | {max(r['lqueries_max_all'] - r['lCmax'] for r in rows):+.2f} |")
        blocks["sampledb_dear"] = "\n".join(lines)
        blocks["sampledb_dear_summary"] = (
            f"{sum(r['runs'] for r in dear):,} runs with the invalid inner behaviour in {len(dear)} cases: "
            f"{sum(r['abort_reasons'].get('abort-query budget', 0) for r in dear):,} were stopped by the abort rule on the query budget, "
            f"{sum(r['closed'] for r in dear):,} closed, and **{sum(r['cost_bound_exceeded'] for r in dear)}** spent more than `C_max` evaluations; "
            f"with valid inner behaviours and the theorem's `K`: {sum(r['cost_bound_exceeded'] for r in new if r['k_scale'] == 1.0)} of "
            f"{sum(r['runs'] for r in new if r['k_scale'] == 1.0):,}.")
    # literal runs against the lowered sample cap of THY-RES-0004 §3
    import run_sampled
    from metricchain_eng.twolevel.alg2l import lowered_sample_cap
    from metricchain_eng.twolevel.ckernel import Evaluator
    evs = {}
    lines = ["| `u` | `n_o` | `K` scale | cases | largest sample `/ M†` | lowered cap `/ M†` | largest sample / lowered cap | theorem's `M̄ / M†` | cases with a sample at or above the lowered cap |",
             "|---|---|---|---|---|---|---|---|---|"]
    n_viol = n_cases = 0
    worst_ratio = 0.0
    for (u, n_o) in sizes:
        for sc in scales:
            rows = [r for r in new_all if (r["u"], r["n_o"], r["k_scale"]) == (u, n_o, sc) and r["n_i"] == 6]
            if not rows:
                continue
            ev = evs.setdefault((u, n_o), Evaluator(run_sampled.params(u, n_o, 6)))
            P = run_sampled.params(u, n_o, 6)
            rat, capm, viol = [], [], 0
            for r in rows:
                lK = math.log(r["K"])
                lcap = lowered_sample_cap(P, ev.outer, ev.C, lK)
                lMd = lK - math.log(1 - P.eta) - ev.C.lpi_dag
                lM = math.log(r["M_max"])
                rat.append((lM - lMd, lM - lcap))
                capm.append(lcap - lMd)
                viol += (r["M_max"] > r["K"]) and (lM >= lcap - 1e-12)
            n_viol += viol
            n_cases += len(rows)
            worst_ratio = max(worst_ratio, math.exp(max(x[1] for x in rat)))
            lmbar = math.log(2 * (1 + P.eta) * ev.C.nu0) + P.lam
            lines.append(f"| {u:g} | {n_o} | {_scale(sc)} | {len(rows)} | {math.exp(max(x[0] for x in rat)):.2f} | {math.exp(capm[0]):.2f} | {math.exp(max(x[1] for x in rat)):.3f} | "
                         f"`{math.exp(lmbar):.1e}` | {viol} |")
    blocks["sampledb_cap"] = "\n".join(lines)
    blocks["sampledb_cap_summary"] = (f"In the {sum(r['runs'] for r in new_all if r['n_i'] == 6):,} literal runs of X-006b with `n_i = 6` ({n_cases} cases, valid and invalid inner behaviours, "
                                      f"`K` from the theorem's value down to 4) the largest sample reached {worst_ratio:.3f} of the lowered cap; cases with a sample at or above it: **{n_viol}**.")
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
