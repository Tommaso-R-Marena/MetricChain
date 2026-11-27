import Mathlib
import proofs.Frontiers.CertificationGeometry

/-!
# Best-first search: a resource-augmentation bound

Setting of `CertificationGeometry.lean`: a known part `f`, a residual `g` admissible for an
envelope `d`, the energy `E = f + g` with minimum `Estar`, the optimality gap `γ z = E z - Estar`,
and the slack `s = slack d g` (nonnegative, triangle inequality): the quasi-metric in which
`ε`-certificates are coverings with the radii `γ + ε`.

**Best-first (Piyavskii–Shubert) search with tolerance `ε`.**  Evaluate an arbitrary first point
`y 0`.  After `k ≥ 1` evaluations the evaluated set is `A_k = {y 0, …, y (k - 1)}`
(`evalSet y k`), and the certified lower bound on the energy is

  `LB_k z = f z + lowerEnv d A_k g z = E z - s(A_k, z)`     (`lowerEnv_eq_sub_slack`).

If `A_k` is an `ε`-certificate the search ends; otherwise it evaluates a minimiser `y k` of
`LB_k`.  `IsBestFirstRun d f g ε y m` says that `y 0, …, y (m - 1)` are the first `m` evaluations
of such a search: for `0 < k < m` the set `A_k` is not an `ε`-certificate and `y k` minimises
`LB_k`.

Results:

* `bestFirst_sep_a`, `bestFirst_sep_b`, `bestFirst_sep_c` — **separation** of the evaluated
  points: for `1 ≤ j < k < m`, with `γ_i = γ (y i)`,
  (a) `γ_k - γ_j + ε < s (y j) (y k)` (the search was not finished at step `k`),
  (b) `γ_k ≤ s (y j) (y k)` (optimism: `LB_k (y k) ≤ Estar`),
  (c) `γ_j - γ_k ≤ s (y k) (y j)` (`y j` was preferred to `y k` at step `j`);
  (a) and (b) also hold for `j = 0`.  The lemmas are stated with energies instead of gaps
  (`γ_k - γ_j = E (y k) - E (y j)`), and (b), (c) with an arbitrary point `z` in place of the
  minimiser of the energy and of `y k`.
* `not_cocovered` — two points separated as in (a)–(c) cannot both lie within the shrunk radii
  `θ (γ + ε')` of a common centre, when `s` is `ρ`-quasi-symmetric, `θ ρ ≤ 1/4`, `θ ≤ 1/4` and
  `6 ε' ≤ ε` (real arithmetic and the triangle inequality only).
* `bestFirst_card_le` — **resource augmentation**: if `d` is symmetric and `g` is `κ`-Lipschitz
  for `d` with `κ < 1`, every best-first run has length at most `|C| + 1`, for every set of
  centres `C` that covers each point `z` within the slack radius `θ (γ z + ε / 6)`, where
  `θ = (1 - κ) / (4 (1 + κ))`.  Every `ε`-certificate is a cover with the radii `γ z + ε`
  (`cover_of_certificate`), so best-first search is competitive with the smallest certificate up
  to the constant factors `θ` and `1/6` in the radii.  It is the case `ρ = (1 + κ) / (1 - κ)` of
  `bestFirst_card_le_of_quasiSymm`, which only assumes a `ρ`-quasi-symmetric slack.
* `bestFirst_run_exists_or_certificate`, `bestFirst_certificate_of_card_lt`,
  `bestFirst_certifies` — the search is well defined (a run can always be continued until a
  certificate is found), hence it returns an `ε`-certificate after at most `|C| + 1` evaluations.
* `isBestFirstRun_one`, `isBestFirstRun_two_iff`, `bestFirst_instance_run`,
  `bestFirst_card_le_sharp` — sanity: runs of length one and two, and an explicit instance on
  `Bool` in which all hypotheses of `bestFirst_card_le` hold and its bound is attained.
-/

namespace MetricChain

open Finset

variable {X : Type*}

/-! ### Evaluated sets -/

section EvalSet

variable [DecidableEq X]

/-- The set `A_k = {y 0, …, y (k - 1)}` of the first `k` points of the sequence `y`: the points
evaluated before step `k` by a search that evaluates `y 0, y 1, …` in this order. -/
def evalSet (y : ℕ → X) (k : ℕ) : Finset X := (Finset.range k).image y

/-- Membership in the evaluated set. -/
theorem mem_evalSet {y : ℕ → X} {k : ℕ} {a : X} : a ∈ evalSet y k ↔ ∃ i < k, y i = a := by
  simp [evalSet]

/-- Earlier points belong to the evaluated set. -/
theorem mem_evalSet_of_lt (y : ℕ → X) {j k : ℕ} (hjk : j < k) : y j ∈ evalSet y k :=
  mem_evalSet.mpr ⟨j, hjk, rfl⟩

