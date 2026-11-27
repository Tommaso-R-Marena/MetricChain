# Consolidation assessment — Scientific Discovery, Translation & Independent Validation Division

*Branch `research/scientific-translation`.  Written 2026-11-27 under the research owner's directive on controlled
consolidation (recorded verbatim as D-5 in `docs/science/OWNER_DIRECTIVES.md`).  Status of every statement below:
internal work of AI agents — paper proofs, replications, enumerations — **none of it externally reviewed, none of
it compared with an experiment**.  "Not found" is the strongest originality statement any search of ours supports.
Where this document and an earlier file of the branch disagree, the later linked correction holds; the handoff is
`docs/science/RESEARCH_SYNTHESIS.md`, the state table `docs/collaboration/status/science.md`.*

---

## A. Executive assessment

The division existed for about two days (first commit 25 November, 74 checkpoints, about 180 commits, 29 referee
workstreams — one of them stopped before it began — and about twenty prior-art, measurement and formalisation
workstreams, all AI agents).  It produced three
kinds of output, of unequal value.

1. **Independent validation — the output that changed most.**  Thirty reviews with replication of the other
   divisions' statements (SCI-REV-0001 … -0030).  No headline theorem of the theory division was found false,
   and its central cost result was re-derived from scratch with identical constants.  But reviews of ours
   caused: a published conclusion of the engineering division withdrawn (SCI-REV-0018); three sentences of the
   theory division's nesting section replaced and a false certificate mechanism identified (SCI-REV-0027,
   accepted in full); a random seed inside the Structural Biology division's energy model exposed, which their
   own measurement then found material on all six structures (SCI-REV-0026); the Geometry division's stability
   theorem shown unusable as an error bar (SCI-REV-0028).  The same standard applied to ourselves produced about
   a dozen linked corrections, the last one an hour before this document (SCI-REV-0029).
2. **Own mathematics.**  (a) A certified two-sided bracket for the free energy of a side-chain ensemble under a
   real force field *with a many-body implicit-solvent term*, to `10⁻²`–`10⁻⁴` nats at up to `5·10¹⁷` states,
   now with a file format and a checker (§B1).  (b) Theorems on what averaged and thermodynamic data are worth
   to a certified computation, with machine-checked cores (§B2).  (c) Smaller results: a closed-form robust
   range for monotone macrostates, cut certificates for barriers, a bracket for continuous site variables.
3. **Measurement of what the mathematics is about** (§B3): which class real residuals live in, what certified
   reweighting costs on real rotamer instances, how often uncertified error bars fail, what a rotamer
   discretisation costs.

**The critical bottom line, in four sentences.**
* **Nothing here is evidence about a molecule.**  Every "real" instance is a capped peptide of at most thirty
  residues on an idealised backbone, in one fixed-charge force field with an implicit solvent, in rotamer
  variables.
* **The guarantees are two to four orders of magnitude more precise than the model they are about.**  The
  certified brackets are `10⁻²` nats wide or better; the rigid-rotamer discretisation alone moves a free energy by
  0.6 to 3.2 nats *per torsion* in our own measurement, refits within one force-field lineage move one-residue
  terms by 0.6–2.6 kcal/mol, and the generalized-Born model is off by more than `2 kT` in individual pair terms
  against the Poisson equation (literature, abstract level).  A certificate removes the *computational* line of
  an error budget; in every budget we have looked at it is the smallest line.
* **Originality is narrow.**  Several statements we sent out as ours were in print (§C).  The claims that may
  survive a hostile expert are the certified tail of the solvent term (§B1) and the "what data are worth"
  theorems on the cube (§B2) — both "not found" in bounded searches, neither searched at full-text depth by
  anyone with library access.
* **What the programme can credibly offer is auditability, not accuracy**: a number, with a file that a third
  party can check, saying what a stated model implies — and, through the reviews, a record of which of its own
  claims survived an adversary.

## B. Strongest contributions, ranked

Ranking by originality × correctness × significance × utility.  B4 is not mathematics; it is ranked where its
consequence puts it.

### B1. Certified two-sided free-energy brackets for a force field with a many-body solvent term, and a checkable certificate

