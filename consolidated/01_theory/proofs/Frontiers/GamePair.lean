import proofs.Frontiers.BoundedAccuracy

/-!
# Every game function yields a `HintPair`

Theory report §11.21 (Theorem 11.66) and §11.20, Theorem 11.64, step (ii); workstream F, Theorem
F8 (this file: workstream M, `docs/workstreams/M_REPORT.md`).  In every problem of the family the *hinted* exponent is

  `R(e) = max_{0 ≤ t ≤ 1} [F(t) − t e]`

for a "game function" `F` on `[0, 1]` with `F(0) = F(1) = 0`, and the exponent of non-adaptive
sampling is `θna = R ∘ S⁻¹` with the shift `S(e) = e + R(e)`.  That `(θna, R)` is a `HintPair`
(`HintRecursion.lean`) is a convex-analysis argument which the theory report has as a paper
proof (for the uniform cube `CubeHintPair.lean` does the calculus by hand).  This file proves it
for every game function at once, so that the exact level recursion `exactRec`
(`BoundedAccuracy.lean`) built on `θna` comes within any `η` of `R`
(`exactRec_reaches_hint_of_pair`); and, since `R` is also a lower barrier of the recursion, the
recursion converges to `R`.

**Part 1 — an abstract hinted exponent.**  `HintShape θh E ec` collects the properties of a
hinted exponent on the whole line: convex, nonincreasing, `e + θh e` nondecreasing (slopes in
`[-1, 0]`), nonnegative, zero exactly on `[E, ∞)`, `E > 0`, and a critical accuracy `ec < 0` at
which the shift `S(e) = e + θh e` vanishes and after which it is positive.  For such a function:

* `shiftInv θh x = sSup {e | e + θh e ≤ x}` inverts the shift `[ec, ∞) → [0, ∞)`
  (`strictMonoOn_shift_of_convexOn`: a convex function that vanishes at `ec` and is positive
  afterwards is strictly increasing from `ec` on; `exists_shift_eq`, `shiftInv_shift`,
  `shiftInv_spec`), and is monotone on `[0, ∞)` and continuous on `(0, ∞)`
  (`shiftInv_monotoneOn`, `shiftInv_continuousAt`);
* `partner θh = θh ∘ shiftInv θh` is the non-adaptive partner: `partner_shift` (the functional
  equation `θna (e + θh e) = θh e` on `[ec, ∞)`), `partner_isLeast`
  (`θna(x) = min {θh e : e + θh e ≤ x}`), `partner_antitoneOn`, `partner_le`,
  `partner_continuousAt`, `partner_eq_zero`, `lt_partner` (`θh < θna` on `[0, E)`);
* **`HintShape.pair : HintPair (partner θh) θh (θh ec) (θh 0) E`**, and `HintShape.exists_pair`;
* `exactRec_congr`: `exactRec θna k g`, `g > 0`, depends on `θna` only through its values at
  positive arguments; `HintShape.eq_partner`: the functional equation on `(ec, ∞)` determines
  `θna` on `(0, ∞)`; hence **`HintShape.exactRec_reaches`**: the recursion built on *any* function
  with the functional equation comes within `η` of `θh` on `(0, E)`;
* `HintShape.superSolution : StepLE (partner θh) θh θh` (the convexity argument of the theory
  report, here in abstract form), hence `HintShape.le_exactRec` (no level undercuts `θh`),
  `HintShape.Rstep_hint` (`θh` is a fixed point of the step) and
  **`HintShape.exactRec_tendsto`**: the exact recursion converges to `θh` at every `g > 0`.
* `HintShape.of_convex`: the fields `anti` and `ec_neg` follow from the other seven.

**Part 2 — game functions.**  `GameFunction F E L`: `F` continuous on `[0, 1]`,
`F 0 = F 1 = 0`, `F t ≤ L (1 - t)`, `F t ≤ E t`, `E` sharp, `E > 0`.
`hinted F e = sSup ((fun t => F t - t * e) '' Icc 0 1)` (a maximum: `hinted_attained`) and
`critical F = shiftInv (hinted F) 0`, the largest `e` with `e + R(e) ≤ 0`.  Then
**`GameFunction.hintShape_critical : HintShape (hinted F) E (critical F)`**
(`GameFunction.hintShape` with the critical accuracy quantified), `GameFunction.pair`,
**`GameFunction.exactRec_reaches`** and `GameFunction.exactRec_tendsto`, for any `θna` with
`θna (e + R(e)) = R(e)` wherever the shift `e + R(e)` is positive.  (The shift is nonnegative
everywhere and vanishes on `(-∞, e_c]`, so the equation cannot be asked wherever it is
nonnegative: `GameFunction.not_forall_shift_eq`.)  `GameFunction.critical_eq_neg_L`: if the
constant `L` is sharp then `e_c = -L`, so the bound `a = -e_c` of `θna` is `sup_{t<1} F(t)/(1-t)`,
as `E = sup_{t>0} F(t)/t`.

**Part 3 — a witness.**  `toyGame t = t (1 - t)` is a game function with `E = L = 1`
(`toyGame_gameFunction`); its hinted exponent is `((1 - e)/2)²` on `[-1, 1]`
(`hinted_toyGame`; `-e` below and `0` above), its critical accuracy is `-1`
(`toyGame_hintShape`), its partner is `gaussNa` on `(0, ∞)` (`partner_toyGame`) and its pair has
the constants of `gaussPair` (`toyGame_pair`); so the hypotheses of all the theorems above are
satisfiable, and `gauss_exactRec_tendsto` is the resulting statement about the small-slope pair
of `HintRecursion.lean`.

**Not formalised:** that the exponent functions of the problems of the theory report are of
this form — that their hinted exponents are `max_{t ≤ 1} [F*(t) − t e]` for game functions `F*`
with the properties of `GameFunction`, and that `R ∘ S⁻¹` is the exponent of non-adaptive
sampling (paper theorems of the theory report, §11.20) — and anything about algorithms.
-/

namespace MetricChain.GamePair

open MetricChain.HintRecursion MetricChain.BoundedAccuracy Set

/-! ### The exact recursion sees `θna` only at positive arguments -/

