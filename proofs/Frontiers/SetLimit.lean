import proofs.Frontiers.CoverStability

/-!
# Fekete's lemma for sets: Hausdorff limits of approximately super-additive families

Theory report §11.22, Theorem 11.69 (abstract part) and Theorem 11.71(a) (abstract form);
workstream S, `docs/workstreams/S_REPORT.md`, Lemma 3.3.

* `lowerLimit E`: the points approached by all sets `E M`.
* `ApproxNested E c`: every point of `E m` is within `c/m + c·m/M` of `E M` (`M ≥ m ≥ 1`).
* `hausdorff_limit`: for a bounded, approximately nested sequence of non-empty sets in a
  proper normed space the lower limit `K` is compact and non-empty, eventually every point
  of `E M` is within `ε` of `K`, and eventually every point of `K` is within `ε` of `E M` —
  Hausdorff convergence.  (Every cluster point of points `y_i ∈ E (φ i)`, `φ i → ∞`, lies in
  the lower limit: `mem_lowerLimit_of_tendsto`.)
* `SuperAdditive Q β β' R`: conditions (C), (E), (B) of the theorem — `Q` is super-additive
  up to `β`, has increments at most `β'`, and is bounded by `R·M`.
  `SuperAdditive.approxNested`: then the normalised sets `scaled Q M = Q M / M` are
  approximately nested with `c = β + β' + R` (from `CoverStability.approx_nested`).
* `SuperAdditive.hausdorff_limit`: **the normalised sets converge**.
* `SuperAdditive.dist_limit_le`: **the one-sided rate** — every point of `Q M / M` is within
  `β/M` of the limit.
* `SuperAdditive.convex_limit`: **the limit is convex** (`SuperAdditive.combination`: `a`
  copies of one point and `b` copies of another are within `(a+b)β` of `Q ((a+b)m)`).
* `SuperAdditive.cover_sandwich`: for client sets in `V × ℝ` (a profile and a credit), the
  covering numbers of `Q M / M` are, for all large `M`, sandwiched by those of the limit at
  accuracies shifted by `(2L + e)η` — the abstract form of "the certificate sizes converge
  to the covering number of the limit shape".
* `superAdditive_example`, `one_mem_limit_example`: a witness.

What is *not* here: that the sets of (profile, number of gauche torsions) of lattice
bridges satisfy `SuperAdditive` (Lemma 11.68 of the theory report, a paper proof checked
numerically), and everything else about lattice chains.
-/

namespace MetricChain.SetLimit

open Filter Topology

variable {W : Type*} [NormedAddCommGroup W]

/-- The lower limit of a sequence of sets: the points that are approached by *all* `E M`. -/
def lowerLimit (E : ℕ → Set W) : Set W :=
  {x | ∀ ε > 0, ∀ᶠ M in atTop, ∃ y ∈ E M, ‖y - x‖ ≤ ε}

/-- Approximate nestedness: every point of `E m` is within `c/m + c·m/M` of `E M`. -/
def ApproxNested (E : ℕ → Set W) (c : ℝ) : Prop :=
  ∀ m M : ℕ, 1 ≤ m → m ≤ M → ∀ x ∈ E m, ∃ y ∈ E M, ‖y - x‖ ≤ c / m + c * m / M

theorem isClosed_lowerLimit (E : ℕ → Set W) : IsClosed (lowerLimit E) := by
  refine IsSeqClosed.isClosed fun x a hx ha => ?_
  intro ε hε
  have h2 : ∀ᶠ n in atTop, ‖x n - a‖ < ε / 2 := by
    have := (tendsto_iff_norm_sub_tendsto_zero.mp ha)
    exact this.eventually (gt_mem_nhds (by linarith))
  obtain ⟨n, hn⟩ := h2.exists
  filter_upwards [hx n (ε / 2) (by linarith)] with M hM
  obtain ⟨y, hy, hyx⟩ := hM
  refine ⟨y, hy, ?_⟩
  calc ‖y - a‖ = ‖(y - x n) + (x n - a)‖ := by congr 1; abel
    _ ≤ ‖y - x n‖ + ‖x n - a‖ := norm_add_le _ _
    _ ≤ ε := by linarith

theorem norm_le_of_mem_lowerLimit {E : ℕ → Set W} {R : ℝ} (hB : ∀ M, ∀ x ∈ E M, ‖x‖ ≤ R)
    {x : W} (hx : x ∈ lowerLimit E) : ‖x‖ ≤ R := by
  refine le_of_forall_pos_le_add fun ε hε => ?_
  obtain ⟨M, y, hy, hyx⟩ := (hx ε hε).exists
  calc ‖x‖ = ‖y - (y - x)‖ := by congr 1; abel
    _ ≤ ‖y‖ + ‖y - x‖ := norm_sub_le _ _
    _ ≤ R + ε := add_le_add (hB M y hy) hyx

