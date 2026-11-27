"""All tables of the R10-E1 computation, generated from results/*.json (no number of a table is typed by hand).

    python experiments/eng/weighted_cube/make_tables.py                             # print the blocks
    python experiments/eng/weighted_cube/make_tables.py --out results/tables.txt    # write them to a text file
    python experiments/eng/weighted_cube/make_tables.py --write                     # fill the blocks of REPORT.md
    python experiments/eng/weighted_cube/make_tables.py --verify                    # fail if REPORT.md or the
                                                                                    # stored tables.txt differ

A block is the text between ``<!-- BEGIN name -->`` and ``<!-- END name -->``.  ``--write`` / ``--verify`` act on a
file ``REPORT.md`` in this directory if one exists (a write-up that embeds the blocks); ``--verify`` also checks
``results/tables.txt``.
Rounding: certified upper bounds are rounded up, certified lower bounds down (decimal arithmetic on the stored
12-decimal strings); ratios to the cube are upper bound / lower end of the cube, rounded up (lower bound / upper
end of the cube, rounded down, for the lower bounds of the 5-site block).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
REPORT = HERE / "REPORT.md"
PS = ["0.45", "0.4", "0.3", "0.2", "0.1"]
US = ["0.5", "1", "1.5", "2", "2.5", "3", "4", "6"]


def load(name):
    f = RES / name
    return json.loads(f.read_text()) if f.exists() else None


def up(x, nd=6):
    return str(Decimal(str(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_CEILING))


def dn(x, nd=6):
    return str(Decimal(str(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_FLOOR))


def rn(x, nd=4):
    return str(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_EVEN))


def ratio_up(num, den, nd=4):
    return str((Decimal(num) / Decimal(den)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_CEILING))


def ratio_dn(num, den, nd=4):
    return str((Decimal(num) / Decimal(den)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_FLOOR))


def cells_of(L):
    out = {}
    for name in sorted(RES.glob(f"bounds_L{L}*.json")):
        d = json.loads(name.read_text())
        for c in d["cells"]:
            out[(c["p"], c["u"])] = c
    return out


def sp(n) -> str:
    """Integer with thin thousands separators (spaces)."""
    return f"{int(n):,}".replace(",", " ")


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def block_enumeration():
    rows = []
    for L in (1, 2, 3, 4, 5):
        d = load(f"chambers_L{L}.json")
        if d is None:
            continue
        for st in d["stopped"]:
            rows.append([str(L), str(d["dimension"]), str(d["inequalities"]), f"just above `{st['just_above_wall']}` (at `{st['r0']}`)",
                         f"**stopped** at {st['vertices_found']:,} found".replace(",", " "), f"{st['orbits_found']:,} found".replace(",", " "),
                         "—", "—", "—"])
        for e in d["chambers"]:
            rows.append([str(L), str(d["dimension"]), str(d["inequalities"]), f"`({e['lo']}, {e['hi']})`",
                         f"{e['n_vertices']:,}".replace(",", " "), f"{e['n_orbits']:,}".replace(",", " "),
                         f"{e['degree_min']} / {rn(e['degree_mean_over_vertices'], 1)} / {e['degree_max']}",
                         f"{e['vertices_ending_at_lo']:,} / {e['vertices_ending_at_hi']:,}".replace(",", " "),
                         "`" + e.get("sha256_multiset", "")[:16] + "…`"])
    return table(["`L`", "dim", "ineq.", "chamber of `r = u*/u`", "vertices", "orbits", "degree min / mean / max",
                  "vertices ending at lower / upper wall", "checksum"], rows)


def block_walls():
    rows = []
    for L in (3, 4, 5):
        d = load(f"chambers_L{L}.json")
        if d is None:
            continue
        for w in d["wall_checks"]:
            rows.append([str(L), f"`{w['wall']}`", sp(w["vertices_surviving"]), sp(w["orbits_surviving"]),
                         "yes" if w["same_set"] else "NO"])
    return table(["`L`", "wall", "vertices that exist on both sides", "orbits", "same orbits found by the two enumerations"], rows)


def block_validation():
    c = cells_of(3)[("0.3", "3")]
    a = c["a"]
    lines = [f"* vertices of the 3-site block at `(p, u) = (0.3, 3)`: **{c['n_vertices']}** (chamber `({c['chamber'][0]}, {c['chamber'][1]})`; "
             f"`u* = {c['ustar']}`, `u*/u = {c['ratio']}`);",
             f"* capacity of the block, all {a['n_interval_evaluations']} vertices in interval arithmetic: "
             f"`{dn(Decimal(a['lower']) * 3, 11)} <= cap_3 <= {up(Decimal(a['upper']) * 3, 11)}`, per site "
             f"**`{a['lower']} <= cap_3/3 <= {a['upper']}`** (certified; the two ends agree to the 12 decimals stored);",
             f"* the request's `a <= 3 x 0.495806` is this bound per block: `{a['upper']}` rounded up to six decimals is `{up(a['upper'], 6)}`;",
             f"* the cube: `a_cube(3)` in `[{c['cube']['a_lo']}, {c['cube']['a_hi']}]`; ratio of the bound to the cube `<= {ratio_up(a['upper'], c['cube']['a_lo'])}`."]
    return "\n".join(lines)


def block_bounds(kind, Ls=(3, 4)):
    cm = {L: cells_of(L) for L in Ls}
    rows = []
    for p in PS:
        row = [f"`{p}`"]
        for u in US:
            parts = []
            for L in Ls:
                c = cm[L][(p, u)]
                q = c[kind]
                mark = "**" if q["below_cube"] else ""
                parts.append(f"{mark}{up(q['upper'])}{mark} ({ratio_up(q['upper'], c['cube'][kind + '_lo'])})")
            row.append(" / ".join(parts))
        rows.append(row)
    cube = ["cube"] + [dn(cm[Ls[0]][(PS[0], u)]["cube"][kind + "_lo"]) for u in US]
    head = (f"`{kind}`: certified upper bound per site with blocks of `L = {Ls[0]}` / `L = {Ls[1]}` sites (in brackets: ratio to the "
            "cube, rounded up); bold = certified below the cube; last row: the cube (closed form, rounded down)")
    return head + "\n\n" + table(["`p` \\ `u`"] + [f"`{u}`" for u in US], rows + [cube])


def status_of(kind, p, u, cm, quoted, partial):
    """B3 / B4 / B5: certified below the cube, first block length that shows it; A: above (quoted from the science
    division's map), A*: the same with its mark R*; U-: undecided and L = 5 provably cannot decide; U?: undecided,
    L = 5 open; U: undecided also with the complete L = 5 block."""
    qv = quoted["map_" + kind][f"{p},{u}"]["verdict"]
    for L in (3, 4, 5):
        c = cm.get(L, {}).get((p, u))
        if c is not None and c.get("chamber") is not None and c[kind]["below_cube"]:
            if qv in ("R", "R*"):
                return f"**CONFLICT** (B{L} here, above in the quoted map)"
            return f"**B{L}**"
    if qv in ("R", "R*"):
        return "A" if qv == "R" else "A*"
    pc = partial.get((p, u))
    if pc is not None and kind in pc:
        return "U-" if pc[kind]["block_cannot_show_below_cube"] else "U?"
    return "U"


def partial_cells():
    d = load("partial_L5.json")
    return {} if d is None else {(c["p"], c["u"]): c for c in d["cells"]}


def block_status(kind):
    cm = {L: cells_of(L) for L in (3, 4, 5)}
    quoted = load("quoted_science_L3.json")
    partial = partial_cells()
    rows = [[f"`{p}`"] + [status_of(kind, p, u, cm, quoted, partial) for u in US] for p in PS]
    return table(["`p` \\ `u`"] + [f"`{u}`" for u in US], rows)


def block_L5():
    rows = []
    c5 = cells_of(5)
    for (p, u), c in sorted(c5.items(), key=lambda kv: (PS.index(kv[0][0]), US.index(kv[0][1]))):
        if c.get("chamber") is None:
            continue
        a, h = c["a"], c["h"]
        rows.append([f"`({p}, {u})`", f"`({c['chamber'][0]}, {c['chamber'][1]})`", f"{c['n_vertices']:,}".replace(",", " "),
                     f"[{dn(a['lower'])}, {up(a['upper'])}]", ratio_up(a["upper"], c["cube"]["a_lo"]),
                     f"[{dn(h['lower'])}, {up(h['upper'])}]", ratio_up(h["upper"], c["cube"]["h_lo"]), a["method"]])
    return table(["`(p, u)`", "chamber", "vertices", "`a`: certified bracket of `cap_5/5`", "upper / cube",
                  "`h`: certified bracket of `sup_t F*/5`", "upper / cube", "method"], rows)


def block_partial(kind):
    partial = partial_cells()
    key = "lower_bound_of_block_capacity" if kind == "a" else "lower_bound_of_block_sup"
    rows = []
    for p in PS:
        row = [f"`{p}`"]
        for u in US:
            c = partial.get((p, u))
            if c is None or kind not in c:
                row.append("(enumerated)" if c is None else "—")
                continue
            q = c[kind]
            mark = "**" if q["block_cannot_show_below_cube"] else ""
            row.append(f"{mark}{dn(q[key])}{mark} ({ratio_dn(q[key], c['cube'][kind + '_hi'])})")
        rows.append(row)
    return table(["`p` \\ `u`"] + [f"`{u}`" for u in US], rows)


def block_partial_search_full():
    d = load("partial_L5.json")
    rows = []
    for c in d["cells"]:
        s = c["search"]
        rows.append([f"`({c['p']}, {c['u']})`", c["ratio"][:8], f"`{s['r0']}`", sp(s["vertices_found"]), sp(s["orbits_found"]),
                     str(s["orbits_processed"]), sp(s["vertices_valid_at_cell"]), sp(c["a"]["neighbours_examined"]),
                     str(c["a"]["improving_neighbours_added"]), str(c["h"]["improving_neighbours_added"]) if "h" in c else "—",
                     "yes" if abs(c["a"]["partial_optimum_float"] - c["a"]["sitewise_float"]) < 1e-10 else "no"])
    return table(["`(p, u)`", "`u*/u`", "search at", "vertices found at the stop", "orbits found", "orbits processed",
                  "of these, vertices at the cell", "neighbours of the support examined (`a`)", "improving neighbours (`a`)",
                  "improving neighbours (`h`)", "optimum of the part = site-wise optimum (`a`)"], rows)


def block_partial_search():
    d = load("partial_L5.json")
    groups = {}
    for c in d["cells"]:
        s = c["search"]
        groups.setdefault((s["vertices_found"], s["orbits_found"], s["orbits_processed"]), []).append(c)
    lines = []
    for (vf, of, op), cells in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        valid = sorted({c["search"]["vertices_valid_at_cell"] for c in cells})
        lines.append(f"* {len(cells)} cells (`u*/u` from {min(float(c['ratio']) for c in cells):.4f} to {max(float(c['ratio']) for c in cells):.4f}): "
                     f"search stopped with {sp(vf)} vertices in {sp(of)} orbits found ({op} processed); vertices of the cell's own "
                     f"polytope among them (a rigorous lower bound of its number of vertices): {sp(valid[0])}"
                     + ("" if len(valid) == 1 else f" to {sp(valid[-1])}") + ";")
    nb = [c["a"]["neighbours_examined"] for c in d["cells"]]
    sw_equal = [c for c in d["cells"] if abs(c["a"]["partial_optimum_float"] - c["a"]["sitewise_float"]) < 1e-10]
    not_equal = [f"`({c['p']}, {c['u']})`" for c in d["cells"] if c not in sw_equal]
    lines.append(f"* neighbours of the support examined per cell (`a`): {sp(min(nb))} to {sp(max(nb))}; improving neighbours found: "
                 f"{sum(c['a']['improving_neighbours_added'] for c in d['cells'])} (`a`), "
                 f"{sum(c['h']['improving_neighbours_added'] for c in d['cells'] if 'h' in c)} (`h`);")
    lines.append(f"* the optimum over the part equals the optimum over the 32 site-wise labels in {len(sw_equal)} of {len(d['cells'])} cells"
                 + (f" (all cells with `p >= 0.3`); it is larger at {', '.join(not_equal)}." if not_equal else "."))
    return "\n".join(lines)


def block_crossover():
    d = load("crossover.json")
    rows = []
    for r in d["rows"]:
        if not r["crossings"]:
            first = r["sign_table"][0][0]
            last = r["sign_table"][-1][0]
            rows.append([str(r["L"]), f"`{r['p']}`", f"`{r['kind']}`", f"none: above the cube at every tabulated slope in `[{first:g}, {last:g}]`", "—", "—"])
            continue
        for c in r["crossings"]:
            nd, bl = c["not_decided_at"], c["below_at"]
            word = "downwards" if c["direction"] == "down" else "upwards"
            rows.append([str(r["L"]), f"`{r['p']}`", f"`{r['kind']}`", f"`{c['numerical_crossing']:.3f}` ({word})",
                         f"`u = {bl['u']}`: `{up(bl['upper'], 9)} < {dn(bl['cube_lo'], 9)}`" if bl["below_cube"] else f"`u = {bl['u']}`: not certified",
                         (f"`u = {nd['u']}`: `{dn(nd['lower'], 9)} > {up(nd['cube_hi'], 9)}`" if nd["lower_end_above_cube"]
                          else f"`u = {nd['u']}`: bracket `[{dn(nd['lower'], 9)}, {up(nd['upper'], 9)}]` contains the cube's `{up(nd['cube_hi'], 9)}`")])
    return table(["`L`", "`p`", "exponent", "bound crosses the cube at `u ≈` (numerical)", "certified below the cube at",
                  "block quantity certified above the cube at"], rows)


def block_sitewise():
    d = load("sitewise.json")
    cm = {(c["p"], c["u"]): c for c in d["cells"]}
    rows1, rows2 = [], []
    for p in PS:
        r1, r2 = [f"`{p}`"], [f"`{p}`"]
        for u in US:
            c = cm[(p, u)]
            fb = c["first_L_with_sitewise_below_cube"]
            if fb is not None:
                r1.append(str(fb))
            elif c["extrapolated_first_L"] is not None:
                r1.append(f"> {d['Lmax']} (≈ {c['extrapolated_first_L']})")
            else:
                r1.append("none")
            r2.append(rn(c["last_increment_ratio_to_cube"], 4))
        rows1.append(r1)
        rows2.append(r2)
    t1 = ("shortest block length `L` with (site-wise optimum)`/L <` cube; shorter blocks cannot show `a` below the cube "
          f"(`> {d['Lmax']} (≈ n)`: none up to `L = {d['Lmax']}`, `n` extrapolated; `none`: the increment itself is above the cube)\n\n"
          + table(["`p` \\ `u`"] + [f"`{u}`" for u in US], rows1))
    t2 = (f"increment `sw_{d['Lmax']} - sw_{d['Lmax'] - 1}` of the site-wise optimum divided by the cube's `a` (numerical indication of "
          "`a_inf / a_cube` where site-wise labels are optimal; not a bound)\n\n" + table(["`p` \\ `u`"] + [f"`{u}`" for u in US], rows2))
    rows3 = [[f"`{c['p']}`", "—" if c["increment_exact_L3_to_L4"] is None else f"{c['increment_exact_L3_to_L4']:.2f}",
              "—" if c["increment_sitewise_L6_to_L7"] is None else f"{c['increment_sitewise_L6_to_L7']:.2f}"]
             for c in d["increment_crossings"]]
    t3 = ("slope at which the increment of the block capacity crosses the cube's `a` (numerical; search interval `[1, 3]`)\n\n"
          + table(["`p`", "exact capacities, `cap_4 - cap_3`", "site-wise optima, `sw_7 - sw_6`"], rows3))
    return "\n\n".join([t1, t2, t3])


def block_increments():
    cm = {L: cells_of(L) for L in (2, 3, 4)}
    rows = []
    for p in PS:
        row = [f"`{p}`"]
        for u in US:
            c3, c4 = cm[3][(p, u)], cm[4][(p, u)]
            inc = 4 * c4["a"]["float_lower"] - 3 * c3["a"]["float_lower"]
            row.append(rn(inc / float(c4["cube"]["a_lo"]), 4))
        rows.append(row)
    return table(["`p` \\ `u`"] + [f"`{u}`" for u in US], rows)


def block_compare():
    q = load("quoted_science_L3.json")
    c3 = cells_of(3)
    da, dh, dg = [], [], []
    for r in q["rows"]:
        c = c3[(r["p"], r["u"])]
        da.append(abs(float(c["a"]["upper"]) - float(r["a_upper_L3"])))
        dg.append(c["h"]["float_lower"] - float(r["h_gridmax_L3"]))
        dh.append(float(r["h_upper_L3"]) - float(c["h"]["upper"]))
    lines = [f"* `a`, {len(da)} cells: largest `|ours - theirs|` = `{max(da):.1e}` (their values have six decimals);",
             f"* `h`, their largest dual value on a grid of step 0.005 against our lower end `max_t G_t(M_t)`: ours - theirs in "
             f"`[{min(dg):.1e}, {max(dg):.1e}]`;",
             f"* `h`, their upper bound (interval rule on that grid) minus ours (refined grid): in `[{min(dh):.1e}, {max(dh):.1e}]`"
             + (" — ours is smaller in every cell." if min(dh) > 0 else " — ours is larger in some cell.")]
    return "\n".join(lines)


def block_crosschecks():
    d = load("crosschecks.json")
    small = d["small"]
    methods = sorted(set(m for r in small for m in r["methods"]))
    lines = [f"* `L <= 3`, {len(small)} weight vectors (" + ", ".join(f"`{tuple(r['weights'])}`: {r['n_vertices']}" for r in small)
             + f" vertices): the methods {', '.join(methods)} give "
             + ("identical vertex sets in every case" if all(r["all_equal"] for r in small) else "DIFFERENT SETS")
             + "; every vertex passes the exact rank test."]
    for r in d["four"]:
        lines.append(f"* `L = 4`, chamber `({r['chamber'][0]}, {r['chamber'][1]})`, {sp(r['n_vertices'])} vertices: "
                     + ("identical to the vertex set of the Parma Polyhedra Library" if r.get("ppl_same_set") else "PPL not available")
                     + ("; orbits, stabilisers and degrees identical to the reference implementation." if r["reference_orbits_same"]
                        else "; REFERENCE IMPLEMENTATION DIFFERS."))
    f = d["five"]
    lines.append(f"* uniform 5-cube: {sp(f['uniform_cube']['n_vertices'])} vertices in {f['uniform_cube']['n_orbits']} orbits "
                 f"(known number of height functions: {sp(f['uniform_cube']['expected'])}).")
    for r in f["chambers"]:
        s = (f"* `L = 5`, chamber `({r['chamber'][0]}, {r['chamber'][1]})`: all {sp(r['closure_neighbours_checked'])} neighbours of "
             f"{r['closure_sample_orbits']} representatives (the three of largest degree and 40 random ones) recomputed with the "
             f"reference implementation lie in the enumerated orbits; {r['rank_test_sample']} random representatives pass the exact "
             f"rank test")
        if "equals_2_times_990_squared" in r:
            s += "; the count equals `2 x 990^2`"
        lines.append(s + ".")
    return "\n".join(lines)


def block_optimal_support():
    lines = []
    for L in (3, 4):
        cm = cells_of(L)
        exc = [(p, u, cm[(p, u)]["a"]["sitewise_float"] / cm[(p, u)]["a"]["float_lower"]) for p in PS for u in US
               if not cm[(p, u)]["a"]["sitewise_is_optimal"]]
        ok_p = [p for p in PS if all(cm[(p, u)]["a"]["sitewise_is_optimal"] for u in US)]
        lines.append(f"* `L = {L}`: the capacity is attained by the `2^L` site-wise labels alone in {40 - len(exc)} of 40 cells (all cells "
                     f"with `p` in {{{', '.join(ok_p)}}}); exceptions (site-wise optimum / capacity): "
                     + ", ".join(f"`({p}, {u})` {rn(x, 5)}" for p, u, x in exc) + ".")
    return "\n".join(lines)


BLOCKS = {
    "enumeration": block_enumeration,
    "walls": block_walls,
    "validation": block_validation,
    "bounds_a": lambda: block_bounds("a"),
    "bounds_h": lambda: block_bounds("h"),
    "status_a": lambda: block_status("a"),
    "status_h": lambda: block_status("h"),
    "L5_complete": block_L5,
    "L5_partial_a": lambda: block_partial("a"),
    "L5_partial_h": lambda: block_partial("h"),
    "L5_partial_search": block_partial_search,
    "L5_partial_search_full": block_partial_search_full,
    "crossover": block_crossover,
    "increments": block_increments,
    "sitewise": block_sitewise,
    "optimal_support": block_optimal_support,
    "compare_science": block_compare,
    "crosschecks": block_crosschecks,
}


def render(blocks):
    return "".join(f"<!-- BEGIN {k} -->\n{v}\n<!-- END {k} -->\n\n" for k, v in blocks.items())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--out", type=str, default=None)
    ap.add_argument("--report", type=str, default=None, help="write-up to fill / verify (default: REPORT.md here)")
    ap.add_argument("--only", type=str, nargs="*")
    args = ap.parse_args()
    global REPORT
    if args.report:
        REPORT = Path(args.report)
    blocks = {k: f() for k, f in BLOCKS.items() if not args.only or k in args.only}
    if args.out:
        out = Path(args.out)
        out = out if out.is_absolute() else HERE / out
        out.write_text(render(blocks))
        print(f"wrote {len(blocks)} blocks to {out.relative_to(HERE)}")
    if not (args.write or args.verify):
        if not args.out:
            print(render(blocks), end="")
        return
    bad = []
    stored = RES / "tables.txt"
    if args.verify and stored.exists() and stored.read_text() != render({k: f() for k, f in BLOCKS.items()}):
        bad.append("results/tables.txt differs from the results")
    found = 0
    if REPORT.exists():
        text = REPORT.read_text()
        for k, v in blocks.items():
            pat = re.compile(rf"(<!-- BEGIN {k} -->\n)(.*?)(<!-- END {k} -->)", re.S)
            m = pat.search(text)
            if not m:
                continue                      # the write-up may embed a subset of the blocks
            found += 1
            if args.write:
                text = text[:m.start(2)] + v + "\n" + text[m.end(2):]
            elif m.group(2) != v + "\n":
                bad.append(f"block {k} of {REPORT.name} differs from the results")
        if args.write:
            REPORT.write_text(text)
        if found == 0:
            bad.append(f"no block markers in {REPORT.name}")
    elif args.write:
        bad.append(f"no write-up at {REPORT.name}")
    if bad:
        print("\n".join(bad))
        sys.exit(1)
    print("%d generated blocks; %d %s in the write-up" % (len(blocks), found, "written" if args.write else "verified"))


if __name__ == "__main__":
    main()
