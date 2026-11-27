"""Adversarial review STRUCTBIO-REV-0001 — `mincheck.check_min_certificate` on in-memory certificates.

Tests whose docstring starts with ``FINDING`` demonstrate a defect and FAIL with the reviewed
code; they are left red on purpose.  Tests whose docstring starts with ``SURVIVED`` document
attacks that the checker withstood and pass (regression tests).

Nothing here comes from the producer (`gmec`): certificates are hand-built or random.  Ground
truth is exhaustive enumeration in Python integers; a second, independent reading of the
certificate semantics (`_Oracle`) predicts the verdict; the theory division's reference checker
judges the converted document.
"""
import contextlib
import itertools
import json
import random
import signal
import sys
import threading
import tracemalloc
import warnings
from fractions import Fraction

import numpy as np
import pytest

from metricchain_sb import mincert
from metricchain_sb.mincert import MalformedCertificate, MinCertificate, to_metricchain_cert1
from metricchain_sb.mincheck import check_min_certificate
from metricchain_sb.model import PairModel, brute_force_min


# ----------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------

class _Deadline(BaseException):
    """Raised by the alarm; a BaseException so that the checkers' `except Exception` cannot swallow it."""


@contextlib.contextmanager
def _deadline(seconds):
    if threading.current_thread() is not threading.main_thread() or not hasattr(signal, "setitimer"):
        pytest.skip("needs SIGALRM in the main thread")

    def handler(signum, frame):
        raise _Deadline()

    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


def _peak_megabytes(fn):
    tracemalloc.start()
    try:
        out = fn()
        peak = tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()
    return out, peak / 1e6


def _small_model():
    return PairModel(unary=[np.array([0, 1]), np.array([0, 2])], pair={(0, 1): np.array([[0, 1], [1, 0]])},
                     scale_bits=0)


def _cert(model=None, **fields):
    model = _small_model() if model is None else model
    base = dict(model=model, message_bits=0, domains=model.full_domains(), lower_bound=0, witness=None,
                root={"node": "leaf", "m": {}})
    base.update(fields)
    return MinCertificate(**base)


class _Oracle:
    """Independent reading of the certificate semantics (`mincert` module docstring), Python integers only."""

    def __init__(self, model, mb):
        self.n = model.n
        self.H = [[int(v) * mb for v in u.tolist()] for u in model.unary]
        self.J = {k: [[int(v) * mb for v in row] for row in t.tolist()] for k, t in model.pair.items()}
        self.nb = {i: [] for i in range(self.n)}
        for (i, j) in self.J:
            self.nb[i].append(j)
            self.nb[j].append(i)

    def pair(self, i, j, a, b):
        return self.J[(i, j)][a][b] if i < j else self.J[(j, i)][b][a]

    def margin(self, D, i, r, t):
        return self.H[i][r] - self.H[i][t] + sum(
            min(self.pair(i, j, r, s) - self.pair(i, j, t, s) for s in D[j]) for j in self.nb[i])

    def leaf(self, D, m):
        b = 0
        for i in range(self.n):
            b += min(self.H[i][a] + sum(m[(i, j)][a] for j in self.nb[i] if (i, j) in m) for a in D[i])
        for (i, j) in self.J:
            b += min(self.J[(i, j)][a][c] - (m[(i, j)][a] if (i, j) in m else 0) - (m[(j, i)][c] if (j, i) in m else 0)
                     for a in D[i] for c in D[j])
        return b

    def bound(self, node, D):
        """Least leaf bound over the part of the tree a checker visits; None if a visited node is invalid."""
        kind = node["node"]
        if kind == "leaf":
            return self.leaf(D, node.get("m", {}))
        if kind == "branch":
            i, best = node["site"], None
            for a in D[i]:
                if a not in node["children"]:
                    return None
                D2 = list(D)
                D2[i] = [a]
                b = self.bound(node["children"][a], D2)
                if b is None:
                    return None
                best = b if best is None else min(best, b)
            return best
        i, r, t = node["site"], node["remove"], node["dominator"]
        if t == r or t not in D[i] or self.margin(D, i, r, t) < 0:
            return None
        D2 = list(D)
        D2[i] = [s for s in D[i] if s != r]
        return self.bound(node["rest"], D2)


