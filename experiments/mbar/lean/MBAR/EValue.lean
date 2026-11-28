import Mathlib
import MBAR.Allocation

/-!
# The stratified likelihood-ratio e-value (finite support)

Division 9, `docs/mbar/MATHEMATICS.md` Theorem B1.  A stratified sample consists of `n k`
independent draws from each state `k`.  For a product statistic `T(x) = Π_k Π_i g_k(x_{k,i})`:

* `expect_stat`       : `E[T] = Π_k (E_k g_k)^{n_k}`                      (independence);
* `prod_pow_le_one`   : `Π_k b_k^{n_k} ≤ 1` whenever `Σ_k n_k b_k ≤ Σ_k n_k`  (weighted AM–GM);
* `stratified_evalue` : hence `E[T] ≤ 1` whenever `Σ_k n_k E_k g_k ≤ N`;
* `lr_family_evalue`  : the family `g_k = λ_k · m_w / (s_k p_k)` — any label predictor `λ`
  (`Σ_k λ_k ≤ 1`) and any tilt `w` (`Σ w ≤ 1`) — satisfies the hypothesis.  With `λ = π(f')`
  and `w = s` this is the reverse-logistic likelihood ratio `Π π_{y}(f')/π_{y}(f*)`;
* `markov_finite`     : therefore `P(T ≥ 1/a) ≤ a`: the confidence region `{f : T_f < 1/a}`
  misses the truth with probability at most `a`, at every sample size.

Not formalised: the sequential statement (Ville's inequality for the product over batches with
predictable plug-ins) — an external theorem, labelled [X] in the mathematics note.
-/

open Finset

namespace MBAR

namespace Model

variable {ι α : Type*} [Fintype ι] [Fintype α] [DecidableEq ι] (M : Model ι α)

/-- A stratified sample: `n k` points for each state `k`. -/
abbrev Sample (n : ι → ℕ) (α : Type*) := (k : ι) → Fin (n k) → α

/-- Probability of a stratified sample of independent draws. -/
def prob (n : ι → ℕ) (x : Sample n α) : ℝ := ∏ k, ∏ i, M.p k (x k i)

/-- A product statistic `Π_k Π_i g_k(x_{k,i})`. -/
def stat (n : ι → ℕ) (g : ι → α → ℝ) (x : Sample n α) : ℝ := ∏ k, ∏ i, g k (x k i)

omit [DecidableEq ι] in
lemma prob_nonneg (n : ι → ℕ) (x : Sample n α) : 0 ≤ M.prob n x :=
  Finset.prod_nonneg (fun k _ => Finset.prod_nonneg (fun i _ => M.nonneg k (x k i)))

omit [Fintype α] [DecidableEq ι] in
lemma stat_nonneg (n : ι → ℕ) {g : ι → α → ℝ} (hg : ∀ k x, 0 ≤ g k x) (x : Sample n α) :
    0 ≤ stat n g x :=
  Finset.prod_nonneg (fun k _ => Finset.prod_nonneg (fun i _ => hg k (x k i)))

/-- **Independence**: the expectation of a product statistic factorises. -/
theorem expect_stat (n : ι → ℕ) (g : ι → α → ℝ) :
    ∑ x : Sample n α, M.prob n x * stat n g x = ∏ k, (M.E k (g k)) ^ n k := by
  have h1 : ∀ x : Sample n α, M.prob n x * stat n g x
      = ∏ k, ∏ i, (M.p k (x k i) * g k (x k i)) := by
    intro x
    simp only [prob, stat, ← Finset.prod_mul_distrib]
  simp only [h1]
  have h2 : ∀ k, (M.E k (g k)) ^ n k
      = ∑ y : Fin (n k) → α, ∏ i, (M.p k (y i) * g k (y i)) := by
    intro k
    have h3 := Finset.prod_univ_sum (fun (_ : Fin (n k)) => (Finset.univ : Finset α))
      (fun _ a => M.p k a * g k a)
    rw [Fintype.piFinset_univ] at h3
    rw [← h3, Finset.prod_const, Finset.card_univ, Fintype.card_fin]
    rfl
  simp only [h2]
  have h4 := Finset.prod_univ_sum (fun (k : ι) => (Finset.univ : Finset (Fin (n k) → α)))
    (fun k y => ∏ i, (M.p k (y i) * g k (y i)))
  rw [Fintype.piFinset_univ] at h4
  exact h4.symm

