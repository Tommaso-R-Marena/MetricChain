import Mathlib
import proofs.Core.Basic
import proofs.Frontiers.EnvelopeDuality

/-!
# Certification geometry: certificates are coverings in the slack quasi-metric

Setting of `EnvelopeDuality.lean`: a known part `f`, an unknown residual `g` admissible for an
envelope `d`, energy `E = f + g`, and a finite set `A` of points at which `g` has been evaluated.

The **slack** of the envelope between `a` and `y` for the residual `g` is

  `slack d g a y = d a y - g a + g y ≥ 0`,

the amount by which the envelope inequality `g a - g y ≤ d a y` fails to be tight.  It is again an
envelope (zero diagonal, triangle inequality), and it is the geometry in which certification takes
place:

* `lowerEnv_eq_sub_slack`, `upperEnv_eq_add_slack` — the McShane bracket at `y` is
  `[g y - s(A, y), g y + s(y, A)]`: its half-widths are the slack distances from and to the
  evaluated set;
* `certLB_eq` — the best lower bound on `min E` that is valid for every residual consistent with
  the evaluations is `min_y (E y - s(A, y))`;
* `isCertificate_iff_cover` — the evaluated set certifies `ε`-optimality (`certUB - certLB ≤ ε`)
  iff every `y` lies within slack distance `E y - certUB + ε` of `A`: a **covering problem whose
  radii are the points' own optimality gaps**;
* `cover_of_certificate`, `certificate_of_cover` — up to one extra evaluation (a minimiser) the
  minimal certificate size is the covering number at the level `E* - ε`.

Lower bounds on the size of any cover, for an arbitrary covering relation `R`
(all are instances of weak duality for the covering linear program):

* `card_ge_of_weights` — any weighting with total weight at most one on every covered set;
* `card_ge_of_fooling`, `mem_of_forced` — packings ("fooling sets") and forced points;
  `anchor_necessary'` re-derives the witness-size bound of `EnvelopeDuality.lean` from it;
* `card_ge_sum_inv` — the volume form `∑_y 1 / M y ≤ |A|` (a discrete version of the integral
  `∫ dx / vol(ball of radius gap(x) + ε)` of certified Lipschitz optimisation);
* `partition_bound` — **partition-function bound**: for every `t ≥ 0`,
  `e^{-tε} ∑_y e^{-t·gap(y)} ≤ |A| · B` whenever `∑_y e^{-t·slack a y} ≤ B` for all `a`:
  the number of evaluations is at least the partition function of the true landscape at inverse
  temperature `t` divided by the partition function of a slack ball.
-/

namespace MetricChain

open Finset

variable {X : Type*}

/-! ### The slack quasi-metric -/

/-- Slack of the envelope inequality `g a - g y ≤ d a y`. -/
def slack (d : X → X → ℝ) (g : X → ℝ) (a y : X) : ℝ := d a y - g a + g y

