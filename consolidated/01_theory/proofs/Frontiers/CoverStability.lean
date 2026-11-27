import Mathlib

/-!
# Stability of covering numbers, and approximate nestedness of approximately super-additive families

Theory report §11.22 (limit shape of profile sets; workstream S, `docs/workstreams/S_REPORT.md`).

* `Covers`, `HasCover`: a covering problem with *position-dependent radii* and *internal
  centres*: a client is a pair `(p, g)` (a profile and a credit), a centre `a` covers it at
  accuracy `ε` if `L‖a − p‖ ≤ e·g + ε`, and centres must be first components of clients.
  `HasCover L e ε F k` says that `k` centres suffice — i.e. the covering number is at most `k`.
* `hasCover_of_close` (Lemma 11.70(b)): if every client of `F` is within `η` of a client of
  `F'` and conversely (distance `max(‖Δp‖, |Δg|)`), then a cover of `F` with `k` centres at
  accuracy `ε` yields one of `F'` with `k` centres at accuracy `ε + (2L + e)η`.
* `hasCover_sandwich`: the two-sided form `N(F', ε + (2L+e)η) ≤ N(F, ε) ≤ N(F', ε − (2L+e)η)`.
* `hasCover_upper_iff` (Lemma 11.70(a)): only the lower boundary matters — adding clients
  `(p, t)` with `t` above an existing client `(p, g)` does not change the covering problem.
* `hasCover_mono`: monotone in the accuracy and in the number of centres.
* `not_hasCover_shifted`, `hasCover_limit_point`: the two-point example in which the covering
  numbers of a convergent sequence do not converge at a jump of `ε ↦ N(F, ε)`
  (Lemma 11.70(d)), which is also the witness that the hypotheses are satisfiable and that
  a shift of the accuracy is necessary.