def _random_model(rng):
    n = rng.randint(1, 5)
    sizes = [rng.randint(1, 4) for _ in range(n)]
    amp = rng.choice([2, 6, 12, 1000])
    unary = [np.array([rng.randint(-amp, amp) + rng.choice([0, 0, amp, 3 * amp]) for _ in range(k)]) for k in sizes]
    pair = {}
    density = rng.choice([0.3, 0.7, 1.0])
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < density:
                pair[(i, j)] = np.array([[rng.randint(-amp, amp) for _ in range(sizes[j])] for _ in range(sizes[i])])
    return PairModel(unary=unary, pair=pair, scale_bits=rng.choice([0, 0, 3]))


class _TreeGenerator:
    """Random certificate trees: random messages; prunes that are valid, almost valid (margin -1..-3
    units), of states outside the domain, repeated, or with a dominator already removed; branches with
    missing and with extra children."""

    def __init__(self, rng, model, mb, oracle):
        self.rng, self.model, self.mb, self.oracle, self.count = rng, model, mb, oracle, 0

    def messages(self):
        rng, model = self.rng, self.model
        if rng.random() < 0.25:
            return {}
        amp = rng.choice([1, 3, 20, 2000]) * self.mb
        m = {}
        for (i, j) in model.pair:
            for (a, b) in ((i, j), (j, i)):
                if rng.random() < 0.7:
                    m[(a, b)] = [rng.randint(-amp, amp) for _ in range(model.sizes[a])]
        return m

    def node(self, D, depth):
        rng, model = self.rng, self.model
        n, sizes = model.n, model.sizes
        self.count += 1
        r = rng.random()
        if depth >= 5 or self.count > 60 or r < 0.3:
            return {"node": "leaf", "m": self.messages()}
        if r < 0.6:
            i = rng.randrange(n)
            children = {}
            for a in D[i]:
                if rng.random() < 0.04:
                    continue                                    # a missing child
                D2 = list(D)
                D2[i] = [a]
                children[a] = self.node(D2, depth + 1)
            if rng.random() < 0.15:
                a = rng.randrange(sizes[i])                     # possibly an extra child
                if a not in children:
                    D2 = list(D)
                    D2[i] = [a]
                    children[a] = self.node(D2, depth + 1)
            return {"node": "branch", "site": i, "children": children}
        candidates = [(i, r_, t) for i in range(n) for r_ in range(sizes[i]) for t in D[i] if t != r_]
        valid = [c for c in candidates if self.oracle.margin(D, *c) >= 0]
        almost = [c for c in candidates if -3 * self.mb <= self.oracle.margin(D, *c) < 0]
        q = rng.random()
        if valid and q < 0.7:
            i, r_, t = rng.choice(valid)
        elif almost and q < 0.85:
            i, r_, t = rng.choice(almost)
        else:
            i = rng.randrange(n)
            r_, t = rng.randrange(sizes[i]), rng.randrange(sizes[i])
        D2 = list(D)
        D2[i] = [s for s in D[i] if s != r_] or list(D[i])
        return {"node": "prune", "site": i, "remove": r_, "dominator": t, "rest": self.node(D2, depth + 1)}