theorem slack_nonneg {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (a y : X) :
    0 ≤ slack d g a y := by
  have := hg a y
  unfold slack
  linarith

theorem slack_self {d : X → X → ℝ} (hd : IsEnvelope d) (g : X → ℝ) (a : X) :
    slack d g a a = 0 := by
  unfold slack
  rw [hd.self a]
  ring

theorem slack_triangle {d : X → X → ℝ} (hd : IsEnvelope d) (g : X → ℝ) (a y z : X) :
    slack d g a z ≤ slack d g a y + slack d g y z := by
  have := hd.triangle a y z
  unfold slack
  linarith

/-- The slack is again an envelope. -/
theorem slack_isEnvelope {d : X → X → ℝ} (hd : IsEnvelope d) (g : X → ℝ) :
    IsEnvelope (slack d g) :=
  ⟨slack_self hd g, slack_triangle hd g⟩

/-- If the residual is `κ`-Lipschitz for the envelope, the slack dominates `(1 - κ) d`. -/
theorem slack_ge_of_lipschitz {d : X → X → ℝ} {g : X → ℝ} {κ : ℝ}
    (hgκ : ∀ x y, g x - g y ≤ κ * d x y) (a y : X) : (1 - κ) * d a y ≤ slack d g a y := by
  have := hgκ a y
  unfold slack
  linarith

/-- Slack distance from a finite set to a point. -/
noncomputable def slackFrom (d : X → X → ℝ) (g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    (y : X) : ℝ :=
  A.inf' hA fun a => slack d g a y

/-- Slack distance from a point to a finite set. -/
noncomputable def slackTo (d : X → X → ℝ) (g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    (y : X) : ℝ :=
  A.inf' hA fun a => slack d g y a

/-- **McShane lower envelope in slack form**: `L_A y = g y - s(A, y)`. -/
theorem lowerEnv_eq_sub_slack (d : X → X → ℝ) (g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    (y : X) : lowerEnv d A hA g y = g y - slackFrom d g A hA y := by
  unfold lowerEnv slackFrom
  apply le_antisymm
  · apply Finset.sup'_le
    intro a ha
    have h := Finset.inf'_le (fun a => slack d g a y) ha
    unfold slack at h ⊢
    linarith
  · obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => slack d g a y)
    have h := Finset.le_sup' (fun a => g a - d a y) ha
    rw [hmin]
    unfold slack
    linarith

/-- **McShane upper envelope in slack form**: `U_A y = g y + s(y, A)`. -/
theorem upperEnv_eq_add_slack (d : X → X → ℝ) (g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    (y : X) : upperEnv d A hA g y = g y + slackTo d g A hA y := by
  unfold upperEnv slackTo
  apply le_antisymm
  · obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => slack d g y a)
    have h := Finset.inf'_le (fun a => g a + d y a) ha
    rw [hmin]
    unfold slack
    linarith
  · apply Finset.le_inf'
    intro a ha
    have h := Finset.inf'_le (fun a => slack d g y a) ha
    have h' : slack d g y a = d y a - g y + g a := rfl
    linarith

/-! ### Certificates and coverings -/

section Certificates

variable [Fintype X] [Nonempty X]

/-- The certified lower bound on `min (f + h)` over all residuals `h` consistent with the
evaluations of `g` on `A`: the minimum of `f` plus the lower McShane envelope. -/
noncomputable def certLB (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty) : ℝ :=
  univ.inf' univ_nonempty fun y => f y + lowerEnv d A hA g y

/-- The incumbent: the best evaluated energy. -/
noncomputable def certUB (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty) : ℝ :=
  A.inf' hA fun a => f a + g a

/-- The evaluated set `A` is an `ε`-certificate: the incumbent is within `ε` of the certified
lower bound. -/
def IsCertificate (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty) (ε : ℝ) :
    Prop :=
  certUB f g A hA - certLB d f g A hA ≤ ε

/-- **Soundness of the certified lower bound**: it is below `f + h` everywhere, for every
admissible residual `h` that agrees with `g` on the evaluated set. -/
theorem certLB_le {d : X → X → ℝ} (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty) {h : X → ℝ}
    (hh : Admissible d h) (hAg : ∀ a ∈ A, h a = g a) (y : X) :
    certLB d f g A hA ≤ f y + h y := by
  have h1 : certLB d f g A hA ≤ f y + lowerEnv d A hA g y :=
    Finset.inf'_le (fun y => f y + lowerEnv d A hA g y) (mem_univ y)
  have h2 := lowerEnv_le hh A hA g hAg y
  linarith

/-- The certified lower bound is attained by an admissible residual consistent with the data (the
lower McShane envelope itself): no better bound is valid. -/
theorem certLB_attained {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) {g : X → ℝ}
    (hg : Admissible d g) (A : Finset X) (hA : A.Nonempty) :
    ∃ h, Admissible d h ∧ (∀ a ∈ A, h a = g a) ∧ ∃ y, f y + h y = certLB d f g A hA := by
  refine ⟨lowerEnv d A hA g, lowerEnv_admissible hd A hA g, fun a ha => ?_, ?_⟩
  · exact lowerEnv_eq_of_mem hd A hA g (fun a _ b _ => hg a b) ha
  · obtain ⟨y, _, hy⟩ := Finset.exists_mem_eq_inf' univ_nonempty
      (fun y => f y + lowerEnv d A hA g y)
    exact ⟨y, hy.symm⟩

/-- **Certified lower bound in slack form**: `LB(A) = min_y (E y - s(A, y))`. -/
theorem certLB_eq (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty) :
    certLB d f g A hA =
      univ.inf' univ_nonempty fun y => f y + g y - slackFrom d g A hA y := by
  unfold certLB
  congr 1
  funext y
  rw [lowerEnv_eq_sub_slack]
  ring

/-- **Certificates are coverings.**  `A` is an `ε`-certificate iff every point `y` is within slack
distance `E y - UB(A) + ε` of some evaluated point. -/
theorem isCertificate_iff_cover (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    (ε : ℝ) :
    IsCertificate d f g A hA ε ↔
      ∀ y, ∃ a ∈ A, slack d g a y ≤ f y + g y - certUB f g A hA + ε := by
  unfold IsCertificate
  rw [certLB_eq]
  constructor
  · intro h y
    obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => slack d g a y)
    have h1 : univ.inf' univ_nonempty (fun y => f y + g y - slackFrom d g A hA y) ≤
        f y + g y - slackFrom d g A hA y :=
      Finset.inf'_le (fun y => f y + g y - slackFrom d g A hA y) (mem_univ y)
    have h3 : slackFrom d g A hA y = slack d g a y := hmin
    refine ⟨a, ha, ?_⟩
    linarith
  · intro h
    have key : certUB f g A hA - ε ≤
        univ.inf' univ_nonempty (fun y => f y + g y - slackFrom d g A hA y) := by
      apply Finset.le_inf'
      intro y _
      obtain ⟨a, ha, hay⟩ := h y
      have h2 : slackFrom d g A hA y ≤ slack d g a y :=
        Finset.inf'_le (fun a => slack d g a y) ha
      linarith
    linarith

/-- The covering relation at level `Estar - ε`: `a` covers `y` when the slack from `a` to `y`
is at most the gap of `y` above `Estar` plus `ε`. -/
def Covers (d : X → X → ℝ) (f g : X → ℝ) (Estar ε : ℝ) (a y : X) : Prop :=
  slack d g a y ≤ f y + g y - Estar + ε

/-- Every `ε`-certificate is a cover at the level of any lower bound `Estar` on the energy. -/
theorem cover_of_certificate {d : X → X → ℝ} {f g : X → ℝ} {A : Finset X} {hA : A.Nonempty}
    {ε Estar : ℝ} (hE : ∀ y, Estar ≤ f y + g y) (h : IsCertificate d f g A hA ε) (y : X) :
    ∃ a ∈ A, Covers d f g Estar ε a y := by
  obtain ⟨a, ha, hay⟩ := (isCertificate_iff_cover d f g A hA ε).mp h y
  refine ⟨a, ha, ?_⟩
  have hUB : Estar ≤ certUB f g A hA := Finset.le_inf' _ _ fun a _ => hE a
  unfold Covers
  linarith

/-- Conversely, a cover at the level `Estar` that contains a point of energy at most `Estar` is an
`ε`-certificate.  Hence the minimal certificate size is the covering number, up to one point. -/
theorem certificate_of_cover {d : X → X → ℝ} {f g : X → ℝ} {A : Finset X} {hA : A.Nonempty}
    {ε Estar : ℝ} (hmin : ∃ a ∈ A, f a + g a ≤ Estar)
    (hcov : ∀ y, ∃ a ∈ A, Covers d f g Estar ε a y) : IsCertificate d f g A hA ε := by
  rw [isCertificate_iff_cover]
  intro y
  obtain ⟨a, ha, hay⟩ := hcov y
  obtain ⟨b, hb, hbE⟩ := hmin
  have hUB : certUB f g A hA ≤ Estar :=
    (Finset.inf'_le (fun a => f a + g a) hb).trans hbE
  refine ⟨a, ha, ?_⟩
  unfold Covers at hay
  linarith

end Certificates

/-! ### Lower bounds on the size of a cover (weak duality of the covering LP) -/

section Covering

variable [Fintype X] {R : X → X → Prop}

open Classical in
/-- **Weighted covering bound.**  If every point is covered by some element of `A` and the
weights `w ≥ 0` put total mass at most one on the set covered by any single point, then the
total weight is at most `|A|`. -/
theorem card_ge_of_weights (A : Finset X) (hcov : ∀ y, ∃ a ∈ A, R a y) (w : X → ℝ)
    (hw : ∀ y, 0 ≤ w y) (hcap : ∀ a, ∑ y ∈ univ.filter (fun y => R a y), w y ≤ 1) :
    ∑ y, w y ≤ A.card := by
  choose φ hφA hφR using hcov
  have h1 : ∑ y, w y ≤ ∑ a ∈ A, ∑ y ∈ univ.filter (fun y => R a y), w y := by
    calc ∑ y, w y = ∑ a ∈ A, ∑ y ∈ univ.filter (fun y => φ y = a), w y :=
          (Finset.sum_fiberwise_of_maps_to (fun y _ => hφA y) _).symm
      _ ≤ ∑ a ∈ A, ∑ y ∈ univ.filter (fun y => R a y), w y := by
          apply Finset.sum_le_sum
          intro a _
          apply Finset.sum_le_sum_of_subset_of_nonneg
          · intro y hy
            have hya : φ y = a := (Finset.mem_filter.mp hy).2
            exact Finset.mem_filter.mpr ⟨mem_univ y, hya ▸ hφR y⟩
          · intro y _ _
            exact hw y
  have h2 : ∑ a ∈ A, ∑ y ∈ univ.filter (fun y => R a y), w y ≤ ∑ _a ∈ A, (1 : ℝ) :=
    Finset.sum_le_sum fun a _ => hcap a
  simpa using h1.trans h2

omit [Fintype X] in
/-- **Forced points.**  A point that no other point covers belongs to every cover. -/
theorem mem_of_forced (A : Finset X) (hcov : ∀ y, ∃ a ∈ A, R a y) (y : X)
    (hy : ∀ a, a ≠ y → ¬ R a y) : y ∈ A := by
  obtain ⟨a, ha, hay⟩ := hcov y
  by_cases h : a = y
  · exact h ▸ ha
  · exact absurd hay (hy a h)

omit [Fintype X] in
/-- **Fooling sets.**  If no single point covers two distinct points of `P`, every cover has at
least `|P|` elements. -/
theorem card_ge_of_fooling (A : Finset X) (hcov : ∀ y, ∃ a ∈ A, R a y) (P : Finset X)
    (hP : ∀ a, ∀ y ∈ P, ∀ y' ∈ P, R a y → R a y' → y = y') : P.card ≤ A.card := by
  classical
  choose φ hφA hφR using hcov
  apply Finset.card_le_card_of_injOn φ (fun y _ => hφA y)
  intro y hy y' hy' h
  exact hP (φ y) y hy y' hy' (hφR y) (h ▸ hφR y')

open Classical in
/-- **Volume bound.**  If `M y` bounds the number of points covered by any point that covers `y`,
then `∑_y 1 / M y ≤ |A|` for every cover `A`: the discrete form of the integral
`∫ dx / vol(B(x, gap(x) + ε))`. -/
theorem card_ge_sum_inv (A : Finset X) (hcov : ∀ y, ∃ a ∈ A, R a y) (M : X → ℝ)
    (hM0 : ∀ y, 0 < M y)
    (hM : ∀ a y, R a y → ((univ.filter fun y' => R a y').card : ℝ) ≤ M y) :
    ∑ y, 1 / M y ≤ A.card := by
  apply card_ge_of_weights A hcov (fun y => 1 / M y) (fun y => by have := hM0 y; positivity)
  intro a
  by_cases hne : (univ.filter fun y => R a y).Nonempty
  · have hc : (0 : ℝ) < ((univ.filter fun y' => R a y').card : ℝ) := by
      exact_mod_cast Finset.card_pos.mpr hne
    calc ∑ y ∈ univ.filter (fun y => R a y), 1 / M y
        ≤ ∑ _y ∈ univ.filter (fun y => R a y), 1 / ((univ.filter fun y' => R a y').card : ℝ) := by
          apply Finset.sum_le_sum
          intro y hy
          have hR : R a y := (Finset.mem_filter.mp hy).2
          exact one_div_le_one_div_of_le hc (hM a y hR)
      _ = 1 := by
          rw [Finset.sum_const, nsmul_eq_mul]
          field_simp
  · rw [Finset.not_nonempty_iff_eq_empty.mp hne, Finset.sum_empty]
    exact zero_le_one

end Covering

/-! ### The partition-function bound -/

section Partition

variable [Fintype X] [Nonempty X]

omit [Nonempty X] in
/-- **Partition-function bound on covers.**  Let `A` cover `X` at the level `Estar - ε` and let
`B` bound the slack partition sum `∑_y exp(-t · slack a y)` of every point `a`.  Then for every
`t ≥ 0`

  `exp(-t ε) · ∑_y exp(-t (E y - Estar)) ≤ |A| · B`.

The left-hand side is the partition function of the true landscape at inverse temperature `t`
(measured from `Estar`); the bound says that the number of evaluations is at least its ratio to
the partition function of a slack ball. -/
theorem partition_bound {d : X → X → ℝ} {f g : X → ℝ} {A : Finset X} {ε Estar t B : ℝ}
    (ht : 0 ≤ t) (hcov : ∀ y, ∃ a ∈ A, Covers d f g Estar ε a y)
    (hB : ∀ a, ∑ y, Real.exp (-t * slack d g a y) ≤ B) :
    Real.exp (-t * ε) * ∑ y, Real.exp (-t * (f y + g y - Estar)) ≤ A.card * B := by
  classical
  have hterm : ∀ a y, Covers d f g Estar ε a y →
      Real.exp (-t * ε) * Real.exp (-t * (f y + g y - Estar)) ≤ Real.exp (-t * slack d g a y) := by
    intro a y hay
    rw [← Real.exp_add]
    apply Real.exp_le_exp.mpr
    unfold Covers at hay
    nlinarith [mul_le_mul_of_nonneg_left hay ht]
  choose φ hφA hφR using hcov
  calc Real.exp (-t * ε) * ∑ y, Real.exp (-t * (f y + g y - Estar))
      = ∑ y, Real.exp (-t * ε) * Real.exp (-t * (f y + g y - Estar)) := by rw [Finset.mul_sum]
    _ ≤ ∑ y, Real.exp (-t * slack d g (φ y) y) :=
        Finset.sum_le_sum fun y _ => hterm (φ y) y (hφR y)
    _ = ∑ a ∈ A, ∑ y ∈ univ.filter (fun y => φ y = a), Real.exp (-t * slack d g (φ y) y) :=
        (Finset.sum_fiberwise_of_maps_to (fun y _ => hφA y) _).symm
    _ ≤ ∑ a ∈ A, ∑ y, Real.exp (-t * slack d g a y) := by
        apply Finset.sum_le_sum
        intro a _
        calc ∑ y ∈ univ.filter (fun y => φ y = a), Real.exp (-t * slack d g (φ y) y)
            = ∑ y ∈ univ.filter (fun y => φ y = a), Real.exp (-t * slack d g a y) := by
              apply Finset.sum_congr rfl
              intro y hy
              rw [(Finset.mem_filter.mp hy).2]
          _ ≤ ∑ y, Real.exp (-t * slack d g a y) :=
              Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
                fun y _ _ => (Real.exp_pos _).le
    _ ≤ ∑ _a ∈ A, B := Finset.sum_le_sum fun a _ => hB a
    _ = A.card * B := by rw [Finset.sum_const, nsmul_eq_mul]

/-- **Partition-function bound for certificates.**  Every `ε`-certificate `A` satisfies the bound
of `partition_bound` with `Estar` any lower bound on the energy (in particular its minimum). -/
theorem partition_bound_certificate {d : X → X → ℝ} {f g : X → ℝ} {A : Finset X}
    {hA : A.Nonempty} {ε Estar t B : ℝ} (ht : 0 ≤ t) (hE : ∀ y, Estar ≤ f y + g y)
    (hcert : IsCertificate d f g A hA ε)
    (hB : ∀ a, ∑ y, Real.exp (-t * slack d g a y) ≤ B) :
    Real.exp (-t * ε) * ∑ y, Real.exp (-t * (f y + g y - Estar)) ≤ A.card * B :=
  partition_bound ht (fun y => cover_of_certificate hE hcert y) hB

end Partition

/-! ### The witness-size bound of `EnvelopeDuality.lean` as a forced-point statement -/

section Forced

variable [Fintype X] [Nonempty X]

/-- **Forced evaluations.**  If `y` is `σ`-separated in the envelope from every other point, the
residual is `κ`-Lipschitz (`κ ≤ 1`) and the gap of `y` above `Estar` is below `(1 - κ) σ - ε`,
then `y` belongs to every `ε`-certificate.  (This is `anchor_necessary`, obtained here from the
covering characterisation: such a point can only be covered by itself.) -/
theorem anchor_necessary' {d : X → X → ℝ} {f g : X → ℝ} {κ : ℝ} (hκ : κ ≤ 1)
    (hgκ : ∀ x y, g x - g y ≤ κ * d x y) {A : Finset X} {hA : A.Nonempty} {ε Estar σ : ℝ}
    (hE : ∀ y, Estar ≤ f y + g y) (hcert : IsCertificate d f g A hA ε) (y : X)
    (hsep : ∀ a, a ≠ y → σ ≤ d a y) (hy : f y + g y - Estar < (1 - κ) * σ - ε) : y ∈ A := by
  apply mem_of_forced (R := Covers d f g Estar ε) A (fun y => cover_of_certificate hE hcert y) y
  intro a hay hcov
  have h1 := slack_ge_of_lipschitz hgκ a y
  have h2 : (1 - κ) * σ ≤ (1 - κ) * d a y :=
    mul_le_mul_of_nonneg_left (hsep a hay) (by linarith)
  unfold Covers at hcov
  linarith

end Forced

end MetricChain