omit [DecidableEq ι] in
/-- **Weighted AM–GM with integer weights**: if `Σ_k n_k b_k ≤ Σ_k n_k` then `Π_k b_k^{n_k} ≤ 1`. -/
theorem prod_pow_le_one {n : ι → ℕ} {b : ι → ℝ} (hb : ∀ k, 0 ≤ b k) (hN : 0 < ∑ k, n k)
    (h : ∑ k, (n k : ℝ) * b k ≤ ∑ k, (n k : ℝ)) : ∏ k, b k ^ n k ≤ 1 := by
  have hNsum : ((∑ k, n k : ℕ) : ℝ) = ∑ k, (n k : ℝ) := by push_cast; rfl
  have hNpos : (0 : ℝ) < ∑ k, (n k : ℝ) := by rw [← hNsum]; exact_mod_cast hN
  set S : ℝ := ∑ k, (n k : ℝ) with hS
  have hw0 : ∀ k ∈ (Finset.univ : Finset ι), 0 ≤ (n k : ℝ) / S :=
    fun k _ => div_nonneg (Nat.cast_nonneg _) hNpos.le
  have hw1 : ∑ k, (n k : ℝ) / S = 1 := by
    rw [← Finset.sum_div, ← hS]; exact div_self hNpos.ne'
  have hgm := Real.geom_mean_le_arith_mean_weighted Finset.univ (fun k => (n k : ℝ) / S) b
    hw0 hw1 (fun k _ => hb k)
  have hle1 : ∑ k, (n k : ℝ) / S * b k ≤ 1 := by
    have e : ∑ k, (n k : ℝ) / S * b k = (∑ k, (n k : ℝ) * b k) / S := by
      rw [Finset.sum_div]; exact Finset.sum_congr rfl (fun k _ => by ring)
    rw [e, div_le_one hNpos]; exact h
  have hg0 : 0 ≤ ∏ k, b k ^ ((n k : ℝ) / S) :=
    Finset.prod_nonneg (fun k _ => Real.rpow_nonneg (hb k) _)
  have hpow : ∏ k, b k ^ n k = (∏ k, b k ^ ((n k : ℝ) / S)) ^ (∑ k, n k) := by
    rw [← Finset.prod_pow]
    refine Finset.prod_congr rfl (fun k _ => ?_)
    rw [← Real.rpow_natCast (b k ^ ((n k : ℝ) / S)) (∑ k, n k), ← Real.rpow_mul (hb k), hNsum]
    have e : (n k : ℝ) / S * S = (n k : ℝ) := div_mul_cancel₀ _ hNpos.ne'
    rw [e, Real.rpow_natCast]
  rw [hpow]
  exact pow_le_one₀ hg0 (hgm.trans hle1)

/-- **Stratified e-value**: a nonnegative product statistic with `Σ_k n_k E_k g_k ≤ N` has
expectation at most one under independent stratified sampling. -/
theorem stratified_evalue {n : ι → ℕ} (hN : 0 < ∑ k, n k) {g : ι → α → ℝ}
    (hg : ∀ k x, 0 ≤ g k x) (hmix : ∑ k, (n k : ℝ) * M.E k (g k) ≤ ∑ k, (n k : ℝ)) :
    ∑ x : Sample n α, M.prob n x * stat n g x ≤ 1 := by
  rw [M.expect_stat]
  exact prod_pow_le_one (fun k => M.E_nonneg k (hg k)) hN hmix

/-- The likelihood-ratio family: label predictor `lam`, tilt `w`; with `s_k = n_k/N`,
`g_k(x) = lam_k(x) · (Σ_j w_j p_j(x)) / (s_k p_k(x))` on `p_k(x) > 0`. -/
noncomputable def lrFactor (n : ι → ℕ) (lam : ι → α → ℝ) (w : ι → ℝ) (k : ι) (x : α) : ℝ :=
  if M.p k x = 0 ∨ n k = 0 then 0
  else lam k x * (∑ j, w j * M.p j x) * ((∑ j, (n j : ℝ)) / n k) / M.p k x

