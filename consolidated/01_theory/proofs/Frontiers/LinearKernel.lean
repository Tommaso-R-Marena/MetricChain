import Mathlib
import proofs.CertificateAlgebra

/-!
# A kernel for residuals that are linear in pairwise features

Theory report §11.17, blueprint §7.  The residual is `g(x) = ∑_α θ_α F_α(x)` with **known
pairwise features** `F_α` (rational tables with nonnegative entries: contact counts, cumulative
pair counts) and **unknown real coefficients** in a box `lo ≤ θ ≤ hi`, of which some values
`g(a) = v` have been evaluated ("anchors").  The uncertainty of such a residual is correlated
through the coefficients; the kernel below certifies lower bounds on `min_x (E₀(x) + g(x))` that
hold for **every** coefficient vector of the box that is consistent with the anchors.

A certificate (`LCert`) is a subdivision of the coefficient box.  At a leaf, with current box
`[lo, hi]`:

* a certificate of the existing kernel (`Cert`, `verify`) shows `m ≤ min_x (E₀ + ∑_α lo_α F_α)(x)`
  — a pairwise problem, because the features are pairwise; since the features are nonnegative,
  this is a lower bound for every `θ ≥ lo`;
* multipliers `λ_i` for the anchors add the **data term**
  `∑_i λ_i v_i − ∑_α max (lo_α c_α, hi_α c_α)`, `c_α = ∑_i λ_i F_α(a_i)`, a lower bound for
  `∑_i λ_i (v_i − θ·F(a_i)) = 0`.  On a part of the box that contradicts the anchors the data term
  can be made large, so such parts are discharged without work.

`verifyL_sound`, `verifyLTop_sound`: an accepted certificate bounds the energy of every
configuration of the box, for every admissible coefficient vector.  The example at the end
(`contactTriangle_bound`) shows the effect of one anchor: without it the best bound is `-1`,
with it the kernel certifies `1`, which is attained.
-/

namespace MetricChain

open Finset

variable {n k p : ℕ}

/-! ### Linear combinations of pairwise instances -/

/-- The pairwise instance `base + ∑_α c_α · feat_α` (tables combined entrywise). -/
def PairInstance.addSmul (base : PairInstance n k) (feat : Fin p → PairInstance n k)
    (c : Fin p → ℚ) : PairInstance n k where
  h := fun i a => base.h i a + ∑ α, c α * (feat α).h i a
  J := fun i j a b => base.J i j a b + ∑ α, c α * (feat α).J i j a b

/-- The energy of a combined instance is the combination of the energies. -/
theorem PairInstance.addSmul_energy (base : PairInstance n k) (feat : Fin p → PairInstance n k)
    (c : Fin p → ℚ) (x : Config n k) :
    (base.addSmul feat c).energy x = base.energy x + ∑ α, c α * (feat α).energy x := by
  unfold PairInstance.energy PairInstance.addSmul
  have e1 : ∑ i, (base.h i (x i) + ∑ α, c α * (feat α).h i (x i)) =
      ∑ i, base.h i (x i) + ∑ α, c α * ∑ i, (feat α).h i (x i) := by
    rw [Finset.sum_add_distrib, Finset.sum_comm]
    congr 1
    exact Finset.sum_congr rfl fun α _ => (Finset.mul_sum _ _ _).symm
  have e2 : ∑ i, ∑ j ∈ univ.erase i,
        (base.J i j (x i) (x j) + ∑ α, c α * (feat α).J i j (x i) (x j)) =
      ∑ i, ∑ j ∈ univ.erase i, base.J i j (x i) (x j) +
        ∑ α, c α * ∑ i, ∑ j ∈ univ.erase i, (feat α).J i j (x i) (x j) := by
    have hin : ∀ i, ∑ j ∈ univ.erase i,
          (base.J i j (x i) (x j) + ∑ α, c α * (feat α).J i j (x i) (x j)) =
        ∑ j ∈ univ.erase i, base.J i j (x i) (x j) +
          ∑ α, c α * ∑ j ∈ univ.erase i, (feat α).J i j (x i) (x j) := by
      intro i
      rw [Finset.sum_add_distrib, Finset.sum_comm]
      congr 1
      exact Finset.sum_congr rfl fun α _ => (Finset.mul_sum _ _ _).symm
    rw [Finset.sum_congr rfl fun i _ => hin i, Finset.sum_add_distrib]
    congr 1
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl fun α _ => (Finset.mul_sum _ _ _).symm
  show ∑ i, (base.h i (x i) + ∑ α, c α * (feat α).h i (x i)) +
      ∑ i, ∑ j ∈ univ.erase i, (base.J i j (x i) (x j) + ∑ α, c α * (feat α).J i j (x i) (x j)) =
    ∑ i, base.h i (x i) + ∑ i, ∑ j ∈ univ.erase i, base.J i j (x i) (x j) +
      ∑ α, c α * (∑ i, (feat α).h i (x i) + ∑ i, ∑ j ∈ univ.erase i, (feat α).J i j (x i) (x j))
  rw [e1, e2]
  simp only [mul_add, Finset.sum_add_distrib]
  ring

