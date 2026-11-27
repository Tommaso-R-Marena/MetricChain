import Mathlib

/-!
# Proposition A1.2, items 1–3: windows of conditional laws and the chain-rule bound

Science division, workstream L2.  Source: `docs/science/workstreams/A1_REPORT.md`, section 9.3
(Proposition A1.2) and section 2.5 (Proposition A1.1, the two-letter case).

Setting of the report: sites `i` with finite alphabets `S i`, positive site weights `π i`,
envelopes `d i`, reference `π = ⊗ π i`, class `𝒞 = {ψ : ψ x - ψ y ≤ ∑_i d i (x i) (y i)}`,
`ν_ψ ∝ π e^{-ψ}`; the *window* of a site is
`𝒲 = {p : π a p b ≤ e^{d a b} π b p a for all a, b}` (`p` a probability vector).

## What is proved

Item 1 (one site; sections `OneSite`, `Vertices`, `VertexBound`):
* `gibbsLaw_mem_window`, `exists_gibbsLaw_of_mem_window`, `window_eq_gibbs_image` —
  `𝒲 = {π_γ : γ ∈ L}`, `L = {γ : γ a - γ b ≤ d a b}`;
* `window_convex`, `isCompact_window` — `𝒲` is convex and compact;
* `lipClass_extremePoints_eq_empty` — `L` itself has **no** extreme points (it is invariant under
  adding constants), so "the vertices of the Lipschitz polytope `L`" must be read modulo
  constants;
* `extremePoints_window_eq` — **the vertex statement, corrected**:
  `extremePoints 𝒲 = gibbsLaw π '' extremePoints (lipNorm d a₀)`, `lipNorm d a₀` the class
  normalised at a base point (`gibbsLaw_extreme_of_extreme`, `extreme_of_gibbsLaw_extreme`,
  through the tight pairs: `window_tight_iff`, `perturb_mem_lipNorm`, `perturb_mem_window`).

Item 2:
* `site_conditional_mem_window` — the form of the brief: on `α × β` with weight
  `π a * w r * e^{-ψ (a, r)}`, `ψ (a, r) - ψ (b, r) ≤ d a b`, the law of the site letter lies in
  the window;