/-- Every cluster point of points `y i ∈ E (φ i)` with `φ i → ∞` lies in the lower limit. -/
theorem mem_lowerLimit_of_tendsto {E : ℕ → Set W} {c : ℝ} (hN : ApproxNested E c)
    {φ : ℕ → ℕ} (hφ : Tendsto φ atTop atTop) {y : ℕ → W} (hy : ∀ i, y i ∈ E (φ i))
    {a : W} (ha : Tendsto y atTop (𝓝 a)) : a ∈ lowerLimit E := by
  intro ε hε
  have h1 : ∀ᶠ i in atTop, ‖y i - a‖ < ε / 3 :=
    (tendsto_iff_norm_sub_tendsto_zero.mp ha).eventually (gt_mem_nhds (by linarith))
  have h2 : ∀ᶠ i in atTop, 1 ≤ φ i ∧ c / (φ i : ℝ) ≤ ε / 3 := by
    have hlarge : ∀ᶠ i in atTop, (max 1 (Nat.ceil (3 * c / ε))) ≤ φ i :=
      hφ.eventually (eventually_ge_atTop _)
    filter_upwards [hlarge] with i hi
    have h1φ : 1 ≤ φ i := le_trans (le_max_left _ _) hi
    have hpos : (0 : ℝ) < φ i := by exact_mod_cast h1φ
    refine ⟨h1φ, ?_⟩
    have hge : 3 * c / ε ≤ (φ i : ℝ) :=
      (Nat.le_ceil _).trans (by exact_mod_cast le_trans (le_max_right _ _) hi)
    rw [div_le_iff₀ hpos]
    have := (div_le_iff₀ hε).mp hge
    nlinarith
  obtain ⟨i, hi1, hi2, hi3⟩ := (h1.and h2).exists
  have hpos : (0 : ℝ) < φ i := by exact_mod_cast hi2
  refine eventually_atTop.mpr ⟨max (φ i) (Nat.ceil (3 * c * φ i / ε) + 1), fun M hM => ?_⟩
  have hMφ : φ i ≤ M := le_trans (le_max_left _ _) hM
  have hMpos : (0 : ℝ) < M := lt_of_lt_of_le hpos (by exact_mod_cast hMφ)
  obtain ⟨z, hz, hzy⟩ := hN (φ i) M hi2 hMφ (y i) (hy i)
  refine ⟨z, hz, ?_⟩
  have hM2 : 3 * c * φ i / ε ≤ (M : ℝ) := by
    have h := le_trans (le_max_right _ _) hM
    have h' : (Nat.ceil (3 * c * φ i / ε) : ℝ) ≤ M := by exact_mod_cast (Nat.le_succ _).trans h
    exact (Nat.le_ceil _).trans h'
  have hterm : c * φ i / M ≤ ε / 3 := by
    rw [div_le_iff₀ hMpos]
    have := (div_le_iff₀ hε).mp hM2
    nlinarith
  calc ‖z - a‖ = ‖(z - y i) + (y i - a)‖ := by congr 1; abel
    _ ≤ ‖z - y i‖ + ‖y i - a‖ := norm_add_le _ _
    _ ≤ (c / φ i + c * φ i / M) + ε / 3 := add_le_add hzy hi1.le
    _ ≤ ε := by linarith