/-! ### Problems, the class, certificates -/

/-- A linear-residual problem: the pairwise known part, `p` pairwise features, a box for the
coefficients, and a list of evaluated anchors `(configuration, residual value)`. -/
structure LProblem (n k p : ℕ) where
  /-- explicit pairwise part -/
  base : PairInstance n k
  /-- pairwise features -/
  feat : Fin p → PairInstance n k
  /-- lower ends of the coefficient box -/
  lo : Fin p → ℚ
  /-- upper ends of the coefficient box -/
  hi : Fin p → ℚ
  /-- evaluated residual values -/
  anchors : List (Config n k × ℚ)

/-- All feature tables are nonnegative (contact counts, cumulative pair counts). -/
def LProblem.FeatNonneg (P : LProblem n k p) : Prop :=
  ∀ α, (∀ i a, 0 ≤ (P.feat α).h i a) ∧ ∀ i j a b, 0 ≤ (P.feat α).J i j a b

instance (P : LProblem n k p) : Decidable P.FeatNonneg := by
  unfold LProblem.FeatNonneg
  infer_instance

/-- A feature with nonnegative tables has nonnegative energy. -/
theorem LProblem.FeatNonneg.energy_nonneg {P : LProblem n k p} (hF : P.FeatNonneg) (α : Fin p)
    (x : Config n k) : 0 ≤ (P.feat α).energy x := by
  unfold PairInstance.energy
  exact add_nonneg (Finset.sum_nonneg fun i _ => (hF α).1 i (x i))
    (Finset.sum_nonneg fun i _ => Finset.sum_nonneg fun j _ => (hF α).2 i j (x i) (x j))

/-- The admissible coefficient vectors: in the box and consistent with every anchor. -/
def LinResidualClass (P : LProblem n k p) (θ : Fin p → ℝ) : Prop :=
  (∀ α, (P.lo α : ℝ) ≤ θ α ∧ θ α ≤ (P.hi α : ℝ)) ∧
    ∀ av ∈ P.anchors, ∑ α, θ α * (((P.feat α).energy av.1 : ℚ) : ℝ) = (av.2 : ℝ)

/-- Certificates: a subdivision of the coefficient box with, at every leaf, multipliers for the
anchors, a claimed minimum of the pairwise problem at the lower corner, and a certificate of
the pairwise kernel for it. -/
inductive LCert (n k p : ℕ) : Type
  | leaf (lam : List ℚ) (m : ℚ) (c : Cert n k) : LCert n k p
  | split (α : Fin p) (mid : ℚ) (left right : LCert n k p) : LCert n k p

/-- `∑_i λ_i v_i` over the anchors paired with the multipliers. -/
def lamDotV (anchors : List (Config n k × ℚ)) (lam : List ℚ) : ℚ :=
  ((anchors.zip lam).map fun t => t.2 * t.1.2).sum

