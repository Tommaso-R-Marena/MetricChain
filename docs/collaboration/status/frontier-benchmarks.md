# Status of the Frontier Benchmarking division

*Updated at every checkpoint.  The newest entry is first.*

## 2026-11-27, about 00:50 UTC — checkpoint 3: replies read, protocols amended

* Third read-only synchronisation (00:26 UTC).  Replies from science, structural biology,
  complexity, geometry and engineering read; **no division contradicts the CASP17
  determination; two explicitly agree**.
* Protocols amended to version 1.1 from their criticism (`ASSESSMENT_PROTOCOLS.md` §6);
  answers recorded against our questions (`MATHEMATICAL_FEEDBACK.md`, last section).
* FRONTIER-MSG-0003 sent.  Still open: FRONTIER-REQ-0001 (engineering), items 1, 3, 5 of
  FRONTIER-REQ-0002 (science), and the theory, ensemble and geometry questions listed as open.
* One check-in is scheduled for 2026-11-30 05:00 UTC (official CASP17 results; replies).
  Between sessions this division does no work.

## 2026-11-27, about 00:40 UTC — checkpoint 2: protocols, registers, two pilots, held-out list, three freezes

**Done since checkpoint 1**

* `ASSESSMENT_PROTOCOLS.md` (FB-P-01 … FB-P-11), `BENCHMARK_REGISTRY.md` (53 rows),
  `STATE_OF_THE_ART.md`, `CONTAMINATION_AUDIT.md`, `MATHEMATICAL_FEEDBACK.md`,
  `RESULTS.md`, `NEGATIVE_RESULTS.md`, `SCIENTIFIC_SYNTHESIS.md`, `RESEARCH_LOG.md`,
  `HANDOFF.md`.
* Second read-only synchronisation (23:36 UTC): all branches had moved; linked corrections
  issued (FRONTIER-MSG-0002 §1).
* **Freeze FRONTIER-FRZ-0002**: sealed held-out list of 47 structures (key with the research
  owner).  **Freeze FRONTIER-FRZ-0003**: our scores of 1,163 public CASP17 model files,
  frozen before the official numbers (a check of our scoring code).
* Scoring tools with planted-answer controls and cross-checks; 64 tests.
* **Pilot 1** (exploratory): the software division's certified minimum against toulbar2 on
  ten public fixed-sequence instances — agreement wherever both finish; the certified route
  much slower, with abstentions; certificates contain little or no search.
* **Pilot 2** (exploratory): nine planted identification controls of the ensemble division
  recomputed independently — all replicate; two baselines return single, sometimes wrong,
  ensembles on the non-identified ones.
* FRONTIER-MSG-0002 (all), FRONTIER-REQ-0001 (engineering), FRONTIER-REQ-0002 (science).

**Waiting on others**

| who | what | reference |
|---|---|---|
| structural biology | a frozen release for held-out evaluation; acceptance of the opening sequence | FRONTIER-MSG-0002 §2 |
| engineering | accept / revise / decline parts A, B, C; whether it already holds a held-out list; whether it wants its manifests time-stamped | FRONTIER-REQ-0001; FRONTIER-MSG-0002 §§2–3 |
| science | adversarial review of interpretations | FRONTIER-REQ-0002 |
| theory, ensemble, geometry, complexity | the questions of `MATHEMATICAL_FEEDBACK.md` | FRONTIER-MSG-0002 §6 |
| research owner | holds the passphrase and commitment salt of the sealed list; releases them to engineering after the software division's freeze | FRZ-0002 `SELECTION_RULE.md` |
| CASP organisers | official results, announced for 2026-11-29 | FRZ-0003 `COMPARISON_PLAN.md` |

**Open obligations of ours:** `HANDOFF.md` §5.

**Results claimed:** none as validation.  Two exploratory pilots and the conformance of our
own instruments (`RESULTS.md`).  **Negative results recorded:** sixteen
(`NEGATIVE_RESULTS.md`), five of them about our own work.

**Answer to the founding question at this checkpoint** (`SCIENTIFIC_SYNTHESIS.md`): not
established in either direction on any dimension involving experiment; established as a
design property on guarantees; currently negative on speed; most distinctive on recognising
insufficient evidence.

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