* **Contribution.**  For `E = f + g` on a product of rotamer states — `f` the pairwise vacuum part of Amber
  ff14SB, `g` the GBn2 polarisation energy, which is not pairwise — evaluate `g` on a Hamming ball about an
  anchor state, bound the remainder of the anchored expansion term by term *for every order* with interval
  enclosures of the derivatives of the Born-radius rescaling and kernel, sum those bounds over all `m`-subsets in
  closed form, and assemble a floor `m₋ ≤ E` and a ceiling `m₊ ≥ E` that are banded pairwise models, so that
  `ln Z(m₊) ≤ ln Z(E) ≤ ln Z(m₋)` by transfer matrix, with no sampling.  Refinements: pair shares of the
  remainder; penalties resolved by rotamer state (the charged case); first- and second-order recovery of the
  slack of the band.  Results: Ace-(Val)₂₀-NMe, `3.5·10⁹` states, `[518.2552, 518.2715]`; Ace-(Leu)₃₀-NMe,
  `[866.910485, 866.921008]` (0.0105 nats); Ace-(Lys)₂₀-NMe on a helix, `5.5·10¹⁷` states,
  `[800.5150660, 800.5154710]`; Ace-(Lys)₁₂-NMe `[517.1284375, 517.1286523]`.
* **Artifacts.**  `docs/science/workstreams/P3_REPORT.md` (Proposition 1, Lemma 2, Theorem 3, Proposition 4,
  Theorem 5), `P6_REPORT.md`, `P8_REPORT.md`, `P9_REPORT.md`; `INFERENCE_LIMITS_ADDENDA.md` A17 (10), (13)–(24)
  (Propositions A17.19, A17.23); `experiments/science/ws_P3`, `ws_P6`, `ws_P8`, `ws_P9`, `pi_inference/`;
  **certificate:** `docs/science/SANDWICH_CERTIFICATE_FORMAT.md`, `experiments/science/sandwich_cert/`.  Commits:
  `a841cb4` (P3), `c1b710c` (P6), `ddd4be3` (P8), `90abf0e` (P9), `0930440` (A17 (20)), `59e88bc` (second-order
  recovery), `100472f` (certificate, Stage 1).  Messages SCI-MSG-0020, -0025, -0027, -0028, -0036.
* **Verification and review.**  Paper proofs with stated floating-point allowances.  No violation at any state
  of any enumerated instance (5.5 million state checks in P3 alone); a second driver reproduces P9 digit for
  digit; an independent chain-model estimate (`518.2626 ± 0.0001`) lies inside.  Internal referees: parts (19)–(20)
  (R19), (21)–(22) (R24), (25)–(26) (R28).  **Unrefereed: parts (13)–(18) — the referee launched for them was
  terminated by a platform safeguard and its work was not done by anyone — and parts (23)–(24), except inequality
  (c) of Proposition A17.23, which the theory division machine-checked.**  Nothing else is machine-checked.
  Stage 1 of the certificate: reference checker with 85 controls (planted truth; 71 planted faults rejected).
* **Essential assumptions.**  Fixed backbone; rigid rotamers; the stated force field and solvent model; an
  evaluation tolerance of `10⁻⁷` kcal/mol per energy value (measured `1.8·10⁻¹²`, not proved); `mpmath` interval
  arithmetic; and, for a Stage 1 file, three data assumptions (G1)–(G3) that are **not checked** — the step-A
  sums, the bracketing of the evaluated part, the tolerance.
* **Closest prior art.**  Provable partition-function algorithms of computational protein design (K\*, BBK\*,
  MARK\*; review: Hallen and Donald, *Commun. ACM* 2019) — guarantees relative to a *given* pairwise energy;
  LUTE (Hallen, Jou, Donald 2017) — a fitted local expansion of a non-pairwise energy, without a certified
  error; pairwise approximations of generalized Born (Simonson, Archontis, Gaillard and co-workers);
  truncation-error bounds for anchored decompositions (Rahman, *Math. Comp.* 2014, expected error).  All at
  abstract level.
* **Distinction.**  A *rigorous sup-norm bound*, for a specific widely used solvent model, on what lies beyond the
  evaluated low orders, in closed form over all subsets, turned into a two-sided bracket of `ln Z` — and a
  certificate a third party can check.
* **Evidence for originality.**  Not found in six targeted queries (P3 §4) nor in the searches of workstreams
  P2 and A3: (a) a rigorous bound on the non-pairwise part of a generalized-Born energy in rotamer variables;
  (b) interval enclosures of the derivatives used; (c) a certified bracket of a partition function whose energy
  contains such a term.
