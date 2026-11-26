"""Minimum-energy certificates: producer, independent checker, and the theory division's
reference checker as an external oracle.  Ground truth is exhaustive enumeration in exact
integer arithmetic on instances small enough to enumerate."""
import copy
import json
import random
from fractions import Fraction

import numpy as np
import pytest

from metricchain_sb.model import PairModel, brute_force_min
from metricchain_sb.synthetic import random_pair_model
from metricchain_sb.gmec import certify_gmec
from metricchain_sb.mincert import MalformedCertificate, MinCertificate, to_metricchain_cert1
from metricchain_sb.mincheck import check_min_certificate


def small_models():
    out = []
    for seed in range(24):
        rng = random.Random(seed)
        n = rng.randint(2, 6)
        kmax = rng.randint(2, 4)
        density = rng.choice([0.4, 0.7, 1.0])
        out.append(random_pair_model(seed, n=n, kmax=kmax, density=density, scale_bits=rng.choice([0, 3, 8])))
    return out


def test_energy_is_sum_of_unary_and_pair_tables():
    model = PairModel(
        unary=[np.array([3, -1]), np.array([0, 5, 2])],
        pair={(0, 1): np.array([[1, 0, -4], [2, 2, 7]])},
        scale_bits=2,
    )
    assert model.energy_int((1, 2)) == -1 + 2 + 7
    assert model.energy((0, 2)) == Fraction(3 + 2 - 4, 4)
    assert brute_force_min(model) == (min(model.energy_int((a, b)) for a in range(2) for b in range(3)), (0, 2))


def test_certificate_is_accepted_and_exact_on_small_instances():
    for model in small_models():
        emin, _ = brute_force_min(model)
        cert = certify_gmec(model, eps=Fraction(0))
        result = check_min_certificate(cert)
        assert result.accepted, result.reason
        assert result.lower_bound == Fraction(emin, 2 ** model.scale_bits)
        assert result.witness_energy == result.lower_bound
        assert result.certified_gap == 0


def test_certificate_with_tolerance_brackets_the_minimum():
    eps = Fraction(1, 2)
    for model in small_models()[:10]:
        emin = Fraction(brute_force_min(model)[0], 2 ** model.scale_bits)
        cert = certify_gmec(model, eps=eps)
        result = check_min_certificate(cert)
        assert result.accepted, result.reason
        assert result.lower_bound <= emin <= result.witness_energy
        assert result.certified_gap <= eps


def test_reference_checker_accepts_the_converted_certificate(reference_checker):
    for model in small_models()[:12]:
        emin = Fraction(brute_force_min(model)[0], 2 ** model.scale_bits)
        cert = certify_gmec(model, eps=Fraction(0))
        doc = to_metricchain_cert1(cert)
        verdict = reference_checker.check_text(json.dumps(doc))
        assert verdict["accepted"] is True, verdict
        assert Fraction(verdict["lower_bound"]) == emin
        assert Fraction(verdict["certified_gap"]) == 0


def test_raising_the_claimed_bound_by_one_unit_is_rejected_by_both_checkers(reference_checker):
    for model in small_models()[:12]:
        cert = certify_gmec(model, eps=Fraction(0))
        bad = copy.deepcopy(cert)
        bad.lower_bound += 1          # one unit of 2**-(scale_bits + message_bits) above the optimum
        assert not check_min_certificate(bad).accepted
        assert reference_checker.check_text(json.dumps(to_metricchain_cert1(bad)))["accepted"] is False