def _random_certificate(seed):
    rng = random.Random(seed)
    model = _random_model(rng)
    sizes = model.sizes
    message_bits = rng.choice([0, 0, 1, 4])
    mb = 2 ** message_bits
    domains = [list(range(k)) if rng.random() < 0.6 else rng.sample(range(k), rng.randint(1, k)) for k in sizes]
    oracle = _Oracle(model, mb)
    root = _TreeGenerator(rng, model, mb, oracle).node(domains, 0)
    bound = oracle.bound(root, domains)
    emin, _ = brute_force_min(model, domains)
    lower = emin * mb + rng.choice([-5, -1, 0, 1]) if bound is None else bound + rng.choice([-7, -1, 0, 0, 0, 1, 2])
    witness = None if rng.random() < 0.3 else tuple(rng.randrange(k) for k in sizes)
    cert = MinCertificate(model=model, message_bits=message_bits, domains=domains, lower_bound=lower,
                          witness=witness, root=root)
    return cert, (bound is not None and lower <= bound), bound, emin


# ----------------------------------------------------------------------------------------------
# attacks that the checker withstood
# ----------------------------------------------------------------------------------------------

def test_random_hand_built_trees_agree_with_enumeration_an_independent_oracle_and_the_reference_checker(
        reference_checker):
    """SURVIVED.  2,500 random certificates that do not come from the producer.  For each one:
    the verdict equals the verdict of an independent reading of the semantics; an accepted bound
    is at most the enumerated minimum of the root box; `full_box`, the reported bound and the
    witness energy are right; the file round trip is canonical and judged identically; the
    reference checker judges the converted document identically.  (The same campaign was run
    once on 60,000 seeds during the review: 25,819 acceptances, no discrepancy.)"""
    accepted = rejected = tight = with_prune = with_branch = 0
    for seed in range(2500):
        cert, expected, bound, emin = _random_certificate(seed)
        model = cert.model
        unit = 2 ** cert.unit_bits
        truth = Fraction(emin, 2 ** model.scale_bits)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            ours = check_min_certificate(cert)
        assert ours.accepted == expected, (seed, ours.reason)
        if bound is not None:
            assert Fraction(bound, unit) <= truth, seed                 # the rules themselves are sound
        if ours.accepted:
            accepted += 1
            assert Fraction(cert.lower_bound, unit) <= truth, seed      # soundness against enumeration
            assert ours.lower_bound == Fraction(cert.lower_bound, unit)
            assert ours.full_box == all(sorted(d) == list(range(k)) for d, k in zip(cert.domains, model.sizes))
            w = cert.witness
            if w is not None and all(w[i] in cert.domains[i] for i in range(model.n)):
                assert ours.witness_energy == model.energy(w) and ours.certified_gap >= 0
            else:
                assert ours.witness_energy is None and ours.certified_gap is None
            tight += Fraction(cert.lower_bound, unit) == truth
            with_prune += ours.stats["prune"] > 0
            with_branch += ours.stats["branch"] > 0
        else:
            rejected += 1
        text = mincert.dumps(cert)
        back = mincert.loads(text)
        assert mincert.dumps(back) == text and check_min_certificate(back).accepted == ours.accepted, seed
        theirs = reference_checker.check_text(json.dumps(to_metricchain_cert1(cert)))
        assert theirs["accepted"] == ours.accepted, (seed, ours.reason, theirs)
        if ours.accepted:
            assert Fraction(theirs["lower_bound"]) == ours.lower_bound
            energy = theirs.get("witness_energy")
            assert (energy is None) == (ours.witness_energy is None)
            assert energy is None or Fraction(energy) == ours.witness_energy
    assert accepted > 800 and rejected > 800 and tight > 200 and with_prune > 250 and with_branch > 150


def _star(leaves, entry, message):
    """Site 0 (two states) joined to `leaves` one-state sites; every pair table holds `entry`; every
    message from site 0 is `message` (the leaf bound is then exactly min h_0 + leaves * entry)."""
    unary = [np.array([7, 3])] + [np.array([0]) for _ in range(leaves)]
    pair = {(0, j): np.array([[entry], [entry]]) for j in range(1, leaves + 1)}
    model = PairModel(unary=unary, pair=pair, scale_bits=0)
    m = {(0, j): [message, message] for j in range(1, leaves + 1)}
    return model, {"node": "leaf", "m": m}


