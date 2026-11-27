import Mathlib
import proofs.Core.Basic

/-!
# Dominance calculus: transport, thermal pruning, and gauge invariance

* `partition_transport` — **dominance transport lemma.**  If an injective map `T` sends a set of
  configurations `A` into a set `S` while lowering the energy by at least `γ`, then
  `Z(A) ≤ exp(-β γ) · Z(S)` at every inverse temperature `β ≥ 0`.  Dead-end elimination
  (uniform dominator), split DEE (context-dependent dominator), pair elimination and
  symmetry-based dominance are all instances: only injectivity of `T` matters.
* `partition_prune_bracket`, `freeEnergy_prune_bracket` — pruning a dominated set changes the
  partition function by a factor in `[1, 1 + exp(-β γ)]`, i.e. the free energy by at most
  `(1/β) log(1 + exp(-β γ))`; at `β → ∞` this is the classical statement that dominance pruning
  preserves the optimum (`min_transport`).
* `PairModel.energy_update`, `PairModel.goldstein_isLeast` — for pairwise models the energy
  difference of two states of a site is *separable* in the neighbours, hence Goldstein's criterion
  computes the **exact** dominance margin over product domains.
* `PairModel.energy_reparam`, `PairModel.goldstein_gauge_invariant` — the exact margin is a gauge
  invariant: no reparameterisation (LP-dual message passing, soft arc consistency) can change it.
* `PairModel.desmet_le_exactMargin`, `PairModel.desmet_optimalGauge` — the original
  Desmet bounds criterion is gauge dependent, never exceeds the exact margin, and attains it at an
  explicit gauge.  Hence "dual-reparameterised pruning" cannot beat Goldstein for pairwise models;
  it only matters for higher-order terms or non-product domains.
-/

namespace MetricChain

open Finset

/-! ### Dominance transport -/

section Transport

variable {Ω : Type*} [DecidableEq Ω]

/-- **Dominance transport lemma.** -/
theorem partition_transport {β γ : ℝ} (hβ : 0 ≤ β) (E : Ω → ℝ) {A S : Finset Ω} (T : Ω → Ω)
    (hinj : Set.InjOn T A) (hmaps : ∀ x ∈ A, T x ∈ S) (hdom : ∀ x ∈ A, E (T x) + γ ≤ E x) :
    partitionFn β E A ≤ Real.exp (-β * γ) * partitionFn β E S := by
  unfold partitionFn
  calc ∑ x ∈ A, Real.exp (-β * E x)
      ≤ ∑ x ∈ A, Real.exp (-β * γ) * Real.exp (-β * E (T x)) := by
        refine Finset.sum_le_sum fun x hx => ?_
        rw [← Real.exp_add]
        apply Real.exp_le_exp.mpr
        have := mul_le_mul_of_nonneg_left (hdom x hx) hβ
        linarith
    _ = Real.exp (-β * γ) * ∑ x ∈ A, Real.exp (-β * E (T x)) := by rw [Finset.mul_sum]
    _ = Real.exp (-β * γ) * ∑ y ∈ A.image T, Real.exp (-β * E y) := by
        rw [Finset.sum_image hinj]
    _ ≤ Real.exp (-β * γ) * ∑ y ∈ S, Real.exp (-β * E y) := by
        apply mul_le_mul_of_nonneg_left _ (Real.exp_pos _).le
        apply Finset.sum_le_sum_of_subset_of_nonneg
        · intro y hy
          obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hy
          exact hmaps x hx
        · intro _ _ _
          exact (Real.exp_pos _).le

/-- **Thermal pruning bracket.**  Removing a dominated set `A` (margin `γ`, dominance map into
the survivors `S`) changes the partition function by a factor between `1` and `1 + exp(-β γ)`. -/
theorem partition_prune_bracket {β γ : ℝ} (hβ : 0 ≤ β) (E : Ω → ℝ) {A S : Finset Ω} (T : Ω → Ω)
    (hinj : Set.InjOn T A) (hmaps : ∀ x ∈ A, T x ∈ S) (hdom : ∀ x ∈ A, E (T x) + γ ≤ E x)
    (hdisj : Disjoint A S) :
    partitionFn β E S ≤ partitionFn β E (A ∪ S) ∧
      partitionFn β E (A ∪ S) ≤ (1 + Real.exp (-β * γ)) * partitionFn β E S := by
  rw [partitionFn_union β E hdisj]
  have h1 := partition_transport hβ E T hinj hmaps hdom
  have h2 := partitionFn_nonneg β E A
  constructor
  · linarith
  · linarith

