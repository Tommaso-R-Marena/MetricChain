"""An independent check of the structural-biology division's stored "min" certificate files (claims K1, K4 of its
request STRUCTBIO-REQ-0001), written by the Computational Research Division from the format description in the
docstring of ``mincert.py`` at its commit 0544ff4 -- not from its loader or its checker.

Inputs: the integer tables of an instance as a numpy archive (``export_tables.py``) and a *detached* certificate file
``structbio-mincert/1``, which names its instance by ``model_sha256`` and contains ``message_bits``, ``domains``, a
claim and a tree of nodes

    {"node": "leaf", "m": {"i,j": [ints]}}
    {"node": "branch", "site": i, "children": {"a": node, ...}}
    {"node": "prunes", "steps": [[site, remove, dominator], ...], "rest": node}        (a chain of eliminations, flat)

What this file does on its own: parses the JSON strictly (duplicate keys, non-integers, non-canonical keys and unknown
fields are errors); recomputes the checksum of the tables in the canonical form the format names (compact JSON of
``scale_bits``, ``unary``, ``pair`` with sorted keys) and compares it with the file's; replays the tree with the rules
of the docstring; recomputes the witness's energy from the tables.

Arithmetic: tables and messages are held in int64 *after* a check that every scaled entry and message is below 2^50
in absolute value and every site has fewer than 4093 neighbours, so that no partial sum can reach 2^62 (the same
limits as the format states); all totals are accumulated in Python integers.

    python experiments/eng/sb_review/check_files.py --tables DIR --certs DIR [--results results.jsonl] --out FILE
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np

LIMIT = 2 ** 50


class Malformed(ValueError):
    pass


def need(cond, msg):
    if not cond:
        raise Malformed(msg)


def is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def no_dup(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Malformed(f"duplicate key {k!r}")
        out[k] = v
    return out


def no_float(text):
    raise Malformed(f"a number that is not an integer: {text}")


def no_const(name):
    raise Malformed(f"non-finite number {name}")


def canon_int(text: str) -> int:
    need(text.isdigit() and (text == "0" or not text.startswith("0")), f"non-canonical index {text!r}")
    return int(text)


def load_tables(path: Path) -> dict:
    with np.load(path, allow_pickle=False) as z:
        n = int(z["n"])
        unary = [np.asarray(z[f"u{i}"], dtype=np.int64) for i in range(n)]
        pair = {(int(i), int(j)): np.asarray(z[f"p{int(i)}_{int(j)}"], dtype=np.int64) for i, j in z["pairs"]}
        return dict(scale_bits=int(z["scale_bits"]), unary=unary, pair=pair)


def tables_sha256(T: dict) -> str:
    doc = {"scale_bits": T["scale_bits"], "unary": [[int(v) for v in u.tolist()] for u in T["unary"]],
           "pair": {f"{i},{j}": [[int(v) for v in row] for row in t.tolist()] for (i, j), t in T["pair"].items()}}
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def parse_certificate(text: str) -> dict:
    try:
        doc = json.loads(text, object_pairs_hook=no_dup, parse_float=no_float, parse_constant=no_const)
    except Malformed:
        raise
    except Exception as exc:
        raise Malformed(f"not JSON: {exc}") from None
    need(isinstance(doc, dict), "document")
    need(doc.get("format") == "structbio-mincert/1", "format")
    need(set(doc) <= {"format", "model_sha256", "message_bits", "domains", "claim", "certificate", "meta"}, f"unknown fields {sorted(set(doc))}")
    need(isinstance(doc.get("model_sha256"), str), "model_sha256")
    need(is_int(doc.get("message_bits")) and 0 <= doc["message_bits"] <= 62, "message_bits")
    claim = doc.get("claim")
    need(isinstance(claim, dict) and set(claim) <= {"lower_bound", "witness"} and is_int(claim.get("lower_bound")), "claim")

    def node(d, depth=0):
        need(isinstance(d, dict), "node")
        kind = d.get("node")
        if kind == "leaf":
            need(set(d) <= {"node", "m"}, "leaf fields")
            m = d.get("m", {})
            need(isinstance(m, dict), "leaf m")
            out = {}
            for k, v in m.items():
                parts = k.split(",")
                need(len(parts) == 2, f"message key {k!r}")
                need(isinstance(v, list) and all(is_int(x) for x in v), "message vector")
                out[(canon_int(parts[0]), canon_int(parts[1]))] = v
            return ("leaf", out)
        if kind == "branch":
            need(set(d) == {"node", "site", "children"} and is_int(d["site"]) and isinstance(d["children"], dict), "branch fields")
            return ("branch", d["site"], {canon_int(a): node(c, depth + 1) for a, c in d["children"].items()})
        if kind == "prunes":
            need(set(d) == {"node", "steps", "rest"} and isinstance(d["steps"], list), "prunes fields")
            for s in d["steps"]:
                need(isinstance(s, list) and len(s) == 3 and all(is_int(x) for x in s), "prune step")
            return ("prunes", d["steps"], node(d["rest"], depth + 1))
        if kind == "prune":                       # a single elimination, if a file uses the nested form
            need(set(d) == {"node", "site", "remove", "dominator", "rest"}, "prune fields")
            need(all(is_int(d[k]) for k in ("site", "remove", "dominator")), "prune integers")
            return ("prunes", [[d["site"], d["remove"], d["dominator"]]], node(d["rest"], depth + 1))
        raise Malformed(f"node kind {kind!r}")

    return dict(model_sha256=doc["model_sha256"], message_bits=doc["message_bits"], domains=doc.get("domains"),
                lower_bound=claim["lower_bound"], witness=claim.get("witness"), root=node(doc.get("certificate")))


def check(T: dict, C: dict) -> dict:
    """Replay.  Returns dict(accepted, reason, proves, stats)."""
    unary, pair = T["unary"], T["pair"]
    n = len(unary)
    sizes = [len(u) for u in unary]
    mb = 2 ** C["message_bits"]
    need(max((int(np.abs(u).max()) for u in unary), default=0) * mb < LIMIT, "a unary entry is outside the supported range")
    need(max((int(np.abs(t).max()) for t in pair.values()), default=0) * mb < LIMIT, "a pair entry is outside the supported range")
    nbrs = [[] for _ in range(n)]
    for (i, j) in pair:
        need(0 <= i < j < n, "pair key")
        nbrs[i].append(j)
        nbrs[j].append(i)
    need(max((len(v) for v in nbrs), default=0) < 4093, "degree outside the supported range")
    H = [u * mb for u in unary]
    J = {k: t * mb for k, t in pair.items()}
    D0 = C["domains"]
    need(isinstance(D0, list) and len(D0) == n, "domains")
    for i, d in enumerate(D0):
        need(isinstance(d, list) and len(d) >= 1 and all(is_int(a) and 0 <= a < sizes[i] for a in d) and len(set(d)) == len(d), "domain")
    full_box = all(sorted(d) == list(range(sizes[i])) for i, d in enumerate(D0))

    def row(i, j, a):                      # J_ij(a, .) over all states of j
        return J[(i, j)][a, :] if i < j else J[(j, i)][:, a]

    stats = dict(leaf=0, branch=0, prune=0, message_integers=0)
    least = None
    stack = [(C["root"], [np.array(d, dtype=np.int64) for d in D0])]
    while stack:
        nd, D = stack.pop()
        if nd[0] == "leaf":
            stats["leaf"] += 1
            m = {}
            for (i, j), vec in nd[1].items():
                need(0 <= i < n and 0 <= j < n and i != j and (min(i, j), max(i, j)) in pair, "message for a pair that is not listed")
                need(len(vec) == sizes[i], "message length")
                need(all(abs(v) < LIMIT for v in vec), "a message is outside the supported range")
                m[(i, j)] = np.array(vec, dtype=np.int64)
                stats["message_integers"] += len(vec)
            B = 0
            for i in range(n):
                vals = H[i][D[i]].copy()
                for j in nbrs[i]:
                    if (i, j) in m:
                        vals = vals + m[(i, j)][D[i]]
                B += int(vals.min())
            for (i, j), t in J.items():
                sub = t[np.ix_(D[i], D[j])]
                if (i, j) in m:
                    sub = sub - m[(i, j)][D[i]][:, None]
                if (j, i) in m:
                    sub = sub - m[(j, i)][D[j]][None, :]
                B += int(sub.min())
            least = B if least is None else min(least, B)
        elif nd[0] == "branch":
            stats["branch"] += 1
            i, ch = nd[1], nd[2]
            need(0 <= i < n, "branch site")
            for a in ch:
                need(0 <= a < sizes[i], "child state")
            for a in D[i].tolist():
                if a not in ch:
                    return dict(accepted=False, reason=f"branch on site {i}: no child for state {a}", proves=None, stats=stats, full_box=full_box)
                D2 = list(D)
                D2[i] = np.array([a], dtype=np.int64)
                stack.append((ch[a], D2))
        else:
            D = list(D)
            for (i, r, t) in nd[1]:
                stats["prune"] += 1
                need(0 <= i < n and 0 <= r < sizes[i] and 0 <= t < sizes[i], "prune step out of range")
                if t == r or t not in D[i].tolist():
                    return dict(accepted=False, reason="prune: the dominator is not another state of the current domain", proves=None, stats=stats, full_box=full_box)
                margin = int(H[i][r]) - int(H[i][t])
                for j in nbrs[i]:
                    margin += int((row(i, j, r)[D[j]] - row(i, j, t)[D[j]]).min())
                if margin < 0:
                    return dict(accepted=False, reason="prune: dominance fails", proves=None, stats=stats, full_box=full_box)
                D[i] = D[i][D[i] != r]
            stack.append((nd[2], D))
    ok = C["lower_bound"] <= least
    return dict(accepted=ok, reason="accepted" if ok else "a leaf bound is below the claim", proves=least, stats=stats, full_box=full_box)


def energy(T: dict, x) -> int:
    e = sum(int(T["unary"][i][a]) for i, a in enumerate(x))
    for (i, j), t in T["pair"].items():
        e += int(t[x[i], x[j]])
    return e


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", type=Path, required=True)
    ap.add_argument("--certs", type=Path, required=True)
    ap.add_argument("--results", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    theirs = {}
    if args.results and args.results.exists():
        for line in args.results.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                theirs[r["pdb_id"]] = r            # the latest row wins, as in their own check
    export = {}
    es = args.tables / "export_summary.json"
    if es.exists():
        export = {r["pdb_id"]: r for r in json.loads(es.read_text())}
    rows = []
    for path in sorted(args.certs.glob("*.mincert.json")):
        pdb_id = path.name.split(".")[0]
        tfile = args.tables / f"{pdb_id}.npz"
        if not tfile.exists():
            continue
        T = load_tables(tfile)
        text = path.read_text()
        t0 = time.perf_counter()
        row = dict(pdb_id=pdb_id, sites=len(T["unary"]), states_total=sum(len(u) for u in T["unary"]), pairs=len(T["pair"]),
                   cert_bytes=len(text), cert_sha256=hashlib.sha256(text.encode()).hexdigest())
        try:
            C = parse_certificate(text)
            row["tables_sha256"] = tables_sha256(T)
            row["checksum_matches_certificate"] = row["tables_sha256"] == C["model_sha256"]
            res = check(T, C)
            unit = 2 ** (T["scale_bits"] + C["message_bits"])
            row.update(accepted=res["accepted"], reason=res["reason"], full_box=res["full_box"], stats=res["stats"],
                       claimed_lower_bound=C["lower_bound"], proves=res["proves"], unit_bits=T["scale_bits"] + C["message_bits"],
                       claimed_lower_bound_kcal=C["lower_bound"] / unit)
            if C["witness"] is not None:
                need(len(C["witness"]) == len(T["unary"]) and all(is_int(a) and 0 <= a < len(T["unary"][i]) for i, a in enumerate(C["witness"])), "witness")
                e = energy(T, C["witness"]) * 2 ** C["message_bits"]
                row.update(witness_energy=e, gap=e - C["lower_bound"])
        except Malformed as exc:
            row.update(accepted=False, reason=f"malformed: {exc}")
        row["seconds"] = round(time.perf_counter() - t0, 3)
        th = theirs.get(pdb_id)
        if th:
            row.update(their_model_sha256_matches=th.get("model_sha256") == row.get("tables_sha256"),
                       their_cert_sha256_matches=th.get("cert_sha256") == row["cert_sha256"],
                       their_lower_bound_kcal=th.get("certified_lower_bound_kcal"), their_check_seconds=th.get("seconds_check_certificate"),
                       their_produce_seconds=th.get("seconds_produce_certificate"), their_toulbar2_seconds=th.get("seconds_toulbar2"),
                       their_stats=dict(leaf=th.get("cert_leaves"), branch=th.get("cert_branches"), prune=th.get("cert_prunes")))
        ex = export.get(pdb_id)
        if ex:
            row.update(our_toulbar2_optimum_int=ex["toulbar2_optimum_int"], our_toulbar2_seconds=ex["toulbar2_seconds"],
                       toulbar2_equals_certified=(ex["toulbar2_optimum_int"] * 2 ** C["message_bits"] == C["lower_bound"]) if "claimed_lower_bound" in row else None)
        rows.append(row)
        print(json.dumps({k: v for k, v in row.items() if k not in ("tables_sha256", "cert_sha256")})[:600], flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
