import Mathlib
import proofs.Frontiers.PartitionProduct

/-!
# Summing a site out of a box sum: the identity behind bucket elimination

`WInstance.elim1` and `WInstance.elim2` (`PartitionProduct.lean`) sum out a site with one or two
neighbours because the result is again a pairwise instance.  The identity underneath does not
depend on the pairwise form.  This file states it for arbitrary summands — as asked by the
Structural & Computational Biology division (STRUCTBIO-REQ-0003, item R-1) — together with the
termwise relaxation of a factor (the semantic core of its item R-3):

* `sum_boxFinset_branch` — a box sum is additive over the states of a site (the general form of
  `WInstance.Z_branch`);
* `sum_boxFinset_elim` — if `G` does not depend on site `i`, then
  `∑_{x ∈ D} F x · G x = ∑_{y ∈ D, y_i = p} (∑_{a ∈ D_i} F (y[i ↦ a])) · G y`;
* `sum_boxFinset_sumOut` — the case `G = 1`;
* `sum_boxFinset_relax` — if `lo · F' ≤ F ≤ hi · F'` on the box and `G ≥ 0`, the box sums of `F · G`
  and `F' · G` are within the factors `lo` and `hi`.

These are *semantic* rules about sums of rational functions over a box.  They are not an
executable certificate kernel: a checker of tables that implements bucket elimination is not
verified by this file.
-/

namespace MetricChain

open Finset

variable {n k : ℕ}

/-- A sum over a box is additive over the states of a site. -/
theorem sum_boxFinset_branch (D : Dom n k) (i : Fin n) (f : Config n k → ℚ) :
    ∑ x ∈ boxFinset D, f x = ∑ a ∈ (D i).toFinset, ∑ x ∈ boxFinset (D.fix i a), f x := by
  have hmaps : ∀ x ∈ boxFinset D, x i ∈ (D i).toFinset := fun x hx =>
    List.mem_toFinset.mpr (mem_boxFinset.mp hx i)
  rw [← Finset.sum_fiberwise_of_maps_to hmaps]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr _ (fun _ _ => rfl)
  ext x
  simp only [Finset.mem_filter, mem_boxFinset]
  constructor
  · rintro ⟨hx, hxa⟩ j
    unfold Dom.fix
    by_cases hj : j = i
    · subst hj
      simp [hxa]
    · rw [Function.update_of_ne hj]
      exact hx j
  · intro hx
    have hxi : x i = a := by
      have h := hx i
      unfold Dom.fix at h
      simpa using h
    refine ⟨fun j => ?_, hxi⟩
    by_cases hj : j = i
    · subst hj
      rw [hxi]
      exact List.mem_toFinset.mp ha
    · have h := hx j
      unfold Dom.fix at h
      rwa [Function.update_of_ne hj] at h

/-- **Bucket elimination.**  If `G` does not depend on site `i`, the sum of `F · G` over a box is
the sum, over the box with site `i` pinned to any state `p`, of `G` times the sum of `F` over the
states of site `i`. -/
theorem sum_boxFinset_elim (D : Dom n k) (i : Fin n) (p : Fin k) (F G : Config n k → ℚ)
    (hG : ∀ (x : Config n k) (a : Fin k), G (Function.update x i a) = G x) :
    ∑ x ∈ boxFinset D, F x * G x =
      ∑ y ∈ boxFinset (D.fix i p), (∑ a ∈ (D i).toFinset, F (Function.update y i a)) * G y := by
  rw [sum_boxFinset_branch D i]
  have h1 : ∀ a ∈ (D i).toFinset, ∑ x ∈ boxFinset (D.fix i a), F x * G x =
      ∑ y ∈ boxFinset (D.fix i p), F (Function.update y i a) * G y := by
    intro a _
    rw [sum_boxFinset_fix D i a p]
    apply Finset.sum_congr rfl
    intro y _
    rw [hG]
  rw [Finset.sum_congr rfl h1, Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro y _
  rw [Finset.sum_mul]

/-- Summing a site out of a box sum (the case `G = 1` of `sum_boxFinset_elim`; it also shows that
the hypothesis on `G` is satisfiable). -/
theorem sum_boxFinset_sumOut (D : Dom n k) (i : Fin n) (p : Fin k) (F : Config n k → ℚ) :
    ∑ x ∈ boxFinset D, F x =
      ∑ y ∈ boxFinset (D.fix i p), ∑ a ∈ (D i).toFinset, F (Function.update y i a) := by
  have h := sum_boxFinset_elim D i p F (fun _ => 1) (fun _ _ => rfl)
  simpa using h

/-- **Termwise relaxation of a factor.**  If `lo · F' ≤ F ≤ hi · F'` on the box and `G` is
nonnegative there, the box sums of `F · G` and of `F' · G` are within the factors `lo` and `hi`. -/
theorem sum_boxFinset_relax (D : Dom n k) (F F' G : Config n k → ℚ) (lo hi : ℚ)
    (hG : ∀ x ∈ boxFinset D, 0 ≤ G x)
    (h : ∀ x ∈ boxFinset D, lo * F' x ≤ F x ∧ F x ≤ hi * F' x) :
    lo * ∑ x ∈ boxFinset D, F' x * G x ≤ ∑ x ∈ boxFinset D, F x * G x ∧
      ∑ x ∈ boxFinset D, F x * G x ≤ hi * ∑ x ∈ boxFinset D, F' x * G x := by
  constructor
  · rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro x hx
    have h1 := mul_le_mul_of_nonneg_right (h x hx).1 (hG x hx)
    linarith [h1]
  · rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro x hx
    have h1 := mul_le_mul_of_nonneg_right (h x hx).2 (hG x hx)
    linarith [h1]

end MetricChain
