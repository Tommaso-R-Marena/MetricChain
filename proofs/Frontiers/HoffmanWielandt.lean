import Mathlib

/-!
# The Hoffman–Wielandt inequality for real symmetric matrices

For real symmetric matrices `A`, `B` indexed by a finite type `n`, with decreasingly sorted
eigenvalue lists `λ₀(A), λ₀(B) : Fin (Fintype.card n) → ℝ` (Mathlib's
`Matrix.IsHermitian.eigenvalues₀`), we prove

* `MetricChain.trace_mul_le_sum_sorted_eigenvalues` — the **von Neumann trace inequality**
  (symmetric case): `trace (A * B) ≤ ∑ k, λ₀(A) k * λ₀(B) k`;
* `MetricChain.hoffman_wielandt` — the **Hoffman–Wielandt inequality**:
  `∑ k, (λ₀(A) k - λ₀(B) k)² ≤ ∑ i, ∑ j, (A i j - B i j)²`, i.e. the sorted spectrum is
  1-Lipschitz from the Frobenius norm to the Euclidean norm.

## Proof outline

1. Spectral theorem: `A = U diag(a) Uᵀ`, `B = V diag(b) Vᵀ` with `U`, `V` orthogonal
   (`exists_orthogonal_diagonalization`).
2. With `W = Uᵀ V`: `trace (A * B) = ∑ i j, a i * b j * (W i j)²`
   (`trace_conj_diagonal_mul_conj_diagonal`).
3. `(W i j)²` is a doubly stochastic matrix (`sq_entries_mem_doublyStochastic`).
4. Birkhoff's theorem: a linear functional on the doubly stochastic matrices is bounded by its
   maximum over permutation matrices (`sum_mul_doublyStochastic_le`).
5. Rearrangement inequality for the two antitone eigenvalue lists
   (`sum_eigenvalues_mul_perm_le`).
6. Frobenius expansion `‖A - B‖² = tr A² - 2 tr AB + tr B²` and `tr A² = ∑ λ₀(A)²`
   (`sum_sq_sub_eq_trace`, `trace_mul_self_eq_sum_sq_eigenvalues₀`).

The auxiliary identities `trace_eq_sum_eigenvalues₀`, `trace_mul_self_eq_sum_sq_eigenvalues₀` and
`sum_sq_eq_sum_sq_eigenvalues₀` (trace, trace of the square and squared Frobenius norm in terms of
the sorted spectrum) are exported for use in `proofs/Frontiers/Realizability.lean`.
-/

namespace MetricChain

open Matrix Finset

variable {n : Type*} [Fintype n] [DecidableEq n]

/-! ### Spectral decomposition and the trace formula -/

/-- Trace of a product of two orthogonally conjugated diagonal matrices: with `W = Uᵀ V`,
`trace ((U diag(a) Uᵀ) (V diag(b) Vᵀ)) = ∑ i j, a i * b j * (W i j)²`.
(No orthogonality assumption is needed for this identity.) -/
theorem trace_conj_diagonal_mul_conj_diagonal (U V : Matrix n n ℝ) (a b : n → ℝ) :
    Matrix.trace ((U * diagonal a * Uᵀ) * (V * diagonal b * Vᵀ)) =
      ∑ i, ∑ j, a i * b j * ((Uᵀ * V) i j) ^ 2 := by
  have h : (U * diagonal a * Uᵀ) * (V * diagonal b * Vᵀ)
      = U * (diagonal a * (Uᵀ * V) * diagonal b * Vᵀ) := by
    simp only [Matrix.mul_assoc]
  rw [h, Matrix.trace_mul_comm]
  have h2 : diagonal a * (Uᵀ * V) * diagonal b * Vᵀ * U
      = diagonal a * (Uᵀ * V) * diagonal b * (Uᵀ * V)ᵀ := by
    rw [Matrix.transpose_mul, Matrix.transpose_transpose]
    simp only [Matrix.mul_assoc]
  rw [h2]
  simp only [Matrix.trace, Matrix.diag_apply]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Matrix.mul_apply]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [Matrix.mul_diagonal, Matrix.diagonal_mul, Matrix.transpose_apply]
  ring

