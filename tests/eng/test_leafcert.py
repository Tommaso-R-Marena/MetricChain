"""Tests of the exact checker for "shares at the leaves" certificates (``src/metricchain_eng/leafcert``).

The checker was written from the text of the science division's P7 report (§5.1-5.4 at commit ``2b4ccdf``
of ``research/scientific-translation``); these tests try to break it.  Layers:

  1. the nine certificate files of that commit (read with ``git show``, sha256 against the checksum file of
     the same commit): accepted by both engines with the counts of the report's table; the three controls
     of §5.2 rejected on an inequality; the bound confirmed by enumeration of the whole domain;
  2. the strict loader, the Python engine and the C parser each reject malformed input, with a reason;
  3. boundary cases (empty domain, one-state site, depth 0, missing and extra children, integers at the
     64-bit limit);
  4. soundness fuzz: thousands of small random instances with certificates from a producer written here
     (exact dynamic programming, linear programmes, random messages; random trees with shared leaves) and
     with adversarial variants; whenever an engine accepts a bound, enumeration must confirm it, and the
     two engines must agree on verdict, first failing inequality and operation counts;
  5. mutation of accepted certificates: every integer changed by +-1, by a large amount and to the exact
     edge of its slack; subtrees swapped, deleted, duplicated, leaf indices changed.  The verdict on every
     mutant is predicted from the slacks by a third evaluator written here, and every accepted mutant is
     confirmed by enumeration;
  6. the tests have teeth: deliberately broken copies of both checkers must be caught by the fuzz corpus;
  7. the C parser against corrupted encodings, compared with a decoder written here, and run under the
     address and undefined-behaviour sanitizers.

``LEAFCERT_FUZZ=k`` multiplies the size of layers 4, 5 and 7 by ``k`` and extends layer 5 to all nine
files (default 1: the whole file runs in under a minute); ``LEAFCERT_SEED`` changes the seed.  Statistics
are printed (``pytest -s`` or ``-rP``) on lines that start with ``LEAFCERT``.
"""
from __future__ import annotations

import copy
import itertools
import json
import os
import pickle
import random
import shutil
import subprocess
import sys
import types
from collections import Counter
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "leafcert"))

from metricchain_eng.leafcert import check, ckernel, loader, pycheck  # noqa: E402
import run_vectors as rv  # noqa: E402

SCALE = max(1, int(os.environ.get("LEAFCERT_FUZZ", "1")))
SEED = int(os.environ.get("LEAFCERT_SEED", "20261126"))
INT64_MIN, INT64_MAX = -2 ** 63, 2 ** 63 - 1
HAVE_COMMIT = rv.commit_available()
NO_COMMIT = (f"commit {rv.COMMIT} of research/scientific-translation (the science division's nine test vectors) "
             f"is not in this clone: fetch that branch to run these tests")


# ================================================================================================ helpers
def strip(result):
    """An engine's result without its wording."""
    return {key: result[key] for key in ("accepted", "kind", "failure", "bound", "counts")}


def front(result):
    """The same for a ``Result`` of the front door."""
    return {"accepted": result.accepted, "kind": result.kind, "failure": result.failure, "bound": result.bound,
            "counts": result.counts}


def clone(obj):
    return pickle.loads(pickle.dumps(obj, -1))


def run_engines(obj):
    """Both engines without the front door: ``pycheck`` on the object, ``leafcert.c`` on the encoding of
    ``loader.validate(obj)``.  The loader and ``pycheck`` must agree on well-formedness, the two engines on
    everything but the wording.  Returns the Python engine's result."""
    rp = pycheck.verify(obj)
    try:
        cert = loader.validate(obj)
    except loader.FormatError as exc:
        assert rp["kind"] == "format", f"the loader rejects ({exc}) but pycheck returns {rp}"
        assert str(exc) and rp["reason"]
        return rp
    assert rp["kind"] != "format", f"pycheck rejects the format ({rp['reason']}) but the loader accepts"
    rc = ckernel.check_encoded(loader.encode(cert))
    assert strip(rc) == strip(rp), f"engines differ:\n C      {rc}\n Python {rp}"
    return rp


def brute_min(obj):
    """Minimum of the instance over the whole domain, by enumeration with Python integers."""
    H, J = obj["H"], obj["J"]
    n = len(H)
    tables = [(i, j, J[f"{i},{j}"]) for i in range(n) for j in range(i + 1, n)]
    best = None
    for x in itertools.product(*[range(len(row)) for row in H]):
        e = 0
        for i in range(n):
            e += H[i][x[i]]
        for i, j, table in tables:
            e += table[x[i]][x[j]]
        if best is None or e < best:
            best = e
    return best


def visits(obj):
    """Leaf nodes of a well-formed tree in the order of the traversal: ``(leaf index, {site: state})``."""
    shape = [len(row) for row in obj["H"]]
    out = []

    def walk(node, fixed):
        if "leaf" in node:
            out.append((node["leaf"], dict(fixed)))
            return
        site = node["site"]
        for a in range(shape[site]):
            fixed[site] = a
            walk(node["children"][str(a)], fixed)
            del fixed[site]

    walk(obj["tree"], {})
    return out


def slack_table(obj):
    """Third evaluator (neither engine's code): for every leaf node, in order, the slack ``right - left`` of
    every inequality of the leaf rule; dicts in the order in which a checker meets the inequalities."""
    H, J, L = obj["H"], obj["J"], obj["L"]
    n = len(H)
    table = []
    for t, fixed in visits(obj):
        leaf = obj["leaves"][t]
        U, P2, m = leaf["U"], leaf["P2"], leaf["m"]
        D = [[fixed[i]] if i in fixed else list(range(len(H[i]))) for i in range(n)]
        site = {(i, a): H[i][a] + sum(m[f"{i},{j}"][a] for j in range(n) if j != i) - U[i]
                for i in range(n) for a in D[i]}
        pair = {(i, j, a, b): J[f"{i},{j}"][a][b] - m[f"{i},{j}"][a] - m[f"{j},{i}"][b] - P2[f"{i},{j}"]
                for i in range(n) for j in range(i + 1, n) for a in D[i] for b in D[j]}
        table.append({"leaf": t, "fixed": fixed, "box": D, "site": site, "pair": pair,
                      "total": sum(U) + sum(P2.values()) - L})
    return table


def predicted(obj):
    """Verdict and first failing inequality according to :func:`slack_table`: ``None`` (accept) or
    ``(visit, kind, i, a, j, b)``."""
    for visit, row in enumerate(slack_table(obj)):
        for (i, a), slack in row["site"].items():
            if slack < 0:
                return visit, "site", i, a, None, None
        for (i, j, a, b), slack in row["pair"].items():
            if slack < 0:
                return visit, "pair", i, a, j, b
        if row["total"] < 0:
            return visit, "total", None, None, None, None
    return None


def located(result):
    """The first failing inequality of an engine's result in the form of :func:`predicted`."""
    f = result["failure"]
    return None if f is None else (f["visit"], f["inequality"], f["i"], f["a"], f["j"], f["b"])


def violations(obj):
    """All violated inequalities as ``(visit, kind)`` according to :func:`slack_table`."""
    out = []
    for visit, row in enumerate(slack_table(obj)):
        out += [(visit, "site")] * sum(s < 0 for s in row["site"].values())
        out += [(visit, "pair")] * sum(s < 0 for s in row["pair"].values())
        out += [(visit, "total")] * (row["total"] < 0)
    return out


def emit(label, stats):
    print(f"LEAFCERT {label}: {json.dumps(stats, sort_keys=True)}")


# ================================================================================================ 1. the nine vectors
_VECTORS = {}


def load_vectors():
    """The nine files at the pinned commit (``{}`` if the commit is not in this clone)."""
    if HAVE_COMMIT and not _VECTORS:
        sums = rv.expected_checksums()
        for name in rv.FILES:
            data, digest = rv.read_vector(name)
            _VECTORS[name] = {"data": data, "sha256": digest, "expected_sha256": sums.get(name),
                              "obj": loader.parse_json_strict(data)}
    return _VECTORS


@pytest.fixture(scope="module")
def vectors():
    if not HAVE_COMMIT:
        pytest.skip(NO_COMMIT)
    return load_vectors()


_TENSORS = {}


def tensor(obj):
    """Energy of every state (cached: the four Ser6 files carry the same tables)."""
    key = json.dumps([obj["H"], obj["J"]], sort_keys=True)
    if key not in _TENSORS:
        _TENSORS[key] = rv.energy_tensor(obj)
    return _TENSORS[key]


def test_the_checksum_file_lists_exactly_the_nine_files(vectors):
    assert set(rv.expected_checksums()) == set(rv.FILES) and len(rv.FILES) == 9


@pytest.mark.parametrize("name", list(rv.FILES))
def test_vector_is_accepted_by_both_engines_with_the_counts_of_the_report(vectors, name):
    v = vectors[name]
    assert v["sha256"] == v["expected_sha256"], "the file differs from the one the science division hashed"
    rc, rp = check(v["data"], "c"), check(v["data"], "python")
    assert rc.accepted and rp.accepted and bool(rc) and rc.verdict == "accept", (rc.reason, rp.reason)
    assert front(rc) == front(rp)
    assert strip(run_engines(v["obj"])) == front(rc)                 # the route without the front door
    assert rc.notes == () and rp.notes == ()                         # the annotation keys agree with the certificate
    row = rv.REPORT_TABLE[rv.FILES[name]]
    counts = rc.counts
    assert (counts["depth"], counts["leaf_certificates"], counts["leaf_boxes"], counts["cert_integers"],
            counts["additions"], counts["comparisons"]) == (row["depth"], row["leaf_certificates"], row["leaf_boxes"],
                                                            row["integers"], row["additions"], row["comparisons"])
    assert predicted(v["obj"]) is None                               # the third evaluator


@pytest.mark.parametrize("name", list(rv.FILES))
def test_vector_controls_are_rejected_on_an_inequality(vectors, name):
    obj = vectors[name]["obj"]
    controls = rv.build_controls(obj)
    assert set(controls) == {"bound_plus_one", "first_leaf_alone", "children_exchanged"}
    for label, control in controls.items():
        assert control is not None and control != obj, label
        rc, rp = check(control, "c"), check(control, "python")
        assert not rc.accepted and not rp.accepted and not bool(rc) and rc.verdict == "reject", label
        assert rc.kind == rp.kind == "inequality", (label, rc.reason, rp.reason)    # not a format error
        assert front(rc) == front(rp), label
        assert located(front(rc)) == predicted(control), label
    # the bound is raised by exactly one unit and fails exactly on (T), in the leaf whose total is L
    f = check(controls["bound_plus_one"], "c").failure
    assert f["inequality"] == "total" and f["lhs"] == obj["L"] + 1 and f["rhs"] == obj["L"]


@pytest.mark.parametrize("name", list(rv.FILES))
def test_vector_bound_by_enumeration_of_the_whole_domain(vectors, name):
    obj = vectors[name]["obj"]
    states = 1
    for row in obj["H"]:
        states *= len(row)
    assert states <= rv.MAX_STATES                    # all nine domains are small enough (18 270 .. 531 441 states)
    E = tensor(obj)
    out = rv.brute_force(obj, E)
    assert out["states"] == states and out["bound_confirmed"] and out["minimum"] == obj["L"] == 0
    assert out["energy_at_ref"] == 0 and out["minimisers"] == 1      # the bound is attained, only at the reference
    table_states = rv.REPORT_TABLE[rv.FILES[name]]["states"]
    assert table_states in (None, states)
    assert rv.leaf_annotations_by_enumeration(obj, E) == []          # the files' bf_min and LB <= bf_min


def test_vector_split_rule_columns(vectors):
    for name, row_name in rv.FILES.items():
        row, out = rv.REPORT_TABLE[row_name], rv.split_rule(vectors[name]["obj"])
        assert out["accepted"]
        want = row["split"] or (row["additions"], row["comparisons"])    # a dash in the table: nothing is shared
        assert (out["additions"], out["comparisons"]) == want, name


def test_vector_first_leaf_with_the_other_leaves_left_in_the_file_is_a_format_error(vectors):
    """The other way to build control (ii): this checker then rejects before any arithmetic (unused leaf
    certificates), which is why ``build_controls`` removes them."""
    obj = clone(vectors["p7_02_cert_L16_P2_tau0.60_ff99SB.json"]["obj"])
    obj["tree"] = {"leaf": 0}
    for engine in ("c", "python"):
        result = check(obj, engine)
        assert result.kind == "format" and "not referenced" in result.reason


def test_vectors_stand_alone_executable(vectors, tmp_path):
    exe = ckernel.executable()
    names, expected = [], []
    for name, v in vectors.items():
        for label, obj in [("vector", v["obj"])] + list(rv.build_controls(v["obj"]).items()):
            path = tmp_path / f"{len(names)}.txt"
            path.write_bytes(loader.encode(loader.validate(obj)))
            names.append(str(path))
            expected.append(ckernel.check_encoded(path.read_bytes()))
    done = subprocess.run([str(exe), *names], capture_output=True, text=True)
    assert done.returncode == 1 and done.stderr == ""                # some files (the controls) are rejected
    lines = done.stdout.splitlines()
    assert len(lines) == len(names) == 36
    for line, want in zip(lines, expected):
        verdict = line.split(": ", 1)[1]
        if want["accepted"]:
            assert verdict.startswith("ACCEPT bound=0 ") and f" additions={want['counts']['additions']} " in verdict
        else:
            f = want["failure"]
            assert verdict.startswith(f"REJECT inequality inequality={f['inequality']} visit={f['visit']} leaf={f['leaf']} ")
            assert f" lhs={f['lhs']} rhs={f['rhs']} " in verdict
    alone = subprocess.run([str(exe), names[0]], capture_output=True, text=True)
    assert alone.returncode == 0 and alone.stdout.split(": ", 1)[1].startswith("ACCEPT")
    assert subprocess.run([str(exe), str(tmp_path / "missing")], capture_output=True).returncode == 2


