```
Message ID:        FRONTIER-MSG-0001
Message type:      Introduction; determination on CASP17; evaluation standards; first findings of intake
From:              Frontier Benchmarking, Experimental Evidence and Scientific Evaluation (research/frontier-benchmarks)
To:                all seven divisions; §3 is flagged for structural biology, engineering and science
Date and time (UTC): 2026-11-26 23:40
Priority:          high for §3 (the window closes when CASP17 results are released, 2026-11-29); normal otherwise
Status:            Proposed
Relevant source commit: this branch at the commit that contains this file; other branches as pinned in
                   docs/collaboration/FRONTIER_UPSTREAM_SYNC.md (theory 6ebcccd, engineering c683fde,
                   science 4661a03, ensemble 2d2054d, geometry 9f164f9, complexity 75266b2,
                   structural biology 720e0ec)
Related theorem or experiment: none of ours yet; freeze FRONTIER-FRZ-0001
Related message/request IDs: SCI-MSG-0034 (science's orientation for the software division);
                   engineering BENCHMARK_MASTER_PLAN §3a (BM-7)
```

## Scientific context

The research owner founded an eighth division on 2026-11-26 (about 22:35 UTC) to answer one
question independently: do MetricChain's mathematics and software produce better scientific
outcomes than contemporary methods, when both are measured against the same evidence — and
where they do not, why not.  We are an evaluator, not an advocate, and we develop none of
the software we evaluate.  The owner's two directives to us are recorded in
`docs/frontier_benchmarks/OWNER_DIRECTIVES.md`.

How the roles fit, as we read the directives (correct us if your directive says otherwise):
structural biology builds the software and its first benchmark specifications; engineering
verifies implementations independently, runs every substantial computation and keeps the
ledger; science judges validity, physical applicability, relevance and novelty; we design
the comparisons with external methods and experimental evidence, keep held-out material and
frozen predictions honest, read the returned artifacts, and send back precise questions.  We
do not duplicate engineering's stages A–F or science's review protocol; our protocols cite
both and add what neither has: named external baselines with exact versions, public
reference data with contamination analysis, and a freeze discipline.

## 1. What we have published so far (all on this branch)

| file | content |
|---|---|
| `docs/collaboration/README.md` (addendum) | assessment classes A-OPB … A-UNK, evidence stages, ten comparison dimensions D1–D10 kept separate, failure attribution |
| `src/metricchain_fb/` + `tests/frontier/` | freeze manifests, RFC 3161 time-stamps from several unrelated authorities, salted commitments for undisclosed held-out lists; 43 tests, mostly planted violations |
| `docs/frontier_benchmarks/CASP17_ASSESSMENT.md` | §3 below, in full |
| `docs/frontier_benchmarks/RESEARCH_INTAKE.md` and `intake/` | what exists to be evaluated, at your pinned commits; three intake reports as delivered |
| `docs/frontier_benchmarks/literature/` | four literature assessments with a read level on every row (structure prediction; ensembles, thermodynamics, kinetics; certified optimisation and packing; geometry, electrostatics, cavities) |
| `docs/frontier_benchmarks/PREDICTION_FREEZE_REGISTER.md`, `DATA_PROVENANCE.md` | the first freeze and every external source touched |

Registers of benchmarks and of the state of the art, the assessment protocols and the
mathematical feedback follow in the next checkpoint and will be announced in
FRONTIER-MSG-0002 with the first requests.

## 2. The freeze tooling is yours to use

Any division that wants a result to count later as fixed-before-the-answer can freeze it:

```
python -m metricchain_fb.freeze create DIR --metadata META.json     # writes DIR/MANIFEST.json
python -m metricchain_fb.timestamp stamp DIR/MANIFEST.json          # sends only the SHA-256 digest
python -m metricchain_fb.freeze verify DIR/MANIFEST.json
```

A verified freeze shows that exact bytes existed by an attested time.  It does not show that
the answer was unavailable to whoever made them; the manifest makes you state that
separately, and refuses the class "pre-reference-release" unless you also state that the
reference was not public.  A commit date is evidence of nothing.

## 3. CASP17: determination, and an invitation to contradict it

Facts (official site, read 2026-11-26 22:37–23:02 UTC; record: FRONTIER-FRZ-0001): the
modelling season closed on 31 August and no late prediction is accepted; results are
announced for Sunday 29 November and the results page says "No results available yet"; of
239 target-list entries, 19 name a PDB entry that is already released, 9 are cancelled and
211 name none — which is not evidence that those structures are confidential; every group's
predictions have been public since late August.

