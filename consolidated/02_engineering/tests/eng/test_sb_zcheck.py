"""Tests of the independent checker for ``structbio-zcert/1`` (``experiments/eng/sb_zcheck/indep_zcheck.py``) and
regression tests of what was found in the structural-biology division's checker at its commit 0544ff4.

Layers:

  1. ``indep_zcheck`` alone (no other package needed): certificates of the producer of ``gen`` against 400-bit
     enumeration (``ln Z`` and every population), the rounded mode and the Taylor exponential against the default
     mode, every adversarial variant, the strict loader, deep nesting, fuzz ("never an internal error"), the two
     exponential enclosures against each other and against mpmath, and the freeze record;
  2. the reviewed package, imported from a read-only checkout (``$SB_CHECKOUT``, default: ``MetricChain-sb-0544ff4``
     next to this repository; the tests are skipped when it is absent): a differential run on small instances
     (their checker in both tiers, ours, enumeration), and the findings as regression tests.  A finding that is
     still present is reported as ``xfail`` with its description, so that the file passes as it stands and starts
     passing plainly when the defect is corrected.

Nothing of the reviewed package is copied here.  The whole file runs in well under a minute.
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "eng" / "sb_zcheck"
sys.path.insert(0, str(EXP))

import gen  # noqa: E402
import indep_zcheck as Z  # noqa: E402
import sb_bridge as B  # noqa: E402
import truth  # noqa: E402

needs_sb = pytest.mark.skipif(not B.available(), reason="no checkout of the reviewed package (set SB_CHECKOUT)")

TOY = {"unary": [[0, 3, 5], [1, -2]], "pair": {(0, 1): [[0, 1], [2, -3], [4, 5]]}, "scale_bits": 2}


def _model(tables):
    return Z.make_model(tables["unary"], tables["pair"], tables["scale_bits"])


def _truth(tables, doc):
    return truth.enumerate_truth(tables["unary"], tables["pair"], tables["scale_bits"], Fraction(doc["beta"]),
                                 doc["domains"])


def _toy_text():
    sha = Z.model_sha256(_model(TOY))
    return ('{"format":"structbio-zcert/1","model_sha256":"%s","beta":"3/7","domains":[[0,1,2],[0,1]],"keep":null,'
            '"claim":{},"root":{"steps":[{"op":"prune","site":0,"remove":2,"dominator":0},{"op":"relax","pair":[0,1],'
            '"f":[0,1,0],"g":[0,0]}],"order":[1,0]},"meta":"{}"}' % sha), sha


# ------------------------------------------------------------------------------------------- 1. indep_zcheck alone

def test_checker_is_the_frozen_one():
    record = json.loads((EXP / "results" / "freeze.json").read_text())
    assert hashlib.sha256((EXP / "indep_zcheck.py").read_bytes()).hexdigest() == record["indep_zcheck_sha256_at_freeze"]


def test_checksum_is_the_one_their_serialiser_wrote():
    # the value printed by their ``zcert.dumps`` for this instance (observed before the freeze)
    assert Z.model_sha256(_model(TOY)) == "d2794bffbf0fab023d0303b0280dc372c2abd28f2e1de0bd0b83531ac8d8e48b"


def test_own_certificates_against_enumeration():
    rng = random.Random(2026)
    accepted = pops = 0
    for case in range(150):
        tables = gen.random_tables(rng)
        model = _model(tables)
        doc = gen.random_certificate(rng, tables, Z.model_sha256(model))
        text = gen.dumps(doc)
        res = Z.check_text(text, model)
        rounded = Z.check_text(text, model, round_bits=96)
        assert res.kind in ("ok", "abstain") and rounded.accepted, (res.reason, rounded.reason, text)
        tr = _truth(tables, doc)
        for r in ([res, rounded] if res.accepted else [rounded]):
            assert tr.ln_z_contains(r.ln_z_lo, r.ln_z_hi) == "yes", text
            if doc["keep"] is not None:
                for a in range(len(tables["unary"][doc["keep"]])):
                    lo, hi = r.population(a)
                    assert tr.pop_contains(doc["keep"], a, lo, hi) == "yes", (a, text)
                    pops += 1
        if res.accepted:
            accepted += 1
            assert res.ideal_lo[1] - res.ideal_lo[0] < Fraction(1, 10 ** 60)
            assert res.ideal_hi[1] - res.ideal_hi[0] < Fraction(1, 10 ** 60)
            tol = Fraction(1, 2 ** 280)                       # the rounded mode contains the exact one
            assert rounded.ln_z_lo <= res.ln_z_lo + tol and res.ln_z_hi <= rounded.ln_z_hi + tol
            if case % 5 == 0:                                  # the Taylor exponential (no library) agrees
                tay = Z.check_text(text, model, exp_impl="taylor", exp_bits=128)
                assert tay.accepted and tr.ln_z_contains(tay.ln_z_lo, tay.ln_z_hi) == "yes"
                assert max(tay.ideal_lo[0], res.ideal_lo[0]) <= min(tay.ideal_lo[1], res.ideal_lo[1])
                assert max(tay.ideal_hi[0], res.ideal_hi[0]) <= min(tay.ideal_hi[1], res.ideal_hi[1])
    assert accepted > 100 and pops > 100


def test_adversarial_variants_are_rejected_or_sound():
    rng = random.Random(7)
    seen = set()
    for case in range(80):
        tables = gen.random_tables(rng)
        model = _model(tables)
        doc = gen.random_certificate(rng, tables, Z.model_sha256(model))
        for name, expect, variant in gen.variants(rng, doc, tables):
            res = Z.check_text(gen.dumps(variant), model, round_bits=128)
            assert res.kind != "internal", (name, res.reason)
            seen.add(name)
            if expect == "invalid":
                assert not res.accepted and res.kind in ("malformed", "invalid"), (name, gen.dumps(variant))
            if expect == "valid":
                assert res.accepted, (name, res.reason)
            if res.accepted:
                tr = _truth(tables, variant)
                assert tr.ln_z_contains(res.ln_z_lo, res.ln_z_hi) == "yes", (name, gen.dumps(variant))
    assert len(seen) >= 40


def test_strict_loader():
    good, sha = _toy_text()
    model = _model(TOY)
    assert Z.check_text(good, model).accepted
    cases = [
        (good.replace('"keep":null', '"keep":null,"keep":null'), "malformed"),          # duplicate key
        (good.replace('"site":0,', '"site":0,"site":0,'), "malformed"),
        (good.replace('"beta":"3/7"', '"beta":0.5'), "malformed"),                      # float
        (good.replace('"beta":"3/7"', '"beta":"6/14"'), "malformed"),                   # not in lowest terms
        (good.replace('"beta":"3/7"', '"beta":"+3/7"'), "malformed"),
        (good.replace('"beta":"3/7"', '"beta":"--3/7"'), "malformed"),
        (good.replace('"beta":"3/7"', '"beta":"-0/1"'), "malformed"),
        (good.replace('"beta":"3/7"', '"beta":"-3/7"'), "invalid"),                     # negative beta
        (good.replace('"site":0', '"site":0.0'), "malformed"),
        (good.replace('"site":0', '"site":false'), "malformed"),                        # boolean
        (good.replace('"site":0', '"site":"0"'), "malformed"),                          # string
        (good.replace('"site":0', '"site":-0'), "malformed"),
        (good.replace('"remove":2', '"remove":NaN'), "malformed"),
        (good.replace('"remove":2', '"remove":Infinity'), "malformed"),
        (good.replace('"meta":"{}"', '"meta":"{}","extra":1'), "malformed"),            # unknown fields
        (good.replace('"dominator":0', '"dominator":0,"margin":5'), "malformed"),
        (good.replace('"order":[1,0]', '"order":[1,0],"note":1'), "malformed"),
        (good.replace(',"meta":"{}"', ''), "malformed"),                                # missing field
        (good.replace(sha, "0" * 64), "malformed"),                                     # wrong checksum
        (good[:-5], "malformed"),                                                       # truncated
        (good + "x", "malformed"),
        ("[" + good + "]", "malformed"),
        (good.replace('"claim":{}', '"claim":{"ln_z_lo":"-10/1"}'), "malformed"),
        (good.replace('"claim":{}', '"claim":{"ln_z_lo":"6/5","ln_z_hi":"10/1"}'), "claim"),
        (good.replace('"remove":2', '"remove":' + "9" * 5000), "abstain"),
        (good.replace('"domains":[[0,1,2],[0,1]]', '"domains":[[0,2,1],[0,1]]'), "malformed"),
        (good.replace('"domains":[[0,1,2],[0,1]]', '"domains":[[0,1,1],[0,1]]'), "malformed"),
        (good.replace('"domains":[[0,1,2],[0,1]]', '"domains":[[0,1,2],[]]'), "invalid"),
    ]
    for text, kind in cases:
        assert Z.check_text(text, model).kind == kind, text
    assert Z.check_text(good.replace(",", " ,\n"), model).accepted                      # whitespace is free
    assert Z.check_text(good.replace('"claim":{}', '"claim":{"ln_z_lo":"-10/1","ln_z_hi":"10/1"}'), model).accepted
    for not_text in (None, 5, b"{}", []):
        assert Z.check_text(not_text, model).kind == "malformed"


def test_deep_nesting_and_degenerate_models():
    m1 = Z.make_model([[0, 1]], {}, 0)
    sha = Z.model_sha256(m1)
    for depth in (10, 990, 3000):
        node = {"steps": [], "order": [0]}
        for _ in range(depth):
            node = {"steps": [], "branch": 0, "children": {"0": node}}
        doc = {"format": Z.FORMAT_TAG, "model_sha256": sha, "beta": "1/1", "domains": [[0]], "keep": None,
               "claim": {}, "root": node, "meta": "{}"}
        res = Z.check_document(doc, m1)
        assert res.accepted and res.ln_z_lo == res.ln_z_hi == 0, depth
    text = ('{"format":"structbio-zcert/1","model_sha256":"%s","beta":"1/1","domains":[[0]],"keep":null,"claim":{},'
            '"root":' % sha + '{"steps":[],"branch":0,"children":{"0":' * 20000 + '{"steps":[],"order":[0]}'
            + '}}' * 20000 + ',"meta":"{}"}')
    assert Z.check_text(text, m1).kind == "abstain"                    # the JSON parser's limit: a refusal, no error
    m0 = Z.make_model([], {}, 0)                                       # no site: Z = 1
    doc = {"format": Z.FORMAT_TAG, "model_sha256": Z.model_sha256(m0), "beta": "1/1", "domains": [], "keep": None,
           "claim": {}, "root": {"steps": [], "order": []}, "meta": "{}"}
    res = Z.check_document(doc, m0)
    assert res.accepted and res.ln_z_lo == res.ln_z_hi == 0


def test_never_an_internal_error():
    good, _ = _toy_text()
    model = _model(TOY)
    rng = random.Random(11)
    alphabet = '{}[]:,"0123456789-+.eE/ \n\\untrfalsNaIiy' + "prunerelax"
    kinds = set()
    for _ in range(4000):
        s = list(good)
        for _ in range(rng.randint(1, 4)):
            op, pos = rng.randrange(3), rng.randrange(len(s))
            if op == 0:
                s[pos] = rng.choice(alphabet)
            elif op == 1:
                del s[pos]
            else:
                s.insert(pos, rng.choice(alphabet))
        text = "".join(s)
        res = Z.check_text(text, model)
        kinds.add(res.kind)
        assert res.kind != "internal", (res.reason, text)
        if res.accepted:
            d = json.loads(text)
            assert _truth(TOY, d).ln_z_contains(res.ln_z_lo, res.ln_z_hi) == "yes", text
    base = json.loads(good)
    for _ in range(2000):                                               # documents with values of other types
        doc = json.loads(good)
        target, key = doc, None
        for _ in range(rng.randint(1, 4)):
            if isinstance(target, dict) and target:
                parent, key = target, rng.choice(list(target))
            elif isinstance(target, list) and target:
                parent, key = target, rng.randrange(len(target))
            else:
                break
            target = parent[key]
        parent[key] = rng.choice([None, True, 1.5, float("nan"), "0", b"x", (1, 2), [], {}, [[0]], {"op": "prune"},
                                  2 ** 70, -1, {0: 1}, object()])
        assert Z.check_document(doc, model).kind != "internal"
    assert base == json.loads(good) and {"ok", "malformed"} <= kinds


def test_exponential_and_logarithm_enclosures():
    import mpmath
    rng = random.Random(99)
    for _ in range(600):
        q = Fraction(rng.randint(-10 ** rng.randint(1, 30), 10 ** rng.randint(1, 30)), rng.randint(1, 10 ** rng.randint(0, 20)))
        bits = rng.choice([16, 64, 256])
        for coarse, fine in ((Z.exp_enclosure_arb, Z.exp_enclosure_taylor), (Z.exp_enclosure_taylor, Z.exp_enclosure_arb)):
            c_lo, c_hi = coarse(q, bits)
            f_lo, f_hi = fine(q, bits + 120)
            assert Z._dy_le(c_lo, c_hi) and Z._dy_le(c_lo, f_hi) and Z._dy_le(f_lo, c_hi), (q, bits)
            assert Z._dy_le((c_hi[0] << bits, c_hi[1]), (c_lo[0] * ((1 << bits) + 1), c_lo[1])), (q, bits)   # width
        if abs(q) < 10 ** 6:
            with mpmath.workdps(60):
                v = mpmath.exp(mpmath.mpf(q.numerator) / q.denominator)
                lo, hi = Z.exp_enclosure_arb(q, 64)
                assert mpmath.mpf(lo[0]) * mpmath.mpf(2) ** lo[1] <= v * (1 + mpmath.mpf(10) ** -40)
                assert mpmath.mpf(hi[0]) * mpmath.mpf(2) ** hi[1] >= v * (1 - mpmath.mpf(10) ** -40)
    for _ in range(100):
        m, e = rng.randint(1, 10 ** rng.randint(1, 60)), rng.randint(-10 ** 9, 10 ** 9)
        lo, hi = Z.ln_enclosure((m, e), 128)
        lo2, hi2 = Z.ln_enclosure((m, e), 128, "taylor")              # certified through the Taylor exponential
        assert lo2 <= lo <= hi <= hi2
        with mpmath.workdps(80):
            v = mpmath.log(m) + e * mpmath.log(2)
            assert abs(mpmath.mpf(lo.numerator) / lo.denominator - v) < abs(v) * mpmath.mpf(10) ** -30 + mpmath.mpf(10) ** -30


# ------------------------------------------------------------------------------------- 2. the reviewed package

def _f1():
    tables = {"unary": [[0, 678], [0]], "pair": {(0, 1): [[677], [0]]}, "scale_bits": 0}
    model = _model(tables)
    doc = {"format": Z.FORMAT_TAG, "model_sha256": Z.model_sha256(model), "beta": "1/1", "domains": [[0, 1], [0]],
           "keep": None, "claim": {}, "root": {"steps": [], "order": [1, 0]}, "meta": "{}"}
    return tables, model, doc, gen.dumps(doc)


@needs_sb
def test_differential_on_small_instances():
    """Their checker (both tiers), ours and enumeration on certificates of their producer, of ``gen`` and variants."""
    rng = random.Random(4242)
    S = B.sb()
    counts = {"theirs": 0, "mine": 0, "both": 0, "float": 0}
    allowed = ("domain_not_sorted", "branch_surplus_child_outside_domain", "relax_pair_reversed")
    for index in range(45):
        tables = gen.random_tables(rng)
        gen.temper(rng, tables, max(gen.BETAS), 600)
        sizes = [len(u) for u in tables["unary"]]
        pm, model = B.pair_model(tables), _model(tables)
        sha = Z.model_sha256(model)
        assert sha == S["mincert"].model_sha256(pm)
        items = []
        try:
            cert = S["partition"].certify_partition(pm, rng.choice(gen.BETAS), domains=gen.random_box(rng, sizes),
                                                    keep=rng.choice([None, 0]), tau=rng.choice([None, 2]),
                                                    theta=rng.choice([None, 1]), max_entries=rng.choice([4, 10 ** 6]),
                                                    max_leaves=64)
            items.append(("their producer", json.loads(S["zcert"].dumps(cert))))
        except S["partition"].PartitionBudgetExceeded:
            pass
        doc = gen.random_certificate(rng, tables, sha, max_prune_kt=12, wild_kt=200)
        items.append(("gen producer", doc))
        items.extend((name, variant) for name, _, variant in gen.variants(rng, doc, tables))
        for name, d in items:
            hz = gen.hazard(d, tables)
            if hz is not None and Fraction(d["beta"]) >= 0 and (hz[0] > 14 or hz[1] > 30000 or hz[2] > 30000):
                continue                                   # their checker would need gigabytes (finding F3)
            text = gen.dumps(d)
            my = Z.check_text(text, model, round_bits=None if hz is None or max(hz) < 15000 else 256)
            assert my.kind != "internal", (name, my.reason)
            th = B.their_check_text(text, pm, "exact")
            assert th["exception"] is None, (name, th["exception"])
            assert th["load_error"] is None or th["load_error"].startswith("malformed"), (name, th["load_error"])
            if th["accepted"] != my.accepted:
                assert any(key in name for key in allowed), (name, th["reason"], my.reason, text)
            if not (th["accepted"] or my.accepted):
                continue
            box = [sorted(set(dom)) for dom in d["domains"]]
            tr = truth.enumerate_truth(tables["unary"], tables["pair"], tables["scale_bits"], Fraction(d["beta"]), box)
            keep = d["keep"]
            if my.accepted:
                counts["mine"] += 1
                assert tr.ln_z_contains(my.ln_z_lo, my.ln_z_hi) == "yes", (name, text)
            if th["accepted"]:
                counts["theirs"] += 1
                assert tr.ln_z_contains(th["lo"], th["hi"]) == "yes", (name, text)          # claim Z1
                if keep is not None:
                    for a in range(sizes[keep]):
                        lo, hi = B.their_population(th, a)
                        assert tr.pop_contains(keep, a, lo, hi) == "yes", (name, a, text)   # claim Z2
                doc2 = dict(d)
                doc2["claim"] = {}
                fl = B.their_check_text(gen.dumps(doc2), pm, "float")
                assert fl["exception"] is None
                if fl["accepted"]:
                    counts["float"] += 1
                    assert tr.ln_z_contains(fl["lo"], fl["hi"]) == "yes", (name, text)
            if th["accepted"] and my.accepted:
                counts["both"] += 1
                assert th["lo"] <= my.ideal_lo[1] and my.ideal_hi[0] <= th["hi"], (name, text)   # what the rules prove
                assert th["lo"] <= my.ln_z_lo and my.ln_z_hi <= th["hi"], (name, text)           # ours inside theirs
    assert counts["both"] > 150 and counts["float"] > 150, counts


@needs_sb
def test_finding_f1_float_tier_with_large_exp_bits():
    """F1 (critical): with ``exp_bits = 990`` their float tier accepts this certificate and returns an interval
    0.31 nats below ``ln Z`` (``FloatTables._ldexp_up`` returns 1e-300 for a weight that is larger)."""
    tables, model, doc, text = _f1()
    tr = _truth(tables, doc)
    mine = Z.check_text(text, model)
    assert mine.accepted and tr.ln_z_contains(mine.ln_z_lo, mine.ln_z_hi) == "yes"
    pm = B.pair_model(tables)
    for tier, bits in (("exact", 64), ("float", 64), ("exact", 990)):
        r = B.their_check_text(text, pm, tier, exp_bits=bits)
        assert r["accepted"] and tr.ln_z_contains(r["lo"], r["hi"]) == "yes", (tier, bits)
    r = B.their_check_text(text, pm, "float", exp_bits=990)
    if r["accepted"] and tr.ln_z_contains(r["lo"], r["hi"]) == "no":
        pytest.xfail(f"finding F1 is present: float tier, exp_bits=990 accepts [{float(r['lo']):.6f}, "
                     f"{float(r['hi']):.6f}] while ln Z = {tr.ln_z.str(12)}")
    assert not r["accepted"] or tr.ln_z_contains(r["lo"], r["hi"]) == "yes"


@needs_sb
def test_finding_f2_float_interval_does_not_contain_exact_interval():
    """F2 (claim Z3 as stated): on the same certificate the float tier's interval is not always a superset of the
    exact tier's (both contain the truth; the final ``log_bounds`` is not monotone)."""
    rng = random.Random(1)
    S = B.sb()
    for _ in range(40):
        tables = gen.random_tables(rng, n=4, kmax=3, graph="dense", amp="medium")
        gen.temper(rng, tables, Fraction(1), 300)
        pm = B.pair_model(tables)
        cert = S["partition"].certify_partition(pm, Fraction(1, 2))
        cert.claim = {}
        text = S["zcert"].dumps(cert)
        ex, fl = B.their_check_text(text, pm, "exact"), B.their_check_text(text, pm, "float")
        assert ex["accepted"] and fl["accepted"]
        tr = truth.enumerate_truth(tables["unary"], tables["pair"], tables["scale_bits"], Fraction(1, 2), cert.domains)
        assert tr.ln_z_contains(ex["lo"], ex["hi"]) == "yes" and tr.ln_z_contains(fl["lo"], fl["hi"]) == "yes"
        if not (fl["lo"] <= ex["lo"] and ex["hi"] <= fl["hi"]):
            pytest.xfail("finding F2 is present: a float-tier interval that does not contain the exact-tier interval "
                         f"(lower ends differ by {float(fl['lo'] - ex['lo']):.2e})")