/-- **Many-to-one dominance transport.**  If `T` maps `A` into `S`, lowers the energy by at least
`γ`, and every fibre of `T` in `A` has at most `m` elements, then `Z(A) ≤ m · e^{-βγ} · Z(S)`. -/
theorem partition_transport_fibers {β γ : ℝ} (hβ : 0 ≤ β) (E : Ω → ℝ) {A S : Finset Ω} (T : Ω → Ω)
    (m : ℕ) (hfib : ∀ s ∈ S, (A.filter fun x => T x = s).card ≤ m)
    (hmaps : ∀ x ∈ A, T x ∈ S) (hdom : ∀ x ∈ A, E (T x) + γ ≤ E x) :
    partitionFn β E A ≤ m * (Real.exp (-β * γ) * partitionFn β E S) := by
  unfold partitionFn
  calc ∑ x ∈ A, Real.exp (-β * E x)
      ≤ ∑ x ∈ A, Real.exp (-β * γ) * Real.exp (-β * E (T x)) := by
        refine Finset.sum_le_sum fun x hx => ?_
        rw [← Real.exp_add]
        apply Real.exp_le_exp.mpr
        have := mul_le_mul_of_nonneg_left (hdom x hx) hβ
        linarith
    _ = ∑ s ∈ S, ∑ x ∈ A.filter (fun x => T x = s),
          Real.exp (-β * γ) * Real.exp (-β * E (T x)) :=
        (Finset.sum_fiberwise_of_maps_to hmaps _).symm
    _ = ∑ s ∈ S, ((A.filter fun x => T x = s).card : ℝ) *
          (Real.exp (-β * γ) * Real.exp (-β * E s)) := by
        apply Finset.sum_congr rfl
        intro s _
        have h : ∀ x ∈ A.filter (fun x => T x = s),
            Real.exp (-β * γ) * Real.exp (-β * E (T x)) =
              Real.exp (-β * γ) * Real.exp (-β * E s) := by
          intro x hx
          rw [(Finset.mem_filter.mp hx).2]
        rw [Finset.sum_congr rfl h, Finset.sum_const, nsmul_eq_mul]
    _ ≤ ∑ s ∈ S, (m : ℝ) * (Real.exp (-β * γ) * Real.exp (-β * E s)) := by
        apply Finset.sum_le_sum
        intro s hs
        apply mul_le_mul_of_nonneg_right _ (by positivity)
        exact_mod_cast hfib s hs
    _ = m * (Real.exp (-β * γ) * ∑ s ∈ S, Real.exp (-β * E s)) := by
        rw [← Finset.mul_sum, ← Finset.mul_sum]

/-- **Thermal pruning bracket, many-to-one form.**  Removing a set `A` whose configurations are
mapped at most `m`-to-one into the survivors `S` with margin `γ` changes the partition function
by a factor between `1` and `1 + m · exp(-β γ)`. -/
theorem partition_prune_bracket_fibers {β γ : ℝ} (hβ : 0 ≤ β) (E : Ω → ℝ) {A S : Finset Ω}
    (T : Ω → Ω) (m : ℕ) (hfib : ∀ s ∈ S, (A.filter fun x => T x = s).card ≤ m)
    (hmaps : ∀ x ∈ A, T x ∈ S) (hdom : ∀ x ∈ A, E (T x) + γ ≤ E x) (hdisj : Disjoint A S) :
    partitionFn β E S ≤ partitionFn β E (A ∪ S) ∧
      partitionFn β E (A ∪ S) ≤ (1 + m * Real.exp (-β * γ)) * partitionFn β E S := by
  rw [partitionFn_union β E hdisj]
  have h1 := partition_transport_fibers hβ E T m hfib hmaps hdom
  have h2 := partitionFn_nonneg β E A
  constructor
  · linarith
  · nlinarith

/-- **Free-energy form of thermal pruning.**  Pruning with margin `γ` raises the free energy by
at most `(1/β) log(1 + exp(-β γ))` and never lowers it. -/
theorem freeEnergy_prune_bracket {β γ : ℝ} (hβ : 0 < β) (E : Ω → ℝ) {A S : Finset Ω} (T : Ω → Ω)
    (hinj : Set.InjOn T A) (hmaps : ∀ x ∈ A, T x ∈ S) (hdom : ∀ x ∈ A, E (T x) + γ ≤ E x)
    (hdisj : Disjoint A S) (hS : S.Nonempty) :
    freeEnergy β E S - (1 / β) * Real.log (1 + Real.exp (-β * γ)) ≤ freeEnergy β E (A ∪ S) ∧
      freeEnergy β E (A ∪ S) ≤ freeEnergy β E S := by
  obtain ⟨hlo, hhi⟩ := partition_prune_bracket hβ.le E T hinj hmaps hdom hdisj
  have hZS := partitionFn_pos β E hS
  have hZU : 0 < partitionFn β E (A ∪ S) := lt_of_lt_of_le hZS hlo
  have hpos : 0 < 1 + Real.exp (-β * γ) := by positivity
  have hinv : 0 < 1 / β := by positivity
  unfold freeEnergy
  constructor
  · have h1 := Real.log_le_log hZU hhi
    rw [Real.log_mul hpos.ne' hZS.ne'] at h1
    nlinarith
  · have h1 := Real.log_le_log hZS hlo
    nlinarith