* **Evidence against.**  Every ingredient is standard (anchored expansions, Faà di Bruno, Bell polynomials,
  interval differentiation, transfer matrices); the remainder inequality with class constants is the theory
  division's Theorem 11.18; the search was six queries at abstract level in a literature none of us surveyed;
  the provable-design community has a decade of partition-function bounds for pairwise energies and may regard
  the step as an exercise.  "Not found" is not "new".
* **Limitations.**  §A: the bracket is far finer than the model.  Homopeptides and one mixed sequence, idealised
  backbones, no buried environment.  Compact charged ensembles need state-resolved tables, and a theorem of ours
  (SCI-MSG-0024) shows no bound blind to the signs of the charges can see the cancellation.  Cost grows as
  `n^{m−1}` energy evaluations.  The software is research scripts with untracked caches.
* **Before publication or use.**  Stage 2 of the certificate (open problem E5); a referee for parts (13)–(18),
  (23)–(24); a full-text prior-art search by someone who knows the protein-design literature; one instance on a
  real protein backbone; a head-to-head with a published provable method on the same pairwise approximation.

### B2. What averaged and thermodynamic data are worth to a certified free-energy computation

* **Contribution.**  On the envelope class of the Hamming cube: exact knowledge of all marginals of bounded
  order changes neither the adaptive nor the non-adaptive exponent of certified estimation of `ln Z`; with error
  bars, correlations of *every* order change nothing (Theorem 4-τ); marginals of order `αn` do lower it
  (Theorem 4‴); uniform local data are compatible with the whole a-priori entropy interval (Theorem 2); a
  mean-energy datum fixes `ln Z` to within `n·KL(σ_u‖½)/2` and removes an exponential cost in a named window of
  accuracies, below which a "plateau twin" bounds what it can do (addendum A16; Lemma A16.5, an isoperimetric
  inequality with an energy constraint); with a field, one-body data change neither exponent (a compensation
  lemma).  Also: data certify a *lower* bound on model error (Theorem 8), with exact identified sets on lattice
  chains.
* **Artifacts.**  `docs/science/INFERENCE_LIMITS.md` (version 3; Lemma 1, Theorems 2–8, Propositions 5b, 6, 9);
  addenda A12, A16; Lean: `experiments/science/ws_L1/*.lean`, `ws_L2/*.lean`, `ws_L3/*.lean`
  (`MarginalOracle`, `IdentifiedSets`, `BasinBound`, `Pinsker`, `Compensation`, `A16Rearrangement`, …).
  Commits `2f2004e`, `11110b5`, `8aa649b`, `44f00cd`, `2f52fbf`.  Messages SCI-MSG-0008, -0011, -0012, -0016,
  SCI-RES-0006.
* **Verification and review.**  Short cores machine-checked (Lemma 1; Theorem 3 in Markov form; Theorems 4, 4′,
  5, 7 in Pinsker form; Propositions 6, 9; the algebraic core of Lemma A16.5); adversarial internal referees R3
  and R8 (one over-claim, "exact cost", corrected by SCI-MSG-0016); the non-adaptive half proved independently
  three times (ours, a referee's, the theory division's Proposition 11.104).  Open: Theorem 2 and the sharp
  Theorem 7 in Lean; Conjecture A16.4.
* **Essential assumptions.**  The uniform cube with zero known part (the field case excepted); worst case over an
  envelope class; exact or interval data.
* **Closest prior art.**  Orthogonal arrays and `k`-wise independence (the mechanism of Lemma 1); the
  identified-set and moment-problem literature (the framework of §§8–9 is known under four names); the theory
  division's own lower bounds.
* **Distinction.**  The two-oracle model — energy evaluations *and* averaged data — and exact exponents in it.
* **Evidence for originality.**  Workstreams A1, A2: the oracle-invariance statements not found.
* **Evidence against.**  The mechanism is classical coding theory; the identified-set framework and its
  divergence-ball versions are in print; the result is negative and about a worst case — a referee may call it
  expected.
* **Limitations.**  Worst case, cube, zero known part.  It does **not** say that data are useless on real
  instances — instance-wise the oracle helps, and nothing here has touched a measurement.
* **Before publication.**  Joint with the theory division's Proposition 11.104; a full-text search; the two
  open Lean items; an honest title ("in the worst case over a first-order class").

