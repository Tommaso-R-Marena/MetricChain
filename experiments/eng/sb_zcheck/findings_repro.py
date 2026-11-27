"""Minimal reproductions of the findings against ``metricchain_sb`` at 0544ff4, stored as ``results/findings.json``.

Everything here is small (seconds, tens of megabytes).  The observations that need gigabytes (a prune step with a
margin below about -20 kT) are NOT re-run here: the numbers seen in an ad-hoc probe are copied into the file and
labelled as such.

    python findings_repro.py
"""
from __future__ import annotations

import resource

resource.setrlimit(resource.RLIMIT_AS, (3_000_000_000, 3_000_000_000))

import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import tracemalloc  # noqa: E402
from fractions import Fraction  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen  # noqa: E402
import indep_zcheck as Z  # noqa: E402
import sb_bridge as B  # noqa: E402
import truth  # noqa: E402
from campaign_z12 import dec  # noqa: E402

# F1: two sites (2 states, 1 state); E(x0 = 0) = 677, E(x0 = 1) = 678 (table units = energy units, beta = 1)
F1_TABLES = {"unary": [[0, 678], [0]], "pair": {(0, 1): [[677], [0]]}, "scale_bits": 0}


def leaf_doc(tables, beta: str, order, keep=None, steps=()):
    mine = Z.make_model(tables["unary"], tables["pair"], tables["scale_bits"])
    return {"format": "structbio-zcert/1", "model_sha256": Z.model_sha256(mine), "beta": beta,
            "domains": [list(range(len(u))) for u in tables["unary"]], "keep": keep, "claim": {},
            "root": {"steps": list(steps), "order": list(order)}, "meta": "{}"}, mine


