"""Campaign Z5: "the checker never raises" -- malformed objects, malformed files, odd parameters.

STATUS: WRITTEN BUT NEVER EXECUTED.  The programme was wound down before this script was run even once; it has not
been debugged and there is no result file for it.  Do not quote it as evidence.

A  object fuzz: valid in-memory certificates with one to three fields (at any depth) replaced by values of other
   types; ``check_partition_certificate`` is called in both tiers.  An exception that escapes is a finding; a call
   that does not return within the time limit is recorded as a hang; an *accepted* mutant is confronted with the
   enumerated truth whenever it still denotes a box.
B  hand-built objects: shared and cyclic nodes, deep trees, numpy integers, string keys, an empty model.
C  file fuzz: character-level mutations of valid files through their loader and checker (and through
   ``indep_zcheck``): exceptions of the loader other than ``MalformedZCertificate``, exceptions of the checker,
   accepted mutants against the truth, and the two verdicts side by side.
D  parameters: ``arithmetic``, ``max_entries``, ``exp_bits`` of the wrong type or out of range; accepted results
   against the truth (the range of ``exp_bits`` in which the float tier is unsound is the subject of the Z3 campaign
   and is excluded here).

    python campaign_z5.py --seed 1 --objects 6000 --files 20000
"""
from __future__ import annotations

import resource

resource.setrlimit(resource.RLIMIT_AS, (3_000_000_000, 3_000_000_000))

import argparse  # noqa: E402
import collections  # noqa: E402
import copy  # noqa: E402
import decimal  # noqa: E402
import json  # noqa: E402
import random  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from fractions import Fraction  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen  # noqa: E402
import indep_zcheck as Z  # noqa: E402
import sb_bridge as B  # noqa: E402
import truth  # noqa: E402
from campaign_z12 import box_as_sets, dec  # noqa: E402

TIME_LIMIT = 20


class Weird:
    """An object whose comparisons and hash raise."""

    def __eq__(self, other):
        raise RuntimeError("weird __eq__")

    def __hash__(self):
        raise RuntimeError("weird __hash__")

    def __repr__(self):
        return "Weird()"


def garbage(rng: random.Random, depth: int = 0):
    r = rng.random()
    if depth > 2 or r < 0.55:
        return rng.choice([
            None, True, False, 0, 1, -1, 2, 3, 7, 10 ** 4, -10 ** 4, 0.0, 1.0, -1.5, float("nan"), float("inf"),
            "", "0", "1", "prune", "relax", "1/1", b"0", (0, 1), frozenset([0]), set(), 3 + 4j, Fraction(1, 2),
            Fraction(0), Fraction(-1), decimal.Decimal("1.5"), np.int64(1), np.int32(0), np.uint8(1), np.float64(1.0),
            np.bool_(True), np.array([0, 1]), np.array(1), range(2), Weird(), Ellipsis, NotImplemented, object(),
            lambda: 0, [0, 1], [1, 0], [[0]], {}, {0: 1}, {"op": "prune"}, {"steps": [], "order": []}])
    if r < 0.8:
        return [garbage(rng, depth + 1) for _ in range(rng.randint(0, 3))]
    keys = ["op", "site", "remove", "dominator", "pair", "f", "g", "steps", "order", "branch", "children", 0, 1, "0",
            None, (0,), 1.0, True, "ln_z_lo", "ln_z_hi"]
    return {rng.choice(keys): garbage(rng, depth + 1) for _ in range(rng.randint(0, 4))}


def paths(obj, prefix=()):
    """All positions inside nested lists and dicts (as tuples of keys/indices)."""
    out = [prefix]
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.extend(paths(v, prefix + (k,)))
    elif isinstance(obj, list):
        for k, v in enumerate(obj):
            out.extend(paths(v, prefix + (k,)))
    return out


def set_path(obj, path, value):
    for k in path[:-1]:
        obj = obj[k]
    obj[path[-1]] = value


