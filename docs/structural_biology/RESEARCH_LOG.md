# Research log of the Structural & Computational Biology division

Newest entry first.  "Resume here" is the recovery point for a successor.

## Resume here (state at the first checkpoint, 2026-11-26 about 23:15 UTC)

1. **Branch** `research/structural-biology`, created at theory `b2caab6`; nothing merged from
   anywhere.  Directives: `OWNER_DIRECTIVES.md` (SB-D-1 founding, SB-D-2 eighth division).
2. **Environment** (not in the repository — rebuild if the machine is new):
   `python3 -m venv ~/.venvs/structbio && ~/.venvs/structbio/bin/pip install -r requirements-structbio.txt`;
   Lean 4.31.0 unpacked in `~/.lean/lean-4.31.0-linux/` (release archive from GitHub), then
   `lake exe cache get` and `lake build proofs.CertificateAlgebra proofs.Frontiers.PartitionProduct`
   (57 s here).  Read-only worktrees of the other branches are convenient and disposable.
3. **Done:** capability C1 with tests, the molecular layer, the development results
   (RESULTS R-1 … R-5), intake, plan, benchmark plan, first messages (MSG-0001, -0002;
   REQ-0001, -0002, -0003).
4. **In progress when this was written:** SB-X-002 synthetic validation (`--quick`), whose
   rows append to `experiments/structbio/gmec_synth/results.jsonl`; four documents being
   drafted by a subagent (ARCHITECTURE, ASSUMPTION_REGISTER, PHYSICAL_APPLICABILITY,
   VERIFICATION_REPORT) — review them before relying on them.
5. **Next, in order:** (a) C1b — per-residue flip gaps by `min` certificates on restricted
   boxes; (b) C2 engine — certified exponential with rounding, factor tables, elimination,
   steps `prune`/`relax`, exact and outward-rounded tiers, checker, tests against enumeration;
   crambin and local ensembles; (c) `proofs/StructBio/FactorElimination.lean`; (d) an internal
   adversarial review of `mincheck.py`/`mincert.py` by a subagent with a mandate to break
   them; (e) read ENSEMBLE-MSG-0006, GEOMETRY-MSG-0005–0008 and the science division's
   protocol of its checkpoint 65; (f) at every checkpoint: fetch all branches, read what is
   addressed to us, update `STRUCTBIO_UPSTREAM_SYNC.md`, status and digest.
6. **Do not:** run Modal or any paid service; touch another branch; open a pull request;
   look at held-out structures (anything outside the development list of the benchmark plan);
   fetch CASP17 reference data.

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
