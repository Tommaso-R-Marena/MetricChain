#!/usr/bin/env python3
"""Generate the Markdown tables of ENG-RES-0002 from the stored artifacts.

Every number in the tables of ``docs/collaboration/responses/engineering/ENG-RES-0002.md`` is
produced by this script from ``data/`` and ``results/`` -- nothing is typed by hand.

    python experiments/eng/chain_cover/make_tables.py            # print the tables
    python experiments/eng/chain_cover/make_tables.py --write F  # replace the marked blocks in file F
    python experiments/eng/chain_cover/make_tables.py --verify F # exit 1 if F's blocks differ

A block in a document is delimited by ``<!-- TABLE:name -->`` and ``<!-- /TABLE:name -->``.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.chains.profile_cover import parse_enum_output  # noqa: E402

EPS_KEYS = ["eps=0", "eps=1", "eps=1/20*N", "eps=1/10*N", "eps=1/4*N", "eps=1/2*N"]
DELTA_KEYS = ["delta=4", "delta=2", "delta=1", "delta=1/2", "delta=1/4"]


def fmt_int(x: int) -> str:
    return f"{x:,}".replace(",", " ")


def table(n: int):
    p = HERE / "data" / f"dia_Sc12_n{n}.txt"
    return parse_enum_output(p.read_text()) if p.exists() else None


def cover_cell(v: dict) -> str:
    if v["proved_optimal"]:
        return str(v["N_cov"])
    lo = max(v.get("lower_certified", 1), v.get("lower_solver", 1))
    return str(v["N_cov"]) if lo >= v["N_cov"] else f"[{lo}, {v['N_cov']}]"


def net_cell(v: dict) -> str:
    b = v["net_closed_radius"]
    return str(b["upper"]) if b["exact"] else f"[{b['lower']}, {b['upper']}]"


def build() -> dict[str, str]:
    out: dict[str, str] = {}
    res = json.loads((HERE / "results" / "lattice_Sc12.json").read_text())
    rows = {r["n_torsions"]: r for r in res["rows"]}

    # ---- sequence of conformations and classes, n = 13..24 --------------------------------------
    ns = [n for n in range(13, 25) if table(n) is not None]
    tabs = {n: table(n) for n in ns}
    lines = ["| `n` | " + " | ".join(str(n) for n in ns) + " |", "|---|" + "---|" * len(ns),
             "| conformations | " + " | ".join(fmt_int(tabs[n].n_conformations) for n in ns) + " |",
             "| profile classes | " + " | ".join(fmt_int(tabs[n].n_classes) for n in ns) + " |"]
    out["sequence"] = "\n".join(lines)

    # ---- covering numbers -------------------------------------------------------------------------
    lines = ["| `n` | `N` | `L=1`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` | `L=1/5`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for n in sorted(rows):
        if n < 5:
            continue
        c = rows[n]["cover"]
        cells = [cover_cell(c[f"L=1,{k}"]) for k in EPS_KEYS] + [cover_cell(c[f"L=1/5,{k}"]) for k in EPS_KEYS]
        lines.append(f"| {n} | {rows[n]['n_beads']} | " + " | ".join(cells) + " |")
    out["cover"] = "\n".join(lines)
    out["cover_range"] = f"{min(n for n in rows if n >= 5)}…{max(rows)}"

    # ---- finite-size expansion of the profile set ---------------------------------------------------
    sel = [n for n in (8, 12, 16, 18, 20, 22, 24) if table(n) is not None]
    hdr = "| `N` (beads) | " + " | ".join(str(n + 3) for n in sel) + " | bulk lattice |"
    l1, l2, l3 = [], [], []
    for n in sel:
        t = table(n)
        N = t.n_beads
        norms = t.l1_norms()
        i = int(np.argmax(norms))
        l1.append(f"{t.hist.sum(axis=1).max() / N:.2f}")
        l2.append(f"{norms.max() / N:.2f}")
        l3.append(f"{int(t.gmin[i])}/{n}")
    out["finite_size"] = "\n".join([
        hdr, "|---|" + "---|" * (len(sel) + 1),
        "| largest number of pairs inside the cutoff, per bead | " + " | ".join(l1) + " | 12 |",
        "| largest `‖N^x‖₁`, per bead | " + " | ".join(l2) + " | 35 |",
        "| fewest gauche torsions in that extreme class, of `n` | " + " | ".join(l3) + " | — |"])

    # ---- entropy -------------------------------------------------------------------------------------
    lines = ["| `n` | `δ = 4` | `δ = 2` | `δ = 1` | `δ = ½` | `δ = ¼` | traversal `m(δ)` at the same five radii |", "|---|---|---|---|---|---|---|"]
    for n in sorted(rows):
        if n not in (8, 10, 12, 13, 14, 16, 18, 20, 22, 24):
            continue
        e = rows[n]["entropy"]
        if "net_closed_radius" not in e[DELTA_KEYS[0]]:
            continue
        lines.append(f"| {n} | " + " | ".join(net_cell(e[k]) for k in DELTA_KEYS)
                     + " | " + ", ".join(str(e[k]["m_fpt"]) for k in DELTA_KEYS) + " |")
    out["entropy"] = "\n".join(lines)

    # ---- single-flip constants -----------------------------------------------------------------------
    fp = HERE / "results" / "lattice_Sc12_flip.json"
    if fp.exists():
        flip = json.loads(fp.read_text())["rows"]
        lines = ["| `n` | `c^{sf}` (first half; symmetric under chain reversal) | `min_j c_j / d_j` | sets `T` with budget below `D_max` | pairs enumerated | violations | worst excess |",
                 "|---|---|---|---|---|---|---|"]
        for r in flip:
            n = r["n_torsions"]
            if n < 8:
                continue
            c = r["c_sf"]
            half = c[: (n + 1) // 2]
            assert r["symmetric"]
            ratio = min(c[j] / min(j + 1, n - j) for j in range(n))      # d_j = distance from the nearer end, 1-based
            lines.append(f"| {n} | {', '.join(map(str, half))} | {ratio:.1f} | {r['sets_with_budget_below_Dmax']} | "
                         f"{fmt_int(r['pairs_checked'])} | {r['pairs_violating']} | {r['worst_excess'] if r['pairs_checked'] else '—'} |")
        out["flip"] = "\n".join(lines)
        out["flip_range"] = f"{flip[0]['n_torsions']}…{flip[-1]['n_torsions']}"
        out["flip_all_valid"] = str(all(r["valid_hamming_envelope"] for r in flip))
    # ---- generic (off-lattice) chain ---------------------------------------------------------------
    gp = HERE / "results" / "generic_Sc16.json"
    if gp.exists():
        g = json.loads(gp.read_text())["rows"]
        lines = ["| `n` | `N` | conformations | classes | `L=1`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` | `L=1/5`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` | nearest tie |",
                 "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]

        def gcell(v: dict) -> str:
            return str(v["upper"]) if v["exact"] else f"[{v['lower']}, {v['upper']}]"

        for key in sorted(g, key=int):
            r = g[key]
            c = r["cover"]
            cells = [gcell(c[f"L=1,{k}"]) for k in EPS_KEYS] + [gcell(c[f"L=1/5,{k}"]) for k in EPS_KEYS]
            tie = min(v["nearest_tie"] for v in c.values())
            lines.append(f"| {r['n_torsions']} | {r['n_beads']} | {fmt_int(r['conformations'])} | {fmt_int(r['classes'])} | "
                         + " | ".join(cells) + f" | {tie:.1e} |")
        out["generic"] = "\n".join(lines)
    # ---- THY-REQ-0008, item 6: single-flip constants against Proposition 11.74 and the scaling form ----------
    fp = HERE / "results" / "lattice_Sc12_flip.json"
    if fp.exists():
        flip = sorted(json.loads(fp.read_text())["rows"], key=lambda r: r["n_torsions"])
        lines = ["| `n` | `j` with `d_j ≥ 5` | least `c_j − (14 d_j − 15)` | largest `c_j / (70 (d_j + 3))` | bound violated |", "|---|---|---|---|---|"]
        total = bad = 0
        for r in flip:
            n, c = r["n_torsions"], r["c_sf"]
            js = [j for j in range(1, n + 1) if min(j, n + 1 - j) >= 5]
            if not js:
                continue
            lo = min(c[j - 1] - (14 * min(j, n + 1 - j) - 15) for j in js)
            hi = max(c[j - 1] / (70 * (min(j, n + 1 - j) + 3)) for j in js)
            v = sum(not (14 * min(j, n + 1 - j) - 15 <= c[j - 1] <= 70 * (min(j, n + 1 - j) + 3)) for j in js)
            total += len(js)
            bad += v
            lines.append(f"| {n} | {len(js)} | {lo} | {hi:.3f} | {v} |")
        lines.append(f"| all | {total} | | | **{bad}** |")
        out["flip_bounds"] = "\n".join(lines)
        ns = [r["n_torsions"] for r in flip if r["n_torsions"] >= 8]
        dmax = max((n + 1) // 2 for n in ns)
        lines = ["| `n` | " + " | ".join(f"`d_j = {d}`" for d in range(1, dmax + 1)) + " |", "|---|" + "---|" * dmax]
        for r in flip:
            n, c = r["n_torsions"], r["c_sf"]
            if n < 8:
                continue
            cells = [f"{c[d - 1] / n:.2f} ({d / n:.2f})" if d <= (n + 1) // 2 else "" for d in range(1, dmax + 1)]
            lines.append(f"| {n} | " + " | ".join(cells) + " |")
        out["flip_scaling"] = "\n".join(lines)
    # ---- THY-REQ-0008, item 5: distance entropy of the generic chain -------------------------------------------
    ep = HERE / "results" / "generic_Sc16_entropy.json"
    if ep.exists():
        e = json.loads(ep.read_text())
        rows_e = e["rows"]
        rhos = [f"{x:g}" for x in e["rhos"]]
        lines = ["| `n` | `N` | conformations | classes | `ln(classes)/n` | pairs within the cutoff per bead: mean over classes / over conformations / max | "
                 + " | ".join(f"`σ(ρ = {x})`" for x in rhos) + " |", "|---|---|---|---|---|---|" + "---|" * len(rhos)]
        for key in sorted(rows_e, key=int):
            r = rows_e[key]
            pb = r["pairs_per_bead"]
            lines.append(f"| {r['n_torsions']} | {r['n_beads']} | {fmt_int(r['conformations'])} | {fmt_int(r['classes'])} | {r['ln_classes_per_torsion']:.3f} | "
                         f"{pb['mean_over_classes']:.2f} / {pb['mean_over_conformations']:.2f} / {pb['max']:.2f} | "
                         + " | ".join(f"{r['sigma'][x]['mean']:.3f}" for x in rhos) + " |")
        out["generic_entropy"] = "\n".join(lines)
        keys = sorted(rows_e, key=int)
        cov = json.loads(gp.read_text())["rows"] if gp.exists() else {}
        pairs = (("L=1,eps=1/4*N", "0.25"), ("L=1,eps=1/2*N", "0.5"), ("L=1/5,eps=1/4*N", "1.25"), ("L=1/5,eps=1/2*N", "2.5"))
        lines = ["| `n → n+1` | growth of the number of classes | "
                 + " | ".join(f"`{k.replace('eps=', 'ε=').replace('*N', ' N').replace(',', ', ')}`: predicted (classes growth / `e^σ`, `ρ = {x}`) / measured" for k, x in pairs) + " |",
                 "|---|---|" + "---|" * len(pairs)]
        for a, b in zip(keys, keys[1:]):
            ra, rb = rows_e[a], rows_e[b]
            g = rb["classes"] / ra["classes"]
            cells = []
            for k, x in pairs:
                pred = g / math.exp(rb["sigma"][x]["mean"])
                if a in cov and b in cov:
                    ca, cb = cov[a]["cover"][k], cov[b]["cover"][k]
                    lo, hi = cb["lower"] / ca["upper"], cb["upper"] / ca["lower"]
                    meas = f"{lo:.2f}" if ca["exact"] and cb["exact"] else f"[{lo:.2f}, {hi:.2f}]"
                else:
                    meas = "—"
                cells.append(f"{pred:.2f} / {meas}")
            lines.append(f"| {a} → {b} | {g:.3f} | " + " | ".join(cells) + " |")
        out["generic_entropy_growth"] = "\n".join(lines)
    return out


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