omit [DecidableEq ι] in
lemma lrFactor_nonneg (n : ι → ℕ) {lam : ι → α → ℝ} {w : ι → ℝ} (hlam : ∀ k x, 0 ≤ lam k x)
    (hw : ∀ j, 0 ≤ w j) (k : ι) (x : α) : 0 ≤ M.lrFactor n lam w k x := by
  unfold lrFactor
  split_ifs with h
  · exact le_rfl
  · have h1 : 0 ≤ ∑ j, w j * M.p j x :=
      Finset.sum_nonneg (fun j _ => mul_nonneg (hw j) (M.nonneg j x))
    have h2 : 0 ≤ (∑ j, (n j : ℝ)) / n k :=
      div_nonneg (Finset.sum_nonneg (fun j _ => Nat.cast_nonneg _)) (Nat.cast_nonneg _)
    exact div_nonneg (mul_nonneg (mul_nonneg (hlam k x) h1) h2) (M.nonneg k x)

/-- **The likelihood-ratio family consists of e-values** (Theorem B1, finite support): for every
label predictor (`lam ≥ 0`, `Σ_k lam_k ≤ 1`) and every tilt (`w ≥ 0`, `Σ w ≤ 1`),
`E[ Π_k Π_i lam_k m_w/(s_k p_k) ] ≤ 1` under independent stratified sampling from the model. -/
theorem lr_family_evalue {n : ι → ℕ} (hN : 0 < ∑ k, n k) {lam : ι → α → ℝ} {w : ι → ℝ}
    (hlam : ∀ k x, 0 ≤ lam k x) (hlam1 : ∀ x, ∑ k, lam k x ≤ 1) (hw : ∀ j, 0 ≤ w j)
    (hw1 : ∑ j, w j ≤ 1) :
    ∑ x : Sample n α, M.prob n x * stat n (M.lrFactor n lam w) x ≤ 1 := by
  refine M.stratified_evalue hN (M.lrFactor_nonneg n hlam hw) ?_
  set S : ℝ := ∑ j, (n j : ℝ) with hS
  have hS0 : 0 ≤ S := Finset.sum_nonneg (fun j _ => Nat.cast_nonneg _)
  have hmw : ∀ x, 0 ≤ ∑ j, w j * M.p j x :=
    fun x => Finset.sum_nonneg (fun j _ => mul_nonneg (hw j) (M.nonneg j x))
  -- pointwise: n_k p_k(x) g_k(x) ≤ N lam_k(x) m_w(x)
  have hpt : ∀ k x, (n k : ℝ) * (M.p k x * M.lrFactor n lam w k x)
      ≤ S * (lam k x * ∑ j, w j * M.p j x) := by
    intro k x
    unfold lrFactor
    split_ifs with h
    · rw [mul_zero, mul_zero]
      exact mul_nonneg hS0 (mul_nonneg (hlam k x) (hmw x))
    · have hp : M.p k x ≠ 0 := fun h0 => h (Or.inl h0)
      have hn0 : n k ≠ 0 := fun h0 => h (Or.inr h0)
      have hn : (n k : ℝ) ≠ 0 := by exact_mod_cast hn0
      have e : (n k : ℝ) * (M.p k x * (lam k x * (∑ j, w j * M.p j x) * (S / n k) / M.p k x))
          = S * (lam k x * ∑ j, w j * M.p j x) := by
        field_simp
      rw [← hS, e]
  calc ∑ k, (n k : ℝ) * M.E k (M.lrFactor n lam w k)
      = ∑ k, ∑ x, (n k : ℝ) * (M.p k x * M.lrFactor n lam w k x) := by
        simp only [E, Finset.mul_sum]
    _ ≤ ∑ k, ∑ x, S * (lam k x * ∑ j, w j * M.p j x) :=
        Finset.sum_le_sum (fun k _ => Finset.sum_le_sum (fun x _ => hpt k x))
    _ = S * ∑ x, (∑ j, w j * M.p j x) * ∑ k, lam k x := by
        rw [Finset.sum_comm, Finset.mul_sum]
        refine Finset.sum_congr rfl (fun x _ => ?_)
        rw [Finset.mul_sum, Finset.mul_sum]
        exact Finset.sum_congr rfl (fun k _ => by ring)
    _ ≤ S * ∑ x, (∑ j, w j * M.p j x) * 1 :=
        mul_le_mul_of_nonneg_left
          (Finset.sum_le_sum (fun x _ => mul_le_mul_of_nonneg_left (hlam1 x) (hmw x))) hS0
    _ = S * ∑ j, w j := by
        congr 1
        simp only [mul_one]
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl (fun j _ => ?_)
        rw [← Finset.mul_sum, M.sum_one j, mul_one]
    _ ≤ S * 1 := mul_le_mul_of_nonneg_left hw1 hS0
    _ = S := mul_one S

