"""Hardening after the adversarial review STRUCTBIO-REV-0001 and the Engineering division's review:
tests for what was added (one entry point from file text to verdict, the instance checksum in
the verdict, checkers for the stability claims, documented limits) and for the decisions taken
where the review left a choice.  Every documented limit named here is tested on both sides.
"""
import dataclasses
import itertools
import json
import sys
from fractions import Fraction

import numpy as np
import pytest

from metricchain_sb import mincert, stability, zcert
from metricchain_sb.gmec import certify_gmec
from metricchain_sb.mincert import MalformedCertificate, MinCertificate
from metricchain_sb.mincheck import CheckResult, check_min_certificate
from metricchain_sb.model import PairModel
from metricchain_sb.partition import certify_partition, weighted_model
from metricchain_sb.synthetic import random_pair_model
from metricchain_sb.zcert import MalformedZCertificate, ZCertificate
from metricchain_sb.zcheck import check_partition_certificate


def _model():
    return PairModel(unary=[np.array([0, 1, 4]), np.array([0, 2])],
                     pair={(0, 1): np.array([[0, 1], [1, 0], [3, 3]])}, scale_bits=1)


def _certificate(model=None, **fields):
    model = _model() if model is None else model
    base = dict(model=model, message_bits=1, domains=model.full_domains(), lower_bound=0, witness=(0, 0),
                root={"node": "prune", "site": 0, "remove": 2, "dominator": 0,
                      "rest": {"node": "branch", "site": 0, "children": {0: {"node": "leaf", "m": {}},
                                                                         1: {"node": "leaf", "m": {}}}}})
    base.update(fields)
    return MinCertificate(**base)


# ----------------------------------------------------------------------------------------------
# One entry point from file text to verdict (Engineering division): `mincheck.check_text`
# ----------------------------------------------------------------------------------------------

def test_check_text_judges_a_file_and_names_the_instance_the_verdict_is_about():
    from metricchain_sb.mincheck import check_text
    model = _model()
    sha = mincert.model_sha256(model)
    embedded = mincert.dumps(_certificate(model))
    detached = mincert.dumps(_certificate(model), include_model=False)
    for text, kwargs in ((embedded, {}), (embedded, dict(model=model)), (detached, dict(model=model)),
                         (embedded, dict(expected_model_sha256=sha)),
                         (detached, dict(model=model, expected_model_sha256=sha))):
        result = check_text(text, **kwargs)
        assert isinstance(result, CheckResult)
        assert result.accepted and result.lower_bound == 0 and result.certified_gap == 0, result.reason
        assert result.model_sha256 == sha
    assert check_min_certificate(_certificate(model)).model_sha256 == sha      # also from the in-memory entry point


def test_check_text_refuses_a_file_about_another_instance_than_the_expected_one():
    from metricchain_sb.mincheck import check_text
    model = _model()
    text = mincert.dumps(_certificate(model))
    assert check_text(text, expected_model_sha256=mincert.model_sha256(model)).accepted
    for wrong in ("0" * 64, mincert.model_sha256(model).upper(), "", 17):
        result = check_text(text, expected_model_sha256=wrong)
        assert result.accepted is False and "instance" in result.reason, wrong
        assert result.lower_bound is None                     # nothing of the foreign verdict is reported as certified
    other = PairModel(unary=[np.array([-50, 1, 4]), np.array([0, 2])],
                      pair={(0, 1): np.array([[0, 1], [1, 0], [3, 3]])}, scale_bits=1)
    foreign = check_text(text, model=other)                   # the file embeds another instance than the caller holds
    assert foreign.accepted is False and "instance" in foreign.reason
    detached = mincert.dumps(_certificate(model), include_model=False)
    assert check_text(detached).accepted is False             # no instance at all
    assert check_text(detached, model=other).accepted is False


@pytest.mark.parametrize("text", ["", "  ", "garbage", "{", "[1,2", "null", "17", '"text"', "[]", "{}", '{"format":1}',
                                  '{"format":"structbio-mincert/1"}', "[" * 30000 + "]" * 30000, "\x00", "\ufeff{}",
                                  None, 17, 1.5, b"{}", ["{}"], {"format": "structbio-mincert/1"}])
def test_check_text_turns_garbage_into_a_rejection_never_an_exception(text):
    from metricchain_sb.mincheck import check_text
    result = check_text(text)
    assert isinstance(result, CheckResult) and result.accepted is False and result.reason
    assert check_text(text, model=_model(), expected_model_sha256="0" * 64).accepted is False
    assert check_text(text, model="not a model").accepted is False


def test_a_file_nested_1200_nodes_deep_round_trips_at_the_default_recursion_limit():
    from metricchain_sb.mincheck import check_text
    model = _model()
    node = {"node": "leaf", "m": {}}
    for _ in range(1200):
        node = {"node": "branch", "site": 1, "children": {0: node, 1: {"node": "leaf", "m": {}}}}
    cert = _certificate(model, root=node)
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)                 # the interpreter's default (the reference checker raises it when imported)
    try:
        text = mincert.dumps(cert)
        back = mincert.loads(text)
        assert mincert.dumps(back) == text
        assert mincert.count_nodes(back.root)["depth"] == 1201
        result = check_text(text)
    finally:
        sys.setrecursionlimit(old)
    assert result.accepted and result.stats == {"leaf": 2, "branch": 1200, "prune": 0}      # the nodes on the box