def test_int64_sums_are_exact_at_the_edge_of_the_supported_range():
    """SURVIVED.  The guard admits entries and messages below 2**50 and a degree of at most 4092;
    at exactly those limits the site sum reaches 4093 * (2**50 - 1) < 2**62 and must not wrap."""
    big = 2 ** 50 - 1
    for entry, message in ((big, big), (-big, -big), (big, -big), (-big, big)):
        model, root = _star(4092, entry, message)
        bound = _Oracle(model, 1).bound(root, model.full_domains())
        assert bound == 3 + 4092 * entry and bound == brute_force_min(model)[0]
        if abs(bound) < 2 ** 62:
            assert check_min_certificate(_cert(model, root=root, lower_bound=bound)).accepted
            assert not check_min_certificate(_cert(model, root=root, lower_bound=bound + 1)).accepted
        else:                                                   # the claim itself is outside the range
            assert not check_min_certificate(_cert(model, root=root, lower_bound=bound)).accepted
    model, root = _star(4092, 5, big)                           # huge messages that cancel exactly
    assert check_min_certificate(_cert(model, root=root, lower_bound=3 + 4092 * 5)).accepted
    assert not check_min_certificate(_cert(model, root=root, lower_bound=3 + 4092 * 5 + 1)).accepted


def test_inputs_outside_the_supported_range_are_rejected_not_wrapped():
    """SURVIVED.  One more neighbour, one more unit of magnitude: a rejection, never an acceptance."""
    model, root = _star(4093, 1, 1)
    assert not check_min_certificate(_cert(model, root=root, lower_bound=-10 ** 9)).accepted
    model, root = _star(3, 2 ** 50, 0)
    assert not check_min_certificate(_cert(model, root=root, lower_bound=-2 ** 61)).accepted
    model, root = _star(3, 2 ** 49, 0)
    assert not check_min_certificate(_cert(model, root=root, lower_bound=-2 ** 61, message_bits=1)).accepted
    model, root = _star(3, 1, 2 ** 50)
    assert not check_min_certificate(_cert(model, root=root, lower_bound=-2 ** 61)).accepted
    model, root = _star(3, 1, 1)
    for lower in (2 ** 62, -2 ** 62, -2 ** 200):
        assert not check_min_certificate(_cert(model, root=root, lower_bound=lower)).accepted
    huge = PairModel(unary=[np.array([2 ** 70, 0], dtype=object)], pair={}, scale_bits=0)   # object-dtype tables
    assert not check_min_certificate(_cert(huge, lower_bound=0)).accepted


