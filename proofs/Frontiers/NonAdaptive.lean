import Mathlib
import proofs.Frontiers.QueryLowerBound

/-!
# Algorithms without a hint: non-adaptive lower bounds and the tail lemma

Theory report §11.16.  Two machine-checked ingredients of the statement that plain Monte Carlo
is exponent-optimal among **non-adaptive** algorithms on the Hamming–Lipschitz class of the cube,
and that adaptivity is necessary to do better.

* `nonadaptive_expected_queries_ge` — a lower bound for algorithms whose set of evaluated points
  does not depend on the answers: for a family of pairs `(g j, g' j)` of class members whose
  values of `Φ` differ by more than `ε`, and weights such that every point lies in difference
  sets of total weight at most `B`, the expected number of evaluations is at least
  `(1 - 2δ) (∑ w) / B`.  For adaptive algorithms only alternatives of one common instance can be
  combined in this way (`expected_queries_ge_packing`); here both members of the pair may vary,
  because the query set is the same on every instance.
* `cube_nonadaptive_bound` — the instance: the cones `c · dist (·, s)` and their flattened
  versions `max (c · dist (·, s)) R`, one pair for every centre `s`.  A non-adaptive algorithm
  needs at least `(1 - 2δ) 2^n / |B|` evaluations, `|B|` the size of the open Hamming ball on which
  the two differ.  An adaptive algorithm reads the centre off `n + 1` evaluations.
* `weight_le_of_outside`, `sum_le_truncated_add_tail` — the tail lemma behind the matching upper
  bound: above a threshold `t`, a Gibbs weight of an admissible residual is at most `t` times
  `exp (β · (envelope distance to a point below the threshold))`; hence the partition function is
  at most the sum of the truncated weights plus `t` times a purely geometric sum over the
  super-level set.  `weight_ge_of_inside`, `sum_truncated_ge` bound the truncated weights from
  below by another geometric sum.  **Not formalised here**: the comparison of the two geometric
  sums with their values for Hamming balls (a paper reduction to Harper's vertex-isoperimetric
  theorem), the closed forms of the sums in `cube_nonadaptive_bound`, and every asymptotic
  statement — in particular the exponent of theory report Theorems 11.44–11.45.
-/

namespace MetricChain

open Finset

/-! ### Non-adaptive algorithms -/

section NonAdaptive

variable {X : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ} {Ω : Type*} [Fintype Ω]