/-- **Zero-temperature limit.**  With a nonnegative margin, every pruned configuration is matched
by a survivor of no larger energy, so pruning preserves the optimal value. -/
theorem min_transport {γ : ℝ} (hγ : 0 ≤ γ) (E : Ω → ℝ) {A S : Finset Ω} (T : Ω → Ω)
    (hmaps : ∀ x ∈ A, T x ∈ S) (hdom : ∀ x ∈ A, E (T x) + γ ≤ E x) :
    ∀ x ∈ A ∪ S, ∃ y ∈ S, E y ≤ E x := by
  intro x hx
  rcases Finset.mem_union.mp hx with hA | hS
  · exact ⟨T x, hmaps x hA, by have := hdom x hA; linarith⟩
  · exact ⟨x, hS, le_rfl⟩

/-- Boltzmann average of an observable `f` over a finite configuration set. -/
noncomputable def boltzmannAvg (β : ℝ) (E f : Ω → ℝ) (S : Finset Ω) : ℝ :=
  (∑ x ∈ S, Real.exp (-β * E x) * f x) / partitionFn β E S

/-- **Ensemble averages under pruning.**  If the pruned set `A` carries at most the fraction `ρ`
of the Boltzmann weight of the survivors `S`, every observable bounded by `B` changes its
Boltzmann average by at most `2 B ρ` when `A` is discarded. -/
theorem boltzmannAvg_prune_error {β ρ B : ℝ} (E f : Ω → ℝ) {A S : Finset Ω}
    (hdisj : Disjoint A S) (hS : S.Nonempty)
    (hρ : partitionFn β E A ≤ ρ * partitionFn β E S) (hB : ∀ x ∈ A ∪ S, |f x| ≤ B) :
    |boltzmannAvg β E f (A ∪ S) - boltzmannAvg β E f S| ≤ 2 * B * ρ := by
  have hZS : 0 < partitionFn β E S := partitionFn_pos β E hS
  have hZA : 0 ≤ partitionFn β E A := partitionFn_nonneg β E A
  have hB0 : 0 ≤ B := by
    obtain ⟨x, hx⟩ := hS
    exact le_trans (abs_nonneg _) (hB x (Finset.mem_union_right A hx))
  have hρ0 : 0 ≤ ρ := by
    by_contra hneg
    have hlt : ρ < 0 := not_le.mp hneg
    nlinarith
  have hnum : ∀ T : Finset Ω, T ⊆ A ∪ S →
      |∑ x ∈ T, Real.exp (-β * E x) * f x| ≤ B * partitionFn β E T := by
    intro T hT
    unfold partitionFn
    rw [Finset.mul_sum]
    refine le_trans (Finset.abs_sum_le_sum_abs _ _) (Finset.sum_le_sum fun x hx => ?_)
    rw [abs_mul, abs_of_pos (Real.exp_pos _), mul_comm]
    exact mul_le_mul_of_nonneg_right (hB x (hT hx)) (Real.exp_pos _).le
  have hNA := hnum A Finset.subset_union_left
  have hNS := hnum S Finset.subset_union_right
  have havgU : boltzmannAvg β E f (A ∪ S) =
      ((∑ x ∈ A, Real.exp (-β * E x) * f x) + ∑ x ∈ S, Real.exp (-β * E x) * f x) /
        (partitionFn β E A + partitionFn β E S) := by
    unfold boltzmannAvg
    rw [partitionFn_union β E hdisj, Finset.sum_union hdisj]
  have halg : ∀ NA NS ZA ZS : ℝ, 0 ≤ ZA → 0 < ZS →
      (NA + NS) / (ZA + ZS) - NS / ZS = (NA * ZS - NS * ZA) / ((ZA + ZS) * ZS) := by
    intro NA NS ZA ZS hA hS'
    have h1 : ZA + ZS ≠ 0 := by positivity
    field_simp
    ring
  have hbound : ∀ NA NS ZA ZS : ℝ, 0 ≤ ZA → 0 < ZS → ZA ≤ ρ * ZS → |NA| ≤ B * ZA →
      |NS| ≤ B * ZS → |(NA * ZS - NS * ZA) / ((ZA + ZS) * ZS)| ≤ 2 * B * ρ := by
    intro NA NS ZA ZS hA hS' hr hNA' hNS'
    have hden : (0 : ℝ) < (ZA + ZS) * ZS := by positivity
    rw [abs_div, abs_of_pos hden, div_le_iff₀ hden]
    have h2 : |NA * ZS - NS * ZA| ≤ |NA| * ZS + |NS| * ZA := by
      calc |NA * ZS - NS * ZA| ≤ |NA * ZS| + |NS * ZA| := abs_sub _ _
        _ = |NA| * ZS + |NS| * ZA := by
          rw [abs_mul, abs_mul, abs_of_pos hS', abs_of_nonneg hA]
    have h3 : |NA| * ZS ≤ B * ZA * ZS := mul_le_mul_of_nonneg_right hNA' hS'.le
    have h4 : |NS| * ZA ≤ B * ZS * ZA := mul_le_mul_of_nonneg_right hNS' hA
    have h5 : B * ZA * ZS ≤ B * (ρ * ZS) * ZS :=
      mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hr hB0) hS'.le
    have h6 : 0 ≤ 2 * B * ρ * (ZA * ZS) := by positivity
    nlinarith
  rw [havgU]
  unfold boltzmannAvg
  rw [halg _ _ _ _ hZA hZS]
  exact hbound _ _ _ _ hZA hZS hρ hNA hNS

