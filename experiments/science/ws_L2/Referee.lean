import Mathlib

/-!
# Three finite statements of the referee (R3 report, section 4): R6.1, R5(2), R6.2

Science division, workstream L2.  Source: `docs/science/workstreams/R3_REPORT.md`, section 4.

## R6.1 (excess identity) — `Excess` section

Any finite type `X`, any two real functions `g₀, T`; `g′ = min (g₀, T)`; `Z_g = ∑ e^{-g}`,
`U_g = ∑ g e^{-g} / Z_g`; `E = ∑ (e^{-T} - e^{-g₀})₊`, `D = ∑_{T < g₀} (T e^{-T} - g₀ e^{-g₀})`.

* `partSum_twinMin` — `Z′ = Z₀ + E`;
* `enSum_twinMin` — `∑ g′ e^{-g′} = ∑ g₀ e^{-g₀} + D`;
* `meanEn_twinMin_sub` — `U′ - U₀ = (D - U₀ E) / (Z₀ + E)` (no condition on `E`);
* `excess_identity` — `U′ - U₀ = (E / (Z₀ + E)) (D / E - U₀)` for `E ≠ 0` (the referee's form);
* `excessMass_eq_zero_iff`, `twinMin_eq_of_excessMass_eq_zero` — `E = 0` iff `g₀ ≤ T`
  everywhere, and then `g′ = g₀`;
* `meanEn_twinMin_eq_iff` — for `E ≠ 0`: `U′ = U₀ ↔ D / E = U₀` ("the twin leaves the mean
  energy unchanged iff the mean energy of its excess mass equals `U₀`").

## R5(2) (symmetrised cones) — `Centres` section

Abstract form: a finite type `X`, a non-empty finite set `C` of centres, profiles
`dist c : X → ℝ` (in the report: `dist c x = d_H(x, a + c)`), `distTo = min_{c ∈ C} dist c`.

* `sum_sub_pair_min_le_sup'` — a maximum of non-negative terms is at least their sum minus the
  sum of the pairwise minima (ordered pairs of distinct indices, factor `1/2`);
  `sum_offDiag_eq_two_mul_sum_lt` — the same double sum as twice the sum over pairs `i < j`;
  `sum_sub_pair_min_lt_le_sup'` — the statement with pairs `i < j`;
  `sum_sub_pair_min_needs_nonneg` — it fails for the family `(0, 0, -1)`;
* `sum_apply_distTo_le` — `∑_x φ (distTo x) ≤ ∑_{c ∈ C} ∑_x φ (dist c x)` for `φ ≥ 0`; in
  particular `flat_distTo_le` — `Z(flat^C) ≤ ∑_c Z(flat_c)` (`= |C| Z(flat)` by translation);
* `cone_distTo_ge` — `Z(cone^C) ≥ ∑_c Z(cone_c) - ½ ∑_{c ≠ c′} ∑_x e^{-u (dist c x + dist c′ x)/2}`
  for `u ≥ 0`;
* `r5_2_abstract` — hence, if every single cone has partition sum `A₁`, every single flattened
  cone `F₁`, every pair sum is at most `κ A₁`, and `γ = ½ (|C| - 1) κ < 1`, then
  `log Z(cone^C) - log Z(flat^C) ≥ log A₁ - log F₁ + log (1 - γ)`.

## R6.2 (signs at the ends) — `Signs` section

See the section header.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL2

open Finset

/-! ### R6.1 — the excess identity -/

section Excess

variable {X : Type*} [Fintype X]

/-- `Z_g = ∑ exp (-g)` (units `β = 1`). -/
def partSum (g : X → ℝ) : ℝ := ∑ x, Real.exp (-g x)

/-- `∑ g exp (-g)`, the numerator of the mean energy. -/
def enSum (g : X → ℝ) : ℝ := ∑ x, g x * Real.exp (-g x)

/-- `U_g = E_{μ_g} g`, the mean energy of `g` in its own Gibbs measure. -/
def meanEn (g : X → ℝ) : ℝ := enSum g / partSum g

/-- The twin instance `g′ = min (g₀, T)`. -/
def twinMin (g₀ T : X → ℝ) (x : X) : ℝ := min (g₀ x) (T x)

/-- `E = ∑ (e^{-T} - e^{-g₀})₊`, the excess mass of the twin. -/
def excessMass (g₀ T : X → ℝ) : ℝ := ∑ x, max (Real.exp (-T x) - Real.exp (-g₀ x)) 0

/-- `D = ∑_{T < g₀} (T e^{-T} - g₀ e^{-g₀})`, the excess energy of the twin. -/
def excessEnergy (g₀ T : X → ℝ) : ℝ :=
  ∑ x, if T x < g₀ x then T x * Real.exp (-T x) - g₀ x * Real.exp (-g₀ x) else 0

theorem partSum_pos [Nonempty X] (g : X → ℝ) : 0 < partSum g :=
  Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty

theorem excessMass_nonneg (g₀ T : X → ℝ) : 0 ≤ excessMass g₀ T :=
  Finset.sum_nonneg (fun _ _ => le_max_right _ _)

/-- **R6.1, first identity**: `Z′ = Z₀ + E`. -/
theorem partSum_twinMin (g₀ T : X → ℝ) :
    partSum (twinMin g₀ T) = partSum g₀ + excessMass g₀ T := by
  unfold partSum excessMass twinMin
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun x _ => ?_)
  rcases le_or_gt (g₀ x) (T x) with h | h
  · have h' : Real.exp (-T x) ≤ Real.exp (-g₀ x) := Real.exp_le_exp.2 (by linarith)
    rw [min_eq_left h, max_eq_right (by linarith)]
    ring
  · have h' : Real.exp (-g₀ x) < Real.exp (-T x) := Real.exp_lt_exp.2 (by linarith)
    rw [min_eq_right h.le, max_eq_left (by linarith)]
    ring

/-- **R6.1, numerator**: `∑ g′ e^{-g′} = ∑ g₀ e^{-g₀} + D`. -/
theorem enSum_twinMin (g₀ T : X → ℝ) :
    enSum (twinMin g₀ T) = enSum g₀ + excessEnergy g₀ T := by
  unfold enSum excessEnergy twinMin
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun x _ => ?_)
  rcases le_or_gt (g₀ x) (T x) with h | h
  · rw [min_eq_left h, if_neg (not_lt.2 h)]
    ring
  · rw [min_eq_right h.le, if_pos h]
    ring