/-- `c_α = ∑_i λ_i F_α(a_i)`. -/
def lamDotF (feat : Fin p → PairInstance n k) (anchors : List (Config n k × ℚ)) (lam : List ℚ)
    (α : Fin p) : ℚ :=
  ((anchors.zip lam).map fun t => t.2 * (feat α).energy t.1.1).sum

/-- The data term of a leaf: a lower bound, on the box `[lo, hi]`, for
`∑_i λ_i (v_i − θ·F(a_i))`, which vanishes for coefficients consistent with the anchors. -/
def dataTerm (P : LProblem n k p) (lam : List ℚ) (lo hi : Fin p → ℚ) : ℚ :=
  lamDotV P.anchors lam -
    ∑ α, max (lo α * lamDotF P.feat P.anchors lam α) (hi α * lamDotF P.feat P.anchors lam α)

/-- **The kernel.**  `verifyL c P lo hi D L = true` certifies `L ≤ E₀(x) + ∑_α θ_α F_α(x)` for all
`x` in the box `∏ D` and all coefficient vectors in `[lo, hi]` consistent with the anchors. -/
def verifyL : LCert n k p → LProblem n k p → (Fin p → ℚ) → (Fin p → ℚ) → Dom n k → ℚ → Bool
  | .leaf lam m c, P, lo, hi, D, L =>
      verify c (P.base.addSmul P.feat lo) D m && decide (L ≤ m + dataTerm P lam lo hi)
  | .split α mid l r, P, lo, hi, D, L =>
      verifyL l P lo (Function.update hi α mid) D L &&
        verifyL r P (Function.update lo α mid) hi D L

/-- Number of leaves of a certificate. -/
def LCert.leaves : LCert n k p → ℕ
  | .leaf _ _ _ => 1
  | .split _ _ l r => l.leaves + r.leaves

/-! ### Soundness -/

/-- For coefficients consistent with the anchors, `∑_i λ_i v_i = ∑_α θ_α c_α`. -/
theorem lamDotV_eq (feat : Fin p → PairInstance n k) (θ : Fin p → ℝ) :
    ∀ (l : List ((Config n k × ℚ) × ℚ)),
      (∀ t ∈ l, ∑ α, θ α * (((feat α).energy t.1.1 : ℚ) : ℝ) = (t.1.2 : ℝ)) →
      (((l.map fun t => t.2 * t.1.2).sum : ℚ) : ℝ) =
        ∑ α, θ α * (((l.map fun t => t.2 * (feat α).energy t.1.1).sum : ℚ) : ℝ) := by
  intro l
  induction l with
  | nil =>
    intro _
    simp
  | cons t l ih =>
    intro h
    have ht := h t (List.mem_cons_self)
    have hl := ih fun s hs => h s (List.mem_cons_of_mem _ hs)
    simp only [List.map_cons, List.sum_cons, Rat.cast_add, Rat.cast_mul]
    rw [hl, ← ht]
    simp only [mul_add, Finset.sum_add_distrib, Finset.mul_sum]
    congr 1
    refine Finset.sum_congr rfl fun α _ => ?_
    ring

/-- The data term is nonpositive on the part of the box that is consistent with the anchors
(it is a lower bound for an expression that vanishes there). -/
theorem dataTerm_le_zero (P : LProblem n k p) (lam : List ℚ) (lo hi : Fin p → ℚ)
    (θ : Fin p → ℝ) (hθ : ∀ α, (lo α : ℝ) ≤ θ α ∧ θ α ≤ (hi α : ℝ))
    (hanch : ∀ av ∈ P.anchors, ∑ α, θ α * (((P.feat α).energy av.1 : ℚ) : ℝ) = (av.2 : ℝ)) :
    ((dataTerm P lam lo hi : ℚ) : ℝ) ≤ 0 := by
  have hid := lamDotV_eq P.feat θ (P.anchors.zip lam) fun t ht =>
    hanch t.1 (List.of_mem_zip ht).1
  unfold dataTerm lamDotV
  rw [Rat.cast_sub, hid, Rat.cast_sum, sub_nonpos]
  refine Finset.sum_le_sum fun α _ => ?_
  rw [Rat.cast_max, Rat.cast_mul, Rat.cast_mul]
  show θ α * ((lamDotF P.feat P.anchors lam α : ℚ) : ℝ) ≤ _
  by_cases hc : 0 ≤ ((lamDotF P.feat P.anchors lam α : ℚ) : ℝ)
  · exact le_max_of_le_right (mul_le_mul_of_nonneg_right (hθ α).2 hc)
  · exact le_max_of_le_left (mul_le_mul_of_nonpos_right (hθ α).1 (not_le.mp hc).le)