def test_the_file_format_has_a_documented_nesting_limit_enforced_by_writer_and_reader():
    """`mincert.MAX_FILE_DEPTH` nested nodes: at the limit a file is written and read back; one
    level deeper the writer refuses, and a hand-written file of that depth is malformed."""
    model = _model()
    leaf = '{"node":"leaf","m":{}}'

    def nested(depth):                          # `depth` nodes on the longest path
        node = {"node": "leaf", "m": {}}
        for _ in range(depth - 1):
            node = {"node": "branch", "site": 1, "children": {0: node, 1: {"node": "leaf", "m": {}}}}
        return _certificate(model, root=node)

    limit = mincert.MAX_FILE_DEPTH
    text = mincert.dumps(nested(limit))
    assert check_min_certificate(mincert.loads(text)).accepted
    with pytest.raises(MalformedCertificate):
        mincert.dumps(nested(limit + 1))
    assert check_min_certificate(nested(limit + 1)).accepted          # the checker itself has no depth limit
    doc = json.loads(mincert.dumps(_certificate(model)))
    doc["certificate"] = "@@"
    deep = '{"node":"branch","site":1,"children":{"0":' * limit + leaf + (',"1":' + leaf + '}}') * limit
    with pytest.raises(MalformedCertificate):
        mincert.loads(json.dumps(doc, separators=(",", ":")).replace('"@@"', deep))


def test_numerals_of_a_file_have_a_documented_maximum_length_whatever_the_interpreter_allows():
    text = mincert.dumps(_certificate())
    limit = mincert.MAX_INT_DIGITS
    old = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)               # what the reference checker does when it is imported
    try:
        ok = text.replace('"lower_bound":0', '"lower_bound":-' + "9" * limit)
        assert mincert.loads(ok).lower_bound == -int("9" * limit)
        assert check_min_certificate(mincert.loads(ok)).accepted is False       # outside the checker's range, not the loader's
        for mutated in (text.replace('"lower_bound":0', '"lower_bound":-' + "9" * (limit + 1)),
                        text.replace('"lower_bound":0', '"lower_bound":' + "1" + "0" * limit),
                        text.replace('"children":{"0"', '"children":{"' + "1" * (limit + 1) + '"')):
            assert mutated != text
            with pytest.raises(MalformedCertificate):
                mincert.loads(mutated)
        z = _z_certificate()
        ztext = zcert.dumps(z)
        with pytest.raises(MalformedZCertificate):
            zcert.loads(ztext.replace('"beta":"3/2"', '"beta":"' + "3" * (limit + 1) + '/2"'), z.model)
    finally:
        sys.set_int_max_str_digits(old)


def test_randomly_damaged_files_raise_only_the_malformed_exception_of_their_loader():
    """Finding 9 as a regression test: 400 random edits of a valid file of each format (characters
    deleted, replaced, doubled; pieces moved; brackets and digits inserted).  The loader either
    returns a certificate or raises its own exception; the checkers and `check_text` never raise."""
    import random
    from metricchain_sb.mincheck import check_text
    rng = random.Random(9)
    z = _z_certificate(steps=[{"op": "relax", "pair": [0, 1], "f": [1, 0], "g": [0, -1]}], order=[], branch=0,
                       children={0: {"steps": [{"op": "prune", "site": 1, "remove": 1, "dominator": 0}], "order": [0, 1]},
                                 1: {"steps": [], "order": [1, 0]}}, claim={"ln_z_lo": Fraction(-7, 2)})
    alphabet = '{}[]",:-0123456789 \\ue\u00b2\u0663/abn.'

    def damaged(text):
        for _ in range(rng.choice([1, 1, 2, 4])):
            i, j = sorted(rng.randrange(len(text) + 1) for _ in range(2))
            kind = rng.randrange(5)
            if kind == 0:
                text = text[:i] + text[j if j - i < 40 else i + 1:]
            elif kind == 1:
                text = text[:i] + rng.choice(alphabet) + text[i + 1:]
            elif kind == 2:
                text = text[:i] + text[i:j][:60] * 2 + text[j:]
            elif kind == 3:
                text = text[:i] + rng.choice(alphabet) * rng.choice([1, 1, 3, 2000]) + text[i:]
            else:
                text = text[:i] + text[j:] + text[i:j]
        return text

    outcomes = {"loaded": 0, "malformed": 0}
    for text, load, check, error in (
            (mincert.dumps(_certificate()), mincert.loads, check_min_certificate, MalformedCertificate),
            (zcert.dumps(z), lambda t: zcert.loads(t, z.model), check_partition_certificate, MalformedZCertificate)):
        for _ in range(400):
            mutated = damaged(text)
            try:
                cert = load(mutated)
            except error:
                outcomes["malformed"] += 1
                if error is MalformedCertificate:
                    assert check_text(mutated).accepted is False
                continue
            outcomes["loaded"] += 1
            assert check(cert).accepted in (True, False)        # a verdict, not an exception
            if error is MalformedCertificate:
                assert check_text(mutated).accepted is check(cert).accepted
    assert outcomes["malformed"] > 500 and outcomes["loaded"] > 5


# ----------------------------------------------------------------------------------------------
# Decisions about in-memory certificates
# ----------------------------------------------------------------------------------------------