/-- After at least one evaluation the evaluated set is nonempty. -/
theorem evalSet_nonempty (y : ℕ → X) {k : ℕ} (hk : 0 < k) : (evalSet y k).Nonempty :=
  ⟨y 0, mem_evalSet_of_lt y hk⟩

/-- The evaluated set `A_k` only depends on the first `k` points of the sequence. -/
theorem evalSet_congr {y y' : ℕ → X} {k : ℕ} (h : ∀ i < k, y i = y' i) :
    evalSet y k = evalSet y' k :=
  Finset.image_congr fun i hi => h i (Finset.mem_range.mp hi)

/-- With a single evaluated point the lower McShane envelope is one cone. -/
theorem lowerEnv_evalSet_one (d : X → X → ℝ) (g : X → ℝ) (y : ℕ → X)
    (h : (evalSet y 1).Nonempty) (z : X) :
    lowerEnv d (evalSet y 1) h g z = g (y 0) - d (y 0) z := by
  unfold lowerEnv
  apply le_antisymm
  · apply Finset.sup'_le
    intro a ha
    obtain ⟨i, hi, rfl⟩ := mem_evalSet.mp ha
    obtain rfl : i = 0 := by omega
    exact le_rfl
  · exact Finset.le_sup' (fun a => g a - d a z) (mem_evalSet_of_lt y Nat.one_pos)

/-- With a single evaluated point the incumbent is the energy of that point. -/
theorem certUB_evalSet_one (f g : X → ℝ) (y : ℕ → X) (h : (evalSet y 1).Nonempty) :
    certUB f g (evalSet y 1) h = f (y 0) + g (y 0) := by
  unfold certUB
  apply le_antisymm
  · exact Finset.inf'_le (fun a => f a + g a) (mem_evalSet_of_lt y Nat.one_pos)
  · apply Finset.le_inf'
    intro a ha
    obtain ⟨i, hi, rfl⟩ := mem_evalSet.mp ha
    obtain rfl : i = 0 := by omega
    exact le_rfl

end EvalSet

/-! ### Best-first runs -/

section Run

variable [Fintype X] [Nonempty X] [DecidableEq X]

/-- **Best-first runs.**  `IsBestFirstRun d f g ε y m`: the points `y 0, …, y (m - 1)` are the
first `m` evaluations of a best-first search with tolerance `ε`.  The first point `y 0` is
arbitrary; at every later step `0 < k < m` the evaluated set `A_k = evalSet y k` is not yet an
`ε`-certificate, and the next point `y k` minimises the certified lower bound
`LB_k z = f z + lowerEnv d A_k g z`.  (The values `y i` with `i ≥ m` are irrelevant.) -/
structure IsBestFirstRun (d : X → X → ℝ) (f g : X → ℝ) (ε : ℝ) (y : ℕ → X) (m : ℕ) : Prop where
  /-- At least one point, the arbitrary first point `y 0`, is evaluated. -/
  pos : 0 < m
  /-- The search continues at step `k`: the evaluated set `A_k` is not an `ε`-certificate. -/
  not_certificate : ∀ k (hk : 0 < k), k < m →
    ¬ IsCertificate d f g (evalSet y k) (evalSet_nonempty y hk) ε
  /-- The point evaluated at step `k` minimises the lower bound `LB_k`. -/
  minimises : ∀ k (hk : 0 < k), k < m → ∀ z,
    f (y k) + lowerEnv d (evalSet y k) (evalSet_nonempty y hk) g (y k) ≤
      f z + lowerEnv d (evalSet y k) (evalSet_nonempty y hk) g z

/-- **Runs of length one.**  The first point is arbitrary: every sequence is a best-first run of
length one. -/
theorem isBestFirstRun_one (d : X → X → ℝ) (f g : X → ℝ) (ε : ℝ) (y : ℕ → X) :
    IsBestFirstRun d f g ε y 1 :=
  ⟨Nat.one_pos, fun k hk hk1 => absurd hk1 (by omega), fun k hk hk1 => absurd hk1 (by omega)⟩

