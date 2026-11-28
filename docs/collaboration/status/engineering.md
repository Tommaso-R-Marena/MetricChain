# Status of the Computational Research Division

*Updated 2026-11-28 after the first cycle under the owner's directive D-12 (the commit time is
authoritative).  Phase II branch: `research/phase2-certified-inference`.  Phase I branch, unchanged since
its halt: `research/ubuntu-engineering`.*

## Since directive D-12 (2026-11-28, about 05:30 UTC): bounded cycles for the collaboration with the fourth division

The owner established a fourth Phase II division (`research/phase2-certified-mbar`, multistate
free-energy estimation) and asked this division to look for real compositions with its work, to remain
the coordinator of Modal computation for all four divisions (one ceiling of $25 in total), and to
"continue your existing bounded research cycles".  The main work of Phase II stays complete (next
section); what follows is the only thing in progress.

| item | state |
|---|---|
| mailbox for four branches; how to request computation | `docs/collaboration/README.md`, section "Phase II" |
| mathematics | `docs/engineering/phase2/MBAR_INTEGRATION.md`: Theorem M1 (uncertainty of free energies as an envelope), Proposition M2 (shared energy error), Proposition M3 (which sampling laws need free energies); paper proofs, **unrefereed** |
| software | `src/metricchain_eng/certinf/multistate.py`; 14 new tests; 46 tests of the certified-inference library pass |
| experiments | `experiments/eng/phase2_mbar/`: predictions written before the runs; outcomes, including the refuted ones, in `MBAR_INTEGRATION.md` §8 |
| read from the new division | its provenance note, the four text files of its imported package and, at its second commit, its prior-art note, three theorem statements of its Lean file on e-values and its coverage logs — as proposals; its code was not run and its Lean project not rebuilt.  **Used:** its likelihood-ratio region for free energies (its Theorem B1), re-derived, implemented and tested by us; with it our certified bound for an event of probability 10⁻⁶ is within 22 % of the exact value at 2·10⁵ draws |
| messages | sent: ENG-MSG-0011 (to the new division; for the record of the other two), ENG-RES-0021.  Read: HIE-MSG-0002 and HIE-MSG-0003 (adaptive hierarchy; ask nothing of us); of MBAR-MSG-0001 and THY-MSG-0024 the sections addressed to us |
| requests for computation received | one: MBAR-REQ-0001 (a molecular-dynamics campaign of about 120 GPU-hours, $80–$130; optional pilot under $8).  Answered in ENG-RES-0021: **nothing launched**; the campaign needs the research owner and is premature by the owner's order of preference; the pilot is deferred; two cheaper routes proposed |
| remote computation | **none**; Modal ceiling of $25 untouched |
| monitoring | at synchronisation points only (`UPSTREAM_SYNC.md`); no model-based polling.  **None is scheduled**: the account-wide usage counter, which the other divisions' sessions share, stands close to the ceiling of D-11, so the next synchronisation waits for the research owner |

## Phase II (research owner's directive D-11): COMPLETE (2026-11-28) — its work is not resumed; see above for what continues under D-12

Task: verify, improve and validate the proposed theorem "S3" (sampled compression of the set of ensemble
moments compatible with an energy envelope), close the verification gaps left by Phase I, and coordinate
computation for the two other Phase II divisions.  Everything is indexed in
`docs/engineering/phase2/README.md`; start with `FINAL_REPORT.md` there.

| item | state |
|---|---|
| mathematics (`CERTIFIED_INFERENCE.md`) | second version, corrected for every finding of an independent review; two claims of the first version withdrawn; not refereed again |
| software (`src/metricchain_eng/certinf/`) | 32 tests pass |
| validation (`RESULTS.md`) | campaign under a pre-registered protocol complete: seven hypotheses hold, six are refuted; two supplementary experiments |
| Phase I verification gaps (`VERIFICATION_GAPS.md`) | closed, with one correction of our own wording about the constants `c_k` |
| messages sent | ENG-MSG-0009 (opening), ENG-MSG-0010 (corrections and replies), ENG-RES-0020 (replication for HIE-REQ-0001) |
| messages read | THY-MSG-0023 (theory, Phase II), HIE-MSG-0001 and HIE-REQ-0001 (adaptive hierarchy) |
| remote computation | **none**: no Modal job in Phase II; ceiling of $25 untouched |
| running | **nothing**: no process, no agent, no scheduled task |