/-- Spectral theorem for a real symmetric matrix in orthogonal form: `A = U diag(a) Uᵀ` with
`Uᵀ U = U Uᵀ = 1` and `a = hA.eigenvalues` (Mathlib's eigenvalue function indexed by `n`). -/
theorem exists_orthogonal_diagonalization (A : Matrix n n ℝ) (hA : A.IsHermitian) :
    ∃ U : Matrix n n ℝ, Uᵀ * U = 1 ∧ U * Uᵀ = 1 ∧ A = U * diagonal hA.eigenvalues * Uᵀ := by
  refine ⟨(hA.eigenvectorUnitary : Matrix n n ℝ), ?_, ?_, ?_⟩
  · have := Unitary.coe_star_mul_self hA.eigenvectorUnitary
    simpa [Matrix.star_eq_conjTranspose] using this
  · have := Unitary.coe_mul_star_self hA.eigenvectorUnitary
    simpa [Matrix.star_eq_conjTranspose] using this
  · have := hA.spectral_theorem
    rw [Unitary.conjStarAlgAut_apply] at this
    simpa [Matrix.star_eq_conjTranspose] using this

/-! ### Doubly stochastic matrices and Birkhoff's theorem -/

/-- The entrywise square of an orthogonal matrix is doubly stochastic. -/
theorem sq_entries_mem_doublyStochastic (W : Matrix n n ℝ) (h1 : W * Wᵀ = 1) (h2 : Wᵀ * W = 1) :
    (Matrix.of fun i j => (W i j) ^ 2) ∈ doublyStochastic ℝ n := by
  rw [mem_doublyStochastic_iff_sum]
  refine ⟨fun i j => sq_nonneg _, fun i => ?_, fun j => ?_⟩
  · have := congrFun (congrFun h1 i) i
    simpa [Matrix.mul_apply, sq] using this
  · have := congrFun (congrFun h2 j) j
    simpa [Matrix.mul_apply, sq] using this

/-- The bilinear functional `S ↦ ∑ i j, a i * b j * S i j` evaluated at a permutation matrix. -/
theorem sum_mul_permMatrix (a b : n → ℝ) (σ : Equiv.Perm n) :
    ∑ i, ∑ j, a i * b j * (σ.permMatrix ℝ) i j = ∑ i, a i * b (σ i) := by
  simp [Equiv.Perm.permMatrix, PEquiv.toMatrix_apply, Equiv.toPEquiv_apply]

/-- **Birkhoff bound.** A linear functional `S ↦ ∑ i j, a i * b j * S i j` on the doubly stochastic
matrices is bounded by any bound valid on all permutation matrices. -/
theorem sum_mul_doublyStochastic_le (a b : n → ℝ) (c : ℝ)
    (hc : ∀ σ : Equiv.Perm n, ∑ i, a i * b (σ i) ≤ c) {S : Matrix n n ℝ}
    (hS : S ∈ doublyStochastic ℝ n) : ∑ i, ∑ j, a i * b j * S i j ≤ c := by
  have hS' : S ∈ convexHull ℝ {x | ∃ σ : Equiv.Perm n, σ.permMatrix ℝ = x} := by
    rw [← doublyStochastic_eq_convexHull_permMatrix]; exact hS
  have hlin : IsLinearMap ℝ (fun S : Matrix n n ℝ => ∑ i, ∑ j, a i * b j * S i j) := by
    refine ⟨fun S T => ?_, fun r S => ?_⟩
    · simp [mul_add, Finset.sum_add_distrib]
    · simp only [Matrix.smul_apply, smul_eq_mul, Finset.mul_sum]
      refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
      ring
  have hconv : Convex ℝ {S : Matrix n n ℝ | ∑ i, ∑ j, a i * b j * S i j ≤ c} :=
    convex_halfSpace_le hlin c
  refine convexHull_min ?_ hconv hS'
  rintro _ ⟨σ, rfl⟩
  simp only [Set.mem_setOf_eq]
  rw [sum_mul_permMatrix]
  exact hc σ

/-! ### Sorted versus unsorted eigenvalues, rearrangement -/

/-- Sums over the `n`-indexed eigenvalues agree with sums over the sorted eigenvalues. -/
theorem sum_eigenvalues_eq_sum_eigenvalues₀ {A : Matrix n n ℝ} (hA : A.IsHermitian)
    (f : ℝ → ℝ) : ∑ i, f (hA.eigenvalues i) = ∑ k, f (hA.eigenvalues₀ k) := by
  rw [← Equiv.sum_comp (Fintype.equivOfCardEq (Fintype.card_fin _))]
  simp [Matrix.IsHermitian.eigenvalues]

/-- **Rearrangement step.** Pairing the eigenvalues of `A` and `B` along any permutation gives at
most the pairing of the two decreasingly sorted lists. -/
theorem sum_eigenvalues_mul_perm_le {A B : Matrix n n ℝ} (hA : A.IsHermitian)
    (hB : B.IsHermitian) (σ : Equiv.Perm n) :
    ∑ i, hA.eigenvalues i * hB.eigenvalues (σ i) ≤
      ∑ k, hA.eigenvalues₀ k * hB.eigenvalues₀ k := by
  set e : Fin (Fintype.card n) ≃ n := Fintype.equivOfCardEq (Fintype.card_fin _) with he
  have h1 : ∑ i, hA.eigenvalues i * hB.eigenvalues (σ i) =
      ∑ k, hA.eigenvalues₀ k * hB.eigenvalues₀ ((e.trans (σ.trans e.symm)) k) := by
    rw [← Equiv.sum_comp e]
    simp [Matrix.IsHermitian.eigenvalues, he]
  rw [h1]
  exact Monovary.sum_mul_comp_perm_le_sum_mul
    (hA.eigenvalues₀_antitone.monovary hB.eigenvalues₀_antitone)

/-! ### The von Neumann trace inequality -/

/-- **von Neumann trace inequality** (real symmetric case): `trace (A * B)` is at most the pairing
of the decreasingly sorted eigenvalues of `A` and `B`. -/
theorem trace_mul_le_sum_sorted_eigenvalues (A B : Matrix n n ℝ) (hA : A.IsHermitian)
    (hB : B.IsHermitian) :
    Matrix.trace (A * B) ≤ ∑ k, hA.eigenvalues₀ k * hB.eigenvalues₀ k := by
  obtain ⟨U, hU1, hU2, hAU⟩ := exists_orthogonal_diagonalization A hA
  obtain ⟨V, hV1, hV2, hBV⟩ := exists_orthogonal_diagonalization B hB
  have key := trace_conj_diagonal_mul_conj_diagonal U V hA.eigenvalues hB.eigenvalues
  rw [← hAU, ← hBV] at key
  rw [key]
  have hW1 : (Uᵀ * V) * (Uᵀ * V)ᵀ = 1 := by
    rw [Matrix.transpose_mul, Matrix.transpose_transpose, Matrix.mul_assoc,
      ← Matrix.mul_assoc V, hV2, Matrix.one_mul, hU1]
  have hW2 : (Uᵀ * V)ᵀ * (Uᵀ * V) = 1 := by
    rw [Matrix.transpose_mul, Matrix.transpose_transpose, Matrix.mul_assoc,
      ← Matrix.mul_assoc U, hU2, Matrix.one_mul, hV1]
  exact sum_mul_doublyStochastic_le _ _ _ (sum_eigenvalues_mul_perm_le hA hB)
    (sq_entries_mem_doublyStochastic _ hW1 hW2)

/-! ### Trace identities in terms of the sorted spectrum -/

/-- The trace of a real symmetric matrix is the sum of its sorted eigenvalues. -/
theorem trace_eq_sum_eigenvalues₀ {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    Matrix.trace A = ∑ k, hA.eigenvalues₀ k := by
  rw [hA.trace_eq_sum_eigenvalues]
  exact sum_eigenvalues_eq_sum_eigenvalues₀ hA (fun x => x)

/-- `trace (A * A)` is the sum of the squares of the sorted eigenvalues. -/
theorem trace_mul_self_eq_sum_sq_eigenvalues₀ {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    Matrix.trace (A * A) = ∑ k, hA.eigenvalues₀ k ^ 2 := by
  obtain ⟨U, hU1, hU2, hAU⟩ := exists_orthogonal_diagonalization A hA
  have key := trace_conj_diagonal_mul_conj_diagonal U U hA.eigenvalues hA.eigenvalues
  rw [← hAU, hU1] at key
  rw [key, ← sum_eigenvalues_eq_sum_eigenvalues₀ hA (fun x => x ^ 2)]
  refine Finset.sum_congr rfl fun i _ => ?_
  simp [Matrix.one_apply, sq]

omit [DecidableEq n] in
/-- For symmetric `B`, `trace (A * B)` is the entrywise (Frobenius) inner product. -/
theorem trace_mul_eq_sum_mul {A B : Matrix n n ℝ} (hB : B.IsHermitian) :
    Matrix.trace (A * B) = ∑ i, ∑ j, A i j * B i j := by
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  have := hB.apply i j
  simp only [star_trivial] at this
  rw [this]

omit [DecidableEq n] in
/-- Frobenius expansion: `‖A - B‖_F² = tr A² - 2 tr AB + tr B²` for symmetric `A`, `B`. -/
theorem sum_sq_sub_eq_trace {A B : Matrix n n ℝ} (hA : A.IsHermitian) (hB : B.IsHermitian) :
    ∑ i, ∑ j, (A i j - B i j) ^ 2 =
      Matrix.trace (A * A) - 2 * Matrix.trace (A * B) + Matrix.trace (B * B) := by
  rw [trace_mul_eq_sum_mul hA, trace_mul_eq_sum_mul hB, trace_mul_eq_sum_mul hB]
  simp only [Finset.mul_sum, ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  ring

/-- The squared Frobenius norm of a real symmetric matrix is the sum of the squares of its sorted
eigenvalues. -/
theorem sum_sq_eq_sum_sq_eigenvalues₀ {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    ∑ i, ∑ j, A i j ^ 2 = ∑ k, hA.eigenvalues₀ k ^ 2 := by
  rw [← trace_mul_self_eq_sum_sq_eigenvalues₀ hA, trace_mul_eq_sum_mul hA]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  ring

/-! ### The Hoffman–Wielandt inequality -/

/-- **Hoffman–Wielandt inequality** for real symmetric matrices: the decreasingly sorted spectrum
is 1-Lipschitz from the Frobenius norm to the Euclidean norm,
`∑ k, (λ₀(A) k - λ₀(B) k)² ≤ ∑ i j, (A i j - B i j)²`. -/
theorem hoffman_wielandt (A B : Matrix n n ℝ)
    (hA : A.IsHermitian) (hB : B.IsHermitian) :
    ∑ k, (hA.eigenvalues₀ k - hB.eigenvalues₀ k) ^ 2 ≤ ∑ i, ∑ j, (A i j - B i j) ^ 2 := by
  have hspec : ∑ k, (hA.eigenvalues₀ k - hB.eigenvalues₀ k) ^ 2 =
      (∑ k, hA.eigenvalues₀ k ^ 2) - 2 * (∑ k, hA.eigenvalues₀ k * hB.eigenvalues₀ k)
        + ∑ k, hB.eigenvalues₀ k ^ 2 := by
    simp only [Finset.mul_sum, ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun k _ => ?_
    ring
  rw [sum_sq_sub_eq_trace hA hB, hspec, trace_mul_self_eq_sum_sq_eigenvalues₀ hA,
    trace_mul_self_eq_sum_sq_eigenvalues₀ hB]
  have := trace_mul_le_sum_sorted_eigenvalues A B hA hB
  linarith

end MetricChain
