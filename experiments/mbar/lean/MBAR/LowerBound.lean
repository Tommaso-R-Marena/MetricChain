import Mathlib
import MBAR.Allocation

/-!
# Deterministic cores of the lower bounds (finite support)

Division 9, `docs/mbar/MATHEMATICS.md` part C.

Handoff D1 (general-graph two-point family):
* `weighted_ls_identity`, `edge_energy_identity` — the weighted least-squares identity that turns
  the per-state divergences into the Laplacian energy `Σ_e ℓ_e (θ_i − θ_j)²`;
* `chisq_categorical` — the χ² divergence of a perturbed categorical law with a private category;
* `abs_exp_sub_one_le_mul_exp` — `|e^z − 1| ≤ |z| e^{|z|}`;
* `kl_le_chisq` — `KL ≤ χ²` for finite laws;
* `max_principle`, `harmonic_extremes` — the discrete maximum principle on a connected network;
* `le_cam` — the two-point testing inequality `P₀(A) + P₁(Aᶜ) ≥ 1 − TV`.

Local minimax bound of this division (least-favourable submodel `dG_t = (1 + t h) dG`):
* `tilt_sum_one`, `chisq_tilt` — the tilted law and its χ² distance `t² Var_k(h)/(1 + t E_k h)²`;
* `log_one_add_ge`, `log_one_add_le` — `u − 2u² ≤ log(1+u) ≤ u` on `u ≥ −1/2` (separation);
* with `Model.cs_form` and `Model.efficiency_bound` (file `Allocation`) these are all the
  deterministic steps of Theorems C1 and C2.

Not formalised: Pinsker's inequality and the chain rule of the Kullback–Leibler divergence for
adaptively chosen states — external, labelled [X] in the mathematics note.
-/

open Finset

namespace MBAR

/-! ### The weighted least-squares identity -/

/-- For `a = (s_i θ_i + s_j θ_j)/(s_i + s_j)`:
`s_i (a − θ_i)² + s_j (a − θ_j)² = (s_i s_j/(s_i + s_j)) (θ_i − θ_j)²`. -/
theorem weighted_ls_identity {si sj ti tj : ℝ} (hi : 0 < si) (hj : 0 < sj) :
    si * ((si * ti + sj * tj) / (si + sj) - ti) ^ 2
      + sj * ((si * ti + sj * tj) / (si + sj) - tj) ^ 2
      = si * sj / (si + sj) * (ti - tj) ^ 2 := by
  have h : si + sj ≠ 0 := (add_pos hi hj).ne'
  field_simp
  ring

/-- Summed over the edges of a network with endpoint maps `src`, `dst`: the divergence budget of
the hard family equals the Laplacian energy of `θ`. -/
theorem edge_energy_identity {ι E : Type*} [Fintype E] (src dst : E → ι) {s : ι → ℝ}
    (hs : ∀ k, 0 < s k) (w : E → ℝ) (θ : ι → ℝ) :
    ∑ e, w e * (s (src e) * ((s (src e) * θ (src e) + s (dst e) * θ (dst e))
          / (s (src e) + s (dst e)) - θ (src e)) ^ 2
        + s (dst e) * ((s (src e) * θ (src e) + s (dst e) * θ (dst e))
          / (s (src e) + s (dst e)) - θ (dst e)) ^ 2)
      = ∑ e, w e * (s (src e) * s (dst e) / (s (src e) + s (dst e)))
          * (θ (src e) - θ (dst e)) ^ 2 := by
  refine Finset.sum_congr rfl (fun e _ => ?_)
  rw [weighted_ls_identity (hs (src e)) (hs (dst e))]
  ring

/-! ### Divergence inequalities -/

