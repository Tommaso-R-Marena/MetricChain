import proofs.Frontiers.CubeHintPair

/-!
# The level recursion, exactly, and the passage to a bounded accuracy

Theory report §11.19 (workstream K; `docs/workstreams/K_REPORT.md`).  Three groups of statements.

**1. The exact recursion.**  `HintRecursion.lean` and `CubeHintPair.lean` prove convergence for
*any* sequence of functions that satisfies the step inequality `StepLE`.  Here the sequence of
the theory report is *defined*,

  `T₁ = θ_na`,   `T_{k+1}(g) = min(T_k(g), R[T_k](g))`,
  `R[T](g) = inf_{0<φ<1, 0<β<g} sup_{γ≥β} [ min(γ, φ θ_na((g−β)/φ)) + (1−φ) T(γ/(1−φ)) ]`

(`exactRec`; the infimum of the suprema is written as the infimum of all upper bounds, a set
that is nonempty and bounded below), and shown to satisfy those hypotheses
(`stepLE_exact`, `Rstep_anti`, `exactRec_props`).  Hence `exactRec_reaches_hint`: for the
functions of the cube some level is within `η` of the hinted exponent — with no hypothesis
about the sequence.  In the other direction the hinted exponent is a lower barrier
(`exactRec_ge_hint`: the "necessary condition" that no level may undercut the lower bound),
so the exact recursion **converges** to it: `exactRec_tendsto_hint`.  This is Theorem 11.53 of
the theory report for the cube with nothing assumed.  (Workstream K, except the last two
statements and their two lemmas.)

**2. The recursion at accuracy zero.**  The exponents `τ k` at a *bounded* accuracy obey
`τ (k+1) ≤ inf_φ max((1−φ) τ k, sup_{0<γ≤φa} [γ + (1−φ) T k (γ/(1−φ))])`; if the extensive
exponents `T k` converge pointwise to a function `≤ h`, some `τ k` is below `h + ε`
(`bounded_iterates_lt`; for an abstract `HintPair`: `levels_reach_hint_at_zero`; for the cube:
`cube_levels_reach_hint_at_zero`).  `two_rung_bound` is the iteration actually used in the
proof of Theorem 11.58 of the theory report (Theorem K3 of the workstream).

**3. The deterministic algebra of Algorithm 2L⁺** (Theorem 11.56 / K1): the sum form of the
lower end of the bracket (`certified_lower_sum_le_mean`), the populated part of the upper end
against it (`populated_part_le`), the count of sampled points close to a level
(`close_points_bound'`: the two factors `e^b` cancel) and the width (`width_le`).

**Not formalised:** the algorithm, its probabilistic events, the cost sum, the tail lemmas,
Harper's theorem, the assembly of the families over the levels, and the identification of
`τ k` with exponents of algorithms.  Those are paper proofs (theory report §11.19).
-/

namespace MetricChain
namespace BoundedAccuracy

open MetricChain.HintRecursion Set

/-! ### The exact level recursion -/

/-- The upper bounds of the two-level bracket at accuracy `g` over all admissible `(φ, β)`. -/
def admissible (θna T : ℝ → ℝ) (g : ℝ) : Set ℝ :=
  {B | ∃ φ β : ℝ, 0 < β ∧ β < g ∧ 0 < φ ∧ φ < 1 ∧
    ∀ γ, β ≤ γ → min γ (φ * θna ((g - β) / φ)) + (1 - φ) * T (γ / (1 - φ)) ≤ B}

/-- `R[T](g)`. -/
noncomputable def Rstep (θna T : ℝ → ℝ) (g : ℝ) : ℝ := sInf (admissible θna T g)

/-- The exact recursion (index shifted by one: `exactRec θna k` is `T_{k+1}` of the report). -/
noncomputable def exactRec (θna : ℝ → ℝ) : ℕ → ℝ → ℝ
  | 0 => θna
  | k + 1 => fun g => min (exactRec θna k g) (Rstep θna (exactRec θna k) g)

theorem admissible_nonneg {θna T : ℝ → ℝ} (hθ : ∀ x, 0 < x → 0 ≤ θna x)
    (hT : ∀ x, 0 < x → 0 ≤ T x) {g B : ℝ} (hB : B ∈ admissible θna T g) : 0 ≤ B := by
  obtain ⟨φ, β, hβ, hβg, hφ0, hφ1, h⟩ := hB
  have h1 := h β le_rfl
  have h2 : 0 ≤ min β (φ * θna ((g - β) / φ)) :=
    le_min hβ.le (mul_nonneg hφ0.le (hθ _ (div_pos (by linarith) hφ0)))
  have h3 : 0 ≤ (1 - φ) * T (β / (1 - φ)) :=
    mul_nonneg (by linarith) (hT _ (div_pos hβ (by linarith)))
  linarith

/-- The step inequality holds for `min(T, R[T])` by definition of the infimum. -/
theorem stepLE_exact {θna T : ℝ → ℝ} (hθ : ∀ x, 0 < x → 0 ≤ θna x)
    (hT : ∀ x, 0 < x → 0 ≤ T x) :
    StepLE θna T (fun g => min (T g) (Rstep θna T g)) := by
  intro g φ β B hβ hβg hφ0 hφ1 hB
  have hmem : B ∈ admissible θna T g := ⟨φ, β, hβ, hβg, hφ0, hφ1, hB⟩
  have hbdd : BddBelow (admissible θna T g) := ⟨0, fun x hx => admissible_nonneg hθ hT hx⟩
  exact (min_le_right _ _).trans (csInf_le hbdd hmem)

