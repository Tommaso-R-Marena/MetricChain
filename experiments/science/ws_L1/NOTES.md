# Workstream L1 — notes (machine-checking the science division's core statements)

Chronological log; updated after every step.  2026-11-25 (UTC).

**Correction (19:29 UTC, read from `date`):** the clock times in the section headers below from
"18:40" to "22:15" were my estimates and are wrong — the whole of that work happened between 18:27
and 19:29 UTC (file modification times: IdentifiedSets 18:41, Separation 18:48, OrthogonalArray 18:54,
MaxEntStability ~19:00 and 19:22, MarginalOracle 19:10–19:28, PerturbationBracket 19:22, BasinBound 19:26).
The headers are kept as step labels, marked `(est.)`; times from here on are read from `date`.

## 18:27 start

* Read `COMMON.md`, `L1_brief.md`, `INFERENCE_LIMITS.md` (all), `INFERENCE_LIMITS_ADDENDA.md` (all).
* Environment: Lean 4.31.0 at `~/.lean/lean-4.31.0-linux/bin`; `.lake/packages` has mathlib, batteries,
  aesop, Qq, proofwidgets, plausible, importGraph, LeanSearchClient, Cli.  `lakefile.lean` options:
  `autoImplicit false`, `relaxedAutoImplicit false`.
* Rules I am bound by: write only in `experiments/science/ws_L1/` and `docs/science/workstreams/L1_REPORT.md`;
  no git state change; check files only with `lake env lean <abs path>`, one at a time; no sorry/admit/
  native_decide/axioms; `#print axioms` at the end of each file.

## Plan (targets in priority order from the brief)

1. `IdentifiedSets.lean` — Theorem 8 / §8: (a) model-free certificate, (b) envelope ("flow with gains"),
   (c) falsification, (d) divergence ball via Gibbs variational inequality.
2. `Separation.lean` — Theorem 4′ separation inequality (abstract) + concrete `F ≤ |C|·F1`.
3. `OrthogonalArray.lean` — Lemma 1.
4. `MaxEntStability.lean` — Theorem 7 algebraic core; Pinsker search in Mathlib.
5. optional: Theorem 3 / Theorem 2(d).

## step 18:40 (est.) environment probe

* `lake env lean` on a file that only imports Mathlib and runs `#check`s: 26 s wall.
* Mathlib at `fabf563a` (2026-06-15, "bump toolchain to v4.31.0").
* **Pinsker**: `grep -rIl -i pinsker .lake/packages/` → no file at all (not in Mathlib, not in any
  dependency).  No total-variation distance (`tvDist`, `totalVariationDist`) either.
  `Mathlib/InformationTheory/KullbackLeibler/{Basic,ChainRule,KLFun}.lean` exist (measure-theoretic
  `klDiv`, non-negativity, chain rule) but no Pinsker, no Donsker–Varadhan (`grep -i "donsker\|varadhan"` → nothing).
* The theory division's proofs have `klFin`, `tilt`, `expTilt`, `klFin_nonneg_of_dominated`,
  `logMGF_eq_tilt` (ThermalRobustness / EnsembleDivergence) but no Pinsker either.
* Lemma names checked: `Finset.sum_sq_le_sum_mul_sum_of_sq_eq_mul` is deprecated →
  `Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul`; `Real.add_pow_le_pow_mul_pow_of_add_eq_one` (named in
  the brief) does not exist under that name; `Real.hasSum_log_one_add_inv` exists (gives
  `log(1+1/a) ≥ 2/(2a+1)`), `hammingDist_eq_hammingNorm : hammingDist x y = hammingNorm (-x + y)`.

## step 18:55 (est.) Target 1 DONE — `IdentifiedSets.lean` (checks, 38 s, no errors)