def test_a_leaf_may_be_referenced_twice_but_a_node_with_descendants_may_not():
    """Finding 8 (object graphs that are not trees).  A leaf has no descendants: referring to one
    leaf object from several places is harmless and stays accepted (hand-written certificates do
    it).  A branch or prune node that occurs twice is refused — that is what makes the walk
    linear in the size of the object and guarantees that it ends."""
    leaf = {"node": "leaf", "m": {}}
    shared_leaf = {"node": "branch", "site": 1, "children": {0: leaf, 1: leaf}}
    assert check_min_certificate(_certificate(root=shared_leaf)).accepted
    inner = {"node": "branch", "site": 1, "children": {0: {"node": "leaf", "m": {}}, 1: {"node": "leaf", "m": {}}}}
    shared_branch = {"node": "branch", "site": 0, "children": {0: inner, 1: inner, 2: dict(inner)}}
    result = check_min_certificate(_certificate(root=shared_branch))
    assert result.accepted is False and "tree" in result.reason
    with pytest.raises(MalformedCertificate):
        mincert.validate_structure(_certificate(root=shared_branch))
    with pytest.raises(MalformedCertificate):
        mincert.dumps(_certificate(root=shared_branch))
    distinct = {"node": "branch", "site": 0, "children": {0: json.loads(json.dumps(inner)), 1: dict(inner), 2: dict(inner)}}
    for child in distinct["children"].values():                 # JSON turned the keys into strings: restore them
        child["children"] = {int(a): c for a, c in child["children"].items()}
    assert check_min_certificate(_certificate(root=distinct)).accepted


def test_numpy_integers_anywhere_in_a_min_certificate_are_read_as_python_integers():
    """Findings 1 and 2: every integer of a certificate is normalised at validation; the verdict on
    a certificate written with NumPy integers is the verdict on the same certificate in Python
    integers, and the file written from it is the same file."""
    model = _model()
    plain = _certificate(model, root={"node": "prune", "site": 0, "remove": 2, "dominator": 0,
                                      "rest": {"node": "leaf", "m": {(0, 1): [0, -1, 0], (1, 0): [0, 0]}}})
    numpy_ = _certificate(model, message_bits=np.int8(1), lower_bound=np.int64(0),
                          domains=[[np.int64(0), np.int32(1), np.uint8(2)], [np.int16(0), 1]],
                          witness=(np.int64(0), np.uint16(0)),
                          root={"node": "prune", "site": np.int64(0), "remove": np.int8(2), "dominator": np.uint8(0),
                                "rest": {"node": "leaf", "m": {(np.int64(0), np.int8(1)): [np.int8(0), np.int64(-1), 0],
                                                                (1, 0): [np.int8(0), np.int16(0)]}}})
    a, b = check_min_certificate(plain), check_min_certificate(numpy_)
    assert a.accepted and b.accepted
    assert (a.lower_bound, a.witness_energy, a.certified_gap, a.full_box, a.stats) == \
           (b.lower_bound, b.witness_energy, b.certified_gap, b.full_box, b.stats)
    assert mincert.dumps(numpy_) == mincert.dumps(plain)
    normal = mincert.normalised(numpy_)
    assert type(normal.message_bits) is int and type(normal.lower_bound) is int
    assert all(type(a) is int for d in normal.domains for a in d) and all(type(a) is int for a in normal.witness)
    for wrong in (dict(message_bits=np.float64(1)), dict(lower_bound=np.bool_(False)), dict(witness=np.array([0, 0])),
                  dict(witness=[0.0, 0]), dict(domains=[[0, 1, np.float32(2)], [0, 1]])):
        assert check_min_certificate(_certificate(model, **wrong)).accepted is False, wrong


def test_min_checker_limits_are_documented_and_tested_on_both_sides():
    """Finding 7: `message_bits` and `scale_bits` are range-checked before any power is computed."""
    from metricchain_sb import mincheck
    from metricchain_sb.model import MAX_SCALE_BITS
    zero = PairModel(unary=[np.array([0, 0])], pair={}, scale_bits=0)

    def verdict(model, message_bits):
        return check_min_certificate(MinCertificate(model=model, message_bits=message_bits, domains=model.full_domains(),
                                                    lower_bound=0, witness=None, root={"node": "leaf", "m": {}}))

    assert verdict(zero, mincheck.MAX_MESSAGE_BITS).accepted
    over = verdict(zero, mincheck.MAX_MESSAGE_BITS + 1)
    assert over.accepted is False and "range" in over.reason
    fine = PairModel(unary=[np.array([0, 0])], pair={}, scale_bits=MAX_SCALE_BITS)
    assert verdict(fine, 0).accepted
    finer = PairModel(unary=[np.array([0, 0])], pair={}, scale_bits=MAX_SCALE_BITS + 1)
    over = verdict(finer, 0)
    assert over.accepted is False and "range" in over.reason


