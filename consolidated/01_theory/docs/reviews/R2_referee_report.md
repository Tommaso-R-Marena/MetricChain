# R2 — Independent referee report on the second research phase

Subject: `docs/THEORY_REPORT.md` §§10–12 and the corrected paragraphs of §§2.3–2.4, 3.2, 3.4; the Lean
modules `CertificationGeometry`, `CertificateNotions`, `ConditionalEnvelope`, `CertificateComplexity`,
`ExponentialWeights`, `ProductRates`, `BestFirst`, `ThermalRobustness`, `SecondOrderEnvelope`,
`PartitionProduct`, and the two modules that appeared during the review, `HigherOrderEnvelope` and
`SampledSandwich`; harness tests `XI.1`–`XI.13`, `DEAD.6`–`DEAD.9`; README "Status", `BLUEPRINT.md` §6.3, §6.6, §9,
`DEAD_ENDS.md` D21–D28.  I had no part in the work.

**Repository state.**  The tree changed twice while I worked.

| time (UTC, 2026-11-24) | `git log --oneline \| head -1` | `git status --short \| wc -l` |
|---|---|---|
| 16:38 (start) | `477391f Final-check repairs: audit walk by module, strict reference checker` | 24 |
| 17:07 | `607de4a Cycle 7: independent referee report, reclassification, certification geometry` | 2, later 6 |
| 17:31 (final) | `ee2053f Cycle 7, second checkpoint: order-m remainder, sampled sandwich, attribution` | 0 (1 with this file) |

Everything below refers to `ee2053f`; line numbers are those of that commit.  `SampledSandwich.lean` and §11.9
(Theorem 11.21, row G10) **were present at the end** and are reviewed.  Two things I had found against `607de4a`
were repaired by the authors in `ee2053f` before this report was written and are therefore not listed as errors:
the attribution of the finite-temperature exponent (now credited to Merhav 2011) and "every `β`" in Theorem 11.14
(now `β ≥ 0`, any coupling).

**Method.**  (i) Statements of all cited Lean declarations read against the prose.  (ii) Three scratch files
outside `proofs/` checked with `lake env lean` against the final tree (no `lake build`): 76 cited declarations exist
and depend only on `propext`, `Classical.choice`, `Quot.sound`; four lemmas of my own are machine-checked there
(Appendix A).  (iii) Independent numerics, own code, exact arithmetic or LP/ILP where possible (§5).  (iv) One
primary source read for the novelty question (Merhav, arXiv:1103.2882v1, text extracted from the PDF).

## 0. Summary

* No machine-checked statement was found false.  Every `[V]` name cited in §§10–11 exists with the stated meaning,
  with the exceptions listed under m1, m4, m5, m10 (prose slightly stronger than, or differently scoped from, the
  Lean statement).
* **One paper theorem is false as stated**: Theorem 11.15 with the hypothesis "`ε = o(n)`".  For `ε = 0` every
  certificate of `ln Z` is the whole space (`N_Z = kⁿ`, machine-checked in Appendix A) while `R_β < ln k`.  The
  proof given is correct under the additional hypothesis `ln(1/ε_n) = o(n)`.
* **Four major overstatements**: the doubling-space remark after Theorem 11.11 is false in the paper's own
  grey-box setting; the planning formula of `BLUEPRINT.md` §6.6 misquotes Theorem 11.9 and is wrong in three ways;
  "second-order envelopes: the way out" omits that the remainder is quadratic in the Hamming distance, so that with
  non-sparse constants the exponential covering problem returns; the "exponential separation" of the partition
  kernel is an exact-endpoint statement whose hypothesis `Rigid` is satisfied by a product measure.
* Theorem 11.5 (three notions) is true but not sharp: in fact `N_value = N_point` and `N_point = max(1, N_config)`
  (machine-checked exchange lemmas, Appendix A).  The "three notions" are one number.
* Novelty: the exponent formulas are corollaries of the type covering lemma (zero temperature) and of Merhav's
  2011 exponential-moment theorem (finite temperature, confirmed in the primary text); the one-shot converses are
  Chernoff/Hölder relaxations of the covering LP.  What is not in print, as far as I can tell, is the dictionary
  (certificate ↔ covering code with the gap as distortion budget), the dichotomy "sharp or exponential", the
  grey-box formulation, and the machine-checked statements.  This is a coherent note, not a theorem-driven paper.

## 1. Verdict per result

| # | correct? | depth | novelty | one-line justification |
|---|---|---|---|---|
| G1 slack covering, three notions | correct; Thm 11.5 not sharp | trivial | new formulation of a known notion | `isCertificate_iff_cover` is a rearrangement of `UB − min_y(E − s(A,·)) ≤ ε` (no hypothesis on `d`, `g`); the three notions collapse: `N_val = N_point = max(1, N_conf)` (App. A) |
| G2 conditional envelope | correct | routine | known (minimal STN; McShane) | Lean matches prose; LIPO attribution attached to the wrong statement (m3) |
| G3 dual lower bounds | correct | routine | known tools | (a)–(c) are feasible points of the covering-LP dual (checked: `w = e^{−tε} v/B` is feasible); Chernoff step = Csiszár's dual bound |
| G4 dichotomy + exponent (Thm 11.7–11.9) | correct; proof of 11.9 incomplete for unequal sites | routine (an exercise in the method of types after the reformulation) | formula known in spirit (Csiszár 1998, consequence of Lemma VI.1, with a type-dependent level); identification and dichotomy apparently new | reproduced numerically: closed forms, primal = dual, layer counts `0.2073, 0.1994, 0.1947, 0.1919`; needs `κ < 1` (counterexample at `κ = 1`) |
| G5 hardness | correct | trivial | known in spirit | brute force on 300 graphs agrees; complexity reading is [K] |
| G6 best-first, resource augmentation | Lean theorem correct; remark on doubling spaces **false** (M1); "attained" only on a two-point instance | routine (packing against a cover, Plesník/Hochbaum–Shmoys) | new formulation | 16 277 runs, no violation, 298 equalities; comparison class up to 14× larger than `N_cov`; constants 4 and 6 not shown necessary |
| G7 finite temperature (Thm 11.12–11.15) | `[V]` parts correct; **Thm 11.15 false as stated** (C1), correct with `ln(1/ε_n) = o(n)` | routine | exponent formula known (Merhav 2011, eq. (37) and first example); one-shot Hölder converse and the identification apparently new | identity primal = dual to `2·10⁻⁶` on 14 sites; quoted values reproduced; `N_Z(0) = \|X\|` |
| G8 second/higher-order envelopes | correct (LP-verified for `m = 2, 3`) | routine (discrete Taylor remainder) | anchored decomposition known; class and exact reduction apparently new | "the way out" overstated (M3); `[V]` on attainment for general ball data covers only zero data (m1) |
| G9 cut and elimination rules | correct | trivial (cut), routine (elimination = transfer matrix) | known | separation is exact-endpoint only and `Rigid` is representation-dependent (M4); treewidth ≤ 2 is [P] (numerically confirmed) |
| G10 sampled sandwich (Thm 11.21) | correct | routine (Chernoff + McDiarmid mgf) | known | exact enumeration, 10 577 cases, no violation; product hypothesis necessary |