* `cylinder_cross_le`, `condLaw_mem_window` — the form of the report: on a dependent product
  `∀ i, S i`, for every site `i`, every set `P ∌ i` of conditioning sites and every pattern on
  `P`, the conditional law of `x i` lies in the window of site `i` (this contains "every order of
  the sites and every prefix");
* `single_site_of_admissible` — the single-site hypothesis follows from membership of `𝒞`;
* `window_needs_diag_zero` — it fails if the envelopes do not vanish on the diagonal.

Item 3 (`ChainRule`, `VertexBound` sections):
* `kl_gibbs_prod_eq` — the chain rule for the relative entropy of a Gibbs law on a product of
  two finite types with respect to a product law, as an explicit identity;
* `klBound_prod` — a bound on `KL(ν_ψ ‖ Q)` over the class tensorises over two factors;
* `klBound_pi` — on `∀ i : Fin n, S i`, `KL(ν_ψ ‖ ⊗ Q i) ≤ ∑_i M i` for every `ψ ∈ 𝒞` whenever
  `M i` bounds `KL(π_γ ‖ Q i)` over `γ ∈ L i`;
* `klBound_of_vertices`, `klBound_pi_of_vertices` — **item 3, the inequality as stated**: it is
  enough that `M i` bounds `KL(π_φ ‖ Q i)` over the *vertices* `φ` of the normalised site class
  (Krein–Milman, convexity and continuity of the divergence, the vertex correspondence);
* `kl_additive_pi` — `KL(ν_ψ ‖ ⊗ Q i) = ∑_i KL(π_{γ i} ‖ Q i)` at the additive instance
  `ψ x = ∑_i γ i (x i)`;
* `kl_pi_isGreatest`, `exists_site_max`, `kl_pi_exists_isGreatest` — the site maxima exist, and
  their sum is the greatest value of `KL(ν_ψ ‖ ⊗ Q i)` over `𝒞`.

Not proved here: that the vertex set is finite, the identification of `∑_i M i` with `n · a`
(capacity) for the Shannon centres, items 4 and 5.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL2

open Finset

/-! ### Item 1: the window of one site -/

section OneSite

variable {α : Type*} [Fintype α]

/-- The Gibbs law `π_γ ∝ π e^{-γ}`. -/
def gibbsLaw (π γ : α → ℝ) (a : α) : ℝ := π a * Real.exp (-γ a) / ∑ b, π b * Real.exp (-γ b)

/-- `γ` is in the class of the envelope `d`: `γ a - γ b ≤ d a b`. -/
def Admissible (d : α → α → ℝ) (γ : α → ℝ) : Prop := ∀ a b, γ a - γ b ≤ d a b

/-- The window of a site: the probability vectors `p` with `π a p b ≤ e^{d a b} π b p a`. -/
def window (π : α → ℝ) (d : α → α → ℝ) : Set (α → ℝ) :=
  {p | (∀ a, 0 ≤ p a) ∧ ∑ a, p a = 1 ∧ ∀ a b, π a * p b ≤ Real.exp (d a b) * π b * p a}

theorem gibbsZ_pos [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (γ : α → ℝ) :
    0 < ∑ b, π b * Real.exp (-γ b) :=
  Finset.sum_pos (fun b _ => mul_pos (hπ b) (Real.exp_pos _)) Finset.univ_nonempty

theorem gibbsLaw_pos [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (γ : α → ℝ) (a : α) :
    0 < gibbsLaw π γ a :=
  div_pos (mul_pos (hπ a) (Real.exp_pos _)) (gibbsZ_pos hπ γ)

theorem sum_gibbsLaw [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (γ : α → ℝ) :
    ∑ a, gibbsLaw π γ a = 1 := by
  unfold gibbsLaw
  rw [← Finset.sum_div]
  exact div_self (gibbsZ_pos hπ γ).ne'

/-- Item 1, `⊇`: the Gibbs law of a member of the Lipschitz class lies in the window. -/
theorem gibbsLaw_mem_window [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) {d : α → α → ℝ}
    {γ : α → ℝ} (hγ : Admissible d γ) : gibbsLaw π γ ∈ window π d := by
  refine ⟨fun a => (gibbsLaw_pos hπ γ a).le, sum_gibbsLaw hπ γ, fun a b => ?_⟩
  have hZ := gibbsZ_pos hπ γ
  unfold gibbsLaw
  have hexp : Real.exp (-γ b) ≤ Real.exp (d a b) * Real.exp (-γ a) := by
    rw [← Real.exp_add, Real.exp_le_exp]
    linarith [hγ a b]
  have h1 : π a * (π b * Real.exp (-γ b)) ≤ Real.exp (d a b) * π b * (π a * Real.exp (-γ a)) := by
    have := mul_le_mul_of_nonneg_left hexp (mul_pos (hπ a) (hπ b)).le
    linarith
  calc π a * (π b * Real.exp (-γ b) / ∑ c, π c * Real.exp (-γ c))
      = π a * (π b * Real.exp (-γ b)) / ∑ c, π c * Real.exp (-γ c) := by ring
    _ ≤ Real.exp (d a b) * π b * (π a * Real.exp (-γ a)) / ∑ c, π c * Real.exp (-γ c) :=
        div_le_div_of_nonneg_right h1 hZ.le
    _ = Real.exp (d a b) * π b * (π a * Real.exp (-γ a) / ∑ c, π c * Real.exp (-γ c)) := by ring

/-- Every member of the window is strictly positive. -/
theorem window_pos {π : α → ℝ} (hπ : ∀ a, 0 < π a) {d : α → α → ℝ} {p : α → ℝ}
    (hp : p ∈ window π d) (a : α) : 0 < p a := by
  obtain ⟨hp0, hp1, hpw⟩ := hp
  have hex : ∃ b, 0 < p b := by
    by_contra hcon
    have hcon' : ∀ b, p b ≤ 0 := fun b => not_lt.1 (fun hb => hcon ⟨b, hb⟩)
    have : ∑ b, p b = 0 :=
      Finset.sum_eq_zero (fun b _ => le_antisymm (hcon' b) (hp0 b))
    linarith
  obtain ⟨b, hb⟩ := hex
  have h := hpw a b
  have h1 : 0 < π a * p b := mul_pos (hπ a) hb
  have h2 : 0 < Real.exp (d a b) * π b := mul_pos (Real.exp_pos _) (hπ b)
  by_contra hcon
  have hpa : p a = 0 := le_antisymm (not_lt.1 hcon) (hp0 a)
  rw [hpa, mul_zero] at h
  linarith

/-- Item 1, `⊆`: every member of the window is the Gibbs law of a member of the Lipschitz
class, namely of `γ = log π - log p`. -/
theorem exists_gibbsLaw_of_mem_window {π : α → ℝ} (hπ : ∀ a, 0 < π a) {d : α → α → ℝ}
    {p : α → ℝ} (hp : p ∈ window π d) : ∃ γ, Admissible d γ ∧ p = gibbsLaw π γ := by
  have hpos := window_pos hπ hp
  obtain ⟨_, hp1, hpw⟩ := hp
  refine ⟨fun a => Real.log (π a) - Real.log (p a), ?_, ?_⟩
  · intro a b
    have h := Real.log_le_log (mul_pos (hπ a) (hpos b)) (hpw a b)
    rw [Real.log_mul (hπ a).ne' (hpos b).ne',
      Real.log_mul (mul_pos (Real.exp_pos _) (hπ b)).ne' (hpos a).ne',
      Real.log_mul (Real.exp_pos _).ne' (hπ b).ne', Real.log_exp] at h
    linarith
  · have hterm : ∀ a, π a * Real.exp (-(Real.log (π a) - Real.log (p a))) = p a := by
      intro a
      have e : -(Real.log (π a) - Real.log (p a)) = Real.log (p a) - Real.log (π a) := by ring
      rw [e, Real.exp_sub, Real.exp_log (hpos a), Real.exp_log (hπ a)]
      field_simp [(hπ a).ne']
    funext a
    unfold gibbsLaw
    rw [Finset.sum_congr rfl (fun b _ => hterm b), hterm a, hp1, div_one]

/-- **Item 1**: the window is the set of Gibbs laws of the Lipschitz class. -/
theorem window_eq_gibbs_image [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (d : α → α → ℝ) :
    window π d = {p | ∃ γ, Admissible d γ ∧ p = gibbsLaw π γ} := by
  ext p
  constructor
  · exact fun hp => exists_gibbsLaw_of_mem_window hπ hp
  · rintro ⟨γ, hγ, rfl⟩
    exact gibbsLaw_mem_window hπ hγ

/-- **Item 1**: the window is convex (its constraints are linear in `p`). -/
theorem window_convex (π : α → ℝ) (d : α → α → ℝ) : Convex ℝ (window π d) := by
  intro p hp q hq s t hs ht hst
  obtain ⟨hp0, hp1, hpw⟩ := hp
  obtain ⟨hq0, hq1, hqw⟩ := hq
  refine ⟨fun a => ?_, ?_, fun a b => ?_⟩
  · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    exact add_nonneg (mul_nonneg hs (hp0 a)) (mul_nonneg ht (hq0 a))
  · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, hp1, hq1]
    linarith
  · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    have h1 := mul_le_mul_of_nonneg_left (hpw a b) hs
    have h2 := mul_le_mul_of_nonneg_left (hqw a b) ht
    linarith

omit [Fintype α] in
/-- The Lipschitz class itself has no extreme points: it is invariant under adding constants.
("The vertices of the Lipschitz polytope" in item 1 are vertices modulo constants.) -/
theorem lipClass_extremePoints_eq_empty [Nonempty α] (d : α → α → ℝ) :
    Set.extremePoints ℝ {γ : α → ℝ | Admissible d γ} = ∅ := by
  ext γ
  simp only [Set.mem_empty_iff_false, iff_false]
  intro hγ
  rw [mem_extremePoints] at hγ
  obtain ⟨hmem, hext⟩ := hγ
  have h1 : (fun a => γ a + 1) ∈ {γ : α → ℝ | Admissible d γ} := by
    intro a b
    have := hmem a b
    simp only
    linarith
  have h2 : (fun a => γ a - 1) ∈ {γ : α → ℝ | Admissible d γ} := by
    intro a b
    have := hmem a b
    simp only
    linarith
  have hseg : γ ∈ openSegment ℝ (fun a => γ a + 1) (fun a => γ a - 1) := by
    refine ⟨1 / 2, 1 / 2, by norm_num, by norm_num, by norm_num, ?_⟩
    funext a
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have := (hext _ h1 _ h2 hseg).1
  obtain ⟨a⟩ := ‹Nonempty α›
  have h3 : γ a + 1 = γ a := congrFun this a
  linarith

end OneSite

/-! ### Item 2: conditional laws lie in the window -/

section Conditional

/-- **Item 2, in the form of the brief.**  `α` the site, `β` "the rest".  For a weight
`π a * w r * exp (-ψ (a, r))` on `α × β` — `w ≥ 0` any weight on the rest that does not depend
on the site letter — with `ψ (a, r) - ψ (b, r) ≤ d a b`, the law of the site letter lies in the
window. -/
theorem site_conditional_mem_window {α β : Type*} [Fintype α] [Fintype β] [Nonempty α]
    {π : α → ℝ} (hπ : ∀ a, 0 < π a) {w : β → ℝ} (hw : ∀ r, 0 ≤ w r) (hw1 : ∃ r, 0 < w r)
    {d : α → α → ℝ} {ψ : α × β → ℝ} (hψ : ∀ a b r, ψ (a, r) - ψ (b, r) ≤ d a b) :
    (fun a => π a * (∑ r, w r * Real.exp (-ψ (a, r))) /
        ∑ b, π b * ∑ r, w r * Real.exp (-ψ (b, r))) ∈ window π d := by
  obtain ⟨r₀, hr₀⟩ := hw1
  have hN : ∀ a, 0 < ∑ r, w r * Real.exp (-ψ (a, r)) := by
    intro a
    have h1 : 0 < w r₀ * Real.exp (-ψ (a, r₀)) := mul_pos hr₀ (Real.exp_pos _)
    have h2 : w r₀ * Real.exp (-ψ (a, r₀)) ≤ ∑ r, w r * Real.exp (-ψ (a, r)) :=
      Finset.single_le_sum (f := fun r => w r * Real.exp (-ψ (a, r)))
        (fun r _ => mul_nonneg (hw r) (Real.exp_pos _).le) (Finset.mem_univ r₀)
    linarith
  have hZ : 0 < ∑ b, π b * ∑ r, w r * Real.exp (-ψ (b, r)) :=
    Finset.sum_pos (fun b _ => mul_pos (hπ b) (hN b)) Finset.univ_nonempty
  refine ⟨fun a => (div_pos (mul_pos (hπ a) (hN a)) hZ).le, ?_, fun a b => ?_⟩
  · rw [← Finset.sum_div]
    exact div_self hZ.ne'
  · have hNab : ∑ r, w r * Real.exp (-ψ (b, r)) ≤
        Real.exp (d a b) * ∑ r, w r * Real.exp (-ψ (a, r)) := by
      rw [Finset.mul_sum]
      refine Finset.sum_le_sum (fun r _ => ?_)
      have hexp : Real.exp (-ψ (b, r)) ≤ Real.exp (d a b) * Real.exp (-ψ (a, r)) := by
        rw [← Real.exp_add, Real.exp_le_exp]
        linarith [hψ a b r]
      have := mul_le_mul_of_nonneg_left hexp (hw r)
      linarith
    have h1 : π a * (π b * ∑ r, w r * Real.exp (-ψ (b, r))) ≤
        Real.exp (d a b) * π b * (π a * ∑ r, w r * Real.exp (-ψ (a, r))) := by
      have := mul_le_mul_of_nonneg_left hNab (mul_pos (hπ a) (hπ b)).le
      linarith
    calc π a * (π b * (∑ r, w r * Real.exp (-ψ (b, r))) /
          ∑ c, π c * ∑ r, w r * Real.exp (-ψ (c, r)))
        = π a * (π b * ∑ r, w r * Real.exp (-ψ (b, r))) /
          ∑ c, π c * ∑ r, w r * Real.exp (-ψ (c, r)) := by ring
      _ ≤ Real.exp (d a b) * π b * (π a * ∑ r, w r * Real.exp (-ψ (a, r))) /
          ∑ c, π c * ∑ r, w r * Real.exp (-ψ (c, r)) := div_le_div_of_nonneg_right h1 hZ.le
      _ = Real.exp (d a b) * π b * (π a * (∑ r, w r * Real.exp (-ψ (a, r))) /
          ∑ c, π c * ∑ r, w r * Real.exp (-ψ (c, r))) := by ring

variable {ι : Type*} [Fintype ι] [DecidableEq ι] {S : ι → Type*} [∀ i, Fintype (S i)]
  [∀ i, DecidableEq (S i)]

/-- The unnormalised `ν_ψ`-weight of the cylinder `{x : x i = a, x j = y j for j ∈ P}`. -/
def cylW (π : ∀ i, S i → ℝ) (ψ : (∀ i, S i) → ℝ) (i : ι) (P : Finset ι) (y : ∀ j, S j)
    (a : S i) : ℝ :=
  ∑ x ∈ Finset.univ.filter (fun x : ∀ j, S j => x i = a ∧ ∀ j ∈ P, x j = y j),
    (∏ j, π j (x j)) * Real.exp (-ψ x)

/-- The conditional law of the letter at site `i` given the pattern `y` on the sites `P`. -/
def condLaw (π : ∀ i, S i → ℝ) (ψ : (∀ i, S i) → ℝ) (i : ι) (P : Finset ι) (y : ∀ j, S j)
    (a : S i) : ℝ :=
  cylW π ψ i P y a / ∑ b, cylW π ψ i P y b

omit [∀ i, Fintype (S i)] [∀ i, DecidableEq (S i)] in
/-- The single-site condition follows from membership of the class `𝒞`, when the site
envelopes vanish on the diagonal. -/
theorem single_site_of_admissible (d : ∀ i, S i → S i → ℝ) (hd : ∀ i s, d i s s ≤ 0)
    {ψ : (∀ i, S i) → ℝ} (hψ : ∀ x y, ψ x - ψ y ≤ ∑ i, d i (x i) (y i)) (i : ι)
    (x : ∀ j, S j) (b : S i) : ψ x - ψ (Function.update x i b) ≤ d i (x i) b := by
  refine (hψ x (Function.update x i b)).trans ?_
  rw [← Finset.add_sum_erase _ _ (Finset.mem_univ i)]
  have h1 : ∑ j ∈ Finset.univ.erase i, d j (x j) (Function.update x i b j) ≤ 0 := by
    refine Finset.sum_nonpos (fun j hj => ?_)
    rw [Function.update_of_ne (Finset.ne_of_mem_erase hj)]
    exact hd j (x j)
  rw [Function.update_self]
  linarith

/-- **Item 2, cross-multiplied.**  For every site `i`, every set `P ∌ i` of conditioning sites,
every pattern `y`: `π i a * N(b) ≤ e^{d a b} * π i b * N(a)`, `N` the cylinder weights. -/
theorem cylinder_cross_le (π : ∀ i, S i → ℝ) (hπ : ∀ i s, 0 ≤ π i s) (ψ : (∀ i, S i) → ℝ)
    (i : ι) (d : S i → S i → ℝ) (hψ : ∀ x b, ψ x - ψ (Function.update x i b) ≤ d (x i) b)
    (P : Finset ι) (hiP : i ∉ P) (y : ∀ j, S j) (a b : S i) :
    π i a * cylW π ψ i P y b ≤ Real.exp (d a b) * π i b * cylW π ψ i P y a := by
  unfold cylW
  -- re-index the cylinder of `b` by the cylinder of `a` through `x ↦ update x i b`
  have hreindex : ∑ x ∈ Finset.univ.filter (fun x : ∀ j, S j => x i = b ∧ ∀ j ∈ P, x j = y j),
        (∏ j, π j (x j)) * Real.exp (-ψ x) =
      ∑ x ∈ Finset.univ.filter (fun x : ∀ j, S j => x i = a ∧ ∀ j ∈ P, x j = y j),
        (∏ j, π j (Function.update x i b j)) * Real.exp (-ψ (Function.update x i b)) := by
    symm
    refine Finset.sum_nbij' (fun x => Function.update x i b) (fun x => Function.update x i a)
      ?_ ?_ ?_ ?_ ?_
    · intro x hx
      rw [Finset.mem_filter] at hx ⊢
      refine ⟨Finset.mem_univ _, Function.update_self .., fun j hj => ?_⟩
      have hji : j ≠ i := fun h => hiP (h ▸ hj)
      rw [Function.update_of_ne hji]
      exact hx.2.2 j hj
    · intro x hx
      rw [Finset.mem_filter] at hx ⊢
      refine ⟨Finset.mem_univ _, Function.update_self .., fun j hj => ?_⟩
      have hji : j ≠ i := fun h => hiP (h ▸ hj)
      rw [Function.update_of_ne hji]
      exact hx.2.2 j hj
    · intro x hx
      rw [Finset.mem_filter] at hx
      rw [Function.update_idem, ← hx.2.1, Function.update_eq_self]
    · intro x hx
      rw [Finset.mem_filter] at hx
      rw [Function.update_idem, ← hx.2.1, Function.update_eq_self]
    · intro x _
      rfl
  rw [hreindex, Finset.mul_sum, Finset.mul_sum]
  refine Finset.sum_le_sum (fun x hx => ?_)
  rw [Finset.mem_filter] at hx
  have hxi : x i = a := hx.2.1
  -- the product of the site weights after the update
  have hprod_upd : ∏ j, π j (Function.update x i b j) =
      π i b * ∏ j ∈ Finset.univ.erase i, π j (x j) := by
    rw [← Finset.mul_prod_erase _ _ (Finset.mem_univ i), Function.update_self]
    congr 1
    refine Finset.prod_congr rfl (fun j hj => ?_)
    rw [Function.update_of_ne (Finset.ne_of_mem_erase hj)]
  have hprod : ∏ j, π j (x j) = π i a * ∏ j ∈ Finset.univ.erase i, π j (x j) := by
    rw [← Finset.mul_prod_erase _ _ (Finset.mem_univ i), hxi]
  have hR : 0 ≤ ∏ j ∈ Finset.univ.erase i, π j (x j) :=
    Finset.prod_nonneg (fun j _ => hπ j (x j))
  have hexp : Real.exp (-ψ (Function.update x i b)) ≤ Real.exp (d a b) * Real.exp (-ψ x) := by
    rw [← Real.exp_add, Real.exp_le_exp]
    have := hψ x b
    rw [hxi] at this
    linarith
  rw [hprod_upd, hprod]
  have hcoef : 0 ≤ π i a * (π i b * ∏ j ∈ Finset.univ.erase i, π j (x j)) :=
    mul_nonneg (hπ i a) (mul_nonneg (hπ i b) hR)
  have := mul_le_mul_of_nonneg_left hexp hcoef
  linarith

/-- **Item 2, in the form of the report.**  For every `ψ` with the single-site property at `i`
(in particular every `ψ ∈ 𝒞`), every set `P ∌ i` of conditioning sites and every pattern `y` on
`P` (in particular: every order of the sites and every prefix), the conditional law of the
letter at site `i` lies in the window of site `i`. -/
theorem condLaw_mem_window [∀ i, Nonempty (S i)] (π : ∀ i, S i → ℝ) (hπ : ∀ i s, 0 < π i s)
    (ψ : (∀ i, S i) → ℝ) (i : ι) (d : S i → S i → ℝ)
    (hψ : ∀ x b, ψ x - ψ (Function.update x i b) ≤ d (x i) b)
    (P : Finset ι) (hiP : i ∉ P) (y : ∀ j, S j) :
    condLaw π ψ i P y ∈ window (π i) d := by
  have hN0 : ∀ a, 0 ≤ cylW π ψ i P y a := fun a =>
    Finset.sum_nonneg (fun x _ =>
      mul_nonneg (Finset.prod_nonneg (fun j _ => (hπ j (x j)).le)) (Real.exp_pos _).le)
  have hNpos : ∀ a, 0 < cylW π ψ i P y a := by
    intro a
    unfold cylW
    refine Finset.sum_pos (fun x _ =>
      mul_pos (Finset.prod_pos (fun j _ => hπ j (x j))) (Real.exp_pos _)) ?_
    refine ⟨Function.update y i a, ?_⟩
    rw [Finset.mem_filter]
    refine ⟨Finset.mem_univ _, Function.update_self .., fun j hj => ?_⟩
    have hji : j ≠ i := fun h => hiP (h ▸ hj)
    rw [Function.update_of_ne hji]
  have hZ : 0 < ∑ b, cylW π ψ i P y b :=
    Finset.sum_pos (fun b _ => hNpos b) Finset.univ_nonempty
  refine ⟨fun a => div_nonneg (hN0 a) hZ.le, ?_, fun a b => ?_⟩
  · unfold condLaw
    rw [← Finset.sum_div]
    exact div_self hZ.ne'
  · have h := cylinder_cross_le π (fun j s => (hπ j s).le) ψ i d hψ P hiP y a b
    unfold condLaw
    calc π i a * (cylW π ψ i P y b / ∑ c, cylW π ψ i P y c)
        = π i a * cylW π ψ i P y b / ∑ c, cylW π ψ i P y c := by ring
      _ ≤ Real.exp (d a b) * π i b * cylW π ψ i P y a / ∑ c, cylW π ψ i P y c :=
          div_le_div_of_nonneg_right h hZ.le
      _ = Real.exp (d a b) * π i b * (cylW π ψ i P y a / ∑ c, cylW π ψ i P y c) := by ring

end Conditional

/-! ### The envelopes must vanish on the diagonal

Proposition A1.2 lists "`d_j ≥ 0` with the triangle inequality" as hypotheses on the site
envelopes.  Neither is used in items 1–3; what is used is `d_j s s ≤ 0`.  It cannot be dropped:
two binary sites, uniform weights, `d₁ ≡ 0` and `d₂ ≡ 1` (non-negative, triangle inequality),
`ψ (a, r) = [a]`.  Then `ψ` is in the class of `d₁ ⊕ d₂`, but the law of the first letter is not
in the window of `d₁` (which is `{π₁}`). -/

section Diagonal

theorem window_needs_diag_zero :
    ∃ ψ : Bool × Bool → ℝ,
      (∀ z z' : Bool × Bool, ψ z - ψ z' ≤ (0 : ℝ) + 1) ∧
      (fun a : Bool => (1 : ℝ) * (∑ r : Bool, (1 : ℝ) * Real.exp (-ψ (a, r))) /
          ∑ b : Bool, (1 : ℝ) * ∑ r : Bool, (1 : ℝ) * Real.exp (-ψ (b, r))) ∉
        window (fun _ : Bool => (1 : ℝ)) (fun _ _ => 0) := by
  refine ⟨fun z => if z.1 then 1 else 0, ?_, ?_⟩
  · intro z z'
    by_cases h : z.1 <;> by_cases h' : z'.1 <;> simp [h, h']
  · rintro ⟨_, _, hw⟩
    have h := hw true false
    have he : Real.exp (-1) < 1 := by
      rw [← Real.exp_zero]
      exact Real.exp_lt_exp.2 (by norm_num)
    have hpos : 0 < Real.exp (-1) := Real.exp_pos _
    simp only [Fintype.sum_bool, Real.exp_zero, one_mul, if_true] at h
    norm_num at h
    rw [div_le_div_iff_of_pos_right (by positivity)] at h
    linarith

end Diagonal

/-! ### Item 3: the chain-rule bound -/

section ChainRule

universe u

/-- Relative entropy `∑ p (log p - log q)` of two positive vectors on a finite type. -/
def klDivFin {X : Type*} [Fintype X] (p q : X → ℝ) : ℝ :=
  ∑ x, p x * (Real.log (p x) - Real.log (q x))

/-- `KL(ν_ψ ‖ Q) ≤ M` for every member `ψ` of the class of the envelope `d`. -/
def KLBound {X : Type*} [Fintype X] (π : X → ℝ) (d : X → X → ℝ) (Q : X → ℝ) (M : ℝ) : Prop :=
  ∀ ψ, Admissible d ψ → klDivFin (gibbsLaw π ψ) Q ≤ M

/-- The soft minimum of `ψ` over the first coordinate, with weights `π₁`:
`r ↦ -log ∑_a π₁ a e^{-ψ (a, r)}`. -/
def softMin {α β : Type*} [Fintype α] (π₁ : α → ℝ) (ψ : α × β → ℝ) (r : β) : ℝ :=
  -Real.log (∑ a, π₁ a * Real.exp (-ψ (a, r)))

/-- Adding a constant to the energy does not change the Gibbs law. -/
theorem gibbsLaw_add_const {X : Type*} [Fintype X] (π γ : X → ℝ) (c : ℝ) :
    gibbsLaw π (fun x => γ x + c) = gibbsLaw π γ := by
  funext x
  unfold gibbsLaw
  have h : ∀ y, π y * Real.exp (-(γ y + c)) = π y * Real.exp (-γ y) * Real.exp (-c) := by
    intro y
    rw [neg_add, Real.exp_add]
    ring
  simp only [h]
  rw [← Finset.sum_mul, mul_div_mul_right _ _ (Real.exp_pos (-c)).ne']

section TwoFactors

variable {α β : Type*} [Fintype α] [Fintype β] [Nonempty α] [Nonempty β]

omit [Fintype β] [Nonempty β] in
theorem exp_neg_softMin {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) (ψ : α × β → ℝ) (r : β) :
    Real.exp (-softMin π₁ ψ r) = ∑ a, π₁ a * Real.exp (-ψ (a, r)) := by
  unfold softMin
  rw [neg_neg, Real.exp_log (gibbsZ_pos hπ₁ (fun a => ψ (a, r)))]

omit [Fintype β] [Nonempty β] in
/-- The soft minimum of a function that is `d₂`-Lipschitz in the second coordinate is
`d₂`-Lipschitz (the theory division's `softmin_admissible`). -/
theorem softMin_admissible {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {d₂ : β → β → ℝ}
    {ψ : α × β → ℝ} (hψ : ∀ a r r', ψ (a, r) - ψ (a, r') ≤ d₂ r r') :
    Admissible d₂ (softMin π₁ ψ) := by
  intro r r'
  have hm := gibbsZ_pos hπ₁ (fun a => ψ (a, r))
  have hm' := gibbsZ_pos hπ₁ (fun a => ψ (a, r'))
  have hle : ∑ a, π₁ a * Real.exp (-ψ (a, r')) ≤
      Real.exp (d₂ r r') * ∑ a, π₁ a * Real.exp (-ψ (a, r)) := by
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum (fun a _ => ?_)
    have hexp : Real.exp (-ψ (a, r')) ≤ Real.exp (d₂ r r') * Real.exp (-ψ (a, r)) := by
      rw [← Real.exp_add, Real.exp_le_exp]
      linarith [hψ a r r']
    have := mul_le_mul_of_nonneg_left hexp (hπ₁ a).le
    linarith
  have hlog := Real.log_le_log hm' hle
  rw [Real.log_mul (Real.exp_pos _).ne' hm.ne', Real.log_exp] at hlog
  unfold softMin
  linarith

/-- The Gibbs law on a product factorises: marginal of the second coordinate (the Gibbs law of
the soft minimum) times the conditional law of the first. -/
theorem gibbsLaw_prod_apply {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {π₂ : β → ℝ}
    (hπ₂ : ∀ r, 0 < π₂ r) (ψ : α × β → ℝ) (a : α) (r : β) :
    gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) ψ (a, r) =
      gibbsLaw π₂ (softMin π₁ ψ) r * gibbsLaw π₁ (fun a => ψ (a, r)) a := by
  have hm : 0 < ∑ a, π₁ a * Real.exp (-ψ (a, r)) := gibbsZ_pos hπ₁ (fun a => ψ (a, r))
  have hZ : ∑ z : α × β, π₁ z.1 * π₂ z.2 * Real.exp (-ψ z) =
      ∑ r, π₂ r * Real.exp (-softMin π₁ ψ r) := by
    rw [Fintype.sum_prod_type, Finset.sum_comm]
    refine Finset.sum_congr rfl (fun r _ => ?_)
    rw [exp_neg_softMin hπ₁, Finset.mul_sum]
    refine Finset.sum_congr rfl (fun a _ => ?_)
    ring
  have hZpos : 0 < ∑ r, π₂ r * Real.exp (-softMin π₁ ψ r) := gibbsZ_pos hπ₂ _
  unfold gibbsLaw
  rw [hZ, exp_neg_softMin hπ₁]
  field_simp

/-- **Chain rule** for the relative entropy of a Gibbs law on `α × β` with respect to a product
vector `Q₁ ⊗ Q₂`: the divergence of the `β`-marginal plus the mean divergence of the
conditional laws on `α`. -/
theorem kl_gibbs_prod_eq {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {π₂ : β → ℝ}
    (hπ₂ : ∀ r, 0 < π₂ r) {Q₁ : α → ℝ} (hQ₁ : ∀ a, 0 < Q₁ a) {Q₂ : β → ℝ}
    (hQ₂ : ∀ r, 0 < Q₂ r) (ψ : α × β → ℝ) :
    klDivFin (gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) ψ) (fun z => Q₁ z.1 * Q₂ z.2) =
      klDivFin (gibbsLaw π₂ (softMin π₁ ψ)) Q₂ +
        ∑ r, gibbsLaw π₂ (softMin π₁ ψ) r *
          klDivFin (gibbsLaw π₁ (fun a => ψ (a, r))) Q₁ := by
  unfold klDivFin
  rw [Fintype.sum_prod_type, Finset.sum_comm, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun r _ => ?_)
  have hν : 0 < gibbsLaw π₂ (softMin π₁ ψ) r := gibbsLaw_pos hπ₂ _ r
  have hc : ∀ a, 0 < gibbsLaw π₁ (fun a => ψ (a, r)) a := fun a => gibbsLaw_pos hπ₁ _ a
  have hc1 : ∑ a, gibbsLaw π₁ (fun a => ψ (a, r)) a = 1 := sum_gibbsLaw hπ₁ _
  have hsum : ∑ a, gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) ψ (a, r) *
        (Real.log (gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) ψ (a, r)) -
          Real.log (Q₁ a * Q₂ r)) =
      ∑ a, (gibbsLaw π₁ (fun a => ψ (a, r)) a *
          (gibbsLaw π₂ (softMin π₁ ψ) r *
            (Real.log (gibbsLaw π₂ (softMin π₁ ψ) r) - Real.log (Q₂ r))) +
        gibbsLaw π₂ (softMin π₁ ψ) r *
          (gibbsLaw π₁ (fun a => ψ (a, r)) a *
            (Real.log (gibbsLaw π₁ (fun a => ψ (a, r)) a) - Real.log (Q₁ a)))) := by
    refine Finset.sum_congr rfl (fun a _ => ?_)
    rw [gibbsLaw_prod_apply hπ₁ hπ₂, Real.log_mul hν.ne' (hc a).ne',
      Real.log_mul (hQ₁ a).ne' (hQ₂ r).ne']
    ring
  refine hsum.trans ?_
  rw [Finset.sum_add_distrib, ← Finset.sum_mul, hc1, one_mul, ← Finset.mul_sum]

/-- **Tensorisation of the bound.**  If `KL(ν_γ ‖ Q₁) ≤ M₁` on the class of `d₁` and
`KL(ν_γ ‖ Q₂) ≤ M₂` on the class of `d₂`, then `KL(ν_ψ ‖ Q₁ ⊗ Q₂) ≤ M₁ + M₂` on the class of
`d₁ ⊕ d₂` on the product.  (The envelopes must vanish on the diagonal.) -/
theorem klBound_prod {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {π₂ : β → ℝ} (hπ₂ : ∀ r, 0 < π₂ r)
    {Q₁ : α → ℝ} (hQ₁ : ∀ a, 0 < Q₁ a) {Q₂ : β → ℝ} (hQ₂ : ∀ r, 0 < Q₂ r)
    {d₁ : α → α → ℝ} (hd₁ : ∀ a, d₁ a a ≤ 0) {d₂ : β → β → ℝ} (hd₂ : ∀ r, d₂ r r ≤ 0)
    {M₁ M₂ : ℝ} (h₁ : KLBound π₁ d₁ Q₁ M₁) (h₂ : KLBound π₂ d₂ Q₂ M₂) :
    KLBound (fun z : α × β => π₁ z.1 * π₂ z.2) (fun z z' => d₁ z.1 z'.1 + d₂ z.2 z'.2)
      (fun z => Q₁ z.1 * Q₂ z.2) (M₁ + M₂) := by
  intro ψ hψ
  rw [kl_gibbs_prod_eq hπ₁ hπ₂ hQ₁ hQ₂]
  have hA : Admissible d₂ (softMin π₁ ψ) := by
    refine softMin_admissible hπ₁ (fun a r r' => ?_)
    have := hψ (a, r) (a, r')
    simp only at this
    linarith [hd₁ a]
  have hB : ∀ r, Admissible d₁ (fun a => ψ (a, r)) := by
    intro r a a'
    have := hψ (a, r) (a', r)
    simp only at this
    linarith [hd₂ r]
  have h2 := h₂ _ hA
  have h1 : ∑ r, gibbsLaw π₂ (softMin π₁ ψ) r *
      klDivFin (gibbsLaw π₁ (fun a => ψ (a, r))) Q₁ ≤ M₁ := by
    calc ∑ r, gibbsLaw π₂ (softMin π₁ ψ) r * klDivFin (gibbsLaw π₁ (fun a => ψ (a, r))) Q₁
        ≤ ∑ r, gibbsLaw π₂ (softMin π₁ ψ) r * M₁ :=
          Finset.sum_le_sum (fun r _ =>
            mul_le_mul_of_nonneg_left (h₁ _ (hB r)) (gibbsLaw_pos hπ₂ _ r).le)
      _ = M₁ := by rw [← Finset.sum_mul, sum_gibbsLaw hπ₂, one_mul]
  linarith

/-- **Additivity at additive instances** (two factors):
`KL(ν_{γ₁ ⊕ γ₂} ‖ Q₁ ⊗ Q₂) = KL(ν_{γ₁} ‖ Q₁) + KL(ν_{γ₂} ‖ Q₂)`. -/
theorem kl_gibbs_prod_additive {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {π₂ : β → ℝ}
    (hπ₂ : ∀ r, 0 < π₂ r) {Q₁ : α → ℝ} (hQ₁ : ∀ a, 0 < Q₁ a) {Q₂ : β → ℝ}
    (hQ₂ : ∀ r, 0 < Q₂ r) (γ₁ : α → ℝ) (γ₂ : β → ℝ) :
    klDivFin (gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) (fun z => γ₁ z.1 + γ₂ z.2))
        (fun z => Q₁ z.1 * Q₂ z.2) =
      klDivFin (gibbsLaw π₁ γ₁) Q₁ + klDivFin (gibbsLaw π₂ γ₂) Q₂ := by
  rw [kl_gibbs_prod_eq hπ₁ hπ₂ hQ₁ hQ₂]
  have hsoft : softMin π₁ (fun z : α × β => γ₁ z.1 + γ₂ z.2) =
      fun r => γ₂ r + (-Real.log (∑ a, π₁ a * Real.exp (-γ₁ a))) := by
    funext r
    unfold softMin
    have h : ∀ a, π₁ a * Real.exp (-(γ₁ a + γ₂ r)) =
        Real.exp (-γ₂ r) * (π₁ a * Real.exp (-γ₁ a)) := by
      intro a
      rw [neg_add, Real.exp_add]
      ring
    simp only [h]
    rw [← Finset.mul_sum, Real.log_mul (Real.exp_pos _).ne' (gibbsZ_pos hπ₁ γ₁).ne',
      Real.log_exp]
    ring
  have hcond : ∀ r, gibbsLaw π₁ (fun a => γ₁ a + γ₂ r) = gibbsLaw π₁ γ₁ :=
    fun r => gibbsLaw_add_const π₁ γ₁ (γ₂ r)
  rw [hsoft, gibbsLaw_add_const]
  simp only [hcond]
  rw [← Finset.sum_mul, sum_gibbsLaw hπ₂, one_mul]
  ring

end TwoFactors

/-- Transport of a Gibbs law along an equivalence. -/
theorem gibbsLaw_equiv {X Y : Type*} [Fintype X] [Fintype Y] (e : Y ≃ X) (π ψ : X → ℝ)
    (y : Y) : gibbsLaw (fun y => π (e y)) (fun y => ψ (e y)) y = gibbsLaw π ψ (e y) := by
  unfold gibbsLaw
  rw [Equiv.sum_comp e (fun x => π x * Real.exp (-ψ x))]

/-- Transport of the relative entropy of a Gibbs law along an equivalence. -/
theorem klDivFin_gibbs_equiv {X Y : Type*} [Fintype X] [Fintype Y] (e : Y ≃ X)
    (π ψ Q : X → ℝ) :
    klDivFin (gibbsLaw (fun y => π (e y)) (fun y => ψ (e y))) (fun y => Q (e y)) =
      klDivFin (gibbsLaw π ψ) Q := by
  unfold klDivFin
  simp only [gibbsLaw_equiv]
  exact Equiv.sum_comp e (fun x => gibbsLaw π ψ x * (Real.log (gibbsLaw π ψ x) - Real.log (Q x)))

/-- Transport of a bound along an equivalence. -/
theorem klBound_equiv {X Y : Type*} [Fintype X] [Fintype Y] (e : Y ≃ X) {π : X → ℝ}
    {d : X → X → ℝ} {Q : X → ℝ} {M : ℝ} (h : KLBound π d Q M) :
    KLBound (fun y => π (e y)) (fun y y' => d (e y) (e y')) (fun y => Q (e y)) M := by
  intro ψ hψ
  have hadm : Admissible d (fun x => ψ (e.symm x)) := by
    intro x x'
    have := hψ (e.symm x) (e.symm x')
    simpa using this
  have h1 := h _ hadm
  rw [← klDivFin_gibbs_equiv e] at h1
  simpa using h1

/-- **Item 3, the inequality.**  On a product `∀ i : Fin n, S i` of finite alphabets with
positive site weights `π i`, envelopes `d i` vanishing on the diagonal and positive site
vectors `Q i`: if `M i` bounds `KL(π_γ ‖ Q i)` over the site class `L i`, then
`KL(ν_ψ ‖ ⊗ Q i) ≤ ∑_i M i` for every `ψ` in the class of `∑_i d i`. -/
theorem klBound_pi {n : ℕ} : ∀ (S : Fin n → Type u) [∀ i, Fintype (S i)] [∀ i, Nonempty (S i)]
    (π : ∀ i, S i → ℝ) (d : ∀ i, S i → S i → ℝ) (Q : ∀ i, S i → ℝ) (M : Fin n → ℝ),
    (∀ i s, 0 < π i s) → (∀ i s, 0 < Q i s) → (∀ i s, d i s s ≤ 0) →
    (∀ i, KLBound (π i) (d i) (Q i) (M i)) →
    KLBound (fun x : ∀ i, S i => ∏ i, π i (x i)) (fun x y => ∑ i, d i (x i) (y i))
      (fun x => ∏ i, Q i (x i)) (∑ i, M i) := by
  induction n with
  | zero =>
    intro S _ _ π d Q M _ _ _ _ ψ _
    have hsum : ∀ F : (∀ i : Fin 0, S i) → ℝ, ∑ x, F x = F default :=
      fun F => Fintype.sum_unique F
    have hg : gibbsLaw (fun x : ∀ i : Fin 0, S i => ∏ i, π i (x i)) ψ default = 1 := by
      unfold gibbsLaw
      rw [hsum]
      exact div_self (by simp)
    unfold klDivFin
    rw [hsum, hg]
    simp
  | succ n ih =>
    intro S _ _ π d Q M hπ hQ hd h
    have ih' := ih (fun i => S i.succ) (fun i => π i.succ) (fun i => d i.succ)
      (fun i => Q i.succ) (fun i => M i.succ) (fun i s => hπ i.succ s) (fun i s => hQ i.succ s)
      (fun i s => hd i.succ s) (fun i => h i.succ)
    have h2 := klBound_prod (hπ 0)
      (fun r : ∀ i : Fin n, S i.succ => Finset.prod_pos (fun i _ => hπ i.succ (r i)))
      (hQ 0) (fun r : ∀ i : Fin n, S i.succ => Finset.prod_pos (fun i _ => hQ i.succ (r i)))
      (hd 0) (fun r : ∀ i : Fin n, S i.succ => Finset.sum_nonpos (fun i _ => hd i.succ (r i)))
      (h 0) ih'
    have h3 := klBound_equiv (Fin.consEquiv S).symm h2
    have e1 : (fun x : ∀ i, S i => ∏ i, π i (x i)) =
        fun x => π 0 ((Fin.consEquiv S).symm x).1 *
          ∏ i : Fin n, π i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.prod_univ_succ]
      rfl
    have e2 : (fun x y : ∀ i, S i => ∑ i, d i (x i) (y i)) =
        fun x y => d 0 ((Fin.consEquiv S).symm x).1 ((Fin.consEquiv S).symm y).1 +
          ∑ i : Fin n, d i.succ (((Fin.consEquiv S).symm x).2 i)
            (((Fin.consEquiv S).symm y).2 i) := by
      funext x y
      rw [Fin.sum_univ_succ]
      rfl
    have e3 : (fun x : ∀ i, S i => ∏ i, Q i (x i)) =
        fun x => Q 0 ((Fin.consEquiv S).symm x).1 *
          ∏ i : Fin n, Q i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.prod_univ_succ]
      rfl
    rw [e1, e2, e3, Fin.sum_univ_succ]
    exact h3

/-- **Item 3, additive instances.**  For `ψ x = ∑_i γ i (x i)` the Gibbs law is the product of
the site Gibbs laws and `KL(ν_ψ ‖ ⊗ Q i) = ∑_i KL(π_{γ i} ‖ Q i)`. -/
theorem kl_additive_pi {n : ℕ} : ∀ (S : Fin n → Type u) [∀ i, Fintype (S i)]
    [∀ i, Nonempty (S i)] (π : ∀ i, S i → ℝ) (Q : ∀ i, S i → ℝ) (γ : ∀ i, S i → ℝ),
    (∀ i s, 0 < π i s) → (∀ i s, 0 < Q i s) →
    klDivFin (gibbsLaw (fun x : ∀ i, S i => ∏ i, π i (x i)) (fun x => ∑ i, γ i (x i)))
        (fun x => ∏ i, Q i (x i)) =
      ∑ i, klDivFin (gibbsLaw (π i) (γ i)) (Q i) := by
  induction n with
  | zero =>
    intro S _ _ π Q γ _ _
    have hsum : ∀ F : (∀ i : Fin 0, S i) → ℝ, ∑ x, F x = F default :=
      fun F => Fintype.sum_unique F
    have hg : gibbsLaw (fun x : ∀ i : Fin 0, S i => ∏ i, π i (x i))
        (fun x => ∑ i, γ i (x i)) default = 1 := by
      unfold gibbsLaw
      rw [hsum]
      exact div_self (by simp)
    unfold klDivFin
    rw [hsum, hg]
    simp
  | succ n ih =>
    intro S _ _ π Q γ hπ hQ
    have ih' := ih (fun i => S i.succ) (fun i => π i.succ) (fun i => Q i.succ)
      (fun i => γ i.succ) (fun i s => hπ i.succ s) (fun i s => hQ i.succ s)
    have h2 := kl_gibbs_prod_additive (hπ 0)
      (π₂ := fun r : ∀ i : Fin n, S i.succ => ∏ i, π i.succ (r i))
      (fun r => Finset.prod_pos (fun i _ => hπ i.succ (r i)))
      (hQ 0) (Q₂ := fun r : ∀ i : Fin n, S i.succ => ∏ i, Q i.succ (r i))
      (fun r => Finset.prod_pos (fun i _ => hQ i.succ (r i)))
      (γ 0) (fun r : ∀ i : Fin n, S i.succ => ∑ i, γ i.succ (r i))
    have h3 := klDivFin_gibbs_equiv (Fin.consEquiv S).symm
      (fun z : S 0 × (∀ i : Fin n, S i.succ) => π 0 z.1 * ∏ i, π i.succ (z.2 i))
      (fun z => γ 0 z.1 + ∑ i, γ i.succ (z.2 i))
      (fun z => Q 0 z.1 * ∏ i, Q i.succ (z.2 i))
    have e1 : (fun x : ∀ i, S i => ∏ i, π i (x i)) =
        fun x => π 0 ((Fin.consEquiv S).symm x).1 *
          ∏ i : Fin n, π i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.prod_univ_succ]
      rfl
    have e2 : (fun x : ∀ i, S i => ∑ i, γ i (x i)) =
        fun x => γ 0 ((Fin.consEquiv S).symm x).1 +
          ∑ i : Fin n, γ i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.sum_univ_succ]
      rfl
    have e3 : (fun x : ∀ i, S i => ∏ i, Q i (x i)) =
        fun x => Q 0 ((Fin.consEquiv S).symm x).1 *
          ∏ i : Fin n, Q i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.prod_univ_succ]
      rfl
    rw [e1, e2, e3, h3, h2, ih', Fin.sum_univ_succ]

/-- **Item 3, as a maximum.**  If, for every site, `M i` is the greatest value of
`KL(π_γ ‖ Q i)` over the site class `L i`, then `∑_i M i` is the greatest value of
`KL(ν_ψ ‖ ⊗ Q i)` over the class `𝒞` of the product, and it is attained at an additive
instance. -/
theorem kl_pi_isGreatest {n : ℕ} (S : Fin n → Type u) [∀ i, Fintype (S i)]
    [∀ i, Nonempty (S i)] (π : ∀ i, S i → ℝ) (d : ∀ i, S i → S i → ℝ) (Q : ∀ i, S i → ℝ)
    (M : Fin n → ℝ) (hπ : ∀ i s, 0 < π i s) (hQ : ∀ i s, 0 < Q i s) (hd : ∀ i s, d i s s ≤ 0)
    (hM : ∀ i, IsGreatest
      {m | ∃ γ, Admissible (d i) γ ∧ klDivFin (gibbsLaw (π i) γ) (Q i) = m} (M i)) :
    IsGreatest {m | ∃ ψ, Admissible (fun x y : ∀ i, S i => ∑ i, d i (x i) (y i)) ψ ∧
        klDivFin (gibbsLaw (fun x : ∀ i, S i => ∏ i, π i (x i)) ψ) (fun x => ∏ i, Q i (x i)) = m}
      (∑ i, M i) := by
  constructor
  · choose γ hγ hγM using fun i => (hM i).1
    refine ⟨fun x => ∑ i, γ i (x i), ?_, ?_⟩
    · intro x y
      rw [← Finset.sum_sub_distrib]
      exact Finset.sum_le_sum (fun i _ => hγ i (x i) (y i))
    · rw [kl_additive_pi S π Q γ hπ hQ]
      exact Finset.sum_congr rfl (fun i _ => hγM i)
  · rintro m ⟨ψ, hψ, rfl⟩
    exact klBound_pi S π d Q M hπ hQ hd (fun i γ hγ => (hM i).2 ⟨γ, hγ, rfl⟩) ψ hψ

end ChainRule

/-! ### Item 1, the vertices: extreme points of the window and of the normalised class

The class `{γ : γ a - γ b ≤ d a b}` has no extreme points (`lipClass_extremePoints_eq_empty`).
Normalised at a base point `a₀` (`lipNorm d a₀ = {γ admissible, γ a₀ = 0}`) it does, and they
correspond to the extreme points of the window:
`extremePoints (window π d) = gibbsLaw π '' extremePoints (lipNorm d a₀)`.
The proof uses the *tight* pairs `γ a - γ b = d a b` (equivalently
`π a p b = e^{d a b} π b p a`): a perturbation that is constant along tight pairs can be added
and subtracted with a small coefficient without leaving the set. -/

section Vertices

variable {α : Type*} [Fintype α]

/-- The Lipschitz class normalised at the base point `a₀`. -/
def lipNorm (d : α → α → ℝ) (a₀ : α) : Set (α → ℝ) := {γ | Admissible d γ ∧ γ a₀ = 0}

/-- Finitely many strict slacks leave room for a common positive scale. -/
theorem exists_pos_scale {κ : Type*} [Fintype κ] [Nonempty κ] (slack bound : κ → ℝ)
    (hb : ∀ k, 0 ≤ bound k) :
    ∃ ε : ℝ, 0 < ε ∧ ∀ k, 0 < slack k → ε * bound k ≤ slack k := by
  classical
  set f : κ → ℝ := fun k => if 0 < slack k then slack k / (1 + bound k) else 1 with hf
  have hfpos : ∀ k, 0 < f k := by
    intro k
    rw [hf]
    by_cases h : 0 < slack k
    · have h2 : 0 < 1 + bound k := by linarith [hb k]
      simpa [h] using div_pos h h2
    · simp [h]
  obtain ⟨k₀, -, hmin⟩ := Finset.exists_min_image Finset.univ f Finset.univ_nonempty
  refine ⟨f k₀, hfpos k₀, fun k hk => ?_⟩
  have hfk : f k = slack k / (1 + bound k) := by
    rw [hf]
    exact if_pos hk
  have h1 : f k₀ ≤ slack k / (1 + bound k) := hfk ▸ hmin k (Finset.mem_univ k)
  have h2 : 0 < 1 + bound k := by linarith [hb k]
  rw [le_div_iff₀ h2] at h1
  nlinarith [hfpos k₀, hb k]

/-- If a proper convex combination of two numbers `≤ c` equals `c`, both equal `c`. -/
theorem eq_of_convex_comb_eq {s t x₁ x₂ c : ℝ} (hs : 0 < s) (ht : 0 < t) (hst : s + t = 1)
    (h₁ : x₁ ≤ c) (h₂ : x₂ ≤ c) (h : s * x₁ + t * x₂ = c) : x₁ = c ∧ x₂ = c := by
  have hc : (s + t) * c = c := by rw [hst, one_mul]
  have h4 : 0 ≤ s * (c - x₁) := mul_nonneg hs.le (by linarith)
  have h5 : 0 ≤ t * (c - x₂) := mul_nonneg ht.le (by linarith)
  have h6 : s * (c - x₁) = 0 := by nlinarith
  have h7 : t * (c - x₂) = 0 := by nlinarith
  have h8 := (mul_eq_zero.1 h6).resolve_left hs.ne'
  have h9 := (mul_eq_zero.1 h7).resolve_left ht.ne'
  exact ⟨by linarith, by linarith⟩

/-- The slack of a window constraint at a Gibbs law. -/
theorem window_slack_eq [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (γ : α → ℝ)
    (d : α → α → ℝ) (a b : α) :
    Real.exp (d a b) * π b * gibbsLaw π γ a - π a * gibbsLaw π γ b =
      π a * π b / (∑ c, π c * Real.exp (-γ c)) *
        (Real.exp (d a b - γ a) - Real.exp (-γ b)) := by
  have hZ := gibbsZ_pos hπ γ
  unfold gibbsLaw
  rw [sub_eq_add_neg (d a b) (γ a), Real.exp_add]
  field_simp

/-- A window constraint is tight at `π_γ` iff the corresponding Lipschitz constraint is tight
at `γ`. -/
theorem window_tight_iff [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (γ : α → ℝ)
    (d : α → α → ℝ) (a b : α) :
    π a * gibbsLaw π γ b = Real.exp (d a b) * π b * gibbsLaw π γ a ↔ γ a - γ b = d a b := by
  have hZ := gibbsZ_pos hπ γ
  have hs := window_slack_eq hπ γ d a b
  have hc : 0 < π a * π b / (∑ c, π c * Real.exp (-γ c)) :=
    div_pos (mul_pos (hπ a) (hπ b)) hZ
  constructor
  · intro h
    have h0 : π a * π b / (∑ c, π c * Real.exp (-γ c)) *
        (Real.exp (d a b - γ a) - Real.exp (-γ b)) = 0 := by
      rw [← hs]
      linarith
    have h1 := (mul_eq_zero.1 h0).resolve_left hc.ne'
    have h2 : Real.exp (d a b - γ a) = Real.exp (-γ b) := by linarith
    have h3 := Real.exp_injective h2
    linarith
  · intro h
    have h2 : Real.exp (d a b - γ a) = Real.exp (-γ b) := by
      congr 1
      linarith
    rw [h2, sub_self, mul_zero] at hs
    linarith

omit [Fintype α] in
/-- A direction that vanishes at the base point and is constant along tight pairs can be added
to and subtracted from `γ` with a small positive coefficient inside the normalised class. -/
theorem perturb_mem_lipNorm [Finite α] [Nonempty α] {d : α → α → ℝ} {a₀ : α} {γ θ : α → ℝ}
    (hγ : γ ∈ lipNorm d a₀) (hθ0 : θ a₀ = 0)
    (hθtight : ∀ a b, γ a - γ b = d a b → θ a = θ b) :
    ∃ ε : ℝ, 0 < ε ∧ (fun a => γ a + ε * θ a) ∈ lipNorm d a₀ ∧
      (fun a => γ a - ε * θ a) ∈ lipNorm d a₀ := by
  have := Fintype.ofFinite α
  obtain ⟨hadm, hγ0⟩ := hγ
  obtain ⟨ε, hε, hεb⟩ := exists_pos_scale (κ := α × α)
    (fun k => d k.1 k.2 - (γ k.1 - γ k.2)) (fun k => |θ k.1 - θ k.2|) (fun k => abs_nonneg _)
  have hbound : ∀ a b, ε * |θ a - θ b| ≤ d a b - (γ a - γ b) := by
    intro a b
    have hslack : 0 ≤ d a b - (γ a - γ b) := by linarith [hadm a b]
    rcases eq_or_lt_of_le hslack with h0 | hpos
    · have hθ : θ a = θ b := hθtight a b (by linarith)
      rw [hθ, sub_self, abs_zero, mul_zero]
      exact hslack
    · exact hεb (a, b) hpos
  refine ⟨ε, hε, ⟨fun a b => ?_, ?_⟩, ⟨fun a b => ?_, ?_⟩⟩
  · have h1 := hbound a b
    have h2 := mul_le_mul_of_nonneg_left (le_abs_self (θ a - θ b)) hε.le
    simp only
    linarith
  · simp [hγ0, hθ0]
  · have h1 := hbound a b
    have h2 := mul_le_mul_of_nonneg_left (neg_le_abs (θ a - θ b)) hε.le
    simp only
    linarith
  · simp [hγ0, hθ0]

/-- A direction of mean zero that is constant along tight pairs can be added to and subtracted
from `p` (multiplicatively) with a small positive coefficient inside the window. -/
theorem perturb_mem_window [Nonempty α] {π : α → ℝ} {d : α → α → ℝ} {p τ : α → ℝ}
    (hp : p ∈ window π d) (hτsum : ∑ a, p a * τ a = 0)
    (hτtight : ∀ a b, π a * p b = Real.exp (d a b) * π b * p a → τ a = τ b) :
    ∃ ε : ℝ, 0 < ε ∧ (fun a => p a * (1 + ε * τ a)) ∈ window π d ∧
      (fun a => p a * (1 - ε * τ a)) ∈ window π d := by
  obtain ⟨hp0, hp1, hpw⟩ := hp
  obtain ⟨ε₁, hε₁, hb₁⟩ := exists_pos_scale (κ := α × α)
    (fun k => Real.exp (d k.1 k.2) * π k.2 * p k.1 - π k.1 * p k.2)
    (fun k => |π k.1 * p k.2 * τ k.2 - Real.exp (d k.1 k.2) * π k.2 * p k.1 * τ k.1|)
    (fun k => abs_nonneg _)
  obtain ⟨ε₂, hε₂, hb₂⟩ := exists_pos_scale (κ := α) (fun _ => (1 : ℝ)) (fun a => |τ a|)
    (fun a => abs_nonneg _)
  have hε : 0 < min ε₁ ε₂ := lt_min hε₁ hε₂
  have hpos : ∀ a, min ε₁ ε₂ * |τ a| ≤ 1 := fun a =>
    le_trans (mul_le_mul_of_nonneg_right (min_le_right _ _) (abs_nonneg _)) (hb₂ a one_pos)
  have hwin : ∀ a b, min ε₁ ε₂ *
      |π a * p b * τ b - Real.exp (d a b) * π b * p a * τ a| ≤
        Real.exp (d a b) * π b * p a - π a * p b := by
    intro a b
    have hslack : 0 ≤ Real.exp (d a b) * π b * p a - π a * p b := by linarith [hpw a b]
    rcases eq_or_lt_of_le hslack with h0 | hposs
    · have hτ : τ a = τ b := hτtight a b (by linarith)
      have hz : π a * p b * τ b - Real.exp (d a b) * π b * p a * τ a = 0 := by
        have he : π a * p b = Real.exp (d a b) * π b * p a := by linarith
        rw [hτ, he]
        ring
      rw [hz, abs_zero, mul_zero]
      exact hslack
    · exact le_trans (mul_le_mul_of_nonneg_right (min_le_left _ _) (abs_nonneg _))
        (hb₁ (a, b) hposs)
  refine ⟨min ε₁ ε₂, hε, ⟨fun a => ?_, ?_, fun a b => ?_⟩, ⟨fun a => ?_, ?_, fun a b => ?_⟩⟩
  · have h1 := hpos a
    have h2 := mul_le_mul_of_nonneg_left (neg_le_abs (τ a)) hε.le
    exact mul_nonneg (hp0 a) (by linarith)
  · have e : ∑ a, p a * (1 + min ε₁ ε₂ * τ a) = ∑ a, p a + min ε₁ ε₂ * ∑ a, p a * τ a := by
      rw [Finset.mul_sum, ← Finset.sum_add_distrib]
      exact Finset.sum_congr rfl (fun a _ => by ring)
    rw [e, hp1, hτsum]
    ring
  · have h1 := hwin a b
    have h2 := mul_le_mul_of_nonneg_left
      (le_abs_self (π a * p b * τ b - Real.exp (d a b) * π b * p a * τ a)) hε.le
    simp only
    linarith
  · have h1 := hpos a
    have h2 := mul_le_mul_of_nonneg_left (le_abs_self (τ a)) hε.le
    exact mul_nonneg (hp0 a) (by linarith)
  · have e : ∑ a, p a * (1 - min ε₁ ε₂ * τ a) = ∑ a, p a - min ε₁ ε₂ * ∑ a, p a * τ a := by
      rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl (fun a _ => by ring)
    rw [e, hp1, hτsum]
    ring
  · have h1 := hwin a b
    have h2 := mul_le_mul_of_nonneg_left
      (neg_le_abs (π a * p b * τ b - Real.exp (d a b) * π b * p a * τ a)) hε.le
    simp only
    linarith

/-- If `γ` is an extreme point of the normalised class, `π_γ` is an extreme point of the
window. -/
theorem gibbsLaw_extreme_of_extreme [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a)
    {d : α → α → ℝ} {a₀ : α} {γ : α → ℝ} (hγ : γ ∈ Set.extremePoints ℝ (lipNorm d a₀)) :
    gibbsLaw π γ ∈ Set.extremePoints ℝ (window π d) := by
  rw [mem_extremePoints] at hγ ⊢
  obtain ⟨hγmem, hext⟩ := hγ
  have hadm : Admissible d γ := hγmem.1
  refine ⟨gibbsLaw_mem_window hπ hadm, ?_⟩
  have main : ∀ q₁ ∈ window π d, ∀ q₂ ∈ window π d, ∀ s t : ℝ, 0 < s → 0 < t → s + t = 1 →
      s • q₁ + t • q₂ = gibbsLaw π γ → q₁ = gibbsLaw π γ := by
    intro q₁ hq₁ q₂ hq₂ s t hs ht hst hcomb
    have hp_pos : ∀ a, 0 < gibbsLaw π γ a := gibbsLaw_pos hπ γ
    have hcomb' : ∀ a, s * q₁ a + t * q₂ a = gibbsLaw π γ a := fun a => by
      have := congrFun hcomb a
      simpa using this
    -- tight pairs of `γ` are tight for `q₁`
    have htight : ∀ a b, γ a - γ b = d a b →
        π a * q₁ b = Real.exp (d a b) * π b * q₁ a := by
      intro a b hab
      have hp := (window_tight_iff hπ γ d a b).2 hab
      have h1 := hq₁.2.2 a b
      have h2 := hq₂.2.2 a b
      rw [← hcomb' a, ← hcomb' b] at hp
      have h3 := eq_of_convex_comb_eq (c := 0) hs ht hst
        (x₁ := π a * q₁ b - Real.exp (d a b) * π b * q₁ a)
        (x₂ := π a * q₂ b - Real.exp (d a b) * π b * q₂ a) (by linarith) (by linarith)
        (by linarith)
      linarith [h3.1]
    -- the ratio `q₁ / p`, normalised at the base point
    have hratio : ∀ a b, γ a - γ b = d a b →
        q₁ a / gibbsLaw π γ a = q₁ b / gibbsLaw π γ b := by
      intro a b hab
      have hp := (window_tight_iff hπ γ d a b).2 hab
      have hq := htight a b hab
      have hπa := (hπ a).ne'
      have e1 : gibbsLaw π γ b = Real.exp (d a b) * π b * gibbsLaw π γ a / π a := by
        rw [eq_div_iff hπa]
        linarith
      have e2 : q₁ b = Real.exp (d a b) * π b * q₁ a / π a := by
        rw [eq_div_iff hπa]
        linarith
      have hπb := (hπ b).ne'
      have hE := (Real.exp_pos (d a b)).ne'
      have hpa := (hp_pos a).ne'
      rw [e2, e1]
      field_simp
    have hθzero : ∀ a, q₁ a / gibbsLaw π γ a - q₁ a₀ / gibbsLaw π γ a₀ = 0 := by
      by_contra hne
      obtain ⟨ε, hε, hplus, hminus⟩ := perturb_mem_lipNorm hγmem
        (θ := fun a => q₁ a / gibbsLaw π γ a - q₁ a₀ / gibbsLaw π γ a₀) (by simp)
        (fun a b hab => by rw [hratio a b hab])
      have hseg : γ ∈ openSegment ℝ
          (fun a => γ a + ε * (q₁ a / gibbsLaw π γ a - q₁ a₀ / gibbsLaw π γ a₀))
          (fun a => γ a - ε * (q₁ a / gibbsLaw π γ a - q₁ a₀ / gibbsLaw π γ a₀)) := by
        refine ⟨1 / 2, 1 / 2, by norm_num, by norm_num, by norm_num, ?_⟩
        funext a
        simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
        ring
      have h := (hext _ hplus _ hminus hseg).1
      apply hne
      intro a
      have ha : γ a + ε * (q₁ a / gibbsLaw π γ a - q₁ a₀ / gibbsLaw π γ a₀) = γ a :=
        congrFun h a
      have hz : ε * (q₁ a / gibbsLaw π γ a - q₁ a₀ / gibbsLaw π γ a₀) = 0 := by linarith
      exact (mul_eq_zero.1 hz).resolve_left hε.ne'
    have hc : ∀ a, q₁ a = (q₁ a₀ / gibbsLaw π γ a₀) * gibbsLaw π γ a := by
      intro a
      have h := hθzero a
      have hpa := (hp_pos a).ne'
      have h' : q₁ a / gibbsLaw π γ a = q₁ a₀ / gibbsLaw π γ a₀ := by linarith
      rw [← h', div_mul_cancel₀ _ hpa]
    have hconst : q₁ a₀ / gibbsLaw π γ a₀ = 1 := by
      have hsum : ∑ a, q₁ a = (q₁ a₀ / gibbsLaw π γ a₀) * ∑ a, gibbsLaw π γ a := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl (fun a _ => hc a)
      rw [hq₁.2.1, sum_gibbsLaw hπ γ, mul_one] at hsum
      exact hsum.symm
    funext a
    rw [hc a, hconst, one_mul]
  intro p₁ hp₁ p₂ hp₂ hseg
  obtain ⟨s, t, hs, ht, hst, hcomb⟩ := hseg
  exact ⟨main p₁ hp₁ p₂ hp₂ s t hs ht hst hcomb,
    main p₂ hp₂ p₁ hp₁ t s ht hs (by linarith) (by rw [add_comm]; exact hcomb)⟩

/-- If `π_γ` is an extreme point of the window, `γ` is an extreme point of the normalised
class. -/
theorem extreme_of_gibbsLaw_extreme [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a)
    {d : α → α → ℝ} {a₀ : α} {γ : α → ℝ} (hγmem : γ ∈ lipNorm d a₀)
    (hp : gibbsLaw π γ ∈ Set.extremePoints ℝ (window π d)) :
    γ ∈ Set.extremePoints ℝ (lipNorm d a₀) := by
  rw [mem_extremePoints] at hp ⊢
  obtain ⟨hpw, hext⟩ := hp
  refine ⟨hγmem, ?_⟩
  have hp_pos : ∀ a, 0 < gibbsLaw π γ a := gibbsLaw_pos hπ γ
  have main : ∀ γ₁ ∈ lipNorm d a₀, ∀ γ₂ ∈ lipNorm d a₀, ∀ s t : ℝ, 0 < s → 0 < t → s + t = 1 →
      s • γ₁ + t • γ₂ = γ → γ₁ = γ₂ := by
    intro γ₁ hγ₁ γ₂ hγ₂ s t hs ht hst hcomb
    have hcomb' : ∀ a, s * γ₁ a + t * γ₂ a = γ a := fun a => by
      have := congrFun hcomb a
      simpa using this
    -- tight pairs of `γ` are tight for `γ₁` and `γ₂`
    have htight : ∀ a b, γ a - γ b = d a b → γ₁ a - γ₂ a = γ₁ b - γ₂ b := by
      intro a b hab
      have h3 := eq_of_convex_comb_eq (c := d a b) hs ht hst
        (x₁ := γ₁ a - γ₁ b) (x₂ := γ₂ a - γ₂ b) (hγ₁.1 a b) (hγ₂.1 a b)
        (by rw [← hab, ← hcomb' a, ← hcomb' b]; ring)
      linarith [h3.1, h3.2]
    -- the mean of the direction under `p`
    set c : ℝ := ∑ a, gibbsLaw π γ a * (γ₁ a - γ₂ a) with hcdef
    have hτsum : ∑ a, gibbsLaw π γ a * ((γ₁ a - γ₂ a) - c) = 0 := by
      have e : ∑ a, gibbsLaw π γ a * ((γ₁ a - γ₂ a) - c) =
          ∑ a, gibbsLaw π γ a * (γ₁ a - γ₂ a) - c * ∑ a, gibbsLaw π γ a := by
        rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
        exact Finset.sum_congr rfl (fun a _ => by ring)
      rw [e, sum_gibbsLaw hπ γ, mul_one, ← hcdef, sub_self]
    obtain ⟨ε, hε, hplus, hminus⟩ := perturb_mem_window hpw
      (τ := fun a => (γ₁ a - γ₂ a) - c) hτsum
      (fun a b hab => by
        have := htight a b ((window_tight_iff hπ γ d a b).1 hab)
        linarith)
    have hseg : gibbsLaw π γ ∈ openSegment ℝ
        (fun a => gibbsLaw π γ a * (1 + ε * ((γ₁ a - γ₂ a) - c)))
        (fun a => gibbsLaw π γ a * (1 - ε * ((γ₁ a - γ₂ a) - c))) := by
      refine ⟨1 / 2, 1 / 2, by norm_num, by norm_num, by norm_num, ?_⟩
      funext a
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      ring
    have h := (hext _ hplus _ hminus hseg).1
    have hconst : ∀ a, γ₁ a - γ₂ a = c := by
      intro a
      have ha : gibbsLaw π γ a * (1 + ε * ((γ₁ a - γ₂ a) - c)) = gibbsLaw π γ a :=
        congrFun h a
      have hz : gibbsLaw π γ a * (ε * ((γ₁ a - γ₂ a) - c)) = 0 := by linarith
      have hz' := (mul_eq_zero.1 hz).resolve_left (hp_pos a).ne'
      have hz'' := (mul_eq_zero.1 hz').resolve_left hε.ne'
      linarith
    have hc0 : c = 0 := by
      have := hconst a₀
      rw [hγ₁.2, hγ₂.2, sub_self] at this
      exact this.symm
    funext a
    have := hconst a
    linarith
  intro γ₁ hγ₁ γ₂ hγ₂ hseg
  obtain ⟨s, t, hs, ht, hst, hcomb⟩ := hseg
  have heq := main γ₁ hγ₁ γ₂ hγ₂ s t hs ht hst hcomb
  have h1 : γ₁ = γ := by
    rw [← hcomb, ← heq]
    funext a
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    have : (s + t) * γ₁ a = γ₁ a := by rw [hst, one_mul]
    linarith
  exact ⟨h1, heq ▸ h1⟩

/-- **Item 1, the vertex statement, corrected**: the extreme points of the window are exactly
the Gibbs laws of the extreme points of the Lipschitz class normalised at a base point. -/
theorem extremePoints_window_eq [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a)
    (d : α → α → ℝ) (a₀ : α) :
    Set.extremePoints ℝ (window π d) = gibbsLaw π '' Set.extremePoints ℝ (lipNorm d a₀) := by
  ext p
  constructor
  · intro hp
    obtain ⟨γ', hγ', rfl⟩ := exists_gibbsLaw_of_mem_window hπ hp.1
    have hnorm : (fun a => γ' a + -γ' a₀) ∈ lipNorm d a₀ := by
      refine ⟨fun a b => ?_, by simp⟩
      have := hγ' a b
      simp only
      linarith
    have heq : gibbsLaw π (fun a => γ' a + -γ' a₀) = gibbsLaw π γ' :=
      gibbsLaw_add_const π γ' (-γ' a₀)
    refine ⟨fun a => γ' a + -γ' a₀, ?_, heq⟩
    exact extreme_of_gibbsLaw_extreme hπ hnorm (heq ▸ hp)
  · rintro ⟨γ, hγ, rfl⟩
    exact gibbsLaw_extreme_of_extreme hπ hγ

end Vertices

/-! ### Item 3 with vertex labels: a convex function on the window is bounded by its values at
the vertex laws -/

section VertexBound

universe u

variable {α : Type*} [Fintype α]

/-- The window is compact. -/
theorem isCompact_window (π : α → ℝ) (d : α → α → ℝ) : IsCompact (window π d) := by
  have hbox : IsCompact (Set.univ.pi (fun _ : α => Set.Icc (0 : ℝ) 1)) :=
    isCompact_univ_pi (fun _ => isCompact_Icc)
  refine hbox.of_isClosed_subset ?_ ?_
  · have h1 : IsClosed {p : α → ℝ | ∀ a, 0 ≤ p a} := by
      rw [Set.setOf_forall]
      exact isClosed_iInter (fun a => isClosed_le continuous_const (continuous_apply a))
    have h2 : IsClosed {p : α → ℝ | ∑ a, p a = 1} :=
      isClosed_eq (continuous_finsetSum _ (fun a _ => continuous_apply a)) continuous_const
    have h3 : IsClosed {p : α → ℝ | ∀ a b, π a * p b ≤ Real.exp (d a b) * π b * p a} := by
      rw [Set.setOf_forall]
      refine isClosed_iInter (fun a => ?_)
      rw [Set.setOf_forall]
      exact isClosed_iInter (fun b =>
        isClosed_le (continuous_const.mul (continuous_apply b))
          (continuous_const.mul (continuous_apply a)))
    exact h1.inter (h2.inter h3)
  · intro p hp
    obtain ⟨hp0, hp1, _⟩ := hp
    rw [Set.mem_univ_pi]
    intro a
    refine ⟨hp0 a, ?_⟩
    calc p a ≤ ∑ b, p b := Finset.single_le_sum (fun b _ => hp0 b) (Finset.mem_univ a)
      _ = 1 := hp1

/-- `p ↦ KL(p ‖ Q)` is convex on the window. -/
theorem klDivFin_convexOn_window (π : α → ℝ) (d : α → α → ℝ) (Q : α → ℝ) :
    ConvexOn ℝ (window π d) (fun p => klDivFin p Q) := by
  refine ⟨window_convex π d, ?_⟩
  intro p hp q hq s t hs ht hst
  unfold klDivFin
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_le_sum (fun a _ => ?_)
  have hc := Real.convexOn_mul_log.2 (show p a ∈ Set.Ici (0 : ℝ) from hp.1 a)
    (show q a ∈ Set.Ici (0 : ℝ) from hq.1 a) hs ht hst
  simp only [smul_eq_mul] at hc
  linarith

/-- `p ↦ KL(p ‖ Q)` is continuous (with the convention `0 log 0 = 0`). -/
theorem continuous_klDivFin (Q : α → ℝ) : Continuous (fun p : α → ℝ => klDivFin p Q) := by
  have e : (fun p : α → ℝ => klDivFin p Q) =
      fun p => ∑ a, (p a * Real.log (p a) - p a * Real.log (Q a)) := by
    funext p
    unfold klDivFin
    exact Finset.sum_congr rfl (fun a _ => by ring)
  rw [e]
  exact continuous_finsetSum _ (fun a _ =>
    (Real.continuous_mul_log.comp (continuous_apply a)).sub
      ((continuous_apply a).mul continuous_const))

/-- **Vertex labels suffice.**  If `KL(π_γ ‖ Q) ≤ M` at every extreme point `γ` of the
normalised Lipschitz class, then `KL(π_γ ‖ Q) ≤ M` on the whole class (Krein–Milman, convexity
and continuity of the divergence, and the vertex correspondence). -/
theorem klBound_of_vertices [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (d : α → α → ℝ)
    (a₀ : α) (Q : α → ℝ) {M : ℝ}
    (hM : ∀ γ ∈ Set.extremePoints ℝ (lipNorm d a₀), klDivFin (gibbsLaw π γ) Q ≤ M) :
    KLBound π d Q M := by
  intro γ hγ
  have hmem : gibbsLaw π γ ∈ window π d := gibbsLaw_mem_window hπ hγ
  have hKM := closure_convexHull_extremePoints (isCompact_window π d) (window_convex π d)
  have hclosed : IsClosed {p : α → ℝ | klDivFin p Q ≤ M} :=
    isClosed_le (continuous_klDivFin Q) continuous_const
  have hsub : convexHull ℝ (Set.extremePoints ℝ (window π d)) ⊆
      {p : α → ℝ | klDivFin p Q ≤ M} := by
    intro p hp
    obtain ⟨y, hy, hle⟩ := (klDivFin_convexOn_window π d Q).exists_ge_of_mem_convexHull
      extremePoints_subset hp
    rw [extremePoints_window_eq hπ d a₀] at hy
    obtain ⟨γ', hγ', rfl⟩ := hy
    exact le_trans hle (hM γ' hγ')
  have hall := closure_minimal hsub hclosed
  rw [hKM] at hall
  exact hall hmem

/-- **Item 3, the inequality with vertex labels**: if `M i` bounds `KL(π_φ ‖ Q i)` over the
vertices `φ` of the (normalised) site class, then `KL(ν_ψ ‖ ⊗ Q i) ≤ ∑_i M i` for every `ψ` in
the class of the product. -/
theorem klBound_pi_of_vertices {n : ℕ} (S : Fin n → Type u) [∀ i, Fintype (S i)]
    [∀ i, Nonempty (S i)] (π : ∀ i, S i → ℝ) (d : ∀ i, S i → S i → ℝ) (Q : ∀ i, S i → ℝ)
    (M : Fin n → ℝ) (a₀ : ∀ i, S i) (hπ : ∀ i s, 0 < π i s) (hQ : ∀ i s, 0 < Q i s)
    (hd : ∀ i s, d i s s ≤ 0)
    (hM : ∀ i, ∀ γ ∈ Set.extremePoints ℝ (lipNorm (d i) (a₀ i)),
      klDivFin (gibbsLaw (π i) γ) (Q i) ≤ M i) :
    KLBound (fun x : ∀ i, S i => ∏ i, π i (x i)) (fun x y => ∑ i, d i (x i) (y i))
      (fun x => ∏ i, Q i (x i)) (∑ i, M i) :=
  klBound_pi S π d Q M hπ hQ hd
    (fun i => klBound_of_vertices (hπ i) (d i) (a₀ i) (Q i) (hM i))

/-- The site maximum exists: `KL(π_γ ‖ Q)` attains a greatest value over a non-empty Lipschitz
class (compactness of the window, continuity of the divergence). -/
theorem exists_site_max [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (d : α → α → ℝ)
    (Q : α → ℝ) (hne : ∃ γ, Admissible d γ) :
    ∃ M, IsGreatest {m | ∃ γ, Admissible d γ ∧ klDivFin (gibbsLaw π γ) Q = m} M := by
  obtain ⟨γ₀, hγ₀⟩ := hne
  have hne' : (window π d).Nonempty := ⟨_, gibbsLaw_mem_window hπ hγ₀⟩
  obtain ⟨p, hp, hmax⟩ := (isCompact_window π d).exists_isMaxOn hne'
    (continuous_klDivFin Q).continuousOn
  obtain ⟨γ, hγ, rfl⟩ := exists_gibbsLaw_of_mem_window hπ hp
  refine ⟨klDivFin (gibbsLaw π γ) Q, ⟨γ, hγ, rfl⟩, ?_⟩
  rintro m ⟨γ', hγ', rfl⟩
  exact (isMaxOn_iff.1 hmax) _ (gibbsLaw_mem_window hπ hγ')

/-- **Item 3, as a maximum, without hypotheses on the site maxima**: for non-empty site classes
(e.g. `d i ≥ 0`) with envelopes vanishing on the diagonal, the site maxima `M i` exist, and
`∑_i M i` is the greatest value of `KL(ν_ψ ‖ ⊗ Q i)` over the class of the product. -/
theorem kl_pi_exists_isGreatest {n : ℕ} (S : Fin n → Type u) [∀ i, Fintype (S i)]
    [∀ i, Nonempty (S i)] (π : ∀ i, S i → ℝ) (d : ∀ i, S i → S i → ℝ) (Q : ∀ i, S i → ℝ)
    (hπ : ∀ i s, 0 < π i s) (hQ : ∀ i s, 0 < Q i s) (hd : ∀ i s, d i s s ≤ 0)
    (hne : ∀ i, ∃ γ, Admissible (d i) γ) :
    ∃ M : Fin n → ℝ,
      (∀ i, IsGreatest
        {m | ∃ γ, Admissible (d i) γ ∧ klDivFin (gibbsLaw (π i) γ) (Q i) = m} (M i)) ∧
      IsGreatest {m | ∃ ψ, Admissible (fun x y : ∀ i, S i => ∑ i, d i (x i) (y i)) ψ ∧
        klDivFin (gibbsLaw (fun x : ∀ i, S i => ∏ i, π i (x i)) ψ)
          (fun x => ∏ i, Q i (x i)) = m} (∑ i, M i) := by
  choose M hM using fun i => exists_site_max (hπ i) (d i) (Q i) (hne i)
  exact ⟨M, hM, kl_pi_isGreatest S π d Q M hπ hQ hd hM⟩

end VertexBound

end ScienceL2

end

#print axioms ScienceL2.gibbsZ_pos
#print axioms ScienceL2.gibbsLaw_pos
#print axioms ScienceL2.sum_gibbsLaw
#print axioms ScienceL2.gibbsLaw_mem_window
#print axioms ScienceL2.window_pos
#print axioms ScienceL2.exists_gibbsLaw_of_mem_window
#print axioms ScienceL2.window_eq_gibbs_image
#print axioms ScienceL2.window_convex
#print axioms ScienceL2.lipClass_extremePoints_eq_empty
#print axioms ScienceL2.site_conditional_mem_window
#print axioms ScienceL2.single_site_of_admissible
#print axioms ScienceL2.cylinder_cross_le
#print axioms ScienceL2.condLaw_mem_window
#print axioms ScienceL2.window_needs_diag_zero
#print axioms ScienceL2.gibbsLaw_add_const
#print axioms ScienceL2.exp_neg_softMin
#print axioms ScienceL2.softMin_admissible
#print axioms ScienceL2.gibbsLaw_prod_apply
#print axioms ScienceL2.kl_gibbs_prod_eq
#print axioms ScienceL2.klBound_prod
#print axioms ScienceL2.kl_gibbs_prod_additive
#print axioms ScienceL2.gibbsLaw_equiv
#print axioms ScienceL2.klDivFin_gibbs_equiv
#print axioms ScienceL2.klBound_equiv
#print axioms ScienceL2.klBound_pi
#print axioms ScienceL2.kl_additive_pi
#print axioms ScienceL2.kl_pi_isGreatest
#print axioms ScienceL2.exists_pos_scale
#print axioms ScienceL2.eq_of_convex_comb_eq
#print axioms ScienceL2.window_slack_eq
#print axioms ScienceL2.window_tight_iff
#print axioms ScienceL2.perturb_mem_lipNorm
#print axioms ScienceL2.perturb_mem_window
#print axioms ScienceL2.gibbsLaw_extreme_of_extreme
#print axioms ScienceL2.extreme_of_gibbsLaw_extreme
#print axioms ScienceL2.extremePoints_window_eq
#print axioms ScienceL2.isCompact_window
#print axioms ScienceL2.klDivFin_convexOn_window
#print axioms ScienceL2.continuous_klDivFin
#print axioms ScienceL2.klBound_of_vertices
#print axioms ScienceL2.klBound_pi_of_vertices
#print axioms ScienceL2.exists_site_max
#print axioms ScienceL2.kl_pi_exists_isGreatest