/-- **R6.1, division-free form**: `U′ - U₀ = (D - U₀ E) / (Z₀ + E)`; no condition on `E`. -/
theorem meanEn_twinMin_sub [Nonempty X] (g₀ T : X → ℝ) :
    meanEn (twinMin g₀ T) - meanEn g₀ =
      (excessEnergy g₀ T - meanEn g₀ * excessMass g₀ T) / (partSum g₀ + excessMass g₀ T) := by
  have hZ := partSum_pos g₀
  have hE := excessMass_nonneg g₀ T
  have hZE : 0 < partSum g₀ + excessMass g₀ T := by linarith
  unfold meanEn
  rw [partSum_twinMin, enSum_twinMin]
  field_simp
  ring

/-- **Lemma R6.1 (excess identity)** in the referee's form:
`U′ - U₀ = (E / (Z₀ + E)) * (D / E - U₀)`, for `E ≠ 0`. -/
theorem excess_identity [Nonempty X] (g₀ T : X → ℝ) (hE : excessMass g₀ T ≠ 0) :
    meanEn (twinMin g₀ T) - meanEn g₀ =
      excessMass g₀ T / (partSum g₀ + excessMass g₀ T) *
        (excessEnergy g₀ T / excessMass g₀ T - meanEn g₀) := by
  rw [meanEn_twinMin_sub]
  have hZ := partSum_pos g₀
  have hE0 := excessMass_nonneg g₀ T
  have hZE : partSum g₀ + excessMass g₀ T ≠ 0 := by
    have : 0 < partSum g₀ + excessMass g₀ T := by linarith
    exact this.ne'
  field_simp

