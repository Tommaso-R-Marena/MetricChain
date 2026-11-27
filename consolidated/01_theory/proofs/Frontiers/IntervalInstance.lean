import Mathlib
import proofs.Core.Rounding
import proofs.Frontiers.PartitionCertificate

/-!
# From interval energy tables to certified partition functions

`Z_encloses_partitionFn` brackets the real partition function of a pairwise model by the exact
rational partition sums of two weight instances, *assuming* that their entries bracket the true
Boltzmann factors.  This file discharges that assumption from the certified exponential of
`Core/Rounding.lean`:

* `WInstance.lowerOfIntervals`, `WInstance.upperOfIntervals` — the two weight instances are
  *computed* from rational interval tables enclosing the energies (`expLo` of the scaled lower
  endpoint, `expHi` of the scaled upper endpoint), so a checker can recompute them;
* `Z_encloses_partitionFn_of_intervals` — if every table entry of the real model lies in its
  rational interval, the computed instances bracket the real partition function;
* `certified_partition_of_intervals` — hence two certificates accepted by the top-level kernel
  `zverifyTop` give a two-sided rational enclosure of the real partition function.  The only
  remaining hypotheses are the enclosures of the energy tables and the range condition of the
  certified exponential.
-/

namespace MetricChain

open Finset

variable {n k : ℕ}

/-- Lower weight instance computed from rational interval tables of the energies:
entry `expLo` of the scaled interval, a rational lower bound of the Boltzmann factor. -/
def WInstance.lowerOfIntervals (β : ℚ) (N K : ℕ) (Ih : Fin n → Fin k → QInterval)
    (IJ : Fin n → Fin n → Fin k → Fin k → QInterval) : WInstance n k where
  w i a := (((Ih i a).scale (-β)).exp N K).lo
  W i j a b := (((IJ i j a b).scale (-β)).exp N K).lo

/-- Upper weight instance computed from rational interval tables of the energies. -/
def WInstance.upperOfIntervals (β : ℚ) (N K : ℕ) (Ih : Fin n → Fin k → QInterval)
    (IJ : Fin n → Fin n → Fin k → Fin k → QInterval) : WInstance n k where
  w i a := (((Ih i a).scale (-β)).exp N K).hi
  W i j a b := (((IJ i j a b).scale (-β)).exp N K).hi

/-- The computed lower instance has nonnegative factors (no hypothesis needed). -/
theorem WInstance.lowerOfIntervals_nonneg (β : ℚ) (N K : ℕ) (Ih : Fin n → Fin k → QInterval)
    (IJ : Fin n → Fin n → Fin k → Fin k → QInterval) :
    (WInstance.lowerOfIntervals β N K Ih IJ).Nonneg :=
  ⟨fun _ _ => expLo_nonneg _ _ _, fun _ _ _ _ => expLo_nonneg _ _ _⟩

/-- **From interval energy tables to an enclosure of the real partition function.**  If rational
intervals enclose every table entry of a real pairwise model, the weight instances computed from
them by the certified exponential bracket the real partition function over every box. -/
theorem Z_encloses_partitionFn_of_intervals (M : PairModel ℝ (Fin n) (fun _ => Fin k)) (β : ℚ)
    {N K : ℕ} (hN : 0 < N) (Ih : Fin n → Fin k → QInterval)
    (IJ : Fin n → Fin n → Fin k → Fin k → QInterval)
    (hbh : ∀ i a, |β * (Ih i a).lo| ≤ 2 ^ K ∧ |β * (Ih i a).hi| ≤ 2 ^ K)
    (hbJ : ∀ i j a b, |β * (IJ i j a b).lo| ≤ 2 ^ K ∧ |β * (IJ i j a b).hi| ≤ 2 ^ K)
    (hh : ∀ i a, (Ih i a).Contains (M.h i a))
    (hJ : ∀ i j a b, (IJ i j a b).Contains (M.J i j a b)) (D : Dom n k) :
    (((WInstance.lowerOfIntervals β N K Ih IJ).Z D : ℚ) : ℝ) ≤
        partitionFn (β : ℝ) M.energy (boxFinset D) ∧
      partitionFn (β : ℝ) M.energy (boxFinset D) ≤
        (((WInstance.upperOfIntervals β N K Ih IJ).Z D : ℚ) : ℝ) := by
  refine Z_encloses_partitionFn M (β : ℝ) _ _ (WInstance.lowerOfIntervals_nonneg β N K Ih IJ)
    (fun i a => ?_) (fun i j a b => ?_) D
  · exact QInterval.contains_boltzmann hN β (hbh i a).1 (hbh i a).2 (hh i a)
  · exact QInterval.contains_boltzmann hN β (hbJ i j a b).1 (hbJ i j a b).2 (hJ i j a b)

