import Mathlib
import proofs.Frontiers.HoffmanWielandt

/-!
# A trace-enhanced spectral obstruction to low-dimensional Euclidean realizability

Let `Dhat` be a symmetric hollow `L × L` matrix of *predicted squared distances* and let
`Ghat = -(1/2) J Dhat J` (with `J = 1 - (1/L) 𝟙𝟙ᵀ` the centering matrix) be its classical-MDS Gram
matrix, with decreasingly sorted eigenvalues `λ₀`.  For `r : ℕ` put

* `tailSq Ghat r  = ∑_{k ≥ r} (λ₀ k)²` — squared mass of the spectrum beyond the top `r`,
* `tailSum Ghat r = ∑_{k ≥ r} λ₀ k`   — the "tail trace".

The main result (`sstress_lower_bound`) is a certificate of non-realizability in `ℝ^r`: for *every*
configuration `Y` of `L` points in `ℝ^r`,

`4 * (tailSq Ghat r + (tailSum Ghat r)² / (r + 1)) ≤ ∑ i j, (Dhat i j - ‖Y i - Y j‖²)²`.

## Contents

* **T1** `eigenvalues₀_eq_zero_of_rank_le`: a PSD matrix of rank `≤ r` has sorted spectrum
  vanishing beyond index `r`.
* **T2** `rank_psd_trace_obstruction`: for symmetric `A` and PSD `G` of rank `≤ r`,
  `tailSq A r + (tailSum A r)² / (r + 1) ≤ ‖G - A‖_F² + (tr G - tr A)²`
  (Hoffman–Wielandt + Cauchy–Schwarz on `r + 1` numbers).
* **T3** `K_identity`, `K_lower_bound`: for symmetric `E` with zero row sums,
  `∑ i j, (E i i + E j j - 2 E i j)² = 4 ‖E‖_F² + 2 L ∑ i, (E i i)² + 2 (tr E)²
     ≥ 4 ‖E‖_F² + 4 (tr E)²`.
* **T4** `sstress_lower_bound` (abstract Gram form: `sstress_lower_bound_gram`; statement with
  `J`, `Ghat` and the squared distances written out: `sstress_lower_bound_explicit`), with the
  corollaries `tail_eq_zero_of_realizable` and `exists_ne_sqDist_of_tail_pos`.
* **T5** non-vacuity: `simplex_sstress_lower_bound` — for the regular simplex on `L` points (all
  squared distances `1`) every configuration in `ℝ^r` has squared-distance misfit at least
  `L (L - 1 - r) / (r + 1)` (hence `simplex_not_realizable` for `r + 1 < L`); in particular
  `equilateral_triangle_sstress_lower_bound`: three points on a line miss the equilateral
  triangle by at least `3/2`.  These are obtained *from* T4, by evaluating the spectral
  certificate of the simplex exactly (`simplex_certificate_eq`: its Gram matrix is `(1/2) J`, a
  scaled projection, so its eigenvalues lie in `{0, 1/2}` and sum to `(L - 1) / 2`).

## Conventions

`tailSq A r` and `tailSum A r` are defined for every real square matrix `A`, with the junk value
`0` when `A` is not symmetric; `tailSq_eq` / `tailSum_eq` unfold them for symmetric `A`.  All
matrices whose tails occur in the theorems below are symmetric (by hypothesis, or by
`gramOfSqDist_isSymm`).  No hypothesis `1 ≤ L` is needed in T4: for `L = 0` both sides vanish.
-/

namespace MetricChain

open Matrix Finset

/-! ### Spectral tails, T1 and T2 -/

section Tail

variable {n : Type*} [Fintype n] [DecidableEq n]

open Classical in
/-- `tailSq A r`: the sum of the squares of all but the top `r` decreasingly sorted eigenvalues of
the real symmetric matrix `A` (junk value `0` if `A` is not symmetric). -/
noncomputable def tailSq (A : Matrix n n ℝ) (r : ℕ) : ℝ :=
  if hA : A.IsHermitian then
    ∑ k : Fin (Fintype.card n), if (k : ℕ) < r then 0 else (hA.eigenvalues₀ k) ^ 2
  else 0

open Classical in
/-- `tailSum A r`: the sum of all but the top `r` decreasingly sorted eigenvalues of the real
symmetric matrix `A`, the "tail trace" (junk value `0` if `A` is not symmetric). -/
noncomputable def tailSum (A : Matrix n n ℝ) (r : ℕ) : ℝ :=
  if hA : A.IsHermitian then
    ∑ k : Fin (Fintype.card n), if (k : ℕ) < r then 0 else hA.eigenvalues₀ k
  else 0

theorem tailSq_eq {A : Matrix n n ℝ} (hA : A.IsHermitian) (r : ℕ) :
    tailSq A r =
      ∑ k : Fin (Fintype.card n), if (k : ℕ) < r then 0 else (hA.eigenvalues₀ k) ^ 2 := by
  rw [tailSq, dif_pos hA]

theorem tailSum_eq {A : Matrix n n ℝ} (hA : A.IsHermitian) (r : ℕ) :
    tailSum A r = ∑ k : Fin (Fintype.card n), if (k : ℕ) < r then 0 else hA.eigenvalues₀ k := by
  rw [tailSum, dif_pos hA]

theorem tailSq_nonneg (A : Matrix n n ℝ) (r : ℕ) : 0 ≤ tailSq A r := by
  unfold tailSq
  split_ifs with hA
  · exact Finset.sum_nonneg fun k _ => by split_ifs <;> positivity
  · exact le_rfl