/-- **Thermal dominance controls observables.**  Pruning a dominated set with margin `γ` changes
the Boltzmann average of any observable bounded by `B` by at most `2 B exp(-β γ)`. -/
theorem boltzmannAvg_dominance_error {β γ B : ℝ} (hβ : 0 ≤ β) (E f : Ω → ℝ) {A S : Finset Ω}
    (T : Ω → Ω) (hinj : Set.InjOn T A) (hmaps : ∀ x ∈ A, T x ∈ S)
    (hdom : ∀ x ∈ A, E (T x) + γ ≤ E x) (hdisj : Disjoint A S) (hS : S.Nonempty)
    (hB : ∀ x ∈ A ∪ S, |f x| ≤ B) :
    |boltzmannAvg β E f (A ∪ S) - boltzmannAvg β E f S| ≤ 2 * B * Real.exp (-β * γ) :=
  boltzmannAvg_prune_error E f hdisj hS (partition_transport hβ E T hinj hmaps hdom) hB

end Transport

/-! ### Site-level dominance on product domains -/

section SiteDominance

variable {ι : Type*} [Fintype ι] [DecidableEq ι] {σ : ι → Type*} [∀ i, DecidableEq (σ i)]

omit [Fintype ι] in
/-- Replacing the state of site `i` by `t` is injective on configurations with `x i = r`
(this also holds for context-dependent dominators; see `update_dep_injOn`). -/
theorem update_injOn (i : ι) (r t : σ i) (B : Finset (∀ i, σ i)) :
    Set.InjOn (fun x : ∀ i, σ i => Function.update x i t) (B.filter fun x => x i = r) := by
  intro x hx y hy hxy
  have hx' : x i = r := (Finset.mem_filter.mp hx).2
  have hy' : y i = r := (Finset.mem_filter.mp hy).2
  funext j
  by_cases hj : j = i
  · subst hj
    rw [hx', hy']
  · have := congrFun hxy j
    simpa [Function.update_of_ne hj] using this

omit [Fintype ι] in
/-- Split dead-end elimination: the dominator may depend on the configuration (e.g. on the state
of a splitting site); the transport map is still injective on `{x | x i = r}`. -/
theorem update_dep_injOn (i : ι) (r : σ i) (t : (∀ i, σ i) → σ i) (B : Finset (∀ i, σ i)) :
    Set.InjOn (fun x : ∀ i, σ i => Function.update x i (t x)) (B.filter fun x => x i = r) := by
  intro x hx y hy hxy
  have hx' : x i = r := (Finset.mem_filter.mp hx).2
  have hy' : y i = r := (Finset.mem_filter.mp hy).2
  funext j
  by_cases hj : j = i
  · subst hj
    rw [hx', hy']
  · have := congrFun hxy j
    simpa [Function.update_of_ne hj] using this

/-- **Thermal dead-end elimination on a product domain.**  If state `r` of site `i` is dominated
by `t ≠ r` with margin `γ` on the box `∏ D`, then deleting `r` changes the partition function of
the box by a factor in `[1, 1 + exp(-β γ)]`. -/
theorem thermal_dee {β γ : ℝ} (hβ : 0 ≤ β) (E : (∀ i, σ i) → ℝ) (D : ∀ i, Finset (σ i)) (i : ι)
    (r t : σ i) (ht : t ∈ D i) (htr : t ≠ r)
    (hdom : ∀ x ∈ Fintype.piFinset D, x i = r → E (Function.update x i t) + γ ≤ E x) :
    partitionFn β E ((Fintype.piFinset D).filter fun x => x i ≠ r) ≤
        partitionFn β E (Fintype.piFinset D) ∧
      partitionFn β E (Fintype.piFinset D) ≤
        (1 + Real.exp (-β * γ)) * partitionFn β E ((Fintype.piFinset D).filter fun x => x i ≠ r) := by
  classical
  set B := Fintype.piFinset D
  set A := B.filter fun x => x i = r
  set S := B.filter fun x => x i ≠ r
  have hunion : A ∪ S = B := Finset.filter_union_filter_not_eq (fun x => x i = r) B
  have hdisj : Disjoint A S := Finset.disjoint_filter_filter_not B B (fun x => x i = r)
  have hmaps : ∀ x ∈ A, Function.update x i t ∈ S := by
    intro x hx
    have hxB : x ∈ B := (Finset.mem_filter.mp hx).1
    refine Finset.mem_filter.mpr ⟨?_, by simpa using htr⟩
    rw [Fintype.mem_piFinset] at hxB ⊢
    intro j
    by_cases hj : j = i
    · subst hj
      simpa using ht
    · rw [Function.update_of_ne hj]
      exact hxB j
  have hdom' : ∀ x ∈ A, E (Function.update x i t) + γ ≤ E x := fun x hx =>
    hdom x (Finset.mem_filter.mp hx).1 (Finset.mem_filter.mp hx).2
  have := partition_prune_bracket hβ E (fun x => Function.update x i t) (update_injOn i r t B)
    hmaps hdom' hdisj
  rwa [hunion] at this

