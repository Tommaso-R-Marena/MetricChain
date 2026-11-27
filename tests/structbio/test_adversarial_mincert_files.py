"""Adversarial review STRUCTBIO-REV-0001 — the file format `structbio-mincert/1` (`mincert.loads`)
and the conversion to `metricchain-cert/1`.

``FINDING`` tests fail with the reviewed code and are left red; ``SURVIVED`` tests pass.
"""
import json
import sys

import numpy as np
import pytest

from metricchain_sb import mincert
from metricchain_sb.mincert import MalformedCertificate, MinCertificate, to_metricchain_cert1
from metricchain_sb.mincheck import check_min_certificate
from metricchain_sb.model import PairModel


def _model():
    return PairModel(unary=[np.array([0, 1, 4]), np.array([0, 2])],
                     pair={(0, 1): np.array([[0, 1], [1, 0], [3, 3]])}, scale_bits=1)


def _certificate(model=None):
    model = _model() if model is None else model
    leaf_a = {"node": "leaf", "m": {(0, 1): [0, 0, 0], (1, 0): [0, 0]}}
    leaf_b = {"node": "leaf", "m": {}}
    root = {"node": "prune", "site": 0, "remove": 2, "dominator": 0,
            "rest": {"node": "branch", "site": 0, "children": {0: leaf_a, 1: leaf_b}}}
    return MinCertificate(model=model, message_bits=1, domains=model.full_domains(), lower_bound=0,
                          witness=(0, 0), root=root)


def _text():
    return mincert.dumps(_certificate())


def _edit(path, value, text=None):
    """The file with the entry at `path` replaced (`...` deletes it); re-serialised compactly."""
    doc = json.loads(_text() if text is None else text)
    target = doc
    for key in path[:-1]:
        target = target[key]
    if value is ...:
        del target[path[-1]]
    else:
        target[path[-1]] = value
    return json.dumps(doc, separators=(",", ":"))


LEAF = {"node": "leaf", "m": {}}
BRANCH = ("certificate", "rest")                     # path of the branch node in the file
LEAF_A = BRANCH + ("children", "0")


def test_the_reference_file_is_accepted_and_canonical():
    """SURVIVED (sanity of the fixture used by every test of this module)."""
    text = _text()
    cert = mincert.loads(text)
    result = check_min_certificate(cert)
    assert result.accepted and result.lower_bound == 0 and result.stats == {"leaf": 2, "branch": 1, "prune": 1}
    assert mincert.dumps(cert) == text
    assert json.loads(text)["certificate"]["node"] == "prunes"


