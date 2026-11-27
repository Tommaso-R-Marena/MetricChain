# Research intake: what exists to be evaluated

> **Read §6 first.**  Sections 1–5 describe the branches as pinned at 22:35–23:00 UTC on
> 2026-11-26.  Within the hour the structural-biology branch gained a molecular layer and a
> toulbar2 comparison; §6 lists what that changes.  Sections 1–5 are kept as written.

*Frontier Benchmarking division.  Version 1, 2026-11-26.  Sources: the seven other branches
at the commits pinned in `docs/collaboration/FRONTIER_UPSTREAM_SYNC.md`; the three intake
reports in `intake/` (committed as delivered); and what the coordinator read directly (§5).
Nothing here was re-proved or re-run by this division.  Labels are the originating
divisions' own.*

## 1. What MetricChain is, in one paragraph

A body of mathematics and checkers for **finite models of fixed-sequence chain molecules**:
exact-arithmetic certificate kernels (a minimum-energy bound, the same under an unknown
residual of a stated class, two-sided bounds on partition functions), whose soundness is
machine-checked in Lean; a theory of how many energy evaluations any algorithm needs to
certify such quantities; identifiability theory for ensembles observed through averaged
data; rigidity and reconstruction theory for chains; and complexity classifications.  It
contains **no structure predictor, no force field of its own, no reader of experimental
data**.  Every guarantee is a statement about a published table of rationals or a stated
mathematical class.

## 2. The capabilities an evaluation could address

"Maturity" is ours: **M3** software exists, runs on stated inputs and has an independent
check; **M2** a specification and test instances exist, software is partial; **M1**
mathematics only; **M0** stated intention.

| # | capability | owner (commit) | status as labelled by its owner | maturity | external comparison done? | dimensions it could bear on |
|---|---|---|---|---|---|---|
| C1 | certificate of a lower bound on the minimum energy of a pairwise integer model (branch, leaf, prune rules) | theory kernel `verify_sound` [V]; producers and checkers at structural biology (`720e0ec`) and engineering (`c683fde`, checker only; its producer is uncommitted) | rule semantics [V]; checker implementations "tested, not verified" | **M3** on abstract tables; **M0** on anything molecular | **none** | D3, D8, D9 |
| C2 | the same for every residual of an envelope class, with a check that the class is not empty | theory `verifyITop_sound` [V] | envelope constants and anchors are inputs; "certifying such constants for a concrete learned residual is not part of this development" | M1–M2 | none | D9, D10 |
| C3 | two-sided certified bounds on ln Z and populations of a rotamer model | theory kernel [V]; science's sandwich certificate [P]+[M] | Lys₁₂ instance certified to 8·10⁻⁵ nats; parts unrefereed; "the certificate is not a file" yet (engineering Q-08) | M2 | none (K\*, model counters, annealed sampling: read about, never run) | D5, D9, D3 |
| C4 | lower bounds on the number of evaluations any algorithm needs; nested adaptive algorithms | theory §§10–11 ([V] lower bounds, [P] upper bounds); engineering BM-1 | at every simulable size the adaptive algorithm is worse than plain Monte Carlo; certified nested bounds 1.9–4× the lower bound in the exponent (draft, unpublished) | M3 as a computation about a synthetic class | internal baselines only | D3 (negative so far), D9 |
| C5 | identification verdicts and exact certified intervals for an ensemble on a finite candidate pool observed through linear averaged data | ensemble (`2d2054d`): E1, F1–F3, [V] cores | 18 control instances specified, "verified by their generator only"; harness not built; no request to engineering | **M2** | none; no reweighting tool ever run | D5, D10, D9 |
| C6 | demixing of K-state chain ensembles from averaged squared distances; exact thresholds | geometry (`9f164f9`): Theorems B, C, I, I′, DEMIX | exact on exact data; **no noise guarantee**; K must be supplied; automatic K detection failed at noise 10⁻⁴ | M2 | none | D4, D10 |
| C7 | global stability of reconstruction from sequence-local distances | geometry Theorem L/L⁺ | by its authors and by science: certified range ≤ 10⁻⁵ Å — "empty for data of realistic accuracy" | M1 | none | D4 (negative) |
| C8 | hardness of multi-strand nearest-neighbour folding; an all-orderings partition-function algorithm | complexity (`75266b2`) | hardness [P], reviewed across divisions; algorithm is reference Python, prior art for the base-pair model | M2 | none (a NUPACK-type code is named, not read) | D9, D3 |
| C9 | class constants of real force-field residuals; divergence diagnostics for surrogates | science | measured on grids, "a lower bound … never a bound"; H3 refuted for an implicit-solvent term in backbone torsions | M2 | uses OpenMM force fields as the model, no comparator method | D2 |
| C10 | realizability and torsion-to-RMSD bounds | theory phase 1 | novelty withdrawn after review (known results); RMSD bound loose (19.61 against an actual 2.01 at 96 torsions) | M1 | classical bounds only | D4 |