# ================================================================================================ a producer (tests only)
# Small integer instances and certificates built here, independently of the science division's producer.
# The step that makes every certificate valid by construction is ``leaf_from_messages``: for ANY integer
# messages, U and P2 are computed as the exact minima of the brackets over the box.
def pairs_of(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def jval(inst, p, q, a, b):
    """J_pq(a, b), whichever of p, q is smaller."""
    return inst["J"][f"{p},{q}"][a][b] if p < q else inst["J"][f"{q},{p}"][b][a]


def zero_messages(inst):
    shape = [len(row) for row in inst["H"]]
    return {(i, j): [0] * shape[i] for i in range(len(shape)) for j in range(len(shape)) if i != j}


def leaf_from_messages(inst, D, m):
    H = inst["H"]
    n = len(H)
    U = [min(H[i][a] + sum(m[i, j][a] for j in range(n) if j != i) for a in D[i]) for i in range(n)]
    P2 = {f"{i},{j}": min(jval(inst, i, j, a, b) - m[i, j][a] - m[j, i][b] for a in D[i] for b in D[j])
          for i, j in pairs_of(n)}
    return {"U": U, "P2": P2, "m": {f"{i},{j}": list(vec) for (i, j), vec in m.items()}}


def random_messages(inst, D, rng):
    m = zero_messages(inst)
    for vec in m.values():
        for a in range(len(vec)):
            vec[a] = rng.randint(-4, 4)
    return m


def dp_messages(inst, D, rng):
    """Exact dynamic programming.  Pairs with a fixed site are folded into the free site; on the free sites
    a spanning forest is chosen (pairs that are not identically zero on the box first) and min-sum messages
    are passed from the leaves of each tree to its root; pairs outside the forest keep zero messages.  The
    resulting bound is the exact minimum over the box whenever every pair of free sites that is not
    identically zero on the box lies in the forest (always if at most two sites are free)."""
    H = inst["H"]
    n = len(H)
    shape = [len(row) for row in H]
    m = zero_messages(inst)
    free = [i for i in range(n) if len(D[i]) > 1]
    for i in free:
        for j in range(n):
            if len(D[j]) == 1:
                m[i, j] = [jval(inst, i, j, a, D[j][0]) for a in range(shape[i])]
    edges = [(p, q) for x, p in enumerate(free) for q in free[x + 1:]]
    rng.shuffle(edges)
    edges.sort(key=lambda e: all(jval(inst, e[0], e[1], a, b) == 0 for a in D[e[0]] for b in D[e[1]]))
    group = {i: i for i in free}

    def find(v):
        while group[v] != v:
            v = group[v]
        return v

    adj = {i: [] for i in free}
    for p, q in edges:
        if find(p) != find(q):
            group[find(p)] = find(q)
            adj[p].append(q)
            adj[q].append(p)
    seen = set()
    roots = list(free)
    rng.shuffle(roots)
    for root in roots:
        if root in seen:
            continue
        order, parent = [root], {root: None}
        seen.add(root)
        for v in order:
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    parent[w] = v
                    order.append(w)
        for c in reversed(order[1:]):
            p = parent[c]
            theta = [H[c][b] + sum(m[c, j][b] for j in range(n) if j != c and j != p) for b in range(shape[c])]
            m[p, c] = [min(jval(inst, p, c, a, b) + theta[b] for b in D[c]) for a in range(shape[p])]
            m[c, p] = [-theta[b] for b in range(shape[c])]
    return m


def lp_messages(inst, D, rng):
    """The dual of the pairwise relaxation of the box, solved in floating point (scipy/HiGHS), the messages
    rounded to integers.  Floating point is used to *propose* messages only; ``leaf_from_messages`` then
    computes U and P2 exactly."""
    from scipy.optimize import linprog
    H = inst["H"]
    n = len(H)
    col = {}
    for i in range(n):
        col["U", i] = len(col)
    for pair in pairs_of(n):
        col["P", pair] = len(col)
    for i in range(n):
        for j in range(n):
            if i != j:
                for a in D[i]:
                    col["m", i, j, a] = len(col)
    rows, rhs = [], []
    for i in range(n):
        for a in D[i]:
            row = np.zeros(len(col))
            row[col["U", i]] = 1
            for j in range(n):
                if j != i:
                    row[col["m", i, j, a]] = -1
            rows.append(row)
            rhs.append(H[i][a])
    for i, j in pairs_of(n):
        for a in D[i]:
            for b in D[j]:
                row = np.zeros(len(col))
                row[col["P", (i, j)]] = row[col["m", i, j, a]] = row[col["m", j, i, b]] = 1
                rows.append(row)
                rhs.append(jval(inst, i, j, a, b))
    cost = np.zeros(len(col))
    cost[: n + len(pairs_of(n))] = -1
    res = linprog(cost, A_ub=np.array(rows), b_ub=np.array(rhs, dtype=float), bounds=[(None, None)] * len(col),
                  method="highs")
    m = zero_messages(inst)
    if res.status == 0:
        for key, index in col.items():
            if key[0] == "m":
                m[key[1], key[2]][key[3]] = int(round(float(res.x[index])))
    return m


PRODUCERS = {"zero": lambda inst, D, rng: zero_messages(inst), "random": random_messages, "dp": dp_messages,
             "lp": lp_messages}


def random_instance(rng, style=None):
    """2-5 sites with 2-4 states (sometimes a site with one state), small integer tables with negative
    entries and ties.  Styles: all pairs coupled, some pairs, a chain, a tree, a ring (frustrated cycles:
    the relaxation has a gap), and ``termwise``: every table has its unique minimum at one common state, so
    that the certificate with zero messages is tight and every inequality has exactly one tight state."""
    n = rng.randint(2, 5)
    shape = [rng.choice((2, 2, 3, 3, 4)) for _ in range(n)]
    if rng.random() < 0.2:
        shape = [rng.choice((2, 3))] * n                 # uniform alphabet
    elif rng.random() < 0.1:
        shape[rng.randrange(n)] = 1                      # a site with one state
    style = style or rng.choice(("dense", "dense", "sparse", "chain", "tree", "ring", "termwise", "termwise"))
    R = rng.choice((1, 2, 3, 6, 25))
    pairs = pairs_of(n)
    order = list(range(n))
    rng.shuffle(order)
    link = lambda u, v: (min(u, v), max(u, v))           # noqa: E731
    if style == "sparse":
        active = {pair for pair in pairs if rng.random() < 0.5}
    elif style == "chain":
        active = {link(order[x], order[x + 1]) for x in range(n - 1)}
    elif style == "ring":
        active = {link(order[x], order[(x + 1) % n]) for x in range(n)} if n > 2 else set(pairs)
    elif style == "tree":
        active = {link(order[x], order[rng.randrange(x)]) for x in range(1, n)}
    else:
        active = set(pairs)
    if style == "termwise":
        star = [rng.randrange(k) for k in shape]
        H = [[rng.randint(1, R + 3) for _ in range(k)] for k in shape]
        J = {f"{i},{j}": [[rng.randint(1, R + 3) for _ in range(shape[j])] for _ in range(shape[i])] for i, j in pairs}
        for i in range(n):
            H[i][star[i]] = rng.randint(-R, 0)
        for i, j in pairs:
            J[f"{i},{j}"][star[i]][star[j]] = rng.randint(-R, 0)
    else:
        H = [[rng.randint(-R, R) for _ in range(k)] for k in shape]
        J = {f"{i},{j}": [[rng.randint(-R, R) if (i, j) in active else 0 for _ in range(shape[j])]
                          for _ in range(shape[i])] for i, j in pairs}
        if rng.random() < 0.3:                           # shift the minimum above zero
            lift = rng.randint(0, 2 * R * (n + len(pairs)))
            H[0] = [v + lift for v in H[0]]
    return {"shape": shape, "H": H, "J": J, "style": style}


def random_tree_shape(rng, shape, depth_cap, p_stop):
    """``None`` (a leaf node) or ``(site, [subtree per state])``; a site is branched on at most once per path."""
    def build(fixed, depth):
        free = [i for i in range(len(shape)) if i not in fixed]
        if not free or depth >= depth_cap or (depth > 0 and rng.random() < p_stop):
            return None
        site = rng.choice(free)
        return site, [build(fixed | {site}, depth + 1) for _ in range(shape[site])]
    return build(frozenset(), 0)


def assemble(rng, inst, tree_shape, producer, share=0.0):
    """A certificate object for ``inst``: a leaf certificate per leaf node (``producer`` chooses the
    messages), or, at a branch whose children are all leaf nodes and with probability ``share``, one leaf
    certificate per block of states, computed on the box of the block and shared by its children.  The
    bound is the smallest ``sum U + sum P2`` over the leaf certificates, so the certificate is valid."""
    shape = [len(row) for row in inst["H"]]
    n = len(shape)
    leaves = []

    def new_leaf(D):
        leaves.append(leaf_from_messages(inst, D, PRODUCERS[producer](inst, D, rng)))
        return {"leaf": len(leaves) - 1}

    def build(node, fixed):
        D = [[fixed[i]] if i in fixed else list(range(shape[i])) for i in range(n)]
        if node is None:
            return new_leaf(D)
        site, kids = node
        if all(kid is None for kid in kids) and len(kids) >= 2 and rng.random() < share:
            states = list(range(len(kids)))
            rng.shuffle(states)
            cut = rng.randint(1, len(states))
            children = {}
            for block in (sorted(states[:cut]), sorted(states[cut:])):
                if block:
                    ref = new_leaf(D[:site] + [block] + D[site + 1:])
                    for a in block:
                        children[str(a)] = dict(ref)
            return {"site": site, "children": children}
        return {"site": site, "children": {str(a): build(kid, {**fixed, site: a}) for a, kid in enumerate(kids)}}

    tree = build(tree_shape, {})
    L = min(sum(leaf["U"]) + sum(leaf["P2"].values()) for leaf in leaves)
    return {"shape": list(shape), "H": inst["H"], "J": inst["J"], "L": L, "tree": tree, "leaves": leaves}


def gauge(obj, t, i, j, d):
    """Add ``d`` to the message vector ``m_ij`` of leaf ``t`` and compensate in ``U_i`` and ``P2_ij``: every
    slack of the certificate stays the same."""
    leaf = obj["leaves"][t]
    leaf["m"][f"{i},{j}"] = [v + d for v in leaf["m"][f"{i},{j}"]]
    leaf["U"][i] += d
    leaf["P2"][f"{min(i, j)},{max(i, j)}"] -= d


def tiny():
    """A small valid certificate used by the format tests: 3 sites with 2, 3 and 2 states, branch on site 1,
    exact messages, three leaf certificates."""
    inst = {"H": [[-3, 0], [1, 0, 2], [0, 1]],
            "J": {"0,1": [[0, 2, -1], [1, 0, 0]], "0,2": [[0, 1], [-2, 0]], "1,2": [[0, 0], [1, -1], [0, 2]]}}
    obj = assemble(random.Random(1), inst, (1, [None, None, None]), "dp")
    assert run_engines(obj)["accepted"] and obj["L"] == brute_min(obj) == -2
    return obj


def test_the_producer_is_exact_where_it_claims_to_be():
    """Dynamic programming gives the exact minimum on chains and trees without branching, and on any
    instance once all but two sites are fixed; every certificate of every producer is accepted."""
    rng = random.Random(SEED)
    exact = 0
    for _ in range(150):
        inst = random_instance(rng)
        n = len(inst["H"])
        low = brute_min(inst)
        assert low == int(rv.energy_tensor(inst).min())               # the two enumerations agree
        for producer in PRODUCERS:
            obj = assemble(rng, inst, random_tree_shape(rng, inst["shape"], rng.randint(0, 2), 0.3), producer, 0.5)
            assert run_engines(obj)["accepted"] and obj["L"] <= low and predicted(obj) is None
        if inst["style"] in ("chain", "tree", "termwise"):
            obj = assemble(rng, inst, None, "dp")
            assert obj["L"] == low and run_engines(obj)["accepted"]
            exact += 1
        obj = assemble(rng, inst, random_tree_shape(rng, inst["shape"], max(0, n - 2), 0.0), "dp")
        assert obj["L"] == low and run_engines(obj)["accepted"]
        if inst["style"] == "termwise":
            assert assemble(rng, inst, None, "zero")["L"] == low
    assert exact >= 30


# ================================================================================================ 2. malformed input
def _set(path, value):
    """A mutation: set ``obj[path[0]]..[path[-1]] = value``."""
    def apply(obj):
        for key in path[:-1]:
            obj = obj[key]
        obj[path[-1]] = value
    return apply


def _del(*path):
    def apply(obj):
        for key in path[:-1]:
            obj = obj[key]
        del obj[path[-1]]
    return apply


def _call(fn):
    return fn


# (what the loader must complain about, mutation of the object of ``tiny()``)
MALFORMED = [
    ("missing key", _del("H")), ("missing key", _del("J")), ("missing key", _del("L")),
    ("missing key", _del("tree")), ("missing key", _del("leaves")),
    ("unexpected key", _set(["domain"], [[0, 1], [0, 1, 2], [0, 1]])),
    ("unexpected key", _set(["triples"], [])),
    ("H: expected a list", _set(["H"], {"0": [0, 3]})),
    ("H: no site", _set(["H"], [])),
    ("H[1]: expected a list", _set(["H", 1], 7)),
    ("empty domain", _set(["H", 1], [])),
    ("H[0]", _set(["H", 0, 1], 3.0)), ("H[0]", _set(["H", 0, 1], "3")), ("H[0]", _set(["H", 0, 1], True)),
    ("H[0]", _set(["H", 0, 1], None)), ("H[0]", _set(["H", 0, 1], [3])),
    ("shape", _set(["H", 0], [-3, 0, 5])),                              # one more state than shape and J say
    ("J['0,1']: expected 3 rows", _call(lambda obj: (obj.pop("shape"), obj["H"].__setitem__(0, [-3, 0, 5])))),
    ("shape", _set(["shape"], [2, 3, 3])), ("shape", _set(["shape"], [2, 3])), ("shape", _set(["shape"], "2,3,2")),
    ("shape", _set(["shape"], [True, 3, 2])), ("shape", _set(["shape"], [2.0, 3, 2])),
    ("J: missing key", _del("J", "0,2")),
    ("J: unexpected key", _set(["J", "2,0"], [[0, -2], [1, 0]])),
    ("J: unexpected key", _set(["J", "0, 1"], [[0, 2, -1], [1, 0, 0]])),
    ("J: unexpected key", _set(["J", "0,0"], [[0, 0], [0, 0]])),
    ("J: expected an object", _set(["J"], [[0]])),
    ("J['0,1']: expected 2 rows", _set(["J", "0,1"], [[0, 2, -1]])),
    ("J['0,1'][1]: expected 3 integers", _set(["J", "0,1", 1], [1, 0])),
    ("J['0,1'][1]: expected 3 integers", _set(["J", "0,1", 1], [1, 0, 0, 0])),
    ("J['0,1'][0][2]", _set(["J", "0,1", 0, 2], -1.0)),
    ("J['1,2']: expected a list", _set(["J", "1,2"], None)),
    ("L: expected an integer", _set(["L"], -2.0)), ("L: expected an integer", _set(["L"], "-2")),
    ("L: expected an integer", _set(["L"], False)), ("L: expected an integer", _set(["L"], None)),
    ("L: expected an integer", _set(["L"], [0])),
    ("leaves: expected a list", _set(["leaves"], {})), ("leaves: no leaf certificate", _set(["leaves"], [])),
    ("leaves[0]: expected an object", _set(["leaves", 0], [])),
    ("leaves[0]: missing key", _del("leaves", 0, "U")), ("leaves[1]: missing key", _del("leaves", 1, "P2")),
    ("leaves[2]: missing key", _del("leaves", 2, "m")),
    ("leaves[0]: unexpected key", _set(["leaves", 0, "V"], [0, 0, 0])),
    ("leaves[0].U: expected 3 integers", _set(["leaves", 0, "U"], [0, 0])),
    ("leaves[0].U: expected 3 integers", _set(["leaves", 0, "U"], [0, 0, 0, 0])),
    ("leaves[0].U[1]", _set(["leaves", 0, "U", 1], 0.5)), ("leaves[0].U: expected a list", _set(["leaves", 0, "U"], 0)),
    ("leaves[1].P2: missing key", _del("leaves", 1, "P2", "1,2")),
    ("leaves[1].P2: unexpected key", _set(["leaves", 1, "P2", "1,0"], 0)),
    ("leaves[1].P2['0,2']", _set(["leaves", 1, "P2", "0,2"], 1.5)),
    ("leaves[1].P2['0,2']", _set(["leaves", 1, "P2", "0,2"], [0])),
    ("leaves[1].P2: expected an object", _set(["leaves", 1, "P2"], [0, 0, 0])),
    ("leaves[2].m: missing key", _del("leaves", 2, "m", "2,1")),
    ("leaves[2].m: unexpected key", _set(["leaves", 2, "m", "1,1"], [0, 0, 0])),
    ("leaves[2].m['0,1']: expected 2 integers", _set(["leaves", 2, "m", "0,1"], [0, 0, 0])),     # k_j instead of k_i
    ("leaves[2].m['1,0']: expected 3 integers", _set(["leaves", 2, "m", "1,0"], [0, 0])),
    ("leaves[2].m['1,0'][2]", _set(["leaves", 2, "m", "1,0", 2], True)),
    ("leaves[2].m: expected an object", _set(["leaves", 2, "m"], None)),
    ("tree: expected an object", _set(["tree"], [0])), ("tree: expected an object", _set(["tree"], 0)),
    ("tree: missing key", _set(["tree"], {})),
    ("tree: unexpected key", _set(["tree", "leaf"], 0)),                 # a node that is both a branch and a leaf
    ("tree: unexpected key", _set(["tree", "note"], "x")),
    ("tree: missing key", _del("tree", "children")), ("tree: missing key", _del("tree", "site")),
    ("tree.site: expected an integer", _set(["tree", "site"], "1")),
    ("tree.site: expected an integer", _set(["tree", "site"], 1.0)),
    ("tree.site: expected an integer", _set(["tree", "site"], True)),
    ("outside 0..2", _set(["tree", "site"], 3)), ("outside 0..2", _set(["tree", "site"], -1)),
    ("unexpected key(s) ['2']", _set(["tree", "site"], 0)),              # site 0 has 2 states: child "2" is extra
    ("tree.children", _set(["tree", "children"], [])),
    ("missing key(s) ['2']", _del("tree", "children", "2")),             # the children do not cover the domain
    ("missing key(s) ['0']", _del("tree", "children", "0")),
    ("unexpected key(s) ['3']", _set(["tree", "children", "3"], {"leaf": 0})),      # an extra child
    ("unexpected key(s) ['-1']", _set(["tree", "children", "-1"], {"leaf": 0})),
    ("unexpected key(s) ['01']", _set(["tree", "children", "01"], {"leaf": 0})),
    ("unexpected key(s) [' 1']", _set(["tree", "children", " 1"], {"leaf": 0})),
    ("unexpected key(s) ['+1']", _set(["tree", "children", "+1"], {"leaf": 0})),
    ("unexpected key(s) ['1.0']", _set(["tree", "children", "1.0"], {"leaf": 0})),
    ("not a string", _set(["tree", "children", 1], {"leaf": 0})),
    ("tree.children[1]: expected an object", _set(["tree", "children", "1"], 1)),
    ("tree.children[1]: missing key", _set(["tree", "children", "1"], {})),
    ("tree.children[1].leaf: expected an integer", _set(["tree", "children", "1"], {"leaf": "1"})),
    ("tree.children[1].leaf: expected an integer", _set(["tree", "children", "1"], {"leaf": 1.0})),
    ("tree.children[1].leaf: expected an integer", _set(["tree", "children", "1"], {"leaf": True})),
    ("tree.children[1].leaf: expected an integer", _set(["tree", "children", "1"], {"leaf": None})),
    ("outside 0..2", _set(["tree", "children", "1"], {"leaf": 3})),
    ("outside 0..2", _set(["tree", "children", "1"], {"leaf": -1})),
    ("already fixed", _set(["tree", "children", "1"], {"site": 1, "children": {str(a): {"leaf": 1} for a in range(3)}})),
    ("not referenced", _set(["tree", "children", "1"], {"leaf": 0})),    # leaf certificate 1 is no longer used
    ("not referenced", _call(lambda obj: obj["leaves"].append(clone(obj["leaves"][0])))),
]


@pytest.mark.parametrize("case", range(len(MALFORMED)))
def test_malformed_objects_are_rejected_with_a_reason(case):
    needle, mutate = MALFORMED[case]
    obj = tiny()
    mutate(obj)
    with pytest.raises(loader.FormatError) as info:
        loader.validate(obj)
    assert needle in str(info.value), f"the loader's reason {str(info.value)!r} does not mention {needle!r}"
    assert run_engines(obj)["kind"] == "format"                       # pycheck rejects it too, by itself
    for engine in ("c", "python"):
        result = check(obj, engine)
        assert not result.accepted and result.kind == "format" and needle in result.reason
        assert result.failure is None and result.counts is None


def test_a_document_that_is_not_an_object_is_rejected():
    for obj in ([], "certificate", None, 5, 1.5, True, [tiny()]):
        with pytest.raises((loader.FormatError, TypeError)):
            loader.validate(loader.load(obj) if isinstance(obj, dict) else obj)
        assert pycheck.verify(obj)["kind"] == "format"


def _text(obj):
    return json.dumps(obj)


JSON_CASES = [
    ("duplicate key 'L'", lambda t: t.replace('"L": -2', '"L": -2, "L": -2')),
    ("duplicate key 'L'", lambda t: t.replace('"L": -2', '"L": -3, "L": -2')),
    ("duplicate key '0'", lambda t: t.replace('"children": {"0":', '"children": {"0": {"leaf": 0}, "0":')),
    ("duplicate key '0,1'", lambda t: t.replace('"J": {"0,1":', '"J": {"0,1": [[0, 2, -1], [1, 0, 0]], "0,1":')),
    ("duplicate key 'U'", lambda t: t.replace('"leaves": [{"U":', '"leaves": [{"U": [0, 0, 0], "U":', 1)),
    ("not an integer", lambda t: t.replace('"L": -2', '"L": -2.0')),
    ("not an integer", lambda t: t.replace('"L": -2', '"L": -2e0')),
    ("not an integer", lambda t: t.replace('"L": -2', '"L": -0.2E1')),
    ("not an integer", lambda t: t.replace('"L": -2', '"L": NaN')),
    ("not an integer", lambda t: t.replace('"L": -2', '"L": -Infinity')),
    ("not valid JSON", lambda t: t.replace('"L": -2', '"L": +2')),
    ("not valid JSON", lambda t: t.replace('"L": -2', '"L": 02')),
    ("not valid JSON", lambda t: t.replace('"L": -2', '"L": 0x2')),
    ("not valid JSON", lambda t: t.replace('"L": -2', '"L": -2,')[:-1] + ",}"),
    ("not valid JSON", lambda t: t + "x"), ("not valid JSON", lambda t: t + t), ("not valid JSON", lambda t: t[:-1]),
    ("not valid JSON", lambda t: t[: len(t) // 2]), ("not valid JSON", lambda t: ""), ("not valid JSON", lambda t: " "),
    ("not valid JSON", lambda t: "﻿" + t),                         # byte order mark
    ("not valid JSON", lambda t: t.replace('"L": -2', "'L': -2")),
    ("not valid JSON", lambda t: t.replace('"L": -2', '"L": ' + "9" * 5000)),      # beyond the interpreter's digit limit
    ("expected an integer", lambda t: t.replace('"L": -2', '"L": "-2"')),
    ("expected an integer", lambda t: t.replace('"L": -2', '"L": true')),
    ("expected an integer", lambda t: t.replace('"L": -2', '"L": null')),
    ("top level: expected an object", lambda t: "[" + t + "]"),
    ("top level: expected an object", lambda t: "0"),
    ("nesting too deep", lambda t: "[" * 100000 + "]" * 100000),
]


@pytest.mark.parametrize("case", range(len(JSON_CASES)))
def test_malformed_json_text_is_rejected_with_a_reason(case):
    needle, mutate = JSON_CASES[case]
    good = _text(tiny())
    assert check(good.encode(), "python").accepted
    bad = mutate(good)
    assert bad != good
    for engine in ("c", "python"):
        result = check(bad.encode("utf-8"), engine)
        assert result.kind == "format" and needle in result.reason, result.reason


def test_json_encodings_and_paths(tmp_path):
    good = _text(tiny())
    for engine in ("c", "python"):
        assert check(good.encode("utf-16"), engine).kind == "format"         # only UTF-8 is read
        assert check(b"\xff\xfe" + good.encode(), engine).kind == "format"
        assert "not UTF-8" in check(good.encode() + b"\xc3", engine).reason
    path = tmp_path / "tiny.json"
    path.write_text(good)
    assert check(path, "c").accepted and check(str(path), "python").accepted
    assert check(good.replace('"L": -2', '"L": -0').encode()).kind == "inequality"   # "-0" is the integer 0: a bound above the minimum
    with pytest.raises(OSError):
        check(tmp_path / "absent.json")
    with pytest.raises(TypeError):
        check(3.5)
    with pytest.raises(ValueError):
        check(tiny(), engine="lean")


def test_annotation_keys_never_change_a_verdict_but_are_reported():
    obj = tiny()
    base = front(check(obj, "c"))
    noted = clone(obj)
    noted.update({"label": "x", "note": "y", "ref": [1, 0, 0], "depth": 7, "n_leaf_boxes": 3, "n_leaf_certificates": 2,
                  "order": 3, "unit_log2": -40})
    noted["leaves"][0].update({"kind": "N", "box": [[0, 1], [0], [0, 1]], "LB": 99, "nstates": 5, "bf_min": 0})
    for engine in ("c", "python"):
        result = check(noted, engine)
        assert front(result) == base
        text = " | ".join(result.notes)
        for needle in ("depth = 7", "n_leaf_certificates = 2", "order = 3", "at ref", "leaves[0].LB", "leaves[0].nstates",
                       "leaves[0].kind"):
            assert needle in text, (needle, text)
        assert "n_leaf_boxes" not in text and "leaves[0].box" not in text      # these two are right
    noted["ref"] = [0, 3, 0]
    assert "ref is not a state" in " ".join(check(noted, "c").notes)


# ------------------------------------------------------------------------------------------------ the C parser
def tokens_of(obj):
    return loader.encode(loader.validate(obj)).split()


def c_kind(tokens, sep=b" "):
    out = ckernel.check_encoded(sep.join(tokens))
    assert out["reason"]
    return out["kind"]


def replaced(tokens, old, new, nth=0):
    at = [x for x, tok in enumerate(tokens) if tok == old][nth]
    return tokens[:at] + ([new] if isinstance(new, bytes) else list(new)) + tokens[at + 1:]


def with_tree(tokens, tree):
    at = tokens.index(b"tree")
    return tokens[: at + 1] + [tok.encode() for tok in loader.tree_tokens(tree)] + [b"end"]


def test_c_parser_accepts_the_encoding_whatever_the_blanks():
    toks = tokens_of(tiny())
    want = strip(pycheck.verify(tiny()))
    for sep in (b" ", b"\n", b"\t", b"\r\n", b"  \n\t "):
        assert strip(ckernel.check_encoded(sep.join(toks))) == want
        assert strip(ckernel.check_encoded(b"\n " + sep.join(toks) + b" \n\n")) == want


def test_c_parser_rejects_malformed_encodings():
    toks = tokens_of(tiny())
    L, B = (lambda t: ("L", t)), (lambda site, *kids: ("B", site, tuple(kids)))
    good_tree = B(1, (0, L(0)), (1, L(1)), (2, L(2)))
    assert with_tree(toks, good_tree) == toks
    big = str(2 ** 63).encode()
    cases = [
        ("format", []), ("format", [b""]), ("format", toks[:1]), ("format", toks[:-1]), ("format", toks + [b"end"]),
        ("format", toks + [b"0"]), ("format", toks[1:]), ("format", [b"LEAFCERT"] + toks[1:]),
        ("format", replaced(toks, b"1", b"2")), ("format", replaced(toks, b"sites", b"site")),
        ("format", replaced(toks, b"3", b"0", 0)), ("format", replaced(toks, b"3", b"-3", 0)),
        ("format", replaced(toks, b"3", b"3x", 0)), ("format", replaced(toks, b"3", b"03", 0)),
        ("format", replaced(toks, b"3", b"+3", 0)), ("format", replaced(toks, b"3", b"3.0", 0)),
        ("limit", replaced(toks, b"3", b"4097", 0)), ("limit", replaced(toks, b"3", big, 0)),
        ("format", replaced(toks, b"3", b"4", 0)), ("format", replaced(toks, b"3", b"2", 0)),
        ("format", toks[:5] + [b"0"] + toks[6:]),                        # shape 0 3 2: a site without states
        ("limit", toks[:5] + [b"1048577"] + toks[6:]),
        ("format", toks[:5] + [b"3"] + toks[6:]),                        # shape 3 3 2: the tables no longer fit
        ("format", replaced(toks, b"-2", b"-02")), ("format", replaced(toks, b"-2", b"--2")),
        ("format", replaced(toks, b"-2", b"-")), ("format", replaced(toks, b"-2", b"2-")),
        ("format", replaced(toks, b"-2", b"-2.0")), ("format", replaced(toks, b"-2", b"-2e0")),
        ("format", replaced(toks, b"-2", b"0x2")), ("format", replaced(toks, b"-2", b"-0")),
        ("format", replaced(toks, b"-2", b"+2")), ("format", replaced(toks, b"-2", "٢".encode())),
        ("format", replaced(toks, b"-2", b"2\x002")), ("format", replaced(toks, b"-2", b"\xff")),
        ("range", replaced(toks, b"-2", big)), ("range", replaced(toks, b"-2", str(-2 ** 63 - 1).encode())),
        ("range", replaced(toks, b"-2", b"9" * 1000)), ("range", replaced(toks, b"-2", b"-" + b"9" * 40)),
        ("format", replaced(toks, b"h", b"H")), ("format", replaced(toks, b"h", [b"h", b"h"])),
        ("format", replaced(toks, b"u", b"U")), ("format", replaced(toks, b"p", b"u")),
        ("format", replaced(toks, b"m", b"j")), ("format", replaced(toks, b"tree", b"Tree")),
        ("format", replaced(toks, b"end", b"END")), ("format", replaced(toks, b"leaves", [b"leaves", b"3"])),
        ("format", replaced(toks, b"leaf", [b"leaf", b"0"], 1)),         # the leaf certificates out of order
        ("format", [t for x, t in enumerate(toks) if x != toks.index(b"h") + 1]),      # a label dropped
        ("format", [t for x, t in enumerate(toks) if x != toks.index(b"h") + 2]),      # a value dropped
        ("format", toks[: toks.index(b"h") + 2] + [b"0"] + toks[toks.index(b"h") + 2:]),   # a value added
        ("format", toks[: toks.index(b"leaves") + 1] + [b"0"] + toks[toks.index(b"leaves") + 2:]),
        ("format", toks[: toks.index(b"leaves") + 1] + [b"4"] + toks[toks.index(b"leaves") + 2:]),
        ("format", toks[: toks.index(b"leaves") + 1] + [b"2"] + toks[toks.index(b"leaves") + 2:]),
        ("limit", toks[: toks.index(b"leaves") + 1] + [b"99999999999"] + toks[toks.index(b"leaves") + 2:]),
        ("format", with_tree(toks, B(1, (0, L(0)), (1, L(1))))),                         # a child is missing
        ("format", with_tree(toks, B(1, (0, L(0)), (1, L(1)), (2, L(2)), (3, L(0))))),   # an extra child
        ("format", with_tree(toks, B(1, (0, L(0)), (2, L(2)), (1, L(1))))),              # children out of order
        ("format", with_tree(toks, B(1, (0, L(0)), (1, L(1)), (1, L(2))))),              # a state twice
        ("format", with_tree(toks, B(1, (1, L(0)), (2, L(1)), (3, L(2))))),              # states 1..3
        ("format", with_tree(toks, B(1, (0, L(0)), (1, L(1)), (2, L(3))))),              # leaf index out of range
        ("format", with_tree(toks, B(3, (0, L(0)), (1, L(1)), (2, L(2))))),              # site out of range
        ("format", with_tree(toks, B(1, (0, L(0)), (1, B(1, (0, L(1)), (1, L(1)), (2, L(1)))), (2, L(2))))),   # site fixed twice
        ("format", with_tree(toks, B(1, (0, L(0)), (1, L(0)), (2, L(2))))),              # leaf certificate 1 unused
        ("format", with_tree(toks, L(0))),                                               # leaf certificates 1, 2 unused
        ("format", toks[: toks.index(b"tree") + 1] + [b"end"]),                          # no tree
        ("format", toks[: toks.index(b"tree") + 1] + [b"X", b"0", b"end"]),
        ("format", toks[: toks.index(b"tree") + 1] + [b"L", b"end"]),
        ("format", toks[: toks.index(b"tree") + 1] + [b"B", b"1", b"3", b"0", b"L", b"0", b"1", b"L", b"1", b"end"]),
        ("format", toks[: toks.index(b"tree") + 1] + [b"B", b"1", b"99999999999999999999", b"0", b"L", b"0", b"end"]),
    ]
    kinds = Counter()
    for want, case in cases:
        got = c_kind(case)
        assert got == want, (want, got, b" ".join(case)[-120:])
        kinds[got] += 1
    assert c_kind(replaced(toks, b"-2", str(2 ** 63 - 1).encode())) == "inequality"     # the two ends of the range are read
    assert c_kind(replaced(toks, b"-2", str(-2 ** 63).encode())) is None
    # sizes that a short input cannot contain are refused before anything is allocated for them
    assert c_kind([b"leafcert", b"1", b"sites", b"4096", b"shape"] + [b"1048576"] * 4096 + [b"bound", b"0"]) in ("format", "limit")
    assert c_kind([b"leafcert", b"1", b"sites", b"4096"]) == "format"
    emit("C parser, hand-made malformed encodings", dict(kinds))


def test_c_structure_checks_agree_with_the_python_side_on_malformed_trees():
    """The same malformed tree as an object (loader, pycheck) and as tokens (leafcert.c)."""
    obj, toks = tiny(), tokens_of(tiny())
    leaf = lambda t: {"leaf": t}                                         # noqa: E731
    trees = [
        ({"site": 1, "children": {"0": leaf(0), "1": leaf(1)}}, ("B", 1, ((0, ("L", 0)), (1, ("L", 1))))),
        ({"site": 1, "children": {"0": leaf(0), "1": leaf(1), "2": leaf(2), "3": leaf(0)}},
         ("B", 1, ((0, ("L", 0)), (1, ("L", 1)), (2, ("L", 2)), (3, ("L", 0))))),
        ({"site": 1, "children": {"0": leaf(0), "1": leaf(1), "2": leaf(5)}}, ("B", 1, ((0, ("L", 0)), (1, ("L", 1)), (2, ("L", 5))))),
        ({"site": 4, "children": {"0": leaf(0), "1": leaf(1), "2": leaf(2)}}, ("B", 4, ((0, ("L", 0)), (1, ("L", 1)), (2, ("L", 2))))),
        ({"site": 1, "children": {"0": leaf(0), "1": leaf(0), "2": leaf(2)}}, ("B", 1, ((0, ("L", 0)), (1, ("L", 0)), (2, ("L", 2))))),
        ({"site": 1, "children": {"0": leaf(0), "1": leaf(1),
                                  "2": {"site": 1, "children": {"0": leaf(2), "1": leaf(2), "2": leaf(2)}}}},
         ("B", 1, ((0, ("L", 0)), (1, ("L", 1)), (2, ("B", 1, ((0, ("L", 2)), (1, ("L", 2)), (2, ("L", 2)))))))),
    ]
    for json_tree, token_tree in trees:
        bad = clone(obj)
        bad["tree"] = json_tree
        assert run_engines(bad)["kind"] == "format"
        assert c_kind(with_tree(toks, token_tree)) == "format"
    # and a well-formed deeper tree goes through all three
    deep = clone(obj)
    deep["tree"]["children"]["2"] = {"site": 0, "children": {"0": leaf(2), "1": leaf(2)}}
    assert run_engines(deep)["accepted"]
    assert c_kind(with_tree(toks, ("B", 1, ((0, ("L", 0)), (1, ("L", 1)), (2, ("B", 0, ((0, ("L", 2)), (1, ("L", 2)))))))) ) is None


def test_c_source_has_no_floating_point(tmp_path):
    source = ckernel.SOURCE.read_text()
    code = "\n".join(line for line in source.split("*/", 1)[1].splitlines())       # after the header comment
    import re
    assert not re.search(r"\b(float|double|long\s+double)\b", code)
    assert not re.search(r"\b\d+\.\d*([eE][-+]?\d+)?[fFlL]?\b", re.sub(r"/\*.*?\*/|\"[^\"\n]*\"", "", code, flags=re.S))
    assert "<math.h>" not in source and "printf(\"%f" not in source
    if os.uname().machine in ("x86_64", "aarch64"):
        # the compiler refuses any use of floating-point or vector registers
        ckernel.compile_c(tmp_path / "lib.so", flags=("-mgeneral-regs-only",))
        ckernel.compile_c(tmp_path / "exe", flags=("-mgeneral-regs-only",), shared=False)
        ckernel.compile_c(tmp_path / "pedantic.so", flags=("-pedantic", "-Wconversion", "-Wshadow"))


def test_the_library_is_the_one_compiled_from_the_source():
    lib = ckernel.load_library()
    assert lib.leafcert_acc_bits() == 128 and ckernel.load_library(acc64=True).leafcert_acc_bits() == 64
    digest = __import__("hashlib").sha256(ckernel.SOURCE.read_bytes() + repr((ckernel.CFLAGS, (), True)).encode()).hexdigest()[:16]
    assert digest in lib._name and Path(lib._name).parent == ckernel.build_dir()


# ================================================================================================ 3. boundary cases
def one_site(H, U, L):
    return {"H": [list(H)], "J": {}, "L": L, "tree": {"leaf": 0}, "leaves": [{"U": [U], "P2": {}, "m": {}}]}


def test_one_site_depth_zero():
    ok = run_engines(one_site([5, 7], 5, 5))
    assert ok["accepted"] and ok["counts"] == {"leaf_certificates": 1, "leaf_boxes": 1, "depth": 0, "cert_integers": 1,
                                                "instance_integers": 2, "additions": 0, "comparisons": 3}
    assert run_engines(one_site([5, 7], 5, -10 ** 6))["accepted"]
    bad = run_engines(one_site([5, 7], 5, 6))
    assert bad["failure"] == {"inequality": "total", "visit": 0, "leaf": 0, "path": [], "i": None, "a": None, "j": None,
                              "b": None, "lhs": 6, "rhs": 5} and bad["counts"]["comparisons"] == 3
    bad = run_engines(one_site([5, 7], 6, 6))
    assert bad["failure"] == {"inequality": "site", "visit": 0, "leaf": 0, "path": [], "i": 0, "a": 0, "j": None,
                              "b": None, "lhs": 6, "rhs": 5} and bad["counts"]["comparisons"] == 1
    bad = run_engines(one_site([7, 5], 6, 6))
    assert bad["failure"]["a"] == 1 and bad["counts"]["comparisons"] == 2       # the first state passes, the second fails
    branched = one_site([5, 7], 5, 5)
    branched["tree"] = {"site": 0, "children": {"0": {"leaf": 0}, "1": {"leaf": 1}}}
    branched["leaves"].append({"U": [7], "P2": {}, "m": {}})
    out = run_engines(branched)
    assert out["accepted"] and out["counts"]["leaf_boxes"] == 2 and out["counts"]["depth"] == 1 and out["counts"]["comparisons"] == 4
    branched["leaves"][0]["U"] = [6]                                   # U_0 = 6 > H_0(0) = 5 on the box {x_0 = 0}
    assert run_engines(branched)["failure"]["path"] == [[0, 0]]
    branched["leaves"][0]["U"], branched["L"] = [5], 6                 # only the state 0 has energy below 6
    out = run_engines(branched)
    assert out["failure"]["inequality"] == "total" and out["failure"]["path"] == [[0, 0]]


def test_empty_domain_and_no_site_are_format_errors():
    """A site without states makes the domain empty: every bound would hold vacuously.  Rejected as
    malformed by the loader, by pycheck and by leafcert.c, each on its own."""
    empty = {"H": [[1, 2], []], "J": {"0,1": [[], []]}, "L": 10 ** 9, "tree": {"leaf": 0},
             "leaves": [{"U": [0, 0], "P2": {"0,1": 0}, "m": {"0,1": [0, 0], "1,0": []}}]}
    assert run_engines(empty)["kind"] == "format"
    for engine in ("c", "python"):
        assert "empty domain" in check(empty, engine).reason
    nosite = {"H": [], "J": {}, "L": 0, "tree": {"leaf": 0}, "leaves": [{"U": [], "P2": {}, "m": {}}]}
    assert run_engines(nosite)["kind"] == "format" and "no site" in check(nosite).reason
    text = b"leafcert 1 sites 2 shape 2 0 bound 0 h 0 1 2 h 1 j 0 1 leaves 1 leaf 0 u 0 0 p 0 m 0 1 0 0 m 1 0 tree L 0 end"
    out = ckernel.check_encoded(text)
    assert out["kind"] == "format" and "empty domain" in out["reason"]
    out = ckernel.check_encoded(b"leafcert 1 sites 0 shape bound 0 leaves 1 leaf 0 u p tree L 0 end")
    assert out["kind"] == "format" and "no site" in out["reason"]
    # an empty branch (no children) for the empty site is not a way round it either
    empty["tree"] = {"site": 1, "children": {}}
    assert run_engines(empty)["kind"] == "format"


def test_site_with_one_state():
    rng = random.Random(SEED + 3)
    seen = 0
    while seen < 40:
        inst = random_instance(rng)
        if 1 not in inst["shape"]:
            continue
        seen += 1
        site = inst["shape"].index(1)
        n = len(inst["shape"])
        low = brute_min(inst)
        # depth 0, and a branch on the one-state site (a single child), and full branching
        flat = assemble(rng, inst, random_tree_shape(rng, inst["shape"], max(0, n - 2), 0.0), "dp")
        single = assemble(rng, inst, (site, [None]), "lp")
        for obj in (flat, single):
            assert run_engines(obj)["accepted"] and obj["L"] <= low
        assert flat["L"] == low
        assert single["tree"] == {"site": site, "children": {"0": {"leaf": 0}}}
        over = clone(flat)
        over["L"] += 1
        assert run_engines(over)["failure"]["inequality"] == "total"
        missing = clone(single)
        missing["tree"]["children"] = {}
        assert run_engines(missing)["kind"] == "format"
        extra = clone(single)
        extra["tree"]["children"]["1"] = {"leaf": 0}
        assert run_engines(extra)["kind"] == "format"
    # all sites with one state: the domain is one state, the bound is its energy
    one = {"H": [[4], [-7], [1]], "J": {"0,1": [[2]], "0,2": [[-3]], "1,2": [[5]]}}
    obj = assemble(rng, one, None, "zero")
    assert obj["L"] == 2 == brute_min(one) and run_engines(obj)["accepted"]
    obj["L"] = 3
    assert run_engines(obj)["kind"] == "inequality"


def test_full_depth_tree_every_leaf_box_is_one_state():
    rng = random.Random(SEED + 4)
    inst = random_instance(rng, "dense")
    while len(inst["shape"]) != 5:
        inst = random_instance(rng, "dense")
    obj = assemble(rng, inst, random_tree_shape(rng, inst["shape"], 5, 0.0), "zero")
    states = int(np.prod(inst["shape"]))
    out = run_engines(obj)
    assert out["accepted"] and out["counts"]["leaf_boxes"] == states and out["counts"]["depth"] == 5
    assert out["counts"]["comparisons"] == states * (5 + 10 + 1) and obj["L"] == brute_min(inst)
    obj["L"] += 1
    out = run_engines(obj)
    E = rv.energy_tensor(inst)
    in_order = [int(E[tuple(fixed[i] for i in range(5))]) for _, fixed in visits(obj)]     # energy of each leaf box
    assert out["failure"]["inequality"] == "total" and out["failure"]["visit"] == in_order.index(min(in_order))
    assert out["failure"]["rhs"] == min(in_order) == obj["L"] - 1 and len(out["failure"]["path"]) == 5
    # one level too many: the sixth branch has to reuse a site
    obj["L"] -= 1
    node = obj["tree"]
    while "children" in node["children"]["0"]:
        node = node["children"]["0"]
    node["children"]["0"] = {"site": obj["tree"]["site"], "children": {str(a): node["children"]["0"]
                                                                        for a in range(inst["shape"][obj["tree"]["site"]])}}
    assert run_engines(obj)["kind"] == "format"


def test_tree_of_depth_200():
    """200 sites; the tree branches on every one of them in turn (a site with one state has one child), so
    the single leaf node lies 200 branches deep: the recursion of leafcert.c and the explicit stacks of the
    Python side.  Then the same with two states per site on a chain: one child of every branch is a leaf
    node, the other goes on; the exact minimum is known from dynamic programming on the chain."""
    rng = random.Random(SEED + 200)
    n = 200
    inst = {"H": [[rng.randint(-9, 9)] for _ in range(n)],
            "J": {f"{i},{j}": [[rng.randint(-9, 9)]] for i, j in pairs_of(n)}}
    obj = assemble(rng, inst, None, "zero")
    energy = sum(row[0] for row in inst["H"]) + sum(table[0][0] for table in inst["J"].values())
    assert obj["L"] == energy
    tree = {"leaf": 0}
    for site in rng.sample(range(n), n):
        tree = {"site": site, "children": {"0": tree}}
    obj["tree"] = tree
    out = run_engines(obj)
    assert out["accepted"] and out["counts"]["depth"] == n and out["counts"]["leaf_boxes"] == 1
    assert out["counts"]["comparisons"] == n + n * (n - 1) // 2 + 1
    obj["L"] += 1
    out = run_engines(obj)
    assert out["failure"]["inequality"] == "total" and len(out["failure"]["path"]) == n
    obj["L"] -= 1
    inner = obj["tree"]
    for _ in range(n - 1):
        inner = inner["children"]["0"]
    inner["children"]["0"] = {"site": inner["site"], "children": {"0": {"leaf": 0}}}      # a 201st branch must reuse a site
    assert run_engines(obj)["kind"] == "format"
    # a chain of 40 binary sites, 2^40 states, a caterpillar tree of depth 40 with 41 leaf nodes
    n = 40
    chain = {"shape": [2] * n, "style": "chain", "H": [[rng.randint(-5, 5) for _ in range(2)] for _ in range(n)],
             "J": {f"{i},{j}": [[rng.randint(-5, 5) if j == i + 1 else 0 for _ in range(2)] for _ in range(2)]
                   for i, j in pairs_of(n)}}
    best = [0, 0]                                         # minimum over x_0..x_{i-1} given x_i, by dynamic programming
    for i in range(n):
        best = [chain["H"][i][b] + (min(best[a] + chain["J"][f"{i - 1},{i}"][a][b] for a in range(2)) if i else 0)
                for b in range(2)]
    low = min(best)
    shape_tree = None
    for site in reversed(range(n)):
        shape_tree = (site, [None, shape_tree] if rng.random() < 0.5 else [shape_tree, None])
    deep = assemble(rng, chain, shape_tree, "dp")
    out = run_engines(deep)
    assert out["accepted"] and deep["L"] == low and out["counts"]["depth"] == n and out["counts"]["leaf_boxes"] == n + 1
    assert assemble(rng, chain, None, "dp")["L"] == low
    deep["L"] += 1
    assert run_engines(deep)["failure"]["inequality"] == "total"


def test_children_must_be_exactly_the_states_of_the_site():
    obj = tiny()
    assert run_engines(obj)["accepted"]
    for a in "012":
        short = clone(obj)
        del short["tree"]["children"][a]
        assert run_engines(short)["kind"] == "format"
        assert "missing" in check(short, "c").reason
    for key in ("3", "4", "-1", "00", "0 ", "a", ""):
        more = clone(obj)
        more["tree"]["children"][key] = {"leaf": 0}
        assert run_engines(more)["kind"] == "format"
        assert "unexpected" in check(more, "python").reason


# ------------------------------------------------------------------------------------------------ 64-bit limit
B63 = 2 ** 63


def two_points(H0, H1, J, p, q, U0, U1, P2, L):
    """Two sites with one state each: brackets ``H0 + p``, ``H1 + q``, ``J - p - q``; total ``U0 + U1 + P2``."""
    return {"H": [[H0], [H1]], "J": {"0,1": [[J]]}, "L": L, "tree": {"leaf": 0},
            "leaves": [{"U": [U0, U1], "P2": {"0,1": P2}, "m": {"0,1": [p], "1,0": [q]}}]}


def wrapped(x):
    return (x + B63) % (2 * B63) - B63


def wrapping_verdict(obj):
    """What a checker computing every sum modulo 2^64 would say (accept or not)."""
    for row in slack_table(obj):
        t = row["leaf"]
        leaf = obj["leaves"][t]
        n = len(obj["H"])
        for (i, a) in row["site"]:
            s = obj["H"][i][a]
            for j in range(n):
                if j != i:
                    s = wrapped(s + leaf["m"][f"{i},{j}"][a])
            if not leaf["U"][i] <= s:
                return False
        for (i, j, a, b) in row["pair"]:
            s = wrapped(wrapped(obj["J"][f"{i},{j}"][a][b] - leaf["m"][f"{i},{j}"][a]) - leaf["m"][f"{j},{i}"][b])
            if not leaf["P2"][f"{i},{j}"] <= s:
                return False
        s = 0
        for v in list(leaf["U"]) + list(leaf["P2"].values()):
            s = wrapped(s + v)
        if not obj["L"] <= s:
            return False
    return True


def run_near_limit(obj):
    """Python engine (exact), C engine with 128-bit sums (must agree exactly), C engine with 64-bit sums
    (must agree or report an overflow; never a wrapped result)."""
    rp = pycheck.verify(obj)
    assert located(rp) == predicted(obj)
    data = loader.encode(loader.validate(obj))
    rc = ckernel.check_encoded(data)
    assert strip(rc) == strip(rp), (rc, rp)
    r64 = ckernel.check_encoded(data, ckernel.load_library(acc64=True))
    assert r64["kind"] == "overflow" or strip(r64) == strip(rp), (r64, rp)
    return rp, r64


def test_sums_beyond_64_bits_are_exact_not_wrapped():
    M = B63 - 1
    cases = [
        # (object, accepted?, would a checker computing modulo 2^64 accept?)
        (two_points(-B63, 0, 0, -B63, M, 0, 0, 0, 0), False, True),     # (S) 0 <= -2^64 is false; modulo 2^64 it reads 0 <= 0
        (two_points(M, 0, 0, M, -M, M, -M, 0, 0), True, False),         # (S) 2^63-1 <= 2^64-2 is true; modulo 2^64: <= -2
        (two_points(M, M, 0, -B63, -B63, -1, -1, 5, 3), True, False),   # (P) 5 <= 2^64 is true; modulo 2^64: 5 <= 0
        (two_points(0, 0, -2, M, M, 0, 0, 0, 0), False, True),          # (P) 0 <= -2^64 is false; modulo 2^64: 0 <= 0
        (two_points(M, M, 2, 0, 0, M, M, 2, M), True, False),           # (T) 2^63-1 <= 2^64 is true; modulo 2^64: <= 0
        (two_points(0, 0, 0, 0, 0, -B63, -B63, 0, 0), False, True),     # (T) 0 <= -2^64 is false; modulo 2^64: 0 <= 0
        (two_points(-B63, M, 1, 0, 0, -B63, M, 1, 0), True, True),      # the most negative 64-bit value is read as itself
        (two_points(M, M, M, 0, 0, M, M, M, M), True, False),           # everything at the top of the range
    ]
    overflow64 = 0
    for obj, accepted, wrap_accepts in cases:
        rp, r64 = run_near_limit(obj)
        assert rp["accepted"] is accepted, obj
        assert wrapping_verdict(obj) is wrap_accepts, obj               # the case separates exact sums from wrapped ones
        if accepted:
            assert obj["L"] <= brute_min(obj)                           # and what is accepted is true
        overflow64 += r64["kind"] == "overflow"
    assert overflow64 >= 6
    # two false claims that arithmetic modulo 2^64 would accept: the energy is below the claimed bound
    for bad in (cases[0][0], cases[3][0], two_points(-B63, -B63, 0, 0, 0, -B63, -B63, 0, 0)):
        assert brute_min(bad) < bad["L"] and wrapping_verdict(bad) and not run_near_limit(bad)[0]["accepted"]


def test_integers_outside_64_bits_c_declines_python_decides():
    for value in (B63, -B63 - 1, 2 ** 64, -2 ** 64, 10 ** 30, -10 ** 30, 2 ** 127, 2 ** 200):
        for where in ("H", "J", "L", "U", "P2", "m"):
            obj = two_points(0, 0, 0, 0, 0, 0, 0, 0, 0)
            if where == "H":
                obj["H"][0][0] = value
            elif where == "J":
                obj["J"]["0,1"][0][0] = value
            elif where == "L":
                obj["L"] = value
            elif where == "U":
                obj["leaves"][0]["U"][1] = value
            elif where == "P2":
                obj["leaves"][0]["P2"]["0,1"] = value
            else:
                obj["leaves"][0]["m"]["1,0"][0] = value
            rc, rp = check(obj, "c"), check(obj, "python")
            assert rc.kind == "range" and not rc.accepted and rc.failure is None, (where, value, rc)
            assert rp.kind in (None, "inequality")                        # Python integers: a real verdict
            assert located(front(rp)) == predicted(obj)
            if rp.accepted:
                assert obj["L"] <= brute_min(obj)
            r64 = ckernel.check_encoded(loader.encode(loader.validate(obj)), ckernel.load_library(acc64=True))
            assert r64["kind"] == "range"
    # a valid certificate with numbers of 200 bits, for the Python engine
    big = two_points(3 * 2 ** 200, -2 ** 200, 2 ** 199, 2 ** 198, -2 ** 198, 3 * 2 ** 200 + 2 ** 198, -2 ** 200 - 2 ** 198,
                     2 ** 199, 2 ** 201 + 2 ** 199)
    assert check(big, "python").accepted and brute_min(big) == big["L"] and check(big, "c").kind == "range"
    big["L"] += 1
    assert check(big, "python").failure["inequality"] == "total"


def test_random_instances_at_the_64_bit_limit():
    """Tables and messages drawn at the edges of the 64-bit range.  U and P2 are the exact minima of the
    brackets (Python integers) clipped to 64 bits, so a certificate is valid unless a minimum had to be
    clipped upwards or the bound is too high.  128-bit sums must reproduce the exact verdict; 64-bit sums
    must reproduce it or report an overflow; a checker working modulo 2^64 would get many of them wrong."""
    rng = random.Random(SEED + 64)
    pool = [0, 0, 1, -1, B63 - 1, -B63, B63 - 2, -B63 + 1, 2 ** 62, -2 ** 62, 2 ** 62 + 1, -2 ** 62 - 1, 3 * 2 ** 61, -3 * 2 ** 61]
    clip = lambda v: max(-B63, min(B63 - 1, v))                           # noqa: E731
    stats = Counter()
    for _ in range(1500 * SCALE):
        n = rng.randint(1, 3)
        shape = [rng.randint(1, 2) for _ in range(n)]
        draw = lambda: rng.choice(pool) if rng.random() < 0.8 else rng.randint(-B63, B63 - 1)     # noqa: E731
        inst = {"H": [[draw() for _ in range(k)] for k in shape],
                "J": {f"{i},{j}": [[draw() for _ in range(shape[j])] for _ in range(shape[i])] for i, j in pairs_of(n)}}
        m = zero_messages(inst)
        for vec in m.values():
            for a in range(len(vec)):
                vec[a] = draw() if rng.random() < 0.6 else 0
        leaf = leaf_from_messages(inst, [list(range(k)) for k in shape], m)
        leaf["U"] = [clip(v) for v in leaf["U"]]
        leaf["P2"] = {key: clip(v) for key, v in leaf["P2"].items()}
        if rng.random() < 0.2:                                            # disturb one number of the leaf
            at = rng.randrange(n)
            leaf["U"][at] = clip(leaf["U"][at] + rng.choice((1, -1)))
        total = sum(leaf["U"]) + sum(leaf["P2"].values())
        obj = {"H": inst["H"], "J": inst["J"], "L": clip(total - rng.choice((0, 0, 0, 1, -1, 7, B63, -B63))),
               "tree": {"leaf": 0}, "leaves": [leaf]}
        rp, r64 = run_near_limit(obj)
        wrap = wrapping_verdict(obj)
        stats["accepted" if rp["accepted"] else "rejected"] += 1
        stats["64-bit sums: overflow reported"] += r64["kind"] == "overflow"
        stats["64-bit sums: same result"] += r64["kind"] != "overflow"
        stats["modulo 2^64 would reject a valid certificate"] += rp["accepted"] and not wrap
        stats["modulo 2^64 would accept an invalid certificate"] += wrap and not rp["accepted"]
        if rp["accepted"]:
            assert obj["L"] <= brute_min(obj)
        elif wrap:
            stats["modulo 2^64 would accept a false bound"] += obj["L"] > brute_min(obj)
    emit("random instances at the 64-bit limit", dict(stats))
    assert stats["accepted"] > 300 * SCALE and stats["rejected"] > 300 * SCALE
    assert stats["64-bit sums: overflow reported"] > 300 * SCALE and stats["64-bit sums: same result"] > 100 * SCALE
    assert stats["modulo 2^64 would reject a valid certificate"] > 50 * SCALE
    assert stats["modulo 2^64 would accept a false bound"] > 20 * SCALE


def test_64_bit_accumulator_build_agrees_where_nothing_overflows(vectors):
    lib64 = ckernel.load_library(acc64=True)
    for v in vectors.values():
        data = loader.encode(loader.validate(v["obj"]))
        assert ckernel.check_encoded(data, lib64) == ckernel.check_encoded(data)
        control = rv.build_controls(v["obj"])["children_exchanged"]
        data = loader.encode(loader.validate(control))
        assert ckernel.check_encoded(data, lib64) == ckernel.check_encoded(data)


# ================================================================================================ 4. soundness fuzz
def leaf_total(leaf):
    return sum(leaf["U"]) + sum(leaf["P2"].values())


def argmin_state(obj):
    """One minimiser of the instance (the first in lexicographic order)."""
    H, J = obj["H"], obj["J"]
    n = len(H)
    energy = lambda x: (sum(H[i][x[i]] for i in range(n))                # noqa: E731
                        + sum(J[f"{i},{j}"][x[i]][x[j]] for i in range(n) for j in range(i + 1, n)))
    return min(itertools.product(*[range(len(row)) for row in H]), key=energy)


def prune_leaves(obj):
    """Drop the leaf certificates that the tree no longer names and renumber the others."""
    order = []
    stack = [obj["tree"]]
    while stack:
        node = stack.pop()
        if "leaf" in node:
            if node["leaf"] not in order:
                order.append(node["leaf"])
        else:
            stack.extend(node["children"][a] for a in sorted(node["children"], key=int, reverse=True))
    index = {old: new for new, old in enumerate(order)}
    stack = [obj["tree"]]
    while stack:
        node = stack.pop()
        if "leaf" in node:
            node["leaf"] = index[node["leaf"]]
        else:
            stack.extend(node["children"].values())
    obj["leaves"] = [obj["leaves"][old] for old in order]


def branch_nodes(obj):
    out, stack = [], [obj["tree"]]
    while stack:
        node = stack.pop()
        if "children" in node:
            out.append(node)
            stack.extend(node["children"].values())
    return out


def count_leaf_nodes(tree_shape):
    return 1 if tree_shape is None else sum(count_leaf_nodes(kid) for kid in tree_shape[1])


def small_tree_shape(rng, shape, depth_cap, p_stop, most=16):
    """A random tree with at most ``most`` leaf nodes (the depth is reduced until it fits)."""
    while True:
        tree = random_tree_shape(rng, shape, depth_cap, p_stop)
        if count_leaf_nodes(tree) <= most:
            return tree
        depth_cap -= 1


def valid_certificates(rng, inst, everything=False):
    """Certificates that are valid by construction, as ``(label, object)``."""
    shape = inst["shape"]
    n = len(shape)
    out = []
    if everything or rng.random() < 0.6:
        out.append(("dp, all but two sites branched",
                    assemble(rng, inst, small_tree_shape(rng, shape, max(0, n - 2), 0.0), "dp")))
    if everything or not out or rng.random() < 0.4:
        producer = rng.choice(("dp",) * 10 + ("zero",) * 4 + ("random",) * 5 + ("lp",))
        depth = rng.randint(0, 1) if producer == "lp" else rng.randint(0, 3)
        out.append((f"{producer}, random tree",
                    assemble(rng, inst, small_tree_shape(rng, shape, depth, 0.35), producer, 0.5)))
    if inst["style"] in ("chain", "tree", "termwise") and (everything or rng.random() < 0.4):
        out.append(("dp, no branching", assemble(rng, inst, None, "dp")))
    if inst["style"] == "termwise" and (everything or rng.random() < 0.5):
        out.append(("zero messages", assemble(rng, inst, small_tree_shape(rng, shape, rng.randint(0, 2), 0.4), "zero", 0.5)))
    return out


def adversaries(rng, inst, base, low, everything=False, sample=5):
    """Variants of a valid certificate ``base`` (``low`` is the true minimum), as ``(label, object, must)``
    with ``must`` True where the variant is valid by construction.  The variants built from a tight
    certificate (bound = minimum) are false claims aimed at one term of one inequality: a checker that
    drops or misreads that term would accept them.  ``everything``: all variants (and, for the instances
    whose tables have their minima at one common state, one per site, pair and message vector); otherwise
    the two valid transformations and ``sample`` of the others."""
    n = len(base["H"])
    pairs = pairs_of(n)
    ordered = [(i, j) for i in range(n) for j in range(n) if i != j]
    always, plans = [], []
    # ---- valid transformations
    g = clone(base)
    for _ in range(rng.randint(1, 4)):
        if n > 1:
            i, j = rng.sample(range(n), 2)
            gauge(g, rng.randrange(len(g["leaves"])), i, j, rng.randint(-4, 4))
    always.append(("valid: gauge shifts", lambda: g, True))

    def lowered():
        c = clone(base)
        c["L"] -= rng.randint(1, 3)
        return c

    def raised():
        c = clone(base)
        c["L"] += 1
        return c

    always.append(("valid: bound lowered", lowered, True))
    plans.append(("bound + 1", raised, False))
    tight = base["L"] == low
    systematic = everything and inst["style"] == "termwise" and len(base["leaves"]) <= 4

    def cheats(start, tag):
        binding = [t for t, leaf in enumerate(start["leaves"]) if leaf_total(leaf) == start["L"]]

        def make(label, change):
            def build():
                c = clone(start)
                c["L"] += 1
                for t in binding:
                    change(c["leaves"][t])
                return c
            plans.append((f"false claim{tag}: {label}", build, False))

        def raise_U(i):
            return lambda leaf: leaf["U"].__setitem__(i, leaf["U"][i] + 1)

        def raise_P(key):
            return lambda leaf: leaf["P2"].__setitem__(key, leaf["P2"][key] + 1)

        def message_site(p, q):                          # m_pq - 1 everywhere, P2 + 1: only (S) of site p suffers
            def change(leaf):
                leaf["m"][f"{p},{q}"] = [v - 1 for v in leaf["m"][f"{p},{q}"]]
                leaf["P2"][f"{min(p, q)},{max(p, q)}"] += 1
            return change

        def message_pair(p, q):                          # m_pq + 1 everywhere, U_p + 1: only (P) of the pair suffers
            def change(leaf):
                leaf["m"][f"{p},{q}"] = [v + 1 for v in leaf["m"][f"{p},{q}"]]
                leaf["U"][p] += 1
            return change

        for i in (range(n) if systematic else rng.sample(range(n), 1)):
            make("U_i + 1", raise_U(i))
        for i, j in (pairs if systematic else rng.sample(pairs, min(len(pairs), 1))):
            make("P2_ij + 1", raise_P(f"{i},{j}"))
        for p, q in (ordered if systematic else rng.sample(ordered, min(len(ordered), 1))):
            make("m_pq - 1, P2 + 1", message_site(p, q))
            make("m_pq + 1, U_p + 1", message_pair(p, q))

    if tight:
        cheats(base, "")
        if n > 1 and g["L"] == low:
            cheats(g, ", after gauge shifts")
        if n > 1:
            # the total without one of its terms, after a gauge shift that makes this term negative in every leaf
            i, j = rng.sample(range(n), 2)
            key = f"{min(i, j)},{max(i, j)}"

            def without_U():
                c = clone(base)
                shift = max(leaf["U"][i] for leaf in c["leaves"]) + rng.randint(1, 3)
                for t in range(len(c["leaves"])):
                    gauge(c, t, i, j, -shift)             # U_i < 0 everywhere
                c["L"] = min(leaf_total(leaf) - leaf["U"][i] for leaf in c["leaves"])
                return c

            def without_P():
                c = clone(base)
                shift = max(leaf["P2"][key] for leaf in c["leaves"]) + rng.randint(1, 3)
                for t in range(len(c["leaves"])):
                    gauge(c, t, i, j, shift)              # P2_ij < 0 everywhere
                c["L"] = min(leaf_total(leaf) - leaf["P2"][key] for leaf in c["leaves"])
                return c

            def only_U():
                c = clone(base)
                c["L"] = min(sum(leaf["U"]) for leaf in c["leaves"])
                return c

            plans.append(("false claim: the total without U_i", without_U, False))
            plans.append(("false claim: the total without P2_ij", without_P, False))
            plans.append(("claim: the sum of U alone", only_U, None))
        star = argmin_state(base)

        def lower_H():
            c = clone(base)
            site = rng.randrange(n)
            c["H"][site][star[site]] -= 1
            return c

        def lower_J():
            c = clone(base)
            a, b = rng.choice(pairs)
            c["J"][f"{a},{b}"][star[a]][star[b]] -= 1
            return c

        plans.append(("false claim: H lowered at a minimiser", lower_H, False))
        if pairs:
            plans.append(("false claim: J lowered at a minimiser", lower_J, False))
    # ---- the tree
    if branch_nodes(base):
        def exchange():
            c = clone(base)
            node = rng.choice(branch_nodes(c))
            a, b = rng.sample(sorted(node["children"]), 2) if len(node["children"]) > 1 else ("0", "0")
            node["children"][a], node["children"][b] = node["children"][b], node["children"][a]
            return c

        def one_for_all():
            c = clone(base)
            node = rng.choice(branch_nodes(c))
            a = rng.choice(sorted(node["children"]))
            for b in node["children"]:
                node["children"][b] = clone(node["children"][a])
            prune_leaves(c)
            c["L"] = min(leaf_total(leaf) for leaf in c["leaves"])
            return c

        def hoist():
            c = clone(base)
            path, node = [], c["tree"]
            while "children" in node and (not path or rng.random() < 0.6):
                path.append(rng.choice(sorted(node["children"])))
                node = node["children"][path[-1]]
            if len(path) >= 2:
                parent = c["tree"]
                for step in path[:-2]:
                    parent = parent["children"][step]
                parent["children"][path[-2]] = node
            else:
                c["tree"] = node
            prune_leaves(c)
            c["L"] = min(leaf_total(leaf) for leaf in c["leaves"])
            return c

        def reorder():
            c = clone(base)
            x, y = rng.sample(range(len(c["leaves"])), 2)
            c["leaves"][x], c["leaves"][y] = c["leaves"][y], c["leaves"][x]
            return c

        plans.append(("tree: two children exchanged", exchange, None))
        plans.append(("tree: one child's subtree for every state", one_for_all, None))
        plans.append(("tree: a subtree in the place of its parent", hoist, None))
        if len(base["leaves"]) > 1:
            plans.append(("tree: two leaf certificates exchanged in the list", reorder, None))
    # ---- another reading of the tables
    if tight and len(set(inst["shape"])) == 1 and pairs:
        def transposed():
            mirror = {"shape": inst["shape"], "style": inst["style"], "H": inst["H"],
                      "J": {key: [list(col) for col in zip(*table)] for key, table in inst["J"].items()}}
            c = assemble(rng, mirror, small_tree_shape(rng, inst["shape"], max(0, n - 2), 0.0), "dp")
            c["J"] = inst["J"]
            return c

        def exchanged_messages():
            c = clone(base)
            for leaf in c["leaves"]:
                for a, b in pairs:
                    leaf["m"][f"{a},{b}"], leaf["m"][f"{b},{a}"] = leaf["m"][f"{b},{a}"], leaf["m"][f"{a},{b}"]
            return c

        def opposite_sign():
            c = clone(base)
            for leaf in c["leaves"]:
                leaf["m"] = {key: [-v for v in vec] for key, vec in leaf["m"].items()}
            return c

        plans.append(("other reading: certificate of the instance with J transposed", transposed, None))
        plans.append(("other reading: m_ij and m_ji exchanged", exchanged_messages, None))
        plans.append(("other reading: messages with the opposite sign", opposite_sign, None))

    # ---- one number of the certificate changed by a little
    def noise():
        c = clone(base)
        leaf = rng.choice(c["leaves"])
        part = rng.choice(("U", "P2", "m")) if pairs else "U"
        delta = rng.choice((-2, -1, 1, 2))
        if part == "U":
            leaf["U"][rng.randrange(n)] += delta
        elif part == "P2":
            leaf["P2"][rng.choice(sorted(leaf["P2"]))] += delta
        else:
            vec = leaf["m"][rng.choice(sorted(leaf["m"]))]
            vec[rng.randrange(len(vec))] += delta
        return c

    plans.append(("noise: one number of a leaf certificate", noise, None))
    plans.append(("noise: one number of a leaf certificate", noise, None))
    chosen = plans if everything else rng.sample(plans, min(sample, len(plans)))
    return [(label, build(), must) for label, build, must in always + chosen]


def fuzz_cases(seed, instances, everything=False):
    """The fuzz corpus as a generator of ``(label, object, must be accepted?, true minimum)``."""
    rng = random.Random(seed)
    for _ in range(instances):
        inst = random_instance(rng)
        low = brute_min(inst)
        for label, base in valid_certificates(rng, inst, everything):
            yield f"valid: {label}", base, True, low
            for label2, obj, must in adversaries(rng, inst, base, low, everything):
                changed = obj["H"] != inst["H"] or obj["J"] != inst["J"]
                yield label2, obj, must, (brute_min(obj) if changed else low)


def test_soundness_fuzz():
    """Whenever an engine accepts a bound, enumeration confirms it; the engines agree on every input; the
    third evaluator predicts the same first failing inequality; what is valid by construction is accepted."""
    stats, by_label, single = Counter(), {}, Counter()
    instances = 2000 * SCALE
    for label, obj, must, low in fuzz_cases(SEED, instances):
        out = run_engines(obj)                            # asserts C == Python
        assert out["kind"] in (None, "inequality"), (label, out["reason"])
        table = slack_table(obj)                          # third evaluator
        bad = [(visit, kind, *key) for visit, row in enumerate(table)
               for kind, slacks in (("site", row["site"]), ("pair", row["pair"]), ("total", {(): row["total"]}))
               for key, slack in slacks.items() if slack < 0]
        if out["accepted"]:
            assert not bad, label
        else:
            f = out["failure"]
            first = (f["visit"], f["inequality"]) + tuple(v for v in ((f["i"], f["a"]) if f["inequality"] == "site" else
                                                                       (f["i"], f["j"], f["a"], f["b"]) if f["inequality"] == "pair" else ()))
            assert bad and bad[0] == first, (label, bad[:2], first)
        false_claim = obj["L"] > low
        row = by_label.setdefault(label, Counter())
        row["cases"] += 1
        row["accepted"] += out["accepted"]
        row["false claims"] += false_claim
        stats["certificates"] += 1
        if out["accepted"]:
            assert obj["L"] <= low, f"UNSOUND: {label}: bound {obj['L']} accepted, the minimum is {low}"
            stats["accepted"] += 1
            stats["accepted, bound = minimum"] += obj["L"] == low
        else:
            stats["rejected"] += 1
            stats["rejected: " + out["failure"]["inequality"]] += 1
        if must:
            assert out["accepted"], (label, out["reason"])
            stats["valid by construction (all accepted)"] += 1
        if false_claim:
            stats["false claims (all rejected)"] += 1
            if len(bad) == 1:
                stats["false claims with exactly one violated inequality"] += 1
                single[bad[0][1]] += 1
    stats["instances"] = instances
    emit("soundness fuzz", dict(stats))
    emit("soundness fuzz, false claims with one violated inequality, by kind", dict(single))
    emit("soundness fuzz, by family (cases / accepted / false claims)",
         {label: [row["cases"], row["accepted"], row["false claims"]] for label, row in sorted(by_label.items())})
    assert stats["certificates"] > 15000 * SCALE
    assert stats["accepted"] > 0.3 * stats["certificates"] and stats["rejected"] > 0.3 * stats["certificates"]
    assert stats["accepted, bound = minimum"] > 2000 * SCALE
    assert stats["false claims (all rejected)"] > 3000 * SCALE
    assert min(single["site"], single["pair"], single["total"]) > 200 * SCALE


# ================================================================================================ 5. mutation of accepted certificates
def encode_with_roles(obj):
    """Second encoder (tests only), written from the grammar in the header of ``leafcert.c``: the tokens,
    and for every integer of the certificate the index of its token.  The tables must be well formed; the
    tree and the list of leaves are transcribed as they are, also when they are not (missing or extra
    children, indices out of range), children in increasing order of the state."""
    H = obj["H"]
    n = len(H)
    toks = ["leafcert", "1", "sites", str(n), "shape", *[str(len(row)) for row in H], "bound"]
    where = {("L",): len(toks)}
    toks.append(str(obj["L"]))
    for i, row in enumerate(H):
        toks += ["h", str(i)]
        for a, v in enumerate(row):
            where["H", i, a] = len(toks)
            toks.append(str(v))
    for i, j in pairs_of(n):
        toks += ["j", str(i), str(j)]
        for a, row in enumerate(obj["J"][f"{i},{j}"]):
            for b, v in enumerate(row):
                where["J", i, j, a, b] = len(toks)
                toks.append(str(v))
    toks += ["leaves", str(len(obj["leaves"]))]
    for t, leaf in enumerate(obj["leaves"]):
        toks += ["leaf", str(t), "u"]
        for i, v in enumerate(leaf["U"]):
            where["U", t, i] = len(toks)
            toks.append(str(v))
        toks.append("p")
        for i, j in pairs_of(n):
            where["P2", t, i, j] = len(toks)
            toks.append(str(leaf["P2"][f"{i},{j}"]))
        for i in range(n):
            for j in range(n):
                if i != j:
                    toks += ["m", str(i), str(j)]
                    for a, v in enumerate(leaf["m"][f"{i},{j}"]):
                        where["m", t, i, j, a] = len(toks)
                        toks.append(str(v))
    toks.append("tree")
    stack = [obj["tree"]]
    while stack:
        node = stack.pop()
        if isinstance(node, str):
            toks.append(node)
        elif "leaf" in node:
            toks += ["L", str(node["leaf"])]
        else:
            kids = sorted(node["children"], key=int)
            toks += ["B", str(node["site"]), str(len(kids))]
            for key in reversed(kids):
                stack.append(node["children"][key])
                stack.append(str(int(key)))
    toks.append("end")
    return toks, where


def slot(obj, role):
    """The container and the key that hold the integer with this role."""
    kind = role[0]
    if kind == "L":
        return obj, "L"
    if kind == "H":
        return obj["H"][role[1]], role[2]
    if kind == "J":
        return obj["J"][f"{role[1]},{role[2]}"][role[3]], role[4]
    if kind == "U":
        return obj["leaves"][role[1]]["U"], role[2]
    if kind == "P2":
        return obj["leaves"][role[1]]["P2"], f"{role[2]},{role[3]}"
    return obj["leaves"][role[1]]["m"][f"{role[2]},{role[3]}"], role[4]


def slack_intervals(obj):
    """For every integer of an accepted certificate, the interval ``[lo, hi]`` (``None`` = unbounded) of the
    amounts ``d`` that can be added to it with every inequality still holding -- computed from the slacks of
    :func:`slack_table`, without either engine.  A single-integer mutant is valid iff ``lo <= d <= hi``."""
    n = len(obj["H"])
    bounds = {}

    def at_least(role, x):                               # d >= x
        cur = bounds.setdefault(role, [None, None])
        cur[0] = x if cur[0] is None else max(cur[0], x)

    def at_most(role, x):                                # d <= x
        cur = bounds.setdefault(role, [None, None])
        cur[1] = x if cur[1] is None else min(cur[1], x)

    for row in slack_table(obj):
        t = row["leaf"]
        for (i, a), s in row["site"].items():            # U_i <= H_i(a) + sum_j m_ij(a)
            at_least(("H", i, a), -s)
            at_most(("U", t, i), s)
            for j in range(n):
                if j != i:
                    at_least(("m", t, i, j, a), -s)
        for (i, j, a, b), s in row["pair"].items():      # P2_ij <= J_ij(a,b) - m_ij(a) - m_ji(b)
            at_least(("J", i, j, a, b), -s)
            at_most(("P2", t, i, j), s)
            at_most(("m", t, i, j, a), s)
            at_most(("m", t, j, i, b), s)
        for i in range(n):                               # L <= sum U + sum P2
            at_least(("U", t, i), -row["total"])
        for i, j in pairs_of(n):
            at_least(("P2", t, i, j), -row["total"])
        at_most(("L",), row["total"])
    return bounds


def mutant_class(role, d, lo, hi):
    kind = role[0]
    if kind in ("H", "J"):
        return ("instance entry raised: every inequality that uses it gains" if d > 0
                else "instance entry lowered within the slack of every inequality that uses it")
    if kind == "L":
        return "bound lowered: a weaker claim" if d < 0 else "bound raised within the slack of every leaf's total"
    if kind in ("U", "P2"):
        return (f"{kind} lowered within the slack of the total" if d < 0
                else f"{kind} raised within the slack of the inequalities it bounds")
    if lo is None and hi is None:
        return "message entry of a state outside every box of its leaf: used by no inequality"
    return "message entry changed within the slack of its site and pair inequalities"


def mutate_every_integer(obj, big, sound, stats, python_every=1):
    """Every integer of the accepted certificate ``obj`` changed by +1, -1, +big, -big and by the four
    amounts at the edges of its slack interval.  The C engine checks every mutant, the Python engine every
    ``python_every``-th; both must give the verdict predicted from the slacks.  ``sound(role, d)`` must say
    by enumeration whether the bound of the mutant is true; it is asked for every accepted mutant."""
    toks, where = encode_with_roles(obj)
    assert " ".join(toks).encode() == b" ".join(loader.encode(loader.validate(obj)).split())    # the two encoders agree
    intervals = slack_intervals(obj)
    count = 0
    for role, index in where.items():
        lo, hi = intervals.get(role, (None, None))
        box, key = slot(obj, role)
        value = box[key]
        assert toks[index] == str(value)
        deltas = {1, -1, big, -big}
        if hi is not None:
            deltas |= {hi, hi + 1}
        if lo is not None:
            deltas |= {lo, lo - 1}
        deltas.discard(0)
        for d in sorted(deltas):
            expect = (lo is None or d >= lo) and (hi is None or d <= hi)
            toks[index] = str(value + d)
            rc = ckernel.check_encoded(" ".join(toks).encode())
            assert rc["kind"] in (None, "inequality") and rc["accepted"] == expect, (role, d, lo, hi, rc["reason"])
            count += 1
            if count % python_every == 0:
                box[key] = value + d
                rp = pycheck.verify(obj)
                box[key] = value
                assert strip(rp) == strip(rc), (role, d)
                stats["mutants also checked by the Python engine"] += 1
            stats["mutants"] += 1
            if expect:
                assert sound(role, d), f"UNSOUND: {role} changed by {d} is accepted"
                stats["accepted: " + mutant_class(role, d, lo, hi)] += 1
            else:
                stats[f"caught: {role[0]}"] += 1
                stats["caught"] += 1
        toks[index] = str(value)


def nodes_with_paths(tree):
    """Every node as ``(path of child keys, sites fixed above it, node)``."""
    out, stack = [], [((), (), tree)]
    while stack:
        path, fixed, node = stack.pop()
        out.append((path, fixed, node))
        if "children" in node:
            for key in sorted(node["children"], key=int, reverse=True):
                stack.append((path + (key,), fixed + (node["site"],), node["children"][key]))
    return out


def node_at(tree, path):
    for key in path:
        tree = tree["children"][key]
    return tree


def structural_mutants(obj):
    """Every single change of the structure of a certificate, as ``(label, mutant)``."""
    shape = [len(row) for row in obj["H"]]
    out = []

    def changed(path, new):
        c = clone(obj)
        if path:
            node_at(c["tree"], path[:-1])["children"][path[-1]] = new
        else:
            c["tree"] = new
        return c

    for path, fixed, node in nodes_with_paths(obj["tree"]):
        if "children" in node:
            keys = sorted(node["children"], key=int)
            for x, a in enumerate(keys):
                for b in keys[x + 1:]:
                    c = clone(obj)
                    kids = node_at(c["tree"], path)["children"]
                    kids[a], kids[b] = kids[b], kids[a]
                    out.append(("two children exchanged", c))
                c = clone(obj)
                del node_at(c["tree"], path)["children"][a]
                out.append(("a child deleted", c))
                for b in keys:
                    if b != a:
                        c = clone(obj)
                        kids = node_at(c["tree"], path)["children"]
                        kids[b] = clone(kids[a])
                        out.append(("a subtree duplicated over a sibling", c))
                out.append(("a branch replaced by one of its children", changed(path, clone(node["children"][a]))))
            c = clone(obj)
            node_at(c["tree"], path)["children"][str(len(keys))] = {"leaf": 0}
            out.append(("an extra child added", c))
            for site in range(len(shape)):
                if site != node["site"]:
                    c = clone(obj)
                    node_at(c["tree"], path)["site"] = site
                    out.append(("the site of a branch changed", c))
        else:
            for t in range(-1, len(obj["leaves"]) + 1):
                if t != node["leaf"]:
                    out.append(("a leaf index changed", changed(path, {"leaf": t})))
            for site in range(len(shape)):
                if site not in fixed:
                    out.append(("a branch inserted above a leaf node (all children name the same leaf)",
                                changed(path, {"site": site, "children": {str(a): {"leaf": node["leaf"]}
                                                                           for a in range(shape[site])}})))
    for t in range(len(obj["leaves"])):
        c = clone(obj)
        del c["leaves"][t]
        out.append(("a leaf certificate deleted from the list", c))
        c = clone(obj)
        c["leaves"].append(clone(c["leaves"][t]))
        out.append(("a leaf certificate duplicated in the list", c))
        for u in range(t + 1, len(obj["leaves"])):
            c = clone(obj)
            c["leaves"][t], c["leaves"][u] = c["leaves"][u], c["leaves"][t]
            out.append(("two leaf certificates exchanged in the list", c))
    return out


def expanded(obj):
    """The tree with every leaf index replaced by the content of the leaf certificate (two objects with the
    same expansion are the same certificate), as a JSON string."""
    def expand(node):
        if "leaf" in node:
            return obj["leaves"][node["leaf"]]
        return {"site": node["site"], "children": {key: expand(kid) for key, kid in node["children"].items()}}
    return json.dumps(expand(obj["tree"]), sort_keys=True)


def run_structural(base, mutant, low, label, stats):
    """One structural mutant through the loader, the Python engine and (on the tokens of the second
    encoder, so also when the tree is malformed) the C engine; soundness of what is accepted."""
    rp = run_engines(mutant)                              # loader/pycheck agree; C agrees when well formed
    toks, _ = encode_with_roles(mutant)
    rc = ckernel.check_encoded(" ".join(toks).encode())
    assert rc["kind"] == rp["kind"] and rc["accepted"] == rp["accepted"], (label, rc["reason"], rp["reason"])
    stats[label, "mutants"] += 1
    if rp["kind"] == "format":
        stats[label, "caught: not well formed"] += 1
    elif rp["kind"] == "inequality":
        assert located(rp) == predicted(mutant)
        stats[label, "caught: an inequality fails"] += 1
    else:
        assert predicted(mutant) is None and mutant["L"] <= low, f"UNSOUND: {label}"
        if expanded(mutant) == expanded(base):
            stats[label, "accepted: the same certificate (equal subtrees or equal leaf certificates)"] += 1
        elif "inserted" in label:
            stats[label, "accepted: a leaf certificate that holds on a box holds on each part of it"] += 1
        else:
            stats[label, "accepted: another valid certificate (every leaf holds on the box it now has)"] += 1
    return rp


def test_mutation_of_small_certificates():
    """Accepted certificates of small random instances: every integer and every piece of structure
    mutated.  The verdict on every integer mutant is predicted from the slacks, on every structural mutant
    by the third evaluator; every accepted mutant is confirmed by enumeration."""
    rng = random.Random(SEED + 5)
    ints, struct = Counter(), Counter()
    done = 0
    while done < 40 * SCALE:
        inst = random_instance(rng)
        if len(inst["shape"]) > 4 or max(inst["shape"]) > 3:
            continue
        low = brute_min(inst)
        producer = rng.choice(("dp", "dp", "dp", "zero", "random", "lp") if inst["style"] != "termwise" else ("zero", "dp"))
        base = assemble(rng, inst, small_tree_shape(rng, inst["shape"], rng.randint(0, 2), 0.3, most=6), producer, 0.5)
        if rng.random() < 0.5 and len(inst["shape"]) > 1:
            i, j = rng.sample(range(len(inst["shape"])), 2)
            gauge(base, rng.randrange(len(base["leaves"])), i, j, rng.randint(-3, 3))
        if rng.random() < 0.3:
            base["L"] -= rng.randint(1, 2)
        assert run_engines(base)["accepted"]
        done += 1
        ints["certificates"] += 1
        ints["certificates with bound = minimum"] += base["L"] == low

        def sound(role, d):
            if role[0] == "L":
                return base["L"] + d <= low
            if role[0] in ("H", "J"):                     # the instance changed: enumerate again
                box, key = slot(base, role)
                box[key] += d
                try:
                    return base["L"] <= brute_min(base)
                finally:
                    box[key] -= d
            return base["L"] <= low

        mutate_every_integer(base, 10 ** 6, sound, ints)
        for label, mutant in structural_mutants(base):
            run_structural(base, mutant, low, label, struct)
            try:
                pruned = clone(mutant)
                prune_leaves(pruned)
            except (KeyError, IndexError, TypeError):
                continue
            if pruned["leaves"] and all(0 <= t < len(pruned["leaves"]) for t in
                                        [n_["leaf"] for _, _, n_ in nodes_with_paths(pruned["tree"]) if "leaf" in n_]):
                if pruned != mutant:
                    run_structural(base, pruned, low, label + ", then unused leaf certificates removed", struct)
                claimed = clone(pruned)
                claimed["L"] = min(leaf_total(leaf) for leaf in claimed["leaves"])
                if claimed["L"] != pruned["L"]:
                    out = run_engines(claimed)
                    struct["re-claimed", "mutants"] += 1
                    struct["re-claimed", "false claims"] += claimed["L"] > low
                    if out["accepted"]:
                        assert claimed["L"] <= low, f"UNSOUND: {label}, bound re-claimed"
                        struct["re-claimed", "accepted (bound confirmed by enumeration)"] += 1
    emit("mutation, small certificates, integers", dict(ints))
    emit("mutation, small certificates, structure", {f"{a} | {b}": v for (a, b), v in sorted(struct.items())})
    assert ints["mutants"] > 10000 * SCALE and ints["caught"] > 0.4 * ints["mutants"]
    assert ints["mutants"] - ints["caught"] > 0.2 * ints["mutants"]
    assert ints["mutants also checked by the Python engine"] == ints["mutants"]
    assert sum(v for (label, what), v in struct.items() if what == "mutants") > 2000 * SCALE


# the seven files with distinct integers (the two Ser6 files at tau 0.70 repeat those at tau 0.60)
DISTINCT_VECTORS = [name for name in rv.FILES if "tau0.70" not in name]
MUTATED_VECTORS = ["p7_02_cert_L16_P2_tau0.60_ff99SB.json"] if SCALE == 1 else DISTINCT_VECTORS


@pytest.mark.parametrize("name", MUTATED_VECTORS)
def test_mutation_of_the_vectors(vectors, name):
    """Every integer of a real certificate (tables and leaf certificates) changed by +-1, by +-2^50 and to
    the edges of its slack; every piece of structure changed.  The verdict of the C engine on every mutant
    and of the Python engine on a sample must be the one predicted from the slacks; an accepted mutant of a
    table entry is confirmed by enumeration (the minimum over the states that use the entry)."""
    obj = clone(vectors[name]["obj"])
    E = tensor(obj)
    n = E.ndim
    low, L = int(E.min()), obj["L"]
    single = [E.min(axis=tuple(d for d in range(n) if d != i)) for i in range(n)]
    pair = {(i, j): E.min(axis=tuple(d for d in range(n) if d not in (i, j))) for i, j in pairs_of(n)}

    def sound(role, d):
        if role[0] == "L":
            return L + d <= low
        if role[0] == "H":                                # the new minimum is min(low, minimum over x_i = a, plus d)
            return L <= min(low, int(single[role[1]][role[2]]) + d)
        if role[0] == "J":
            return L <= min(low, int(pair[role[1], role[2]][role[3], role[4]]) + d)
        return L <= low

    ints, struct = Counter(), Counter()
    mutate_every_integer(obj, 2 ** 50, sound, ints, python_every=41)
    assert obj == vectors[name]["obj"]                    # everything was restored
    mutants = structural_mutants(obj)
    if len(mutants) > 150 and SCALE < 3:                  # a sample for the larger trees
        mutants = random.Random(SEED).sample(mutants, 150)
    for label, mutant in mutants:
        run_structural(obj, mutant, low, label, struct)
    emit(f"mutation, {name}, integers", dict(ints))
    emit(f"mutation, {name}, structure", {f"{a} | {b}": v for (a, b), v in sorted(struct.items())})
    assert ints["caught"] > 0.3 * ints["mutants"] and ints["mutants also checked by the Python engine"] > 100


def test_every_leaf_certificate_with_small_entries_exhaustively():
    """Small scope, no generator: for a few instances on two sites with two states each, EVERY leaf
    certificate whose seven numbers lie in {-1, 0, 1}, with three bounds, on the whole domain: the C engine
    on all of them and the Python engine on every seventh must return exactly the verdict and the first
    failing inequality of the definition (third evaluator); what is accepted is true by enumeration."""
    rng = random.Random(SEED + 8)
    stats = Counter()
    for round_ in range(3 + SCALE):
        inst = {"H": [[rng.randint(-1, 1) for _ in range(2)] for _ in range(2)],
                "J": {"0,1": [[rng.randint(-1, 1) for _ in range(2)] for _ in range(2)]}}
        low = brute_min(inst)
        obj = {**inst, "L": 0, "tree": {"leaf": 0},
               "leaves": [{"U": [0, 0], "P2": {"0,1": 0}, "m": {"0,1": [0, 0], "1,0": [0, 0]}}]}
        toks, where = encode_with_roles(obj)
        leaf = obj["leaves"][0]
        roles = [("U", 0, 0), ("U", 0, 1), ("P2", 0, 0, 1), ("m", 0, 0, 1, 0), ("m", 0, 0, 1, 1), ("m", 0, 1, 0, 0), ("m", 0, 1, 0, 1)]
        for values in itertools.product((-1, 0, 1), repeat=7):
            leaf["U"][0], leaf["U"][1], leaf["P2"]["0,1"] = values[:3]
            leaf["m"]["0,1"][0], leaf["m"]["0,1"][1], leaf["m"]["1,0"][0], leaf["m"]["1,0"][1] = values[3:]
            for role, v in zip(roles, values):
                toks[where[role]] = str(v)
            for L in (low - 1, low, low + 1):
                obj["L"] = L
                toks[where["L",]] = str(L)
                rc = ckernel.check_encoded(" ".join(toks).encode())
                want = predicted(obj)
                assert located(rc) == want and rc["accepted"] == (want is None)
                stats["certificates"] += 1
                stats["accepted"] += rc["accepted"]
                if rc["accepted"]:
                    assert L <= low
                    stats["accepted with the bound equal to the minimum"] += L == low
                if stats["certificates"] % 7 == 0:
                    assert strip(pycheck.verify(obj)) == strip(rc)
    emit("exhaustive small scope", dict(stats))
    assert stats["accepted"] > 100 and stats["accepted with the bound equal to the minimum"] > 0


def test_command_line(tmp_path, capsys):
    from metricchain_eng.leafcert.__main__ import main
    good, bad = tmp_path / "good.json", tmp_path / "bad.json"
    obj = tiny()
    good.write_text(json.dumps(obj))
    obj["L"] += 1
    bad.write_text(json.dumps(obj))
    assert main([str(good)]) == 0
    out = capsys.readouterr().out
    assert out.count("ACCEPT bound=-2") == 2 and "[c]" in out and "[python]" in out and "DISAGREE" not in out
    assert main(["--engine", "c", str(good), str(bad)]) == 1
    out = capsys.readouterr().out
    assert "REJECT (inequality)" in out and "L = -1 > -2" not in out and "L > sum U + sum P2" in out
    assert main(["--engine", "python", str(bad)]) == 1
    assert "L = -1 > -2 = sum U + sum P2" in capsys.readouterr().out
    assert main(["--encode", str(good)]) == 0
    text = capsys.readouterr().out
    assert text.encode() == loader.encode(loader.validate(tiny()))
    (tmp_path / "junk.json").write_text("{}")
    assert main(["--encode", str(tmp_path / "junk.json")]) == 1


# ================================================================================================ 6. the tests have teeth
# Deliberately broken copies of the two checkers (one change each, made in the source text) are run on a
# corpus built like the soundness fuzz.  A copy that is too lax must be caught the hard way: it accepts a
# bound that enumeration refutes ("unsound").  A copy that is too strict, or that reads another format, can
# only be caught by comparison with the reference result ("differs").
C_MUTANTS = [
    ("(S) the last state of a domain is skipped", "unsound",
     "for (size_t a = lo; a < hi; a++) {\n            sum = Hi[a];", "for (size_t a = lo; a + 1u < hi; a++) {\n            sum = Hi[a];"),
    ("(S) the first state of a domain is skipped", "unsound",
     "for (size_t a = lo; a < hi; a++) {\n            sum = Hi[a];", "for (size_t a = lo + 1u; a < hi; a++) {\n            sum = Hi[a];"),
    ("(S) one message vector is left out of the sum", "unsound",
     "for (size_t block = 0; block + 1u < n; block++) {", "for (size_t block = 0; block + 2u < n; block++) {"),
    ("(S) accepts U_i one unit above the sum", "unsound", "!((acc_t)U[i] <= sum))", "!((acc_t)U[i] <= sum + 1))"),
    ("(S) is not compared at all", "unsound", "if (c->overflow || !((acc_t)U[i] <= sum))", "if (c->overflow)"),
    ("(S) asks for a strict inequality", "differs", "!((acc_t)U[i] <= sum))", "!((acc_t)U[i] < sum))"),
    ("(P) the last state of the second site is skipped", "unsound",
     "for (size_t b = jlo; b < jhi; b++) {", "for (size_t b = jlo; b + 1u < jhi; b++) {"),
    ("(P) m_ji is not subtracted", "unsound", "                    ACC_SUB(c, sum, mji[b]);\n", ""),
    ("(P) m_ij is added instead of subtracted", "unsound", "ACC_SUB(c, sum, mij[a]);", "ACC_ADD(c, sum, mij[a]);"),
    ("(P) m_ji is taken from the vector of another site", "unsound",
     "+ i * kj;            /* i < j", "+ (j - 1u) * kj;            /* i < j"),
    ("(P) the table J_ij is read transposed", "unsound", "sum = Jij[a * kj + b];", "sum = Jij[b * ki + a];"),
    ("(P) accepts P2_ij one unit above the sum", "unsound", "!((acc_t)P[p] <= sum))", "!((acc_t)P[p] <= sum + 1))"),
    ("(P) compares with the P2 of the first pair", "unsound", "!((acc_t)P[p] <= sum))", "!((acc_t)P[0] <= sum))"),
    ("(T) compares the total with 0 instead of L", "unsound", "!((acc_t)c->L <= sum))", "!((acc_t)0 <= sum))"),
    ("(T) accepts L one unit above the total", "unsound", "!((acc_t)c->L <= sum))", "!((acc_t)c->L <= sum + 1))"),
    ("(T) P2 is left out of the total", "unsound",
     "{ ACC_ADD(c, sum, P[q]); c->res->additions++; }", "{ c->res->additions++; }"),
    ("(T) U_1 is left out of the total", "unsound",
     "for (size_t i = 1; i < n; i++) { ACC_ADD(c, sum, U[i]);", "for (size_t i = 2; i < n; i++) { ACC_ADD(c, sum, U[i]);"),
    ("(T) the last P2 is left out of the total", "unsound",
     "for (size_t q = 0; q < c->npairs; q++) { ACC_ADD", "for (size_t q = 0; q + 1u < c->npairs; q++) { ACC_ADD"),
    ("branch: every child is checked on the box of state 0", "unsound",
     "        c->fixed[site] = (int64_t)a;\n        c->path[2u * c->depth] = (int64_t)site;",
     "        c->fixed[site] = 0;\n        c->path[2u * c->depth] = (int64_t)site;"),
    ("branch: the box of a child is not restricted", "differs",
     "        c->fixed[site] = (int64_t)a;\n        c->path[2u * c->depth] = (int64_t)site;",
     "        c->path[2u * c->depth] = (int64_t)site;"),
    ("leaf node: always the first leaf certificate", "differs",
     "if (check_leaf(c, c->nval[node])) return 1;", "if (check_leaf(c, 0)) return 1;"),
    ("parser: the sign of negative numbers is dropped", "differs",
     "*out = (acc == (uint64_t)INT64_MAX + 1u) ? INT64_MIN : -(int64_t)acc;", "*out = (int64_t)(acc & (uint64_t)INT64_MAX);"),
    ("sums are computed modulo 2^64", "unsound",
     "typedef i128 acc_t;\n#define LC_ACC_BITS 128\n#endif", "typedef int64_t acc_t;\n#define LC_ACC_BITS 128\n#endif\n#define __builtin_add_overflow(x, y, r) (*(r) = (acc_t)((uint64_t)(x) + (uint64_t)(y)), 0)\n#define __builtin_sub_overflow(x, y, r) (*(r) = (acc_t)((uint64_t)(x) - (uint64_t)(y)), 0)"),
]

PY_MUTANTS = [
    ("(S) the last state of a domain is skipped", "unsound",
     "        for a in box[i]:\n            value = H[i][a]", "        for a in box[i][:-1]:\n            value = H[i][a]"),
    ("(S) one message vector is left out of the sum", "unsound",
     "others = [m[i, j] for j in range(n) if j != i]", "others = [m[i, j] for j in range(n) if j != i][:-1]"),
    ("(S) accepts U_i one unit above the sum", "unsound", "if not U[i] <= value:", "if not U[i] <= value + 1:"),
    ("(S) asks for a strict inequality", "differs", "if not U[i] <= value:", "if not U[i] < value:"),
    ("(P) the last state of the second site is skipped", "unsound",
     "            for b in box[j]:\n                value = row[b] - ma - mji[b]",
     "            for b in box[j][:-1]:\n                value = row[b] - ma - mji[b]"),
    ("(P) m_ji is not subtracted", "unsound", "value = row[b] - ma - mji[b]", "value = row[b] - ma"),
    ("(P) m_ij is added instead of subtracted", "unsound", "value = row[b] - ma - mji[b]", "value = row[b] + ma - mji[b]"),
    ("(P) the two message vectors are exchanged (m_ji(a), m_ij(b))", "differs",
     "table, mij, mji, bound = J[i, j], m[i, j], m[j, i], P2[i, j]",
     "table, bound = J[i, j], P2[i, j]\n        mij = m[j, i] if len(m[j, i]) == len(m[i, j]) else m[i, j]\n"
     "        mji = m[i, j] if len(m[j, i]) == len(m[i, j]) else m[j, i]"),
    ("(P) the table J_ij is read transposed where it is square", "unsound",
     "value = row[b] - ma - mji[b]", "value = (table[b][a] if len(table) == len(row) else row[b]) - ma - mji[b]"),
    ("(P) accepts P2_ij one unit above the sum", "unsound", "if not bound <= value:", "if not bound <= value + 1:"),
    ("(T) compares the total with 0 instead of L", "unsound", "if not L <= total:", "if not 0 <= total:"),
    ("(T) accepts L one unit above the total", "unsound", "if not L <= total:", "if not L <= total + 1:"),
    ("(T) P2 is left out of the total", "unsound", "    for pair in tab.pairs:\n        total += P2[pair]\n", ""),
    ("(T) U_1 is left out of the total", "unsound",
     "    for value in U:\n        total += value\n", "    for value in U[:1] + U[2:]:\n        total += value\n"),
    ("box: a fixed site is put at state 0", "unsound",
     "[[fixed[i]] if i in fixed else list(range(k[i])) for i in range(len(k))]",
     "[[0] if i in fixed else list(range(k[i])) for i in range(len(k))]"),
    ("box: fixed sites are not restricted", "differs",
     "[[fixed[i]] if i in fixed else list(range(k[i])) for i in range(len(k))]", "[list(range(k[i])) for i in range(len(k))]"),
    ("leaf node: always the first leaf certificate", "differs",
     "first_violation(tab, t, box, L)\n        add, cmp_", "first_violation(tab, 0, box, L)\n        add, cmp_"),
    ("the comparisons are reversed (U_i >= sum, ...)", "differs", "if not U[i] <= value:", "if not U[i] >= value:"),
]


@pytest.fixture(scope="module")
def kill_corpus():
    """Cases as in the soundness fuzz, with every adversary of every certificate (not a sample), plus the
    false claims at the 64-bit limit: ``(label, object, encoding, reference result, false claim?)``."""
    corpus = []
    for label, obj, must, low in fuzz_cases(SEED + 6, 90, everything=True):
        ref = strip(run_engines(obj))
        corpus.append((label, obj, loader.encode(loader.validate(obj)), ref, obj["L"] > low))
    for obj in (two_points(-B63, 0, 0, -B63, B63 - 1, 0, 0, 0, 0), two_points(0, 0, -2, B63 - 1, B63 - 1, 0, 0, 0, 0),
                two_points(-B63, -B63, 0, 0, 0, -B63, -B63, 0, 0)):
        ref = strip(run_engines(obj))
        assert not ref["accepted"] and obj["L"] > brute_min(obj)
        corpus.append(("false claim at the 64-bit limit", obj, loader.encode(loader.validate(obj)), ref, True))
    return corpus


def hunt(run, corpus, want):
    """Run a broken checker over the corpus.  Returns ``("unsound", label)`` for the first false claim it
    accepts; failing that (or if ``want`` is ``"differs"``), ``("differs", label)`` for the first result
    that is not the reference result; ``None`` if it survives."""
    differs = None
    for label, obj, data, ref, false_claim in corpus:
        try:
            out = strip(run(obj, data))
        except Exception:                                 # a crash of a broken Python copy is a difference
            out = None
        if out is not None and out["accepted"] and false_claim:
            return "unsound", label
        if differs is None and out != ref:
            differs = label
            if want == "differs":
                break
    return ("differs", differs) if differs is not None else None


def patched(source, old, new):
    assert source.count(old) == 1, f"the source no longer contains exactly once: {old!r}"
    return source.replace(old, new)


def test_broken_copies_of_the_c_checker_are_caught(kill_corpus, tmp_path):
    source = ckernel.SOURCE.read_text()
    jobs = []
    for index, (name, want, old, new) in enumerate(C_MUTANTS):
        src, lib = tmp_path / f"mutant{index}.c", tmp_path / f"mutant{index}.so"
        src.write_text(patched(source, old, new))
        jobs.append((name, want, lib, ["cc", "-std=c11", "-O0", "-w", "-shared", "-fPIC", "-o", str(lib), str(src)]))
    running = []
    for job in jobs:                                      # two compilations at a time
        running.append(subprocess.Popen(job[3]))
        if len(running) == 2:
            assert running.pop(0).wait() == 0
    assert all(proc.wait() == 0 for proc in running)
    report = {}
    for name, want, lib, _ in jobs:
        handle = ckernel.bind(lib)
        found = hunt(lambda obj, data: ckernel.check_encoded(data, handle), kill_corpus, want)
        assert found is not None, f"the corpus does not notice: {name}"
        assert found[0] == want or want == "differs", f"{name}: caught only by comparison ({found}), not by enumeration"
        report[name] = f"{found[0]}: {found[1]}"
    assert hunt(lambda obj, data: ckernel.check_encoded(data), kill_corpus, "unsound") is None    # the real one survives
    emit("broken copies of leafcert.c (how each was caught)", report)


def test_broken_copies_of_the_python_checker_are_caught(kill_corpus):
    source = Path(pycheck.__file__).read_text()
    no_self_check = patched(source, 'if (closed_add, closed_cmp) != (counts["additions"], counts["comparisons"]):', "if False:")
    report = {}
    for name, want, old, new in PY_MUTANTS:
        module = types.ModuleType("pycheck_mutant")
        exec(compile(patched(no_self_check, old, new), "pycheck_mutant.py", "exec"), module.__dict__)
        found = hunt(lambda obj, data: module.verify(obj), kill_corpus, want)
        assert found is not None, f"the corpus does not notice: {name}"
        assert found[0] == want or want == "differs", f"{name}: caught only by comparison ({found}), not by enumeration"
        report[name] = f"{found[0]}: {found[1]}"
    assert hunt(lambda obj, data: pycheck.verify(obj), kill_corpus, "unsound") is None
    emit("broken copies of pycheck.py (how each was caught)", report)
    # the consistency check inside pycheck (terms counted against the closed formula) catches skipped terms by itself
    module = types.ModuleType("pycheck_mutant")
    exec(compile(patched(source, PY_MUTANTS[0][2], PY_MUTANTS[0][3]), "pycheck_mutant.py", "exec"), module.__dict__)
    with pytest.raises(AssertionError):
        module.verify(tiny())


# ================================================================================================ 7. the C parser under corruption
class Undecodable(Exception):
    pass


def decode(data):
    """Decoder of the text read by ``leafcert.c`` (tests only), written from the grammar in the header of
    that file and not from its code: the object of the certificate, or :class:`Undecodable`.  It checks
    the syntax (keywords, labels, canonical integers, counts, nothing after ``end``); whether the tree fits
    the instance is left to ``pycheck`` on the decoded object."""
    import re
    toks = [tok for tok in re.split(rb"[ \n\t\r]+", data) if tok]
    integer = re.compile(rb"(0|-?[1-9][0-9]*)\Z")
    at = 0

    def take():
        nonlocal at
        if at >= len(toks):
            raise Undecodable("input ends")
        at += 1
        return toks[at - 1]

    def word(expected):
        if take() != expected:
            raise Undecodable(f"expected {expected!r}")

    def value():
        tok = take()
        if not integer.match(tok):
            raise Undecodable("not an integer")
        return int(tok)

    def label(expected):
        if value() != expected:
            raise Undecodable("wrong label")

    def count(least):
        v = value()
        if v < least:
            raise Undecodable("count too small")
        return v

    word(b"leafcert")
    word(b"1")
    word(b"sites")
    n = count(1)
    if n > len(toks):
        raise Undecodable("input ends")
    word(b"shape")
    shape = [count(1) for _ in range(n)]
    if sum(shape) > len(toks):
        raise Undecodable("input ends")
    word(b"bound")
    obj = {"L": value(), "H": [], "J": {}, "leaves": []}
    for i in range(n):
        word(b"h")
        label(i)
        obj["H"].append([value() for _ in range(shape[i])])
    for i, j in pairs_of(n):
        word(b"j")
        label(i)
        label(j)
        obj["J"][f"{i},{j}"] = [[value() for _ in range(shape[j])] for _ in range(shape[i])]
    word(b"leaves")
    T = count(1)
    if T > len(toks):
        raise Undecodable("input ends")
    for t in range(T):
        word(b"leaf")
        label(t)
        word(b"u")
        U = [value() for _ in range(n)]
        word(b"p")
        P2 = {f"{i},{j}": value() for i, j in pairs_of(n)}
        m = {}
        for i in range(n):
            for j in range(n):
                if i != j:
                    word(b"m")
                    label(i)
                    label(j)
                    m[f"{i},{j}"] = [value() for _ in range(shape[i])]
        obj["leaves"].append({"U": U, "P2": P2, "m": m})
    word(b"tree")

    def node(depth):
        if depth > 200:
            raise Undecodable("too deep")
        kind = take()
        if kind == b"L":
            return {"leaf": value()}
        if kind != b"B":
            raise Undecodable("node")
        site, kids = value(), count(0)
        if kids > len(toks):
            raise Undecodable("input ends")
        children = {}
        for a in range(kids):
            label(a)
            children[str(a)] = node(depth + 1)
        return {"site": site, "children": children}

    obj["tree"] = node(0)
    word(b"end")
    if at != len(toks):
        raise Undecodable("data after end")
    return obj


def integers_of(obj):
    yield obj["L"]
    for row in obj["H"]:
        yield from row
    for table in obj["J"].values():
        for row in table:
            yield from row
    for leaf in obj["leaves"]:
        yield from leaf["U"]
        yield from leaf["P2"].values()
        for vec in leaf["m"].values():
            yield from vec


def corrupt(rng, data):
    """One to three random corruptions of an encoding, at the level of tokens or of bytes."""
    junk = [b"0", b"1", b"2", b"3", b"-1", b"7", b"-0", b"+1", b"01", b"1.5", b"1e3", b"x", b"L", b"B", b"end", b"tree",
            b"leaf", b"u", b"p", b"m", b"h", b"j", b"-", b"", str(2 ** 63).encode(), str(2 ** 63 - 1).encode(),
            str(-2 ** 63).encode(), str(-2 ** 63 - 1).encode(), b"9" * 30, b"4097", b"1048577", b"99999999999"]
    for _ in range(rng.choice((1, 1, 1, 2, 3))):
        how = rng.randrange(10)
        toks = data.split(b" ") if how < 7 else None
        if toks is not None and len(toks) < 2:
            how, toks = 9, None
        if how == 0:                                      # one token replaced
            toks[rng.randrange(len(toks))] = rng.choice(junk)
        elif how == 1:                                    # one number changed a little
            at = rng.randrange(len(toks))
            try:
                toks[at] = str(int(toks[at]) + rng.choice((-1, 1, 1, 2, 5))).encode()
            except ValueError:
                toks[at] = rng.choice(junk)
        elif how == 2:
            del toks[rng.randrange(len(toks))]
        elif how == 3:
            at = rng.randrange(len(toks))
            toks.insert(at, toks[at])
        elif how == 4:
            at = rng.randrange(len(toks) - 1)
            toks[at], toks[at + 1] = toks[at + 1], toks[at]
        elif how == 5:
            toks = toks[: rng.randrange(len(toks))]
        elif how == 6:
            toks += [rng.choice(junk) for _ in range(rng.randint(1, 3))]
        if toks is not None:
            data = b" ".join(toks)
            continue
        raw = bytearray(data)
        at = rng.randrange(len(raw) + 1)
        byte = rng.choice((0, 9, 10, 11, 12, 13, 32, 43, 45, 46, 48, 57, 66, 76, 101, 255, rng.randrange(256)))
        if how == 7 and at < len(raw):
            raw[at] = byte
        elif how == 8:
            raw.insert(at, byte)
        elif at < len(raw):
            del raw[at]
        data = bytes(raw)
    return data


@pytest.fixture(scope="module")
def corrupted_encodings():
    """Corrupted encodings of small certificates, with the result of ``leafcert.c`` on each."""
    rng = random.Random(SEED + 7)
    seeds = []
    for label, obj, must, low in fuzz_cases(SEED + 7, 12):
        seeds.append(b" ".join(loader.encode(loader.validate(obj)).split()))
    out = []
    for _ in range(3000 * SCALE):
        data = corrupt(rng, rng.choice(seeds))
        out.append((data, ckernel.check_encoded(data)))
    return out


def test_c_parser_on_corrupted_encodings_against_the_decoder(corrupted_encodings):
    """No corrupted input may be accepted or given an inequality verdict unless it decodes to a well-formed
    certificate on which the Python engine returns the same result; and every input that decodes to a
    well-formed certificate with 64-bit integers must get that result (the parser may not refuse it)."""
    stats = Counter()
    for data, rc in corrupted_encodings:
        try:
            obj = decode(data)
            rp = pycheck.verify(obj)
        except Undecodable:
            obj = rp = None
        in_range = obj is not None and all(INT64_MIN <= v <= INT64_MAX for v in integers_of(obj))
        if rp is not None and rp["kind"] != "format" and in_range:
            assert strip(rc) == strip(rp), (data[-200:], rc, rp)
            stats["still a well-formed certificate: accepted" if rp["accepted"] else
                  "still a well-formed certificate: an inequality fails"] += 1
            if rp["accepted"]:
                assert obj["L"] <= brute_min(obj)
        else:
            assert rc["kind"] in ("format", "range", "limit") and not rc["accepted"], (data[-200:], rc)
            assert rc["failure"] is None and rc["counts"] is None and rc["reason"]
            if rp is not None and rp["kind"] != "format":
                assert rc["kind"] == "range"                  # a well-formed certificate with an integer beyond 64 bits
            stats["rejected: " + rc["kind"]] += 1
    emit("C parser, corrupted encodings", dict(stats))
    assert stats["rejected: format"] > 1500 * SCALE and stats["rejected: range"] > 5 * SCALE
    assert stats["still a well-formed certificate: accepted"] + stats["still a well-formed certificate: an inequality fails"] > 150 * SCALE


def test_c_parser_under_sanitizers(corrupted_encodings, tmp_path):
    """The stand-alone checker compiled with the address and undefined-behaviour sanitizers reads every
    corrupted encoding and (if the commit is present) the nine vectors and their controls: no report, and
    the verdicts of the library."""
    try:
        exe = ckernel.compile_c(tmp_path / "leafcert_san", shared=False,
                                flags=("-O1", "-g", "-fsanitize=address,undefined", "-fno-sanitize-recover=all"))
    except subprocess.CalledProcessError:
        pytest.skip("the compiler cannot build with -fsanitize=address,undefined on this machine")
    cases = list(corrupted_encodings)
    for v in load_vectors().values():
        for obj in [v["obj"], *rv.build_controls(v["obj"]).values()]:
            data = loader.encode(loader.validate(obj))
            cases.append((data, ckernel.check_encoded(data)))
    names = []
    for index, (data, _) in enumerate(cases):
        path = tmp_path / f"{index}.txt"
        path.write_bytes(data)
        names.append(str(path))
    env = dict(os.environ, ASAN_OPTIONS="exitcode=99:detect_leaks=1", UBSAN_OPTIONS="exitcode=99:print_stacktrace=1")
    lines = []
    for start in range(0, len(names), 1000):
        done = subprocess.run([str(exe), *names[start:start + 1000]], capture_output=True, env=env)
        assert done.returncode in (0, 1) and done.stderr == b"", done.stderr[-2000:]
        lines += done.stdout.splitlines()
    assert len(lines) == len(cases)
    for line, name, (data, rc) in zip(lines, names, cases):
        verdict = line[len(name) + 2:]
        want = b"ACCEPT" if rc["accepted"] else b"REJECT " + rc["kind"].encode()
        assert line.startswith(name.encode() + b": ") and verdict.startswith(want), (line[-200:], rc)
    emit("C parser under sanitizers", {"inputs": len(cases), "reports": 0})