@needs_sb
def test_finding_f3_prune_with_negative_margin_is_sound_but_loose():
    """F3: a prune with margin -10 kT is charged ``exp(-beta m)`` instead of ``ln(1 + exp(-beta m))``: sound, and
    22000 nats wide where the rule proves 5e-5 (below about -20 kT the same step needs gigabytes; not run here)."""
    tables = {"unary": [[0, 10]], "pair": {}, "scale_bits": 0}
    model = _model(tables)
    doc = {"format": Z.FORMAT_TAG, "model_sha256": Z.model_sha256(model), "beta": "1/1", "domains": [[0, 1]],
           "keep": None, "claim": {}, "root": {"steps": [{"op": "prune", "site": 0, "remove": 0, "dominator": 1}],
                                               "order": [0]}, "meta": "{}"}
    text = gen.dumps(doc)
    tr = _truth(tables, doc)
    mine = Z.check_text(text, model)
    th = B.their_check_text(text, B.pair_model(tables), "exact")
    assert mine.accepted and th["accepted"]
    assert tr.ln_z_contains(mine.ln_z_lo, mine.ln_z_hi) == "yes" and tr.ln_z_contains(th["lo"], th["hi"]) == "yes"
    assert mine.ln_z_hi < Fraction(1, 10 ** 4) and th["hi"] >= mine.ideal_hi[0]


