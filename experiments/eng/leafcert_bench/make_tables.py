"""Every table of the benchmark report, regenerated from the stored results.

    python experiments/eng/leafcert_bench/make_tables.py             # print the tables and write results/tables.txt
    python experiments/eng/leafcert_bench/make_tables.py --verify    # exit status 1 if results/tables.txt is not
                                                                     # what the result files give
    options: --results DIR (default: results next to this file)

Conventions.  Times are wall-clock seconds on a shared machine and are noisy; "med [min-max]" is the median
and the range over the instances named in the column header.  Producer times are over the certified
instances of a cell, baseline times over the instances the baseline solved.  "a/b" is "a of the b attempted".
A cell marked ``ext`` is an extension cell (the producer had stopped on the ladder; baselines on 3 instances).
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import config  # noqa: E402


# ================================================================================================ formatting
def med(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def num(x, digits=3):
    """A number with ``digits`` significant digits, integers in full."""
    if x is None:
        return "-"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, int) or (isinstance(x, float) and x.is_integer() and abs(x) < 1e15):
        return f"{int(x)}"
    if x == 0:
        return "0"
    return f"{x:.{max(0, digits - 1 - int(math.floor(math.log10(abs(x)))))}f}" if abs(x) < 10 ** digits else f"{x:.0f}"


def big(x):
    """Counts: 12345 -> 12.3k, 1234567 -> 1.23M."""
    if x is None:
        return "-"
    x = float(x)
    for unit, scale in (("G", 1e9), ("M", 1e6), ("k", 1e3)):
        if abs(x) >= scale:
            return f"{num(x / scale)}{unit}"
    return num(x)


def sec(x):
    if x is None:
        return "-"
    if x < 0.00095:
        return f"{1e6 * x:.0f}us"
    if x < 0.0995:
        return f"{1000 * x:.1f}ms" if x < 0.00995 else f"{1000 * x:.0f}ms"
    return f"{x:.2f}s" if x < 9.995 else f"{x:.1f}s"


def mr(values, fmt=num):
    """median [min-max]"""
    values = [v for v in values if v is not None]
    if not values:
        return "-"
    lo, hi = min(values), max(values)
    if lo == hi:
        return fmt(lo)
    return f"{fmt(statistics.median(values))} [{fmt(lo)}-{fmt(hi)}]"


def table(title, header, rows, out, note=None):
    out.append("")
    out.append(title)
    if note:
        out.extend(note if isinstance(note, list) else [note])
    if not rows:
        out.append("  (no data)")
        return
    cells = [list(map(str, header))] + [list(map(str, row)) for row in rows]
    widths = [max(len(row[c]) for row in cells) for c in range(len(header))]
    for r, row in enumerate(cells):
        out.append("  " + "  ".join(row[c].ljust(widths[c]) if c == 0 else row[c].rjust(widths[c]) for c in range(len(row))).rstrip())
        if r == 0:
            out.append("  " + "  ".join("-" * w for w in widths))


# ================================================================================================ data
def load(folder):
    docs = {}
    if folder.is_dir():
        for path in sorted(folder.glob("*.json")):
            if path.name.startswith("_"):
                continue
            docs[path.stem] = json.loads(path.read_text())
    return docs


def run_log(folder):
    path = folder / "_run.json"
    return json.loads(path.read_text()) if path.exists() else None


def ladder_cells(main, family, k):
    return [main[name] for n in config.SIZES[family] for name in [config.cell_name(family, k, n)] if name in main]


def certified(doc):
    return [r for r in doc["instances"] if r.get("producer", {}).get("status") == "certified"]


def rel_gap(rec):
    opt, lp = rec["agreement"]["optimum"], rec["root_lp"]["value"]
    if opt is None or lp is None:
        return None
    return (opt - lp) / max(1.0, abs(opt))


# ================================================================================================ the main pass
def main_tables(main, out):
    out.append("")
    out.append("=" * 110)
    out.append("MAIN PASS, cell by cell: producer (bound mp, branching strong) with caps "
               f"{config.CAPS['max_cert_integers']:,} integers / {config.CAPS['max_check_ops']:,} checker operations, "
               f"time limit {config.TIME_LIMIT:.0f} s")
    out.append("=" * 110)
    for family in config.FAMILY_ORDER:
        rows_a, rows_b, rows_c = [], [], []
        for k in config.ALPHABETS:
            for doc in ladder_cells(main, family, k):
                recs = doc["instances"]
                prod = [r["producer"] for r in recs if "producer" in r]
                ok = [p for p in prod if p["status"] == "certified"]
                label = [k, f"{doc['n']}" + (" ext" if doc["task"].get("extension") else "")]
                if doc.get("error"):
                    rows_a.append(label + [len(recs), "ERROR"] + ["-"] * 9)
                    continue
                stops = [p["stats"]["stop"] for p in prod if p["status"] != "certified"]
                fails = "/".join(str(stops.count(name)) for name in ("cert_integers", "check_ops", "time", "leaves"))
                gaps = [rel_gap(r) for r in recs]
                tight = sum(1 for g in gaps if g is not None and g < 1e-9)
                rows_a.append(label + [
                    len(recs), f"{len(ok)}/{len(prod)}" if prod else "-", fails if prod else "-",
                    sum(p["stats"]["leaf_boxes"] == 1 for p in ok) if prod else "-",
                    mr([p["stats"]["leaf_boxes"] for p in ok]), mr([p["stats"]["leaf_certificates"] for p in ok]),
                    mr([p["stats"]["depth"] for p in ok]), mr([p["stats"]["cert_integers"] for p in ok], big),
                    mr([p.get("json_bytes") for p in ok], big),
                    f"{tight}/{sum(g is not None for g in gaps)}",
                    mr([None if g is None else 100 * g for g in gaps], lambda v: f"{v:.1f}")])
                plain = [r["plain"] for r in recs if "plain" in r]
                plain_ok = [p for p in plain if p["status"] == "optimal"]
                rows_b.append(label + [
                    mr([p["stats"]["time_search"] for p in ok], sec), mr([p["stats"]["time_assemble"] for p in ok], sec),
                    mr([p["stats"]["time_check_c"] for p in ok], sec), mr([p["stats"]["time_check_python"] for p in ok], sec),
                    mr([p.get("c_kernel_seconds") for p in ok], sec), mr([p["seconds"] for p in ok], sec),
                    num(max([p["peak_rss_mb"] for p in prod if p.get("peak_rss_mb")] or [None]))])
                row = label + [f"{len(plain_ok)}/{len(plain)}" if plain else "-", mr([p["seconds"] for p in plain_ok], sec),
                               mr([p.get("leaf_boxes") for p in plain_ok])]
                for name in ("dp", "brute"):
                    got = [r[name] for r in recs if r.get(name, {}).get("status") == "optimal"]
                    row += [f"{len(got)}/{len(recs)}", mr([g["seconds"] for g in got], sec)]
                for name in ("cpsat", "milp"):
                    got = [r[name] for r in recs if name in r]
                    solved = [g for g in got if g["status"] == "optimal"]
                    row += [f"{len(solved)}/{len(got)}" if got else "-", mr([g["seconds"] for g in solved], sec)]
                rows_c.append(row)
        if not rows_a:
            continue
        title = f"--- {family} ---"
        table(f"{title}  (A) certification: instances, certified, failures by cause (integer cap / operation cap / 60 s / leaf "
              "boxes), instances with one leaf; over the certified instances: leaf boxes, distinct leaf certificates, depth, "
              "integers of the leaf certificates, bytes of the JSON; instances whose relaxation is tight at the root; "
              "(optimum - relaxation) / |optimum| in %",
              ["k", "n", "inst", "certified", "fail i/o/t/l", "1-leaf", "leaf boxes", "leaf certs", "depth", "cert integers",
               "JSON bytes", "LP tight", "root gap %"], rows_a, out)
        table(f"{title}  (B) times of the producer over the certified instances: search, assembling, check(obj, 'c'), "
              "check(obj, 'python'), leafcert.c alone, total; largest peak resident memory of a producer run in MB",
              ["k", "n", "search", "assemble", "check C", "check Python", "C kernel", "total", "peak MB"], rows_b, out)
        table(f"{title}  (C) solving without a certificate (solved/attempted; time and leaf boxes over the solved): the "
              "same search without certificate, dynamic programming, enumeration, CP-SAT, MILP",
              ["k", "n", "search", "time", "leaf boxes", "DP", "time", "brute", "time", "CP-SAT", "time", "MILP", "time"],
              rows_c, out)


def m1(values, fmt=num):
    """median only"""
    values = [v for v in values if v is not None]
    return fmt(statistics.median(values)) if values else "-"


def report_tables(main, out):
    """One compact table per family: what the report quotes."""
    out.append("")
    out.append("=" * 110)
    out.append("COMPACT TABLES PER FAMILY (medians; ranges where they matter; everything else is in the cell tables below)")
    out.append("  cert = certified / producer runs;  1L = certified with one leaf;  boxes, certs, ints (integers of the leaf")
    out.append("  certificates), bytes (JSON) and the producer's times are over the certified instances;  produce = search +")
    out.append("  assembling;  chk C / chk Py = check(obj, engine);  search = the same search without certificate (solved/run,")
    out.append("  median time over the solved);  DP, CP-SAT, MILP: solved/run and median time over the solved;  ext = extension cell")
    out.append("=" * 110)
    for family in config.FAMILY_ORDER:
        rows = []
        for k in config.ALPHABETS:
            for doc in ladder_cells(main, family, k):
                recs = doc["instances"]
                prod = [r["producer"] for r in recs if "producer" in r]
                ok = [p for p in prod if p["status"] == "certified"]
                if doc.get("error"):
                    rows.append([k, doc["n"], "ERROR"] + ["-"] * 13)
                    continue
                plain = [r["plain"] for r in recs if "plain" in r]
                plain_ok = [p for p in plain if p["status"] == "optimal"]

                def solved(name):
                    got = [r[name] for r in recs if name in r and r[name]["status"] != "skipped"]
                    good = [g for g in got if g["status"] == "optimal"]
                    return f"{len(good)}/{len(got)} {m1([g['seconds'] for g in good], sec)}" if got else "-"

                rows.append([
                    k, f"{doc['n']}" + (" ext" if doc["task"].get("extension") else ""),
                    f"{len(ok)}/{len(prod)}" if prod else "-", sum(p["stats"]["leaf_boxes"] == 1 for p in ok) if prod else "-",
                    mr([p["stats"]["leaf_boxes"] for p in ok]), m1([p["stats"]["leaf_certificates"] for p in ok]),
                    m1([p["stats"]["cert_integers"] for p in ok], big), m1([p.get("json_bytes") for p in ok], big),
                    mr([p["stats"]["time_search"] + p["stats"]["time_assemble"] for p in ok], sec),
                    m1([p["stats"]["time_check_c"] for p in ok], sec), m1([p["stats"]["time_check_python"] for p in ok], sec),
                    f"{len(plain_ok)}/{len(plain)} {m1([p['seconds'] for p in plain_ok], sec)}" if plain else "-",
                    m1([p.get("leaf_boxes") for p in plain_ok]),
                    solved("dp"), solved("cpsat"), solved("milp")])
        table(f"--- {family} ---", ["k", "n", "cert", "1L", "leaf boxes", "certs", "ints", "bytes", "produce", "chk C",
                                     "chk Py", "search", "its boxes", "DP", "CP-SAT", "MILP"], rows, out)


def overview(main, out, log=None):
    ended = {}
    if log:
        for family, k, _ in log.get("stopped_by_rule", []):
            ended[(family, str(k))] = "stop rule"
        for family, k, _ in log.get("not_started_budget", []):
            ended[(family, str(k))] = "BUDGET"
    rows = []
    totals = {"cells": 0, "instances": 0, "attempted": 0, "certified": 0}
    for family in config.FAMILY_ORDER:
        for k in config.ALPHABETS:
            docs = ladder_cells(main, family, k)
            if not docs:
                continue
            reach, first_fail, single_max = None, None, None
            attempted = cert = 0
            for doc in docs:
                prod = [r["producer"] for r in doc["instances"] if "producer" in r]
                ok = [p for p in prod if p["status"] == "certified"]
                totals["cells"] += 1
                totals["instances"] += len(doc["instances"])
                attempted += len(prod)
                cert += len(ok)
                if prod and len(ok) == len(prod):
                    reach = doc["n"]
                if prod and len(ok) < len(prod) and first_fail is None:
                    first_fail = f"{doc['n']} ({len(ok)}/{len(prod)})"
                if prod and all(p["stats"]["leaf_boxes"] == 1 for p in ok) and len(ok) == len(prod):
                    single_max = doc["n"]
            totals["attempted"] += attempted
            totals["certified"] += cert
            last = docs[-1]
            rows.append([family, k, " ".join(str(d["n"]) + ("e" if d["task"].get("extension") else "") for d in docs),
                         f"{cert}/{attempted}", reach or "-", first_fail or "-", single_max or "-",
                         "last size" if last["n"] == config.SIZES[family][-1] else ended.get((family, str(k)), "?")])
    table("OVERVIEW: per ladder, the sizes run (e = extension cell: baselines only, 3 instances); producer runs certified; "
          "the largest n with all 10 certified; the first n with a failure (certified/10); the largest n at which every "
          "instance needed one leaf only; why the ladder ended (last size reached / stop rule: neither the producer nor "
          "the search was left / BUDGET: the cell was not started)",
          ["family", "k", "sizes run", "certified", "all certified up to", "first failure at", "one leaf up to", "ended by"],
          rows, out)
    out.append("")
    out.append(f"  cells {totals['cells']}, instances {totals['instances']}, producer runs {totals['attempted']}, "
               f"certified {totals['certified']}")


def consistency(main, compare, out):
    multi = bad = total = 0
    lines = []
    for doc in main.values():
        for rec in doc["instances"]:
            total += 1
            ag = rec["agreement"]
            multi += len(ag["exact_values"]) >= 2
            if not ag["consistent"]:
                bad += 1
                lines.append(f"  INCONSISTENT {doc['family']} k={doc['k']} n={doc['n']} r={rec['index']}: {ag}")
    cbad = sum(not rec["consistent"] for doc in compare.values() for rec in doc["instances"])
    out.append("")
    out.append("CONSISTENCY of exact values (certified L, search without certificate, DP, enumeration, CP-SAT, MILP)")
    out.append(f"  main pass: {total} instances, {multi} with at least two exact values, {bad} inconsistent; "
               f"comparison pass: {cbad} inconsistent")
    out.extend(lines)
    errors = [name for name, doc in list(main.items()) + list(compare.items()) if doc.get("error")]
    out.append(f"  cells that ended in an error: {len(errors)} {errors if errors else ''}")
    rejected = [(name, r["index"]) for name, doc in main.items() for r in doc["instances"]
                if r.get("producer", {}).get("status") == "rejected"]
    out.append(f"  certificates the checker did not accept: {len(rejected)} {rejected if rejected else ''}")


def cost_tables(main, out):
    """What the certificate costs on top of the search, and where the time goes."""
    rows = []
    for family in config.FAMILY_ORDER:
        for label, pick in (("1 leaf", lambda p: p["stats"]["leaf_boxes"] == 1),
                            ("2-100 leaf boxes", lambda p: 1 < p["stats"]["leaf_boxes"] <= 100),
                            (">100 leaf boxes", lambda p: p["stats"]["leaf_boxes"] > 100)):
            ratios, post, share_py, share_c, front = [], [], [], [], []
            for name, doc in main.items():
                if doc["family"] != family:
                    continue
                for rec in doc["instances"]:
                    p = rec.get("producer")
                    q = rec.get("plain")
                    if not p or p["status"] != "certified" or not pick(p):
                        continue
                    s = p["stats"]
                    after = s["time_assemble"] + s["time_check_c"] + s["time_check_python"]
                    post.append(after / max(s["time_search"], 1e-9))
                    share_py.append(s["time_check_python"] / max(after, 1e-9))
                    share_c.append(s["time_check_c"] / max(after, 1e-9))
                    if p.get("c_kernel_seconds") is not None:
                        front.append(1.0 - p["c_kernel_seconds"] / max(s["time_check_c"], 1e-9))
                    if q and q["status"] == "optimal":
                        ratios.append(p["seconds"] / max(q["seconds"], 1e-9))
            if post:
                rows.append([family, label, len(post), mr(ratios, num), mr(post, num), mr(share_py, lambda v: f"{100 * v:.0f}%"),
                             mr(share_c, lambda v: f"{100 * v:.0f}%"), mr(front, lambda v: f"{100 * v:.0f}%")])
    table("COST OF THE CERTIFICATE (certified instances of the main pass, by tree size)",
          ["family", "tree", "instances", "producer / plain search", "(assemble+checks) / search", "Python engine share",
           "C engine share", "of check C: loading+encoding"], rows, out,
          note=["  producer = search + assembling + both engines; plain search = the same search with certificate=False;",
                "  shares are of the time after the search; the last column is the part of check(obj, 'c') spent outside leafcert.c"])


def checking_tables(main, out):
    rows = []
    buckets = ((0, 1e4), (1e4, 1e5), (1e5, 1e6), (1e6, 1e7), (1e7, 1e9))
    for lo, hi in buckets:
        ops, kern, cc, cp, ints = [], [], [], [], []
        for doc in main.values():
            for rec in doc["instances"]:
                p = rec.get("producer")
                if not p or p["status"] != "certified":
                    continue
                o = p["stats"]["check_ops"]
                if lo <= o < hi:
                    ops.append(o)
                    kern.append(p.get("c_kernel_seconds"))
                    cc.append(p["stats"]["time_check_c"])
                    cp.append(p["stats"]["time_check_python"])
                    ints.append(p["stats"]["cert_integers"] + p["stats"]["instance_integers"])
        if ops:
            rows.append([f"{big(lo)} - {big(hi)}", len(ops), mr(ints, big), mr(kern, sec), mr(cc, sec), mr(cp, sec),
                         mr([o / k for o, k in zip(ops, kern) if k], big), mr([o / t for o, t in zip(ops, cp) if t], big)])
    table("CHECKING COST by number of checker operations (additions + comparisons), certified instances of the main pass",
          ["operations", "instances", "integers read", "leafcert.c alone", "check(obj, 'c')", "check(obj, 'python')",
           "ops/s leafcert.c", "ops/s Python engine"], rows, out)


def density_tables(main, out):
    rows = []
    for family in config.FAMILY_ORDER:
        for k in config.ALPHABETS:
            docs = [d for d in ladder_cells(main, family, k) if certified(d)]
            if not docs:
                continue
            doc = docs[-1]
            recs = certified(doc)
            f = [r["producer"]["formats"] for r in recs]
            rows.append([family, k, doc["n"], len(recs),
                         mr([r["dense_instance_integers"] / r["sparse_instance_integers"] for r in recs], num),
                         mr([r["dense_ints_per_leaf"] for r in recs], big), mr([r["sparse_ints_per_leaf"] for r in recs], big),
                         mr([r["dense_ints_per_leaf"] / r["sparse_ints_per_leaf"] for r in recs], num),
                         mr([x["dense"]["check_ops"] / x["sparse"]["check_ops"] for x in f], num),
                         mr([(x["dense"]["cert_integers"] + x["dense"]["instance_integers"])
                             / (x["sparse"]["cert_integers"] + x["sparse"]["instance_integers"]) for x in f], num)])
    table("DENSITY OF THE FORMAT: the dense format against a sparse variant (interacting pairs only), at the largest n "
          "of each ladder with a certified instance", ["family", "k", "n", "instances", "instance: dense/sparse",
                                                       "leaf integers dense", "sparse", "leaf: dense/sparse",
                                                       "checker ops: dense/sparse", "whole file: dense/sparse"], rows, out,
          note="  exact counts; the sparse variant is hypothetical (formats.py says what is counted)")


def dead_data_tables(main, out):
    rows = []
    for k in config.ALPHABETS:
        for label, pick in (("1 leaf", lambda b: b == 1), ("2-100 leaf boxes", lambda b: 1 < b <= 100),
                            (">100 leaf boxes", lambda b: b > 100)):
            total = dead = 0
            frac, split = [], []
            for doc in main.values():
                if doc["k"] != k:
                    continue
                for rec in certified(doc):
                    f = rec["producer"]["formats"]["dense"]
                    if not pick(rec["producer"]["stats"]["leaf_boxes"]) or "message_integers" not in f:
                        continue
                    total += f["message_integers"]
                    dead += f["message_integers_never_read"]
                    frac.append(f["message_integers_never_read"] / max(1, f["message_integers"]))
                    if f.get("check_ops_split_rule"):
                        split.append(f["check_ops"] / f["check_ops_split_rule"])
            if frac:
                rows.append([k, label, len(frac), big(total), big(dead), f"{100 * dead / max(1, total):.1f}%",
                             mr(frac, lambda v: f"{100 * v:.0f}%"), mr(split, num)])
    table("DATA THAT NO INEQUALITY READS, AND REPEATED CHECKS (certified instances of the main pass): message entries "
          "m_ij(a) with the state a outside every box the leaf is used on; checker operations as they are against "
          "operations if a shared leaf were checked once on the union of its boxes (a 'states | other states' rule)",
          ["k", "tree", "instances", "message integers", "never read", "share", "share per instance",
           "ops now / ops with a split rule"], rows, out)


def sharing_tables(main, compare, out):
    rows = []
    for k in config.ALPHABETS:
        boxes = certs = 0
        inst = shared_inst = 0
        ratios = []
        for doc in main.values():
            if doc["k"] != k:
                continue
            for rec in certified(doc):
                s = rec["producer"]["stats"]
                if s["leaf_boxes"] < 2:
                    continue
                inst += 1
                boxes += s["leaf_boxes"]
                certs += s["leaf_certificates"]
                shared_inst += s["leaf_boxes"] > s["leaf_certificates"]
                ratios.append(s["leaf_certificates"] / s["leaf_boxes"])
        if inst:
            rows.append([k, inst, shared_inst, boxes, certs, f"{100 * (1 - certs / boxes):.1f}%", mr(ratios, num)])
    table("SHARED LEAVES (main pass, certified instances with at least two leaf boxes): distinct leaf certificates "
          "against leaf boxes", ["k", "instances", "with sharing", "leaf boxes", "leaf certificates", "saved",
                                 "certs/boxes per instance"], rows, out)
    rows = []
    for name, doc in compare.items():
        a = [r["searches"].get("mp/strong") for r in doc["instances"]]
        b = [r["searches"].get("mp/strong/noshare") for r in doc["instances"]]
        pairs = [(x, y) for x, y in zip(a, b) if x and y and x["status"] == y["status"] == "optimal"]
        if pairs:
            rows.append([doc["family"], doc["k"], doc["n"], len(pairs), mr([x["leaf_certificates"] for x, _ in pairs]),
                         mr([y["leaf_certificates"] for _, y in pairs]),
                         mr([x["leaf_certificates"] / y["leaf_certificates"] for x, y in pairs], num),
                         mr([x["nodes"] / y["nodes"] for x, y in pairs], num)])
    table("SHARED LEAVES (comparison pass): the same search with and without sharing",
          ["family", "k", "n", "instances", "certs with sharing", "certs without", "ratio", "nodes evaluated: ratio"], rows, out)


# ================================================================================================ the comparison pass
def compare_tables(compare, out):
    out.append("")
    out.append("=" * 110)
    out.append("COMPARISON PASS: searches without certificate (same nodes as the producer), time limit "
               f"{config.TIME_LIMIT:.0f} s; instances solved by every configuration of a row group are compared")
    out.append("=" * 110)
    for title, names, base, where in (
            ("LEAF-BOUND METHODS (branching strong; lp/frac: the programme's most fractional site); instances 0-4",
             ["mp/strong", "lp/strong", "hybrid/strong", "lp/frac"], "mp/strong", config.COMPARE_LP_CELLS),
            ("BRANCHING RULES (bound mp); all 10 instances", ["mp/strong", "mp/maxdeg", "mp/margin", "mp/maxdom"],
             "mp/strong", config.COMPARE_RULE_CELLS)):
        rows = []
        for cell in where:
            doc = compare.get(config.cell_name(*cell))
            if not doc or doc.get("error"):
                continue
            recs = [r for r in doc["instances"] if len(names) == 4 and (names[1] in r["searches"])]
            for name in names:
                got = [r["searches"][name] for r in recs if name in r["searches"]]
                if not got:
                    continue
                solved = [g for g in got if g["status"] == "optimal"]
                common = [r for r in recs if name in r["searches"] and base in r["searches"]
                          and r["searches"][name]["status"] == "optimal" and r["searches"][base]["status"] == "optimal"]
                rows.append([f"{doc['family']} k={doc['k']} n={doc['n']}", name, f"{len(solved)}/{len(got)}",
                             mr([g["leaf_boxes"] for g in solved]), mr([g["leaf_certificates"] for g in solved]),
                             mr([g["depth"] for g in solved]), mr([g["nodes"] for g in solved]),
                             mr([g["seconds"] for g in solved], sec),
                             mr([r["searches"][name]["leaf_boxes"] / r["searches"][base]["leaf_boxes"] for r in common], num),
                             mr([r["searches"][name]["seconds"] / max(r["searches"][base]["seconds"], 1e-9) for r in common], num),
                             mr([g["lp_calls"] for g in solved]) if name.split("/")[0] != "mp" else "-"])
        table(title, ["cell", "configuration", "solved", "leaf boxes", "leaf certs", "depth", "nodes", "time",
                      f"boxes / {base}", f"time / {base}", "LP solves"], rows, out)
    rows = []
    for cell in config.COMPARE_CELLS:
        doc = compare.get(config.cell_name(*cell))
        if not doc:
            continue
        for rec in doc["instances"]:
            for name, p in rec.get("certified", {}).items():
                s = p["stats"]
                rows.append([f"{doc['family']} k={doc['k']} n={doc['n']} r={rec['index']}", name, p["status"],
                             s["stop"] or "-", s["leaf_boxes"], s["leaf_certificates"], sec(s["time_search"]),
                             sec(s["time_assemble"] + s["time_check_c"] + s["time_check_python"]),
                             num(s["lp_rounding_loss_root"]) if s["lp_rounding_loss_root"] is not None else "-"])
    table("CERTIFICATES FROM THE LINEAR PROGRAMME (comparison pass, instances 0 and 1, same caps): built and checked",
          ["instance", "configuration", "status", "limit", "leaf boxes", "leaf certs", "search", "assemble+checks",
           "root: LP value - rounded bound"], rows, out)
    rows = []
    for cell in config.COMPARE_CELLS:
        doc = compare.get(config.cell_name(*cell))
        if not doc:
            continue
        losses, tight_fail_lp, tight_fail_mp, tight = [], 0, 0, 0
        for rec in doc["instances"]:
            lp, mp_ = rec["searches"].get("lp/strong"), rec["searches"].get("mp/strong")
            if not lp or lp["root_lp_value"] is None:
                continue
            losses.append(lp["lp_rounding_loss_root"])
            if lp["status"] == "optimal" and lp["value"] - lp["root_lp_value"] < 1e-6:
                tight += 1
                tight_fail_lp += lp["leaf_boxes"] > 1
                tight_fail_mp += bool(mp_ and mp_["status"] == "optimal" and mp_["leaf_boxes"] > 1)
        if losses:
            rows.append([f"{doc['family']} k={doc['k']} n={doc['n']}", len(losses), mr(losses, num), tight, tight_fail_lp, tight_fail_mp])
    table("ROUNDING AT THE ROOT (comparison pass, instances with the lp/strong run): value of the programme minus the "
          "exact value of its rounded multipliers; instances whose relaxation is tight at the root, and how many of "
          "them still needed more than one leaf", ["cell", "instances", "rounding loss", "tight at the root",
                                                   "lp: more than one leaf", "mp: more than one leaf"], rows, out)


def long_tables(long, main, out):
    rows = []
    for name, doc in long.items():
        for rec in doc["instances"]:
            task = doc["task"]
            first = main.get(config.cell_name(doc["family"], doc["k"], doc["n"]))
            before = None
            if first:
                for r in first["instances"]:
                    if r["index"] == rec["index"] and task["solver"] in r:
                        before = r[task["solver"]]
            got = rec.get(task["solver"])
            if got is None:
                rows.append([f"{doc['family']} k={doc['k']} n={doc['n']} r={task['index']}", task["solver"], "ERROR", "-", "-", "-", "-"])
                continue
            if task["solver"] == "producer":
                s = got["stats"]
                detail = (f"{s['leaf_boxes']} boxes, {big(s['cert_integers'])} integers, search {sec(s['time_search'])}, "
                          f"assemble+checks {sec(s['time_assemble'] + s['time_check_c'] + s['time_check_python'])}")
                rows.append([f"{doc['family']} k={doc['k']} n={doc['n']} r={task['index']}", "producer (caps x5)",
                             f"{before['status']} ({before['stats']['stop']})" if before else "-", got["status"],
                             s["stop"] or "-", sec(got["seconds"]), detail])
            else:
                rows.append([f"{doc['family']} k={doc['k']} n={doc['n']} r={task['index']}", task["solver"],
                             before["status"] if before else "-", got["status"], got.get("stop") or "-", sec(got["seconds"]),
                             f"{got.get('leaf_boxes', '-')} leaf boxes" if task["solver"] == "plain" else f"value {got.get('value')}"])
    table(f"SECOND PASS ({config.LONG_TIME_LIMIT:.0f} s; producer with caps {config.LONG_CAPS['max_cert_integers']:,} integers / "
          f"{config.LONG_CAPS['max_check_ops']:,} operations)",
          ["instance", "solver", "at 60 s", f"at {config.LONG_TIME_LIMIT:.0f} s", "limit", "time", "detail"], rows, out)


def exploratory_tables(results, out):
    path = results / "exploratory_integrality.json"
    if not path.exists():
        return
    doc = json.loads(path.read_text())
    rows = []
    for r in doc["rows"]:
        scaled = []
        for factor in ("2", "6"):
            if factor in r["scaled"]:
                v = r["scaled"][factor]
                scaled.append(f"x{factor}: lp {v['lp']['leaf_boxes']} (root {v['lp']['root_value']} vs {int(factor) * r['optimum']}), "
                              f"mp {v['mp']['leaf_boxes']}")
        rows.append([f"{r['family']} k={r['k']} n={r['n']} r={r['index']}", r["optimum"], r["mp"]["root_value"],
                     r["optimum"] - r["mp"]["root_value"], r["mp"]["leaf_boxes"], r["lp"]["root_value"], r["lp"]["leaf_boxes"],
                     "; ".join(scaled) if scaled else "-"])
    table("EXPLORATORY (not in the protocol; integrality_probe.py): certified instances of the main pass whose relaxation is "
          "tight at the root and for which the producer (message passing) needed more than one leaf.  Root bound and leaf "
          "boxes with message passing and with the rounded linear programme; where the rounded programme needs more than one "
          "leaf too, the same with every table multiplied by 2 and by 6 (leaf boxes; root bound against the scaled optimum)",
          ["instance", "optimum", "mp root bound", "short by", "mp leaf boxes", "lp root bound", "lp leaf boxes",
           "tables scaled"], rows, out)


# ================================================================================================ hypotheses
def hypothesis_numbers(main, compare, out):
    out.append("")
    out.append("NUMBERS FOR THE HYPOTHESES OF PROTOCOL.txt (the verdicts are in the report; here are the numbers)")
    pct = lambda v: f"{100 * v:.0f}%"                    # noqa: E731

    def cells(families, ks=config.ALPHABETS, extension=False):
        return [d for d in main.values() if d["family"] in families and d["k"] in ks
                and (extension or not d["task"].get("extension"))]

    def prods(docs):
        return [r["producer"] for d in docs for r in d["instances"] if "producer" in r]

    def counts(family, k):
        """per size: certified/attempted of the producer"""
        return " ".join(f"{d['n']}:{sum(p['status'] == 'certified' for p in prods([d]))}/{len(prods([d]))}"
                        for d in ladder_cells(main, family, k) if prods([d]))

    def plain_median(doc):
        got = [r["plain"]["leaf_boxes"] for r in doc["instances"] if r.get("plain", {}).get("status") == "optimal"]
        full = len(got) == len(doc["instances"])
        return (statistics.median(got) if got else None), full

    # ---- H1
    prod = prods(cells(("chain", "tree")))
    single = sum(p["status"] == "certified" and p["stats"]["leaf_boxes"] == 1 for p in prod)
    top = [r for d in cells(("chain", "tree")) if d["n"] == 100 for r in certified(d)]
    dp_ok = [r for r in top if r["dp"]["status"] == "optimal"]
    out.append(f"  H1  chains and trees: {single} of {len(prod)} producer runs certified with one leaf.  At n = 100 "
               f"({len(top)} instances): producer total {mr([r['producer']['seconds'] for r in top], sec)}; share of it after the "
               f"search {mr([1 - r['producer']['stats']['time_search'] / r['producer']['seconds'] for r in top], pct)}; "
               f"DP {mr([r['dp']['seconds'] for r in dp_ok], sec)}; producer / DP "
               f"{mr([r['producer']['seconds'] / max(r['dp']['seconds'], 1e-9) for r in dp_ok], num)}")
    k10 = [r for r in top if r["alphabets"] == [10]]
    out.append(f"      k = 10, n = 100: producer total {mr([r['producer']['seconds'] for r in k10], sec)}")
    # ---- H2
    for ks, label in (((2,), "k = 2"), ((3, 5, 10, "mixed"), "k >= 3 and mixed")):
        docs = cells(("potts",), ks)
        prod = prods(docs)
        cert = [p for p in prod if p["status"] == "certified"]
        low = [(d["k"], d["n"], sum(p["status"] == "certified" and p["stats"]["leaf_boxes"] == 1 for p in prods([d])))
               for d in docs]
        out.append(f"  H2  Potts, {label}: certified {len(cert)}/{len(prod)}; with one leaf {sum(p['stats']['leaf_boxes'] == 1 for p in cert)}; "
                   f"cells (k, n, one-leaf instances) with fewer than 8 one-leaf instances: {[c for c in low if c[2] < 8]}")
    # ---- H3
    sparse = ("grid", "cubic", "band2", "band3")
    small = prods([d for d in cells(sparse) if d["n"] <= 12])
    out.append(f"  H3a sparse frustrated families, n <= 12: certified {sum(p['status'] == 'certified' for p in small)}/{len(small)}")
    decreasing, jumps = [], []
    for family in sparse + ("complete",):
        for k in config.ALPHABETS:
            docs = [d for d in ladder_cells(main, family, k) if not d["task"].get("extension")]
            pts = [(d["n"],) + plain_median(d) for d in docs]
            full = [(n, b) for n, b, ok in pts if ok and b is not None]
            for (n0, b0), (n1, b1) in zip(full, full[1:]):
                if b1 < b0:
                    decreasing.append((family, k, n0, b0, n1, b1))
            if family in ("band2", "band3"):
                by_n = {n: (b, ok) for n, b, ok in pts}
                if 25 in by_n and 50 in by_n and by_n[25][0] and by_n[50][0]:
                    jumps.append(f"{family} k={k}: {num(by_n[25][0])} -> {num(by_n[50][0])}"
                                 f"{'' if by_n[50][1] else ' (at 50 over the instances searched only: a lower bound)'}"
                                 f" = x{num(by_n[50][0] / by_n[25][0])}")
            usable = [(n, b) for n, b in full if b > 1]
            rate = "-"
            if len(usable) >= 2:
                (n0, b0), (n1, b1) = usable[0], usable[-1]
                rate = f"x{math.exp(math.log(b1 / b0) / (n1 - n0)):.3f} per site (n {n0} -> {n1})"
            out.append(f"  H3b/H4b {family} k={k}: median leaf boxes of the search by n "
                       f"{' '.join(f'{n}:{num(b)}' + ('' if ok else '*') for n, b, ok in pts if b is not None)}; growth {rate}")
    out.append("      (* = not all instances of the cell were searched: median over those searched)")
    out.append(f"  H3b ladders in which the median decreases between two fully searched sizes: {decreasing if decreasing else 'none'}")
    out.append(f"  H3b leaf boxes from n = 25 to n = 50: {'; '.join(jumps)}")
    for family, ks in (("band3", (3, 5, 10)), ("band2", (5, 10)), ("grid", (10,)), ("grid", (2,)), ("cubic", (2, 3))):
        for k in ks:
            out.append(f"  H3c {family} k={k}: certified by n  {counts(family, k)}")
    fails = [(d, r) for d in cells(sparse) for r in d["instances"] if r.get("producer", {}).get("status") not in (None, "certified")]
    causes = {}
    for _, r in fails:
        causes[r["producer"]["stats"]["stop"]] = causes.get(r["producer"]["stats"]["stop"], 0) + 1
    searched = [r["plain"] for _, r in fails if "plain" in r]
    out.append(f"  H3d failures of the producer in these families: {len(fails)}, by cause {causes}; the search without "
               f"certificate was run on {len(searched)} of them and solved {sum(q['status'] == 'optimal' for q in searched)} within the limit")
    # ---- H4
    gaps = [rel_gap(r) for d in cells(("complete",), (2,), extension=True) if d["n"] >= 16 for r in d["instances"]]
    gaps = [g for g in gaps if g is not None]
    out.append(f"  H4a complete k = 2, n >= 16: relative gap of the relaxation {mr(gaps, pct)} over {len(gaps)} instances with a known optimum")
    for k in config.ALPHABETS:
        docs = ladder_cells(main, "complete", k)
        line = []
        for d in docs:
            pl = [r["plain"] for r in d["instances"] if "plain" in r]
            line.append(f"{d['n']}:{sum(p['status'] == 'certified' for p in prods([d]))}/{len(prods([d]))}"
                        f"|{sum(q['status'] == 'optimal' for q in pl)}/{len(pl)}")
        out.append(f"  H4c/d complete k={k}: by n, certified/attempted | search solved/attempted  {' '.join(line)}")
    # ---- H5
    post, share = [], []
    for d in main.values():
        for r in certified(d):
            st = r["producer"]["stats"]
            if st["leaf_certificates"] > 100:
                after = st["time_assemble"] + st["time_check_c"] + st["time_check_python"]
                post.append(after / max(st["time_search"], 1e-9))
                share.append(st["time_check_python"] / max(after, 1e-9))
    out.append(f"  H5  certified instances with more than 100 leaf certificates: {len(post)}; (assemble + checks) / search "
               f"{mr(post, num)}; above 1 in {sum(v > 1 for v in post)}, above 2 in {sum(v > 2 for v in post)}; "
               f"Python engine share of the time after the search {mr(share, pct)}")
    # ---- H6
    allc = [r["producer"] for d in main.values() for r in certified(d)]
    bigc = [p for p in allc if p["stats"]["check_ops"] >= 1e5]
    out.append(f"  H6  leafcert.c alone: largest time {sec(max([p['c_kernel_seconds'] for p in allc] or [None]))} over {len(allc)} "
               f"certificates; Python engine: largest {sec(max([p['stats']['time_check_python'] for p in allc] or [None]))}; "
               f"check(obj, 'c'): largest {sec(max([p['stats']['time_check_c'] for p in allc] or [None]))}")
    out.append(f"      certificates with at least 1e5 operations ({len(bigc)}): share of check(obj, 'c') outside leafcert.c "
               f"{mr([1 - p['c_kernel_seconds'] / max(p['stats']['time_check_c'], 1e-9) for p in bigc], pct)}; "
               f"operations per second leafcert.c {mr([p['stats']['check_ops'] / max(p['c_kernel_seconds'], 1e-9) for p in bigc], big)}, "
               f"Python engine (whole check) {mr([p['stats']['check_ops'] / max(p['stats']['time_check_python'], 1e-9) for p in bigc], big)}; "
               f"ratio {mr([p['stats']['time_check_python'] / max(p['c_kernel_seconds'], 1e-9) for p in bigc], num)}")
    # ---- H7
    at100 = [(d, r) for d in main.values() if d["n"] == 100 for r in d["instances"]
             if r.get("producer", {}).get("status") not in (None, "certified")]
    causes = {}
    for _, r in at100:
        causes[r["producer"]["stats"]["stop"]] = causes.get(r["producer"]["stats"]["stop"], 0) + 1
    searched = [r["plain"] for _, r in at100 if "plain" in r]
    out.append(f"  H7  failures of the producer at n = 100: {len(at100)}, by cause {causes}; searched without certificate "
               f"{len(searched)}, solved {sum(q['status'] == 'optimal' for q in searched)}")
    # ---- H8, H9 (the comparison pass)
    def ratios(cell, name, base, key):
        doc = compare.get(config.cell_name(*cell))
        if not doc:
            return None
        vals = [r["searches"][name][key] / max(r["searches"][base][key], 1e-9) for r in doc["instances"]
                if name in r["searches"] and base in r["searches"]
                and r["searches"][name]["status"] == "optimal" and r["searches"][base]["status"] == "optimal"]
        return statistics.median(vals) if vals else None

    for name in ("lp/strong", "hybrid/strong", "lp/frac"):
        box = {f"{c[0]} k={c[1]} n={c[2]}": ratios(c, name, "mp/strong", "leaf_boxes") for c in config.COMPARE_LP_CELLS}
        tim = {f"{c[0]} k={c[1]} n={c[2]}": ratios(c, name, "mp/strong", "seconds") for c in config.COMPARE_LP_CELLS}
        out.append(f"  H8  {name} against mp/strong, median ratio per cell: leaf boxes { {c: num(v) for c, v in box.items()} }")
        out.append(f"      time { {c: num(v) for c, v in tim.items()} }")
    hy = {f"{c[0]} k={c[1]} n={c[2]}": ratios(c, "hybrid/strong", "lp/strong", "leaf_boxes") for c in config.COMPARE_LP_CELLS}
    out.append(f"  H8  hybrid/strong against lp/strong, median ratio of leaf boxes per cell: { {c: num(v) for c, v in hy.items()} }")
    best_count = cells_seen = 0
    for cell in config.COMPARE_RULE_CELLS:
        doc = compare.get(config.cell_name(*cell))
        if not doc:
            continue
        meds = {}
        for name in ("mp/strong", "mp/maxdeg", "mp/margin", "mp/maxdom"):
            got = [r["searches"][name]["leaf_boxes"] for r in doc["instances"]
                   if all(c in r["searches"] and r["searches"][c]["status"] == "optimal"
                          for c in ("mp/strong", "mp/maxdeg", "mp/margin", "mp/maxdom"))]
            meds[name] = statistics.median(got) if got else None
        if meds["mp/strong"] is None:
            continue
        cells_seen += 1
        best_count += meds["mp/strong"] <= min(v for v in meds.values())
    out.append(f"  H9  cells in which strong has the smallest median number of leaf boxes (ties count; instances solved by all "
               f"four rules): {best_count} of {cells_seen}")
    out.append(f"      time of strong / maxdeg, median per cell: "
               f"{ {f'{c[0]} k={c[1]} n={c[2]}': num(ratios(c, 'mp/strong', 'mp/maxdeg', 'seconds')) for c in config.COMPARE_RULE_CELLS} }")
    out.append(f"      leaf boxes of maxdom / maxdeg, median per cell: "
               f"{ {f'{c[0]} k={c[1]} n={c[2]}': num(ratios(c, 'mp/maxdom', 'mp/maxdeg', 'leaf_boxes')) for c in config.COMPARE_RULE_CELLS} }")
    # ---- H10
    forest = [r for d in cells(("chain", "tree", "band2", "band3"), extension=True) for r in d["instances"]]
    big_n = [r for d in cells(("chain", "tree", "band2", "band3"), extension=True) if d["n"] >= 50 for r in d["instances"]]
    fastest = 0
    for r in big_n:
        times = {name: r[name]["seconds"] for name in ("dp", "brute", "cpsat", "milp", "plain")
                 if r.get(name, {}).get("status") == "optimal"}
        fastest += bool(times) and min(times, key=times.get) == "dp"
    out.append(f"  H10a chains, trees, bands: DP solved {sum(r['dp']['status'] == 'optimal' for r in forest)} of {len(forest)} "
               f"instances; with n >= 50 it was the fastest exact method on {fastest} of {len(big_n)}")
    rows = []
    for d in sorted(cells(("complete",), extension=True), key=lambda d: (str(d["k"]), d["n"])):
        if d["n"] < 16:
            continue
        both = [r for r in d["instances"] if r.get("plain", {}).get("status") == "optimal"]
        for name in ("milp", "cpsat"):
            got = [r for r in both if r.get(name, {}).get("status") == "optimal"]
            if got:
                rows.append(f"k={d['k']} n={d['n']} {name}: search {sec(med([r['plain']['seconds'] for r in got]))} "
                            f"vs {sec(med([r[name]['seconds'] for r in got]))}")
    out.append(f"  H10b complete, n >= 16, instances solved by both (median times): {'; '.join(rows) if rows else 'none'}")
    for k in config.ALPHABETS:
        first = {}
        for name in ("cpsat", "milp", "plain"):
            for d in ladder_cells(main, "complete", k):
                if any(r.get(name, {}).get("status") == "limit" for r in d["instances"]):
                    first[name] = d["n"]
                    break
        out.append(f"  H10c complete k={k}: first size with a 60 s hit: {first if first else 'none'}")
    ratios_b = []
    for d in cells(("band2", "band3")):
        for r in certified(d):
            if r["producer"]["stats"]["leaf_boxes"] < 2:
                continue
            best = [r[name]["seconds"] for name in ("dp", "brute", "cpsat", "milp") if r.get(name, {}).get("status") == "optimal"]
            if best:
                ratios_b.append(r["producer"]["seconds"] / max(min(best), 1e-9))
    out.append(f"  H10d band2 and band3, certified instances that needed branching: {len(ratios_b)}; producer / fastest exact "
               f"baseline {mr(ratios_b, num)}; at least 10 in {sum(v >= 10 for v in ratios_b)}")
    ratios_all = []
    for d in main.values():
        for r in certified(d):
            if r["producer"]["stats"]["leaf_boxes"] < 2:
                continue
            best = [r[name]["seconds"] for name in ("dp", "brute", "cpsat", "milp") if r.get(name, {}).get("status") == "optimal"]
            if best:
                ratios_all.append(r["producer"]["seconds"] / max(min(best), 1e-9))
    out.append(f"      all families, certified instances that needed branching and have an exact baseline: {len(ratios_all)}; "
               f"producer / fastest of (DP, enumeration, CP-SAT, MILP) {mr(ratios_all, num)}; at least 10 in "
               f"{sum(v >= 10 for v in ratios_all)}, below 1 in {sum(v < 1 for v in ratios_all)}")
    # ---- H11
    k2 = [r["producer"]["stats"] for d in main.values() if d["k"] == 2 for r in certified(d)]
    out.append(f"  H11 k = 2: certified instances {len(k2)}; with leaf boxes != leaf certificates: "
               f"{sum(st['leaf_boxes'] != st['leaf_certificates'] for st in k2)}")
    k10 = [r["producer"]["stats"] for d in main.values() if d["k"] == 10 for r in certified(d) if r["producer"]["stats"]["leaf_boxes"] >= 2]
    boxes, certs = sum(st["leaf_boxes"] for st in k10), sum(st["leaf_certificates"] for st in k10)
    out.append(f"      k = 10: {len(k10)} certified instances with at least two leaf boxes; leaf boxes {boxes}, leaf certificates "
               f"{certs}; saved {100 * (1 - certs / max(1, boxes)):.1f}%")
    # ---- H12
    tight = branched = 0
    by_family = {}
    for d in main.values():
        for r in certified(d):
            g = rel_gap(r)
            if g is not None and g < 1e-9:
                tight += 1
                more = r["producer"]["stats"]["leaf_boxes"] > 1
                branched += more
                t = by_family.setdefault(d["family"], [0, 0])
                t[0] += 1
                t[1] += more
    out.append(f"  H12 certified instances whose relaxation is tight at the root (LP value = optimum): {tight}; of these the "
               f"producer needed more than one leaf in {branched}; by family (tight, branched): "
               f"{ {f: tuple(v) for f, v in sorted(by_family.items())} }")
    # ---- H13
    peaks = [p["peak_rss_mb"] for d in main.values() for r in d["instances"] for p in [r.get("producer")] if p and p.get("peak_rss_mb")]
    virt = [d.get("worker_vm_peak_mb") for d in main.values() if d.get("worker_vm_peak_mb")]
    out.append(f"  H13 peak resident memory of a producer run (search, assembling, both checks): largest "
               f"{num(max(peaks) if peaks else None)} MB; largest virtual size of a worker process: {num(max(virt) if virt else None)} MB")


def build(results):
    main, compare, long = load(results / "main"), load(results / "compare"), load(results / "long")
    out = [f"Tables of the certificate benchmark (protocol version {config.PROTOCOL_VERSION}); generated by make_tables.py "
           "from results/main, results/compare, results/long.",
           "Times are wall-clock on a shared machine (noisy): medians and ranges, not means."]
    for phase, folder in (("main", results / "main"), ("compare", results / "compare"), ("long", results / "long")):
        log = run_log(folder)
        if log:
            v = log["versions"]
            out.append(f"{phase}: started {log['started_utc']}, wall {log['wall_seconds']:.0f} s, budget {log['budget_minutes']:.0f} min, "
                       f"{len(log['cells'])} cells; load average at start {v.get('load_average')}, at end {log.get('load_average_end')}; "
                       f"python {v['python']}, numpy {v['numpy']}, scipy {v['scipy']}, ortools {v['ortools']}; {v.get('cpu')}")
            if log["not_started_budget"]:
                out.append(f"  not started (budget rule): {log['not_started_budget']}")
            if log.get("stopped_by_rule"):
                out.append(f"  ladders stopped by the stop rule before their last size: {log['stopped_by_rule']}")
    if main:
        overview(main, out, run_log(results / "main"))
        consistency(main, compare, out)
        cost_tables(main, out)
        checking_tables(main, out)
        density_tables(main, out)
        dead_data_tables(main, out)
        sharing_tables(main, compare, out)
        hypothesis_numbers(main, compare, out)
    if compare:
        compare_tables(compare, out)
    if long:
        long_tables(long, main, out)
    exploratory_tables(results, out)
    if main:
        report_tables(main, out)
        main_tables(main, out)
    return "\n".join(out) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--results", default=str(HERE / "results"))
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    results = Path(args.results)
    text = build(results)
    path = results / "tables.txt"
    if args.verify:
        same = path.exists() and path.read_text() == text
        print("tables.txt is what the result files give" if same else "tables.txt DIFFERS from what the result files give")
        return 0 if same else 1
    path.write_text(text)
    if not args.quiet:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
