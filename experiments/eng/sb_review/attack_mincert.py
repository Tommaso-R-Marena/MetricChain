"""Independent tests of the structural-biology division's certificate core (``src/metricchain_sb`` at its commit
720e0ec: ``model``, ``mincert``, ``mincheck``, ``gmec``), written by the Computational Research Division.

Nothing of the reviewed package is copied here: it is imported from a pinned, read-only checkout given by
``--sb`` (a ``git worktree`` of that commit).  The tests are ours and are built to *falsify* its claims:

  A  random certificate trees that its producer would never emit (valid and invalid prunes, missing and surplus
     children, arbitrary messages), with the claimed bound set exactly at, below and above what the tree proves:
     its checker against ours (``indep_mincheck``), against the theory division's reference checker after its
     own conversion, and against enumeration
  B  hand-made traps (a state "dominated" by itself, by a state outside the box, ...)
  C  the limits of its fixed-width arithmetic (a star of degree 4092 with entries next to 2^50)
  D  malformed JSON documents through its loader
  E  its producer against exact solvers of ours (enumeration; dynamic programming on trees), degenerate
     instances, large magnitudes, the abstention path, and timings

    python experiments/eng/sb_review/attack_mincert.py --sb ~/research/MetricChain-sb-720e0ec --part all
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import itertools
import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import indep_mincheck as ours  # noqa: E402

OUT = HERE / "results"


def load_sb(root: Path):
    sys.path.insert(0, str(root / "src"))
    import metricchain_sb.gmec as gmec
    import metricchain_sb.mincert as mincert
    import metricchain_sb.mincheck as mincheck
    import metricchain_sb.model as model
    spec = importlib.util.spec_from_file_location("sb_reference_checker", root / "experiments" / "reference_checker.py")
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)
    return dict(gmec=gmec, mincert=mincert, mincheck=mincheck, model=model, ref=ref)


# ------------------------------------------------------------------ instances

def random_plain_model(rng: random.Random, n: int, kmax: int, density: float, amp: int, kmin: int = 1) -> dict:
    sizes = [rng.randint(kmin, kmax) for _ in range(n)]
    unary = [[rng.randint(-amp, amp) for _ in range(k)] for k in sizes]
    pair = {}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < density:
                pair[(i, j)] = [[rng.randint(-amp, amp) for _ in range(sizes[j])] for _ in range(sizes[i])]
    return dict(unary=unary, pair=pair)


def sb_model(SB, plain: dict, scale_bits: int = 0):
    return SB["model"].PairModel(unary=[np.array(u, dtype=object) for u in plain["unary"]],
                                 pair={k: np.array(t, dtype=object) for k, t in plain["pair"].items()}, scale_bits=scale_bits)


def enum_min(plain: dict, domains=None) -> int:
    """Exact minimum by vectorised enumeration (int64 is safe for the small tables used with it)."""
    unary, pair = plain["unary"], plain["pair"]
    n = len(unary)
    D = [list(range(len(u))) for u in unary] if domains is None else domains
    shape = [len(d) for d in D]
    E = np.zeros(shape, dtype=np.int64)
    for i in range(n):
        sh = [1] * n
        sh[i] = shape[i]
        E = E + np.array([unary[i][a] for a in D[i]], dtype=np.int64).reshape(sh)
    for (i, j), t in pair.items():
        sh = [1] * n
        sh[i], sh[j] = shape[i], shape[j]
        E = E + np.array([[t[a][b] for b in D[j]] for a in D[i]], dtype=np.int64).reshape(sh)
    return int(E.min())


def tree_dp_min(plain: dict, parent: list) -> int:
    """Exact minimum of a model whose pairs are the edges {i, parent[i]} of a rooted forest (parent[i] < i or -1)."""
    unary, pair = plain["unary"], plain["pair"]
    n = len(unary)
    msg = [list(u) for u in unary]
    for i in range(n - 1, -1, -1):
        p = parent[i]
        if p < 0:
            continue
        t = pair[(p, i)]                                  # indexed [state of p][state of i]
        for a in range(len(unary[p])):
            msg[p][a] += min(t[a][b] + msg[i][b] for b in range(len(unary[i])))
    return sum(min(msg[i]) for i in range(n) if parent[i] < 0)


# ------------------------------------------------------------------ part A: random trees

def random_tree(rng: random.Random, plain: dict, D: list, depth: int, mb: int, amp: int) -> dict:
    unary, pair = plain["unary"], plain["pair"]
    n = len(unary)
    sizes = [len(u) for u in unary]
    nbrs = [[] for _ in range(n)]
    for (i, j) in pair:
        nbrs[i].append(j)
        nbrs[j].append(i)
    x = rng.random()
    if depth <= 0 or x < 0.4:
        m = {}
        for (i, j) in pair:
            for (a, b) in ((i, j), (j, i)):
                if rng.random() < 0.6:
                    m[(a, b)] = [rng.randint(-amp * mb, amp * mb) if rng.random() < 0.8 else 0 for _ in range(sizes[a])]
        return {"node": "leaf", "m": m}
    if x < 0.7:
        i = rng.randrange(n)
        children = {}
        for a in D[i]:
            if rng.random() < 0.06 and len(D[i]) > 1:
                continue                                        # a missing child
            D2 = list(D)
            D2[i] = [a]
            children[a] = random_tree(rng, plain, D2, depth - 1, mb, amp)
        outside = [a for a in range(sizes[i]) if a not in D[i]]
        if outside and rng.random() < 0.25:                     # a surplus child, with a subtree that is invalid on purpose
            a = rng.choice(outside)
            children[a] = {"node": "prune", "site": i, "remove": a, "dominator": a, "rest": {"node": "leaf", "m": {}}}
        return {"node": "branch", "site": i, "children": children}
    i = rng.randrange(n)

    def J(i_, j_, a, b):
        return pair[(i_, j_)][a][b] if i_ < j_ else pair[(j_, i_)][b][a]

    def margin(r, t):
        return unary[i][r] - unary[i][t] + sum(min(J(i, j, r, s) - J(i, j, t, s) for s in D[j]) for j in nbrs[i])

    r = rng.choice(D[i]) if rng.random() < 0.85 else rng.randrange(sizes[i])
    good = [t for t in D[i] if t != r and margin(r, t) >= 0]
    y = rng.random()
    if good and y < 0.65:
        t = rng.choice(good)
    elif y < 0.75:
        t = r                                                   # "dominated by itself"
    else:
        t = rng.randrange(sizes[i])                             # anything: maybe outside the box, maybe not a dominator
    D2 = list(D)
    D2[i] = [s for s in D[i] if s != r] or D[i]                 # (if the prune is accepted the box loses r; never empty)
    return {"node": "prune", "site": i, "remove": r, "dominator": t, "rest": random_tree(rng, plain, D2, depth - 1, mb, amp)}


def part_a(SB, cases: int, seed: int) -> dict:
    rng = random.Random(seed)
    MinCertificate = SB["mincert"].MinCertificate
    stats = dict(cases=0, structure_valid=0, sb_accept=0, sb_reject=0, disagree_ours=0, disagree_reference=0, unsound_sb=0,
                 unsound_format=0, conversion_malformed=0, reference_checked=0, exact_at_bound=0, examples=[])
    for _ in range(cases):
        n = rng.randint(1, 5)
        plain = random_plain_model(rng, n, rng.randint(1, 4), rng.choice([0.3, 0.7, 1.0]), rng.choice([3, 12]))
        message_bits = rng.choice([0, 0, 2, 5])
        mb = 2 ** message_bits
        sizes = [len(u) for u in plain["unary"]]
        domains = []
        for k in sizes:                                         # the root box: usually everything, sometimes a sub-box
            d = list(range(k))
            if rng.random() < 0.3:
                rng.shuffle(d)
                d = sorted(d[:rng.randint(1, k)]) if rng.random() < 0.7 else d[:rng.randint(1, k)]
            domains.append(d)
        root = random_tree(rng, plain, domains, rng.randint(0, 4), mb, 12)
        base = dict(scale_bits=0, unary=plain["unary"], pair=plain["pair"], message_bits=message_bits, domains=domains, lower_bound=0, root=root)
        proves = ours.check_plain(base)["proves"]
        truth = ours.brute_force_min_box(base)
        stats["structure_valid"] += proves is not None
        if proves is not None and proves > truth:
            stats["unsound_format"] += 1
            stats["examples"].append(dict(kind="format proves more than the minimum", case=json.dumps(_jsonable(base))[:2000]))
        for delta in ((-3, -1, 0, 1, 2) if proves is not None else (None,)):
            L = (proves + delta) if proves is not None else truth - 5
            mine = ours.check_plain(dict(base, lower_bound=L))
            cert = MinCertificate(model=sb_model(SB, plain), message_bits=message_bits, domains=copy.deepcopy(domains), lower_bound=L,
                                  witness=None, root=copy.deepcopy(root))
            res = SB["mincheck"].check_min_certificate(cert)
            stats["cases"] += 1
            stats["sb_accept" if res.accepted else "sb_reject"] += 1
            if delta == 0 and res.accepted:
                stats["exact_at_bound"] += 1
            if res.accepted != mine["accepted"]:
                stats["disagree_ours"] += 1
                if len(stats["examples"]) < 10:
                    stats["examples"].append(dict(kind="their checker and ours disagree", theirs=res.reason, ours=mine["reason"], L=L, proves=proves,
                                                  case=json.dumps(_jsonable(base))[:2000]))
            if res.accepted and L > truth:
                stats["unsound_sb"] += 1
                stats["examples"].append(dict(kind="UNSOUND ACCEPTANCE", L=L, truth=truth, case=json.dumps(_jsonable(base))[:2000]))
            try:
                doc = SB["mincert"].to_metricchain_cert1(cert)
            except SB["mincert"].MalformedCertificate:
                stats["conversion_malformed"] += 1
                continue
            verdict = SB["ref"].check_text(json.dumps(doc))
            stats["reference_checked"] += 1
            if bool(verdict["accepted"]) != res.accepted:
                stats["disagree_reference"] += 1
                if len(stats["examples"]) < 10:
                    stats["examples"].append(dict(kind="their checker and the reference checker (after their conversion) disagree", theirs=res.reason,
                                                  reference=str(verdict)[:300], L=L, proves=proves, case=json.dumps(_jsonable(base))[:2000]))
    return stats


def _jsonable(c: dict) -> dict:
    def node(d):
        if not isinstance(d, dict):
            return d
        out = dict(d)
        if "m" in out:
            out["m"] = {f"{k[0]},{k[1]}": v for k, v in out["m"].items()}
        if "children" in out:
            out["children"] = {str(a): node(ch) for a, ch in out["children"].items()}
        if "rest" in out:
            out["rest"] = node(out["rest"])
        return out
    return dict(c, pair={f"{k[0]},{k[1]}": v for k, v in c["pair"].items()}, root=node(c["root"]))


# ------------------------------------------------------------------ part B: traps

def part_b(SB) -> list:
    MinCertificate = SB["mincert"].MinCertificate
    PairModel = SB["model"].PairModel
    check = SB["mincheck"].check_min_certificate
    out = []

    def case(name, model, domains, L, root, truth_min, expect_accept, message_bits=0):
        cert = MinCertificate(model=model, message_bits=message_bits, domains=domains, lower_bound=L, witness=None, root=root)
        r = check(cert)
        try:
            ref = bool(SB["ref"].check_text(json.dumps(SB["mincert"].to_metricchain_cert1(cert)))["accepted"])
        except Exception as exc:  # noqa: BLE001
            ref = f"conversion raised {type(exc).__name__}"
        mine = ours.check_plain(ours.plain_from_object(cert))
        out.append(dict(name=name, accepted=r.accepted, reason=r.reason, reference=ref, ours=mine["accepted"], expected=expect_accept,
                        claim=L, true_minimum=truth_min, unsound=bool(r.accepted and L > truth_min),
                        as_expected=(r.accepted == expect_accept)))

    # one site, two states, energies 5 and 7: min 5
    m1 = PairModel(unary=[np.array([5, 7])], pair={})
    leaf = {"node": "leaf", "m": {}}
    case("a state removed with itself as dominator, then a bound that needs it gone", m1, [[0, 1]], 7,
         {"node": "prune", "site": 0, "remove": 0, "dominator": 0, "rest": leaf}, 5, False)
    case("the low state removed by the high one (dominance false)", m1, [[0, 1]], 7,
         {"node": "prune", "site": 0, "remove": 0, "dominator": 1, "rest": leaf}, 5, False)
    case("the high state removed by the low one, bound 5", m1, [[0, 1]], 5,
         {"node": "prune", "site": 0, "remove": 1, "dominator": 0, "rest": leaf}, 5, True)
    # the dominator is outside the box: on the box {1, 2} the minimum is 7, state 0 (energy 5) is not in the box
    m2 = PairModel(unary=[np.array([5, 7, 9])], pair={})
    case("dominator outside the root box", m2, [[1, 2]], 9,
         {"node": "prune", "site": 0, "remove": 1, "dominator": 0, "rest": leaf}, 7, False)
    case("the box {1, 2}: bound 7 with a legitimate prune of 2 by 1", m2, [[1, 2]], 7,
         {"node": "prune", "site": 0, "remove": 2, "dominator": 1, "rest": leaf}, 7, True)
    case("a dominator that an earlier prune removed", m2, [[0, 1, 2]], 9,
         {"node": "prune", "site": 0, "remove": 0, "dominator": 0,
          "rest": {"node": "prune", "site": 0, "remove": 1, "dominator": 0, "rest": leaf}}, 5, False)
    case("prune of a state that is not in the box (a no-op), then the true bound", m2, [[1, 2]], 7,
         {"node": "prune", "site": 0, "remove": 0, "dominator": 1, "rest": leaf}, 7, False)   # dominance of 0 by 1 is false: rejected
    # two sites; a branch that omits a state
    m3 = PairModel(unary=[np.array([0, 0]), np.array([0, 0])], pair={(0, 1): np.array([[1, 5], [5, -4]])})
    case("a branch without the child that holds the minimum", m3, [[0, 1], [0, 1]], 1,
         {"node": "branch", "site": 0, "children": {0: leaf}}, -4, False)
    case("a complete branch, bound -4", m3, [[0, 1], [0, 1]], -4,
         {"node": "branch", "site": 0, "children": {0: leaf, 1: leaf}}, -4, True)
    case("a branch with a surplus child for a state outside the box", m3, [[0], [0, 1]], 1,
         {"node": "branch", "site": 0, "children": {0: leaf, 1: {"node": "prune", "site": 0, "remove": 1, "dominator": 1, "rest": leaf}}}, 1, True)
    case("a second branch on a site already fixed", m3, [[0, 1], [0, 1]], -4,
         {"node": "branch", "site": 0, "children": {0: {"node": "branch", "site": 0, "children": {0: leaf}},
                                                    1: {"node": "branch", "site": 0, "children": {1: leaf}}}}, -4, True)
    # messages: a correct reparameterisation proves -4 without branching; shifted by one unit it must fail
    case("one leaf with messages, bound -4", m3, [[0, 1], [0, 1]], -4,
         {"node": "leaf", "m": {(0, 1): [1, -4], (1, 0): [0, 0]}}, -4, True)
    case("the same leaf, claim -3", m3, [[0, 1], [0, 1]], -3,
         {"node": "leaf", "m": {(0, 1): [1, -4], (1, 0): [0, 0]}}, -4, False)
    case("a message for a pair that the model does not list", PairModel(unary=[np.array([0, 0]), np.array([0, 0]), np.array([0])], pair={(0, 1): np.array([[1, 5], [5, -4]])}),
         [[0, 1], [0, 1], [0]], -4, {"node": "leaf", "m": {(0, 2): [9, 9]}}, -4, False)
    case("message_bits 3: the claim in finer units, exact", m3, [[0, 1], [0, 1]], -32,
         {"node": "leaf", "m": {(0, 1): [8, -32], (1, 0): [0, 0]}}, -32, True, message_bits=3)
    case("message_bits 3: one fine unit above", m3, [[0, 1], [0, 1]], -31,
         {"node": "leaf", "m": {(0, 1): [8, -32], (1, 0): [0, 0]}}, -32, False, message_bits=3)
    # objects that are not of the format
    for name, kw in (("lower_bound a float", dict(L=1.0)), ("lower_bound True", dict(L=True)), ("domains with a repeated state", dict(domains=[[0, 0], [0, 1]])),
                     ("an empty domain", dict(domains=[[], [0, 1]])), ("message_bits -1", dict(message_bits=-1))):
        cert = MinCertificate(model=m3, message_bits=kw.get("message_bits", 0), domains=kw.get("domains", [[0, 1], [0, 1]]),
                              lower_bound=kw.get("L", -4), witness=None, root={"node": "branch", "site": 0, "children": {0: leaf, 1: leaf}})
        r = check(cert)
        out.append(dict(name=name, accepted=r.accepted, reason=r.reason, expected=False, as_expected=not r.accepted, unsound=False))
    return out


# ------------------------------------------------------------------ part C: limits of the arithmetic

def part_c(SB) -> list:
    MinCertificate = SB["mincert"].MinCertificate
    PairModel = SB["model"].PairModel
    check = SB["mincheck"].check_min_certificate
    out = []
    big = 2 ** 50 - 1
    for deg, expect_supported in ((4092, True), (4093, False)):
        # a hub with two states and `deg` leaves with one state each.  The hub's messages are all -(2^50 - 1), so its
        # site term is 3 - deg (2^50 - 1), next to -2^62 (the largest sum the checker allows itself in int64); every
        # pair term gives +(2^50 - 1) back, so the bound proved is the small number 3 = the true minimum.
        unary = [np.array([3, 7], dtype=object)] + [np.array([0], dtype=object) for _ in range(deg)]
        pair = {(0, j): np.array([[0], [0]], dtype=object) for j in range(1, deg + 1)}
        model = PairModel(unary=unary, pair=pair)
        m = {(0, j): [-big, -big] for j in range(1, deg + 1)}
        plain = dict(scale_bits=0, unary=[[3, 7]] + [[0]] * deg, pair={k: [[0], [0]] for k in pair}, message_bits=0,
                     domains=[[0, 1]] + [[0]] * deg, lower_bound=0, root={"node": "leaf", "m": m})
        proves = ours.check_plain(plain)["proves"]
        row = dict(degree=deg, hub_site_sum_bits=(deg * big).bit_length(), ours_proves=proves, true_minimum=3, supported_expected=expect_supported)
        for delta in (0, 1):
            cert = MinCertificate(model=model, message_bits=0, domains=[[0, 1]] + [[0]] * deg, lower_bound=proves + delta, witness=None,
                                  root={"node": "leaf", "m": copy.deepcopy(m)})
            r = check(cert)
            row[f"claim_proves_plus_{delta}"] = dict(accepted=r.accepted, reason=r.reason)
        out.append(row)
    # the claimed bound itself next to 2^62 (a model whose minimum is that large: 4097 sites with one state of energy 2^50 - 1)
    nbig = 4097
    model = PairModel(unary=[np.array([big], dtype=object) for _ in range(nbig)], pair={})
    for L in (nbig * big, 2 ** 62 - 1, 2 ** 62):
        r = check(MinCertificate(model=model, message_bits=0, domains=[[0]] * nbig, lower_bound=L, witness=None, root={"node": "leaf", "m": {}}))
        out.append(dict(claim_bits=L.bit_length(), claim_is_true=L <= nbig * big, accepted=r.accepted, reason=r.reason))
    # entries at the limit itself
    for entry, mbits in ((2 ** 50, 0), (2 ** 50 - 1, 0), (2 ** 40, 10), (2 ** 40 - 1, 10)):
        model = PairModel(unary=[np.array([entry, 0], dtype=object)], pair={})
        r = check(MinCertificate(model=model, message_bits=mbits, domains=[[0, 1]], lower_bound=0, witness=None, root={"node": "leaf", "m": {}}))
        out.append(dict(entry_bits=entry.bit_length(), entry_is_power=entry == 2 ** (entry.bit_length() - 1), message_bits=mbits, accepted=r.accepted, reason=r.reason))
    # an all-zero model with a huge message_bits: the magnitude test passes (0 * 2^k = 0); what happens then?
    for mbits in (62, 63, 64, 200, 100_000):
        model = PairModel(unary=[np.array([0, 0])], pair={})
        t0 = time.time()
        r = check(MinCertificate(model=model, message_bits=mbits, domains=[[0, 1]], lower_bound=0, witness=None, root={"node": "leaf", "m": {}}))
        out.append(dict(all_zero_model=True, message_bits=mbits, accepted=r.accepted, reason=r.reason, seconds=round(time.time() - t0, 3)))
    return out


# ------------------------------------------------------------------ part D: malformed JSON

def part_d(SB) -> list:
    mincert, check = SB["mincert"], SB["mincheck"].check_min_certificate
    PairModel = SB["model"].PairModel
    model = PairModel(unary=[np.array([5, 7]), np.array([0, 3])], pair={(0, 1): np.array([[0, 2], [1, 0]])})
    good = mincert.MinCertificate(model=model, message_bits=0, domains=[[0, 1], [0, 1]], lower_bound=5, witness=(0, 0),
                                  root={"node": "branch", "site": 0, "children": {0: {"node": "leaf", "m": {}}, 1: {"node": "leaf", "m": {}}}})
    text = mincert.dumps(good)
    assert check(mincert.loads(text)).accepted and ours.check_plain(ours.strict_loads(text))["accepted"]
    doc = json.loads(text)
    out = []

    def run(name, new_text, literal_claim_true, silent=None):
        row = dict(name=name, literal_claim_is_true=literal_claim_true, silent=silent)
        try:
            cert = mincert.loads(new_text)
            r = check(cert)
            row.update(their_loader="loaded", their_verdict=r.accepted, checked_claim=str(r.lower_bound) if r.accepted else None,
                       checked_model_unary=[[int(v) for v in u.tolist()] for u in cert.model.unary], checked_lower_bound=int(cert.lower_bound))
        except Exception as exc:  # noqa: BLE001
            row.update(their_loader=f"raises {type(exc).__name__}", their_verdict=None)
        try:
            row["ours"] = "accepted" if ours.check_plain(ours.strict_loads(new_text))["accepted"] else "rejected"
        except ours.Malformed as exc:
            row["ours"] = f"malformed: {exc}"
        out.append(row)

    def edit(fn):
        d = copy.deepcopy(doc)
        fn(d)
        return json.dumps(d, separators=(",", ":"))

    run("the unchanged document", text, True)
    # duplicate keys: the standard library keeps the last one
    run("two `lower_bound` keys: 6 (false), then 5 (true)", text.replace('"lower_bound":5', '"lower_bound":6,"lower_bound":5'), None, "the first value is dropped")
    run("two `lower_bound` keys: 5 (true), then 6 (false)", text.replace('"lower_bound":5', '"lower_bound":5,"lower_bound":6'), None, "the first value is dropped")
    run("two `unary` keys: other tables first, the original last", text.replace('"unary":[[5,7],[0,3]]', '"unary":[[9,9],[9,9]],"unary":[[5,7],[0,3]]'), None, "the first tables are dropped")
    run("two `unary` keys: the original first, `[[9,9],[9,9]]` last", text.replace('"unary":[[5,7],[0,3]]', '"unary":[[5,7],[0,3]],"unary":[[9,9],[9,9]]'), None,
        "the first tables are dropped; the model checked is the second")
    # numbers that are not integers
    run("`lower_bound` 5.9 (the minimum is 5)", edit(lambda d: d["claim"].__setitem__("lower_bound", 5.9)), False, "5.9 read as 5")
    run("`lower_bound` 5.0", edit(lambda d: d["claim"].__setitem__("lower_bound", 5.0)), None, "5.0 read as 5")
    run("a table entry 5.9 in place of 5", edit(lambda d: d["model"]["unary"][0].__setitem__(0, 5.9)), None, "5.9 read as 5")
    run("a table entry given as the string \"5\"", edit(lambda d: d["model"]["unary"][0].__setitem__(0, "5")), None, "the string read as 5")
    run("a table entry `true` in place of 5", edit(lambda d: d["model"]["unary"][0].__setitem__(0, True)), None, "`true` read as 1")
    run("`lower_bound` given as the string \"5\"", edit(lambda d: d["claim"].__setitem__("lower_bound", "5")), None, "the string read as 5")
    run("`lower_bound` NaN", text.replace('"lower_bound":5', '"lower_bound":NaN'), None)
    run("`lower_bound` -Infinity", text.replace('"lower_bound":5', '"lower_bound":-Infinity'), None)
    # keys
    run("pair key \"0, 1\" (with a space)", text.replace('"0,1":', '"0, 1":'), None, "read as the pair (0, 1)")
    run("two tables for one pair, keys \"0,1\" and \"0, 1\" (the second all zeros)", text.replace('"pair":{"0,1":[[0,2],[1,0]]}', '"pair":{"0,1":[[0,2],[1,0]],"0, 1":[[0,0],[0,0]]}'), None,
        "the second table replaces the first")
    run("child keys \"00\" and \"0\" for one state", text.replace('"children":{"0":', '"children":{"00":{"node":"leaf","m":{}},"0":'), None, "the later key replaces the earlier")
    # the checksum and unknown fields
    run("`model_sha256` replaced by zeros", edit(lambda d: d.__setitem__("model_sha256", "0" * 64)), None, "the checksum is not compared")
    run("a table entry changed (5 to 4) without changing `model_sha256`; the claim 5 is then false", edit(lambda d: d["model"]["unary"][0].__setitem__(0, 4)), False,
        "the checksum is not compared")
    run("an unknown top-level field", edit(lambda d: d.__setitem__("note", "x")), None, "ignored")
    run("format `structbio-mincert/2`", edit(lambda d: d.__setitem__("format", "structbio-mincert/2")), None)
    run("a truncated document", text[:len(text) // 2], None)
    run("the certificate replaced by a list", edit(lambda d: d.__setitem__("certificate", [])), None)
    return out


# ------------------------------------------------------------------ part E: the producer

def part_e(SB, seed: int, quick: bool) -> dict:
    rng = random.Random(seed)
    certify, Budget = SB["gmec"].certify_gmec, SB["gmec"].CertificationBudgetExceeded
    check = SB["mincheck"].check_min_certificate
    res = dict(random=dict(instances=0, wrong_optimum=0, rejected=0, gap_nonzero=0, raised={}, ours_disagrees=0, reference_disagrees=0),
               tolerance=dict(instances=0, bad=0), degenerate=[], trees=[], dense=[], magnitude=[], abstention=[], examples=[])

    def run(plain, scale_bits=0, eps=Fraction(0), **kw):
        model = sb_model(SB, plain, scale_bits)
        t0 = time.time()
        cert = certify(model, eps=eps, **kw)
        dt = time.time() - t0
        r = check(cert)
        return model, cert, r, dt

    # (1) random small instances against enumeration, including sites with one state and sparse graphs
    for _ in range(150 if quick else 1500):
        n = rng.randint(1, 8)
        plain = random_plain_model(rng, n, rng.randint(1, 4), rng.choice([0.0, 0.3, 0.7, 1.0]), rng.choice([1, 3, 12, 1000]))
        sb = rng.choice([0, 0, 3, 8])
        truth = enum_min(plain)
        R = res["random"]
        R["instances"] += 1
        try:
            model, cert, r, _ = run(plain, sb, message_bits=rng.choice([0, 4, 12]))
        except Exception as exc:  # noqa: BLE001
            R["raised"][type(exc).__name__] = R["raised"].get(type(exc).__name__, 0) + 1
            if len(res["examples"]) < 6:
                res["examples"].append(dict(kind=f"producer raised {type(exc).__name__}: {exc}", plain=json.dumps(dict(unary=plain["unary"], pair={f'{k[0]},{k[1]}': v for k, v in plain["pair"].items()}))[:1500]))
            continue
        if not r.accepted:
            R["rejected"] += 1
            continue
        if r.lower_bound != Fraction(truth, 2 ** sb) or r.witness_energy != r.lower_bound:
            R["wrong_optimum"] += 1
        if r.certified_gap != 0:
            R["gap_nonzero"] += 1
        if not ours.check_plain(ours.plain_from_object(cert))["accepted"]:
            R["ours_disagrees"] += 1
        if not SB["ref"].check_text(json.dumps(SB["mincert"].to_metricchain_cert1(cert)))["accepted"]:
            R["reference_disagrees"] += 1
    # (2) a tolerance
    for _ in range(40 if quick else 300):
        plain = random_plain_model(rng, rng.randint(2, 7), rng.randint(2, 4), 0.8, 12)
        sb = rng.choice([0, 3])
        eps = Fraction(rng.choice([1, 2, 5]), rng.choice([1, 2, 8]))
        truth = Fraction(enum_min(plain), 2 ** sb)
        model, cert, r, _ = run(plain, sb, eps=eps)
        res["tolerance"]["instances"] += 1
        if not (r.accepted and r.lower_bound <= truth <= r.witness_energy and r.certified_gap <= eps):
            res["tolerance"]["bad"] += 1
    # (3) degenerate instances
    deg = {
        "one site, one state": dict(unary=[[4]], pair={}),
        "one site, three equal states": dict(unary=[[2, 2, 2]], pair={}),
        "five sites, no pair": dict(unary=[[rng.randint(-5, 5) for _ in range(3)] for _ in range(5)], pair={}),
        "all tables zero": dict(unary=[[0, 0, 0] for _ in range(5)], pair={(i, j): [[0] * 3 for _ in range(3)] for i in range(5) for j in range(i + 1, 5)}),
        "every site has one state": dict(unary=[[rng.randint(-5, 5)] for _ in range(6)], pair={(i, i + 1): [[rng.randint(-5, 5)]] for i in range(5)}),
        "two components": dict(unary=[[0, 1], [1, 0], [0, 2], [2, 0]], pair={(0, 1): [[3, 0], [0, 3]], (2, 3): [[0, 4], [4, 0]]}),
        "entries in {0, 1}, many ties": dict(unary=[[rng.randint(0, 1) for _ in range(3)] for _ in range(7)],
                                              pair={(i, j): [[rng.randint(0, 1) for _ in range(3)] for _ in range(3)] for i in range(7) for j in range(i + 1, 7)}),
        "antiferromagnetic triangle (frustrated)": dict(unary=[[0, 0]] * 3, pair={(i, j): [[1, 0], [0, 1]] for i in range(3) for j in range(i + 1, 3)}),
    }
    for name, plain in deg.items():
        row = dict(name=name, truth=enum_min(plain))
        try:
            model, cert, r, dt = run(plain)
            row.update(accepted=r.accepted, lower_bound=str(r.lower_bound), gap=str(r.certified_gap), nodes=cert.meta.get("bnb_nodes"), seconds=round(dt, 4),
                       correct=bool(r.accepted and r.lower_bound == row["truth"] and r.certified_gap == 0))
        except Exception as exc:  # noqa: BLE001
            row.update(raised=f"{type(exc).__name__}: {exc}", correct=False)
        res["degenerate"].append(row)
    # (4) trees against dynamic programming, with timings
    for n, k in ((50, 6), (100, 6), (200, 6)) if quick else ((50, 6), (100, 6), (200, 6), (400, 6), (200, 20), (100, 40)):
        parent = [-1] + [rng.randrange(i) for i in range(1, n)]
        unary = [[rng.randint(-50, 50) for _ in range(k)] for _ in range(n)]
        pair = {(parent[i], i): [[rng.randint(-50, 50) for _ in range(k)] for _ in range(k)] for i in range(1, n)}
        plain = dict(unary=unary, pair=pair)
        truth = tree_dp_min(plain, parent)
        row = dict(sites=n, states=k, truth=truth)
        try:
            model, cert, r, dt = run(plain, time_limit=300.0)
            row.update(accepted=r.accepted, correct=bool(r.accepted and r.lower_bound == truth and r.certified_gap == 0), seconds=round(dt, 3),
                       nodes=cert.meta.get("bnb_nodes"), stats=r.stats, bytes=len(SB["mincert"].dumps(cert)))
            t0 = time.time()
            check(cert)
            row["check_seconds"] = round(time.time() - t0, 4)
            t0 = time.time()
            row["ours_accepts"] = ours.check_plain(ours.plain_from_object(cert))["accepted"]
            row["ours_check_seconds"] = round(time.time() - t0, 4)
        except Budget as exc:
            row.update(abstained=str(exc))
        except Exception as exc:  # noqa: BLE001
            row.update(raised=f"{type(exc).__name__}: {exc}")
        res["trees"].append(row)
    # (5) dense frustrated instances against enumeration, with a time limit
    for n, k, reps in ((10, 3, 6), (12, 3, 6)) if quick else ((10, 3, 12), (12, 3, 12), (14, 3, 8), (11, 4, 8)):
        for _ in range(reps):
            plain = random_plain_model(rng, n, k, 1.0, 100, kmin=k)
            truth = enum_min(plain)
            row = dict(sites=n, states=k, truth=truth)
            try:
                model, cert, r, dt = run(plain, time_limit=60.0, max_nodes=2_000_000)
                row.update(accepted=r.accepted, correct=bool(r.accepted and r.lower_bound == truth and r.certified_gap == 0), seconds=round(dt, 3),
                           nodes=cert.meta.get("bnb_nodes"), stats=r.stats, bytes=len(SB["mincert"].dumps(cert)))
            except Budget as exc:
                row.update(abstained=str(exc))
            except Exception as exc:  # noqa: BLE001
                row.update(raised=f"{type(exc).__name__}: {exc}")
            res["dense"].append(row)
    # (6) magnitudes next to the supported range: does the producer emit what its own checker accepts?
    for bits, mbits in ((48, 0), (49, 0), (37, 12), (30, 12), (20, 12)):
        ok = bad = raised = 0
        notes = {}
        for _ in range(10 if quick else 40):
            n = rng.randint(3, 6)
            amp = 2 ** bits
            plain = random_plain_model(rng, n, 3, 1.0, amp, kmin=2)
            truth = enum_min_big(plain)
            try:
                model, cert, r, _ = run(plain, message_bits=mbits, time_limit=30.0)
                if r.accepted and r.lower_bound == truth and r.certified_gap == 0:
                    ok += 1
                else:
                    bad += 1
                    notes[r.reason] = notes.get(r.reason, 0) + 1
            except Exception as exc:  # noqa: BLE001
                raised += 1
                notes[type(exc).__name__] = notes.get(type(exc).__name__, 0) + 1
        res["magnitude"].append(dict(entry_bits=bits, message_bits=mbits, exact_and_accepted=ok, not_accepted_or_not_exact=bad, raised=raised, notes=notes))
    # (7) the abstention path
    plain = random_plain_model(rng, 12, 3, 1.0, 100, kmin=3)
    for kw in (dict(max_nodes=1), dict(time_limit=0.0)):
        try:
            run(plain, **kw)
            res["abstention"].append(dict(kw=str(kw), outcome="a certificate was returned"))
        except Budget as exc:
            res["abstention"].append(dict(kw=str(kw), outcome=f"abstained: {exc}"))
        except Exception as exc:  # noqa: BLE001
            res["abstention"].append(dict(kw=str(kw), outcome=f"raised {type(exc).__name__}: {exc}"))
    return res


PART_F = r"""
import json, random, sys
sys.path.insert(0, sys.argv[1] + "/src")
import numpy as np
from metricchain_sb.model import PairModel
from metricchain_sb.gmec import certify_gmec
from metricchain_sb.mincheck import check_min_certificate
from metricchain_sb import mincert
out = dict(recursion_limit=sys.getrecursionlimit(), produced=[], loaded=[])
rng = random.Random(3)
for n, k in ((20, 20), (30, 30), (40, 30), (60, 30)):
    # a chain in which one state per site is clearly best: dead-end elimination removes nearly every other state
    unary = [np.array([0] + [rng.randint(50, 90) for _ in range(k - 1)]) for _ in range(n)]
    pair = {(i, i + 1): np.array([[rng.randint(-3, 3) for _ in range(k)] for _ in range(k)]) for i in range(n - 1)}
    cert = certify_gmec(PairModel(unary=unary, pair=pair))
    counts = mincert.count_nodes(cert.root)
    row = dict(sites=n, states=k, accepted_in_memory=check_min_certificate(cert).accepted, prune=counts["prune"], depth=counts["depth"])
    for name, fn in (("dumps", lambda: mincert.dumps(cert)), ("to_metricchain_cert1", lambda: mincert.to_metricchain_cert1(cert))):
        try:
            fn()
            row[name] = "ok"
        except RecursionError:
            row[name] = "RecursionError"
    out["produced"].append(row)