def _mutations():
    text = _text()
    out = []

    def add(label, mutated):
        out.append(pytest.param(mutated, id=label))

    # --- wrong types and containers, position by position
    for label, path, value in [
        ("format-missing", ("format",), ...), ("format-other", ("format",), "structbio-mincert/2"),
        ("format-number", ("format",), 1),
        ("message_bits-string", ("message_bits",), "1"), ("message_bits-bool", ("message_bits",), True),
        ("message_bits-null", ("message_bits",), None), ("message_bits-list", ("message_bits",), [1]),
        ("message_bits-missing", ("message_bits",), ...),
        ("domains-object", ("domains",), {"0": [0, 1, 2], "1": [0, 1]}), ("domains-flat", ("domains",), [0, 1]),
        ("domains-string-entry", ("domains", 0, 0), "0"), ("domains-bool-entry", ("domains", 0, 0), False),
        ("domains-null-entry", ("domains", 0, 0), None), ("domains-nested-entry", ("domains", 0, 0), [0]),
        ("domains-missing", ("domains",), ...),
        ("claim-list", ("claim",), [0]), ("claim-missing", ("claim",), ...),
        ("lower_bound-string", ("claim", "lower_bound"), "0"), ("lower_bound-bool", ("claim", "lower_bound"), False),
        ("lower_bound-null", ("claim", "lower_bound"), None), ("lower_bound-list", ("claim", "lower_bound"), [0]),
        ("lower_bound-missing", ("claim", "lower_bound"), ...),
        ("witness-string", ("claim", "witness"), "00"), ("witness-object", ("claim", "witness"), {"0": 0, "1": 0}),
        ("witness-bool-entry", ("claim", "witness", 0), False), ("witness-string-entry", ("claim", "witness", 0), "0"),
        ("witness-null-entry", ("claim", "witness", 0), None),
        ("certificate-missing", ("certificate",), ...), ("certificate-null", ("certificate",), None),
        ("certificate-list", ("certificate",), [LEAF]), ("certificate-string", ("certificate",), "leaf"),
        ("node-kind-unknown", ("certificate",), {"node": "sum", "parts": []}),
        ("node-kind-missing", ("certificate",), {"m": {}}),
        ("node-kind-prune-singular", ("certificate",), {"node": "prune", "site": 0, "remove": 2, "dominator": 0, "rest": LEAF}),
        ("steps-missing", ("certificate", "steps"), ...), ("steps-object", ("certificate", "steps"), {"0": [0, 2, 0]}),
        ("steps-flat", ("certificate", "steps"), [0, 2, 0]), ("step-two-entries", ("certificate", "steps", 0), [0, 2]),
        ("step-four-entries", ("certificate", "steps", 0), [0, 2, 0, 0]),
        ("step-string-entry", ("certificate", "steps", 0), [0, "2", 0]),
        ("step-bool-entry", ("certificate", "steps", 0), [0, 2, False]),
        ("rest-missing", ("certificate", "rest"), ...), ("rest-null", ("certificate", "rest"), None),
        ("prunes-then-prunes", ("certificate", "rest"),
         {"node": "prunes", "steps": [[0, 1, 0]], "rest": LEAF}),
        ("branch-site-string", BRANCH + ("site",), "0"), ("branch-site-bool", BRANCH + ("site",), False),
        ("branch-site-missing", BRANCH + ("site",), ...),
        ("children-list", BRANCH + ("children",), [LEAF, LEAF]), ("children-missing", BRANCH + ("children",), ...),
        ("child-null", BRANCH + ("children", "0"), None), ("child-list", BRANCH + ("children", "0"), [LEAF]),
        ("messages-list", LEAF_A + ("m",), [[0, 0, 0]]), ("message-string", LEAF_A + ("m", "0,1"), "000"),
        ("message-object", LEAF_A + ("m", "0,1"), {"0": 0}), ("message-bool-entry", LEAF_A + ("m", "0,1"), [0, 0, True]),
        ("message-null-entry", LEAF_A + ("m", "0,1"), [0, 0, None]),
        ("message-string-entry", LEAF_A + ("m", "0,1"), [0, 0, "0"]),
        ("model-list", ("model",), [[0, 1, 4], [0, 2]]), ("model-unary-object", ("model", "unary"), {"0": [0, 1, 4]}),
        ("model-unary-flat", ("model", "unary"), [0, 1, 4]), ("model-unary-empty-row", ("model", "unary", 1), []),
        ("model-unary-string-entry", ("model", "unary", 0, 0), "0"),
        ("model-unary-bool-entry", ("model", "unary", 0, 0), False),
        ("model-unary-null-entry", ("model", "unary", 0, 0), None),
        ("model-pair-list", ("model", "pair"), [[[0, 1], [1, 0], [3, 3]]]),
        ("model-pair-flat-table", ("model", "pair", "0,1"), [0, 1, 1, 0, 3, 3]),
        ("model-pair-ragged", ("model", "pair", "0,1"), [[0, 1], [1], [3, 3]]),
        ("model-pair-wrong-shape", ("model", "pair", "0,1"), [[0, 1], [1, 0]]),
        ("model-pair-empty", ("model", "pair", "0,1"), []),
        ("model-pair-string-entry", ("model", "pair", "0,1"), [[0, 1], [1, "0"], [3, 3]]),
        ("model-scale_bits-negative", ("model", "scale_bits"), -1), ("model-scale_bits-string", ("model", "scale_bits"), "1"),
        ("model-scale_bits-bool", ("model", "scale_bits"), True), ("model-scale_bits-missing", ("model", "scale_bits"), ...),
        ("model-meta-object", ("model", "meta"), {}), ("model-meta-not-json", ("model", "meta"), "{"),
        ("model-meta-json-list", ("model", "meta"), "[]"),
        ("meta-object", ("meta",), {}), ("meta-not-json", ("meta",), "{"), ("meta-json-list", ("meta",), "[1]"),
        ("checksum-missing", ("model_sha256",), ...), ("checksum-wrong", ("model_sha256",), "0" * 64),
        ("checksum-number", ("model_sha256",), 0), ("checksum-null", ("model_sha256",), None),
        ("checksum-uppercase", ("model_sha256",), json.loads(text)["model_sha256"].upper()),
    ]:
        add(label, _edit(path, value, text))

    # --- keys that are not in canonical form
    for bad in ("01,1", "0, 1", " 0,1", "0,1 ", "+0,1", "-0,1", "0,1,2", "0", "", "0;1", "0.0,1", "0,1.0",
                "٠,١", "0x0,1", "0_0,1", "0,1\n"):
        doc = json.loads(text)
        doc["certificate"]["rest"]["children"]["0"]["m"][bad] = [0, 0, 0]
        add(f"message-key-{bad!r}", json.dumps(doc))
        doc = json.loads(text)
        doc["model"]["pair"][bad] = doc["model"]["pair"].pop("0,1")
        add(f"pair-key-{bad!r}", json.dumps(doc))
    for bad in ("00", "+1", " 1", "1 ", "-1", "1.0", "", "one", "١", "0x1", "1_0", "1\n"):
        doc = json.loads(text)
        doc["certificate"]["rest"]["children"][bad] = LEAF
        add(f"child-key-{bad!r}", json.dumps(doc))
    for bad in ("1,0", "0,0", "0,5", "5,6"):                    # reversed, diagonal and out-of-range pairs
        doc = json.loads(text)
        doc["model"]["pair"][bad] = [[0, 1], [1, 0], [3, 3]]
        doc["model"]["pair"].pop("0,1")
        add(f"model-pair-{bad}", json.dumps(doc))

    # --- text-level attacks: one file must have one reading
    add("duplicate-key-top", text[:-1] + ',"message_bits":0}')
    add("duplicate-key-claim", text.replace('"claim":{', '"claim":{"lower_bound":-1000,'))
    add("duplicate-key-model", text.replace('"model":{', '"model":{"scale_bits":0,'))
    add("duplicate-key-node", text.replace('{"node":"leaf","m":{}}', '{"node":"leaf","m":{},"m":{}}'))
    add("duplicate-key-pair", text.replace('"pair":{', '"pair":{"0,1":[[0,0],[0,0],[0,0]],'))
    add("duplicate-format", '{"format":"other",' + text[1:])
    for literal in ("NaN", "Infinity", "-Infinity", "1e2", "1E2", "0.0", "1.0", "-0.0", "1.5"):
        add(f"literal-{literal}", text.replace('"lower_bound":0', f'"lower_bound":{literal}'))
        add(f"table-literal-{literal}", text.replace('"unary":[[0,1,4]', f'"unary":[[{literal},1,4]'))
    add("bom", "﻿" + text)
    add("trailing-garbage", text + "x")
    add("two-documents", text + text)
    add("empty", "")
    add("only-whitespace", "  ")
    add("top-level-list", "[" + text + "]")
    add("top-level-string", json.dumps(text))
    add("single-quotes", text.replace('"', "'"))
    add("comment", "// c\n" + text)
    add("truncated", text[:-1])
    add("json-nesting-beyond-the-parser", text.replace('"meta":"{}"}', '"meta":"{}","x":' + "[" * 20000 + "]" * 20000 + "}"))
    return out