def test_the_checkers_read_the_instance_as_it_is_and_refuse_one_that_is_no_longer_an_integer_model():
    """Finding 4: nothing derived from the tables is cached on the instance; a table replaced after
    construction by something that is not an integer table of the right shape is refused."""
    model = PairModel(unary=[np.array([0, 0]), np.array([0, 0])], pair={}, scale_bits=0)
    assert model.neighbors(0) == []
    model.pair[(0, 1)] = np.array([[0, 5], [5, 0]])
    assert model.neighbors(0) == [1] and model.neighbors(1) == [0]
    cert = MinCertificate(model=model, message_bits=0, domains=[[0, 1], [0, 1]], lower_bound=0, witness=(0, 0),
                          root={"node": "leaf", "m": {(0, 1): [0, 0]}})
    result = check_min_certificate(cert)
    assert result.accepted and result.model_sha256 == mincert.model_sha256(model)
    for broken in (np.array([[0.5, 5], [5, 0]]), np.array([[0, 5, 1], [5, 0, 1]]), [[0, 5], [5, 0.5]], "table"):
        model.pair[(0, 1)] = broken
        result = check_min_certificate(cert)
        assert result.accepted is False and result.reason, broken
        z = ZCertificate(model=model, beta=Fraction(1), domains=[[0, 1], [0, 1]], steps=[], order=[0, 1])
        for arithmetic in ("exact", "float"):
            assert check_partition_certificate(z, arithmetic=arithmetic).accepted is False, broken
    model.pair[(0, 1)] = np.array([[0, 5], [5, 0]])
    model.pair[(1, 0)] = np.array([[0, 5], [5, 0]])              # a key the constructor would have refused
    assert check_min_certificate(cert).accepted is False


# ----------------------------------------------------------------------------------------------
# The Z checker: documented limits, exact integers and rationals, claims
# ----------------------------------------------------------------------------------------------

def _z_certificate(**fields):
    model = PairModel(unary=[np.array([0, 1]), np.array([0, 2])], pair={(0, 1): np.array([[0, 1], [1, 0]])},
                      scale_bits=0)
    base = dict(model=model, beta=Fraction(3, 2), domains=model.full_domains(), steps=[], order=[0, 1])
    base.update(fields)
    return ZCertificate(**base)


def test_a_rational_with_numpy_components_must_not_make_the_z_checker_compute_in_fixed_width():
    """Same class as finding 2 (not listed by the review): `Fraction(np.int64(p), np.int64(q))`
    keeps NumPy integers inside the Fraction, so `beta * energy` wraps at 64 bits.  One
    configuration of energy 3 * 2**40 at beta = 2**40 / 3: the product is 2**80; in int64
    arithmetic it wraps to 0 and ln Z = 0 is certified where ln Z = -2**80 ... (the exponent is far
    outside the range the checker evaluates, so the right answer is a rejection)."""
    energy, p, q = 3 * 2 ** 40, 2 ** 40, 3
    model = PairModel(unary=[np.array([energy], dtype=object)], pair={}, scale_bits=0)
    wrapped = Fraction(np.int64(p), np.int64(q))
    cert = ZCertificate(model=model, beta=wrapped, domains=[[0]], steps=[], order=[0])
    truth = -Fraction(p, q) * energy
    for arithmetic in ("exact", "float"):
        result = check_partition_certificate(cert, arithmetic=arithmetic)
        assert (not result.accepted) or result.ln_z_lo <= truth <= result.ln_z_hi, (
            f"{arithmetic}: accepted [{float(result.ln_z_lo)}, {float(result.ln_z_hi)}], ln Z = {float(truth)}")
    small = ZCertificate(model=PairModel(unary=[np.array([3])], pair={}, scale_bits=0),
                         beta=Fraction(np.int64(1), np.int64(3)), domains=[[0]], steps=[], order=[0],
                         claim={"ln_z_lo": Fraction(np.int64(-2), np.int64(1)), "ln_z_hi": Fraction(np.int64(0))})
    result = check_partition_certificate(small)                 # ln Z = -1 exactly
    assert result.accepted and result.ln_z_lo <= -1 <= result.ln_z_hi
    normal = zcert.normalised(small)
    assert type(normal.beta.numerator) is int and type(normal.beta.denominator) is int
    assert all(type(v.numerator) is int for v in normal.claim.values())