/-- **Soundness of the linear-residual kernel.** -/
theorem verifyL_sound (P : LProblem n k p) (hF : P.FeatNonneg) :
    ∀ (c : LCert n k p) (lo hi : Fin p → ℚ) (D : Dom n k) (L : ℚ),
      verifyL c P lo hi D L = true →
      ∀ θ : Fin p → ℝ, (∀ α, (lo α : ℝ) ≤ θ α ∧ θ α ≤ (hi α : ℝ)) →
        (∀ av ∈ P.anchors, ∑ α, θ α * (((P.feat α).energy av.1 : ℚ) : ℝ) = (av.2 : ℝ)) →
        ∀ x, InBox D x →
          (L : ℝ) ≤ ((P.base.energy x : ℚ) : ℝ) + ∑ α, θ α * (((P.feat α).energy x : ℚ) : ℝ) := by
  intro c
  induction c with
  | leaf lam m c =>
    intro lo hi D L hv θ hθ hanch x hx
    simp only [verifyL, Bool.and_eq_true, decide_eq_true_eq] at hv
    obtain ⟨hmin, hL⟩ := hv
    have h1 := verify_sound c (P.base.addSmul P.feat lo) D m hmin x hx
    rw [PairInstance.addSmul_energy] at h1
    have h1r : (m : ℝ) ≤ ((P.base.energy x : ℚ) : ℝ) +
        ∑ α, (lo α : ℝ) * (((P.feat α).energy x : ℚ) : ℝ) := by
      have := (Rat.cast_le (K := ℝ)).mpr h1
      push_cast at this
      exact this
    have h2 : ∑ α, (lo α : ℝ) * (((P.feat α).energy x : ℚ) : ℝ) ≤
        ∑ α, θ α * (((P.feat α).energy x : ℚ) : ℝ) :=
      Finset.sum_le_sum fun α _ => mul_le_mul_of_nonneg_right (hθ α).1
        (by exact_mod_cast hF.energy_nonneg α x)
    have h3 := dataTerm_le_zero P lam lo hi θ hθ hanch
    have hLr : (L : ℝ) ≤ (m : ℝ) + ((dataTerm P lam lo hi : ℚ) : ℝ) := by
      have := (Rat.cast_le (K := ℝ)).mpr hL
      push_cast at this
      exact this
    linarith
  | split α mid l r ihl ihr =>
    intro lo hi D L hv θ hθ hanch x hx
    simp only [verifyL, Bool.and_eq_true] at hv
    obtain ⟨hl, hr⟩ := hv
    by_cases hmid : θ α ≤ (mid : ℝ)
    · refine ihl lo (Function.update hi α mid) D L hl θ (fun β => ?_) hanch x hx
      by_cases hβ : β = α
      · subst hβ
        rw [Function.update_self]
        exact ⟨(hθ β).1, hmid⟩
      · rw [Function.update_of_ne hβ]
        exact hθ β
    · refine ihr (Function.update lo α mid) hi D L hr θ (fun β => ?_) hanch x hx
      by_cases hβ : β = α
      · subst hβ
        rw [Function.update_self]
        exact ⟨(not_le.mp hmid).le, (hθ β).2⟩
      · rw [Function.update_of_ne hβ]
        exact hθ β

/-- Top-level check: the features are nonnegative and the certificate is accepted on the
whole coefficient box. -/
def verifyLTop (c : LCert n k p) (P : LProblem n k p) (D : Dom n k) (L : ℚ) : Bool :=
  decide P.FeatNonneg && verifyL c P P.lo P.hi D L