## 3. Findings of other divisions that every evaluation here inherits

These are not ours; they are quoted because an evaluator who forgot them would overstate
whatever is measured next.

1. **The best certified number is far more precise than its model is accurate.**  Science's
   four-line budget for its Lys₁₂ certificate: certified width 8·10⁻⁵ nats; discretisation
   term not bounded (of order a nat per angle at rotamer resolution on a toy chain); energy
   model of order k_BT per residue between force fields of one lineage; evaluation tolerance
   10⁻⁴–10⁻³ nats resting on an evaluator bound that is assumed, not proved.  Its own verdict:
   the certificate "removes sampling error only", by "four to five orders of magnitude" more
   than the model's accuracy warrants.
2. **The step from a real-valued energy to the integer tables the kernels check is unproved**
   (assumption A9; engineering Q-19, design started).  Until it exists, "certified" means
   certified for the published integers.
3. **A cheap residual class does not contain the physics tested so far**: an implicit-solvent
   polarisation energy in backbone torsions has class constants of 12–53 k_BT per site,
   growing with length (science B1, hypothesis H3 refuted there; confirmed for same-lineage
   force-field differences).
4. **Asymptotic advantages have not appeared at accessible sizes**: the nested algorithm is
   "not competitive at any size where it can be evaluated"; one schedule costs more than the
   non-adaptive bound up to n ≈ 2·10⁴; several guarantees are recorded by theory itself as
   computationally vacuous.