def test_z_checker_limits_are_documented_and_tested_on_both_sides():
    """Finding 6.  Exponent arguments (beta times a table entry, a relax step's residual range, a
    node's accumulated factor) are evaluated up to `zcheck.MAX_EXPONENT`; a prune whose margin is
    below `zcheck.MIN_PRUNE_EXPONENT / beta` is refused; beyond the limits the checker rejects with
    a reason that names the range — it never exponentiates a large number as an exact rational."""
    from metricchain_sb import zcheck
    from metricchain_sb.model import MAX_SCALE_BITS
    top = zcheck.MAX_EXPONENT

    def one_entry(energy, beta=Fraction(1), scale_bits=0):
        model = PairModel(unary=[np.array([0, energy], dtype=object)], pair={}, scale_bits=scale_bits)
        return ZCertificate(model=model, beta=beta, domains=model.full_domains(), steps=[], order=[0])

    for arithmetic in ("exact", "float"):
        assert check_partition_certificate(one_entry(top), arithmetic=arithmetic).accepted
        assert check_partition_certificate(one_entry(-top), arithmetic=arithmetic).accepted
        for cert in (one_entry(top + 1), one_entry(-top - 1), one_entry(top, beta=Fraction(top + 1, top))):
            result = check_partition_certificate(cert, arithmetic=arithmetic)
            assert result.accepted is False and "range this checker evaluates" in result.reason
        assert check_partition_certificate(one_entry(1, scale_bits=MAX_SCALE_BITS), arithmetic=arithmetic).accepted
        over = check_partition_certificate(one_entry(1, scale_bits=MAX_SCALE_BITS + 1), arithmetic=arithmetic)
        assert over.accepted is False and "scale_bits" in over.reason

        def relax(f):
            return _z_certificate(beta=Fraction(1), steps=[{"op": "relax", "pair": [0, 1], "f": [f, 0], "g": [0, 0]}])

        assert check_partition_certificate(relax(top), arithmetic=arithmetic).accepted          # residuals in [-top, 1]
        over = check_partition_certificate(relax(top + 2), arithmetic=arithmetic)
        assert over.accepted is False and "range this checker evaluates" in over.reason

        def prune(entry, leaves=1):
            """Site 0 (two states) and `leaves` one-state sites; state 1 of site 0 costs `entry` against
            every leaf and is pruned by state 0: the margin is `leaves * entry`, and ln Z = ln(1 + exp(-margin))."""
            unary = [np.array([0, 0])] + [np.array([0]) for _ in range(leaves)]
            pair = {(0, j): np.array([[0], [entry]], dtype=object) for j in range(1, leaves + 1)}
            model = PairModel(unary=unary, pair=pair, scale_bits=0)
            return ZCertificate(model=model, beta=Fraction(1), domains=model.full_domains(),
                                order=list(range(leaves + 1)),
                                steps=[{"op": "prune", "site": 0, "remove": 1, "dominator": 0}])

        floor = zcheck.MIN_PRUNE_EXPONENT
        assert floor < 0
        at = check_partition_certificate(prune(floor), arithmetic=arithmetic)
        assert at.accepted and at.ln_z_lo <= -floor <= at.ln_z_hi               # ln Z = ln(1 + e**9) = 9.0001...
        below = check_partition_certificate(prune(floor - 1), arithmetic=arithmetic)
        assert below.accepted is False and "prune" in below.reason and "margin" in below.reason
        # a huge positive margin (a clash) is the safest prune: accepted, and bounded without huge arithmetic
        cap = zcheck.PRUNE_EXPONENT_CAP
        assert cap < top
        for entry, leaves in ((cap - 1, 1), (cap, 1), (cap + 1, 1), (top, 1), (top, 7)):
            result = check_partition_certificate(prune(entry, leaves), arithmetic=arithmetic)
            assert result.accepted and result.ln_z_lo <= 0 < result.ln_z_hi, (entry, leaves, result.reason)
            assert result.ln_z_hi - result.ln_z_lo < Fraction(1, 10 ** 9)


def test_exp_bits_is_checked_against_a_documented_range_in_each_tier():
    """Finding 3: the float tier evaluates `exp_bits` only inside `zcheck.EXP_BITS_RANGE["float"]`
    (and its conversion of weights is correct for every mantissa); the exact tier has its own range."""
    from metricchain_sb import zcheck
    cert = _z_certificate()
    for arithmetic in ("exact", "float"):
        low, high = zcheck.EXP_BITS_RANGE[arithmetic]
        for bits in (low, 64, high, np.int64(64)):
            assert check_partition_certificate(cert, arithmetic=arithmetic, exp_bits=bits).accepted, (arithmetic, bits)
        for bits in (low - 1, high + 1, 0, -64, 10 ** 9, 64.0, True, None, "64"):
            result = check_partition_certificate(cert, arithmetic=arithmetic, exp_bits=bits)
            assert result.accepted is False and "exp_bits" in result.reason, (arithmetic, bits)
    assert zcheck.EXP_BITS_RANGE["float"][1] < zcheck.EXP_BITS_RANGE["exact"][1]


def test_float_weight_conversion_is_an_upper_bound_for_every_mantissa():
    """Finding 3 at its root: `FloatTables._ldexp_up` tested the exponent, not the value."""
    from metricchain_sb.itables import FloatTables
    for mantissa_bits in (1, 53, 200, 900, 1003, 1004, 1020, 1023):
        for exponent in (-3000, -2001, -2000, -1999, -1500, -1100, -1023 - mantissa_bits, -mantissa_bits):
            m = (1 << mantissa_bits) - 1
            f = FloatTables._up(m)
            up, down = FloatTables._ldexp_up(f, exponent), FloatTables._ldexp_down(FloatTables._down(m), exponent)
            exact = Fraction(m) * Fraction(2) ** exponent
            assert Fraction(down) <= exact <= Fraction(up), (mantissa_bits, exponent)


def test_the_claim_of_a_producer_made_z_certificate_is_on_the_documented_grid_and_contains_the_interval():
    """Finding 12: a claim is what the producer asserts — its interval moved outward to the grid
    `2**-zcert.CLAIM_GRID_BITS` nats; the checker accepts iff the interval it computes lies inside."""
    beta = Fraction(1000, 593)
    grid = 2 ** zcert.CLAIM_GRID_BITS
    for seed in range(4):
        model = random_pair_model(seed, n=4, kmax=3, density=1.0, scale_bits=2, amplitude=6, kmin=2)
        for made in ("exact", "float"):
            cert = certify_partition(model, beta, tau=3, theta=2, arithmetic=made)
            lo, hi = cert.claim["ln_z_lo"], cert.claim["ln_z_hi"]
            assert (lo * grid).denominator == 1 and (hi * grid).denominator == 1
            for checked in ("exact", "float"):
                result = check_partition_certificate(cert, arithmetic=checked)
                assert result.accepted, result.reason
                assert lo <= result.ln_z_lo <= result.ln_z_hi <= hi
                if checked == made:                 # at most two grid steps wider than what the producer computed
                    assert result.ln_z_lo - lo <= Fraction(2, grid) and hi - result.ln_z_hi <= Fraction(2, grid)
                for narrow in ({"ln_z_lo": result.ln_z_lo + Fraction(1, 10 ** 30)},
                               {"ln_z_hi": result.ln_z_hi - Fraction(1, 10 ** 30)}):
                    refused = check_partition_certificate(dataclasses.replace(cert, claim=narrow), arithmetic=checked)
                    assert refused.accepted is False and "claim" in refused.reason


