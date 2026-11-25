# Workstream L1 — machine-checking the science division's core statements

*Lean 4.31.0 + Mathlib `v4.31.0` (commit `fabf563a`).  Files: `experiments/science/ws_L1/*.lean`;
log: `experiments/science/ws_L1/NOTES.md`.  2026-11-25.*

Labels: **[V]** machine-checked here (declaration named) · **[P]** paper proof · **[K]** known ·
**[N]** numerical only.  Every **[V]** below means: the file checks with
`lake env lean <file>` and `#print axioms <declaration>` returns exactly
`[propext, Classical.choice, Quot.sound]`; no `sorry`, `admit`, `native_decide` or axiom occurs
in any file.

---

## 1. Verdicts

All four priority targets are done, and two of the division's theorems that were targeted only
through their "algebraic core" are now machine-checked **as theorems**.
(1) The soundness of the three identified-set certificate formats of `INFERENCE_LIMITS.md` §8 and
of the falsification certificate of Theorem 8(b),(c) is **[V]**, including the divergence-ball
format (via a direct proof of the Gibbs variational / Donsker–Varadhan inequality on a finite
type).  (2) The separation inequality of Theorem 4′ is **[V]**, abstractly and for the Hamming
distance to a translated code; beyond the brief, **Theorems 4 and 4′ themselves are [V]** as
corollaries of the theory division's machine-checked packing bounds, in an explicit model of an
oracle-assisted algorithm.  (3) Lemma 1 is **[V]** for every finite field.  (4) **Theorem 7 is
[V] in full, (i)–(v), with no Pinsker hypothesis**: Mathlib `v4.31.0` has no Pinsker inequality,
but the theorem needs only the symmetrised inequality `4·TV² ≤ KL(p‖q) + KL(q‖p)`, which has a
short direct proof.  No statement of the notes was found false.  Three places where the formal
statement had to differ from the text are listed in §2.6; the one of substance is that the proof
of Theorem 4′ (and of Theorem 4) invokes the theory division's theorems for a kind of algorithm
those theorems do not literally cover.

## 2. Statements

### 2.1 Table: statement of the note → Lean declaration

`axioms` column: "std" = `[propext, Classical.choice, Quot.sound]` (output of `#print axioms`,
recorded from the last check of each file).

