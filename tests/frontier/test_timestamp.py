"""RFC 3161 time-stamp evidence: stored tokens must verify for the datum they attest and for
nothing else.  The live test (network) runs only when FB_LIVE_TSA=1."""
import copy
import os
import shutil
from pathlib import Path

import pytest

from metricchain_fb import freeze, timestamp

DATA = Path(__file__).resolve().parent / "data"
PROBE = DATA / "tsa_probe.txt"
TOKENS = {"digicert": DATA / "tsa_probe_digicert.tsr", "sectigo": DATA / "tsa_probe_sectigo.tsr"}
HAVE_TOOLS = shutil.which("openssl") is not None and Path(timestamp.DEFAULT_CAFILE).is_file()
needs_openssl = pytest.mark.skipif(not HAVE_TOOLS, reason="openssl or the system trust store is not available")


def test_openssl_time_format_is_parsed():
    assert timestamp._parse_openssl_time("Nov 26 22:55:32 2026 GMT") == "2026-11-26T22:55:32Z"
    assert timestamp._parse_openssl_time("Nov  6 02:05:35.189 2026 GMT") == "2026-11-06T02:05:35Z"
    with pytest.raises(timestamp.TimestampError):
        timestamp._parse_openssl_time("yesterday")


@needs_openssl
@pytest.mark.parametrize("name", sorted(TOKENS))
def test_stored_token_attests_the_probe_and_nothing_else(name):
    digest = freeze.sha256_file(PROBE)
    info = timestamp.read_token(TOKENS[name])
    assert info["status"].startswith("Granted")
    assert info["gen_time_utc"].startswith("2026-11-26T22:55:")
    assert info["digest_hex"] == digest, "the token must carry the digest of the probe file"
    ok, detail = timestamp.verify_token(TOKENS[name], digest)
    if not ok:
        pytest.skip(f"this machine's trust store does not verify the {name} chain: {detail}")
    # negative controls: another digest, and a corrupted token, must not verify
    other = freeze.sha256_bytes(PROBE.read_bytes() + b"x")
    assert timestamp.verify_token(TOKENS[name], other)[0] is False
    assert timestamp.verify_token(TOKENS[name], "nothex")[0] is False


@needs_openssl
def test_corrupted_token_does_not_verify(tmp_path):
    digest = freeze.sha256_file(PROBE)
    data = bytearray(TOKENS["digicert"].read_bytes())
    data[len(data) // 2] ^= 0xFF
    bad = tmp_path / "bad.tsr"
    bad.write_bytes(bytes(data))
    assert timestamp.verify_token(bad, digest)[0] is False


@needs_openssl
def test_evidence_for_another_manifest_is_not_accepted(tmp_path):
    """A side-car that names a different manifest digest must count for nothing."""
    from test_freeze import GOOD_META
    root = tmp_path / "frz"
    root.mkdir()
    (root / "a.txt").write_text("x")
    path, digest = freeze.write_manifest(root, freeze.build_manifest(root, copy.deepcopy(GOOD_META)))
    (root / freeze.TIMESTAMP_DIR).mkdir()
    shutil.copy(TOKENS["digicert"], root / freeze.TIMESTAMP_DIR / "digicert.tsr")
    evidence = {"schema": "metricchain-fb-evidence/1", "manifest_sha256": digest, "evidence": [{
        "type": "rfc3161", "name": "digicert", "token_file": "timestamps/digicert.tsr",
        "token_sha256": freeze.sha256_file(TOKENS["digicert"])}]}
    (root / freeze.EVIDENCE_NAME).write_bytes(freeze.normal_form(evidence))
    result = timestamp.verify_evidence(path)
    assert result["verified"] == [] and result["earliest_utc"] == ""   # the token attests the probe, not this manifest
    assert result["unverified"] and result["unverified"][0]["name"] == "digicert"
    evidence["manifest_sha256"] = "0" * 64
    (root / freeze.EVIDENCE_NAME).write_bytes(freeze.normal_form(evidence))
    assert timestamp.verify_evidence(path)["verified"] == []
    assert freeze.verify_freeze(path).ok, "bookkeeping files never affect the freeze itself"


@pytest.mark.skipif(os.environ.get("FB_LIVE_TSA") != "1", reason="live TSA test: set FB_LIVE_TSA=1")
def test_live_stamp_and_verify(tmp_path):
    from test_freeze import GOOD_META
    root = tmp_path / "frz"
    root.mkdir()
    (root / "a.txt").write_text("x")
    path, digest = freeze.write_manifest(root, freeze.build_manifest(root, copy.deepcopy(GOOD_META)))
    evidence = timestamp.stamp_manifest(path)
    assert evidence["manifest_sha256"] == digest
    result = timestamp.verify_evidence(path)
    assert len(result["verified"]) >= 2, result
    assert freeze.verify_freeze(path).ok
    # tampering with the manifest after stamping invalidates every token
    data = path.read_bytes().replace(b"synthetic control", b"synthetic CONTROL")
    path.write_bytes(data)
    assert timestamp.verify_evidence(path)["verified"] == []


@pytest.mark.skipif(os.environ.get("FB_LIVE_TSA") != "1", reason="live TSA test: set FB_LIVE_TSA=1")
def test_live_stamp_of_an_arbitrary_file(tmp_path):
    """Another division's manifest (any file) can be time-stamped without being touched."""
    target = tmp_path / "MANIFEST.sha256"
    target.write_text("0" * 64 + "  12  predictions/model_1.pdb\n")
    before = target.read_bytes()
    timestamp.stamp_file(target)
    assert target.read_bytes() == before
    assert len(timestamp.verify_file_evidence(target)["verified"]) >= 2
    target.write_text("1" * 64 + "  12  predictions/model_1.pdb\n")
    assert timestamp.verify_file_evidence(target)["verified"] == []
