# Research intake: what exists to be evaluated

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
