# Research log of the Structural & Computational Biology division

Newest entry first.  "Resume here" is the recovery point for a successor.

## Resume here (state at the consolidation halt, 2026-11-27)

**The division is halted by the owner's directive SB-D-3.  Do nothing without explicit
authorisation.**  When authorised, in this order: (1) read
`docs/collaboration/consolidation/structural-biology.md` and `HANDOFF.md` ("Unfinished work");
(2) run the three verification commands of `HANDOFF.md`; (3) fetch the other seven branches
and read what answers STRUCTBIO-MSG-0004, -RES-0003, -REQ-0001, -REQ-0004 (never the Frontier
division's sealed list); (4) take the owner's decision on which of the three recommended
actions (consolidation report §E) to pursue.  Environment of the session machine, which a new
machine will not have: Python environment `~/.venvs/structbio` (rebuild from
`requirements-structbio.txt`); Lean 4.31.0 under `~/.lean/` with Mathlib v4.31.0 in `.lake/`
(`lake exe cache get`).

## 2026-11-27 — third cycle and consolidation (about 23:45 UTC on 26 November to the halt)

- Crambin on v1 with conditioning: `ln Z` to 0.054 nats; request STRUCTBIO-REQ-0004; defect
  SB-DEF-08 (rows recorded the head at row time).
- SCI-REV-0026 arrived (adversarial review by Science).  Its major finding F1 was measured
  with the reading committed first (SB-X-005): the seed of model v1 moves the certified
  minimum by 12.8 to 24.6 kcal/mol.  Model v2 written test-first (deterministic hydrogens;
  wells; shares of torsion space); development set re-run on `v2` and `v2-lib` (R-9); two of
  our five expectations were wrong and are recorded.
- The science division's two constructions implemented and run (well gaps; optimality under
  entrywise error): R-10.  State weights for C2; crambin on `v2-lib`: `ln Z_w` to 0.0075 nats,
  populations of all residues to 0.024 (R-11).  Null method (R-12): the relaxation is tight on
  all twelve development instances.  Regime quantities for Complexity (R-13).
- Lean subagent delivered 19 theorems for the Z rules; verified by our own build and audit;
  the theory division's audit file left untouched.
- A container restart at about 00:25 UTC killed two background jobs; files survived; the jobs
  were re-run.
- Fourth synchronisation through a read-only subagent (`intake/SYNC4_REPORT.md`): Engineering's
  review of our first commit, Frontier's sealed list and pilot, Complexity's answer to Q-5.
- Adversarial reviewer closed STRUCTBIO-REV-0001: 19 findings; a fixer subagent was started on
  them; then the owner's consolidation directive arrived.  Stopped: everything listed in
  `OWNER_DIRECTIVES.md` SB-D-3 ("How this division applied it").  Written: results R-10 … R-13,
  STRUCTBIO-RES-0003, STRUCTBIO-MSG-0004, the consolidation assessment, this handoff.

## Resume here as it stood at the second checkpoint (2026-11-26 about 23:40 UTC; superseded)

1. **Branch** `research/structural-biology`, created at theory `b2caab6`; nothing merged from
   anywhere.  Directives: `OWNER_DIRECTIVES.md` (SB-D-1 founding, SB-D-2 eighth division).
2. **Environment** (not in the repository — rebuild if the machine is new):
   `python3 -m venv ~/.venvs/structbio && ~/.venvs/structbio/bin/pip install -r requirements-structbio.txt`;
   Lean 4.31.0 unpacked in `~/.lean/lean-4.31.0-linux/` (release archive from GitHub), then
   `lake exe cache get` and `lake build proofs.CertificateAlgebra proofs.Frontiers.PartitionProduct`
   (57 s here).  Read-only worktrees of the other branches are convenient and disposable.
3. **Done:** capabilities C1 and C1b with tests, C2 in a first version, the molecular layer,
   the development results (RESULTS R-1 … R-7), intake, plan, benchmark plan, architecture,
   assumption and physical-applicability registers, verification report (the last four drafted
   by a subagent from the code and corrected by the coordinator), messages MSG-0001 … -0003,
   requests REQ-0001 … -0003.
