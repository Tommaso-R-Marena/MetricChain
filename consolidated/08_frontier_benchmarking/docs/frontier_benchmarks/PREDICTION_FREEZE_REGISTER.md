# Prediction freeze register

*Frontier Benchmarking division.  One row per freeze, newest last.  A freeze is a directory
under `experiments/frontier/freezes/` with a `MANIFEST.json` in normal form; its identity is
the SHA-256 of that file.  Tooling and its limits: `src/metricchain_fb/freeze.py`,
`timestamp.py`, `commitment.py`; rules: `ASSESSMENT_PROTOCOLS.md` §3.*

## How to check any row yourself

From the repository root, with `PYTHONPATH=src` (the package is not installed):

```
export PYTHONPATH=src
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
| FRONTIER-FRZ-0002 | **sealed held-out list v1**: 47 high-resolution single-chain crystal structures first released on or after 2026-07-01, one per 30 % cluster, in a secret salted order; public rule and query, salted commitment, encrypted list (`FRONTIER-FRZ-0002_heldout_commitment_v1/`).  For FB-P-01 (held-out stage), FB-P-02, SB-BM-3, SB-BM-6 | held-out-commitment · n/a · held-out | `c5df5b3cdedcf5a3389ff1cde78959d563a4e7d0e39247eda332ed4d8df54284` | 2026-11-26T23:42:32Z (DigiCert, Sectigo, GlobalSign, Certum; all verify) | the members are public PDB entries — "held out" from development, never blind; membership and order unknown to the software division; passphrase and commitment salt with the research owner | sealed; to be opened after the software division freezes its release |
| FRONTIER-FRZ-0003 | **our scores of every public CASP17 model file of T2409, T2410, T2411** (1,163 files) against the released PDB references, with the plan for comparing them with the official numbers (`FRONTIER-FRZ-0003_casp17_scoring_check/`).  Tests our scoring code, no MetricChain method | scores · **A-PLB** · development | `2a65d774cfb244c1413ef10bba1c6a2fc9341011627ce112fbcd74e4a46cb334` | 2026-11-26T23:58:17Z (the same four; all verify) | references public (PDB, released 2026-09-16); official per-model scores not public (results announced for 2026-11-29) | frozen; **to be assessed** against the official numbers by `COMPARISON_PLAN.md` |

## Freezes kept by other divisions

The engineering division keeps the custody record of every batch it runs, in its own format
(`docs/engineering/benchmarks/PREDICTION_FREEZE.md` on its branch: `MANIFEST.sha256`,
`PROVENANCE.json`, `FREEZE.md`, pushed at once).  Its words *blind*, *pre-leaderboard* and
*retrospective* correspond to our classes A-PRR, A-PLB and A-RET; its rule that a prediction
whose category cannot be established is retrospective is adopted here for anything reported
as a prediction.  Its batches are indexed in this register by manifest digest when they
exist; none exists yet.  Any file can be time-stamped without being modified:
`python -m metricchain_fb.timestamp stamp-file PATH`.