end SiteDominance

/-! ### Higher-order terms: exact dominance factorises over blocks of the link graph -/

section Blocks

variable {ι : Type*} {σ : ι → Type*} {κ : Type*} [Fintype κ]

/-- **Block-separable minimisation.**  Let the sites be partitioned into blocks by `blk`, and let
`ℓ c` depend only on the coordinates of block `c`.  Over a product domain the minimum of
`∑ c, ℓ c` is the sum of the block minima.

For dead-end elimination with many-body terms this says: *the exact dominance margin of a site
factorises over the connected components of its link graph* (the graph on the neighbours in which
two neighbours are joined when they share a many-body term with the site).  Pairwise models are
the case of singleton blocks (Goldstein); chain-local 3-body terms give blocks of bounded size,
so exact dominance stays cheap; a single large block is a general pairwise minimisation problem
(coNP-hard to bound exactly). -/
theorem isLeast_sum_of_block_separable (D : ∀ j, Set (σ j)) (blk : ι → κ)
    (ℓ : κ → (∀ j, σ j) → ℝ)
    (hloc : ∀ c x y, (∀ j, blk j = c → x j = y j) → ℓ c x = ℓ c y) (m : κ → ℝ)
    (hm : ∀ c, IsLeast (ℓ c '' {x | ∀ j, x j ∈ D j}) (m c)) :
    IsLeast ((fun x => ∑ c, ℓ c x) '' {x | ∀ j, x j ∈ D j}) (∑ c, m c) := by
  constructor
  · -- glue the block minimisers
    have hex : ∀ c, ∃ x : ∀ j, σ j, (∀ j, x j ∈ D j) ∧ ℓ c x = m c := fun c => by
      obtain ⟨x, hx, hxm⟩ := (hm c).1
      exact ⟨x, hx, hxm⟩
    choose xs hxsD hxsm using hex
    refine ⟨fun j => xs (blk j) j, fun j => hxsD (blk j) j, ?_⟩
    simp only
    apply Finset.sum_congr rfl
    intro c _
    rw [← hxsm c]
    apply hloc
    intro j hj
    rw [hj]
  · rintro _ ⟨x, hx, rfl⟩
    exact Finset.sum_le_sum fun c _ => (hm c).2 ⟨x, hx, rfl⟩

/-- **Exact dominance with many-body terms.**  If the energy difference between states `r` and
`t` of site `i` is a constant plus a block-separable function of the context, the exact dominance
margin over a product domain is the constant plus the sum of the block minima. -/
theorem exact_margin_of_block_separable [DecidableEq ι] (E : (∀ j, σ j) → ℝ) (i : ι)
    (r t : σ i) (D : ∀ j, Set (σ j)) (blk : ι → κ) (c₀ : ℝ) (ℓ : κ → (∀ j, σ j) → ℝ)
    (hdiff : ∀ x, E (Function.update x i r) - E (Function.update x i t) = c₀ + ∑ c, ℓ c x)
    (hloc : ∀ c x y, (∀ j, blk j = c → x j = y j) → ℓ c x = ℓ c y) (m : κ → ℝ)
    (hm : ∀ c, IsLeast (ℓ c '' {x | ∀ j, x j ∈ D j}) (m c)) :
    IsLeast ((fun x => E (Function.update x i r) - E (Function.update x i t)) ''
        {x | ∀ j, x j ∈ D j}) (c₀ + ∑ c, m c) := by
  have h := isLeast_sum_of_block_separable D blk ℓ hloc m hm
  constructor
  · obtain ⟨x, hx, hxm⟩ := h.1
    refine ⟨x, hx, ?_⟩
    simp only at hxm ⊢
    rw [hdiff x, hxm]
  · rintro _ ⟨x, hx, rfl⟩
    simp only
    rw [hdiff x]
    have := h.2 ⟨x, hx, rfl⟩
    simp only at this
    linarith

end Blocks

/-! ### Pairwise models: separability, exactness of Goldstein, gauge invariance -/

/-- A pairwise energy model with scalars `R` over sites `ι` with state spaces `σ i`.  The pair
table `J i j` is used for every ordered pair `i ≠ j`.  (`R = ℝ` for the theory, `R = ℚ` for the
executable certificate kernel.) -/
structure PairModel (R : Type*) (ι : Type*) (σ : ι → Type*) where
  /-- one-body terms -/
  h : ∀ i, σ i → R
  /-- two-body terms on ordered pairs -/
  J : ∀ i j, σ i → σ j → R

