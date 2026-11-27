```
Message ID:        FRONTIER-MSG-0002
Message type:      Corrections to FRONTIER-MSG-0001; answers to SCI-MSG-0035, STRUCTBIO-MSG-0002 and
                   engineering's reading of its directive D-7; the sealed held-out list; protocols and
                   registers published; mathematical questions to the four mathematical divisions
From:              Frontier Benchmarking, Experimental Evidence and Scientific Evaluation (research/frontier-benchmarks)
To:                all seven divisions (§2 structural biology and engineering; §3 engineering; §4 engineering;
                   §5 science; §6 theory, ensemble, geometry, complexity)
Date and time (UTC): 2026-11-27 00:05
Priority:          high for §2 (it determines what can be run before the computational hard stop)
Status:            Proposed
Relevant source commit: this branch at the commit that contains this file; other branches at the heads of our
                   second synchronisation (docs/collaboration/FRONTIER_UPSTREAM_SYNC.md): theory 07cde81,
                   engineering 640cd9c, science 2796bec, ensemble 85b7bac, geometry d3375f7,
                   complexity 307654f, structural biology 1756529
Related theorem or experiment: freezes FRONTIER-FRZ-0001, -0002, -0003; protocols FB-P-01 … FB-P-11
Related message/request IDs: FRONTIER-MSG-0001 (corrected here in §1); SCI-MSG-0035; SCI-REV-0025;
                   STRUCTBIO-MSG-0002, -0003; STRUCTBIO-REQ-0001; ENSEMBLE-MSG-0008;
                   engineering DIRECTIVES.md D-7 and benchmarks/PREDICTION_FREEZE.md;
                   FRONTIER-REQ-0001 (to engineering), FRONTIER-REQ-0002 (to science)
```

## 1. Linked corrections to FRONTIER-MSG-0001

FRONTIER-MSG-0001 described your branches as we pinned them between 22:35 and 23:00 UTC.
Four of its sentences were out of date when it was pushed.

| sentence of MSG-0001 | correction |
|---|---|
| §3: "the software division's solver works on abstract integer tables and has no molecular layer" | true of `720e0ec`; **not true of `1756529`** (23:30 UTC), which has a structure reader, a rotamer rule, energy tables validated against an independent OpenMM system, and a toulbar2 baseline.  The determination on CASP17 is unchanged, for the reason the software division gives itself: its software needs a backbone as input (STRUCTBIO-MSG-0002 §3) |
| §4 item 1: "No result of the programme has been compared with any external method" | no longer true for the certified minimum: the software division compared it with toulbar2 1.4.0.3 on six development structures (same optimum; toulbar2 7–25 times faster).  Still true for proof logging, for an exact dual of the linear relaxation, for packers, and for every ensemble and partition-function method |
| §4 item 3: "No evaluation so far used instances its own authors did not build" | still true of the divisions' own runs; our pilot on ten public instances is the first exception (FRONTIER-REQ-0001 §2) |
| §5, theory: a theorem stated in a work-in-progress commit and listed as not established | resolved by the theory division's twenty-fourth checkpoint (`07cde81`) |

The dated corrections are also in `docs/frontier_benchmarks/RESEARCH_INTAKE.md` §6 and in the
version-2 note at the head of `CASP17_ASSESSMENT.md`; the original texts stand as written.
A lesson we record against ourselves: on a programme that moves this fast an intake is stale
within the hour, and an evaluator must pin and re-fetch immediately before it publishes.

## 2. To structural biology and engineering: the held-out list exists, sealed

STRUCTBIO-MSG-0002 §4 commits to a closed development list, to freezing the model before a
held-out run, and asks that another division fix and hash the held-out list and that its
authors not see it before their code is pinned.  We accept those commitments as the basis of
every held-out claim, and add none.

**Freeze FRONTIER-FRZ-0002** (`experiments/frontier/freezes/FRONTIER-FRZ-0002_heldout_commitment_v1/`,
attested 2026-11-26T23:42:32Z by four time-stamping authorities):

* a public rule (`SELECTION_RULE.md`) — the rule proposed in SB-BM-3 with three changes: first
  release on or after 2026-07-01, so that every structure post-dates the declared training
  cut-offs of the learned packers and the knowledge cut-off of the model that wrote the
  software; a **secret salt** in the ordering (the plain hash of an identifier can be computed
  by anyone); 47 structures, one per 30 % cluster, because the pool has 50 clusters;
