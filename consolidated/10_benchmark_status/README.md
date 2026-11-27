# Benchmark status across the eight divisions

*Written for the archive on 2026-11-27 from the divisions' own registries and results files; the rows
about engineering's jobs M-016 and M-021 (§§2–4) were rewritten at the final refresh of the same day from
that division's addendum and ledger.  Nothing was run, re-run or re-analysed for this file.  Paths are relative to `consolidated/`; in the tables of §§2–6,
`07_…/X.md` and `08_…/X.md` abbreviate the documents directory of that division given in full in §1.*

**The state in four sentences.**  Every computational evaluation so far is on synthetic instances or on
development structures chosen by the authors, except one exploratory pilot on ten public instances.  No
held-out evaluation has been run by anyone: the sealed held-out list (47 structures) is unopened and no
software release is frozen for it.  Nothing has been compared with an experimental observable.  No
MetricChain entry exists for CASP17, by a determination that no division contradicted.

Other files here: [`COMPUTE_AND_MODAL.md`](COMPUTE_AND_MODAL.md) (every Modal job; the final reconciliation),
[`INCOMPLETE_AND_UNREVIEWED.md`](INCOMPLETE_AND_UNREVIEWED.md) (unfinished subagent work, unreviewed
statements, incomplete computations).

## 1. Where each division keeps its benchmark records

| division | plan, protocols, baselines | registry / queue | results | readiness and limitations |
|---|---|---|---|---|
| engineering (coordinator of shared computations) | `02_engineering/docs/engineering/benchmarks/BENCHMARK_MASTER_PLAN.md`, `BASELINE_SPECIFICATIONS.md`, `protocols/BM-1_X-011.md`, `protocols/BM-6_X-014.md`, `PREDICTION_FREEZE.md` | `…/benchmarks/BENCHMARK_REGISTRY.md` (queue rows Q-01 … Q-20; the table "Status at the consolidation halt" is the current one) | `…/benchmarks/BENCHMARK_RESULTS.md`; `02_engineering/docs/engineering/EXPERIMENT_REGISTER.md` (X-001 … X-019) | `…/benchmarks/BENCHMARK_READINESS.md`, `BENCHMARK_LIMITATIONS.md`, `REPRODUCIBILITY.md` |
| frontier (evaluation design and integrity) | `08_frontier_benchmarking/docs/frontier_benchmarks/ASSESSMENT_PROTOCOLS.md` (eleven protocols FB-P-…), `STATE_OF_THE_ART.md`, `CONTAMINATION_AUDIT.md`, `DATA_PROVENANCE.md` | `…/BENCHMARK_REGISTRY.md`, `PREDICTION_FREEZE_REGISTER.md` | `…/RESULTS.md` (§§1–6), `NEGATIVE_RESULTS.md` | `…/BENCHMARK_READINESS.md`, `CASP17_ASSESSMENT.md` |
| structural biology | `07_structural_biology/docs/structural_biology/BENCHMARK_MASTER_PLAN.md` (SB-BM-1 … SB-BM-7), `BASELINE_REGISTER.md` | same | `…/RESULTS.md` (R-1 … R-13), `VERIFICATION_REPORT.md` | `…/PHYSICAL_APPLICABILITY.md`, `ASSUMPTION_REGISTER.md` |
| science | `03_scientific_translation/docs/science/BENCHMARK_DESIGN.md`, `SOFTWARE_EVALUATION_PROTOCOL.md` | — | `…/INDEPENDENT_VALIDATION.md`, `PHYSICAL_APPLICABILITY.md` | `…/PHYSICAL_APPLICABILITY.md` |
| ensemble | `04_ensemble_identifiability/docs/ensemble/BENCHMARK_CONTROLS.md` | — | `04_ensemble_identifiability/experiments/ensemble/benchmarks/controls_v1.json`, `torus_instances_v1.json` (frozen reference instances) | consolidation report §B3, §D |
| geometry | `05_geometric_inference/docs/geometry/BENCHMARKS.md` | — | `05_geometric_inference/experiments/geometry/benchmark_suite/` (23 labelled synthetic instances) | consolidation report §C |
| complexity | — (validation against exhaustive enumeration; `06_biological_complexity/docs/complexity/HANDOFF.md`) | — | `06_biological_complexity/experiments/complexity/strands/`, `reviews/` | consolidation report §D |
| theory | audit harness, mutation tests, separation benchmarks: `01_theory/scripts/audit_all.sh`, `experiments/falsify_conjectures.py`, `mutation_tests.py`, `separation_benchmarks.py` | — | `01_theory/docs/falsification_output.txt`, `mutation_output.txt`, `benchmarks_output.txt` | `01_theory/docs/THEORY_REPORT.md` §8 |