open Classical in
/-- **Non-adaptive packing bound.**  Let `alg ω` be algorithms indexed by a finite probability
space whose query sets `Q ω` do not depend on the residual, `(ε/2, δ)`-correct for `Φ` on the
class `G`.  Let `(g j, g' j)` be pairs of class members with `|Φ (g' j) - Φ (g j)| > ε` and
`w ≥ 0` weights such that every point `a` lies in difference sets `{g' j ≠ g j}` of total weight
at most `B`.  Then `(1 - 2δ) ∑ w ≤ E|Q| · B`. -/
theorem nonadaptive_expected_queries_ge {ι : Type*} [Fintype ι] (alg : Ω → QueryAlgorithm X)
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    (Q : Ω → Finset X) (hna : ∀ ω g, (alg ω).queries g = Q ω)
    (g g' : ι → X → ℝ) (hg : ∀ j, G (g j)) (hg' : ∀ j, G (g' j))
    (hsens : ∀ j, ε < |Φ (g' j) - Φ (g j)|) (w : ι → ℝ) (hw : ∀ j, 0 ≤ w j) {B : ℝ}
    (hcap : ∀ a, ∑ j ∈ univ.filter (fun j => g' j a ≠ g j a), w j ≤ B) :
    (1 - 2 * δ) * ∑ j, w j ≤ (∑ ω, P ω * (Q ω).card) * B := by
  have hdet : ∀ j, 1 - 2 * δ ≤
      ∑ ω ∈ univ.filter (fun ω => ∃ a ∈ Q ω, g' j a ≠ g j a), P ω := by
    intro j
    have h := prob_query_ne_ge alg P hP hP1 hcorr (hg j) (hg' j) (hsens j)
    have hfil : univ.filter (fun ω => ∃ a ∈ (alg ω).queries (g j), g' j a ≠ g j a) =
        univ.filter (fun ω => ∃ a ∈ Q ω, g' j a ≠ g j a) := by
      refine Finset.filter_congr fun ω _ => ?_
      rw [hna ω (g j)]
    rwa [hfil] at h
  have hrun : ∀ ω, ∑ j ∈ univ.filter (fun j => ∃ a ∈ Q ω, g' j a ≠ g j a), w j ≤
      (Q ω).card * B := fun ω =>
    sum_detected_le_card (R := fun a j => g' j a ≠ g j a) (Q ω) w hw fun a _ => hcap a
  calc (1 - 2 * δ) * ∑ j, w j = ∑ j, w j * (1 - 2 * δ) := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl fun j _ => mul_comm _ _
    _ ≤ ∑ j, w j * ∑ ω ∈ univ.filter (fun ω => ∃ a ∈ Q ω, g' j a ≠ g j a), P ω :=
        Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_left (hdet j) (hw j)
    _ = ∑ j, ∑ ω, if (∃ a ∈ Q ω, g' j a ≠ g j a) then w j * P ω else 0 := by
        refine Finset.sum_congr rfl fun j _ => ?_
        rw [Finset.mul_sum, Finset.sum_filter]
    _ = ∑ ω, ∑ j, if (∃ a ∈ Q ω, g' j a ≠ g j a) then w j * P ω else 0 :=
        Finset.sum_comm
    _ = ∑ ω, P ω * ∑ j ∈ univ.filter (fun j => ∃ a ∈ Q ω, g' j a ≠ g j a), w j := by
        refine Finset.sum_congr rfl fun ω _ => ?_
        rw [Finset.mul_sum, Finset.sum_filter]
        refine Finset.sum_congr rfl fun j _ => ?_
        split_ifs
        · ring
        · simp
    _ ≤ ∑ ω, P ω * ((Q ω).card * B) :=
        Finset.sum_le_sum fun ω _ => mul_le_mul_of_nonneg_left (hrun ω) (hP ω)
    _ = (∑ ω, P ω * (Q ω).card) * B := by
        rw [Finset.sum_mul]
        exact Finset.sum_congr rfl fun ω _ => by ring

end NonAdaptive

/-! ### Cones and flattened cones on the cube -/

section CubeNonAdaptive

variable {Ω : Type*} [Fintype Ω]

/-- The cone `c · dist (·, s)` is admissible for the envelope `c ·` Hamming distance. -/
theorem cone_admissible {n : ℕ} {c : ℝ} (hc : 0 ≤ c) (s : Fin n → Bool) :
    Admissible (hamEnv fun _ : Fin n => c) fun x => hamEnv (fun _ : Fin n => c) x s := by
  intro x y
  have h := (hamEnv_isEnvelope (σ := fun _ : Fin n => Bool) (c := fun _ => c) fun _ => hc).triangle
    x y s
  linarith

/-- The weighted Hamming envelope is nonnegative for nonnegative site constants. -/
theorem hamEnv_nonneg' {n : ℕ} {c : ℝ} (hc : 0 ≤ c) (x y : Fin n → Bool) :
    0 ≤ hamEnv (fun _ : Fin n => c) x y := by
  unfold hamEnv
  refine Finset.sum_nonneg fun i _ => ?_
  split_ifs
  · exact le_rfl
  · exact hc

/-- The cone with a flattened bottom, `max (c · dist (·, s)) R`, is admissible. -/
theorem flatCone_admissible {n : ℕ} {c : ℝ} (hc : 0 ≤ c) (R : ℝ) (s : Fin n → Bool) :
    Admissible (hamEnv fun _ : Fin n => c)
      fun x => max (hamEnv (fun _ : Fin n => c) x s) R := by
  intro x y
  have h1 := cone_admissible (n := n) hc s x y
  have h2 := max_sub_max_le_max (hamEnv (fun _ : Fin n => c) x s) R
    (hamEnv (fun _ : Fin n => c) y s) R
  have h3 : max (hamEnv (fun _ : Fin n => c) x s - hamEnv (fun _ : Fin n => c) y s) (R - R) ≤
      hamEnv (fun _ : Fin n => c) x y := by
    rw [sub_self]
    exact max_le h1 (hamEnv_nonneg' hc x y)
  exact h2.trans h3

open Classical in
/-- **Non-adaptive algorithms on the cube.**  Zero known part, envelope `c ·` Hamming distance.
If flattening the bottom of a cone at level `R` lowers `log Z` by more than `ε`, and every open
Hamming ball `{s : c · dist (a, s) < R}` has at most `B` points, then every randomised
**non-adaptive** algorithm that is `(ε/2, δ)`-correct on the class makes at least
`(1 - 2δ) 2^n / B` evaluations in expectation.  (An adaptive algorithm finds the centre of a cone
with `n + 1` evaluations.) -/
theorem cube_nonadaptive_bound (n : ℕ) (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ)
    (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {β c ε δ R : ℝ} (hc : 0 ≤ c)
    (Q : Ω → Finset (Fin n → Bool)) (hna : ∀ ω g, (alg ω).queries g = Q ω)
    (hsens : ∀ s : Fin n → Bool, ε <
      Real.log (∑ x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + hamEnv (fun _ : Fin n => c) x s))) -
      Real.log (∑ x : Fin n → Bool,
        Real.exp (-β * ((0 : ℝ) + max (hamEnv (fun _ : Fin n => c) x s) R))))
    {B : ℝ} (hB : ∀ a : Fin n → Bool,
      ((univ.filter fun s : Fin n → Bool => hamEnv (fun _ : Fin n => c) a s < R).card : ℝ) ≤ B)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ ε / 2), P ω) :
    (1 - 2 * δ) * 2 ^ n ≤ (∑ ω, P ω * (Q ω).card) * B := by
  have key := nonadaptive_expected_queries_ge
    (Φ := fun g : (Fin n → Bool) → ℝ => Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x))))
    (G := Admissible (hamEnv fun _ : Fin n => c)) alg P hP hP1 hcorr Q hna
    (fun s x => hamEnv (fun _ : Fin n => c) x s)
    (fun s x => max (hamEnv (fun _ : Fin n => c) x s) R)
    (fun s => cone_admissible hc s) (fun s => flatCone_admissible hc R s)
    (fun s => by
      have h := hsens s
      rw [abs_sub_comm]
      exact lt_of_lt_of_le h (le_abs_self _))
    (fun _ => (1 : ℝ)) (fun _ => zero_le_one) (B := B)
    (fun a => by
      have hcongr : (univ.filter fun s : Fin n → Bool =>
          max (hamEnv (fun _ : Fin n => c) a s) R ≠ hamEnv (fun _ : Fin n => c) a s) =
          univ.filter fun s : Fin n → Bool => hamEnv (fun _ : Fin n => c) a s < R := by
        refine Finset.filter_congr fun s _ => ?_
        constructor
        · intro hne
          by_contra hle
          exact hne (max_eq_left (not_lt.mp hle))
        · intro hlt heq
          have : R ≤ hamEnv (fun _ : Fin n => c) a s := heq ▸ le_max_right _ _
          linarith
      rw [hcongr, Finset.sum_const, nsmul_eq_mul, mul_one]
      exact hB a)
  have hcard : ∑ _s : Fin n → Bool, (1 : ℝ) = (2 : ℝ) ^ n := by
    simp
  rw [hcard] at key
  exact key

end CubeNonAdaptive

/-! ### The tail lemma -/

section Tail

variable {X : Type*}

/-- **Pointwise tail bound.**  If the Gibbs weight of `z` is at most `t`, the weight of any `x`
is at most `t · exp (β d z x)`: an admissible residual cannot fall faster than the envelope. -/
theorem weight_le_of_outside {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) {β t : ℝ}
    (hβ : 0 ≤ β) {x z : X} (hz : Real.exp (-β * g z) ≤ t) :
    Real.exp (-β * g x) ≤ t * Real.exp (β * d z x) := by
  have h1 : g z - g x ≤ d z x := hg z x
  have hsplit : Real.exp (-β * g x) = Real.exp (-β * g z) * Real.exp (β * (g z - g x)) := by
    rw [← Real.exp_add]
    ring_nf
  have h2 : Real.exp (β * (g z - g x)) ≤ Real.exp (β * d z x) :=
    Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left h1 hβ)
  have ht : 0 ≤ t := (Real.exp_pos _).le.trans hz
  calc Real.exp (-β * g x) = Real.exp (-β * g z) * Real.exp (β * (g z - g x)) := hsplit
    _ ≤ t * Real.exp (β * (g z - g x)) := mul_le_mul_of_nonneg_right hz (Real.exp_pos _).le
    _ ≤ t * Real.exp (β * d z x) := mul_le_mul_of_nonneg_left h2 ht

variable [Fintype X]

open Classical in
/-- **Tail lemma.**  Let `g` be admissible, `t` a threshold, and let `ρ x` bound the envelope
distance from some point of weight at most `t` to `x`, for every `x` of weight above `t`.  Then

  `∑_x exp (-β g x) ≤ ∑_x min (exp (-β g x)) t + t · ∑_{x : weight > t} (exp (β ρ x) - 1)`.

The second sum depends only on the geometry of the super-level set.  On the cube, with
`ρ = c · dist (·, complement)`, Harper's theorem bounds it by its value for a Hamming ball of the
same size, which is the excess of a dip at the zero residual (`cube_exact_dip_randomized`). -/
theorem sum_le_truncated_add_tail {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) {β t : ℝ}
    (hβ : 0 ≤ β) (ρ : X → ℝ)
    (hρ : ∀ x, t < Real.exp (-β * g x) → ∃ z, Real.exp (-β * g z) ≤ t ∧ d z x ≤ ρ x) :
    ∑ x, Real.exp (-β * g x) ≤ ∑ x, min (Real.exp (-β * g x)) t +
      t * ∑ x ∈ univ.filter (fun x => t < Real.exp (-β * g x)), (Real.exp (β * ρ x) - 1) := by
  have hpt : ∀ x, Real.exp (-β * g x) ≤ min (Real.exp (-β * g x)) t +
      (if t < Real.exp (-β * g x) then t * (Real.exp (β * ρ x) - 1) else 0) := by
    intro x
    by_cases hx : t < Real.exp (-β * g x)
    · rw [if_pos hx, min_eq_right hx.le]
      obtain ⟨z, hz, hdz⟩ := hρ x hx
      have h1 := weight_le_of_outside hg hβ (x := x) hz
      have ht : 0 ≤ t := (Real.exp_pos _).le.trans hz
      have h2 : t * Real.exp (β * d z x) ≤ t * Real.exp (β * ρ x) :=
        mul_le_mul_of_nonneg_left
          (Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left hdz hβ)) ht
      linarith
    · rw [if_neg hx, min_eq_left (not_lt.mp hx)]
      simp
  calc ∑ x, Real.exp (-β * g x)
      ≤ ∑ x, (min (Real.exp (-β * g x)) t +
          (if t < Real.exp (-β * g x) then t * (Real.exp (β * ρ x) - 1) else 0)) :=
        Finset.sum_le_sum fun x _ => hpt x
    _ = ∑ x, min (Real.exp (-β * g x)) t +
          t * ∑ x ∈ univ.filter (fun x => t < Real.exp (-β * g x)),
            (Real.exp (β * ρ x) - 1) := by
        rw [Finset.sum_add_distrib, Finset.mul_sum, Finset.sum_filter]

omit [Fintype X] in
/-- **Pointwise bound from the other side.**  If the Gibbs weight of `y` is at least `t`, the
weight of any `x` is at least `t · exp (-β d x y)`: an admissible residual cannot rise faster than
the envelope either. -/
theorem weight_ge_of_inside {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) {β t : ℝ}
    (hβ : 0 ≤ β) (ht : 0 ≤ t) {x y : X} (hy : t ≤ Real.exp (-β * g y)) :
    t * Real.exp (-β * d x y) ≤ Real.exp (-β * g x) := by
  have h1 : g x - g y ≤ d x y := hg x y
  have hsplit : Real.exp (-β * g x) = Real.exp (-β * g y) * Real.exp (-β * (g x - g y)) := by
    rw [← Real.exp_add]
    ring_nf
  have h2 : Real.exp (-β * d x y) ≤ Real.exp (-β * (g x - g y)) :=
    Real.exp_le_exp.mpr (by nlinarith)
  calc t * Real.exp (-β * d x y) ≤ t * Real.exp (-β * (g x - g y)) :=
        mul_le_mul_of_nonneg_left h2 ht
    _ ≤ Real.exp (-β * g y) * Real.exp (-β * (g x - g y)) :=
        mul_le_mul_of_nonneg_right hy (Real.exp_pos _).le
    _ = Real.exp (-β * g x) := hsplit.symm

open Classical in
/-- **Two-sided tail lemma, lower half** (suggested by the fifth referee).  Let `ρ x` bound the
envelope distance from `x` to some point of weight at least `t`, for every `x` of weight below
`t`, and let `ρ x = 0` otherwise.  Then the truncated weights carry at least

  `∑_x min (exp (-β g x)) t ≥ t · ∑_x exp (-β ρ x)`.

On the cube, with `ρ = c · dist (·, {weight ≥ t})`, Harper's theorem bounds the right-hand side
below by its value for a Hamming ball of the same size.  Together with
`sum_le_truncated_add_tail` this compares the mass above a threshold with the truncated mass,
for every member of the class, and gives the accuracy of Monte Carlo at every fixed accuracy. -/
theorem sum_truncated_ge {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) {β t : ℝ}
    (hβ : 0 ≤ β) (ht : 0 ≤ t) (ρ : X → ℝ)
    (hρ : ∀ x, Real.exp (-β * g x) < t → ∃ y, t ≤ Real.exp (-β * g y) ∧ d x y ≤ ρ x)
    (hρ0 : ∀ x, t ≤ Real.exp (-β * g x) → ρ x = 0) :
    t * ∑ x, Real.exp (-β * ρ x) ≤ ∑ x, min (Real.exp (-β * g x)) t := by
  rw [Finset.mul_sum]
  refine Finset.sum_le_sum fun x _ => ?_
  by_cases hx : Real.exp (-β * g x) < t
  · rw [min_eq_left hx.le]
    obtain ⟨y, hy, hdy⟩ := hρ x hx
    have h1 := weight_ge_of_inside hg hβ ht (x := x) hy
    have h2 : Real.exp (-β * ρ x) ≤ Real.exp (-β * d x y) :=
      Real.exp_le_exp.mpr (by nlinarith)
    calc t * Real.exp (-β * ρ x) ≤ t * Real.exp (-β * d x y) :=
          mul_le_mul_of_nonneg_left h2 ht
      _ ≤ Real.exp (-β * g x) := h1
  · have hx' := not_lt.mp hx
    rw [min_eq_right hx', hρ0 x hx']
    simp

end Tail

end MetricChain