/-- **Hausdorff convergence of an approximately nested, bounded sequence of non-empty sets**
(the limit statement of "Fekete's lemma for sets", theory report Theorem 11.69): the lower
limit is compact and non-empty, eventually every point of `E M` is within `ε` of it, and
eventually every point of it is within `ε` of `E M`. -/
theorem hausdorff_limit [ProperSpace W] {E : ℕ → Set W} {c R : ℝ}
    (hne : ∀ M, 1 ≤ M → (E M).Nonempty) (hB : ∀ M, ∀ x ∈ E M, ‖x‖ ≤ R)
    (hN : ApproxNested E c) :
    IsCompact (lowerLimit E) ∧ (lowerLimit E).Nonempty ∧
      (∀ ε > 0, ∀ᶠ M in atTop, ∀ x ∈ E M, ∃ z ∈ lowerLimit E, ‖x - z‖ ≤ ε) ∧
      (∀ ε > 0, ∀ᶠ M in atTop, ∀ z ∈ lowerLimit E, ∃ y ∈ E M, ‖y - z‖ ≤ ε) := by
  have hball : IsCompact (Metric.closedBall (0 : W) R) := isCompact_closedBall 0 R
  have hcompact : IsCompact (lowerLimit E) :=
    hball.of_isClosed_subset (isClosed_lowerLimit E)
      (fun x hx => mem_closedBall_zero_iff.mpr (norm_le_of_mem_lowerLimit hB hx))
  -- a sequence of points of `E (i+1)` and a convergent subsequence
  have hne' : ∀ i : ℕ, ∃ y, y ∈ E (i + 1) := fun i => hne (i + 1) (Nat.le_add_left 1 i)
  choose y0 hy0 using hne'
  obtain ⟨a0, -, ψ0, hψ0, ha0⟩ := hball.tendsto_subseq
    (fun i => mem_closedBall_zero_iff.mpr (hB (i + 1) (y0 i) (hy0 i)))
  have hnonempty : (lowerLimit E).Nonempty :=
    ⟨a0, mem_lowerLimit_of_tendsto hN (φ := fun i => ψ0 i + 1)
      (tendsto_atTop_mono (fun i => Nat.le_succ _) hψ0.tendsto_atTop) (fun i => hy0 (ψ0 i)) ha0⟩
  refine ⟨hcompact, hnonempty, ?_, ?_⟩
  · -- eventually `E M` is inside the `ε`-neighbourhood of the limit
    intro ε hε
    by_contra hcon
    have hfreq : ∃ᶠ M in atTop, ∃ x ∈ E M, ∀ z ∈ lowerLimit E, ε < ‖x - z‖ := by
      refine (not_eventually.mp hcon).mono fun M hM => ?_
      push Not at hM
      exact hM
    obtain ⟨φ, hφ, hφbad⟩ := extraction_of_frequently_atTop hfreq
    choose x hx hxbad using hφbad
    obtain ⟨a, -, ψ, hψ, ha⟩ := hball.tendsto_subseq
      (fun i => mem_closedBall_zero_iff.mpr (hB (φ i) (x i) (hx i)))
    have haK : a ∈ lowerLimit E :=
      mem_lowerLimit_of_tendsto hN (φ := fun i => φ (ψ i))
        (hφ.tendsto_atTop.comp hψ.tendsto_atTop) (fun i => hx (ψ i)) ha
    have hclose : ∀ᶠ i in atTop, ‖x (ψ i) - a‖ < ε :=
      (tendsto_iff_norm_sub_tendsto_zero.mp ha).eventually (gt_mem_nhds hε)
    obtain ⟨i, hi⟩ := hclose.exists
    exact absurd hi (not_lt.mpr (hxbad (ψ i) a haK).le)
  · -- eventually the limit is inside the `ε`-neighbourhood of `E M`, uniformly
    intro ε hε
    obtain ⟨t, htK, htfin, hcover⟩ := finite_cover_balls_of_compact hcompact (half_pos hε)
    have hall : ∀ᶠ M in atTop, ∀ z ∈ t, ∃ y ∈ E M, ‖y - z‖ ≤ ε / 2 :=
      (eventually_all_finite htfin).mpr fun z hz => htK hz (ε / 2) (half_pos hε)
    filter_upwards [hall] with M hM z hz
    obtain ⟨w, hw, hzw⟩ := Set.mem_iUnion₂.mp (hcover hz)
    obtain ⟨y, hy, hyw⟩ := hM w hw
    refine ⟨y, hy, ?_⟩
    have hzw' : ‖w - z‖ < ε / 2 := by
      rw [← dist_eq_norm, dist_comm]; exact Metric.mem_ball.mp hzw
    calc ‖y - z‖ = ‖(y - w) + (w - z)‖ := by congr 1; abel
      _ ≤ ‖y - w‖ + ‖w - z‖ := norm_add_le _ _
      _ ≤ ε := by linarith

/-! ### Fekete's lemma for sets -/

section Fekete

open MetricChain.CoverStability

variable [NormedSpace ℝ W]

/-- The normalised sets `Q M / M`. -/
def scaled (Q : ℕ → Set W) (M : ℕ) : Set W := {w | ∃ q ∈ Q M, w = (1 / (M : ℝ)) • q}