* `approx_multiple`, `approx_nested` (the quantitative step of Theorem 11.69, "Fekete's lemma
  for sets"): if a family of sets `Q M` is super-additive up to `β` (condition (C)), has
  increments bounded by `β'` (condition (E)) and is bounded by `R·M` (condition (B)), then
  every point of `Q m / m` is within `β/m + m(β' + R)/M` of `Q M / M` for all `M ≥ m ≥ 1`.

Not machine-checked: the existence of the Hausdorff limit and its convexity (a compactness
argument on top of `approx_nested`), and everything about lattice chains.
-/

namespace MetricChain.CoverStability

variable {V : Type*} [NormedAddCommGroup V]

/-- The centres `A` cover every client `(p, g) ∈ F` at accuracy `ε`: `L‖a − p‖ ≤ e·g + ε`. -/
def Covers (L e ε : ℝ) (A : Finset V) (F : Set (V × ℝ)) : Prop :=
  ∀ x ∈ F, ∃ a ∈ A, L * ‖a - x.1‖ ≤ e * x.2 + ε

/-- `k` internal centres (first components of clients) suffice at accuracy `ε`. -/
def HasCover (L e ε : ℝ) (F : Set (V × ℝ)) (k : ℕ) : Prop :=
  ∃ A : Finset V, (∀ a ∈ A, ∃ g : ℝ, (a, g) ∈ F) ∧ A.card ≤ k ∧ Covers L e ε A F

theorem hasCover_mono {L e ε ε' : ℝ} {F : Set (V × ℝ)} {k k' : ℕ} (hε : ε ≤ ε') (hk : k ≤ k')
    (h : HasCover L e ε F k) : HasCover L e ε' F k' := by
  obtain ⟨A, hA, hcard, hcov⟩ := h
  refine ⟨A, hA, hcard.trans hk, fun x hx => ?_⟩
  obtain ⟨a, ha, hle⟩ := hcov x hx
  exact ⟨a, ha, by linarith⟩

/-- **Lemma 11.70(b), one direction.**  Clients within `η` of each other in both directions:
a cover of `F` at accuracy `ε` gives a cover of `F'` with the same number of centres at
accuracy `ε + (2L + e)η`. -/
theorem hasCover_of_close {L e ε η : ℝ} (hL : 0 ≤ L) (he : 0 ≤ e) {F F' : Set (V × ℝ)}
    (h₁ : ∀ x ∈ F, ∃ y ∈ F', ‖y.1 - x.1‖ ≤ η ∧ |y.2 - x.2| ≤ η)
    (h₂ : ∀ y ∈ F', ∃ x ∈ F, ‖y.1 - x.1‖ ≤ η ∧ |y.2 - x.2| ≤ η)
    {k : ℕ} (h : HasCover L e ε F k) : HasCover L e (ε + (2 * L + e) * η) F' k := by
  classical
  obtain ⟨A, hA, hcard, hcov⟩ := h
  -- for every centre choose a client of `F'` near one of its own clients
  have hchoice : ∀ a ∈ A, ∃ a' : V, (∃ g' : ℝ, (a', g') ∈ F') ∧ ‖a' - a‖ ≤ η := by
    intro a ha
    obtain ⟨g, hg⟩ := hA a ha
    obtain ⟨y, hy, hy1, -⟩ := h₁ (a, g) hg
    exact ⟨y.1, ⟨y.2, hy⟩, hy1⟩
  choose! f hf using hchoice
  refine ⟨A.image f, ?_, (Finset.card_image_le).trans hcard, ?_⟩
  · intro a' ha'
    obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp ha'
    exact (hf a ha).1
  · intro y hy
    obtain ⟨x, hx, hx1, hx2⟩ := h₂ y hy
    obtain ⟨a, ha, hle⟩ := hcov x hx
    refine ⟨f a, Finset.mem_image_of_mem f ha, ?_⟩
    have hfa : ‖f a - a‖ ≤ η := (hf a ha).2
    have htri : ‖f a - y.1‖ ≤ ‖f a - a‖ + ‖a - x.1‖ + ‖y.1 - x.1‖ := by
      have h1 : f a - y.1 = (f a - a) + (a - x.1) - (y.1 - x.1) := by abel
      rw [h1]
      have h2 := norm_sub_le ((f a - a) + (a - x.1)) (y.1 - x.1)
      have h3 := norm_add_le (f a - a) (a - x.1)
      linarith
    have hg : x.2 ≤ y.2 + η := by
      have := (abs_le.mp hx2).1
      linarith
    have hmul : L * ‖f a - y.1‖ ≤ L * (η + ‖a - x.1‖ + η) :=
      mul_le_mul_of_nonneg_left (htri.trans (by linarith)) hL
    have heg : e * x.2 ≤ e * (y.2 + η) := mul_le_mul_of_nonneg_left hg he
    nlinarith [hmul, heg, hle]

/-- **Lemma 11.70(b), two-sided.**  `N(F', ε + (2L+e)η) ≤ N(F, ε) ≤ N(F', ε − (2L+e)η)`, stated
for the property "`k` centres suffice". -/
theorem hasCover_sandwich {L e ε η : ℝ} (hL : 0 ≤ L) (he : 0 ≤ e) {F F' : Set (V × ℝ)}
    (h₁ : ∀ x ∈ F, ∃ y ∈ F', ‖y.1 - x.1‖ ≤ η ∧ |y.2 - x.2| ≤ η)
    (h₂ : ∀ y ∈ F', ∃ x ∈ F, ‖y.1 - x.1‖ ≤ η ∧ |y.2 - x.2| ≤ η) (k : ℕ) :
    (HasCover L e ε F k → HasCover L e (ε + (2 * L + e) * η) F' k) ∧
      (HasCover L e (ε - (2 * L + e) * η) F' k → HasCover L e ε F k) := by
  refine ⟨hasCover_of_close hL he h₁ h₂, fun h => ?_⟩
  have h₁' : ∀ y ∈ F', ∃ x ∈ F, ‖x.1 - y.1‖ ≤ η ∧ |x.2 - y.2| ≤ η := by
    intro y hy
    obtain ⟨x, hx, hx1, hx2⟩ := h₂ y hy
    exact ⟨x, hx, by rwa [norm_sub_rev], by rwa [abs_sub_comm]⟩
  have h₂' : ∀ x ∈ F, ∃ y ∈ F', ‖x.1 - y.1‖ ≤ η ∧ |x.2 - y.2| ≤ η := by
    intro x hx
    obtain ⟨y, hy, hy1, hy2⟩ := h₁ x hx
    exact ⟨y, hy, by rwa [norm_sub_rev], by rwa [abs_sub_comm]⟩
  have := hasCover_of_close (ε := ε - (2 * L + e) * η) hL he h₁' h₂' h
  simpa using this

/-- The clients above the lower boundary: `(p, t)` with `t ≥ g` for some client `(p, g)`. -/
def upper {V : Type*} (F : Set (V × ℝ)) : Set (V × ℝ) := {x | ∃ g : ℝ, (x.1, g) ∈ F ∧ g ≤ x.2}

omit [NormedAddCommGroup V] in
theorem subset_upper (F : Set (V × ℝ)) : F ⊆ upper F := fun x hx => ⟨x.2, hx, le_rfl⟩

/-- **Lemma 11.70(a).**  Only the lower boundary matters. -/
theorem hasCover_upper_iff {L e ε : ℝ} (he : 0 ≤ e) {F : Set (V × ℝ)} {k : ℕ} :
    HasCover L e ε (upper F) k ↔ HasCover L e ε F k := by
  constructor
  · rintro ⟨A, hA, hcard, hcov⟩
    refine ⟨A, fun a ha => ?_, hcard, fun x hx => hcov x (subset_upper F hx)⟩
    obtain ⟨t, g, hg, -⟩ := hA a ha
    exact ⟨g, hg⟩
  · rintro ⟨A, hA, hcard, hcov⟩
    refine ⟨A, fun a ha => ?_, hcard, ?_⟩
    · obtain ⟨g, hg⟩ := hA a ha
      exact ⟨g, subset_upper F hg⟩
    · rintro x ⟨g, hg, hgx⟩
      obtain ⟨a, ha, hle⟩ := hcov (x.1, g) hg
      refine ⟨a, ha, ?_⟩
      have : e * g ≤ e * x.2 := mul_le_mul_of_nonneg_left hgx he
      simpa using hle.trans (by linarith)

/-! ### The two-point example: no convergence at a jump -/

/-- The limit set: two clients at distance exactly `1`, no credit. -/
def twoPoints (t : ℝ) : Set (ℝ × ℝ) := {((0 : ℝ), (0 : ℝ)), (t, (0 : ℝ))}

/-- At `L = e = ε = 1` one centre covers `{(0,0), (1,0)}` … -/
theorem hasCover_limit_point : HasCover (1 : ℝ) 1 1 (twoPoints 1) 1 := by
  refine ⟨{(0 : ℝ)}, ?_, by simp, ?_⟩
  · intro a ha
    rw [Finset.mem_singleton] at ha
    exact ⟨0, by rw [ha]; left; rfl⟩
  · intro x hx
    refine ⟨0, Finset.mem_singleton_self _, ?_⟩
    rcases hx with rfl | rfl <;> norm_num

/-- … but no single centre covers `{(0,0), (1+δ,0)}` for any `δ > 0`: the covering numbers
of the sets `{(0,0), (1 + 1/N, 0)}`, which converge to `{(0,0), (1,0)}`, stay at `2`. -/
theorem not_hasCover_shifted {δ : ℝ} (hδ : 0 < δ) :
    ¬ HasCover (1 : ℝ) 1 1 (twoPoints (1 + δ)) 1 := by
  rintro ⟨A, hA, hcard, hcov⟩
  obtain ⟨a, ha, h0⟩ := hcov ((0 : ℝ), (0 : ℝ)) (by left; rfl)
  obtain ⟨b, hb, h1⟩ := hcov (1 + δ, (0 : ℝ)) (by right; rfl)
  have hab : a = b := Finset.card_le_one.mp hcard a ha b hb
  subst hab
  obtain ⟨g, hg⟩ := hA a ha
  simp only [one_mul, mul_zero, zero_add, sub_zero, Real.norm_eq_abs] at h0 h1
  have ha0 := abs_le.mp h0
  have ha1 := abs_le.mp h1
  rcases hg with hg | hg
  · have : a = 0 := (Prod.mk.inj hg).1
    subst this
    linarith [ha1.1]
  · have : a = 1 + δ := (Prod.mk.inj hg).1
    subst this
    linarith [ha0.2]

/-- Non-vacuity of `hasCover_of_close` on the same example: the sets `{(0,0), (1,0)}` and
`{(0,0), (1+δ,0)}` are within `δ` of each other, so one centre covers the second at the
accuracy `1 + 3δ` — while by `not_hasCover_shifted` it does not at the accuracy `1`: some
shift of the accuracy is necessary. -/
theorem hasCover_shifted_of_close {δ : ℝ} (hδ : 0 ≤ δ) :
    HasCover (1 : ℝ) 1 (1 + (2 * 1 + 1) * δ) (twoPoints (1 + δ)) 1 := by
  refine hasCover_of_close (by norm_num) (by norm_num) ?_ ?_ hasCover_limit_point
  · intro x hx
    rcases hx with rfl | rfl
    · exact ⟨((0 : ℝ), (0 : ℝ)), by left; rfl, by simpa using hδ, by simpa using hδ⟩
    · refine ⟨(1 + δ, (0 : ℝ)), by right; rfl, ?_, by simpa using hδ⟩
      simp [abs_of_nonneg hδ]
  · intro y hy
    rcases hy with rfl | rfl
    · exact ⟨((0 : ℝ), (0 : ℝ)), by left; rfl, by simpa using hδ, by simpa using hδ⟩
    · refine ⟨((1 : ℝ), (0 : ℝ)), by right; rfl, ?_, by simpa using hδ⟩
      simp [abs_of_nonneg hδ]

/-! ### Approximate nestedness (the quantitative step of Fekete's lemma for sets) -/

section Fekete

variable {W : Type*} [NormedAddCommGroup W]

/-- From (E): `r` further steps move a point by at most `r β'`. -/
theorem approx_extend {Q : ℕ → Set W} {β' : ℝ}
    (hE : ∀ M : ℕ, ∀ q ∈ Q M, ∃ q' ∈ Q (M + 1), ‖q' - q‖ ≤ β')
    {M : ℕ} {p : W} (hp : p ∈ Q M) (r : ℕ) : ∃ p' ∈ Q (M + r), ‖p' - p‖ ≤ r * β' := by
  induction r with
  | zero => exact ⟨p, by simpa using hp, by simp⟩
  | succ r ih =>
    obtain ⟨p₁, hp₁, hn₁⟩ := ih
    obtain ⟨p₂, hp₂, hn₂⟩ := hE _ p₁ hp₁
    refine ⟨p₂, by simpa [add_assoc] using hp₂, ?_⟩
    have : p₂ - p = (p₂ - p₁) + (p₁ - p) := by abel
    rw [this]
    calc ‖(p₂ - p₁) + (p₁ - p)‖ ≤ ‖p₂ - p₁‖ + ‖p₁ - p‖ := norm_add_le _ _
      _ ≤ β' + r * β' := add_le_add hn₂ hn₁
      _ = ((r + 1 : ℕ) : ℝ) * β' := by push_cast; ring

variable [NormedSpace ℝ W]

/-- From (C): `k` copies of a point of `Q m` are within `(k − 1)β` of a point of `Q (k m)`. -/
theorem approx_multiple {Q : ℕ → Set W} {β : ℝ}
    (hC : ∀ M₁ M₂ : ℕ, ∀ q₁ ∈ Q M₁, ∀ q₂ ∈ Q M₂, ∃ q ∈ Q (M₁ + M₂), ‖q - q₁ - q₂‖ ≤ β)
    {m : ℕ} {q : W} (hq : q ∈ Q m) (k : ℕ) :
    ∃ p ∈ Q ((k + 1) * m), ‖p - ((k : ℝ) + 1) • q‖ ≤ k * β := by
  induction k with
  | zero => exact ⟨q, by simpa using hq, by simp⟩
  | succ k ih =>
    obtain ⟨p, hp, hpn⟩ := ih
    obtain ⟨p', hp', hpn'⟩ := hC _ _ p hp q hq
    have hidx : (k + 1 + 1) * m = (k + 1) * m + m := by ring
    refine ⟨p', by rw [hidx]; exact hp', ?_⟩
    have hsplit : p' - (((k + 1 : ℕ) : ℝ) + 1) • q = (p' - p - q) + (p - ((k : ℝ) + 1) • q) := by
      push_cast
      rw [add_smul ((k : ℝ) + 1) 1 q, one_smul]
      abel
    rw [hsplit]
    calc ‖(p' - p - q) + (p - ((k : ℝ) + 1) • q)‖ ≤ ‖p' - p - q‖ + ‖p - ((k : ℝ) + 1) • q‖ := norm_add_le _ _
      _ ≤ β + k * β := add_le_add hpn' hpn
      _ = ((k + 1 : ℕ) : ℝ) * β := by push_cast; ring

/-- **Approximate nestedness** (step (ii) of the proof of Theorem 11.69).  Under (C), (E), (B),
for `M = (k+1)·m + r` with `r < m`: every point `q/m` of `Q m / m` is within
`β/m + m(β' + R)/M` of the point `p/M` of `Q M / M` constructed from it. -/
theorem approx_nested {Q : ℕ → Set W} {β β' R : ℝ} (hβ : 0 ≤ β) (hβ' : 0 ≤ β') (hR : 0 ≤ R)
    (hC : ∀ M₁ M₂ : ℕ, ∀ q₁ ∈ Q M₁, ∀ q₂ ∈ Q M₂, ∃ q ∈ Q (M₁ + M₂), ‖q - q₁ - q₂‖ ≤ β)
    (hE : ∀ M : ℕ, ∀ q ∈ Q M, ∃ q' ∈ Q (M + 1), ‖q' - q‖ ≤ β')
    (hB : ∀ M : ℕ, ∀ q ∈ Q M, ‖q‖ ≤ R * M)
    {m : ℕ} (hm : 0 < m) {q : W} (hq : q ∈ Q m) (k r : ℕ) (hr : r < m) :
    ∃ p ∈ Q ((k + 1) * m + r),
      ‖(1 / (((k + 1) * m + r : ℕ) : ℝ)) • p - (1 / (m : ℝ)) • q‖
        ≤ β / m + m * (β' + R) / (((k + 1) * m + r : ℕ) : ℝ) := by
  obtain ⟨p₁, hp₁, hn₁⟩ := approx_multiple hC hq k
  obtain ⟨p, hp, hn⟩ := approx_extend hE hp₁ r
  refine ⟨p, hp, ?_⟩
  set M : ℝ := (((k + 1) * m + r : ℕ) : ℝ) with hMdef
  have hmR : (0 : ℝ) < m := by exact_mod_cast hm
  have hMval : M = ((k : ℝ) + 1) * m + r := by rw [hMdef]; push_cast; ring
  have hMpos : 0 < M := by rw [hMval]; positivity
  have hMm : (m : ℝ) ≤ M := by
    rw [hMval]
    have : (0 : ℝ) ≤ (k : ℝ) * m + r := by positivity
    nlinarith
  have hrm : (r : ℝ) ≤ m := by exact_mod_cast hr.le
  -- decomposition: p/M − q/m = (p − (k+1) q)/M − (r/(M m)) q
  have hdecomp : (1 / M) • p - (1 / (m : ℝ)) • q
      = (1 / M) • (p - ((k : ℝ) + 1) • q) - (r / (M * m)) • q := by
    have hcoef : (1 / M) * ((k : ℝ) + 1) + r / (M * m) = 1 / m := by
      rw [hMval]
      field_simp
    rw [smul_sub, smul_smul, sub_sub, ← add_smul, hcoef]
  rw [hdecomp]
  have hq_norm : ‖q‖ ≤ R * m := hB m q hq
  have h1 : ‖p - ((k : ℝ) + 1) • q‖ ≤ k * β + r * β' := by
    have : p - ((k : ℝ) + 1) • q = (p - p₁) + (p₁ - ((k : ℝ) + 1) • q) := by abel
    rw [this]
    exact (norm_add_le _ _).trans (by linarith)
  have hA : ‖(1 / M) • (p - ((k : ℝ) + 1) • q)‖ ≤ (k * β + r * β') / M := by
    rw [norm_smul, Real.norm_of_nonneg (by positivity), one_div, inv_mul_eq_div]
    exact div_le_div_of_nonneg_right h1 hMpos.le
  have hBd : ‖(r / (M * m)) • q‖ ≤ r * R / M := by
    rw [norm_smul, Real.norm_of_nonneg (by positivity)]
    calc r / (M * m) * ‖q‖ ≤ r / (M * m) * (R * m) :=
          mul_le_mul_of_nonneg_left hq_norm (by positivity)
      _ = r * R / M := by field_simp
  have hkβ : (k : ℝ) * β / M ≤ β / m := by
    rw [div_le_div_iff₀ hMpos hmR]
    have : (k : ℝ) * m ≤ M := by rw [hMval]; nlinarith [show (0 : ℝ) ≤ (r : ℝ) by positivity]
    nlinarith
  calc ‖(1 / M) • (p - ((k : ℝ) + 1) • q) - (r / (M * m)) • q‖
      ≤ ‖(1 / M) • (p - ((k : ℝ) + 1) • q)‖ + ‖(r / (M * m)) • q‖ := norm_sub_le _ _
    _ ≤ (k * β + r * β') / M + r * R / M := add_le_add hA hBd
    _ = k * β / M + r * (β' + R) / M := by ring
    _ ≤ β / m + m * (β' + R) / M := by
        refine add_le_add hkβ ?_
        exact div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_right hrm (by linarith)) hMpos.le

/-- Non-vacuity of `approx_nested`: the family `Q M = {M}` on the line satisfies (C) with
`β = 0`, (E) with `β' = 1` and (B) with `R = 1`. -/
theorem approx_nested_example (m : ℕ) (hm : 0 < m) (k r : ℕ) (hr : r < m) :
    ∃ p ∈ ({(((k + 1) * m + r : ℕ) : ℝ)} : Set ℝ),
      ‖(1 / (((k + 1) * m + r : ℕ) : ℝ)) • p - (1 / (m : ℝ)) • (m : ℝ)‖
        ≤ 0 / m + m * (1 + 1) / (((k + 1) * m + r : ℕ) : ℝ) := by
  have h := approx_nested (Q := fun M : ℕ => ({(M : ℝ)} : Set ℝ)) (β := 0) (β' := 1) (R := 1)
    le_rfl zero_le_one zero_le_one
    (by
      intro M₁ M₂ q₁ hq₁ q₂ hq₂
      rw [Set.mem_singleton_iff] at hq₁ hq₂
      exact ⟨((M₁ + M₂ : ℕ) : ℝ), rfl, by rw [hq₁, hq₂]; push_cast; simp⟩)
    (by
      intro M q hq
      rw [Set.mem_singleton_iff] at hq
      exact ⟨((M + 1 : ℕ) : ℝ), rfl, by rw [hq]; push_cast; simp⟩)
    (by
      intro M q hq
      rw [Set.mem_singleton_iff] at hq
      rw [hq]; simp)
    hm (q := (m : ℝ)) rfl k r hr
  exact h

end Fekete

end MetricChain.CoverStability