/-- `R[T]` is nonincreasing in the accuracy: parameters admissible for `x` are admissible for
`y ≥ x`, with a smaller bracket. -/
theorem Rstep_anti {θna T : ℝ → ℝ} {C : ℝ} (hθ : ∀ x, 0 < x → 0 ≤ θna x)
    (hT : ∀ x, 0 < x → 0 ≤ T x) (hθanti : ∀ x y, 0 < x → x ≤ y → θna y ≤ θna x)
    (hTC : ∀ x, 0 < x → T x ≤ C) {x y : ℝ} (hx : 0 < x) (hxy : x ≤ y) :
    Rstep θna T y ≤ Rstep θna T x := by
  have hbdd : BddBelow (admissible θna T y) := ⟨0, fun b hb => admissible_nonneg hθ hT hb⟩
  have hne : (admissible θna T x).Nonempty := by
    refine ⟨(1 / 2) * θna ((x - x / 2) / (1 / 2)) + (1 - 1 / 2) * C, 1 / 2, x / 2, by positivity,
      by linarith, by norm_num, by norm_num, ?_⟩
    intro γ hγ
    have hγ0 : 0 < γ := lt_of_lt_of_le (by positivity) hγ
    have h1 : min γ ((1 / 2) * θna ((x - x / 2) / (1 / 2))) ≤ (1 / 2) * θna ((x - x / 2) / (1 / 2)) :=
      min_le_right _ _
    have h2 : T (γ / (1 - 1 / 2)) ≤ C := hTC _ (div_pos hγ0 (by norm_num))
    have h3 : (1 - 1 / 2 : ℝ) * T (γ / (1 - 1 / 2)) ≤ (1 - 1 / 2) * C :=
      mul_le_mul_of_nonneg_left h2 (by norm_num)
    linarith
  have hsub : admissible θna T x ⊆ admissible θna T y := by
    rintro B ⟨φ, β, hβ, hβx, hφ0, hφ1, h⟩
    refine ⟨φ, β, hβ, lt_of_lt_of_le hβx hxy, hφ0, hφ1, fun γ hγ => ?_⟩
    have h1 : θna ((y - β) / φ) ≤ θna ((x - β) / φ) :=
      hθanti _ _ (div_pos (by linarith) hφ0) (div_le_div_of_nonneg_right (by linarith) hφ0.le)
    have h2 : min γ (φ * θna ((y - β) / φ)) ≤ min γ (φ * θna ((x - β) / φ)) :=
      min_le_min le_rfl (mul_le_mul_of_nonneg_left h1 hφ0.le)
    have h3 := h γ hγ
    linarith
  exact csInf_le_csInf hbdd hne hsub

/-- Nonnegativity, boundedness and monotonicity are inherited along the exact recursion. -/
theorem exactRec_props {θna : ℝ → ℝ} {C : ℝ} (hθ : ∀ x, 0 < x → 0 ≤ θna x)
    (hθanti : ∀ x y, 0 < x → x ≤ y → θna y ≤ θna x) (hθC : ∀ x, 0 < x → θna x ≤ C) (k : ℕ) :
    (∀ x, 0 < x → 0 ≤ exactRec θna k x) ∧ (∀ x, 0 < x → exactRec θna k x ≤ C) ∧
      (∀ x y, 0 < x → x ≤ y → exactRec θna k y ≤ exactRec θna k x) := by
  induction k with
  | zero => exact ⟨hθ, hθC, hθanti⟩
  | succ k ih =>
    obtain ⟨h0, hC, hanti⟩ := ih
    refine ⟨fun x hx => ?_, fun x hx => ?_, fun x y hx hxy => ?_⟩
    · show 0 ≤ min (exactRec θna k x) (Rstep θna (exactRec θna k) x)
      exact le_min (h0 x hx) (Real.sInf_nonneg (fun b hb => admissible_nonneg hθ h0 hb))
    · show min (exactRec θna k x) (Rstep θna (exactRec θna k) x) ≤ C
      exact (min_le_left _ _).trans (hC x hx)
    · show min (exactRec θna k y) (Rstep θna (exactRec θna k) y)
          ≤ min (exactRec θna k x) (Rstep θna (exactRec θna k) x)
      exact min_le_min (hanti x y hx hxy) (Rstep_anti hθ h0 hθanti hC hx hxy)

/-- **Statement (R) for the exact recursion of the cube.**  For every accuracy rate
`g ∈ (0, ε*)` and every `η > 0` some level of the exact recursion
`T₁ = θ_na`, `T_{k+1} = min(T_k, R[T_k])` is within `η` of the hinted exponent. -/
theorem exactRec_reaches_hint {u : ℝ} (hu : 0 < u) {g : ℝ} (hg : 0 < g) (hgE : g < cubeEstar u)
    {η : ℝ} (hη : 0 < η) : ∃ k, exactRec (cubeNa u) k g < cubeHint u g + η := by
  have hθ : ∀ x, 0 < x → 0 ≤ cubeNa u x := fun x _ => cubeNa_nonneg u x
  have hθanti : ∀ x y, 0 < x → x ≤ y → cubeNa u y ≤ cubeNa u x := fun x y hx hxy =>
    cubeNa_antitoneOn hu (mem_Ici.mpr hx.le) (mem_Ici.mpr (hx.le.trans hxy)) hxy
  have hθC : ∀ x, 0 < x → cubeNa u x ≤ cubeA u := fun x hx => cubeNa_le_cubeA hu hx.le
  have P := fun k => exactRec_props hθ hθanti hθC k
  refine cube_iterates_lt_hint_add hu (exactRec (cubeNa u)) (fun k => ?_) (fun k x _ => ?_)
    (fun k x y hx hxy => (P k).2.2 x y hx hxy) ⟨cubeA u, fun x hx => (P 0).2.1 x hx⟩
    (fun k x hx => (P k).1 x hx) hg hgE hη
  · exact stepLE_exact hθ (P k).1
  · exact min_le_left _ _