4. **In progress when this was written:** see the last item of the second-cycle entry below.
5. **Next, in order** (state after the second checkpoint: C1b done; C2 first version done):
   (a) collect the two subagents' work — if `tests/structbio/test_adversarial_*.py` has a
   failing test, that is a finding to fix first; if `proofs/StructBio/FactorElimination.lean`
   exists, build it (`lake build proofs.StructBio.FactorElimination`), then decide whether to
   run the whole audit (`scripts/audit_all.sh`, about an hour) before committing the edit of
   `proofs/AxiomAudit.lean`; (b) C2: conditioning (a `branch` step) so that crambin can be
   enclosed tightly at the cost of hours — then a request to the engineering division to run
   it; a file format for Z certificates; populations with the kept site's pairs exact;
   (c) the second-order sandwich needs pair marginals of the reference — only worth building
   if the theory division answers Q-5; (d) read ENSEMBLE-MSG-0006, GEOMETRY-MSG-0005–0008 and
   the science division's protocol of its checkpoint 65, then start C3; (e) at every
   checkpoint: fetch all branches, read what is addressed to us, update
   `STRUCTBIO_UPSTREAM_SYNC.md`, status and digest.
6. **Do not:** run Modal or any paid service; touch another branch; open a pull request;
   look at held-out structures (anything outside the development list of the benchmark plan);
   fetch CASP17 reference data.

## 2026-11-26 — second cycle (about 23:10–23:40 UTC)

* Capability C1b (flip gaps) written test-first; all residues of five development structures
  certified (R-6).  Reading: the certified minimum is unique and rounding-robust, and
  thermally negligible.
* A subagent asked to write the checker's specification from the code found three things we
  had wrong: a loader that was not strict, no report of whether the root box is full, and a
  misattributed Lean theorem.  Fixed test-first (commit 263dd18); linked correction
  STRUCTBIO-MSG-0003; certificate files regenerated.
* Capability C2, first version, written test-first: certified exponential with outward
  rounding, interval tables in two tiers, steps `prune` and `relax`, elimination, populations
  of one kept site, checker, producer.  47 tests pass.  Crambin: `ln Z ∈ [69.564, 70.927]` (R-7).
* Synthetic validation (quick grid, 120 s limit): certified to 25 sites, abstentions from 40
  (R-5); hypothesis H2b is expected to fail.
* Started in the background and not finished when this was written: flip gaps of ubiquitin
  (rows append to `experiments/structbio/flipgaps_dev/results.jsonl`); the remaining cells of
  the synthetic quick grid; a Lean file for rules R-1 … R-4 (subagent; target
  `proofs/StructBio/FactorElimination.lean` with an append-only edit of `proofs/AxiomAudit.lean`);
  an adversarial review of the checkers (subagent; report `reviews/STRUCTBIO-REV-0001.md`, new
  tests `tests/structbio/test_adversarial_*.py` — a failing one there is a finding, not noise).

## 2026-11-26 — first cycle

* 21:55 UTC founding directive received.  Six branch heads recorded; eight read-only
  reviewers (one per slice of the six divisions) wrote the intake reports now in `intake/`.
* Branch created at theory `b2caab6` (latest declared checkpoint; kernel files identical at
  the theory head); Lean toolchain and Mathlib cache installed; kernel modules build.
* C1 written test-first: exact model, compact certificate format with exact conversion to
  `metricchain-cert/1`, independent integer checker, producer.  The differential mutation
  test found one converter defect (SB-DEF-02) on its second run.
* Molecular layer written by a subagent against a written specification and an acceptance
  test (agreement with an independent OpenMM system); it found and fixed the hydrogen
  reproducibility defect (SB-DEF-03).
* First real structure (crambin) certified at zero gap in 0.3 s.  Larger structures exposed
  the recursion defect (SB-DEF-01) and the masked test (SB-DEF-04).  All six development
  structures certified; SB-X-001 committed with detached certificates.
* Exploratory measurement for partition functions (R-3): the planned route does not reach
  ubiquitin.  Recorded as SB-D-E-01; question Q-5 sent to the theory division.
* 22:40 UTC supplementary directive (eighth division).  Protocol copy updated; maturity
  statement written (MSG-0002).  No CASP17 data held or fetched.
* Other divisions had already written to us: SCI-MSG-0034 (read in full; its requests
  S-1 … S-6 answered in REQ-0002), engineering's BM-7 and freeze rules (read),
  COMPLEXITY-MSG-0005 (head read), ENSEMBLE-MSG-0006 and GEOMETRY-MSG-0005–0008 (not yet read).
* Prior-art search by a subagent with web access (`PRIOR_ART.md`, `BASELINE_REGISTER.md`):
  checkable optimality proofs and guaranteed partition-function brackets both have close
  precedents; not found: proof logging for cost-function networks, checkable enclosures of
  Boltzmann sums, certified rotamer populations.
* Budget: no Modal job, no paid service.  The balance of Claude credits is not visible from
  this session; the engineering ledger (read at `96c4fd2`) has no allocation for this division.
