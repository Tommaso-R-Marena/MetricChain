# Status of the Frontier Benchmarking division

*Updated at every checkpoint.  The newest entry is first.*

## 2026-11-26, about 23:45 UTC — checkpoint 1: intake, CASP17 determination, integrity tooling

**Done**

* Evaluation-integrity tooling (`src/metricchain_fb/`: freeze manifests, RFC 3161 time-stamps,
  commitments) with 43 tests; first freeze **FRONTIER-FRZ-0001** (public state of CASP17,
  attested 2026-11-26T23:03:21Z by four authorities).
* **CASP17 determination** (`docs/frontier_benchmarks/CASP17_ASSESSMENT.md`): nothing in
  MetricChain is mature enough for an evaluation before the release of 2026-11-29; no
  prediction produced; MetricChain is not a participant.  19 of 239 targets already have a
  released PDB entry; all groups' predictions are public; results are not.
* Intake of all seven branches at pinned commits (`RESEARCH_INTAKE.md`, `intake/`).
* Four literature assessments with read levels (`literature/`).
* FRONTIER-MSG-0001 to all divisions.

**In progress**

* Benchmark registry, state-of-the-art register, contamination audit, assessment protocols,
  mathematical feedback; requests to engineering, structural biology and science.
* Scoring tools with synthetic controls; blind test of those tools on public CASP17 models
  (to be frozen before 2026-11-29).

**Waiting on others**

* Structural biology, engineering, science: any contradiction of the CASP17 maturity table
  (deadline 2026-11-28 18:00 UTC; silence is agreement).

**Open obligations of ours**

* After 2026-11-29: read the official CASP17 assessment; compare the frozen scores of our
  tools with the official numbers; update the state-of-the-art register.

**Results claimed:** none.  **Negative results recorded:** the determination above.

## 2026-11-26, about 23:05 UTC — division founded (checkpoint 0: scaffolding only)

* Branch `research/frontier-benchmarks` created at theory checkpoint `b2caab6`
  (rationale: `docs/collaboration/FRONTIER_UPSTREAM_SYNC.md`).
* Owner directives FB-D-1 (founding) and FB-D-2 (scope clarification) recorded in
  `docs/frontier_benchmarks/OWNER_DIRECTIVES.md`.
* Protocol copy for eight divisions: `docs/collaboration/README.md` (assessment classes,
  evidence stages, comparison dimensions and failure attribution are defined in its addendum).
* First read-only synchronisation of all seven other branches done; heads pinned in
  `FRONTIER_UPSTREAM_SYNC.md`.
* In progress: CASP17 feasibility assessment from the official site; evaluation-integrity
  tooling; benchmark registry and state-of-the-art register; first messages to all divisions.
* Nothing has been evaluated yet; no result of any kind is claimed.
