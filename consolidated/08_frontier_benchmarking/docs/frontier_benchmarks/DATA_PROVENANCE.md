# Data provenance

*Frontier Benchmarking division.  Every external source this division has read or stored,
with where it came from, when, under what terms, and what — if anything — is kept in the
repository.  Sources consulted only by the literature assessors are listed, with their read
levels, in the source tables of `literature/*.md` and are not repeated here.*

## 1. Principles

* Third-party data are **referenced by URL, retrieval time and SHA-256**; they are copied
  into the repository only when small, licensed for redistribution and needed as evidence.
* Raw downloads live outside the repository tree and are treated as untrusted input
  (parsed by scripts kept elsewhere, Python run with `-I`).
* Nothing private, nothing that identifies a person, no credentials.
* A dataset's licence and its fitness for a purpose are two questions; both are recorded.

## 2. Sources retrieved by the coordinator

| source | what | retrieved (UTC) | terms | kept in the repository | checksum record |
|---|---|---|---|---|---|
| Protein Structure Prediction Center, `predictioncenter.org/casp17/` | index, message board, target list (HTML and CSV), format and Q&A pages, domain summary, results page | 2026-11-26 22:37–23:02 | CC BY 4.0 (site terms of use) | target list CSV verbatim (21 kB); short verbatim extracts of two announcements and of the results page; parsed directory listings | FRZ-0001 `pages_sha256.json` (every raw page), manifest |
| the same, `/download_area/CASP17/` | directory listings of predictions, sequences, targets, results, extra experiments; four sequence files (165 kB) | 2026-11-26 22:38–23:02 | CC BY 4.0 | listings as JSON; sequence files not stored (checksums only) | FRZ-0001 |
| RCSB PDB Data API, `data.rcsb.org/rest/v1/core/entry/<ID>` | deposit and release dates, method, resolution, title for the 19 entries named on the CASP17 target list (one more identifier returned 404: a ligand code) | 2026-11-26 ≈22:58 | PDB data are CC0 1.0 | the 20 small records as JSON | FRZ-0001 `rcsb_release_status.json` |
| public RFC 3161 time-stamping authorities (DigiCert, Sectigo, GlobalSign, Certum) | time-stamp tokens for manifest digests | at each freeze | public services; **only a SHA-256 digest is sent** | tokens (`timestamps/*.tsr`, 6–8 kB each) | `MANIFEST.evidence.json` of each freeze |
| the same four plus others, connectivity probe | tokens for a 55-byte probe file with no content | 2026-11-26 22:55 | as above | two tokens as test fixtures (`tests/frontier/data/`) | test-suite |
| INRAE "EvalGM" graphical-model benchmark repository, `web-genobioinfo.toulouse.inrae.fr/~degivry/evalgm/` | directory indexes and two readme files; from `MRF/ProteinFolding/`: the ten fixed-sequence instances `pdb*.wcsp.xz` in full (3.6 MB), and only the first 300 kB of each of the eleven other instances, to read their headers | 2026-11-26 23:11 | no licence statement found on the pages read — **redistribution status unknown**; instances are referenced by URL and SHA-256, never copied | nothing but checksums | SHA-256 of each instance file in the rows of `experiments/frontier/exploratory_gmec/results/` |
| Protein Structure Prediction Center, public prediction archives `predictions/regular/T2409.tar.gz`, `T2410.tar.gz`, `T2411.tar.gz` | every group's submitted models for three targets (1,163 files) — **scored, not used as inputs to any prediction** | 2026-11-26 23:27 | CC BY 4.0 | derived score tables only (FRZ-0003) | archive SHA-256 in the FRZ-0003 manifest |
| RCSB PDB, coordinate files `30ZQ.cif`, `31GL.cif`, `30ZR.cif`, `1CRN.cif` | references of the three targets; one 0.945 Å structure as a test fixture | 2026-11-26 23:26–23:27 | CC0 1.0 | `1crn.cif` as a test fixture (69 kB); the others by checksum | FRZ-0003 manifest |
| RCSB PDB search and GraphQL services | the candidate pool of the held-out list (150 entries) and their metadata | 2026-11-26 23:40 | CC0 1.0 | the query; counts; a digest of the pool; the list itself only encrypted | FRZ-0002 |
| Ensemble division, `experiments/ensemble/benchmarks/controls_v1.json` at `2d2054d` | 18 planted controls (internal source, listed for completeness) | read from the repository | — | not copied; results of our recomputation in `experiments/frontier/exploratory_identification/results/` | SHA-256 `48f095b1d39e1851099c89434d1ee3496a09a299b6fe312b4004e33e461d8a4e` |
| Structural-biology division, `src/metricchain_sb/` at `720e0ec` and `1756529` | the software evaluated in the pilot (internal source) | `git archive` into a scratch directory | — | not copied | commit ids |
| PyPI | Python packages listed in `requirements-frontier.txt` (plus `pytoulbar2` 1.4.0.3, MIT, installed for a planned baseline) | 2026-11-26 | each package's licence | version pins only | `requirements-frontier.txt` |

## 3. Derived data, and who derived it

| file | derived from | by | caveat |
|---|---|---|---|
| FRZ-0001 `targets_classified.csv` | CASP17 target list ⋈ RCSB release records | `experiments/frontier/build_casp17_snapshot.py` | "no PDB code on the target list" is **not** evidence that a structure is unreleased |
| FRZ-0001 `download_area_listing.json` | Apache directory listings | same script (regular expression over the HTML) | sizes are as displayed (rounded), not byte counts |

## 4. Sources deliberately not used

| source | why not |
|---|---|
| the "CASP-DREAM TAP" challenge announced on 2026-11-25 (which peptide–MHC complexes bind which T-cell receptors) | a target-specific functional prediction task; outside the charter |
| protein- and binder-design benchmarks; affinity-optimisation benchmarks | outside the charter (sequence engineering, target-specific optimisation) |
| mutational-scan stability data as training or optimisation targets | in scope only as measured thermodynamic reference values for fixed sequences; never as an objective |
| the public CASP17 prediction archives as *inputs to a prediction* | every model there is a participant's prediction; using them as inputs would make any output a derivative of someone else's entry (`CASP17_ASSESSMENT.md` §4.3).  They may be *scored* as public models in tests of our scoring tools |
