# Reproducibility and provenance of the archive

*Written for the archive on 2026-11-27; updated at the final refresh of the same day (§8 says what a
refresh is).  Paths are relative to `consolidated/`.*

| file | content |
|---|---|
| `README.md` | this file |
| [`PINNED_COMMITS.md`](PINNED_COMMITS.md) | generated: branch, pinned commit, date and size per division |
| [`EXCLUDED_ARTIFACTS.md`](EXCLUDED_ARTIFACTS.md) | generated: every file left out, with path, commit, git object id, SHA-256 and the retrieval command |
| [`LEAN_FILES.md`](LEAN_FILES.md) | generated: every Lean file with line, declaration, `sorry` and `axiom` counts and its imports within the project (a text scan, not a build) |
| `pins.json` | the input of the build: branch and commit per division, the sealed paths, the quoted audit statements |
| `build_archive.py` | builds `consolidated/` from `pins.json` (standard library only) |
| `verify_manifest.py` | checks a copy of the archive against `MANIFEST.json` |
| `scan_sensitive.py` | the scan for credentials, personal data and local paths run before publication |

## 1. Pinned commits

<!-- GEN:pins -->
| # | division | branch | pinned commit | commit date (UTC) | merge-base with theory | files | MiB |
|---|---|---|---|---|---|---:|---:|
| 01 | Theoretical Research Division | `claude/determined-ride-og1u7j` | `b3c5d6115df06bb160d6490a95d9ec6e1a108d02` | 2026-11-27 01:26:54 | — | 1864 | 18.46 |
| 02 | Computational Research Division (engineering) | `research/ubuntu-engineering` | `dcb49f3e0372b0383bf816ef4050716b5d8da5e6` | 2026-11-27 18:46:01 | `d81eb8aba138` | 722 | 36.84 |
| 03 | Scientific Discovery, Translation & Independent Validation Division | `research/scientific-translation` | `340081afba8841a4093b3df9b18387e8a36f20b1` | 2026-11-27 01:17:37 | `5ed407282d89` | 4281 | 60.43 |
| 04 | Ensemble Identifiability and Certified Inference Division | `research/ensemble-identifiability` | `a089a0ce2427c7f3797b838837d16659c8b0a1e4` | 2026-11-27 01:24:04 | `a844b5a8f374` | 181 | 2.20 |
| 05 | Geometric Inference, Rigidity and Inverse Problems Division | `research/geometric-inference` | `229527e37bbd53428f31718339b7ceb61bc1e942` | 2026-11-27 01:08:57 | `a844b5a8f374` | 189 | 1.88 |
| 06 | Mathematical Biology and Computational Complexity Division | `research/biological-complexity` | `4a09627d3560dc86cf162bce6c93f030ae84efb9` | 2026-11-27 01:27:10 | `a844b5a8f374` | 437 | 2.95 |
| 07 | Structural & Computational Biology, Software Development and Applications Division | `research/structural-biology` | `a5cc106dd59d984237dff483716360cae5306538` | 2026-11-27 02:49:58 | `b2caab689155` | 127 | 9.58 |
| 08 | Frontier Benchmarking, Experimental Evidence and Scientific Evaluation Division | `research/frontier-benchmarks` | `14254f33bee9cc33f7e015f5ec5c58976f7efcb5` | 2026-11-27 01:25:04 | `b2caab689155` | 98 | 1.15 |
| | **all eight** | | | | | **7899** | **133.48** |
<!-- /GEN:pins -->

<!-- GEN:totals -->
7899 files (133.48 MiB) imported from the eight branches; 3 files (24.74 MiB) left out by reference; heads pinned at 2026-11-27T18:47:45Z.
<!-- /GEN:totals -->

## 2. What was copied, and by which rule