/-- **Markov's inequality on the sample space**: a nonnegative statistic with expectation at most
one is at least `1/a` with probability at most `a`. -/
theorem markov_finite {n : ι → ℕ} {T : Sample n α → ℝ} (hT : ∀ x, 0 ≤ T x) {a : ℝ}
    (ha : 0 < a) (hE : ∑ x : Sample n α, M.prob n x * T x ≤ 1)
    [DecidablePred fun x : Sample n α => 1 / a ≤ T x] :
    ∑ x ∈ Finset.univ.filter (fun x : Sample n α => 1 / a ≤ T x), M.prob n x ≤ a := by
  have h1 : ∀ x ∈ Finset.univ.filter (fun x : Sample n α => 1 / a ≤ T x),
      M.prob n x ≤ a * (M.prob n x * T x) := by
    intro x hx
    have h2 : 1 / a ≤ T x := (Finset.mem_filter.1 hx).2
    have h3 : 1 ≤ a * T x := by
      have := mul_le_mul_of_nonneg_left h2 ha.le
      rwa [mul_one_div_cancel ha.ne'] at this
    have h4 := mul_le_mul_of_nonneg_left h3 (M.prob_nonneg n x)
    linarith
  calc ∑ x ∈ Finset.univ.filter (fun x : Sample n α => 1 / a ≤ T x), M.prob n x
      ≤ ∑ x ∈ Finset.univ.filter (fun x : Sample n α => 1 / a ≤ T x),
          a * (M.prob n x * T x) := Finset.sum_le_sum h1
    _ ≤ ∑ x : Sample n α, a * (M.prob n x * T x) :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
          (fun x _ _ => mul_nonneg ha.le (mul_nonneg (M.prob_nonneg n x) (hT x)))
    _ = a * ∑ x : Sample n α, M.prob n x * T x := by rw [Finset.mul_sum]
    _ ≤ a * 1 := mul_le_mul_of_nonneg_left hE ha.le
    _ = a := mul_one a

/-- **Coverage of the likelihood-ratio region at a fixed sample size** (finite support): the
probability that the likelihood-ratio statistic built from any label predictor and tilt reaches
`1/a` at the true model is at most `a`. -/
theorem lr_region_coverage {n : ι → ℕ} (hN : 0 < ∑ k, n k) {lam : ι → α → ℝ} {w : ι → ℝ}
    (hlam : ∀ k x, 0 ≤ lam k x) (hlam1 : ∀ x, ∑ k, lam k x ≤ 1) (hw : ∀ j, 0 ≤ w j)
    (hw1 : ∑ j, w j ≤ 1) {a : ℝ} (ha : 0 < a)
    [DecidablePred fun x : Sample n α => 1 / a ≤ stat n (M.lrFactor n lam w) x] :
    ∑ x ∈ Finset.univ.filter
        (fun x : Sample n α => 1 / a ≤ stat n (M.lrFactor n lam w) x), M.prob n x ≤ a :=
  M.markov_finite (fun x => stat_nonneg n (M.lrFactor_nonneg n hlam hw) x) ha
    (M.lr_family_evalue hN hlam hlam1 hw hw1)

end Model

end MBAR