def _mutate(cert: MinCertificate, rng: random.Random) -> MinCertificate:
    """A random small change of the certificate tree or of the claim; may or may not stay valid."""
    bad = copy.deepcopy(cert)
    nodes = []

    def walk(node):
        nodes.append(node)
        if node["node"] == "branch":
            for child in node["children"].values():
                walk(child)
        elif node["node"] == "prune":
            walk(node["rest"])

    walk(bad.root)
    node = rng.choice(nodes)
    kind = rng.choice(["bound", "message", "child", "prune", "site"])
    if kind == "bound":
        bad.lower_bound += rng.choice([-3, -1, 1, 2, 5])
    elif kind == "message" and node["node"] == "leaf" and node["m"]:
        key = rng.choice(sorted(node["m"]))
        vec = node["m"][key]
        vec[rng.randrange(len(vec))] += rng.choice([-7, -1, 1, 4])
    elif kind == "child" and node["node"] == "branch" and len(node["children"]) > 1:
        del node["children"][rng.choice(sorted(node["children"]))]
    elif kind == "prune" and node["node"] == "prune":
        k = bad.model.sizes[node["site"]]
        node[rng.choice(["remove", "dominator"])] = rng.randrange(k)
    elif kind == "site" and node["node"] in ("branch", "prune"):
        node["site"] = rng.randrange(bad.model.n)
    else:
        bad.lower_bound += 1
    return bad


def test_checkers_agree_on_mutated_certificates_and_never_accept_a_false_bound(reference_checker):
    rng = random.Random(2026)
    accepted = rejected = malformed = 0
    for model in small_models():
        emin = Fraction(brute_force_min(model)[0], 2 ** model.scale_bits)
        cert = certify_gmec(model, eps=Fraction(0))
        for _ in range(12):
            bad = _mutate(cert, rng)
            ours = check_min_certificate(bad)
            try:
                doc = to_metricchain_cert1(bad)
            except MalformedCertificate:
                # an index outside a site's own state set: not a well-formed object of our format
                # (the padded alphabet of the reference format could still express it)
                assert not ours.accepted and "malformed" in ours.reason
                malformed += 1
                continue
            theirs = reference_checker.check_text(json.dumps(doc))
            assert ours.accepted == theirs["accepted"], (ours.reason, theirs)
            if ours.accepted:
                accepted += 1
                assert ours.lower_bound <= emin          # soundness against brute force
            else:
                rejected += 1
    assert accepted > 0 and rejected > 0 and malformed > 0   # the test exercises all three outcomes


def test_checker_rejects_a_certificate_whose_tables_exceed_the_supported_range():
    model = PairModel(unary=[np.array([2 ** 61, 0]), np.array([0, 1])], pair={(0, 1): np.array([[0, 1], [1, 0]])},
                      scale_bits=0)
    cert = MinCertificate(model=model, message_bits=8, domains=[[0, 1], [0, 1]], lower_bound=0, witness=None,
                          root={"node": "leaf", "m": {}})
    result = check_min_certificate(cert)
    assert not result.accepted and "range" in result.reason


def test_serialised_certificate_round_trips_and_is_judged_identically():
    from metricchain_sb import mincert
    for model in small_models()[:8]:
        cert = certify_gmec(model, eps=Fraction(0))
        text = mincert.dumps(cert)
        back = mincert.loads(text)
        assert mincert.dumps(back) == text                         # canonical: stable under a round trip
        assert json.loads(text)["model_sha256"] == mincert.model_sha256(back.model)
        a, b = check_min_certificate(cert), check_min_certificate(back)
        assert a.accepted and b.accepted and a.lower_bound == b.lower_bound and a.stats == b.stats
        counts = mincert.count_nodes(back.root)
        assert {k: counts[k] for k in ("leaf", "branch", "prune")} == b.stats


def test_checksum_changes_when_one_table_entry_changes():
    from metricchain_sb import mincert
    model = small_models()[3]
    other = PairModel(unary=[u.copy() for u in model.unary], pair={k: t.copy() for k, t in model.pair.items()},
                      scale_bits=model.scale_bits)
    assert mincert.model_sha256(other) == mincert.model_sha256(model)
    other.unary[0][0] += 1
    assert mincert.model_sha256(other) != mincert.model_sha256(model)