### B3. Measurements of what the programme's objects cost on a real force field

* **Contribution.**  (i) *Which class a real residual lives in:* same-lineage force-field differences are
  exactly additive or residue-local; a solvent term in torsion variables has class constants `βc = 12–53`,
  growing with length — near pair-additive in root-mean-square (0.2–0.9 `kT`), not in sup norm (2–16 `kT`); in
  rotamer variables it is pairwise to 0.003–0.2 kcal/mol for neutral side chains.  (ii) *Prices of certified
  reweighting on 74 enumerated instances:* the sup norm is the wrong coordinate (`D₂ ≤ 1.3·10⁻³` while the
  remainder is 15 `kT` wide); a one-sided floor plus a variance brackets `ln Z` without exponential cost.  (iii)
  *How often uncertified error bars are wrong:* a two-standard-error bar of a reweighting estimate covers in
  92–100 % of repetitions when `D₂ < 1` and in 5–82 % when `D₂` = 3–45, missing by up to 6 nats; brackets with
  a guarantee never fell below 0.978.  (iv) *The rotamer discretisation:* a rigid-rotamer table's free energy is
  off by 0.6–3.2 nats per torsion against the same force field with continuous torsions, minimising inside
  cells repairs populations but not that term (1.2–2.3 nats), and one-residue cell free energies reduce the
  coupling error to `4·10⁻⁴`–`4·10⁻²` nats per torsion at three cells.
* **Artifacts.**  `docs/science/PHYSICAL_APPLICABILITY.md`; workstream reports SP, P2; addenda A17 (6), (7),
  (11), (25), (26) with item 103; `experiments/science/ws_P`, `ws_P2`, `pi_inference/continuous_cells_real*`.
  Commits `7c463b0`, `e01dfa0`, `b438c89`, `071ffa6`, `2796bec`, `7b59bae`.
* **Verification and review.**  Exact enumeration on grids; (iv) replicated by referee R28 in 329 items without
  a disagreement and corrected in five statements (below); (i)–(iii) author-only or one workstream, two numbers
  re-run.  **Grid maxima are not bounds.**
* **Assumptions; prior art; distinction.**  One force field, capped peptides, idealised backbones.  Prior art:
  the brackets are Hoeffding (1963, Theorem 3) and Bennett; the cost table is Block and Shetty (arXiv, February
  2026); the discretisation phenomenon is Georgiev, Lilien, Donald (2008) and Gainza, Roberts, Donald (2012);
  cell free energies are LUTE (2017).  What is ours is the *numbers on this programme's instances* and the
  reading of them — no originality in the mathematics is claimed.
* **Limitation that was itself a finding.**  Our most quoted example — "the minimum of a rigid-rotamer table lies
  in another well; ideal rotamers are strained by 3.8 and 5.9 `kT`" — is one builder's bond angle on a knife
  edge (referee R28; re-measured by the coordinator: gone under a 2° shift, without the solvent term, and with
  one bond angle relaxed).  Corrected by SCI-REV-0029.
* **Before use.**  Repeat (iii) and (iv) on a protein with a real backbone and relaxed bond geometry; they are
  the two measurements a practitioner could act on.

### B4. The validation record (reviews with replication; prior-art determinations)

* **Contribution.**  A method — independent re-derivation, own code, controls that can fail, predictions written
  before runs, reading levels stated per source, linked corrections — applied thirty times.  Outcomes of
  consequence are in §A.1.  Prior-art determinations (workstreams A1–A4): the odds-ratio lemma, the
  non-adaptive exponent formulas at the cone, the channel-coding dictionary's identities, the identified-set
  framework, Lemma 11.89, the mechanism of the Geometry division's Theorem L — **in print**; "adaptive = hinted"
  with exact exponents and a matching algorithm without log-concavity, and the two-round separation — not found.
* **Artifacts.**  `docs/science/INDEPENDENT_VALIDATION.md`; `docs/collaboration/messages/science/SCI-REV-*.md`;
  `docs/science/workstreams/R*_REPORT.md`, `A*_REPORT.md`; `PRIOR_ART_MATRIX.md` (body at version 1, addenda
  current); `DEAD_ENDS.md` (rules SD13–SD78).