/-- **Master soundness for residuals that are linear in features.**  If the kernel accepts,
then for every coefficient vector of the box that is consistent with the anchors, `L` is a
lower bound on `E₀ + g` over the box of configurations. -/
theorem verifyLTop_sound (c : LCert n k p) (P : LProblem n k p) (D : Dom n k) (L : ℚ)
    (hv : verifyLTop c P D L = true) (θ : Fin p → ℝ) (hθ : LinResidualClass P θ)
    (x : Config n k) (hx : InBox D x) :
    (L : ℝ) ≤ ((P.base.energy x : ℚ) : ℝ) + ∑ α, θ α * (((P.feat α).energy x : ℚ) : ℝ) := by
  simp only [verifyLTop, Bool.and_eq_true, decide_eq_true_eq] at hv
  exact verifyL_sound P hv.1 c P.lo P.hi D L hv.2 θ hθ.1 hθ.2 x hx

/-! ### Example: one anchor decides -/

/-- The feature "sites `0` and `1` are both in state `1`" on three binary sites. -/
def contactFeature : PairInstance 3 2 where
  h := fun _ _ => 0
  J := fun i j a b => if i = 0 ∧ j = 1 ∧ a = 1 ∧ b = 1 then 1 else 0

/-- The frustrated triangle with a contact term of unknown strength `θ ∈ [-2, 2]`, evaluated
once: at `(1,1,0)` the residual is `3/4`. -/
def contactTriangle : LProblem 3 2 1 where
  base := triangle
  feat := fun _ => contactFeature
  lo := fun _ => -2
  hi := fun _ => 2
  anchors := [(![1, 1, 0], 3 / 4)]

/-- Two leaves: for `θ ≤ 0` the anchor contradicts the box and the multiplier `8/3` lifts the
bound `-1` of the lower corner to `1`; for `θ ≥ 0` the contact term is nonnegative and the
triangle bound `1` applies. -/
def contactTriangleCert : LCert 3 2 1 :=
  .split 0 0
    (.leaf [8 / 3] (-1) (exhaustive3 (PairInstance.addSmul (p := 1) triangle (fun _ => contactFeature) fun _ => -2)))
    (.leaf [] 1 (exhaustive3 (PairInstance.addSmul (p := 1) triangle (fun _ => contactFeature) fun _ => 0)))

theorem contactTriangle_verified :
    verifyLTop contactTriangleCert contactTriangle (fullDom 3 2) 1 = true := by decide +kernel

/-- Without the anchor the same problem only admits the bound `-1` (it is attained at
`θ = -2`, `x = (1,1,0)`): the kernel rejects the bound `1` for the lower corner alone. -/
theorem contactTriangle_no_anchor_rejects :
    verifyLTop (.leaf [] 1 (exhaustive3 (PairInstance.addSmul (p := 1) triangle (fun _ => contactFeature) fun _ => -2)))
      contactTriangle (fullDom 3 2) 1 = false := by decide +kernel

/-- **For every contact strength in `[-2, 2]` that is consistent with the one evaluation, every
configuration has energy at least `1`.** -/
theorem contactTriangle_bound (θ : Fin 1 → ℝ) (hθ : LinResidualClass contactTriangle θ)
    (x : Config 3 2) :
    ((1 : ℚ) : ℝ) ≤ ((triangle.energy x : ℚ) : ℝ) +
      ∑ α, θ α * (((contactFeature.energy x : ℚ)) : ℝ) :=
  verifyLTop_sound contactTriangleCert contactTriangle (fullDom 3 2) 1 contactTriangle_verified
    θ hθ x (inBox_fullDom x)

/-- The admissible class of the example is not empty: `θ = 3/4`. -/
theorem contactTriangle_class_nonempty : LinResidualClass contactTriangle fun _ => 3 / 4 := by
  refine ⟨fun α => ⟨by norm_num [contactTriangle], by norm_num [contactTriangle]⟩, ?_⟩
  intro av hav
  simp only [contactTriangle, List.mem_singleton] at hav
  subst hav
  have he : contactFeature.energy ![1, 1, 0] = 1 := by decide +kernel
  simp [contactTriangle, he]

end MetricChain