def test_long_elimination_chains_serialise_convert_and_check_without_recursion():
    """Regression (found on BPTI and ubiquitin, 2026-11-26): more than a thousand consecutive prune
    nodes made the serialiser and the converter exceed Python's recursion limit.  The limit is
    lowered here because the reference checker, when loaded by other tests, raises it globally."""
    import sys
    from metricchain_sb import mincert
    k = 700                                     # one site with 700 states, each dominated by state 0
    model = PairModel(unary=[np.arange(k, dtype=np.int64), np.array([0, 3])],
                      pair={(0, 1): np.zeros((k, 2), dtype=np.int64)}, scale_bits=0)
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(250)
    try:
        cert = certify_gmec(model, eps=Fraction(0))
        assert mincert.count_nodes(cert.root)["prune"] >= k - 1
        text = mincert.dumps(cert)
        back = mincert.loads(text)
        assert check_min_certificate(back).accepted
        doc = to_metricchain_cert1(back)
        mincert.validate_structure(back)
    finally:
        sys.setrecursionlimit(old)
    assert doc["certificate"]["node"] == "prune" and json.dumps(doc)[:1] == "{"


def test_detached_certificate_needs_the_instance_with_the_recorded_checksum(tmp_path):
    from metricchain_sb import mincert, modelio
    model = small_models()[5]
    cert = certify_gmec(model, eps=Fraction(0))
    text = mincert.dumps(cert, include_model=False)
    assert '"model":' not in text and mincert.model_sha256(model) in text
    path = tmp_path / "instance.npz"
    modelio.save_model(model, path)
    again = modelio.load_model(path)
    assert mincert.model_sha256(again) == mincert.model_sha256(model) and again.meta == model.meta
    back = mincert.loads(text, model=again)
    assert check_min_certificate(back).accepted
    with pytest.raises(mincert.MalformedCertificate):
        mincert.loads(text)                                  # no instance supplied
    other = small_models()[6]
    with pytest.raises(mincert.MalformedCertificate):
        mincert.loads(text, model=other)                     # wrong instance: checksum mismatch


def test_loader_is_strict_so_that_a_file_has_one_reading():
    """Found by an internal review (2026-11-26): duplicate keys were accepted (last one wins) and
    non-integers were passed through `int()`; one file could then be read two ways."""
    from metricchain_sb import mincert
    model = small_models()[4]
    cert = certify_gmec(model, eps=Fraction(0))
    text = mincert.dumps(cert)
    assert check_min_certificate(mincert.loads(text)).accepted
    doc = json.loads(text)

    def rejected(mutated_text):
        with pytest.raises(mincert.MalformedCertificate):
            mincert.loads(mutated_text)
        return True

    assert rejected(text[:-1] + ',"message_bits":0}')                         # duplicate key
    for path, value in [(("claim", "lower_bound"), doc["claim"]["lower_bound"] + 0.5),
                        (("claim", "lower_bound"), True),
                        (("claim", "lower_bound"), str(doc["claim"]["lower_bound"])),
                        (("message_bits",), 12.0),
                        (("model", "scale_bits"), 1.5)]:
        bad = json.loads(text)
        target = bad
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        assert rejected(json.dumps(bad))
    bad = json.loads(text)
    bad["domains"][0][0] = float(bad["domains"][0][0]) + 0.25
    assert rejected(json.dumps(bad))
    bad = json.loads(text)
    bad["model"]["unary"][0][0] = bad["model"]["unary"][0][0] + 0.5            # a table entry that is not an integer
    assert rejected(json.dumps(bad))
    assert rejected(text.replace('"format":"structbio-mincert/1"', '"format":"structbio-mincert/1","extra":NaN'))


def test_check_result_says_whether_the_claim_covers_every_state_of_every_site():
    """A certificate over a sub-box is a true statement about that sub-box only; whoever reads an
    acceptance as 'global minimum' must know which case holds (internal review, 2026-11-26)."""
    model = small_models()[7]
    full = check_min_certificate(certify_gmec(model, eps=Fraction(0)))
    assert full.accepted and full.full_box is True
    domains = [[0] if k > 1 else [0] for k in model.sizes]
    part = check_min_certificate(certify_gmec(model, eps=Fraction(0), domains=domains))
    assert part.accepted and part.full_box is (all(k == 1 for k in model.sizes))