@pytest.mark.parametrize("mutated", _mutations())
def test_strict_loader_rejects_the_mutated_file_as_malformed(mutated):
    """SURVIVED.  About 180 mutations of a valid file — wrong container or scalar type at every
    position, keys outside the canonical form, duplicate keys at four depths, non-integer
    literals, a 'prunes' node directly followed by a non-empty one, a wrong, missing or
    non-canonical checksum — are all errors of type `MalformedCertificate`."""
    with pytest.raises(MalformedCertificate):
        mincert.loads(mutated)


def test_detached_and_embedded_instances_are_bound_to_the_recorded_checksum(tmp_path):
    """SURVIVED.  A detached certificate presented with a different instance (one table entry or the
    scale changed), with no instance, or an embedded instance whose tables were edited without the
    checksum, is rejected; whitespace around a valid document and `-0` are harmless."""
    cert = _certificate()
    detached = mincert.dumps(cert, include_model=False)
    assert '"model":' not in detached
    assert check_min_certificate(mincert.loads(detached, model=_model())).accepted
    with pytest.raises(MalformedCertificate):
        mincert.loads(detached)
    other = _model()
    other.unary[1][1] += 1
    with pytest.raises(MalformedCertificate):
        mincert.loads(detached, model=other)
    rescaled = PairModel(unary=[u.copy() for u in _model().unary], pair=dict(_model().pair), scale_bits=2)
    with pytest.raises(MalformedCertificate):
        mincert.loads(detached, model=rescaled)
    with pytest.raises(MalformedCertificate):
        mincert.loads(_edit(("model", "unary", 1, 1), 3))       # embedded tables edited, checksum kept
    with pytest.raises(MalformedCertificate):
        mincert.loads(_edit(("model", "scale_bits"), 2))
    text = _text()
    assert check_min_certificate(mincert.loads(" \n" + text + "\n ")).accepted
    assert check_min_certificate(mincert.loads(text.replace('"lower_bound":0', '"lower_bound":-0'))).accepted
    # an integer literal beyond the interpreter's conversion limit is either refused by the loader or by the checker
    long_literal = text.replace('"lower_bound":0', '"lower_bound":-' + "9" * 5000)
    try:
        verdict = check_min_certificate(mincert.loads(long_literal)).accepted
    except MalformedCertificate:
        verdict = False
    assert verdict is False