All of §8 soundness + Theorem 8(b) inequality + 8(c):
`modelFree_certificate_sound_support` (note's form, arbitrary data set D + support-function bound),
`modelFree_certificate_sound` (box form of the brief), `flow_term_nonpos`,
`envelope_flow_sound_weights` (brief's (b)), `envelope_flow_sound_normalised`,
`envelope_flow_sound_gibbs` (note's form: every admissible g consistent with the data),
`falsification_sound_weights` / `_ensemble` / `_gibbs`, `theorem8c_falsification` (note's form with b, β),
`gibbs_variational` (Donsker–Varadhan on a finite type, μ₀ need not be normalised),
`divergenceBall_certificate_sound` (§8 second bullet), `kl_lower_bound_certificate_sound` (Thm 8(b) inequality),
witnesses `envelope_flow_certificate_witness` (certificate satisfiable AND tight: t = 2/3 attained),
`falsification_certificate_witness` (certificate exists for data some ensemble satisfies).
`#print axioms`: all 14 → `[propext, Classical.choice, Quot.sound]`.

Observations while formalising (for the report):
* (b) needs NO sign condition on μ₀ or κ, only `w ≥ 0`, `Σ μ₀ w > 0`.
* DV inequality does not need μ₀ normalised; needs `μ ≪ μ₀` (with the real-valued KL formula; if
  not `μ ≪ μ₀` the true KL is +∞ and the claim is trivial but the real formula is not the KL).
* Thm 8(c): proved "no member of the class is consistent with the data".  The note's conclusion
  `b_min(D) > b` (strict, about an infimum) additionally needs attainment (D closed) — true by a
  compactness argument but NOT formalised.
* Model-free soundness needs neither convexity nor compactness of D.

## step 19:15 (est.) Target 2 DONE — `Separation.lean` (checks, 48 s)

Abstract: `exp_sub_exp_max_antitone`, `pSum_sub_flat_mono` (A₁−F₁ ≤ A−F), `separation_ratio`
(F ≤ m·F₁ ⟹ 1 + (A₁/F₁ − 1)/m ≤ A/F; needs only u ≥ 0, m > 0 is derived), `separation_log`
(m ≥ 1 ⟹ log(A₁/F₁) − log m ≤ log A − log F).
Concrete on `ι → G` (G finite additive commutative group, so `Fin n → ZMod 2` is an instance):
`distToCoset C hC s x = min_{a∈C} d_H(x, s+a)`, `pSum_flat_distToCoset_le` (F ≤ |C|·F₁, for ANY
non-empty finite set C of translations and any real u — no linearity, no sign condition),
`distToCoset_le` (needs 0 ∈ C), `separation_distToCoset`, `sensitivity_distToCoset`.
`#print axioms` for the 7 headline declarations: `[propext, Classical.choice, Quot.sound]`.
Observation: the separation step of Theorem 4′ uses of C only: finite, non-empty, contains 0.
Linearity/dual distance is used only for the oracle (Lemma 1) — and for the count of the
difference sets one needs nothing either.
Not done: closed forms A₁ = (1+e^{−u})^n, F₁ = Σ_j C(n,j) e^{−u max(j,R)} (the theory division's
`cube_nonadaptive_bound` does not have them either).
(after the check I replaced a `first | (field_simp; ring) | field_simp` by `field_simp` to silence a
linter warning; to be re-checked in the final pass)

## step 19:40 (est.) Target 3 DONE — `OrthogonalArray.lean` (checks, 21–63 s)

Lemma 1 proved for any finite field F (in particular ZMod 2), C : Submodule F (ι → F):
`restrict_surjective_of_dual` (projection to S onto if no non-zero dual word supported on S),
`marginal_const_of_invariant`, `uniform_marginal_of_invariant` (cylinder weight = 1/|F|^|S|),
`lemma1_uniform_marginals` (dual-distance form: every non-zero u ⟂ C has hammingNorm u > k),
`lemma1_binary` (F₂, literal note statement), `lemma1_marginals_agree` (oracle form),
`lemma1_sharp_witness` (repetition code {00,11}: hypothesis holds with k = 1; uniform measure on C
is invariant; marginal on both coordinates is 1/2 ≠ 1/4 — `|S| ≤ k` is sharp).
`#print axioms`: 7 × `[propext, Classical.choice, Quot.sound]`.
Notes: * μ ≥ 0 is NOT needed (total mass 1 + invariance suffice).
* Proof simpler than the note's: translate by a codeword projecting to y' − y (no coset
  decomposition, no fibre counting).
* One elaboration trap: for ι = Fin n the `Decidable (∀ i ∈ S, …)` instance is
  `Nat.decidableForallFin`, in the generic statement `Fintype.decidableForallFintype`;
  `exact` fails with identical-looking types, `convert h using 3` closes it.
* `AddSubgroup.toZModSubmodule` exists in Mathlib (subgroup ≃ subspace over ZMod n); not used.

## step 19:45 (est.) Target 4 plan — `MaxEntStability.lean`

KEY OBSERVATION: Theorem 7 needs only the *symmetrised* Pinsker `J ≥ 4 TV²`, and that has a
direct elementary proof without Pinsker:
  (a−b)(ln a − ln b) ≥ 2(a−b)²/(a+b)   [from ln t ≥ 2(t−1)/(t+1), t ≥ 1; Mathlib:
  `Real.hasSum_log_sub_log_of_abs_lt_one`, first term of a series with non-negative terms]
  and Cauchy–Schwarz (Σ|p−q|)² ≤ Σ (p−q)²/(p+q) · Σ (p+q) = 2 Σ (p−q)²/(p+q).
So Theorem 7(ii)–(iii) can be proved with NO Pinsker hypothesis.
SECOND OBSERVATION: the brief's "purely algebraic step" (4T² ≤ J, J ≤ ωT ⟹ T ≤ ω/4, J ≤ ω²/4)
is FALSE as literally stated: T = J = 0, ω = −1.  It needs ω ≥ 0 (then T ≥ 0 is not needed).
Harmless for the note (ω = β·osc(r) ≥ 0).

## step 20:10 (est.) Target 4 DONE — `MaxEntStability.lean` (checks first time, 33 s, no warnings)

ALL of Theorem 7 (i)–(v) machine-checked, NO Pinsker hypothesis:
`symmKL_eq_of_logRatio` (algebraic core of (i)), `two_mul_sub_div_add_le_log_sub`,
`sq_div_add_le_mul_log`, `symm_pinsker` (4 TV² ≤ KL(p‖q)+KL(q‖p), positive probability vectors),
`abs_sum_sub_le_osc_mul_tv`, `pinsker_closing` (needs 0 ≤ ω), `pinsker_closing_needs_nonneg`
(counterexample T = J = 0, ω = −1), `pythagoras_expFam`, `theorem7_i_energies`,
`theorem7_ii_iii_energies`, `theorem7` (note's form, (i)–(v) bundled), `expFam_isIProjection`
(exponential form with matching moments ⟹ minimiser of KL(·‖μ₀) on the moment class),
`tv_bounded_perturbation` (no-feature instance; non-vacuity).
`#print axioms`: 11 × `[propext, Classical.choice, Quot.sound]`.
Differences from the note: ν is ASSUMED of exponential form with matching Φ-means (that the
I-projection has this form — Csiszár — is not formalised; the converse is); ω replaced by any
hi − lo with lo ≤ r ≤ hi; β ≥ 0 explicit.

Re-checked after edits: IdentifiedSets.lean (30 s), Separation.lean (21 s): clean, no warnings.

## step 20:15 (est.) Decision on extras (targets 1–4 complete)

Order: (E1) assemble Theorems 4 and 4′ as real query lower bounds with the marginal oracle
modelled explicitly (needs an oracle-aware algorithm structure: the theory division's
`QueryAlgorithm.consistent` is FALSE for an algorithm that also sees an oracle answer, so their
`expected_queries_ge_packing` / `nonadaptive_expected_queries_ge` cannot be applied verbatim);
(E5) Theorem 5 bracket + width identity; (E8) Theorem 7′ closing step; (E2) Pinsker proper;
(E3) Theorem 3.

## step 21:00 (est.) Extra E1 DONE — `MarginalOracle.lean`: Theorems 4 and 4′ assembled in full

(878 → ~960 lines; checks in 15–26 s; clean after adding `omit`s.)
Model: an oracle-assisted algorithm = family `alg ω o : MetricChain.QueryAlgorithm (ι → F)` of the
theory division's query algorithms indexed by the oracle answer `o`; run on g with
`o = marginalOracle β k g`.  On a family with common answer o₀ the algorithm is the plain
`alg ω o₀`, correct on the class restricted to {O = o₀}: so both theorems are COROLLARIES of the
theory division's `expected_queries_ge_packing` and `nonadaptive_expected_queries_ge`
(imported read-only; their axioms: standard three).
Why a new model was needed (finding for the report): the note's proof of Theorem 4′ says "the
algorithm restricted to the family is non-adaptive in the sense of Theorem 11.45(a)".  As
machine-checked, 11.45(a) (`nonadaptive_expected_queries_ge`) is about `QueryAlgorithm`, whose
consistency axiom is FALSE for an algorithm that also sees an oracle answer depending on g, and
it assumes non-adaptivity for ALL g.  The argument is repaired by indexing by the oracle answer
and restricting the class to the fibre {O = o₀}; nothing else changes.
Declarations: `distToCoset_lipschitz`, `distToCoset_add_mem`, `card_centres_near`,
`HammingLip` (= theory `Admissible` for c·d_H, `hammingLip_iff_admissible` is `Iff.rfl`), `logZ`,
`gibbs`, `marginalOracle`, `marginalOracle_singleton` (sanity: order ≥ 1 gives one-site marginals),
`symDip`, `dipAt`, `codeSubmodule`, `marginalOracle_of_invariant`, `marginalOracle_eq_of_invariant`,
`theorem4_adaptive_marginal_oracle`, `theorem4'_nonadaptive_marginal_oracle` (any finite field),
`theorem4_binary_cube`, `theorem4'_binary_cube` (F₂ⁿ, with 2^n; over ZMod 2 "linear" = contains 0 and
closed under +).  `#print axioms`: `[propext, Classical.choice, Quot.sound]` for all.
The file repeats the proofs of Lemma 1 and of the separation inequality verbatim (files here do
not import each other).

## step 21:40 (est.) Extras E8 and E5 DONE

* `MaxEntStability.lean` extended (checks, 20 s, clean): `transport_le_coupling` (weak
  Kantorovich–Rubinstein), `transport_closing` (K ≤ aW, W² ≤ 2mK, a, m ≥ 0 ⟹ W ≤ 2ma, K ≤ 2ma²),
  `theorem7'_of_transportEntropy`, `theorem7'_observable` — Theorem 7′ of the addenda (A2) WITH
  THE TRANSPORT–ENTROPY INEQUALITY AS AN EXPLICIT HYPOTHESIS on one coupling (m = κn).  Marton's
  inequality (κ = 1/4 for products) not formalised.  Axioms: standard three.
* `PerturbationBracket.lean` (new; checks first time, 14 s): Theorem 5, first display —
  `kl_model_true`, `kl_true_model`, `theorem5_bracket` (−βE_{μ₀}g ≤ ln(Z_g/Z_0) ≤ −βE_{μ_g}g and
  width = KL(μ₀‖μ_g)+KL(μ_g‖μ₀); any real β, any g), `zRatio_eq_partition_ratio`.  Axioms: std.
* First full version of `docs/science/workstreams/L1_REPORT.md` written (to be extended).

## step 21:45 (est.) Extra E3 plan — `BasinBound.lean` (Theorem 3)

General alphabet A with a "sign" s : A → ℝ, Σ_b s b = 0, s² = 1 (A = Bool: s = ±1).
chi s T x = Π_{i∈T} s (x i).  Steps: (A) chi_T·chi_T' = chi_{T∆T'}; (B) uniform marginal on T,
T ≠ ∅ ⟹ E_μ chi_T = 0 (fibre decomposition + Π Σ = Σ Π); (C) E_μ f² = M_t for
f = Σ_{|T|≤t} chi_T(a) chi_T, when 2t ≤ k; (D) Markov ⟹ m·μ(B) ≤ M_t if m ≤ f² on B;
point mass μ(a) ≤ 1/M_t.  Not planned: Krawtchouk identification f = F_t(d_H(·,a)), asymptotics.

## step 22:10 (est.) Extra E3 DONE — `BasinBound.lean` (Theorem 3 core; checks first time, 15 s)

`chi`, `chi_mul_chi` (χ_T χ_T' = χ_{T∆T'}), `sum_mul_chi_eq_zero` (uniform marginal on T ≠ ∅ ⟹
E_μ χ_T = 0), `sum_mul_sq_eq_card` (E_μ f² = M_t when 2t ≤ k), `basin_bound` (Markov form:
m ≤ f² on B ⟹ m·μ(B) ≤ M_t), `point_mass_le` (μ({a}) ≤ 1/M_t), `card_subsets_le`
(M_t = Σ_{j≤t} C(n,j)), `theorem3_bool`, `theorem3_point_mass_bool` ({0,1}ⁿ = ι → Bool).
Axioms: standard three.  General alphabet with a balanced sign s (Σ s = 0, s² = 1).
NOT formalised: f(x) = F_t(d_H(x,a)) (Krawtchouk), so the "ball" is an arbitrary set B with a
lower bound m of f² on it; asymptotics.

## step 22:15 (est.) `MarginalOracle.lean` extended (clean, 14 s)

* `queryAlgorithm_output_const_of_no_queries`: a theory-division `QueryAlgorithm` with no queries
  has constant output — formal form of the model gap.
* `repetition_dual_distance`, `repetition_add_mem`, `theorem4_one_body_marginals`,
  `theorem4'_one_body_marginals`: explicit hypothesis-free instance (k = 1, C = {0ⁿ,1ⁿ}):
  all one-site marginals for free cost at most a factor 2 in both bounds.  Axioms: std.

## ~19:33 UTC Further extras DONE (between `date` readings 19:29 and 19:36; the earlier header
## text "19:45 UTC (clock)" was wrong and is corrected here)

* `MaxEntStability.lean`: `expFam_eq_of_moments_eq` (Proposition 6, identifiability: equal Φ-means ⟹
  equal ensembles; from Theorem 7(i) with r = 0 and the symmetrised Pinsker inequality).  Clean.
* `PerturbationBracket.lean`: Proposition 9 (§10) — `logZ_step`, `meanEnergy_anti`,
  `caloric_bracket`, `caloric_bracket_width`; derived from Theorem 5 on each interval, no calculus
  (the integral identity is not formalised).  One fix (unfold order), then clean.
* `Pinsker.lean` (new): `kemperman_scalar`, `pinsker` (2·TV² ≤ KL(p‖q), p ≥ 0, q > 0 probability
  vectors on a finite type), `pinsker_tv_le`.  The calculus part (derivative of
  G(t) = (2t²+4t) log t − (5t²−4t−1) is 4((t+1) log t − 2(t−1)), sign of t − 1) passed first time;
  one fix in the Cauchy–Schwarz side condition (`generalize` before `field_simp`).  Axioms: std.

## 19:36–19:37 UTC (from `check_log.txt`) FINAL CHECK of all eight files

`check_log.txt`: each file run with `lake env lean <abs path>`, sequentially; all exit code 0, no
warning, no error; 74 `#print axioms` lines, every one exactly
`[propext, Classical.choice, Quot.sound]` (IdentifiedSets 14, Separation 7, OrthogonalArray 7,
MaxEntStability 16, MarginalOracle 11, PerturbationBracket 8, BasinBound 8, Pinsker 3).
Forbidden-token scan (`grep "sorry|admit|native_decide|axiom"` minus the `#print axioms` lines)
on `*.lean`: no match.

## Numerical sanity check of the formal statements (`sanity_numerics.py`, output in
## `sanity_numerics_output.txt`; 2.5 s; seed 20261125)

[7,3] simplex code on F_2^7: |C| = 8, dual distance 3 (so k = 2: a non-trivial instance of the
hypothesis of Lemma 1 / Theorems 4, 4′ beyond the k = 1 instance proved in Lean).
(2) random C-invariant μ: marginals of order 1, 2 uniform to 5.6e-17, order 3 off by 4.5e-2.
(3) separation: min slacks |C|F1 − F = 1.05, (A−F)−(A1−F1) = 2.75, log form 2.1 (6 centres,
u ∈ {0.5,1,2}, R ∈ {1,2,2.5,3}).  (4) centre count: slack 0 (the bound of `card_centres_near` is
attained).  (5) Theorem 3 point mass: M_1 = 8, uniform measure on C has point mass 1/8 = bound
(attained).  (6) 20000 random pairs: min(KL − 2TV²) = 3.7e-10, min(J − 4TV²) = 7.6e-10.
(7) Theorem 7 on 196 of 200 random instances (4 discarded: BFGS did not match the moments to 1e-7):
|J − β(E_ν r − E_μ r)| ≤ 2.9e-7, TV/(βω/4) ≤ 0.726, J/((βω)²/4) ≤ 0.624.
These are sanity checks of statement fidelity, not evidence for the theorems (which are proved).

## Git (observation, 19:38 UTC)

`git status` / `git log` (read-only) show that the files of this directory and `L1_REPORT.md` were
committed by the coordinator's periodic checkpoints (`[SCI] Checkpoint 14–16`, 19:00–19:34 UTC).
I ran no git command that changes state.