/-- **Runs of length two.**  `y 0, y 1` is a best-first run iff the first point alone is not an
`ε`-certificate, which here reads `ε < f (y 0) - f (y 1) + d (y 0) (y 1)`, and the second point
minimises `LB_1 z = f z + g (y 0) - d (y 0) z`. -/
theorem isBestFirstRun_two_iff {d : X → X → ℝ} {f g : X → ℝ} {ε : ℝ} {y : ℕ → X} :
    IsBestFirstRun d f g ε y 2 ↔
      ε < f (y 0) - f (y 1) + d (y 0) (y 1) ∧ ∀ z, f (y 1) - d (y 0) (y 1) ≤ f z - d (y 0) z := by
  constructor
  · intro hrun
    have hnc := hrun.not_certificate 1 Nat.one_pos Nat.one_lt_two
    have hmin := hrun.minimises 1 Nat.one_pos Nat.one_lt_two
    have h1 : f (y 1) + lowerEnv d (evalSet y 1) (evalSet_nonempty y Nat.one_pos) g (y 1) ≤
        certLB d f g (evalSet y 1) (evalSet_nonempty y Nat.one_pos) :=
      Finset.le_inf' _ _ fun z _ => hmin z
    unfold IsCertificate at hnc
    rw [certUB_evalSet_one] at hnc
    rw [lowerEnv_evalSet_one] at h1
    refine ⟨by linarith, fun z => ?_⟩
    have h2 := hmin z
    rw [lowerEnv_evalSet_one, lowerEnv_evalSet_one] at h2
    linarith
  · rintro ⟨hε, hmin⟩
    have key : ∀ k, 0 < k → k < 2 → k = 1 := fun k h1 h2 => by omega
    refine ⟨Nat.zero_lt_two, fun k hk hkm => ?_, fun k hk hkm z => ?_⟩
    · obtain rfl := key k hk hkm
      have h1 : certLB d f g (evalSet y 1) (evalSet_nonempty y hk) ≤
          f (y 1) + lowerEnv d (evalSet y 1) (evalSet_nonempty y hk) g (y 1) :=
        Finset.inf'_le _ (mem_univ (y 1))
      rw [lowerEnv_evalSet_one] at h1
      unfold IsCertificate
      rw [certUB_evalSet_one]
      linarith
    · obtain rfl := key k hk hkm
      rw [lowerEnv_evalSet_one, lowerEnv_evalSet_one]
      linarith [hmin z]

omit [Fintype X] [Nonempty X] [DecidableEq X] in
/-- The lower McShane envelope only depends on the evaluated set, not on the proof that it is
nonempty. -/
private theorem lowerEnv_congr {d : X → X → ℝ} {g : X → ℝ} {A B : Finset X} (h : A = B)
    (hA : A.Nonempty) (hB : B.Nonempty) (z : X) : lowerEnv d A hA g z = lowerEnv d B hB g z := by
  subst h
  rfl

omit [DecidableEq X] in
/-- Being a certificate only depends on the evaluated set, not on the proof that it is
nonempty. -/
private theorem isCertificate_congr {d : X → X → ℝ} {f g : X → ℝ} {ε : ℝ} {A B : Finset X}
    (h : A = B) (hA : A.Nonempty) (hB : B.Nonempty) :
    IsCertificate d f g A hA ε ↔ IsCertificate d f g B hB ε := by
  subst h
  rfl

