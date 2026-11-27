"""Tests of the producer of "shares at the leaves" certificates (``src/metricchain_eng/leafprod``).

The producer is never trusted here: every certificate it returns is given again to both engines of the
checker, and every claimed minimum is compared with an enumeration written in this file.  Layers:

  1. the C kernel against its plain-Python reference (identical messages and values), and the dual value
     against enumeration of the box (it is a lower bound whatever the messages);
  2. small random instances, every leaf-bound method and branching rule: the certified ``L`` is the true
     minimum, the certificate with ``L + 1`` is rejected by both engines, a request for ``L = min + 1`` is
     refuted with a state, no floating-point number is in a certificate;
  3. chains and trees are certified with a single leaf by every method (the relaxation is tight there);
     frustrated cycles need branching, with the depth the science division's Proposition P7.5 predicts;
  4. unequal alphabets, ties, negative entries, degenerate cases, malformed instances;
  5. limits (time, leaves, integers, checker operations), partial certificates, determinism, shared leaves;
  6. the exact solvers used as oracles and baselines, and the seeded instance generators;
  7. the published instances of the science division's nine certificate files (read with ``git show`` at
     commit ``2b4ccdf``; skipped if that commit is not in the clone): the producer certifies their bound
     ``L = 0`` on each, and its trees are compared with theirs.

``LEAFPROD_FUZZ=k`` multiplies the number of random instances by ``k`` (default 1: about a minute).
Statistics are printed (``pytest -s``) on lines that start with ``LEAFPROD``.
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "leafcert"))

from metricchain_eng.leafcert import check  # noqa: E402
from metricchain_eng.leafprod import InstanceError, ckernel, exact, families, produce, pykernel, root_relaxation  # noqa: E402
from metricchain_eng.leafprod.model import MAX_ABS, Model  # noqa: E402
import run_vectors as rv  # noqa: E402  (reads the science division's nine files with ``git show``; executes nothing of theirs)

SCALE = max(1, int(os.environ.get("LEAFPROD_FUZZ", "1")))
SEED = int(os.environ.get("LEAFPROD_SEED", "20261126"))
CONFIGS = [("mp", "strong"), ("mp", "maxdeg"), ("mp", "margin"), ("mp", "maxdom"),
           ("lp", "strong"), ("lp", "frac"), ("hybrid", "strong"), ("hybrid", "frac")]


# ================================================================================================ helpers
def emit(label, stats):
    print(f"LEAFPROD {label}: {json.dumps(stats, sort_keys=True)}")


def enumerate_min(inst, box=None):
    """Minimum of the instance over the whole domain (or a box, as a list of lists of states), with Python
    integers and nothing of the library."""
    H, J = inst["H"], inst["J"]
    n = len(H)
    tables = [(int(key.split(",")[0]), int(key.split(",")[1]), table) for key, table in J.items()]
    best = None
    for x in itertools.product(*(box if box is not None else [range(len(row)) for row in H])):
        e = sum(H[i][x[i]] for i in range(n)) + sum(table[x[i]][x[j]] for i, j, table in tables)
        if best is None or e < best:
            best = e
    return best


def random_instance(rng, style=None, n=None, kmax=4, R=None, one_state=0.1):
    """1-6 sites with 1-``kmax`` states; styles: all pairs, some pairs, a chain, a tree, a ring, ``ties``
    (entries from a set of two values, so that minima are far from unique)."""
    n = n or rng.randint(1, 6)
    shape = [1 if rng.random() < one_state else rng.randint(2, kmax) for _ in range(n)]
    style = style or rng.choice(("dense", "dense", "sparse", "chain", "tree", "ring", "ties"))
    R = R or rng.choice((1, 3, 25, 1000))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    order = list(range(n))
    rng.shuffle(order)
    link = lambda u, v: (min(u, v), max(u, v))          # noqa: E731
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
    draw = (lambda: rng.choice((0, -R))) if style == "ties" else (lambda: rng.randint(-R, R))
    H = [[draw() for _ in range(k)] for k in shape]
    J = {f"{i},{j}": [[draw() for _ in range(shape[j])] for _ in range(shape[i])] for i, j in pairs if (i, j) in active}
    return {"H": H, "J": J, "style": style}


def integers_only(obj):
    """Every number of a JSON-like object is a Python ``int`` (not a float, not a bool)."""
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
        elif not isinstance(cur, str) and type(cur) is not int:
            return False
    return True


def assert_certified(result, low, inst=None):
    """``result`` is a certificate for ``low`` that both engines accept, with a witness state."""
    assert result.status == "certified", (result.status, result.reason, inst)
    assert result.L == low and result.optimal and result.energy == low and result.best_bound == low
    cert = result.certificate
    for engine in ("c", "python"):
        res = check(cert, engine=engine)
        assert res.accepted and res.bound == low and not res.notes, (engine, res.reason, res.notes)
        assert res.counts["leaf_boxes"] == result.stats["leaf_boxes"]
        assert res.counts["leaf_certificates"] == result.stats["leaf_certificates"]
        assert res.counts["depth"] == result.stats["depth"]
        assert res.counts["additions"] + res.counts["comparisons"] == result.stats["check_ops"]
        assert res.counts["cert_integers"] == result.stats["cert_integers"]
    assert integers_only(cert)
    assert cert["ref"] == result.x
    raised = dict(cert, L=low + 1)
    for engine in ("c", "python"):                       # the same certificate does not prove more
        res = check(raised, engine=engine)
        assert not res.accepted and res.kind == "inequality" and res.failure["inequality"] == "total"


# ================================================================================================ 1. the kernel
def test_c_kernel_equals_the_python_reference_and_bounds_hold():
    rng = random.Random(SEED)
    stats = Counter()
    for _ in range(400 * SCALE):
        inst = random_instance(rng)
        mod = Model(inst)
        kc, kp = ckernel.Kernel(mod), pykernel.Kernel(mod)
        path = [(i, rng.randrange(int(mod.k[i]))) for i in range(mod.n) if rng.random() < 0.3]
        cand = [i for i in range(mod.n) if i not in dict(path) and mod.k[i] >= 2]
        block = None
        if cand and rng.random() < 0.3:
            i = rng.choice(cand)
            block = (i, sorted(rng.sample(range(int(mod.k[i])), rng.randint(1, int(mod.k[i])))))
        dlen, dom = mod.box(path, block)
        doms = [[int(dom[mod.koff[i] + t]) for t in range(int(dlen[i]))] for i in range(mod.n)]
        low = enumerate_min(inst, doms)
        start = (np.array([rng.randint(-5, 5) for _ in range(max(mod.M, 1))], dtype=np.int64)
                 if rng.random() < 0.5 else mod.zero_messages())
        before = kc.eval(dlen, dom, start)[0]
        assert before <= low                              # any integer messages give a lower bound
        for wmode in (0, 1):
            mc, mp = start.copy(), start.copy()
            target = rng.choice((10 ** 9, -10 ** 9, low))
            sweeps, patience = rng.choice((0, 1, 2, 50)), rng.choice((1, 3))
            rc = kc.ascent(dlen, dom, mc, target, sweeps, patience, wmode)
            rp = kp.ascent(dlen, dom, mp, target, sweeps, patience, wmode)
            assert rc == rp and (mc == mp).all()
            ec, ep = kc.eval(dlen, dom, mc), kp.eval(dlen, dom, mp)
            assert ec[0] == ep[0] and all((a == b).all() for a, b in zip(ec[1:], ep[1:]))
            assert ec[0] <= low
            if rc[0] is not None:
                assert rc[0] == ec[0]                     # the value the passes computed is the exact value
            if sweeps:
                assert ec[0] >= before                    # the ascent does not decrease the value
            assert (kc.probe_all(dlen, dom, mc) == kp.probe_all(dlen, dom, mp)).all()
            assert (kc.decode(dlen, dom, mc) == kp.decode(dlen, dom, mp)).all()
            assert (kc.core(dlen) == kp.core(dlen)).all()
            i = rng.randrange(mod.n)
            a1, a2 = mc.copy(), mp.copy()
            t1, t2 = kc.pull_site(dlen, dom, a1, i), kp.pull_site(dlen, dom, a2, i)
            assert (t1 == t2).all() and (a1 == a2).all()
            assert kc.eval(dlen, dom, a1)[0] >= ec[0]     # a pull does not decrease the value either
            x1 = np.array([rng.choice(d) for d in doms], dtype=np.int64)
            x2 = x1.copy()
            assert kc.icm(x1, (dlen, dom)) == kp.icm(x2, (dlen, dom)) and (x1 == x2).all()
            assert kc.energy(x1) == mod.energy([int(v) for v in x1])
        m = start.copy()                                  # one full sweep from any start is exact on a forest
        kc.ascent(dlen, dom, m, 10 ** 9, 1, 1, 0)
        value = kc.eval(dlen, dom, m)[0]
        stats["instances"] += 1
        stats["one sweep is tight"] += value == low
        if inst["style"] in ("chain", "tree"):
            assert value == low
            x = kc.decode(dlen, dom, m)
            assert mod.energy([int(v) for v in x]) == low             # and the decoded state attains the minimum
            stats["forests"] += 1
    emit("kernel", dict(stats))
    assert stats["forests"] >= 60 * SCALE


def test_the_pull_formula_behind_shared_leaves():
    """After a pull at site i the value on the box with D_i = B is ``rest + min_{a in B} theta_i(a)``."""
    rng = random.Random(SEED + 1)
    for _ in range(300 * SCALE):
        inst = random_instance(rng, n=rng.randint(2, 5), one_state=0.0)
        mod = Model(inst)
        ker = ckernel.Kernel(mod)
        i = rng.randrange(mod.n)
        path = [(j, rng.randrange(int(mod.k[j]))) for j in range(mod.n) if j != i and rng.random() < 0.3]
        dlen, dom = mod.box(path)
        m = np.array([rng.randint(-9, 9) for _ in range(max(mod.M, 1))], dtype=np.int64)
        theta = ker.pull_site(dlen, dom, m, i)
        total, U, P, _ = ker.eval(dlen, dom, m)
        rest = total - int(U[i]) - sum(int(P[e]) for e, _ in mod.nbrs[i])
        states = sorted(rng.sample(range(int(mod.k[i])), rng.randint(1, int(mod.k[i]))))
        hull = mod.box(path, (i, states))
        assert ker.eval(hull[0], hull[1], m)[0] == rest + min(int(theta[a]) for a in states)


# ================================================================================================ 2. against enumeration
def test_small_random_instances_every_method_and_rule():
    rng = random.Random(SEED + 2)
    stats = Counter()
    for _ in range(150 * SCALE):
        inst = random_instance(rng)
        low = enumerate_min(inst)
        assert exact.brute_force(inst)[0] == low and exact.eliminate(inst)[0] == low      # the oracles agree
        for bound, branching in CONFIGS:
            res = produce(inst, bound=bound, branching=branching, order=rng.choice(("best", "dfs")), time_limit=30)
            assert_certified(res, low, inst)
            assert res.stats["anomalies"] == 0
            stats[f"{bound}/{branching} leaf boxes"] += res.stats["leaf_boxes"]
            stats[f"{bound}/{branching} single leaf"] += res.stats["leaf_boxes"] == 1
        res = produce(inst, L=low - 7, time_limit=30)                 # a bound below the minimum
        assert res.status == "certified" and res.L == low - 7 and not res.optimal and "ref" not in res.certificate
        assert check(res.certificate, "c").accepted and check(res.certificate, "python").accepted
        res = produce(inst, L=low, time_limit=30)                     # the minimum itself, given
        assert_certified(res, low, inst)
        for bound in ("mp", "lp", "hybrid"):                          # one more is refuted, never certified
            res = produce(inst, L=low + 1, bound=bound, time_limit=30)
            assert res.status == "refuted" and res.certificate is None and res.L is None
            assert res.energy == low and Model(inst).energy(res.x) == low
    emit("random instances", dict(stats))


def test_the_python_kernel_gives_the_same_certificate():
    rng = random.Random(SEED + 3)
    for _ in range(25 * SCALE):
        inst = random_instance(rng, n=rng.randint(3, 6))
        a = produce(inst, kernel="c", branching=rng.choice(("strong", "margin")))
        b = produce(inst, kernel="python", branching=a.stats["branching"])
        assert a.status == b.status == "certified" and a.certificate == b.certificate


def test_search_without_certificate_is_the_same_search():
    rng = random.Random(SEED + 4)
    for _ in range(40 * SCALE):
        inst = random_instance(rng, n=rng.randint(4, 7), style=rng.choice(("dense", "ring", "sparse")))
        a = produce(inst)
        b = produce(inst, certificate=False)
        assert b.status == "solved" and b.certificate is None and b.L == a.L and b.optimal
        for key in ("nodes", "leaf_boxes", "leaf_certificates", "depth", "check_ops", "cert_integers"):
            assert a.stats[key] == b.stats[key]


def test_determinism_and_seed():
    inst = families.make("complete", 9, 3, 12345)
    a, b, c = produce(inst, seed=1), produce(inst, seed=1), produce(inst, seed=2)
    assert a.status == b.status == c.status == "certified"
    assert json.dumps(a.certificate, sort_keys=True) == json.dumps(b.certificate, sort_keys=True)
    assert a.L == c.L == exact.brute_force(inst)[0]


# ================================================================================================ 3. tight and not tight
@pytest.mark.parametrize("bound", ["mp", "lp", "hybrid"])
def test_chains_and_trees_need_a_single_leaf(bound):
    """The relaxation is tight on forests.  ``mp`` is exact there by construction (the backward pass is
    dynamic programming); for ``lp`` this is an observation about the multipliers HiGHS returns."""
    rng = random.Random(SEED + 5)
    stats = Counter()
    cases = [(family, n, k) for family in ("chain", "tree") for n in (2, 3, 7, 20, 45) for k in (2, 3, 6, "mixed")]
    for family, n, k in cases * SCALE:
        inst = families.make(family, n, k, rng.getrandbits(60))
        low = exact.eliminate(inst)[0]
        res = produce(inst, bound=bound, time_limit=30)
        assert res.status == "certified" and res.L == low
        stats["instances"] += 1
        stats["single leaf"] += res.stats["leaf_boxes"] == 1
        if res.stats["leaf_boxes"] != 1:
            stats[f"not single: {family} n={n} k={k}"] += 1
    emit(f"forests, bound={bound}", dict(stats))
    assert stats["single leaf"] == stats["instances"]


def ring(n, w4=7, r4=40):
    """The ring of the science division's Proposition P7.5 in units of 1/4: binary sites, a changed site
    costs 4, two changed ring neighbours gain ``w4`` (w = w4/4), two changed sites elsewhere cost ``r4``."""
    H = [[0, 4] for _ in range(n)]
    J = {}
    for i in range(n):
        for j in range(i + 1, n):
            near = j - i == 1 or (i == 0 and j == n - 1)
            J[f"{i},{j}"] = [[0, 0], [0, -w4 if near else r4]]
    return {"H": H, "J": J}


@pytest.mark.parametrize("n", [4, 5, 6, 7, 8, 9])
def test_the_ring_of_P7_5_needs_depth_n_over_3(n):
    """Their statement: the reference (no site changed) is the unique minimiser, value 0; for 3/2 < w < 2
    every certified tree has depth at least ceil(n/3), and one with ceil(n/3) + 1 leaves exists."""
    inst = ring(n)
    assert enumerate_min(inst) == 0
    assert root_relaxation(inst) < -0.25                  # the relaxation has a gap
    need = -(-n // 3)
    out = {}
    for bound, branching in CONFIGS:
        res = produce(inst, bound=bound, branching=branching)
        assert_certified(res, 0, inst)
        assert res.x == [0] * n
        assert res.stats["depth"] >= need and res.stats["leaf_boxes"] >= need + 1
        out[f"{bound}/{branching}"] = [res.stats["depth"], res.stats["leaf_boxes"]]
    emit(f"ring n={n} (depth, leaf boxes; P7.5: at least {need}, {need + 1})", out)


def test_a_frustrated_triangle_needs_branching_and_three_sites_need_one_level():
    """Three binary sites that dislike agreeing: minimum 1, relaxation 0.  One branching on any site
    certifies every three-site instance (their Proposition P7.4(c))."""
    J = {key: [[1, 0], [0, 1]] for key in ("0,1", "0,2", "1,2")}
    inst = {"H": [[0, 0]] * 3, "J": J}
    assert enumerate_min(inst) == 1 and abs(root_relaxation(inst)) < 1e-9
    for bound, branching in CONFIGS:
        res = produce(inst, bound=bound, branching=branching)
        assert_certified(res, 1, inst)
        assert res.stats["depth"] == 1 and res.stats["leaf_boxes"] == 2
    rng = random.Random(SEED + 6)
    gaps = 0
    for _ in range(150 * SCALE):
        inst = random_instance(rng, n=3, style="dense", one_state=0.0)
        low = enumerate_min(inst)
        for bound in ("mp", "lp"):
            res = produce(inst, bound=bound)
            assert_certified(res, low, inst)
            assert res.stats["depth"] <= 1
        gaps += res.stats["depth"] == 1
    emit("three sites", {"instances": 150 * SCALE, "needed one branching": gaps})


# ================================================================================================ 4. corner cases
def test_degenerate_instances():
    for inst, low in (({"H": [[5]], "J": {}}, 5),                                 # one site, one state
                      ({"H": [[3, -2, 7]], "J": {}}, -2),                          # one site
                      ({"H": [[4], [-1], [0]], "J": {"0,1": [[2]], "1,2": [[-9]]}}, -4),      # one state everywhere
                      ({"H": [[0, 0], [0, 0, 0]], "J": {"0,1": [[0, 0, 0], [0, 0, 0]]}}, 0),  # nothing but zeros
                      ({"H": [[1, 1], [1, 1]], "J": {"0,1": [[5, 5], [5, 5]]}}, 7),          # constant tables
                      ({"H": [[0, 0], [7], [0, 0, 0]], "J": {"0,2": [[1, 0, 0], [0, 1, 1]]}}, 7),
                      ({"H": [[-MAX_ABS, MAX_ABS], [MAX_ABS, -MAX_ABS]], "J": {"0,1": [[MAX_ABS, 0], [-MAX_ABS, MAX_ABS]]}},
                       -2 * MAX_ABS)):
        assert enumerate_min(inst) == low
        for bound, branching in CONFIGS:
            res = produce(inst, bound=bound, branching=branching)
            assert_certified(res, low, inst)
    res = produce({"H": [[5]], "J": {}})
    assert res.stats["leaf_boxes"] == 1 and res.certificate["tree"] == {"leaf": 0} and res.certificate["J"] == {}
    # pairs omitted from J are zero tables, written out in the certificate
    res = produce({"H": [[0, 1], [2, 0], [0, 3]], "J": {"0,2": [[0, 5], [5, 0]]}})
    assert sorted(res.certificate["J"]) == ["0,1", "0,2", "1,2"] and res.certificate["J"]["0,1"] == [[0, 0], [0, 0]]
    assert res.stats["missing_pairs"] == 2


def test_ties_everywhere():
    """Potts-like tables with many equal entries: every minimiser is as good as any other."""
    rng = random.Random(SEED + 7)
    for _ in range(60 * SCALE):
        inst = random_instance(rng, style="ties", n=rng.randint(2, 6), one_state=0.0)
        low = enumerate_min(inst)
        for bound, branching in (("mp", "strong"), ("lp", "frac"), ("hybrid", "strong")):
            assert_certified(produce(inst, bound=bound, branching=branching), low, inst)


@pytest.mark.parametrize("bad, text", [
    ({"H": [], "J": {}}, "non-empty"),
    ({"H": [[]], "J": {}}, "needs a state"),
    ({"H": [[1.0, 2]], "J": {}}, "not an integer"),
    ({"H": [[True, 2]], "J": {}}, "not an integer"),
    ({"H": [[1, 2], [0, 0]], "J": {"0,1": [[1, 2]]}}, "2 row"),
    ({"H": [[1, 2], [0, 0]], "J": {"0,1": [[1, 2], [3]]}}, "list of 2"),
    ({"H": [[1, 2], [0, 0]], "J": {"1,0": [[1, 2], [3, 4]]}}, "i < j"),
    ({"H": [[1, 2], [0, 0]], "J": {"0, 1": [[1, 2], [3, 4]]}}, "decimal"),
    ({"H": [[1, 2], [0, 0]], "J": {"0,2": [[1, 2], [3, 4]]}}, "i < j"),
    ({"H": [[1, 2], [0, 0]], "J": {"a,b": [[1, 2], [3, 4]]}}, "form"),
    ({"H": [[1, 2], [0, 0]], "J": [[1, 2], [3, 4]]}, "dict"),
    ({"H": [[1, 2 ** 57]], "J": {}}, "2^56"),
    ({"H": [[1, 2], [0, 0]], "J": {"0,1": [[1, 2], [3, -2 ** 57]]}}, "2^56"),
    ({"H": [[0, 0]] * 40, "J": {f"0,{j}": [[2 ** 55, 0], [0, 0]] for j in range(1, 40)}}, "not be safe"),
    ([[1, 2]], "dict"),
])
def test_malformed_instances_are_refused_with_a_reason(bad, text):
    with pytest.raises(InstanceError) as err:
        produce(bad)
    assert text in str(err.value)


def test_arguments_are_validated():
    inst = {"H": [[0, 1]], "J": {}}
    for kwargs in ({"bound": "x"}, {"branching": "x"}, {"order": "x"}, {"L": 1.5}, {"kernel": "x"},
                   {"bound": "mp", "branching": "frac"}):
        with pytest.raises(ValueError):
            produce(inst, **kwargs)


# ================================================================================================ 5. limits and sharing
def hard_instance():
    return families.make("complete", 10, 4, 99)           # 4^10 states; a tree of 28 leaf boxes


def test_limits_are_reported_and_the_partial_certificate_is_checked():
    inst = hard_instance()
    low = exact.brute_force(inst)[0]
    full = produce(inst)
    assert_certified(full, low)
    assert full.stats["leaf_boxes"] > 20                  # a real tree
    seen = Counter()
    for kwargs in ({"max_leaves": 5}, {"max_cert_integers": 3 * full.stats["ints_per_leaf"]},
                   {"max_check_ops": full.stats["check_ops"] // 4}, {"time_limit": 0.0}):
        res = produce(inst, **kwargs)
        assert res.status == "limit" and res.L is None and not res.optimal
        seen[res.stats["stop"]] += 1
        assert res.energy >= low
        if res.certificate is not None:                   # a certificate for the weaker bound, checked
            assert res.bound_checked and res.best_bound <= low
            for engine in ("c", "python"):
                out = check(res.certificate, engine=engine)
                assert out.accepted and out.bound == res.best_bound
        else:
            assert not res.bound_checked
        if res.best_bound is not None:
            assert res.best_bound <= low
        res = produce(inst, partial=False, **kwargs)
        assert res.status == "limit" and res.certificate is None and not res.bound_checked
    assert set(seen) == {"leaves", "cert_integers", "check_ops", "time"}
    res = produce(inst, max_leaves=5)
    assert res.certificate is not None and res.best_bound < low        # the partial bound is a real statement


def test_children_share_leaf_certificates():
    rng = random.Random(SEED + 8)
    shared = total = 0
    for _ in range(12 * SCALE):
        inst = families.make("complete", 6, 6, rng.getrandbits(60))
        low = exact.brute_force(inst)[0]
        a = produce(inst)
        b = produce(inst, share=False)
        assert_certified(a, low)
        assert_certified(b, low)
        assert b.stats["leaf_boxes"] == b.stats["leaf_certificates"]
        assert a.stats["leaf_certificates"] <= a.stats["leaf_boxes"]
        assert a.stats["shared_by_parent"] + a.stats["shared_by_sibling"] >= a.stats["leaf_boxes"] - a.stats["leaf_certificates"]
        shared += a.stats["leaf_boxes"] - a.stats["leaf_certificates"]
        total += a.stats["leaf_boxes"]
        used = Counter()
        stack = [a.certificate["tree"]]
        while stack:
            node = stack.pop()
            if "leaf" in node:
                used[node["leaf"]] += 1
            else:
                stack.extend(node["children"].values())
        assert sum(v - 1 for v in used.values()) == a.stats["leaf_boxes"] - a.stats["leaf_certificates"]
    emit("shared leaves (complete graph, 6 sites, 6 states)", {"leaf boxes": total, "saved certificates": shared})
    assert shared > 0


def test_messages_outside_the_box_and_dense_form():
    """The dense certificate has a message vector for every ordered pair and a table for every pair."""
    inst = families.make("grid", 9, 3, 7)
    res = produce(inst)
    cert = res.certificate
    n = 9
    assert len(cert["J"]) == n * (n - 1) // 2
    for leaf in cert["leaves"]:
        assert len(leaf["m"]) == n * (n - 1) and len(leaf["P2"]) == n * (n - 1) // 2 and len(leaf["U"]) == n
        for key, table in cert["J"].items():
            if not any(any(row) for row in table):        # no interaction: zero messages, zero pair term
                i, j = key.split(",")
                assert leaf["P2"][key] == 0 and not any(leaf["m"][key]) and not any(leaf["m"][f"{j},{i}"])


# ================================================================================================ 6. oracles, generators
def test_exact_solvers_agree_with_enumeration():
    rng = random.Random(SEED + 9)
    for _ in range(200 * SCALE):
        inst = random_instance(rng, n=rng.randint(1, 7))
        low = enumerate_min(inst)
        value, x, states = exact.brute_force(inst)
        assert value == low and Model(inst).energy(x) == low
        assert states == int(np.prod([len(row) for row in inst["H"]]))
        value, x = exact.eliminate(inst)
        assert value == low and Model(inst).energy(x) == low
    assert exact.brute_force(families.make("chain", 40, 3, 1), max_states=10 ** 6) is None
    assert exact.eliminate(families.make("complete", 12, 4, 1), max_table=10 ** 4) is None
    order, largest, _ = exact.plan(families.make("band3", 30, 3, 1))
    assert largest == 3 ** 4 and sorted(order) == list(range(30))
    assert exact.plan(families.make("tree", 30, 5, 1))[1] == 25


def test_generators_are_seeded_and_have_the_structure_they_claim():
    for family in families.FAMILIES:
        for k in (2, 3, "mixed"):
            n = 12
            seed = families.seed_of("test", family, k, n, 0)
            a, b = families.make(family, n, k, seed), families.make(family, n, k, seed)
            assert a == b and families.digest(a) == families.digest(b)
            assert families.digest(a) != families.digest(families.make(family, n, k, seed + 1))
            mod = Model(a)
            assert mod.n == n and mod.max_abs <= families.R
            degree = Counter()
            for e in range(mod.ne):
                degree[int(mod.eu[e])] += 1
                degree[int(mod.ev[e])] += 1
            if family == "chain":
                assert mod.ne == n - 1 and max(degree.values()) == 2
            elif family == "tree":
                assert mod.ne == n - 1 and exact.plan(mod)[1] <= max(mod.k) ** 2
            elif family == "cubic":
                assert all(degree[i] == 3 for i in range(n))
            elif family == "complete":
                assert a["edges"] == n * (n - 1) // 2
            elif family in ("grid", "potts"):
                assert a["edges"] == 17 and families.grid_shape(n) == (3, 4)
            elif family == "band2":
                assert a["edges"] == 2 * n - 3
            elif family == "band3":
                assert a["edges"] == 3 * n - 6
            if k == "mixed":
                assert set(mod.k.tolist()) <= set(families.MIXED)
            if family == "potts":
                for table in a["J"].values():
                    assert all((v < 0) == (i == j) for i, row in enumerate(table) for j, v in enumerate(row))
    # the generator's output must not drift between interpreter versions: one instance, pinned
    assert families.seed_of("leafcert-bench-v1", "grid", 3, 25, 0) == PINNED_SEED
    assert families.digest(families.make("grid", 25, 3, PINNED_SEED)) == PINNED_DIGEST


PINNED_SEED = 16390318503233351280
PINNED_DIGEST = "e77ece63ee2aaad0f76f7d6ca55e8afcf4100eee5b7f69c7e0993ab92d831c38"


# ================================================================================================ 7. the published instances
@pytest.mark.skipif(not rv.commit_available(), reason=f"commit {rv.COMMIT} (the science division's nine files) is not in this clone")
def test_the_published_instances_of_the_science_division():
    """Their request P7-E1 names these files as test vectors of a producer.  For each file: the instance
    (``H``, ``J``) is taken, everything else of the file is ignored; the producer must certify their bound
    ``L = 0`` (the minimum, attained only at their ``ref``), and both engines must accept."""
    seen = {}
    for name, row in rv.FILES.items():
        obj = json.loads(rv.read_vector(name)[0])
        key = json.dumps([obj["H"], obj["J"]], sort_keys=True)
        if key in seen:                                   # nine files, four instances
            continue
        inst = {"H": obj["H"], "J": obj["J"]}
        value, state, _ = exact.brute_force(inst)
        assert value == 0 == obj["L"] and state == obj["ref"]
        theirs = [(len(json.loads(rv.read_vector(other)[0])["leaves"]), rv.REPORT_TABLE[label]["leaf_boxes"],
                   rv.REPORT_TABLE[label]["depth"]) for other, label in rv.FILES.items()
                  if json.dumps([json.loads(rv.read_vector(other)[0])[t] for t in ("H", "J")], sort_keys=True) == key]
        out = {"sites": len(obj["H"]), "their (leaf certificates, leaf boxes, depth)": sorted(set(theirs))}
        for bound, branching in (("mp", "strong"), ("mp", "maxdeg"), ("lp", "strong"), ("hybrid", "strong")):
            res = produce(inst, bound=bound, branching=branching, time_limit=60)
            assert_certified(res, 0, name)
            assert res.x == obj["ref"]
            given = produce(inst, L=0, bound=bound, branching=branching, time_limit=60)
            assert given.status == "certified" and given.L == 0
            out[f"{bound}/{branching}"] = [res.stats["leaf_certificates"], res.stats["leaf_boxes"], res.stats["depth"],
                                           round(res.stats["time_total"], 3)]
        seen[key] = out
        emit(f"published instance of {row.split(',')[0]}", out)
    assert len(seen) == 4                                 # nine files, four instances (Ser6 x4, Lys3 x2, LKSE:6 x2, Leu16)