def test_malformed_in_memory_certificates_are_rejected_without_an_exception():
    """SURVIVED.  Wrong container types, booleans, floats, missing parts, indices out of range,
    repeated and empty domains, at every position of the in-memory object."""
    model = _small_model()
    leaf = {"node": "leaf", "m": {}}
    bad = [
        dict(domains=[(0, 1), [0, 1]]), dict(domains=[[0, 1]]), dict(domains=[[0, 1], []]),
        dict(domains=[[0, 0], [0, 1]]), dict(domains=[[0, 2], [0, 1]]), dict(domains=[[0, -1], [0, 1]]),
        dict(domains=[[0, True], [0, 1]]), dict(domains=[[0, 1.0], [0, 1]]), dict(domains=None),
        dict(domains=[{0, 1}, [0, 1]]), dict(message_bits=-1), dict(message_bits=True), dict(message_bits=1.0),
        dict(message_bits=None), dict(lower_bound=0.0), dict(lower_bound=True), dict(lower_bound=Fraction(0)),
        dict(lower_bound="0"), dict(witness=(0,)), dict(witness=(0, 2)), dict(witness=(0, -1)),
        dict(witness=(0, True)), dict(witness="00"), dict(root=None), dict(root=[leaf]), dict(root={}),
        dict(root={"node": "sum"}), dict(root={"node": "leaf", "m": []}), dict(root={"node": "leaf", "m": {"0,1": [0, 0]}}),
        dict(root={"node": "leaf", "m": {(0, 1): [0]}}), dict(root={"node": "leaf", "m": {(0, 1): (0, 0)}}),
        dict(root={"node": "leaf", "m": {(0, 1): [0, 0.5]}}), dict(root={"node": "leaf", "m": {(0, 0): [0, 0]}}),
        dict(root={"node": "leaf", "m": {(0, 2): [0, 0]}}), dict(root={"node": "leaf", "m": {(0, 1, 0): [0, 0]}}),
        dict(root={"node": "leaf", "m": {(0, 1): [0, True]}}), dict(root={"node": "leaf", "u": [0, 0]}),
        dict(root={"node": "branch", "site": 2, "children": {}}), dict(root={"node": "branch", "site": 0}),
        dict(root={"node": "branch", "site": 0, "children": [leaf, leaf]}),
        dict(root={"node": "branch", "site": 0, "children": {0: leaf}}),
        dict(root={"node": "branch", "site": 0, "children": {0: leaf, 1: leaf, 2: leaf}}),
        dict(root={"node": "branch", "site": 0, "children": {0: leaf, True: leaf}}),
        dict(root={"node": "branch", "site": 0, "children": {0: leaf, 1: None}}),
        dict(root={"node": "prune", "site": 0, "remove": 1, "dominator": 0}),
        dict(root={"node": "prune", "site": 0, "remove": 1, "dominator": 1, "rest": leaf}),
        dict(root={"node": "prune", "site": 0, "remove": 2, "dominator": 0, "rest": leaf}),
        dict(root={"node": "prune", "site": 0, "remove": 1, "dominator": 0, "rest": leaf, "ell": {}}),
        dict(root={"node": "prune", "site": 0.0, "remove": 1, "dominator": 0, "rest": leaf}),
        dict(model=None), dict(model="model"),
    ]
    for fields in bad:
        result = check_min_certificate(_cert(model, **fields) if "model" not in fields else
                                       MinCertificate(model=fields["model"], message_bits=0, domains=[[0]],
                                                      lower_bound=0, witness=None, root=leaf))
        assert result.accepted is False and result.reason, fields
    assert check_min_certificate(None).accepted is False
    assert check_min_certificate(_cert(model, lower_bound=0)).accepted            # the unmutated object is fine


def test_semantic_corner_cases_of_prune_and_branch_nodes():
    """SURVIVED.  A prune of a state that is not in the domain is a no-op (accepted only if its
    inequality holds); a prune whose dominator was removed before, a repeated prune and a prune by
    itself are rejected; extra children are ignored; a re-branch on a fixed site needs one child."""
    model = PairModel(unary=[np.array([0, 5, 9]), np.array([0, 1])], pair={(0, 1): np.array([[0, 0], [0, 0], [0, 0]])},
                      scale_bits=0)
    leaf = {"node": "leaf", "m": {}}

    def chain(*steps):
        node = leaf
        for (i, r, t) in reversed(steps):
            node = {"node": "prune", "site": i, "remove": r, "dominator": t, "rest": node}
        return node

    def accepted(root, lower=0, domains=None):
        return check_min_certificate(_cert(model, root=root, lower_bound=lower,
                                           domains=domains or model.full_domains())).accepted

    assert accepted(chain((0, 2, 1), (0, 1, 0)))
    assert not accepted(chain((0, 1, 0), (0, 2, 1)))            # dominator 1 was removed before
    assert accepted(chain((0, 2, 0), (0, 2, 0)))                # the second one removes nothing; inequality holds
    assert not accepted(chain((0, 1, 1)))
    assert not accepted(chain((0, 0, 1)))                       # state 0 is strictly better than state 1
    assert accepted(chain((0, 2, 1)), domains=[[0, 1], [0, 1]])  # state 2 is not in the root box: a no-op
    assert not accepted(chain((0, 2, 1)), domains=[[0], [0, 1]])  # ... but the dominator must be in the box
    assert not accepted(chain((0, 2, 1), (0, 1, 0)), lower=1)   # and the bound is still checked
    extra = {"node": "branch", "site": 0, "children": {0: leaf, 1: leaf, 2: {"node": "leaf", "m": {(0, 1): [9, 9, 9]}}}}
    assert accepted(extra, domains=[[0, 1], [0, 1]])
    again = {"node": "branch", "site": 1, "children": {0: {"node": "branch", "site": 1, "children": {0: leaf}}, 1: leaf}}
    assert accepted(again)
    missing = {"node": "branch", "site": 1, "children": {0: {"node": "branch", "site": 1, "children": {1: leaf}}, 1: leaf}}
    assert not accepted(missing)