/-- **T1.** A positive semidefinite matrix of rank at most `r` has decreasingly sorted spectrum
vanishing from index `r` on. -/
theorem eigenvalues₀_eq_zero_of_rank_le {G : Matrix n n ℝ} (hG : G.PosSemidef) {r : ℕ}
    (hr : G.rank ≤ r) (k : Fin (Fintype.card n)) (hk : r ≤ (k : ℕ)) :
    hG.isHermitian.eigenvalues₀ k = 0 := by
  set e : Fin (Fintype.card n) ≃ n := Fintype.equivOfCardEq (Fintype.card_fin _) with he
  have hnonneg : ∀ j, 0 ≤ hG.isHermitian.eigenvalues₀ j := by
    intro j
    have := hG.eigenvalues_nonneg (e j)
    simpa [Matrix.IsHermitian.eigenvalues, he] using this
  by_contra hne
  have hpos : 0 < hG.isHermitian.eigenvalues₀ k := lt_of_le_of_ne (hnonneg k) (Ne.symm hne)
  -- by antitonicity, the `k + 1` indices `0, …, k` all carry nonzero eigenvalues
  have hall : ∀ j ≤ k, hG.isHermitian.eigenvalues₀ j ≠ 0 := by
    intro j hj
    have := hG.isHermitian.eigenvalues₀_antitone hj
    exact (lt_of_lt_of_le hpos this).ne'
  have hrank := hG.isHermitian.rank_eq_card_non_zero_eigs
  have hcard : (k : ℕ) + 1 ≤ Fintype.card {i // hG.isHermitian.eigenvalues i ≠ 0} := by
    rw [Fintype.card_subtype]
    have hsub : (Finset.Iic k).map e.toEmbedding ⊆
        Finset.univ.filter (fun i => hG.isHermitian.eigenvalues i ≠ 0) := by
      intro i hi
      simp only [Finset.mem_map, Finset.mem_Iic, Equiv.coe_toEmbedding] at hi
      obtain ⟨j, hj, rfl⟩ := hi
      simp only [Finset.mem_filter, Finset.mem_univ, true_and]
      have := hall j hj
      simpa [Matrix.IsHermitian.eigenvalues, he] using this
    calc (k : ℕ) + 1 = (Finset.Iic k).card := by simp [Fin.card_Iic]
      _ = ((Finset.Iic k).map e.toEmbedding).card := (Finset.card_map _).symm
      _ ≤ _ := Finset.card_le_card hsub
  omega

/-- **T2 (rank-constrained PSD approximation with trace penalty).** If `A` is symmetric and `G` is
positive semidefinite of rank at most `r`, then the squared Frobenius distance from `G` to `A` plus
the squared trace mismatch is at least `tailSq A r + (tailSum A r)² / (r + 1)`. -/
theorem rank_psd_trace_obstruction (A G : Matrix n n ℝ) (hA : A.IsHermitian) (hG : G.PosSemidef)
    (r : ℕ) (hr : G.rank ≤ r) :
    tailSq A r + (tailSum A r) ^ 2 / (r + 1) ≤
      (∑ i, ∑ j, (G i j - A i j) ^ 2) + (Matrix.trace G - Matrix.trace A) ^ 2 := by
  rw [tailSq_eq hA, tailSum_eq hA]
  set lam := hA.eigenvalues₀ with hlam
  set mu := hG.isHermitian.eigenvalues₀ with hmu
  have hHW : ∑ k, (mu k - lam k) ^ 2 ≤ ∑ i, ∑ j, (G i j - A i j) ^ 2 :=
    hoffman_wielandt G A hG.isHermitian hA
  have htr : Matrix.trace G - Matrix.trace A = ∑ k, (mu k - lam k) := by
    rw [trace_eq_sum_eigenvalues₀ hG.isHermitian, trace_eq_sum_eigenvalues₀ hA,
      Finset.sum_sub_distrib]
  have hzero : ∀ k : Fin (Fintype.card n), r ≤ (k : ℕ) → mu k = 0 :=
    fun k hk => eigenvalues₀_eq_zero_of_rank_le hG hr k hk
  -- `x` = the spectral differences on the head `k < r`
  set x : Fin (Fintype.card n) → ℝ := fun k => if (k : ℕ) < r then mu k - lam k else 0 with hx
  set P := ∑ k, x k ^ 2 with hP
  set s := ∑ k, x k with hs
  set T := ∑ k : Fin (Fintype.card n), if (k : ℕ) < r then 0 else lam k ^ 2 with hT
  set τ := ∑ k : Fin (Fintype.card n), if (k : ℕ) < r then 0 else lam k with hτ
  have h1 : ∑ k, (mu k - lam k) ^ 2 = P + T := by
    rw [hP, hT, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun k _ => ?_
    by_cases hk : (k : ℕ) < r
    · simp [hx, hk]
    · simp [hx, hk, hzero k (not_lt.mp hk)]
  have h2 : ∑ k, (mu k - lam k) = s - τ := by
    rw [hs, hτ, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun k _ => ?_
    by_cases hk : (k : ℕ) < r
    · simp [hx, hk]
    · simp [hx, hk, hzero k (not_lt.mp hk)]
  have hP0 : 0 ≤ P := Finset.sum_nonneg fun k _ => sq_nonneg _
  -- Cauchy–Schwarz on the (at most `r`) head terms
  have h3 : s ^ 2 ≤ r * P := by
    have hs' : s = ∑ k ∈ Finset.univ.filter (fun k : Fin (Fintype.card n) => (k : ℕ) < r),
        (mu k - lam k) := by
      rw [hs, Finset.sum_filter]
    have hP' : P = ∑ k ∈ Finset.univ.filter (fun k : Fin (Fintype.card n) => (k : ℕ) < r),
        (mu k - lam k) ^ 2 := by
      rw [hP, Finset.sum_filter]
      refine Finset.sum_congr rfl fun k _ => ?_
      by_cases hk : (k : ℕ) < r <;> simp [hx, hk]
    have hcs := sq_sum_le_card_mul_sum_sq
      (s := Finset.univ.filter (fun k : Fin (Fintype.card n) => (k : ℕ) < r))
      (f := fun k => mu k - lam k)
    have hcard : ((Finset.univ.filter
        (fun k : Fin (Fintype.card n) => (k : ℕ) < r)).card : ℝ) ≤ r := by
      rw [Fin.card_filter_val_lt]
      exact_mod_cast min_le_right _ _
    rw [← hs', ← hP'] at hcs
    calc s ^ 2 ≤ _ := hcs
      _ ≤ r * P := mul_le_mul_of_nonneg_right hcard hP0
  -- Cauchy–Schwarz on the `r + 1` numbers `(x k)_{k < r}` and `τ - s`
  have h4 : τ ^ 2 / (r + 1) ≤ P + (s - τ) ^ 2 := by
    rw [div_le_iff₀ (by positivity)]
    rcases Nat.eq_zero_or_pos r with hr0 | hr0
    · subst hr0
      have hs0 : s = 0 := by
        have : s ^ 2 ≤ 0 := by simpa using h3
        nlinarith [sq_nonneg s]
      rw [hs0]; simp; nlinarith
    · have hr' : (0 : ℝ) < r := by exact_mod_cast hr0
      have hid : (r : ℝ) * ((P + (s - τ) ^ 2) * (r + 1) - τ ^ 2) =
          (r + 1) * (r * P - s ^ 2) + (s + r * (s - τ)) ^ 2 := by ring
      have hnn : 0 ≤ (r : ℝ) * ((P + (s - τ) ^ 2) * (r + 1) - τ ^ 2) := by
        rw [hid]; have := sq_nonneg (s + r * (s - τ)); nlinarith
      have := nonneg_of_mul_nonneg_right hnn hr'
      linarith
  rw [htr, h2]
  calc T + τ ^ 2 / (r + 1) ≤ T + (P + (s - τ) ^ 2) := by linarith
    _ = (P + T) + (s - τ) ^ 2 := by ring
    _ = ∑ k, (mu k - lam k) ^ 2 + (s - τ) ^ 2 := by rw [h1]
    _ ≤ _ := by linarith

/-- The hypotheses of `rank_psd_trace_obstruction` are satisfiable. -/
example : ∃ (A G : Matrix (Fin 2) (Fin 2) ℝ) (r : ℕ), A.IsHermitian ∧ G.PosSemidef ∧ G.rank ≤ r :=
  ⟨1, 0, 0, Matrix.isHermitian_one, Matrix.PosSemidef.zero, by simp⟩

end Tail

/-! ### T3: the K-identity -/

section KIdentity

variable {L : ℕ}

/-- **T3 (K-identity).** For a symmetric matrix `E` with zero row sums,
`∑ i j, (E i i + E j j - 2 E i j)² = 4 ∑ i j, (E i j)² + 2 L ∑ i, (E i i)² + 2 (∑ i, E i i)²`. -/
theorem K_identity (E : Matrix (Fin L) (Fin L) ℝ) (hE : E.IsSymm)
    (hrow : ∀ i, ∑ j, E i j = 0) :
    ∑ i, ∑ j, (E i i + E j j - 2 * E i j) ^ 2 =
      4 * ∑ i, ∑ j, (E i j) ^ 2 + 2 * L * ∑ i, (E i i) ^ 2 + 2 * (∑ i, E i i) ^ 2 := by
  have hcol : ∀ j, ∑ i, E i j = 0 := fun j => by
    rw [← hrow j]; exact Finset.sum_congr rfl fun i _ => hE.apply j i
  have expand : ∀ i j, (E i i + E j j - 2 * E i j) ^ 2 =
      E i i ^ 2 + E j j ^ 2 + 4 * E i j ^ 2 + 2 * (E i i * E j j) - 4 * (E i i * E i j)
        - 4 * (E j j * E i j) := by
    intro i j; ring
  simp only [expand, Finset.sum_add_distrib, Finset.sum_sub_distrib]
  have t1 : ∑ i, ∑ _j : Fin L, E i i ^ 2 = L * ∑ i, E i i ^ 2 := by
    simp [Finset.sum_const, Finset.mul_sum]
  have t2 : ∑ _i : Fin L, ∑ j, E j j ^ 2 = L * ∑ i, E i i ^ 2 := by
    simp [Finset.sum_const]
  have t3 : ∑ i, ∑ j, 4 * E i j ^ 2 = 4 * ∑ i, ∑ j, E i j ^ 2 := by
    simp [Finset.mul_sum]
  have t4 : ∑ i, ∑ j, 2 * (E i i * E j j) = 2 * (∑ i, E i i) ^ 2 := by
    rw [sq, Finset.sum_mul_sum]; simp [Finset.mul_sum]
  have t5 : ∑ i, ∑ j, 4 * (E i i * E i j) = 0 := by
    have : ∀ i, ∑ j, 4 * (E i i * E i j) = 0 := fun i => by
      rw [← Finset.mul_sum, ← Finset.mul_sum, hrow i]; ring
    simp [this]
  have t6 : ∑ i, ∑ j, 4 * (E j j * E i j) = 0 := by
    rw [Finset.sum_comm]
    have : ∀ j, ∑ i, 4 * (E j j * E i j) = 0 := fun j => by
      rw [← Finset.mul_sum, ← Finset.mul_sum, hcol j]; ring
    simp [this]
  rw [t1, t2, t3, t4, t5, t6]; ring

/-- **T3 (consequence).** For a symmetric matrix `E` with zero row sums,
`4 ‖E‖_F² + 4 (tr E)² ≤ ∑ i j, (E i i + E j j - 2 E i j)²`. -/
theorem K_lower_bound (E : Matrix (Fin L) (Fin L) ℝ) (hE : E.IsSymm)
    (hrow : ∀ i, ∑ j, E i j = 0) :
    4 * (∑ i, ∑ j, (E i j) ^ 2) + 4 * (Matrix.trace E) ^ 2 ≤
      ∑ i, ∑ j, (E i i + E j j - 2 * E i j) ^ 2 := by
  rw [K_identity E hE hrow]
  have hcs : (∑ i, E i i) ^ 2 ≤ L * ∑ i, E i i ^ 2 := by
    have := sq_sum_le_card_mul_sum_sq (s := (Finset.univ : Finset (Fin L))) (f := fun i => E i i)
    simpa using this
  have htr : Matrix.trace E = ∑ i, E i i := rfl
  rw [htr]; nlinarith

end KIdentity

/-! ### The centering matrix -/

section Centering

variable {L : ℕ}

/-- The centering matrix `J = 1 - (1/L) 𝟙𝟙ᵀ`. -/
noncomputable def centering (L : ℕ) : Matrix (Fin L) (Fin L) ℝ :=
  1 - (1 / (L : ℝ)) • Matrix.of (fun _ _ => (1 : ℝ))

theorem centering_apply (i j : Fin L) :
    centering L i j = (if i = j then 1 else 0) - 1 / (L : ℝ) := by
  simp [centering, Matrix.one_apply]

theorem centering_isSymm : (centering L).IsSymm := by
  ext i j; simp [centering_apply, eq_comm]

/-- Left multiplication by `J` subtracts the column means. -/
theorem centering_mul_apply {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) (i : Fin L) (k : Fin p) :
    (centering L * Y) i k = Y i k - 1 / (L : ℝ) * ∑ l, Y l k := by
  simp [Matrix.mul_apply, centering_apply, sub_mul, Finset.sum_sub_distrib, Finset.mul_sum]

/-- Right multiplication by `J` subtracts the row means. -/
theorem mul_centering_apply {p : ℕ} (M : Matrix (Fin p) (Fin L) ℝ) (i : Fin p) (j : Fin L) :
    (M * centering L) i j = M i j - 1 / (L : ℝ) * ∑ l, M i l := by
  simp only [Matrix.mul_apply, centering_apply, mul_sub, Finset.sum_sub_distrib, mul_ite, mul_one,
    mul_zero, Finset.sum_ite_eq', Finset.mem_univ, if_true, ← Finset.sum_mul]
  ring

/-- The columns of `J * Y` sum to zero. -/
theorem sum_centering_mul_apply {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) (k : Fin p) :
    ∑ i, (centering L * Y) i k = 0 := by
  rcases Nat.eq_zero_or_pos L with rfl | hL
  · simp
  · have hL' : (L : ℝ) ≠ 0 := by positivity
    simp only [centering_mul_apply, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul]
    field_simp
    ring

/-- The rows of `M * J` sum to zero. -/
theorem sum_mul_centering_apply {p : ℕ} (M : Matrix (Fin p) (Fin L) ℝ) (i : Fin p) :
    ∑ j, (M * centering L) i j = 0 := by
  rcases Nat.eq_zero_or_pos L with rfl | hL
  · simp
  · have hL' : (L : ℝ) ≠ 0 := by positivity
    simp only [mul_centering_apply, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul]
    field_simp
    ring

/-- The centering matrix is idempotent. -/
theorem centering_mul_self (L : ℕ) : centering L * centering L = centering L := by
  ext i j
  rw [mul_centering_apply]
  have := sum_mul_centering_apply (1 : Matrix (Fin L) (Fin L) ℝ) i
  rw [Matrix.one_mul] at this
  rw [this]; ring

theorem trace_centering (hL : 0 < L) : Matrix.trace (centering L) = (L : ℝ) - 1 := by
  have hL' : (L : ℝ) ≠ 0 := by positivity
  simp only [Matrix.trace, Matrix.diag_apply, centering_apply, if_true, Finset.sum_const,
    Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  field_simp

end Centering

/-! ### Squared distances and Gram matrices -/

section Gram

variable {L : ℕ}

/-- Squared Euclidean distances of a configuration `Y` of `L` points in `ℝ^p` (rows are points). -/
def sqDist {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) (i j : Fin L) : ℝ :=
  ∑ k, (Y i k - Y j k) ^ 2

theorem sqDist_self {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) (i : Fin L) : sqDist Y i i = 0 := by
  simp [sqDist]

theorem sqDist_comm {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) (i j : Fin L) :
    sqDist Y i j = sqDist Y j i := by
  unfold sqDist
  exact Finset.sum_congr rfl fun _ _ => by ring

theorem sqDist_nonneg {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) (i j : Fin L) : 0 ≤ sqDist Y i j :=
  Finset.sum_nonneg fun _ _ => sq_nonneg _

/-- The classical-MDS Gram matrix `Ghat = -(1/2) J D J` of a matrix `D` of squared distances. -/
noncomputable def gramOfSqDist (D : Matrix (Fin L) (Fin L) ℝ) : Matrix (Fin L) (Fin L) ℝ :=
  -(1 / 2 : ℝ) • (centering L * D * centering L)

/-- The Gram matrix `(J Y) (J Y)ᵀ` of the centered configuration. -/
noncomputable def centeredGram {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) :
    Matrix (Fin L) (Fin L) ℝ :=
  (centering L * Y) * (centering L * Y)ᵀ

/-- Entries of the double centering `J D J` of a symmetric matrix. -/
theorem centering_mul_mul_centering_apply {D : Matrix (Fin L) (Fin L) ℝ} (hD : D.IsSymm)
    (i j : Fin L) :
    (centering L * D * centering L) i j =
      D i j - 1 / (L : ℝ) * (∑ l, D j l) - 1 / (L : ℝ) * (∑ l, D i l)
        + (1 / (L : ℝ)) ^ 2 * ∑ k, ∑ l, D k l := by
  rw [mul_centering_apply]
  simp only [centering_mul_apply]
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum]
  have h1 : ∑ k, D k j = ∑ l, D j l := Finset.sum_congr rfl fun k _ => hD.apply j k
  have h2 : ∑ x, ∑ l, D l x = ∑ k, ∑ l, D k l :=
    Finset.sum_congr rfl fun x _ => Finset.sum_congr rfl fun l _ => hD.apply x l
  rw [h1, h2]; ring

theorem gramOfSqDist_isSymm {D : Matrix (Fin L) (Fin L) ℝ} (hD : D.IsSymm) :
    (gramOfSqDist D).IsSymm := by
  ext i j
  simp only [gramOfSqDist, Matrix.transpose_apply, Matrix.smul_apply,
    centering_mul_mul_centering_apply hD, hD.apply i j]
  ring

theorem gramOfSqDist_isHermitian {D : Matrix (Fin L) (Fin L) ℝ} (hD : D.IsSymm) :
    (gramOfSqDist D).IsHermitian :=
  Matrix.isHermitian_iff_isSymm.mpr (gramOfSqDist_isSymm hD)

theorem gramOfSqDist_row_sum (D : Matrix (Fin L) (Fin L) ℝ) (i : Fin L) :
    ∑ j, gramOfSqDist D i j = 0 := by
  simp only [gramOfSqDist, Matrix.smul_apply, smul_eq_mul, ← Finset.mul_sum,
    sum_mul_centering_apply, mul_zero]

/-- A symmetric hollow `D` is recovered from its Gram matrix:
`D i j = Ghat i i + Ghat j j - 2 Ghat i j`. -/
theorem gramOfSqDist_K {D : Matrix (Fin L) (Fin L) ℝ} (hD : D.IsSymm)
    (hhollow : ∀ i, D i i = 0) (i j : Fin L) :
    gramOfSqDist D i i + gramOfSqDist D j j - 2 * gramOfSqDist D i j = D i j := by
  simp only [gramOfSqDist, Matrix.smul_apply, smul_eq_mul, centering_mul_mul_centering_apply hD,
    hhollow]
  ring

theorem centeredGram_apply {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) (i j : Fin L) :
    centeredGram Y i j = ∑ k, (centering L * Y) i k * (centering L * Y) j k := by
  rw [centeredGram, Matrix.mul_apply]
  rfl

theorem centeredGram_posSemidef {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) :
    (centeredGram Y).PosSemidef := by
  have := posSemidef_self_mul_conjTranspose (centering L * Y)
  rwa [Matrix.conjTranspose_eq_transpose_of_trivial] at this

theorem centeredGram_rank_le {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) :
    (centeredGram Y).rank ≤ p :=
  (Matrix.rank_mul_le_left _ _).trans (Matrix.rank_le_width _)

theorem centeredGram_row_sum {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) (i : Fin L) :
    ∑ j, centeredGram Y i j = 0 := by
  simp only [centeredGram_apply]
  rw [Finset.sum_comm]
  simp only [← Finset.mul_sum, sum_centering_mul_apply, mul_zero, Finset.sum_const_zero]

/-- Squared distances from the centered Gram matrix (centering does not change differences). -/
theorem centeredGram_K {p : ℕ} (Y : Matrix (Fin L) (Fin p) ℝ) (i j : Fin L) :
    centeredGram Y i i + centeredGram Y j j - 2 * centeredGram Y i j = sqDist Y i j := by
  simp only [centeredGram_apply, sqDist, centering_mul_apply]
  rw [← Finset.sum_add_distrib, Finset.mul_sum, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun k _ => ?_
  ring

end Gram

/-! ### T4: the sstress lower bound -/

section Sstress

variable {L r : ℕ}

/-- **T4, abstract Gram form.** If `Ghat` is symmetric with zero row sums and `G` is positive
semidefinite of rank at most `r` with zero row sums, then the squared misfit between the associated
squared-distance matrices is at least `4 (tailSq Ghat r + (tailSum Ghat r)² / (r + 1))`. -/
theorem sstress_lower_bound_gram (Ghat G : Matrix (Fin L) (Fin L) ℝ) (hGhat : Ghat.IsSymm)
    (hGhat0 : ∀ i, ∑ j, Ghat i j = 0) (hG : G.PosSemidef) (hG0 : ∀ i, ∑ j, G i j = 0)
    (hr : G.rank ≤ r) :
    4 * (tailSq Ghat r + (tailSum Ghat r) ^ 2 / (r + 1)) ≤
      ∑ i, ∑ j, ((Ghat i i + Ghat j j - 2 * Ghat i j) - (G i i + G j j - 2 * G i j)) ^ 2 := by
  have hGhat' : Ghat.IsHermitian := Matrix.isHermitian_iff_isSymm.mpr hGhat
  have hE : (G - Ghat).IsSymm := (Matrix.isHermitian_iff_isSymm.mp hG.isHermitian).sub hGhat
  have hE0 : ∀ i, ∑ j, (G - Ghat) i j = 0 := fun i => by
    simp [Matrix.sub_apply, Finset.sum_sub_distrib, hGhat0 i, hG0 i]
  have h3 := K_lower_bound (G - Ghat) hE hE0
  have h2 := rank_psd_trace_obstruction Ghat G hGhat' hG r hr
  have e1 : ∑ i, ∑ j, ((G - Ghat) i i + (G - Ghat) j j - 2 * (G - Ghat) i j) ^ 2 =
      ∑ i, ∑ j, ((Ghat i i + Ghat j j - 2 * Ghat i j) - (G i i + G j j - 2 * G i j)) ^ 2 := by
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    simp only [Matrix.sub_apply]; ring
  have e2 : Matrix.trace (G - Ghat) = Matrix.trace G - Matrix.trace Ghat := Matrix.trace_sub _ _
  have e3 : ∑ i, ∑ j, ((G - Ghat) i j) ^ 2 = ∑ i, ∑ j, (G i j - Ghat i j) ^ 2 := rfl
  rw [e1, e2, e3] at h3
  linarith

/-- **T4 (sstress lower bound, spectral non-realizability certificate).** Let `Dhat` be a symmetric
hollow matrix of predicted squared distances and `Ghat = gramOfSqDist Dhat = -(1/2) J Dhat J`.
Then for every configuration `Y` of `L` points in `ℝ^r`,
`4 (tailSq Ghat r + (tailSum Ghat r)² / (r + 1)) ≤ ∑ i j, (Dhat i j - sqDist Y i j)²`. -/
theorem sstress_lower_bound (Dhat : Matrix (Fin L) (Fin L) ℝ) (hsymm : Dhat.IsSymm)
    (hhollow : ∀ i, Dhat i i = 0) (Y : Matrix (Fin L) (Fin r) ℝ) :
    4 * (tailSq (gramOfSqDist Dhat) r + (tailSum (gramOfSqDist Dhat) r) ^ 2 / (r + 1)) ≤
      ∑ i, ∑ j, (Dhat i j - sqDist Y i j) ^ 2 := by
  have h := sstress_lower_bound_gram (r := r) (gramOfSqDist Dhat) (centeredGram Y)
    (gramOfSqDist_isSymm hsymm) (gramOfSqDist_row_sum Dhat) (centeredGram_posSemidef Y)
    (centeredGram_row_sum Y) (centeredGram_rank_le Y)
  simp only [gramOfSqDist_K hsymm hhollow, centeredGram_K] at h
  exact h

/-- `sstress_lower_bound` with the centering matrix `J`, the Gram matrix `Ghat = -(1/2) J Dhat J`
and the squared distances of `Y` written out in the statement. -/
theorem sstress_lower_bound_explicit (Dhat : Matrix (Fin L) (Fin L) ℝ) (hsymm : Dhat.IsSymm)
    (hhollow : ∀ i, Dhat i i = 0) (Y : Matrix (Fin L) (Fin r) ℝ) :
    let J : Matrix (Fin L) (Fin L) ℝ := 1 - (1 / (L : ℝ)) • Matrix.of (fun _ _ => (1 : ℝ))
    let Ghat : Matrix (Fin L) (Fin L) ℝ := -(1 / 2 : ℝ) • (J * Dhat * J)
    4 * (tailSq Ghat r + (tailSum Ghat r) ^ 2 / (r + 1)) ≤
      ∑ i, ∑ j, (Dhat i j - ∑ k, (Y i k - Y j k) ^ 2) ^ 2 :=
  sstress_lower_bound Dhat hsymm hhollow Y

/-- If `Dhat` is exactly the squared-distance matrix of a configuration in `ℝ^r`, then the spectral
tail of its Gram matrix beyond `r` vanishes. -/
theorem tail_eq_zero_of_realizable (Dhat : Matrix (Fin L) (Fin L) ℝ)
    (Y : Matrix (Fin L) (Fin r) ℝ) (hY : ∀ i j, Dhat i j = sqDist Y i j) :
    tailSq (gramOfSqDist Dhat) r = 0 ∧ tailSum (gramOfSqDist Dhat) r = 0 := by
  have hsymm : Dhat.IsSymm := by
    ext i j
    rw [Matrix.transpose_apply, hY, hY, sqDist_comm]
  have hhollow : ∀ i, Dhat i i = 0 := fun i => by rw [hY, sqDist_self]
  have h := sstress_lower_bound Dhat hsymm hhollow Y
  have h0 : ∑ i, ∑ j, (Dhat i j - sqDist Y i j) ^ 2 = 0 := by simp [hY]
  have hsq := tailSq_nonneg (gramOfSqDist Dhat) r
  have hr1 : (0 : ℝ) < r + 1 := by positivity
  have hdiv : 0 ≤ (tailSum (gramOfSqDist Dhat) r) ^ 2 / (r + 1) := by positivity
  have h1 : tailSq (gramOfSqDist Dhat) r = 0 := by linarith
  have h2 : (tailSum (gramOfSqDist Dhat) r) ^ 2 / (r + 1) = 0 := by linarith
  refine ⟨h1, ?_⟩
  rcases div_eq_zero_iff.mp h2 with h | h
  · exact pow_eq_zero_iff (two_ne_zero) |>.mp h
  · exact absurd h hr1.ne'

/-- **Non-realizability certificate.** If the spectral certificate of a symmetric hollow `Dhat` is
positive, no configuration of points in `ℝ^r` realizes `Dhat` exactly. -/
theorem exists_ne_sqDist_of_tail_pos (Dhat : Matrix (Fin L) (Fin L) ℝ) (hsymm : Dhat.IsSymm)
    (hhollow : ∀ i, Dhat i i = 0)
    (hpos : 0 < tailSq (gramOfSqDist Dhat) r + (tailSum (gramOfSqDist Dhat) r) ^ 2 / (r + 1))
    (Y : Matrix (Fin L) (Fin r) ℝ) : ∃ i j, Dhat i j ≠ sqDist Y i j := by
  by_contra! hcon
  have h := sstress_lower_bound Dhat hsymm hhollow Y
  have h0 : ∑ i, ∑ j, (Dhat i j - sqDist Y i j) ^ 2 = 0 := by simp [hcon]
  linarith

end Sstress

/-! ### Spectral tails of scaled projections -/

section Projection

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- If `A * A = c • A` (a scaled projection), every eigenvalue `λ` satisfies `λ² = c λ`. -/
theorem eigenvalues₀_mul_self_of_mul_self_eq_smul {A : Matrix n n ℝ} (hA : A.IsHermitian) {c : ℝ}
    (h : A * A = c • A) (k : Fin (Fintype.card n)) :
    hA.eigenvalues₀ k * hA.eigenvalues₀ k = c * hA.eigenvalues₀ k := by
  obtain ⟨U, hU1, hU2, hAU⟩ := exists_orthogonal_diagonalization A hA
  set a := hA.eigenvalues with ha
  have hD : Uᵀ * A * U = diagonal a := by
    calc Uᵀ * A * U = Uᵀ * (U * diagonal a * Uᵀ) * U := by rw [← hAU]
      _ = (Uᵀ * U) * diagonal a * (Uᵀ * U) := by simp only [Matrix.mul_assoc]
      _ = diagonal a := by rw [hU1, Matrix.one_mul, Matrix.mul_one]
  have h2 : diagonal a * diagonal a = c • diagonal a := by
    calc diagonal a * diagonal a = (Uᵀ * A * U) * (Uᵀ * A * U) := by rw [hD]
      _ = Uᵀ * A * (U * Uᵀ) * A * U := by simp only [Matrix.mul_assoc]
      _ = Uᵀ * (A * A) * U := by rw [hU2, Matrix.mul_one]; simp only [Matrix.mul_assoc]
      _ = c • (Uᵀ * A * U) := by rw [h]; simp
      _ = c • diagonal a := by rw [hD]
  have h3 : ∀ i, a i * a i = c * a i := fun i => by
    have := congrFun (congrFun h2 i) i
    simpa using this
  have h4 := h3 (Fintype.equivOfCardEq (Fintype.card_fin _) k)
  simpa [ha, Matrix.IsHermitian.eigenvalues] using h4

/-- For a scaled projection `A * A = c • A`, `tailSq A r = c * tailSum A r`. -/
theorem tailSq_eq_mul_tailSum_of_mul_self_eq_smul {A : Matrix n n ℝ} (hA : A.IsHermitian)
    {c : ℝ} (h : A * A = c • A) (r : ℕ) : tailSq A r = c * tailSum A r := by
  rw [tailSq_eq hA, tailSum_eq hA, Finset.mul_sum]
  refine Finset.sum_congr rfl fun k _ => ?_
  have := eigenvalues₀_mul_self_of_mul_self_eq_smul hA h k
  split_ifs
  · simp
  · rw [sq]; exact this

/-- For a scaled projection `A * A = c • A` with `c ≥ 0`, removing the top `r` eigenvalues removes
at most `r c` from the trace: `tr A - r c ≤ tailSum A r`. -/
theorem trace_sub_le_tailSum_of_mul_self_eq_smul {A : Matrix n n ℝ} (hA : A.IsHermitian)
    {c : ℝ} (hc : 0 ≤ c) (h : A * A = c • A) (r : ℕ) :
    Matrix.trace A - r * c ≤ tailSum A r := by
  rw [tailSum_eq hA, trace_eq_sum_eigenvalues₀ hA]
  have hle : ∀ k, hA.eigenvalues₀ k ≤ c := fun k => by
    have h1 := eigenvalues₀_mul_self_of_mul_self_eq_smul hA h k
    have h2 : hA.eigenvalues₀ k * (hA.eigenvalues₀ k - c) = 0 := by linarith
    rcases mul_eq_zero.mp h2 with h0 | h0
    · rw [h0]; exact hc
    · linarith
  have hsplit : ∑ k, hA.eigenvalues₀ k =
      (∑ k : Fin (Fintype.card n), if (k : ℕ) < r then hA.eigenvalues₀ k else 0) +
        ∑ k : Fin (Fintype.card n), if (k : ℕ) < r then 0 else hA.eigenvalues₀ k := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun k _ => ?_
    split_ifs <;> simp
  have hhead : (∑ k : Fin (Fintype.card n), if (k : ℕ) < r then hA.eigenvalues₀ k else 0)
      ≤ r * c := by
    calc (∑ k : Fin (Fintype.card n), if (k : ℕ) < r then hA.eigenvalues₀ k else 0)
        ≤ ∑ k : Fin (Fintype.card n), if (k : ℕ) < r then c else 0 :=
          Finset.sum_le_sum fun k _ => by
            split_ifs
            · exact hle k
            · exact le_rfl
      _ = ((Finset.univ.filter (fun k : Fin (Fintype.card n) => (k : ℕ) < r)).card : ℝ) * c := by
          rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
      _ ≤ r * c := by
          apply mul_le_mul_of_nonneg_right _ hc
          rw [Fin.card_filter_val_lt]
          exact_mod_cast min_le_right _ _
  linarith

end Projection

/-! ### T5: non-vacuity — the regular simplex -/

section Simplex

/-- Squared-distance matrix of the regular simplex on `L` points with unit edges: `0` on the
diagonal and `1` elsewhere. -/
def simplexSqDist (L : ℕ) : Matrix (Fin L) (Fin L) ℝ :=
  Matrix.of fun i j => if i = j then 0 else 1

theorem simplexSqDist_isSymm (L : ℕ) : (simplexSqDist L).IsSymm := by
  ext i j; simp [simplexSqDist, eq_comm]

theorem simplexSqDist_diag (L : ℕ) (i : Fin L) : simplexSqDist L i i = 0 := by
  simp [simplexSqDist]

/-- The hypotheses of `sstress_lower_bound` are satisfiable (see
`equilateral_triangle_sstress_lower_bound` below for a quantitative instance). -/
example : (simplexSqDist 3).IsSymm ∧ ∀ i, simplexSqDist 3 i i = 0 :=
  ⟨simplexSqDist_isSymm 3, simplexSqDist_diag 3⟩

/-- The equilateral triangle as an explicit matrix. -/
theorem simplexSqDist_three : simplexSqDist 3 = !![0, 1, 1; 1, 0, 1; 1, 1, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [simplexSqDist]

/-- The Gram matrix of the regular simplex is half the centering matrix. -/
theorem gramOfSqDist_simplexSqDist (L : ℕ) :
    gramOfSqDist (simplexSqDist L) = (1 / 2 : ℝ) • centering L := by
  rcases Nat.eq_zero_or_pos L with rfl | hL
  · ext i; exact i.elim0
  · have hL' : (L : ℝ) ≠ 0 := by positivity
    have hrow : ∀ i : Fin L, ∑ l, simplexSqDist L i l = (L : ℝ) - 1 := by
      intro i
      have : ∀ l : Fin L, simplexSqDist L i l = 1 - (if i = l then 1 else 0) := by
        intro l; by_cases h : i = l <;> simp [simplexSqDist, h]
      simp [this, Finset.sum_sub_distrib]
    ext i j
    simp only [gramOfSqDist, Matrix.smul_apply, smul_eq_mul,
      centering_mul_mul_centering_apply (simplexSqDist_isSymm L), hrow, centering_apply,
      Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    by_cases hij : i = j
    · simp [simplexSqDist, hij]; field_simp; ring
    · simp [simplexSqDist, hij]; field_simp; ring

/-- The Gram matrix of the regular simplex is a scaled projection. -/
theorem gramOfSqDist_simplexSqDist_mul_self (L : ℕ) :
    gramOfSqDist (simplexSqDist L) * gramOfSqDist (simplexSqDist L) =
      (1 / 2 : ℝ) • gramOfSqDist (simplexSqDist L) := by
  rw [gramOfSqDist_simplexSqDist, Matrix.smul_mul, Matrix.mul_smul, centering_mul_self]

/-- Spectral certificate of the simplex, squared part: `tailSq = (1/2) tailSum`. -/
theorem tailSq_gram_simplex (L r : ℕ) :
    tailSq (gramOfSqDist (simplexSqDist L)) r =
      1 / 2 * tailSum (gramOfSqDist (simplexSqDist L)) r :=
  tailSq_eq_mul_tailSum_of_mul_self_eq_smul (gramOfSqDist_isHermitian (simplexSqDist_isSymm L))
    (gramOfSqDist_simplexSqDist_mul_self L) r

/-- Spectral certificate of the simplex, trace part: `(L - 1 - r) / 2 ≤ tailSum`. -/
theorem tailSum_gram_simplex_ge {L : ℕ} (hL : 0 < L) (r : ℕ) :
    ((L : ℝ) - 1 - r) / 2 ≤ tailSum (gramOfSqDist (simplexSqDist L)) r := by
  have htrace : Matrix.trace (gramOfSqDist (simplexSqDist L)) = ((L : ℝ) - 1) / 2 := by
    rw [gramOfSqDist_simplexSqDist, Matrix.trace_smul, trace_centering hL]
    simp; ring
  have h2 := trace_sub_le_tailSum_of_mul_self_eq_smul
    (gramOfSqDist_isHermitian (simplexSqDist_isSymm L)) (by norm_num)
    (gramOfSqDist_simplexSqDist_mul_self L) r
  rw [htrace] at h2
  linarith

/-- All but the last decreasingly sorted eigenvalue of the simplex Gram matrix equal `1/2`. -/
theorem eigenvalues₀_gram_simplex {L : ℕ} (k : Fin (Fintype.card (Fin L)))
    (hk : (k : ℕ) + 1 < L) :
    (gramOfSqDist_isHermitian (simplexSqDist_isSymm L)).eigenvalues₀ k = 1 / 2 := by
  set hH := gramOfSqDist_isHermitian (simplexSqDist_isSymm L) with hHdef
  have hL : 0 < L := by omega
  have hmul := eigenvalues₀_mul_self_of_mul_self_eq_smul hH (gramOfSqDist_simplexSqDist_mul_self L)
  have hmem : ∀ j, hH.eigenvalues₀ j = 0 ∨ hH.eigenvalues₀ j = 1 / 2 := fun j => by
    have h1 := hmul j
    have h2 : hH.eigenvalues₀ j * (hH.eigenvalues₀ j - 1 / 2) = 0 := by linarith
    rcases mul_eq_zero.mp h2 with h0 | h0
    · exact Or.inl h0
    · exact Or.inr (by linarith)
  rcases hmem k with h0 | h0
  · -- if `λ₀ k = 0` then the whole tail from `k` on vanishes, contradicting the trace
    exfalso
    have hzero : ∀ j, k ≤ j → hH.eigenvalues₀ j = 0 := fun j hj => by
      have hanti := hH.eigenvalues₀_antitone hj
      rcases hmem j with h | h
      · exact h
      · rw [h, h0] at hanti; norm_num at hanti
    have htail : tailSum (gramOfSqDist (simplexSqDist L)) k = 0 := by
      rw [tailSum_eq hH]
      refine Finset.sum_eq_zero fun j _ => ?_
      split_ifs with hjk
      · rfl
      · exact hzero j (by rw [Fin.le_def]; omega)
    have hge := tailSum_gram_simplex_ge hL (k : ℕ)
    rw [htail] at hge
    have hk' : ((k : ℕ) : ℝ) + 1 < L := by exact_mod_cast hk
    linarith
  · exact h0

/-- Exact tail trace of the simplex Gram matrix: `tailSum = (L - 1 - r) / 2` for `r + 1 ≤ L`. -/
theorem tailSum_gram_simplex {L r : ℕ} (hr : r + 1 ≤ L) :
    tailSum (gramOfSqDist (simplexSqDist L)) r = ((L : ℝ) - 1 - r) / 2 := by
  have hL : 0 < L := by omega
  set hH := gramOfSqDist_isHermitian (simplexSqDist_isSymm L) with hHdef
  have htrace : ∑ k, hH.eigenvalues₀ k = ((L : ℝ) - 1) / 2 := by
    rw [← trace_eq_sum_eigenvalues₀ hH, gramOfSqDist_simplexSqDist, Matrix.trace_smul,
      trace_centering hL]
    simp; ring
  rw [tailSum_eq hH]
  have hsplit : ∑ k, hH.eigenvalues₀ k =
      (∑ k : Fin (Fintype.card (Fin L)), if (k : ℕ) < r then hH.eigenvalues₀ k else 0) +
        ∑ k : Fin (Fintype.card (Fin L)), if (k : ℕ) < r then 0 else hH.eigenvalues₀ k := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun k _ => ?_
    split_ifs <;> simp
  have hhead : (∑ k : Fin (Fintype.card (Fin L)), if (k : ℕ) < r then hH.eigenvalues₀ k else 0)
      = (r : ℝ) / 2 := by
    have hval : ∀ k : Fin (Fintype.card (Fin L)),
        (if (k : ℕ) < r then hH.eigenvalues₀ k else 0) =
          if (k : ℕ) < r then (1 / 2 : ℝ) else 0 := by
      intro k
      split_ifs with hk
      · exact eigenvalues₀_gram_simplex k (by omega)
      · rfl
    simp only [hval]
    rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, Fin.card_filter_val_lt,
      Fintype.card_fin, min_eq_right (by omega)]
    ring
  linarith

/-- **Exact value of the T4 certificate for the regular simplex**: for `r + 1 ≤ L` the left-hand
side of `sstress_lower_bound` equals `L (L - 1 - r) / (r + 1)`. -/
theorem simplex_certificate_eq {L r : ℕ} (hr : r + 1 ≤ L) :
    4 * (tailSq (gramOfSqDist (simplexSqDist L)) r +
        (tailSum (gramOfSqDist (simplexSqDist L)) r) ^ 2 / (r + 1)) =
      (L : ℝ) * ((L : ℝ) - 1 - r) / (r + 1) := by
  rw [tailSq_gram_simplex, tailSum_gram_simplex hr]
  field_simp
  ring

/-- **T5 (non-vacuity, general form).** Every configuration `Y` of `L` points in `ℝ^r` misses the
regular unit simplex by at least `L (L - 1 - r) / (r + 1)` in squared-distance misfit.  For
`r + 1 ≤ L` this is exactly the bound of `sstress_lower_bound` (see `simplex_certificate_eq`); it
is positive as soon as `r + 1 < L`.  (For `L ≤ r` the stated bound is nonpositive, hence trivial.) -/
theorem simplex_sstress_lower_bound (L r : ℕ) (Y : Matrix (Fin L) (Fin r) ℝ) :
    (L : ℝ) * ((L : ℝ) - 1 - r) / (r + 1) ≤
      ∑ i, ∑ j, (simplexSqDist L i j - sqDist Y i j) ^ 2 := by
  rcases Nat.lt_or_ge L (r + 1) with hLr | hLr
  · have hLr' : (L : ℝ) ≤ r := by exact_mod_cast Nat.lt_succ_iff.mp hLr
    have hr1 : (0 : ℝ) < r + 1 := by positivity
    have h0 : (L : ℝ) * ((L : ℝ) - 1 - r) / (r + 1) ≤ 0 :=
      div_nonpos_of_nonpos_of_nonneg
        (mul_nonpos_of_nonneg_of_nonpos (Nat.cast_nonneg _) (by linarith)) hr1.le
    exact h0.trans (Finset.sum_nonneg fun i _ => Finset.sum_nonneg fun j _ => sq_nonneg _)
  · rw [← simplex_certificate_eq hLr]
    exact sstress_lower_bound (simplexSqDist L) (simplexSqDist_isSymm L) (simplexSqDist_diag L) Y

/-- The regular simplex on `L` points is not realizable in `ℝ^r` when `r + 1 < L`. -/
theorem simplex_not_realizable {L r : ℕ} (hr : r + 1 < L) (Y : Matrix (Fin L) (Fin r) ℝ) :
    ∃ i j, sqDist Y i j ≠ simplexSqDist L i j := by
  by_contra! hcon
  have h := simplex_sstress_lower_bound L r Y
  have h0 : ∑ i, ∑ j, (simplexSqDist L i j - sqDist Y i j) ^ 2 = 0 := by simp [hcon]
  have h1 : (r : ℝ) + 1 < L := by exact_mod_cast hr
  have h2 : (0 : ℝ) ≤ r := Nat.cast_nonneg r
  have hpos : 0 < (L : ℝ) * ((L : ℝ) - 1 - r) / (r + 1) :=
    div_pos (mul_pos (by linarith) (by linarith)) (by linarith)
  linarith

/-- **T5 (non-vacuity witness).** No three points on a line come close to an equilateral triangle:
for every `Y : Matrix (Fin 3) (Fin 1) ℝ` the squared-distance misfit is at least `3/2`.  This is
the instance `L = 3`, `r = 1` of `sstress_lower_bound`, whose left-hand side equals `3/2`
(`simplex_certificate_eq`). -/
theorem equilateral_triangle_sstress_lower_bound (Y : Matrix (Fin 3) (Fin 1) ℝ) :
    (3 / 2 : ℝ) ≤ ∑ i, ∑ j, (simplexSqDist 3 i j - sqDist Y i j) ^ 2 := by
  have h := simplex_sstress_lower_bound 3 1 Y
  norm_num at h
  linarith

/-- The same witness with the equilateral triangle written out as an explicit matrix. -/
theorem equilateral_triangle_sstress_lower_bound' (Y : Matrix (Fin 3) (Fin 1) ℝ) :
    (3 / 2 : ℝ) ≤ ∑ i, ∑ j,
      ((!![0, 1, 1; 1, 0, 1; 1, 1, 0] : Matrix (Fin 3) (Fin 3) ℝ) i j - sqDist Y i j) ^ 2 := by
  rw [← simplexSqDist_three]
  exact equilateral_triangle_sstress_lower_bound Y

end Simplex

end MetricChain