* **Status and limits.**  Internal AI review — the same family of models reviewing itself; replication is the
  part that does not depend on that.  The last review (SCI-REV-0030) was wound down and re-checked by nobody.
  The theory division's audit was replicated on our machine at several of its commits, not at its newest.

### B5. A closed-form robust range for free-energy differences between monotone macrostates

* **Contribution.**  Over an envelope class with a submodular known part, the Gibbs measure is sandwiched in
  stochastic order between two fields; the ratio of weights of any lower set against any upper set is extremal
  there, and uncertainty common to both macrostates cancels exactly; extended to ordered alphabets and finite
  distributive lattices.  `INFERENCE_LIMITS_ADDENDA.md` A11, A13, A14; Lean `ws_L2/Sandwich.lean`; commits
  `436bdb6`, `2f52fbf`; SCI-MSG-0009, -0014.
* **Status.**  Machine-checked since checkpoint 29; 900 exact linear programmes.  Adopted by the theory division,
  which solved the general (non-monotone) problem as a transport problem (its §11.28, reviewed by us).
* **Originality, honestly.**  Two lines from Holley's inequality.  The statement was not found; an expert in
  correlation inequalities would not be surprised by it.
* **Limits.**  Submodularity and monotone macrostates are strong; no physical instance.

*Considered and not ranked:* certified kinetics (cut certificates for barriers, 32 Lean theorems, a PSPACE
obstruction — no physical instance); Proposition A17.24 (continuous site variables — correct, refereed, "at
most a new combination" after the referee's search); necessary optimality under interval tables (classical).

## C. Negative results, rediscoveries, and what to deprioritise

**Rediscoveries (sent as ours, found in print).**  The cost table of certified reweighting (Block and Shetty
2026) and its bracket (Hoeffding 1963) — sent to the theory division as "our extension" before the search
returned; necessary optimality under interval costs (Kasperski and Zieliński) — said to be classical from
memory, confirmed; the rigid-rotamer finding (Georgiev et al. 2008; Gainza et al. 2012) — sent to two divisions
without its prior art; cell free energies as state energies (LUTE 2017).  Rule adopted after the third: a
measurement that leaves the branch carries its prior-art class, "not searched" if that is the truth.

**False or overstated statements of ours** (all corrected by linked messages; `DEAD_ENDS.md`): the leucine
example (above); an "exact cost" that was a bound in a quantile sense; a "sharpening" that was not one; five
published sentences wrong in scope, quantifier, gloss, attribution or kind; a clause false beyond a junction.
About a dozen predictions written before runs were missed and are recorded with the runs.

**Negative results worth keeping.**
* By analysis alone the constants of the solvent term can be bounded only with a loss of a factor 33–1 400; the
  certificate needs evaluations on a ball.  On a serine helix it stops at an order where the ball is
  unaffordable while the measured remainder is `0.002–0.004 kT`: *the price is small and the proof is missing.*
* No bound that ignores the signs of the charges can certify a compact charged ensemble.
* A pointwise floor costs `e^{floor}/ε`; no polynomial moment of the remainder suffices.
* In the worst case local data are worth nothing (§B2); certifying barriers on chains meets a PSPACE obstruction
  (workstream K).
* The Geometry division's stability theorem gives error bars smaller than the object only for distance errors
  below `4·10⁻³` to `10⁻⁶` Å; the theory division's finite-size theorem beats non-adaptive cost only where it
  certifies `e^{890}` evaluations (their numbers, read by one referee).
* **Unfavourable comparison for the whole direction:** in the one published study we verified (Yanover,
  Schueler-Furman, Weiss 2008, abstract) finding the exact optimum improves side-chain accuracy by less than
  0.1 %, while the energy function and library move it by 6–10 points.

**Deprioritise or abandon.**
1. Higher orders and longer idealised homopeptides for the sandwich — each costs more and none reduces the
   dominant error.
2. Worst-case envelope classes for a solvent term in torsion variables (`βc` = 12–53: vacuous).
3. Certified kinetics on physical systems.
4. Further reviews of asymptotic exponents that have no reachable size.
5. Machine-checking elementary lemmas of ours for completeness.
6. Any claim of structure prediction or of accuracy gains from certification.

## D. Practical opportunities

| capability | mathematically possible | software | synthetic validation | realistic computational validation | experiment |
|---|---|---|---|---|---|
| **1. A guaranteed bracket for a reweighting / free-energy-perturbation estimate** (one-sided floor + variance; Hoeffding's Theorem 3, Bennett) as a replacement for a standard error where a floor is known | yes (known inequalities) | scripts (`pi_inference/`, `ws_P3`) | yes: 45–74 enumerated rotamer instances, coverage never below 0.978 against 5–82 % for standard errors when the model is poor | **no** — no molecular-dynamics data, no explicit solvent | none |
| **2. An auditable side-chain free energy or population on a fixed backbone with a many-body solvent term** (§B1), with a certificate file | yes | research scripts; Stage 1 checker; engineering to write the independent checker | yes (enumeration to `5·10⁶` states) | **partial** — capped homopeptides, ideal backbones; no protein | none |
| **3. An audit trail for side-chain packing and design software** (the Structural Biology division's tool; our role is evaluation) | yes | theirs | theirs | theirs, on six development structures; the Frontier division's sealed list unopened | none |
| **4. Falsification of a model from averaged data** (a certified lower bound on model error; Theorem 8) | yes | linear programmes | lattice chains to 10 beads | no | none |

The first is the shortest path to something a practitioner might use: it needs no new mathematics, it has a
measured failure rate of the standard practice to compare against, and the missing piece is a floor for a
realistic model — which §B1 supplies only for one implicit-solvent term.  The second is the programme's
distinctive capability and is worth exactly what "fixed backbone, rigid rotamers, implicit solvent" is worth.
For all four the honest claim is **auditability**: what a stated model implies, checkable by a third party.

## E. Recommended next actions (three)

Costs: this division never used Modal.  Our only measured unit of Claude expenditure is a one-hour referee
workstream — about 0.63 million tokens each for the last two (harness figures); dollar figures are not available
to us and none is given.

**E1. The error budget on real protein instances: does a certificate change any conclusion?**
* *Objective.*  For side-chain placement and side-chain free energies on real backbones, measure every line of
  the budget in the same units — optimality gap (zero with a certificate), rounding, discretisation, bond
  geometry (including the source-well bias of rigidly rotated geometries, 1.2–1.9 `kT` per leucine by one
  referee), energy model — and state which conclusions depend on the certified line.
* *Prerequisites.*  The Structural Biology division's software and tables (model v2); our protocol
  (`SOFTWARE_EVALUATION_PROTOCOL.md`), the necessary-optimality construction, referee R28's scripts
  (`ws_R28/ff_flex.py`, `ff_relaxgeom.py`); the Frontier division's protocols.  **The review of model v2 owed
  under the owner's third directive was not started and belongs here.**
* *Missing.*  Flexible-geometry tables on real backbones; a second energy model; the per-site bookkeeping.
* *Baselines.*  Published packers named in the Frontier division's register; the uncertified exact solver
  (toulbar2); the 2008 study above as the expectation.
* *Benchmark.*  The development structures first; the Frontier division's sealed list only after predictions
  are frozen, and never opened by us.
* *Success / failure.*  Written before the run.  Expected: the certified line is below every other by a factor
  above ten at more than 90 % of sites, and certification changes rotamer recovery by less than 0.5 points —
  which would establish "auditability, not accuracy" with numbers.  The expectation fails if a heuristic's
  shortfall changes a conclusion somewhere; that would be the more interesting outcome.
* *Claude.*  Two to four units of the size above (one for the v2 review, the rest for measurement and an
  adversarial referee).  *Compute.*  Minutes to hours of CPU per structure on the scale we have seen; Modal cost
  not estimable by us — the runs would be the engineering division's.  *Dependencies.*  Structural Biology
  (software), Frontier (protocols, freeze), Engineering (runs).  *Model.*  The measurement could continue on
  Opus; the adversarial review and the interpretation are where the stronger model earned its cost here.

**E2. Make the strongest own result defensible: Stage 2 of the certificate and a referee for the unrefereed parts.**
* *Objective.*  Turn the three data assumptions of a Stage 1 file into checks: (G1) the evaluated part recomputed
  exactly from the ball values, with the construction's choices as a witness — designed, not coded (handoff
  §0); (G3) an evaluation bound or an interval evaluator; (G2) a specification of P3's Theorem 3 and
  Proposition 4 separate from our code.  And an adversarial referee for addenda A17 (13)–(18), (23)–(24).
* *Prerequisites.*  Everything in `experiments/science/sandwich_cert/`, `ws_P3`, `ws_P6`; the format note §9.
* *Missing.*  The exact construction; the specification; the review.  *Baseline.*  The published provable
  partition-function methods on the same pairwise approximation of the same instance.  *Benchmark.*  The two
  published instances plus one on a real backbone.
* *Success / failure.*  An independent checker of the engineering division accepts files whose only remaining
  assumption is the force field itself; failure is a step that cannot be specified without our code, or a
  referee's counterexample in parts (13)–(18).
* *Claude.*  (G1): about one unit.  (G2) and the referee: two to three.  (G3): not estimable before the
  evaluator is chosen.  *Compute.*  CPU minutes; no Modal.  *Dependencies.*  Engineering (checker).
  *Model.*  (G1) and the checker are mechanical and suit Opus; the referee and (G2) need the stronger model.
  **A platform safeguard stopped the first referee of parts (13)–(16) within two minutes; the owner should
  expect that a review of those parts may need a differently worded brief or a human.**

**E3. An originality determination that would stand before an external expert, for B1 and B2.**
* *Objective.*  Full-text prior-art searches by a reader with library access and knowledge of (a) provable
  protein-design algorithms and implicit-solvent approximations, (b) query complexity and coding theory; then
  two short manuscripts or two retractions of the word "new".
* *Prerequisites.*  `PRIOR_ART_MATRIX.md`, the search logs of workstreams A1–A4, P2, P3, R28; the list of
  sources we could not open (Decoster 2004; Dagum–Karp–Luby–Ross; Schrader 1967; Luo–Wu 2011; every full text
  in protein design).
* *Missing.*  Library access; a human expert.  *Success / failure.*  Each claim ends as "in print, cite X" or
  "survived a named expert's search".
* *Claude.*  About one unit of reading per manuscript once sources are available.  *Compute.*  None.
  *Model.*  Either; the binding constraint is access to the literature, not reasoning.

## F. Publication readiness

Nothing on this branch is ready for an external venue.  Two results could become so.

1. **A note on certified free-energy brackets with a generalized-Born term (B1).**  Needed: Stage 2 or an
   equivalent independent re-implementation; a referee for the unrefereed parts; the full-text search of E3; an
   instance a reader cares about (a real backbone); the comparison with a published provable method; and a
   limitations section that leads with §A's second bullet.  Formal verification would help the certificate's
   kernel, not the claim of novelty.
2. **"What local and thermodynamic data are worth" (B2)**, jointly with the theory division's Proposition
   11.104.  Needed: the search; the two open Lean items or their removal from the claims; a title that says
   "worst case".

A third text would be worth writing for internal use rather than publication: **the method and outcomes of the
validation record (B4)** — which kinds of claim survived adversarial replication, which did not, and at what
cost — because it is the part of this programme most likely to be reused.

## G. State at the halt

* **Subagents:** none active.  Referee R28 handed back and is closed (SCI-REV-0029).  Referee R29 was wound down
  on the coordinator's order when the directive arrived, handed back incomplete and is published as such
  (SCI-REV-0030).  **Background processes, scheduled sessions, Modal jobs: none; this division never used Modal.**
* **Finished under the directive because it was in hand and consequential:** the Stage 1 certificate (pushed
  minutes before the directive arrived); the correction of our leucine example, re-measured by the coordinator.
* **Not started, recorded as open:** the review of the Structural Biology division's model v2; items 1 (a),
  1 (b), 3, 5 of FRONTIER-REQ-0002; Stage 2 of the certificate; a re-check of referee R29's findings; the
  reading of ENG-RES-0015/-0016/-0018, ENSEMBLE-RES-0007/-0008 and ENSEMBLE-MSG-0009, GEOMETRY-MSG-0010 and the
  Geometry division's thirteenth checkpoint, COMPLEXITY-RES-0010, STRUCTBIO-REV-0001, the Frontier protocols.
  The Frontier division's sealed material was never opened.
* **For the owner's decision:** addenda A17 (13)–(18) remain unrefereed because the referee launched for them
  was terminated by a platform safeguard; the coordinator did not do that referee's work.
* **To resume:** `docs/science/RESEARCH_SYNTHESIS.md` §0 (first block), then `docs/science/OPEN_PROBLEMS.md`.
  A new container starts without the caches of `ws_P3`/`ws_P6` and without the referees' data files (all
  regenerable; each report says how).