/-- **A run that has not reached a certificate can be continued**: on a finite space the lower
bound `LB_m` has a minimiser `x`, and evaluating it next gives a run of length `m + 1`. -/
theorem IsBestFirstRun.extend {d : X → X → ℝ} {f g : X → ℝ} {ε : ℝ} {y : ℕ → X} {m : ℕ}
    (hrun : IsBestFirstRun d f g ε y m)
    (hnc : ¬ IsCertificate d f g (evalSet y m) (evalSet_nonempty y hrun.pos) ε) :
    ∃ x, IsBestFirstRun d f g ε (Function.update y m x) (m + 1) := by
  obtain ⟨x, -, hx⟩ := Finset.exists_min_image univ
    (fun z => f z + lowerEnv d (evalSet y m) (evalSet_nonempty y hrun.pos) g z) univ_nonempty
  have hy : ∀ i < m, Function.update y m x i = y i := fun i hi =>
    Function.update_of_ne (Nat.ne_of_lt hi) x y
  have hset : ∀ k ≤ m, evalSet (Function.update y m x) k = evalSet y k := fun k hk =>
    evalSet_congr fun i hi => hy i (lt_of_lt_of_le hi hk)
  refine ⟨x, Nat.succ_pos m, fun k hk hkm => ?_, fun k hk hkm z => ?_⟩
  · have hkm' : k ≤ m := Nat.lt_succ_iff.mp hkm
    rw [isCertificate_congr (hset k hkm') _ (evalSet_nonempty y hk)]
    rcases Nat.lt_or_eq_of_le hkm' with h | rfl
    · exact hrun.not_certificate k hk h
    · exact hnc
  · have hkm' : k ≤ m := Nat.lt_succ_iff.mp hkm
    rw [lowerEnv_congr (hset k hkm') _ (evalSet_nonempty y hk),
      lowerEnv_congr (hset k hkm') _ (evalSet_nonempty y hk)]
    rcases Nat.lt_or_eq_of_le hkm' with h | rfl
    · rw [hy k h]
      exact hrun.minimises k hk h z
    · rw [Function.update_self]
      exact hx z (mem_univ z)

/-- **Best-first search is well defined.**  From every first point `x₀` and for every `n` there
is a best-first run starting at `x₀` that either has length `n + 1` or is shorter and ends with
an `ε`-certificate: the search can always be continued until a certificate is found. -/
theorem bestFirst_run_exists_or_certificate (d : X → X → ℝ) (f g : X → ℝ) (ε : ℝ) (x₀ : X)
    (n : ℕ) :
    ∃ (y : ℕ → X) (m : ℕ), y 0 = x₀ ∧ m ≤ n ∧ IsBestFirstRun d f g ε y (m + 1) ∧
      (m = n ∨ IsCertificate d f g (evalSet y (m + 1)) (evalSet_nonempty y m.succ_pos) ε) := by
  induction n with
  | zero => exact ⟨fun _ => x₀, 0, rfl, le_rfl, isBestFirstRun_one d f g ε _, Or.inl rfl⟩
  | succ n ih =>
    obtain ⟨y, m, hy0, hmn, hrun, hm⟩ := ih
    by_cases hc : IsCertificate d f g (evalSet y (m + 1)) (evalSet_nonempty y m.succ_pos) ε
    · exact ⟨y, m, hy0, Nat.le_succ_of_le hmn, hrun, Or.inr hc⟩
    · obtain rfl : m = n := hm.resolve_right hc
      obtain ⟨x, hx⟩ := hrun.extend hc
      refine ⟨Function.update y (m + 1) x, m + 1, ?_, le_rfl, hx, Or.inl rfl⟩
      rw [Function.update_of_ne (Nat.succ_ne_zero m).symm, hy0]

/-! ### Lemma A: separation of the evaluated points -/

/-- **Separation (a): the search was not finished.**  For `j < k < m` in a best-first run,

  `E (y k) - E (y j) + ε < s (y j) (y k)`,

that is `γ_k - γ_j + ε < s (y j) (y k)` for the gaps `γ_i = E (y i) - Estar`.  Indeed `A_k` is not
an `ε`-certificate, so `LB_k (y k) = min LB_k < certUB A_k - ε ≤ E (y j) - ε`, while
`LB_k (y k) ≥ E (y k) - s (y j) (y k)` because `y j ∈ A_k`. -/
theorem bestFirst_sep_a {d : X → X → ℝ} {f g : X → ℝ} {ε : ℝ} {y : ℕ → X} {m : ℕ}
    (hrun : IsBestFirstRun d f g ε y m) {j k : ℕ} (hjk : j < k) (hkm : k < m) :
    f (y k) + g (y k) - (f (y j) + g (y j)) + ε < slack d g (y j) (y k) := by
  have hk : 0 < k := Nat.zero_lt_of_lt hjk
  have hmem : y j ∈ evalSet y k := mem_evalSet_of_lt y hjk
  have hnc := hrun.not_certificate k hk hkm
  have h1 : f (y k) + lowerEnv d (evalSet y k) (evalSet_nonempty y hk) g (y k) ≤
      certLB d f g (evalSet y k) (evalSet_nonempty y hk) :=
    Finset.le_inf' _ _ fun z _ => hrun.minimises k hk hkm z
  have h2 : certUB f g (evalSet y k) (evalSet_nonempty y hk) ≤ f (y j) + g (y j) :=
    Finset.inf'_le (fun a => f a + g a) hmem
  have h3 : g (y j) - d (y j) (y k) ≤
      lowerEnv d (evalSet y k) (evalSet_nonempty y hk) g (y k) :=
    Finset.le_sup' (fun a => g a - d a (y k)) hmem
  unfold IsCertificate at hnc
  unfold slack
  linarith

/-- **Separation (b): optimism.**  For `j < k < m` in a best-first run and every competitor `z`,

  `E (y k) - E z ≤ s (y j) (y k)`;

for a minimiser `z` of the energy this is `γ_k ≤ s (y j) (y k)`.  Indeed
`E (y k) - s (y j) (y k) ≤ LB_k (y k) ≤ LB_k z ≤ E z`, the last step by admissibility. -/
theorem bestFirst_sep_b {d : X → X → ℝ} {f g : X → ℝ} {ε : ℝ} {y : ℕ → X} {m : ℕ}
    (hg : Admissible d g) (hrun : IsBestFirstRun d f g ε y m) {j k : ℕ} (hjk : j < k)
    (hkm : k < m) (z : X) :
    f (y k) + g (y k) - (f z + g z) ≤ slack d g (y j) (y k) := by
  have hk : 0 < k := Nat.zero_lt_of_lt hjk
  have h1 := hrun.minimises k hk hkm z
  have h2 := lowerEnv_le hg (evalSet y k) (evalSet_nonempty y hk) g (fun _ _ => rfl) z
  have h3 : g (y j) - d (y j) (y k) ≤
      lowerEnv d (evalSet y k) (evalSet_nonempty y hk) g (y k) :=
    Finset.le_sup' (fun a => g a - d a (y k)) (mem_evalSet_of_lt y hjk)
  unfold slack
  linarith

/-- **Separation (c): earlier points were preferred.**  For `0 < j < m` in a best-first run and
every point `z`,

  `E (y j) - E z ≤ s z (y j)`;

for `z = y k` this is `γ_j - γ_k ≤ s (y k) (y j)`.  Indeed `y j` minimises `LB_j = f + L_j` and
the lower envelope `L_j` is admissible, so `f (y j) - f z ≤ L_j z - L_j (y j) ≤ d z (y j)`.
(The first point `y 0` is arbitrary, hence `j = 0` is excluded.) -/
theorem bestFirst_sep_c {d : X → X → ℝ} {f g : X → ℝ} {ε : ℝ} {y : ℕ → X} {m : ℕ}
    (hd : IsEnvelope d) (hrun : IsBestFirstRun d f g ε y m) {j : ℕ} (hj : 0 < j) (hjm : j < m)
    (z : X) :
    f (y j) + g (y j) - (f z + g z) ≤ slack d g z (y j) := by
  have h1 := hrun.minimises j hj hjm z
  have h2 := lowerEnv_admissible hd (evalSet y j) (evalSet_nonempty y hj) g z (y j)
  unfold slack
  linarith

end Run

/-! ### Lemma B: two separated points cannot share a shrunk centre -/

/-- **Two separated points cannot share a shrunk centre.**  Let `s ≥ 0` satisfy the triangle
inequality and be `ρ`-quasi-symmetric (`s x y ≤ ρ * s y x`), and let `θ ρ ≤ 1/4`, `θ ≤ 1/4`,
`ε' ≥ 0` and `6 ε' ≤ ε`.  If the points `p`, `q` with gaps `γp, γq ≥ 0` are separated,

  `γq - γp + ε < s p q`,   `γq ≤ s p q`,   `γp - γq ≤ s q p`,

then no centre `a` covers both of them with the shrunk radii: `s a p ≤ θ (γp + ε')` and
`s a q ≤ θ (γq + ε')` cannot hold together.

Proof: such a centre gives `s p q, s q p ≤ (γp + γq) / 4 + ε' / 2`.  The last two separation
inequalities then yield `γq ≤ 2 ε'` and `γp ≤ 4 ε'`, and the first one the contradiction
`ε < (5/4) γp + ε' / 2 ≤ 6 ε' ≤ ε`. -/
theorem not_cocovered {s : X → X → ℝ} {ρ θ ε ε' : ℝ} (hs : ∀ x y, 0 ≤ s x y)
    (htri : ∀ x y z, s x z ≤ s x y + s y z) (hqs : ∀ x y, s x y ≤ ρ * s y x)
    (hθρ : θ * ρ ≤ 1 / 4) (hθ : θ ≤ 1 / 4) (hε' : 0 ≤ ε') (hε : 6 * ε' ≤ ε) {p q : X}
    {γp γq : ℝ} (hγp : 0 ≤ γp) (hγq : 0 ≤ γq) (ha : γq - γp + ε < s p q) (hb : γq ≤ s p q)
    (hc : γp - γq ≤ s q p) : ¬ ∃ a, s a p ≤ θ * (γp + ε') ∧ s a q ≤ θ * (γq + ε') := by
  rintro ⟨a, hap, haq⟩
  -- a point `x` of gap `γ` covered by `a` satisfies `s x a, s a x ≤ (γ + ε') / 4`
  have key : ∀ x γ, 0 ≤ γ → s a x ≤ θ * (γ + ε') →
      s x a ≤ (γ + ε') / 4 ∧ s a x ≤ (γ + ε') / 4 := by
    intro x γ hγ hax
    have hpos : 0 ≤ γ + ε' := by linarith
    constructor
    · have h1 := hqs x a
      rcases le_or_gt 0 ρ with hρ | hρ
      · have h2 : ρ * s a x ≤ ρ * (θ * (γ + ε')) := mul_le_mul_of_nonneg_left hax hρ
        have h3 : θ * ρ * (γ + ε') ≤ 1 / 4 * (γ + ε') := mul_le_mul_of_nonneg_right hθρ hpos
        linarith
      · have h2 : ρ * s a x ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hρ.le (hs a x)
        linarith
    · have h3 : θ * (γ + ε') ≤ 1 / 4 * (γ + ε') := mul_le_mul_of_nonneg_right hθ hpos
      linarith
  obtain ⟨hpa, hap'⟩ := key p γp hγp hap
  obtain ⟨hqa, haq'⟩ := key q γq hγq haq
  have h1 := htri p a q
  have h2 := htri q a p
  linarith

/-! ### The resource-augmentation bound -/

/-- A symmetric envelope is nonnegative: `0 = d x x ≤ d x y + d y x = 2 d x y`. -/
private theorem nonneg_of_symm_envelope {d : X → X → ℝ} (hd : IsEnvelope d)
    (hsymm : ∀ x y, d x y = d y x) (x y : X) : 0 ≤ d x y := by
  have h1 := hd.triangle x y x
  have h2 := hd.self x
  have h3 := hsymm y x
  linarith

/-- If the envelope is symmetric and the residual is `κ`-Lipschitz for it with `κ < 1`, then
`(1 - κ) d ≤ slack ≤ (1 + κ) d`, so the slack is quasi-symmetric with the constant
`ρ = (1 + κ) / (1 - κ)`. -/
private theorem slack_quasi_symm {d : X → X → ℝ} {g : X → ℝ} {κ : ℝ}
    (hsymm : ∀ x y, d x y = d y x) (hκ1 : κ < 1) (hgκ : ∀ x y, |g x - g y| ≤ κ * d x y)
    (x y : X) : slack d g x y ≤ (1 + κ) / (1 - κ) * slack d g y x := by
  have h2 : g y - g x ≤ κ * d x y := by
    have h := (abs_le.mp (hgκ y x)).2
    rwa [hsymm y x] at h
  have hpos : 0 < 1 - κ := by linarith
  rw [div_mul_eq_mul_div, le_div_iff₀ hpos]
  unfold slack
  rw [hsymm y x]
  linarith

section Bound

variable [Fintype X] [Nonempty X] [DecidableEq X]

/-- **Best-first search against shrunk covers, general form.**  Let the residual `g` be admissible
for the envelope `d` (not necessarily symmetric) and let the slack be `ρ`-quasi-symmetric,
`slack d g x y ≤ ρ * slack d g y x`.  Let `θ ρ ≤ 1/4`, `θ ≤ 1/4`, `ε' ≥ 0` and `6 ε' ≤ ε`, let
`Estar` be the minimum of the energy `E = f + g`, and let `C` be a set of centres that covers
every point `z` within the shrunk radius `slack d g a z ≤ θ * (E z - Estar + ε')` for some
`a ∈ C`.  Then every best-first run with tolerance `ε` has length at most `|C| + 1`.

Proof: by the separation inequalities and `not_cocovered` no centre covers two of the points
`y 1, …, y (m - 1)`; choosing a covering centre for each of them is therefore injective, so
`m - 1 ≤ |C|`. -/
theorem bestFirst_card_le_of_quasiSymm {d : X → X → ℝ} {f g : X → ℝ} {ρ θ ε ε' Estar : ℝ}
    (hd : IsEnvelope d) (hg : Admissible d g)
    (hqs : ∀ x y, slack d g x y ≤ ρ * slack d g y x) (hθρ : θ * ρ ≤ 1 / 4) (hθ : θ ≤ 1 / 4)
    (hε' : 0 ≤ ε') (hε : 6 * ε' ≤ ε) (hE : ∀ z, Estar ≤ f z + g z)
    (hx : ∃ x, f x + g x = Estar) {C : Finset X}
    (hC : ∀ z, ∃ a ∈ C, slack d g a z ≤ θ * (f z + g z - Estar + ε'))
    {y : ℕ → X} {m : ℕ} (hrun : IsBestFirstRun d f g ε y m) : m ≤ C.card + 1 := by
  obtain ⟨xs, hxs⟩ := hx
  -- choose a covering centre for every point; two points of the run never share their centre
  choose φ hφC hφ using hC
  have hne : ∀ j k, 0 < j → j < k → k < m → φ (y j) ≠ φ (y k) := by
    intro j k hj hjk hkm heq
    have hsa := bestFirst_sep_a hrun hjk hkm
    have hsb := bestFirst_sep_b hg hrun hjk hkm xs
    have hsc := bestFirst_sep_c hd hrun hj (hjk.trans hkm) (y k)
    have hEj := hE (y j)
    have hEk := hE (y k)
    refine not_cocovered (γp := f (y j) + g (y j) - Estar) (γq := f (y k) + g (y k) - Estar)
      (slack_nonneg hg) (slack_triangle hd g) hqs hθρ hθ hε' hε (by linarith) (by linarith)
      (by linarith) (by linarith) (by linarith) ⟨φ (y j), hφ (y j), ?_⟩
    rw [heq]
    exact hφ (y k)
  -- hence `i ↦ φ (y i)` embeds `{1, …, m - 1}` into `C`
  have hinj : Set.InjOn (fun i => φ (y i)) (Finset.Ico 1 m : Set ℕ) := by
    intro i hi i' hi' heq
    have hi1 := Finset.mem_Ico.mp (Finset.mem_coe.mp hi)
    have hi1' := Finset.mem_Ico.mp (Finset.mem_coe.mp hi')
    have heq' : φ (y i) = φ (y i') := heq
    rcases lt_trichotomy i i' with h | h | h
    · exact absurd heq' (hne i i' (by omega) h hi1'.2)
    · exact h
    · exact absurd heq'.symm (hne i' i (by omega) h hi1.2)
  have hcard : (Finset.Ico 1 m).card ≤ C.card :=
    Finset.card_le_card_of_injOn (fun i => φ (y i)) (fun i _ => hφC (y i)) hinj
  rw [Nat.card_Ico] at hcard
  omega

/-- **Resource augmentation for best-first search.**  Let `d` be a symmetric envelope, let the
residual be `κ`-Lipschitz for it, `|g x - g y| ≤ κ * d x y` with `0 ≤ κ < 1`, let `ε ≥ 0` and let
`Estar` be the minimum of the energy `E = f + g`.  Put `θ = (1 - κ) / (4 (1 + κ))` and let `C` be
any set of centres that covers every point `z` within the shrunk radius of its own gap:
`slack d g a z ≤ θ * (E z - Estar + ε / 6)` for some `a ∈ C`.  Then every best-first run with
tolerance `ε` has length at most `|C| + 1`.

Proof: `d ≥ 0` by symmetry, so `g` is admissible; `(1 - κ) d ≤ s ≤ (1 + κ) d` makes the slack
`ρ`-quasi-symmetric with `ρ = (1 + κ) / (1 - κ)`; and `θ ρ = 1/4`, `θ ≤ 1/4`.  The claim is then
`bestFirst_card_le_of_quasiSymm` with `ε' = ε / 6`. -/
theorem bestFirst_card_le {d : X → X → ℝ} {f g : X → ℝ} {κ ε Estar : ℝ} (hd : IsEnvelope d)
    (hsymm : ∀ x y, d x y = d y x) (hκ0 : 0 ≤ κ) (hκ1 : κ < 1)
    (hgκ : ∀ x y, |g x - g y| ≤ κ * d x y) (hε : 0 ≤ ε) (hE : ∀ z, Estar ≤ f z + g z)
    (hx : ∃ x, f x + g x = Estar) {C : Finset X}
    (hC : ∀ z, ∃ a ∈ C,
      slack d g a z ≤ (1 - κ) / (4 * (1 + κ)) * (f z + g z - Estar + ε / 6))
    {y : ℕ → X} {m : ℕ} (hrun : IsBestFirstRun d f g ε y m) : m ≤ C.card + 1 := by
  -- the residual is admissible: `g x - g y ≤ κ d x y ≤ d x y`
  have hg : Admissible d g := by
    intro x y
    have h1 := (abs_le.mp (hgκ x y)).2
    have h2 : κ * d x y ≤ 1 * d x y :=
      mul_le_mul_of_nonneg_right hκ1.le (nonneg_of_symm_envelope hd hsymm x y)
    linarith
  -- the constants: `θ ρ = 1/4` and `θ ≤ 1/4`
  have hθρ : (1 - κ) / (4 * (1 + κ)) * ((1 + κ) / (1 - κ)) ≤ 1 / 4 := by
    have h1 : (1 - κ) ≠ 0 := by linarith
    have h2 : (1 + κ) ≠ 0 := by linarith
    apply le_of_eq
    field_simp
  have hθ : (1 - κ) / (4 * (1 + κ)) ≤ 1 / 4 := by
    rw [div_le_iff₀ (by linarith)]
    linarith
  exact bestFirst_card_le_of_quasiSymm (ε' := ε / 6) hd hg (slack_quasi_symm hsymm hκ1 hgκ) hθρ hθ
    (by linarith) (by linarith) hE hx hC hrun

/-- **After `|C| + 1` evaluations best-first search has found a certificate.**  Under the
hypotheses of `bestFirst_card_le`, the evaluated set of every run longer than `|C|` (that is, of
length exactly `|C| + 1`) is an `ε`-certificate: otherwise the run could be continued
(`IsBestFirstRun.extend`), which contradicts the bound. -/
theorem bestFirst_certificate_of_card_lt {d : X → X → ℝ} {f g : X → ℝ} {κ ε Estar : ℝ}
    (hd : IsEnvelope d) (hsymm : ∀ x y, d x y = d y x) (hκ0 : 0 ≤ κ) (hκ1 : κ < 1)
    (hgκ : ∀ x y, |g x - g y| ≤ κ * d x y) (hε : 0 ≤ ε) (hE : ∀ z, Estar ≤ f z + g z)
    (hx : ∃ x, f x + g x = Estar) {C : Finset X}
    (hC : ∀ z, ∃ a ∈ C,
      slack d g a z ≤ (1 - κ) / (4 * (1 + κ)) * (f z + g z - Estar + ε / 6))
    {y : ℕ → X} {m : ℕ} (hrun : IsBestFirstRun d f g ε y m) (hm : C.card < m) :
    IsCertificate d f g (evalSet y m) (evalSet_nonempty y hrun.pos) ε := by
  by_contra hnc
  obtain ⟨x, hrun'⟩ := hrun.extend hnc
  have hle := bestFirst_card_le hd hsymm hκ0 hκ1 hgκ hε hE hx hC hrun'
  omega

/-- **Best-first search certifies within `|C| + 1` evaluations.**  Under the hypotheses of
`bestFirst_card_le`, from every first point `x₀` there is a best-first run of length at most
`|C| + 1` whose evaluated set is an `ε`-certificate. -/
theorem bestFirst_certifies {d : X → X → ℝ} {f g : X → ℝ} {κ ε Estar : ℝ} (hd : IsEnvelope d)
    (hsymm : ∀ x y, d x y = d y x) (hκ0 : 0 ≤ κ) (hκ1 : κ < 1)
    (hgκ : ∀ x y, |g x - g y| ≤ κ * d x y) (hε : 0 ≤ ε) (hE : ∀ z, Estar ≤ f z + g z)
    (hx : ∃ x, f x + g x = Estar) {C : Finset X}
    (hC : ∀ z, ∃ a ∈ C,
      slack d g a z ≤ (1 - κ) / (4 * (1 + κ)) * (f z + g z - Estar + ε / 6))
    (x₀ : X) :
    ∃ (y : ℕ → X) (m : ℕ), y 0 = x₀ ∧ m ≤ C.card ∧ IsBestFirstRun d f g ε y (m + 1) ∧
      IsCertificate d f g (evalSet y (m + 1)) (evalSet_nonempty y m.succ_pos) ε := by
  obtain ⟨y, m, hy0, -, hrun, hm⟩ :=
    bestFirst_run_exists_or_certificate d f g ε x₀ (C.card + 1)
  have hle := bestFirst_card_le hd hsymm hκ0 hκ1 hgκ hε hE hx hC hrun
  exact ⟨y, m, hy0, by omega, hrun, hm.resolve_left (by omega)⟩

end Bound

/-! ### An explicit instance: the bound is attained -/

/-- **An explicit run of length two** on `Bool`: discrete envelope `d x y = [x ≠ y]`, known part
`f = (0, 20)` and residual `g = (0, 1/2)` (values at `false`, `true`), tolerance `ε = 1`.  Starting
at `true`, the single evaluation is not a certificate and the lower bound is minimised at
`false`. -/
theorem bestFirst_instance_run :
    IsBestFirstRun (discreteEnvelope 1) (fun b : Bool => if b then (20 : ℝ) else 0)
      (fun b : Bool => if b then (1 / 2 : ℝ) else 0) 1 (fun n => decide (n = 0)) 2 := by
  rw [isBestFirstRun_two_iff]
  refine ⟨by norm_num [discreteEnvelope], fun z => ?_⟩
  cases z <;> norm_num [discreteEnvelope]

/-- **The hypotheses of `bestFirst_card_le` are satisfiable and its bound is attained.**  For the
data of `bestFirst_instance_run`, with `κ = 1/2` (hence `θ = 1/12`) and `Estar = 0`, the single
centre `false` covers both points with the shrunk radii, and the run has length `2 = |C| + 1`. -/
theorem bestFirst_card_le_sharp :
    ∃ (d : Bool → Bool → ℝ) (f g : Bool → ℝ) (κ ε Estar : ℝ) (C : Finset Bool) (y : ℕ → Bool)
      (m : ℕ), IsEnvelope d ∧ (∀ u v, d u v = d v u) ∧ 0 ≤ κ ∧ κ < 1 ∧
        (∀ u v, |g u - g v| ≤ κ * d u v) ∧ 0 ≤ ε ∧ (∀ z, Estar ≤ f z + g z) ∧
        (∃ x, f x + g x = Estar) ∧
        (∀ z, ∃ a ∈ C,
          slack d g a z ≤ (1 - κ) / (4 * (1 + κ)) * (f z + g z - Estar + ε / 6)) ∧
        IsBestFirstRun d f g ε y m ∧ m = C.card + 1 := by
  refine ⟨discreteEnvelope 1, fun b => if b then 20 else 0, fun b => if b then 1 / 2 else 0,
    1 / 2, 1, 0, {false}, fun n => decide (n = 0), 2, discreteEnvelope_isEnvelope zero_le_one,
    ?_, by norm_num, by norm_num, ?_, zero_le_one, ?_, ⟨false, by norm_num⟩, ?_,
    bestFirst_instance_run, by simp⟩
  · intro u v
    cases u <;> cases v <;> simp [discreteEnvelope]
  · intro u v
    cases u <;> cases v <;> norm_num [discreteEnvelope]
  · intro z
    cases z <;> norm_num
  · intro z
    refine ⟨false, by simp, ?_⟩
    cases z <;> norm_num [slack, discreteEnvelope]

end MetricChain
