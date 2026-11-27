"""The exact checker on the science division's nine test vectors (P7 report §5.2).

Reads the nine certificate files and their checksum file from commit ``2b4ccdf`` of
``research/scientific-translation`` with ``git show`` (read-only; nothing of that branch is executed), and
writes ``results/vectors.json``: per file the verdicts of both engines, the verdicts on the three controls
of §5.2, the counts next to the numbers of the table of §5.2 with every difference flagged, a brute-force
minimum of the instance over the whole domain, and the consistency of the files' annotation keys.

    python experiments/eng/leafcert/run_vectors.py          (from the repository root, about 5 s)

The helpers ``build_controls``, ``energy_tensor``, ``brute_force`` and ``split_rule`` are also used by
``tests/eng/test_leafcert.py``.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.leafcert import check, loader, pycheck  # noqa: E402

COMMIT = "2b4ccdf"
BASE = "experiments/science/ws_P7"
CHECKSUM_FILE = f"{BASE}/logs/run1/cert_sha256.txt"
REPORT = "docs/science/workstreams/P7_REPORT.md"
MAX_STATES = 2_000_000          # brute force is run on domains with at most this many states

# The table of §5.2 of the report (commit 2b4ccdf), row by row: depth; leaf certificates / boxes; integers;
# additions; comparisons; "with a domain-split rule: additions / comparisons" (None where the table has a
# dash); states of the domain (the table gives it on the first row of each instance only).
REPORT_TABLE = {
    "Ser6, one leaf per state": dict(depth=1, leaf_certificates=9, leaf_boxes=9, integers=2619, additions=17640,
                                     comparisons=8118, split=None, states=531441),
    "Ser6, shared leaves": dict(depth=1, leaf_certificates=2, leaf_boxes=9, integers=582, additions=17640,
                                comparisons=8118, split=(4585, 2126), states=None),
    "Lys3, one leaf per state": dict(depth=1, leaf_certificates=21, leaf_boxes=21, integers=3486, additions=41643,
                                     comparisons=20790, split=None, states=18270),
    "Lys3, shared leaves": dict(depth=1, leaf_certificates=2, leaf_boxes=21, integers=332, additions=41643,
                                comparisons=20790, split=(6246, 3120), states=None),
    "LKSE:6, one leaf per state (site 3)": dict(depth=1, leaf_certificates=13, leaf_boxes=13, integers=5473,
                                                additions=44668, comparisons=20891, split=None, states=341172),
    "LKSE:6, shared leaves (site 1)": dict(depth=1, leaf_certificates=3, leaf_boxes=27, integers=1263,
                                           additions=59886, comparisons=27513, split=(9318, 4353), states=None),
    "Leu16": dict(depth=2, leaf_certificates=3, leaf_boxes=3, integers=1848, additions=4354, comparisons=1386,
                  split=None, states=65536),
}
# file -> row of the table (the table has seven rows for nine files: the two Ser6 files at tau 0.70 carry
# the same integers as those at tau 0.60 -- report §0: "the same domain at both clash thresholds")
FILES = {
    "p7_02_cert_S6_E_tau0.60_ff03.json": "Ser6, one leaf per state",
    "p7_02_cert_S6_E_tau0.70_ff03.json": "Ser6, one leaf per state",
    "p7_02_certB_S6_E_tau0.60_ff03.json": "Ser6, shared leaves",
    "p7_02_certB_S6_E_tau0.70_ff03.json": "Ser6, shared leaves",
    "p7_02_cert_K3_H_tau0.60_ff99SB.json": "Lys3, one leaf per state",
    "p7_02_certB_K3_H_tau0.60_ff99SB.json": "Lys3, shared leaves",
    "p7_02_cert_LKSE6_E_tau0.60_ff99SB.json": "LKSE:6, one leaf per state (site 3)",
    "p7_02_certB_LKSE6_E_tau0.60_ff99SB.json": "LKSE:6, shared leaves (site 1)",
    "p7_02_cert_L16_P2_tau0.60_ff99SB.json": "Leu16",
}


# ------------------------------------------------------------------------------------------- reading the vectors
def commit_available() -> bool:
    done = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{COMMIT}^{{commit}}"], capture_output=True)
    return done.returncode == 0


def git_show(path: str) -> bytes:
    """The bytes of ``path`` at the pinned commit (``git show``; the working tree is not touched)."""
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{COMMIT}:{path}"], capture_output=True, check=True).stdout


def expected_checksums() -> dict:
    """file name -> sha256 from the checksum file of the same commit."""
    out = {}
    for line in git_show(CHECKSUM_FILE).decode("ascii").splitlines():
        digest, name = line.split()
        out[Path(name).name] = digest
    return out


def read_vector(name: str):
    """(bytes, sha256 of the bytes) of one certificate file."""
    data = git_show(f"{BASE}/out/{name}")
    return data, hashlib.sha256(data).hexdigest()


# ------------------------------------------------------------------------------------------- the three controls
def first_differing_children(node):
    """The two smallest states of a branch node whose subtrees differ, or ``None``."""
    states = sorted(node["children"], key=int)
    for x, a in enumerate(states):
        for b in states[x + 1:]:
            if node["children"][a] != node["children"][b]:
                return a, b
    return None


def build_controls(obj) -> dict:
    """The three controls of §5.2, each a certificate object that a checker must reject.

    ``bound_plus_one``      the same certificate for the bound ``L + 1``;
    ``first_leaf_alone``    the first leaf certificate of the file alone, on the whole domain (the tree is
                            one leaf node; the other leaf certificates are removed, since an unused leaf
                            certificate is a format error for this checker and the control must fail on an
                            inequality);
    ``children_exchanged``  at the root, the subtrees of two states exchanged.  The report does not say
                            which two; here: the two smallest states whose subtrees differ (exchanging
                            equal subtrees changes nothing).  ``None`` if the root is a leaf node.
    """
    plus = copy.deepcopy(obj)
    plus["L"] = obj["L"] + 1
    alone = copy.deepcopy(obj)
    alone["tree"] = {"leaf": 0}
    alone["leaves"] = [alone["leaves"][0]]
    swapped = None
    if "children" in obj["tree"]:
        pair = first_differing_children(obj["tree"])
        if pair is not None:
            swapped = copy.deepcopy(obj)
            kids = swapped["tree"]["children"]
            kids[pair[0]], kids[pair[1]] = kids[pair[1]], kids[pair[0]]
    return {"bound_plus_one": plus, "first_leaf_alone": alone, "children_exchanged": swapped}


def exchange_survey(obj) -> dict:
    """Every exchange of two children with different subtrees, at every branch node: how many of the
    resulting certificates the C engine rejects.  (An exchange that is still accepted is another valid
    certificate, not an error: a leaf certificate may hold on the box of another state.)"""
    total = rejected = 0
    accepted = []
    stack = [((), obj["tree"])]
    while stack:
        path, node = stack.pop()
        if "children" not in node:
            continue
        states = sorted(node["children"], key=int)
        for a in states:
            stack.append((path + (a,), node["children"][a]))
        for x, a in enumerate(states):
            for b in states[x + 1:]:
                if node["children"][a] == node["children"][b]:
                    continue
                mutant = copy.deepcopy(obj)
                target = mutant["tree"]
                for step in path:
                    target = target["children"][step]
                kids = target["children"]
                kids[a], kids[b] = kids[b], kids[a]
                total += 1
                if check(mutant, "c").accepted:
                    accepted.append({"node": [int(s) for s in path], "site": node["site"], "states": [int(a), int(b)]})
                else:
                    rejected += 1
    return {"exchanges": total, "rejected": rejected, "still_accepted": accepted}


# ------------------------------------------------------------------------------------------- brute force
def energy_tensor(obj) -> np.ndarray:
    """``E[x_0, .., x_{n-1}] = sum_i H_i(x_i) + sum_{i<j} J_ij(x_i, x_j)`` for every state, from the tables of
    the file (read here directly, not through the loader).  int64, exact: the sum of the largest absolute
    values of all tables is checked to be below 2^62 first."""
    H, J = obj["H"], obj["J"]
    shape = [len(row) for row in H]
    n = len(shape)
    reach = sum(max(abs(v) for v in row) for row in H)
    reach += sum(max(abs(v) for row in J[f"{i},{j}"] for v in row) for i in range(n) for j in range(i + 1, n))
    if reach >= 2 ** 62:
        raise OverflowError("tables too large for an int64 enumeration")
    E = np.zeros(shape, dtype=np.int64)
    for i in range(n):
        E += np.array(H[i], dtype=np.int64).reshape([shape[i] if d == i else 1 for d in range(n)])
    for i in range(n):
        for j in range(i + 1, n):
            E += np.array(J[f"{i},{j}"], dtype=np.int64).reshape([shape[d] if d in (i, j) else 1 for d in range(n)])
    return E


def brute_force(obj, E=None) -> dict:
    """Minimum of the instance over the whole domain by enumeration, and the comparison with ``L``."""
    E = energy_tensor(obj) if E is None else E
    minimum = int(E.min())
    out = {"states": int(E.size), "minimum": minimum, "bound": obj["L"], "bound_confirmed": minimum >= obj["L"],
           "bound_attained": minimum == obj["L"], "minimisers": int((E == minimum).sum())}
    ref = obj.get("ref")
    if ref is not None:
        out["energy_at_ref"] = int(E[tuple(ref)])
        out["ref_is_a_minimiser"] = out["energy_at_ref"] == minimum
    return out


def leaf_annotations_by_enumeration(obj, E) -> list:
    """The annotation ``bf_min`` of every leaf against the minimum of the instance over the leaf's ``box``
    (both annotations), and ``LB <= bf_min``.  Returns the list of disagreements."""
    out = []
    for t, leaf in enumerate(obj["leaves"]):
        if "box" not in leaf or "bf_min" not in leaf:
            continue
        low = int(E[np.ix_(*leaf["box"])].min())
        if low != leaf["bf_min"]:
            out.append(f"leaves[{t}].bf_min = {leaf['bf_min']}, enumeration over its box gives {low}")
        if "LB" in leaf and leaf["LB"] > low:
            out.append(f"leaves[{t}].LB = {leaf['LB']} exceeds the minimum {low} over its box")
    return out


# ------------------------------------------------------------------------------------------- domain-split rule
def split_rule(obj) -> dict:
    """What the check would cost "with a domain-split rule" (last columns of the table of §5.2): every leaf
    certificate checked once, on the per-site union of the boxes of the nodes that use it.  A leaf
    certificate that holds on that box holds on each of the boxes it contains, so acceptance here implies
    acceptance of the tree; the converse can fail when the union is not itself one of the boxes."""
    tab = pycheck.Tables(obj)
    nodes = pycheck.flatten(obj["tree"], tab.k, len(tab.leaves))
    hull = [[set() for _ in range(tab.n)] for _ in tab.leaves]
    for t, path in nodes:
        for i, dom in enumerate(pycheck.box_of(path, tab.k)):
            hull[t][i].update(dom)
    additions = comparisons = 0
    accepted = True
    for t in range(len(tab.leaves)):
        box = [sorted(dom) for dom in hull[t]]
        failure, site_terms, pair_terms, total_done = pycheck.first_violation(tab, t, box, tab.L)
        add, cmp_ = pycheck.cost(tab.n, site_terms, pair_terms, total_done)
        additions += add
        comparisons += cmp_
        accepted = accepted and failure is None
    return {"accepted": accepted, "additions": additions, "comparisons": comparisons}


# ------------------------------------------------------------------------------------------- main
def engine_summary(result) -> dict:
    return {"verdict": result.verdict, "kind": result.kind, "failure": result.failure, "counts": result.counts}


def run_one(name: str, checksums: dict) -> dict:
    data, digest = read_vector(name)
    obj = loader.parse_json_strict(data)
    row = FILES[name]
    table = REPORT_TABLE[row]
    rc, rp = check(data, "c"), check(data, "python")
    ours = rc.counts or {}
    split = split_rule(obj)
    differences = []
    for key, mine in (("depth", ours.get("depth")), ("leaf_certificates", ours.get("leaf_certificates")),
                      ("leaf_boxes", ours.get("leaf_boxes")), ("integers", ours.get("cert_integers")),
                      ("additions", ours.get("additions")), ("comparisons", ours.get("comparisons"))):
        if mine != table[key]:
            differences.append(f"{key}: ours {mine}, report {table[key]}")
    if table["split"] is not None and (split["additions"], split["comparisons"]) != table["split"]:
        differences.append(f"split rule: ours {split['additions']} / {split['comparisons']}, report {table['split']}")
    E = energy_tensor(obj) if int(np.prod([len(row_) for row_ in obj["H"]], dtype=object)) <= MAX_STATES else None
    brute = brute_force(obj, E) if E is not None else None
    if brute is not None and table["states"] is not None and brute["states"] != table["states"]:
        differences.append(f"states of the domain: ours {brute['states']}, report {table['states']}")
    controls = {}
    for label, control in build_controls(obj).items():
        cc, cp = check(control, "c"), check(control, "python")
        controls[label] = {"c": engine_summary(cc), "python": engine_summary(cp),
                           "rejected_by_both_on_an_inequality": cc.kind == cp.kind == "inequality",
                           "engines_agree": engine_summary(cc) == engine_summary(cp)}
    return {
        "file": f"{BASE}/out/{name}",
        "sha256": digest,
        "sha256_matches_checksum_file": checksums.get(name) == digest,
        "report_row": row,
        "c": engine_summary(rc),
        "python": engine_summary(rp),
        "engines_agree": engine_summary(rc) == engine_summary(rp),
        "counts": {"depth": ours.get("depth"), "leaf_certificates": ours.get("leaf_certificates"),
                   "leaf_boxes": ours.get("leaf_boxes"), "integers": ours.get("cert_integers"),
                   "instance_integers": ours.get("instance_integers"), "additions": ours.get("additions"),
                   "comparisons": ours.get("comparisons")},
        "report_table": {key: (list(value) if isinstance(value, tuple) else value) for key, value in table.items()},
        "split_rule": split,
        "differences_from_report": differences,
        "controls": controls,
        "exchange_survey": exchange_survey(obj),
        "brute_force": brute,
        "annotation_findings": list(rc.notes) + (leaf_annotations_by_enumeration(obj, E) if E is not None else []),
    }


def main() -> int:
    if not commit_available():
        print(f"commit {COMMIT} (research/scientific-translation) is not in this clone; nothing was run")
        return 2
    t0 = time.perf_counter()
    checksums = expected_checksums()
    rows = [run_one(name, checksums) for name in FILES]
    ok = True
    print(f"{'file':44s} {'C':7s} {'Python':7s} controls(rejected) counts=table  brute force")
    for row in rows:
        controls_ok = all(c["rejected_by_both_on_an_inequality"] for c in row["controls"].values())
        good = (row["c"]["verdict"] == row["python"]["verdict"] == "accept" and row["engines_agree"] and controls_ok
                and not row["differences_from_report"] and row["sha256_matches_checksum_file"]
                and (row["brute_force"] is None or row["brute_force"]["bound_confirmed"]))
        ok = ok and good
        brute = row["brute_force"]
        print(f"{Path(row['file']).name:44s} {row['c']['verdict']:7s} {row['python']['verdict']:7s} "
              f"{sum(c['rejected_by_both_on_an_inequality'] for c in row['controls'].values())}/3               "
              f"{'yes' if not row['differences_from_report'] else 'NO: ' + '; '.join(row['differences_from_report'])}"
              f"           min {brute['minimum'] if brute else 'not run'} over {brute['states'] if brute else '-'} states"
              f"{'' if good else '   <-- CHECK'}")
    out = {
        "source": {"commit": COMMIT, "branch": "research/scientific-translation", "directory": f"{BASE}/out",
                   "checksum_file": CHECKSUM_FILE, "report_table": f"{REPORT} section 5.2"},
        "summary": {
            "files": len(rows),
            "accepted_by_both_engines": sum(r["c"]["verdict"] == r["python"]["verdict"] == "accept" for r in rows),
            "controls": sum(len(r["controls"]) for r in rows),
            "controls_rejected_by_both_engines_on_an_inequality":
                sum(c["rejected_by_both_on_an_inequality"] for r in rows for c in r["controls"].values()),
            "files_whose_counts_equal_the_report_table": sum(not r["differences_from_report"] for r in rows),
            "files_checked_by_brute_force": sum(r["brute_force"] is not None for r in rows),
            "files_with_bound_confirmed_by_brute_force":
                sum(bool(r["brute_force"] and r["brute_force"]["bound_confirmed"]) for r in rows),
            "files_with_annotation_findings": sum(bool(r["annotation_findings"]) for r in rows),
            "all_as_expected": ok,
        },
        "vectors": rows,
    }
    target = Path(__file__).with_name("results") / "vectors.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(out, indent=1) + "\n")
    print(f"wrote {target.relative_to(ROOT)}   ({time.perf_counter() - t0:.1f} s)   all as expected: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
