# Assessment protocols

*Frontier Benchmarking division.  Version 1.1, 2026-11-27 (version 1 of 2026-11-26 amended in §6 after criticism from the science and complexity divisions; no protocol had been frozen).  A protocol here is a design until it
is frozen (hash and time-stamp, `PREDICTION_FREEZE_REGISTER.md`) and executed; substantial
execution belongs to the engineering division and is requested through the mailbox.  These
protocols complement, and do not replace, engineering's stages A–F
(`BENCHMARK_MASTER_PLAN.md` on its branch) and science's review protocol
(`SOFTWARE_EVALUATION_PROTOCOL.md` on its branch): they add named external baselines, public
reference data, contamination control and a freeze discipline.*

## 1. The design standard (every protocol answers all seventeen)

| # | field | what counts as an answer |
|---|---|---|
| 1 | scientific question | one sentence a practitioner outside the programme would ask |
| 2 | mathematical claim | the statement tested, with division, commit, label ([V], [P], …) and assumptions |
| 3 | computational capability | the software, at a pinned commit, and the exact entry point |
| 4 | reference evidence | what the answer is compared with, and how good that evidence is (resolution, error model, who measured or computed it) |
| 5 | scope | why this is inside the charter; where the boundary lies |
| 6 | data provenance | source, retrieval time, checksum, licence (`DATA_PROVENANCE.md`) |
| 7 | inclusion and exclusion | rule fixed before results; every exclusion listed with its reason |
| 8 | comparison methodology | same model, same information, same budget; what "same" means here |
| 9 | baseline justification | the strongest relevant contemporary methods, exact versions, run by their published recipes (`STATE_OF_THE_ART.md`); why each is fair |
| 10 | statistical analysis | primary metric, paired design, interval estimate, multiplicity, fixed in advance (§2) |
| 11 | computational accounting | everything counted: precomputation, table generation, certificate production **and** checking, failures, hardware |
| 12 | failure criteria | outcomes that refute the claim or the interpretation, written before the run |
| 13 | success criteria | outcomes that support it, and on which dimension (D1–D10) |
| 14 | reproducibility | commits, commands, seeds, environment pins, artifacts with checksums |
| 15 | uncertainty treatment | which numbers are certified, which estimated with what confidence statement, which neither |
| 16 | contamination risks | what the methods compared were trained or tuned on, relative to the test data (`CONTAMINATION_AUDIT.md`) |
| 17 | interpretation limits | what a success would **not** establish |

**Standing rules.**  Exploratory, development, held-out and replication results are kept
apart and labelled; a development result is never reported as validation.  No instance is
dropped after results are seen; "too easy" and "too hard" instances stay in the tables.
Missing predictions, abstentions, time-outs, crashes and rejected certificates are results
and are reported with the same prominence as successes.  The ten dimensions are reported
separately: a certificate is not accuracy, speed is not accuracy, one success is not a proof.

## 2. Statistical standards

* **One primary metric per question**, named in advance; everything else is secondary and
  labelled so.
* **Paired designs.**  Methods are compared on the same instances; differences are summarised
  with a paired bootstrap interval (10,000 resamples of instances, seed recorded) and an exact
  sign or Wilcoxon signed-rank test; clusters (chains of one protein, variants of one
  target) are resampled as clusters.
* **Equivalence, not only difference.**  Where the honest expectation is "no difference"
  (FB-P-02), an equivalence margin is fixed in advance and the result is one of: better
  beyond the margin, equivalent within it, worse beyond it, inconclusive.
* **Censoring.**  Solver comparisons report, per method: solved / proved / certified /
  certificate checked within the budget, as counts, and performance profiles
  (Dolan–Moré) over *all* instances with unsolved instances at infinity — never means over
  the solved subset.
* **Guarantees are tested as guarantees.**  A certified interval must contain the truth in
  every case where its hypotheses hold: one miss is a defect, not a frequency.  Statistical
  intervals of baselines are scored by observed coverage against nominal.
* **Abstention is scored.**  For methods that may decline (D10): risk–coverage curves, the
  rate of confident error, and — on planted non-identifiable instances — whether ambiguity is
  reported.
* **Multiplicity.**  The number of comparisons is stated; no result is called significant on
  an uncorrected secondary metric.

## 3. Freezing, held-out material and custody

1. **What is frozen, and when.**  The protocol, the method's commit and configuration, and
   then the predictions — each before the next stage sees them.  Tooling:
   `src/metricchain_fb/`.
