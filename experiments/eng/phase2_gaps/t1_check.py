"""T1: check one detached ``structbio-mincert/1`` certificate of models v2 / v2-lib with one of three checkers.

    python experiments/eng/phase2_gaps/t1_check.py --checker {files,indep,sb} --tables T.npz --cert C.json [--sb <sb-worktree>]

checkers
  files  engineering's detached-file checker ``experiments/eng/sb_review/check_files.py`` (its strict parser and its
         numpy/int64 replay with range checks), unchanged, imported.
  indep  engineering's pure-Python checker ``experiments/eng/sb_review/indep_mincheck.py`` (``check_plain``), unchanged,
         imported, fed through the ADAPTER below.  ``indep_mincheck.strict_loads`` cannot read these files: it requires
         the tables embedded in the document (a top-level field ``model``, and exactly the eight top-level fields
         format/model/model_sha256/message_bits/domains/claim/certificate/meta) and knows only the nested elimination
         node ``{"node": "prune", "site", "remove", "dominator", "rest"}``; the files are *detached* (no ``model``) and
         write chains of eliminations flat, ``{"node": "prunes", "steps": [[site, remove, dominator], ...], "rest"}``.
         The adapter: (1) parses the file with check_files.parse_certificate (strict: duplicate keys, floats,
         non-canonical keys, unknown fields refused); (2) takes the tables from the npz archive and checks their
         canonical checksum against the file's ``model_sha256`` (check_files.tables_sha256); (3) rewrites every flat
         ``prunes`` chain into the equivalent nested ``prune`` nodes in the same order (iteratively) and the leaves'
         message keys into tuples; (4) calls ``indep_mincheck.check_plain``.  Nothing else is changed.
  sb     the structural-biology division's own checker ``metricchain_sb.mincheck.check_text`` at the worktree given by
         --sb (a5cc106, i.e. after the repair 0e934eb), with the instance built as ``PairModel`` from the same npz and
         ``expected_model_sha256`` = the file's checksum.

Prints one JSON line.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sb_review"))
import check_files  # noqa: E402
import indep_mincheck  # noqa: E402


def to_plain(T: dict, C: dict) -> dict:
    """The adapter: check_files' parsed form + tables -> the plain form of indep_mincheck."""
    def build(nd):
        # iterative: returns the nested-dict node for the parsed node nd
        root_holder = {}
        stack = [(nd, root_holder, "x")]
        while stack:
            p, parent, key = stack.pop()
            if p[0] == "leaf":
                parent[key] = {"node": "leaf", "m": {k: list(v) for k, v in p[1].items()}}
            elif p[0] == "branch":
                out = {"node": "branch", "site": p[1], "children": {}}
                parent[key] = out
                for a, ch in p[2].items():
                    stack.append((ch, out["children"], a))
            else:   # prunes chain -> nested prune nodes
                cur_parent, cur_key = parent, key
                for (i, r, t) in p[1]:
                    node = {"node": "prune", "site": i, "remove": r, "dominator": t}
                    cur_parent[cur_key] = node
                    cur_parent, cur_key = node, "rest"
                stack.append((p[2], cur_parent, cur_key))
        return root_holder["x"]

    return dict(scale_bits=T["scale_bits"], unary=[[int(v) for v in u.tolist()] for u in T["unary"]],
                pair={k: [[int(v) for v in row] for row in t.tolist()] for k, t in T["pair"].items()},
                message_bits=C["message_bits"], domains=C["domains"], lower_bound=C["lower_bound"], root=build(C["root"]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checker", choices=["files", "indep", "sb"], required=True)
    ap.add_argument("--tables", type=Path, required=True)
    ap.add_argument("--cert", type=Path, required=True)
    ap.add_argument("--sb", type=Path)
    args = ap.parse_args()
    t_load0 = time.perf_counter()
    T = check_files.load_tables(args.tables)
    text = args.cert.read_text()
    out = dict(checker=args.checker, cert_bytes=len(text), cert_sha256=hashlib.sha256(text.encode()).hexdigest(),
               sites=len(T["unary"]), states_total=sum(len(u) for u in T["unary"]), pairs=len(T["pair"]))
    tsha = check_files.tables_sha256(T)
    out["tables_sha256"] = tsha
    out["seconds_load_tables"] = round(time.perf_counter() - t_load0, 3)
    t0 = time.perf_counter()
    if args.checker in ("files", "indep"):
        try:
            C = check_files.parse_certificate(text)
            out["checksum_matches_certificate"] = tsha == C["model_sha256"]
            out["claimed_lower_bound"] = C["lower_bound"]
            out["unit_bits"] = T["scale_bits"] + C["message_bits"]
            out["claimed_lower_bound_kcal"] = C["lower_bound"] / 2 ** out["unit_bits"]
            if C["witness"] is not None:
                out["witness_energy_scaled"] = check_files.energy(T, C["witness"]) * 2 ** C["message_bits"]
                out["gap"] = out["witness_energy_scaled"] - C["lower_bound"]
            if args.checker == "files":
                res = check_files.check(T, C)
                out.update(accepted=res["accepted"] and out["checksum_matches_certificate"], replay_accepted=res["accepted"],
                           reason=res["reason"], proves=res["proves"], full_box=res["full_box"], stats=res["stats"])
            else:
                plain = to_plain(T, C)
                out["seconds_adapter"] = round(time.perf_counter() - t0, 3)
                res = indep_mincheck.check_plain(plain)
                st = dict(leaf=0, branch=0, prune=0)
                stack = [plain["root"]]
                while stack:                        # count nodes of the nested form
                    nd = stack.pop()
                    st[nd["node"]] += 1
                    if nd["node"] == "branch":
                        stack.extend(nd["children"].values())
                    elif nd["node"] == "prune":
                        stack.append(nd["rest"])
                full_box = all(sorted(d) == list(range(len(T["unary"][i]))) for i, d in enumerate(C["domains"]))
                out.update(accepted=res["accepted"] and out["checksum_matches_certificate"], replay_accepted=res["accepted"],
                           reason=res["reason"], proves=res["proves"], full_box=full_box, stats=st)
        except check_files.Malformed as exc:
            out.update(accepted=False, reason=f"malformed: {exc}")
    else:
        sys.path.insert(0, str(args.sb / "src"))
        from metricchain_sb.mincheck import check_text
        from metricchain_sb.model import PairModel
        model = PairModel(unary=T["unary"], pair=T["pair"], scale_bits=T["scale_bits"])
        expected = json.loads(text)["model_sha256"]
        t0 = time.perf_counter()
        res = check_text(text, model=model, expected_model_sha256=expected)
        out.update(accepted=bool(res.accepted), reason=res.reason, full_box=res.full_box, stats=res.stats,
                   checker_model_sha256_matches_tables=res.model_sha256 == tsha, file_checksum_matches_tables=expected == tsha,
                   lower_bound_kcal=str(res.lower_bound) if res.lower_bound is not None else None,
                   witness_energy_kcal=str(res.witness_energy) if res.witness_energy is not None else None,
                   certified_gap_kcal=str(res.certified_gap) if res.certified_gap is not None else None)
    out["seconds_check"] = round(time.perf_counter() - t0, 3)
    print(json.dumps(out), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
