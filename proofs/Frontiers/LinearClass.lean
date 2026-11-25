import Mathlib
import proofs.Frontiers.EnvelopeDuality

/-!
# Residual classes with correlated uncertainty: linear in features

Theory report §11.17.  A first-order (envelope) class treats the uncertainty of the residual
at different configurations as independent up to pairwise constraints, and its certificates
are coverings.  If the residual is **linear in known features** with unknown coefficients in a
box,

  `g(x) = ∑_α θ_α F_α(x)`,   `|θ_α - θ₀_α| ≤ w_α`,

the uncertainty is correlated through the coefficients, and evaluations combine linearly:

* `linRes_sub_le`, `linRes_dev_admissible`, `linRes_sub_attained` — without evaluations the
  class is exactly as wide as the first-order class of the **feature envelope**
  `∑_α w_α |F_α(x) - F_α(y)|` (a pulled-back weighted `ℓ¹` distance), which is an envelope
  (`featEnv_isEnvelope`);
* `sumClass_span_upper`, `sumClass_sub_le` — a first-order remainder on top of the linear part
  adds a transport term to the bracket, weighted by the absolute values of the coefficients;
* `linRes_span_upper`, `linRes_span_lower`, `linRes_span_exact` — after evaluations at points
  `a k`, for **every** choice of coefficients `lam`, the value at `y` lies within
  `∑_α w_α |r_α|` of `∑_k lam k · g(a k) + ∑_α θ₀_α r_α`, where
  `r = F(y) - ∑_k lam k · F(a k)` is the part of the feature vector of `y` not explained by the
  evaluated ones.  McShane's bound is the special case of one unit coefficient.  If the feature
  vector of `y` lies in the span of the evaluated ones, the value is determined exactly: a
  certificate needs at most as many evaluations as there are independent features, whatever
  the size of the configuration space.  (That the bound is attained after minimising over `lam`
  is linear-programming duality — Smolyak's lemma of optimal recovery — and is not formalised.)

**Pair-additive residuals** `g(x) = ∑_k φ(s_k) · cnt_k(x)` — `cnt_k(x)` the number of pairs at the
`k`-th grid distance, `φ` an unknown radial function with `φ = 0` at the cutoff and increments
bounded by `L·Δ_k` — are of this form with the **cumulative pair counts** as features
(`pairRes_eq_cum`, summation by parts).  Hence

* `pairRes_sub_le`, `pairRes_admissible` — the envelope is the weighted `L¹` distance between
  cumulative pair-count profiles (a transport distance between pair-distance distributions);
* `pairRes_span_upper`, `pairRes_span_lower` — the bracket after evaluations is the `L¹` distance
  from the profile of `y` to a linear combination of the evaluated profiles.
-/

namespace MetricChain

open Finset

/-! ### Linear classes -/

section LinearClass

variable {X : Type*} {ι : Type*} [Fintype ι]

/-- A residual that is linear in the features `F` with coefficients `θ`. -/
def linRes (F : X → ι → ℝ) (θ : ι → ℝ) (x : X) : ℝ := ∑ α, θ α * F x α

/-- The feature envelope: the weighted `ℓ¹` distance of feature vectors. -/
def featEnv (w : ι → ℝ) (F : X → ι → ℝ) (x y : X) : ℝ := ∑ α, w α * |F x α - F y α|

/-- The feature envelope is an envelope (a pseudometric) for nonnegative weights. -/
theorem featEnv_isEnvelope {w : ι → ℝ} (hw : ∀ α, 0 ≤ w α) (F : X → ι → ℝ) :
    IsEnvelope (featEnv w F) where
  self := fun x => by simp [featEnv]
  triangle := fun x y z => by
    unfold featEnv
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_le_sum fun α _ => ?_
    rw [← mul_add]
    exact mul_le_mul_of_nonneg_left (abs_sub_le _ _ _) (hw α)

/-- **No evaluations.**  For coefficients in the box around `θ₀`, differences of the residual
exceed those of the centre by at most the feature envelope. -/
theorem linRes_sub_le {F : X → ι → ℝ} {θ θ₀ w : ι → ℝ} (hθ : ∀ α, |θ α - θ₀ α| ≤ w α)
    (x y : X) :
    linRes F θ x - linRes F θ y ≤ (linRes F θ₀ x - linRes F θ₀ y) + featEnv w F x y := by
  unfold linRes featEnv
  rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
  refine Finset.sum_le_sum fun α _ => ?_
  have h2 : (θ α - θ₀ α) * (F x α - F y α) ≤ w α * |F x α - F y α| :=
    calc (θ α - θ₀ α) * (F x α - F y α) ≤ |(θ α - θ₀ α) * (F x α - F y α)| := le_abs_self _
      _ = |θ α - θ₀ α| * |F x α - F y α| := abs_mul _ _
      _ ≤ w α * |F x α - F y α| := mul_le_mul_of_nonneg_right (hθ α) (abs_nonneg _)
  nlinarith [h2]

/-- The deviation of a member of the linear class from its centre is admissible for the
feature envelope: the linear class is contained in a first-order class. -/
theorem linRes_dev_admissible {F : X → ι → ℝ} {θ θ₀ w : ι → ℝ}
    (hθ : ∀ α, |θ α - θ₀ α| ≤ w α) :
    Admissible (featEnv w F) fun x => linRes F θ x - linRes F θ₀ x := by
  intro x y
  have := linRes_sub_le (F := F) hθ x y
  linarith

/-- **The feature envelope is attained**: for every pair of configurations some member of the
linear class realises the full envelope distance. -/
theorem linRes_sub_attained (F : X → ι → ℝ) (θ₀ : ι → ℝ) {w : ι → ℝ} (hw : ∀ α, 0 ≤ w α)
    (x y : X) :
    ∃ θ : ι → ℝ, (∀ α, |θ α - θ₀ α| ≤ w α) ∧
      linRes F θ x - linRes F θ y = (linRes F θ₀ x - linRes F θ₀ y) + featEnv w F x y := by
  refine ⟨fun α => θ₀ α + (if 0 ≤ F x α - F y α then w α else -w α), fun α => ?_, ?_⟩
  · have : θ₀ α + (if 0 ≤ F x α - F y α then w α else -w α) - θ₀ α =
        (if 0 ≤ F x α - F y α then w α else -w α) := by ring
    rw [this]
    split_ifs
    · rw [abs_of_nonneg (hw α)]
    · rw [abs_neg, abs_of_nonneg (hw α)]
  · unfold linRes featEnv
    rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun α _ => ?_
    beta_reduce
    by_cases h : 0 ≤ F x α - F y α
    · rw [if_pos h, abs_of_nonneg h]
      ring
    · rw [if_neg h, abs_of_neg (not_le.mp h)]
      ring

variable {κ : Type*} [Fintype κ]

/-- The residual at `y` minus a linear combination of evaluated values is the coefficient
vector applied to the unexplained part of the feature vector. -/
theorem linRes_sub_comb (F : X → ι → ℝ) (θ : ι → ℝ) (a : κ → X) (lam : κ → ℝ) (y : X) :
    linRes F θ y - ∑ k, lam k * linRes F θ (a k) =
      ∑ α, θ α * (F y α - ∑ k, lam k * F (a k) α) := by
  unfold linRes
  have hswap : ∑ k, lam k * ∑ α, θ α * F (a k) α = ∑ α, θ α * ∑ k, lam k * F (a k) α := by
    simp_rw [Finset.mul_sum]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun α _ => Finset.sum_congr rfl fun k _ => ?_
    ring
  rw [hswap, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun α _ => ?_
  ring

/-- **Span bracket, upper end.**  For every choice of coefficients `lam`, the value at `y` is at
most the combination of the evaluated values, plus the centre applied to the unexplained part
`r` of the feature vector, plus `∑ w |r|`. -/
theorem linRes_span_upper {F : X → ι → ℝ} {θ θ₀ w : ι → ℝ} (hθ : ∀ α, |θ α - θ₀ α| ≤ w α)
    (a : κ → X) (lam : κ → ℝ) (y : X) :
    linRes F θ y ≤ ∑ k, lam k * linRes F θ (a k) +
      ∑ α, θ₀ α * (F y α - ∑ k, lam k * F (a k) α) +
      ∑ α, w α * |F y α - ∑ k, lam k * F (a k) α| := by
  have h := linRes_sub_comb F θ a lam y
  have hle : ∑ α, θ α * (F y α - ∑ k, lam k * F (a k) α) ≤
      ∑ α, θ₀ α * (F y α - ∑ k, lam k * F (a k) α) +
      ∑ α, w α * |F y α - ∑ k, lam k * F (a k) α| := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_le_sum fun α _ => ?_
    have h2 : (θ α - θ₀ α) * (F y α - ∑ k, lam k * F (a k) α) ≤
        w α * |F y α - ∑ k, lam k * F (a k) α| :=
      calc (θ α - θ₀ α) * (F y α - ∑ k, lam k * F (a k) α)
          ≤ |(θ α - θ₀ α) * (F y α - ∑ k, lam k * F (a k) α)| := le_abs_self _
        _ = |θ α - θ₀ α| * |F y α - ∑ k, lam k * F (a k) α| := abs_mul _ _
        _ ≤ w α * |F y α - ∑ k, lam k * F (a k) α| :=
            mul_le_mul_of_nonneg_right (hθ α) (abs_nonneg _)
    nlinarith [h2]
  linarith

/-- **Span bracket, lower end.** -/
theorem linRes_span_lower {F : X → ι → ℝ} {θ θ₀ w : ι → ℝ} (hθ : ∀ α, |θ α - θ₀ α| ≤ w α)
    (a : κ → X) (lam : κ → ℝ) (y : X) :
    ∑ k, lam k * linRes F θ (a k) +
      ∑ α, θ₀ α * (F y α - ∑ k, lam k * F (a k) α) -
      ∑ α, w α * |F y α - ∑ k, lam k * F (a k) α| ≤ linRes F θ y := by
  have h := linRes_sub_comb F θ a lam y
  have hge : ∑ α, θ₀ α * (F y α - ∑ k, lam k * F (a k) α) -
      ∑ α, w α * |F y α - ∑ k, lam k * F (a k) α| ≤
      ∑ α, θ α * (F y α - ∑ k, lam k * F (a k) α) := by
    rw [← Finset.sum_sub_distrib]
    refine Finset.sum_le_sum fun α _ => ?_
    have h2 : -(w α * |F y α - ∑ k, lam k * F (a k) α|) ≤
        (θ α - θ₀ α) * (F y α - ∑ k, lam k * F (a k) α) :=
      calc -(w α * |F y α - ∑ k, lam k * F (a k) α|)
          ≤ -(|θ α - θ₀ α| * |F y α - ∑ k, lam k * F (a k) α|) :=
            neg_le_neg (mul_le_mul_of_nonneg_right (hθ α) (abs_nonneg _))
        _ = -|(θ α - θ₀ α) * (F y α - ∑ k, lam k * F (a k) α)| := by rw [abs_mul]
        _ ≤ (θ α - θ₀ α) * (F y α - ∑ k, lam k * F (a k) α) := neg_abs_le _
    nlinarith [h2]
  linarith

/-- **Exact determination.**  If the feature vector of `y` is a linear combination of the
evaluated feature vectors, the value at `y` is the same combination of the evaluated values —
for every coefficient vector, in the box or not. -/
theorem linRes_span_exact (F : X → ι → ℝ) (θ : ι → ℝ) (a : κ → X) (lam : κ → ℝ) (y : X)
    (hspan : ∀ α, F y α = ∑ k, lam k * F (a k) α) :
    linRes F θ y = ∑ k, lam k * linRes F θ (a k) := by
  have h := linRes_sub_comb F θ a lam y
  have hz : ∑ α, θ α * (F y α - ∑ k, lam k * F (a k) α) = 0 := by
    refine Finset.sum_eq_zero fun α _ => ?_
    rw [hspan α, sub_self, mul_zero]
  linarith

/-- **Linear part plus a first-order remainder.**  Let the residual be a member of the linear
class plus a remainder `ρ` that is admissible for an envelope `d`.  For coefficients that sum
to one, the span bracket holds with one more term: the remainder is transported from the
evaluated points to `y`, each unit of positive coefficient at cost `d y (a k)`, each unit of
negative coefficient at cost `d (a k) y`.  So with a remainder the size of the coefficients
matters: combinations that reach far, or that use large coefficients of both signs, pay for
it. -/
theorem sumClass_span_upper {F : X → ι → ℝ} {θ θ₀ w : ι → ℝ} (hθ : ∀ α, |θ α - θ₀ α| ≤ w α)
    {d : X → X → ℝ} {ρ : X → ℝ} (hρ : Admissible d ρ) (a : κ → X) (lam : κ → ℝ)
    (hlam : ∑ k, lam k = 1) (y : X) :
    linRes F θ y + ρ y ≤ ∑ k, lam k * (linRes F θ (a k) + ρ (a k)) +
      ∑ α, θ₀ α * (F y α - ∑ k, lam k * F (a k) α) +
      ∑ α, w α * |F y α - ∑ k, lam k * F (a k) α| +
      ∑ k, (max (lam k) 0 * d y (a k) + max (-lam k) 0 * d (a k) y) := by
  have hlin := linRes_span_upper (F := F) hθ a lam y
  have hrem : ρ y - ∑ k, lam k * ρ (a k) ≤
      ∑ k, (max (lam k) 0 * d y (a k) + max (-lam k) 0 * d (a k) y) := by
    have hy : ρ y = ∑ k, lam k * ρ y := by rw [← Finset.sum_mul, hlam, one_mul]
    rw [hy, ← Finset.sum_sub_distrib]
    refine Finset.sum_le_sum fun k _ => ?_
    have h1 := hρ y (a k)
    have h2 := hρ (a k) y
    by_cases hk : 0 ≤ lam k
    · rw [max_eq_left hk, max_eq_right (by linarith : -lam k ≤ 0), zero_mul, add_zero]
      nlinarith [mul_le_mul_of_nonneg_left h1 hk]
    · have hk' : lam k ≤ 0 := (not_le.mp hk).le
      rw [max_eq_right hk', max_eq_left (by linarith : (0 : ℝ) ≤ -lam k), zero_mul, zero_add]
      nlinarith [mul_le_mul_of_nonneg_left h2 (by linarith : (0 : ℝ) ≤ -lam k)]
  have hsplit : ∑ k, lam k * (linRes F θ (a k) + ρ (a k)) =
      ∑ k, lam k * linRes F θ (a k) + ∑ k, lam k * ρ (a k) := by
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun k _ => by ring
  rw [hsplit]
  linarith

/-- The sum of a linear class and a first-order class is contained in the first-order class of
the sum of the two envelopes (around the centre): the case of one evaluated point. -/
theorem sumClass_sub_le {F : X → ι → ℝ} {θ θ₀ w : ι → ℝ} (hθ : ∀ α, |θ α - θ₀ α| ≤ w α)
    {d : X → X → ℝ} {ρ : X → ℝ} (hρ : Admissible d ρ) (x y : X) :
    (linRes F θ x + ρ x) - (linRes F θ y + ρ y) ≤
      (linRes F θ₀ x - linRes F θ₀ y) + featEnv w F x y + d x y := by
  have h1 := linRes_sub_le (F := F) hθ x y
  have h2 := hρ x y
  linarith

end LinearClass

/-! ### Pair-additive residuals: cumulative pair counts -/

section PairAdditive

variable {X : Type*}

/-- A pair-additive residual on a grid of distances: `cnt x k` pairs of the configuration `x`
sit at the `k`-th grid distance, `k < m`, and each contributes `φ k`. -/
def pairRes (φ : ℕ → ℝ) (cnt : X → ℕ → ℝ) (m : ℕ) (x : X) : ℝ := ∑ k ∈ range m, φ k * cnt x k

/-- The cumulative pair count: the number of pairs at grid distances `0, …, k`. -/
def cumCount (cnt : X → ℕ → ℝ) (x : X) (k : ℕ) : ℝ := ∑ j ∈ range (k + 1), cnt x j

/-- Summation by parts. -/
theorem sum_mul_eq_sum_diff_mul_cum (φ c : ℕ → ℝ) (m : ℕ) :
    ∑ k ∈ range m, φ k * c k = φ m * ∑ j ∈ range m, c j +
      ∑ k ∈ range m, (φ k - φ (k + 1)) * ∑ j ∈ range (k + 1), c j := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ, ih, Finset.sum_range_succ (fun k => (φ k - φ (k + 1)) *
      ∑ j ∈ range (k + 1), c j), Finset.sum_range_succ c]
    ring

/-- **A pair-additive residual is linear in the cumulative pair counts**, with the increments
of the radial function as coefficients, when the radial function vanishes at the cutoff. -/
theorem pairRes_eq_cum (φ : ℕ → ℝ) (cnt : X → ℕ → ℝ) (m : ℕ) (hφm : φ m = 0) (x : X) :
    pairRes φ cnt m x = ∑ k ∈ range m, (φ k - φ (k + 1)) * cumCount cnt x k := by
  unfold pairRes cumCount
  rw [sum_mul_eq_sum_diff_mul_cum, hφm, zero_mul, zero_add]

/-- The profile envelope: `L` times the weighted `L¹` distance between cumulative pair-count
profiles, `Δ k` the length of the `k`-th grid cell. -/
def profEnv (L : ℝ) (Δ : ℕ → ℝ) (cnt : X → ℕ → ℝ) (m : ℕ) (x y : X) : ℝ :=
  ∑ k ∈ range m, L * Δ k * |cumCount cnt x k - cumCount cnt y k|

/-- The profile envelope is an envelope. -/
theorem profEnv_isEnvelope {L : ℝ} {Δ : ℕ → ℝ} (hL : 0 ≤ L) (hΔ : ∀ k, 0 ≤ Δ k)
    (cnt : X → ℕ → ℝ) (m : ℕ) : IsEnvelope (profEnv L Δ cnt m) where
  self := fun x => by simp [profEnv]
  triangle := fun x y z => by
    unfold profEnv
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_le_sum fun k _ => ?_
    rw [← mul_add]
    exact mul_le_mul_of_nonneg_left (abs_sub_le _ _ _) (mul_nonneg hL (hΔ k))

variable {κ : Type*} [Fintype κ]

/-- **Span bracket for pair-additive residuals, upper end.**  If the radial function vanishes
at the cutoff and its increments are bounded by `L · Δ k`, then for every choice of
coefficients the value at `y` exceeds the combination of the evaluated values by at most `L`
times the weighted `L¹` distance between the cumulative profile of `y` and the same combination
of the evaluated profiles. -/
theorem pairRes_span_upper {φ : ℕ → ℝ} {Δ : ℕ → ℝ} {L : ℝ} {m : ℕ} (hφm : φ m = 0)
    (hφ : ∀ k < m, |φ k - φ (k + 1)| ≤ L * Δ k) (cnt : X → ℕ → ℝ) (a : κ → X) (lam : κ → ℝ)
    (y : X) :
    pairRes φ cnt m y ≤ ∑ i, lam i * pairRes φ cnt m (a i) +
      ∑ k ∈ range m, L * Δ k * |cumCount cnt y k - ∑ i, lam i * cumCount cnt (a i) k| := by
  have hswap : ∑ i, lam i * pairRes φ cnt m (a i) =
      ∑ k ∈ range m, (φ k - φ (k + 1)) * ∑ i, lam i * cumCount cnt (a i) k := by
    simp_rw [pairRes_eq_cum φ cnt m hφm, Finset.mul_sum]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun k _ => Finset.sum_congr rfl fun i _ => ?_
    ring
  rw [hswap, pairRes_eq_cum φ cnt m hφm, ← Finset.sum_add_distrib]
  refine Finset.sum_le_sum fun k hk => ?_
  have hk' := Finset.mem_range.mp hk
  have h2 : (φ k - φ (k + 1)) * (cumCount cnt y k - ∑ i, lam i * cumCount cnt (a i) k) ≤
      L * Δ k * |cumCount cnt y k - ∑ i, lam i * cumCount cnt (a i) k| :=
    calc (φ k - φ (k + 1)) * (cumCount cnt y k - ∑ i, lam i * cumCount cnt (a i) k)
        ≤ |(φ k - φ (k + 1)) * (cumCount cnt y k - ∑ i, lam i * cumCount cnt (a i) k)| :=
          le_abs_self _
      _ = |φ k - φ (k + 1)| * |cumCount cnt y k - ∑ i, lam i * cumCount cnt (a i) k| :=
          abs_mul _ _
      _ ≤ L * Δ k * |cumCount cnt y k - ∑ i, lam i * cumCount cnt (a i) k| :=
          mul_le_mul_of_nonneg_right (hφ k hk') (abs_nonneg _)
  nlinarith [h2]

/-- **Span bracket for pair-additive residuals, lower end.** -/
theorem pairRes_span_lower {φ : ℕ → ℝ} {Δ : ℕ → ℝ} {L : ℝ} {m : ℕ} (hφm : φ m = 0)
    (hφ : ∀ k < m, |φ k - φ (k + 1)| ≤ L * Δ k) (cnt : X → ℕ → ℝ) (a : κ → X) (lam : κ → ℝ)
    (y : X) :
    ∑ i, lam i * pairRes φ cnt m (a i) -
      ∑ k ∈ range m, L * Δ k * |cumCount cnt y k - ∑ i, lam i * cumCount cnt (a i) k| ≤
      pairRes φ cnt m y := by
  have hneg := pairRes_span_upper (φ := fun k => -φ k) (Δ := Δ) (L := L) (m := m)
    (by simp [hφm]) (fun k hk => by
      have := hφ k hk
      have e : -φ k - -φ (k + 1) = -(φ k - φ (k + 1)) := by ring
      rw [e, abs_neg]
      exact this) cnt a lam y
  have e1 : pairRes (fun k => -φ k) cnt m y = -pairRes φ cnt m y := by
    unfold pairRes
    rw [← Finset.sum_neg_distrib]
    exact Finset.sum_congr rfl fun k _ => by ring
  have e2 : ∑ i, lam i * pairRes (fun k => -φ k) cnt m (a i) =
      -∑ i, lam i * pairRes φ cnt m (a i) := by
    rw [← Finset.sum_neg_distrib]
    refine Finset.sum_congr rfl fun i _ => ?_
    unfold pairRes
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_neg_distrib]
    refine Finset.sum_congr rfl fun k _ => ?_
    beta_reduce
    ring
  rw [e1, e2] at hneg
  linarith

/-- **The transport envelope.**  Differences of a pair-additive residual are bounded by the
profile envelope: `g(x) - g(y) ≤ L ∑_k Δ_k |N_k(x) - N_k(y)|`. -/
theorem pairRes_sub_le {φ : ℕ → ℝ} {Δ : ℕ → ℝ} {L : ℝ} {m : ℕ} (hφm : φ m = 0)
    (hφ : ∀ k < m, |φ k - φ (k + 1)| ≤ L * Δ k) (cnt : X → ℕ → ℝ) (x y : X) :
    pairRes φ cnt m x - pairRes φ cnt m y ≤ profEnv L Δ cnt m x y := by
  have h := pairRes_span_upper hφm hφ cnt (fun _ : Unit => y) (fun _ => 1) x
  simp only [Finset.univ_unique, Finset.sum_singleton, one_mul] at h
  unfold profEnv
  linarith

/-- A pair-additive residual is admissible for the profile envelope. -/
theorem pairRes_admissible {φ : ℕ → ℝ} {Δ : ℕ → ℝ} {L : ℝ} {m : ℕ} (hφm : φ m = 0)
    (hφ : ∀ k < m, |φ k - φ (k + 1)| ≤ L * Δ k) (cnt : X → ℕ → ℝ) :
    Admissible (profEnv L Δ cnt m) (pairRes φ cnt m) :=
  fun x y => pairRes_sub_le hφm hφ cnt x y

end PairAdditive

end MetricChain
