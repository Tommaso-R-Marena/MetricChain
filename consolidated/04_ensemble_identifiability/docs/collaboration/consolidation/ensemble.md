# Consolidation assessment — Ensemble Identifiability and Certified Inference Division

*Branch `research/ensemble-identifiability`.  Written 2026-11-27 (UTC) under the research owner's
directive "Controlled Consolidation and Temporary Research Halt".  This is the division's own
assessment of its own work.  "Review" below means internal AI review (by subagents of this
division, or by another division of the programme) unless it says otherwise.  **No statement
of this division has been read by an external human expert.**  Labels: [V] kernel-checked in
Lean, [P] written proof, [K] cited from the literature, [N] numerical evidence, [C] conjecture.*

Where things are: mathematics `docs/ensemble/ENSEMBLE_REPORT.md` (Parts I–VIII, statements
E1–E32); state of every statement `docs/ensemble/THEOREM_REGISTER.md`; what is owed
`OPEN_OBLIGATIONS.md`; searches `PRIOR_ART.md`; errors and withdrawn claims `DEAD_ENDS.md`;
what a tool may implement `SOFTWARE_INTERFACE.md`; reference instances
`BENCHMARK_CONTROLS.md`; hand-over `HANDOFF.md`, `RESEARCH_LOG.md` ("Resume here").

---

## A. Executive assessment

