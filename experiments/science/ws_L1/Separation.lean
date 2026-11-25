import Mathlib

/-!
# The separation inequality of Theorem 4′ (symmetrised cones)

Science division, workstream L1.  Source: `docs/science/INFERENCE_LIMITS_ADDENDA.md`, A1,
Theorem 4′ (the non-adaptive exponent is unchanged by a marginal oracle), the step
"it remains to bound the separation".

Notation of the note: `d_C = d_H(·, s + C)` the Hamming distance to the translated code,
`A = Z(cone^C_s) = ∑ exp (-u d_C)`, `F = Z(flat^C_s) = ∑ exp (-u max (d_C, R))`, and `A₁`, `F₁`
the same sums for `C = {0}`; `D_R = log A₁ - log F₁`.  Claim of the note:
`A / F ≥ 1 + (exp D_R - 1) / |C| ≥ exp D_R / |C|`, i.e. `log A - log F ≥ D_R - log |C|`.

## What is proved

Abstract part (any finite type `X`, real-valued profiles `dC ≤ d1` pointwise, `u ≥ 0`, any `R`):

* `exp_sub_exp_max_antitone` — `t ↦ exp (-u t) - exp (-u max (t, R))` is non-increasing;
* `pSum_sub_flat_mono` — hence `A₁ - F₁ ≤ A - F`;
* `separation_ratio` — if `F ≤ m * F₁` then `1 + (A₁ / F₁ - 1) / m ≤ A / F`;
* `separation_log` — if moreover `1 ≤ m` then `log (A₁ / F₁) - log m ≤ log A - log F`.

Concrete part (`ι → G`, `G` a finite additive commutative group with decidable equality — in
particular `Fin n → ZMod 2`; `C` *any* non-empty finite set of translations, no linearity
needed):

* `distToCoset C hC s x = min_{a ∈ C} d_H(x, s + a)`;
* `pSum_flat_distToCoset_le` — `F ≤ |C| * F₁`;
* `distToCoset_le` — `d_C ≤ d_H(·, s)` when `0 ∈ C`;
* `separation_distToCoset` — `log (A₁ / F₁) - log |C| ≤ log A - log F`;
* `sensitivity_distToCoset` — hence `ε < log (A₁/F₁) - log |C|` implies `ε < log A - log F`,
  the hypothesis `hsens` needed by the theory division's non-adaptive packing bound.

Not proved here: the closed forms `A₁ = (1 + exp (-u))^n` and
`F₁ = ∑_j C(n,j) exp (-u max (j, R))` (so `D_R` appears as `log (A₁ / F₁)`), and the
query lower bound itself.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL1

open Finset

/-! ### Abstract separation -/

section Abstract

variable {X : Type*} [Fintype X]

/-- The partition sum `∑ x, exp (-u * h x)` of the energy profile `h` at inverse temperature
`u` (zero known part). -/
def pSum (u : ℝ) (h : X → ℝ) : ℝ := ∑ x, Real.exp (-u * h x)

theorem pSum_pos [Nonempty X] (u : ℝ) (h : X → ℝ) : 0 < pSum u h :=
  Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty

omit [Fintype X] in
/-- For `u ≥ 0`, `t ↦ exp (-u t) - exp (-u max (t, R)) = (exp (-u t) - exp (-u R))₊` is
non-increasing. -/
theorem exp_sub_exp_max_antitone {u : ℝ} (hu : 0 ≤ u) (R : ℝ) {s t : ℝ} (hst : s ≤ t) :
    Real.exp (-u * t) - Real.exp (-u * max t R) ≤
      Real.exp (-u * s) - Real.exp (-u * max s R) := by
  rcases le_total t R with htR | hRt
  · rw [max_eq_right htR, max_eq_right (hst.trans htR)]
    have h1 : Real.exp (-u * t) ≤ Real.exp (-u * s) := by
      refine Real.exp_le_exp.mpr ?_
      have := mul_le_mul_of_nonneg_left hst hu
      linarith
    linarith
  · rw [max_eq_left hRt, sub_self]
    have h1 : Real.exp (-u * max s R) ≤ Real.exp (-u * s) := by
      refine Real.exp_le_exp.mpr ?_
      have := mul_le_mul_of_nonneg_left (le_max_left s R) hu
      linarith
    linarith