def test_z_certificates_are_nested_at_most_a_documented_number_of_branch_nodes_deep():
    """The evaluator of the Z checker recurses once per conditioning level; `zcert.MAX_BRANCH_DEPTH`
    keeps it inside the interpreter's default recursion limit."""
    def nested(depth):                          # `depth` nested branch nodes on site 0
        node = {"steps": [], "order": [0, 1]}
        for _ in range(depth):
            node = {"steps": [], "branch": 0, "children": {0: node, 1: {"steps": [], "order": [0, 1]}}}
        return _z_certificate(order=[], branch=0, children=node["children"])

    limit = zcert.MAX_BRANCH_DEPTH
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 1000))
    try:
        at = check_partition_certificate(nested(limit), arithmetic="float")
    finally:
        sys.setrecursionlimit(old)
    assert at.accepted, at.reason
    text = zcert.dumps(nested(limit))
    assert zcert.dumps(zcert.loads(text, nested(1).model)) == text
    over = check_partition_certificate(nested(limit + 1), arithmetic="float")
    assert over.accepted is False and "deep" in over.reason
    with pytest.raises(MalformedZCertificate):
        zcert.dumps(nested(limit + 1))


# ----------------------------------------------------------------------------------------------
# Conversion to the nested format has a documented limit and a dedicated exception
# ----------------------------------------------------------------------------------------------

def test_conversion_too_deep_is_not_a_malformed_certificate():
    assert issubclass(mincert.ConversionTooDeep, ValueError)
    assert not issubclass(mincert.ConversionTooDeep, MalformedCertificate)
    assert not issubclass(MalformedCertificate, mincert.ConversionTooDeep)
    assert mincert.MAX_CERT1_NESTING >= 3001          # 1,500 nested branch nodes are converted (finding 10)


# ----------------------------------------------------------------------------------------------
# Checkers for the stability claims (finding 18)
# ----------------------------------------------------------------------------------------------

def _stability_model():
    return PairModel(unary=[np.array([0, 10, 1]), np.array([0, 5]), np.array([2, 0, 3])],
                     pair={(0, 1): np.array([[0, 2], [1, 0], [0, 1]]), (1, 2): np.array([[0, 1, 2], [3, 0, 1]])},
                     scale_bits=1)


def _brute(model, allowed=lambda x: True):
    energies = {x: model.energy(x) for x in itertools.product(*[range(k) for k in model.sizes]) if allowed(x)}
    best = min(energies.values())
    return best, min(x for x, e in energies.items() if e == best)


def test_honest_exclusion_gaps_pass_their_checker_and_carry_the_enumerated_gap():
    model = _stability_model()
    e_star, x_star = _brute(model)
    for exclude in ({i: {x_star[i]} for i in range(model.n)}, {0: {x_star[0], 1}, 2: {0, 1, 2}}):
        gaps = stability.certify_exclusion_gaps(model, x_star, exclude)
        for gap in gaps:
            ok, reason = stability.check_exclusion_gap(model, x_star, gap.site, exclude[gap.site], gap)
            assert ok, reason
            if gap.gap is None:
                assert set(exclude[gap.site]) >= set(range(model.sizes[gap.site]))
            else:
                truth, _ = _brute(model, lambda x: x[gap.site] not in exclude[gap.site])
                assert gap.gap == truth - e_star


def test_exclusion_gap_checker_refuses_a_tampered_box_another_model_and_a_wrong_gap():
    model = _stability_model()
    e_star, x_star = _brute(model)
    site, excluded = 0, {x_star[0]}
    (honest,) = stability.certify_exclusion_gaps(model, x_star, {site: excluded})
    check = stability.check_exclusion_gap
    assert check(model, x_star, site, excluded, honest) == (True, "ok")

    def refused(gap, *words, model=model, x_star=x_star, site=site, excluded=excluded):
        ok, reason = check(model, x_star, site, excluded, gap)
        assert ok is False and reason and all(w in reason for w in words), (ok, reason)
        return True

    # a certificate that is true, accepted and tight — on a box with one more state removed
    smaller = [list(d) for d in honest.certificate.domains]
    smaller[site] = smaller[site][:-1]
    cert = certify_gmec(model, eps=Fraction(0), domains=smaller)
    assert check_min_certificate(cert).accepted
    tampered = stability.FlipGap(site=site, gap=cert.lower_bound_fraction() - e_star, alternative=cert.witness,
                                 certificate=cert)
    assert refused(tampered, "box")
    # ... or on a box in which another site lost a state
    other_site = [list(d) for d in honest.certificate.domains]
    other_site[2] = other_site[2][1:]
    cert = certify_gmec(model, eps=Fraction(0), domains=other_site)
    assert refused(stability.FlipGap(site, cert.lower_bound_fraction() - e_star, cert.witness, cert), "box")
    # ... or on the full box (nothing excluded)
    cert = certify_gmec(model, eps=Fraction(0))
    assert refused(stability.FlipGap(site, cert.lower_bound_fraction() - e_star, cert.witness, cert), "box")
    # a certificate about another model (one table entry differs)
    other = _stability_model()
    other.unary[1][1] += 1
    (foreign,) = stability.certify_exclusion_gaps(other, x_star, {site: excluded})
    assert refused(foreign, "instance")
    # a wrong gap, a wrong alternative, a claim about another site, a certificate with slack
    assert refused(dataclasses.replace(honest, gap=honest.gap + Fraction(1, 2)), "gap")
    assert refused(dataclasses.replace(honest, gap=honest.gap - Fraction(1, 2)), "gap")
    assert refused(dataclasses.replace(honest, alternative=x_star), "alternative")
    assert refused(dataclasses.replace(honest, alternative=None), "alternative")
    assert refused(dataclasses.replace(honest, alternative=(-1, 0, 0)), "alternative")
    assert refused(dataclasses.replace(honest, site=1), "site")
    assert refused(honest, "box", excluded={x_star[0], 1})
    slack = certify_gmec(model, eps=Fraction(1), domains=honest.certificate.domains)
    slack.lower_bound -= 1
    assert check_min_certificate(slack).accepted and check_min_certificate(slack).certified_gap > 0
    assert refused(stability.FlipGap(site, slack.lower_bound_fraction() - e_star, slack.witness, slack), "zero")
    rejected = dataclasses.replace(honest.certificate, lower_bound=honest.certificate.lower_bound + 1)
    assert refused(dataclasses.replace(honest, certificate=rejected), "rejected")
    assert refused(dataclasses.replace(honest, certificate=None))
    assert refused(None) and refused("gap")
    # a site all of whose states are excluded has no gap; claiming one, or claiming none when a state is left, is refused
    everything = set(range(model.sizes[site]))
    (none_left,) = stability.certify_exclusion_gaps(model, x_star, {site: everything})
    assert none_left.gap is None and check(model, x_star, site, everything, none_left) == (True, "ok")
    assert refused(honest, excluded=everything)
    assert refused(none_left)
    # malformed arguments are a refusal, not an exception
    assert check(model, (-1, 0, 0), site, excluded, honest)[0] is False
    assert check(model, x_star, 7, excluded, honest)[0] is False
    assert check("model", x_star, site, excluded, honest)[0] is False