## 2. Errors and overstatements

### CRITICAL

**C1. Theorem 11.15 is false for `ε_n → 0` faster than `e^{−o(n)}`, in particular for `ε = 0`.**
Location: `THEORY_REPORT.md` 1487–1492 ("accuracy `ε = o(n)`"); the exponent is quoted without the restriction
in row G7 (1152) and README 91–95.

*Counterexample.*  Let the slack be positive off the diagonal and `β > 0`.  If `Z(f+L_A) ≤ Z(f+U_A)` (certificate of
`ln Z` with `ε = 0`), then `L_A = U_A` pointwise, hence `s(A,y) = 0` for all `y`, hence `A = X`
(`exact_free_energy_certificate_eq_univ`, Appendix A; also brute force, §5).  So `N_Z(0) = kⁿ` and
`n⁻¹ ln N_Z = ln k`.  But `R_β ≤ max_Q H(Q) = ln k` with equality only if `π` is uniform; for the report's own
example (`e/c = 1/2`) `R_β = 0.666, 0.482, 0.216 < ln 2`.  More generally, a two-sided certificate forces
`π(Aᶜ) ≤ ε/(1 − e^{−β s_min})`, so for `ε_n = e^{−λn}` the set `A` contains at least half of every type class with
`KL(Q‖π) < λ`, and the exponent is at least `max{H(Q) : KL(Q‖π) < λ}`, which equals `ln k` for
`λ > KL(uniform‖π)`.

*What the proof shows.*  The construction in the proof gives `Z_hi/Z ≤ 1 + 1/(n+1)` and `Z_lo/Z ≥ 1 − 1/(n+1)`,
i.e. accuracy `≈ 2/n`; it does not reach smaller `ε`.

*Fix.*  State the theorem for `ε_n = o(n)` **and** `ln(1/ε_n) = o(n)` (e.g. `ε_n ≥ n^{−m}`).  In the proof replace
the level by `D_Q = max(0, KL(Q‖π)/β − a_n)`, `a_n = [(k+1) ln(n+1) + ln(4/ε_n)]/(nβ) → 0`; then
`Z_hi/Z ≤ 1 + ε_n/4`, `Z_lo/Z ≥ 1 − ε_n/4`.  Add the remark that for exponentially small `ε_n` the exponent is
different and tends to `ln k`.  (Theorem 11.9 does not have this problem: `ε = 0` is allowed there.)

### MAJOR

**M1. "In a doubling space the shrinkage converts into a constant factor" is false in the grey-box setting.**
Location: `THEORY_REPORT.md` 1418–1419 (unmarked remark after Theorem 11.11); contradicted by §12 item 2
(1711–1714), which lists the same statement, for `f ≡ 0` only, as "sketched, unverified".

*Counterexample.*  `X = {0} ∪ {2^{−i} : 1 ≤ i ≤ m} ⊂ ℝ` with `d(x,y) = |x−y|` (doubling), `f(x) = x`, `g ≡ 0`
(`κ = 0`, `θ = 1/4`), `ε = 2^{−m−3}`.  The point `0` covers everything (`s(0,y) = y ≤ gap(y) + ε`), so
`N_cov = N_point = 1`.  At the shrunk radius `θ(gap(y) + ε/6) = y/4 + ε/24 < y/2` the point `y = 2^{−i}` is covered
only by itself (its nearest neighbours are `y/2` and `2y`), and so is `0`; every shrunk cover has `m + 1` points.
Computed (§5): `m = 4, 8, 12, 16` give `N_cov = 1`, `N_shrunk = 5, 9, 13, 17`; best-first search uses at most 2
evaluations from every start.  The ratio is unbounded on a subset of the line.

*Fix.*  Delete the sentence, or restrict it to `f ≡ 0` and mark it as a conjecture.  State next to Theorem 11.11
that the comparison class can be arbitrarily larger than `N_cov` even in dimension one when `f` is not constant.

**M2. `BLUEPRINT.md` §6.6, Step 2 misstates Theorem 11.9.**
Location: `BLUEPRINT.md` 480–483: "On independent sites the bound is exponentially tight: the count is one if every
site is sharp and otherwise about `exp(Σ_i r_i)` with `r_i = max_t [ln Z_i^{gap}(t) − ln Z_i^{slack}(t)]`".
Three independent errors:

1. *Per-site maximisation.*  Theorem 11.9 has one common `t`.  Type A (`e = 0.5, c = 1`) and type B (`e = 5, c = 10`),
   `m` binary sites of each, zero residual: `Σ_i max_t r_i = 0.3765 m`, `max_t Σ_i r_i = 0.2329 m`.  Exact orbit
   counts (§5): `(1/m) ln N_frac ∈ [0.2472, 0.2852]` at `m = 150`, hence `(1/m) ln N_cov ≤ 0.321 < 0.3765`.  The
   blueprint's number is not even a lower bound; it overshoots by a factor `≥ e^{8}` at `m = 150`.
2. *Boltzmann weights are not optimal for `k ≥ 3`.*  One site with gaps `(0, 0.5, 3)`, `c = 1`, zero residual:
   `R* = 0.1882` (dual LP = primal maximum over types), the partition-function bound gives `0.1066`.
3. *Nor for sites with a residual, even binary ones.*  `φ = (0, 0.677)`, `γ = (0, 0.644)`, `c = 1` (non-sharp,
   `κ = 0.644`): `R* = 0.0252`, the Boltzmann bound is `≤ 0` for every `t`.  Three-state example: `φ = (0, .5, .9)`,
   `γ = (0, .3, −.2)`: `R* = 0.1037`, Boltzmann `0`.  In addition `partition_bound_hamming` replaces the slack by
   `(1−κ)c`, which loses more.