/-- **The exact recursion reaches the hinted exponent for any pair with the abstract
properties.**  If `θna` is nonnegative and nonincreasing and `(θna, θh)` is a `HintPair`, then the
exact level recursion built on `θna` comes within any `η` of `θh` at every accuracy rate
`g ∈ (0, E)`.  (`exactRec_reaches_hint` is the case of the cube; theory report §11.20 uses this
form for the pair of the biased cube, whose `HintPair` property is a paper proof.) -/
theorem exactRec_reaches_hint_of_pair {θna θh : ℝ → ℝ} {a h E : ℝ} (hp : HintPair θna θh a h E)
    (hθ : ∀ x, 0 < x → 0 ≤ θna x) (hθanti : ∀ x y, 0 < x → x ≤ y → θna y ≤ θna x)
    {g : ℝ} (hg : 0 < g) (hgE : g < E) {η : ℝ} (hη : 0 < η) :
    ∃ k, exactRec θna k g < θh g + η := by
  have P := fun k => exactRec_props hθ hθanti hp.na_le k
  refine iterates_lt_hint_add hp (exactRec θna) (fun k => ?_) (fun k x _ => ?_)
    (fun k x y hx hxy => (P k).2.2 x y hx hxy) ⟨a, fun x hx => (P 0).2.1 x hx⟩
    (fun k x hx => (P k).1 x hx) hg hgE hη
  · exact stepLE_exact hθ (P k).1
  · exact min_le_left _ _

/-- The admissible set is nonempty as soon as `T` is bounded above. -/
theorem admissible_nonempty {θna T : ℝ → ℝ} {C : ℝ} (hTC : ∀ x, 0 < x → T x ≤ C) {x : ℝ}
    (hx : 0 < x) : (admissible θna T x).Nonempty := by
  refine ⟨(1 / 2) * θna ((x - x / 2) / (1 / 2)) + (1 - 1 / 2) * C, 1 / 2, x / 2, by positivity,
    by linarith, by norm_num, by norm_num, ?_⟩
  intro γ hγ
  have hγ0 : 0 < γ := lt_of_lt_of_le (by positivity) hγ
  have h1 : min γ ((1 / 2) * θna ((x - x / 2) / (1 / 2))) ≤ (1 / 2) * θna ((x - x / 2) / (1 / 2)) :=
    min_le_right _ _
  have h2 : T (γ / (1 - 1 / 2)) ≤ C := hTC _ (div_pos hγ0 (by norm_num))
  have h3 : (1 - 1 / 2 : ℝ) * T (γ / (1 - 1 / 2)) ≤ (1 - 1 / 2) * C :=
    mul_le_mul_of_nonneg_left h2 (by norm_num)
  linarith

