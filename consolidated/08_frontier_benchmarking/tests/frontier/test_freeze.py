"""Freeze manifests: every planted violation must be detected.

The tests are negative controls first: a tool that guards frozen predictions is worth what its
ability to notice a change is worth.
"""
import copy
import json
import os
from pathlib import Path

import pytest

from metricchain_fb import commitment, freeze

ROOT = Path(__file__).resolve().parents[2]
FREEZES = ROOT / "experiments" / "frontier" / "freezes"

GOOD_META = {
    "freeze_id": "FRONTIER-FRZ-9999",
    "kind": "control",
    "title": "synthetic control freeze used by the test-suite",
    "assessment_class": "A-EXP",
    "evidence_stage": "exploratory",
    "created_utc": "2026-11-26T23:00:00Z",
    "source_commits": {"frontier-benchmarks": "0" * 40},
    "protocol": {"id": "FB-P-TEST", "version": "1"},
    "method": {"name": "none", "version": "0", "declared_training_cutoff": "n/a", "dependencies": {}},
    "inputs": [{"description": "generated in the test", "sha256": "a" * 64}],
    "random_seeds": [1, "two"],
    "config_files": [],
    "reference_status": {"reference_public_at_freeze": "n/a", "statement": "synthetic: no reference exists"},
    "contamination_assessment": "not applicable: synthetic bytes",
    "exclusions": [],
    "notes": "",
}


def make_freeze(tmp_path, meta=None):
    root = tmp_path / "frz"
    (root / "sub").mkdir(parents=True)
    (root / "a.txt").write_bytes(b"alpha\n")
    (root / "sub" / "b.bin").write_bytes(bytes(range(256)))
    manifest = freeze.build_manifest(root, copy.deepcopy(meta or GOOD_META))
    path, digest = freeze.write_manifest(root, manifest)
    return root, path, digest


# ------------------------------------------------------------------ positive control
def test_intact_freeze_verifies(tmp_path):
    root, path, digest = make_freeze(tmp_path)
    report = freeze.verify_freeze(path)
    assert report.ok, report.summary()
    assert report.n_artifacts == 2
    assert report.manifest_sha256 == digest == freeze.sha256_file(path)
    assert [a["path"] for a in json.loads(path.read_text())["artifacts"]] == ["a.txt", "sub/b.bin"]


def test_manifest_is_in_normal_form_and_digest_is_plain_sha256(tmp_path):
    root, path, digest = make_freeze(tmp_path)
    manifest, digest2, is_normal = freeze.load_manifest(path)
    assert is_normal and digest2 == digest
    assert freeze.normal_form(manifest) == path.read_bytes()
    import hashlib
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest


def test_bookkeeping_files_are_not_artifacts(tmp_path):
    root, path, _ = make_freeze(tmp_path)
    (root / freeze.EVIDENCE_NAME).write_text("{}\n")
    (root / freeze.TIMESTAMP_DIR).mkdir()
    (root / freeze.TIMESTAMP_DIR / "x.tsr").write_bytes(b"\x30\x03\x02\x01\x00")
    assert freeze.verify_freeze(path).ok


# ------------------------------------------------------------------ planted violations
def test_one_flipped_bit_in_an_artifact_is_detected(tmp_path):
    root, path, _ = make_freeze(tmp_path)
    data = bytearray((root / "sub" / "b.bin").read_bytes())
    data[17] ^= 0x01
    (root / "sub" / "b.bin").write_bytes(bytes(data))
    report = freeze.verify_freeze(path)
    assert not report.ok and any("content changed" in e for e in report.errors)


def test_size_change_missing_and_extra_files_are_detected(tmp_path):
    root, path, _ = make_freeze(tmp_path)
    (root / "a.txt").write_bytes(b"alpha\nbeta\n")
    assert any("size changed" in e for e in freeze.verify_freeze(path).errors)
    (root / "a.txt").unlink()
    assert any("missing" in e for e in freeze.verify_freeze(path).errors)
    (root / "a.txt").write_bytes(b"alpha\n")
    assert freeze.verify_freeze(path).ok
    (root / "added_later.pdb").write_bytes(b"ATOM\n")
    strict = freeze.verify_freeze(path)
    assert not strict.ok and any("not listed" in e for e in strict.errors)
    lenient = freeze.verify_freeze(path, strict=False)
    assert lenient.ok and any("not listed" in w for w in lenient.warnings)


def test_editing_the_manifest_changes_its_digest_and_is_detected(tmp_path):
    root, path, digest = make_freeze(tmp_path)
    manifest = json.loads(path.read_text())
    # (a) a semantic edit, re-serialised in normal form: a different manifest, a different digest
    manifest["assessment_class"] = "A-PLB"
    path.write_bytes(freeze.normal_form(manifest))
    assert freeze.verify_freeze(path).manifest_sha256 != digest
    # (b) whitespace only: same content, but not the frozen bytes
    manifest["assessment_class"] = "A-EXP"
    path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n")
    report = freeze.verify_freeze(path)
    assert not report.ok and any("normal form" in e for e in report.errors)


def test_a_manifest_is_never_overwritten(tmp_path):
    root, path, _ = make_freeze(tmp_path)
    manifest = json.loads(path.read_text())
    with pytest.raises(FileExistsError):
        freeze.write_manifest(root, manifest)


def test_symbolic_links_are_refused(tmp_path):
    root = tmp_path / "frz"
    root.mkdir()
    (tmp_path / "outside.txt").write_text("x")
    os.symlink(tmp_path / "outside.txt", root / "link.txt")
    with pytest.raises(freeze.ManifestError):
        freeze.build_manifest(root, copy.deepcopy(GOOD_META))