# ----------------------------------------------------------------------------------------------
# findings (these tests fail with the reviewed code)
# ----------------------------------------------------------------------------------------------

@pytest.mark.parametrize("message_bits, entry", [(np.int64(20), -2 ** 44), (np.int64(12), -2 ** 52),
                                                 (np.int8(7), -5)])
def test_numpy_message_bits_must_not_bypass_the_magnitude_guard(message_bits, entry):
    """FINDING (unsound acceptance; in-memory certificates only).  `validate_structure` admits a
    NumPy integer as `message_bits`; `2 ** message_bits` is then a fixed-width integer, the guard
    `max_abs_entry * 2**message_bits < 2**50` and the scaling of the tables wrap around, and the
    checker accepts the bound 0 for a one-state model whose only energy is negative."""
    model = PairModel(unary=[np.array([entry])], pair={}, scale_bits=0)
    cert = MinCertificate(model=model, message_bits=message_bits, domains=[[0]], lower_bound=0, witness=(0,),
                          root={"node": "leaf", "m": {}})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = check_min_certificate(cert)
    truth = model.energy((0,))
    assert truth < 0
    assert (not result.accepted) or result.lower_bound <= truth, (
        f"accepted lower bound {result.lower_bound} for a model whose minimum is {truth} "
        f"(certified_gap reported as {result.certified_gap})")


def test_checker_must_not_trust_a_stale_neighbour_cache_of_the_instance():
    """FINDING (unsound acceptance; in-memory instance changed after construction).  `PairModel`
    is a mutable dataclass that caches its neighbour lists; the checker takes the tables from
    `model.pair` but the neighbours from the cache.  After `model.pair[(0, 1)] = table` a message
    on that pair is subtracted in the pair term and never added in a site term, and a prune
    ignores the pair: any bound is accepted.  (A file round trip rebuilds the instance and is safe.)"""
    model = PairModel(unary=[np.array([0, 0]), np.array([0, 0])], pair={}, scale_bits=0)
    model.pair[(0, 1)] = np.array([[0, 5], [5, 0]])
    truth = min(model.energy(x) for x in itertools.product(range(2), range(2)))
    cert = MinCertificate(model=model, message_bits=0, domains=[[0, 1], [0, 1]], lower_bound=1000, witness=(0, 0),
                          root={"node": "leaf", "m": {(0, 1): [-1000, -1000]}})
    result = check_min_certificate(cert)
    assert (not result.accepted) or result.lower_bound <= truth, (
        f"accepted lower bound {result.lower_bound}; the minimum of model.energy is {truth}")


def test_witness_given_as_a_mapping_must_not_yield_the_energy_of_no_configuration():
    """FINDING (wrong container type accepted; in-memory only).  A dict `{site: state}` passes
    `validate_structure` (its keys are read as the states), and `witness_energy` then mixes keys
    (unary terms) with values (pair terms): here it reports energy 0 and a certified gap of 0
    although every configuration has energy at least 10."""
    model = PairModel(unary=[np.array([0, 5]), np.array([5, 0])], pair={(0, 1): np.array([[10, 10], [0, 10]])},
                      scale_bits=0)
    truth = min(model.energy(x) for x in itertools.product(range(2), range(2)))
    result = check_min_certificate(_cert(model, lower_bound=0, witness={0: 1, 1: 0}))
    assert (not result.accepted) or result.witness_energy is None or result.witness_energy >= truth, (
        f"witness_energy {result.witness_energy} (gap {result.certified_gap}) but the minimum is {truth}")