def test_the_producers_of_stability_claims_refuse_to_return_a_claim_that_fails_its_checker():
    """`certify_exclusion_gaps` / `certify_flip_gaps` / `certify_necessary_optimality` hand out
    checked claims only: with a producer that silently drops a state (or minimises another table)
    they raise `StabilityCheckFailed` instead of returning a number."""
    model = _stability_model()
    _, x_star = _brute(model)
    honest = stability.certify_gmec

    def drops_a_state(model, eps=Fraction(0), domains=None, **options):
        domains = [list(d) for d in (model.full_domains() if domains is None else domains)]
        for i, d in enumerate(domains):
            if len(d) > 1:
                domains[i] = d[:-1]
                break
        return honest(model, eps=eps, domains=domains, **options)

    def another_table(model, eps=Fraction(0), **options):
        other = PairModel([u + 1 for u in model.unary], {k: t.copy() for k, t in model.pair.items()},
                          scale_bits=model.scale_bits)
        return honest(other, eps=eps, **options)

    assert issubclass(stability.StabilityCheckFailed, RuntimeError)
    for faulty in (drops_a_state, another_table):
        stability.certify_gmec = faulty
        try:
            with pytest.raises(stability.StabilityCheckFailed):
                stability.certify_flip_gaps(model, x_star, sites=[0])
            with pytest.raises(stability.StabilityCheckFailed):
                stability.certify_exclusion_gaps(model, x_star, {1: {x_star[1]}})
            with pytest.raises(stability.StabilityCheckFailed):
                stability.certify_necessary_optimality(model, x_star, 1)
        finally:
            stability.certify_gmec = honest
    assert len(stability.certify_flip_gaps(model, x_star)) == 3          # the honest producer is unaffected


def test_necessary_optimality_checker_accepts_honest_verdicts_and_refuses_tampered_ones():
    model = _stability_model()
    _, x_star = _brute(model)
    check = stability.check_necessary_optimality
    seen = set()
    for b in (0, 1, 2, 5, ([[0, 1, 0], [1, 0], [0, 0, 2]], {(0, 1): [[1, 0], [0, 0], [0, 1]], (1, 2): [[0, 0, 0], [0, 1, 0]]})):
        verdict = stability.certify_necessary_optimality(model, x_star, b)
        assert check(model, x_star, b, verdict) == (True, "ok")
        shifted = stability.shifted_model(model, x_star, b)
        truth, _ = _brute(shifted)
        assert verdict.margin == truth - shifted.energy(x_star) and verdict.holds is (verdict.margin == 0)
        seen.add(verdict.holds)

        def refused(candidate, *words, b=b, x=x_star, m=model):
            ok, reason = check(m, x, b, candidate)
            assert ok is False and reason and all(w in reason for w in words), (ok, reason)
            return True

        assert refused(dataclasses.replace(verdict, holds=not verdict.holds), "holds")
        assert refused(dataclasses.replace(verdict, margin=verdict.margin - 1), "margin")
        assert refused(dataclasses.replace(verdict, margin=verdict.margin + Fraction(1, 2)), "margin")
        if verdict.holds:
            assert refused(dataclasses.replace(verdict, counterexample=x_star), "counterexample")
        else:
            assert refused(dataclasses.replace(verdict, counterexample=None), "counterexample")
            assert refused(dataclasses.replace(verdict, counterexample=x_star), "counterexample")
            scenario = verdict.scenario()
            assert scenario.energy(verdict.counterexample) < scenario.energy(x_star)
        # the certificate must be about the shifted model of exactly these arguments
        assert refused(verdict, "shifted", b=7)
        other_x = tuple((a + 1) % k for a, k in zip(x_star, model.sizes))
        assert refused(verdict, x=other_x)
        other = _stability_model()
        other.unary[2][2] += 1
        assert refused(verdict, m=other)
        # ... over the full box, with zero gap
        sub = shifted.full_domains()
        sub[0] = [x_star[0]]
        cert = certify_gmec(shifted, eps=Fraction(0), domains=sub)
        margin = cert.lower_bound_fraction() - shifted.energy(x_star)
        assert refused(dataclasses.replace(verdict, certificate=cert, margin=margin, holds=margin == 0,
                                           counterexample=None if margin == 0 else cert.witness), "full")
        rejected = dataclasses.replace(verdict.certificate, lower_bound=verdict.certificate.lower_bound + 1)
        assert refused(dataclasses.replace(verdict, certificate=rejected), "rejected")
        assert refused(None) and refused(dataclasses.replace(verdict, certificate=None))
    assert seen == {True, False}
    assert check(model, (0, 0), 1, verdict)[0] is False and check(model, x_star, -1, verdict)[0] is False
    assert check(model, x_star, 1.5, verdict)[0] is False