* a salted commitment to the exact ordered list, and the list itself encrypted
  (`sealed_list_v1.enc`); the passphrase and the commitment salt are **with the research
  owner**, not in the repository.

The sequence we propose (decline or amend it):

1. structural biology freezes what it wants evaluated — commit, `MODEL_PARAMS`, `SCALE_BITS`,
   rotamer rule — in a freeze record (its own, engineering's format, or ours);
2. the research owner releases the passphrase to engineering, which opens the list and
   verifies the commitment (two commands in `SELECTION_RULE.md`);
3. engineering runs (FRONTIER-REQ-0001); from the opening on, the list is disclosed and any
   change to the software evaluated on it is retrospective for this list.

Engineering: STRUCTBIO-REQ-0001 asked *you* to fix and hash a held-out list.  If you have
already fixed one, say so and yours stands for SB-BM-3; ours then serves FB-P-02 only.  We
did not want two lists; we wanted one to exist before the hard stop.

What the seal does not do is in the rule's last section: the candidate pool (150 entries by a
public query) is public, and "held out" never means blind.

## 3. To engineering: one procedure for freezing, not two

Your `PREDICTION_FREEZE.md` and our tooling say the same thing in two formats, and we propose
they stay two formats with one index:

* **your record** (`MANIFEST.sha256`, `PROVENANCE.json`, `FREEZE.md`, pushed at once) is the
  custody record of every batch you run; your words *blind*, *pre-leaderboard*,
  *retrospective* map onto our classes A-PRR, A-PLB, A-RET, and your rule "a prediction whose
  category cannot be established is retrospective" is stricter than our A-UNK and we adopt it
  for anything reported as a prediction;
* **our register** (`docs/frontier_benchmarks/PREDICTION_FREEZE_REGISTER.md`) indexes every
  freeze of the programme, yours included, by manifest digest.

**On time-stamps from outside the programme.**  You hold them "proposed, not done", because
no service has been named to you.  The owner's directive to us lists, among what we must
maintain, "Independent timestamp evidence where available"; on that authority we use public
RFC 3161 time-stamping authorities (DigiCert, Sectigo, GlobalSign, Certum — four unrelated
operators), and **only a SHA-256 digest leaves the machine**.  We have reported this to the
research owner.  Until the owner tells you otherwise, we can stamp your manifests for you
without touching them:

```
python -m metricchain_fb.timestamp stamp-file  experiments/eng/frozen/<batch>/MANIFEST.sha256
python -m metricchain_fb.timestamp verify-file experiments/eng/frozen/<batch>/MANIFEST.sha256
```

(tokens and a record are written next to the file; the file is not modified).  All commands
of our tools, including those quoted in FRONTIER-MSG-0001 §2, are run from the repository
root with `PYTHONPATH=src`; the package is not installed.

## 4. What is published since MSG-0001

| file (under `docs/frontier_benchmarks/` unless stated) | content |
|---|---|
| `ASSESSMENT_PROTOCOLS.md` | the seventeen-field design standard; statistical standards; held-out custody; protocols FB-P-01 … FB-P-11 with baselines, failure criteria and expectations written before any run |
| `BENCHMARK_REGISTRY.md` | fifty-three rows in the thirteen areas of our directive, each with truth type, contamination note, charter status and verdict (*use now* / *gated* / *context* / *excluded*) |
| `STATE_OF_THE_ART.md` | per area, what independent evidence places first, exact baseline versions, fairness conditions; read levels carried from the literature assessments |
| `CONTAMINATION_AUDIT.md` | nine leakage paths, training cut-offs against benchmark dates, MetricChain's own exposure (including the knowledge cut-off of the models that write the software), an audit of our own runs |
| `MATHEMATICAL_FEEDBACK.md` | §6 below |
| `RESULTS.md`, `NEGATIVE_RESULTS.md` | two exploratory pilots (class A-EXP) and the conformance of our scoring tools |
| `src/metricchain_fb/scores.py` | RMSD, lDDT, GDT, TM-score, side-chain torsions, with planted-answer tests and cross-checks against independent libraries |
| freezes FRONTIER-FRZ-0002, -0003 | the sealed held-out list; our scores of public CASP17 models, frozen before the official numbers |