Open on our side, for whoever continues: a second review of the corrected note; samplers for the
extremal ensemble (Theorem 5.4) beyond enumerable models; bounds for references that are not products
that are tighter than Proposition 9.7.  (Written at completion: "The division does not resume when a
message arrives."  Since D-12 it reads the mailbox of the three other Phase II branches at its
synchronisation points and answers requests for computation; it still starts no new line of research
on a message alone.)

## Phase I: HALTED (research owner's directive D-8, 2026-11-27) — the record below is that of Phase I

The division is in the controlled halt ordered by the research owner: no research loop, no new
experiment, no new subagent, no new Modal job, and **no resumption when a message arrives** — only
on the research owner's explicit authorisation.  The assessment of the division's work, the state of
every open item and the record of what is still running are in
`docs/collaboration/consolidation/engineering.md`; the final message is ENG-MSG-0008.  Still running
*at the halt*: two detached Modal runs (jobs M-016, M-021; sixteen tasks) — **closed on 2026-11-27,
see "Administrative task D-10" below; nothing of this division is running**.  The tables below are
the state at the halt; "in progress" means *stopped in that state*.

**Administrative task D-9 (2026-11-27, about 05:00–06:00 UTC).**  On the research owner's order this
division assembled the unified archive of all eight divisions on the new branch
`research/consolidated-archive` (directory `consolidated/`; start at `00_MASTER_INDEX.md`): copies of
every division's own files at pinned commits with a manifest of provenance and checksums.  It is
administrative: nothing was re-derived, no other branch was modified, the sealed held-out list was
neither copied nor read.  What this division still owes under D-9, and nothing else: collect the two
Modal runs once they have ended, close them in the ledger, regenerate the tables, commit, and refresh
the archive once.  *(Done under D-10, next paragraph.)*

**Administrative task D-10 (2026-11-27, from 18:19 UTC): final collection and handoff.**  On
the research owner's order the two Modal runs were collected and closed: job M-021 complete (16 of
16 cells), job M-016 with 17 of 18 — the cell `u = 1`, `n = 32 000`, family "wide" has no row: its
task had been restarted by the platform and could not return before the existing cutoff, so its
run was stopped at 18:24 UTC and nothing was restarted.  The 33 stored rows were checked
(structure; the first two nested levels recomputed locally, 33 of 33 equal), the tables generated,
and the pre-registered hypotheses read off: H12 refuted; H13(a) and H3 refuted again at larger
sizes; H13(b) and H1 not decided there.  All of it, with what is missing and what the rows cannot
show: `docs/engineering/benchmarks/X-011_ADDENDUM.md`.  Money: credits consumed by the workspace
$62.99, billed cost $0.00, $21.58 of the $1,750 authorised used, nothing committed
(`docs/engineering/COMPUTE_LEDGER.md`, "Final reconciliation").  The unified archive was refreshed
once more with these files and with whatever the other divisions had pushed since.  **Nothing of
this division is running, scheduled or owed.  The halt of D-8 stands.**

## Pins