@pytest.mark.parametrize("bad", ["../escape.txt", "/abs.txt", "a//b.txt", "./a.txt", "a\\b.txt", "", "sub/../a.txt",
                                 "MANIFEST.json", "timestamps/t.tsr"])
def test_artifact_paths_outside_the_freeze_are_rejected(bad):
    m = copy.deepcopy(GOOD_META)
    m["schema"] = freeze.SCHEMA
    m["artifacts"] = [{"path": bad, "bytes": 1, "sha256": "b" * 64}]
    with pytest.raises(freeze.ManifestError):
        freeze.validate_manifest(m)


@pytest.mark.parametrize("field,value", [
    ("assessment_class", "blind"), ("assessment_class", "A-OPB"), ("kind", "prophecy"),
    ("evidence_stage", "validated"), ("created_utc", "26 Nov 2026"), ("freeze_id", "FRZ-1"),
    ("contamination_assessment", "  "), ("source_commits", {"x": "abc123"}),
    ("reference_status", {"reference_public_at_freeze": "maybe", "statement": "s"}),
    ("reference_status", {"reference_public_at_freeze": "no", "statement": ""}),
    ("random_seeds", [1.5]), ("method", {"name": "m", "version": "1"}),
    ("exclusions", [{"item": "T1"}]), ("title", ""),
])
def test_malformed_metadata_is_rejected(tmp_path, field, value):
    meta = copy.deepcopy(GOOD_META)
    meta[field] = value
    root = tmp_path / "frz"
    root.mkdir()
    (root / "a.txt").write_text("x")
    with pytest.raises(freeze.ManifestError):
        freeze.build_manifest(root, meta)


def test_missing_and_unknown_fields_are_rejected(tmp_path):
    root = tmp_path / "frz"
    root.mkdir()
    (root / "a.txt").write_text("x")
    for key in GOOD_META:
        meta = copy.deepcopy(GOOD_META)
        del meta[key]
        with pytest.raises(freeze.ManifestError):
            freeze.build_manifest(root, meta)
    meta = copy.deepcopy(GOOD_META)
    meta["leaderboard_rank"] = 1
    with pytest.raises(freeze.ManifestError):
        freeze.build_manifest(root, meta)


def test_pre_reference_release_cannot_be_claimed_with_a_public_reference(tmp_path):
    """The class 'pre-reference-release' is refused unless the manifest also states that the
    reference was not public — the tool cannot check the statement, but it can refuse the
    contradiction."""
    root = tmp_path / "frz"
    root.mkdir()
    (root / "a.txt").write_text("x")
    meta = copy.deepcopy(GOOD_META)
    meta["assessment_class"] = "A-PRR"
    for status in ("yes", "partly", "unknown", "n/a"):
        meta["reference_status"] = {"reference_public_at_freeze": status, "statement": "s"}
        with pytest.raises(freeze.ManifestError):
            freeze.build_manifest(root, meta)
    meta["reference_status"] = {"reference_public_at_freeze": "no", "statement": "not released: evidence ..."}
    freeze.build_manifest(root, meta)


def test_floats_are_refused_everywhere(tmp_path):
    with pytest.raises(freeze.ManifestError):
        freeze.normal_form({"a": [1, {"b": 0.1}]})
    path = tmp_path / "MANIFEST.json"
    path.write_text('{"a": 1.0}\n')
    with pytest.raises(freeze.ManifestError):
        freeze.load_manifest(path)


def test_verify_never_raises_on_garbage(tmp_path):
    path = tmp_path / "MANIFEST.json"
    for garbage in (b"", b"\xff\xfe", b"[]\n", b"{}\n", b'{"schema": 3}\n'):
        path.write_bytes(garbage)
        report = freeze.verify_freeze(path)
        assert not report.ok
    assert not freeze.verify_freeze(tmp_path / "absent" / "MANIFEST.json").ok


# ------------------------------------------------------------------ commitments
def test_commitment_opens_only_with_the_committed_payload_and_salt():
    payload = b"1ABC\n2DEF\n"
    c, salt = commitment.commit(payload)
    assert commitment.open_commitment(c, payload, salt)
    assert not commitment.open_commitment(c, payload + b"3GHI\n", salt)
    assert not commitment.open_commitment(c, payload, commitment.new_salt())
    assert not commitment.open_commitment(c, payload, "zz")
    c2, _ = commitment.commit(payload)
    assert c2 != c, "a fresh salt must give a different commitment for the same payload"
    assert commitment.commit(payload, salt)[0] == c


def test_commitment_is_domain_separated_from_a_plain_hash():
    import hashlib
    payload = b"x"
    c, salt = commitment.commit(payload)
    assert c != hashlib.sha256(payload).hexdigest()
    assert c != hashlib.sha256(salt.encode() + payload).hexdigest()


# ------------------------------------------------------------------ the tripwire
def test_every_committed_freeze_is_intact():
    """Every freeze in the repository must verify, strictly.  A frozen artifact that was edited
    after the fact makes the whole suite fail."""
    manifests = list(freeze.iter_manifests(FREEZES)) if FREEZES.is_dir() else []
    ids = set()
    for path in manifests:
        report = freeze.verify_freeze(path, strict=True)
        assert report.ok, f"{path}\n{report.summary()}"
        assert report.freeze_id not in ids, f"duplicate freeze id {report.freeze_id}"
        ids.add(report.freeze_id)
        assert path.parent.name.startswith(report.freeze_id), f"{path}: directory must be named after its freeze id"