## 2. Completed, with stored results

| benchmark or computation | by | outcome, in the owner's words or numbers | source |
|---|---|---|---|
| Lean audit, falsification harness, mutation tests | theory | "AUDIT PASSED … 192 harness tests; 618 mutations, 617 caught and one expected pass" | theory consolidation report, header |
| Replication of that audit on a second machine | engineering; science | no divergence at four heads (engineering); several commits, "not at its newest" (science) | engineering report §A.1; science report §B4 |
| Certified recursion of nested runs to six levels (Q-01, Q-10; X-011a) | engineering | published to `n = 16 000` at slope 1 (`ENG-RES-0015`).  Collected on 2026-11-27, after the halt, in an **unrefereed** addendum: `n = 32 000, 64 000, 128 000` at slope 1 (5 of 6 cells) and `n = 1000 … 64 000` at slopes ½ and 2 (16 of 16); 20 of the 33 stored cells end with a search that ran into its time limit — §3, §4 | registry Q-01, Q-10; `02_engineering/docs/engineering/benchmarks/X-011_ADDENDUM.md` |
| Nested designs run on searched instances (Q-02, X-011b) | engineering | complete, 288 of 288 cells; hypothesis H14 holds at all three slopes at `n = 16 000` | registry Q-02; `ENG-MSG-0008` §2(b) |
| Two-level worst cases at three more sizes (Q-03); exact checker of "shares at the leaves" (Q-04); weighted cubes (Q-05) | engineering | done; Q-04 and Q-05 re-run by science | registry |
| Site-dependent slopes (Q-11, X-014) | engineering | published (`ENG-RES-0016`); 64 800 literal runs with the theorem's constants, 0 invalid, 0 aborted | registry Q-11; `ENG-MSG-0008` §2(c) |
| Exact elimination and ranks for geometry (Q-12); certified optimum on a 4-torus, instance A (Q-16, X-019) | engineering | done; Q-16 by a subagent, "core unread by the coordinator" | registry Q-12, Q-16 |
| Independent verification of the structural-biology software, capability C1 (Q-18; stages S0–S3) and an independent checker for C2 | engineering | at commits `0544ff4`, `41fa668`: tests, 22 472 adversarial claims with no unsound acceptance, the theory kernel accepts the six stored certificates of the first model; one soundness finding in the float tier at a non-default setting; **nothing after `41fa668` tested** | `ENG-RES-0019`; `09_cross_divisional_dependencies/README.md` §3.1 |
| SB-BM-1 conformance of the `min` checker; SB-BM-2 synthetic instances; SB-BM-3 development part; SB-BM-4 tables against the energy function | structural biology | R-1 … R-13: every development minimum certified with zero gap and equal to toulbar2's optimum; crambin's `ln Z` enclosed to 0.0075 nats | `07_…/RESULTS.md` |
| Pilot of FB-P-01: the certified route against toulbar2 on ten public instances (exploratory) | frontier | 4 certified, 6 abstained in 300 s; 17–326 times slower where both finish; diagnosis: node rate | `08_…/RESULTS.md` §1, §6 |
| Pilot of FB-P-04: nine planted identification controls recomputed with independent code | frontier | all nine reproduced; two reweighting baselines return one perfectly fitting ensemble on non-identified controls | `08_…/RESULTS.md` §2 |
| Conformance of frontier's scoring code against two libraries and planted answers | frontier | passed | `08_…/RESULTS.md` §3 |
| 25 control instances with 38 exact verifications; 10 torus instances | ensemble | self-verifying; frozen at the final commit | ensemble report §A, §G |
| Exact partition function and level counts against exhaustive enumeration | complexity | agreement on 280 systems (own) and about 740 runs with referees' enumerators | complexity report §B3 |
| Measurements on a real force field: class constants, certified reweighting on 74 enumerated instances, coverage of error bars, the rotamer discretisation | science | science report §B3 ("Grid maxima are not bounds") | `03_…/PHYSICAL_APPLICABILITY.md` |