The division asked one question: when do finitely many averaged data `y_i = ∫ f_i dμ + ε_i`
determine an ensemble `μ` with no prior on it, and, when they do not, what can still be
certified.  Since its registration (2026-11-26, 15:59 UTC) it has produced a report of eight
Parts, five Lean modules (1 093 lines; 26 headline statements and 10 non-vacuity witnesses in
the programme's axiom audit — §G), thirteen check scripts whose stored output is tied to the
report's sentences by a checker (152 entries), three internal reviews that were applied and
a fourth (§G), an independent review of Part II by the Science division, 25 reference
instances with ground truth and 10 torus instances for benchmarks.

What that amounts to, stated so that a specialist could not fairly object:

1. **The framework is known mathematics.**  "Identified = the data lie in a simplicial face
   over which the feature map is injective; the certificate is a non-negative function of
   the span vanishing exactly on the support" (Theorem E1) is the determinacy theorem of
   di Dio and Schmüdgen (2018) and the dual certificate of non-negative sparse recovery.  We
   derived it before finding it.  Part I is a formulation with exact moduli (E2, E3), not a
   discovery.
2. **Three groups of results may be original, each narrowly.**  Exact thresholds for
   ensembles on a torus observed through multilinear trigonometric means (B1); ensembles of
   frameworks from the laws of their edge lengths, with a sharp quantitative form of the
   Rényi–Heppes theorem (B2); an exact criterion for a finite-temperature union bound (B4).
   "Original" means "not found in documented, limited searches"; the mechanisms behind all
   three are classical, and a specialist may know them as folklore or as corollaries.
3. **The most useful output is the least original.**  Exact reductions that keep certified
   inference possible under realistic observation models — unknown gains and offsets,
   error sets that are not boxes, two time scales, an incomplete conformer library, an
   unknown number of conformers, refinement of the pool, unknown linear parameters of the
   forward model — each with a certificate that a separate program can check (B3).  They
   are elementary convex analysis.
4. **Nothing has touched a measurement, and we wrote no software beyond check scripts.**
   All validation is synthetic and small (at most a few hundred configurations).
5. **The central negative finding.**  With realistic data no ensemble is *identified*:
   the verdict does not survive a refinement of the conformer pool (E30), results on
   distance distributions have no stability modulus (Problem O4), and the graded quantity
   an evaluator would want — the identifiability radius — is NP-hard (E31).  The defensible
   product is therefore *certified intervals* (partial identification), and whether those
   intervals are narrow enough to be informative on realistic problems is untested.

---

## B. Strongest contributions, ranked

Ranking by originality, correctness, significance and utility together.  B1, B2, B4 carry
the originality; B3 the utility; B5 is a synthesis and is fifth for that reason.

### B1. Finite ensembles on a torus from multilinear trigonometric means

* **Contribution.**  Configuration space `𝕋^r` (`r` angles); data: the `3^r` means of products of
  `1, cos φ_k, sin φ_k`.  (i) Two states are determined iff they differ in at least two
  angles, with a certified quadratic modulus (E20′, E20″).  (ii) On `𝕋²` no three-state
  ensemble is determined (E22).  (iii) Generic `K ≤ 2^r − r − 1` states are determined (E20).
  (iv) On `𝕋³`: five generic states are determined (E20a); six states in general position
  never are (E20b); on a hypersurface of special six-tuples they are, by a certificate that
  is not a sum of squares (E20c).  (v) For `r ≥ 4` no `K ≥ 3^r/(r+1)` states in general position
  are determined (E20d).  (vi) At `K = 2^r − r + 1` there is no generic answer over the reals:
  for thirteen states on `𝕋⁴`, 26 of 40 random configurations are identified, 10 are not, 4
  undecided (E20e).
* **Where.**  Report §4c.4.  Commits `32f547a`, `8d42f60`, `2d2054d`, `b654396`, `fb22cb8`.
  `proofs/Ensemble/TwoStateCertificate.lean`, `PermanentCertificate.lean`.  Scripts
  `torus_six_states.py`, `torus_four_angles.py`, `lifted_checks.py`; instances
  `experiments/ensemble/benchmarks/torus_instances_v1.json`.
* **Verification and review.**  [V]: the zero set of the two-state certificate, one
  inequality of E20″, the permanent certificate E21(a).  Everything else [P], with exact
  computer algebra at rational instances (Gröbner bases over `ℚ`, ranks over `ℚ` and modulo a
  prime — not kernel checks) and [N].  Internal review ER3 covered E18–E21, E20″ (applied);
  E20a and E22 *originate* in ER3 and were re-derived by us.  Internal review ER4 examined
  E20a–E20d (applied): no statement false; both exact computations reproduced by an
  independent method; the special six-tuple reproduced; one false clause in the proof of
  E20b replaced; four sentences about these results corrected.  E20e, E22 and the
  constants of E20″: not examined by ER4.
* **Assumptions.**  Exact data.  General position, stated explicitly (rank of the
  tangential conditions).  E20d rests on Laface–Postinghel (arXiv 1105.2136, Theorem 2.1:
  statement read, proof not).
* **Closest prior art.**  **di Dio–Schmüdgen (2018), Section 7, Theorem 40** — full rank of
  the derivative of the moment map makes the data an inner point of the moment cone, and
  then nothing is determinate: found by the reviewer ER4 in the paper we already cited,
  *this is the mechanism of E20b and E20d*; the same paper has determinate functionals
  whose certificates are not sums of squares (Robinson, Motzkin).  Baldi–Blekherman–Sinn,
  arXiv 2407.06017 (moment problems on curves; its Sections 5–6 probably contain E20b and
  E20c *on a given smooth curve* — not yet read in the source by anyone here).
  Laface–Postinghel (secant varieties of Segre–Veronese varieties); Chiantini–Coppens
  (E20); the core variety; Carathéodory–Toeplitz (E22); super-resolution of positive
  measures.
* **Distinction.**  The reduction from the torus to the curve cut out by the lifted
  certificate (the curve depends on the states); the complete answer for two and three
  angles with exact ranks; an instance of a non-SOS certificate on the torus; the
  numerical evidence that at thirteen states on four angles there is no generic answer
  over the reals.
* **Evidence for originality.**  The counts `2^r − r − 1`, "five, not six, on `𝕋³`", the special
  six-tuples and E20e were not found (`PRIOR_ART.md` §5b, §5b′, §5e); the reviewer ER3
  reached E20a and E22 independently.
* **Evidence against.**  Every mechanism is known, and after ER4 more precisely so: E20b
  and E20d are a published criterion applied to one variety, and E20c is probably a
  published description of a moment cone plus a routine extension from the curve to the
  torus.  The reviewer's hostile summary is fair: "a clean worked example: the torus of
  three angles, five and not six, with exact ranks at two rational points — computer
  algebra that no kernel has checked."  The harmonic-retrieval and tensor-identifiability
  literatures were searched only by keyword.
* **Validation.**  Exact computations at rational instances; second compatible ensembles
  constructed in 10 of 10 generic six-tuples; certificates verified on grids with local
  refinement; all in the stored output.
* **Limitations.**  No noise theory beyond two states.  E20e is statistics with
  numerically verified certificates, no exact instance.  The description of the special
  six-tuples by half-periods of a curve of genus one is an explanation, not a proof.
  Between `2^r − r + 1` and `3^r/(r+1)` nothing is known for `r ≥ 4` (scratch only: fourteen states
  on `𝕋⁴` not identified in 15 of 16 instances).  **Relevance to data is indirect:** a scalar
  coupling is a trigonometric polynomial of one angle; means of *products across angles* are
  what few experiments measure.
* **Before publication.**  First read Baldi–Blekherman–Sinn, Sections 5–6, in the source:
  it decides how much of E20b, E20c is theirs.  Then: a reading by an algebraic geometer;
  exact instances of both verdicts of E20e and of a special six-tuple; a literature check
  in tensor identifiability and harmonic retrieval; a stability statement for `K ≥ 3`.

### B2. Ensembles of frameworks from laws of edge lengths; a sharp quantitative Rényi–Heppes theorem

* **Contribution.**  (i) E4: if any two configurations agree in fewer than `r` of `m` features,
  the *laws* of the `m` features determine every ensemble of `K` conformers among all
  ensembles as soon as `m ≥ K(r−1) + 1`; sharp.  (ii) E4.1: if the laws agree within `ε` in total
  variation, the mass away from the conformers is at most `mε/(m − K(r−1))`, attained.
  (iii) E5, E6: for a connected algebraic matroid, jointly generic conformers admit no
  "chimera" (a configuration spliced from several conformers); the exact criterion, and the
  failure of the naive converse.  (iv) E7: on a generically globally rigid graph, generic
  finite ensembles of frameworks are determined by the per-edge laws of lengths, and on a
  graph that is not, none is; E7′ for two rigid bodies; E8: `2K` moments per edge suffice.
* **Where.**  Report §3.  Commits `a570520`, `1a067b5`, `527bf02`, `fb22cb8` and the
  consolidation commit (Lean statement of E4.1).  `proofs/Ensemble/RenyiHeppes.lean`.
  Scripts `rigidity_checks.py`, `robustness_checks.py` (R5).
* **Verification and review.**  [V]: E4 for finite spaces (`Ensemble.renyi_heppes`) and the
  first bound of E4.1 (`Ensemble.renyi_heppes_mass_off_support`; see §G for the audit).
  Internal review ER1; an independent review by the Science division (SCI-REV-0020), which
  also contributed the stability statement ("Proposition B").
* **Assumptions.**  Exact laws; joint genericity; E7 uses Garamvölgyi–Gortler–Jordán (2022,
  Theorem 3.5) and E7′ Connelly–Jordán–Whiteley (2013), neither read in the original by us.
* **Closest prior art.**  Rényi (1952) and Heppes (1956) — `K` points from `K + 1` projections;
  the frameproof-code lemma of Boneh–Shaw (the support step of E4); generic global rigidity;
  unlabelled distance geometry (one configuration from its unlabelled distances — a
  different problem).
* **Distinction.**  Arbitrary features, weights and measures instead of point sets and
  projections; an attained modulus; the reading "a mixture of frameworks from per-edge
  distance distributions".
* **Evidence for originality.**  Not found in our searches nor in eighteen searches of the
  Science division's referee.
* **Evidence against.**  E7 is a four-line corollary of a published theorem; the support
  step of E4 is a known lemma; the rest is elementary — a combinatorialist may call E4
  folklore.
* **Validation.**  Exhaustive counts of splices on small frameworks; random instances for
  the modulus.
* **Limitations.**  **Not usable on data as it stands:** for distance laws there is no
  modulus beyond a band (Problem O4, the "chimera gap") — at moment accuracy `10⁻⁵` large
  mass can sit far from every conformer; and complete per-edge laws for labelled pairs are
  measured by no instrument.
* **Before publication.**  A lower bound on the chimera gap, or a proof that there is none;
  a reading by a rigidity theorist.

### B3. Certified partial identification under realistic observation models

* **Contribution.**  For a finite pool of configurations and data with tolerances: the
  range of any linear target is a pair of linear programmes with dual certificates, and
  the certificate bounds the mass away from a support (E1.1, E17).  On top of that, exact
  reductions: correlated noise and error sets that are not boxes — the tolerance term is a
  support function, systematic directions force orthogonality (E17.1, E17.2); data known
  up to unknown gains and offsets — still one linear programme, and determination is E1
  for projected features (E23, E23.1); lengths and squares of means — unions of convex
  problems, NP-complete in general (E24–E26); convex data and two time scales — a convex
  outer bound that needs no knowledge of the motional regime (E27); an incomplete library
  — a tolerance, and a certified lower bound on the missing weight (E28); the number of
  conformers — partially identified, the minimum NP-hard (E29); a pool that is a net —
  intervals are stable, verdicts are not (E30); the identifiability radius — NP-hard, with
  computable bounds (E31); unknown linear parameters shared by all conformers — outer
  bounds by subdivision of the parameter box and a finite certificate of uniqueness (E32).
* **Where.**  Report §4b, §4d, §4e.  Commits `1a067b5`, `85b7bac`, `297ec78`, `fb22cb8` and
  the consolidation commit (E32).  `proofs/Ensemble/Exposedness.lean`.  Scripts
  `nonlinear_data_checks.py`, `misspecification_checks.py`, `robustness_checks.py`,
  `bilinear_checks.py`, `benchmark_controls.py`.  Software cards in `SOFTWARE_INTERFACE.md`.
* **Verification and review.**  [V]: the exposing certificate, its mass bound, the
  homogeneous certificate (`eq_of_exposing_certificate`, `eq_of_homogeneous_certificate`).
  The rest [P] + [N].  E17 was reviewed (ER2).  E23–E26 were examined by the internal
  review ER4 (applied): correct; E23(b) confirmed exactly on 1 908 instances; one sentence
  of E26 was false as written and is corrected (a sign vector certifies consistency;
  deciding uniqueness is coNP-hard).  **E17.1, E17.2, E23.1, E27–E32 are unreviewed.**
* **Assumptions.**  A finite pool that contains the truth, or E28/E30 for one that does
  not; a forward model with a *stated* error set; for E32, exact data in the uniqueness
  certificate.
* **Closest prior art.**  Maximum occurrence (Bertini, Luchinat, Parigi and co-workers;
  Longinetti–Sgheri–Sottile): the largest weight a conformer can have — the interval of
  one population; maximum-entropy and Bayesian reweighting (one ensemble with a posterior,
  no certificate); linear-programming duality and partial identification in
  econometrics; phase retrieval for E26.
* **Distinction.**  Certificates that a separate program checks; the exact treatment of
  gains, offsets and error sets; hardness statements that say where a tool must not
  promise exactness; reference instances with ground truth.
* **Evidence for originality.**  Little is claimed.  The specific statements E23.1, E28,
  E30–E32 were not found, but were searched only briefly.
* **Evidence against.**  Everything is elementary; intervals of populations are in print
  (maximum occurrence); hardness of sign problems is known.
* **Validation.**  Random instances in the scripts; 25 control instances with 38 exact
  verifications (`benchmarks/controls_v1.json`); the Frontier Benchmarking division
  reports an exploratory pilot on planted controls (its result, not ours).  **No realistic
  forward model, no data.**
* **Limitations.**  Width of the intervals on realistic problems unknown — they may be
  vacuous.  Pools of `10⁴`–`10⁵` conformers need column generation, not written.  Stated
  error sets for forward models do not exist yet (the Science division's prerequisite).
* **Before deployment.**  The benchmark of §E1; a review of the unreviewed statements.

### B4. An exact criterion for the thermal union bound

* **Contribution.**  For binary sites and a class of ensembles within an envelope of a
  polarised member `ν`, with `N` the number of disagreements: the bound
  `TV(μ, ν) ≤ Σ_i (deficit of site i)` holds for every member iff `Var_ν(1_U) ≤ Cov_ν(1_U, N)` for
  every up-set `U` (E15U); companions for the population bound and for stochastic
  domination; a necessary per-site condition that is sufficient at weak coupling and not
  in general (explicit three-site and four-site examples).  E15, E15T are the sufficient
  forms (product reference; positive association).
* **Where.**  Report §4a.  Commits `1a067b5`, `527bf02`, `2d2054d`.
  `proofs/Ensemble/ThermalUnionBound.lean` (core inequality of E15(c) [V]).  Script
  `finite_temperature_checks.py`.
* **Verification and review.**  ER2 (which removed a false converse of ours for E15T).
  The main statement of E15U was re-derived with its own proof and replicated on 950
  random measures by the Science division (SCI-RES-0038); the companions and examples
  have been read by nobody else.
* **Assumptions.**  Binary sites; the first-order classes of the theory division.
* **Closest prior art.**  Correlation inequalities (FKG, Holley, Strassen), from which E15T
  follows; nothing like the up-set criterion was found in two searches.
* **Evidence for / against.**  Not found — but the statement is an elementary extreme-point
  argument, and two searches are few for a field as old as correlation inequalities.
* **Limitations.**  The criterion has exponentially many conditions; binary alphabets
  only (the bound is false for larger ones); use depends on the programme's envelope
  classes.
* **Before publication.**  A search by someone who knows the literature of correlation
  inequalities; then at most a short note.

### B5. How many random conformers pair (and higher-order) data on the cube can identify

* **Contribution.**  A synthesis through E1 of known theorems (Odlyzko; Cover; Bai–Yin;
  Baldi–Vershynin; Kahle; Donoho–Tanner): random supports of `K < n − 10n/ln n` conformers on
  `{±1}ⁿ` are identified by pair correlations with an explicit energy (E10); beyond `2n` none
  is, and beyond `6.34n` every ensemble has an explicit full-support twin (E11); a prior on
  the number of conformers moves the limit from `2n` to `n²/2` (E19(c)); adaptive designs
  (E12).  Numerics: the threshold lies between `1.1n` and `1.2n` (exact decisions to `n = 20`);
  four-body data lie within 2–9 % of the Gaussian curve of Donoho–Tanner for `n ≤ 12` and
  8–15 % above it at `n = 14`.
* **Where.**  Report §4, §4c.  Commits `a570520`, `1a067b5`, `32f547a`, `b654396`.  Scripts
  `pair_capacity_checks.py`, `capacity_*.py`, `kbody_capacity.py`, `gaussian_threshold.py`,
  `output_threshold.txt`.
* **Status.**  ER1, ER3 applied.  E19(a) was derived and then found in print
  (Baldi–Vershynin 2019); E19(g) is Kahle (2010).  Ours: E11(b), the contrast in E19(c),
  the numerics.  The thresholds are conjectures (C2, C3).
* **Limitations.**  Spin models with complete pair data are far from structural data.

---

## C. Negative results, rediscoveries, and what to stop

**Rediscoveries.**  E1(b) = di Dio–Schmüdgen 2018, Theorem 18 (found on the second day).
E19(a) = Baldi–Vershynin 2019.  E19(g) = Kahle 2010, which also makes E21 weaker than the
literature on finite product spaces.  E9 = 3-neighbourliness of the cut polytope.  E2, E3,
E13, E17 are formulations of known duality.

**False statements we made** (all withdrawn; `DEAD_ENDS.md` ED1–ED25): a converse of E15T
that was never proved (found by ER2); "identified implies no chimera" (ER1); a count of
conditions on the torus that was never computed, and a non-identification test on a
product grid that could not have failed (ED24, found by ER3); a conjecture on pair models
refuted by an optimiser after 17 000 random instances had missed the counterexample
(ED23); "ratios of averages are covered by nothing" — published and wrong within the hour
(ED25); three times, numbers in the text that no script printed (ED20; hence the quote
checker).  Found by the last review (ER4): a clause in the proof of E20b that is false
at an explicit instance (the theorem stands); "an answer with its signs is checked in
polynomial time" — true of consistency only; a check described as showing that a bound
is attained, which was a relaxation; "all twins are within `O(√ε)`" — a second-moment bound,
of order `ε`, and nothing about supports.  The pattern in all four reviews: numbered
theorems survived; *sentences that summarise or extend them* did not.

**Unfavourable facts established.**
* Verdicts of identification are not stable under refinement of the pool (E30): a
  verdict about a pool is not a verdict about a molecule.
* Distance-law data: no stability modulus (O4).  Unusable on DEER- or FRET-type data now.
* The identifiability radius is not a linear programme; deciding whether it is one is
  NP-complete (E31).  Squared means (E26) and the least number of conformers (E29) are
  NP-hard as well.
* Under a centred Gaussian model, data known up to one unknown factor identify an
  ensemble of `K` conformers in a pool of `n` with probability below one half unless
  `m ≥ (n + K)/2` (E32(d); unreviewed): with a pool much larger than the number of data,
  exact identification from scale-free data is out of reach in that model.
* A fixed design that identifies all two-conformer ensembles must be complete (E12).
* On planted non-identified controls the certified answer is "NOT IDENTIFIED": correct,
  and by itself useless to a practitioner (the Frontier division's observation).

**Abandon or deprioritise.**  (1) Thresholds on the cube (C2, C3): numerics only, remote
from data.  (2) Counting on tori for larger `r`: real algebraic geometry with no generic
answer and indirect relevance.  (3) Identification from distance laws, until O4 is
decided.  (4) "IDENTIFIED / NOT IDENTIFIED" as a product: replace by intervals.  (5)
Further Lean formalisation of elementary statements.

---

## D. Practical opportunities

| capability | mathematical possibility | implemented software | synthetic validation | realistic computational validation | experimental evidence |
|---|---|---|---|---|---|
| **Certified intervals** for populations and observables of an ensemble, given a conformer pool and averaged data with unknown scale and offset and a stated error set; with a dual certificate checkable by a separate program | yes ([P]; core [V]): E17, E17.2, E23.1 | check scripts only; no tool of ours; cards sent to the Structural Biology division (not verified by us whether implemented) | 25 controls; random instances; Frontier's exploratory pilot | **none** | **none** |
| **Falsification of a conformer library**: data outside the library's moment body, with a certificate and a lower bound on the missing weight | yes ([P]): E28 | script only | controls B9 | none | none |
| **Bounds on the number of conformers** and on the identifiability radius, reported with every answer | yes ([P]): E29, E31 | script only | random instances | none | none |
| **Unknown alignment-type parameters** (one tensor for all conformers): certified outer bounds | yes ([P], unreviewed): E32 | script only (`p = 2`) | small planted instances | none | none |
| **Control instances with ground truth** for the evaluation of reweighting tools | — | `benchmark_controls.py`, `controls_v1.json`, `torus_instances_v1.json` | self-verifying | — | — |

The shortest credible path to something demonstrably useful is the first row: an
interval tool beside an existing reweighting method, evaluated on synthetic data from a
realistic forward model.  Its risk is plain: the intervals may be too wide to matter.

---

## E. Recommended next actions (three)

### E1. Are certified intervals informative on realistic problems?  (the decisive experiment)

* **Objective.**  Measure the width and the coverage of certified intervals for
  populations of states, against the uncertainty reported by standard reweighting, on
  synthetic data generated by realistic forward models from public conformer pools.
* **Prerequisites that exist.**  E17, E17.2, E23.1, E28, E30 with certificates; the
  software cards; the control instances; the Frontier division's protocol drafts.
* **Missing.**  A forward model with a stated error set (Science); a solver for pools of
  `10⁴`–`10⁵` conformers (column generation over the pool); constants of E30 for the chosen
  features.
* **Baselines.**  Maximum-entropy / Bayesian reweighting (BME, EROS-type), maximum
  occurrence, a metainference-type method — named from memory; the Frontier division
  should fix them.
* **Benchmark.**  Planted ensembles on a pool; data = forward model + noise from the
  stated error set; held-out states as targets; pool refined to test E30.
* **Success.**  Coverage 100 % wherever the assumptions hold (anything less is a defect),
  and median width below a pre-registered fraction of the trivial range at realistic
  numbers of data.  **Failure.**  Widths indistinguishable from the trivial range: then
  certified inference without priors is not informative for this data type, and that is
  the result.
* **Reasoning.**  Moderate; implementation follows written cards — could be done with a
  smaller model, with the certificates re-checked independently.
* **Computation.**  Linear programmes; our largest check runs for minutes on one core.
  For pools of `10⁵` we have no measurement, hence no Modal estimate.
* **Dependencies.**  Structural Biology (tool), Science (forward model and error),
  Engineering (execution), Frontier (protocol and custody).

### E2. The chimera gap (Problem O4): can distance distributions be used at all?

* **Objective.**  A lower bound, in terms of the separation of conformers and `K`, on how
  well laws of distances must be known before mass far from every conformer is
  excluded — or a family showing the bound is hopelessly small.
* **Prerequisites.**  E4.1 (the sharp modulus for discrete laws), the Science division's
  Proposition B, E7.
* **Missing.**  The quantitative step from laws of lengths to configurations (a modulus
  for generic global rigidity).
* **Baselines / benchmark.**  None published that we know; the test is a theorem or a
  counterexample, with planted two- and three-conformer instances as a check.
* **Success / failure.**  An explicit modulus usable at experimental accuracy — or a proof
  that none exists, which closes the direction (see C).
* **Reasoning.**  Substantial, mathematical; needs the strongest model.  No computation
  of note.  **Dependencies.**  Geometry division (stability of rigidity).

### E3. External reading of the three possibly original results

* **Objective.**  Decide by expert reading whether B1, B2 (E4, E4.1) and B4 (E15U) are new,
  and correct.
* **Prerequisites.**  Self-contained statements and proofs in the report; scripts.
* **Missing.**  Short stand-alone notes (a few pages each); for B1 the exact instances
  listed there.
* **Success / failure.**  A specialist's verdict, either way.
* **Reasoning.**  Small to moderate for the notes; a smaller model can draft them.  No
  computation.  **Dependencies.**  The research owner (access to readers).

---

## F. Publication readiness

Nothing is ready.  Candidates, in order:

1. **B1 as a short paper** ("which finite ensembles on a torus are determined by
   multilinear trigonometric moments").  After ER4 the honest framing is a worked example
   of known criteria (di Dio–Schmüdgen, Theorem 40; probably Baldi–Blekherman–Sinn on the
   curve; Laface–Postinghel).  Needed first: Baldi–Blekherman–Sinn §5–6 read in the source
   — if it gives E20b and E20c on the curve, what remains is the reduction from the
   torus, the small cases with exact ranks, and E20e; then exact instances for E20e and
   an expert reading.
2. **E4 with E4.1 as a note** (a quantitative Rényi–Heppes theorem for arbitrary features).
   The Lean proof establishes correctness, not novelty; needed: a combinatorialist's
   opinion on whether it is folklore.
3. **E15U as a note**, after a proper search in correlation inequalities.
4. **B3 as a methods paper only together with E1's experiment.**  Without realistic
   validation it is a list of exercises.

Formal verification covers 26 statements of this division; none of them is a statement
whose *novelty* is in question except E4/E4.1.

---

## G. State at the halt

* **Active processes: none.**  The one subagent (the internal review ER4) has reported and
  ended; the one background job (the audit) has finished; no session is scheduled; this
  division never started a Modal job and none is pending.
* **Internal review ER4** (object: E20a–E20d, E23–E26 at commit `b654396`): received,
  committed as received (`87bb28a`), applied (report §7 item 21).  No numbered statement
  false; five major and seven minor findings.  It was stopped at the directive; what it
  did not finish is listed in its §7 and in `OPEN_OBLIGATIONS.md` OB32.
* **Formal verification.**  `scripts/audit_all.sh` passed on the final `proofs/` tree
  (2026-11-27, 01:20 UTC): build without warning, 5151 declarations on the three standard
  axioms, falsification harness.  The last addition is the counting inequality of E4.1
  (`Ensemble.renyi_heppes_mass_off_support`).
* **Numerical evidence.**  Stored output of thirteen scripts; the quote checker (152
  entries) and the reference checker pass.  A full re-run of all scripts was not repeated
  after the last changes of text.
* **Unreviewed statements:** E23.1, E27–E32, E17.2, E20e, E4.1 beyond its machine-checked
  inequality, E15U beyond its main statement, E17.1, E22, two constants of E20″.
* **Evaluation integrity.**  This division holds no sealed data, no credentials and no
  held-out material, made no prediction, and took no part in any assessment.  Its
  reference instances (`controls_v1.json`, `torus_instances_v1.json`) are frozen at the
  final commit.
* **Resumption.**  Only on the research owner's explicit authorisation.  Start from
  `docs/ensemble/HANDOFF.md` item 0 and "Resume here" in `docs/ensemble/RESEARCH_LOG.md`.