namespace PairModel

variable {R : Type*} [CommRing R] {ι : Type*} [Fintype ι] [DecidableEq ι] {σ : ι → Type*}

/-- Total energy of a configuration. -/
def energy (M : PairModel R ι σ) (x : ∀ i, σ i) : R :=
  ∑ i, M.h i (x i) + ∑ i, ∑ j ∈ univ.erase i, M.J i j (x i) (x j)

/-- Local energy of state `a` at site `i` in context `x` (everything that involves site `i`). -/
def localE (M : PairModel R ι σ) (i : ι) (a : σ i) (x : ∀ i, σ i) : R :=
  M.h i a + ∑ j ∈ univ.erase i, (M.J i j a (x j) + M.J j i (x j) a)

/-- The part of the energy that does not involve site `i`. -/
def base (M : PairModel R ι σ) (i : ι) (x : ∀ i, σ i) : R :=
  ∑ k ∈ univ.erase i, M.h k (x k) +
    ∑ k ∈ univ.erase i, ∑ j ∈ (univ.erase k).erase i, M.J k j (x k) (x j)

/-- **Separability.**  The energy of `x[i ↦ a]` splits as a context-only part plus the local
energy of `a`; consequently energy *differences* at a site are sums of one-neighbour terms. -/
theorem energy_update (M : PairModel R ι σ) (x : ∀ i, σ i) (i : ι) (a : σ i) :
    M.energy (Function.update x i a) = M.base i x + M.localE i a x := by
  unfold energy base localE
  have hmem : i ∈ (univ : Finset ι) := mem_univ i
  rw [← Finset.add_sum_erase _ _ hmem, ← Finset.add_sum_erase univ
    (fun k => ∑ j ∈ univ.erase k, M.J k j (Function.update x i a k) (Function.update x i a j)) hmem]
  have h1 : ∑ k ∈ univ.erase i, M.h k (Function.update x i a k) = ∑ k ∈ univ.erase i, M.h k (x k) := by
    apply Finset.sum_congr rfl
    intro k hk
    rw [Function.update_of_ne (Finset.ne_of_mem_erase hk)]
  have h2 : ∑ j ∈ univ.erase i, M.J i j a (Function.update x i a j) =
      ∑ j ∈ univ.erase i, M.J i j a (x j) := by
    apply Finset.sum_congr rfl
    intro j hj
    rw [Function.update_of_ne (Finset.ne_of_mem_erase hj)]
  have h3 : ∑ k ∈ univ.erase i, ∑ j ∈ univ.erase k,
        M.J k j (Function.update x i a k) (Function.update x i a j) =
      ∑ k ∈ univ.erase i, (M.J k i (x k) a + ∑ j ∈ (univ.erase k).erase i, M.J k j (x k) (x j)) := by
    apply Finset.sum_congr rfl
    intro k hk
    have hki : k ≠ i := Finset.ne_of_mem_erase hk
    have hik : i ∈ univ.erase k := Finset.mem_erase.mpr ⟨fun h => hki h.symm, mem_univ i⟩
    rw [← Finset.add_sum_erase _ _ hik, Function.update_of_ne hki, Function.update_self]
    congr 1
    apply Finset.sum_congr rfl
    intro j hj
    rw [Function.update_of_ne (Finset.ne_of_mem_erase hj)]
  rw [Function.update_self, h1, h2, h3, Finset.sum_add_distrib, Finset.sum_add_distrib]
  ring

/-- Energy difference between two states of a site: context-separable. -/
theorem energy_update_sub (M : PairModel R ι σ) (x : ∀ i, σ i) (i : ι) (r t : σ i) :
    M.energy (Function.update x i r) - M.energy (Function.update x i t) =
      M.localE i r x - M.localE i t x := by
  rw [energy_update, energy_update]
  ring

/-- One-neighbour link term of the Goldstein criterion. -/
def link (M : PairModel R ι σ) (i : ι) (r t : σ i) (j : ι) (s : σ j) : R :=
  M.J i j r s + M.J j i s r - M.J i j t s - M.J j i s t

theorem localE_sub (M : PairModel R ι σ) (x : ∀ i, σ i) (i : ι) (r t : σ i) :
    M.localE i r x - M.localE i t x =
      M.h i r - M.h i t + ∑ j ∈ univ.erase i, M.link i r t j (x j) := by
  unfold localE link
  rw [add_sub_add_comm, ← Finset.sum_sub_distrib]
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- Reparameterisation (gauge transformation): move the message `msg i j` from the pair table
`J i j` into the unary table of `i`. -/
def reparam (M : PairModel R ι σ) (msg : ∀ i : ι, ι → σ i → R) : PairModel R ι σ where
  h i a := M.h i a + ∑ j ∈ univ.erase i, msg i j a
  J i j a b := M.J i j a b - msg i j a