| what | commit |
|---|---|
| theory checkpoint this branch is built on (branch point; not merged since) | `d81eb8aba138567a8ca98dc45bc3eece6a5ad517` — audit replicated (ENG-RES-0005) |
| latest theory commit read | `eb88823` — THY-MSG-0018 in full; theory report §11.33 (statements of Theorems 11.118, 11.119, Proposition 11.121) and the paragraph of §11.32 that quotes our X-013; `Z_REPORT.md` §§0, 7 and the file of certified exponents of workstream Z.  What else was and was not read: ENG-MSG-0007 §1.  **Not audited** |
| latest theory commit audited on the engineering machine | `9408e33` — `AUDIT PASSED` (2026-11-26 04:05 UTC, one hour on four threads): 69 Lean files, 37 543 lines, 4015 audited declarations, 504 headline theorems; full harness as expected; 435 mutations, 434 caught, 1 expected pass; 136 baseline runs as expected; 2377 declarations indexed by the document check (ENG-MSG-0004 §2) |
| latest science commit read | `59e88bc` — SCI-REV-0018 with `R18_REPORT.md` §§2, 6; SCI-RES-0030; SCI-RES-0033; the section "Engineering division" of its digest.  Nothing else of the 20 new messages beyond titles (ENG-MSG-0007 §1) |
| other branches read | ensemble `8d42f60`, geometry `288b2de` (GEOMETRY-REQ-0001 with the correction of GEOMETRY-MSG-0003; GEOMETRY-REQ-0006), complexity `1ba144d`: headers and what names engineering.  **Structural biology `720e0ec`: its software read in full and tested (ENG-RES-0018).**  Frontier benchmarking: no branch at 2026-11-26 22:41 UTC |
| the research owner's directives | `docs/engineering/DIRECTIVES.md`, D-1 … D-10 (D-6, D-7: a seventh division whose software this division verifies; an eighth that designs evaluations, CASP17 feasibility; **D-8: controlled consolidation and halt — the operative one**) |
| text that experiment X-010 implements | the referee's design of three levels, docstring of `experiments/reviews/R8/r8_flat3.py` at theory `9408e33`; Proposition K0 of `K_REPORT.md` |
| text that experiments X-005, X-006, X-006b implement | `docs/workstreams/K_REPORT.md` §§2–3 at `63efc69`, with errata m1 and m10 of referee R8 |

## Verified state of the engineering branch

