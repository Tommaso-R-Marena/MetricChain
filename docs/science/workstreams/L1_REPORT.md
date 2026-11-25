# Workstream L1 — machine-checking the science division's core statements

*Lean 4.31.0 + Mathlib `v4.31.0` (commit `fabf563a`).  Eight files, 3 910 lines, in
`experiments/science/ws_L1/`; log `NOTES.md`; last full check `check_log.txt` (2026-11-25,
19:42–19:43 UTC).*

Labels: **[V]** machine-checked here (declaration named) · **[P]** paper proof given here ·
**[K]** known · **[N]** numerical only.

**What [V] means in this file.**  The declaration is in one of the eight files; each file was
checked on its own with
`export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path>`;
exit code 0, no error, no warning; and `#print axioms <declaration>` printed exactly
`[propext, Classical.choice, Quot.sound]`.  This holds for all 78 declarations listed at the
ends of the files (`check_log.txt`).  No `sorry`, `admit`, `native_decide` or `axiom` occurs in
any file (`grep`).  Seven files import only `Mathlib`; `MarginalOracle.lean` also imports,
read-only, `proofs.Frontiers.NonAdaptive` of the theory division.  Nothing was written under
`proofs/`.

---

## 1. Verdicts

All four priority targets of the brief are done, the optional fifth (Theorem 3) is done in its
core form, and several statements that were targeted only through an "algebraic core" are now
machine-checked as theorems.
(1) The soundness of the three identified-set certificate formats of `INFERENCE_LIMITS.md` §8 and
of the falsification certificates of Theorem 8(b),(c) is **[V]**, including the divergence-ball
format (with a direct proof of the Donsker–Varadhan inequality on a finite type).
(2) The separation inequality of Theorem 4′ is **[V]**, and beyond it **Theorems 4 and 4′
themselves are [V]**, as corollaries of the theory division's packing bounds in an explicit
model of an oracle-assisted algorithm, with the note's closed form of `D_R` on the binary cube
and an explicit hypothesis-free instance (free knowledge of all one-site marginals lowers either
bound by at most the factor 2).
(3) Lemma 1 is **[V]** for every finite field.
(4) **Theorem 7 is [V] in full, (i)–(v), with no Pinsker hypothesis.**  Mathlib `v4.31.0` has no
Pinsker inequality; the theorem needs only `4·TV² ≤ KL(p‖q) + KL(q‖p)`, which has a short direct
proof.  Pinsker's inequality itself is now also **[V]** on finite types (`Pinsker.lean`).
(5) Also **[V]**: Theorem 3 in Markov form with the point-mass bound `μ({a}) ≤ 1/M_t`;
Theorem 5 (bracket and width identity); Proposition 6 (identifiability); Proposition 9 (caloric
bracket, without the integral); Theorem 7′ of the addenda *with the transport–entropy inequality
as an explicit hypothesis*.
**No statement of the notes was found false.**  Four places where the formal statement had to
differ from the text are in §2.9; the one of substance is that the proofs of Theorems 4 and 4′
invoke the theory division's theorems for a kind of algorithm those theorems do not cover as
stated.  Not formalised: Theorem 2 (any part), the Krawtchouk form of Theorem 3, existence of
codes for `k ≥ 2`, completeness/duality statements, all asymptotics (§5).

## 2. Statements

### 2.1 Table: statement of the note → Lean declaration

All declarations are in namespace `ScienceL1`.  The `#print axioms` output is the same for every
row: `[propext, Classical.choice, Quot.sound]`.

