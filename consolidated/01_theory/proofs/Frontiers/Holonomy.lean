import Mathlib

/-!
# Cycle-holonomy obstructions for frame graphs

A frame graph assigns a rigid frame to every vertex and a *measured* relative transform to every
edge.  Around a closed cycle the ordered product of the measured transforms (the *holonomy*) would
be trivial if the measurements were consistent with some assignment of vertex frames.  This file
proves the quantitative converse: the holonomy is a lower bound for the total edge error of
**any** vertex assignment.

## H1 — non-abelian holonomy bound (conjugation-invariant norm)

Setting: a `SeminormedGroup E` (multiplicative, not assumed commutative) whose norm is conjugation
invariant, `hconj : ∀ g x, ‖g * x * g⁻¹‖ = ‖x‖`; this is the abstract form of a bi-invariant metric
(e.g. the rotation group with the geodesic angle or the chordal distance).

* `holProd ghat m = ghat 0 * ghat 1 * ⋯ * ghat (m-1)`;
* `norm_mul_div_mul_le` — key lemma `‖(a * b) / (a' * b')‖ ≤ ‖a / a'‖ + ‖b / b'‖`;
* `norm_holProd_div_le` — open-path version;
* `norm_holProd_le_sum` — cycle version, `ℓ¹` form;
* `norm_holProd_sq_le` — cycle version, `ℓ²` form;
* `exists_edge_error_ge` — some edge carries at least the average `‖hol‖ / m`;
* `norm_div_eq_dist_of_conj`, `dist_holProd_one_le_sum` — the same statements in terms of `dist`
  (in Mathlib a `SeminormedGroup` has `dist a b = ‖a⁻¹ * b‖`; under `hconj` this equals `‖a / b‖`).

## H2 — translation holonomy with lever arms (the `SE(3)` semidirect structure)

Absolute frames `(R k, p k)`, measured relative rotations `Rhat k` and translations `that k`, true
relatives `v ↦ (R k).symm (R (k+1) v)` and `(R k).symm (p (k+1) - p k)`.

* `accRot Rhat k = Rhat 0 ∘ ⋯ ∘ Rhat (k-1)` and
  `holTrans Rhat that m = ∑ k < m, accRot Rhat k (that k)`;
* `holAct_eq` — these are the linear and translation parts of the composite of the measured
  relative rigid motions `v ↦ Rhat k v + that k`;
* `norm_accRot_sub_le`, `norm_accRot_sub_self_le` — accumulated rotation error, and the rotation
  part of the holonomy when the frames close up;
* `norm_holTrans_sub_le` — open-path version;
* `norm_holTrans_le` (and `norm_holTrans_le_of_lt`, with the hypothesis only on the edges of the
  cycle) — closed cycle:
  `‖holTrans Rhat that m‖ ≤ ∑ ‖that k - ttrue k‖ + ∑ (∑ l < k, ρ l) * ‖that k‖`.

## H3 — the abelian case is exact

* `norm_holProd_le_sum_of_comm` — H1 in a commutative group (no hypothesis needed);
* `norm_sum_le_sum_edge_error`, `norm_sum_sq_le_edge_error` — additive `ℓ¹` and `ℓ²` forms;
* `exists_assignment_attaining_holonomy` — in a real normed space the `ℓ¹` and the `ℓ²` bounds are
  attained simultaneously by spreading the holonomy evenly over the cycle.

## Genuinely non-commutative instances

* `chordalSeminorm V` — the conjugation-invariant group seminorm `g ↦ ‖g - 1‖` (operator norm) on
  the group `V ≃ₗᵢ[ℝ] V` of linear isometries (the orthogonal group when `V` is Euclidean);
* `chordal_holProd_le`, `opNorm_holProd_sub_id_le` — H1 instantiated there;
* `turnAngle g` — the largest angle by which `g` turns a vector, `angularSeminorm V` the
  corresponding conjugation-invariant group seminorm (the geodesic angle on rotations), and
  `turnAngle_holProd_le` — H1 for it.
-/

namespace MetricChain

open Finset

/-! ## H1. Non-abelian holonomy bound -/

section NonAbelian

/-- Ordered product `ghat 0 * ghat 1 * ⋯ * ghat (m-1)` of the measured edge transforms along a
path with `m` edges (the *holonomy* when the path is a closed cycle). -/
def holProd {M : Type*} [Monoid M] (ghat : ℕ → M) : ℕ → M
  | 0 => 1
  | (m + 1) => holProd ghat m * ghat m

@[simp] theorem holProd_zero {M : Type*} [Monoid M] (ghat : ℕ → M) : holProd ghat 0 = 1 := rfl

@[simp] theorem holProd_succ {M : Type*} [Monoid M] (ghat : ℕ → M) (m : ℕ) :
    holProd ghat (m + 1) = holProd ghat m * ghat m := rfl

/-- Exact (noise-free) relative transforms telescope: their ordered product along a path is the
relative transform of the end points.  In particular the holonomy of a closed cycle is trivial. -/
theorem holProd_exact {G : Type*} [Group G] (x : ℕ → G) (m : ℕ) :
    holProd (fun k => (x k)⁻¹ * x (k + 1)) m = (x 0)⁻¹ * x m := by
  induction m with
  | zero => simp
  | succ m ih => rw [holProd_succ, ih]; group

variable {E : Type*} [SeminormedGroup E]