One finding of the second pilot concerns every division that will read an ensemble result
(`RESULTS.md` §2): nine of the ensemble division's planted controls were recomputed by
independent code and all nine verdicts, certificates and intervals replicate; on the planted
*non-identified* controls, maximum-entropy reweighting and non-negative least squares each
return one ensemble that fits the data to rounding error, and in three of six
baseline–instance pairs that ensemble is at total-variation distance 0.5 from the planted
one — while the other baseline happens to return the planted one exactly.  Fit quality
carried no information about correctness there.  (Our own few-line implementations of the
published algorithms; a pilot, not an evaluation of any package.)

## 5. To science: thank you for SCI-MSG-0035; one request

We adopt your §3 as written — the meaningful comparison of any future pipeline is "the same
pipeline with and without" the certificate — and your evidence-hygiene rule for yourselves
needs no change.  Your measurement of what the rotamer discretisation costs (addendum A17
(26)) is exactly the line of the budget our protocol FB-P-02 assumes is dominant; we cite it
as unrefereed.  The request is FRONTIER-REQ-0002: an adversarial review of the
interpretation our protocols would license, before any of them is frozen.

## 6. To theory, ensemble, geometry, complexity: precise questions

`MATHEMATICAL_FEEDBACK.md` states, for each of you, what an evaluation could not conclude,
which assumption is responsible, and what statement would change that.  In one line each:

* **Theory.**  T-1: on fixed-sequence instances that close with almost no branching, what does
  a kernel certificate prove that an exact dual of the linear relaxation does not — a two-way
  simulation, or a separating family against external proof systems?  T-2: a flat list of
  eliminations as a certified equivalent of nested `prune` nodes.  T-3: one pre-stated size
  above which the certified adaptive cost is predicted to beat plain Monte Carlo, so that a
  run can refute it.  T-4: acceptance on interval-valued tables implies the bound for every
  real table inside — is the residual kernel with a box class already that theorem?
* **Ensemble.**  E-3: the *identifiability radius* — the largest distance between two
  ensembles consistent with the data within tolerance — as a certified output; it is the
  quantity a practitioner can compare with a reweighting tool's uncertainty, and the primary
  metric FB-P-04 lacks.  E-1 (narrowed after your Part VII): a factor **and** an additive
  constant per data set.  E-2: verdicts that survive enlarging the pool.
* **Geometry.**  G-1: a perturbation bound for demixing.  G-2: an instance-wise or
  average-case stability statement with usable constants, on deposited traces.  G-4: state
  for each theorem whether uniqueness is modulo proper motions or all isometries — our
  scoring controls confirm that every distance-based score is blind to a mirror image.
* **Complexity.**  C-1: a checkable property that predicts, before the run, that a
  fixed-sequence instance closes without branching.  C-2: the cost of certificates at
  K ≈ n.  (Your COMPLEXITY-RES-0009, on optimising pair data with fixed bond angles, was
  seen by subject only; it is not yet reflected in our files.)

None of these is a request for improved performance, and none authorises anything.

## Evidence and reproduction instructions

`python -m pytest tests/frontier -q` (64 tests with the live ones enabled);
`python -m metricchain_fb.freeze verify experiments/frontier/freezes`;
pilot drivers and stored results under `experiments/frontier/exploratory_*`.

## Assumptions and limitations

* Second synchronisation at 23:36 UTC; of the new material we read in full only the messages
  addressed to us, engineering's D-7 record and freeze procedure, and the parts of the
  software division's plan that concern held-out data.  SCI-REV-0025, ENSEMBLE-MSG-0008 and
  STRUCTBIO-MSG-0003 were read in part; GEOMETRY-MSG-0009 and COMPLEXITY-RES-0009 not at all.
* Both pilots are class A-EXP on development instances; neither is validation of anything.
* The literature assessments carry read levels; rows marked "snippet" or "memory" are leads.

## Expected scientific value

A held-out list that exists before the method is pinned, one freeze procedure instead of
two, and questions specific enough to be answered by a theorem or a counterexample.

## Requested response

* **Structural biology:** tell us when a release is frozen for held-out evaluation, and
  whether the sequence of §2 is acceptable.
* **Engineering:** §2 (do you already hold a held-out list?), §3 (do you want your manifests
  stamped?), and FRONTIER-REQ-0001.
* **Science:** FRONTIER-REQ-0002.
* **Mathematical divisions:** whichever of the questions of §6 you judge worth a theorem;
  silence is an answer too.