theorem admissible_subset_of_eqOn {θna θna' T T' : ℝ → ℝ} (hθ : ∀ x, 0 < x → θna x = θna' x)
    (hT : ∀ x, 0 < x → T x = T' x) (g : ℝ) : admissible θna T g ⊆ admissible θna' T' g := by
  rintro B ⟨φ, β, hβ, hβg, hφ0, hφ1, h⟩
  refine ⟨φ, β, hβ, hβg, hφ0, hφ1, fun γ hγ => ?_⟩
  have h1 : 0 < (g - β) / φ := div_pos (by linarith) hφ0
  have h2 : 0 < γ / (1 - φ) := div_pos (lt_of_lt_of_le hβ hγ) (by linarith)
  rw [← hθ _ h1, ← hT _ h2]
  exact h γ hγ

/-- The set of admissible bounds at an accuracy depends on `θna` and on the inner exponent
function only through their values at positive arguments. -/
theorem admissible_congr {θna θna' T T' : ℝ → ℝ} (hθ : ∀ x, 0 < x → θna x = θna' x)
    (hT : ∀ x, 0 < x → T x = T' x) (g : ℝ) : admissible θna T g = admissible θna' T' g :=
  Subset.antisymm (admissible_subset_of_eqOn hθ hT g)
    (admissible_subset_of_eqOn (fun x hx => (hθ x hx).symm) (fun x hx => (hT x hx).symm) g)

/-- **Congruence.**  `exactRec θna k g`, `g > 0`, depends on `θna` only through its values at
positive arguments. -/
theorem exactRec_congr {θna θna' : ℝ → ℝ} (hθ : ∀ x, 0 < x → θna x = θna' x) (k : ℕ) :
    ∀ g, 0 < g → exactRec θna k g = exactRec θna' k g := by
  induction k with
  | zero => exact hθ
  | succ k ih =>
    intro g hg
    show min (exactRec θna k g) (Rstep θna (exactRec θna k) g)
      = min (exactRec θna' k g) (Rstep θna' (exactRec θna' k) g)
    unfold Rstep
    rw [ih g hg, admissible_congr hθ ih g]

/-- One step of the recursion from a bounded function above a super-solution `θh` stays above
it: `θh ≤ R[T]` whenever `θh ≤ T` (the abstract form of `hintClip_le_Rstep`). -/
theorem le_Rstep_of_superSolution {θna θh T : ℝ → ℝ} {C : ℝ} (hss : StepLE θna θh θh)
    (hT : ∀ x, 0 < x → θh x ≤ T x) (hTC : ∀ x, 0 < x → T x ≤ C) {g : ℝ} (hg : 0 < g) :
    θh g ≤ Rstep θna T g := by
  apply le_csInf (admissible_nonempty hTC hg)
  intro B hB
  obtain ⟨φ, β, hβ, hβg, hφ0, hφ1, h⟩ := admissible_subset_of_le hT g hB
  exact hss g φ β B hβ hβg hφ0 hφ1 h

/-! ### Three elementary facts about convex functions and functions with slopes in `[-1, 0]` -/

/-- A nonincreasing function `f` for which `e ↦ e + f e` is nondecreasing (slopes in `[-1, 0]`)
is `1`-Lipschitz. -/
theorem lipschitz_of_antitone_of_shift_monotone {f : ℝ → ℝ} (ha : Antitone f)
    (hm : Monotone fun e => e + f e) : LipschitzWith 1 f := by
  refine LipschitzWith.of_le_add fun x y => ?_
  rw [Real.dist_eq]
  rcases le_total x y with h | h
  · have h1 : x + f x ≤ y + f y := hm h
    have h2 : y - x ≤ |x - y| := by rw [abs_sub_comm]; exact le_abs_self _
    linarith
  · have h1 : f x ≤ f y := ha h
    linarith [abs_nonneg (x - y)]

/-- A convex nonnegative function that vanishes exactly from `E` on is nonincreasing. -/
theorem antitone_of_convexOn_of_zero_iff {θh : ℝ → ℝ} {E : ℝ} (hc : ConvexOn ℝ univ θh)
    (hnn : ∀ e, 0 ≤ θh e) (hz : ∀ e, θh e = 0 ↔ E ≤ e) : Antitone θh := by
  intro x y hxy
  rcases le_or_gt E y with hy | hy
  · rw [(hz y).mpr hy]
    exact hnn x
  · have hd : 0 < E - x := by linarith
    obtain ⟨a, ha0, ha1, hay⟩ : ∃ a : ℝ, 0 ≤ a ∧ a ≤ 1 ∧ a * x + (1 - a) * E = y := by
      refine ⟨(E - y) / (E - x), div_nonneg (by linarith) hd.le, ?_, ?_⟩
      · rw [div_le_one hd]; linarith
      · field_simp; ring
    have h := hc.2 (mem_univ x) (mem_univ E) ha0 (sub_nonneg.mpr ha1) (by ring)
    simp only [smul_eq_mul] at h
    rw [hay, (hz E).mpr le_rfl, mul_zero, add_zero] at h
    have h1 : a * θh x ≤ 1 * θh x := mul_le_mul_of_nonneg_right ha1 (hnn x)
    linarith

/-- If `θh` is convex and the shift `e ↦ e + θh e` vanishes at `ec` and is positive afterwards,
then the shift is strictly increasing from `ec` on (a convex function that is zero at a point
and positive afterwards is strictly increasing from that point on). -/
theorem strictMonoOn_shift_of_convexOn {θh : ℝ → ℝ} {ec : ℝ} (hc : ConvexOn ℝ univ θh)
    (hz : ec + θh ec = 0) (hpos : ∀ e, ec < e → 0 < e + θh e) :
    StrictMonoOn (fun e => e + θh e) (Ici ec) := by
  intro x hx y _ hxy
  have hx' : ec ≤ x := hx
  have hSy : 0 < y + θh y := hpos y (lt_of_le_of_lt hx' hxy)
  have hd : 0 < y - ec := by linarith
  obtain ⟨a, ha, ha1, hax⟩ : ∃ a : ℝ, 0 < a ∧ a ≤ 1 ∧ a * ec + (1 - a) * y = x := by
    refine ⟨(y - x) / (y - ec), div_pos (by linarith) hd, ?_, ?_⟩
    · rw [div_le_one hd]; linarith
    · field_simp; ring
  have h := hc.2 (mem_univ ec) (mem_univ y) ha.le (sub_nonneg.mpr ha1) (by ring)
  simp only [smul_eq_mul] at h
  rw [hax] at h
  have h1 : a * (ec + θh ec) = 0 := by rw [hz, mul_zero]
  have h2 : 0 < a * (y + θh y) := mul_pos ha hSy
  show x + θh x < y + θh y
  linarith

/-! ### Part 1: from an abstract hinted exponent to a pair -/

/-- The abstract properties of a hinted exponent function on the whole line. -/
structure HintShape (θh : ℝ → ℝ) (E ec : ℝ) : Prop where
  convex : ConvexOn ℝ Set.univ θh
  anti : Antitone θh
  shift_mono : Monotone (fun e => e + θh e)        -- slopes at least −1
  nonneg : ∀ e, 0 ≤ θh e
  zero_iff : ∀ e, θh e = 0 ↔ E ≤ e
  E_pos : 0 < E
  ec_neg : ec < 0
  ec_zero : ec + θh ec = 0
  pos_after : ∀ e, ec < e → 0 < e + θh e

/-- The generalised inverse of the shift `S(e) = e + θh e`: the largest `e` with `S(e) ≤ x`. -/
noncomputable def shiftInv (θh : ℝ → ℝ) (x : ℝ) : ℝ := sSup {e | e + θh e ≤ x}

/-- The non-adaptive partner `θna = θh ∘ S⁻¹` of a hinted exponent `θh`, `S(e) = e + θh e`.
(Its values at `x < 0` are of no significance.) -/
noncomputable def partner (θh : ℝ → ℝ) (x : ℝ) : ℝ := θh (shiftInv θh x)

/-- The fields `anti` and `ec_neg` of `HintShape` follow from the other seven. -/
theorem HintShape.of_convex {θh : ℝ → ℝ} {E ec : ℝ} (hc : ConvexOn ℝ univ θh)
    (hm : Monotone fun e => e + θh e) (hnn : ∀ e, 0 ≤ θh e) (hz : ∀ e, θh e = 0 ↔ E ≤ e)
    (hE : 0 < E) (hec : ec + θh ec = 0) (hpos : ∀ e, ec < e → 0 < e + θh e) :
    HintShape θh E ec where
  convex := hc
  anti := antitone_of_convexOn_of_zero_iff hc hnn hz
  shift_mono := hm
  nonneg := hnn
  zero_iff := hz
  E_pos := hE
  ec_neg := by
    have h1 : ec ≤ 0 := by linarith [hnn ec]
    refine lt_of_le_of_ne h1 fun h => ?_
    rw [h, zero_add] at hec
    exact absurd ((hz 0).mp hec) (not_le.mpr hE)
  ec_zero := hec
  pos_after := hpos

namespace HintShape

section

variable {θh : ℝ → ℝ} {E ec : ℝ}

theorem le_shift (hs : HintShape θh E ec) (e : ℝ) : e ≤ e + θh e := by
  linarith [hs.nonneg e]

/-- The hinted exponent is positive below the threshold `E`. -/
theorem hint_pos (hs : HintShape θh E ec) {e : ℝ} (he : e < E) : 0 < θh e :=
  lt_of_le_of_ne (hs.nonneg e) fun h => absurd ((hs.zero_iff e).mp h.symm) (not_le.mpr he)

/-- Slopes in `[-1, 0]`: the hinted exponent is `1`-Lipschitz (convexity is not used). -/
theorem lipschitz (hs : HintShape θh E ec) : LipschitzWith 1 θh :=
  lipschitz_of_antitone_of_shift_monotone hs.anti hs.shift_mono

theorem continuous (hs : HintShape θh E ec) : Continuous θh := hs.lipschitz.continuous

/-- The shift is strictly increasing from `ec` on (only `convex`, `ec_zero` and `pos_after` are
used: on `[ec, ∞)` the slope condition `shift_mono` is a consequence of these). -/
theorem shift_strictMonoOn (hs : HintShape θh E ec) :
    StrictMonoOn (fun e => e + θh e) (Ici ec) :=
  strictMonoOn_shift_of_convexOn hs.convex hs.ec_zero hs.pos_after

/-- The shift is positive only after `ec`. -/
theorem lt_of_shift_pos (hs : HintShape θh E ec) {e : ℝ} (he : 0 < e + θh e) : ec < e := by
  by_contra hcon
  rw [not_lt] at hcon
  have h1 : e + θh e ≤ ec + θh ec := hs.shift_mono hcon
  linarith [hs.ec_zero]

/-- The shift maps `[ec, ∞)` onto `[0, ∞)`. -/
theorem exists_shift_eq (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) :
    ∃ e, ec ≤ e ∧ e + θh e = x := by
  have hc : ContinuousOn (fun e => e + θh e) (Icc ec x) :=
    (continuous_id.add hs.continuous).continuousOn
  have hmem : x ∈ Icc (ec + θh ec) (x + θh x) :=
    ⟨by rw [hs.ec_zero]; exact hx, hs.le_shift x⟩
  obtain ⟨e, he, hex⟩ := intermediate_value_Icc (by linarith [hs.ec_neg] : ec ≤ x) hc hmem
  exact ⟨e, he.1, hex⟩

/-- `S⁻¹(S(e)) = e` for `e ≥ ec`. -/
theorem shiftInv_shift (hs : HintShape θh E ec) {e : ℝ} (he : ec ≤ e) :
    shiftInv θh (e + θh e) = e := by
  unfold shiftInv
  apply le_antisymm
  · refine csSup_le ⟨e, le_refl (e + θh e)⟩ fun e' he' => ?_
    by_contra hcon
    rw [not_le] at hcon
    have h1 : e + θh e < e' + θh e' := hs.shift_strictMonoOn he (he.trans hcon.le) hcon
    have h2 : e' + θh e' ≤ e + θh e := he'
    linarith
  · exact le_csSup ⟨e + θh e, fun e' he' => (hs.le_shift e').trans he'⟩
      (show e + θh e ≤ e + θh e from le_rfl)

/-- For `x ≥ 0`, `S⁻¹(x) ≥ ec` and `S(S⁻¹(x)) = x`. -/
theorem shiftInv_spec (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) :
    ec ≤ shiftInv θh x ∧ shiftInv θh x + θh (shiftInv θh x) = x := by
  obtain ⟨e, he, rfl⟩ := hs.exists_shift_eq hx
  rw [hs.shiftInv_shift he]
  exact ⟨he, rfl⟩

/-- The critical accuracy is determined by the function: it is `S⁻¹(0)`. -/
theorem shiftInv_zero (hs : HintShape θh E ec) : shiftInv θh 0 = ec := by
  have h := hs.shiftInv_shift le_rfl
  rwa [hs.ec_zero] at h

theorem lt_shiftInv (hs : HintShape θh E ec) {x : ℝ} (hx : 0 < x) : ec < shiftInv θh x :=
  hs.lt_of_shift_pos (by rw [(hs.shiftInv_spec hx.le).2]; exact hx)

theorem shiftInv_le (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) : shiftInv θh x ≤ x := by
  have h := (hs.shiftInv_spec hx).2
  linarith [hs.nonneg (shiftInv θh x)]

theorem shiftInv_monotoneOn (hs : HintShape θh E ec) : MonotoneOn (shiftInv θh) (Ici 0) := by
  intro x hx y _ hxy
  have hx' : (0 : ℝ) ≤ x := hx
  show sSup {e | e + θh e ≤ x} ≤ sSup {e | e + θh e ≤ y}
  refine csSup_le_csSup ⟨y, fun e he => (hs.le_shift e).trans he⟩ ⟨ec, ?_⟩
    (fun e he => le_trans he hxy)
  show ec + θh ec ≤ x
  rw [hs.ec_zero]
  exact hx'

/-- The inverse of the shift is continuous on `(0, ∞)`: it is monotone and its range contains a
neighbourhood of each of its values there. -/
theorem shiftInv_continuousAt (hs : HintShape θh E ec) {x : ℝ} (hx : 0 < x) :
    ContinuousAt (shiftInv θh) x := by
  refine continuousAt_of_monotoneOn_of_image_mem_nhds (s := Ioi 0)
    (hs.shiftInv_monotoneOn.mono Ioi_subset_Ici_self) (Ioi_mem_nhds hx) ?_
  refine Filter.mem_of_superset (Ioi_mem_nhds (hs.lt_shiftInv hx)) fun e he => ?_
  exact ⟨e + θh e, hs.pos_after e he, hs.shiftInv_shift (le_of_lt he)⟩

/-! #### The partner -/

/-- The functional equation `θna (e + θh e) = θh e` on `[ec, ∞)`. -/
theorem partner_shift (hs : HintShape θh E ec) {e : ℝ} (he : ec ≤ e) :
    partner θh (e + θh e) = θh e := by
  unfold partner
  rw [hs.shiftInv_shift he]

theorem partner_nonneg (hs : HintShape θh E ec) (x : ℝ) : 0 ≤ partner θh x :=
  hs.nonneg _

theorem partner_antitoneOn (hs : HintShape θh E ec) : AntitoneOn (partner θh) (Ici 0) :=
  fun _ hx _ hy hxy => hs.anti (hs.shiftInv_monotoneOn hx hy hxy)

/-- The partner is at most `a = θh ec = -ec`. -/
theorem partner_le (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) : partner θh x ≤ θh ec :=
  hs.anti (hs.shiftInv_spec hx).1

/-- The hinted exponent lies below its partner. -/
theorem le_partner (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) : θh x ≤ partner θh x :=
  hs.anti (hs.shiftInv_le hx)

/-- Below the threshold the hinted exponent is strictly smaller than its partner. -/
theorem lt_partner (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) (hxE : x < E) :
    θh x < partner θh x := by
  have hS := (hs.shiftInv_spec hx).2
  show θh x < θh (shiftInv θh x)
  generalize shiftInv θh x = r at hS ⊢
  have hr : 0 < θh r := hs.hint_pos (by linarith [hs.nonneg r])
  have hd : 0 < E - r := by linarith
  obtain ⟨a, ha0, ha1, hax⟩ : ∃ a : ℝ, 0 ≤ a ∧ a < 1 ∧ a * r + (1 - a) * E = x := by
    refine ⟨(E - x) / (E - r), div_nonneg (by linarith) hd.le, ?_, ?_⟩
    · rw [div_lt_one hd]; linarith
    · field_simp; ring
  have hc := hs.convex.2 (mem_univ r) (mem_univ E) ha0 (by linarith : (0 : ℝ) ≤ 1 - a) (by ring)
  simp only [smul_eq_mul] at hc
  rw [hax, (hs.zero_iff E).mpr le_rfl, mul_zero, add_zero] at hc
  have h1 : a * θh r < 1 * θh r := mul_lt_mul_of_pos_right ha1 hr
  linarith

/-- On `[0, ∞)` the partner is `x - S⁻¹(x)`. -/
theorem partner_eq_sub (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) :
    partner θh x = x - shiftInv θh x := by
  have h := (hs.shiftInv_spec hx).2
  unfold partner
  linarith

/-- The partner is the least hinted exponent among the accuracies whose shift is at most `x`:
`θna(x) = min {θh e : e + θh e ≤ x}`. -/
theorem partner_isLeast (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) :
    IsLeast (θh '' {e | e + θh e ≤ x}) (partner θh x) := by
  refine ⟨⟨shiftInv θh x, (hs.shiftInv_spec hx).2.le, rfl⟩, ?_⟩
  rintro _ ⟨e, he, rfl⟩
  exact hs.anti (le_csSup ⟨x, fun e' he' => (hs.le_shift e').trans he'⟩ he)

theorem partner_continuousAt (hs : HintShape θh E ec) {x : ℝ} (hx : 0 < x) :
    ContinuousAt (partner θh) x :=
  hs.continuous.continuousAt.comp (hs.shiftInv_continuousAt hx)

/-- From `E` on the partner vanishes. -/
theorem partner_eq_zero (hs : HintShape θh E ec) {x : ℝ} (hx : E ≤ x) : partner θh x = 0 := by
  have h0 : θh x = 0 := (hs.zero_iff x).mpr hx
  have h := hs.partner_shift (e := x) (by linarith [hs.ec_neg, hs.E_pos])
  rwa [h0, add_zero] at h

/-- **The pair.**  The hinted exponent and its partner satisfy `HintPair`, with `a = θh ec = -ec`
and `h = θh 0`; the constant of `hint_lower` is `1`. -/
theorem pair (hs : HintShape θh E ec) : HintPair (partner θh) θh (θh ec) (θh 0) E where
  h_pos := hs.hint_pos hs.E_pos
  a_pos := by linarith [hs.ec_zero, hs.ec_neg]
  na_le := fun _ hx => hs.partner_le hx.le
  na_cont := fun _ hx => hs.partner_continuousAt hx
  na_h := by
    have h := hs.partner_shift hs.ec_neg.le
    rwa [zero_add] at h
  ident := fun _ he _ => hs.partner_shift (hs.ec_neg.le.trans he.le)
  hint_pos := fun _ _ he => hs.hint_pos he
  hint_mono := fun _ _ _ hee' _ => hs.shift_mono hee'
  hint_lower := ⟨1, fun e he _ => by
    have h : 0 + θh 0 ≤ e + θh e := hs.shift_mono he.le
    linarith⟩

/-- The functional equation on `(ec, ∞)` determines `θna` on `(0, ∞)`. -/
theorem eq_partner (hs : HintShape θh E ec) {θna : ℝ → ℝ}
    (hfun : ∀ e, ec < e → θna (e + θh e) = θh e) {x : ℝ} (hx : 0 < x) :
    θna x = partner θh x := by
  have h := hfun _ (hs.lt_shiftInv hx)
  rw [(hs.shiftInv_spec hx.le).2] at h
  exact h

/-! #### The hinted exponent is a lower barrier of the recursion -/

/-- **The hinted exponent is a super-solution** of the recursion built on its partner: one step
from it does not go below it.  At `γ = max(β, μ)`, `μ = φ θna((g-β)/φ) = φ θh(eo)`, the bracket is
the convex combination `φ θh(eo) + (1-φ) θh(ei)` with `ei = γ/(1-φ)`, and
`φ eo + (1-φ) ei ≤ φ (eo + θh eo) + β = g`; `θh` is convex and nonincreasing. -/
theorem superSolution (hs : HintShape θh E ec) : StepLE (partner θh) θh θh := by
  intro g φ β B hβ hβg hφ0 hφ1 hB
  show θh g ≤ B
  have h1 : 0 < 1 - φ := by linarith
  have hx : 0 ≤ (g - β) / φ := div_nonneg (by linarith) hφ0.le
  obtain ⟨eo, hpart, hS⟩ : ∃ eo, partner θh ((g - β) / φ) = θh eo ∧ eo + θh eo = (g - β) / φ :=
    ⟨_, rfl, (hs.shiftInv_spec hx).2⟩
  have hμ0 : 0 ≤ φ * θh eo := mul_nonneg hφ0.le (hs.nonneg eo)
  have hkey := hB (max β (φ * θh eo)) (le_max_left _ _)
  rw [hpart, min_eq_right (le_max_right _ _)] at hkey
  have hconv := hs.convex.2 (mem_univ eo) (mem_univ (max β (φ * θh eo) / (1 - φ))) hφ0.le h1.le
    (by ring)
  simp only [smul_eq_mul] at hconv
  have h2 : (1 - φ) * (max β (φ * θh eo) / (1 - φ)) = max β (φ * θh eo) := by field_simp
  have h3 : max β (φ * θh eo) ≤ β + φ * θh eo := max_le (by linarith) (by linarith)
  have h4 : φ * (eo + θh eo) = g - β := by rw [hS]; field_simp
  have hmean : φ * eo + (1 - φ) * (max β (φ * θh eo) / (1 - φ)) ≤ g := by rw [h2]; linarith
  exact (hs.anti hmean).trans (hconv.trans hkey)

/-- **No level of the exact recursion built on the partner undercuts the hinted exponent.** -/
theorem le_exactRec_partner (hs : HintShape θh E ec) (k : ℕ) :
    ∀ g, 0 < g → θh g ≤ exactRec (partner θh) k g := by
  induction k with
  | zero => exact fun g hg => hs.le_partner hg.le
  | succ k ih =>
    intro g hg
    show θh g ≤ min (exactRec (partner θh) k g) (Rstep (partner θh) (exactRec (partner θh) k) g)
    have hP := exactRec_props (fun x _ => hs.partner_nonneg x)
      (fun _ _ hx hxy => hs.partner_antitoneOn hx.le (hx.le.trans hxy) hxy)
      (fun _ hx => hs.partner_le hx.le) k
    exact le_min (ih g hg) (le_Rstep_of_superSolution hs.superSolution ih hP.2.1 hg)

end

end HintShape

/-- There is a non-adaptive partner, and it forms a `HintPair`. -/
theorem HintShape.exists_pair {θh : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec) :
    ∃ θna : ℝ → ℝ, HintPair θna θh (θh ec) (θh 0) E ∧
      (∀ e, ec ≤ e → θna (e + θh e) = θh e) ∧
      (∀ x, 0 < x → 0 ≤ θna x) ∧ (∀ x y, 0 < x → x ≤ y → θna y ≤ θna x) :=
  ⟨partner θh, hs.pair, fun _ he => hs.partner_shift he, fun x _ => hs.partner_nonneg x,
    fun _ _ hx hxy => hs.partner_antitoneOn hx.le (hx.le.trans hxy) hxy⟩

/-- The recursion built on any function with the functional equation on `(ec, ∞)` reaches `θh`
(nothing is assumed about `θna` on `(-∞, 0]`). -/
theorem HintShape.exactRec_reaches' {θh θna : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec)
    (hfun : ∀ e, ec < e → θna (e + θh e) = θh e)
    {g : ℝ} (hg : 0 < g) (hgE : g < E) {η : ℝ} (hη : 0 < η) :
    ∃ k, exactRec θna k g < θh g + η := by
  obtain ⟨k, hk⟩ := exactRec_reaches_hint_of_pair hs.pair (fun x _ => hs.partner_nonneg x)
    (fun _ _ hx hxy => hs.partner_antitoneOn hx.le (hx.le.trans hxy) hxy) hg hgE hη
  refine ⟨k, ?_⟩
  rw [exactRec_congr (fun x hx => hs.eq_partner hfun hx) k g hg]
  exact hk

/-- The recursion built on *any* function with the functional equation reaches `θh`. -/
theorem HintShape.exactRec_reaches {θh θna : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec)
    (hfun : ∀ e, ec ≤ e → θna (e + θh e) = θh e)
    {g : ℝ} (hg : 0 < g) (hgE : g < E) {η : ℝ} (hη : 0 < η) :
    ∃ k, exactRec θna k g < θh g + η :=
  hs.exactRec_reaches' (fun e he => hfun e he.le) hg hgE hη

/-- No level of the recursion built on a function with the functional equation undercuts the
hinted exponent. -/
theorem HintShape.le_exactRec {θh θna : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec)
    (hfun : ∀ e, ec < e → θna (e + θh e) = θh e) (k : ℕ) {g : ℝ} (hg : 0 < g) :
    θh g ≤ exactRec θna k g := by
  rw [exactRec_congr (fun x hx => hs.eq_partner hfun hx) k g hg]
  exact hs.le_exactRec_partner k g hg

/-- **The hinted exponent is a fixed point of the step**: `R[θh] = θh` on `(0, E)`, for the step
built on its partner (`step_from_hint_le` and `HintShape.superSolution`). -/
theorem HintShape.Rstep_hint {θh : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec) {g : ℝ}
    (hg : 0 < g) (hgE : g < E) : Rstep (partner θh) θh g = θh g := by
  apply le_antisymm
  · have hstep : StepLE (partner θh) θh (Rstep (partner θh) θh) := by
      intro g φ β B hβ hβg hφ0 hφ1 hB
      exact csInf_le ⟨0, fun b hb => admissible_nonneg (fun x _ => hs.partner_nonneg x)
        (fun x _ => hs.nonneg x) hb⟩ ⟨φ, β, hβ, hβg, hφ0, hφ1, hB⟩
    exact step_from_hint_le hs.pair hstep (fun _ _ _ hxy => hs.anti hxy) hg hgE
  · exact le_Rstep_of_superSolution hs.superSolution (fun _ _ => le_rfl)
      (fun _ hx => hs.anti hx.le) hg

/-- **The exact recursion converges to the hinted exponent**, at every accuracy rate `g > 0`
(from `E` on every level is zero). -/
theorem HintShape.exactRec_tendsto {θh θna : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec)
    (hfun : ∀ e, ec < e → θna (e + θh e) = θh e) {g : ℝ} (hg : 0 < g) :
    Filter.Tendsto (fun k => exactRec θna k g) Filter.atTop (nhds (θh g)) := by
  have hanti : Antitone (fun k => exactRec θna k g) :=
    antitone_nat_of_succ_le fun k => by
      show min (exactRec θna k g) (Rstep θna (exactRec θna k) g) ≤ exactRec θna k g
      exact min_le_left _ _
  have hreach : ∀ η : ℝ, 0 < η → ∃ k, exactRec θna k g < θh g + η := by
    intro η hη
    rcases lt_or_ge g E with h | h
    · exact hs.exactRec_reaches' hfun hg h hη
    · refine ⟨0, ?_⟩
      show θna g < θh g + η
      rw [hs.eq_partner hfun hg, hs.partner_eq_zero h, (hs.zero_iff g).mpr h]
      linarith
  rw [Metric.tendsto_atTop]
  intro ε hε
  obtain ⟨k, hk⟩ := hreach ε hε
  refine ⟨k, fun m hm => ?_⟩
  have h1 : exactRec θna m g ≤ exactRec θna k g := hanti hm
  have h2 := hs.le_exactRec hfun m hg
  rw [Real.dist_eq, abs_lt]
  constructor <;> linarith

/-! ### Part 2: from a game function to the abstract properties -/

/-- A game function on `[0,1]`. -/
structure GameFunction (F : ℝ → ℝ) (E L : ℝ) : Prop where
  cont : ContinuousOn F (Set.Icc 0 1)
  zero0 : F 0 = 0
  zero1 : F 1 = 0
  le_lin : ∀ t ∈ Set.Icc (0 : ℝ) 1, F t ≤ L * (1 - t)
  le_E : ∀ t ∈ Set.Icc (0 : ℝ) 1, F t ≤ E * t
  E_sharp : ∀ e, e < E → ∃ t ∈ Set.Ioc (0 : ℝ) 1, e * t < F t
  E_pos : 0 < E

/-- The hinted exponent of a game function. -/
noncomputable def hinted (F : ℝ → ℝ) (e : ℝ) : ℝ := sSup ((fun t => F t - t * e) '' Set.Icc 0 1)

/-- The critical accuracy `e_c` of a game function: the largest `e` with `e + R(e) ≤ 0`. -/
noncomputable def critical (F : ℝ → ℝ) : ℝ := shiftInv (hinted F) 0

/-- An upper bound of all `F t - t e`, `0 ≤ t ≤ 1`, is an upper bound of the hinted exponent. -/
theorem hinted_le {F : ℝ → ℝ} {e B : ℝ} (h : ∀ t ∈ Icc (0 : ℝ) 1, F t - t * e ≤ B) :
    hinted F e ≤ B :=
  csSup_le ⟨_, 0, ⟨le_rfl, zero_le_one⟩, rfl⟩ (by rintro _ ⟨t, ht, rfl⟩; exact h t ht)

namespace GameFunction

section

variable {F : ℝ → ℝ} {E L : ℝ}

theorem sub_le_max (hF : GameFunction F E L) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) 1) (e : ℝ) :
    F t - t * e ≤ max 0 (E - e) := by
  have h1 := hF.le_E t ht
  rcases le_total 0 (E - e) with h | h
  · have h2 : t * (E - e) ≤ 1 * (E - e) := mul_le_mul_of_nonneg_right ht.2 h
    exact le_max_of_le_right (by linarith)
  · have h2 : t * (E - e) ≤ 0 := mul_nonpos_of_nonneg_of_nonpos ht.1 h
    exact le_max_of_le_left (by linarith)

/-- The supremum in `hinted` is over a set that is bounded above (by `le_E`; continuity of the
game function is not needed). -/
theorem bddAbove (hF : GameFunction F E L) (e : ℝ) :
    BddAbove ((fun t => F t - t * e) '' Icc 0 1) :=
  ⟨max 0 (E - e), by rintro _ ⟨t, ht, rfl⟩; exact hF.sub_le_max ht e⟩

theorem le_hinted (hF : GameFunction F E L) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) 1) (e : ℝ) :
    F t - t * e ≤ hinted F e :=
  le_csSup (hF.bddAbove e) ⟨t, ht, rfl⟩

/-- The supremum in the definition of the hinted exponent is a maximum (the only use of the
continuity of the game function). -/
theorem hinted_attained (hF : GameFunction F E L) (e : ℝ) :
    ∃ t ∈ Icc (0 : ℝ) 1, hinted F e = F t - t * e :=
  isCompact_Icc.exists_sSup_image_eq (nonempty_Icc.mpr zero_le_one)
    (hF.cont.sub (continuousOn_id.mul continuousOn_const))

theorem hinted_nonneg (hF : GameFunction F E L) (e : ℝ) : 0 ≤ hinted F e := by
  have h := hF.le_hinted (t := 0) ⟨le_rfl, zero_le_one⟩ e
  rw [hF.zero0] at h
  linarith

/-- `R(e) ≥ -e`, from `t = 1`: the shift `e + R(e)` is nonnegative. -/
theorem neg_le_hinted (hF : GameFunction F E L) (e : ℝ) : -e ≤ hinted F e := by
  have h := hF.le_hinted (t := 1) ⟨zero_le_one, le_rfl⟩ e
  rw [hF.zero1] at h
  linarith

theorem hinted_le_max (hF : GameFunction F E L) (e : ℝ) : hinted F e ≤ max 0 (E - e) :=
  hinted_le fun _ ht => hF.sub_le_max ht e

/-- A supremum of affine functions is convex. -/
theorem hinted_convexOn (hF : GameFunction F E L) : ConvexOn ℝ univ (hinted F) := by
  refine ⟨convex_univ, fun x _ y _ a b ha hb hab => ?_⟩
  apply hinted_le
  intro t ht
  have h1 := mul_le_mul_of_nonneg_left (hF.le_hinted ht x) ha
  have h2 := mul_le_mul_of_nonneg_left (hF.le_hinted ht y) hb
  have h3 : F t - t * (a * x + b * y) = a * (F t - t * x) + b * (F t - t * y) := by
    linear_combination (-(F t)) * hab
  simp only [smul_eq_mul]
  rw [h3]
  linarith

/-- Slopes at most `0` (because `t ≥ 0`). -/
theorem hinted_antitone (hF : GameFunction F E L) : Antitone (hinted F) := by
  intro x y hxy
  apply hinted_le
  intro t ht
  have h1 := hF.le_hinted ht x
  have h2 : t * x ≤ t * y := mul_le_mul_of_nonneg_left hxy ht.1
  linarith

/-- Slopes at least `-1` (because `t ≤ 1`). -/
theorem hinted_shift_monotone (hF : GameFunction F E L) :
    Monotone (fun e => e + hinted F e) := by
  intro x y hxy
  show x + hinted F x ≤ y + hinted F y
  have h : hinted F x ≤ y - x + hinted F y := by
    apply hinted_le
    intro t ht
    have h1 := hF.le_hinted ht y
    have h2 : (1 - t) * x ≤ (1 - t) * y := mul_le_mul_of_nonneg_left hxy (by linarith [ht.2])
    linarith
  linarith

/-- The hinted exponent vanishes exactly from `E` on. -/
theorem hinted_eq_zero_iff (hF : GameFunction F E L) (e : ℝ) : hinted F e = 0 ↔ E ≤ e := by
  constructor
  · intro h
    by_contra hcon
    rw [not_le] at hcon
    obtain ⟨t, ht, hlt⟩ := hF.E_sharp e hcon
    have h1 := hF.le_hinted (Ioc_subset_Icc_self ht) e
    linarith
  · intro h
    refine le_antisymm (hinted_le fun t ht => ?_) (hF.hinted_nonneg e)
    have h1 := hF.le_E t ht
    have h2 : t * E ≤ t * e := mul_le_mul_of_nonneg_left h ht.1
    linarith

/-- The constant of `le_lin` is nonnegative. -/
theorem L_nonneg (hF : GameFunction F E L) : 0 ≤ L := by
  have h := hF.le_lin 0 ⟨le_rfl, zero_le_one⟩
  rw [hF.zero0] at h
  linarith

/-- `R(-L) ≤ L`: the shift vanishes at `-L`. -/
theorem hinted_neg_L_le (hF : GameFunction F E L) : hinted F (-L) ≤ L := by
  apply hinted_le
  intro t ht
  have h1 := hF.le_lin t ht
  linarith

/-- **The hinted exponent of a game function has the abstract properties**, with the critical
accuracy `e_c = max {e | e + R(e) ≤ 0}`. -/
theorem hintShape_critical (hF : GameFunction F E L) :
    HintShape (hinted F) E (critical F) := by
  have hcont : Continuous fun e => e + hinted F e :=
    continuous_id.add (lipschitz_of_antitone_of_shift_monotone hF.hinted_antitone
      hF.hinted_shift_monotone).continuous
  have hne : ({e | e + hinted F e ≤ 0} : Set ℝ).Nonempty :=
    ⟨-L, by show -L + hinted F (-L) ≤ 0; linarith [hF.hinted_neg_L_le]⟩
  have hbdd : BddAbove {e | e + hinted F e ≤ 0} :=
    ⟨0, fun e he => by
      have h : e + hinted F e ≤ 0 := he
      linarith [hF.hinted_nonneg e]⟩
  have hcl : IsClosed {e | e + hinted F e ≤ 0} := isClosed_le hcont continuous_const
  have hmem : critical F + hinted F (critical F) ≤ 0 := hcl.csSup_mem hne hbdd
  have hzero : critical F + hinted F (critical F) = 0 :=
    le_antisymm hmem (by linarith [hF.neg_le_hinted (critical F)])
  exact HintShape.of_convex hF.hinted_convexOn hF.hinted_shift_monotone hF.hinted_nonneg
    hF.hinted_eq_zero_iff hF.E_pos hzero
    (fun e he => not_le.mp fun h => absurd (le_csSup hbdd h) (not_le.mpr he))

/-- `a = R(e_c) = -e_c`. -/
theorem hinted_critical (hF : GameFunction F E L) : hinted F (critical F) = -critical F := by
  linarith [hF.hintShape_critical.ec_zero]

/-- The critical accuracy is at least `-L` (and negative: `hintShape_critical.ec_neg`). -/
theorem neg_L_le_critical (hF : GameFunction F E L) : -L ≤ critical F := by
  by_contra hcon
  rw [not_le] at hcon
  have h := hF.hintShape_critical.pos_after (-L) hcon
  linarith [hF.hinted_neg_L_le]

/-- If the constant `L` of `le_lin` is sharp, the critical accuracy is `-L`: the bound
`a = R(e_c) = -e_c` of the non-adaptive exponent is `sup_{t < 1} F(t)/(1 - t)`, as the threshold
`E` is `sup_{t > 0} F(t)/t`. -/
theorem critical_eq_neg_L (hF : GameFunction F E L)
    (hL : ∀ l, l < L → ∃ t ∈ Ico (0 : ℝ) 1, l * (1 - t) < F t) : critical F = -L := by
  refine le_antisymm ?_ hF.neg_L_le_critical
  by_contra hcon
  rw [not_le] at hcon
  obtain ⟨t, ht, hlt⟩ := hL (-critical F) (by linarith)
  have h1 := hF.le_hinted (Ico_subset_Icc_self ht) (critical F)
  have h2 := hF.hintShape_critical.ec_zero
  linarith

/-- The shift vanishes up to the critical accuracy: `R(e) = -e` for `e ≤ e_c`. -/
theorem shift_eq_zero (hF : GameFunction F E L) {e : ℝ} (he : e ≤ critical F) :
    e + hinted F e = 0 := by
  have h1 : e + hinted F e ≤ critical F + hinted F (critical F) :=
    hF.hintShape_critical.shift_mono he
  linarith [hF.hintShape_critical.ec_zero, hF.neg_le_hinted e]

/-- The functional equation for the partner, wherever the shift is positive. -/
theorem partner_shift (hF : GameFunction F E L) {e : ℝ} (he : 0 < e + hinted F e) :
    partner (hinted F) (e + hinted F e) = hinted F e :=
  hF.hintShape_critical.partner_shift (hF.hintShape_critical.lt_of_shift_pos he).le

/-- The functional equation cannot be asked wherever the shift is nonnegative: the shift is
nonnegative everywhere and vanishes on `(-∞, e_c]`, where the hinted exponent `-e` is not
constant.  (Hence the strict inequality in `GameFunction.exactRec_reaches`.) -/
theorem not_forall_shift_eq (hF : GameFunction F E L) (θna : ℝ → ℝ) :
    ¬ ∀ e, 0 ≤ e + hinted F e → θna (e + hinted F e) = hinted F e := by
  intro h
  have h1 := h (critical F) (by linarith [hF.neg_le_hinted (critical F)])
  have h2 := h (critical F - 1) (by linarith [hF.neg_le_hinted (critical F - 1)])
  have h3 := hF.shift_eq_zero (e := critical F) le_rfl
  have h4 := hF.shift_eq_zero (e := critical F - 1) (by linarith)
  rw [h3] at h1
  rw [h4] at h2
  linarith

end

end GameFunction

/-- **Part 2.**  The hinted exponent of a game function has the abstract properties. -/
theorem GameFunction.hintShape {F : ℝ → ℝ} {E L : ℝ} (hF : GameFunction F E L) :
    ∃ ec, HintShape (hinted F) E ec :=
  ⟨critical F, hF.hintShape_critical⟩

/-- **The pair of a game function**: `HintPair θna R a h E` with `θna = R ∘ S⁻¹`,
`a = R(e_c) = -e_c`, `h = R(0)`. -/
theorem GameFunction.pair {F : ℝ → ℝ} {E L : ℝ} (hF : GameFunction F E L) :
    HintPair (partner (hinted F)) (hinted F) (hinted F (critical F)) (hinted F 0) E :=
  hF.hintShape_critical.pair

/-- **The level recursion of every game function reaches its hinted exponent.**  `θna` is any
function with `θna (e + R(e)) = R(e)` wherever the shift `e + R(e)` is positive. -/
theorem GameFunction.exactRec_reaches {F θna : ℝ → ℝ} {E L : ℝ} (hF : GameFunction F E L)
    (hfun : ∀ e, 0 < e + hinted F e → θna (e + hinted F e) = hinted F e)
    {g : ℝ} (hg : 0 < g) (hgE : g < E) {η : ℝ} (hη : 0 < η) :
    ∃ k, exactRec θna k g < hinted F g + η :=
  hF.hintShape_critical.exactRec_reaches'
    (fun e he => hfun e (hF.hintShape_critical.pos_after e he)) hg hgE hη

/-- **The level recursion of every game function converges to its hinted exponent**, at every
accuracy rate `g > 0`. -/
theorem GameFunction.exactRec_tendsto {F θna : ℝ → ℝ} {E L : ℝ} (hF : GameFunction F E L)
    (hfun : ∀ e, 0 < e + hinted F e → θna (e + hinted F e) = hinted F e) {g : ℝ} (hg : 0 < g) :
    Filter.Tendsto (fun k => exactRec θna k g) Filter.atTop (nhds (hinted F g)) :=
  hF.hintShape_critical.exactRec_tendsto
    (fun e he => hfun e (hF.hintShape_critical.pos_after e he)) hg

/-! ### Part 3: a witness -/

/-- The toy game function `t (1 - t)`; its hinted exponent is the `gaussHint` of the small-slope
limit (`hinted_toyGame_eq_gaussHint`). -/
def toyGame (t : ℝ) : ℝ := t * (1 - t)

/-- **Non-vacuity.**  `t (1 - t)` is a game function with `E = 1`, `L = 1`. -/
theorem toyGame_gameFunction : GameFunction toyGame 1 1 where
  cont := by unfold toyGame; fun_prop
  zero0 := by simp [toyGame]
  zero1 := by simp [toyGame]
  le_lin := fun t ht => by unfold toyGame; nlinarith [ht.1, ht.2]
  le_E := fun t ht => by unfold toyGame; nlinarith [ht.1, ht.2]
  E_sharp := fun e he => by
    have ht0 : 0 < min 1 ((1 - e) / 2) := lt_min one_pos (by linarith)
    have ht1 : min 1 ((1 - e) / 2) ≤ (1 - e) / 2 := min_le_right _ _
    refine ⟨min 1 ((1 - e) / 2), ⟨ht0, min_le_left _ _⟩, ?_⟩
    unfold toyGame
    nlinarith
  E_pos := one_pos

/-- The hinted exponent of the toy game function on `[-1, 1]`. -/
theorem hinted_toyGame {e : ℝ} (h1 : -1 ≤ e) (h2 : e ≤ 1) :
    hinted toyGame e = ((1 - e) / 2) ^ 2 := by
  apply le_antisymm
  · apply hinted_le
    intro t _
    unfold toyGame
    nlinarith [sq_nonneg (t - (1 - e) / 2)]
  · have h := toyGame_gameFunction.le_hinted (t := (1 - e) / 2) ⟨by linarith, by linarith⟩ e
    have h3 : toyGame ((1 - e) / 2) - (1 - e) / 2 * e = ((1 - e) / 2) ^ 2 := by
      unfold toyGame
      ring
    rw [← h3]
    exact h

/-- The hinted exponent of the toy game function is the `gaussHint` of `HintRecursion.lean`. -/
theorem hinted_toyGame_eq_gaussHint {e : ℝ} (h1 : -1 ≤ e) (h2 : e ≤ 1) :
    hinted toyGame e = gaussHint e := by
  rw [hinted_toyGame h1 h2]
  unfold gaussHint
  ring

/-- The critical accuracy of the toy game function. -/
theorem critical_toyGame : critical toyGame = -1 := by
  have hs := toyGame_gameFunction.hintShape_critical
  have h1 : -1 ≤ critical toyGame := toyGame_gameFunction.neg_L_le_critical
  have h2 := hs.ec_zero
  rw [hinted_toyGame h1 (by linarith [hs.ec_neg])] at h2
  nlinarith [sq_nonneg (1 + critical toyGame)]

/-- **Non-vacuity of Part 1.**  The toy hinted exponent has the abstract properties, with
`E = 1` and `ec = -1`. -/
theorem toyGame_hintShape : HintShape (hinted toyGame) 1 (-1) := by
  have h := toyGame_gameFunction.hintShape_critical
  rwa [critical_toyGame] at h

/-- Above `1` the toy hinted exponent vanishes (`gaussHint` does not). -/
theorem hinted_toyGame_of_one_le {e : ℝ} (h : 1 ≤ e) : hinted toyGame e = 0 :=
  (toyGame_hintShape.zero_iff e).mpr h

/-- Below `-1` the toy hinted exponent is `-e`. -/
theorem hinted_toyGame_of_le_neg_one {e : ℝ} (h : e ≤ -1) : hinted toyGame e = -e := by
  have h1 := toyGame_gameFunction.shift_eq_zero (e := e) (by rw [critical_toyGame]; exact h)
  linarith

/-- The partner of the toy hinted exponent is the `gaussNa` of `HintRecursion.lean`. -/
theorem partner_toyGame {x : ℝ} (hx : 0 < x) : partner (hinted toyGame) x = gaussNa x := by
  have hF := toyGame_gameFunction
  rcases le_total x 1 with h | h
  · have hs0 : 0 ≤ Real.sqrt x := Real.sqrt_nonneg x
    have hs1 : Real.sqrt x ≤ 1 := by
      calc Real.sqrt x ≤ Real.sqrt 1 := Real.sqrt_le_sqrt h
        _ = 1 := Real.sqrt_one
    have hsq : Real.sqrt x ^ 2 = x := Real.sq_sqrt hx.le
    have hval : hinted toyGame (2 * Real.sqrt x - 1) = (1 - Real.sqrt x) ^ 2 := by
      rw [hinted_toyGame (by linarith) (by linarith)]
      ring
    have hshift : 2 * Real.sqrt x - 1 + hinted toyGame (2 * Real.sqrt x - 1) = x := by
      rw [hval]
      linarith
    have hp := hF.partner_shift (e := 2 * Real.sqrt x - 1) (by rw [hshift]; exact hx)
    rw [hshift, hval] at hp
    rw [hp]
    unfold gaussNa
    rw [min_eq_left h]
  · rw [hF.hintShape_critical.partner_eq_zero h]
    unfold gaussNa
    rw [min_eq_right h, Real.sqrt_one]
    norm_num

/-- The pair of the toy game function has the constants `a = 1`, `h = 1/4`, `E = 1` of
`gaussPair`. -/
theorem toyGame_pair : HintPair (partner (hinted toyGame)) (hinted toyGame) 1 (1 / 4) 1 := by
  have ha : hinted toyGame (critical toyGame) = 1 := by
    rw [critical_toyGame, hinted_toyGame le_rfl (by norm_num)]
    norm_num
  have hh : hinted toyGame 0 = 1 / 4 := by
    rw [hinted_toyGame (by norm_num) (by norm_num)]
    norm_num
  have h := toyGame_gameFunction.pair
  rwa [ha, hh] at h

/-- **The theorems applied to the witness.**  The exact level recursion built on the
non-adaptive exponent `gaussNa` of the small-slope limit converges to the hinted exponent
`gaussHint` at every accuracy rate `0 < g ≤ 1`. -/
theorem gauss_exactRec_tendsto {g : ℝ} (hg : 0 < g) (hg1 : g ≤ 1) :
    Filter.Tendsto (fun k => exactRec gaussNa k g) Filter.atTop (nhds (gaussHint g)) := by
  rw [← hinted_toyGame_eq_gaussHint (by linarith) hg1]
  refine toyGame_gameFunction.exactRec_tendsto (fun e he => ?_) hg
  rw [← partner_toyGame he]
  exact toyGame_gameFunction.partner_shift he

end MetricChain.GamePair