/-- Conditions (C), (E), (B) of Theorem 11.69: super-additive up to `β`, increments at most
`β'`, bounded by `R·M`. -/
structure SuperAdditive (Q : ℕ → Set W) (β β' R : ℝ) : Prop where
  β_nonneg : 0 ≤ β
  β'_nonneg : 0 ≤ β'
  R_nonneg : 0 ≤ R
  add : ∀ M₁ M₂ : ℕ, ∀ q₁ ∈ Q M₁, ∀ q₂ ∈ Q M₂, ∃ q ∈ Q (M₁ + M₂), ‖q - q₁ - q₂‖ ≤ β
  succ : ∀ M : ℕ, ∀ q ∈ Q M, ∃ q' ∈ Q (M + 1), ‖q' - q‖ ≤ β'
  bound : ∀ M : ℕ, ∀ q ∈ Q M, ‖q‖ ≤ R * M

theorem SuperAdditive.norm_scaled_le {Q : ℕ → Set W} {β β' R : ℝ} (h : SuperAdditive Q β β' R)
    (M : ℕ) {w : W} (hw : w ∈ scaled Q M) : ‖w‖ ≤ R := by
  obtain ⟨q, hq, rfl⟩ := hw
  rcases Nat.eq_zero_or_pos M with rfl | hM
  · simpa using h.R_nonneg
  · have hMR : (0 : ℝ) < M := by exact_mod_cast hM
    rw [norm_smul, Real.norm_of_nonneg (by positivity), one_div, inv_mul_le_iff₀ hMR]
    simpa [mul_comm] using h.bound M q hq

/-- (C), (E), (B) imply approximate nestedness of the normalised sets, with `c = β + β' + R`. -/
theorem SuperAdditive.approxNested {Q : ℕ → Set W} {β β' R : ℝ} (h : SuperAdditive Q β β' R) :
    ApproxNested (scaled Q) (β + β' + R) := by
  intro m M hm hmM x hx
  obtain ⟨q, hq, rfl⟩ := hx
  have hdiv : 1 ≤ M / m := (Nat.one_le_div_iff hm).mpr hmM
  obtain ⟨k, hk⟩ : ∃ k, M / m = k + 1 := ⟨M / m - 1, (Nat.sub_add_cancel hdiv).symm⟩
  have hM : (k + 1) * m + M % m = M := by rw [← hk, mul_comm]; exact Nat.div_add_mod M m
  obtain ⟨p, hp, hpn⟩ := approx_nested h.β_nonneg h.β'_nonneg h.R_nonneg h.add h.succ h.bound
    hm hq k (M % m) (Nat.mod_lt M hm)
  rw [hM] at hp hpn
  refine ⟨(1 / (M : ℝ)) • p, ⟨p, hp, rfl⟩, hpn.trans ?_⟩
  have hmR : (0 : ℝ) < m := by exact_mod_cast hm
  have hMR : (0 : ℝ) < M := lt_of_lt_of_le hmR (by exact_mod_cast hmM)
  have h1 : β / m ≤ (β + β' + R) / m :=
    div_le_div_of_nonneg_right (by linarith [h.β'_nonneg, h.R_nonneg]) hmR.le
  have h2 : m * (β' + R) / M ≤ (β + β' + R) * m / M := by
    apply div_le_div_of_nonneg_right _ hMR.le
    nlinarith [h.β_nonneg]
  linarith

/-- `a` copies of `q₁` and `b` copies of `q₂` (both in `Q m`, `a + b ≥ 1`) are within
`(a + b − 1)β` of a point of `Q ((a + b) m)`. -/
theorem SuperAdditive.combination {Q : ℕ → Set W} {β β' R : ℝ} (h : SuperAdditive Q β β' R)
    {m : ℕ} {q₁ q₂ : W} (hq₁ : q₁ ∈ Q m) (hq₂ : q₂ ∈ Q m) (a b : ℕ) (hab : 1 ≤ a + b) :
    ∃ p ∈ Q ((a + b) * m), ‖p - (a : ℝ) • q₁ - (b : ℝ) • q₂‖ ≤ ((a + b : ℕ) : ℝ) * β := by
  rcases Nat.eq_zero_or_pos a with rfl | ha
  · obtain ⟨k, rfl⟩ : ∃ k, b = k + 1 := ⟨b - 1, by omega⟩
    obtain ⟨p, hp, hpn⟩ := approx_multiple h.add hq₂ k
    refine ⟨p, by simpa using hp, ?_⟩
    have : p - ((0 : ℕ) : ℝ) • q₁ - ((k + 1 : ℕ) : ℝ) • q₂ = p - ((k : ℝ) + 1) • q₂ := by
      push_cast; simp
    rw [this]
    refine hpn.trans ?_
    push_cast
    nlinarith [h.β_nonneg]
  · obtain ⟨j, rfl⟩ : ∃ j, a = j + 1 := ⟨a - 1, by omega⟩
    obtain ⟨p₁, hp₁, hpn₁⟩ := approx_multiple h.add hq₁ j
    rcases Nat.eq_zero_or_pos b with rfl | hb
    · refine ⟨p₁, by simpa using hp₁, ?_⟩
      have : p₁ - ((j + 1 : ℕ) : ℝ) • q₁ - ((0 : ℕ) : ℝ) • q₂ = p₁ - ((j : ℝ) + 1) • q₁ := by
        push_cast; simp
      rw [this]
      refine hpn₁.trans ?_
      push_cast
      nlinarith [h.β_nonneg]
    · obtain ⟨k, rfl⟩ : ∃ k, b = k + 1 := ⟨b - 1, by omega⟩
      obtain ⟨p₂, hp₂, hpn₂⟩ := approx_multiple h.add hq₂ k
      obtain ⟨p, hp, hpn⟩ := h.add _ _ p₁ hp₁ p₂ hp₂
      have hidx : (j + 1) * m + (k + 1) * m = (j + 1 + (k + 1)) * m := by ring
      refine ⟨p, by rw [← hidx]; exact hp, ?_⟩
      have hsplit : p - ((j + 1 : ℕ) : ℝ) • q₁ - ((k + 1 : ℕ) : ℝ) • q₂
          = (p - p₁ - p₂) + (p₁ - ((j : ℝ) + 1) • q₁) + (p₂ - ((k : ℝ) + 1) • q₂) := by
        push_cast; abel
      rw [hsplit]
      have h3 := norm_add₃_le (a := p - p₁ - p₂) (b := p₁ - ((j : ℝ) + 1) • q₁)
        (c := p₂ - ((k : ℝ) + 1) • q₂)
      push_cast
      nlinarith [h.β_nonneg]

/-- **Fekete's lemma for sets** (theory report, Theorem 11.69, abstract part).  If `Q` is
super-additive up to `β`, has bounded increments and is bounded by `R·M`, and `Q M` is
non-empty for `M ≥ 1`, then the normalised sets `Q M / M` converge in the Hausdorff sense to
the compact non-empty set `K = lowerLimit (scaled Q)`. -/
theorem SuperAdditive.hausdorff_limit [ProperSpace W] {Q : ℕ → Set W} {β β' R : ℝ}
    (h : SuperAdditive Q β β' R) (hne : ∀ M, 1 ≤ M → (Q M).Nonempty) :
    IsCompact (lowerLimit (scaled Q)) ∧ (lowerLimit (scaled Q)).Nonempty ∧
      (∀ ε > 0, ∀ᶠ M in atTop, ∀ x ∈ scaled Q M, ∃ z ∈ lowerLimit (scaled Q), ‖x - z‖ ≤ ε) ∧
      (∀ ε > 0, ∀ᶠ M in atTop, ∀ z ∈ lowerLimit (scaled Q), ∃ y ∈ scaled Q M, ‖y - z‖ ≤ ε) :=
  MetricChain.SetLimit.hausdorff_limit
    (fun M hM => by obtain ⟨q, hq⟩ := hne M hM; exact ⟨_, q, hq, rfl⟩)
    (fun M _ hx => h.norm_scaled_le M hx) h.approxNested

/-- **The one-sided rate**: every point of `Q M / M` is within `β/M` of the limit. -/
theorem SuperAdditive.dist_limit_le [ProperSpace W] {Q : ℕ → Set W} {β β' R : ℝ}
    (h : SuperAdditive Q β β' R) {M : ℕ} (hM : 1 ≤ M) {x : W} (hx : x ∈ scaled Q M) :
    ∃ z ∈ lowerLimit (scaled Q), ‖z - x‖ ≤ β / M := by
  obtain ⟨q, hq, rfl⟩ := hx
  have hMR : (0 : ℝ) < M := by exact_mod_cast hM
  -- the points p_k / ((k+1) M)
  have hex : ∀ k : ℕ, ∃ w ∈ scaled Q ((k + 1) * M), ‖w - (1 / (M : ℝ)) • q‖ ≤ β / M := by
    intro k
    obtain ⟨p, hp, hpn⟩ := approx_multiple h.add hq k
    refine ⟨(1 / (((k + 1) * M : ℕ) : ℝ)) • p, ⟨p, hp, rfl⟩, ?_⟩
    have hk1 : (0 : ℝ) < (k : ℝ) + 1 := by positivity
    have hcast : (((k + 1) * M : ℕ) : ℝ) = ((k : ℝ) + 1) * M := by push_cast; ring
    have hrew : (1 / (((k + 1) * M : ℕ) : ℝ)) • p - (1 / (M : ℝ)) • q
        = (1 / (((k : ℝ) + 1) * M)) • (p - ((k : ℝ) + 1) • q) := by
      rw [hcast, smul_sub, smul_smul]
      congr 2
      field_simp
    rw [hrew, norm_smul, Real.norm_of_nonneg (by positivity)]
    calc 1 / (((k : ℝ) + 1) * M) * ‖p - ((k : ℝ) + 1) • q‖
        ≤ 1 / (((k : ℝ) + 1) * M) * (k * β) := mul_le_mul_of_nonneg_left hpn (by positivity)
      _ ≤ β / M := by
          rw [div_mul_eq_mul_div, one_mul, div_le_div_iff₀ (by positivity) hMR]
          nlinarith [h.β_nonneg]
  choose w hw hwn using hex
  have hball : IsCompact (Metric.closedBall (0 : W) R) := isCompact_closedBall 0 R
  obtain ⟨a, -, ψ, hψ, ha⟩ := hball.tendsto_subseq
    (fun k => mem_closedBall_zero_iff.mpr (h.norm_scaled_le _ (hw k)))
  have hφ : Tendsto (fun i => (ψ i + 1) * M) atTop atTop := by
    refine tendsto_atTop_mono (fun i => ?_) hψ.tendsto_atTop
    calc ψ i ≤ ψ i + 1 := Nat.le_succ _
      _ = (ψ i + 1) * 1 := (mul_one _).symm
      _ ≤ (ψ i + 1) * M := Nat.mul_le_mul_left _ hM
  refine ⟨a, mem_lowerLimit_of_tendsto h.approxNested hφ (fun i => hw (ψ i)) ha, ?_⟩
  have hlim : Tendsto (fun i => ‖w (ψ i) - (1 / (M : ℝ)) • q‖) atTop
      (𝓝 ‖a - (1 / (M : ℝ)) • q‖) := (ha.sub tendsto_const_nhds).norm
  exact le_of_tendsto' hlim (fun i => hwn (ψ i))

/-- The linear-algebra identity behind `SuperAdditive.convex_limit`. -/
theorem convex_decomposition (p q q' x x' : W) (a b N m s t : ℝ) :
    (1 / (N * m)) • p - (s • x + t • x')
      = (1 / (N * m)) • (p - a • q - b • q') + (a / N) • ((1 / m) • q - x)
        + (b / N) • ((1 / m) • q' - x') + (a / N - s) • x + (b / N - t) • x' := by
  module

/-- **The limit is convex.** -/
theorem SuperAdditive.convex_limit {Q : ℕ → Set W} {β β' R : ℝ} (h : SuperAdditive Q β β' R) :
    Convex ℝ (lowerLimit (scaled Q)) := by
  intro x hx x' hx' s t hs ht hst
  have hdata : ∀ i : ℕ, ∃ n : ℕ, ∃ w ∈ scaled Q n, i + 1 ≤ n ∧
      ‖w - (s • x + t • x')‖ ≤ (β + 1 + ‖x‖ + ‖x'‖) * (1 / ((i : ℝ) + 1)) := by
    intro i
    have hNpos : (0 : ℝ) < (i : ℝ) + 1 := by positivity
    have hε : (0 : ℝ) < 1 / ((i : ℝ) + 1) := by positivity
    obtain ⟨m, ⟨⟨y, hy, hyx⟩, ⟨y', hy', hyx'⟩⟩, hmN⟩ :=
      (((hx _ hε).and (hx' _ hε)).and (eventually_ge_atTop (i + 1))).exists
    obtain ⟨q, hq, rfl⟩ := hy
    obtain ⟨q', hq', rfl⟩ := hy'
    have hs1 : s ≤ 1 := by linarith
    have hm1 : 1 ≤ m := le_trans (Nat.le_add_left 1 i) hmN
    have hmpos : (0 : ℝ) < m := by exact_mod_cast hm1
    have hmN' : (i : ℝ) + 1 ≤ m := by exact_mod_cast hmN
    -- the integer weights
    have hfloor_le : Nat.floor (s * ((i : ℝ) + 1)) ≤ i + 1 := by
      apply Nat.floor_le_of_le
      push_cast
      nlinarith
    obtain ⟨b, hb⟩ : ∃ b, Nat.floor (s * ((i : ℝ) + 1)) + b = i + 1 :=
      ⟨i + 1 - Nat.floor (s * ((i : ℝ) + 1)), Nat.add_sub_cancel' hfloor_le⟩
    set a : ℕ := Nat.floor (s * ((i : ℝ) + 1)) with ha
    obtain ⟨p, hp, hpn⟩ := h.combination hq hq' a b (by omega)
    rw [hb] at hp hpn
    have habR : (a : ℝ) + b = (i : ℝ) + 1 := by exact_mod_cast hb
    have ha_le : (a : ℝ) ≤ s * ((i : ℝ) + 1) := Nat.floor_le (by positivity)
    have ha_gt : s * ((i : ℝ) + 1) < (a : ℝ) + 1 := Nat.lt_floor_add_one _
    refine ⟨(i + 1) * m, (1 / (((i + 1) * m : ℕ) : ℝ)) • p, ⟨p, hp, rfl⟩, ?_, ?_⟩
    · calc i + 1 = (i + 1) * 1 := (mul_one _).symm
        _ ≤ (i + 1) * m := Nat.mul_le_mul_left _ hm1
    · set N : ℝ := (i : ℝ) + 1 with hN
      set α : ℝ := (a : ℝ) / N with hα
      set α' : ℝ := (b : ℝ) / N with hα'
      have hcast : (((i + 1) * m : ℕ) : ℝ) = N * m := by push_cast; ring
      have hαnn : 0 ≤ α := by positivity
      have hα'nn : 0 ≤ α' := by positivity
      have hsum : α + α' = 1 := by
        rw [hα, hα', ← add_div, habR, hN]
        exact div_self hNpos.ne'
      have hαs : |α - s| ≤ 1 / N := by
        rw [abs_le]
        constructor
        · rw [hα, le_sub_iff_add_le, neg_add_eq_sub, le_div_iff₀ hNpos]
          have : (s - 1 / N) * N = s * N - 1 := by field_simp
          rw [this]; linarith
        · rw [hα, sub_le_iff_le_add, div_le_iff₀ hNpos]
          have : (1 / N + s) * N = 1 + s * N := by field_simp
          rw [this]; linarith
      have hα't : |α' - t| ≤ 1 / N := by
        have : α' - t = -(α - s) := by linarith
        rw [this, abs_neg]; exact hαs
      have key : (1 / (((i + 1) * m : ℕ) : ℝ)) • p - (s • x + t • x')
          = (1 / (N * m)) • (p - (a : ℝ) • q - (b : ℝ) • q') + α • ((1 / (m : ℝ)) • q - x)
            + α' • ((1 / (m : ℝ)) • q' - x') + (α - s) • x + (α' - t) • x' := by
        rw [hcast, hα, hα']
        exact convex_decomposition p q q' x x' (a : ℝ) (b : ℝ) N (m : ℝ) s t
      rw [key]
      have e1 : ‖(1 / (N * m)) • (p - (a : ℝ) • q - (b : ℝ) • q')‖ ≤ β * (1 / N) := by
        rw [norm_smul, Real.norm_of_nonneg (by positivity)]
        have hpn' : ‖p - (a : ℝ) • q - (b : ℝ) • q'‖ ≤ N * β := by
          have : (((i + 1 : ℕ)) : ℝ) = N := by push_cast; ring
          rw [← this]; exact hpn
        calc 1 / (N * m) * ‖p - (a : ℝ) • q - (b : ℝ) • q'‖ ≤ 1 / (N * m) * (N * β) :=
              mul_le_mul_of_nonneg_left hpn' (by positivity)
          _ = β / m := by field_simp
          _ ≤ β / N := div_le_div_of_nonneg_left h.β_nonneg hNpos hmN'
          _ = β * (1 / N) := by ring
      have e2 : ‖α • ((1 / (m : ℝ)) • q - x)‖ ≤ α * (1 / N) := by
        rw [norm_smul, Real.norm_of_nonneg hαnn]
        exact mul_le_mul_of_nonneg_left hyx hαnn
      have e3 : ‖α' • ((1 / (m : ℝ)) • q' - x')‖ ≤ α' * (1 / N) := by
        rw [norm_smul, Real.norm_of_nonneg hα'nn]
        exact mul_le_mul_of_nonneg_left hyx' hα'nn
      have e4 : ‖(α - s) • x‖ ≤ 1 / N * ‖x‖ := by
        rw [norm_smul, Real.norm_eq_abs]
        exact mul_le_mul_of_nonneg_right hαs (norm_nonneg _)
      have e5 : ‖(α' - t) • x'‖ ≤ 1 / N * ‖x'‖ := by
        rw [norm_smul, Real.norm_eq_abs]
        exact mul_le_mul_of_nonneg_right hα't (norm_nonneg _)
      have tri := norm_add_le
        ((1 / (N * m)) • (p - (a : ℝ) • q - (b : ℝ) • q') + α • ((1 / (m : ℝ)) • q - x)
          + α' • ((1 / (m : ℝ)) • q' - x') + (α - s) • x) ((α' - t) • x')
      have tri2 := norm_add_le
        ((1 / (N * m)) • (p - (a : ℝ) • q - (b : ℝ) • q') + α • ((1 / (m : ℝ)) • q - x)
          + α' • ((1 / (m : ℝ)) • q' - x')) ((α - s) • x)
      have tri3 := norm_add₃_le (a := (1 / (N * m)) • (p - (a : ℝ) • q - (b : ℝ) • q'))
        (b := α • ((1 / (m : ℝ)) • q - x)) (c := α' • ((1 / (m : ℝ)) • q' - x'))
      have hfin : β * (1 / N) + α * (1 / N) + α' * (1 / N) + 1 / N * ‖x‖ + 1 / N * ‖x'‖
          = (β + 1 + ‖x‖ + ‖x'‖) * (1 / N) := by
        have : α * (1 / N) + α' * (1 / N) = 1 / N := by rw [← add_mul, hsum, one_mul]
        linarith
      linarith
  choose n w hw hn hbound using hdata
  have hφ : Tendsto n atTop atTop :=
    tendsto_atTop_mono (fun i => (Nat.le_succ i).trans (hn i)) tendsto_id
  have hlim : Tendsto w atTop (𝓝 (s • x + t • x')) := by
    rw [tendsto_iff_norm_sub_tendsto_zero]
    have h0 : Tendsto (fun i : ℕ => (β + 1 + ‖x‖ + ‖x'‖) * (1 / ((i : ℝ) + 1))) atTop (𝓝 0) := by
      simpa using tendsto_one_div_add_atTop_nhds_zero_nat.const_mul (β + 1 + ‖x‖ + ‖x'‖)
    exact squeeze_zero (fun _ => norm_nonneg _) hbound h0
  exact mem_lowerLimit_of_tendsto h.approxNested hφ hw hlim

/-- Non-vacuity: the family `Q M = {M}` on the line is super-additive (`β = 0`, `β' = 1`,
`R = 1`), … -/
theorem superAdditive_example :
    SuperAdditive (fun M : ℕ => ({(M : ℝ)} : Set ℝ)) 0 1 1 where
  β_nonneg := le_rfl
  β'_nonneg := zero_le_one
  R_nonneg := zero_le_one
  add := by
    intro M₁ M₂ q₁ hq₁ q₂ hq₂
    rw [Set.mem_singleton_iff] at hq₁ hq₂
    exact ⟨((M₁ + M₂ : ℕ) : ℝ), rfl, by rw [hq₁, hq₂]; push_cast; simp⟩
  succ := by
    intro M q hq
    rw [Set.mem_singleton_iff] at hq
    exact ⟨((M + 1 : ℕ) : ℝ), rfl, by rw [hq]; push_cast; simp⟩
  bound := by
    intro M q hq
    rw [Set.mem_singleton_iff] at hq
    rw [hq]; simp

/-- … and its limit contains the point `1` (it is `{1}`). -/
theorem one_mem_limit_example : (1 : ℝ) ∈ lowerLimit (scaled fun M : ℕ => ({(M : ℝ)} : Set ℝ)) := by
  intro ε hε
  refine eventually_atTop.mpr ⟨1, fun M hM => ?_⟩
  have hMR : (0 : ℝ) < M := by exact_mod_cast hM
  refine ⟨(1 / (M : ℝ)) • (M : ℝ), ⟨(M : ℝ), rfl, rfl⟩, ?_⟩
  have : (1 / (M : ℝ)) • (M : ℝ) - 1 = 0 := by
    rw [smul_eq_mul, one_div, inv_mul_cancel₀ hMR.ne', sub_self]
  rw [this, norm_zero]
  exact hε.le

end Fekete

/-! ### Covering numbers of a convergent super-additive family (Theorem 11.71(a), abstract form) -/

section Cover

open MetricChain.CoverStability

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V] [ProperSpace V]

/-- **The covering numbers of the finite sets are sandwiched by those of the limit at
shifted accuracies**: for a super-additive family of client sets in `V × ℝ` (profile and
credit, with the distance `max(‖Δp‖, |Δg|)`), every `η > 0` and all large `M`,
`N(Q M / M, ε + (2L+e)η) ≤ N(K, ε)` and `N(K, ε) ≤ N(Q M / M, ε − (2L+e)η)`, in the form
"`k` centres suffice". -/
theorem SuperAdditive.cover_sandwich {Q : ℕ → Set (V × ℝ)} {β β' R : ℝ}
    (h : SuperAdditive Q β β' R) (hne : ∀ M, 1 ≤ M → (Q M).Nonempty)
    {L e : ℝ} (hL : 0 ≤ L) (he : 0 ≤ e) (ε : ℝ) {η : ℝ} (hη : 0 < η) :
    ∀ᶠ M in atTop, ∀ k : ℕ,
      (HasCover L e ε (lowerLimit (scaled Q)) k →
          HasCover L e (ε + (2 * L + e) * η) (scaled Q M) k) ∧
        (HasCover L e (ε - (2 * L + e) * η) (scaled Q M) k →
          HasCover L e ε (lowerLimit (scaled Q)) k) := by
  obtain ⟨-, -, h1, h2⟩ := h.hausdorff_limit hne
  filter_upwards [h1 η hη, h2 η hη] with M hM1 hM2 k
  refine hasCover_sandwich hL he ?_ ?_ k
  · intro x hx
    obtain ⟨y, hy, hyx⟩ := hM2 x hx
    rw [Prod.norm_def] at hyx
    exact ⟨y, hy, (le_max_left _ _).trans hyx,
      by simpa [Real.norm_eq_abs] using (le_max_right _ _).trans hyx⟩
  · intro y hy
    obtain ⟨x, hx, hyx⟩ := hM1 y hy
    rw [Prod.norm_def] at hyx
    exact ⟨x, hx, (le_max_left _ _).trans hyx,
      by simpa [Real.norm_eq_abs] using (le_max_right _ _).trans hyx⟩

end Cover

end MetricChain.SetLimit