m = PairModel(unary=[np.array([5, 7])], pair={})
text0 = mincert.dumps(mincert.MinCertificate(model=m, message_bits=0, domains=[[0, 1]], lower_bound=5, witness=None, root={"node": "leaf", "m": {}}))
leaf = '{"node":"leaf","m":{}}'
for d in (400, 900, 1200, 5000):
    t = leaf
    for _ in range(d):
        t = '{"node":"prune","site":0,"remove":1,"dominator":0,"rest":' + t + '}'
    try:
        c = mincert.loads(text0.replace('"certificate":' + leaf, '"certificate":' + t))
        out["loaded"].append(dict(depth=d, loads="ok", accepted=check_min_certificate(c).accepted))
    except RecursionError:
        out["loaded"].append(dict(depth=d, loads="RecursionError"))
print(json.dumps(out))
"""


def part_f(sb_root: Path) -> dict:
    """Nesting depth, in a fresh interpreter (the theory division's reference checker raises the recursion limit when
    it is imported, which would hide the effect)."""
    import subprocess
    r = subprocess.run([sys.executable, "-B", "-c", PART_F, str(sb_root)], capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        return dict(error=r.stderr[-800:])
    return json.loads(r.stdout.strip().splitlines()[-1])


def enum_min_big(plain: dict) -> int:
    """Enumeration in Python integers (for tables beyond int64 sums)."""
    unary, pair = plain["unary"], plain["pair"]
    best = None
    for x in itertools.product(*[range(len(u)) for u in unary]):
        e = sum(unary[i][a] for i, a in enumerate(x)) + sum(t[x[i]][x[j]] for (i, j), t in pair.items())
        best = e if best is None or e < best else best
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sb", type=Path, required=True, help="a read-only checkout of the reviewed commit")
    ap.add_argument("--part", default="all")
    ap.add_argument("--cases", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20261126)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    SB = load_sb(args.sb.expanduser())
    OUT.mkdir(exist_ok=True)
    parts = "abcdef" if args.part == "all" else args.part
    for p in parts:
        t0 = time.time()
        if p == "a":
            r = part_a(SB, args.cases, args.seed)
        elif p == "b":
            r = part_b(SB)
        elif p == "c":
            r = part_c(SB)
        elif p == "d":
            r = part_d(SB)
        elif p == "f":
            r = part_f(args.sb.expanduser())
        else:
            r = part_e(SB, args.seed, args.quick)
        (OUT / f"mincert_part_{p}.json").write_text(json.dumps(dict(seconds=round(time.time() - t0, 1), seed=args.seed, result=r), indent=1, default=str))
        print(f"part {p}: {time.time() - t0:.0f} s", flush=True)
        if p == "a":
            print("  ", {k: v for k, v in r.items() if k != "examples"}, flush=True)
            for ex in r["examples"][:3]:
                print("   example:", json.dumps(ex)[:600], flush=True)
        elif p in "bd":
            for row in r:
                print("  ", json.dumps(row, default=str)[:330], flush=True)
        elif p == "c":
            for row in r:
                print("  ", json.dumps(row, default=str)[:300], flush=True)
        elif p == "f":
            print("  ", json.dumps(r)[:1500], flush=True)
        else:
            for k, v in r.items():
                print("  ", k, json.dumps(v, default=str)[:900], flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