/-- Flattening at level `R` lowers the partition sum more for the lower profile:
`A₁ - F₁ ≤ A - F` when `dC ≤ d1` pointwise. -/
theorem pSum_sub_flat_mono {u : ℝ} (hu : 0 ≤ u) (R : ℝ) (dC d1 : X → ℝ)
    (hle : ∀ x, dC x ≤ d1 x) :
    pSum u d1 - pSum u (fun x => max (d1 x) R) ≤
      pSum u dC - pSum u (fun x => max (dC x) R) := by
  unfold pSum
  rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
  exact Finset.sum_le_sum fun x _ => exp_sub_exp_max_antitone hu R (hle x)

/-- Flattening does not increase the partition sum: `F ≤ A`. -/
theorem pSum_flat_le {u : ℝ} (hu : 0 ≤ u) (R : ℝ) (d : X → ℝ) :
    pSum u (fun x => max (d x) R) ≤ pSum u d := by
  unfold pSum
  refine Finset.sum_le_sum fun x _ => Real.exp_le_exp.mpr ?_
  have := mul_le_mul_of_nonneg_left (le_max_left (d x) R) hu
  linarith

/-- **Separation inequality of Theorem 4′, ratio form.**  `dC ≤ d1` pointwise, `u ≥ 0`.  With
`A = ∑ exp (-u dC)`, `F = ∑ exp (-u max (dC, R))`, `A₁ = ∑ exp (-u d1)`,
`F₁ = ∑ exp (-u max (d1, R))`: if `F ≤ m * F₁` then `1 + (A₁ / F₁ - 1) / m ≤ A / F`. -/
theorem separation_ratio [Nonempty X] {u : ℝ} (hu : 0 ≤ u) (R : ℝ) (dC d1 : X → ℝ)
    (hle : ∀ x, dC x ≤ d1 x) {m : ℝ}
    (hF : pSum u (fun x => max (dC x) R) ≤ m * pSum u (fun x => max (d1 x) R)) :
    1 + (pSum u d1 / pSum u (fun x => max (d1 x) R) - 1) / m ≤
      pSum u dC / pSum u (fun x => max (dC x) R) := by
  have hdiff := pSum_sub_flat_mono hu R dC d1 hle
  have hF1A1 := pSum_flat_le hu R d1
  have hFpos : 0 < pSum u (fun x => max (dC x) R) := pSum_pos u _
  have hF1pos : 0 < pSum u (fun x => max (d1 x) R) := pSum_pos u _
  revert hdiff hF1A1 hFpos hF1pos hF
  generalize pSum u dC = A
  generalize pSum u (fun x => max (dC x) R) = F
  generalize pSum u d1 = A1
  generalize pSum u (fun x => max (d1 x) R) = F1
  intro hF hdiff hF1A1 hFpos hF1pos
  have hm : 0 < m := by
    by_contra hneg
    have := mul_nonpos_of_nonpos_of_nonneg (not_lt.mp hneg) hF1pos.le
    linarith
  have hm' := hm.ne'
  have hF1' := hF1pos.ne'
  rw [le_div_iff₀ hFpos]
  have hq : F / (m * F1) ≤ 1 := (div_le_one (mul_pos hm hF1pos)).mpr hF
  have e : (1 + (A1 / F1 - 1) / m) * F = F + (A1 - F1) * (F / (m * F1)) := by
    field_simp
  rw [e]
  have h2 := mul_le_mul_of_nonneg_left hq (sub_nonneg.mpr hF1A1)
  linarith