/-- `E = 0` iff the twin is nowhere below `g₀`. -/
theorem excessMass_eq_zero_iff (g₀ T : X → ℝ) : excessMass g₀ T = 0 ↔ ∀ x, g₀ x ≤ T x := by
  unfold excessMass
  rw [Finset.sum_eq_zero_iff_of_nonneg (fun _ _ => le_max_right _ _)]
  constructor
  · intro h x
    have hx := h x (Finset.mem_univ x)
    have h1 : Real.exp (-T x) - Real.exp (-g₀ x) ≤ 0 := by
      have := le_max_left (Real.exp (-T x) - Real.exp (-g₀ x)) 0
      linarith
    have h2 : Real.exp (-T x) ≤ Real.exp (-g₀ x) := by linarith
    have h3 := Real.exp_le_exp.1 h2
    linarith
  · intro h x _
    have h2 : Real.exp (-T x) ≤ Real.exp (-g₀ x) := Real.exp_le_exp.2 (by linarith [h x])
    exact max_eq_right (by linarith)

/-- If `E = 0` the twin is `g₀` itself (so `U′ = U₀`, `Z′ = Z₀`, and the referee's formula, which
divides by `E`, is not needed). -/
theorem twinMin_eq_of_excessMass_eq_zero (g₀ T : X → ℝ) (hE : excessMass g₀ T = 0) :
    twinMin g₀ T = g₀ := by
  funext x
  exact min_eq_left ((excessMass_eq_zero_iff g₀ T).1 hE x)

/-- **R6.1, the reading**: for `E ≠ 0`, the twin leaves the mean energy unchanged iff the mean
energy of its excess mass equals `U₀`. -/
theorem meanEn_twinMin_eq_iff [Nonempty X] (g₀ T : X → ℝ) (hE : excessMass g₀ T ≠ 0) :
    meanEn (twinMin g₀ T) = meanEn g₀ ↔ excessEnergy g₀ T / excessMass g₀ T = meanEn g₀ := by
  have hZ := partSum_pos g₀
  have hE0 := excessMass_nonneg g₀ T
  have hEpos : 0 < excessMass g₀ T := lt_of_le_of_ne hE0 (Ne.symm hE)
  have hZE : 0 < partSum g₀ + excessMass g₀ T := by linarith
  have key := excess_identity g₀ T hE
  have hfac : 0 < excessMass g₀ T / (partSum g₀ + excessMass g₀ T) := div_pos hEpos hZE
  constructor
  · intro h
    rw [h, sub_self] at key
    have := (mul_eq_zero.1 key.symm).resolve_left hfac.ne'
    linarith
  · intro h
    rw [h, sub_self, mul_zero] at key
    linarith

end Excess

/-! ### R5(2) — the two inequalities for symmetrised cones -/

section Centres

variable {ι : Type*}

/-- **A maximum of non-negative terms is at least their sum minus the sum of the pairwise
minima.**  The pairs are ordered pairs of distinct indices, hence the factor `1/2`. -/
theorem sum_sub_pair_min_le_sup' [DecidableEq ι] (s : Finset ι) (hs : s.Nonempty) (a : ι → ℝ)
    (ha : ∀ i ∈ s, 0 ≤ a i) :
    ∑ i ∈ s, a i - (1 / 2) * ∑ i ∈ s, ∑ j ∈ s.erase i, min (a i) (a j) ≤ s.sup' hs a := by
  obtain ⟨m, hm, hmax⟩ := Finset.exists_max_image s a hs
  have hsup : a m ≤ s.sup' hs a := Finset.le_sup' a hm
  have hFm : ∑ j ∈ s.erase m, min (a m) (a j) = ∑ j ∈ s.erase m, a j := by
    refine Finset.sum_congr rfl (fun j hj => ?_)
    exact min_eq_right (hmax j (Finset.mem_of_mem_erase hj))
  have hFi : ∀ i ∈ s.erase m, a i ≤ ∑ j ∈ s.erase i, min (a i) (a j) := by
    intro i hi
    have him : i ≠ m := Finset.ne_of_mem_erase hi
    have his : i ∈ s := Finset.mem_of_mem_erase hi
    have hmem : m ∈ s.erase i := Finset.mem_erase.2 ⟨Ne.symm him, hm⟩
    calc a i = min (a i) (a m) := (min_eq_left (hmax i his)).symm
      _ ≤ ∑ j ∈ s.erase i, min (a i) (a j) :=
          Finset.single_le_sum (f := fun j => min (a i) (a j))
            (fun j hj => le_min (ha i his) (ha j (Finset.mem_of_mem_erase hj))) hmem
  have hsplit : ∑ i ∈ s, ∑ j ∈ s.erase i, min (a i) (a j) =
      ∑ j ∈ s.erase m, min (a m) (a j) +
        ∑ i ∈ s.erase m, ∑ j ∈ s.erase i, min (a i) (a j) :=
    (Finset.add_sum_erase s (fun i => ∑ j ∈ s.erase i, min (a i) (a j)) hm).symm
  have hsum : ∑ i ∈ s, a i = a m + ∑ i ∈ s.erase m, a i := (Finset.add_sum_erase s a hm).symm
  have hge : ∑ i ∈ s.erase m, a i ≤ ∑ i ∈ s.erase m, ∑ j ∈ s.erase i, min (a i) (a j) :=
    Finset.sum_le_sum hFi
  rw [hsplit, hFm, hsum]
  linarith