* **Ownership.**  All eight branches descend from one root (`897242c`).  The theory branch is the trunk;
  every other division forked from it and never rewrote the theory files.  The archive therefore takes
  the *whole tree* of the theory head, and for every other division the files it **added or modified
  relative to the merge-base** of its pinned commit with the pinned theory commit.  Checked when the
  archive was built: these sets are disjoint except for `docs/collaboration/README.md` (each division
  edited its own copy of the mailbox rules), `proofs/AxiomAudit.lean` (ensemble, geometry) and the root
  `README.md` (geometry); each such copy is kept under its division.  No division deleted a file of the
  trunk.  Eight stored outputs exist with identical content in two divisions (seven outputs of science's reviews
  that theory keeps with its checks of those reviews, and one output of engineering's replication of a
  theory benchmark that is byte-identical to theory's own); the manifest marks them (`same_content_as`).
  Where theory adopted a Lean file of science (`RateFull.lean`) it added a provenance header, so the two
  copies differ.
* **Paths.**  `consolidated/<NN_division>/<original repository path>`.  Nothing was renamed.
* **Bytes.**  Every imported file is the same git object as in the source branch (the manifest gives the
  object id; `verify_manifest.py --git` checks it).  Nothing was edited or redacted.
* **A consequence to keep in mind.**  A division's tree at its pinned commit also contains the theory
  files *as they were at its merge-base*, not as they are at the theory head.  To build a division's Lean
  proofs or run its code exactly as its authors did, check out its pinned commit; the archive is for
  reading, not for building in place.

## 3. What was left out

<!-- GEN:excluded -->
| division | file | bytes | reason | git object | SHA-256 |
|---|---|---:|---|---|---|
| structbio | `experiments/structbio/gmec_dev/certs/v2-lib/1UBQ.mincert.json` | 10035244 | larger-than-5-MiB | `1ec678294f77494990a20ccc0f74b4ec48270b17` | `0c9dfbd9392ec930eeddf41ef53ff7a475d09237782e83ecd5f422c242a1ad79` |
| structbio | `experiments/structbio/gmec_dev/certs/v2/1UBQ.mincert.json` | 15901276 | larger-than-5-MiB | `f6c18f9d8192a0379985737fa2221ad3e7306267` | `f1250c338d0fc8342d6c2cf8995fdbde1f15f091064c1a6e6dc9d5b54a981954` |
| frontier | `experiments/frontier/freezes/FRONTIER-FRZ-0002_heldout_commitment_v1/sealed_list_v1.enc` | 2736 | sealed-evaluation-material | `562e85f0682b82616f81d6ab263a5eaaeeb87e84` | not computed (file not read) |
<!-- /GEN:excluded -->

Rules: (1) sealed evaluation material is never copied and was not read, not even to compute a checksum —
the manifest gives its git object id, which is public metadata of the branch; (2) files larger than 5 MiB
are referenced with their SHA-256; (3) caches and build products would be referenced — none is committed
in any branch.  To retrieve a file:

```
git clone https://github.com/Tommaso-R-Marena/MetricChain.git && cd MetricChain
git show <pinned commit of the division>:<original path> > <local file>
sha256sum <local file>            # compare with EXCLUDED_ARTIFACTS.md
```

Not in any branch and therefore not referenced: untracked caches that divisions describe as regenerable
(science: the caches of `ws_P3`, `ws_P6` and referees' data files; "each report says how"); logs of cloud
jobs; tool installations (Lean and Mathlib builds, toulbar2, OpenMM); the credentials of the sealed list.

## 4. Verifying a copy

```
python3 consolidated/11_reproducibility/verify_manifest.py          # checksums of every listed file
python3 consolidated/11_reproducibility/verify_manifest.py --git    # also: identity with the pinned commits (needs a full clone)
```

To rebuild from scratch: clone the repository with all branches, check out `research/consolidated-archive`,
and run `python3 consolidated/11_reproducibility/build_archive.py`; the output is a function of
`pins.json` and of the hand-written files only, so `git status` must then show no change.

Run on the final version before it was published: `7899 imported artifacts and 23 index files listed; 0
problems`, with `--git` — every imported file is the identical git object of its pinned commit.

## 5. The scan before publication

`scan_sensitive.py` searches every text file of the archive for key and token formats, private-key
blocks, assignments of secrets, e-mail addresses, home-directory paths and service URLs, and for a list
of literal strings supplied at run time (the names of the compute workspace and of the local account,
which are not written anywhere in the archive).  Result for this version: no credential, no supplied
literal.  Findings left in place because they are not sensitive: the path `/home/user` of the divisions'
cloud containers (331 occurrences); one public contact address of the CASP organisers inside a frozen
copy of their public announcements (`08_frontier_benchmarking/…/FRONTIER-FRZ-0001_casp17_public_state/announcements_extract.txt`);
three matrix products in Python source that look like addresses.  A second pass looked for a salt or
passphrase written next to a long token and found only git object ids, file paths and the public manifest
digest of the held-out commitment.

Final version: 7847 text files scanned; the same findings as in the interim version and no others (the
container path, counting its mention in this paragraph and in two generated files, 332 times; four
address-like strings); no credential, no supplied literal.  The sealed file is not in the tree.

## 6. Environments and toolchains

Nothing was installed or built for the archive.  Where each division records how to re-run its work:

| division | toolchain pins | how to re-run |
|---|---|---|
| theory | `01_theory/lean-toolchain`, `lake-manifest.json`, `lakefile.lean` | `01_theory/scripts/audit_all.sh`, `scripts/lean_env.sh`; `01_theory/docs/RESEARCH_LOG.md` ("Resume here") |
| engineering | (Python package under `02_engineering/src/metricchain_eng/`; versions in the reproducibility note) | `02_engineering/docs/engineering/benchmarks/REPRODUCIBILITY.md`; every message's "reproduction" section; `make_tables*.py --verify` regenerate the published tables from stored rows |
| science | — | `03_scientific_translation/docs/science/RESEARCH_SYNTHESIS.md` §0; each workstream report |
| ensemble | — | `04_ensemble_identifiability/docs/ensemble/HANDOFF.md`; `experiments/ensemble/run_all.py`, `check_quotes.py` |
| geometry | — | `05_geometric_inference/docs/geometry/HANDOFF.md`; `experiments/geometry/run_checks.py` |
| complexity | — | `06_biological_complexity/docs/complexity/HANDOFF.md` |
| structural biology | `07_structural_biology/requirements-structbio.txt` | `07_structural_biology/docs/structural_biology/HANDOFF.md` |
| frontier | `08_frontier_benchmarking/requirements-frontier.txt` | `08_frontier_benchmarking/docs/frontier_benchmarks/HANDOFF.md`; `experiments/frontier/make_tables.py --verify` |

Lean sources of divisions other than theory import theory modules; they build against the theory tree
*of their own branch* (see §2, last item).

## 7. Downloading

```
git clone --depth 1 --single-branch --branch research/consolidated-archive https://github.com/Tommaso-R-Marena/MetricChain.git
```

or one compressed file of the branch (it contains `consolidated/` and a one-page `README.md`):

* <https://github.com/Tommaso-R-Marena/MetricChain/archive/refs/heads/research/consolidated-archive.zip>
* <https://github.com/Tommaso-R-Marena/MetricChain/archive/refs/heads/research/consolidated-archive.tar.gz>

For a fixed version, replace `refs/heads/research/consolidated-archive` by the commit hash.

## 8. Versions, and what a refresh is

| version | commit of this branch | engineering pinned at | other seven divisions |
|---|---|---|---|
| interim, first | `2035fe86ff74d62391f83aee35cba70cec4a6f9d` | `846e58c` | as in §1 |
| interim, second | `5c2bcec920e8023a9db37df31249013af4da72ea` | `af74a0e66534294bad1dcbc3d5a9d85433cb72a4` | as in §1 |
| final | the head of the branch (the commit that contains this file) | `dcb49f3e0372b0383bf816ef4050716b5d8da5e6` | as in §1 — unchanged since the first version |

A refresh changes nothing by hand under `01_…` – `08_…`: the new commit of a division is written into
`pins.json`, `build_archive.py` is run (it copies the files of the pinned commits, removes what is no
longer in them, and regenerates the indexes and the manifest), then `verify_manifest.py --git` and
`scan_sensitive.py`.  The hand-written index files are edited where the state they describe has changed;
which ones were, for the final version, is listed in `00_MASTER_INDEX.md` §0.5.  Earlier versions are
never rewritten: every version is a commit of this branch, and the branch has never been force-pushed.

For the final version all eight branches were fetched again (2026-11-27 18:47 UTC): only engineering had
a new commit.  Result of the checks on the final version: see the last lines of §4 and §5.