@needs_sb
def test_finding_f4_loader_raises_other_exceptions():
    """F4: their loader raises ``ValueError``/``RecursionError`` instead of ``MalformedZCertificate`` on some files."""
    tables = {"unary": [[0, 1]], "pair": {}, "scale_bits": 0}
    model = _model(tables)
    pm = B.pair_model(tables)
    doc = {"format": Z.FORMAT_TAG, "model_sha256": Z.model_sha256(model), "beta": "1/1", "domains": [[0, 1]],
           "keep": None, "claim": {}, "root": {"steps": [], "order": [0]}, "meta": "{}"}
    base = gen.dumps(doc)
    assert B.their_load(base, pm)[0] is not None and Z.check_text(base, model).accepted
    bad = [base.replace('"1/1"', '"--5/3"'), base.replace('"1/1"', '"%s/1"' % ("9" * 5000)),
           base.replace('"meta":"{}"', '"meta":"%s"' % ("[" * 100000))]
    raised = []
    for text in bad:
        assert Z.check_text(text, model).kind in ("malformed", "abstain", "ok")
        cert, err = B.their_load(text, pm)
        assert cert is None
        if err.startswith("EXC"):
            raised.append(err.split(":")[0])
    if raised:
        pytest.xfail(f"finding F4 is present: their loader raised {sorted(set(raised))} on malformed files")
