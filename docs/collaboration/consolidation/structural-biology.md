# Consolidation assessment — Structural & Computational Biology, Software Development and Applications

Branch `research/structural-biology`.  Written 2026-11-27 under the research owner's consolidation
directive.  Everything below is development evidence on six public structures (four proteins)
and synthetic instances; nothing has been evaluated on held-out data; nothing is a statement
about a protein.  Review status is internal (AI sessions of other divisions and of this one),
not external peer review.  Details and reproduction: `docs/structural_biology/RESULTS.md`
(R-1 … R-13), `HANDOFF.md`, `VERIFICATION_REPORT.md`.

## A. Executive assessment

**What exists.**  A tested research package (`src/metricchain_sb`, about 3 700 lines; 14 test
files) that goes from a deposited structure to independently checkable statements about a
stated discrete energy model:

1. a molecular layer that builds fixed-backbone, fixed-sequence rotamer tables (Amber ff14SB
   torsions and Lennard-Jones, Coulomb with `ε = 4r`, in vacuo, idealised staggered rotamers,
   hydrogens by a deterministic geometric rule), validated numerically against an independent
   OpenMM system;
2. certificates of the exact minimum of the integer tables with an independent exact checker
   (**C1**), plus certified per-residue gaps — for leaving a state, for leaving a rotamer well,
   and optimality in every table within a stated entrywise error (**C1b**);
3. certificates of two-sided enclosures of `ln Z` and of rotamer populations with an
   independent checker in exact-rational and outward-rounded floating-point arithmetic (**C2**);
4. machine-checked rule semantics: the theory division's kernel for C1, and 19 Lean theorems of
   our own (`proofs/StructBio/FactorElimination.lean`) for the rules of C2.

**What has been shown.**  On the development structures every minimum is certified with zero
gap and equals the optimum of the exact solver toulbar2; crambin's `ln Z` is enclosed to
0.0075 nats and the populations of all its 26 flexible residues to 0.024.  The minimum checker
has been attacked three times (Engineering: 22 472 random claims at our first commit; our own
adversarial reviewer: 60 000 hand-built certificates; the Frontier division ran it unmodified
on ten larger public instances) and the Z checker once (40 000 certificates in two tiers): no
false acceptance under normal use.  Our adversarial review found 19 defects outside that
envelope (STRUCTBIO-REV-0001); their repair is the last engineering item of this checkpoint
(§ "State at the halt").

**What has not been shown, and what was found against us.**  No improvement over established
methods has been demonstrated on any dimension.  toulbar2 finds every certified optimum 6 to 27
times faster and no certificate changed an answer.  On every development instance the plain
linear relaxation is already tight, so a certificate is in substance an exact dual solution of
a linear programme — established technology.  The certified quantities are properties of a
crude model whose own errors (discretisation: nats per torsion; force field: kcal/mol per
residue) exceed every certified width by orders of magnitude.  Our first model contained a
random seed worth 13 to 25 kcal/mol in the certified minimum (found by the science division,
confirmed and removed by us).  Certified partition functions stop at about the size of crambin
under this dense model.

**Defensible summary.**  The division built correct, checkable infrastructure and a set of
quantified limits.  Whether MetricChain's mathematics yields a *superior* structural-biology
method is, on our evidence, not established: established as a design property on guarantees,
negative on speed, untested against experiment.

## B. Strongest contributions (four; ranked)

### B1. Checkable enclosures of `ln Z` and rotamer populations for a pairwise rotamer model (C2)

- *Contribution.*  A certificate format (`structbio-zcert/1`), an untrusted producer (thermal
  dead-end elimination, product-form relaxation of weakly coupled pairs, variable elimination
  on interval tables, conditioning) and an independent checker that returns
  `[ln_z_lo, ln_z_hi]` and population intervals, in exact rationals or outward-rounded
  binary64; states weighted by their share of torsion space.
- *Artifacts.*  `src/metricchain_sb/{zcert,zcheck,itables,expo,partition}.py`;
  `tests/structbio/test_zcert.py`, `test_expo.py`, `test_adversarial_zcheck.py`;
  `proofs/StructBio/FactorElimination.lean`; experiments SB-X-004, SB-X-008; RESULTS R-7, R-11,
  R-13.  Commits `e82010b`, `b40f903`, `53dca3b`, `d61fc53`.
- *Verification and review.*  Rule semantics machine-checked (ours, B3; not reviewed by the
  theory division).  Implementation: contains the 60-digit enumerated value on all test
  instances; 40 000 adversarial certificates × 2 tiers without a miss.  One author wrote
  producer and checker; no independent implementation (requested: STRUCTBIO-REQ-0004).  The
  science division has read the statement, not the code.