| statement of the note | Lean declaration(s) | file | hypotheses as formalised | difference from the paper statement |
|---|---|---|---|---|
| §8 model-free certificate, `sup{E_μψ : E_μΦ∈D} ≤ h_D(λ) + max_x[ψ−λ·Φ]` | `modelFree_certificate_sound_support` | `IdentifiedSets` | `μ ≥ 0`, `Σμ = 1`, `E_μΦ ∈ D` (`D` any set), `h ≥ λ·m` on `D`, `M ≥ ψ−λ·Φ` | soundness only; `D` need not be convex or compact |
| same for a box, `λ^± ≥ 0` (brief 1a) | `modelFree_certificate_sound` | `IdentifiedSets` | `lo_k ≤ E_μφ_k ≤ hi_k`; `ψ ≤ t + Λ` pointwise | none |
| §8 envelope class, "flow with gains" (brief 1b) | `envelope_flow_sound_weights`, `flow_term_nonpos` | `IdentifiedSets` | `w ≥ 0`, `Σμ₀w > 0`, `w y ≤ κ x y·w x`, homogeneous data, `λ^± ≥ 0`, `F ≥ 0`, `(ψ z−t−Λ z)μ₀ z ≤ Σ_x F x z − Σ_y κ z y F z y` | no sign condition on `μ₀`, `κ` needed |
| same for `μ_g`, `g` admissible (the note's wording) | `envelope_flow_sound_normalised`, `envelope_flow_sound_gibbs` | `IdentifiedSets` | `g x−g y ≤ d x y`, `κ = e^{βd}`, `β ≥ 0`, `μ₀ ≥ 0` of positive mass | none |
| Theorem 8(c) falsification (brief 1c) | `falsification_sound_weights`, `_ensemble`, `_gibbs`, `theorem8c_falsification` | `IdentifiedSets` | certificate with `ψ ≡ 1`, `t = 0` | conclusion is "no member of the class of constant `b` is consistent with the data"; the strict `b_min(D) > b` is not formalised (§2.9) |
| Donsker–Varadhan inequality | `gibbs_variational` | `IdentifiedSets` | `μ ≥ 0`, `Σμ = 1`, `μ₀ ≥ 0`, `μ ≪ μ₀` | `μ₀` need not be normalised |
| §8 divergence-ball certificate (brief 1d) | `divergenceBall_certificate_sound` | `IdentifiedSets` | `KL(μ‖μ₀) ≤ ρ`, `η > 0`, `h ≥ h_D(λ)` | none |
| Theorem 8(b), `ρ_min(D) ≥ −h_D(λ) − ln E_{μ₀}e^{−λ·Φ}` | `kl_lower_bound_certificate_sound` | `IdentifiedSets` | every `μ ≪ μ₀` with `E_μΦ ∈ D` | inequality only, not "equality at the supremum" |
| the certificate formats are satisfiable | `envelope_flow_certificate_witness`, `falsification_certificate_witness` | `IdentifiedSets` | two states, `κ = 2` | — |
| Theorem 4′ separation (brief 2, abstract) | `exp_sub_exp_max_antitone`, `pSum_sub_flat_mono`, `separation_ratio`, `separation_log` | `Separation` | finite `X`, `dC ≤ d1`, `u ≥ 0`, real `R`, `F ≤ m·F₁` (`m ≥ 1` for the log form) | `u ≥ 0` suffices; `m > 0` derived |
| `F ≤ |C|·F₁`, `ln A − ln F ≥ D_R − ln|C|` (brief 2, concrete) | `pSum_flat_distToCoset_le`, `separation_distToCoset`, `sensitivity_distToCoset` | `Separation` | `ι → G`, `G` finite additive commutative group; `C` any non-empty finite set (`0 ∈ C` for the assembled form) | no linearity used; `D_R` appears as `log(A₁/F₁)` |
| Lemma 1 (brief 3) | `lemma1_uniform_marginals`, `lemma1_binary`, `lemma1_marginals_agree`, `restrict_surjective_of_dual` | `OrthogonalArray` | finite field `F`; `C` a subspace; every non-zero `u` with `Σu_ic_i = 0` on `C` has weight `> k`; `Σμ = 1`; `μ(x+a) = μ(x)` on `C`; `|S| ≤ k` | `μ ≥ 0` not needed; any finite field |
| Lemma 1 is sharp | `lemma1_sharp_witness` | `OrthogonalArray` | repetition code `{00, 11}`, `k = 1` | — |
| Theorem 7(i) (brief 4) | `symmKL_eq_of_logRatio`, `theorem7_i_energies` | `MaxEntStability` | tilts of `μ₀ > 0`, energies differing by `b·Φ + βr`, equal `Φ`-means | — |
| Theorem 7(i)–(v) | `theorem7` | `MaxEntStability` | `μ₀ > 0`, `β ≥ 0`, `lo ≤ r ≤ hi`, `μ ∝ μ₀e^{−β(λ·Φ+r)}`, `ν ∝ μ₀e^{−βλ'·Φ}`, `E_μΦ = E_νΦ` | `ν` assumed of exponential form (§2.9); `ω := hi − lo`; no Pinsker hypothesis |
| Pinsker step of Theorem 7 | `symm_pinsker`, `sq_div_add_le_mul_log` | `MaxEntStability` | `p, q > 0`, mass 1 | `4TV² ≤ KL(p‖q)+KL(q‖p)` proved directly |
| closing step (brief 4) | `pinsker_closing`, `pinsker_closing_needs_nonneg` | `MaxEntStability` | **`0 ≤ ω`** | false without `0 ≤ ω` (§2.9) |
| "`ν` is the I-projection"; Pythagoras | `expFam_isIProjection`, `pythagoras_expFam` | `MaxEntStability` | as Theorem 7 | exponential form + matching moments ⟹ minimiser; converse not formalised |
| Proposition 6 (identifiability) | `expFam_eq_of_moments_eq` | `MaxEntStability` | `μ₀ > 0`; two members of the family with equal `Φ`-means | the formula for `ln(Z_g/Z_0)` is `kl_true_model` (next file) |
| Theorem 7′ (addenda A2) | `theorem7'_of_transportEntropy`, `theorem7'_observable`, `transport_le_coupling`, `transport_closing` | `MaxEntStability` | a coupling `γ` of `ν`, `μ` with cost `W`; **hypothesis `W² ≤ 2m·KL(μ‖ν)`** (`m = κn`); `r` `c`-Lipschitz for the cost | transport–entropy inequality is a hypothesis (Marton not formalised); stated for one coupling |
| **Theorem 4** | `theorem4_adaptive_marginal_oracle`, `theorem4_binary_cube` | `MarginalOracle` | §2.4 | oracle model explicit; accuracy `ε/2`, gap `> ε` |
| **Theorem 4′** | `theorem4'_nonadaptive_marginal_oracle`, `theorem4'_binary_cube`, `theorem4'_binary_cube_closed_form` | `MarginalOracle` | §2.4 | same; `|B(R−1)|` is `#{y : wt y < R}`; the last one has the note's `D_R` |
| closed forms `A₁ = (1+e^{−u})^n`, `F₁ = Σ_jC(n,j)e^{−u max(j,R)}` | `sum_hammingNorm_binary`, `pSum_weight_binary`, `pSum_flat_binary` | `MarginalOracle` | `Fin n → ZMod 2`, any `φ : ℕ → ℝ` | binary cube only |
| Theorems 4, 4′ for one-body marginals | `theorem4_one_body_marginals`, `theorem4'_one_body_marginals`, `theorem4'_one_body_closed_form`, `repetition_dual_distance` | `MarginalOracle` | `k = 1`, `C = {0ⁿ, 1ⁿ}`; no code hypothesis left | factor `|C|` is `2` |
| Theorem 5, first display | `theorem5_bracket`, `kl_model_true`, `kl_true_model`, `zRatio_eq_partition_ratio` | `PerturbationBracket` | `μ₀ > 0`, `Σμ₀ = 1`, any `g`, any real `β` | sampled (McDiarmid) form not formalised |
| Proposition 9 | `logZ_step`, `meanEnergy_anti`, `caloric_bracket`, `caloric_bracket_width` | `PerturbationBracket` | any energy on a finite non-empty type, any `b 0, …, b m` (monotone for the width) | `ln Z = −∫U` not formalised |
| Theorem 3 | `basin_bound`, `point_mass_le`, `sum_mul_sq_eq_card`, `sum_mul_chi_eq_zero`, `card_subsets_le`, `theorem3_bool`, `theorem3_point_mass_bool` | `BasinBound` | `μ ≥ 0`, `Σμ = 1`, uniform marginals of order `≤ k`, `2t ≤ k`; `B` any set, `m ≤ f_a²` on `B` | Markov form `m·μ(B) ≤ M_t`; `f_a = F_t(d_H(·,a))` (Krawtchouk) not formalised |
| Pinsker's inequality (quoted in §6) | `pinsker`, `pinsker_tv_le`, `kemperman_scalar` | `Pinsker` | `p ≥ 0`, `q > 0`, mass 1, finite type | not in Mathlib; not needed by the notes |

### 2.2 Identified sets and falsification (`IdentifiedSets.lean`) [V]

`dataLagrangian φ lo hi lp lm z = Σ_k (lp_k(φ_k z − hi_k) − lm_k(φ_k z − lo_k))` is the `Λ(z)` of
the note.  The proofs are the note's one-line arguments: multiply the pointwise certificate by
the weights and sum; `flow_term_nonpos` is the identity
`Σ_z w z (Σ_x F x z − Σ_y κ z y F z y) = Σ_{x,y} F x y (w y − κ x y w x) ≤ 0`.

Non-vacuity.  `envelope_flow_certificate_witness`: two states, uniform model, `κ = 2`, target the
indicator of one state; the flow `F(false,true) = 1/6` certifies `Eψ ≤ 2/3`, and the weights
`(1,2)` of the cone attain `2/3`.  `falsification_certificate_witness`: same model, data
`9/10 ≤ Eφ ≤ 1` (satisfied by the ensemble `(1/20, 19/20)`); `λ⁻ = 5`, `F(false,true) = 3/4` is a
falsification certificate.

Remark.  With the real-valued formula `Σμ(log μ − log μ₀)`, the hypothesis `μ ≪ μ₀` of
`gibbs_variational` cannot be dropped (where it fails the divergence is `+∞` and the inequality
is trivially true, but the formula is no longer the divergence).

### 2.3 Lemma 1 (`OrthogonalArray.lean`) [V]

`lemma1_uniform_marginals`: for a finite field `F`, a subspace `C ≤ ι → F` all of whose non-zero
dual words have Hamming weight `> k`, a real `μ` with `Σμ = 1` invariant under `C`, a set `S`
with `|S| ≤ k` and any pattern `y`: `Σ_{x : ∀ i∈S, x i = y i} μ x = 1/|F|^{|S|}`.
Proof as formalised: if `π_S(C)` were a proper subspace of `F^S`, a non-zero functional vanishing
on it would be a non-zero dual word supported on `S`; so every difference of patterns is the
restriction of a codeword `c`, and `x ↦ x + c` carries one cylinder onto the other.  No coset
decomposition and no fibre count is needed.

### 2.4 Theorems 4 and 4′ (`Separation.lean`, `MarginalOracle.lean`) [V]

**Model.**  An oracle-assisted randomised algorithm is a family
`alg ω o : MetricChain.QueryAlgorithm (ι → F)` of the theory division's query algorithms indexed
by the seed `ω` (finite probability space `(Ω, P)`) and by the oracle's answer `o`; on `g` it
runs `alg ω (marginalOracle β k g)`.  `marginalOracle β k g S y` is the `μ_g`-probability of
`{x | ∀ i ∈ S, x i = y i}` if `|S| ≤ k`, and `0` otherwise (`marginalOracle_singleton`: for
`k ≥ 1` it contains the one-site marginals).  Class: `HammingLip c g := ∀ x y, g x − g y ≤ c·d_H(x,y)`
— by definition the theory division's `Admissible` for the envelope `c·d_H`
(`hammingLip_iff_admissible`).  Target `logZ β g = log Σ_x e^{−βg(x)}`.  A linear code is a
finite set `C ∋ 0` closed under addition and scalar multiplication whose non-zero dual words
have weight `> k`.

**Theorem 4 [V]** (`theorem4_adaptive_marginal_oracle`).  `β, c ≥ 0`.  If for every `g` of the
class the output of `alg ω (marginalOracle β k g)` on `g` is within `ε/2` of `logZ β g` with
probability `≥ 1 − δ`, and `ε < logZ β (dip of radius r at 0) − logZ β 0`, then

    (1 − 2δ)·|F|^n  ≤  ( Σ_ω P ω · #queries of alg ω (marginalOracle β k 0) on 0 ) · |C| · #{y : wt y < r}.

**Theorem 4′ [V]** (`theorem4'_nonadaptive_marginal_oracle`).  If the query set is a function
`Q ω o` of the seed and the oracle answer only, and `ε < log(A₁/F₁) − log|C|` with
`A₁ = Σ_x e^{−βc·wt x}`, `F₁ = Σ_x e^{−βc·max(wt x, R)}`, then

    (1 − 2δ)·|F|^n  ≤  ( Σ_ω P ω · #Q ω (marginalOracle β k 0) ) · |C| · #{y : wt y < R}.

`theorem4_binary_cube`, `theorem4'_binary_cube`: `F = ZMod 2`, `ι = Fin n`, `|F|^n = 2^n` (over
`ZMod 2`, "linear" is "contains 0 and is closed under addition").
`theorem4'_binary_cube_closed_form`: the same with the note's
`D_R = n log(1+e^{−u}) − log Σ_j C(n,j)e^{−u max(j,R)}`, `u = βc`, from
`sum_hammingNorm_binary` (`Σ_x φ(wt x) = Σ_j C(n,j)φ(j)` on `F₂ⁿ`).
`theorem4_one_body_marginals`, `theorem4'_one_body_marginals`, `theorem4'_one_body_closed_form`:
`k = 1` with the repetition code (`repetition_dual_distance`): **free and exact knowledge of
every one-site marginal of `μ_g` lowers either lower bound by at most the factor 2**, for every
`n`; no hypothesis about codes remains.  In full, `theorem4'_one_body_closed_form` reads: if the
query set depends only on the seed and on the one-site marginals, the algorithm is
`(ε/2, δ)`-correct on the class, and
`ε < n log(1+e^{−βc}) − log Σ_j C(n,j)e^{−βc·max(j,R)} − log 2`, then
`(1 − 2δ)·2^n ≤ E[#evaluations]·2·#{y : wt y < R}`.

Both theorems are obtained from `MetricChain.expected_queries_ge_packing` and
`MetricChain.nonadaptive_expected_queries_ge` applied to the plain algorithm `alg ω o₀`, `o₀`
the oracle's answer at the zero residual, and to the class restricted to residuals with answer
`o₀`.  Supporting facts proved in the file: `distToCoset_lipschitz`, `distToCoset_add_mem`,
`marginalOracle_of_invariant` (Lemma 1 ⟹ the answer on any code-invariant residual is the
uniform one), `card_centres_near` (a point is within `r` of `s + C` for at most `|C|·#{wt < r}`
centres), `symDip_le_dipAt`, `logZ_anti`, `logZ_dipAt`, `separation_distToCoset`.

What the formalisation shows about the argument: the separation step uses of `C` only that it is
finite and contains `0`; the counting step uses nothing; linearity and the dual distance enter
only through the oracle.

### 2.5 Theorem 7, Proposition 6, Theorem 7′ (`MaxEntStability.lean`) [V]

`theorem7`: `X` finite non-empty, `μ₀ > 0`, `β ≥ 0`, `lo ≤ r ≤ hi`, `ω := hi − lo`,
`μ = expFam μ₀ (β(λ·Φ + r))`, `ν = expFam μ₀ (βλ'·Φ)` (`expFam μ₀ E ∝ μ₀e^{−E}`), `E_μΦ_k = E_νΦ_k`
for all `k`.  Then, with `TV = ½Σ|μ−ν|`:
(i) `KL(μ‖ν)+KL(ν‖μ) = β(E_νr − E_μr)`; (ii) `TV ≤ βω/4`; (iii) `KL(μ‖ν)+KL(ν‖μ) ≤ (βω)²/4`;
(iv) `|E_μψ − E_νψ| ≤ (b−a)·βω/4` for `a ≤ ψ ≤ b`; (v) `0 ≤ KL(μ‖μ₀) − KL(ν‖μ₀) = KL(μ‖ν) ≤ (βω)²/4`.

`symm_pinsker`: `4TV(p,q)² ≤ KL(p‖q) + KL(q‖p)` for positive probability vectors.  Proof:
`(a−b)(log a − log b) ≥ 2(a−b)²/(a+b)` (from `log a − log b ≥ 2(a−b)/(a+b)` for `a ≥ b > 0`, the
first term of the series of `log((1+x)/(1−x))`, Mathlib's
`Real.hasSum_log_sub_log_of_abs_lt_one`), then Cauchy–Schwarz
`(Σ|p−q|)² ≤ Σ(p−q)²/(p+q)·Σ(p+q)`.  This is the inequality the note derives from Pinsker twice.

`expFam_eq_of_moments_eq` (Proposition 6): equal `Φ`-means ⟹ equal ensembles, from (i) with
`r = 0` and `symm_pinsker`.  `tv_bounded_perturbation` (no features) is a non-vacuous instance of
(ii).  `theorem7'_of_transportEntropy`: if a coupling of `ν` and `μ` has cost `W = Σγd` with
`W² ≤ 2m·KL(μ‖ν)` and `r x − r y ≤ c·d x y`, then `W ≤ 2mβc` and `KL(μ‖ν) ≤ 2m(βc)²`;
`theorem7'_observable`: `|E_μψ − E_νψ| ≤ a·2mβc` for `|ψ x − ψ y| ≤ a·d x y`.

### 2.6 Theorem 5 and Proposition 9 (`PerturbationBracket.lean`) [V]

`theorem5_bracket`: for `μ₀ > 0` of mass 1, any `g`, any real `β`, with
`zRatio μ₀ g β = Σμ₀e^{−βg} = Z_g/Z_0` (`zRatio_eq_partition_ratio`) and `tilt μ₀ g β = μ_g`:
`−βE_{μ₀}g ≤ log(Z_g/Z_0) ≤ −βE_{μ_g}g`, and the width equals `KL(μ₀‖μ_g) + KL(μ_g‖μ₀)`.
`caloric_bracket`: `−Σ_j(b_{j+1}−b_j)U(b_j) ≤ log Z(b_m) − log Z(b_0) ≤ −Σ_j(b_{j+1}−b_j)U(b_{j+1})`
for any sequence; `meanEnergy_anti`: `U` is non-increasing; `caloric_bracket_width`: width
`≤ D·(U(b_0) − U(b_m))` for increasing `b` with steps `≤ D`.  Proposition 9 is Theorem 5 applied
on each interval (`logZ_step`); no calculus is used.

### 2.7 Theorem 3 (`BasinBound.lean`) [V]

Alphabet `A` with a balanced sign `s` (`Σ_b s b = 0`, `s² = 1`; `boolSign` on `Bool`),
`chi s T x = Π_{i∈T} s(x i)`, `f_a(x) = Σ_{|T|≤t} χ_T(a)χ_T(x)`, `M_t = #{T : |T| ≤ t} = Σ_{j≤t}C(n,j)`
(`card_subsets_le`).  `sum_mul_chi_eq_zero`: a uniform marginal on `T ≠ ∅` gives `E_μχ_T = 0`.
`sum_mul_sq_eq_card`: `E_μ f_a² = M_t` when `2t ≤ k`.  `basin_bound`: if `m ≤ f_a²` on a set `B`
then `m·μ(B) ≤ M_t`.  `point_mass_le`: `μ({a}) ≤ 1/M_t`.  `theorem3_bool`,
`theorem3_point_mass_bool`: the same on `ι → Bool` with `Σ_{j≤t}C(n,j)`.

### 2.8 Pinsker's inequality (`Pinsker.lean`) [V]

`pinsker`: `p ≥ 0`, `q > 0` probability vectors on a finite type ⟹ `2·TV(p,q)² ≤ KL(p‖q)`;
`pinsker_tv_le`: `TV ≤ √(KL/2)`.  Proof (Kemperman): `kemperman_scalar`,
`3(a−b)² ≤ (2a+4b)(a(log a − log b) − a + b)` for `a ≥ 0`, `b > 0`, from
`G(t) = (2t²+4t)log t − (5t²−4t−1) ≥ 0`, `G(1) = 0`, `G' = 4((t+1)log t − 2(t−1))` of the sign of
`t − 1`; then Cauchy–Schwarz with weights `(2p+4q)/3`.

### 2.9 Discrepancies between formal statements and the text

1. **Theorems 4 and 4′ cite theorems that do not apply as stated (gap in the proofs, repaired;
   the statements stand).**  The note proves Theorem 4′ by "the algorithm restricted to the
   family is non-adaptive in the sense of Theorem 11.45(a)" and Theorem 4 by "the
   indistinguishability argument of the theory division's Theorem 11.22".  As machine-checked,
   those theorems (`nonadaptive_expected_queries_ge`, `expected_queries_ge_packing`) are about
   `QueryAlgorithm`, whose consistency axiom — residuals agreeing on the queried points are
   treated alike — fails for an algorithm that also receives an oracle answer depending on the
   residual.  Formal form of the obstruction **[V]**
   (`queryAlgorithm_output_const_of_no_queries`): a `QueryAlgorithm` that makes no query has a
   constant output, whereas "query nothing and output a function of the one-site marginals" is a
   legitimate oracle-assisted algorithm.  In addition `nonadaptive_expected_queries_ge` assumes
   one query set for *all* residuals.  Repair, as formalised: index the algorithm by the oracle
   answer, fix the answer `o₀` common to the family, and apply the two theorems to `alg ω o₀` on
   the class restricted to `{g : answer = o₀}`.  Nothing else in the argument changes.
2. **The closing step of Theorem 7, as phrased in the brief, is false without `0 ≤ ω`.**
   "`4T² ≤ J` and `J ≤ ωT` imply `T ≤ ω/4` and `J ≤ ω²/4`": `T = J = 0`, `ω = −1`
   (`pinsker_closing_needs_nonneg` **[V]**).  With `0 ≤ ω` it holds and `0 ≤ T` is not needed
   (`pinsker_closing` **[V]**).  The note is unaffected (`ω = β·osc r ≥ 0`), but `β ≥ 0` is an
   implicit hypothesis of Theorem 7(ii).
3. **Theorem 8(c), "then `b_min(D) > b`".**  The certificate proves that no ensemble of the
   class of constant `b` is consistent with the data **[V]**.  The strict inequality for the
   infimum needs attainment.  For closed `D`, `μ₀ > 0` and `d > 0` off the diagonal it holds:
   the sets `{μ : E_μΦ ∈ D, D_d(μ‖μ₀) ≤ b'}`, `b' > b`, are compact, nested, and their
   intersection is the set for `b` **[P, not machine-checked]**.  For non-closed `D` it fails:
   two states, `φ` the indicator of one, `D = (σ(b), 1]` gives `b_min(D) = b` although no member
   of the class is consistent **[P, not machine-checked]**.  The note's standing assumption
   (`D` compact) covers its claim.
4. Minor.  (a) Theorem 7: `ν` is defined as the I-projection and then used in exponential form;
   the formal theorem assumes the exponential form with matching moments and proves that such a
   `ν` minimises `KL(·‖μ₀)` on the moment class (`expFam_isIProjection`).  That the I-projection
   has this form is Csiszár's theorem **[K, from memory — unverified]**, not formalised.
   (b) Theorem 4′: `|B(R−1)| = #{y : wt y < R}` only for integer `R`; the formal statement uses
   the right-hand side for all real `R`.  (c) Theorem 3: the hypothesis "`F_t > 0` on `[0, r]`"
   is not needed for the inequality in Markov form.  (d) Weaker hypotheses suffice in several
   places: signed `μ` and any finite field in Lemma 1; `μ₀`, `κ` of any sign in the flow
   certificate; unnormalised `μ₀` in Donsker–Varadhan; `u ≥ 0` and an arbitrary finite set `C` in
   the separation step.

## 3. Numerics

`experiments/science/ws_L1/sanity_numerics.py` (2.5 s, seed fixed; output in
`sanity_numerics_output.txt`).  Purpose: check that the *formal statements* say what is intended
on a non-trivial instance; the theorems themselves are proved, not inferred from these numbers.
Exact enumeration on `F₂⁷` with the `[7,3]` simplex code (`|C| = 8`; dual distance computed by
brute force: 3, so `k = 2` — a non-trivial instance of the code hypothesis beyond the `k = 1`
instance proved in Lean) **[N]**:

| check | result |
|---|---|
| Lemma 1, random `C`-invariant `μ`: largest deviation of a marginal from `2^{−|S|}` | order 1: `5.6e−17`; order 2: `5.6e−17`; order 3: `4.5e−2` |
| separation, 6 centres, `u ∈ {0.5,1,2}`, `R ∈ {1,2,2.5,3}`: least slack | `|C|F₁ − F`: 1.05; `(A−F)−(A₁−F₁)`: 2.75; log form: 2.1 |
| `card_centres_near`, 6 points, `r ∈ {1,2,2.5,3}`: least slack | 0 (the count is attained) |
| Theorem 3, `t = 1`, `M_1 = 8`: largest point mass | uniform on `C`: `1/8` = bound (attained) |
| 20 000 random pairs, up to 8 points: least `KL − 2TV²`, least `J − 4TV²` | `3.7e−10`, `7.6e−10` |
| Theorem 7, 196 of 200 random instances (4 discarded: moments not matched to `1e−7` by BFGS) | identity (i) to `2.9e−7`; `TV/(βω/4) ≤ 0.726`; `J/((βω)²/4) ≤ 0.624` |

## 4. Search log (one factual question: does Mathlib `v4.31.0` have Pinsker?)

Local copy (`.lake/packages`, Mathlib at `fabf563a`, 2026-06-15), case-insensitive
`grep -rIl`: `pinsker` in all packages → no file; `donsker|varadhan` in `Mathlib/` → no file;
`tvDist|totalVariationDist|total variation distance` in `Mathlib/` → no file.
`Mathlib/InformationTheory/KullbackLeibler/{Basic,ChainRule,KLFun}.lean` [declaration list of
`Basic.lean` read; the other two not opened] contain the measure-theoretic `klDiv` with its
non-negativity; no Pinsker.  **Mathlib `v4.31.0` does not have Pinsker's inequality.**  The
theory division's library has `klFin`, `klFin_nonneg_of_dominated`, `logMGF_eq_tilt`,
`kl_reference_target_eq_gap`, `gibbs_bogoliubov`, and no Pinsker.  Also noted: the lemma
`Real.add_pow_le_pow_mul_pow_of_add_eq_one` named in the brief does not exist under that name.
No literature search was made; no claim of novelty is made for any proof here (all are
textbook arguments).

## 5. Not done, and why

* **Theorem 2**, every part: (a) and (b) are within reach (cone convexity; Lemma 1); (c)–(e)
  need the chain rule for entropy and concavity of the binary entropy on a product type, which
  did not fit.  The entropy lower bound (d) named in the brief is **not** machine-checked.
* Theorem 3: the identification `f_a(x) = F_t(d_H(x,a))` with Krawtchouk polynomials, hence the
  bound for Hamming balls with `min_{d≤r}F_t(d)²`, and the asymptotics.
* Theorems 4/4′: the existence of codes with dual distance `> k` and `|C| ≤ (2n)^{⌈k/2⌉}` for
  `k ≥ 2` (only `k = 1` is proved; `k = 2` on 7 sites is **[N]**); the closed forms for alphabets
  other than `F₂`; the Corollary of A1 and every statement about exponents.
* Completeness statements: equality at the infimum/supremum in §8 and Theorem 8(b) (LP and
  max-entropy duality); `b_min(D) > b` as a strict inequality (§2.9).
* That the I-projection on a linear family has exponential form; Marton's inequality
  (`κ = ¼`); the sampled (McDiarmid) form of Theorem 5; Proposition 5b; `ln Z = −∫U dβ`;
  Proposition 10 and A4 of the addenda; §§7, 11 (numerical sections).

## 6. Three next steps

1. Theorem 2(a),(b),(d): (a),(b) from the cone and Lemma 1; (d) by induction on the number of
   sites (one-step entropy decomposition + the marginal odds of one site lie in `[e^{−b}, e^{b}]`
   + concavity of the binary entropy).
2. A machine-checked code family for `k = 2` (simplex codes: `n = 2^m − 1`, `|C| = n + 1`, dual
   distance 3), which would make Theorems 4/4′ hypothesis-free for pair marginals.
3. The Krawtchouk identity for `f_a`, to state Theorem 3 for Hamming balls.

## 7. Requests

**To the theory division.**
(a) `nonadaptive_expected_queries_ge` uses its hypothesis `hna : ∀ ω g, (alg ω).queries g = Q ω`
only at the first members `g j` of the pairs.  Stating it as `∀ ω j, (alg ω).queries (g j) = Q ω`
makes it apply to algorithms that are non-adaptive only on a family; the proof is unchanged.
(b) `QueryAlgorithm` cannot represent an algorithm with side information that depends on the
residual (`ScienceL1.queryAlgorithm_output_const_of_no_queries`).  If lower bounds "with an
oracle" are to be stated in the theory report, the indexed form
`alg : Answer → QueryAlgorithm X`, run on `g` as `alg (O g)`, suffices and needs no change to the
existing theorems (`experiments/science/ws_L1/MarginalOracle.lean`,
`theorem4_adaptive_marginal_oracle`).
(c) The two sums in the hypothesis `hsens` of `cube_nonadaptive_bound` are left unevaluated in
`NonAdaptive.lean` (its header lists "the closed forms of the sums in `cube_nonadaptive_bound`"
among the items not formalised).  For `Fin n → ZMod 2` they are
now evaluated in `MarginalOracle.lean` (`sum_hammingNorm_binary`: `Σ_x φ(wt x) = Σ_j C(n,j)φ(j)`;
`pSum_weight_binary`; `pSum_flat_binary`); the same thirty lines transfer to `Fin n → Bool`.

**To the engineering division.**  None.

## Appendix: files

| file | lines | headline declarations | imports |
|---|---|---|---|
| `IdentifiedSets.lean` | 590 | 14 | Mathlib |
| `Separation.lean` | 277 | 7 | Mathlib |
| `OrthogonalArray.lean` | 300 | 7 | Mathlib |
| `MaxEntStability.lean` | 678 | 16 | Mathlib |
| `MarginalOracle.lean` | 1220 | 15 | Mathlib, `proofs.Frontiers.NonAdaptive` |
| `PerturbationBracket.lean` | 289 | 8 | Mathlib |
| `BasinBound.lean` | 336 | 8 | Mathlib |
| `Pinsker.lean` | 220 | 3 | Mathlib |

The files do not import each other; `MarginalOracle.lean` therefore repeats the proofs of
Lemma 1 and of the separation inequality verbatim, `Pinsker.lean` repeats one lemma of
`MaxEntStability.lean`, and the definition `klDivFin` appears in four files.  In the final pass
each check took 6–8 s of wall time (earlier single runs: 14–63 s).