2. **Held-out sets on a shared repository.**  Every branch is readable by every division, so a
   held-out list in clear text is disclosed.  Three admissible constructions, in order of
   preference: (a) *prospective*: a public selection rule applied to structures released
   after the method was frozen (nothing to hide); (b) *committed*: the list is fixed now, only
   a salted commitment is published (`commitment.py`), the list and salt are held by the
   research owner or by engineering and revealed after the method freeze; (c) *declared*:
   the list is public and the developers declare in the freeze manifest that it was not used
   — the weakest form, labelled as such.
3. **Development feedback** to the software division uses only development instances.  No
   held-out outcome is reported back before the corresponding method freeze.
4. **After the reference is seen**, any change to a method or a prediction is a new,
   retrospective experiment.

## 4. Protocols

Status key: **P** pilot run by us (exploratory, local); **R** ready to request from
engineering; **G** gated on a prerequisite owned by another division; **D** design only.

### FB-P-01 — What does a checkable certificate of optimality cost, against the solvers people use?  (status P → R)

| field | content |
|---|---|
| 1 question | For the discrete energy minimisation a side-chain placement reduces to, what is the price — in time, in file size, in trusted code — of an optimum that someone else can check, compared with the optimum a state-of-the-art solver merely claims? |
| 2 claim | Theory kernel soundness `verify_sound` [V]: an accepted certificate proves a lower bound on the minimum of the published integer model.  Claim under test is *not* soundness (engineering's BM-2/BM-7 own that) but **value**: that such certificates can be produced and checked on instances of real size at a cost comparable to solving (science's hypothesis H1), and more cheaply than the certified alternative that already exists (H2) |
| 3 capability | structural biology `metricchain_sb.gmec.certify_gmec` + `mincheck` at a pinned commit (pilot: `720e0ec`); engineering's `leafcert` checker and its producer when committed |
| 4 reference | the optimum itself, cross-validated between independent exact methods; on small instances exhaustive enumeration |
| 5 scope | mathematical optimisation over **fixed-sequence** side-chain instances and synthetic instances.  Design instances (variable residue identity) are excluded by rule: any instance with a domain larger than the largest single-residue rotamer count of its library |
| 6 provenance | EvalGM repository (INRAE), category MRF/ProteinFolding, from the 2011 Probabilistic Inference Challenge; licence not stated → instances referenced by URL and SHA-256, not copied |
| 7 inclusion | pilot/development: the ten `pdb*` instances (337–1,972 variables, domains ≤ 81).  Excluded: the eleven instances of the same category with domains up to 350–503 (consistent with design instances).  Held-out: instances the software division has not seen — the remaining Yanover side-chain set if it can be located, and freshly generated fixed-sequence instances once a molecular layer exists (construction (b) of §3) |
| 8 comparison | identical integer tables for every method; identical wall-clock budget on one core; solver defaults plus each tool's published recommended settings, both reported |
| 9 baselines | **toulbar2 1.4.x** (claims optimality; no proof output found) — the practitioner's exact solver; **exact-rational dual of the local-polytope linear relaxation** — because prior work reports the relaxation tight on most fixed-sequence instances, this is the cheapest conceivable certificate and the bar a native format must clear; **pseudo-Boolean encoding + proof-logging solver + VeriPB + CakePB** — the certified state of the art with a formally verified checker; **integer programming** (HiGHS / SCIP, with exact SCIP + VIPR where available); optional: OSPREY rigid-rotamer DEE/A\*, a simulated-annealing packer as the uncertified heuristic reference |
| 10 statistics | counts solved / certified / checked within budget; performance profiles; paired ratios (certified ÷ uncertified time; check ÷ solve time) with bootstrap intervals; certificate bytes; **fraction of instances closed without branching** reported separately, and all metrics stratified by it |
| 11 accounting | table loading, production, serialisation, checking, each timed; peak memory; failures of any stage; hardware and versions |
| 12 failure criteria | (i) any accepted certificate whose bound exceeds an independently established optimum — a soundness defect, stop and report; (ii) H1 fails if the certified route completes on fewer than half of the instances the uncertified solver completes within the same budget; (iii) H2 fails if the pseudo-Boolean/VeriPB route is within a factor 3 of the native route in total time and size on all instances (science's criterion, SCI-REV-0006); (iv) the "native certificate" has no advantage over the linear-relaxation dual on instances closed without branching — expected, and to be stated, not hidden |
| 13 success criteria | D9: a certificate checked by an independent checker on every instance the uncertified solver solves; D3: total certified cost within one order of magnitude of uncertified solving; D8: bit-identical certificates across runs |
| 14 reproducibility | driver `experiments/frontier/exploratory_gmec/run_scp_exploratory.py`; instance checksums; environment pins |
| 15 uncertainty | none statistical in the optimum; timing variability by repetition |
| 16 contamination | the pilot instances are now *seen* by this division and, once reported, by the software division: they are **development** instances from here on |
| 17 limits | says nothing about proteins: the tables are 2011 energy tables rounded to integers.  An optimum of a table is not a structure; exactness has repeatedly been found not to improve agreement with experiment (FB-P-02) |

Pilot outcome: `RESULTS.md` §1 and `NEGATIVE_RESULTS.md`.

### FB-P-02 — Does a certified optimum place side chains more accurately than established packers?  (status G)

| field | content |
|---|---|
| 1 question | On experimental backbones, and on predicted ones, are the side chains of the certified minimum-energy conformation closer to experiment than those of established packers? |
| 2 claim | none of the theorems claims this; the protocol exists because a certified optimum invites that reading |
| 3 capability | **does not exist**: needs a molecular layer (structure input, rotamer library, energy tables) and the bound on the rounding from real energies to integers (assumption A9) |
| 4 reference | crystal structures at ≤ 1.5 Å, side chains with full occupancy and well-ordered density; the experimental uncertainty of a χ angle is part of the analysis |
| 5 scope | fixed sequences, public structures, retrospective |
| 7 inclusion | construction (a) of §3: PDB entries released after the latest training cut-off of any baseline (the ML packers found so far declare cut-offs up to 2023-07-28) **and** after the software's own freeze; monomeric chains of 50–500 residues; non-redundant at 30 % identity against every baseline's training set.  The three 1.1–1.3 Å CASP17 amidase references (released 2026-09-16) are candidate members |
| 8 comparison | every packer receives the same backbone; the certified route and a heuristic search are also compared **on the same energy function**, which is the only comparison that isolates exactness |
| 9 baselines | rotamer-library methods SCWRL4, FASPR, a Rosetta-type annealing packer; learned packers (FlowPacker, PIPPack, AttnPacker, DiffPack with the leakage caveat reported by a competitor); on predicted backbones, the predictor's own side chains |
| 10 statistics | primary: χ1+χ2 recovery within 20° over buried residues; secondary: all-χ recovery, heavy-atom RMSD, clash count, surface residues.  Paired bootstrap over chains.  **Equivalence margin fixed now: ±0.5 percentage points** between certified and heuristic optimum of the same energy |
| 12–13 pre-declared expectations | **E1** certified vs heuristic optimum of the same energy: equivalent within the margin (published: < 0.1 % gain).  **E2** learned packers ahead of any rotamer-library energy on native backbones.  **E3** on predicted backbones no repacking improves on the predictor's own side chains.  A gain beyond the margin for the certified route refutes E1 and would be a positive finding on D1; equivalence confirms that the value of certification lies on D8/D9 |
| 16 contamination | learned packers' training cut-offs and redundancy filters; held-out structures must post-date them |
| 17 limits | a result is relative to one energy function and one rotamer discretisation; science's four-line budget applies in full |

### FB-P-04 — On data that cannot decide, who says so?  Certified identification against reweighting tools  (status R for the planted controls)

| field | content |
|---|---|
| 1 question | Given averaged data on an ensemble drawn from a finite candidate pool, do current ensemble-refinement tools report when the data do not determine the answer — and are certified intervals wider, narrower or simply more honest than what those tools report? |
| 2 claim | ensemble division E1(a) (identification criterion; "if" direction [V]), F1–F3 (exact dual intervals, [P]); valid for the stated pool and for data linear in the ensemble |
| 3 capability | the division's linear programmes and its 18 control instances (`controls_v1.json` at `2d2054d`), "verified by their generator only" |
| 4 reference | **planted truth**: the generating ensemble is known exactly; identifiability of each instance is known by construction |
| 5 scope | synthetic controls; no molecule |
| 7 inclusion | all 18 controls plus the scale families with exact ground truth (random conformers on the cube, n ≤ 22); fresh instances drawn from published seeds as the held-out stage |
| 9 baselines | maximum-entropy / Bayesian reweighting as practised (a BME-type tool; a BioEn-type tool), non-negative least squares and minimal-ensemble selection, a maximum-occurrence analysis; each with its recommended regularisation choice and with its own uncertainty output |
| 10 statistics | primary: on planted **non-identified** instances, the fraction on which a method reports ambiguity rather than a single ensemble (D10).  Secondary: coverage of the planted value by each reported interval (certified intervals: must be 100 %); interval width relative to the a-priori range; total-variation error of point estimates on identified instances |
| 12 failure criteria | for the certified route: any miss of the planted truth inside the hypotheses (defect); intervals within 10 % of the a-priori range on all identified instances (uninformative; science's H5 criterion).  For the interpretation: if baselines' reported uncertainties cover the truth as often at smaller width on every instance including the deception instances, the certified route has no advantage (science's H7) |
| 16 contamination | none for synthetic data; the baselines' defaults were tuned by their authors on real data, not on these controls |
| 17 limits | a verdict holds for the stated pool ("adding one configuration can turn IDENTIFIED into NOT IDENTIFIED"); nothing is said about any instrument until a forward model with a stated error exists |

### The remaining protocols, in brief (each is expanded to the seventeen fields before it is frozen)

| id | question | claim tested (owner) | reference | strongest baselines | primary metric · pre-declared failure | status · prerequisite |
|---|---|---|---|---|---|---|
| FB-P-03 | Are certified two-sided bounds on ln Z worth their cost against established estimators? | partition kernel [V]; science's sandwich certificate | exact ln Z (transfer matrix, enumeration) on small instances; certified counters on larger | a deterministic ε-approximation of the toulbar2 lineage; K\*-type bounds; exact weighted model counting with a verified proof checker (CPOG); annealed importance sampling and thermodynamic integration with their confidence intervals | coverage of the truth (certified: 100 %; samplers: observed vs nominal) and width against time · a certified interval that misses; or samplers reaching the same width with honest coverage at a tenth of the cost | **G** — the certificate must exist as a file (engineering Q-08) |
| FB-P-05 | When does demixing of chain ensembles from averaged distances break under noise? | geometry DEMIX, Theorems B/C/I′ (no noise guarantee) | planted K-state mixtures | non-negative least squares over a planted-plus-decoy pool; classical scaling | breakdown noise level for exact-K recovery; frequency of a wrong confident answer · recovery lost below the accuracy of any conceivable measurement | **R** as a noise sweep; guarantee needs a perturbation bound |
| FB-P-06 | What could the CASP17 ensemble data decide? (retrospective) | ensemble F1–F3; geometry demixing limits | the experimental data of the "hidden states", SAXS/DEER and FRET targets, when released | the official assessment's own ranking | stability of the official ranking over the set of submitted ensembles that fit the data within error · — | **G** — forward models with stated error; data release |
| FB-P-07 | Are the stability constants of local-distance reconstruction usable on real traces? | geometry Theorem L/L⁺ | deposited Cα traces; empirical error of established distance-geometry solvers under the same noise | Branch-and-Prune and SDP-based realisation codes | certified range in ångström per trace · expected outcome is negative (its authors: ≤ 10⁻⁵ Å) — the test is whether any class of structures escapes | **R** (small, local) |
| FB-P-08 | Does the all-orderings partition-function algorithm agree with established nucleic-acid thermodynamics software? | complexity CX-T12, CX-T30 | exact agreement on small fixed systems with matched energy conventions | a Dirks-type multi-strand implementation | exact equality of partition function, minimum free energy and symmetry corrections · any disagreement not traced to a convention | **G** — conventions aligned by the authors |
| FB-P-09 | Outside its hypotheses, does the system fail safe? | every kernel; theory's own false-certificate example under unbounded influence | planted violations: envelope constants too small, inconsistent anchors, tables rounded the wrong way, correlated references where independence is assumed | — (a property test, not a race) | fraction of planted violations that are rejected or abstained on · any violation certified | **R** as a specification to engineering |
| FB-P-10 | Do our own scoring tools reproduce the community's numbers? | none of MetricChain's — the instrument | official CASP17 numbers after 2026-11-29; reference implementations | — | agreement of rank and value, thresholds fixed in the freeze · disagreement beyond them | in progress (ours) |
| FB-P-11 | Does any future electrostatics or pKa layer beat the null model and analytic cases? | none yet | Born and Kirkwood spheres (analytic); measured pKa shifts with the water-pKa null model | finite-difference and boundary-element Poisson–Boltzmann codes; empirical pKa predictors | convergence order on analytic cases; error against the null model · not beating the null model | **D** — nothing to evaluate yet |

## 5. What is deliberately not proposed

* Any evaluation whose output is a designed sequence, an optimised binder or ligand, or a
  ranking of molecules for a target.
* Any comparison in which MetricChain's method is given information its baseline is not.
* Any "leaderboard" entry: a single number across dimensions is refused by rule.
* Running the 2011 design instances "as pure optimisation": their solutions are designed
  sequences, and the same solver questions are answered by fixed-sequence and synthetic
  instances.

## 6. Amendments of version 1.1 (2026-11-27), and where they come from

Criticism received within two hours of version 1 — SCI-RES-0041 (science), COMPLEXITY-RES-0010
(complexity), GEOMETRY-MSG-0010 (geometry) — changes four things.  Where an amendment
contradicts a table above, the amendment holds; the tables are kept as first written so that
the change is visible.

**FB-P-01**

1. *Strata are assigned by a rule fixed in advance and computed without the software under
   test* (science: "'the producer needed no branching' is an outcome"; complexity: closure
   without branching is exactly tightness of the basic linear relaxation after the
   eliminations, a polynomial-time instance property).  **Definition:** an instance is in the
   *tight* stratum iff the optimum of the local-polytope relaxation, computed in exact rational
   arithmetic by the evaluator, equals the optimum established by the uncertified exact
   solver; otherwise *not tight*; if no optimum is established within the budget, *unknown*.
   Field 10's "fraction of instances closed without branching" is replaced by this.  Our
   pilot did not compute it and reports branch-node counts only as an observation.
2. *The sizes of the strata are reported per class of instance* (public fixed-sequence,
   structures from the sealed list, synthetic), because a conclusion about the not-tight
   stratum may be a conclusion about a generator.
3. *H2 is two hypotheses, with expectations written now.*  **Tight:** a format comparison —
   native certificate against an exact-rational dual and against the same eliminations logged
   as steps of a pseudo-Boolean proof; expectation: no large factor either way.  **Not
   tight:** a tree of branchings over relaxation bounds against cutting planes; expectation
   (science's, adopted): the external proof system is the stronger one and **H2 fails**.
4. *H1's two words are defined before the run.*  "Solving" = toulbar2 1.4.x, the better of its
   default and its authors' published settings, on one core.  "Comparable" = the certified
   route completes on at least 90 % of the instances that solver completes within the same
   budget, with total time (production plus checking) within a factor 10 on at least half of
   them.  By this definition the pilot's outcome at 300 s is negative (4 of 7; factors 17–326).

**FB-P-02**

5. *The heuristic is named and the expectation carries its interval* (science, caution (a):
   with a hard repulsive wall and idealised rotamers "the direction is not obvious").
   **Heuristic:** Metropolis simulated annealing on the identical tables, 100 independent
   restarts of 10⁶ single-residue moves each with a geometric temperature schedule from 10 to
   0.05 kcal/mol, best energy kept; seeds 0–99.  **Expectation E1:** the difference in the
   primary metric between the certified optimum and that heuristic lies in [−0.5, +0.5]
   percentage points; a difference outside it in either direction is reported as a finding.
6. *Auditability gets its own outcome variable* (science, caution (b): "no difference" would
   show that certification buys no accuracy and would not test auditability).  **Variable A:**
   the number of instance–method pairs in which an uncertified method returned a value that
   was not a proved optimum without saying so, or two uncertified methods disagreed, and the
   certified route either proved the optimum or abstained.  In the pilot A = 3 of 10 for
   toulbar2's default interface (time-limited values returned without a flag), with the
   certified route abstaining in all three; A is reported whether or not it is favourable.

**FB-P-06**

7. *The prerequisite is further away than version 1 implied.*  The geometry division states
   (GEOMETRY-MSG-0010) that it has an identifiability statement for one forward model only —
   exact averaged squared distances among labelled sites — and that for sparse labels it is
   negative; it asks not to be counted on for the CASP17 ensemble data.  FB-P-06 stays
   **gated**, with the ensemble division's linear and one-unknown-factor results (E1, E23) as
   the only candidates and no forward model with a stated error on any branch.

**All protocols**

8. *Literature rows are upgraded where another division verified them at a higher read
   level.*  The statement that the exact optimum of a standard energy improves side-chain
   accuracy by less than 0.1 % (ours: search snippet) is confirmed by science at the level of
   the abstract through its PubMed record (Yanover, Schueler-Furman and Weiss, J. Comput.
   Biol. 15 (2008) 899), with the further figures 72 % → 78 % for learned weights and 82.6 %
   with an extended library.