- *Assumptions.*  The integer tables are the model; rational `β`; float tier: IEEE-754
  round-to-nearest products and sums in NumPy (F1–F3, stated and tested, not proved).
- *Closest prior art.*  toulbar2's `Z*ε` and the K\*/BBK\*/MARK\* family (floating-point
  ε-brackets of `Z`, no certificate); mini-bucket and tree-reweighted bounds; machine-checked
  weighted model counting (CPOG) with rational weights.
- *Distinction.*  An independently checkable certificate with controlled arithmetic and
  explicit abstention, run on a deposited structure.
- *Evidence for originality.*  Bounded searches (ours, Science's, Frontier's) found no
  published guaranteed two-sided population bounds with a checkable certificate on a real
  protein model.
- *Evidence against.*  Every bracket of `Z` brackets populations by division; enclosing each
  Boltzmann factor between rationals and counting twice with CPOG reaches the same statement
  by composition.  Class: at most a new combination of existing techniques.  The elimination
  and relaxation rules are textbook.
- *Validation.*  Synthetic: enumeration, two tiers.  Realistic: one structure (crambin, 26
  residues): `ln Z_w ∈ [−71.1574, −71.1499]` in 65 s; 26 population certificates in 13 min.
- *Limitations.*  Ends near crambin: for larger proteins no relaxation threshold makes the
  strongly coupled part tractable and the weak part small (R-13).  Population intervals have
  one width for all states (a tighter ratio bound is known, not implemented).  No baseline has
  been run.  The numbers describe a vacuum table with rigid ideal rotamers.