# ----------------------------------------------------------------------------------------------
# findings (these tests fail with the reviewed code)
# ----------------------------------------------------------------------------------------------

def _deep_file(kind, depth):
    leaf = '{"node":"leaf","m":{}}'
    if kind == "branch nodes":
        node = '{"node":"branch","site":1,"children":{"0":' * depth + leaf + (',"1":' + leaf + '}}') * depth
    elif kind == "prunes nodes":
        node = '{"node":"prunes","steps":[],"rest":' * depth + leaf + '}' * depth
    else:
        return _text().replace('"meta":"{}"}', '"meta":"' + "[" * depth + "]" * depth + '"}')
    doc = json.loads(_text())
    doc["certificate"] = "@@"
    return json.dumps(doc, separators=(",", ":")).replace('"@@"', node)


@pytest.mark.parametrize("kind, depth", [("branch nodes", 1500), ("prunes nodes", 1500), ("metadata text", 20000)])
def test_loader_reports_deep_nesting_as_a_malformed_certificate(kind, depth):
    """FINDING (the loader raises an exception that is not `MalformedCertificate`).  `_strict_load`
    converts the parser's RecursionError, but the recursive `_node_from_json` and the second
    `json.loads` of the metadata are outside that handler: a file with 1,500 nested nodes, or with
    deeply nested metadata text, makes `loads` raise a bare RecursionError.  A caller that turns
    `MalformedCertificate` into a rejection crashes instead."""
    text = _deep_file(kind, depth)
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)                 # the default; the reference checker raises it when imported
    raised = None
    try:
        try:
            mincert.loads(text)
        except MalformedCertificate:
            pass
        except RecursionError:
            raised = "RecursionError"           # (reported below, outside the handler: no 1,500-frame traceback)
    finally:
        sys.setrecursionlimit(old)
    assert raised is None, f"mincert.loads raised {raised} on a file with {depth} levels of nested {kind}"


@pytest.mark.parametrize("where", ["pair key of the instance", "message key", "child key"])
def test_loader_reports_non_ascii_digits_in_keys_as_a_malformed_certificate(where):
    """FINDING (the loader raises an exception that is not `MalformedCertificate`).  The canonical-key
    test uses `str.isdigit`, which is true for characters such as SUPERSCRIPT TWO that `int` cannot
    convert: `loads` raises a bare ValueError."""
    text = _text()
    if where == "pair key of the instance":
        mutated = text.replace('"pair":{"0,1"', '"pair":{"0,¹"')
    elif where == "message key":
        mutated = text.replace('"m":{"0,1"', '"m":{"0,¹"')
    else:
        mutated = text.replace('"children":{"0"', '"children":{"²"')
    assert mutated != text
    outcome = "accepted"
    try:
        mincert.loads(mutated)
    except MalformedCertificate:
        outcome = "MalformedCertificate"
    except ValueError as exc:
        outcome = f"{type(exc).__name__}: {exc}"
    assert outcome == "MalformedCertificate", f"mincert.loads -> {outcome}"


