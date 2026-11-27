# Status of the Computational Research Division

*Updated at checkpoint 6 of the engineering branch (2026-11-26/27; the commit time is
authoritative).  Branch `research/ubuntu-engineering`.*

## Pins

| what | commit |
|---|---|
| theory checkpoint this branch is built on (branch point; not merged since) | `d81eb8aba138567a8ca98dc45bc3eece6a5ad517` — audit replicated (ENG-RES-0005) |
| latest theory commit read | `eb88823` — THY-MSG-0018 in full; theory report §11.33 (statements of Theorems 11.118, 11.119, Proposition 11.121) and the paragraph of §11.32 that quotes our X-013; `Z_REPORT.md` §§0, 7 and the file of certified exponents of workstream Z.  What else was and was not read: ENG-MSG-0007 §1.  **Not audited** |
| latest theory commit audited on the engineering machine | `9408e33` — `AUDIT PASSED` (2026-11-26 04:05 UTC, one hour on four threads): 69 Lean files, 37 543 lines, 4015 audited declarations, 504 headline theorems; full harness as expected; 435 mutations, 434 caught, 1 expected pass; 136 baseline runs as expected; 2377 declarations indexed by the document check (ENG-MSG-0004 §2) |
| latest science commit read | `59e88bc` — SCI-REV-0018 with `R18_REPORT.md` §§2, 6; SCI-RES-0030; SCI-RES-0033; the section "Engineering division" of its digest.  Nothing else of the 20 new messages beyond titles (ENG-MSG-0007 §1) |
| other branches read | ensemble `8d42f60`, geometry `288b2de` (GEOMETRY-REQ-0001 with the correction of GEOMETRY-MSG-0003; GEOMETRY-REQ-0006), complexity `1ba144d`: headers and what names engineering.  **Structural biology `720e0ec`: its software read in full and tested (ENG-RES-0018).**  Frontier benchmarking: no branch at 2026-11-26 22:41 UTC |
| the research owner's directives | `docs/engineering/DIRECTIVES.md`, D-1 … D-7 (the last two: a seventh division whose software this division verifies; an eighth that designs evaluations, CASP17 feasibility) |
| text that experiment X-010 implements | the referee's design of three levels, docstring of `experiments/reviews/R8/r8_flat3.py` at theory `9408e33`; Proposition K0 of `K_REPORT.md` |
| text that experiments X-005, X-006, X-006b implement | `docs/workstreams/K_REPORT.md` §§2–3 at `63efc69`, with errata m1 and m10 of referee R8 |

## Verified state of the engineering branch

* `bash scripts/audit_all.sh` (the theory division's audit, unmodified) passes on this branch
  with the engineering additions in place: run in full at checkpoint 2 and with the quick
  harness pass at checkpoint 3 (the state of the branch point `d81eb8a`, which this branch
  contains unchanged; 45 Lean files, 3016 declarations).  Not repeated at checkpoint 4:
  no file outside `docs/collaboration/`, `docs/engineering/`, `src/metricchain_eng/`,
  `experiments/eng/`, `tests/eng/` and `modal_jobs/` was touched.
* `python -m pytest tests/eng/test_certified.py tests/eng/test_chains.py tests/eng/test_geometry_req1.py tests/eng/test_hetero.py tests/eng/test_leafcert.py tests/eng/test_slices.py tests/eng/test_twolevel.py tests/eng/test_weighted_cube.py -q` **in one session**: 466 passed, 4 skipped (2026-11-26 23:45 UTC).  "In one session" matters: until checkpoint 6 one test failed whenever the weighted-cube tests were collected with it, because importing the Parma Polyhedra binding switches the process to upward rounding; the module now restores the mode and `tests/eng/conftest.py` guards it before and after every test.  Two further test files belong to work of subagents that is still in review and are not counted (`test_leafprod.py`, `test_level_rate.py`).
* `python experiments/eng/twolevel/three_levels.py --check`: the referee's 48 three-level numbers at the flat instance reproduced.
* `make_tables_x011.py --verify` for ENG-RES-0015 and ENG-RES-0016, `make_tables_x005c.py --verify` for ENG-RES-0017, `experiments/eng/sb_review/make_tables.py --verify` for ENG-RES-0018: the tables of the messages equal the stored artifacts (the first two use the rows listed in `results/x011_published_rows.json`, so they keep holding while detached jobs append rows).
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
| THY-RES-0013 §4, THY-RES-0015 §6 (R16-THY-1(b)) | designs with servers by certified cost: reproduce and extend the table; run them; two levels at three more sizes | accepted | **completed** up to the sizes still running | ENG-RES-0015 |
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
| GEOMETRY-REQ-0006 (item 2 of -0001) | a certified global maximum on a 4-torus; a certified realisation in four dimensions | **accepted** | next on this line; local |

## Assigned by the research owner (D-6, D-7)

| what | status |
|---|---|
| independent verification of the structural-biology division's software, and review of its benchmark specifications | **first review done** at its first commit `720e0ec` (ENG-RES-0018): checker and producer survive; three findings as software.  Procedure: `docs/engineering/benchmarks/BENCHMARK_MASTER_PLAN.md` §3a.  Checked at every synchronisation |
| coordination with the frontier-benchmarking division: CASP17 assessment feasibility; frozen, independently timestamped predictions | procedure written (`docs/engineering/benchmarks/PREDICTION_FREEZE.md`); what we need from that division is in ENG-MSG-0007 §2; its branch did not exist at 22:41 UTC.  At the reviewed commit no software exists that could produce a structure prediction, so nothing can be frozen yet |

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

Sessions 1–3: jobs M-001 … M-014, $8.73.  Session 4 (2026-11-26): M-015 … M-025, $13.07 by
the billing report at checkpoint 6, with two app runs still open (M-016: six long tasks;
M-020/M-021: eleven).  Credits consumed by the workspace: $55.39; billed cost $0.00.  One
job cost more than the worst case entered for it (M-022: $2.48 against $2.28, restarted
tasks); worst cases now count two attempts for tasks of an hour or more.  The research
owner's authorisation (up to $1,750 of additional expenditure, a ceiling of about
$1,791.41 of cumulative workspace usage, $200 of credits kept in reserve), our own
ask-first line at $1,500, the launch test and every job are in
`docs/engineering/COMPUTE_LEDGER.md`.  Nothing is deployed.

## Synchronisation log

See `docs/collaboration/UPSTREAM_SYNC.md` (both other branches).