def test_error_bounds_and_configurations_of_the_stability_functions_are_exact_integers_or_refused():
    """Finding 5 and the Engineering note on silent truncation: the shift is done in Python
    integers (no wrap at 2**63), and a bound that is not an integer is refused, not truncated."""
    big = 2 ** 63 - 1
    model = PairModel(unary=[np.array([big, 5], dtype=object), np.array([0, 1])],
                      pair={(0, 1): np.array([[0, big], [1, 2]], dtype=object)}, scale_bits=0)
    shifted = stability.shifted_model(model, (0, 1), ([[big, 3], [1, 2 ** 70]], {(0, 1): [[1, big], [big, 2 ** 64]]}))
    assert [int(v) for v in shifted.unary[0]] == [2 * big, 2] and [int(v) for v in shifted.unary[1]] == [-1, 1 + 2 ** 70]
    assert [[int(v) for v in row] for row in shifted.pair[(0, 1)]] == [[-1, 2 * big], [1 - big, 2 - 2 ** 64]]
    small = _stability_model()
    for bad in (1.5, "1", None, True, Fraction(1, 2), ([[0.5, 0, 0], [0, 0], [0, 0, 0]], {}), -1,
                ([[0, 0, 0], [0, 0], [0, 0, 0]], {(0, 1): [[0, 0], [0, 0], [0, 0]]}),          # a pair table is missing
                ([[0, 0], [0, 0], [0, 0, 0]], {(0, 1): [[0, 0], [0, 0], [0, 0]], (1, 2): [[0, 0, 0], [0, 0, 0]]})):
        with pytest.raises(ValueError):
            stability.shifted_model(small, (0, 0, 0), bad)
    for bad_x in ((0, 0), (0, 0, 3), (0, -1, 0), (0, 0.0, 0), "000", {0: 0, 1: 0, 2: 0}):
        with pytest.raises(ValueError):
            stability.shifted_model(small, bad_x, 1)
        with pytest.raises(ValueError):
            stability.certify_exclusion_gaps(small, bad_x, {0: {0}})
        with pytest.raises(ValueError):
            small.energy(bad_x)
    with pytest.raises(ValueError):
        stability.certify_exclusion_gaps(small, (0, 0, 0), {5: {0}})          # no such site
    with pytest.raises(ValueError):
        stability.certify_exclusion_gaps(small, (0, 0, 0), {0: {7}})          # no such state
    for bad_witness in ((0, 0), (0, 0, 3), (0, -1, 0), (0, 0.5, 0), "000"):
        with pytest.raises(ValueError):
            certify_gmec(small, witness=bad_witness)
    assert check_min_certificate(certify_gmec(small, witness=(2, 1, 2))).accepted


def test_weighted_model_adds_the_weights_in_exact_integers_and_refuses_a_table_outside_the_supported_range():
    """Suspected by the reviewer, untested until now: `weighted_model` added the rounded
    -(1/beta) ln(weight) to one-body tables in int64.  The sum is now formed in Python integers and
    a result of 2**62 or more in absolute value — the limit below which `PairModel` and the
    instance files hold a table as int64 — is refused."""
    beta = Fraction(1)
    edge = 2 ** 62 - 1
    model = PairModel(unary=[np.array([edge - 7, -edge + 7, 0])], pair={}, scale_bits=0)
    weights = [[float(np.exp(-7.0)), float(np.exp(7.0)), 1.0]]
    weighted = weighted_model(model, weights, beta)                 # exactly at the edge: still representable
    assert [int(v) for v in weighted.unary[0]] == [edge, -edge, 0]
    for too_far in ([[float(np.exp(-8.0)), 1.0, 1.0]], [[1.0, float(np.exp(8.0)), 1.0]]):
        with pytest.raises(ValueError):
            weighted_model(model, too_far, beta)
    huge = PairModel(unary=[np.array([2 ** 63 - 5, 0], dtype=object)], pair={}, scale_bits=0)
    with pytest.raises(ValueError):
        weighted_model(huge, [[0.5, 0.5]], beta)
    with pytest.raises(ValueError):
        weighted_model(model, [[1e-300, 1.0, 1.0]], Fraction(1, 10 ** 400))      # the shift itself is not finite