| statement of the note | Lean declaration | file | hypotheses as formalised | axioms | difference from the paper statement |
|---|---|---|---|---|---|
| §8, model-free certificate: `sup{E_μψ : E_μΦ ∈ D} ≤ h_D(λ) + max_x[ψ − λ·Φ]` | `modelFree_certificate_sound_support` | `IdentifiedSets.lean` | `μ ≥ 0`, `Σμ = 1`, `E_μΦ ∈ D` (`D` any set), `h` an upper bound of `λ·m` on `D`, `M` an upper bound of `ψ − λ·Φ` | std | soundness only (not the equality at the infimum); `D` need not be convex or compact |
| same, box data with `λ⁺, λ⁻ ≥ 0` (brief 1a) | `modelFree_certificate_sound` | `IdentifiedSets.lean` | `lo_k ≤ E_μφ_k ≤ hi_k`, `ψ x ≤ t + Λ x` for all `x` | std | none |
| §8, envelope class, "flow with gains" (brief 1b) | `envelope_flow_sound_weights` | `IdentifiedSets.lean` | `w ≥ 0`, `Σ μ₀ w > 0`, `w y ≤ κ x y · w x`, data in homogeneous form, `λ^± ≥ 0`, `F ≥ 0`, `(ψ z − t − Λ z) μ₀ z ≤ Σ_x F x z − Σ_y κ z y F z y` | std | no sign condition on `μ₀` or `κ` is needed |
| same, for `μ = μ₀w/Σμ₀w` and for `μ_g`, `g` admissible (the note's wording) | `envelope_flow_sound_normalised`, `envelope_flow_sound_gibbs` | `IdentifiedSets.lean` | `g x − g y ≤ d x y`, `κ = exp(β d)`, `β ≥ 0`, `μ₀ ≥ 0` of positive mass, data on `μ_g ∝ μ₀e^{−βg}` | std | none |
| Theorem 8(c), falsification (brief 1c) | `falsification_sound_weights`, `falsification_sound_ensemble`, `falsification_sound_gibbs`, `theorem8c_falsification` | `IdentifiedSets.lean` | certificate with `ψ ≡ 1`, `t = 0`; conclusion `False` / "no `g` of the class of constant `b` is consistent with the data" | std | the conclusion `b_min(D) > b` as a strict inequality for an infimum is **not** formalised (needs attainment on a compact set); what is proved is that no member of the class is consistent |
| Gibbs variational (Donsker–Varadhan) inequality | `gibbs_variational` | `IdentifiedSets.lean` | `μ ≥ 0`, `Σμ = 1`, `μ₀ ≥ 0`, `μ ≪ μ₀` | std | `μ₀` need not be normalised |
| §8, divergence-ball certificate (brief 1d) | `divergenceBall_certificate_sound` | `IdentifiedSets.lean` | as above, `KL(μ‖μ₀) ≤ ρ`, `η > 0`, `h ≥ h_D(λ)` | std | none |
| Theorem 8(b): `ρ_min(D) ≥ −h_D(λ) − ln E_{μ₀}e^{−λ·Φ}` | `kl_lower_bound_certificate_sound` | `IdentifiedSets.lean` | for every `μ ≪ μ₀` with `E_μΦ ∈ D` | std | the inequality only, not "equality at the supremum" |
| non-vacuity of the flow and falsification certificates | `envelope_flow_certificate_witness`, `falsification_certificate_witness` | `IdentifiedSets.lean` | two states, `κ = 2` | std | — |
| Theorem 4′, separation: `A − F ≥ A₁ − F₁`, `A/F ≥ 1 + (A₁/F₁ − 1)/m`, `ln A − ln F ≥ ln(A₁/F₁) − ln m` | `pSum_sub_flat_mono`, `separation_ratio`, `separation_log` | `Separation.lean` | finite `X`, `dC ≤ d1` pointwise, `u ≥ 0`, any real `R`, `F ≤ m·F₁` (and `m ≥ 1` for the log form) | std | `u ≥ 0` suffices; `m > 0` is derived |
| Theorem 4′, `F ≤ |C|·F₁` and the assembled separation `ln A − ln F ≥ D_R − ln|C|` | `pSum_flat_distToCoset_le`, `separation_distToCoset`, `sensitivity_distToCoset` | `Separation.lean` | `ι → G`, `G` a finite additive commutative group; `C` any non-empty finite set of translations (`0 ∈ C` for the assembled form) | std | no linearity of `C` is used; `D_R` appears as `log(A₁/F₁)`, closed forms not formalised |
| Lemma 1 | `lemma1_uniform_marginals`, `lemma1_binary`, `lemma1_marginals_agree` | `OrthogonalArray.lean` | any finite field `F`; `C` a subspace; every non-zero `u` with `Σ u_i c_i = 0` on `C` has weight `> k`; `Σμ = 1`, `μ(x+a) = μ(x)` for `a ∈ C`; `|S| ≤ k` | std | `μ ≥ 0` not needed; shorter proof (no coset decomposition) |
| Lemma 1, projection onto `S` is onto | `restrict_surjective_of_dual` | `OrthogonalArray.lean` | no non-zero vector supported on `S` is orthogonal to `C` | std | — |
| Lemma 1 is sharp in `|S| ≤ k` | `lemma1_sharp_witness` | `OrthogonalArray.lean` | repetition code `{00,11}` | std | — |
| Theorem 7(i) | `symmKL_eq_of_logRatio`, `theorem7_i_energies` | `MaxEntStability.lean` | `μ, ν` tilts of `μ₀ > 0` with energies differing by `b·Φ + βr`, equal `Φ`-means | std | see next row |
| Theorem 7(i)–(v) | `theorem7` | `MaxEntStability.lean` | `μ₀ > 0`, `β ≥ 0`, `lo ≤ r ≤ hi`, `μ ∝ μ₀e^{−β(λ·Φ+r)}`, `ν ∝ μ₀e^{−βλ'·Φ}`, `E_μΦ = E_νΦ` | std | `ν` is **assumed** of exponential form with matching moments (as the note's proof uses it); `ω` is any `hi − lo`; no Pinsker hypothesis |
| "`ν` is the I-projection" | `expFam_isIProjection`, `pythagoras_expFam` | `MaxEntStability.lean` | as above | std | proves: exponential form with matching moments ⟹ minimiser of `KL(·‖μ₀)` on the moment class; the converse (Csiszár) is not formalised |
| Pinsker step of Theorem 7 | `symm_pinsker` | `MaxEntStability.lean` | `p, q > 0`, total mass 1 | std | the symmetrised inequality `4TV² ≤ KL(p‖q)+KL(q‖p)`, proved directly |
| closing step "`4TV² ≤ J`, `J ≤ ωTV` ⟹ `TV ≤ ω/4`, `J ≤ ω²/4`" | `pinsker_closing`, `pinsker_closing_needs_nonneg` | `MaxEntStability.lean` | **`0 ≤ ω`** | std | false without `0 ≤ ω` (§2.6) |
| **Theorem 4** (whole theorem) | `theorem4_adaptive_marginal_oracle`, `theorem4_binary_cube` | `MarginalOracle.lean` | see §2.4 | std | oracle model made explicit; accuracy convention `ε/2`, gap `> ε` |
| **Theorem 4′** (whole theorem) | `theorem4'_nonadaptive_marginal_oracle`, `theorem4'_binary_cube` | `MarginalOracle.lean` | see §2.4 | std | same; `|B(R−1)|` is `#{y : wt y < R}` |

### 2.2 Identified sets and falsification (`IdentifiedSets.lean`) [V]

`dataLagrangian φ lo hi lp lm z = Σ_k (lp_k (φ_k z − hi_k) − lm_k (φ_k z − lo_k))` is the `Λ(z)`
of the note.  The proofs are the one-line arguments of the note: multiply the pointwise
certificate by the weights and sum; `flow_term_nonpos` is the identity
`Σ_z w z (Σ_x F x z − Σ_y κ z y F z y) = Σ_{x,y} F x y (w y − κ x y w x) ≤ 0`.

Non-vacuity.  `envelope_flow_certificate_witness`: two states, uniform model, `κ = 2`, target
the indicator of one state; the flow `F(false,true) = 1/6` certifies `Eψ ≤ 2/3`, and the weights
`(1, 2)` of the cone attain `2/3` — the format is satisfiable and can be tight.
`falsification_certificate_witness`: same model, data `9/10 ≤ Eφ ≤ 1` (satisfied by the ensemble
`(1/20, 19/20)`); `λ⁻ = 5`, `F(false,true) = 3/4` is a falsification certificate.

Remarks.  (a) The Donsker–Varadhan inequality is proved from `log t ≤ t − 1` in fifteen lines;
neither it nor Pinsker is in Mathlib `v4.31.0` (searched: no file of `.lake/packages` matches
`pinsker`, `donsker`, `varadhan`, `tvDist`, `totalVariationDist`, case-insensitive).  (b) With
the real-valued formula `Σ μ (log μ − log μ₀)` for `KL`, the hypothesis `μ ≪ μ₀` cannot be
dropped (where it fails the true divergence is `+∞` and the claim is trivially true, but the
formula no longer is the divergence).

### 2.3 Lemma 1 (`OrthogonalArray.lean`) [V]

`lemma1_uniform_marginals`: `F` a finite field, `C ≤ ι → F` a subspace such that every non-zero
`u` with `Σ_i u_i c_i = 0` for all `c ∈ C` has `hammingNorm u > k`; `μ` real-valued with
`Σ_x μ x = 1` and `μ (x + a) = μ x` for `a ∈ C`; `S` with `|S| ≤ k`; `y` any pattern.  Then
`Σ_{x : ∀ i ∈ S, x i = y i} μ x = 1 / |F|^{|S|}`.

Proof as formalised: if the projection `π_S(C)` were a proper subspace of `F^S`, a non-zero
functional vanishing on it would be a non-zero dual word supported on `S`
(`Submodule.exists_le_ker_of_lt_top`, `LinearMap.pi_apply_eq_sum_univ`); so every pattern
difference `y' − y` on `S` is the restriction of a codeword `c`, and `x ↦ x + c` maps the
cylinder of `y` onto that of `y'` preserving `μ`.  All `|F|^{|S|}` cylinders have equal weight
and the weights sum to 1.

`lemma1_sharp_witness`: for `C = {00, 11}` the hypothesis holds with `k = 1`, the uniform measure
on `C` is invariant, and its marginal on both coordinates is `1/2 ≠ 1/4`.

### 2.4 Theorems 4 and 4′ (`Separation.lean`, `MarginalOracle.lean`) [V]

**Model.**  An oracle-assisted randomised algorithm is a family
`alg ω o : MetricChain.QueryAlgorithm (ι → F)` of the theory division's query algorithms,
indexed by the seed `ω` (finite probability space `(Ω, P)`) and by the oracle's answer `o`; on
the residual `g` it runs `alg ω (marginalOracle β k g)`.
`marginalOracle β k g S y` is the `μ_g`-probability of `{x | ∀ i ∈ S, x i = y i}` when
`|S| ≤ k` (and `0` otherwise); `marginalOracle_singleton` confirms that for `k ≥ 1` this
contains the one-site marginals.  Class: `HammingLip c g := ∀ x y, g x − g y ≤ c·d_H(x,y)`, which
is definitionally the theory division's `Admissible` for the envelope `c·d_H`
(`hammingLip_iff_admissible`).  Target: `logZ β g = log Σ_x exp(−β g x)`.  A linear code is a
finite set `C ∋ 0` closed under addition and scalar multiplication, of dual distance `> k` in
the form of §2.3.

**Theorem 4 [V]** (`theorem4_adaptive_marginal_oracle`).  `β, c ≥ 0`.  If for every `g` of the
class the output of `alg ω (marginalOracle β k g)` on `g` is within `ε/2` of `logZ β g` with
probability at least `1 − δ`, and `ε < logZ β (dip of radius r at 0) − logZ β 0`, then

    (1 − 2δ) · |F|^n  ≤  ( Σ_ω P ω · #queries of alg ω (marginalOracle β k 0) on 0 ) · |C| · #{y : wt y < r}.

**Theorem 4′ [V]** (`theorem4'_nonadaptive_marginal_oracle`).  If moreover the query set is a
function `Q ω o` of the seed and of the oracle answer only, and
`ε < log(A₁/F₁) − log|C|` with `A₁ = Σ_x exp(−βc·wt x)`, `F₁ = Σ_x exp(−βc·max(wt x, R))`, then

    (1 − 2δ) · |F|^n  ≤  ( Σ_ω P ω · #Q ω (marginalOracle β k 0) ) · |C| · #{y : wt y < R}.

`theorem4_binary_cube`, `theorem4'_binary_cube` are the cases `F = ZMod 2`, `ι = Fin n`
(`|F|^n = 2^n`; over `ZMod 2` closure under scalars is automatic).

Both are obtained from `MetricChain.expected_queries_ge_packing` and
`MetricChain.nonadaptive_expected_queries_ge` applied to the plain algorithm
`alg ω o₀`, `o₀` the oracle's answer at the zero residual, and to the class restricted to
residuals with answer `o₀`.  The supporting facts are all proved in the file:
`distToCoset_lipschitz` (a distance to a set is 1-Lipschitz), `distToCoset_add_mem` (invariance
under the code), `marginalOracle_of_invariant` (Lemma 1 ⟹ the answer on any code-invariant
residual is the uniform one), `card_centres_near` (a point lies within `r` of `s + C` for at most
`|C|·#{wt < r}` centres `s`), `symDip_le_dipAt` and `logZ_anti` (the symmetrised dip lowers the
energy), `separation_distToCoset` (§ A1 of the addenda).

What the formalisation shows about the argument: the separation step uses of `C` only that it is
finite and contains `0`; the counting step uses nothing; linearity and the dual distance enter
only through the oracle.  Not formalised: the closed forms `A₁ = (1+e^{−u})^n`,
`F₁ = Σ_j C(n,j) e^{−u max(j,R)}`, the existence of the BCH codes (§1 "Codes", [K]), and every
asymptotic statement (the Corollary of A1, `θ_hint`, `θ_na`).

### 2.5 Theorem 7 (`MaxEntStability.lean`) [V]

`theorem7`: `X` finite non-empty, `μ₀ > 0`, features `Φ_k`, `β ≥ 0`, `lo ≤ r ≤ hi`,
`μ = expFam μ₀ (β(λ·Φ + r))`, `ν = expFam μ₀ (βλ'·Φ)` (`expFam μ₀ E ∝ μ₀e^{−E}`), and
`E_μΦ_k = E_νΦ_k` for all `k`.  Then, with `TV = ½Σ|μ−ν|` and `ω = hi − lo`:
(i) `KL(μ‖ν) + KL(ν‖μ) = β(E_ν r − E_μ r)`; (ii) `TV ≤ βω/4`; (iii) `KL(μ‖ν)+KL(ν‖μ) ≤ (βω)²/4`;
(iv) `|E_μψ − E_νψ| ≤ (b − a)·βω/4` whenever `a ≤ ψ ≤ b`; (v) `0 ≤ KL(μ‖μ₀) − KL(ν‖μ₀) = KL(μ‖ν) ≤ (βω)²/4`.

The Pinsker step.  `symm_pinsker`: for positive probability vectors,
`4TV(p,q)² ≤ KL(p‖q) + KL(q‖p)`.  Proof: `(a−b)(log a − log b) ≥ 2(a−b)²/(a+b)` for `a, b > 0`
(`sq_div_add_le_mul_log`, from `log a − log b ≥ 2(a−b)/(a+b)` for `a ≥ b`, the first term of
the series of `log((1+x)/(1−x))`, `Real.hasSum_log_sub_log_of_abs_lt_one`), then Cauchy–Schwarz
`(Σ|p−q|)² ≤ Σ (p−q)²/(p+q) · Σ(p+q)`.  This is the inequality "`KL(μ‖ν)+KL(ν‖μ) ≥ 4·TV²`" that
the note obtains from Pinsker twice; proved this way, Theorem 7 does not depend on Pinsker.

`tv_bounded_perturbation` (no features) is a non-vacuous instance:
`TV(μ₀e^{−βr}/Z, μ₀/Z₀) ≤ β(hi−lo)/4`.

### 2.6 Discrepancies between formal statements and the text

1. **Theorems 4 and 4′ cite theorems that do not literally apply (gap in the proof, repaired;
   the statements stand).**  The note proves Theorem 4′ by saying that "the algorithm restricted
   to the family is non-adaptive in the sense of Theorem 11.45(a)" and Theorem 4 by "the
   indistinguishability argument of the theory division's Theorem 11.22".  As machine-checked,
   those theorems (`nonadaptive_expected_queries_ge`, `expected_queries_ge_packing`) are about
   `QueryAlgorithm`, whose consistency axiom — residuals agreeing on the queried points are
   treated alike — **fails for an algorithm that also receives an oracle answer depending on the
   residual**: two residuals can agree on every queried point and have different marginals.
   Moreover `nonadaptive_expected_queries_ge` assumes that the query set is the same for *all*
   residuals.  Counter-instance to the literal application: `X` one binary site, the algorithm
   "query nothing, output a function of the one-site marginal" is a legitimate oracle-assisted
   algorithm and is not a `QueryAlgorithm` (its output differs on residuals that agree on the
   empty set of queried points).  Repair, as formalised: index the algorithm by the oracle
   answer, fix the answer `o₀` common to the family, and apply the theory division's theorems to
   `alg ω o₀` on the class restricted to `{g : oracle answer = o₀}`.  Nothing else in the
   argument changes.
2. **The closing step of Theorem 7 as phrased in the brief is false without `0 ≤ ω`.**
   "`4T² ≤ J` and `J ≤ ωT` imply `T ≤ ω/4` and `J ≤ ω²/4`": take `T = J = 0`, `ω = −1`
   (`pinsker_closing_needs_nonneg` [V]).  With `0 ≤ ω` it holds, and then `0 ≤ T` is not needed
   (`pinsker_closing` [V]).  In the note `ω = β·osc(r) ≥ 0`, so the note is unaffected; `β ≥ 0`
   is an implicit hypothesis of Theorem 7(ii).
3. **Theorem 8(c), "then `b_min(D) > b`".**  The certificate proves that no ensemble of the
   class of constant `b` is consistent with the data [V].  The strict inequality for the
   infimum `b_min(D)` additionally needs the infimum to be attained; that is true for compact
   `D` (the sets `{D_d(·‖μ₀) ≤ b'}` are closed and nested) **[P, not formalised]**, and false in
   general for non-closed `D`.
4. Minor.  (a) Theorem 7: `ν` is defined in the note as the I-projection and then used in
   exponential form; the formal theorem assumes the exponential form with matching moments and
   proves that such a `ν` is the minimiser (`expFam_isIProjection`).  The existence of `λ'` is
   Csiszár's theorem **[K, from memory — unverified]** and is not formalised.  (b) Theorem 4′:
   `|B(R−1)|` equals `#{y : wt y < R}` only for integer `R`; the formal statement uses the
   latter for every real `R`.  (c) Lemma 1 and the certificates hold under weaker hypotheses
   than stated (signed `μ`; any finite field; `μ₀`, `κ` of any sign; unnormalised `μ₀` in
   Donsker–Varadhan).

## 3. Numerics

None was needed for the proofs.  The witnesses of §2.2 and §2.3 are exact rational instances
checked by Lean.

## 4. Prior art / search log

Not a prior-art workstream.  One factual search, on the local copy of Mathlib `v4.31.0`
(`.lake/packages/mathlib`, commit `fabf563a`, 2026-06-15) and of its dependencies:
`grep -rIl -i pinsker .lake/packages/` → no file; `grep -rIl -i "donsker\|varadhan"` → no file;
`grep -rIl -i "tvDist\|totalVariationDist\|total variation distance"` → no file.
`Mathlib/InformationTheory/KullbackLeibler/{Basic,ChainRule,KLFun}.lean` exist [full text of the
declaration lists read] and contain the measure-theoretic `klDiv`, its non-negativity and a chain
rule, but no Pinsker inequality.  **Mathlib `v4.31.0` does not have Pinsker's inequality.**
The theory division's library has `klFin`, `klFin_nonneg_of_dominated`, `logMGF_eq_tilt`,
`kl_reference_target_eq_gap` and no Pinsker either.

## 5. Not done

* Brief target 5 (Theorem 3, Theorem 2(d)) — see the end of this file for what was added after
  the first version of this report.
* Completeness of the certificates (LP duality), the equality cases of Theorem 8(b).
* The strict inequality `b_min(D) > b` (§2.6, item 3).
* Closed forms of `A₁`, `F₁`; existence of codes with `|C| ≤ (2n)^{⌈k/2⌉}`; all asymptotics.
* That the I-projection has exponential form.
* Pinsker's inequality proper (`KL ≥ 2TV²`) — not needed by any statement of the notes.

## 6. Next steps

1. Formalise the BCH/Reed–Muller existence statement at least for one explicit family (simplex
   codes: dual distance 3, `|C| = n+1`), so that Theorems 4/4′ have a machine-checked instance
   with `k = 2` and polynomial `|C|`.
2. The closed forms `A₁ = (1+e^{−u})^n`, `F₁ = Σ_j C(n,j)e^{−u max(j,R)}` (also missing from the
   theory division's `cube_nonadaptive_bound`), to state Theorem 4′ with the note's `D_R`.
3. Pinsker's inequality on a finite type (Kemperman's scalar inequality + Cauchy–Schwarz), as a
   reusable lemma for both divisions.

## 7. Requests

**To the theory division.**  (a) `nonadaptive_expected_queries_ge` uses its hypothesis
`hna : ∀ ω g, (alg ω).queries g = Q ω` only at the first members `g j` of the pairs; stating it
as `∀ ω j, (alg ω).queries (g j) = Q ω` would make it directly applicable to algorithms that are
non-adaptive only on a family (our Theorem 4′).  (b) Consider adding side information to
`QueryAlgorithm` (a structure indexed by an oracle answer, or a consistency axiom conditional on
equal answers); `experiments/science/ws_L1/MarginalOracle.lean` shows the indexed form suffices.

**To the engineering division.**  None.