5. **Novelty has been repeatedly withdrawn after review** (theory D11, D12, D24; science's
   cost table; ensemble E19(a); geometry Theorem B at d = 1; complexity's flagship problems).
   What survives as plausibly new, in science's classification, is narrow: a certificate valid
   for a whole class of residuals, and proof-carrying solving for cost-function networks,
   "its *advantage* unmeasured".
6. **Worst-case searches stop low** (SCI-REV-0018): a "worst instance found" is a lower bound.
7. **Reviews are internal.**  Every referee is an AI session of the programme.

## 4. What has never been done by anyone in the programme

* **No comparison with any external method.**  Not toulbar2, OSPREY, an integer-programming
  solver used as a competitor, proof-logging solvers with VeriPB/CakePB, K\*, a model
  counter, a reweighting tool, an ensemble generator, a packer, or a multi-strand folding
  code.  Theory §6.4 says of the nearest comparison: "has not been measured".
* **No contact with experimental data.**  No PDB structure, NMR or scattering dataset or
  measured free energy enters any computation on any branch; science states "Nothing in any
  branch has been compared with a measurement."
* **No held-out evaluation.**  Every instance used so far was built by the division that
  evaluated on it.
* **No forward model with a stated error** for any experimental observable.

These four absences, not any single benchmark number, are the present answer to the question
this division was founded to ask.  `ASSESSMENT_PROTOCOLS.md` is the plan to replace them
with evidence; `MATHEMATICAL_FEEDBACK.md` says what each division would have to supply.

## 5. What the coordinator verified directly, and what rests on the intake reports

| statement | basis |
|---|---|
| the structural-biology software is one commit of about 1,150 lines operating on abstract integer tables, with no molecular input | read directly (`model.py`, `synthetic.py` in full; other modules by docstring) at `720e0ec` |
| engineering's campaigns BM-1…BM-7, their stages and its readiness test | read directly (`BENCHMARK_MASTER_PLAN.md`, `BENCHMARK_READINESS.md`, `BENCHMARK_RESULTS.md`) at `c683fde` |
| science's evaluation protocol, its four-line budget and its hypotheses H1–H11 | read directly (`SOFTWARE_EVALUATION_PROTOCOL.md` in full; `BENCHMARK_DESIGN.md` §§0–2) at `4661a03` |
| everything else in §§2–4 | the intake reports, each of which states what it did not read |

Known disagreements inside the records we read, passed to their owners in FRONTIER-MSG-0001:
the theory status file lists as not established a theorem that the work-in-progress commit
states; engineering's ledger row "spent" is inconsistent with its neighbouring rows; science's
protocol cites requests S-1…S-5 where its message has six.

## 6. Second synchronisation (2026-11-26 23:36 UTC): what changed, and which sentences above it overtakes

Heads and what was read: `docs/collaboration/FRONTIER_UPSTREAM_SYNC.md`.

| statement above | status after the second synchronisation |
|---|---|
| §2 row C1: "M3 on abstract tables; M0 on anything molecular" | **overtaken.**  At structural biology `1756529` a molecular layer exists (deposited structure → fixed-backbone rotamer model, pairwise ff14SB torsion and Lennard-Jones terms and Coulomb with a distance-dependent dielectric, in vacuo; tables agree with an independent OpenMM system to 4·10⁻¹¹ kcal/mol by its authors' report).  Six development structures (26–65 flexible residues) are certified at zero gap.  Maturity for a *computational* evaluation: M3.  Its authors state it is not a structure predictor and that the energy model is crude |
| §2 row C3: "the certificate is not a file" | partly overtaken: the software division has a first checked enclosure of ln Z for crambin, [69.56, 70.93] (1.36 nats wide, "not tight enough for populations"), and reports that its route "does not reach the size of ubiquitin" |
| §4 "No comparison with any external method" | **no longer true for C1.**  The software division compared its certified producer with toulbar2 1.4.0.3 on its six development structures: same optimum every time, toulbar2 7–25 times faster (development evidence, its own run).  Still true: no comparison with proof logging (VeriPB/CakePB), with an exact dual of the linear relaxation, with any packer, with any ensemble or partition-function method; and no instance its authors did not build — until our pilot (`RESULTS.md` §1) |
| §4 "No contact with experimental data" | partly overtaken: deposited structures are now *inputs* (backbones) and the deposited side chains are a possible reference (its plan SB-BM-6, design only).  No comparison with a measurement has been made |
| §4 "No held-out evaluation" | still true; the software division has closed its development list, asked that another division fix and hash a held-out list, and asked not to see it — done as freeze FRONTIER-FRZ-0002 |
| §5, inconsistency in the theory records | resolved by the theory division's twenty-fourth checkpoint (`07cde81`) |

New material from the other divisions that bears on our protocols:

* **Science** (SCI-MSG-0035, to us): agrees that nothing in MetricChain is a structure
  predictor; names what can be evaluated today (certified quantities against exact solvers
  and converged sampling *of the same model*; uncertainty statements on planted-truth data;
  geometric error bars, "still far too large to be informative"); reports a new measurement
  — on one force field with continuous torsions, the minimum of a rigid-rotamer table can lie
  in a different well from the continuous minimum, populations are off by up to 0.48 in total
  variation, free energies by nats per torsion (unrefereed).  That is line 2 of its error
  budget and it dwarfs any optimality gap.
* **Engineering** (D-7; `PREDICTION_FREEZE.md`): keeps the evidence that a prediction existed;
  defines *blind*, *pre-leaderboard*, *retrospective* compatibly with our classes A-PRR,
  A-PLB, A-RET; regards a time-stamp from a service outside the programme as "proposed, not
  done" pending the owner's naming a service.  Our directive lists "independent timestamp
  evidence where available"; we used public RFC 3161 authorities and send only digests
  (FRONTIER-MSG-0002 §4).
* **Structural biology** (STRUCTBIO-MSG-0002, to us): the commitments of its §4 (closed
  development list; model frozen before a held-out run; no tuning on held-out scores) are
  exactly what `ASSESSMENT_PROTOCOLS.md` §3 needs; its expectation that its vacuum model will
  place side chains worse than specialised packers is written before any run, as is ours
  (FB-P-02, E1–E3).
* **Ensemble** (ENSEMBLE-MSG-0008): data with one unknown positive factor are covered
  (E23: "the price of the factor is exactly the constant function"); lengths and squares of
  means are not linear and are now treated (unreviewed).  This answers part of our
  question E-1.
