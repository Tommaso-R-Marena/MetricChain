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

/-- For a symmetric `f`, the sum over ordered pairs of distinct indices is twice the sum over
pairs `i < j`. -/
theorem sum_offDiag_eq_two_mul_sum_lt [LinearOrder ι] (s : Finset ι) (f : ι → ι → ℝ)
    (hf : ∀ i j, f i j = f j i) :
    ∑ i ∈ s, ∑ j ∈ s.erase i, f i j = 2 * ∑ i ∈ s, ∑ j ∈ s with i < j, f i j := by
  have hsplit : ∀ i ∈ s, ∑ j ∈ s.erase i, f i j =
      ∑ j ∈ s with i < j, f i j + ∑ j ∈ s with j < i, f i j := by
    intro i _
    rw [← Finset.sum_union]
    · refine Finset.sum_congr ?_ (fun _ _ => rfl)
      ext j
      simp only [Finset.mem_erase, Finset.mem_union, Finset.mem_filter]
      constructor
      · rintro ⟨hne, hj⟩
        rcases lt_or_gt_of_ne hne with h | h
        · exact Or.inr ⟨hj, h⟩
        · exact Or.inl ⟨hj, h⟩
      · rintro (⟨hj, h⟩ | ⟨hj, h⟩)
        · exact ⟨h.ne', hj⟩
        · exact ⟨h.ne, hj⟩
    · rw [Finset.disjoint_left]
      intro j h1 h2
      exact lt_asymm (Finset.mem_filter.1 h1).2 (Finset.mem_filter.1 h2).2
  rw [Finset.sum_congr rfl hsplit, Finset.sum_add_distrib]
  have hswap : ∑ i ∈ s, ∑ j ∈ s with j < i, f i j = ∑ i ∈ s, ∑ j ∈ s with i < j, f i j := by
    rw [Finset.sum_comm' (s' := fun j => s.filter (fun i => j < i)) (t' := s)]
    · refine Finset.sum_congr rfl (fun j _ => Finset.sum_congr rfl (fun i _ => hf i j))
    · intro i j
      simp only [Finset.mem_filter]
      tauto
  rw [hswap]
  ring

/-- **A maximum of non-negative terms is at least their sum minus the sum of the pairwise
minima**, with the pairs written as `i < j` (the referee's `∑_{a′ < a″}`). -/
theorem sum_sub_pair_min_lt_le_sup' [LinearOrder ι] (s : Finset ι) (hs : s.Nonempty)
    (a : ι → ℝ) (ha : ∀ i ∈ s, 0 ≤ a i) :
    ∑ i ∈ s, a i - ∑ i ∈ s, ∑ j ∈ s with i < j, min (a i) (a j) ≤ s.sup' hs a := by
  have h := sum_sub_pair_min_le_sup' s hs a ha
  rw [sum_offDiag_eq_two_mul_sum_lt s (fun i j => min (a i) (a j)) (fun i j => min_comm _ _)] at h
  linarith

/-- Non-negativity is needed for three or more terms: for the family `(0, 0, -1)` the maximum is
`0` and the sum minus the pairwise minima is `1`. -/
theorem sum_sub_pair_min_needs_nonneg :
    ¬ (∑ i : Fin 3, (![0, 0, -1] : Fin 3 → ℝ) i -
        ∑ i : Fin 3, ∑ j ∈ (Finset.univ : Finset (Fin 3)) with i < j,
          min ((![0, 0, -1] : Fin 3 → ℝ) i) ((![0, 0, -1] : Fin 3 → ℝ) j) ≤
      (Finset.univ : Finset (Fin 3)).sup' Finset.univ_nonempty (![0, 0, -1] : Fin 3 → ℝ)) := by
  intro h
  have h0 : (Finset.univ.filter (fun j : Fin 3 => (0 : Fin 3) < j)) = {1, 2} := by decide
  have h1 : (Finset.univ.filter (fun j : Fin 3 => (1 : Fin 3) < j)) = {2} := by decide
  have h2 : (Finset.univ.filter (fun j : Fin 3 => (2 : Fin 3) < j)) = ∅ := by decide
  rw [Fin.sum_univ_three, Fin.sum_univ_three, h0, h1, h2] at h
  simp at h
  obtain ⟨b, hb⟩ := h
  fin_cases b <;> norm_num at hb

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

/-! ### R6.2 — signs at the ends

Abstract setting.  `X` a finite non-empty type; `d₀ d' : X → ℕ` two "distance profiles" (on the
cube: the Hamming distances to the centres `a₀` and `a′`; for Corollary R6′: the distances to two
cosets) that are *equidistributed through a bijection* `σ : X ≃ X`, `d' (σ x) = d₀ x` (on the
cube: the translation by `a′ - a₀`).  Units `β = 1`, `c = u > 0`.  For a real level `ρ`,
`basin u ρ d x = -u (ρ - d x)₊`; the visible basin is `g₀ = basin u r₁ d₀`, the twin is
`T_s = basin u (r₁ + s) d'`, and `g′_s = min (g₀, T_s) = twinMin g₀ T_s`.

Quantities of the report: `W = basinW u r₁ d₀ = ∑_{d₀ < r₁} e^{u (r₁ - d₀)}`,
`V = basinV r₁ d₀ = #{d₀ < r₁}`, `A′ = basinA u r₁ d₀`, `2ⁿ` is `Fintype.card X`,
`ω_s = overlapW g₀ T_s = ∑_{g₀ < 0, T_s < 0} e^{-T_s}`.

* layer A (any `g₀ ≤ 0`, `T ≤ 0`): `excessMass_le_freeMass`, `freeMass_sub_overlapW_le`,
  `enSum_le_excessEnergy`, `excessEnergy_le` — "on the overlap each true summand lies between
  `0` and the free one";
* layer B: `partSum_basin`, `enSum_basin`, `freeMass_basin_succ`, `enSum_basin_succ`,
  `freeMass_basin_pred`, `enSum_basin_pred` — the free sums at `s = ±1` in terms of `W, V, A′`;
* layer C (real arithmetic): `sign_plus_arith`, `sign_minus_arith`, `gain_arith`;
* `r6_2_signs` — **Lemma R6.2, the two signs**: under (i) `8 r₁ e^u |X| ≤ W` and
  (ii) `ω_{+1} ≤ e^{-u} W / (2 (r₁ + 1))`: `U′_{+1} < U₀ < U′_{-1}`;
* `r6_2_root` — **Lemma R6.2, the root**: there is `s ∈ (-1, 1)` with `U′_s = U₀` exactly,
  `log Z′_s - log Z₀ ≥ log (1 + e^{-u} (1 - 1/r₁))`, and `g′_s = g₀` wherever `d' > r₁`.
-/

section Signs

variable {X : Type*} [Fintype X]

/-- The excess mass of `T` over the zero function ("if `g₀` were `0`"). -/
def freeMass (T : X → ℝ) : ℝ := ∑ x, (Real.exp (-T x) - 1)

/-- `ω`: the weight of the twin inside the visible basin. -/
def overlapW (g₀ T : X → ℝ) : ℝ := ∑ x, if g₀ x < 0 ∧ T x < 0 then Real.exp (-T x) else 0

theorem overlapW_nonneg (g₀ T : X → ℝ) : 0 ≤ overlapW g₀ T := by
  refine Finset.sum_nonneg (fun x _ => ?_)
  split_ifs
  · exact (Real.exp_pos _).le
  · exact le_refl 0

/-- Layer A: `E ≤ E^f`. -/
theorem excessMass_le_freeMass {g₀ T : X → ℝ} (hg : ∀ x, g₀ x ≤ 0) (hT : ∀ x, T x ≤ 0) :
    excessMass g₀ T ≤ freeMass T := by
  unfold excessMass freeMass
  refine Finset.sum_le_sum (fun x _ => ?_)
  have h1 : 1 ≤ Real.exp (-g₀ x) := Real.one_le_exp (by linarith [hg x])
  have h2 : 1 ≤ Real.exp (-T x) := Real.one_le_exp (by linarith [hT x])
  exact max_le (by linarith) (by linarith)

/-- Layer A: `E^f - ω ≤ E`. -/
theorem freeMass_sub_overlapW_le {g₀ T : X → ℝ} (hg : ∀ x, g₀ x ≤ 0) (hT : ∀ x, T x ≤ 0) :
    freeMass T - overlapW g₀ T ≤ excessMass g₀ T := by
  unfold excessMass freeMass overlapW
  rw [← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum (fun x _ => ?_)
  have e0 : Real.exp (-(0 : ℝ)) = 1 := by simp
  by_cases h : g₀ x < 0 ∧ T x < 0
  · rw [if_pos h]
    have := le_max_right (Real.exp (-T x) - Real.exp (-g₀ x)) 0
    linarith
  · rw [if_neg h]
    rcases not_and_or.1 h with h' | h'
    · have hg0 : g₀ x = 0 := le_antisymm (hg x) (not_lt.1 h')
      rw [hg0, e0]
      have := le_max_left (Real.exp (-T x) - 1) 0
      linarith
    · have hT0 : T x = 0 := le_antisymm (hT x) (not_lt.1 h')
      rw [hT0, e0]
      have := le_max_right ((1 : ℝ) - Real.exp (-g₀ x)) 0
      linarith

/-- Layer A: `D^f ≤ D`. -/
theorem enSum_le_excessEnergy {g₀ T : X → ℝ} (hg : ∀ x, g₀ x ≤ 0) (hT : ∀ x, T x ≤ 0) :
    enSum T ≤ excessEnergy g₀ T := by
  unfold enSum excessEnergy
  refine Finset.sum_le_sum (fun x _ => ?_)
  have h1 : g₀ x * Real.exp (-g₀ x) ≤ 0 :=
    mul_nonpos_of_nonpos_of_nonneg (hg x) (Real.exp_pos _).le
  have h2 : T x * Real.exp (-T x) ≤ 0 :=
    mul_nonpos_of_nonpos_of_nonneg (hT x) (Real.exp_pos _).le
  split_ifs <;> linarith

/-- Layer A: `D ≤ D^f + M ω` when `-M ≤ T`. -/
theorem excessEnergy_le {g₀ T : X → ℝ} {M : ℝ} (hg : ∀ x, g₀ x ≤ 0) (hT : ∀ x, T x ≤ 0)
    (hM : ∀ x, -M ≤ T x) :
    excessEnergy g₀ T ≤ enSum T + M * overlapW g₀ T := by
  unfold enSum excessEnergy overlapW
  rw [Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_le_sum (fun x _ => ?_)
  have hexpT := Real.exp_pos (-T x)
  have hexpg := Real.exp_pos (-g₀ x)
  by_cases h : T x < g₀ x
  · rw [if_pos h]
    have hTneg : T x < 0 := lt_of_lt_of_le h (hg x)
    by_cases hg0 : g₀ x < 0
    · rw [if_pos ⟨hg0, hTneg⟩]
      have hle : Real.exp (-g₀ x) ≤ Real.exp (-T x) := Real.exp_le_exp.2 (by linarith)
      have hgM : -g₀ x ≤ M := by linarith [hM x]
      have hM0 : (0 : ℝ) ≤ M := by linarith [hM x]
      have := mul_le_mul hgM hle hexpg.le hM0
      linarith
    · have hgz : g₀ x = 0 := le_antisymm (hg x) (not_lt.1 hg0)
      rw [if_neg (fun hh => hg0 hh.1), hgz]
      simp
  · rw [if_neg h]
    by_cases hT0 : T x < 0
    · have hg0 : g₀ x < 0 := lt_of_le_of_lt (not_lt.1 h) hT0
      rw [if_pos ⟨hg0, hT0⟩]
      have : 0 ≤ (T x + M) * Real.exp (-T x) := mul_nonneg (by linarith [hM x]) hexpT.le
      linarith
    · have hTz : T x = 0 := le_antisymm (hT x) (not_lt.1 hT0)
      rw [if_neg (fun hh => hT0 hh.2), hTz]
      simp

/-! #### Layer B: the basin -/

/-- The basin of level `ρ` for the distance profile `d`: `x ↦ -u (ρ - d x)₊`. -/
def basin (u ρ : ℝ) (d : X → ℕ) (x : X) : ℝ := -(u * max (ρ - d x) 0)

/-- `W = ∑_{d < r} e^{u (r - d)}`: the weight of the basin. -/
def basinW (u : ℝ) (r : ℕ) (d : X → ℕ) : ℝ :=
  ∑ x, if d x < r then Real.exp (u * ((r : ℝ) - d x)) else 0

/-- `V = #{d < r}`. -/
def basinV (r : ℕ) (d : X → ℕ) : ℝ := ∑ x, if d x < r then (1 : ℝ) else 0

/-- `A′ = ∑_{d < r} u (r - d) e^{u (r - d)} = -∑ g₀ e^{-g₀}`. -/
def basinA (u : ℝ) (r : ℕ) (d : X → ℕ) : ℝ :=
  ∑ x, if d x < r then u * ((r : ℝ) - d x) * Real.exp (u * ((r : ℝ) - d x)) else 0

/-- `#{d = r}`. -/
def sphereC (r : ℕ) (d : X → ℕ) : ℝ := ∑ x, if d x = r then (1 : ℝ) else 0

omit [Fintype X] in
theorem basin_nonpos {u : ℝ} (hu : 0 ≤ u) (ρ : ℝ) (d : X → ℕ) (x : X) : basin u ρ d x ≤ 0 := by
  unfold basin
  have := mul_nonneg hu (le_max_right (ρ - d x) 0)
  linarith

omit [Fintype X] in
theorem basin_anti {u : ℝ} (hu : 0 ≤ u) {ρ ρ' : ℝ} (h : ρ ≤ ρ') (d : X → ℕ) (x : X) :
    basin u ρ' d x ≤ basin u ρ d x := by
  unfold basin
  have h1 : max (ρ - d x) 0 ≤ max (ρ' - d x) 0 := max_le_max (by linarith) le_rfl
  have := mul_le_mul_of_nonneg_left h1 hu
  linarith

omit [Fintype X] in
theorem neg_le_basin {u : ℝ} (hu : 0 ≤ u) {ρ : ℝ} (hρ : 0 ≤ ρ) (d : X → ℕ) (x : X) :
    -(u * ρ) ≤ basin u ρ d x := by
  unfold basin
  have hd : (0 : ℝ) ≤ d x := Nat.cast_nonneg _
  have h1 : max (ρ - d x) 0 ≤ ρ := max_le (by linarith) hρ
  have := mul_le_mul_of_nonneg_left h1 hu
  linarith

theorem basinW_nonneg (u : ℝ) (r : ℕ) (d : X → ℕ) : 0 ≤ basinW u r d := by
  refine Finset.sum_nonneg (fun x _ => ?_)
  split_ifs
  · exact (Real.exp_pos _).le
  · exact le_refl 0

theorem basinV_nonneg (r : ℕ) (d : X → ℕ) : 0 ≤ basinV r d := by
  refine Finset.sum_nonneg (fun x _ => ?_)
  split_ifs <;> norm_num

theorem sphereC_nonneg (r : ℕ) (d : X → ℕ) : 0 ≤ sphereC r d := by
  refine Finset.sum_nonneg (fun x _ => ?_)
  split_ifs <;> norm_num

theorem basinV_add_sphereC_le (r : ℕ) (d : X → ℕ) :
    basinV r d + sphereC r d ≤ Fintype.card X := by
  have hN : (Fintype.card X : ℝ) = ∑ _x : X, (1 : ℝ) := by simp
  unfold basinV sphereC
  rw [hN, ← Finset.sum_add_distrib]
  refine Finset.sum_le_sum (fun x _ => ?_)
  by_cases h : d x < r
  · rw [if_pos h, if_neg (ne_of_lt h)]
    norm_num
  · rw [if_neg h]
    split_ifs <;> norm_num

theorem basinA_nonneg {u : ℝ} (hu : 0 ≤ u) (r : ℕ) (d : X → ℕ) : 0 ≤ basinA u r d := by
  refine Finset.sum_nonneg (fun x _ => ?_)
  split_ifs with h
  · have hc : (d x : ℝ) < r := by exact_mod_cast h
    exact mul_nonneg (mul_nonneg hu (by linarith)) (Real.exp_pos _).le
  · exact le_refl 0

/-- `A′ ≤ u r W`. -/
theorem basinA_le {u : ℝ} (hu : 0 ≤ u) (r : ℕ) (d : X → ℕ) :
    basinA u r d ≤ u * r * basinW u r d := by
  unfold basinA basinW
  rw [Finset.mul_sum]
  refine Finset.sum_le_sum (fun x _ => ?_)
  split_ifs with h
  · have hd : (0 : ℝ) ≤ d x := Nat.cast_nonneg _
    have h1 : u * ((r : ℝ) - d x) ≤ u * r := mul_le_mul_of_nonneg_left (by linarith) hu
    exact mul_le_mul_of_nonneg_right h1 (Real.exp_pos _).le
  · simp

/-- `Z₀ = |X| + W - V`. -/
theorem partSum_basin (u : ℝ) (r : ℕ) (d : X → ℕ) :
    partSum (basin u r d) = Fintype.card X + basinW u r d - basinV r d := by
  have hN : (Fintype.card X : ℝ) = ∑ _x : X, (1 : ℝ) := by simp
  unfold partSum basin basinW basinV
  rw [hN, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl (fun x _ => ?_)
  by_cases h : d x < r
  · have hc : (d x : ℝ) < r := by exact_mod_cast h
    rw [if_pos h, if_pos h, max_eq_left (by linarith), neg_neg]
    ring
  · have hc : (r : ℝ) ≤ d x := by exact_mod_cast not_lt.1 h
    rw [if_neg h, if_neg h, max_eq_right (by linarith)]
    simp

/-- `∑ g₀ e^{-g₀} = -A′`. -/
theorem enSum_basin (u : ℝ) (r : ℕ) (d : X → ℕ) :
    enSum (basin u r d) = -basinA u r d := by
  unfold enSum basin basinA
  rw [← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl (fun x _ => ?_)
  by_cases h : d x < r
  · have hc : (d x : ℝ) < r := by exact_mod_cast h
    rw [if_pos h, max_eq_left (by linarith), neg_neg]
    ring
  · have hc : (r : ℝ) ≤ d x := by exact_mod_cast not_lt.1 h
    rw [if_neg h, max_eq_right (by linarith)]
    simp

/-- The free excess mass at `s = +1`: `E^f_{+1} = e^u (W + #{d = r}) - (V + #{d = r})`. -/
theorem freeMass_basin_succ (u : ℝ) (r : ℕ) (d : X → ℕ) :
    freeMass (basin u ((r : ℝ) + 1) d) =
      Real.exp u * (basinW u r d + sphereC r d) - (basinV r d + sphereC r d) := by
  unfold freeMass basin basinW basinV sphereC
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib, Finset.mul_sum,
    ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl (fun x _ => ?_)
  rcases lt_trichotomy (d x) r with h | h | h
  · have hc : (d x : ℝ) < r := by exact_mod_cast h
    rw [if_pos h, if_pos h, if_neg (ne_of_lt h), max_eq_left (by linarith), neg_neg]
    have e : u * ((r : ℝ) + 1 - d x) = u + u * ((r : ℝ) - d x) := by ring
    rw [e, Real.exp_add]
    ring
  · have hc : (d x : ℝ) = r := by exact_mod_cast h
    rw [if_neg (not_lt.2 (le_of_eq h.symm)), if_neg (not_lt.2 (le_of_eq h.symm)), if_pos h,
      max_eq_left (by linarith), neg_neg, hc]
    have e : u * ((r : ℝ) + 1 - r) = u := by ring
    rw [e]
    ring
  · have hc : (r : ℝ) + 1 ≤ d x := by exact_mod_cast Nat.succ_le_of_lt h
    rw [if_neg (not_lt.2 h.le), if_neg (not_lt.2 h.le), if_neg (ne_of_gt h),
      max_eq_right (by linarith)]
    simp

/-- The free excess energy at `s = +1`: `D^f_{+1} = -e^u (A′ + u (W + #{d = r}))`. -/
theorem enSum_basin_succ (u : ℝ) (r : ℕ) (d : X → ℕ) :
    enSum (basin u ((r : ℝ) + 1) d) =
      -(Real.exp u * (basinA u r d + u * (basinW u r d + sphereC r d))) := by
  unfold enSum basin basinA basinW sphereC
  rw [← Finset.sum_add_distrib, Finset.mul_sum, ← Finset.sum_add_distrib, Finset.mul_sum,
    ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl (fun x _ => ?_)
  rcases lt_trichotomy (d x) r with h | h | h
  · have hc : (d x : ℝ) < r := by exact_mod_cast h
    rw [if_pos h, if_pos h, if_neg (ne_of_lt h), max_eq_left (by linarith), neg_neg]
    have e : u * ((r : ℝ) + 1 - d x) = u + u * ((r : ℝ) - d x) := by ring
    rw [e, Real.exp_add]
    ring
  · have hc : (d x : ℝ) = r := by exact_mod_cast h
    rw [if_neg (not_lt.2 (le_of_eq h.symm)), if_neg (not_lt.2 (le_of_eq h.symm)), if_pos h,
      max_eq_left (by linarith), neg_neg, hc]
    have e : u * ((r : ℝ) + 1 - r) = u := by ring
    rw [e]
    ring
  · have hc : (r : ℝ) + 1 ≤ d x := by exact_mod_cast Nat.succ_le_of_lt h
    rw [if_neg (not_lt.2 h.le), if_neg (not_lt.2 h.le), if_neg (ne_of_gt h),
      max_eq_right (by linarith)]
    simp

/-- The free excess mass at `s = -1`: `E^f_{-1} = e^{-u} W - V`. -/
theorem freeMass_basin_pred (u : ℝ) (r : ℕ) (d : X → ℕ) :
    freeMass (basin u ((r : ℝ) - 1) d) = Real.exp (-u) * basinW u r d - basinV r d := by
  unfold freeMass basin basinW basinV
  rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl (fun x _ => ?_)
  by_cases h : d x < r
  · have hc : (d x : ℝ) + 1 ≤ r := by exact_mod_cast Nat.succ_le_of_lt h
    rw [if_pos h, if_pos h, max_eq_left (by linarith), neg_neg]
    have e : u * ((r : ℝ) - 1 - d x) = -u + u * ((r : ℝ) - d x) := by ring
    rw [e, Real.exp_add]
  · have hc : (r : ℝ) ≤ d x := by exact_mod_cast not_lt.1 h
    rw [if_neg h, if_neg h, max_eq_right (by linarith)]
    simp

/-- The free excess energy at `s = -1`: `D^f_{-1} = -e^{-u} (A′ - u W)`. -/
theorem enSum_basin_pred (u : ℝ) (r : ℕ) (d : X → ℕ) :
    enSum (basin u ((r : ℝ) - 1) d) =
      -(Real.exp (-u) * (basinA u r d - u * basinW u r d)) := by
  unfold enSum basin basinA basinW
  rw [Finset.mul_sum, ← Finset.sum_sub_distrib, Finset.mul_sum, ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl (fun x _ => ?_)
  by_cases h : d x < r
  · have hc : (d x : ℝ) + 1 ≤ r := by exact_mod_cast Nat.succ_le_of_lt h
    rw [if_pos h, if_pos h, max_eq_left (by linarith), neg_neg]
    have e : u * ((r : ℝ) - 1 - d x) = -u + u * ((r : ℝ) - d x) := by ring
    rw [e, Real.exp_add]
    ring
  · have hc : (r : ℝ) ≤ d x := by exact_mod_cast not_lt.1 h
    rw [if_neg h, if_neg h, max_eq_right (by linarith)]
    simp

/-- Equidistributed profiles have the same sums of every function of the distance. -/
theorem sum_comp_of_equidist {d₀ d' : X → ℕ} (σ : X ≃ X) (hσ : ∀ x, d' (σ x) = d₀ x)
    (ψ : ℕ → ℝ) : ∑ x, ψ (d' x) = ∑ x, ψ (d₀ x) := by
  rw [← Equiv.sum_comp σ (fun x => ψ (d' x))]
  exact Finset.sum_congr rfl (fun x _ => by rw [hσ x])

theorem freeMass_basin_equidist {d₀ d' : X → ℕ} (σ : X ≃ X) (hσ : ∀ x, d' (σ x) = d₀ x)
    (u ρ : ℝ) : freeMass (basin u ρ d') = freeMass (basin u ρ d₀) :=
  sum_comp_of_equidist σ hσ (fun k => Real.exp (-(-(u * max (ρ - (k : ℝ)) 0))) - 1)

theorem enSum_basin_equidist {d₀ d' : X → ℕ} (σ : X ≃ X) (hσ : ∀ x, d' (σ x) = d₀ x)
    (u ρ : ℝ) : enSum (basin u ρ d') = enSum (basin u ρ d₀) :=
  sum_comp_of_equidist σ hσ
    (fun k => -(u * max (ρ - (k : ℝ)) 0) * Real.exp (-(-(u * max (ρ - (k : ℝ)) 0))))

/-! #### Layer C: real arithmetic -/

/-- The sign at `s = +1`.  `a = e^{-u}`, `b = e^u`, `q = A′/Z₀ = -U₀`, `c = #{d₀ = r₁}`. -/
theorem sign_plus_arith {u r a b N W V c A Z q E D ω : ℝ}
    (hu : 0 < u) (ha1 : a ≤ 1) (hb : 1 ≤ b)
    (hW : 0 < W) (hc : 0 ≤ c) (hVc : V + c ≤ N) (hV : 0 ≤ V)
    (hZ : Z = N + W - V) (hq : 0 ≤ q) (hqZ : q * Z = A)
    (hE : E ≤ b * (W + c) - (V + c))
    (hD : D ≤ -(b * (A + u * (W + c))) + u * (r + 1) * ω)
    (hii : 2 * (r + 1) * ω ≤ a * W) : D + q * E < 0 := by
  have h1 : q * E ≤ q * (b * (W + c) - (V + c)) := mul_le_mul_of_nonneg_left hE hq
  have h2 : 0 ≤ q * (V + c) := mul_nonneg hq (by linarith)
  have h3 : q * (W + c) ≤ A := by
    rw [← hqZ]
    exact mul_le_mul_of_nonneg_left (by linarith) hq
  have h4 : b * (q * (W + c)) ≤ b * A := mul_le_mul_of_nonneg_left h3 (by linarith)
  have p1 : u * ((r + 1) * ω) ≤ u * (a * W / 2) :=
    mul_le_mul_of_nonneg_left (by linarith) hu.le
  have huW : 0 < u * W := mul_pos hu hW
  have p2 : u * (a * W) ≤ u * W := by nlinarith
  have p3 : u * W ≤ u * (b * (W + c)) := by
    have : W ≤ b * (W + c) := by nlinarith
    exact mul_le_mul_of_nonneg_left this hu.le
  nlinarith

/-- The sign at `s = -1`. -/
theorem sign_minus_arith {u r a N W V A Z q E D ω : ℝ}
    (hu : 0 < u) (hr : 1 ≤ r) (ha : 0 < a) (ha1 : a ≤ 1)
    (hW : 0 < W) (hV : 0 ≤ V) (hVN : V ≤ N) (hω : 0 ≤ ω)
    (hZ : Z = N + W - V) (hq : 0 ≤ q) (hqZ : q * Z = A) (hqr : q ≤ u * r)
    (hE : a * W - V - ω ≤ E) (hD : -(a * (A - u * W)) ≤ D)
    (hi : 8 * r * N ≤ a * W) (hii : 2 * (r + 1) * ω ≤ a * W) : 0 < D + q * E := by
  have hK0 : 0 ≤ a * (N - V) + V + ω := by
    have := mul_nonneg ha.le (sub_nonneg.2 hVN)
    linarith
  have hK1 : a * (N - V) + V + ω ≤ N + ω := by
    have := mul_nonneg (sub_nonneg.2 ha1) (sub_nonneg.2 hVN)
    nlinarith
  have hqK : q * (a * (N - V) + V + ω) ≤ u * r * (a * (N - V) + V + ω) :=
    mul_le_mul_of_nonneg_right hqr hK0
  have hrω : r * ω ≤ (r + 1) * ω := by nlinarith
  have hrK : r * (N + ω) ≤ 5 / 8 * (a * W) := by nlinarith
  have hur : 0 ≤ u * r := mul_nonneg hu.le (by linarith)
  have hurK : u * r * (a * (N - V) + V + ω) ≤ u * (5 / 8 * (a * W)) := by
    calc u * r * (a * (N - V) + V + ω) ≤ u * r * (N + ω) := mul_le_mul_of_nonneg_left hK1 hur
      _ = u * (r * (N + ω)) := by ring
      _ ≤ u * (5 / 8 * (a * W)) := mul_le_mul_of_nonneg_left hrK hu.le
  have hqE : q * (a * W - V - ω) ≤ q * E := mul_le_mul_of_nonneg_left hE hq
  have hid : -(a * (q * Z - u * W)) + q * (a * W - V - ω) =
      a * u * W - q * (a * (N - V) + V + ω) := by
    rw [hZ]
    ring
  rw [← hqZ] at hD
  have hpos : 0 < u * (a * W) := mul_pos hu (mul_pos ha hW)
  nlinarith

/-- The gain in the partition function at `s = -1`. -/
theorem gain_arith {r a N W V Z ω : ℝ} (hr : 1 ≤ r) (ha : 0 < a) (ha1 : a ≤ 1)
    (hV : 0 ≤ V) (hVN : V ≤ N) (hω : 0 ≤ ω) (hZ : Z = N + W - V)
    (hi : 8 * r * N ≤ a * W) (hii : 2 * (r + 1) * ω ≤ a * W) :
    a * (1 - 1 / r) * Z ≤ a * W - V - ω := by
  have hr0 : 0 < r := by linarith
  have hN : 0 ≤ N := by linarith
  have e : a * (1 - 1 / r) * Z = a * (r - 1) * Z / r := by
    field_simp
  rw [e, div_le_iff₀ hr0, hZ]
  have f1 : a * (r - 1) * N ≤ r * N := by
    have h1 : a * (r - 1) ≤ r := by nlinarith
    exact mul_le_mul_of_nonneg_right h1 hN
  have f2 : r * V ≤ r * N := mul_le_mul_of_nonneg_left hVN hr0.le
  have f3 : r * ω ≤ (r + 1) * ω := by nlinarith
  have f4 : 0 ≤ a * (r - 1) * V := mul_nonneg (mul_nonneg ha.le (by linarith)) hV
  nlinarith

/-- `ω` is monotone: a deeper twin has a larger overlap weight. -/
theorem overlapW_mono {g₀ T T' : X → ℝ} (h : ∀ x, T' x ≤ T x) :
    overlapW g₀ T ≤ overlapW g₀ T' := by
  unfold overlapW
  refine Finset.sum_le_sum (fun x _ => ?_)
  by_cases h1 : g₀ x < 0 ∧ T x < 0
  · have h2 : g₀ x < 0 ∧ T' x < 0 := ⟨h1.1, lt_of_le_of_lt (h x) h1.2⟩
    rw [if_pos h1, if_pos h2]
    exact Real.exp_le_exp.2 (by linarith [h x])
  · rw [if_neg h1]
    split_ifs
    · exact (Real.exp_pos _).le
    · exact le_refl 0

/-- A deeper twin has a larger partition sum. -/
theorem partSum_twinMin_mono {g₀ T T' : X → ℝ} (h : ∀ x, T' x ≤ T x) :
    partSum (twinMin g₀ T) ≤ partSum (twinMin g₀ T') := by
  unfold partSum twinMin
  refine Finset.sum_le_sum (fun x _ => Real.exp_le_exp.2 ?_)
  have := min_le_min (le_refl (g₀ x)) (h x)
  linarith

variable [Nonempty X]

/-- The core of Lemma R6.2: the two signs, and the lower bound on the excess mass at `s = -1`. -/
theorem r6_2_core (d₀ d' : X → ℕ) (σ : X ≃ X) (hσ : ∀ x, d' (σ x) = d₀ x) {u : ℝ}
    (hu : 0 < u) {r₁ : ℕ} (hr : 1 ≤ r₁)
    (hi : 8 * (r₁ : ℝ) * Real.exp u * Fintype.card X ≤ basinW u r₁ d₀)
    (hii : overlapW (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d') ≤
      Real.exp (-u) * basinW u r₁ d₀ / (2 * ((r₁ : ℝ) + 1))) :
    meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d')) < meanEn (basin u r₁ d₀) ∧
      meanEn (basin u r₁ d₀) <
        meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d')) ∧
      Real.exp (-u) * (1 - 1 / (r₁ : ℝ)) * partSum (basin u r₁ d₀) ≤
        excessMass (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d') := by
  have hr' : (1 : ℝ) ≤ r₁ := by exact_mod_cast hr
  have ha : 0 < Real.exp (-u) := Real.exp_pos _
  have ha1 : Real.exp (-u) ≤ 1 := by
    rw [← Real.exp_zero]
    exact Real.exp_le_exp.2 (by linarith)
  have hb : 1 ≤ Real.exp u := Real.one_le_exp hu.le
  have hab : Real.exp (-u) * Real.exp u = 1 := by
    rw [← Real.exp_add]
    simp
  have hN : (1 : ℝ) ≤ Fintype.card X := by exact_mod_cast Fintype.card_pos
  have hV := basinV_nonneg r₁ d₀
  have hc := sphereC_nonneg r₁ d₀
  have hVc := basinV_add_sphereC_le r₁ d₀
  have hVN : basinV r₁ d₀ ≤ Fintype.card X := by linarith
  have hW : 0 < basinW u r₁ d₀ := by
    have : (0 : ℝ) < 8 * (r₁ : ℝ) * Real.exp u * Fintype.card X := by positivity
    linarith
  have hi' : 8 * (r₁ : ℝ) * Fintype.card X ≤ Real.exp (-u) * basinW u r₁ d₀ := by
    have h1 := mul_le_mul_of_nonneg_left hi ha.le
    have h2 : Real.exp (-u) * (8 * (r₁ : ℝ) * Real.exp u * Fintype.card X) =
        8 * (r₁ : ℝ) * Fintype.card X * (Real.exp (-u) * Real.exp u) := by ring
    rw [h2, hab, mul_one] at h1
    exact h1
  have hii' : 2 * ((r₁ : ℝ) + 1) * overlapW (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d') ≤
      Real.exp (-u) * basinW u r₁ d₀ := by
    rw [le_div_iff₀ (by positivity)] at hii
    linarith
  have hZ := partSum_basin u r₁ d₀
  have hZpos := partSum_pos (basin u r₁ d₀)
  have hA := basinA_nonneg hu.le r₁ d₀
  have hAle := basinA_le hu.le r₁ d₀
  set q : ℝ := basinA u r₁ d₀ / partSum (basin u r₁ d₀) with hq
  have hq0 : 0 ≤ q := div_nonneg hA hZpos.le
  have hqZ : q * partSum (basin u r₁ d₀) = basinA u r₁ d₀ := div_mul_cancel₀ _ hZpos.ne'
  have hWZ : basinW u r₁ d₀ ≤ partSum (basin u r₁ d₀) := by
    rw [hZ]
    linarith
  have hqr : q ≤ u * r₁ := by
    rw [hq, div_le_iff₀ hZpos]
    have := mul_le_mul_of_nonneg_left hWZ (mul_nonneg hu.le (by linarith : (0 : ℝ) ≤ r₁))
    linarith
  have hU₀ : meanEn (basin u r₁ d₀) = -q := by
    unfold meanEn
    rw [enSum_basin, hq, neg_div]
  have hg : ∀ x, basin u r₁ d₀ x ≤ 0 := fun x => basin_nonpos hu.le _ _ x
  -- the twin at `s = -1`
  have hTm : ∀ x, basin u ((r₁ : ℝ) - 1) d' x ≤ 0 := fun x => basin_nonpos hu.le _ _ x
  have hEm := freeMass_sub_overlapW_le hg hTm
  rw [freeMass_basin_equidist σ hσ, freeMass_basin_pred] at hEm
  have hω0 := overlapW_nonneg (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d')
  have hωmono : overlapW (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d') ≤
      overlapW (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d') :=
    overlapW_mono (fun x => basin_anti hu.le (by linarith) d' x)
  have hii'' : 2 * ((r₁ : ℝ) + 1) * overlapW (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d') ≤
      Real.exp (-u) * basinW u r₁ d₀ := by
    have := mul_le_mul_of_nonneg_left hωmono (by positivity : (0 : ℝ) ≤ 2 * ((r₁ : ℝ) + 1))
    linarith
  refine ⟨?_, ?_, ?_⟩
  · -- s = +1
    have hT : ∀ x, basin u ((r₁ : ℝ) + 1) d' x ≤ 0 := fun x => basin_nonpos hu.le _ _ x
    have hM : ∀ x, -(u * ((r₁ : ℝ) + 1)) ≤ basin u ((r₁ : ℝ) + 1) d' x :=
      fun x => neg_le_basin hu.le (by linarith) d' x
    have hE := excessMass_le_freeMass hg hT
    rw [freeMass_basin_equidist σ hσ, freeMass_basin_succ] at hE
    have hD := excessEnergy_le hg hT hM
    rw [enSum_basin_equidist σ hσ, enSum_basin_succ] at hD
    have key := sign_plus_arith hu ha1 hb hW hc hVc hV hZ hq0 hqZ hE hD hii'
    have hsub := meanEn_twinMin_sub (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d')
    have hE0 := excessMass_nonneg (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d')
    have hden : 0 < partSum (basin u r₁ d₀) +
        excessMass (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d') := by linarith
    have hneg : meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d')) -
        meanEn (basin u r₁ d₀) < 0 := by
      rw [hsub, hU₀]
      apply div_neg_of_neg_of_pos _ hden
      linarith
    linarith
  · -- s = -1
    have hD := enSum_le_excessEnergy hg hTm
    rw [enSum_basin_equidist σ hσ, enSum_basin_pred] at hD
    have key := sign_minus_arith hu hr' ha ha1 hW hV hVN hω0 hZ hq0 hqZ hqr hEm hD hi' hii''
    have hsub := meanEn_twinMin_sub (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d')
    have hE0 := excessMass_nonneg (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d')
    have hden : 0 < partSum (basin u r₁ d₀) +
        excessMass (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d') := by linarith
    have hpos : 0 < meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d')) -
        meanEn (basin u r₁ d₀) := by
      rw [hsub, hU₀]
      apply div_pos _ hden
      linarith
    linarith
  · -- the gain at s = -1
    have hgain := gain_arith hr' ha ha1 hV hVN hω0 hZ hi' hii''
    linarith

/-- **Lemma R6.2 (signs at the ends).**  Under (i) `8 r₁ e^u |X| ≤ W` and
(ii) `ω_{+1} ≤ e^{-u} W / (2 (r₁ + 1))`: `U′_{+1} < U₀ < U′_{-1}`. -/
theorem r6_2_signs (d₀ d' : X → ℕ) (σ : X ≃ X) (hσ : ∀ x, d' (σ x) = d₀ x) {u : ℝ}
    (hu : 0 < u) {r₁ : ℕ} (hr : 1 ≤ r₁)
    (hi : 8 * (r₁ : ℝ) * Real.exp u * Fintype.card X ≤ basinW u r₁ d₀)
    (hii : overlapW (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d') ≤
      Real.exp (-u) * basinW u r₁ d₀ / (2 * ((r₁ : ℝ) + 1))) :
    meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d')) < meanEn (basin u r₁ d₀) ∧
      meanEn (basin u r₁ d₀) <
        meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d')) :=
  ⟨(r6_2_core d₀ d' σ hσ hu hr hi hii).1, (r6_2_core d₀ d' σ hσ hu hr hi hii).2.1⟩

/-- **Lemma R6.2 (the exact root).**  Under the same hypotheses there is `s* ∈ (-1, 1)` with
`U′_{s*} = U₀` exactly, `log Z′_{s*} - log Z₀ ≥ log (1 + e^{-u} (1 - 1/r₁))`, and
`g′_{s*} = g₀` at every point with `d' > r₁` (outside the ball `B(a′, r₁)`). -/
theorem r6_2_root (d₀ d' : X → ℕ) (σ : X ≃ X) (hσ : ∀ x, d' (σ x) = d₀ x) {u : ℝ}
    (hu : 0 < u) {r₁ : ℕ} (hr : 1 ≤ r₁)
    (hi : 8 * (r₁ : ℝ) * Real.exp u * Fintype.card X ≤ basinW u r₁ d₀)
    (hii : overlapW (basin u r₁ d₀) (basin u ((r₁ : ℝ) + 1) d') ≤
      Real.exp (-u) * basinW u r₁ d₀ / (2 * ((r₁ : ℝ) + 1))) :
    ∃ s : ℝ, -1 < s ∧ s < 1 ∧
      meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + s) d')) = meanEn (basin u r₁ d₀) ∧
      Real.log (1 + Real.exp (-u) * (1 - 1 / (r₁ : ℝ))) ≤
        Real.log (partSum (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + s) d'))) -
          Real.log (partSum (basin u r₁ d₀)) ∧
      ∀ x, r₁ < d' x →
        twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + s) d') x = basin u r₁ d₀ x := by
  obtain ⟨hplus, hminus, hgain⟩ := r6_2_core d₀ d' σ hσ hu hr hi hii
  have hr' : (1 : ℝ) ≤ r₁ := by exact_mod_cast hr
  have e : ((r₁ : ℝ) + -1) = (r₁ : ℝ) - 1 := by ring
  have hcont : Continuous
      (fun s : ℝ => meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + s) d'))) := by
    unfold meanEn enSum partSum twinMin basin
    refine Continuous.div ?_ ?_ (fun s => ?_)
    · fun_prop
    · fun_prop
    · exact (Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty).ne'
  have hmem : meanEn (basin u r₁ d₀) ∈ Set.Icc
      ((fun s : ℝ => meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + s) d'))) 1)
      ((fun s : ℝ => meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + s) d'))) (-1)) := by
    refine ⟨hplus.le, ?_⟩
    show meanEn (basin u r₁ d₀) ≤
      meanEn (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + -1) d'))
    rw [e]
    exact hminus.le
  obtain ⟨s, ⟨hs1, hs2⟩, hs⟩ :=
    intermediate_value_Icc' (by norm_num : (-1 : ℝ) ≤ 1) hcont.continuousOn hmem
  simp only at hs
  have hsne1 : s ≠ 1 := by
    rintro rfl
    exact absurd hs (ne_of_lt hplus)
  have hsnem1 : s ≠ -1 := by
    rintro rfl
    rw [e] at hs
    exact absurd hs.symm (ne_of_lt hminus)
  have hs1' : -1 < s := lt_of_le_of_ne hs1 (Ne.symm hsnem1)
  have hs2' : s < 1 := lt_of_le_of_ne hs2 hsne1
  refine ⟨s, hs1', hs2', hs, ?_, ?_⟩
  · have hZpos := partSum_pos (basin u r₁ d₀)
    have hmono : partSum (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) - 1) d')) ≤
        partSum (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + s) d')) :=
      partSum_twinMin_mono (fun x => basin_anti hu.le (by linarith) d' x)
    rw [partSum_twinMin] at hmono
    have h1r : 1 / (r₁ : ℝ) ≤ 1 := by
      rw [div_le_one (by linarith)]
      exact hr'
    have hpos1 : 0 < 1 + Real.exp (-u) * (1 - 1 / (r₁ : ℝ)) := by
      have := mul_nonneg (Real.exp_pos (-u)).le (sub_nonneg.2 h1r)
      linarith
    have hlow : (1 + Real.exp (-u) * (1 - 1 / (r₁ : ℝ))) * partSum (basin u r₁ d₀) ≤
        partSum (twinMin (basin u r₁ d₀) (basin u ((r₁ : ℝ) + s) d')) := by
      linarith
    have hlog := Real.log_le_log (mul_pos hpos1 hZpos) hlow
    rw [Real.log_mul hpos1.ne' hZpos.ne'] at hlog
    linarith
  · intro x hx
    have hc : (r₁ : ℝ) + 1 ≤ d' x := by exact_mod_cast Nat.succ_le_of_lt hx
    have hT0 : basin u ((r₁ : ℝ) + s) d' x = 0 := by
      unfold basin
      rw [max_eq_right (by linarith)]
      simp
    show min (basin u r₁ d₀ x) (basin u ((r₁ : ℝ) + s) d' x) = basin u r₁ d₀ x
    rw [hT0]
    exact min_eq_left (basin_nonpos hu.le _ _ x)

end Signs

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
#print axioms ScienceL2.sum_offDiag_eq_two_mul_sum_lt
#print axioms ScienceL2.sum_sub_pair_min_lt_le_sup'
#print axioms ScienceL2.sum_sub_pair_min_needs_nonneg
#print axioms ScienceL2.sum_apply_distTo_le
#print axioms ScienceL2.flat_distTo_le
#print axioms ScienceL2.flat_distTo_le_card_mul
#print axioms ScienceL2.cone_distTo_ge
#print axioms ScienceL2.r5_2_abstract
#print axioms ScienceL2.excessMass_le_freeMass
#print axioms ScienceL2.freeMass_sub_overlapW_le
#print axioms ScienceL2.enSum_le_excessEnergy
#print axioms ScienceL2.excessEnergy_le
#print axioms ScienceL2.partSum_basin
#print axioms ScienceL2.enSum_basin
#print axioms ScienceL2.freeMass_basin_succ
#print axioms ScienceL2.enSum_basin_succ
#print axioms ScienceL2.freeMass_basin_pred
#print axioms ScienceL2.enSum_basin_pred
#print axioms ScienceL2.sign_plus_arith
#print axioms ScienceL2.sign_minus_arith
#print axioms ScienceL2.gain_arith
#print axioms ScienceL2.r6_2_core
#print axioms ScienceL2.r6_2_signs
#print axioms ScienceL2.r6_2_root