variable {X : Type*} [Fintype X]

/-- The profile "distance to the nearest centre": `distTo x = min_{c ∈ C} dist c x`. -/
def distTo (C : Finset ι) (hC : C.Nonempty) (dist : ι → X → ℝ) (x : X) : ℝ :=
  C.inf' hC (fun c => dist c x)

/-- For any `φ ≥ 0`: `∑_x φ (distTo x) ≤ ∑_{c ∈ C} ∑_x φ (dist c x)`. -/
theorem sum_apply_distTo_le (C : Finset ι) (hC : C.Nonempty) (dist : ι → X → ℝ) (φ : ℝ → ℝ)
    (hφ : ∀ t, 0 ≤ φ t) :
    ∑ x, φ (distTo C hC dist x) ≤ ∑ c ∈ C, ∑ x, φ (dist c x) := by
  rw [Finset.sum_comm]
  refine Finset.sum_le_sum (fun x _ => ?_)
  obtain ⟨c, hc, hEq⟩ := Finset.exists_mem_eq_inf' hC (fun c => dist c x)
  unfold distTo
  rw [hEq]
  exact Finset.single_le_sum (f := fun c => φ (dist c x)) (fun c _ => hφ _) hc

/-- **`Z(flat^C) ≤ ∑_{c ∈ C} Z(flat_c)`** (any real `u`, any real `R`).  When all the
`Z(flat_c)` are equal (translates of one cone) the right-hand side is `|C| Z(flat)`. -/
theorem flat_distTo_le (C : Finset ι) (hC : C.Nonempty) (dist : ι → X → ℝ) (u R : ℝ) :
    ∑ x, Real.exp (-u * max (distTo C hC dist x) R) ≤
      ∑ c ∈ C, ∑ x, Real.exp (-u * max (dist c x) R) :=
  sum_apply_distTo_le C hC dist (fun t => Real.exp (-u * max t R)) (fun _ => (Real.exp_pos _).le)

/-- `Z(flat^C) ≤ |C| Z(flat)` when every centre has the same flattened partition sum `F₁`. -/
theorem flat_distTo_le_card_mul (C : Finset ι) (hC : C.Nonempty) (dist : ι → X → ℝ) (u R : ℝ)
    {F₁ : ℝ} (hF : ∀ c ∈ C, ∑ x, Real.exp (-u * max (dist c x) R) = F₁) :
    ∑ x, Real.exp (-u * max (distTo C hC dist x) R) ≤ C.card * F₁ := by
  have h := flat_distTo_le C hC dist u R
  rw [Finset.sum_congr rfl hF, Finset.sum_const, nsmul_eq_mul] at h
  exact h

theorem min_exp_le_exp_half (p q : ℝ) : min (Real.exp p) (Real.exp q) ≤ Real.exp ((p + q) / 2) := by
  rcases le_total p q with h | h
  · exact le_trans (min_le_left _ _) (Real.exp_le_exp.2 (by linarith))
  · exact le_trans (min_le_right _ _) (Real.exp_le_exp.2 (by linarith))