def main() -> int:
    S = B.sb()
    out = {"what": "minimal reproductions of findings; reviewed commit 0544ff4"}

    # ---- F1: the float tier accepts and misses ln Z when exp_bits is near 990 ----------------------------------
    doc, mine = leaf_doc(F1_TABLES, "1/1", [1, 0])
    text = gen.dumps(doc)
    pm = B.pair_model(F1_TABLES)
    tr = truth.enumerate_truth(F1_TABLES["unary"], F1_TABLES["pair"], 0, Fraction(1), doc["domains"])
    my = Z.check_text(text, mine)
    rows = []
    for exp_bits in (64, 500, 900, 950, 960, 965, 970, 971, 972, 973, 975, 980, 985, 990, 991, 992, 993, 1000):
        row = {"exp_bits": exp_bits}
        for tier in ("float", "exact"):
            with B.time_limit(30):
                r = B.their_check_text(text, pm, tier, exp_bits=exp_bits)
            if r["accepted"]:
                row[tier] = {"accepted": True, "lo": dec(r["lo"], 12), "hi": dec(r["hi"], 12),
                             "contains_truth": tr.ln_z_contains(r["lo"], r["hi"])}
            else:
                row[tier] = {"accepted": False, "reason": r["reason"][:90]}
        rows.append(row)
    out["F1_float_tier_unsound_for_large_exp_bits"] = {
        "tables": {"unary": F1_TABLES["unary"], "pair": {"0,1": F1_TABLES["pair"][(0, 1)]}, "scale_bits": 0},
        "certificate": text, "truth_ln_z": truth.ball_text(tr.ln_z, 20),
        "indep_zcheck": {"accepted": my.accepted, "lo": dec(my.ln_z_lo, 12), "hi": dec(my.ln_z_hi, 12),
                         "contains_truth": tr.ln_z_contains(my.ln_z_lo, my.ln_z_hi)},
        "by_exp_bits": rows,
        "unsound_exp_bits": [r["exp_bits"] for r in rows if r["float"].get("contains_truth") == "no"],
        "sound_or_rejected_exp_bits": [r["exp_bits"] for r in rows if r["float"].get("contains_truth") != "no"]}

    # ---- F3: prune steps with a negative margin: the factor used, and what larger ones cost --------------------
    rows = []
    for x in (2, 5, 10, 15):
        tables = {"unary": [[0, x]], "pair": {}, "scale_bits": 0}
        doc, mine = leaf_doc(tables, "1/1", [0], steps=[{"op": "prune", "site": 0, "remove": 0, "dominator": 1}])
        text = gen.dumps(doc)
        t1 = time.perf_counter()
        r = B.their_check_text(text, B.pair_model(tables), "exact")
        t_theirs = time.perf_counter() - t1
        t1 = time.perf_counter()
        my = Z.check_text(text, mine)
        t_mine = time.perf_counter() - t1
        tr = truth.enumerate_truth(tables["unary"], {}, 0, Fraction(1), [[0, 1]])
        rows.append({"margin_in_kT": -x, "certificate_bytes": len(text), "their_accepted": r["accepted"],
                     "their_upper": dec(r["hi"], 6) if r["accepted"] else None,
                     "their_contains_truth": tr.ln_z_contains(r["lo"], r["hi"]) if r["accepted"] else None,
                     "ideal_upper_indep_zcheck": dec(my.ln_z_hi, 6), "truth": truth.ball_text(tr.ln_z, 12),
                     "their_seconds": round(t_theirs, 4), "mine_seconds": round(t_mine, 4)})
    out["F3_prune_with_negative_margin"] = {
        "re_run_here": rows,
        "observed_in_an_ad_hoc_probe_not_re_run": {
            "conditions": "same one-site certificate (258 bytes), exact tier, address space limited to 2 GB",
            "rows": [{"margin_in_kT": -30, "their_seconds": 9.7, "outcome": "rejected: MemoryError while checking"},
                     {"margin_in_kT": -100, "their_seconds": 10.1, "outcome": "rejected: MemoryError while checking"},
                     {"margin_in_kT": -300, "their_seconds": 14.0, "outcome": "rejected: MemoryError while checking"},
                     {"margin_in_kT": -1000, "their_seconds": 12.3, "outcome": "rejected: MemoryError while checking"},
                     {"margin_in_kT": -3000, "their_seconds": 8.3, "outcome": "rejected: MemoryError while checking"},
                     {"margin_in_kT": -10000, "their_seconds": 18.6, "outcome": "rejected: MemoryError while checking"},
                     {"margin_in_kT": -20000, "their_seconds": ">30", "outcome": "no return within 30 s (stopped)"}],
            "peak_resident_memory_seen_GB": 1.6}}

    # ---- F4: the file loader ----------------------------------------------------------------------------------
    t1m = {"unary": [[0, 1]], "pair": {}, "scale_bits": 0}
    doc, mine1 = leaf_doc(t1m, "1/1", [0])
    base = gen.dumps(doc)
    pm1 = B.pair_model(t1m)
    cases = [
        ("valid", base),
        ("duplicate key", base.replace('"keep":null', '"keep":null,"keep":null')),
        ("float where an integer is required", base.replace('"order":[0]', '"order":[0.0]')),
        ("boolean where an integer is required", base.replace('"order":[0]', '"order":[false]')),
        ("string where an integer is required", base.replace('"order":[0]', '"order":["0"]')),
        ("NaN", base.replace('"order":[0]', '"order":[NaN]')),
        ("Infinity", base.replace('"order":[0]', '"order":[Infinity]')),
        ("integer written -0", base.replace('"order":[0]', '"order":[-0]')),
        ("beta not in lowest terms", base.replace('"1/1"', '"2/2"')),
        ("beta with a plus sign", base.replace('"1/1"', '"+1/1"')),
        ("beta '--5/3'", base.replace('"1/1"', '"--5/3"')),
        ("beta with a superscript digit", base.replace('"1/1"', '"\\u00b2/1"')),
        ("beta with 5000 digits", base.replace('"1/1"', '"%s/1"' % ("9" * 5000))),
        ("claim '--1/1'", base.replace('"claim":{}', '"claim":{"ln_z_lo":"--1/1"}')),
        ("claim with one bound only", base.replace('"claim":{}', '"claim":{"ln_z_lo":"-1/1"}')),
        ("unknown top-level field", base.replace('"meta":"{}"', '"meta":"{}","extra":1')),
        ("unknown field in a step", base.replace('"steps":[]', '"steps":[{"op":"prune","site":0,"remove":1,'
                                                                '"dominator":0,"margin":7}]')),
        ("unknown field in a node", base.replace('"order":[0]', '"order":[0],"note":1')),
        ("leaf with a 'children' field", base.replace('"order":[0]', '"order":[0],"children":{"0":{"steps":[],'
                                                                     '"order":[0]}}')),
        ("missing 'keep'", base.replace('"keep":null,', '')),
        ("missing 'meta'", base.replace(',"meta":"{}"', '')),
        ("missing 'claim'", base.replace('"claim":{},', '')),
        ("meta is not JSON text", base.replace('"meta":"{}"', '"meta":"x"')),
        ("meta holds 100000 nested brackets", base.replace('"meta":"{}"', '"meta":"%s"' % ("[" * 100000))),
        ("domain not sorted", base.replace('"domains":[[0,1]]', '"domains":[[1,0]]')),
        ("domain with a repeated state", base.replace('"domains":[[0,1]]', '"domains":[[0,0]]')),
        ("wrong checksum", base.replace(doc["model_sha256"], "0" * 64)),
        ("truncated file", base[:-7]),
        ("trailing text", base + "x"),
        ("insignificant whitespace", base.replace(",", " ,\n ")),
    ]
    for depth in (500, 990, 1000, 2000, 5000):
        cases.append((f"conditioning nested {depth} deep",
                      base.split('"root":')[0].replace('"domains":[[0,1]]', '"domains":[[0]]') + '"root":'
                      + '{"steps":[],"branch":0,"children":{"0":' * depth + '{"steps":[],"order":[0]}' + '}}' * depth
                      + ',"meta":"{}"}'))
    table = []
    for name, text in cases:
        cert, err = B.their_load(text, pm1)
        theirs = "loaded" if cert is not None else ("refused (MalformedZCertificate)" if err.startswith("malformed")
                                                    else "raised " + err.split(":")[0][4:])
        chk = None
        dumps_ok = None
        if cert is not None:
            r = B.their_check(cert)
            chk = "accepted" if r["accepted"] else "rejected: " + r["reason"][:50]
            try:
                S["zcert"].dumps(cert)
                dumps_ok = True
            except Exception as exc:                               # noqa: BLE001
                dumps_ok = type(exc).__name__
        my = Z.check_text(text, mine1)
        table.append({"case": name, "their_loader": theirs, "their_checker": chk, "their_dumps": dumps_ok,
                      "indep_zcheck": "accepted" if my.accepted else f"{my.kind}: {my.reason[:60]}"})
    out["F4_file_loader"] = {
        "cases": table,
        "their_loader_raised_something_else_than_MalformedZCertificate":
            [r["case"] for r in table if r["their_loader"].startswith("raised")],
        "loaded_by_theirs_and_refused_by_indep_zcheck":
            [r["case"] for r in table if r["their_loader"] == "loaded" and not r["indep_zcheck"].startswith("accepted")]}

    # ---- F6: a model without sites (Z = 1, ln Z = 0) ----------------------------------------------------------
    pm0 = S["model"].PairModel(unary=[], pair={}, scale_bits=0)
    r = B.their_check(S["zcert"].ZCertificate(model=pm0, beta=Fraction(1), domains=[], steps=[], order=[]))
    m0 = Z.make_model([], {}, 0)
    my = Z.check_document({"format": Z.FORMAT_TAG, "model_sha256": Z.model_sha256(m0), "beta": "1/1", "domains": [],
                           "keep": None, "claim": {}, "root": {"steps": [], "order": []}, "meta": "{}"}, m0)
    out["F6_model_without_sites"] = {"theirs": r["reason"], "their_exception": r["exception"],
                                     "indep_zcheck": [str(my.ln_z_lo), str(my.ln_z_hi)] if my.accepted else my.reason}

    # ---- cost on two small dense instances (their producer's certificate without relaxation or pruning) -------
    import random
    rng = random.Random(5)
    cost = []
    for n, k in ((6, 3), (8, 3)):
        tables = {"unary": [[rng.randint(-40, 40) for _ in range(k)] for _ in range(n)],
                  "pair": {(i, j): [[rng.randint(-40, 40) for _ in range(k)] for _ in range(k)]
                           for i in range(n) for j in range(i + 1, n)}, "scale_bits": 4}
        pm = B.pair_model(tables)
        mine = Z.make_model(tables["unary"], tables["pair"], 4)
        cert = S["partition"].certify_partition(pm, Fraction(1, 2))
        cert.claim = {}
        text = S["zcert"].dumps(cert)
        row = {"sites": n, "states": k, "certificate_bytes": len(text)}
        for label, fn in (("their_exact", lambda: B.their_check_text(text, pm, "exact")),
                          ("their_float", lambda: B.their_check_text(text, pm, "float")),
                          ("mine_exact", lambda: Z.check_text(text, mine)),
                          ("mine_rounded_128", lambda: Z.check_text(text, mine, round_bits=128))):
            t1 = time.perf_counter()
            res = fn()
            dt = time.perf_counter() - t1
            tracemalloc.start()
            fn()
            peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            lo, hi = (res["lo"], res["hi"]) if isinstance(res, dict) else (res.ln_z_lo, res.ln_z_hi)
            row[label] = {"seconds": round(dt, 4), "peak_python_MB": round(peak / 2 ** 20, 2),
                          "width": float(hi - lo), "largest_table": (res["stats"] if isinstance(res, dict)
                                                                     else res.stats).get("largest_table",
                                                                                         res.stats.get("max_table")
                                                                                         if not isinstance(res, dict)
                                                                                         else None)}
        cost.append(row)
    out["cost_small_dense"] = cost

    (HERE / "results" / "findings.json").write_text(json.dumps(out, indent=1))
    f1 = out["F1_float_tier_unsound_for_large_exp_bits"]
    print("F1 unsound exp_bits:", f1["unsound_exp_bits"], "| truth", f1["truth_ln_z"])
    for r in f1["by_exp_bits"]:
        print("   ", r["exp_bits"], r["float"], "| exact tier:", r["exact"].get("contains_truth", r["exact"].get("reason")))
    for r in out["F3_prune_with_negative_margin"]["re_run_here"]:
        print("F3", r)
    for r in table:
        print("F4", r)
    print("F6", out["F6_model_without_sites"])
    for r in cost:
        print("cost", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