- *Before publication or use.*  An independent checker; the baselines (`Z*ε` at matched width,
  the CPOG composition, uncertified marginals against certified intervals); an energy model
  with a cutoff or screening that experts accept; states that are cells with their own free
  energy (the science division's construction) so that the number means something.

### B2. Quantified limits of certified side-chain computation on real structures

- *Contribution.*  Four measurements, each with its reading fixed beforehand: (i) a common
  hydrogen-placement protocol (random starts, 50 minimiser iterations) moves the certified
  minimum of a rotamer table by 12.8 to 24.6 kcal/mol between seeds (R-8); (ii) the basic
  linear relaxation is tight on all twelve development instances (R-12); (iii) the certified
  minimiser survives an entrywise table error of one unit (`10⁻⁶` kcal/mol) and not of
  `10⁻²`; rotamer *wells* are held by 3 to 5 kcal/mol in the median where *states* are held by
  tenths (R-10); (iv) the regime table: where a second-order bound could help, the exact part
  is intractable (R-13).
- *Artifacts.*  Experiments SB-X-005, -006, -007, -008 with drivers, rows and expectations
  under `experiments/structbio/`; `src/metricchain_sb/stability.py`.
- *Verification and review.*  (i) was asked for by the science division, which will review
  model v2; (iii) uses its construction, tested against the definition; (ii) answers a request
  of the Frontier and Complexity divisions.  All are single runs on six structures.
- *Prior art.*  (ii) Yanover, Schueler-Furman, Weiss (2008): a relaxation finds the optimum for
  about 85 % of a standard set.  (iii) the worst-case criterion of optimisation with interval
  data is classical; perturbation stability (Lang et al.).  (i) practitioners relax hydrogens
  properly; we know of no report of the size of the effect on rotamer tables (not searched).
- *Distinction and originality.*  None claimed for the methods; the numbers on certified
  instances are ours.  Evidence against originality: all four confirm what the literature or
  the reviewing divisions predicted.
- *Limitations.*  Six structures, four proteins, one energy model; (iii) is a sufficient
  condition per site.
- *Use.*  They say where *not* to spend effort (§C) and they are the honest context for B1, B3.

### B3. Certified minima and certified margins with an independent checker (C1, C1b)

- *Contribution.*  Format `structbio-mincert/1` (dual-bound leaves, branches, dead-end
  eliminations), producer, exact integer checker with the theory kernel's semantics, converter
  to the theory division's reference format; certified gaps for leaving a state or a well; a
  certificate of optimality under entrywise table error with a counterexample scenario.
- *Artifacts.*  `src/metricchain_sb/{model,mincert,mincheck,gmec,stability}.py`; experiments
  SB-X-001, -002, -003, -006; certificates under `experiments/structbio/gmec_dev/certs/`.
- *Verification and review.*  Rule semantics [V] (theory division, `verify_sound`);
  implementation attacked by Engineering (ENG-RES-0018), by our reviewer (STRUCTBIO-REV-0001)
  and exercised by Frontier (FRONTIER-REQ-0001): no false acceptance under normal use.
- *Prior art and distinction.*  DEE/A\*, ILP, toulbar2 (exact, no proof); pseudo-Boolean proof
  logging with a verified checker (VeriPB/CakePB), exact SCIP with VIPR (proofs on encodings).
  A native certificate for cost-function networks was not found in four bounded searches; its
  advantage over the encodings is unmeasured.  In substance the certificate is an exact LP
  dual with an elimination trace (Frontier N-5) — not new.
- *Validation.*  18 development instances (three model variants), all zero gap, all equal to
  toulbar2.  Synthetic frustrated instances: abstentions from 40 sites; Frontier's pilot on
  larger public instances: 4 certified, 6 abstained in 300 s, 17 to 326 times slower than
  toulbar2.
- *Limitations.*  The producer is slow (Python loops in the dual sweeps, quadratic memory in
  eliminations); the certified conformation is a rigid-rotamer minimum (MinDEE literature) of
  a crude model; the certificate has changed no answer.
- *Before use.*  The held-out evaluation designed with Frontier and Engineering; the
  proof-logging comparison; a fast producer (§D).

### B4. Machine-checked rule semantics for partition-function certificates

- *Contribution.*  19 Lean 4 theorems: conditioning; elimination of a site with any number of
  neighbours; monotone interval sums; thermal pruning (`Z(D∖r) ≤ Z(D) ≤ (1+e^{−βγ})·Z(D∖r)`);
  product-form relaxation of a pair; the certified exponential with rounding after every
  squaring.  `proofs/StructBio/FactorElimination.lean`, audit `AxiomAudit.lean` (standard
  axioms only), commit `53dca3b`.
- *Status.*  Checked by Lean; not reviewed by the theory division; not in its audited tree.
- *Originality.*  None as mathematics (elementary identities and inequalities).  Value: it
  extends the theory division's kernel (exact to two neighbours) to what a practical checker
  needs.  It verifies statements, not the Python that applies them.

## C. Negative results, rediscoveries, and what to abandon

1. **No answer changed, no speed gained.**  toulbar2: 6–27× faster on development structures,
   17–326× on Frontier's pilot, 600–1 700× on synthetic frustrated instances.
2. **The relaxation is tight on every development instance**; certificates are LP duals.
3. **Model v1 was a model with noise** (seed: 13–25 kcal/mol).  Retired; kept for reproduction.
4. **Rigid-rotamer minima are not continuous minima** — established since 2008 (MinDEE,
   iMinDEE); our prior art had omitted it (corrected after SCI-REV-0026).
5. **Entrywise robustness is negligible** on dense tables (`b ≤ 10⁻³` kcal/mol).
6. **C2 does not scale past crambin** under this model; a second-order bound would not change
   that (R-13; the Complexity division's CX-T36 says some regime is out of reach for any
   certificate format).
7. **Seven statements of ours were corrected** (RESULTS RC-1 … RC-7), nine software defects
   found by ourselves and nineteen by our adversarial reviewer, several by Engineering.
8. **Not started:** ensemble identification (C3), geometric observability (C4); residual-class
   certificates (C5) are blocked on constants nobody can certify for a real energy.

*Abandon or deprioritise:* competing with exact solvers on speed with our own search; the
certified minimum as a scientific product in itself; model v1; entrywise interval error
models on dense tables; whole-protein partition functions under a dense vacuum model.

## D. Practical opportunities (with the level each has reached)

| opportunity | mathematics | software | synthetic validation | realistic validation | experimental evidence |
|---|---|---|---|---|---|
| **A certified oracle for approximate inference on rotamer models** — how often does an uncertified marginal (belief propagation, sampling) fall outside a certified interval? | available | implemented (C2) | yes | one structure | none |
| **Checkable answers from fast exact solvers** — the solver finds the optimum, a dual-bound leaf certifies it, a small checker verifies it | available ([V] kernel) | implemented; the leaf alone suffices on 12 of 12 development instances (R-12) | yes | development only; larger instances fail with our slow producer | none |
| **Model diagnostics** — which residues a given energy table determines, and by what margin (well gaps; error scenarios) | available | implemented (C1b) | yes | five structures | none |

*Shortest credible path to useful performance* (the second row): keep the checker, replace the
producer.  Our dual sweeps are Python loops over pairs and our eliminations allocate
`k_i² k_j` arrays; a vectorised or compiled dual, started from the optimum that toulbar2
returns, or a dual extracted from the solver's own reparameterisation, would make
certification cost a small multiple of solving on instances where the relaxation is tight,
and say honestly where it is not.  Not done.

## E. Recommended next actions (three)

**E1. Frozen held-out evaluation of C1 and the null method.**  *Objective:* hypotheses
H3a–H3f of our plan and the Frontier division's H1/H2 on its sealed list (47 structures).
*Prerequisites:* this checkpoint after the checker repair; a freeze record (commit, models
`v2` and `v2-lib`, `SCALE_BITS = 20`, rotamer rule) — **not issued**; a standalone format
note for a second checker — **not written** (the specification is in the docstrings of
`mincert.py`, `mincheck.py`).  *Baselines:* toulbar2 on the identical instance; an
exact-rational dual of the relaxation; pseudo-Boolean proof logging with VeriPB/CakePB.
*Success / failure:* as written in `BENCHMARK_MASTER_PLAN.md` SB-BM-3 and FRONTIER-REQ-0001.
*Compute:* our estimate of 2026-11-26 was under 20 core-hours expected, 100 worst case, on
CPUs; at Engineering's stated rate of $0.0473 per core-hour that is of the order of $1–5 plus
memory; the proof-logging route is not estimated.  *Reasoning:* modest; mostly engineering —
Opus is adequate.  *Depends on:* Engineering (runs), Frontier (list, protocol), the owner (key).

**E2. C2 as a certified oracle on an accepted model.**  *Objective:* decide whether certified
populations within 0.05 are obtainable for proteins of 50–100 residues under a pairwise model
with a cutoff, and whether uncertified marginals leave certified intervals.  *Prerequisites:*
C2 as it stands.  *Missing:* the ratio-form population bound (specified in HANDOFF, a day of
work with tests); an independent checker; a sparser energy model; possibly a certified
second-order bound (the Complexity division's CX-T35 with a third-order remainder — open
mathematics).  *Baselines:* `Z*ε`, the CPOG composition, belief propagation.  *Success:* the
target width for at least 90 % of residues on at least three of the development proteins
within a stated budget; *failure:* the exact part needs more than `10⁵` leaves at `3·10⁶`
entries.  *Compute:* crambin cost 13 core-minutes for all populations; larger cases not
estimable before the model is chosen.  *Reasoning:* the mathematics needs the strongest
model; the engineering does not.  *Depends on:* Complexity, Theory, Engineering.

**E3. What the certified number means: discretisation.**  *Objective:* benchmark SB-BM-7 (the
rigid minimum against the per-well continuous minimum of the same energy) and states as cells
with their own free energy.  *Prerequisites:* the molecular layer; the science division's
construction (its item 101 (b)); the theory division's voxel enclosures.  *Missing:* interval
bounds of our energy over a cell.  *Success:* a certified upper end within a stated distance
of the table's value per torsion; *failure:* cells too many to tabulate.  *Cost:* not
estimable.  *Depends on:* Science, Theory.  Needs the strongest model for the design.

## F. Publication readiness

No standalone publishable result exists.  The nearest candidate is a methods note on
independently checkable certificates for rotamer partition functions and populations (B1).
Before an external expert it would need: baselines actually run; an independent checker; an
accepted energy model; held-out structures; and an honest novelty statement — on present
evidence "a new combination of existing techniques at most".  The Lean file is formal
verification of elementary statements and is not evidence of novelty.  The seed measurement
(B2 (i)) is a cautionary technical observation, not a paper.

## State at the halt

- **Evaluation integrity.**  No held-out structure has been looked at or run.  The Frontier
  division's sealed list (FRONTIER-FRZ-0002) has not been opened by us; we hold no key.  No
  release is frozen for held-out evaluation; the sequence the Frontier division proposes
  (freeze by us → key from the owner to Engineering → run) is acceptable to us.  The ten
  public instances of the Frontier pilot are development material.
- **Open requests.**  STRUCTBIO-REQ-0001 (Engineering: independent verification of C1) and
  -REQ-0004 (C2) are unanswered; -REQ-0002 was answered by SCI-REV-0026 (our response:
  STRUCTBIO-RES-0003); -REQ-0003 was answered in part by COMPLEXITY-RES-0010.
- **Processes.**  See the final section of `docs/structural_biology/HANDOFF.md` for what was
  running and what was stopped at the moment of the final commit.