/-- **Certified real partition function from interval tables.**  Two certificates accepted by the
top-level kernel for the two computed instances enclose the real partition function. -/
theorem certified_partition_of_intervals (M : PairModel ℝ (Fin n) (fun _ => Fin k)) (β : ℚ)
    {N K : ℕ} (hN : 0 < N) (Ih : Fin n → Fin k → QInterval)
    (IJ : Fin n → Fin n → Fin k → Fin k → QInterval)
    (hbh : ∀ i a, |β * (Ih i a).lo| ≤ 2 ^ K ∧ |β * (Ih i a).hi| ≤ 2 ^ K)
    (hbJ : ∀ i j a b, |β * (IJ i j a b).lo| ≤ 2 ^ K ∧ |β * (IJ i j a b).hi| ≤ 2 ^ K)
    (hh : ∀ i a, (Ih i a).Contains (M.h i a))
    (hJ : ∀ i j a b, (IJ i j a b).Contains (M.J i j a b)) (D : Dom n k)
    (clo chi : ZCert n k) (a b a' b' : ℚ)
    (hclo : zverifyTop clo (WInstance.lowerOfIntervals β N K Ih IJ) D = some (a, b))
    (hchi : zverifyTop chi (WInstance.upperOfIntervals β N K Ih IJ) D = some (a', b')) :
    (a : ℝ) ≤ partitionFn (β : ℝ) M.energy (boxFinset D) ∧
      partitionFn (β : ℝ) M.energy (boxFinset D) ≤ (b' : ℝ) := by
  have h := Z_encloses_partitionFn_of_intervals M β hN Ih IJ hbh hbJ hh hJ D
  have h1 := (zverifyTop_sound clo _ D a b hclo).1
  have h2 := (zverifyTop_sound chi _ D a' b' hchi).2
  have h1' : (a : ℝ) ≤ (((WInstance.lowerOfIntervals β N K Ih IJ).Z D : ℚ) : ℝ) := by
    exact_mod_cast h1
  have h2' : (((WInstance.upperOfIntervals β N K Ih IJ).Z D : ℚ) : ℝ) ≤ (b' : ℝ) := by
    exact_mod_cast h2
  exact ⟨le_trans h1' h.1, le_trans h.2 h2'⟩

/-! ### Executable example

The frustrated triangle with exact energies `1` (equal neighbours, `i < j`) and `0`, at `β = 1`:
the instances are computed from point intervals with `N = 8` Taylor terms and `K = 1` halving, the
enumeration certificate is run by the kernel, and the result encloses the real partition function
`2 e^{-3} + 6 e^{-1} ≈ 2.3069`. -/

/-- Point-interval tables of the triangle energies. -/
def triangleIh : Fin 3 → Fin 2 → QInterval := fun _ _ => QInterval.point 0

/-- Point-interval tables of the triangle pair energies. -/
def triangleIJ : Fin 3 → Fin 3 → Fin 2 → Fin 2 → QInterval :=
  fun i j a b => QInterval.point (if i < j ∧ a = b then 1 else 0)

/-- Enumeration certificate with exact leaves for a weight instance on three binary sites. -/
def enumZCert (I : WInstance 3 2) : ZCert 3 2 :=
  .branch 0 fun a => .branch 1 fun b => .branch 2 fun c =>
    .leaf (fun i j => I.W i j (![a, b, c] i) (![a, b, c] j))
      (fun i j => I.W i j (![a, b, c] i) (![a, b, c] j))

