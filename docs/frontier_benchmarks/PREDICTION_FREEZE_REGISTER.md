# Prediction freeze register

*Frontier Benchmarking division.  One row per freeze, newest last.  A freeze is a directory
under `experiments/frontier/freezes/` with a `MANIFEST.json` in normal form; its identity is
the SHA-256 of that file.  Tooling and its limits: `src/metricchain_fb/freeze.py`,
`timestamp.py`, `commitment.py`; rules: `ASSESSMENT_PROTOCOLS.md` §3.*

## How to check any row yourself

```
python -m metricchain_fb.freeze verify experiments/frontier/freezes            # bytes unchanged?
python -m metricchain_fb.timestamp verify experiments/frontier/freezes/<dir>/MANIFEST.json
sha256sum experiments/frontier/freezes/<dir>/MANIFEST.json                     # must equal the row
openssl ts -verify -digest <manifest sha256> -in <dir>/timestamps/digicert.tsr -CAfile /etc/ssl/certs/ca-certificates.crt
```

`tests/frontier/test_freeze.py::test_every_committed_freeze_is_intact` runs the first line in
strict mode: editing, adding or removing any file of any freeze fails the test-suite.

## What a row does and does not establish

* **Does:** the manifest and every artifact it lists existed, byte for byte, no later than the
  earliest time attested by a time-stamp token that verifies ("attested not later than").
  The tokens are RFC 3161 tokens from unrelated commercial authorities; only the manifest's
  digest was sent to them.
* **Does not:** that the reference answers were unavailable to the party that produced the
  artifacts.  That is the column "reference at freeze time", argued in the manifest
  (`reference_status`, `contamination_assessment`) from evidence about release dates and
  training data — and it can be wrong even when every hash verifies.
* **Never:** a commit date is not used as evidence of anything.  The commit that first
  contains a freeze is recorded for navigation only.

## Rules

1. A frozen manifest is never rewritten.  A changed prediction is a new freeze with a new
   identifier, and if the change was made after the reference or the official comparison
   became available it is a separate **retrospective** experiment and is labelled so.
2. The assessment class is declared in the manifest at freeze time and is never upgraded.
3. A freeze lists its exclusions (targets or cases left out) with reasons, at freeze time.
4. Missing predictions, failed computations and rejected certificates are artifacts of the
   freeze like any other.
5. Assessment results are recorded in `RESULTS.md` / `NEGATIVE_RESULTS.md` with the freeze
   identifier; the row below is then marked *assessed*, never edited otherwise.

## Register

| id | what was frozen | kind · class · stage | manifest SHA-256 | attested not later than (verifying authorities) | reference at freeze time | status |
|---|---|---|---|---|---|---|
| FRONTIER-FRZ-0001 | public state of CASP17 three days before the announced results: target list, download-area listings, announcements, PDB release status of the references named on the list (`FRONTIER-FRZ-0001_casp17_public_state/`) | data-snapshot · n/a · n/a | `899f916eb2bbf6747f1237ec305276b591c36229c57d822fed1cfed83bde0d29` | 2026-11-26T23:03:21Z (DigiCert, Sectigo, GlobalSign, Certum; all four verify) | no prediction in this freeze; it *is* the record of what was public: results page "No results available yet", reference and results directories empty, 19 of 239 targets with a released PDB entry | frozen |