/-- Reparameterisation leaves the energy function unchanged. -/
theorem energy_reparam (M : PairModel R ι σ) (msg : ∀ i : ι, ι → σ i → R) (x : ∀ i, σ i) :
    (M.reparam msg).energy x = M.energy x := by
  unfold energy reparam
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  ring

/-- **Goldstein's criterion is exact.**  Over a product domain `∏ D`, the minimum of the energy
difference `E(x[i ↦ r]) - E(x[i ↦ t])` over all contexts equals
`h i r - h i t + ∑_{j ≠ i} min_{s ∈ D j} link`: if `m j` is the least value of the link term on
`D j`, the Goldstein value is the *least element* of the set of energy differences. -/
theorem goldstein_isLeast (M : PairModel ℝ ι σ) (i : ι) (r t : σ i) (D : ∀ j, Set (σ j))
    (x₀ : ∀ j, σ j) (hx₀ : ∀ j, x₀ j ∈ D j) (m : ι → ℝ)
    (hm : ∀ j ∈ univ.erase i, IsLeast (M.link i r t j '' D j) (m j)) :
    IsLeast ((fun x => M.energy (Function.update x i r) - M.energy (Function.update x i t)) ''
        {x | ∀ j, x j ∈ D j})
      (M.h i r - M.h i t + ∑ j ∈ univ.erase i, m j) := by
  classical
  constructor
  · -- attained: pick a minimiser at each neighbour
    have hex : ∀ j, ∃ s, s ∈ D j ∧ (j ∈ univ.erase i → M.link i r t j s = m j) := by
      intro j
      by_cases hj : j ∈ univ.erase i
      · obtain ⟨s, hs, hsm⟩ := (hm j hj).1
        exact ⟨s, hs, fun _ => hsm⟩
      · exact ⟨x₀ j, hx₀ j, fun h => absurd h hj⟩
    choose s hsD hsm using hex
    refine ⟨s, hsD, ?_⟩
    simp only
    rw [energy_update_sub, localE_sub]
    congr 1
    exact Finset.sum_congr rfl fun j hj => hsm j hj
  · rintro _ ⟨x, hx, rfl⟩
    simp only
    rw [energy_update_sub, localE_sub]
    have : ∑ j ∈ univ.erase i, m j ≤ ∑ j ∈ univ.erase i, M.link i r t j (x j) :=
      Finset.sum_le_sum fun j hj => (hm j hj).2 ⟨x j, hx j, rfl⟩
    linarith

/-- **Gauge invariance of the Goldstein value.**  Whatever messages are applied, the Goldstein
value computed from the reparameterised tables is the same number. -/
theorem goldstein_gauge_invariant (M : PairModel ℝ ι σ) (msg : ∀ i : ι, ι → σ i → ℝ) (i : ι) (r t : σ i)
    (D : ∀ j, Set (σ j)) (x₀ : ∀ j, σ j) (hx₀ : ∀ j, x₀ j ∈ D j) (m m' : ι → ℝ)
    (hm : ∀ j ∈ univ.erase i, IsLeast (M.link i r t j '' D j) (m j))
    (hm' : ∀ j ∈ univ.erase i, IsLeast ((M.reparam msg).link i r t j '' D j) (m' j)) :
    (M.reparam msg).h i r - (M.reparam msg).h i t + ∑ j ∈ univ.erase i, m' j =
      M.h i r - M.h i t + ∑ j ∈ univ.erase i, m j := by
  have h1 := goldstein_isLeast M i r t D x₀ hx₀ m hm
  have h2 := goldstein_isLeast (M.reparam msg) i r t D x₀ hx₀ m' hm'
  simp only [energy_reparam] at h2
  exact h2.unique h1

/-- Exact dominance margin of `r` against `t` at site `i` over a finite set of contexts. -/
noncomputable def exactMargin (M : PairModel ℝ ι σ) (i : ι) (r t : σ i) (B : Finset (∀ j, σ j))
    (hB : B.Nonempty) : ℝ :=
  B.inf' hB fun x => M.localE i r x - M.localE i t x

/-- Desmet's original bounds criterion: best case of `r` minus worst case of `t`. -/
noncomputable def desmet (M : PairModel ℝ ι σ) (i : ι) (r t : σ i) (B : Finset (∀ j, σ j))
    (hB : B.Nonempty) : ℝ :=
  B.inf' hB (fun x => M.localE i r x) - B.sup' hB (fun x => M.localE i t x)

/-- The exact margin is the minimum of the true energy differences. -/
theorem exactMargin_eq (M : PairModel ℝ ι σ) (i : ι) (r t : σ i) (B : Finset (∀ j, σ j))
    (hB : B.Nonempty) :
    M.exactMargin i r t B hB =
      B.inf' hB fun x => M.energy (Function.update x i r) - M.energy (Function.update x i t) := by
  unfold exactMargin
  congr 1
  funext x
  rw [energy_update_sub]

