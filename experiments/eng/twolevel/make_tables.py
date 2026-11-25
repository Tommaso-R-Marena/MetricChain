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
            summary[(u, n)] = dict(plain=r["plain"] / na, lower=r["lower"] / na, phi_flat=phi_flat, flat=flat_cost(cf) / na,
                                   worst_at_flat=worst(cf) / na, phi_mm=phi_mm, minimax=worst(cm) / na,
                                   flat_at_mm=flat_cost(cm) / na, cap_at_mm=cm["constants"]["lCmax"] / na,
                                   cap_at_flat=cf["constants"]["lCmax"] / na)
            s = summary[(u, n)]
            lines.append(f"| {n} | {f3(s['plain'])} | {f3(s['flat'])} (`φ = {phi_flat:.2f}`) | {f3(s['worst_at_flat'])} | "
                         f"**{f3(s['minimax'])}** (`φ = {phi_mm:.2f}`) | {f3(s['flat_at_mm'])} | {f3(s['cap_at_mm'])} | {f3(s['lower'])} |")
        blocks[f"main_u{u:g}"] = "\n".join(lines)

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
    lines = ["| `u` | `n` | (worst found at the best `φ`)`/(n a)` | minus `τ₂/a` | that difference × `√n` | `ln(C_max)/(n a)` minus worst found |",
             "|---|---|---|---|---|---|"]
    for u in us:
        c = cube_constants(u)
        t2 = tau2(u)[0] / c.a
        for n in sorted(n for (uu, n) in summary if uu == u):
            s = summary[(u, n)]
            lines.append(f"| {u:g} | {n} | {f3(s['minimax'])} | {s['minimax'] - t2:+.3f} | {(s['minimax'] - t2) * math.sqrt(n):.1f} | {s['cap_at_mm'] - s['minimax']:.3f} |")
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
                row.append(f"{(min(vals) if key == 'margin_iii' else max(vals)):+.3f}")
        lines.append(f"| {label} | {claim} | " + " | ".join(row) + " |")
    blocks["claims"] = "\n".join(lines)

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
        pat = re.compile(rf"(<!-- TABLE:{re.escape(name)} -->\n).*?(\n<!-- /TABLE:{re.escape(name)} -->)", re.S)
        new = pat.sub(lambda m: m.group(1) + body + m.group(2), new)
    if args.verify:
        print("tables in", target.name, "match the artifacts" if new == text else "DIFFER from the artifacts")
        return 0 if new == text else 1
    target.write_text(new)
    print("updated", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