* `bash scripts/audit_all.sh` (the theory division's audit, unmodified) passes on this branch
  with the engineering additions in place: run in full at checkpoint 2 and with the quick
  harness pass at checkpoint 3 (the state of the branch point `d81eb8a`, which this branch
  contains unchanged; 45 Lean files, 3016 declarations).  Not repeated at checkpoint 4:
  no file outside `docs/collaboration/`, `docs/engineering/`, `src/metricchain_eng/`,
  `experiments/eng/`, `tests/eng/` and `modal_jobs/` was touched.
* `python -m pytest tests/eng -q` **in one session** (2026-11-27 01:26 UTC, the whole directory, twelve test files): 570 passed, 4 skipped, 3 expected failures, 1 failure that is an artefact of the run.  The three expected failures stand for three findings in the structural-biology division's software (`tests/eng/test_sb_zcheck.py`; they need its commit `0544ff4` checked out beside the repository and are skipped without it).  The one failure, `test_c_parser_under_sanitizers` in `tests/eng/test_leafcert.py`, occurs only under an address-space limit (`ulimit -v`), which the sanitizer cannot work under; run alone without the limit it passes.  So: run the suite without `ulimit -v`, and expect 571 passed.  "In one session" matters: until checkpoint 6 one test failed whenever the weighted-cube tests were collected with it, because importing the Parma Polyhedra binding switches the process to upward rounding; the module now restores the mode and `tests/eng/conftest.py` guards it before and after every test.  Three of the twelve files test work of subagents (`test_leafprod.py`, `test_geometry_req6.py`, `test_sb_zcheck.py`): the tests pass; the code they test was not read by the coordinator.
* `python experiments/eng/twolevel/three_levels.py --check`: the referee's 48 three-level numbers at the flat instance reproduced.
* `make_tables_x011.py --verify` for ENG-RES-0015, ENG-RES-0016 and ENG-MSG-0008, `make_tables_x005c.py --verify` for ENG-RES-0017, `experiments/eng/sb_review/make_tables.py --verify` for ENG-RES-0018 and ENG-RES-0019: the tables of the messages equal the stored artifacts (the first two use the rows listed in `results/x011_published_rows.json`, so they keep holding while detached jobs append rows).
* `python experiments/eng/chain_cover/run_lattice.py --check`: all published values of
  `P_REPORT.md` §3.3 for the lattice chain reproduced.
* `python experiments/eng/twolevel/controls.py --theory <checkout of 63efc69>`: 324 + 18 published
  rows of workstream K reproduced (two of them only with plain floating-point comparisons:
  ENG-MSG-0003 §5).
* `make_tables.py --verify` (`experiments/eng/chain_cover/` for ENG-RES-0002, -0007, -0009;
  `experiments/eng/twolevel/` for ENG-RES-0008, -0013 and -0014; `experiments/eng/slices/` for
  ENG-RES-0012): the tables of the messages equal the stored artifacts.

## Requests received from the Theoretical Research Division

| id | subject | decision | status | response |
|---|---|---|---|---|
| THY-REQ-0001 | adversarial evaluation of the two-level algorithms' validity and cost (target: Algorithm 2L⁺) | accepted | **in progress** — two levels done (ENG-RES-0008, corrected at `n ≤ 500` by ENG-RES-0017; literal runs ENG-RES-0013); three levels of one flat-tuned design (ENG-RES-0014 §3); **nested runs designed by certified cost: the recursion to six levels at `n ≤ 16 000`, runs on searched instances, three slopes, literal three-level runs (ENG-RES-0015)**; larger sizes and `u = 2` at `n = 16 000` running (jobs M-016, M-020, M-021) | ENG-RES-0008, -0013, -0014, **-0015**, **-0017** |
| THY-REQ-0002 | exact chain covering beyond 12 torsions | accepted | **in progress, off-lattice part on hold** — lattice chain complete to 24 torsions; off-lattice: covers to 12 torsions, class tables to 14.  On hold until the off-lattice chain is computed in exact arithmetic (SCI-REV-0008, M2).  Three sentences corrected (ENG-MSG-0004 §4) | ENG-RES-0002, ENG-RES-0007, ENG-RES-0009 §2 |
| THY-REQ-0003 | useful constants in the profile format? | accepted in a revised design | not started | ENG-RES-0003 |
| THY-REQ-0004 | schema, checker, producer for the linear kernel | accepted, with differential testing against the Lean definitions | not started | ENG-RES-0004 |
| THY-REQ-0005 | independent replication of the audit | accepted | **completed** at `d81eb8a`, repeated at `4cef47e` and `63efc69` — no divergence; at `9408e33`: `AUDIT PASSED`, no divergence (finished after ENG-MSG-0004 was written; ENG-MSG-0005) | ENG-RES-0005, ENG-MSG-0002 §2, ENG-MSG-0003 §2, ENG-MSG-0004 §2 |
| THY-REQ-0006 | exact hitting numbers over all sensitive sets | deferred | uniform cube done in closed form; general computation deferred | ENG-RES-0006 |
| THY-REQ-0007 | exact tail function of the flat-histogram reference; adversarial test of Theorem 11.63 | accepted | not started | ENG-RES-0010 |
| THY-REQ-0008 | limit shape of profile sets: vertices, walks against bridges, plateau, off-lattice distance entropy | accepted | **in progress** — item 5 and the single-flip part of item 6 done; items 1–4 and the bridge tables not started (to be combined with the science division's enumeration requests) | ENG-RES-0009 |
| THY-REQ-0009 | two-phase known parts (single-letter supremum); rounds of adaptivity | accepted | not started; design fixed; question 4(c) moved into THY-REQ-0001 | **ENG-RES-0011** |
| THY-REQ-0010 | type classes of the cube: smallest sensitive sets; finite-size approach; refinement across classes | accepted | **in progress** — question 2 done (exact, to `n = 10 000`), the best-centre part of question 1 done; arbitrary sets, shells and question 3 not started | **ENG-RES-0012** |
| THY-RES-0004 §7 (proposals) | three levels at the worst instance; exhaustive test over tail functions; SCI-REV-0004 §6 | first: **done in its smallest form** (ENG-RES-0014 §3); second: deferred with reasons; third: accepted, not started | — | ENG-MSG-0004 §3, ENG-RES-0014 |
| THY-MSG-0015 | (correction: sequential numpy binomials are not tail-safe) | — | received; answered by X-006b | ENG-MSG-0005 |
| THY-RES-0013 §4, THY-RES-0015 §6 (R16-THY-1(b)) | designs with servers by certified cost: reproduce and extend the table; run them; two levels at three more sizes | accepted | **completed** up to the sizes still running at the halt; those were collected on 2026-11-27, one cell short | ENG-RES-0015; `docs/engineering/benchmarks/X-011_ADDENDUM.md` |
| THY-MSG-0017 §6, THY-MSG-0018 §6 (candidates E-C1 … E-C5; a small interval computation) | "S proved under H; believed or doubted under H′" | E-C1: a numerical check in review (subagent); E-C3: **Proposition 11.121 reproduced by a third implementation** (X-015); E-C4/E-C5: the finite-size counterpart is ENG-RES-0015 §2, a comparison at `n = 10⁵ … 10⁶` offered; E-C2: nothing computed; the interval computation: the theory division has since certified the upper side itself, the lower side offered | in progress | ENG-MSG-0007 §4 |

## Requests received from the Scientific Discovery Division

First read at checkpoint 4.  Decisions with reasons: ENG-RES-0013 §§0, 6.

| id | subject | decision | status |
|---|---|---|---|
| SCI-REV-0007 R6-E3 | check the sampler of job M-011; re-run if exposed | accepted and extended | **completed** — all 585 cases re-run with an exact sampler (ENG-RES-0013 §1) |
| SCI-REV-0007 R6-E2 | an invalid inner behaviour in the harness | accepted | **completed** (ENG-RES-0013 §2) |
| SCI-REV-0007 R6-E1 | recompute the separation table; search the design | accepted | table and finer grid **completed**; design search not done (ENG-RES-0013 §3) |
| SCI-REV-0008 R7-ENG-1 | regenerate or withdraw the two-solver validation | withdrawn | **completed** (ENG-MSG-0004 §4) |
| SCI-REV-0008 R7-ENG-2 | both lower ends of open brackets; store off-lattice covers | accepted | wording corrected; printing and storing not started |
| SCI-REV-0008 R7-ENG-3 | the off-lattice chain in exact arithmetic over `ℚ[cos θ]` | accepted as a precondition | not started |
| SCI-REV-0008 R7-ENG-4 | tolerance, budgets, what the count counts; the `1/√n` sentence; convergence control at the two largest sizes; level sets that are not balls | accepted | statements, sentence and **convergence control completed** (ENG-RES-0014 §5: no change); non-ball level sets not started |
| SCI-REV-0008 §4 (1) | instances whose fibres sit at different places of their trivial brackets | taken up | **completed as a bound** (ENG-RES-0014 §4); point-dependent inner behaviours open |
| SCI-REV-0008 R7-ENG-5 | certified branch and bound for nine optima | accepted, in the tree format of SCI-RES-0012 §3 | not started |
| SCI-REV-0004 §6; SCI-REV-0010 R10-E1 | three proposals at the cone with a field; vertices of two weighted cubes | accepted | R10-E1 **completed** (X-013; `experiments/eng/weighted_cube/REPORT.md`; re-run and closed by SCI-RES-0033); the three proposals not started |
| SCI-REV-0006 §7 E-1 | native kernel against pseudo-Boolean proof logging | accepted (= engineering agenda E-1, E-2) | not started |
| SCI-MSG-0011 S-E1; SCI-MSG-0008 R3-E1, R3-E2; SCI-REV-0006 E-2; SCI-REV-0002 §8; SCI-REV-0009 R9-E1, R9-E2 | class tables of bridges, pair-distance histograms, homometric counts; packings and lattice points of the profile hull | accepted as one enumeration job and what follows from it | not started |
| SCI-MSG-0020 P3-E1, SCI-MSG-0025 P6-E1; SCI-MSG-0026 A16-E1 | a stand-alone checker of the sandwich certificate (specification: SCI-MSG-0025 §8) | **not ready as specified** (no certificate file exists; step A is not a specification): a two-stage proposal sent (ENG-MSG-0007 §3 (d)); the science division itself asks to build nothing before its format note | waiting for the file format |
| SCI-RES-0014 §7, P7-E2 | a compiled exact checker of "shares at the leaves" certificates, written from the text | accepted | **completed** (X-012; `experiments/eng/leafcert/REPORT.md`; re-run by the science division, which confirmed and repaired the defect we found in its reference checker: SCI-RES-0030) |
| SCI-RES-0014 §7, P7-E1 | a producer of such certificates; what producing and checking costs against exact solvers | accepted | a producer and a benchmark by a subagent, **in review** |
| SCI-REV-0018, R18-ENG-1 … -5 | the review of ENG-RES-0014 §§1, 4: a conclusion false as worded; the worst product instance at the small sizes; texts; code and tests | accepted in full | **completed** (ENG-RES-0017; X-005c): the conclusion withdrawn; the search repeated in three rounds and reported as *not converged* to the requested `10⁻⁴·na` |
| SCI-MSG-0028 §5, A19-E2 (with SCI-RES-0030 §3; assumption A9) | a proved evaluation tolerance of the energy / the step from a real-valued energy to rounded integer tables | taken up as a prerequisite of all application claims | **design started** (directed rounding entry by entry instead of an a-priori tolerance); the energy terms and parameter files are asked for in ENG-MSG-0007 §3 (d) |
| SCI-MSG-0024 P5-E1, P5-E2; SCI-MSG-0025 P6-E2 | exact pair-by-pair constants on a helix; the certificate at order 7 (on hold on their side); a sparse ball | not read | — |
| SCI-REV-0001 R1-E1; SCI-REV-0005 R5-E1; SCI-REV-0003 R4-E1, R4-E2; SCI-MSG-0016 E-R8-1; SCI-REV-0006 E-3 | (various) | deferred; not assessed in detail | — |
| SCI-RES-0002 P-E1…P-E3; SCI-MSG-0015 P2-E1, P2-E2; SCI-MSG-0020 P3-E2; SCI-MSG-0005 K-E1…K-E3; SCI-MSG-0007 X-E1, X-E2 | constants, certificates and evaluators on real peptides | **not decided** — within the authorised scope; the science division states (SCI-RES-0012 §4) that the instances are synthetic homopeptides built by its own code with the parameters of a public force-field package, with no input from outside its tree; not read | — |

## Requests received from the Geometric Inference Division

| id | subject | decision | status |
|---|---|---|---|
| GEOMETRY-REQ-0001 items 1, 3 | the exact elimination for two states and ten atoms; replication of the exact ranks for `K = 2, 3, 4` | accepted | **completed** (`experiments/eng/geometry_req1/REPORT.md`; ENG-MSG-0007 §5): two reduced affine solutions and one point at infinity of multiplicity 5, found independently of the geometry division's own computation; every rank confirmed |
| GEOMETRY-REQ-0006 (item 2 of -0001) | a certified global maximum on a 4-torus; a certified realisation in four dimensions | **accepted** | **completed for instance A** by a subagent (X-019; `experiments/eng/geometry_req6/REPORT.md`; ENG-MSG-0008 §4): both questions certified in ball arithmetic with the couplings rounded to six decimals; seven controls; the coordinator re-ran tests and drivers and did not read the trusted core.  Instance B not examined |

## Requests received from the Structural & Computational Biology Division

| id | subject | decision | status |
|---|---|---|---|
| STRUCTBIO-REQ-0001 items 1–3 | intake, reproduction, independent tests of capability C1 (claims K1–K8) | accepted | **completed** at `0544ff4` (ENG-RES-0019 §§1–3) |
| STRUCTBIO-REQ-0001 item 4 | the held-out benchmark SB-BM-3 | accepted in principle | **not run**: the model was not frozen (v1 replaced by v2 the same day) and the list must come from the frontier division; then stopped by D-8 |
| STRUCTBIO-REQ-0001 item 5 | proof logging (VeriPB/CakePB, exact SCIP/VIPR) on the same instances | accepted | **not started**; two points for its specification in ENG-RES-0019 §4 |
| STRUCTBIO-REQ-0004 items 1, 2 | an independent checker of partition-function certificates; adversarial tests of Z1–Z5 | accepted | **done in part** by a subagent (X-018): Z1/Z2 at defaults and Z4 survive, a defect at `exp_bits` 990–991, Z3 false as worded, the Z5 campaign written and not run |
| STRUCTBIO-REQ-0004 items 3, 4 | crambin at fine thresholds with populations, 5PTI, 1BPI; baselines | reviewed | **not run** (ENG-RES-0019 §4) |

## Assigned by the research owner (D-6, D-7)

| what | status |
|---|---|
| independent verification of the structural-biology division's software, and review of its benchmark specifications | **stages S0–S3 done for capability C1 at `0544ff4`** (ENG-RES-0019, which corrects ENG-RES-0018): claims K1–K4, K6–K8 survive; the six stored certificates are accepted by our independent checker and by the theory division's kernel executed on them (X-017); **capability C2: an independent checker by a subagent (X-018) — one soundness defect at a non-default precision, claim Z3 false as worded, Z5 untested**.  Held-out benchmark, proof-logging comparison and long `ln Z` runs: reviewed, **not run** (ENG-RES-0019 §4).  New code of `41fa668` not reviewed |
| coordination with the frontier-benchmarking division: CASP17 assessment feasibility; frozen, independently timestamped predictions | **agreed with its determination that nothing is mature enough for a CASP17 evaluation** (ENG-MSG-0008 §5); nothing was run and nothing exists to freeze; no sealed list was opened or asked for; our manual freeze procedure (`docs/engineering/benchmarks/PREDICTION_FREEZE.md`) defers to its tooling |

## Requests and questions sent to the other divisions

| id | to | subject | status |
|---|---|---|---|
| ENG-REQ-0001 | theory | a limit shape for profile sets | **completed** by THY-RES-0001, -0002 |
| ENG-MSG-0002 §4, ENG-RES-0003, ENG-RES-0004 | theory | three questions (version of §11.18, sup-norm remainder, evaluation order) | **answered** in THY-MSG-0005 §3 |
| ENG-MSG-0003; ENG-RES-0008 follow-up 1–3 | theory | the flat-instance table; the worst instance at finite `n`; can `M̄` be lowered; check the reduction | **answered** in THY-RES-0004 |
| ENG-RES-0012 | theory | does the closed form give the limiting centre types `0.455` (`κ = 0.4`) and `0.405` (`κ = 0.3`)? | proposed |
| ENG-RES-0013 | science | is the design search of its §3 wanted at fixed accuracy?  In which format does `own_certified_bb.py` store its tree? | **answered** in SCI-RES-0012 §§2–3 |
| ENG-RES-0014 | theory | next for three levels: the fibre landscape searched, or other slopes? | proposed |
| ENG-RES-0015 §9 | theory, science | which middle design the flat-instance figures of §11.19 rest on; why the bounded design uses less of its width on cones; a referee for Proposition P (dovetailing over designs); fibres hard for the bounded design | proposed |
| ENG-RES-0016 §8 | theory | is §2 Theorems 11.118 and 11.119(a) for claims (ii)–(vi), with termination by our Step 9?  A sharp finite-`n` tail function for a block with two slopes, if one is conjectured | proposed |
| ENG-MSG-0007 §3 (d) | science | the two-stage proposal for the sandwich checker; which energy terms and parameter files the specification of the evaluator will name | proposed |
| ENG-MSG-0007 §2 | frontier benchmarking | targets, categories (blind / pre-leaderboard / retrospective) with evidence, metrics, baselines, the software commit | proposed (the branch does not exist yet) |
| ENG-RES-0018 §3 | structural biology | a flat encoding of eliminations; a strict loader; the verdict bound to the model's checksum | proposed |

## Engineering agenda (independent of requests; ENG-MSG-0001)

| item | subject | status |
|---|---|---|
| E-1 | what is actually trusted: the Lean kernel definitions run on generated certificates, against the Python reference checker — now also in the form the science division proposed (native kernel against pseudo-Boolean proof logging) | planned |
| E-2 | what a native `min` certificate costs at realistic sizes | planned |
| E-3 | which class do residuals live in (with THY-REQ-0003) | planned |
| E-4 | limit shape of profile sets | answered by the theory division (THY-RES-0002); computations that would narrow it: THY-REQ-0008 |

## Compute

25 jobs (M-001 … M-025), $24.10 for this division over all sessions by the billing report; credits
consumed by the workspace $56.99 and billed cost $0.00 at 01:16 UTC on 2026-11-27; $15.58 of the
$1,750 authorised by the research owner has been used.  **Left running under D-8: M-016 (six tasks)
and M-021 (ten tasks)**, bounded by their timeouts (latest end 09:35 UTC on 2026-11-27 without
platform restarts; worst case still to be spent $16.7).  M-020 is complete.  Limits, launch test,
every job, the reconciliation and the commands to collect or stop the running jobs are in
`docs/engineering/COMPUTE_LEDGER.md`.  Nothing is deployed and nothing is scheduled.

*Final figures (2026-11-27 18:37 UTC, directive D-10):* both jobs closed; **$30.28** for this division
over all sessions by the billing report; credits consumed by the workspace **$62.99**, billed cost
**$0.00**; **$21.58 of the $1,750 authorised** used; no job running or queued; one job (M-016) cost
about $0.4 more than its stated worst case because the platform restarted tasks.

## Synchronisation log

See `docs/collaboration/UPSTREAM_SYNC.md` (both other branches).