/-- **Separation inequality of Theorem 4′, logarithmic form.**  If moreover `1 ≤ m`, then
`log (A₁ / F₁) - log m ≤ log A - log F`: symmetrising the cone over `m` translates costs at
most `log m` of the drop `D_R = log (A₁ / F₁)`. -/
theorem separation_log [Nonempty X] {u : ℝ} (hu : 0 ≤ u) (R : ℝ) (dC d1 : X → ℝ)
    (hle : ∀ x, dC x ≤ d1 x) {m : ℝ} (hm : 1 ≤ m)
    (hF : pSum u (fun x => max (dC x) R) ≤ m * pSum u (fun x => max (d1 x) R)) :
    Real.log (pSum u d1 / pSum u (fun x => max (d1 x) R)) - Real.log m ≤
      Real.log (pSum u dC) - Real.log (pSum u (fun x => max (dC x) R)) := by
  have hratio := separation_ratio hu R dC d1 hle hF
  have hF1A1 := pSum_flat_le hu R d1
  have hApos : 0 < pSum u dC := pSum_pos u _
  have hFpos : 0 < pSum u (fun x => max (dC x) R) := pSum_pos u _
  have hA1pos : 0 < pSum u d1 := pSum_pos u _
  have hF1pos : 0 < pSum u (fun x => max (d1 x) R) := pSum_pos u _
  have hm0 : 0 < m := by linarith
  have hρpos : 0 < pSum u d1 / pSum u (fun x => max (d1 x) R) := div_pos hA1pos hF1pos
  have hρ : 1 ≤ pSum u d1 / pSum u (fun x => max (d1 x) R) := (one_le_div hF1pos).mpr hF1A1
  have h1 : pSum u d1 / pSum u (fun x => max (d1 x) R) / m ≤
      1 + (pSum u d1 / pSum u (fun x => max (d1 x) R) - 1) / m := by
    have hinv : 1 / m ≤ 1 := (div_le_one hm0).mpr hm
    have e : 1 + (pSum u d1 / pSum u (fun x => max (d1 x) R) - 1) / m -
        pSum u d1 / pSum u (fun x => max (d1 x) R) / m = 1 - 1 / m := by ring
    linarith
  have h3 : Real.log (pSum u d1 / pSum u (fun x => max (d1 x) R) / m) ≤
      Real.log (pSum u dC / pSum u (fun x => max (dC x) R)) :=
    Real.log_le_log (div_pos hρpos hm0) (h1.trans hratio)
  rw [Real.log_div hρpos.ne' hm0.ne', Real.log_div hApos.ne' hFpos.ne'] at h3
  exact h3

end Abstract

/-! ### The concrete case: Hamming distance to a translated set -/

section Hamming

variable {ι G : Type*} [Fintype ι] [DecidableEq ι] [AddCommGroup G] [Fintype G] [DecidableEq G]

omit [DecidableEq ι] [Fintype G] in
/-- The Hamming distance is translation invariant. -/
theorem hammingDist_add_right_cancel (x y a : ι → G) :
    hammingDist (x + a) (y + a) = hammingDist x y := by
  rw [hammingDist_eq_hammingNorm, hammingDist_eq_hammingNorm]
  congr 1
  abel

/-- `d_C(x) = d_H(x, s + C) = min_{a ∈ C} d_H(x, s + a)`: the Hamming distance from `x` to the
translate `s + C` of a non-empty finite set `C`, as a real number. -/
def distToCoset (C : Finset (ι → G)) (hC : C.Nonempty) (s x : ι → G) : ℝ :=
  C.inf' hC fun a => (hammingDist x (s + a) : ℝ)

omit [DecidableEq ι] [Fintype G] in
/-- `d_C ≤ d_H(·, s)` when `0 ∈ C`. -/
theorem distToCoset_le (C : Finset (ι → G)) (hC : C.Nonempty) (h0 : (0 : ι → G) ∈ C)
    (s x : ι → G) : distToCoset C hC s x ≤ (hammingDist x s : ℝ) := by
  unfold distToCoset
  refine (Finset.inf'_le (fun a => (hammingDist x (s + a) : ℝ)) h0).trans (le_of_eq ?_)
  simp

/-- **`F ≤ |C| · F₁`.**  The flattened symmetrised cone has partition sum at most `|C|` times
that of the flattened cone: `exp (-u max (d_C, R)) = max_a exp (-u max (d_H(·, s + a), R))` is
at most the sum over `a ∈ C`, and each translate has the same partition sum.  No sign
condition on `u`, no structure on `C`. -/
theorem pSum_flat_distToCoset_le (C : Finset (ι → G)) (hC : C.Nonempty) (s : ι → G)
    (u R : ℝ) :
    pSum u (fun x => max (distToCoset C hC s x) R) ≤
      C.card * pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R) := by
  have hshift : ∀ a : ι → G,
      ∑ x : ι → G, Real.exp (-u * max (hammingDist x (s + a) : ℝ) R) =
        pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R) := by
    intro a
    unfold pSum
    symm
    refine Fintype.sum_equiv (Equiv.addRight a) _ _ fun x => ?_
    show Real.exp (-u * max (hammingDist x s : ℝ) R) =
      Real.exp (-u * max (hammingDist (x + a) (s + a) : ℝ) R)
    rw [hammingDist_add_right_cancel]
  have hpt : ∀ x : ι → G, Real.exp (-u * max (distToCoset C hC s x) R) ≤
      ∑ a ∈ C, Real.exp (-u * max (hammingDist x (s + a) : ℝ) R) := by
    intro x
    obtain ⟨a, haC, ha⟩ := Finset.exists_mem_eq_inf' hC fun a => (hammingDist x (s + a) : ℝ)
    have e : distToCoset C hC s x = (hammingDist x (s + a) : ℝ) := ha
    rw [e]
    exact Finset.single_le_sum
      (f := fun a => Real.exp (-u * max (hammingDist x (s + a) : ℝ) R))
      (fun b _ => (Real.exp_pos _).le) haC
  calc pSum u (fun x => max (distToCoset C hC s x) R)
      = ∑ x : ι → G, Real.exp (-u * max (distToCoset C hC s x) R) := rfl
    _ ≤ ∑ x : ι → G, ∑ a ∈ C, Real.exp (-u * max (hammingDist x (s + a) : ℝ) R) :=
        Finset.sum_le_sum fun x _ => hpt x
    _ = ∑ a ∈ C, ∑ x : ι → G, Real.exp (-u * max (hammingDist x (s + a) : ℝ) R) :=
        Finset.sum_comm
    _ = ∑ _a ∈ C, pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R) :=
        Finset.sum_congr rfl fun a _ => hshift a
    _ = C.card * pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R) := by
        rw [Finset.sum_const, nsmul_eq_mul]