## 3. Negative or failed outcomes (recorded as results)

| what | outcome | source |
|---|---|---|
| Speed and completeness of the certified minimum-energy route | "no speed or completeness claim can be made for the present producer"; toulbar2 6–27× faster on development structures, 17–326× on the pilot, 600–1 700× on synthetic frustrated instances | frontier report §C; structural-biology report §C |
| Structural biology's hypothesis H2b (synthetic instances) | fails | `07_…/RESULTS.md` R-5 |
| The speed hypothesis formed on the development set | "held on its development set and fails on public instances; that set never searches" | frontier report §C |
| Engineering's pre-registered predictions H3 (at `n = 16 000`), H13(a), H5 | failed; published with the runs | engineering report §C |
| Engineering's pre-registered predictions on the rows collected after the halt (**unrefereed**) | **H12 refuted** (at slopes ½ and 2 a fifth level still lowers the certified bound: at `u = ½`, `n = 16 000`, and at `u = 2` at all three sizes; it holds at `u = ½`, `n ≤ 4000`); **H3 and H13(a) refuted again** at `n = 64 000` and `128 000`; **H1 and H13(b) not decided** at `n ≥ 32 000` — the searches with five and six levels ran into their time limits (H13(b): one finished share, `0.5018` against "less than `0.50`", inside the rounding of constants that were not recomputed) | `02_engineering/docs/engineering/benchmarks/X-011_ADDENDUM.md` §5 |
| The same rows, slope ½ | no nested design is certified below the base bracket at `n = 1000`, and nothing beyond two levels at `n = 4000` | same, §4 |
| Worst-case search by differential evolution (Q-15) | "not converged to the requested `10⁻⁴·na`, and said so"; a published conclusion withdrawn | registry Q-15; `ENG-RES-0017` |
| Deep nesting at the sizes computed | a fifth level keeps at most a quarter of its asymptotic gain at `n ≤ 16 000` | engineering report §C |
| Cost of producing leaf certificates (subagent's benchmark, **unreviewed**) | 15 % search, 85 % assembling and checking; dynamic programming 55–89 times faster on banded chains | `02_engineering/experiments/eng/leafcert_bench/REPORT.md` |
| Certified partition functions beyond crambin | "C2 does not scale past crambin under this model" | structural-biology report §C item 6 |
| Blind check of the scoring instruments | "has little power: three easy targets" (N-14) | frontier report §B3 |
| CASP17 | "no assessment class admits a MetricChain entry; none was produced" | `08_…/CASP17_ASSESSMENT.md` |

## 4. The two runs that were open at the interim version of the archive: closed

<!-- GEN:status -->
FINAL (built 2026-11-27 under the research owner's directive for the final collection and handoff): every Modal job of the programme is closed and nothing is running.  The engineering section is pinned at the commit that holds the collected results of jobs M-016 and M-021, the tables made from them and the closed compute ledger; one cell of job M-016 has no result, and most of the larger searches ran into their time limits (see the record of incomplete items).  The other seven divisions pushed nothing after the interim version and are pinned at the same commits as there.  The interim version remains in the history of this branch as commit 5c2bcec.
<!-- /GEN:status -->

| job | what | registry row | state |
|---|---|---|---|
| M-016 | the certified cost bound of nested runs to six levels at `n = 32 000, 64 000, 128 000`, slope 1, two families (hypotheses H1, H3, H13) | Q-01, Q-17 | **closed, 5 of 6 cells: the cell `n = 32 000`, family "wide" has no result** (restarted by the platform; its run was stopped before it could return; not restarted) — [`COMPUTE_AND_MODAL.md`](COMPUTE_AND_MODAL.md) §5 |
| M-021 | the same bound at slopes ½ and 2 (hypothesis H12) | Q-10 | **done, 16 of 16 cells** |

Results: [`X-011_ADDENDUM.md`](../02_engineering/docs/engineering/benchmarks/X-011_ADDENDUM.md).  **Nothing is
running in any division**: the other seven say so in the last section of their consolidation reports
and have pushed nothing since; engineering's ledger records the final state.

## 5. Frozen, outcome pending

| what | state | source |
|---|---|---|
| FRONTIER-FRZ-0003: frontier's scores of 1 163 public CASP17 model files of three targets, frozen and time-stamped before the official numbers | the comparison with the official numbers "needs the owner's authorisation"; the scheduled check-in for it was "paused, not deleted" | frontier report §B3, §G; `08_…/experiments/frontier/freezes/FRONTIER-FRZ-0003_casp17_scoring_check/COMPARISON_PLAN.md` |
| FRONTIER-FRZ-0001: the public state of CASP17 three days before the announced results | frozen | `08_…/PREDICTION_FREEZE_REGISTER.md` |
| FRONTIER-FRZ-0002: commitment to the sealed held-out list of 47 structures | sealed; unopened; credentials with the research owner; the encrypted list is **not in this archive** | same; `11_reproducibility/EXCLUDED_ARTIFACTS.md` |

## 6. Proposed or designed, not run

| what | proposed by | what is missing (theirs) | source |
|---|---|---|---|
| Held-out certified-optimum benchmark (SB-BM-3, held-out part; FB-P-01 under a frozen protocol) with the pseudo-Boolean proof-logging baseline | structural biology E1; engineering E1; frontier E1 | a frozen release, an agreed selection rule (IR-14), an independent attack on the repaired checkers, the proof-logging tool chain | the three reports §E |
| Side-chain placement against deposited conformations (SB-BM-6; FB-P-02) | structural biology; frontier E3 | frozen release; baselines built; a public validation list | frontier report §E3 |
| The table against the continuous model of the same energy (SB-BM-7) | science (SCI-REV-0025 §4); structural biology E3 | interval bounds of the energy over a cell | structural-biology report §E3 |
| Certified populations as an oracle on an accepted energy model (SB-BM-5 beyond crambin) | structural biology E2 | ratio-form bound, independent checker, sparser model | structural-biology report §E2 |
| Certified ensemble intervals against reweighting on realistic or public data (FB-P-04 beyond planted controls) | ensemble E1; frontier E2 | a forward model with a stated error set; an interval tool for a general pool | the two reports §E |
| The error budget on real protein instances | science E1 | flexible-geometry tables, a second energy model | science report §E1 |
| Comparison of the multi-strand reference algorithm with established software | complexity E1 | an adapter to published parameter files | complexity report §E1 |
| Negative controls and block-sum identifiability benchmarks | geometry E1 | a forward model and labelling scheme stated by science | geometry report §E1 |
| Engineering queue rows not started: the off-lattice chain in exact arithmetic (Q-06), the enumeration job (Q-07), the sandwich-certificate checker (Q-08), constants in the profile format (Q-09), directed rounding (Q-19, design started) | science, theory | see the registry | `02_engineering/docs/engineering/benchmarks/BENCHMARK_REGISTRY.md` |
| Fuzz campaign for claim Z5 of the partition-function checker | engineering (subagent) | written, **never run** | `02_engineering/experiments/eng/sb_zcheck/REPORT.md` |
| Long `ln Z` runs and the proof-logging comparison requested by structural biology | structural biology | "reviewed, not started" | `ENG-RES-0019` §4 |
| Evaluations on benchmarks beyond CASP17 named in the owner's directive to frontier | frontier | "no evaluation on the benchmarks beyond CASP17" | frontier report §A |

## 7. Evaluation integrity

Stated by the divisions and recorded here unchanged: no division other than frontier has seen the sealed
list ("The Frontier division's sealed material was never opened" — science; "we hold no key" — structural
biology; "No sealed list was opened or asked for; no held-out structure was looked at" — engineering);
frontier's ten public instances "are development material" now; the hypotheses of engineering's BM-1 are
in a protocol committed before collection.  The archive builder did not read the sealed file.