/-- **`Z(cone^C) ≥ ∑_c Z(cone_c) - ½ ∑_{c ≠ c′} ∑_x e^{-u (dist c x + dist c′ x)/2}`** for
`u ≥ 0` (maximum ≥ sum − pairwise minima, and `min (p, q) ≤ √(p q)`). -/
theorem cone_distTo_ge [DecidableEq ι] (C : Finset ι) (hC : C.Nonempty) (dist : ι → X → ℝ)
    {u : ℝ} (hu : 0 ≤ u) :
    ∑ c ∈ C, ∑ x, Real.exp (-u * dist c x) -
        (1 / 2) * ∑ c ∈ C, ∑ c' ∈ C.erase c, ∑ x, Real.exp (-u * (dist c x + dist c' x) / 2) ≤
      ∑ x, Real.exp (-u * distTo C hC dist x) := by
  have hpt : ∀ x, ∑ c ∈ C, Real.exp (-u * dist c x) -
      (1 / 2) * ∑ c ∈ C, ∑ c' ∈ C.erase c, Real.exp (-u * (dist c x + dist c' x) / 2) ≤
        Real.exp (-u * distTo C hC dist x) := by
    intro x
    have h1 := sum_sub_pair_min_le_sup' C hC (fun c => Real.exp (-u * dist c x))
      (fun c _ => (Real.exp_pos _).le)
    have h2 : C.sup' hC (fun c => Real.exp (-u * dist c x)) ≤
        Real.exp (-u * distTo C hC dist x) := by
      refine Finset.sup'_le hC _ (fun c hc => ?_)
      have hle : distTo C hC dist x ≤ dist c x := Finset.inf'_le (fun c => dist c x) hc
      exact Real.exp_le_exp.2 (by nlinarith)
    have h3 : ∑ c ∈ C, ∑ c' ∈ C.erase c,
          min (Real.exp (-u * dist c x)) (Real.exp (-u * dist c' x)) ≤
        ∑ c ∈ C, ∑ c' ∈ C.erase c, Real.exp (-u * (dist c x + dist c' x) / 2) := by
      refine Finset.sum_le_sum (fun c _ => Finset.sum_le_sum (fun c' _ => ?_))
      have := min_exp_le_exp_half (-u * dist c x) (-u * dist c' x)
      have e : (-u * dist c x + -u * dist c' x) / 2 = -u * (dist c x + dist c' x) / 2 := by ring
      rwa [e] at this
    linarith
  have hsum := Finset.sum_le_sum (fun x (_ : x ∈ Finset.univ) => hpt x)
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum] at hsum
  have e1 : ∑ x, ∑ c ∈ C, Real.exp (-u * dist c x) = ∑ c ∈ C, ∑ x, Real.exp (-u * dist c x) :=
    Finset.sum_comm
  have e2 : ∑ x, ∑ c ∈ C, ∑ c' ∈ C.erase c, Real.exp (-u * (dist c x + dist c' x) / 2) =
      ∑ c ∈ C, ∑ c' ∈ C.erase c, ∑ x, Real.exp (-u * (dist c x + dist c' x) / 2) := by
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl (fun c _ => ?_)
    rw [Finset.sum_comm]
  rw [e1, e2] at hsum
  exact hsum