/-- **Key lemma.** For a conjugation-invariant norm the error of a product is at most the sum of
the errors of the factors. -/
theorem norm_mul_div_mul_le (hconj : ∀ g x : E, ‖g * x * g⁻¹‖ = ‖x‖) (a b a' b' : E) :
    ‖(a * b) / (a' * b')‖ ≤ ‖a / a'‖ + ‖b / b'‖ := by
  have h : (a * b) / (a' * b') = (a * (b / b') * a⁻¹) * (a / a') := by
    simp only [div_eq_mul_inv]; group
  rw [h]
  calc ‖a * (b / b') * a⁻¹ * (a / a')‖ ≤ ‖a * (b / b') * a⁻¹‖ + ‖a / a'‖ := norm_mul_le' _ _
    _ = ‖b / b'‖ + ‖a / a'‖ := by rw [hconj]
    _ = ‖a / a'‖ + ‖b / b'‖ := add_comm _ _

/-- For a conjugation-invariant norm, `‖a / b‖` is the distance of `a` and `b` (Mathlib's
`SeminormedGroup` uses the left-invariant convention `dist a b = ‖a⁻¹ * b‖`). -/
theorem norm_div_eq_dist_of_conj (hconj : ∀ g x : E, ‖g * x * g⁻¹‖ = ‖x‖) (a b : E) :
    ‖a / b‖ = dist a b := by
  rw [dist_eq_norm_inv_mul', ← hconj b⁻¹ (a / b)]
  congr 1
  simp only [div_eq_mul_inv]; group

/-- **(H1, open path)** Along any path the measured ordered product deviates from the relative
transform of the end frames by at most the sum of the edge errors. -/
theorem norm_holProd_div_le (hconj : ∀ g x : E, ‖g * x * g⁻¹‖ = ‖x‖) (ghat x : ℕ → E) (m : ℕ) :
    ‖holProd ghat m / ((x 0)⁻¹ * x m)‖ ≤
      ∑ k ∈ range m, ‖ghat k / ((x k)⁻¹ * x (k + 1))‖ := by
  induction m with
  | zero => simp
  | succ m ih =>
    have h : (x 0)⁻¹ * x (m + 1) = ((x 0)⁻¹ * x m) * ((x m)⁻¹ * x (m + 1)) := by group
    rw [holProd_succ, h, sum_range_succ]
    exact (norm_mul_div_mul_le hconj _ _ _ _).trans (add_le_add ih le_rfl)

/-- **(H1, `ℓ¹` form)** Cycle-holonomy obstruction: for a cycle of length `m` with vertex frames
`x 0, …, x m`, `x m = x 0`, the norm of the holonomy of the measured edge transforms is a lower
bound for the total edge error of *any* vertex assignment. -/
theorem norm_holProd_le_sum (hconj : ∀ g x : E, ‖g * x * g⁻¹‖ = ‖x‖) (ghat x : ℕ → E) (m : ℕ)
    (hx : x m = x 0) :
    ‖holProd ghat m‖ ≤ ∑ k ∈ range m, ‖ghat k / ((x k)⁻¹ * x (k + 1))‖ := by
  have h := norm_holProd_div_le hconj ghat x m
  rwa [hx, inv_mul_cancel, div_one] at h

/-- **(H1, `ℓ²` form)** The squared holonomy is at most `m` times the sum of squared edge errors
(Cauchy–Schwarz); equivalently every assignment has least-squares cost `≥ ‖hol‖² / m`. -/
theorem norm_holProd_sq_le (hconj : ∀ g x : E, ‖g * x * g⁻¹‖ = ‖x‖) (ghat x : ℕ → E) (m : ℕ)
    (hx : x m = x 0) :
    ‖holProd ghat m‖ ^ 2 ≤ m * ∑ k ∈ range m, ‖ghat k / ((x k)⁻¹ * x (k + 1))‖ ^ 2 := by
  have h1 := norm_holProd_le_sum hconj ghat x m hx
  have h2 : (∑ k ∈ range m, ‖ghat k / ((x k)⁻¹ * x (k + 1))‖) ^ 2 ≤
      ((range m).card : ℝ) * ∑ k ∈ range m, ‖ghat k / ((x k)⁻¹ * x (k + 1))‖ ^ 2 :=
    sq_sum_le_card_mul_sum_sq
  rw [card_range] at h2
  exact (pow_le_pow_left₀ (norm_nonneg' _) h1 2).trans h2

/-- Pigeonhole form: on a cycle some edge carries an error of at least `‖hol‖ / m`. -/
theorem exists_edge_error_ge (hconj : ∀ g x : E, ‖g * x * g⁻¹‖ = ‖x‖) (ghat x : ℕ → E) {m : ℕ}
    (hm : 0 < m) (hx : x m = x 0) :
    ∃ k < m, ‖holProd ghat m‖ / m ≤ ‖ghat k / ((x k)⁻¹ * x (k + 1))‖ := by
  by_contra hcon
  have hlt : ∀ k ∈ range m, ‖ghat k / ((x k)⁻¹ * x (k + 1))‖ < ‖holProd ghat m‖ / m := by
    intro k hk
    by_contra hk'
    exact hcon ⟨k, mem_range.mp hk, not_lt.mp hk'⟩
  have hsum := sum_lt_sum_of_nonempty (nonempty_range_iff.mpr hm.ne') hlt
  have hm' : (m : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hm.ne'
  rw [sum_const, card_range, nsmul_eq_mul, mul_div_cancel₀ _ hm'] at hsum
  exact absurd (norm_holProd_le_sum hconj ghat x m hx) (not_le.mpr hsum)

/-- `norm_holProd_le_sum` in terms of the (bi-invariant) distance. -/
theorem dist_holProd_one_le_sum (hconj : ∀ g x : E, ‖g * x * g⁻¹‖ = ‖x‖) (ghat x : ℕ → E) (m : ℕ)
    (hx : x m = x 0) :
    dist (holProd ghat m) 1 ≤ ∑ k ∈ range m, dist (ghat k) ((x k)⁻¹ * x (k + 1)) := by
  simp only [← norm_div_eq_dist_of_conj hconj, div_one]
  exact norm_holProd_le_sum hconj ghat x m hx

end NonAbelian

/-! ## H2. Translation holonomy with lever arms -/

section Translation

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]

/-- Accumulated measured rotation `P k = Rhat 0 ∘ Rhat 1 ∘ ⋯ ∘ Rhat (k-1)`, i.e. `P 0 = id` and
`P (k+1) v = P k (Rhat k v)`. -/
def accRot (Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) : ℕ → (V ≃ₗᵢ[ℝ] V)
  | 0 => LinearIsometryEquiv.refl ℝ V
  | (k + 1) => (Rhat k).trans (accRot Rhat k)

@[simp] theorem accRot_zero_apply (Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (v : V) : accRot Rhat 0 v = v := rfl

@[simp] theorem accRot_succ_apply (Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (k : ℕ) (v : V) :
    accRot Rhat (k + 1) v = accRot Rhat k (Rhat k v) := rfl

/-- Translation part of the holonomy of the measured relative transforms:
`t_hol m = ∑ k < m, P k (that k)`. -/
def holTrans (Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (that : ℕ → V) (m : ℕ) : V :=
  ∑ k ∈ range m, accRot Rhat k (that k)

/-- Composite of the measured relative rigid motions `v ↦ Rhat k v + that k`, `k < m`
(the motion of edge `0` is applied last). -/
def holAct (Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (that : ℕ → V) : ℕ → V → V
  | 0 => id
  | (m + 1) => fun v => holAct Rhat that m (Rhat m v + that m)

/-- The semidirect-product structure: the composite of the measured relative rigid motions is
`v ↦ accRot Rhat m v + holTrans Rhat that m`. -/
theorem holAct_eq (Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (that : ℕ → V) (m : ℕ) (v : V) :
    holAct Rhat that m v = accRot Rhat m v + holTrans Rhat that m := by
  induction m generalizing v with
  | zero => simp [holAct, holTrans]
  | succ m ih =>
    show holAct Rhat that m (Rhat m v + that m) = _
    rw [ih]
    simp only [holTrans, sum_range_succ, map_add, accRot_succ_apply]
    abel

/-- Accumulated rotation error: the measured accumulated rotation `P k` deviates from the true one
`v ↦ (R 0).symm (R k v)` by at most the sum of the rotation errors of the edges before `k`. -/
theorem norm_accRot_sub_le (R Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (ρ : ℕ → ℝ) (m : ℕ)
    (hρ : ∀ k < m, ∀ v, ‖Rhat k v - (R k).symm (R (k + 1) v)‖ ≤ ρ k * ‖v‖) :
    ∀ k ≤ m, ∀ v, ‖accRot Rhat k v - (R 0).symm (R k v)‖ ≤ (∑ l ∈ range k, ρ l) * ‖v‖ := by
  intro k
  induction k with
  | zero => intro _ v; simp
  | succ k ih =>
    intro hk v
    have hk' : k < m := hk
    set w : V := (R k).symm (R (k + 1) v) with hw
    have hRw : R k w = R (k + 1) v := by rw [hw, LinearIsometryEquiv.apply_symm_apply]
    have hnw : ‖w‖ = ‖v‖ := by
      rw [hw, LinearIsometryEquiv.norm_map, LinearIsometryEquiv.norm_map]
    have hsplit : accRot Rhat (k + 1) v - (R 0).symm (R (k + 1) v) =
        accRot Rhat k (Rhat k v - w) + (accRot Rhat k w - (R 0).symm (R k w)) := by
      rw [accRot_succ_apply, hRw, map_sub]; abel
    rw [hsplit, sum_range_succ, add_mul]
    calc ‖accRot Rhat k (Rhat k v - w) + (accRot Rhat k w - (R 0).symm (R k w))‖
        ≤ ‖accRot Rhat k (Rhat k v - w)‖ + ‖accRot Rhat k w - (R 0).symm (R k w)‖ :=
          norm_add_le _ _
      _ ≤ ρ k * ‖v‖ + (∑ l ∈ range k, ρ l) * ‖w‖ := by
          refine add_le_add ?_ (ih hk'.le w)
          rw [LinearIsometryEquiv.norm_map]
          exact hρ k hk' v
      _ = (∑ l ∈ range k, ρ l) * ‖v‖ + ρ k * ‖v‖ := by rw [hnw, add_comm]

/-- Rotation part of the holonomy: if the frames close up (`R m = R 0`), the accumulated measured
rotation is within the total rotation error of the identity. -/
theorem norm_accRot_sub_self_le (R Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (ρ : ℕ → ℝ) (m : ℕ)
    (hclosed : R m = R 0)
    (hρ : ∀ k < m, ∀ v, ‖Rhat k v - (R k).symm (R (k + 1) v)‖ ≤ ρ k * ‖v‖) (v : V) :
    ‖accRot Rhat m v - v‖ ≤ (∑ l ∈ range m, ρ l) * ‖v‖ := by
  have h := norm_accRot_sub_le R Rhat ρ m hρ m le_rfl v
  rwa [hclosed, LinearIsometryEquiv.symm_apply_apply] at h

/-- The true relative translations, transported to frame `0`, telescope. -/
theorem sum_true_rel_trans (R : ℕ → (V ≃ₗᵢ[ℝ] V)) (p : ℕ → V) (m : ℕ) :
    ∑ k ∈ range m, (R 0).symm (R k ((R k).symm (p (k + 1) - p k))) =
      (R 0).symm (p m - p 0) := by
  simp only [LinearIsometryEquiv.apply_symm_apply]
  rw [← map_sum, sum_range_sub]

/-- **(H2, open path)** The translation part of the measured ordered product deviates from the
true relative position of the end frames by at most the sum of the translation errors plus the
lever-arm terms `(accumulated rotation error before k) * ‖that k‖`. -/
theorem norm_holTrans_sub_le (R Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (p that : ℕ → V) (ρ : ℕ → ℝ) (m : ℕ)
    (hρ : ∀ k < m, ∀ v, ‖Rhat k v - (R k).symm (R (k + 1) v)‖ ≤ ρ k * ‖v‖) :
    ‖holTrans Rhat that m - (R 0).symm (p m - p 0)‖ ≤
      ∑ k ∈ range m, ‖that k - (R k).symm (p (k + 1) - p k)‖ +
        ∑ k ∈ range m, (∑ l ∈ range k, ρ l) * ‖that k‖ := by
  have hA := norm_accRot_sub_le R Rhat ρ m hρ
  rw [← sum_true_rel_trans R p m, holTrans, ← sum_sub_distrib, ← sum_add_distrib]
  refine (norm_sum_le _ _).trans (sum_le_sum fun k hk => ?_)
  have hk' : k < m := mem_range.mp hk
  set t : V := (R k).symm (p (k + 1) - p k) with ht
  have hsplit : accRot Rhat k (that k) - (R 0).symm (R k t) =
      (R 0).symm (R k (that k - t)) + (accRot Rhat k (that k) - (R 0).symm (R k (that k))) := by
    rw [map_sub, map_sub]; abel
  rw [hsplit]
  refine (norm_add_le _ _).trans (add_le_add ?_ (hA k hk'.le (that k)))
  rw [LinearIsometryEquiv.norm_map, LinearIsometryEquiv.norm_map]

/-- **(H2)** Translation holonomy with lever arms, with the rotation-error hypothesis required
only on the edges `k < m` of the cycle. -/
theorem norm_holTrans_le_of_lt (R Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (p that : ℕ → V) (ρ : ℕ → ℝ) (m : ℕ)
    (hclosed : p m = p 0)
    (hρ : ∀ k < m, ∀ v, ‖Rhat k v - (R k).symm (R (k + 1) v)‖ ≤ ρ k * ‖v‖) :
    ‖holTrans Rhat that m‖ ≤
      ∑ k ∈ range m, ‖that k - (R k).symm (p (k + 1) - p k)‖ +
        ∑ k ∈ range m, (∑ l ∈ range k, ρ l) * ‖that k‖ := by
  have h := norm_holTrans_sub_le R Rhat p that ρ m hρ
  rwa [hclosed, sub_self, map_zero, sub_zero] at h

/-- **(H2)** Translation holonomy with lever arms.  For absolute frames `(R k, p k)` with
`p m = p 0`, measured relative rotations `Rhat k` with operator-norm error at most `ρ k` and
measured relative translations `that k`, the translation part of the holonomy is bounded by the
total translation error plus the lever-arm terms. -/
theorem norm_holTrans_le (R Rhat : ℕ → (V ≃ₗᵢ[ℝ] V)) (p that : ℕ → V) (ρ : ℕ → ℝ) (m : ℕ)
    (hclosed : p m = p 0)
    (hρ : ∀ k v, ‖Rhat k v - (R k).symm (R (k + 1) v)‖ ≤ ρ k * ‖v‖) :
    ‖holTrans Rhat that m‖ ≤
      ∑ k ∈ range m, ‖that k - (R k).symm (p (k + 1) - p k)‖ +
        ∑ k ∈ range m, (∑ l ∈ range k, ρ l) * ‖that k‖ :=
  norm_holTrans_le_of_lt R Rhat p that ρ m hclosed fun k _ => hρ k

end Translation

/-! ## H3. The abelian case is exact -/

section Abelian

/-- In a commutative monoid the ordered product is the plain product. -/
theorem holProd_eq_prod {M : Type*} [CommMonoid M] (ghat : ℕ → M) (m : ℕ) :
    holProd ghat m = ∏ k ∈ range m, ghat k := by
  induction m with
  | zero => simp
  | succ m ih => rw [holProd_succ, ih, prod_range_succ]

/-- **(H3)** H1 in a commutative seminormed group: conjugation invariance is automatic. -/
theorem norm_holProd_le_sum_of_comm {E : Type*} [SeminormedCommGroup E] (ghat x : ℕ → E) (m : ℕ)
    (hx : x m = x 0) :
    ‖holProd ghat m‖ ≤ ∑ k ∈ range m, ‖ghat k / ((x k)⁻¹ * x (k + 1))‖ :=
  norm_holProd_le_sum (fun g y => by rw [mul_comm g y, mul_inv_cancel_right]) ghat x m hx

/-- Additive form of H1 (obtained from the multiplicative statement in `Multiplicative V`): the
sum of the measured edge increments around a cycle is a lower bound for the total edge error of
any potential `x`. -/
theorem norm_sum_le_sum_edge_error {V : Type*} [SeminormedAddCommGroup V] (ghat x : ℕ → V)
    (m : ℕ) (hx : x m = x 0) :
    ‖∑ k ∈ range m, ghat k‖ ≤ ∑ k ∈ range m, ‖ghat k - (x (k + 1) - x k)‖ := by
  have h := norm_holProd_le_sum_of_comm (fun k => Multiplicative.ofAdd (ghat k))
    (fun k => Multiplicative.ofAdd (x k)) m (congrArg _ hx)
  rw [holProd_eq_prod] at h
  convert h using 1
  · rw [← ofAdd_sum]; rfl
  · refine sum_congr rfl fun k _ => ?_
    show ‖ghat k - (x (k + 1) - x k)‖ = ‖ghat k - (-(x k) + x (k + 1))‖
    rw [neg_add_eq_sub]

/-- Additive `ℓ²` form: `‖∑ ghat k‖² ≤ m ∑ ‖edge error‖²` for every potential `x` on the
cycle. -/
theorem norm_sum_sq_le_edge_error {V : Type*} [SeminormedAddCommGroup V] (ghat x : ℕ → V)
    (m : ℕ) (hx : x m = x 0) :
    ‖∑ k ∈ range m, ghat k‖ ^ 2 ≤ m * ∑ k ∈ range m, ‖ghat k - (x (k + 1) - x k)‖ ^ 2 := by
  have h1 := norm_sum_le_sum_edge_error ghat x m hx
  have h2 : (∑ k ∈ range m, ‖ghat k - (x (k + 1) - x k)‖) ^ 2 ≤
      ((range m).card : ℝ) * ∑ k ∈ range m, ‖ghat k - (x (k + 1) - x k)‖ ^ 2 :=
    sq_sum_le_card_mul_sum_sq
  rw [card_range] at h2
  exact (pow_le_pow_left₀ (norm_nonneg _) h1 2).trans h2

/-- **(H3, exactness)** In a real normed space the abelian holonomy bound is attained: spreading
the holonomy `h = ∑ ghat k` evenly over the `m` edges of the cycle gives a potential `x` with
`x m = x 0` all of whose edge errors equal `h / m`, so that both the `ℓ¹` bound and the `ℓ²` bound
hold with equality. -/
theorem exists_assignment_attaining_holonomy {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (ghat : ℕ → V) {m : ℕ} (hm : 0 < m) :
    ∃ x : ℕ → V, x m = x 0 ∧
      (∑ k ∈ range m, ‖ghat k - (x (k + 1) - x k)‖ = ‖∑ k ∈ range m, ghat k‖) ∧
      ((m : ℝ) * ∑ k ∈ range m, ‖ghat k - (x (k + 1) - x k)‖ ^ 2 =
        ‖∑ k ∈ range m, ghat k‖ ^ 2) := by
  have hm' : (m : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hm.ne'
  set h : V := ∑ k ∈ range m, ghat k with hh
  have hedge : ∀ k : ℕ,
      ghat k - ((∑ l ∈ range (k + 1), ghat l - ((k + 1 : ℕ) / m : ℝ) • h) -
        (∑ l ∈ range k, ghat l - ((k : ℕ) / m : ℝ) • h)) = (1 / m : ℝ) • h := by
    intro k
    rw [sum_range_succ]
    have : ((k + 1 : ℕ) / m : ℝ) = (k : ℝ) / m + 1 / m := by push_cast; ring
    rw [this, add_smul]
    abel
  refine ⟨fun k => ∑ l ∈ range k, ghat l - ((k : ℕ) / m : ℝ) • h, ?_, ?_, ?_⟩
  · simp [hm', ← hh]
  · simp only [hedge, norm_smul, sum_const, card_range, nsmul_eq_mul]
    rw [Real.norm_of_nonneg (by positivity)]
    field_simp
  · simp only [hedge, norm_smul, sum_const, card_range, nsmul_eq_mul]
    rw [Real.norm_of_nonneg (by positivity)]
    field_simp

end Abelian

/-! ## A non-commutative instance: linear isometries with the chordal seminorm -/

section Rotations

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]

/-- Deviation `g - 1` of a linear isometry from the identity, as a continuous linear map. -/
noncomputable def devId (g : V ≃ₗᵢ[ℝ] V) : V →L[ℝ] V :=
  (g : V →L[ℝ] V) - ContinuousLinearMap.id ℝ V

@[simp] theorem devId_apply (g : V ≃ₗᵢ[ℝ] V) (v : V) : devId g v = g v - v := rfl

theorem norm_devId_mul_le (g h : V ≃ₗᵢ[ℝ] V) : ‖devId (g * h)‖ ≤ ‖devId g‖ + ‖devId h‖ := by
  refine ContinuousLinearMap.opNorm_le_bound _ (by positivity) fun v => ?_
  have h1 : devId (g * h) v = devId g (h v) + devId h v := by
    simp only [devId_apply, LinearIsometryEquiv.coe_mul, Function.comp_apply]
    abel
  rw [h1, add_mul]
  refine (norm_add_le _ _).trans (add_le_add ?_ ((devId h).le_opNorm v))
  have := (devId g).le_opNorm (h v)
  rwa [LinearIsometryEquiv.norm_map] at this

theorem norm_devId_conj_le (g x : V ≃ₗᵢ[ℝ] V) : ‖devId (g * x * g⁻¹)‖ ≤ ‖devId x‖ := by
  refine ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _) fun v => ?_
  have h1 : devId (g * x * g⁻¹) v = g (devId x (g⁻¹ v)) := by
    simp only [devId_apply, LinearIsometryEquiv.coe_mul, Function.comp_apply, map_sub]
    simp
  rw [h1, LinearIsometryEquiv.norm_map]
  have := (devId x).le_opNorm (g⁻¹ v)
  rwa [LinearIsometryEquiv.norm_map] at this

theorem norm_devId_inv_le (g : V ≃ₗᵢ[ℝ] V) : ‖devId g⁻¹‖ ≤ ‖devId g‖ := by
  refine ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _) fun v => ?_
  have h1 : ‖devId g⁻¹ v‖ = ‖devId g (g⁻¹ v)‖ := by
    simp only [devId_apply]
    rw [norm_sub_rev]
    congr 1
    simp
  rw [h1]
  have := (devId g).le_opNorm (g⁻¹ v)
  rwa [LinearIsometryEquiv.norm_map] at this

/-- The chordal group seminorm `g ↦ ‖g - 1‖` (operator norm) on the group of linear isometries of
a real normed space; for a Euclidean space this is the orthogonal group with the chordal
distance. -/
noncomputable def chordalSeminorm (V : Type*) [NormedAddCommGroup V] [NormedSpace ℝ V] :
    GroupSeminorm (V ≃ₗᵢ[ℝ] V) where
  toFun g := ‖devId g‖
  map_one' := by
    have : devId (1 : V ≃ₗᵢ[ℝ] V) = 0 := by ext v; simp
    rw [this, norm_zero]
  mul_le' := norm_devId_mul_le
  inv' g := le_antisymm (norm_devId_inv_le g) (by simpa using norm_devId_inv_le g⁻¹)

theorem chordalSeminorm_apply (g : V ≃ₗᵢ[ℝ] V) : chordalSeminorm V g = ‖devId g‖ := rfl

/-- The chordal seminorm is conjugation invariant: hypothesis `hconj` of H1 holds in the
(non-commutative) group of linear isometries. -/
theorem chordalSeminorm_conj (g x : V ≃ₗᵢ[ℝ] V) :
    chordalSeminorm V (g * x * g⁻¹) = chordalSeminorm V x := by
  refine le_antisymm (norm_devId_conj_le g x) ?_
  have h := norm_devId_conj_le g⁻¹ (g * x * g⁻¹)
  have h2 : g⁻¹ * (g * x * g⁻¹) * g⁻¹⁻¹ = x := by group
  rw [h2] at h
  exact h

/-- The chordal seminorm of a quotient is the operator-norm distance. -/
theorem chordalSeminorm_div (g h : V ≃ₗᵢ[ℝ] V) :
    chordalSeminorm V (g / h) = ‖(g : V →L[ℝ] V) - (h : V →L[ℝ] V)‖ := by
  rw [chordalSeminorm_apply]
  refine le_antisymm ?_ ?_
  · refine ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _) fun v => ?_
    have h1 : devId (g / h) v = ((g : V →L[ℝ] V) - (h : V →L[ℝ] V)) (h⁻¹ v) := by
      simp [div_eq_mul_inv]
    rw [h1]
    have := ((g : V →L[ℝ] V) - (h : V →L[ℝ] V)).le_opNorm (h⁻¹ v)
    rwa [LinearIsometryEquiv.norm_map] at this
  · refine ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _) fun v => ?_
    have h1 : ((g : V →L[ℝ] V) - (h : V →L[ℝ] V)) v = devId (g / h) (h v) := by
      simp [div_eq_mul_inv]
    rw [h1]
    have := (devId (g / h)).le_opNorm (h v)
    rwa [LinearIsometryEquiv.norm_map] at this

/-- **H1 for rotation groups (abstract form).** -/
theorem chordal_holProd_le (ghat x : ℕ → (V ≃ₗᵢ[ℝ] V)) (m : ℕ) (hx : x m = x 0) :
    chordalSeminorm V (holProd ghat m) ≤
      ∑ k ∈ range m, chordalSeminorm V (ghat k / ((x k)⁻¹ * x (k + 1))) := by
  letI : SeminormedGroup (V ≃ₗᵢ[ℝ] V) := (chordalSeminorm V).toSeminormedGroup
  exact norm_holProd_le_sum (E := V ≃ₗᵢ[ℝ] V) chordalSeminorm_conj ghat x m hx

/-- **H1 for rotation groups (operator-norm form).** Around a cycle of frames `x 0, …, x m = x 0`
the holonomy of the measured relative rotations deviates from the identity by at most the sum of
the operator-norm errors of the measured relative rotations. -/
theorem opNorm_holProd_sub_id_le (ghat x : ℕ → (V ≃ₗᵢ[ℝ] V)) (m : ℕ) (hx : x m = x 0) :
    ‖((holProd ghat m : V ≃ₗᵢ[ℝ] V) : V →L[ℝ] V) - ContinuousLinearMap.id ℝ V‖ ≤
      ∑ k ∈ range m, ‖(ghat k : V →L[ℝ] V) - (((x k)⁻¹ * x (k + 1) : V ≃ₗᵢ[ℝ] V) : V →L[ℝ] V)‖ := by
  have h := chordal_holProd_le ghat x m hx
  simp only [chordalSeminorm_div] at h
  exact h

/-- The isometry group of the plane is not commutative (complex conjugation and the quarter turn
do not commute), so `chordal_holProd_le` is an instance of H1 that is not covered by H3. -/
theorem holonomy_check_1 : ∃ g h : ℂ ≃ₗᵢ[ℝ] ℂ, g * h ≠ h * g := by
  refine ⟨Complex.conjLIE, rotation (Circle.exp (Real.pi / 2)), fun hcomm => ?_⟩
  have h1 := congrArg (fun f : ℂ ≃ₗᵢ[ℝ] ℂ => (f 1).im) hcomm
  simp [rotation_apply, Circle.coe_exp] at h1
  linarith

end Rotations

/-! ## A second non-commutative instance: the angular (geodesic) seminorm -/

section Angular

variable {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]

/-- The largest angle by which the linear isometry `g` of a real inner product space turns a
non-zero vector.  For a rotation of Euclidean 3-space this is its rotation angle in `[0, π]`,
i.e. the geodesic distance to the identity in `SO(3)` (that identification is not proved here). -/
noncomputable def turnAngle (g : V ≃ₗᵢ[ℝ] V) : ℝ :=
  ⨆ v : {v : V // v ≠ 0}, InnerProductGeometry.angle (v : V) (g v)

theorem angle_le_turnAngle (g : V ≃ₗᵢ[ℝ] V) {v : V} (hv : v ≠ 0) :
    InnerProductGeometry.angle v (g v) ≤ turnAngle g := by
  have hbdd : BddAbove (Set.range fun v : {v : V // v ≠ 0} =>
      InnerProductGeometry.angle (v : V) (g v)) :=
    ⟨Real.pi, by rintro _ ⟨w, rfl⟩; exact InnerProductGeometry.angle_le_pi _ _⟩
  exact le_ciSup hbdd ⟨v, hv⟩

theorem turnAngle_le (g : V ≃ₗᵢ[ℝ] V) {c : ℝ} (hc : 0 ≤ c)
    (h : ∀ v : V, v ≠ 0 → InnerProductGeometry.angle v (g v) ≤ c) : turnAngle g ≤ c :=
  Real.iSup_le (fun v => h v v.2) hc

theorem turnAngle_nonneg (g : V ≃ₗᵢ[ℝ] V) : 0 ≤ turnAngle g :=
  Real.iSup_nonneg fun _ => InnerProductGeometry.angle_nonneg _ _

/-- Subadditivity of the turning angle: the spherical triangle inequality. -/
theorem turnAngle_mul_le (g h : V ≃ₗᵢ[ℝ] V) : turnAngle (g * h) ≤ turnAngle g + turnAngle h := by
  refine turnAngle_le _ (add_nonneg (turnAngle_nonneg g) (turnAngle_nonneg h)) fun v hv => ?_
  have hhv : h v ≠ 0 := fun h0 => hv (h.map_eq_zero_iff.mp h0)
  calc InnerProductGeometry.angle v ((g * h) v)
      ≤ InnerProductGeometry.angle v (h v) + InnerProductGeometry.angle (h v) (g (h v)) :=
        InnerProductGeometry.angle_le_angle_add_angle _ _ _
    _ ≤ turnAngle h + turnAngle g := add_le_add (angle_le_turnAngle h hv) (angle_le_turnAngle g hhv)
    _ = turnAngle g + turnAngle h := add_comm _ _

theorem turnAngle_conj_le (g x : V ≃ₗᵢ[ℝ] V) : turnAngle (g * x * g⁻¹) ≤ turnAngle x := by
  refine turnAngle_le _ (turnAngle_nonneg x) fun v hv => ?_
  have hw : g⁻¹ v ≠ 0 := fun h0 => hv ((g⁻¹).map_eq_zero_iff.mp h0)
  have h1 : InnerProductGeometry.angle v ((g * x * g⁻¹) v) =
      InnerProductGeometry.angle (g⁻¹ v) (x (g⁻¹ v)) := by
    rw [← g.toLinearIsometry.angle_map (g⁻¹ v) (x (g⁻¹ v))]
    simp
  rw [h1]
  exact angle_le_turnAngle x hw

theorem turnAngle_inv_le (g : V ≃ₗᵢ[ℝ] V) : turnAngle g⁻¹ ≤ turnAngle g := by
  refine turnAngle_le _ (turnAngle_nonneg g) fun v hv => ?_
  have hw : g⁻¹ v ≠ 0 := fun h0 => hv ((g⁻¹).map_eq_zero_iff.mp h0)
  have h1 : InnerProductGeometry.angle v (g⁻¹ v) =
      InnerProductGeometry.angle (g⁻¹ v) (g (g⁻¹ v)) := by
    rw [InnerProductGeometry.angle_comm]
    simp
  rw [h1]
  exact angle_le_turnAngle g hw

/-- The angular group seminorm `g ↦ turnAngle g` on the group of linear isometries of a real
inner product space. -/
noncomputable def angularSeminorm (V : Type*) [NormedAddCommGroup V] [InnerProductSpace ℝ V] :
    GroupSeminorm (V ≃ₗᵢ[ℝ] V) where
  toFun := turnAngle
  map_one' := le_antisymm
    (turnAngle_le _ le_rfl fun v hv => by simp [InnerProductGeometry.angle_self hv])
    (turnAngle_nonneg _)
  mul_le' := turnAngle_mul_le
  inv' g := le_antisymm (turnAngle_inv_le g) (by simpa using turnAngle_inv_le g⁻¹)

/-- The turning angle is conjugation invariant: hypothesis `hconj` of H1 holds for the angular
seminorm. -/
theorem turnAngle_conj (g x : V ≃ₗᵢ[ℝ] V) : turnAngle (g * x * g⁻¹) = turnAngle x := by
  refine le_antisymm (turnAngle_conj_le g x) ?_
  have h := turnAngle_conj_le g⁻¹ (g * x * g⁻¹)
  have h2 : g⁻¹ * (g * x * g⁻¹) * g⁻¹⁻¹ = x := by group
  rw [h2] at h
  exact h

/-- **H1 for rotation groups with the angular (geodesic) norm.** Around a cycle of frames
`x 0, …, x m = x 0` the turning angle of the holonomy of the measured relative rotations is at
most the sum of the angular errors of the edges. -/
theorem turnAngle_holProd_le (ghat x : ℕ → (V ≃ₗᵢ[ℝ] V)) (m : ℕ) (hx : x m = x 0) :
    turnAngle (holProd ghat m) ≤
      ∑ k ∈ range m, turnAngle (ghat k / ((x k)⁻¹ * x (k + 1))) := by
  letI : SeminormedGroup (V ≃ₗᵢ[ℝ] V) := (angularSeminorm V).toSeminormedGroup
  exact norm_holProd_le_sum (E := V ≃ₗᵢ[ℝ] V) turnAngle_conj ghat x m hx

/-- The angular seminorm is not trivial: the point reflection of the line turns every non-zero
vector by `π`. -/
theorem holonomy_check_2 : turnAngle (LinearIsometryEquiv.neg ℝ : ℝ ≃ₗᵢ[ℝ] ℝ) = Real.pi := by
  refine le_antisymm
    (turnAngle_le _ Real.pi_pos.le fun v _ => InnerProductGeometry.angle_le_pi _ _) ?_
  have h := angle_le_turnAngle (LinearIsometryEquiv.neg ℝ : ℝ ≃ₗᵢ[ℝ] ℝ) (v := 1) one_ne_zero
  simpa [InnerProductGeometry.angle_self_neg_of_nonzero] using h

end Angular

/-! ## Non-vacuity checks -/

section Examples

/-- H1 in the concrete commutative group `Multiplicative ℝ`: three edges each measuring the
increment `1` around a triangle, all vertex frames trivial.  The hypotheses hold, the holonomy has
norm `3`, and the total edge error is `3`: the bound is attained with non-zero holonomy. -/
theorem holonomy_check_3 :
    ∃ ghat x : ℕ → Multiplicative ℝ,
      (∀ g y : Multiplicative ℝ, ‖g * y * g⁻¹‖ = ‖y‖) ∧ x 3 = x 0 ∧
      ‖holProd ghat 3‖ = 3 ∧ ∑ k ∈ range 3, ‖ghat k / ((x k)⁻¹ * x (k + 1))‖ = 3 := by
  refine ⟨fun _ => Multiplicative.ofAdd (1 : ℝ), fun _ => 1,
    fun g y => by rw [mul_comm g y, mul_inv_cancel_right], rfl, ?_, ?_⟩
  · rw [holProd_eq_prod]
    simp only [prod_const, card_range]
    rw [← ofAdd_nsmul, norm_ofAdd]
    norm_num
  · simp

/-- The conclusion of H1 for that instance, obtained from the theorem itself. -/
theorem holonomy_check_4 :
    ‖holProd (fun _ => Multiplicative.ofAdd (1 : ℝ)) 3‖ ≤
      ∑ _k ∈ range 3, ‖Multiplicative.ofAdd (1 : ℝ) / ((1 : Multiplicative ℝ)⁻¹ * 1)‖ :=
  norm_holProd_le_sum (fun g y => by rw [mul_comm g y, mul_inv_cancel_right])
    (fun _ => Multiplicative.ofAdd (1 : ℝ)) (fun _ => 1) 3 rfl

/-- H2 on the line: trivial rotations, all frames at the origin, three measured translations `1`.
The hypotheses hold with `ρ = 0`, the translation holonomy has norm `3` and equals the bound. -/
theorem holonomy_check_5 :
    ‖holTrans (fun _ => LinearIsometryEquiv.refl ℝ ℝ) (fun _ => (1 : ℝ)) 3‖ = 3 ∧
      (∑ _k ∈ range 3, ‖(1 : ℝ) - (LinearIsometryEquiv.refl ℝ ℝ).symm ((0 : ℝ) - 0)‖ +
        ∑ k ∈ range 3, (∑ _l ∈ range k, (0 : ℝ)) * ‖(1 : ℝ)‖) = 3 := by
  constructor
  · have h : ∀ k, accRot (fun _ => LinearIsometryEquiv.refl ℝ ℝ) k (1 : ℝ) = 1 := by
      intro k
      induction k with
      | zero => rfl
      | succ k ih => rw [accRot_succ_apply]; exact ih
    simp [holTrans, h]
  · simp

end Examples

end MetricChain