/-- The frustrated triangle as a real pairwise model. -/
noncomputable def triangleReal : PairModel ℝ (Fin 3) (fun _ => Fin 2) where
  h := fun _ _ => 0
  J := fun i j a b => if i < j ∧ a = b then 1 else 0

/-- Kernel run on the computed lower instance: accepted, with lower endpoint at least `2.3068`. -/
theorem triangle_interval_lo :
    (match zverifyTop (enumZCert (WInstance.lowerOfIntervals 1 8 1 triangleIh triangleIJ))
        (WInstance.lowerOfIntervals 1 8 1 triangleIh triangleIJ) (fullDom 3 2) with
      | some p => decide ((23068 : ℚ) / 10000 ≤ p.1)
      | none => false) = true := by
  decide +kernel

/-- Kernel run on the computed upper instance: accepted, with upper endpoint at most `2.3069`. -/
theorem triangle_interval_hi :
    (match zverifyTop (enumZCert (WInstance.upperOfIntervals 1 8 1 triangleIh triangleIJ))
        (WInstance.upperOfIntervals 1 8 1 triangleIh triangleIJ) (fullDom 3 2) with
      | some p => decide (p.2 ≤ (23069 : ℚ) / 10000)
      | none => false) = true := by
  decide +kernel

/-- **End-to-end example.**  The real partition function `2 e⁻³ + 6 e⁻¹` of the frustrated
triangle at `β = 1` lies in `[2.3068, 2.3069]`: energies ↦ interval tables ↦ computed rational
weight instances ↦ kernel-checked certificates ↦ bound on the real number, with no analytic
hypothesis left. -/
theorem triangle_real_partition_enclosure :
    (23068 / 10000 : ℝ) ≤ partitionFn 1 triangleReal.energy (boxFinset (fullDom 3 2)) ∧
      partitionFn 1 triangleReal.energy (boxFinset (fullDom 3 2)) ≤ (23069 / 10000 : ℝ) := by
  have hlo := triangle_interval_lo
  have hhi := triangle_interval_hi
  cases h1 : zverifyTop (enumZCert (WInstance.lowerOfIntervals 1 8 1 triangleIh triangleIJ))
      (WInstance.lowerOfIntervals 1 8 1 triangleIh triangleIJ) (fullDom 3 2) with
  | none => rw [h1] at hlo; exact absurd hlo (by simp)
  | some p =>
    cases h2 : zverifyTop (enumZCert (WInstance.upperOfIntervals 1 8 1 triangleIh triangleIJ))
        (WInstance.upperOfIntervals 1 8 1 triangleIh triangleIJ) (fullDom 3 2) with
    | none => rw [h2] at hhi; exact absurd hhi (by simp)
    | some p' =>
      rw [h1] at hlo
      rw [h2] at hhi
      simp only [decide_eq_true_eq] at hlo hhi
      have key := certified_partition_of_intervals triangleReal 1 (N := 8) (K := 1) (by norm_num)
        triangleIh triangleIJ
        (fun i a => by simp [triangleIh, QInterval.point])
        (fun i j a b => by
          simp only [triangleIJ, QInterval.point]
          split_ifs <;> norm_num)
        (fun i a => by simp [triangleIh, triangleReal, QInterval.point, QInterval.Contains])
        (fun i j a b => by
          simp only [triangleIJ, triangleReal, QInterval.point, QInterval.Contains]
          split_ifs <;> simp)
        (fullDom 3 2) _ _ p.1 p.2 p'.1 p'.2 h1 h2
      have e1 : ((1 : ℚ) : ℝ) = 1 := by norm_num
      rw [e1] at key
      have a1 : ((23068 / 10000 : ℚ) : ℝ) ≤ (p.1 : ℝ) := by exact_mod_cast hlo
      have a2 : (p'.2 : ℝ) ≤ ((23069 / 10000 : ℚ) : ℝ) := by exact_mod_cast hhi
      push_cast at a1 a2
      exact ⟨le_trans a1 key.1, le_trans key.2 a2⟩

end MetricChain