def test_loader_does_not_silently_replace_the_supplied_instance_by_an_embedded_one():
    """FINDING (one call, two readings).  `loads(text, model=X)` ignores `X` without any error when
    the file embeds an instance: the certificate returned — and accepted by the checker — is about
    the embedded instance `Y`.  A verifier that holds the published instance `X` and is handed a
    file with a foreign embedded instance is told "accepted" for a claim about other tables."""
    mine = PairModel(unary=[np.array([-50, 1, 4]), np.array([0, 2])],
                     pair={(0, 1): np.array([[0, 1], [1, 0], [3, 3]])}, scale_bits=1)
    foreign_text = _text()                                       # embeds `_model()`, not `mine`
    assert mincert.model_sha256(mine) != json.loads(foreign_text)["model_sha256"]
    try:
        cert = mincert.loads(foreign_text, model=mine)
    except MalformedCertificate:
        return
    result = check_min_certificate(cert)
    same_instance = mincert.model_sha256(cert.model) == mincert.model_sha256(mine)
    assert same_instance, (f"loads(text, model=X) returned a certificate about another instance "
                           f"(accepted={result.accepted}, lower_bound={result.lower_bound}; "
                           f"the minimum of X is {min(mine.energy((a, b)) for a in range(3) for b in range(2))})")


@pytest.mark.parametrize("label", ["second lower_bound at top level", "extra key in claim", "extra key in a leaf",
                                   "extra key in a branch", "extra key in the instance",
                                   "prunes node followed by a prunes node without steps"])
def test_loader_rejects_fields_and_encodings_outside_the_format(label):
    """FINDING (strictness).  Unknown fields are ignored everywhere (the reference format and the
    newer `structbio-zcert/1` loader reject them), and the rule "a 'prunes' node must not be
    followed directly by another one" is bypassed by an inner node with an empty step list, so one
    certificate has many accepted spellings and a misspelt or misplaced field goes unnoticed."""
    text = _text()
    if label == "second lower_bound at top level":
        mutated = text[:-1] + ',"lower_bound":999}'
    elif label == "extra key in claim":
        mutated = text.replace('"claim":{', '"claim":{"upper_bound":-5,')
    elif label == "extra key in a leaf":
        mutated = text.replace('{"node":"leaf","m":{}}', '{"node":"leaf","m":{},"u":[0,0],"children":{}}')
    elif label == "extra key in a branch":
        mutated = text.replace('{"node":"branch",', '{"node":"branch","m":{"0,1":[9,9,9]},')
    elif label == "extra key in the instance":
        mutated = text.replace('"model":{', '"model":{"triples":{},')
    else:
        doc = json.loads(text)
        doc["certificate"]["rest"] = {"node": "prunes", "steps": [], "rest": doc["certificate"]["rest"]}
        mutated = json.dumps(doc, separators=(",", ":"))
    assert mutated != text
    with pytest.raises(MalformedCertificate):
        mincert.loads(mutated)


def test_converted_document_can_be_judged_by_the_reference_checker_whenever_ours_accepts(reference_checker):
    """FINDING (the stated equivalence holds only below a size limit).  A valid chain of 10,050
    prune nodes (one per two-state site) is accepted by our iterative checker and converted, but
    the document is 10,050 objects deep: `json.dumps` cannot write it and the reference checker
    cannot parse it ("nested too deeply"), whatever the recursion limit.  The development
    certificates have 344 to 1,280 consecutive prunes; an instance eight times the size of
    ubiquitin is beyond the limit."""
    n = 10_050
    model = PairModel(unary=[np.array([0, 1]) for _ in range(n)], pair={}, scale_bits=0)
    node = {"node": "leaf", "m": {}}
    for i in reversed(range(n)):
        node = {"node": "prune", "site": i, "remove": 1, "dominator": 0, "rest": node}
    cert = MinCertificate(model=model, message_bits=0, domains=[[0, 1] for _ in range(n)], lower_bound=0,
                          witness=None, root=node)
    assert check_min_certificate(cert).accepted
    doc = to_metricchain_cert1(cert)
    parts, cur, depth = [], doc["certificate"], 0                # write the chain without recursion
    while cur["node"] == "prune":
        head = dict(cur)
        cur = head.pop("rest")
        parts.append(json.dumps(head)[:-1] + ',"rest":')
        depth += 1
    top = dict(doc)
    top["certificate"] = "@@"
    text = json.dumps(top).replace('"@@"', "".join(parts) + json.dumps(cur) + "}" * depth)
    verdict = reference_checker.check_text(text)
    try:
        json.dumps(doc)
        writable = True
    except RecursionError:
        writable = False
    assert writable and verdict["accepted"] is True, (
        f"ours: accepted; json.dumps of the converted document: {'ok' if writable else 'RecursionError'}; "
        f"reference checker: {verdict}")