/-- χ² divergence of a categorical law with shared categories `e` (baseline `w e`, perturbation
`Δ e`) and one private category (baseline `1 − Σ w`, perturbation `−Σ Δ`). -/
theorem chisq_categorical {E : Type*} [Fintype E] {w Δ : E → ℝ} (hw : ∀ e, 0 < w e)
    (hW : ∑ e, w e < 1) :
    ∑ e, Δ e ^ 2 / w e + (∑ e, Δ e) ^ 2 / (1 - ∑ e, w e)
      ≤ (∑ e, Δ e ^ 2 / w e) / (1 - ∑ e, w e) := by
  have h1W : 0 < 1 - ∑ e, w e := by linarith
  have hcs : (∑ e, Δ e) ^ 2 ≤ (∑ e, w e) * ∑ e, Δ e ^ 2 / w e := by
    rcases isEmpty_or_nonempty E with hE | hE
    · simp
    · have hWpos : 0 < ∑ e, w e := Finset.sum_pos (fun e _ => hw e) Finset.univ_nonempty
      have h2 := Finset.sq_sum_div_le_sum_sq_div Finset.univ Δ (fun e _ => hw e)
      rw [div_le_iff₀ hWpos] at h2
      linarith [mul_comm (∑ e, Δ e ^ 2 / w e) (∑ e, w e)]
  rw [le_div_iff₀ h1W, add_mul, div_mul_cancel₀ _ h1W.ne']
  nlinarith [hcs]

/-- `|e^z − 1| ≤ |z| e^{|z|}`. -/
theorem abs_exp_sub_one_le_mul_exp (z : ℝ) : |Real.exp z - 1| ≤ |z| * Real.exp |z| := by
  rcases le_total 0 z with hz | hz
  · have h0 : 0 ≤ Real.exp z - 1 := by linarith [Real.add_one_le_exp z]
    rw [abs_of_nonneg hz, abs_of_nonneg h0]
    have h1 := Real.add_one_le_exp (-z)
    have h2 : Real.exp z * Real.exp (-z) = 1 := by rw [← Real.exp_add]; simp
    have h3 := mul_le_mul_of_nonneg_left h1 (Real.exp_pos z).le
    rw [h2] at h3
    linarith
  · have h0 : Real.exp z - 1 ≤ 0 := by linarith [Real.exp_le_one_iff.2 hz]
    rw [abs_of_nonpos hz, abs_of_nonpos h0]
    have h1 := Real.add_one_le_exp z
    have h3 : 1 ≤ Real.exp (-z) := Real.one_le_exp (by linarith)
    have h4 := mul_le_mul_of_nonneg_left h3 (neg_nonneg.2 hz)
    linarith

/-- `KL(P' ‖ P) ≤ χ²(P' ‖ P)` for finite laws (`0 · log 0 = 0`). -/
theorem kl_le_chisq {β : Type*} [Fintype β] {P P' : β → ℝ} (hP : ∀ b, 0 < P b)
    (hP' : ∀ b, 0 ≤ P' b) (h1 : ∑ b, P b = 1) (h1' : ∑ b, P' b = 1) :
    ∑ b, P' b * Real.log (P' b / P b) ≤ ∑ b, (P' b - P b) ^ 2 / P b := by
  have hterm : ∀ b, P' b * Real.log (P' b / P b) ≤ P' b ^ 2 / P b - P' b := by
    intro b
    rcases eq_or_lt_of_le (hP' b) with h | h
    · rw [← h]; simp
    · have hx : 0 < P' b / P b := div_pos h (hP b)
      have hlog := Real.log_le_sub_one_of_pos hx
      calc P' b * Real.log (P' b / P b) ≤ P' b * (P' b / P b - 1) :=
            mul_le_mul_of_nonneg_left hlog h.le
        _ = P' b ^ 2 / P b - P' b := by ring
  have hsum : ∑ b, (P' b - P b) ^ 2 / P b = ∑ b, (P' b ^ 2 / P b - P' b) := by
    have e : ∀ b, (P' b - P b) ^ 2 / P b = (P' b ^ 2 / P b - P' b) + (P b - P' b) := by
      intro b
      have h2 := (hP b).ne'
      field_simp
      ring
    simp only [e, Finset.sum_add_distrib, Finset.sum_sub_distrib, h1, h1']
    ring
  rw [hsum]
  exact Finset.sum_le_sum (fun b _ => hterm b)

/-! ### Discrete maximum principle -/

/-- If `Σ_j w_ij (θ_i − θ_j) ≤ 0` at every vertex except `b`, on a connected network with
nonnegative weights, then `θ` is maximal at `b`. -/
theorem max_principle {ι : Type*} [Fintype ι] {w : ι → ι → ℝ} (hw : ∀ i j, 0 ≤ w i j)
    {θ : ι → ℝ} {b : ι} (hharm : ∀ i, i ≠ b → ∑ j, w i j * (θ i - θ j) ≤ 0)
    (hconn : ∀ i j, Relation.ReflTransGen (fun i j => 0 < w i j) i j) :
    ∀ i, θ i ≤ θ b := by
  obtain ⟨i0, -, hmax⟩ := Finset.exists_max_image Finset.univ θ ⟨b, Finset.mem_univ b⟩
  by_contra hcon
  rcases not_forall.1 hcon with ⟨i1, hi1⟩
  have hb : θ b < θ i0 := lt_of_lt_of_le (not_le.1 hi1) (hmax i1 (Finset.mem_univ _))
  have key : ∀ j, Relation.ReflTransGen (fun i j => 0 < w i j) i0 j → θ j = θ i0 := by
    intro j hj
    induction hj with
    | refl => rfl
    | @tail m k _ hmk ih =>
      have hmb : m ≠ b := by
        intro h
        rw [h] at ih
        exact absurd ih (ne_of_lt hb)
      have hsum := hharm m hmb
      have hterm : ∀ l ∈ (Finset.univ : Finset ι), 0 ≤ w m l * (θ m - θ l) := by
        intro l _
        refine mul_nonneg (hw m l) ?_
        rw [ih]
        exact sub_nonneg.2 (hmax l (Finset.mem_univ _))
      have hzero := (Finset.sum_eq_zero_iff_of_nonneg hterm).1
        (le_antisymm hsum (Finset.sum_nonneg hterm)) k (Finset.mem_univ k)
      have h2 : θ m - θ k = 0 := (mul_eq_zero.1 hzero).resolve_left (ne_of_gt hmk)
      linarith
  exact absurd (key b (hconn i0 b)) (ne_of_lt hb)

/-- A function harmonic away from a source `b` and a sink `a` on a connected network takes its
maximum at `b` and its minimum at `a`; so its oscillation is `θ_b − θ_a` (handoff D1). -/
theorem harmonic_extremes {ι : Type*} [Fintype ι] {w : ι → ι → ℝ} (hw : ∀ i j, 0 ≤ w i j)
    {θ : ι → ℝ} {a b : ι} (hharm : ∀ i, i ≠ a → i ≠ b → ∑ j, w i j * (θ i - θ j) = 0)
    (ha : ∑ j, w a j * (θ a - θ j) ≤ 0) (hb : 0 ≤ ∑ j, w b j * (θ b - θ j))
    (hconn : ∀ i j, Relation.ReflTransGen (fun i j => 0 < w i j) i j) :
    ∀ i, θ a ≤ θ i ∧ θ i ≤ θ b := by
  have hmaxp : ∀ i, θ i ≤ θ b := by
    refine max_principle hw (fun i hib => ?_) hconn
    by_cases hia : i = a
    · rw [hia]; exact ha
    · exact (hharm i hia hib).le
  have hminp : ∀ i, (fun l => -θ l) i ≤ (fun l => -θ l) a := by
    refine max_principle hw (fun i hia => ?_) hconn
    have e : ∑ j, w i j * (-θ i - -θ j) = -∑ j, w i j * (θ i - θ j) := by
      rw [← Finset.sum_neg_distrib]
      exact Finset.sum_congr rfl (fun j _ => by ring)
    rw [e]
    by_cases hib : i = b
    · rw [hib]; linarith
    · rw [hharm i hia hib]; simp
  intro i
  exact ⟨by have := hminp i; simp only at this; linarith, hmaxp i⟩

/-! ### Two-point testing -/

/-- **Le Cam's two-point inequality** on a finite space: the two error probabilities of any test
with acceptance region `A` add up to at least `1 − TV(P₀, P₁)`. -/
theorem le_cam {Ω : Type*} [Fintype Ω] [DecidableEq Ω] (P0 P1 : Ω → ℝ) (A : Finset Ω)
    (h0 : ∑ x, P0 x = 1) (h1 : ∑ x, P1 x = 1) :
    1 - (∑ x, |P0 x - P1 x|) / 2 ≤ ∑ x ∈ A, P0 x + ∑ x ∈ Aᶜ, P1 x := by
  have hmin : ∀ x, min (P0 x) (P1 x) = (P0 x + P1 x - |P0 x - P1 x|) / 2 := by
    intro x
    rcases le_total (P0 x) (P1 x) with h | h
    · rw [min_eq_left h, abs_of_nonpos (sub_nonpos.2 h)]; ring
    · rw [min_eq_right h, abs_of_nonneg (sub_nonneg.2 h)]; ring
  have htot : ∑ x, min (P0 x) (P1 x) = 1 - (∑ x, |P0 x - P1 x|) / 2 := by
    simp only [hmin]
    rw [← Finset.sum_div, Finset.sum_sub_distrib, Finset.sum_add_distrib, h0, h1]
    ring
  rw [← htot, ← Finset.sum_add_sum_compl A (fun x => min (P0 x) (P1 x))]
  exact add_le_add (Finset.sum_le_sum (fun x _ => min_le_left _ _))
    (Finset.sum_le_sum (fun x _ => min_le_right _ _))

/-! ### The least-favourable submodel -/

namespace Model

variable {ι α : Type*} [Fintype ι] [Fintype α] (M : Model ι α)

/-- The tilted law `p_k (1 + t h)/(1 + t E_k h)` is normalised. -/
theorem tilt_sum_one (k : ι) (h : α → ℝ) (t : ℝ) (hden : 1 + t * M.E k h ≠ 0) :
    M.E k (fun x => (1 + t * h x) / (1 + t * M.E k h)) = 1 := by
  rw [M.E_div_const, M.E_add, M.E_const, M.E_const_mul]
  exact div_self hden

/-- χ² distance of the tilted law from `p_k`: exactly `t² Var_k(h)/(1 + t E_k h)²`. -/
theorem chisq_tilt (k : ι) (h : α → ℝ) (t : ℝ) (hden : 1 + t * M.E k h ≠ 0) :
    M.E k (fun x => ((1 + t * h x) / (1 + t * M.E k h) - 1) ^ 2)
      = t ^ 2 * M.Var k h / (1 + t * M.E k h) ^ 2 := by
  have e : (fun x => ((1 + t * h x) / (1 + t * M.E k h) - 1) ^ 2)
      = fun x => t ^ 2 / (1 + t * M.E k h) ^ 2 * (h x - M.E k h) ^ 2 := by
    funext x
    field_simp
    ring
  rw [e, M.E_const_mul, Var]
  ring

/-- Total divergence budget of the submodel under an allocation `n`:
`Σ_k n_k χ²_k = t² Σ_k n_k Var_k(h)/(1 + t E_k h)²`. -/
theorem chisq_budget (n : ι → ℝ) (h : α → ℝ) (t : ℝ) (hden : ∀ k, 1 + t * M.E k h ≠ 0) :
    ∑ k, n k * M.E k (fun x => ((1 + t * h x) / (1 + t * M.E k h) - 1) ^ 2)
      = t ^ 2 * ∑ k, n k * (M.Var k h / (1 + t * M.E k h) ^ 2) := by
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl (fun k _ => ?_)
  rw [M.chisq_tilt k h t (hden k)]
  ring

end Model

/-- `log(1 + u) ≤ u`. -/
theorem log_one_add_le {u : ℝ} (hu : -1 < u) : Real.log (1 + u) ≤ u := by
  have := Real.log_le_sub_one_of_pos (show 0 < 1 + u by linarith)
  linarith

/-- `u − 2u² ≤ log(1 + u)` for `u ≥ −1/2`. -/
theorem log_one_add_ge {u : ℝ} (hu : -1 / 2 ≤ u) : u - 2 * u ^ 2 ≤ Real.log (1 + u) := by
  have hpos : 0 < 1 + u := by linarith
  have h1 := Real.one_sub_inv_le_log_of_pos hpos
  have h2 : u - 2 * u ^ 2 ≤ 1 - (1 + u)⁻¹ := by
    have e : 1 - (1 + u)⁻¹ = u / (1 + u) := by
      field_simp
      ring
    rw [e, le_div_iff₀ hpos]
    nlinarith [sq_nonneg u, mul_nonneg (sq_nonneg u) (show 0 ≤ 1 + 2 * u by linarith)]
  linarith

end MBAR