*Fix.*  "A lower bound, exponentially tight for two-state sites with zero residual; in general use
`max_t Σ_i max_v r_i(t; v)` (one LP per site and `t`)".  The same qualification is needed for the sentence
"The exponent is a free-energy difference: with Boltzmann weights …" (`THEORY_REPORT.md` 1380–1382) and for
"two-state sites: always" (1699), which holds for zero residual only.

**M3. "Second-order envelopes: the way out" omits the limitation that decides whether it is one.**
Locations: `THEORY_REPORT.md` 1548–1555, 1600–1607; README 95–96; `DEAD_ENDS.md` 543–546 ("Ways out that work").

Theorems 11.16–11.17 are correct.  What is not said: the star envelope has half-width `Σ_{i<j changed} c_ij`,
quadratic in the Hamming distance, and further evaluations do not remove this.  For `n` binary sites and
`c_ij = c` for all pairs, the function `g'(x) = −c·C(|x|−1, 2)` (`0` at `|x| ≤ 1`) has all mixed second differences
of absolute value `0` or `c`, vanishes on the **whole Hamming ball of radius 2** around `x₀ = 0`, and equals
`−c(w−1)(w−2)/2` at weight `w`.  LP over the class with all evaluated values zero (§5, `n = 5, 6`, `c = 1`): the
smallest possible residual at weight `w` is `−C(w,2)` given the star, `−C(w−1,2)` given the full radius-2 ball
(`1+n+C(n,2)` evaluations), and `−min(C(w,2), C(n−w,2))` given two stars at opposite corners — the better of the
two single-star bounds, no more.  With `f(x) = e|x|` and zero true residual the radius-2 ball does not certify once
`n ≥ 2e/c + 3`.  Two opposite stars do not once `n ≥ 6e/c + 6`: for a set `S` of `w ≤ (n+2)/3` sites the function
`−c·C(a,2)·C(n−w−b,2)/C(n−w,2)` (`a`, `b` the numbers of changed sites inside and outside `S`) is in the class,
vanishes on both stars and equals `−c·C(w,2)` at the indicator of `S`.  (Membership: the mixed differences are
`c·C(n−w−b,2)/C(n−w,2)` for two sites in `S`, `c·C(a,2)/C(n−w,2)` for two sites outside `S`, and
`c·a(n−w−b−1)/C(n−w,2) ≤ 2c(w−1)/(n−w)` for one of each; all are `≤ c` iff `w ≤ (n+2)/3`.  Also checked by brute
force over all contexts for `n ≤ 10`.)  In both cases the lower model is `≤ E_min − c` at and beyond the
threshold, so the statement holds for every `ε < c`.
A star certifies iff the second-order sharp-minimum condition holds; for an additive known part a sufficient
condition is the row-sum condition `½ Σ_j c_ij ≤` measured single-site excitation energy.  For non-sparse
constants star-type data lead back to covering, now with radius `≈ √(2·gap/c)`; whether other evaluation sets do
better is open (§6).  `prior_art/L5` P9 says as much ("the envelope is small only near an anchor … optimal anchor
placement is a covering problem"); the report does not.

Related: the loop `STARCERT` (`BLUEPRINT.md` 497–510) does not terminate when the minimiser `y` of the lower model
is not better than `x₀` and the gap exceeds `eps` (same `x₀`, same star, same `y` forever); the dense example above
is such an instance.

*Fix.*  State the row-sum condition and the dense counterexample in §11.7; replace "the way out" by "a way out
under weak second-order coupling"; give `STARCERT` a fallback (branching or first-order anchors).

**M4. The "exponential separation" of the partition kernel is weaker than its description.**
Locations: `THEORY_REPORT.md` row G9 (1155), 1629–1638; `BLUEPRINT.md` §9 row "partition kernel without
decomposition rules" (665).

`zverify2_elementary_exact_leaves`, `chain_separation`, `ferroChain_separation` are true.  Two reservations.

1. *`WInstance.Rigid` is a property of the representation, not of the model.*  It asks that one of the two
   **ordered** factors `W i j`, `W j i` distinguishes the states of `i`.  The instance `W₀₁(a,b) = 2^{a+2b}`,
   `W₁₀(b,a) = 2^{−(a+2b)}`, `w ≡ 1` on two binary sites is `Pos` and `Rigid`, every configuration has weight `1`
   (two independent uniform sites, `Z = 4`), and the theorem says that every elementary certificate with exact lower
   end has `4 = 2²` leaves (`gauge_trivial_separation`, Appendix A).  The same construction satisfies the
   hypotheses of `chain_separation` for every length.  So what is measured there is that the leaf rule bounds the
   two orientations of a pair separately; a normalisation step would remove it.  For `ferroChainW` the interaction
   is genuine and the statement is as intended.
2. *Exact lower endpoint only.*  A certificate whose lower end is `(1 − 10⁻⁹) Z` is outside the theorem.  At finite
   temperature approximate enclosures are the normal case (the thermal prune rule is approximate by design), so
   this is not the analogue of the tropical separation, where exactness of the bound is the natural target.  R1's
   exhaustive search (`n ≤ 5`) suggests a robust version is true; none is proved.

*Fix.*  Define rigidity through the symmetrised factor `W_ij(a,b)·W_ji(b,a)`; say "exact lower endpoint" wherever
the separation is advertised; list the approximate version as open.

### MINOR

* **m1. Theorem 11.18, `[V]` tag (1582–1589).**  `higherOrder_remainder` is the stated bound.
  `higherOrder_remainder_sharp` proves attainment for the function `higherRemainder` itself, i.e. for **zero** ball
  data.  "A member of the class with the same ball data" for an arbitrary `g` needs
  `HigherDiffBound m (anchoredInterp m g x₀) 0` and additivity; neither is in the file.  The statement is true
  (LP check for `m = 3`, §5); for `m = 2` it is fully formalised (`secondOrder_lower_attained`).
* **m2. Theorem 11.5 is not sharp (1254–1266, row G1).**  `N_value = N_point` and `N_config ≥ 1 ⟹ N_point ≤ N_config`
  (exchange the anchor that attains `U_A` at the candidate; Appendix A; 1 500 instances by brute force).  A
  configuration certificate saves an evaluation only when no evaluation is needed at all (`N_config = 0`,
  Theorem 2.4).  `IsConfigCertificate` requires a nonempty `A`, so inside the Lean development the "+1" of
  `isCertificate_insert_of_isConfigCertificate` is never needed; the witness `config_certificate_skips_forced_point`
  uses one evaluation that carries no information (`condEnv_singleton`).
* **m3. Misattribution (1221).**  The "potential maximizers" lemma of LIPO (∃ a consistent function maximised at
  `x`) is the query-model contact theorem (Theorem 2.6), not the "first statement" of Theorem 11.2 (∀ consistent
  residuals).
* **m4. `thermal_binary_single_tight` (1501–1504).**  "With equality for the single evaluation of the ground state
  at `ε = n ln(6/5)`" is true for the hypothesis `Z_hi ≤ e^ε Z`, which is not computable from the evaluations.  As
  a certificate of `ln Z` (`Z_hi ≤ e^ε Z_lo`) the single evaluation has width `n ln(4/3)`
  (`Z_hi = (3/2)ⁿ`, `Z_lo = (9/8)ⁿ`).  "Accuracy can be traded for evaluations only at this exponential rate" is
  not a proved statement.
* **m5. Row G6, "augmentation is necessary" under `[V]`.**  None of the three cited theorems shows necessity;
  it is shown by the hub family (`DEAD.6`, B9).  `bestFirst_card_le_sharp` is a two-point instance with `|C| = 1`:
  it shows that the `+1` is needed, not that `θ` or `ε/6` are.  Experiment (§5): with radii `2θ(gap + ε/6)` or
  `θ(gap + ε)` no violation in 900 instances; `3θ`: 6 violations; `4θ`: 14.  The constants are probably not tight.
* **m6. Hansen–Jaumard–Lu (1422).**  Theorem 11.11 concerns point certificates; the matching one-dimensional
  statement is `n_PY ≤ 4 n_B + 1`, not `n_P ≤ 2 n_B + 1` (both are in the abstract quoted in `prior_art/L4`).
* **m7. §12 item 1 (1691).**  `max_t [p_E(t) − ln(1+(k−1)e^{−tc})] = sup_ν [h(ν) − h_b(δ_ν) − δ_ν ln(k−1)]` needs
  the restriction `δ_ν ≤ (k−1)/k` (from `t ≥ 0`); for `δ_ν > 1` the right-hand side is undefined, and without the
  restriction it can exceed the left-hand side (independent two-state sites with `e = 2c`, a sharp landscape: the
  left side is `0`; at `ν` = Bernoulli(1/2), `δ_ν = 1`, the right side is `ln 2`).
* **m8. "The contrast with linear information" (1541–1546).**  "Includes the accuracy `β²c²/8` per site when `βc`
  is small" needs `H(π)` larger than about `(βc/(8(1−κ))) ln(1/βc)`; for a cold sharp site (`e^{−βe} ≤ βc/8`) the
  single evaluation of the ground state already reaches that accuracy.  The concrete instance of §11.9
  (`0.0601 n`, `exp(0.122 n − 1.39 η)`) is correct.
* **m9. §2.4 bullets (354–360).**  The separation `σ` must be read as `d(a,y) ≥ σ` (from the anchors to `y`); with
  the transposed reading the configuration bullet fails for asymmetric envelopes (22 violating cases in 400
  random instances).  The configuration bullet is not formalised and carries no status mark; it is true (three-line
  proof, brute force).
* **m10. README 77, 98–99; `THEORY_REPORT.md` 1075.**  "Exact on … interaction graphs of treewidth at most two" is
  `[P]` beyond chains (confirmed numerically on 120 random partial 2-trees).  "Upper bounds … checked numerically":
  for Theorem 11.15 only the single-letter identity was computed (B8); no finite-`n` check of achievability exists
  in the repository (mine: §5).
* **m11. "Otherwise exponentially many" (README 90; `BLUEPRINT.md` 661; `THEORY_REPORT.md` 1378–1380).**
  Exponential in the number of non-sharp sites; machine-checked only for identical sites, zero residual, `ε = 0`.
* **m12. §8 (1078) against §12.3.**  Checking a certificate with anchors `A` on a product space is
  `min_y max_{a∈A}` of pairwise models, coNP-hard in general (as §12.3 says), not "a pairwise optimisation problem";
  and in the non-sharp regime `|A|` itself is exponential.
* **m13. `DEAD_ENDS.md` D22 (445–446) against `THEORY_REPORT.md` 1637–1638.**  "Lower bounds for connected families … remain
  open" and "it is proved on a connected family" need the same qualifier (elementary certificates, exact end).
* **m14. `BLUEPRINT.md` 477–479.**  The planning bound drops the factor `e^{−t(UB−LB)}` that its own inequality
  for `gap(y)` produces.
* **m15. Theorem 11.9, wording (1343–1344).**  "Between `exp(Σ_{non-sharp} r_i)` and `∏_{non-sharp} k_i`": the `r_i`
  must be taken at a common `t` (see M2.1).
* **m16. Theorem 11.21 / §11.9.**  Correct.  Unstated conditions: exact sampling from the product reference, exact
  evaluation of `Δ`, `Z₀` known; the accuracy floor `β²C/8` cannot be reduced by more samples (stated in the
  blueprint, not in the theorem).
* **m17. Theorem 11.9, proof (1348–1364).**  The upper bound for sites of unequal type is asserted, not proved;
  the argument is supplied in §3.  The statement is correct.

## 3. The paper proofs

**Theorem 11.9.**  Statement correct under the stated hypotheses (`g` additive, `κ < 1`, `c_i > 0`, finitely many
types).
* *Dual formula.*  `R(P; ρ, 0) = max {Σ_s P(s) ln(w(s)/P(s)) : t ≥ 0, w ≥ 0, Σ_s w(s) e^{−tρ(a,s)} ≤ 1 ∀a}`
  (Csiszár with `w = P e^{α}`); the maximum over `P` is `ln Σ_s w(s)` by Gibbs' inequality; both are suprema, so
  the exchange is free.  The credit distortion causes no difficulty: `ρ ≤ 0` on the diagonal, and the substitution
  `w ↦ w e^{−t·gap}` turns it into the nonnegative distortion `s` at the type-dependent level `E_P[gap]`.
  Numerically: primal maximum over types = dual LP to `10⁻⁴` on five three-state sites, symmetric and asymmetric
  slack.
* *Upper bound, identical sites.*  Csiszár–Körner Lemma 9.1 is uniform in the type and in the level
  (`n ≥ n₀(d, δ)`), which is what the type-dependent level needs; this should be said.  Continuity of `R(P, D)` at
  `D = 0` holds for finite alphabets because every letter reproduces itself at zero slack.
* *Upper bound, unequal sites — missing.*  The text proves nothing here.  The argument that closes it: for a joint
  type `(P_j)` cover each `T_{P_j}` at level `D_j` and take the product; minimise `Σ_j λ_j R_j(P_j, D_j)` over
  allocations with `Σ_j λ_j D_j = Σ_j λ_j E_{P_j}[gap_j]` (`λ_j` the fraction of sites of type `j`); by convexity
  in `D_j` the minimum equals `max_t Σ_j λ_j [F_j(P_j,t) − t E_{P_j} gap_j]`, `F_j(P,t)` the Csiszár dual function
  of type `j` for the distortion `s_j`; maximise over `(P_j)`.  This gives `max_t Σ_i max_v r_i(t;v)`.
  The sentence about sources with memory only shows that product weights are the best dual weights; it is not an
  achievability argument.  Numerically the common-slope value is the right one (M2.1).
* *Dichotomy.*  Correct: `r_i(·; v)` is concave with `r_i(0) = 0` and slope `min_a E_v ρ_i(a,·)`; by the minimax
  theorem the value is `≤ 0` iff some mixed centre `Q` has `Σ_a Q(a) ρ(a,s) ≤ 0` for all `s`; at `s = x*` this
  forces `Q = δ_{x*}` because the slack is positive off the diagonal; then the condition is sharpness.  The
  hypothesis `κ < 1` is necessary: `φ = (0,0)`, `γ = (0,c)` has `R* = 0` (the letter `1` covers both letters at
  zero slack) although the site is not sharp; then `N_cov = 1 < N_point = 2`.
* *"`N_cov = 1` or exponential".*  Correct as "one, or at least `exp(c·#non-sharp − tε)`" for finitely many types;
  with a bounded number of non-sharp sites the count is bounded.
* *Binary formula.*  Correct; the maximiser has `μ ≤ 1/(1+ρ)`, where the Shannon lower bound is tight.

**Theorem 11.15.**  See C1 for the hypothesis.  The single-letter identity is correct: with `D = KL(Q‖π)/β` the dual
objective is `(1 + t/β)[Σ_s Q ln(w^{β/(β+t)} π^{t/(β+t)}) + H(Q)]`, concave in `Q`, maximum
`((β+t)/β) ln Σ_s π^{t/(β+t)} w^{β/(β+t)}`.  The lower bound is `thermal_product_exp_weights` rearranged.  The upper
bound is correct for `ε_n ≥ 2/n` as written.  `R_β ≥ H(π)` needs positive slack off the diagonal (stated).
`R_β → R*`: the level `KL(Q‖π)/β = E_Q[gap] − (H(Q) − ln(Z e^{βE*}))/β` converges uniformly in `Q`, and `R` is
jointly continuous; correct.  The formula is the zero of Merhav's exponent
`max_Q [α D_Q(R) − D(Q‖P)]` in `R` (arXiv:1103.2882v1, eq. (37) and the paragraph "The first example is that of
fixed-rate rate-distortion coding … conditions (a) and (b) with `λ(Q) = D_Q(R)` … type covering lemma"), with the
same construction (cover each type class at a type-dependent radius).  The report's `[K, not verified in detail]`
can be replaced by this reference; note that Merhav states the example without proof ("it is not difficult to
see", "a straightforward exercise").

**Theorem 11.18.**  Correct, including attainment for arbitrary ball data (`c_T ≥ 0`): for `|T| = |T'| = m`,
`T ≠ T'`, the mixed difference over `T` of `∏_{i∈T'} [x_i ≠ x₀_i]` vanishes, so the remainder function has order-`m`
differences `c_T·∏(±1 or 0)`, and the interpolant has none.  The induction in the text is sound once "bounded by
`c_T`" is read as "for every context and every pair of states".  LP over the class: `m = 2, 3`, mixed alphabets,
both extremes.

**The [K] halves.**  Theorem 11.6: Lovász/Chvátal bound and dual feasibility are standard and correctly used.
Theorem 11.14: Donsker–Varadhan, exchange of suprema and Kantorovich–Rubinstein duality for quasi-metrics give the
stated identity for `β ≥ 0`; the orientation remark is right.

**§12, conjectural remarks.**  Item 1(c): see m7; "type covering for processes" is not an off-the-shelf lemma for
Markov types with a distortion budget fixed by the pair marginal, so the conjecture `sup_ν R_ν(δ_ν)` is further from
proof than the wording suggests.  Item 2: the question about doubling spaces is consistent with M1 only because it
is restricted to `f ≡ 0`.  Item 4: "covering arrays of strength two appear to be the right object" is doubtful as a
sufficiency statement: the whole radius-2 ball is far more than a covering array of strength two and leaves
quadratic uncertainty (M3).  The new [P] construction in §11.5 (no deterministic procedure is instance-optimal) is
correct; I verified it by enumeration and with an independent family (uniform metric, `g_j = c·1_{h_j}`).

## 4. Publication assessment

*Is "complexity of certifying ground states and free energies under envelope uncertainty" publishable?*  Not as
mathematics or information theory: after the reformulation G1 (a rewriting of the definition), Theorem 11.9 is the
stated consequence of the type covering lemma with a type-dependent level, Theorem 11.15 is the level set of
Merhav's exponent, the converses are five-line Chernoff/Hölder arguments, G5 is the dominating-set reduction, G6
is a packing argument, G8 is a discrete Taylor remainder.  The authors' own "tools are standard, proofs are short"
is accurate.

As a short note in certified/global optimisation (the audience of Bachoc–Cesari–Gerchinovitz, Hansen–Jaumard–Lu,
Baran–Demaine) it has a point of its own: the grey-box model (known part + first-order envelope), the statement
"either the white-box part is sharp or certification is exponential, with exponent `R*`", and an explicit
non-instance-optimality example.  A formalisation venue is the other option, with the Lean development as the
contribution.  What is missing for either:

1. Correct statement of Theorem 11.15 (C1) and complete proofs of both upper bounds (unequal sites; uniformity).
2. Positioning: Csiszár 1998 / Berger 1971 for zero-error covering of type classes; Merhav 2011 and
   Arikan–Merhav 1998 for the finite-temperature formula; state plainly that the exponents are corollaries.
3. An algorithmic statement.  All upper bounds are existence statements for someone who knows `g`.  Either a
   procedure that reaches `exp(nR* + o(n))` without knowing `g`, or a lower bound separating adaptive search from
   `N_cov` on product landscapes.
4. One step beyond product landscapes (pairwise chain as known part), otherwise the exponent theorems do not touch
   the application.
5. G6: a regime in which the comparison class is provably within a constant of `N_cov`, or an honest statement
   that there is none in the grey-box setting (M1); tight constants.
6. G8: a sufficient condition (row sums), a lower bound, and one residual with certified `c_ij`.
7. Since the deterministic model is exponentially pessimistic and Theorem 11.21 shows that sampling is not, a
   probabilistic certificate notion for minimum energies as well.

## 5. Independent numerical checks

All code is mine; nothing from `experiments/` was reused.  Scripts and outputs were kept in the session scratch
directory (not in the repository).

| check | sizes | result |
|---|---|---|
| G1: slack identities, point/value/configuration/cover by brute force; §2.4 bullets; LP for the regret | 400 quasi-metric instances, `\|X\| ≤ 7`, `κ ∈ {0,.4,.8,1}`, asymmetric half of the time | all implications hold; `N_cov ≤ N_val ≤ N_point ≤ N_cov+1`; 131 LP checks of the regret formula |
| exchange lemmas | 1 500 instances; 690 value-not-point sets, 7 887 configuration sets with unevaluated candidate | `N_val = N_point` and `N_point = max(1, N_conf)` in every instance; `N_point = N_cov + 1` in 172 |
| `R*`, binary | `e/c = .25, .5, .75, .9` | dual LP = `max_μ[h(μ) − h(ρμ)]` = `max_x[…]` = primal: `0.3509, 0.1882, 0.0798, 0.0293` |
| `R*`, three states | 5 sites, with and without residual | primal max over types = dual; Boltzmann/optimal = `0.57, 1.00, 0.88, 0, 0` |
| dichotomy | 240 random sites, `k ≤ 4`, `κ ≤ 0.95` | `R* = 0` iff sharp (121 sharp, 115 non-sharp); fails at `κ = 1` as predicted |
| layer counts, binary family | `n = 100, 200, 400, 800`, exact integers | `ρ = 1/2`: `0.2073, 0.1994, 0.1947, 0.1919` (identical to the report); also `ρ = 1/4, 3/4, 9/10` |
| exact covers on small products | ILP/LP, up to 729 states; 90 random products with residual | optimal-weight bound `≤ N_frac ≤ N_cov ≤ ∏_{non-sharp} k_i`; `N_cov = 1` iff all sharp |
| unequal sites | `m = 25, 50, 100, 150` pairs, exact orbit counts | `(1/m) ln N_frac ∈ [0.274, 0.459], [0.263, 0.363], [0.253, 0.306], [0.247, 0.285]`; common slope `0.2329`, per-site maxima `0.3765` |
| Thm 11.15 identity | 14 sites, `k = 2, 3`, `β ∈ {.5, 1, 3, 8}`, asymmetric slack | `\|primal − dual\| ≤ 1.8·10⁻⁶`; `H(π) ≤ R_β < ln k`; `R_β = 0.6658, 0.4817, 0.2159` (and `0.1909` at `β = 400`); sharp site `0.5143` |
| Thm 11.15 at finite `n` | binary, `n ≤ 400`, explicit layer certificate vs machine-checked converse | `β = 4, ε = 1`: `0.4794 ≤ n⁻¹ ln N_Z ≤ 0.5186` at `n = 400` (`R_β = 0.4817`); `β = 1`: `0.6497 … 0.6860` (`0.6658`) |
| minimal free-energy certificates, brute force | 16 instances, all subsets, `\|X\| ≤ 8` | converses never violated (best converse `/ N` between `0.36` and `1.00`); `N_Z(0) = \|X\|` always; two-sided `>` one-sided in 30 of 64 cases |
| best-first search | 16 277 runs, six metric families incl. stars, uniform, line, clusters, trees | bound never violated, attained 298 times; exceeds `N_cov + 1` in 2 517 runs; `N_shrunk/N_cov` up to 14 |
| doubling counterexample; adversary families | `m ≤ 16`; `N = 5, M = 4` and `K = 6, M = 5` | as stated in M1 and §3 |
| second and third order envelopes | LP over the whole class, alphabets up to `(2,3,2,2)`, `m = 2, 3` | LP extremes = `I_{m−1}g ∓ Σ c_T` to `10⁻¹⁴` |
| dense second-order class | LP, `n = 5, 6`; explicit class members, exact rationals, closed form `n ≤ 12`, all contexts `n ≤ 10` | star `−C(w,2)`; radius-2 ball `−C(w−1,2)`; two stars: the better of the two star bounds; explicit two-star member reaches `−C(w,2)` at `w = ⌊(n+2)/3⌋` |
| cut and elimination rules | exact rationals; 264 + 300 instances; 120 random partial 2-trees | bracket and identities hold; full reduction exact |
| domination reduction | 300 graphs, `ε ∈ {0, .5, .99}` | certificate ⇔ `o ∈ A` and `A` dominates |
| sampled sandwich | exact enumeration of sample tuples, 10 577 (instance, `η`) cases | no violation; one-sided ratio up to `0.9998`; correlated reference violates (`1.00 > 0.74`) |
| harness | `XI.1`–`XI.13`, `DEAD.6`–`DEAD.9` in quick mode; mutation group `XI` | all behave as documented; 31 of 31 mutations caught |

*Harness assessment.*  Each test exercises its title.  Limits: `XI.3` tests validity of the product bound and the
one-evaluation criterion, not the exponent; no harness test touches the asymptotic statements of Theorems 11.9 and
11.15 (only benchmark B8); `XI.4` never attains the bound in quick mode and, like its mutation `M1`, can detect a
factor 4 in `θ` but not a factor 2 (m5); `XI.10` tests the lower extremal function only; `XI.13` reaches
`0.53` of its bound, so a prefactor `1.1` instead of `2` would pass.  `XI.1`'s "certificate ⇔ cover" compares two
evaluations of the same expression and cannot fail except through the code path of `L_A`.

## 6. Not checked

* The first research phase, except the corrected paragraphs.
* Lean proofs were not read line by line; statements and axioms only.  I did not run `lake build` or
  `scripts/audit_all.sh`; the scratch files import the built modules of `ee2053f`.
* The harness in full mode; benchmark B9's figures.
* The literature files `L4`–`L6` beyond the items used here; of the primary sources only Merhav's paper was read.
  The type covering lemma is quoted from memory and from `L6`.
* Asymptotic statements beyond `n = 800` (binary), `m = 150` (two types), `n = 400` (finite temperature).
* Whether some evaluation set can certify the dense second-order class with sub-exponentially many evaluations
  (M3 treats one star, two opposite stars and the radius-2 ball only).
* An approximate version of the kernel separation (M4.2).
* `RESEARCH_LOG.md`.

## Appendix A. Referee lemmas, machine-checked against `ee2053f`

The scratch files were checked with `lake env lean <file>` from the repository root; they are not part of the
repository (session scratch directory, `<session scratch directory>/referee2/`: `Referee2.lean`, `Referee2b.lean`, `Referee2c.lean`, and the Python
scripts under `scripts/`).  The complete source of the four lemmas is reproduced here so that they can be
re-checked.  All depend on `propext`, `Classical.choice`, `Quot.sound` only.

*Proof idea of the exchange lemmas.*  Let `a₀` attain `U_A(x) = g(a₀) + d(x,a₀)`.  For every `y` either
`d(x,y) ≤ f(y) − f(x) + ε`, and then `x` covers `y`; or `U_A(x) − L_A(y) ≤ f(y) − f(x) + ε` with `L_A(y)` attained at
`b`.  If `b ≠ a₀`, `b` covers `y` because `U_A(x) ≥ g(x)`; if `b = a₀`, the triangle inequality
`d(x,y) ≤ d(x,a₀) + d(a₀,y)` puts us in the first case.  For value certificates take `x = argmin(f + U_A)`; the
exchange lowers the incumbent by `s(x,a₀)` and the lower bound by at most `s(x,a₀)`.

File 1 (imports: `Mathlib`, `proofs.Frontiers.CertificationGeometry`, `CertificateNotions`, `ConditionalEnvelope`,
`CertificateComplexity`, `ExponentialWeights`, `ProductRates`, `BestFirst`, `ThermalRobustness`,
`SecondOrderEnvelope`, `PartitionProduct`):

```lean
namespace MetricChain.Referee2

open Finset MetricChain

section Notions

variable {X : Type*} [Fintype X] [Nonempty X]

/-- **Exchange for configuration certificates.**  If `A` (nonempty) certifies the configuration
`x`, then replacing the anchor that attains `U_A x` by `x` gives a point certificate.  Its size is
at most `|A|`.  Hence `N_point ≤ N_config` whenever `N_config ≥ 1`. -/
theorem config_exchange [DecidableEq X] {d : X → X → ℝ} (hd : IsEnvelope d) {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) {A : Finset X} {hA : A.Nonempty} {x : X} {ε : ℝ}
    (h : IsConfigCertificate d f g A hA x ε) :
    ∃ a₀ ∈ A, IsCertificate d f g (insert x (A.erase a₀)) (insert_nonempty x _) ε := by
  obtain ⟨a₀, ha₀, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => g a + d x a)
  have hU : upperEnv d A hA g x = g a₀ + d x a₀ := hmin
  refine ⟨a₀, ha₀, ?_⟩
  rw [isCertificate_iff_cover]
  intro y
  have hUB : certUB f g (insert x (A.erase a₀)) (insert_nonempty x _) ≤ f x + g x :=
    Finset.inf'_le (fun a => f a + g a) (mem_insert_self x _)
  have hy := h y
  unfold condEnv at hy
  rcases min_le_iff.mp hy with h1 | h1
  · refine ⟨x, mem_insert_self x _, ?_⟩
    unfold slack
    linarith
  · obtain ⟨b, hb, hmax⟩ := Finset.exists_mem_eq_sup' hA (fun a => g a - d a y)
    have hL : lowerEnv d A hA g y = g b - d b y := hmax
    by_cases hba : b = a₀
    · subst hba
      refine ⟨x, mem_insert_self x _, ?_⟩
      have htri := hd.triangle x b y
      rw [hU, hL] at h1
      unfold slack
      linarith
    · refine ⟨b, mem_insert_of_mem (mem_erase.mpr ⟨hba, hb⟩), ?_⟩
      have hUx := le_upperEnv hg A hA g (fun _ _ => rfl) x
      rw [hL] at h1
      unfold slack
      linarith

/-- Cardinality of the exchanged set. -/
theorem card_exchange_le [DecidableEq X] {A : Finset X} {a₀ x : X} (ha₀ : a₀ ∈ A) :
    (insert x (A.erase a₀)).card ≤ A.card := by
  have h1 := Finset.card_insert_le x (A.erase a₀)
  have h2 := Finset.card_erase_of_mem ha₀
  have h3 : 0 < A.card := Finset.card_pos.mpr ⟨a₀, ha₀⟩
  omega

/-- **Exchange for value certificates.**  If `A` is a value certificate, some set of at most `|A|`
points is a point certificate: replace the anchor that attains `U_A` at a minimiser `y₀` of
`f + U_A` by `y₀`.  Hence `N_point ≤ N_value`, i.e. `N_point = N_value`. -/
theorem value_exchange [DecidableEq X] {d : X → X → ℝ} (hd : IsEnvelope d) {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) {A : Finset X} {hA : A.Nonempty} {ε : ℝ}
    (h : IsValueCertificate d f g A hA ε) :
    ∃ (B : Finset X) (hB : B.Nonempty), B.card ≤ A.card ∧ IsCertificate d f g B hB ε := by
  obtain ⟨y₀, -, hy₀⟩ := Finset.exists_mem_eq_inf' univ_nonempty
    (fun y => f y + upperEnv d A hA g y)
  obtain ⟨a₀, ha₀, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => g a + d y₀ a)
  have hU : upperEnv d A hA g y₀ = g a₀ + d y₀ a₀ := hmin
  refine ⟨insert y₀ (A.erase a₀), insert_nonempty y₀ _, card_exchange_le ha₀, ?_⟩
  rw [isCertificate_iff_cover]
  intro z
  have hUB : certUB f g (insert y₀ (A.erase a₀)) (insert_nonempty y₀ _) ≤ f y₀ + g y₀ :=
    Finset.inf'_le (fun a => f a + g a) (mem_insert_self y₀ _)
  unfold IsValueCertificate at h
  rw [hy₀, hU] at h
  have hLB : certLB d f g A hA ≤ f z + lowerEnv d A hA g z :=
    Finset.inf'_le (fun y => f y + lowerEnv d A hA g y) (mem_univ z)
  obtain ⟨b, hb, hmax⟩ := Finset.exists_mem_eq_sup' hA (fun a => g a - d a z)
  have hL : lowerEnv d A hA g z = g b - d b z := hmax
  rw [hL] at hLB
  have hadm := hg y₀ a₀
  by_cases hba : b = a₀
  · subst hba
    refine ⟨y₀, mem_insert_self y₀ _, ?_⟩
    have htri := hd.triangle y₀ b z
    unfold slack
    linarith
  · refine ⟨b, mem_insert_of_mem (mem_erase.mpr ⟨hba, hb⟩), ?_⟩
    unfold slack
    linarith

end Notions

section Gauge

/-- Two binary sites.  The two ordered pair factors compensate each other:
`W 0 1 a b = 2^(a + 2b)` and `W 1 0 b a = 2^(-(a + 2b))`, so every configuration has weight `1`
(two independent uniform sites), but each ordered factor separately tells all states apart. -/
def gaugeW : WInstance 2 2 where
  w := fun _ _ => 1
  W := fun i j a b =>
    if i = 0 ∧ j = 1 then (2 : ℚ) ^ (a.val + 2 * b.val)
    else if i = 1 ∧ j = 0 then 1 / (2 : ℚ) ^ (b.val + 2 * a.val)
    else 1

theorem gaugeW_pos : gaugeW.Pos := by decide +kernel

theorem gaugeW_rigid : gaugeW.Rigid := by decide +kernel

theorem gaugeW_weight : ∀ x : Config 2 2, gaugeW.weight x = 1 := by decide +kernel

theorem gaugeW_Z : gaugeW.Z (fullDom 2 2) = 4 := by decide +kernel

/-- The instance is a product of two uniform sites (`Z = 2 · 2`), it is `Pos` and `Rigid`, and
therefore every elementary certificate with the exact lower endpoint enumerates all four
configurations: the "separation" is a property of the representation, not of the model. -/
theorem gauge_trivial_separation :
    gaugeW.Pos ∧ gaugeW.Rigid ∧ (∀ x : Config 2 2, gaugeW.weight x = 1) ∧
      ∀ c : ZCert2 2 2, c.Elementary → ∀ hi : ℚ,
        zverify2 c gaugeW (fullDom 2 2) = some (4, hi) → 2 ^ 2 ≤ c.leaves := by
  refine ⟨gaugeW_pos, gaugeW_rigid, gaugeW_weight, fun c hc hi hv => ?_⟩
  rw [← gaugeW_Z] at hv
  exact zverify2_elementary_exact_leaves_fullDom gaugeW_pos gaugeW_rigid c hc hi hv

end Gauge

end MetricChain.Referee2

#print axioms MetricChain.Referee2.config_exchange
#print axioms MetricChain.Referee2.value_exchange
#print axioms MetricChain.Referee2.gauge_trivial_separation
```

File 2 (imports: `Mathlib`, `proofs.Frontiers.CertificationGeometry`, `ThermalRobustness`, `ProductRates`):

```lean
namespace MetricChain.Referee2

open Finset MetricChain

variable {X : Type*} [Fintype X] [Nonempty X]

theorem exact_free_energy_certificate_eq_univ {d : X → X → ℝ} {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) (A : Finset X) (hA : A.Nonempty) {β : ℝ} (hβ : 0 < β)
    (hpos : ∀ a y, a ≠ y → 0 < slack d g a y)
    (h : ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) ≤
      ∑ y, Real.exp (-β * (f y + upperEnv d A hA g y))) : A = univ := by
  have hLU : ∀ y, lowerEnv d A hA g y ≤ upperEnv d A hA g y := fun y =>
    (lowerEnv_le hg A hA g (fun _ _ => rfl) y).trans (le_upperEnv hg A hA g (fun _ _ => rfl) y)
  have hterm : ∀ y ∈ (univ : Finset X), Real.exp (-β * (f y + upperEnv d A hA g y)) ≤
      Real.exp (-β * (f y + lowerEnv d A hA g y)) := by
    intro y _
    apply Real.exp_le_exp.mpr
    nlinarith [hLU y]
  have hsum : ∑ y, Real.exp (-β * (f y + upperEnv d A hA g y)) =
      ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) :=
    le_antisymm (Finset.sum_le_sum hterm) h
  have heq := (Finset.sum_eq_sum_iff_of_le hterm).mp hsum
  rw [Finset.eq_univ_iff_forall]
  intro y
  have hy := Real.exp_injective (heq y (mem_univ y))
  have hLUy : upperEnv d A hA g y = lowerEnv d A hA g y := by
    have h1 : -β * (f y + upperEnv d A hA g y) = -β * (f y + lowerEnv d A hA g y) := hy
    have h2 : β * (upperEnv d A hA g y - lowerEnv d A hA g y) = 0 := by linarith
    rcases mul_eq_zero.mp h2 with h3 | h3
    · exact absurd h3 hβ.ne'
    · linarith
  have hL := lowerEnv_eq_sub_slack d g A hA y
  have hgL := lowerEnv_le hg A hA g (fun _ _ => rfl) y
  have hgU := le_upperEnv hg A hA g (fun _ _ => rfl) y
  have hs0 : slackFrom d g A hA y = 0 := by linarith
  obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => slack d g a y)
  have hsa : slack d g a y = 0 := by
    have : slackFrom d g A hA y = slack d g a y := hmin
    linarith
  by_contra hyA
  have hne : a ≠ y := fun e => hyA (e ▸ ha)
  have := hpos a y hne
  linarith

end MetricChain.Referee2

#print axioms MetricChain.Referee2.exact_free_energy_certificate_eq_univ
```
