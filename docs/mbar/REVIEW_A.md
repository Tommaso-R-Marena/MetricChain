# Division 9 — internal adversarial review A, and the division's response

*The review was made by one AI subagent instructed to find errors, with its own code (no import of the
division's library for mathematical claims), on the tree between commits `7fff440` and `37ac8d7`
(2026-11-28).  It did not run the Lean build.  Its report is reproduced verbatim in Part 2; its scripts
and outputs are in `experiments/mbar/review/`.  This is an internal review by an AI session, not an
external academic review.  Part 1 is the division's response, written by the coordinating session.*

## Part 1 — Response

**Verdict of the referee, in its words:** "I found no false theorem and no wrong constant … The defects
are one statement false as literally written (B2 boundedness, in a corner the code handles correctly),
several incomplete proofs or missing hypotheses, and wording stronger than what is proved … Code: one
serious defect."

**The serious defect (E1) is accepted in full.**  The Newton solver could report convergence at its
starting point when the states' energies differ by constants of some tens of kT; `mbar()` then
returned estimates wrong by tens to hundreds of kT, and the model check rejected correct models.  It
was introduced by our own earlier "fix" of the convergence flag.  None of our benchmarks could see it
(all have free energies of order 1).  The solver was rewritten, regression tests were added, the
referee's failing scripts were re-run, and the stored benchmarks were re-run or regression-checked
with the final code (table below; `DEAD_ENDS.md` E8; `VALIDATION.md` §7 says which).

| finding | accepted? | action | where |
|---|---|---|---|
| **E1** false convergence of the solver; invalid model check; false `REJECT_MODEL`; silently wrong MBAR | yes | solver rewritten: offset-free internal coordinates, row-centred likelihood, iterative-scaling warm-up, regularised Newton, convergence only on a verified Newton system (step `≤ 10⁻⁸`) or gradient `≤ 10⁻¹⁰`; no linear-algebra exception escapes; rejection and intervals only on a verified fit (`ABSTAIN_NUMERICS` otherwise); the model check returns "no rejection" when its fit is not verified.  Tests: equivariance under offsets of 10–1000 kT per state and up to 30 000 kT per sample; no convergence claimed at a saturated start.  Referee's scripts re-run: 0 wrong fits (was 93/400), 0 false rejections (was up to 96/200), 0 intervals too narrow | `estimators.minimize_lse`, `certificates.py`, `tests/test_certificates.py`, `review/rerun_after_fix.out` |
| **G1** B2 boundedness criterion false when batches lack states | yes | statement corrected to the batchwise graph (the code was right) | `MATHEMATICS.md` B2 |
| **G2** "for any set `E` of batches" | yes | restricted to sets fixed in advance or chosen predictably; the referee's three counter-enumerations quoted | B2 |
| **G3** S2: proof does not cover `K = 2` | yes | two-state instance added | `SYNTHESIS.md` S2 |
| **G4** overlapping rounds accepted by the code (10.3 % non-coverage) | yes | the code refuses overlapping batches; test added | `lr_confidence_region`, `test_overlapping_rounds_are_refused` |
| **G5** S4(ii): the region is convex in the wrong coordinates | yes | (ii) withdrawn and replaced by the box of simultaneous intervals; corrected towards the other divisions | `SYNTHESIS.md` S4, MBAR-MSG-0002 |
| **G6** width of the region is not a theorem; rate and threshold statements | yes | *Size* relabelled [N]; `√(V_c/N)` against `√(R_c/N)` stated; C3's threshold corrected | B2, C3 |
| **G7** A6: maximiser unique only up to a constant per component | yes | stated; (i), (ii) hold for every choice | A6 |
| **G8** A10: Sion with infinite values | yes | argument on `{s ≥ ε}` added | A10 |
| **G9** A12(a): what transfers | yes | primal statements only; dual ones need dual forms | A12 |
| **G10** C2: hidden budget threshold | yes | stated in the closing paragraph and in every summary | C2, §0, final report |
| **O1, O2** "adaptive cannot beat static at the leading constant"; "two rounds lose nothing" | yes | weakened everywhere to "not by more than a universal constant factor, locally, above a budget threshold"; two-round optimality labelled conjecture | `MATHEMATICS.md` §0, C2, C4; `SYNTHESIS.md` S2; `FINAL_REPORT.md`; `README.md`; status; MBAR-MSG-0002 |
| **O3** S1′ "the region certifies it" | yes | the target must be sampled (bound `0.272·K′(K′+1)`); width unproved; stated | S1′ |
| **O4** Lean labels stronger than the formal statements | yes | labels narrowed (open orthant, contrasts, inequality only); new declaration `Model.Q_le_budget` for the step of C2, valid on the closed orthant and for any direction | `MATHEMATICS.md`, `LEAN_CORRESPONDENCE.md`, `Allocation.lean` |
| **O5** safeguard docstring | yes | the integer condition `(1−γ)n⁰_k ≥ 1` stated in the docstring and in A9 | `pilot_allocation`, A9 |
| **O6** "the finite-sample form of the LAM bound" | yes | "a two-point bound of the order of …; constants not sharp" | C1 |
| **N1–N6** six numbers | yes | corrected (116 enumerated models; `V/Γ` values; line counts; ranges; "35 %" defined) | `MATHEMATICS.md`, `SYNTHESIS.md`, `DEAD_ENDS.md`, `LEAN_CORRESPONDENCE.md` |
| **M1** `nan` from a state absent from earlier and current batches | yes | the plug-in is masked on states absent from the batch | `lr_confidence_region` |
| **M2** contrast not checked; `LinAlgError` not caught | yes | contrast validated; exceptions cannot escape | `LRRegion.interval`, solver |
| **M3** tolerances | yes | outward shift now exceeds the root finder's absolute and relative tolerance; fallback when the curvature is ill-conditioned | `interval`, `kl_interval` |
| **M4** `REJECT_MODEL` semantics | yes | documented as part of the non-coverage budget | docstring, B2 |
| **M5, M6, M7, M9, M10** wording, hypotheses in the Lean table, citation, a sample-dependent number, a dangling reference | yes | applied | — |
| **M8** value returned before the final rescaling | yes | value recomputed at the returned allocation | `optimal_allocation` |

Found by the division itself while the review was running (also flagged by the referee from the
earlier code): unconverged profile solves and a batch dropped on its own data (`DEAD_ENDS.md` E7); an
ambiguous argument of `optimal_allocation` (E6).

**Not done in response.**  (a) A proof that the default path can never produce a false
`REJECT_MODEL` in floating point — the code now requires a verified fit, but floating point is not
certified.  (b) The interval tests of the referee stop at `K = 5`; larger `K` is covered only by the
benchmark (`K = 10`) and the public data (`K = 26`).  (c) The referee did not check the handoff's D1,
D2, G1, the imported theorems of other divisions, the prior-art claims, or the Lean build; those rest
on the division's own checks.  (d) The corrected documents were not refereed again.

## Part 2 — The referee's report (verbatim)

> # REVIEW A (raw) — independent adversarial referee report, Division 9 (certified MBAR)
> 
> Scope: `docs/mbar/MATHEMATICS.md`, `docs/mbar/SYNTHESIS.md`, `docs/mbar/DEAD_ENDS.md`,
> `docs/mbar/LEAN_CORRESPONDENCE.md`, `experiments/mbar/src/d9mbar/{population,estimators,certificates}.py`,
> stored results under `experiments/mbar/results/`, Lean sources (read only, build not run).
> 
> Version reviewed. The tree changed three times while the review ran (commits `7fff440` -> `aa6fac4` ->
> `883bdbe` -> `37ac8d7`).  Everything below refers to `37ac8d7` plus the working tree at 07:30 on
> 2026-11-28 (md5 prefixes: MATHEMATICS.md `e77468f3a8b0`, certificates.py `654b84f4ef95`, estimators.py
> `096bb1e3cef3`, population.py `073d61bc7d55`).  Two of my interim outputs were already taken into the
> note during the review (A9 integer condition; adjacent-contrast `sqrt(R_c/V_c)` in B4), and the
> division's own fix E7 (unconverged profile solves; batch dropped on its own data) landed in `aa6fac4`
> after I had flagged the same two points from the earlier code; I re-tested the new code.
> All my scripts and outputs are in `experiments/mbar/review/` (`check_*.py`, `check_*.out`).  No existing
> file was edited and no git state was changed.
> 
> ## 1. Summary verdict
> 
> * Mathematics (Parts A, B, C; Synthesis S1-S3): I re-derived every statement listed in section 4 and
>   attacked most of them numerically with my own code (no import of `d9mbar`).  **I found no false
>   theorem and no wrong constant.**  The defects are: one statement that is false as literally written
>   in a corner the code handles correctly (B2 boundedness criterion), several incomplete proofs or
>   missing hypotheses, and wording that is stronger than what is proved (chiefly "adaptive allocation
>   cannot beat the optimal static allocation ... at the level of the leading constant").
> * Code: **one serious defect.**  The Newton solver `minimize_lse` reports `converged=True` at its
>   starting point `f = 0` when the softmax is saturated there, which happens as soon as the states'
>   energies differ by constants of some tens of kT (i.e. whenever the free energies themselves are
>   large, the normal situation for real data).  Consequences, all under exact equilibrium sampling:
>   `mbar()` silently returns estimates that are wrong by 50-340 kT; the model check `classifier_evalue`
>   (Theorem B5) rejects a correct model in up to 48 % of the data sets at alpha = 0.05; the region
>   built with a correct user plug-in is declared empty (`REJECT_MODEL`) in up to 27 % of the data sets;
>   uncaught `LinAlgError` in many others.  The default path of the region stayed valid in my tests but
>   becomes vacuous or abstains.  The stored benchmarks are not affected (all have |f| of order 1).
> * `LRRegion.interval` (current code): no too-narrow interval found in 541 + 314 intervals checked
>   against independent witnesses / an exact reference.
> * Numbers: almost all quoted numbers match the stored results; six small mismatches are listed.
> * Lean table: the 9 declarations I read state what the table says, up to omitted positivity
>   hypotheses; two labels in MATHEMATICS.md are slightly stronger than the formal statements.
> 
> ## 2. Findings, ordered by severity
> 
> ### ERROR
> 
> **E1. False convergence of the unconstrained Newton solver; invalid model check and false
> `REJECT_MODEL`; silently wrong MBAR estimates.**
> Location: `estimators.py`, `minimize_lse`, lines 73 and 83-88 (`d = -np.linalg.solve(H + Jm, g)`;
> `dec = -(g @ d)`; `if gnorm < tol or dec < 1e-14: converged = True`).  Used by `mbar`,
> `LRRegion.__post_init__` (`fhat`, `phi_min`, hence `REJECT_MODEL`) and `classifier_evalue`.
> What is wrong: if every sample is assigned to one state with numerical probability 1 at the start
> `f = 0` (state-dependent constants in the reduced potentials), `H` is numerically zero and `H + Jm` is
> singular.  `solve` then either raises `LinAlgError` or returns a garbage step with a huge *negative*
> "decrement"; the test `dec < 1e-14` accepts a negative decrement and convergence is declared after one
> iteration with gradient norm 0.4-0.75.  (This is the fix recorded as E1 in DEAD_ENDS.md, "convergence
> is declared on the Newton decrement"; it has no sign or consistency check.)
> Evidence (the data are exact i.i.d. equilibrium samples with strong overlap; only a constant
> `off_k ~ N(0, sd^2)` is added to the energy of state k; MBAR is exactly equivariant under this, so the
> right answer is known):
> * `check_falseconv.py`: sd = 30, K = 4, 100 samples per state: `mbar` returns `f = (0,0,0,0)` with
>   `converged=True`, `iterations=1`, `grad=0.51`, `decrement=-2.0e15` where the correct differences are
>   (31.9, -1.3, 51.9); objective 8308 nats above its minimum.  93 of 400 data sets.
> * `check_offsets2.py` (K = 3, 60 per state, 60 data sets per row): `mbar` right / wrong-but-converged /
>   exception = 55/1/4 (sd 10), 27/19/14 (sd 20), 13/19/28 (sd 30), 6/21/33 (sd 50), 0/12/48 (sd 100);
>   largest errors 40, 80, 95, 169, 338 kT.
> * `check_offsets3.py` (K = 4, 100 per state, 200 data sets per row, alpha = 0.05):
>   `classifier_evalue` rejects the correct model in 0/200 (sd 0), 0/200 (sd 5), **21/200 (sd 10),
>   96/200 (sd 20), 87/200 (sd 30), 44/200 (sd 50)** — nominal at most 10/200; in 7, 54, 50, 27 of these
>   `info["converged"]` is True, in the others the statistic is returned although the fit is flagged
>   unconverged.  `lr_confidence_region(..., plugin=<a correct estimate computed from earlier batches>)`
>   returns `REJECT_MODEL` ("no f is compatible"), i.e. does not cover the truth, in **7/200, 54/200,
>   50/200, 27/200**; uncaught `LinAlgError` in 31, 87, 144 of 200 at sd 20, 30, 50.
> * Default path (plug-in = internal `mbar`): no invalid statement found — 0 false `REJECT_MODEL`, and
>   0 of 314 intervals narrower than the exact reference computed in shifted coordinates — because the
>   plug-ins fail in the same way and inflate the threshold.  But the certificate is then useless: at
>   sd 30, 24/60 `ABSTAIN_NO_DATA`, 6 `ABSTAIN_SUPPORT`, 2 crashes, and 22 of the 56 intervals of the
>   28 "OK" regions are infinite; `phi_min` is overestimated by up to 6.5e3 nats in 15 of 28.  There is
>   no argument that the default path cannot produce a false `REJECT_MODEL` (one plug-in fit converging
>   properly while the final fit stops at 0 would do it); I did not observe it.
> Why the division did not see it: every synthetic benchmark has free energies of order 1, and the
> public umbrella data have small bias constants (agreement with PyMBAR 5e-8 there is genuine).
> Consequence for the texts: the docstring of `classifier_evalue` ("P(log E >= log(1/alpha)) <= alpha,
> whatever the predictors") and the sentence "Implementation: `certificates.classifier_evalue`" under
> Theorem B5 are false for the implementation outside |f| of a few kT; `mbar`'s contract (raise if it
> did not converge) is violated; DEAD_ENDS E1 records as a fix the change that causes this.
> Suggested correction: (i) accept convergence only on `gnorm < tol`, or on `0 <= dec < 1e-14` with a
> finite, consistent solve; (ii) solve with the regularised/least-squares system already used in the
> constrained branch (which is why the profile solves did not fail), and catch `LinAlgError`;
> (iii) remove the constants before solving (use the exact equivariance: subtract a per-state reference
> energy, or start from a self-consistent/BAR-type initial point); (iv) in `LRRegion.__post_init__`
> start from the last plug-in and never declare `REJECT_MODEL` unless the fit is verified
> (`gnorm`) ; (v) `classifier_evalue` must abstain when its fit is not verified; (vi) add the unit test
> `mbar(U + off) == mbar(U) + off` for off of size 10^1..10^3 and rerun the model-check benchmark with
> offsets.
> 
> ### GAP
> 
> **G1. Theorem B2, boundedness criterion — false as written when batches do not all contain all
> states.**  The note says `C` is bounded modulo constants iff "the directed support graph of the
> evaluated samples (handoff E1)" is strongly connected, with recession function
> `h -> sum_n [max_{j: q_j(x_n)>0} h_j - h_{y_n}]`.  The maximum must run over
> `{j : beta^{b(n)}_j q_j(x_n) > 0}`: a state that is absent from the batch of sample n does not enter
> `Phi_b`.  Counter-example: K = 2, common support, two evaluated batches, the first containing only
> samples of state 0 and the second only samples of state 1; the E1 graph is complete, but each `Phi_b`
> is constant in f and `C` is everything.  This situation is inside the setting of B2/B3 (counts may be
> zero; "adaptive rounds must be mixed").  The code is right (`support_strongly_connected(-A, y)` uses
> the batchwise graph).  Correction: define the edge i -> j by "some evaluated draw of state i lies in a
> batch that contains state j and has q_j > 0".
> 
> **G2. Theorem B2, "for any set E of batches".**  True for a set fixed in advance or chosen
> predictably (inclusion of batch b decided from batches < b); false for a data-dependent set.  Exact
> enumeration (`check_partB.py`): including a batch only when its e-value exceeds 1 gives expectation up
> to 1.31; letting the plug-in see its own batch 1.52; choosing a sub-batch after the fact 1.11.  The
> new implementation paragraph says this; the theorem statement should.
> 
> **G3. Proposition S2 (SYNTHESIS), proof of the lower bound.**  The bridge instance needs three
> distinct states (a, b, m), so the proof does not cover K = 2, which the statement includes ("over all
> K-state instances").  The claim is true for K = 2: take `P_1` uniform on a block A, `P_2` uniform on
> A ∪ B, contrast `f_2 - f_1`; samples of state 1 are constant in the energies and the efficiency of s
> is exactly `s_2` (checked to 2e-15, `check_partC_synth.py`).  For K >= 3 the bridge instance checks
> out (|V*/V(s) - s_m| <= 9e-10 including allocations with zeros).
> 
> **G4. `lr_confidence_region(batches=...)` does not check that the index sets are disjoint.**  Passing
> cumulative prefixes ("the data so far" as successive rounds — a natural mistake with the adaptive
> interface) reuses samples on which the plug-in was fitted: P(truth not in region) = 0.103 at nominal
> 0.05 (1500 runs, `check_reuse.py`); disjoint rounds 0.000.  The theorem is not at fault; the code
> should refuse overlapping batches.
> 
> **G5. Proposition S4(ii).**  S4 requires a random *convex* region for the vector of averages
> `E_p phi`.  The region C of B2 is convex in the free energies f, i.e. in minus the logarithms of
> ratios of populations; its image in the space of averages is not convex in general (already for three
> populations and an ellipsoidal C), and `h_C(eta) = sup_{f in C} eta.f` is a support function in the
> wrong coordinates for `T(eta) = h_R(eta) + max_p E_p[f - eta.phi]`.  As written, (ii) is not
> justified; (i) (a box of B6 intervals) is.  I did not read Theorem 4.1 of the other division, so this
> rests on the form quoted in SYNTHESIS.md.
> 
> **G6. Width of the region of B2 is not a theorem.**  B2 "Size" and C3 state that the interval "has
> the rate sqrt(R_c/N) of the lower bound (C1)" and list it under "upper bounds that match".  What is
> proved is coverage; the width statement is a second-order expansion with an unproved bound on the
> regret rho, supported by the benchmark.  It should carry [N]/[C].  Two further inaccuracies in the
> same places: C1's rate is sqrt(V_c/N), not sqrt(R_c/N) (ratio 1.9 for strong overlap, 3-4 for
> adjacent states); and C3's "once N/R >~ d log K (B4's threshold)" is the threshold for B4 to apply,
> not for its leading term to dominate — the remainder `sqrt(R_c) kappa B` is below `sqrt(V_c/N)` only
> when N >~ (R_c/V_c) R d log^2(K/alpha).
> 
> **G7. Theorem A6.**  (a) "h_s its dual maximiser": when the sampled states form several overlap
> components (V finite because nu(C) = 0 on each), the maximiser is unique only up to one constant per
> component, and `g_k = Var_k(h_s)` of an unsampled state that straddles components depends on the
> choice.  (i) and (ii) hold for every choice, so nothing is false, but the statement and
> `population.state_variances` (pseudo-inverse choice) should say so.  (b) In the proof of (iii) the
> invariance is under functions constant on each overlap component of all states, not "on the union of
> supports"; the two coincide only under connected overlap.
> 
> **G8. A10, minimax for the maximum criterion.**  Sion is applied to `sum_i w_i V_i(s)` with `V_i`
> taking the value +infinity on parts of the boundary; with `0 * infinity = 0` the function is not upper
> semicontinuous in w there.  The identity is true (apply Sion on `{s >= eps}` and let eps -> 0 using
> A3(a) and monotone convergence of the concave upper semicontinuous functions of w), but that argument
> is missing.
> 
> **G9. A12(a), "A5-A8 hold for it with ||r_k||^2 := Gamma_k(r_k)".**  The third expression of A5, A7
> and A8 transfer verbatim.  The second expression of A5 and the equivalence theorem A6 are stated with
> `Var_k(h)`; for W they need the dual quadratic forms of the `Gamma_k`, not a renaming.
> 
> **G10. Theorem C2, hidden size condition.**  The two side conditions (`t D° <= 1/2`,
> `t <= |l_c(h°)|/(||c||_1 D°^2)`) mean B >= B_0(h°).  In infinite support `D°` may grow without bound
> as eta -> 0, so for a fixed budget the theorem is available only down to some eta(B).  The statement
> is correct as written; the summary sentences that quote it drop the condition.
> 
> ### OVERCLAIM
> 
> **O1. "Adaptive allocation cannot beat the optimal static allocation" / "at the level of the leading
> constant" / "adaptivity changes nothing at leading order"** (summary table of section 0; title and
> closing paragraph of C2; C4 item 3; SYNTHESIS S2).  What C2 proves: for B >= B_0, every strategy errs
> by at least `(tau/4) sqrt((1-eta) V*(B))` with probability `>= (1/2)(1 - 0.943 tau)` at one of two
> instances at distance O(B^{-1/2}) — for tau = 1/2, one eighth of `sqrt(V*)` with probability 0.26.
> That is "no gain beyond a universal constant factor, locally", which SYNTHESIS S2 item 2 states
> correctly.  A statement about the leading constant needs a local asymptotic minimax (van Trees or
> Hajek-Le Cam) argument for adaptive designs, which is not given.
> 
> **O2. SYNTHESIS S2, bold summary** "one round loses a factor up to K; two rounds lose nothing at
> leading order; more rounds cannot gain".  The middle clause is item 4, labelled [C]; the last clause is
> O1.  Only the first clause is proved.
> 
> **O3. SYNTHESIS S1'**, "... samples give accuracy eps asymptotically, and the region of Theorem B2
> certifies it".  The design of the bound leaves the target state K' unsampled; the region of B2
> constrains only states that occur as labels (it abstains otherwise), and where it applies it is
> 2-3 times wider, with no proved width.  A certified statement needs state K' sampled (constants
> change) or the bounded-ratio observable route of B6.
> 
> **O4. Lean labels in MATHEMATICS.md.**  A6 "[V for (i),(ii)]": `Model.efficiency_bound` and
> `Model.equivalence_sufficient` assume `0 < s_k` and `0 < t_k` for all k and a contrast; the note's own
> remark is that optimal designs sit on the boundary, where the formal statements do not apply
> ("costly ends": three of five coordinates are 0).  A4 "[V]" likewise covers the open orthant and
> contrasts; B1 "[V]" covers the inequality, not the identity `exp(-N KL(s||a))`.  C2's "Lean: ... is
> inside `Model.efficiency_bound`" is an internal `have` proved for `h = z_s`, not a declaration and not
> for a general `h°`.
> 
> **O5. `pilot_allocation` docstring** still says the mixture "guarantees V(final) <= V(uniform
> final)/safeguard whatever the pilot says".  For the integer counts this fails when a pilot count is 0
> or 1 (`check_code.py`: coordinatewise domination violated in 6309/9968 and 299/9963 random cases, never
> for pilot counts >= 2; through `pilot_allocation` itself 176 of 1500 runs, e.g. pilot (5,3,0), 2 more
> samples -> counts (0,2,0), true V = infinity against the bound 1.35).  The note now states the exact
> condition `(1-gamma) n0_k >= 1`; the docstring should too.
> 
> **O6. C1, "the finite-sample form of the local asymptotic minimax bound".**  It is a two-point bound
> with non-sharp constants (1/8, 0.26); "of the order of" is what is shown.
> 
> ### NUMBER
> 
> **N1.** MATHEMATICS B1: "exact enumeration of all samples on 286 small models (E <= 0.9999998 ...)".
> The test in the tree (`tests/test_certificates.py::test_evalue_exact_enumeration`) enumerates 116
> models (120 trials, 4 skipped); its largest expectation is 0.999999185 and its identity error 2.4e-15
> (`check_code.py`).
> **N2.** SYNTHESIS S3: "computed: V/Gamma = 0.0625 at Gamma >= 64".  Stored (and recomputed):
> 0.06348 at 64, 0.06274 at 256, 0.06256 at 1024; the limit is 1/16.  ("equals Gamma/16 (1+o(1))
> exactly" is also self-contradictory wording.)
> **N3.** LEAN_CORRESPONDENCE: "1464 lines"; `wc -l` gives 1468 (599 + 213 + 248 + 341 + 63 + 4).
> **N4.** DEAD_ENDS N8: "badly balanced overlap (Dirichlet models, bottleneck: 24-55 %)".  PILOT2:
> bottleneck 24 %, dirichlet0 52 %, dirichlet1 29 %, dirichlet2 11 % [CI 0.82-0.97]; 55 % is PILOT4 on
> dirichlet0.  One of the three Dirichlet models is outside the range and the range mixes two rules.
> **N5.** DEAD_ENDS N5: "rho ~ 32 at K = 26" and "1.9-2.2 times" are the subsampled run only (regret
> 59.3 for all snapshots, 42.6 for every tenth; sub-ladder ratios 2.24-2.27 and 1.75-2.33), while
> "4.6-7.1 times" in the same sentence spans all three runs.
> **N6.** MATHEMATICS A11 / DEAD_ENDS N2: "the worst by 35 %".  For the stored instance (reproduced:
> V = 399.65, 126.76 at the ends, 298.58 at weight 0.241, chord 192.55) 0.355 is the excess divided by
> the value at the mixture; divided by the chord it is 55 %.  The instance is not a midpoint.
> All other numbers I checked agree with the stored files: section 4.
> 
> ### MINOR
> 
> M1. A state that is absent from the earlier batches (no finite energy there) *and* from the current
> batch gives `-inf + inf = nan` and `ABSTAIN_PLUGIN` for good, although the state does not enter that
> batch (`check_code.py`, last test).  Conservative; avoidable by masking columns with beta = 0.
> M2. `LRRegion.interval` does not check that c sums to zero; `lr_confidence_region` and
> `LRRegion.__post_init__` do not catch `LinAlgError` (6 crashes in 216 awkward data sets,
> `check_interval.py`; see E1).
> M3. `interval`: the tolerance is `xtol * max(1, d0)` and `d0` comes from an ill-conditioned inverse in
> weak overlap; the result stays conservative but loose (gap-30 example: +-29.20 returned, about +-28.3
> exact), or infinite when `Rc` comes out non-positive.  The outward shift omits brentq's
> `rtol * |root|`; `kl_interval` shifts by a relative 1e-12 against brentq's absolute 2e-12.
> M4. `REJECT_MODEL` should be documented as an event of probability <= alpha under the model that is
> part of the non-coverage budget (it returns `(nan, nan)`).
> M5. SYNTHESIS S1': "oscillation" is additive for psi and multiplicative for the density ratio in one
> sentence.
> M6. LEAN table rows omit positivity hypotheses (`efficiency_bound`: s, t > 0; `kl_le_chisq`:
> reference law strictly positive).
> M7. A3(a): the radial limit needs no citation — V is nonincreasing and lower semicontinuous.
> M8. `optimal_allocation` returns V evaluated before the final rescaling of s (relative 1e-8).
> M9. C1 numerics: "the exact divergence is at most 0.31 (16/9) tau^2" is a property of that sample; at
> N = N_0 on my instances the largest ratio is 0.4155 (still below 1).
> M10. MATHEMATICS cites `docs/mbar/REVIEW_A.md`, which did not exist while I reviewed.
> 
> ## 3. Code against statements: what I looked for and what I found
> 
> * `lr_confidence_region`: plug-in of batch b uses `U[prev], labels[prev]` only; composition from
>   counts; batches by index; skipping only on reasons that depend on earlier batches (current code);
>   region and threshold agree with the definition in B2.  Correct in exact arithmetic for disjoint
>   batches in time order.  Through the code with an adversarial adaptive rule that knows the truth and
>   the current value of the e-process, stopping at the first exclusion (1200 runs each):
>   P(truth ever excluded) = 0.0067, 0.0000, 0.0058, 0.0000 (bound 0.05).  Defects: G4, M1, E1.
> * `LRRegion.interval`, version of `aa6fac4` (unconverged profile = inside): 216 awkward data sets
>   (K = 2..5, harmonic ladders up to spread 4.5, discrete models with zeros, 5-120 samples per state,
>   2/4/8 batches): 101 OK regions, 541 intervals, **0 witnesses outside a returned interval, 0 cases of
>   the truth inside the region but outside the interval**, 18 infinite intervals, 6 crashes.  Under
>   energy offsets, 314 further intervals against an exact reference: 0 too narrow.  The earlier
>   version (profile value used regardless of convergence) I had flagged from reading; it is fixed.
> * `observable_interval`: union bound alpha + alpha_obs is right (one region event, one two-sided
>   Chernoff event); `r = sup_C osc(f - f0)` is computed correctly from the pair matrix; dividing by
>   `s_k` is right (`E y(f*) = s_k E_k A`).  0 misses in 150 runs (median width 0.52: valid, wide).
>   `pmf_difference_interval` (new): logic and level accounting correct by reading.
> * `classifier_evalue`: in exact arithmetic the statistic is <= the e-value at the truth (largest
>   difference -2.9e-4 over 400 data sets, 0 rejections).  Invalid under E1.
> * `kl_interval`: exact binomial check, failure probability at most 0.55 of `2 e^{-t}`.
> * `pilot_allocation`: O5.  With every pilot count >= 2: 0 violations in 600 runs.
> * The division's 16 unit tests pass on the reviewed tree (136 s).
> 
> ## 4. Statements re-derived and found correct
> 
> Re-derived by hand before reading the given proof; "N" = also attacked numerically with my own code.
> * A1 (primal value, minimiser, convexity); A2 (weak and strong duality, gradient).
> * A3 (a) convex / lsc / monotone / degree -1 / radial limit; (b) finiteness criterion; (c) formula.
>   N: 5532 random finite models with zeros in P and in s, contrasts and observables: criterion (b)
>   agrees with the direct definition in all 5532 (1024 infinite); formula (c) agrees to 1.5e-12;
>   equals `c^T L^+ c - sum c^2/s` in the interior to 1.4e-10.
> * A4 concave, superadditive precision.  N: 7431 pairs on the closed orthant, largest violation 4e-14;
>   adversarial local search on 25 models 2e-15.
> * A5 three expressions (Sion hypotheses hold: Phi is real-valued, linear in s, concave and sup-norm
>   continuous in h).  N: joint convex programme, dual cone programme, group-norm programme agree to
>   5e-5 (solver tolerance); optimum on the boundary in 45 of 60 models.
> * A6 (i), (ii), (iii) and the bound with lower limits.  N: smallest slack of (i) +2e-7, of the
>   lower-limit bound +1e-5 (never negative); median (V*/V)/bound 1.24.
> * A7 monotone step and the equality case.  N: about 4000 allocations including boundary ones, no
>   increase.  A8.  A9 for real-valued allocations and the integer condition `(1-gamma) n0_k >= 1`.
> * A11: the stored counterexample (chains reversible, stationary laws equal to P; values reproduced).
>   A12 (a) convexity and W <= V^corr, (b), (c).
> * B0: handoff B3 (matrix Chernoff exponent 0.6137 N/R from `mu_min/R' = 4N/R`; Bernstein with
>   dimension factor K; `delta <= 1/sqrt6 + 1/12`; coefficient 4 log 2) and handoff C1 (union over
>   2^K tails, cut norm, localisation `1 - e^{-osc} <= Rmax eps`): both as the table says.  Also B4's
>   failure budget and the 0.56 constant.
> * B1 including the identity.  N: full enumeration, 333 models, largest expectation 0.99139;
>   predictor and tilt optimised adversarially: supremum 1.0000000000; identity to 5e-15; wrong
>   proportions in the statistic give exp(N KL(s||s')) = 1.6875 > 1 (so batch proportions are needed,
>   and the code uses them).
> * B2 coverage, convexity, simultaneity; B2' ; B3 (N: two rounds, composition and plug-in chosen
>   adversarially from the first round, exact: 0.9944 <= 1); B5; B6; B7 (a), (b), (c).
> * C1: every constant (density in [3/4, 5/4]; `0 <= u - log(1+u) <= 2u^2`; separation >= tV/2;
>   chi^2 = t^2 Var_k/(1+u_k)^2 <= (16/9) t^2 Var_k; KL <= (16/9) tau^2; Pinsker 2 sqrt2/3; Le Cam
>   radius tau/4; 0.2643 at tau = 1/2; D <= R_c for a unit pair contrast, with equality possible).
>   N at N = N_0: 8766 cases, |dG_t/dG - 1| <= 0.2500, separation >= 1.88 times the claimed bound,
>   KL <= 0.4155 (16/9) tau^2, max D/R_c = 1.000000.
> * C2: the divergence bound holds for every strategy (it uses only `Var_k(h°) <= M° a_k` and
>   `sum a_k N_k <= B`), the KL direction is consistent (`KL(P_0||P_t) = sum_k E_0[N_k] KL(p_k||p_{k,t})`,
>   bounded by `chi^2(p_k||p_{k,t})`), separation right.  N: 80 cases.
> * S1 (also for sequences with repeated states: removing a loop keeps a subset of the steps).  N: 2528
>   cases, max V/bound = 1.000000 (attained when only the source is sampled).  S1' (Bhatia-Davis:
>   maximum of (ea-1)(1-a) is (e-1)^2/(4e) = 0.27154; the density ratio has sup/inf <= e).  N: random
>   ladders, largest step 0.258, V_uniform <= 0.73 of the bound.  S1'' (n_1 makes the union failure
>   exactly delta/2; log error <= eps/2), conditional on Theorem 11.25.  S2 for K >= 3.  S3 numbers.
>   S4 statement with (i).
> * Numbers that match the stored files: certificates_coverage (coverage 100 %, always finite, LR8/ASY
>   2.05-3.06, C1 abstains 4/11 and is 1.39-5.77 times wider, C2 2.41-8.27; v2 identical);
>   lower_bounds_and_chains (0.302; 0.956-1.043; 0.9999999999997; 768/3000; 0.355; 7e-16);
>   synthesis_checks (0.943; 1.0000000098; 5.4-13.6 % on 27 instances; 4.0; 6.7e-16; 0.2);
>   allocation_benchmark_2000 and costpilot2 (every figure of N7-N11, "6 of 8 systems", oracle design
>   (0, 12900, 0, 12900, 0), bound 0.487 against 0.764); robustness (N12, N14 including the 0.99 rows);
>   public_umbrella (84 %, 0.370, 0.069, 4.64-7.09); B4's sqrt(R_c/V_c) = 1.02, 1.07, 1.31, 1.88, 1.90
>   (recomputed: 1.023, 1.071, 1.307, 1.875, 1.901) and 3.0, 4.1 for adjacent states.
> * Lean (9 declarations read against the table): `precision_superadditive`, `efficiency_bound`,
>   `equivalence_sufficient`, `rounding_bound`, `V_convex`, `lr_family_evalue`, `lr_region_coverage`
>   (one batch, fixed predictor — as the table says), `chisq_tilt`, `le_cam`, `kl_le_chisq`,
>   `log_one_add_ge`: each states what the table says (M6, O4 apart).  49 `#print axioms` lines.
> 
> ## 5. Not checked
> 
> * The Lean build and axiom audit (not run, by instruction); the other ~40 declarations.
> * Handoff statements other than B3, B4's budget, B5's constant and C1; handoff D1, D2, G1, E1-E3.
> * Imported theorems of other divisions (11.25, 11.52-11.54, 11.86, H1/H5, Theorem E, 4.1, 5.4, 6.1)
>   and every citation and priority claim (Gill-Vardi-Wellner Problem 6.1, Fellman, Armstrong 2022,
>   Micaletto 2026, the numbering of Yu 1994 Lemma 4.1); PRIOR_ART.md, VALIDATION.md, FINAL_REPORT.md.
> * External theorems used as [X]: Sion, Ville, Pinsker, the chain rule for adaptive sampling, matrix
>   Chernoff/Bernstein, Berry-Esseen — statements taken as given.
> * Measure-theoretic details beyond finite support (measurability of predictors, sigma-finiteness,
>   truncation arguments for unbounded dual maximisers).
> * Figures that come from the unit tests and are not stored (3e-12 on 400 models, 2e-8, 3e-6, 3e-15,
>   2.4e-7, PyMBAR standard errors to 13 digits), the five-state example of DEAD_ENDS N1, and the
>   reruns of the benchmark scripts themselves.
> * `restricted_interval`, `bootstrap_interval`, `asymptotic_interval`, the `max` criterion of
>   `optimal_allocation`: read, not run.  Interval tests stop at K = 5.
> * Behaviour of the region when the within-state order of the input is not the sampling order
>   (e.g. sorted input); correlated samples.
> * Whether the default path can produce a false `REJECT_MODEL` under E1 (not observed, not excluded).
