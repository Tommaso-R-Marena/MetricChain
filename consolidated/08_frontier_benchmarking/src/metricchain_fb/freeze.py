"""Freeze manifests: a tamper-evident record of *what* was fixed, *from what*, and *under which
declared conditions*, made before an assessment.

A freeze is a directory holding the frozen artifacts and one file ``MANIFEST.json``:

* every artifact is listed with its size and SHA-256;
* the manifest carries the provenance the research owner's directive asks for (source commits,
  protocol version, method and dependency versions, inputs with their checksums, declared
  training cut-offs, seeds, configuration files, the status of the reference at freeze time, a
  contamination assessment, exclusions with reasons);
* the manifest is written in a *normal form* (sorted keys, one-space indent, ASCII, final
  newline), so that the manifest's identity is simply the SHA-256 of the file's bytes and can
  be recomputed with any ``sha256sum``;
* evidence about *when* the manifest existed (RFC 3161 time-stamp tokens, the commit that
  first contained it) is kept **outside** the manifest, in ``MANIFEST.evidence.json`` and
  ``timestamps/``, because it can only be produced after the manifest's digest is known.

What a freeze establishes, and what it does not.  A verified manifest plus a verified
time-stamp token establishes that these exact bytes existed no later than the token's time.
It does **not** establish that the reference answers were unavailable to whoever produced the
artifacts: that is a separate statement (``reference_status``, ``contamination_assessment``)
which must be argued from evidence about when the reference became public and what the method
was trained or tuned on.  A commit date alone establishes nothing of the kind.

Only the Python standard library is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

__all__ = [
    "SCHEMA", "ASSESSMENT_CLASSES", "EVIDENCE_STAGES", "KINDS", "MANIFEST_NAME", "EVIDENCE_NAME",
    "sha256_bytes", "sha256_file", "normal_form", "scan_artifacts", "build_manifest",
    "write_manifest", "load_manifest", "validate_manifest", "verify_freeze", "VerifyReport",
    "ManifestError",
]

SCHEMA = "metricchain-fb-freeze/1"
MANIFEST_NAME = "MANIFEST.json"
EVIDENCE_NAME = "MANIFEST.evidence.json"
TIMESTAMP_DIR = "timestamps"

#: Assessment classes of the division (docs/collaboration/README.md, addendum).
ASSESSMENT_CLASSES = ("A-OPB", "A-PRR", "A-PLB", "A-RET", "A-EXP", "A-UNK", "n/a")
EVIDENCE_STAGES = ("exploratory", "development", "held-out", "replication", "n/a")
KINDS = ("prediction", "scores", "baseline", "protocol", "data-snapshot", "held-out-commitment",
         "control")
REFERENCE_PUBLIC = ("yes", "no", "partly", "unknown", "n/a")

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_ID = re.compile(r"^FRONTIER-FRZ-\d{4}$")


class ManifestError(ValueError):
    """The manifest is not a well-formed object of the schema."""


# --------------------------------------------------------------------------- hashing, normal form
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: os.PathLike, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def normal_form(obj) -> bytes:
    """The unique byte representation of a manifest: sorted keys, indent 1, ASCII, final newline.

    Floats are refused: a manifest holds strings, integers, booleans, lists and objects only, so
    that no platform-dependent number formatting can change the bytes.
    """
    _refuse_floats(obj)
    return (json.dumps(obj, sort_keys=True, indent=1, ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def _refuse_floats(obj, where: str = "manifest") -> None:
    if isinstance(obj, float):
        raise ManifestError(f"{where}: floating-point numbers are not allowed in a manifest (use strings)")
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise ManifestError(f"{where}: object keys must be strings")
            _refuse_floats(v, f"{where}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            _refuse_floats(v, f"{where}[{i}]")
    elif not (obj is None or isinstance(obj, (str, int, bool))):
        raise ManifestError(f"{where}: unsupported value of type {type(obj).__name__}")


# --------------------------------------------------------------------------- artifact listing
def _check_relpath(rel: str) -> None:
    if not isinstance(rel, str) or not rel:
        raise ManifestError("artifact path must be a non-empty string")
    if "\\" in rel or "\x00" in rel:
        raise ManifestError(f"artifact path {rel!r}: backslashes and NUL are not allowed")
    p = PurePosixPath(rel)
    if p.is_absolute() or any(part in ("..", ".", "") for part in p.parts):
        raise ManifestError(f"artifact path {rel!r} must be relative, normalised and inside the freeze directory")
    if str(p) != rel:
        raise ManifestError(f"artifact path {rel!r} is not in normal form ({str(p)!r})")


def _is_bookkeeping(rel: str) -> bool:
    """Files of the freeze directory that are *about* the manifest and are never artifacts."""
    return rel in (MANIFEST_NAME, EVIDENCE_NAME) or rel.startswith(TIMESTAMP_DIR + "/")


def scan_artifacts(root: os.PathLike) -> list:
    """All regular files under ``root`` except the bookkeeping files, as sorted manifest entries.

    Symbolic links are refused (a link's target could change without the link's bytes changing).
    """
    root = Path(root)
    entries = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for name in list(dirnames):
            if (Path(dirpath) / name).is_symlink():
                raise ManifestError(f"symbolic link in freeze directory: {Path(dirpath) / name}")
        for name in sorted(filenames):
            full = Path(dirpath) / name
            rel = full.relative_to(root).as_posix()
            if _is_bookkeeping(rel):
                continue
            if full.is_symlink():
                raise ManifestError(f"symbolic link in freeze directory: {full}")
            if not full.is_file():
                raise ManifestError(f"not a regular file: {full}")
            _check_relpath(rel)
            entries.append({"path": rel, "bytes": full.stat().st_size, "sha256": sha256_file(full)})
    entries.sort(key=lambda e: e["path"])
    return entries


# --------------------------------------------------------------------------- manifest content
_REQUIRED = {
    "schema": str, "freeze_id": str, "kind": str, "title": str, "assessment_class": str,
    "evidence_stage": str, "created_utc": str, "source_commits": dict, "protocol": dict,
    "method": dict, "inputs": list, "random_seeds": list, "config_files": list,
    "reference_status": dict, "contamination_assessment": str, "exclusions": list,
    "artifacts": list, "notes": str,
}


def validate_manifest(m) -> None:
    """Raise :class:`ManifestError` unless ``m`` is a well-formed manifest of the schema."""
    if not isinstance(m, dict):
        raise ManifestError("manifest must be a JSON object")
    _refuse_floats(m)
    for key, typ in _REQUIRED.items():
        if key not in m:
            raise ManifestError(f"missing field {key!r}")
        if not isinstance(m[key], typ) or (typ is not bool and isinstance(m[key], bool)):
            raise ManifestError(f"field {key!r} must be of type {typ.__name__}")
    unknown = set(m) - set(_REQUIRED)
    if unknown:
        raise ManifestError(f"unknown field(s): {sorted(unknown)}")
    if m["schema"] != SCHEMA:
        raise ManifestError(f"schema must be {SCHEMA!r}")
    if not _ID.match(m["freeze_id"]):
        raise ManifestError("freeze_id must look like FRONTIER-FRZ-0001")
    if m["kind"] not in KINDS:
        raise ManifestError(f"kind must be one of {KINDS}")
    if m["assessment_class"] not in ASSESSMENT_CLASSES:
        raise ManifestError(f"assessment_class must be one of {ASSESSMENT_CLASSES}")
    if m["evidence_stage"] not in EVIDENCE_STAGES:
        raise ManifestError(f"evidence_stage must be one of {EVIDENCE_STAGES}")
    if not _UTC.match(m["created_utc"]):
        raise ManifestError("created_utc must look like 2026-11-26T23:59:59Z")
    if not m["title"].strip():
        raise ManifestError("title must not be empty")
    for name, commit in m["source_commits"].items():
        if not isinstance(commit, str) or not _HEX40.match(commit):
            raise ManifestError(f"source_commits[{name!r}] must be a full 40-hex commit id")
    for key in ("id", "version"):
        if not isinstance(m["protocol"].get(key), str) or not m["protocol"][key]:
            raise ManifestError(f"protocol.{key} must be a non-empty string")
    for key in ("name", "version", "declared_training_cutoff"):
        if not isinstance(m["method"].get(key), str) or not m["method"][key]:
            raise ManifestError(f"method.{key} must be a non-empty string ('n/a' if it does not apply)")
    if not isinstance(m["method"].get("dependencies", {}), dict):
        raise ManifestError("method.dependencies must be an object")
    for i, item in enumerate(m["inputs"]):
        if not isinstance(item, dict) or not isinstance(item.get("description"), str):
            raise ManifestError(f"inputs[{i}] must be an object with a description")
        if "sha256" in item and not (isinstance(item["sha256"], str) and _HEX64.match(item["sha256"])):
            raise ManifestError(f"inputs[{i}].sha256 must be 64 lowercase hex digits")
    for i, item in enumerate(m["config_files"]):
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) \
                or not (isinstance(item.get("sha256"), str) and _HEX64.match(item["sha256"])):
            raise ManifestError(f"config_files[{i}] must be an object with path and sha256")
    for i, seed in enumerate(m["random_seeds"]):
        if isinstance(seed, bool) or not isinstance(seed, (int, str)):
            raise ManifestError(f"random_seeds[{i}] must be an integer or a string")
    rs = m["reference_status"]
    if rs.get("reference_public_at_freeze") not in REFERENCE_PUBLIC:
        raise ManifestError(f"reference_status.reference_public_at_freeze must be one of {REFERENCE_PUBLIC}")
    if not isinstance(rs.get("statement"), str) or not rs["statement"].strip():
        raise ManifestError("reference_status.statement must say what was public at freeze time and how that is known")
    if not m["contamination_assessment"].strip():
        raise ManifestError("contamination_assessment must not be empty (write what is known and what is not)")
    for i, item in enumerate(m["exclusions"]):
        if not isinstance(item, dict) or not isinstance(item.get("item"), str) or not isinstance(item.get("reason"), str):
            raise ManifestError(f"exclusions[{i}] must be an object with item and reason")
    seen = set()
    previous = None
    for i, a in enumerate(m["artifacts"]):
        if not isinstance(a, dict) or set(a) != {"path", "bytes", "sha256"}:
            raise ManifestError(f"artifacts[{i}] must have exactly the fields path, bytes, sha256")
        _check_relpath(a["path"])
        if _is_bookkeeping(a["path"]):
            raise ManifestError(f"artifacts[{i}]: {a['path']!r} is a bookkeeping file, not an artifact")
        if isinstance(a["bytes"], bool) or not isinstance(a["bytes"], int) or a["bytes"] < 0:
            raise ManifestError(f"artifacts[{i}].bytes must be a natural number")
        if not (isinstance(a["sha256"], str) and _HEX64.match(a["sha256"])):
            raise ManifestError(f"artifacts[{i}].sha256 must be 64 lowercase hex digits")
        if a["path"] in seen:
            raise ManifestError(f"artifact listed twice: {a['path']!r}")
        if previous is not None and a["path"] < previous:
            raise ManifestError("artifacts must be sorted by path")
        seen.add(a["path"])
        previous = a["path"]
    # The assessment class constrains what may be claimed about the reference.
    if m["assessment_class"] == "A-PRR" and rs["reference_public_at_freeze"] != "no":
        raise ManifestError("class A-PRR (pre-reference-release) requires reference_public_at_freeze == 'no'")
    if m["assessment_class"] == "A-OPB":
        raise ManifestError("class A-OPB (official prospective blind) cannot be self-declared by this tool")


def build_manifest(root: os.PathLike, metadata: dict) -> dict:
    """Manifest for the directory ``root``: ``metadata`` (everything except ``schema`` and
    ``artifacts``) plus the scanned artifact list.  The result is validated."""
    m = dict(metadata)
    if "artifacts" in m or "schema" in m:
        raise ManifestError("metadata must not contain 'schema' or 'artifacts'")
    m["schema"] = SCHEMA
    m["artifacts"] = scan_artifacts(root)
    validate_manifest(m)
    return m


def write_manifest(root: os.PathLike, manifest: dict, overwrite: bool = False):
    """Write ``MANIFEST.json`` in normal form; returns ``(path, sha256 of the file)``.

    Refuses to overwrite an existing manifest unless asked: a frozen manifest is not edited, a
    changed one is a new freeze with a new identifier.
    """
    validate_manifest(manifest)
    path = Path(root) / MANIFEST_NAME
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; a freeze is never rewritten (make a new freeze)")
    data = normal_form(manifest)
    path.write_bytes(data)
    return path, sha256_bytes(data)


def load_manifest(path: os.PathLike):
    """Returns ``(manifest, sha256 of the file bytes, bytes are in normal form)``."""
    data = Path(path).read_bytes()
    try:
        manifest = json.loads(data.decode("ascii"), parse_float=_no_float)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"{path}: not ASCII JSON ({exc})") from None
    try:
        is_normal = normal_form(manifest) == data
    except ManifestError:
        is_normal = False
    return manifest, sha256_bytes(data), is_normal


def _no_float(text):
    raise ManifestError(f"floating-point number {text!r} in manifest")


# --------------------------------------------------------------------------- verification
@dataclass
class VerifyReport:
    manifest_sha256: str = ""
    freeze_id: str = ""
    n_artifacts: int = 0
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def summary(self) -> str:
        head = f"{self.freeze_id or '?'}  manifest sha256 {self.manifest_sha256 or '?'}  artifacts {self.n_artifacts}"
        lines = [head, "RESULT: " + ("INTACT" if self.ok else "NOT INTACT")]
        lines += [f"  error: {e}" for e in self.errors]
        lines += [f"  warning: {w}" for w in self.warnings]
        return "\n".join(lines)


def verify_freeze(manifest_path: os.PathLike, strict: bool = True) -> VerifyReport:
    """Recompute everything the manifest states about the directory it sits in.

    Errors: malformed manifest, manifest not in normal form, missing artifact, size or checksum
    mismatch, symbolic links, and (``strict``) files present but not listed.  The function never
    raises on bad content: every defect is an entry of the report.
    """
    report = VerifyReport()
    manifest_path = Path(manifest_path)
    root = manifest_path.parent
    try:
        manifest, digest, is_normal = load_manifest(manifest_path)
    except (OSError, ManifestError) as exc:
        report.errors.append(f"cannot read manifest: {exc}")
        return report
    report.manifest_sha256 = digest
    try:
        validate_manifest(manifest)
    except ManifestError as exc:
        report.errors.append(f"malformed manifest: {exc}")
        return report
    report.freeze_id = manifest["freeze_id"]
    report.n_artifacts = len(manifest["artifacts"])
    if not is_normal:
        report.errors.append("manifest bytes are not in normal form (the file was edited or re-serialised)")
    listed = set()
    for a in manifest["artifacts"]:
        listed.add(a["path"])
        full = root / a["path"]
        if full.is_symlink():
            report.errors.append(f"artifact is a symbolic link: {a['path']}")
            continue
        if not full.is_file():
            report.errors.append(f"artifact missing: {a['path']}")
            continue
        size = full.stat().st_size
        if size != a["bytes"]:
            report.errors.append(f"artifact size changed: {a['path']} ({size} bytes, manifest says {a['bytes']})")
            continue
        if sha256_file(full) != a["sha256"]:
            report.errors.append(f"artifact content changed: {a['path']}")
    try:
        present = {e["path"] for e in scan_artifacts(root)}
    except ManifestError as exc:
        report.errors.append(str(exc))
        present = listed
    extra = sorted(present - listed)
    for rel in extra:
        (report.errors if strict else report.warnings).append(f"file present but not listed: {rel}")
    return report


def iter_manifests(base: os.PathLike) -> Iterable[Path]:
    """Every ``MANIFEST.json`` below ``base`` (sorted)."""
    return sorted(Path(base).rglob(MANIFEST_NAME))


# --------------------------------------------------------------------------- command line
def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m metricchain_fb.freeze", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_create = sub.add_parser("create", help="scan a directory and write its MANIFEST.json")
    p_create.add_argument("directory")
    p_create.add_argument("--metadata", required=True, help="JSON file with every manifest field except schema and artifacts")
    p_verify = sub.add_parser("verify", help="verify one MANIFEST.json, or every manifest below a directory")
    p_verify.add_argument("path")
    p_verify.add_argument("--lenient", action="store_true", help="unlisted files are warnings, not errors")
    p_digest = sub.add_parser("digest", help="print the SHA-256 of a file")
    p_digest.add_argument("path")
    args = parser.parse_args(argv)
    if args.cmd == "digest":
        print(sha256_file(args.path))
        return 0
    if args.cmd == "create":
        metadata = json.loads(Path(args.metadata).read_text(encoding="ascii"), parse_float=_no_float)
        manifest = build_manifest(args.directory, metadata)
        path, digest = write_manifest(args.directory, manifest)
        print(f"{path}\nsha256 {digest}\nartifacts {len(manifest['artifacts'])}")
        return 0
    target = Path(args.path)
    manifests = [target] if target.is_file() else list(iter_manifests(target))
    if not manifests:
        print(f"no {MANIFEST_NAME} found under {target}")
        return 1
    status = 0
    for path in manifests:
        report = verify_freeze(path, strict=not args.lenient)
        print(f"{path}\n{report.summary()}")
        status |= 0 if report.ok else 1
    return status


if __name__ == "__main__":  # pragma: no cover
    sys.exit(_main())