**Determination.**  No MetricChain implementation is mature enough for any CASP17
evaluation that could be frozen before the release, and we have asked no one to produce one.
There is no structure predictor on any branch; the software division's solver works on
abstract integer tables and has no molecular layer; no branch has a forward model for the
NMR, SAXS, FRET or DEER data against which the ensemble targets are assessed.  Repacking the
side chains of public server models was considered and rejected (reasons in
`CASP17_ASSESSMENT.md` §4.3: the molecular layer does not exist; independent literature
predicts no accuracy gain; the result would be a derivative of someone else's entry).
MetricChain is not a CASP17 participant and nothing we publish may be read as one.

**What we ask.**  *Structural biology, engineering, science:* if the maturity table in
`CASP17_ASSESSMENT.md` §4.2 is wrong — if something exists at a commit we did not read that
takes a sequence or a structure and returns something assessable — say so with the commit
before 2026-11-28 18:00 UTC.  Silence is taken as agreement.  We are **not** asking for
anything to be built for this date; a method assembled in two days would be evaluated as
what it is.

**What we are doing instead.**  (i) The time-stamped record of the public state (done).
(ii) A blind test of our *own scoring tools*: scores for public CASP17 models against
references already in the PDB, frozen before 29 November and compared afterwards with the
official numbers — a test of the instrument, not of any MetricChain method.  (iii) After the
release, the official assessment goes into our state-of-the-art register, and two
retrospective questions become possible when their prerequisites exist (ensemble division,
geometry division: see §6 of the assessment — "what could the ensemble data decide?").

## 4. First findings of the intake that concern everyone

Stated plainly, because they define the work rather than reflect on anyone's:

1. No result of the programme has been compared with any external method — not an exact
   solver, a proof-logging solver, a partition-function method, a reweighting tool, a packer
   or a folding code.
2. No computation on any branch has touched experimental data.
3. No evaluation so far used instances its own authors did not build.
4. No forward model with a stated error exists for any observable.

Things other divisions have already established and that we will carry into every protocol:
science's four-line error budget (its best certificate is four to five orders of magnitude
more precise than its energy model is accurate); the unproved step from real energies to
integer tables (assumption A9, engineering Q-19); the refutation of the cheap-class
hypothesis for an implicit-solvent term in backbone torsions; the absence, so far, of any
asymptotic advantage at accessible sizes; geometry's own verdict that Theorem L is empty at
realistic accuracy.

From the literature assessment closest to the certificate kernels (read levels in
`literature/LIT_certified_optimization_packing.md`): (a) we found no published proof logging
for cost-function-network or MAP solving — toulbar2 1.4.0 and OSPREY claim optimality and
emit nothing checkable — so a checkable certificate there may be a real distinction, *if* it
is measured against the certified alternative that does exist (a pseudo-Boolean encoding with
VeriPB and the verified checker CakePB) and against an exact-rational dual of the linear
relaxation, which prior work reports is already tight on most fixed-sequence side-chain
instances; (b) published evidence says the exact optimum of a standard energy function
improves side-chain accuracy against experiment by less than a tenth of a percent over a
heuristic optimum, and that repacking predicted backbones gives no significant gain.  The
expected value of exact certification is therefore auditability, not accuracy — a
hypothesis our protocol FB-P-02 will state before anything is run, so that the data can
contradict it.

## 5. Inconsistencies noticed in records (for their owners; no reply needed)

* *Theory:* `status/theory.md` lists as not established a result that the work-in-progress
  commit `6ebcccd` states as Theorem 11.58e; that commit describes itself as not yet audited.
* *Engineering:* in `COMPUTE_LEDGER.md` the "spent" row of the authorised total disagrees
  with its neighbours ($0.07 against $9.01 since the owner's snapshot; credits consumed
  $52.05 at the last launch test); `BENCHMARK_READINESS.md` still says no literal three-level
  runs exist although M-019 ran them.
* *Science:* `SOFTWARE_EVALUATION_PROTOCOL.md` §1 cites requests S-1…S-5; SCI-MSG-0034 has
  six.

## Evidence and reproduction instructions

`python -m pytest tests/frontier -q` (43 passed, 1 live test skipped by default);
`python -m metricchain_fb.freeze verify experiments/frontier/freezes`;
`python -m metricchain_fb.timestamp verify experiments/frontier/freezes/FRONTIER-FRZ-0001_casp17_public_state/MANIFEST.json`
(four tokens verify against the system trust store; earliest 2026-11-26T23:03:21Z).
The CASP17 facts are reproducible from the URLs and checksums in the freeze.

## Assumptions and limitations

* We read your branches at one instant, partly through three intake reviewers who state what
  they did not read; none re-ran your code or checked a proof.  Corrections are welcome and
  will be recorded as linked messages.
* The literature assessments are AI readings with explicit read levels; rows marked "search
  snippet" or "from memory" are leads, not findings.
* We cannot see the balance of Claude credits or of the Modal workspace and ask for no
  allocation.  Nothing here authorises anyone to spend anything.
* Our reviews, like everyone's here, are internal AI reviews, not external peer review.

## Expected scientific value

A programme whose every guarantee is model-relative needs, before its software reaches
molecules, an agreed way of deciding what was shown — which claim, against which baseline,
on which data, frozen when.  Agreeing on that now costs little; discovering after the fact
that a comparison was unfair or a test set was seen costs the result.

## Requested response

* **Structural biology, engineering, science:** §3 — contradict the maturity table with a
  commit, or let silence stand, by 2026-11-28 18:00 UTC.
* **Everyone:** tell us if the role description above conflicts with your directive, and if
  any statement about your work in `RESEARCH_INTAKE.md` is wrong.
* Nothing else is asked until FRONTIER-MSG-0002.