/-- The exact margin is a gauge invariant. -/
theorem exactMargin_reparam (M : PairModel ℝ ι σ) (msg : ∀ i : ι, ι → σ i → ℝ) (i : ι) (r t : σ i)
    (B : Finset (∀ j, σ j)) (hB : B.Nonempty) :
    (M.reparam msg).exactMargin i r t B hB = M.exactMargin i r t B hB := by
  rw [exactMargin_eq, exactMargin_eq]
  simp only [energy_reparam]

/-- Desmet's criterion never exceeds the exact margin, in any gauge. -/
theorem desmet_le_exactMargin (M : PairModel ℝ ι σ) (i : ι) (r t : σ i) (B : Finset (∀ j, σ j))
    (hB : B.Nonempty) : M.desmet i r t B hB ≤ M.exactMargin i r t B hB := by
  unfold desmet exactMargin
  apply Finset.le_inf'
  intro x hx
  have h1 := Finset.inf'_le (fun x => M.localE i r x) hx
  have h2 := Finset.le_sup' (fun x => M.localE i t x) hx
  linarith

/-- In every gauge Desmet's criterion is bounded by the (gauge-invariant) exact margin. -/
theorem desmet_reparam_le (M : PairModel ℝ ι σ) (msg : ∀ i : ι, ι → σ i → ℝ) (i : ι) (r t : σ i)
    (B : Finset (∀ j, σ j)) (hB : B.Nonempty) :
    (M.reparam msg).desmet i r t B hB ≤ M.exactMargin i r t B hB := by
  rw [← exactMargin_reparam M msg i r t B hB]
  exact desmet_le_exactMargin _ i r t B hB

/-- The gauge that makes the local energy of `t` at site `i` context independent. -/
def optimalGauge (M : PairModel ℝ ι σ) (i : ι) (t : σ i) : ∀ a : ι, ι → σ a → ℝ :=
  fun a b s => if b = i ∧ a ≠ i then M.J i a t s + M.J a i s t else 0

theorem localE_optimalGauge (M : PairModel ℝ ι σ) (i : ι) (t : σ i) (x : ∀ j, σ j) :
    (M.reparam (M.optimalGauge i t)).localE i t x = M.h i t := by
  have hh : (M.reparam (M.optimalGauge i t)).h i t = M.h i t := by
    show M.h i t + ∑ j ∈ univ.erase i, M.optimalGauge i t i j t = M.h i t
    have h0 : ∑ j ∈ univ.erase i, M.optimalGauge i t i j t = 0 := by
      apply Finset.sum_eq_zero
      intro j _
      simp [optimalGauge]
    rw [h0, add_zero]
  have hs : ∑ j ∈ univ.erase i, ((M.reparam (M.optimalGauge i t)).J i j t (x j) +
      (M.reparam (M.optimalGauge i t)).J j i (x j) t) = 0 := by
    apply Finset.sum_eq_zero
    intro j hj
    have hji : j ≠ i := Finset.ne_of_mem_erase hj
    have e1 : M.optimalGauge i t i j t = 0 := by simp [optimalGauge]
    have e2 : M.optimalGauge i t j i (x j) = M.J i j t (x j) + M.J j i (x j) t := by
      simp [optimalGauge, hji]
    show M.J i j t (x j) - M.optimalGauge i t i j t +
      (M.J j i (x j) t - M.optimalGauge i t j i (x j)) = 0
    rw [e1, e2]
    ring
  show (M.reparam (M.optimalGauge i t)).h i t + ∑ j ∈ univ.erase i,
    ((M.reparam (M.optimalGauge i t)).J i j t (x j) +
      (M.reparam (M.optimalGauge i t)).J j i (x j) t) = M.h i t
  rw [hh, hs, add_zero]

/-- **Goldstein is the gauge-optimal Desmet criterion.**  At the explicit gauge `optimalGauge`
Desmet's criterion equals the exact (Goldstein) margin. -/
theorem desmet_optimalGauge (M : PairModel ℝ ι σ) (i : ι) (r t : σ i) (B : Finset (∀ j, σ j))
    (hB : B.Nonempty) :
    (M.reparam (M.optimalGauge i t)).desmet i r t B hB = M.exactMargin i r t B hB := by
  rw [← exactMargin_reparam M (M.optimalGauge i t) i r t B hB]
  unfold desmet exactMargin
  simp only [localE_optimalGauge]
  rw [Finset.sup'_const]
  apply le_antisymm
  · apply Finset.le_inf'
    intro x hx
    have := Finset.inf'_le (fun x => (M.reparam (M.optimalGauge i t)).localE i r x) hx
    linarith
  · have h : B.inf' hB (fun x => (M.reparam (M.optimalGauge i t)).localE i r x - M.h i t) + M.h i t ≤
        B.inf' hB fun x => (M.reparam (M.optimalGauge i t)).localE i r x := by
      apply Finset.le_inf'
      intro x hx
      have := Finset.inf'_le
        (fun x => (M.reparam (M.optimalGauge i t)).localE i r x - M.h i t) hx
      linarith
    linarith

end PairModel

end MetricChain