/-- **R5(2), abstract form.**  If every single cone has partition sum `A₁`, every single
flattened cone has partition sum `F₁`, every pair of distinct centres has
`∑_x e^{-u (dist c x + dist c′ x)/2} ≤ κ A₁` (on the cube: `κ = cosh(u/2)^{-d_min}`), and
`γ = ½ (|C| - 1) κ < 1`, then
`log Z(cone^C) - log Z(flat^C) ≥ log A₁ - log F₁ + log (1 - γ)`. -/
theorem r5_2_abstract [DecidableEq ι] [Nonempty X] (C : Finset ι) (hC : C.Nonempty)
    (dist : ι → X → ℝ) {u : ℝ} (hu : 0 ≤ u) (R : ℝ) {A₁ F₁ κ : ℝ}
    (hA : ∀ c ∈ C, ∑ x, Real.exp (-u * dist c x) = A₁)
    (hF : ∀ c ∈ C, ∑ x, Real.exp (-u * max (dist c x) R) = F₁)
    (hpair : ∀ c ∈ C, ∀ c' ∈ C, c ≠ c' →
      ∑ x, Real.exp (-u * (dist c x + dist c' x) / 2) ≤ κ * A₁)
    (hγ : (1 / 2) * ((C.card : ℝ) - 1) * κ < 1) :
    Real.log A₁ - Real.log F₁ + Real.log (1 - (1 / 2) * ((C.card : ℝ) - 1) * κ) ≤
      Real.log (∑ x, Real.exp (-u * distTo C hC dist x)) -
        Real.log (∑ x, Real.exp (-u * max (distTo C hC dist x) R)) := by
  obtain ⟨c₀, hc₀⟩ := hC
  have hCne : C.Nonempty := ⟨c₀, hc₀⟩
  have hcard : (0 : ℝ) < C.card := by exact_mod_cast Finset.card_pos.2 hCne
  have hA₁ : 0 < A₁ := by
    rw [← hA c₀ hc₀]
    exact Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty
  have hF₁ : 0 < F₁ := by
    rw [← hF c₀ hc₀]
    exact Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty
  have hflat := flat_distTo_le_card_mul C hCne dist u R hF
  have hcone := cone_distTo_ge C hCne dist hu
  rw [Finset.sum_congr rfl hA, Finset.sum_const, nsmul_eq_mul] at hcone
  have hpairs : ∑ c ∈ C, ∑ c' ∈ C.erase c, ∑ x, Real.exp (-u * (dist c x + dist c' x) / 2) ≤
      C.card * (((C.card : ℝ) - 1) * (κ * A₁)) := by
    have h1 : ∀ c ∈ C, ∑ c' ∈ C.erase c, ∑ x, Real.exp (-u * (dist c x + dist c' x) / 2) ≤
        ((C.card : ℝ) - 1) * (κ * A₁) := by
      intro c hc
      have h2 : ∑ c' ∈ C.erase c, ∑ x, Real.exp (-u * (dist c x + dist c' x) / 2) ≤
          ∑ _c' ∈ C.erase c, κ * A₁ :=
        Finset.sum_le_sum (fun c' hc' => hpair c hc c' (Finset.mem_of_mem_erase hc')
          (Ne.symm (Finset.ne_of_mem_erase hc')))
      rw [Finset.sum_const, nsmul_eq_mul, Finset.card_erase_of_mem hc,
        Nat.cast_sub (Finset.card_pos.2 ⟨c, hc⟩), Nat.cast_one] at h2
      exact h2
    have h3 := Finset.sum_le_sum h1
    rw [Finset.sum_const, nsmul_eq_mul] at h3
    exact h3
  have hZc : C.card * A₁ * (1 - (1 / 2) * ((C.card : ℝ) - 1) * κ) ≤
      ∑ x, Real.exp (-u * distTo C hCne dist x) := by
    nlinarith
  have hZf_pos : 0 < ∑ x, Real.exp (-u * max (distTo C hCne dist x) R) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty
  have hγ' : 0 < 1 - (1 / 2) * ((C.card : ℝ) - 1) * κ := by linarith
  have hlow_pos : 0 < C.card * A₁ * (1 - (1 / 2) * ((C.card : ℝ) - 1) * κ) :=
    mul_pos (mul_pos hcard hA₁) hγ'
  have hlog1 := Real.log_le_log hlow_pos hZc
  have hlog2 := Real.log_le_log hZf_pos hflat
  rw [Real.log_mul (mul_pos hcard hA₁).ne' hγ'.ne', Real.log_mul hcard.ne' hA₁.ne'] at hlog1
  rw [Real.log_mul hcard.ne' hF₁.ne'] at hlog2
  linarith

end Centres

end ScienceL2

end

#print axioms ScienceL2.partSum_twinMin
#print axioms ScienceL2.enSum_twinMin
#print axioms ScienceL2.meanEn_twinMin_sub
#print axioms ScienceL2.excess_identity
#print axioms ScienceL2.excessMass_eq_zero_iff
#print axioms ScienceL2.twinMin_eq_of_excessMass_eq_zero
#print axioms ScienceL2.meanEn_twinMin_eq_iff
#print axioms ScienceL2.sum_sub_pair_min_le_sup'
#print axioms ScienceL2.sum_apply_distTo_le
#print axioms ScienceL2.flat_distTo_le
#print axioms ScienceL2.flat_distTo_le_card_mul
#print axioms ScienceL2.cone_distTo_ge
#print axioms ScienceL2.r5_2_abstract
