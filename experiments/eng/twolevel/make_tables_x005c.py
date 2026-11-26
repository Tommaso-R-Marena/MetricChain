"""Tables of ENG-RES-0017 (experiment X-005c: the worst product instance re-examined after SCI-REV-0018), generated
from the stored results so that no number in the message is typed by hand.

    python experiments/eng/twolevel/make_tables_x005c.py                 # print every block
    python experiments/eng/twolevel/make_tables_x005c.py --write FILE    # fill the <!-- TABLE:name --> blocks of FILE
    python experiments/eng/twolevel/make_tables_x005c.py --verify FILE   # exit 1 if FILE differs from the artifacts
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
ORACLES = ("bottom", "top")
PHIS = (0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85)
SMALL = (250, 350, 500)
SIX = ((2.0, 250, 0.85), (2.0, 350, 0.85), (0.5, 250, 0.5), (0.5, 350, 0.5), (0.5, 350, 0.55), (0.5, 500, 0.35))


def jl(name: str) -> list[dict]:
    p = RES / name
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()] if p.exists() else []


def key(r: dict) -> tuple:
    return (r["u"], r["n"], r["phi"])


def best(r: dict, objective: str, oracle: str | None = None) -> float:
    return max(s["best_value"] for s in r["searches"] if s["objective"] == objective and (oracle is None or s["oracle"] == oracle))


def build() -> dict[str, str]:
    blocks: dict[str, str] = {}
    cost = {key(r): r for r in jl("x005_cost.jsonl")}
    anyp = {key(r): r for r in jl("x005_anyplacement.jsonl")}
    sp = RES / "x005c_stored.json"
    if not sp.exists():
        return blocks
    stored = {key(r): r for r in json.loads(sp.read_text())["rows"]}
    w = lambda d: max(d.values())  # noqa: E731

    # ---- (i) the stored maximisers of the bound, as the product instances they are -------------------------------
    rows = list(stored.values())
    moved = [r for r in rows if w(r["new"]) > w(r["old"]) + 1e-9]
    moved4 = [r for r in rows if w(r["new"]) - w(r["old"]) > 1e-4 * r["na"]]
    moved3 = [r for r in rows if w(r["new"]) - w(r["old"]) > 1e-3 * r["na"]]
    big = [r for r in rows if w(r["bound"]) - w(r["old"]) > 1e-4 * r["na"]]
    closed = [r for r in big if abs(w(r["bound"]) - w(r["new"])) <= 1e-6 * r["na"]]
    top = max(moved, key=lambda r: (w(r["new"]) - w(r["old"])) / r["na"])
    below = [r for r in rows if w(r["old"]) - w(r["bound"]) > 1e-4 * r["na"]]
    low = min(rows, key=lambda r: (w(r["bound"]) - w(r["old"])) / r["na"])
    not_repro = sorted((r for r in rows if r["recheck"] > 1e-9), key=lambda r: -r["recheck"])
    blocks["x005c_stored"] = (
        f"{len(rows)} cells (every cell of job M-014: `n ≤ 16 000`), {4 * len(rows):,} stored maximisers of the bound, each decoded as the product instance it is and run "
        f"with the compiled kernel under both inner behaviours; no run violates a claim of Theorem 11.56.  Such a product instance costs more than the worst product "
        f"instance found by job M-008 in **{len(moved)} cells** ({len(moved4)} by more than `10⁻⁴·na`, {len(moved3)} by more than `10⁻³·na`; largest "
        f"`{(w(top['new']) - w(top['old'])) / top['na']:+.5f}·na` at `u = {top['u']:g}`, `n = {top['n']}`, `φ = {top['phi']:g}`).  Of the {len(big)} cells in which the searched bound "
        f"exceeds the product search by more than `10⁻⁴·na`, {len(closed)} are closed in this way to `10⁻⁶·na`; the other {len(big) - len(closed)} are "
        + ", ".join(f"`({r['u']:g}, {r['n']}, {r['phi']:g})`" for r in big if r not in closed)
        + f".  Conversely the bound search ends below the product search by more than `10⁻⁴·na` in {len(below)} cells (down to "
        f"`{(w(low['bound']) - w(low['old'])) / low['na']:+.4f}·na` at `u = {low['u']:g}`, `n = {low['n']}`, `φ = {low['phi']:g}`).  "
        f"The stored product maximisers themselves are returned by the present kernel to `10⁻⁹` in all but {len(not_repro)} cells"
        + (" (" + ", ".join(f"`({r['u']:g}, {r['n']}, {r['phi']:g})`: `{r['recheck']:.2g}`" for r in not_repro) + " in `ln cost`; the tie rule of ENG-MSG-0003 §5, as in the recheck of ENG-RES-0008)" if not_repro else "")
        + ".")

    # ---- the review's stored product instances, with the kernel ---------------------------------------------------
    sci = RES / "x005c_science_instances.json"
    if sci.exists():
        d = json.loads(sci.read_text())["rows"]
        lines = ["| `(u, n, φ)`, behaviour | the review's product instance: `ln cost` by our compiled kernel | by our Python reference, as run by the review | bound searched (M-014) | worst product instance found (M-008) | in the class? | claims violated |",
                 "|---|---|---|---|---|---|---|"]
        for r in sorted(d, key=lambda r: (-r["u"], r["n"], r["phi"])):
            if abs(r["lcost_kernel"] - r["bound_searched"]) > 1e-6:
                continue                      # the review's files for the other u = 1/2 cells hold other constructions
            lines.append(f"| ({r['u']:g}, {r['n']}, {r['phi']:g}), {r['oracle']} | {r['lcost_kernel']:.9f} | {r['lcost_review']:.9f} | {r['bound_searched']:.6f} | "
                         f"{r['worst_product_found']:.6f} | Lipschitz violation `{r['lipschitz_violation']:.0e}`, slopes {'in `[0, u]`' if r['monotone'] else 'in `[−u, u]`'}, reference in shell {r['d_ref']} | {len(r['violations'])} |")
        blocks["x005c_science"] = "\n".join(lines)

    # ---- (ii) the searches with added starting points ---------------------------------------------------------------
    srch = {key(r): r for r in jl("x005c_search.jsonl")}
    if srch:
        na = lambda k: stored[k]["na"]  # noqa: E731
        lines = ["| `(u, n, φ)` | worst product instance, job M-008 | bound, job M-014 | stored maximiser of the bound as a product instance (i) | product search with the added starting points (ii) | bound search with the same starting points (ii) | (ii) product − M-008, in `na` | (ii) bound − (ii) product, in `na` |",
                 "|---|---|---|---|---|---|---|---|"]
        for k in SIX:
            if k not in srch:
                continue
            r, s = stored[k], srch[k]
            p2, b2 = best(s, "cost"), best(s, "cost_any_placement")
            lines.append(f"| ({k[0]:g}, {k[1]}, {k[2]:g}) | {w(r['old']):.6f} | {w(r['bound']):.6f} | {w(r['new']):.6f} | **{p2:.6f}** | {b2:.6f} | `{(p2 - w(r['old'])) / na(k):+.5f}` | `{(b2 - p2) / na(k):+.5f}` |")
        blocks["x005c_six"] = "\n".join(lines)

        # per cell: the new worst product instance = max(old, (i), (ii))
        new_worst, new_bound = {}, {}
        for k, s in srch.items():
            new_worst[k] = max(w(stored[k]["old"]), w(stored[k]["new"]), best(s, "cost"))
            new_bound[k] = max(w(stored[k]["bound"]), best(s, "cost_any_placement"))
        inc = {k: (new_worst[k] - w(stored[k]["old"])) / na(k) for k in srch}
        gap = {k: (new_bound[k] - new_worst[k]) / na(k) for k in srch}
        nviol = sum(x["n_violations"] or 0 for s in srch.values() for x in s["searches"])
        over_cap = max(x["cost_over_cap"] for s in srch.values() for x in s["searches"] if x["objective"] == "cost")
        lip = max(x["lipschitz_violation"] for s in srch.values() for x in s["searches"])
        kmax = max(inc, key=inc.get)
        gpos = [k for k in gap if gap[k] > 1e-4]
        gneg = [k for k in gap if gap[k] < -1e-4]
        kg = max(gap, key=gap.get)
        kl = min(gap, key=gap.get)
        n_runs = sum(x["n_eval"] for s in srch.values() for x in s["searches"])
        blocks["x005c_search_summary"] = (
            f"{len(srch)} of 108 cells (`n = 250, 350, 500`), {sum(len(s['searches']) for s in srch.values())} searches, {n_runs:,} mean runs; three times the budgets of job M-008; "
            f"{nviol} runs of a product instance with a violated claim; the largest `ln(cost/C_max)` is `{over_cap:.2f}`; every maximiser is in the class "
            f"(largest Lipschitz violation `{lip:.1e}`).  The worst product instance found rises in {sum(v > 1e-9 for v in inc.values())} cells — in {sum(v > 1e-4 for v in inc.values())} by more "
            f"than `10⁻⁴·na`, in {sum(v > 1e-3 for v in inc.values())} by more than `10⁻³·na`, in {sum(v > 1e-2 for v in inc.values())} by more than `10⁻²·na`; the largest rise is "
            f"`{inc[kmax]:+.5f}·na` at `u = {kmax[0]:g}`, `n = {kmax[1]}`, `φ = {kmax[2]:g}`.  After it the bound search (repeated with the same starting points) and the product search "
            f"differ by more than `10⁻⁴·na` in {len(gpos) + len(gneg)} cells: the bound is higher in {len(gpos)} (at most `{gap[kg]:+.5f}·na`, `({kg[0]:g}, {kg[1]}, {kg[2]:g})`) "
            f"and *lower* in {len(gneg)} (down to `{gap[kl]:+.5f}·na`, `({kl[0]:g}, {kl[1]}, {kl[2]:g})`).")

        # where does the new maximiser sit?
        ref_far, c_low, tot = 0, 0, 0
        for k, s in srch.items():
            x = max((x for x in s["searches"] if x["objective"] == "cost"), key=lambda x: x["best_value"])
            if inc[k] > 1e-4:
                tot += 1
                n_o = cost[k]["n_o"]
                ref_far += x["d0"] in (0, n_o)
                c_low += x["c_in_frac"] < 0.02 or x["c_in_frac"] > 0.98
        blocks["x005c_where"] = (f"In the {tot} cells where the worst product instance rises by more than `10⁻⁴·na`, the new maximiser has its reference point in the first or the last "
                                 f"shell in {ref_far} and its fibres at an end of the range of places in {c_low}.")

        # the headline of ENG-RES-0008 at the three small sizes: worst instance at the flat-best fraction; the minimax fraction
        lines = ["| `u` | `n` | best `φ` for the flat instance: worst instance found there, ENG-RES-0008 → now | best `φ` against the worst instance, and that worst case: ENG-RES-0008 → now | certified cap `C_max` at the new fraction |",
                 "|---|---|---|---|---|"]
        changes = []
        for u in sorted({k[0] for k in srch}):
            for n in SMALL:
                ks = [(u, n, phi) for phi in PHIS]
                if not all(k in srch for k in ks):
                    continue
                nn = na(ks[0])

                def flat(k):
                    return cost[k]["flat"]["bottom"]["lcost"]

                def old_w(k):
                    return max(w(stored[k]["old"]), max(cost[k]["flat"][o]["lcost"] for o in ORACLES))

                def new_w(k):
                    return max(old_w(k), new_worst[k])

                kf = min(ks, key=flat)
                ko, kn = min(ks, key=old_w), min(ks, key=new_w)
                changes.append((new_w(kn) - old_w(ko)) / nn)
                lines.append(f"| {u:g} | {n} | `φ = {kf[2]:.2f}`: {old_w(kf) / nn:.3f} → {new_w(kf) / nn:.3f} | **{old_w(ko) / nn:.3f}** (`φ = {ko[2]:.2f}`) → **{new_w(kn) / nn:.3f}** (`φ = {kn[2]:.2f}`) | "
                             f"{cost[kn]['constants']['lCmax'] / nn:.3f} |")
        if changes:
            blocks["x005c_main"] = "\n".join(lines)
            blocks["x005c_main_summary"] = (f"The number ENG-RES-0008 reports — the worst case found at the best outer fraction — rises in {sum(c > 5e-4 for c in changes)} of {len(changes)} "
                                            f"pairs `(u, n)` at these three sizes, by at most `{max(changes):.4f}` in units of `n a`.")

        # every cell whose worst product instance moved by more than 0.001 na
        lines = ["| `(u, n, φ)` | ENG-RES-0008 | now | rise, in `na` | found by |", "|---|---|---|---|---|"]
        for k in sorted((k for k in inc if inc[k] > 1e-3), key=lambda k: -inc[k]):
            src = "the search with added starting points" if best(srch[k], "cost") >= w(stored[k]["new"]) - 1e-9 and best(srch[k], "cost") > w(stored[k]["old"]) + 1e-9 else "a stored maximiser of the bound"
            lines.append(f"| ({k[0]:g}, {k[1]}, {k[2]:g}) | {w(stored[k]['old']) / na(k):.4f} | {new_worst[k] / na(k):.4f} | `{inc[k]:+.4f}` | {src} |")
        blocks["x005c_cells"] = "\n".join(lines)

    # ---- (iii) other seeds ----------------------------------------------------------------------------------------------
    seeds = jl("x005c_seeds.jsonl")
    if seeds and srch:
        by = defaultdict(list)
        for r in seeds:
            by[key(r)].append(r)
        diffs_p, diffs_b = [], []
        for k, rs in by.items():
            if k not in srch:
                continue
            p1, b1 = best(srch[k], "cost"), best(srch[k], "cost_any_placement")
            for r in rs:
                diffs_p.append(((best(r, "cost") - p1) / stored[k]["na"], k, r["seed"]))
                diffs_b.append(((best(r, "cost_any_placement") - b1) / stored[k]["na"], k, r["seed"]))
        if diffs_p:
            tp, lp = max(diffs_p), min(diffs_p)
            tb, lb = max(diffs_b), min(diffs_b)
            blocks["x005c_seeds"] = (
                f"{len(seeds)} further searches of each kind (seeds 2 and 3; `φ = 0.5, 0.85`; {len(by)} cells).  Against seed 1 the product search changes by between "
                f"`{lp[0]:+.5f}` and `{tp[0]:+.5f}` in units of `n a` (the largest rise at `({tp[1][0]:g}, {tp[1][1]}, {tp[1][2]:g})`, seed {tp[2]}), the bound search by between "
                f"`{lb[0]:+.5f}` and `{tb[0]:+.5f}`; {sum(abs(d[0]) > 1e-4 for d in diffs_p)} of {len(diffs_p)} product searches and {sum(abs(d[0]) > 1e-4 for d in diffs_b)} of "
                f"{len(diffs_b)} bound searches differ from seed 1 by more than `10⁻⁴·na`.")

    # ---- the control at larger sizes ------------------------------------------------------------------------------------
    large = {key(r): r for r in jl("x005c_large.jsonl")}
    if large:
        lines = ["| `(u, n, φ)` | worst product instance, job M-008 | bound, job M-014 | product search with the added starting points | bound search with them | product: rise over M-008, in `na` |",
                 "|---|---|---|---|---|---|"]
        rises = []
        for k in sorted(large):
            r, s = stored[k], large[k]
            p2, b2 = best(s, "cost"), best(s, "cost_any_placement")
            rises.append((max(p2, w(r["new"])) - w(r["old"])) / r["na"])
            lines.append(f"| ({k[0]:g}, {k[1]}, {k[2]:g}) | {w(r['old']):.4f} | {w(r['bound']):.4f} | {p2:.4f} | {b2:.4f} | `{(p2 - w(r['old'])) / r['na']:+.5f}` |")
        blocks["x005c_large"] = "\n".join(lines)
        blocks["x005c_large_summary"] = (f"{len(large)} cells at `n = 1000` and `4000`, the budgets of job M-008: with the added starting points (and the stored maximisers as seeds) the worst "
                                         f"product instance found rises by at most `{max(rises):.5f}·na`.")
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