@pytest.mark.parametrize("shape", ["prune chain", "branch", "shared subtrees"])
def test_checker_terminates_on_a_certificate_whose_tree_is_not_a_tree(shape):
    """FINDING (hang; in-memory only).  `validate_structure` walks every path of the object graph:
    a node that is its own descendant makes it loop for ever, and 40 levels of shared children
    make it walk 2**40 paths, although the checking loop itself would visit 40 nodes."""
    leaf = {"node": "leaf", "m": {}}
    if shape == "prune chain":
        root = {"node": "prune", "site": 0, "remove": 1, "dominator": 0}
        root["rest"] = root
    elif shape == "branch":
        root = {"node": "branch", "site": 0, "children": {1: leaf}}
        root["children"][0] = root
    else:
        root = leaf
        for _ in range(40):
            root = {"node": "branch", "site": 0, "children": {0: root, 1: root}}
    result = None
    try:
        with _deadline(2.0):
            result = check_min_certificate(_cert(root=root))
    except _Deadline:
        pass
    assert result is not None, "check_min_certificate did not return within 2 s"


@pytest.mark.parametrize("field", ["message_bits", "scale_bits"])
def test_exponent_fields_of_a_small_file_do_not_make_the_checker_compute_astronomical_powers(field):
    """FINDING (resource exhaustion from a 350-byte file).  `2 ** message_bits` and
    `2 ** scale_bits` are computed before (or without) any range check.  With 5*10**7 the check
    allocates tens of megabytes.  Measured during the review: message_bits = 10**8 -> 0.4 s and
    47 MB, 10**9 -> 4.9 s and 467 MB (so, extrapolating, 10**10 costs about a minute and several
    gigabytes); scale_bits = 3*10**8 -> the certificate is *accepted* after 3.4 s and 180 MB."""
    if field == "message_bits":
        text = mincert.dumps(_cert(witness=(0, 0))).replace('"message_bits":0', '"message_bits":50000000')
    else:
        model = PairModel(unary=[np.array([0, 1]), np.array([0, 2])], pair={(0, 1): np.array([[0, 1], [1, 0]])},
                          scale_bits=50_000_000)
        text = mincert.dumps(_cert(model, witness=(0, 0)))
    assert len(text) < 400
    result, peak = _peak_megabytes(lambda: check_min_certificate(mincert.loads(text)))
    assert peak < 2.0, f"{peak:.0f} MB allocated to judge a {len(text)}-byte file (accepted={result.accepted})"


def test_converter_and_serialiser_work_on_every_certificate_that_the_checker_accepts():
    """FINDING (exception on an accepted certificate).  The checker is iterative; the converter and
    the serialiser recurse through branch nodes, whose nesting the docstring of
    `to_metricchain_cert1` bounds by the number of sites.  That holds for the producer only: a
    hand-built tree may branch on the same site again and again.  With Python's default recursion
    limit both functions raise RecursionError on a certificate that the checker accepts, so the
    reference checker cannot be consulted about it."""
    node = {"node": "leaf", "m": {}}
    for _ in range(1500):
        node = {"node": "branch", "site": 0, "children": {0: node, 1: {"node": "leaf", "m": {}}}}
    cert = _cert(root=node, witness=(0, 0))
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)                 # the default; the reference checker raises it when imported
    try:
        assert check_min_certificate(cert).accepted
        problems = []
        for name, fn in (("to_metricchain_cert1", lambda: to_metricchain_cert1(cert)),
                         ("dumps", lambda: mincert.dumps(cert))):
            try:
                fn()
            except MalformedCertificate:
                pass
            except RecursionError:
                problems.append(name)
    finally:
        sys.setrecursionlimit(old)
    assert not problems, f"RecursionError from {problems} on a certificate accepted by check_min_certificate"
