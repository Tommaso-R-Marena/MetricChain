"""Independent time-stamp evidence for freeze manifests (RFC 3161).

A git commit date is written by the committer and can be set to anything; it is not evidence
of when a file existed.  An RFC 3161 time-stamp token is a statement signed by a third party
(a time-stamping authority, TSA): "a datum with this SHA-256 digest existed at this time".
Only the digest leaves the machine — never the manifest, the artifacts, or any name.

This module wraps two external programs, both required: ``openssl`` (to build the query, to
print and to verify the token) and ``curl`` (to post the query).  Several unrelated public
TSAs are used for one manifest, so that the evidence does not rest on one operator.

What a verified token establishes: the *manifest bytes* existed no later than the token's
time, as attested by that TSA, provided its signing certificate chains to a root the verifier
trusts.  It establishes nothing about when the reference answers became available.

Tokens are verified against the certificate authorities of the verifying machine
(``cafile``).  A token whose chain ends at a root that the machine does not trust is recorded
as *unverified here* — it is kept (another verifier may trust that root) but never counted.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Sequence

from .freeze import EVIDENCE_NAME, MANIFEST_NAME, TIMESTAMP_DIR, normal_form, sha256_file

__all__ = ["DEFAULT_TSAS", "DEFAULT_CAFILE", "make_query", "post_query", "read_token",
           "verify_token", "stamp_manifest", "stamp_file", "verify_file_evidence", "verify_evidence",
           "TimestampError"]

#: Public time-stamping authorities reachable from the session machine on 2026-11-26 whose
#: tokens verified against the machine's ordinary trust store.  Operators are unrelated.
DEFAULT_TSAS = {
    "digicert": "http://timestamp.digicert.com",
    "sectigo": "https://timestamp.sectigo.com",
    "globalsign": "http://timestamp.globalsign.com/tsa/r6advanced1",
    "certum": "http://time.certum.pl",
}
DEFAULT_CAFILE = "/etc/ssl/certs/ca-certificates.crt"
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class TimestampError(RuntimeError):
    pass


def _need(program: str) -> str:
    path = shutil.which(program)
    if path is None:
        raise TimestampError(f"required program not found: {program}")
    return path


def _run(cmd, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, **kw)


def make_query(digest_hex: str) -> bytes:
    """DER time-stamp request for a SHA-256 digest (with a nonce; the TSA certificate is requested
    so that the token can be verified without fetching anything)."""
    if not _HEX64.match(digest_hex):
        raise TimestampError("digest must be 64 lowercase hex digits")
    proc = _run([_need("openssl"), "ts", "-query", "-digest", digest_hex, "-sha256", "-cert"])
    if proc.returncode != 0 or not proc.stdout:
        raise TimestampError(f"openssl ts -query failed: {proc.stderr.decode(errors='replace')[:300]}")
    return proc.stdout


def post_query(url: str, query: bytes) -> bytes:
    """POST the request to a TSA and return the DER reply.  Only the digest is transmitted."""
    with tempfile.TemporaryDirectory() as tmp:
        qfile = Path(tmp) / "q.tsq"
        qfile.write_bytes(query)
        proc = _run([_need("curl"), "-sS", "--max-time", "60", "--fail",
                     "-H", "Content-Type: application/timestamp-query",
                     "--data-binary", f"@{qfile}", url])
    if proc.returncode != 0 or not proc.stdout:
        raise TimestampError(f"no reply from {url}: {proc.stderr.decode(errors='replace')[:300]}")
    return proc.stdout


_MONTHS = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}


def _parse_openssl_time(text: str) -> str:
    """'Nov 26 22:55:32 2026 GMT' or 'Nov 26 22:55:35.189 2026 GMT' -> '2026-11-26T22:55:32Z'."""
    m = re.match(r"^(\w{3})\s+(\d{1,2})\s+(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?\s+(\d{4})\s+GMT$", text.strip())
    if not m:
        raise TimestampError(f"unrecognised time in token: {text!r}")
    mon, day, hh, mm, ss, year = m.groups()
    stamp = _dt.datetime(int(year), _MONTHS[mon], int(day), int(hh), int(mm), int(ss))
    return stamp.strftime("%Y-%m-%dT%H:%M:%SZ")


def read_token(token_path) -> dict:
    """Status, time and signer of a time-stamp reply (as printed by openssl; not a verification)."""
    proc = _run([_need("openssl"), "ts", "-reply", "-in", str(token_path), "-text"])
    if proc.returncode != 0:
        raise TimestampError(f"not a time-stamp reply: {token_path}")
    text = proc.stdout.decode(errors="replace")
    out = {"status": "", "gen_time_utc": "", "tsa_name": "", "digest_hex": "", "hash_algorithm": ""}
    m = re.search(r"^Status:\s*(.+)$", text, re.M)
    if m:
        out["status"] = m.group(1).strip().rstrip(".")
    m = re.search(r"^Time stamp:\s*(.+)$", text, re.M)
    if m:
        out["gen_time_utc"] = _parse_openssl_time(m.group(1))
    m = re.search(r"^TSA:\s*(.+)$", text, re.M)
    if m:
        out["tsa_name"] = m.group(1).strip()
    m = re.search(r"^Hash Algorithm:\s*(\S+)", text, re.M)
    if m:
        out["hash_algorithm"] = m.group(1)
    hexbytes = re.findall(r"^\s+[0-9a-f]{4} - ((?:[0-9a-f]{2}[ -])+)", text, re.M)
    out["digest_hex"] = "".join(re.sub(r"[ -]", "", chunk) for chunk in hexbytes)
    return out


def verify_token(token_path, digest_hex: str, cafile: str = DEFAULT_CAFILE):
    """``(ok, detail)``: does the token attest *this* digest and chain to a root in ``cafile``?"""
    if not _HEX64.match(digest_hex):
        return False, "digest must be 64 lowercase hex digits"
    if not Path(cafile).is_file():
        return False, f"trust store not found: {cafile}"
    proc = _run([_need("openssl"), "ts", "-verify", "-digest", digest_hex, "-in", str(token_path),
                 "-CAfile", cafile])
    out = (proc.stdout + proc.stderr).decode(errors="replace")
    if proc.returncode == 0 and "Verification: OK" in out:
        return True, "Verification: OK"
    reason = re.findall(r"Verify error:([^\n]+)|:([^:\n]*mismatch[^\n]*)", out)
    flat = "; ".join(x for pair in reason for x in pair if x) or out.strip().splitlines()[-1][:200]
    return False, flat


def stamp_manifest(manifest_path, tsas: dict | None = None, cafile: str = DEFAULT_CAFILE) -> dict:
    """Obtain one token per TSA for the manifest's SHA-256 and write the evidence side-car.

    Tokens go to ``timestamps/<name>.tsr``; ``MANIFEST.evidence.json`` records, per token, the
    TSA, the token's checksum, its time and whether it verified on this machine.  Existing
    evidence is extended, never replaced.  Returns the evidence object.
    """
    manifest_path = Path(manifest_path)
    if manifest_path.name != MANIFEST_NAME:
        raise TimestampError(f"expected a file named {MANIFEST_NAME}")
    root = manifest_path.parent
    digest = sha256_file(manifest_path)
    tsdir = root / TIMESTAMP_DIR
    tsdir.mkdir(exist_ok=True)
    evidence_path = root / EVIDENCE_NAME
    if evidence_path.exists():
        evidence = json.loads(evidence_path.read_text(encoding="ascii"))
        if evidence.get("manifest_sha256") != digest:
            raise TimestampError("existing evidence refers to a different manifest digest")
    else:
        evidence = {"schema": "metricchain-fb-evidence/1", "manifest_sha256": digest, "evidence": []}
    have = {e.get("name") for e in evidence["evidence"] if e.get("type") == "rfc3161"}
    query = make_query(digest)
    for name, url in (tsas or DEFAULT_TSAS).items():
        if name in have:
            continue
        entry = {"type": "rfc3161", "name": name, "tsa_url": url}
        try:
            token = post_query(url, query)
            token_file = tsdir / f"{name}.tsr"
            token_file.write_bytes(token)
            info = read_token(token_file)
            ok, detail = verify_token(token_file, digest, cafile)
            entry.update({
                "token_file": f"{TIMESTAMP_DIR}/{name}.tsr",
                "token_sha256": sha256_file(token_file),
                "status": info["status"],
                "gen_time_utc": info["gen_time_utc"],
                "tsa_name": info["tsa_name"],
                "verified_on_this_machine": ok,
                "verification_detail": detail,
                "trust_store": cafile,
            })
        except TimestampError as exc:
            entry.update({"error": str(exc)[:300], "verified_on_this_machine": False})
        evidence["evidence"].append(entry)
    evidence_path.write_bytes(normal_form(evidence))
    return evidence


def verify_evidence(manifest_path, cafile: str = DEFAULT_CAFILE) -> dict:
    """Re-verify every stored token against the manifest as it is now.

    Returns ``{"manifest_sha256", "verified": [...], "unverified": [...], "earliest_utc"}`` where
    ``earliest_utc`` is the earliest time attested by a token that verifies here ("" if none).
    """
    manifest_path = Path(manifest_path)
    root = manifest_path.parent
    digest = sha256_file(manifest_path)
    result = {"manifest_sha256": digest, "verified": [], "unverified": [], "earliest_utc": ""}
    evidence_path = root / EVIDENCE_NAME
    if not evidence_path.is_file():
        return result
    evidence = json.loads(evidence_path.read_text(encoding="ascii"))
    if evidence.get("manifest_sha256") != digest:
        result["unverified"].append({"name": "*", "reason": "evidence side-car refers to a different manifest digest"})
        return result
    for entry in evidence.get("evidence", []):
        if entry.get("type") != "rfc3161" or "token_file" not in entry:
            continue
        token = root / entry["token_file"]
        if not token.is_file():
            result["unverified"].append({"name": entry.get("name"), "reason": "token file missing"})
            continue
        if sha256_file(token) != entry.get("token_sha256"):
            result["unverified"].append({"name": entry.get("name"), "reason": "token file changed"})
            continue
        ok, detail = verify_token(token, digest, cafile)
        if ok:
            info = read_token(token)
            result["verified"].append({"name": entry.get("name"), "gen_time_utc": info["gen_time_utc"],
                                       "tsa_name": info["tsa_name"]})
        else:
            result["unverified"].append({"name": entry.get("name"), "reason": detail})
    times = sorted(v["gen_time_utc"] for v in result["verified"] if v["gen_time_utc"])
    result["earliest_utc"] = times[0] if times else ""
    return result


def stamp_file(path, tsas: dict | None = None, cafile: str = DEFAULT_CAFILE) -> dict:
    """Time-stamp ANY file (for instance another division's ``MANIFEST.sha256``) without touching it.

    Tokens go to ``<file>.timestamps/<name>.tsr`` and the record to ``<file>.evidence.json``, both
    next to the file.  Only the file's SHA-256 digest is sent out.
    """
    path = Path(path)
    digest = sha256_file(path)
    tsdir = path.with_name(path.name + ".timestamps")
    tsdir.mkdir(exist_ok=True)
    evidence = {"schema": "metricchain-fb-evidence/1", "file": path.name, "file_sha256": digest, "evidence": []}
    query = make_query(digest)
    for name, url in (tsas or DEFAULT_TSAS).items():
        entry = {"type": "rfc3161", "name": name, "tsa_url": url}
        try:
            token_file = tsdir / f"{name}.tsr"
            token_file.write_bytes(post_query(url, query))
            info = read_token(token_file)
            ok, detail = verify_token(token_file, digest, cafile)
            entry.update({"token_file": f"{tsdir.name}/{name}.tsr", "token_sha256": sha256_file(token_file),
                          "gen_time_utc": info["gen_time_utc"], "tsa_name": info["tsa_name"],
                          "verified_on_this_machine": ok, "verification_detail": detail, "trust_store": cafile})
        except TimestampError as exc:
            entry.update({"error": str(exc)[:300], "verified_on_this_machine": False})
        evidence["evidence"].append(entry)
    path.with_name(path.name + ".evidence.json").write_bytes(normal_form(evidence))
    return evidence


def verify_file_evidence(path, cafile: str = DEFAULT_CAFILE) -> dict:
    """Re-verify the tokens written by :func:`stamp_file` against the file as it is now."""
    path = Path(path)
    digest = sha256_file(path)
    result = {"file_sha256": digest, "verified": [], "unverified": [], "earliest_utc": ""}
    record = path.with_name(path.name + ".evidence.json")
    if not record.is_file():
        return result
    evidence = json.loads(record.read_text(encoding="ascii"))
    for entry in evidence.get("evidence", []):
        if "token_file" not in entry:
            continue
        token = path.parent / entry["token_file"]
        ok, detail = (verify_token(token, digest, cafile) if token.is_file() else (False, "token file missing"))
        if ok:
            result["verified"].append({"name": entry.get("name"), "gen_time_utc": read_token(token)["gen_time_utc"]})
        else:
            result["unverified"].append({"name": entry.get("name"), "reason": detail})
    times = sorted(v["gen_time_utc"] for v in result["verified"])
    result["earliest_utc"] = times[0] if times else ""
    return result


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m metricchain_fb.timestamp", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name, helptext in (("stamp", "request tokens for a MANIFEST.json (sends only its digest)"),
                           ("verify", "re-verify the stored tokens of a MANIFEST.json"),
                           ("stamp-file", "request tokens for any file, e.g. another division's manifest"),
                           ("verify-file", "re-verify the tokens of a file stamped with stamp-file")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("manifest")
        p.add_argument("--cafile", default=DEFAULT_CAFILE)
    args = parser.parse_args(argv)
    if args.cmd == "stamp-file":
        for e in stamp_file(args.manifest, cafile=args.cafile)["evidence"]:
            print(f"{e.get('name'):12s} {e.get('gen_time_utc', '-'):22s} verified={e.get('verified_on_this_machine')} {e.get('error', '')}")
        return 0
    if args.cmd == "verify-file":
        result = verify_file_evidence(args.manifest, cafile=args.cafile)
        print(json.dumps(result, indent=1, sort_keys=True))
        return 0 if result["verified"] else 1
    if args.cmd == "stamp":
        evidence = stamp_manifest(args.manifest, cafile=args.cafile)
        for e in evidence["evidence"]:
            print(f"{e.get('name'):12s} {e.get('gen_time_utc', '-'):22s} verified={e.get('verified_on_this_machine')} "
                  f"{e.get('error', '')}")
        return 0
    result = verify_evidence(args.manifest, cafile=args.cafile)
    print(json.dumps(result, indent=1, sort_keys=True))
    return 0 if result["verified"] else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(_main())