/-- **Theorem 4′, the separation step.**  `C` a finite set of translations containing `0`,
`s` a centre, `u ≥ 0`, any level `R`.  With `d_C = d_H(·, s + C)`:
`log (A₁ / F₁) - log |C| ≤ log Z(cone^C_s) - log Z(flat^C_s)`,
where `log (A₁ / F₁) = D_R` is the drop for the unsymmetrised cone. -/
theorem separation_distToCoset (C : Finset (ι → G)) (hC : C.Nonempty)
    (h0 : (0 : ι → G) ∈ C) (s : ι → G) {u : ℝ} (hu : 0 ≤ u) (R : ℝ) :
    Real.log (pSum u (fun x : ι → G => (hammingDist x s : ℝ)) /
        pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R)) - Real.log C.card ≤
      Real.log (pSum u (distToCoset C hC s)) -
        Real.log (pSum u (fun x => max (distToCoset C hC s x) R)) := by
  have hcard : (1 : ℝ) ≤ C.card := by exact_mod_cast Finset.card_pos.mpr hC
  exact separation_log hu R (distToCoset C hC s) (fun x => (hammingDist x s : ℝ))
    (distToCoset_le C hC h0 s) hcard (pSum_flat_distToCoset_le C hC s u R)

/-- The sensitivity hypothesis of the non-adaptive packing bound for the symmetrised pair:
if `ε < D_R - log |C|` then `ε < log Z(cone^C_s) - log Z(flat^C_s)`. -/
theorem sensitivity_distToCoset (C : Finset (ι → G)) (hC : C.Nonempty)
    (h0 : (0 : ι → G) ∈ C) (s : ι → G) {u : ℝ} (hu : 0 ≤ u) (R : ℝ) {ε : ℝ}
    (hε : ε < Real.log (pSum u (fun x : ι → G => (hammingDist x s : ℝ)) /
        pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R)) - Real.log C.card) :
    ε < Real.log (pSum u (distToCoset C hC s)) -
        Real.log (pSum u (fun x => max (distToCoset C hC s x) R)) :=
  lt_of_lt_of_le hε (separation_distToCoset C hC h0 s hu R)

end Hamming

/-! ### Non-vacuity

The hypotheses of `separation_distToCoset` are satisfiable for a non-trivial code: the
repetition code `{00, 11}` in `Fin 2 → ZMod 2`. -/

example : ∃ (C : Finset (Fin 2 → ZMod 2)) (_ : C.Nonempty), (0 : Fin 2 → ZMod 2) ∈ C ∧
    C.card = 2 :=
  ⟨{0, fun _ => 1}, ⟨0, by simp⟩, by simp, by
    rw [Finset.card_pair]
    intro h
    have := congrFun h 0
    revert this
    decide⟩

end ScienceL1

end

#print axioms ScienceL1.exp_sub_exp_max_antitone
#print axioms ScienceL1.pSum_sub_flat_mono
#print axioms ScienceL1.separation_ratio
#print axioms ScienceL1.separation_log
#print axioms ScienceL1.pSum_flat_distToCoset_le
#print axioms ScienceL1.separation_distToCoset
#print axioms ScienceL1.sensitivity_distToCoset