/-- The admissible set shrinks when the inner exponent function grows: `R` is monotone. -/
theorem admissible_subset_of_le {θna T T' : ℝ → ℝ} (hTT' : ∀ x, 0 < x → T x ≤ T' x) (g : ℝ) :
    admissible θna T' g ⊆ admissible θna T g := by
  rintro B ⟨φ, β, hβ, hβg, hφ0, hφ1, h⟩
  refine ⟨φ, β, hβ, hβg, hφ0, hφ1, fun γ hγ => ?_⟩
  have hγ0 : 0 < γ := lt_of_lt_of_le hβ hγ
  have h1 : (1 - φ) * T (γ / (1 - φ)) ≤ (1 - φ) * T' (γ / (1 - φ)) :=
    mul_le_mul_of_nonneg_left (hTT' _ (div_pos hγ0 (by linarith))) (by linarith)
  have h2 := h γ hγ
  linarith

/-- One step of the recursion from any bounded function above the hinted exponent of the cube
stays above it: `θ_hint ≤ R[T]` whenever `θ_hint ≤ T`. -/
theorem hintClip_le_Rstep {u : ℝ} (hu : 0 < u) {T : ℝ → ℝ} {C : ℝ}
    (hT : ∀ x, 0 < x → cubeHintClip u x ≤ T x) (hTC : ∀ x, 0 < x → T x ≤ C) {g : ℝ}
    (hg : 0 < g) : cubeHintClip u g ≤ Rstep (cubeNa u) T g := by
  apply le_csInf (admissible_nonempty hTC hg)
  intro B hB
  obtain ⟨φ, β, hβ, hβg, hφ0, hφ1, h⟩ := admissible_subset_of_le hT g hB
  exact cube_hint_superSolution hu g φ β B hβ hβg hφ0 hφ1 h

/-- **No level of the exact recursion undercuts the hinted exponent** — the necessary
condition that every accounting of the two-level algorithm has to pass (`DEAD_ENDS.md`, D45),
here for the recursion as defined. -/
theorem exactRec_ge_hint {u : ℝ} (hu : 0 < u) (k : ℕ) :
    ∀ g, 0 < g → cubeHintClip u g ≤ exactRec (cubeNa u) k g := by
  have hθ : ∀ x, 0 < x → 0 ≤ cubeNa u x := fun x _ => cubeNa_nonneg u x
  have hθanti : ∀ x y, 0 < x → x ≤ y → cubeNa u y ≤ cubeNa u x := fun x y hx hxy =>
    cubeNa_antitoneOn hu (mem_Ici.mpr hx.le) (mem_Ici.mpr (hx.le.trans hxy)) hxy
  have hθC : ∀ x, 0 < x → cubeNa u x ≤ cubeA u := fun x hx => cubeNa_le_cubeA hu hx.le
  induction k with
  | zero =>
    intro g hg
    show cubeHintClip u g ≤ cubeNa u g
    rcases lt_or_ge g (cubeEstar u) with h | h
    · rw [cubeHintClip_eq h.le]
      exact (cubeHint_lt_cubeNa hu hg.le h).le
    · rw [cubeHintClip_of_cubeEstar_le hu h]
      exact cubeNa_nonneg u g
  | succ k ih =>
    intro g hg
    show cubeHintClip u g
      ≤ min (exactRec (cubeNa u) k g) (Rstep (cubeNa u) (exactRec (cubeNa u) k) g)
    exact le_min (ih g hg) (hintClip_le_Rstep hu ih (exactRec_props hθ hθanti hθC k).2.1 hg)

/-- **Theorem 11.53 for the cube, with nothing assumed about the sequence.**  The exact level
recursion `T₁ = θ_na`, `T_{k+1} = min(T_k, R[T_k])` converges, at every accuracy rate
`g ∈ (0, ε*)`, to the hinted exponent `θ_hint(g) = KL((Λ₁+g)/u ‖ 1/2)`. -/
theorem exactRec_tendsto_hint {u : ℝ} (hu : 0 < u) {g : ℝ} (hg : 0 < g) (hgE : g < cubeEstar u) :
    Filter.Tendsto (fun k => exactRec (cubeNa u) k g) Filter.atTop (nhds (cubeHint u g)) := by
  have hanti : Antitone (fun k => exactRec (cubeNa u) k g) :=
    antitone_nat_of_succ_le fun k => by
      show min (exactRec (cubeNa u) k g) (Rstep (cubeNa u) (exactRec (cubeNa u) k) g)
        ≤ exactRec (cubeNa u) k g
      exact min_le_left _ _
  have hlow : ∀ k, cubeHint u g ≤ exactRec (cubeNa u) k g := fun k => by
    have h := exactRec_ge_hint hu k g hg
    rwa [cubeHintClip_eq hgE.le] at h
  rw [Metric.tendsto_atTop]
  intro ε hε
  obtain ⟨k, hk⟩ := exactRec_reaches_hint hu hg hgE hε
  refine ⟨k, fun m hm => ?_⟩
  have h1 : exactRec (cubeNa u) m g ≤ exactRec (cubeNa u) k g := hanti hm
  have h2 := hlow m
  rw [Real.dist_eq, abs_lt]
  constructor <;> linarith

/-! ### The recursion at accuracy zero -/

/-- **The bounded-accuracy exponents converge to `h`.**  `T k x` (`x > 0`) are exponent
functions at extensive accuracies, nonincreasing in `x` and in `k`, bounded by `τ k`, and
converging pointwise on `(0, E)` to within any `ε` of a function `θh ≤ h`; `τ k` obeys the
one-level bound at accuracy zero for every outer fraction `φ`.  Then some `τ k` is below
`h + ε`. -/
theorem bounded_iterates_lt {h a E : ℝ} (θh : ℝ → ℝ) (hh : 0 < h) (ha : 0 < a) (hE : 0 < E)
    (hθle : ∀ x, 0 < x → x < E → θh x ≤ h)
    (T : ℕ → ℝ → ℝ) (τ : ℕ → ℝ)
    (hconv : ∀ x, 0 < x → x < E → ∀ ε, 0 < ε → ∃ k, T k x < θh x + ε)
    (hmono : ∀ k x, 0 < x → T (k + 1) x ≤ T k x)
    (hanti : ∀ k x y, 0 < x → x ≤ y → T k y ≤ T k x)
    (hTτ : ∀ k x, 0 < x → T k x ≤ τ k)
    (hstep : ∀ k φ B, 0 < φ → φ < 1 → (1 - φ) * τ k ≤ B →
      (∀ γ, 0 < γ → γ ≤ φ * a → γ + (1 - φ) * T k (γ / (1 - φ)) ≤ B) → τ (k + 1) ≤ B)
    {ε : ℝ} (hε : 0 < ε) : ∃ k, τ k < h + ε := by
  by_contra hcon0
  have hcon : ∀ k, h + ε ≤ τ k := fun k => not_lt.mp fun hk => hcon0 ⟨k, hk⟩
  -- the outer fraction and the cut
  obtain ⟨φ, hφ0, hφhalf, hφa⟩ : ∃ φ : ℝ, 0 < φ ∧ φ ≤ 1 / 2 ∧ φ * a ≤ ε / 4 := by
    refine ⟨min (1 / 2) (ε / (4 * a)), lt_min (by norm_num) (by positivity), min_le_left _ _, ?_⟩
    have h1 : min (1 / 2) (ε / (4 * a)) ≤ ε / (4 * a) := min_le_right _ _
    have h2 := mul_le_mul_of_nonneg_right h1 ha.le
    have h3 : ε / (4 * a) * a = ε / 4 := by field_simp
    linarith
  have hφ1 : φ < 1 := by linarith
  have h1φ : 0 < 1 - φ := by linarith
  obtain ⟨x0, hx0, hx0E, hx0φ⟩ : ∃ x0 : ℝ, 0 < x0 ∧ x0 < E ∧ x0 ≤ φ * h / 2 := by
    refine ⟨min (E / 2) (φ * h / 2), lt_min (by linarith) (by positivity), ?_, min_le_right _ _⟩
    exact lt_of_le_of_lt (min_le_left _ _) (by linarith)
  obtain ⟨k0, hk0⟩ := hconv x0 hx0 hx0E (ε / 4) (by linarith)
  have hθ0 := hθle x0 hx0 hx0E
  have hmono' : ∀ m : ℕ, T (k0 + m) x0 ≤ T k0 x0 := by
    intro m
    induction m with
    | zero => exact le_rfl
    | succ m ih => exact (hmono (k0 + m) x0 hx0).trans ih
  -- one step contracts by the factor `1 - φ/2`
  have hcontr : ∀ m : ℕ, τ (k0 + m + 1) ≤ (1 - φ / 2) * τ (k0 + m) := by
    intro m
    have hτk := hcon (k0 + m)
    have hτk1 := hcon (k0 + m + 1)
    have hB : τ (k0 + m + 1) ≤ max ((1 - φ) * (τ (k0 + m) + x0)) (h + ε / 2) := by
      apply hstep (k0 + m) φ _ hφ0 hφ1
      · apply le_max_of_le_left
        nlinarith
      · intro γ hγ0 hγ
        by_cases hy : γ / (1 - φ) < x0
        · apply le_max_of_le_left
          have hT := hTτ (k0 + m) (γ / (1 - φ)) (div_pos hγ0 h1φ)
          have hγ' : γ < x0 * (1 - φ) := (div_lt_iff₀ h1φ).mp hy
          have hT' := mul_le_mul_of_nonneg_left hT h1φ.le
          nlinarith
        · have hy : x0 ≤ γ / (1 - φ) := not_lt.mp hy
          apply le_max_of_le_right
          have hT := hanti (k0 + m) x0 (γ / (1 - φ)) hx0 hy
          have hT2 := hmono' m
          have hT3 : T (k0 + m) (γ / (1 - φ)) ≤ h + ε / 4 := by linarith
          have hT4 := mul_le_mul_of_nonneg_left hT3 h1φ.le
          nlinarith
    rcases le_max_iff.mp hB with h1 | h1
    · have h2 : (1 - φ) * x0 ≤ φ / 2 * τ (k0 + m) := by
        have h3 : x0 ≤ φ / 2 * τ (k0 + m) := by nlinarith
        nlinarith
      nlinarith
    · linarith
  have hpow : ∀ m : ℕ, τ (k0 + m) ≤ (1 - φ / 2) ^ m * τ k0 := by
    intro m
    induction m with
    | zero => simp
    | succ m ih =>
      have h1 := hcontr m
      have h2 : (0 : ℝ) ≤ 1 - φ / 2 := by linarith
      calc τ (k0 + (m + 1)) = τ (k0 + m + 1) := rfl
        _ ≤ (1 - φ / 2) * τ (k0 + m) := h1
        _ ≤ (1 - φ / 2) * ((1 - φ / 2) ^ m * τ k0) := mul_le_mul_of_nonneg_left ih h2
        _ = (1 - φ / 2) ^ (m + 1) * τ k0 := by ring
  have hτ0 : 0 < τ k0 := by have := hcon k0; linarith
  obtain ⟨m, hm⟩ := exists_pow_lt_of_lt_one (div_pos hh hτ0) (show 1 - φ / 2 < 1 by linarith)
  have h1 := hpow m
  have h2 := hcon (k0 + m)
  have h3 : (1 - φ / 2) ^ m * τ k0 < h := by
    have := (lt_div_iff₀ hτ0).mp hm
    linarith
  linarith

/-- **The iteration in the proof of Theorem K3** (two-rung ladder).  If the bounded-accuracy
exponents `t m` of the families `G_m` satisfy
`t (m+1) ≤ max(φ a + (1-φ) Tξ, (1-φ)(ξ + t m))`, with `Tξ ≤ h + η` (the extensive exponent at the
rate `ξ`), `φ a ≤ η`, `ξ ≤ φ η` and `t 0 ≤ a`, then `t m ≤ η + max(h + η, (1-φ)^m a)` for all `m`. -/
theorem two_rung_bound {h a η φ ξ Tξ : ℝ} (t : ℕ → ℝ) (hφ0 : 0 ≤ φ) (hφ1 : φ ≤ 1) (hη : 0 ≤ η)
    (hh : 0 ≤ h) (hφa : φ * a ≤ η) (hξ : ξ ≤ φ * η) (hT : Tξ ≤ h + η) (ht0 : t 0 ≤ a)
    (hstep : ∀ m, t (m + 1) ≤ max (φ * a + (1 - φ) * Tξ) ((1 - φ) * (ξ + t m))) :
    ∀ m, t m ≤ η + max (h + η) ((1 - φ) ^ m * a) := by
  have h1φ : 0 ≤ 1 - φ := by linarith
  intro m
  induction m with
  | zero =>
    have : a ≤ max (h + η) ((1 - φ) ^ 0 * a) := by
      rw [pow_zero, one_mul]; exact le_max_right _ _
    linarith
  | succ m ih =>
    refine (hstep m).trans (max_le ?_ ?_)
    · have h2 : (1 - φ) * Tξ ≤ (1 - φ) * (h + η) := mul_le_mul_of_nonneg_left hT h1φ
      have h3 : (1 - φ) * (h + η) ≤ h + η := by nlinarith
      have h4 : h + η ≤ max (h + η) ((1 - φ) ^ (m + 1) * a) := le_max_left _ _
      linarith
    · have h2 : (1 - φ) * (ξ + t m) ≤ (1 - φ) * (ξ + (η + max (h + η) ((1 - φ) ^ m * a))) :=
        mul_le_mul_of_nonneg_left (by linarith) h1φ
      have h3 : (1 - φ) * max (h + η) ((1 - φ) ^ m * a) ≤ max (h + η) ((1 - φ) ^ (m + 1) * a) := by
        rcases le_total (h + η) ((1 - φ) ^ m * a) with hc | hc
        · rw [max_eq_right hc]
          have : (1 - φ) * ((1 - φ) ^ m * a) = (1 - φ) ^ (m + 1) * a := by ring
          rw [this]; exact le_max_right _ _
        · rw [max_eq_left hc]
          have : (1 - φ) * (h + η) ≤ h + η := by nlinarith
          exact this.trans (le_max_left _ _)
      have h4 : (1 - φ) * ξ ≤ φ * η := by
        rcases le_total 0 ξ with hξ0 | hξ0
        · have : (1 - φ) * ξ ≤ ξ := by nlinarith
          linarith
        · have h5 : (1 - φ) * ξ ≤ 0 := mul_nonpos_of_nonneg_of_nonpos h1φ hξ0
          have h6 : 0 ≤ φ * η := mul_nonneg hφ0 hη
          linarith
      have e : (1 - φ) * (ξ + (η + max (h + η) ((1 - φ) ^ m * a)))
          = (1 - φ) * ξ + (η - φ * η) + (1 - φ) * max (h + η) ((1 - φ) ^ m * a) := by ring
      rw [e] at h2
      linarith

/-- **The level recursion on `[0, ∞)` reaches `h` at accuracy zero.**  `θna`, `θh` an abstract
pair with the properties of the cube (`HintPair`), and `θh ≤ h` on `(0, E)`.  `T k` satisfy the
level recursion at extensive accuracies (`StepLE`, Theorem 11.52), are nonincreasing in the
level and in the accuracy, nonnegative, `T 0 ≤ a`; `τ k ≥ T k x` obey the recursion at accuracy
zero (Theorem K2 of the workstream report).  Then for every `ε > 0` some `τ k < h + ε`. -/
theorem levels_reach_hint_at_zero {θna θh : ℝ → ℝ} {a h E : ℝ} (hp : HintPair θna θh a h E)
    (hE : 0 < E) (hθle : ∀ x, 0 < x → x < E → θh x ≤ h)
    (T : ℕ → ℝ → ℝ) (τ : ℕ → ℝ)
    (hstep : ∀ k, StepLE θna (T k) (T (k + 1)))
    (hmono : ∀ k x, 0 < x → T (k + 1) x ≤ T k x)
    (hanti : ∀ k x y, 0 < x → x ≤ y → T k y ≤ T k x)
    (hbdd : ∀ x, 0 < x → T 0 x ≤ a) (hnn : ∀ k x, 0 < x → 0 ≤ T k x)
    (hTτ : ∀ k x, 0 < x → T k x ≤ τ k)
    (hstep0 : ∀ k φ B, 0 < φ → φ < 1 → (1 - φ) * τ k ≤ B →
      (∀ γ, 0 < γ → γ ≤ φ * a → γ + (1 - φ) * T k (γ / (1 - φ)) ≤ B) → τ (k + 1) ≤ B)
    {ε : ℝ} (hε : 0 < ε) : ∃ k, τ k < h + ε := by
  apply bounded_iterates_lt θh hp.h_pos hp.a_pos hE hθle T τ _ hmono hanti hTτ hstep0 hε
  intro x hx hxE η hη
  exact iterates_lt_hint_add hp T hstep hmono hanti ⟨a, hbdd⟩ hnn hx hxE hη

/-- On the cube the hinted exponent is at most its value at accuracy zero: `θ_hint(e) ≤ h` for
`0 < e < ε*` (`KL(· ‖ 1/2)` decreases on `[0, 1/2]` and the radius `(Λ₁+e)/u` increases with `e`). -/
theorem cubeHint_le_cubeH {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : 0 < x) (hxE : x < cubeEstar u) :
    cubeHint u x ≤ cubeH u := by
  have h0 := cubeHintRadius_mem hu (e := 0) le_rfl (cubeEstar_pos hu).le
  have hx' := cubeHintRadius_mem hu hx.le hxE.le
  have hp := cubeP_pos u
  rw [add_zero] at h0
  have hle : cubeLam u / u ≤ (cubeLam u + x) / u :=
    div_le_div_of_nonneg_right (by linarith) hu.le
  have hanti := klBin_half_strictAntiOn.antitoneOn
  have h1 : cubeLam u / u ∈ Icc (0 : ℝ) (1 / 2) := ⟨by linarith [h0.1], h0.2⟩
  have h2 : (cubeLam u + x) / u ∈ Icc (0 : ℝ) (1 / 2) := ⟨by linarith [hx'.1], hx'.2⟩
  have := hanti h1 h2 hle
  unfold cubeHint cubeH
  exact this

/-- **The bounded-accuracy exponents of the cube reach `h`.**  `T k` satisfy the level recursion
of the cube at extensive accuracies (`StepLE (cubeNa u)`), are nonincreasing in the level and in
the accuracy, nonnegative, and `T 0` is bounded; `τ k ≥ T k x` obey the recursion at accuracy
zero with `a = cubeA u = KL(p_u ‖ 1/2)`.  Then for every `ε > 0` some `τ k < cubeH u + ε`,
`cubeH u = KL(Λ₁/u ‖ 1/2)`. -/
theorem cube_levels_reach_hint_at_zero {u : ℝ} (hu : 0 < u) (T : ℕ → ℝ → ℝ) (τ : ℕ → ℝ)
    (hstep : ∀ k, StepLE (cubeNa u) (T k) (T (k + 1)))
    (hmono : ∀ k x, 0 < x → T (k + 1) x ≤ T k x)
    (hanti : ∀ k x y, 0 < x → x ≤ y → T k y ≤ T k x)
    (hbdd : ∃ C, ∀ x, 0 < x → T 0 x ≤ C) (hnn : ∀ k x, 0 < x → 0 ≤ T k x)
    (hTτ : ∀ k x, 0 < x → T k x ≤ τ k)
    (hstep0 : ∀ k φ B, 0 < φ → φ < 1 → (1 - φ) * τ k ≤ B →
      (∀ γ, 0 < γ → γ ≤ φ * cubeA u → γ + (1 - φ) * T k (γ / (1 - φ)) ≤ B) → τ (k + 1) ≤ B)
    {ε : ℝ} (hε : 0 < ε) : ∃ k, τ k < cubeH u + ε := by
  have hp := cubePair hu
  apply bounded_iterates_lt (cubeHint u) hp.h_pos hp.a_pos (cubeEstar_pos hu)
    (fun x hx hxE => cubeHint_le_cubeH hu hx hxE) T τ _ hmono hanti hTτ hstep0 hε
  intro x hx hxE η hη
  exact cube_iterates_lt_hint_add hu T hstep hmono hanti hbdd hnn hx hxE hη

/-- The hypotheses of `cube_levels_reach_hint_at_zero` are consistent: the zero functions
satisfy them. -/
theorem cube_levels_reach_hint_at_zero_consistent {u : ℝ} (hu : 0 < u) {ε : ℝ} (hε : 0 < ε) :
    ∃ k : ℕ, (fun _ : ℕ => (0 : ℝ)) k < cubeH u + ε :=
  cube_levels_reach_hint_at_zero hu (fun _ _ => 0) (fun _ => 0)
    (fun _ => cube_zero_superSolution u) (fun _ _ _ => le_rfl) (fun _ _ _ _ _ => le_rfl)
    ⟨0, fun _ _ => le_rfl⟩ (fun _ _ _ => le_rfl) (fun _ _ _ => le_rfl)
    (fun _ φ B _ hφ1 hB _ => by simpa using hB) hε

/-! ### The sum form of the lower end; width and count -/

open Finset LayerCake

variable {α : Type*} [Fintype α]

/-- Lower Riemann sum at one point, for the first `m` levels: with nondecreasing levels
`0 ≤ t 0 ≤ t 1 ≤ …` and `w ≥ 0`,
`Σ_{i<m} (t_{i+1} − t_i)·[w > t_{i+1}] ≤ max(0, min(w, t_m) − t_0)`. -/
theorem pointwise_lower (t : ℕ → ℝ) (ht : Monotone t) (w : ℝ) (m : ℕ) :
    ∑ i ∈ range m, (t (i + 1) - t i) * (if t (i + 1) < w then (1 : ℝ) else 0)
      ≤ max 0 (min w (t m) - t 0) := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ]
    by_cases hlt : t (m + 1) < w
    · have hall : ∀ i ∈ range m,
          (t (i + 1) - t i) * (if t (i + 1) < w then (1 : ℝ) else 0) = t (i + 1) - t i := by
        intro i hi
        have hle : t (i + 1) ≤ t (m + 1) := ht (by have := Finset.mem_range.mp hi; omega)
        rw [if_pos (lt_of_le_of_lt hle hlt), mul_one]
      rw [Finset.sum_congr rfl hall, Finset.sum_range_sub, if_pos hlt, mul_one, min_eq_right hlt.le]
      exact le_max_of_le_right (by linarith)
    · rw [if_neg hlt, mul_zero, add_zero]
      refine ih.trans (max_le_max le_rfl ?_)
      have hle : t m ≤ t (m + 1) := ht (Nat.le_succ m)
      exact sub_le_sub_right (min_le_min le_rfl hle) _

/-- The same for an arbitrary finite set `P` of levels (the populated ones). -/
theorem pointwise_lower_subset (t : ℕ → ℝ) (ht : Monotone t) (ht0 : 0 ≤ t 0) {w : ℝ} (hw : 0 ≤ w)
    (P : Finset ℕ) :
    ∑ i ∈ P, (t (i + 1) - t i) * (if t (i + 1) < w then (1 : ℝ) else 0) ≤ w := by
  obtain ⟨m, hm⟩ : ∃ m, P ⊆ range m :=
    ⟨P.sup id + 1, fun i hi => Finset.mem_range.mpr (Nat.lt_succ_of_le (Finset.le_sup (f := id) hi))⟩
  have hnn : ∀ i ∈ range m, i ∉ P →
      0 ≤ (t (i + 1) - t i) * (if t (i + 1) < w then (1 : ℝ) else 0) := by
    intro i _ _
    have hle : t i ≤ t (i + 1) := ht (Nat.le_succ i)
    split_ifs
    · linarith
    · simp
  calc ∑ i ∈ P, (t (i + 1) - t i) * (if t (i + 1) < w then (1 : ℝ) else 0)
      ≤ ∑ i ∈ range m, (t (i + 1) - t i) * (if t (i + 1) < w then (1 : ℝ) else 0) :=
        Finset.sum_le_sum_of_subset_of_nonneg hm hnn
    _ ≤ max 0 (min w (t m) - t 0) := pointwise_lower t ht w m
    _ ≤ w := by
        apply max_le hw
        have := min_le_left w (t m)
        linarith

/-- **Sum form of the lower end.**  For nondecreasing nonnegative levels and any finite set `P`
of indices, `Σ_{i ∈ P} (t_{i+1} − t_i) · P(W > t_{i+1}) ≤ E W`. -/
theorem lower_layer_sum_le_mean [Nonempty α] (W : α → ℝ) (hW : ∀ a, 0 ≤ W a) (t : ℕ → ℝ)
    (ht : Monotone t) (ht0 : 0 ≤ t 0) (P : Finset ℕ) :
    ∑ i ∈ P, (t (i + 1) - t i) * exceed W (t (i + 1)) ≤ mean W := by
  have h1 : ∑ i ∈ P, (t (i + 1) - t i) * exceed W (t (i + 1))
      = mean (fun a => ∑ i ∈ P, (t (i + 1) - t i) * (if t (i + 1) < W a then (1 : ℝ) else 0)) := by
    rw [mean_sum]
    apply Finset.sum_congr rfl
    intro i _
    rw [mean_const_mul, exceed_eq_mean_indicator]
  rw [h1]
  exact mean_mono fun a => pointwise_lower_subset t ht ht0 (hW a) P

/-- With certified lower bounds `pbar i ≤ P(W > t_{i+1})` on the populated levels. -/
theorem certified_lower_sum_le_mean [Nonempty α] (W : α → ℝ) (hW : ∀ a, 0 ≤ W a) (t : ℕ → ℝ)
    (ht : Monotone t) (ht0 : 0 ≤ t 0) (P : Finset ℕ) (pbar : ℕ → ℝ)
    (hp : ∀ i ∈ P, pbar i ≤ exceed W (t (i + 1))) :
    ∑ i ∈ P, (t (i + 1) - t i) * pbar i ≤ mean W := by
  refine le_trans (Finset.sum_le_sum fun i hi => ?_) (lower_layer_sum_le_mean W hW t ht ht0 P)
  exact mul_le_mul_of_nonneg_left (hp i hi) (sub_nonneg.mpr (ht (Nat.le_succ i)))

/-! ### Width and count: the algebra -/

/-- **Populated part of the upper end against the sum-form lower end.**  If `q i ≤ c · pbar i`
on the populated levels, then
`Σ (e^λ − 1) s_i q_i ≤ c e^{λ+b} · [(1 − e^{−λ}) e^{−b} Σ s_i pbar_i]`. -/
theorem populated_part_le {lam b c : ℝ} (hlam : 0 ≤ lam) (P : Finset ℕ) (s q pbar : ℕ → ℝ)
    (hs : ∀ i ∈ P, 0 ≤ s i) (hq : ∀ i ∈ P, q i ≤ c * pbar i) :
    ∑ i ∈ P, (Real.exp lam - 1) * s i * q i
      ≤ c * Real.exp (lam + b) * ((1 - Real.exp (-lam)) * Real.exp (-b) * ∑ i ∈ P, s i * pbar i) := by
  have hid : c * Real.exp (lam + b) * ((1 - Real.exp (-lam)) * Real.exp (-b))
      = c * (Real.exp lam - 1) := by
    have e1 : Real.exp (lam + b) * Real.exp (-b) = Real.exp lam := by
      rw [← Real.exp_add]; congr 1; ring
    have e2 : Real.exp lam * Real.exp (-lam) = 1 := by
      rw [← Real.exp_add]; simp
    calc c * Real.exp (lam + b) * ((1 - Real.exp (-lam)) * Real.exp (-b))
        = c * (Real.exp (lam + b) * Real.exp (-b)) * (1 - Real.exp (-lam)) := by ring
      _ = c * (Real.exp lam - Real.exp lam * Real.exp (-lam)) := by rw [e1]; ring
      _ = c * (Real.exp lam - 1) := by rw [e2]
  have hrhs : c * Real.exp (lam + b) * ((1 - Real.exp (-lam)) * Real.exp (-b) * ∑ i ∈ P, s i * pbar i)
      = ∑ i ∈ P, (Real.exp lam - 1) * s i * (c * pbar i) := by
    rw [Finset.mul_sum, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    calc c * Real.exp (lam + b) * ((1 - Real.exp (-lam)) * Real.exp (-b) * (s i * pbar i))
        = c * Real.exp (lam + b) * ((1 - Real.exp (-lam)) * Real.exp (-b)) * (s i * pbar i) := by ring
      _ = c * (Real.exp lam - 1) * (s i * pbar i) := by rw [hid]
      _ = (Real.exp lam - 1) * s i * (c * pbar i) := by ring
  rw [hrhs]
  apply Finset.sum_le_sum
  intro i hi
  have h1 : 0 ≤ Real.exp lam - 1 := by
    have := Real.add_one_le_exp lam
    linarith
  exact mul_le_mul_of_nonneg_left (hq i hi) (mul_nonneg h1 (hs i hi))

/-- **The count on which the cost rests**, with the constants of Algorithm 2L+.  The
negligibility threshold of level `s` is `ν s/(ℓ e^b)`; an earlier level `sᵢ ≥ s e^{−x−λ}` has
exceedance probability `P` with `sᵢ P ≤ c e^b ℓ`.  Then `(ν s/(ℓ e^b)) · P ≤ ν c e^{x+λ}`: the two
factors `e^b` cancel. -/
theorem close_points_bound' {ν ℓ b x lam s si P c : ℝ} (hν : 0 ≤ ν) (hℓ : 0 < ℓ)
    (hsi : s * Real.exp (-x - lam) ≤ si) (hP : 0 ≤ P) (hcert : si * P ≤ c * Real.exp b * ℓ) :
    ν * s / (ℓ * Real.exp b) * P ≤ ν * c * Real.exp (x + lam) := by
  have hb : 0 < Real.exp b := Real.exp_pos b
  have hxl : 0 < Real.exp (x + lam) := Real.exp_pos _
  have hden : 0 < ℓ * Real.exp b := mul_pos hℓ hb
  have hexp : Real.exp (-x - lam) * Real.exp (x + lam) = 1 := by
    rw [← Real.exp_add]; simp
  have h1 : s * P ≤ c * Real.exp b * ℓ * Real.exp (x + lam) := by
    have h2 : s * Real.exp (-x - lam) * P ≤ c * Real.exp b * ℓ :=
      (mul_le_mul_of_nonneg_right hsi hP).trans hcert
    have h3 := mul_le_mul_of_nonneg_right h2 hxl.le
    have h4 : s * Real.exp (-x - lam) * P * Real.exp (x + lam) = s * P := by
      calc s * Real.exp (-x - lam) * P * Real.exp (x + lam)
          = s * P * (Real.exp (-x - lam) * Real.exp (x + lam)) := by ring
        _ = s * P := by rw [hexp, mul_one]
    linarith
  rw [div_mul_eq_mul_div, div_le_iff₀ hden]
  calc ν * s * P = ν * (s * P) := by ring
    _ ≤ ν * (c * Real.exp b * ℓ * Real.exp (x + lam)) := mul_le_mul_of_nonneg_left h1 hν
    _ = ν * c * Real.exp (x + lam) * (ℓ * Real.exp b) := by ring

/-- **Width.**  If the bottom level is at most `ε₀ L`, the populated part at most
`c e^{λ+b} L`, the negligible part at most `η' e^b L` and the tail at most `θ e^b L`, then the
upper end is at most `(ε₀ + e^b (c e^λ + η' + θ)) L`. -/
theorem width_le {s0 pop neg tail L b lam c ε0 η' θ : ℝ}
    (h0 : s0 ≤ ε0 * L) (hpop : pop ≤ c * Real.exp (lam + b) * L)
    (hneg : neg ≤ η' * Real.exp b * L) (htail : tail ≤ θ * Real.exp b * L) :
    s0 + pop + neg + tail ≤ (ε0 + Real.exp b * (c * Real.exp lam + η' + θ)) * L := by
  have e : Real.exp (lam + b) = Real.exp lam * Real.exp b := Real.exp_add lam b
  rw [e] at hpop
  nlinarith

end BoundedAccuracy
end MetricChain