def to_object(doc: dict, pm):
    """Their in-memory certificate from a document of the file shape (children keyed by integers)."""
    zcert = B.sb()["zcert"]

    def node(d):
        out = {"steps": copy.deepcopy(d["steps"])}
        if "order" in d:
            out["order"] = list(d["order"])
        else:
            out["branch"] = d["branch"]
            out["children"] = {int(k): node(v) for k, v in d["children"].items()}
        return out

    root = node(doc["root"])
    claim = {k: Fraction(v) for k, v in doc["claim"].items()}
    return zcert.ZCertificate(model=pm, beta=Fraction(doc["beta"]), domains=copy.deepcopy(doc["domains"]),
                              steps=root["steps"], order=root.get("order", []), keep=doc["keep"], claim=claim,
                              meta={}, branch=root.get("branch"), children=root.get("children"))


def well_defined(cert, pm, sizes):
    """``(beta, box)`` if the mutated object still names the instance, a nonnegative rational beta and a box."""
    try:
        if cert.model is not pm or type(cert.beta) is not Fraction or cert.beta < 0:
            return None
        if type(cert.domains) is not list:
            return None
        box = box_as_sets([list(d) if type(d) is list else None for d in cert.domains], sizes)
        if box is None:
            return None
        return cert.beta, box
    except Exception:                                              # noqa: BLE001
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--objects", type=int, default=6000)
    ap.add_argument("--files", type=int, default=20000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    S = B.sb()
    zcert, zcheck = S["zcert"], S["zcheck"]
    t0 = time.time()
    findings = []
    out = {"campaign": "z5", "seed": args.seed}

    def instance():
        tables = gen.random_tables(rng, n=rng.randint(1, 4), kmax=3)
        gen.temper(rng, tables, max(gen.BETAS), 200)
        pm = B.pair_model(tables)
        mine = Z.make_model(tables["unary"], tables["pair"], tables["scale_bits"])
        doc = gen.random_certificate(rng, tables, Z.model_sha256(mine), max_prune_kt=8, wild_kt=50)
        return tables, pm, mine, doc

    # ------------------------------------------------------------------------------------------------------- A
    A = collections.Counter()
    reasons = collections.Counter()
    for case in range(args.objects):
        tables, pm, mine, doc = instance()
        sizes = [len(u) for u in tables["unary"]]
        cert = to_object(doc, pm)
        fields = ["model", "beta", "domains", "steps", "order", "keep", "claim", "meta", "branch", "children"]
        for _ in range(rng.randint(1, 3)):
            name = rng.choice(fields)
            value = getattr(cert, name)
            inner = [p for p in paths(value) if p] if isinstance(value, (list, dict)) else []
            if inner and rng.random() < 0.7:
                try:
                    set_path(value, rng.choice(inner), garbage(rng))
                except Exception:                                  # noqa: BLE001
                    setattr(cert, name, garbage(rng))
            else:
                setattr(cert, name, garbage(rng))
        arithmetic = rng.choice(["exact", "float"])
        A["cases"] += 1
        try:
            with B.time_limit(TIME_LIMIT):
                rec = B.their_check(cert, arithmetic)
        except B.Timeout:
            A["hang"] += 1
            findings.append({"part": "A", "kind": "no return within the time limit", "object": repr(cert)[:600]})
            continue
        if rec["exception"]:
            A["EXCEPTION"] += 1
            findings.append({"part": "A", "kind": "exception escaped the checker", "exception": rec["exception"],
                             "object": repr(cert)[:600]})
            continue
        A["accepted" if rec["accepted"] else "rejected"] += 1
        if not rec["accepted"]:
            reasons[rec["reason"].split(":")[0][:40] + (": " + rec["reason"].split(":")[1][:30]
                                                        if rec["reason"].startswith("rejected") else "")] += 1
            continue
        wd = well_defined(cert, pm, sizes)
        if wd is None:
            A["accepted_without_a_well_defined_question"] += 1
            findings.append({"part": "A", "kind": "accepted although beta, the model or the box is not well defined",
                             "object": repr(cert)[:600]})
            continue
        tr = truth.enumerate_truth(tables["unary"], tables["pair"], tables["scale_bits"], wd[0], wd[1])
        v = tr.ln_z_contains(rec["lo"], rec["hi"])
        A["accepted_truth_" + v] += 1
        if v == "no":
            findings.append({"part": "A", "kind": "CRITICAL accepted mutant misses ln Z", "object": repr(cert)[:900],
                             "interval": [dec(rec["lo"]), dec(rec["hi"])], "truth": truth.ball_text(tr.ln_z)})
        keep = rec["keep"]
        if type(keep) in (int, np.int64, np.int32) and 0 <= keep < len(sizes):
            for a in range(sizes[keep]):
                p = B.their_population(rec, a)
                if p is None:
                    continue
                v = tr.pop_contains(int(keep), a, p[0], p[1])
                A["accepted_pop_" + v] += 1
                if v == "no":
                    findings.append({"part": "A", "kind": "CRITICAL accepted mutant misses a population",
                                     "object": repr(cert)[:900]})
    out["A_object_fuzz"] = dict(A)
    out["A_reject_reasons"] = dict(reasons.most_common(25))

    # ------------------------------------------------------------------------------------------------------- B
    Bres = {}
    PM = S["model"].PairModel
    pm1 = PM(unary=[[0, 1]], pair={}, scale_bits=0)

    def run(name, cert, **kw):
        t1 = time.time()
        try:
            with B.time_limit(TIME_LIMIT):
                rec = B.their_check(cert, **kw)
            Bres[name] = {"exception": rec["exception"], "accepted": rec["accepted"], "reason": rec["reason"][:90],
                          "seconds": round(time.time() - t1, 3)}
            if rec["exception"]:
                findings.append({"part": "B", "kind": "exception escaped the checker", "case": name,
                                 "exception": rec["exception"]})
        except B.Timeout:
            Bres[name] = {"hang": True, "seconds": round(time.time() - t1, 1)}
            findings.append({"part": "B", "kind": "no return within the time limit", "case": name})

    leaf = {"steps": [], "order": [0]}
    run("valid leaf", zcert.ZCertificate(pm1, Fraction(1), [[0, 1]], [], [0]))
    shared = zcert.ZCertificate(pm1, Fraction(1), [[0, 1]], [], [], branch=0, children={0: leaf, 1: leaf})
    run("the same node object as both children", shared)
    cyc = {"steps": [], "branch": 0, "children": {}}
    cyc["children"][0] = cyc
    run("a node that is its own only child (cycle)",
        zcert.ZCertificate(pm1, Fraction(1), [[0]], [], [], branch=0, children={0: cyc}))
    cyc2 = {"steps": [], "branch": 0, "children": {}}
    cyc2["children"][0] = cyc2
    cyc2["children"][1] = cyc2
    run("a node that is both of its own children (cycle, two branches)",
        zcert.ZCertificate(pm1, Fraction(1), [[0, 1]], [], [], branch=0, children={0: cyc2, 1: cyc2}))
    for depth in (900, 990, 1000, 5000, 100000):
        node = {"steps": [], "order": [0]}
        for _ in range(depth):
            node = {"steps": [], "branch": 0, "children": {0: node}}
        run(f"in-memory tree of depth {depth}",
            zcert.ZCertificate(pm1, Fraction(1), [[0]], [], [], branch=0, children={0: node}))
        del node
    run("numpy integers everywhere",
        zcert.ZCertificate(pm1, Fraction(1), [[np.int64(0), np.int64(1)]],
                           [{"op": "prune", "site": np.int64(0), "remove": np.int64(1), "dominator": np.int64(0)}],
                           [np.int64(0)], keep=None))
    run("children keyed by strings",
        zcert.ZCertificate(pm1, Fraction(1), [[0, 1]], [], [], branch=0, children={"0": leaf, "1": leaf}))
    run("children keyed by numpy integers",
        zcert.ZCertificate(pm1, Fraction(1), [[0, 1]], [], [], branch=0, children={np.int64(0): leaf, np.int64(1): leaf}))
    run("domains as tuples", zcert.ZCertificate(pm1, Fraction(1), [(0, 1)], [], [0]))
    run("beta as int", zcert.ZCertificate(pm1, 1, [[0, 1]], [], [0]))
    run("beta as float", zcert.ZCertificate(pm1, 1.0, [[0, 1]], [], [0]))
    run("empty model (no site): ln Z = 0", zcert.ZCertificate(PM(unary=[], pair={}, scale_bits=0), Fraction(1), [], [], []))
    run("model is None", zcert.ZCertificate(None, Fraction(1), [[0, 1]], [], [0]))
    run("certificate is None", None)
    run("certificate is a dict", {"model": pm1})
    out["B_hand_built_objects"] = Bres

    # ------------------------------------------------------------------------------------------------------- C
    C = collections.Counter()
    loader_exc = collections.Counter()
    side = collections.Counter()
    alphabet = '{}[]:,"0123456789-+.eE/ \n\\untrfalsNI' + "prunelaxodbchimsg_"
    for case in range(args.files // 25):
        tables, pm, mine, doc = instance()
        sizes = [len(u) for u in tables["unary"]]
        if rng.random() < 0.3:
            base = S["zcert"].dumps(to_object(doc, pm))
        else:
            base = gen.dumps(doc)
        for _ in range(25):
            s = list(base)
            for _ in range(rng.randint(1, 3)):
                op, pos = rng.randrange(4), rng.randrange(len(s))
                if op == 0:
                    s[pos] = rng.choice(alphabet)
                elif op == 1:
                    del s[pos]
                elif op == 2:
                    s.insert(pos, rng.choice(alphabet))
                else:                                               # duplicate a slice (repeated keys, nested copies)
                    end = min(len(s), pos + rng.randint(1, 40))
                    s[pos:pos] = s[pos:end]
            text = "".join(s)
            C["cases"] += 1
            my = Z.check_text(text, mine)
            if my.kind == "abstain":
                my = Z.check_text(text, mine, round_bits=256)
            if my.kind == "internal":
                C["MINE_INTERNAL"] += 1
                findings.append({"part": "C", "kind": "internal error of indep_zcheck", "text": text, "reason": my.reason})
            try:
                with B.time_limit(TIME_LIMIT):
                    th = B.their_check_text(text, pm, "exact")
            except B.Timeout:
                C["hang"] += 1
                findings.append({"part": "C", "kind": "no return within the time limit", "text": text})
                continue
            if th["load_error"] and th["load_error"].startswith("EXC"):
                C["loader_exception_other_than_Malformed"] += 1
                loader_exc[th["load_error"].split(":")[0]] += 1
                if len([f for f in findings if f.get("kind") == "loader exception"]) < 5:
                    findings.append({"part": "C", "kind": "loader exception", "exception": th["load_error"], "text": text})
            if th["exception"]:
                C["CHECKER_EXCEPTION"] += 1
                findings.append({"part": "C", "kind": "exception escaped the checker", "exception": th["exception"],
                                 "text": text})
            C["their_loaded"] += th["load_error"] is None
            C["their_accept"] += th["accepted"]
            C["mine_accept"] += my.accepted
            side[("theirs accepts" if th["accepted"] else "theirs rejects") + " / " +
                 ("mine accepts" if my.accepted else "mine rejects")] += 1
            if th["accepted"] or my.accepted:
                try:
                    d = json.loads(text)
                    beta = Fraction(d["beta"])
                    box = box_as_sets(d["domains"], sizes)
                except Exception:                                   # noqa: BLE001
                    beta = box = None
                if box is None or beta is None or beta < 0:
                    C["accepted_without_a_well_defined_question"] += 1
                    findings.append({"part": "C", "kind": "accepted although the file does not denote a box", "text": text,
                                     "theirs": th["accepted"], "mine": my.accepted})
                    continue
                tr = truth.enumerate_truth(tables["unary"], tables["pair"], tables["scale_bits"], beta, box)
                if th["accepted"]:
                    v = tr.ln_z_contains(th["lo"], th["hi"])
                    C["their_accept_truth_" + v] += 1
                    if v == "no":
                        findings.append({"part": "C", "kind": "CRITICAL accepted mutant file misses ln Z", "text": text})
                    keep = d.get("keep")
                    if type(keep) is int and 0 <= keep < len(sizes):
                        for a in range(sizes[keep]):
                            p = B.their_population(th, a)
                            if p is not None:
                                v = tr.pop_contains(keep, a, p[0], p[1])
                                C["their_accept_pop_" + v] += 1
                                if v == "no":
                                    findings.append({"part": "C", "kind": "CRITICAL accepted mutant file misses a "
                                                                          "population", "text": text})
                if my.accepted:
                    v = tr.ln_z_contains(my.ln_z_lo, my.ln_z_hi)
                    C["mine_accept_truth_" + v] += 1
                    if v != "yes":
                        findings.append({"part": "C", "kind": "indep_zcheck accepted mutant misses ln Z", "text": text})
    out["C_file_fuzz"] = dict(C)
    out["C_loader_exception_types"] = dict(loader_exc)
    out["C_verdicts_side_by_side"] = dict(side)

    # ------------------------------------------------------------------------------------------------------- D
    D = collections.Counter()
    Dexamples = {}
    odd_arith = ["exact", "float", "EXACT", "", None, 0, b"exact", ["exact"]]
    odd_entries = [None, 5_000_000, 1, 0, -1, 1.5, "10", 2 ** 70, True, float("inf"), float("nan"), [1]]
    odd_bits = [64, 80, 40, 24, 8, 2, 1, 0, -1, -8, -15, -16, -17, -100, 200, 500, 1.5, 64.0, None, "64", True, [64],
                Fraction(64), np.int64(64)]
    for case in range(max(1, args.objects // 4)):
        tables, pm, mine, doc = instance()
        sizes = [len(u) for u in tables["unary"]]
        cert = to_object(doc, pm)
        which = rng.randrange(3)
        kw = {"arithmetic": rng.choice(["exact", "float"]), "max_entries": 5_000_000, "exp_bits": 64}
        if which == 0:
            kw["arithmetic"] = rng.choice(odd_arith)
        elif which == 1:
            kw["max_entries"] = rng.choice(odd_entries)
        else:
            kw["exp_bits"] = rng.choice(odd_bits)
        D["cases"] += 1
        label = f"{['arithmetic', 'max_entries', 'exp_bits'][which]}={kw[['arithmetic', 'max_entries', 'exp_bits'][which]]!r}"
        try:
            with B.time_limit(TIME_LIMIT):
                rec = B.their_check(cert, **kw)
        except B.Timeout:
            D["hang"] += 1
            findings.append({"part": "D", "kind": "no return within the time limit", "parameters": label})
            continue
        if rec["exception"]:
            D["EXCEPTION"] += 1
            findings.append({"part": "D", "kind": "exception escaped the checker", "parameters": label,
                             "exception": rec["exception"]})
            continue
        Dexamples.setdefault(label, collections.Counter())["accepted" if rec["accepted"] else
                                                           "rejected: " + rec["reason"][:50]] += 1
        D["accepted" if rec["accepted"] else "rejected"] += 1
        if rec["accepted"]:
            tr = truth.enumerate_truth(tables["unary"], tables["pair"], tables["scale_bits"], Fraction(doc["beta"]),
                                       doc["domains"])
            v = tr.ln_z_contains(rec["lo"], rec["hi"])
            D["accepted_truth_" + v] += 1
            if v == "no":
                findings.append({"part": "D", "kind": "CRITICAL accepted with odd parameters and misses ln Z",
                                 "parameters": label, "certificate": gen.dumps(doc), "tables": str(tables)})
            if doc["keep"] is not None:
                for a in range(sizes[doc["keep"]]):
                    p = B.their_population(rec, a)
                    if p is not None:
                        v = tr.pop_contains(doc["keep"], a, p[0], p[1])
                        D["accepted_pop_" + v] += 1
                        if v == "no":
                            findings.append({"part": "D", "kind": "CRITICAL accepted with odd parameters and misses a "
                                                                  "population", "parameters": label,
                                             "certificate": gen.dumps(doc), "tables": str(tables)})
    out["D_parameters"] = dict(D)
    out["D_by_parameter"] = {k: dict(v) for k, v in sorted(Dexamples.items())}
    out["findings"] = findings[:60]
    out["findings_total"] = len(findings)
    out["seconds"] = round(time.time() - t0, 1)
    path = Path(args.out) if args.out else HERE / "results" / "z5.json"
    path.write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: v for k, v in out.items() if k not in ("findings", "D_by_parameter")}, indent=1, default=str))
    for f in findings[:12]:
        print("FINDING", json.dumps(f, default=str)[:400])
    return 0


if __name__ == "__main__":
    sys.exit(main())
