import Mathlib
import proofs.Frontiers.VoxelEnclosure
import proofs.Core.Rounding

/-!
# Voxel bridge: from energy enclosures to certified continuous partition functions

`certified_voxel_partition` (`VoxelEnclosure.lean`) turns two accepted `ZCert`s into a two-sided
rational enclosure of a continuous partition integral, but it *assumes* its hypothesis `hb`: the
weights of the two rational instances bracket the Boltzmann integral of every voxel.  This file
derives `hb` from quantities a certificate producer can actually enclose, and closes the pipeline
for product voxels in torsion coordinates.

## The abstract bridge (one voxel)

* `voxel_boltzmann_integrableOn` — a measurable energy that is bounded below on a measurable
  voxel of finite volume has an integrable Boltzmann factor (for `β ≥ 0`); this discharges the
  integrability hypothesis of `voxel_boltzmann_bounds`.
* `pairwise_voxel_weight_bounds` — **the bridge**.  If on the voxel `V x` the energy is enclosed
  by the energies `Mlo.energy x ≤ E ≤ Mhi.energy x` of two real pairwise *table* models, the
  volume factorises as `vol(V x) = ∏ i, vol i (x i)`, and the rational factors of `Ilo` / `Ihi`
  are outward-rounded brackets of `vol i a · exp(-β h i a)` and `exp(-β J i j a b)`, then
  `Ilo.weight x ≤ ∫_{V x} exp(-β E) ≤ Ihi.weight x`.  This is exactly `hb`.

## Product voxels in torsion coordinates

On `Fin n → ℝ` with a product measure `Measure.pi ν` and cells `s i a ⊆ ℝ` (`a : Fin k`) the voxel
of a configuration `x` is `prodVoxel s x = ∏ i, s i (x i)`.

* `measurableSet_prodVoxel`, `measure_prodVoxel`, `measure_prodVoxel_ne_top`,
  `toReal_measure_prodVoxel` — measurability and factorised (finite) volume;
* `prodVoxel_disjoint` — distinct configurations have disjoint voxels when the cells of every
  coordinate are pairwise disjoint;
* `iUnion_prodVoxel_boxFinset`, `iUnion_prodVoxel_fullDom` — the voxels of a box tile the product
  domain `∏ i, ⋃ a, s i a`;
* `torsionEnergy u U` — the pairwise energy `∑ i, u i (θ i) + ∑ i, ∑ j ≠ i, U i j (θ i) (θ j)`
  on the continuous configuration space (the shape of `PairModel.energy`; only measurability of
  the terms is ever required), `measurable_torsionEnergy`, and `torsionEnergy_voxel_bounds`:
  cellwise table enclosures of the terms `u i`, `U i j` enclose the energy on every product voxel;
* `integrableOn_prodVoxel_boltzmann` — integrability of the Boltzmann factor on a product voxel.

## End-to-end theorems

* `certified_prodVoxel_partition` — for any measurable energy enclosed voxelwise by two pairwise
  table models: outward-rounded rational instances plus two accepted certificates give a
  two-sided rational enclosure of `∫ exp(-β E)` over the union of the voxels of the box.
* `certified_torsion_partition` — the same for a pairwise energy `torsionEnergy u U`, with the
  voxelwise enclosure *derived* from cellwise enclosures of the one- and two-body terms.
  Its hypotheses are: (i) regularity (measurable, pairwise disjoint cells of finite measure,
  measurable energy terms); (ii) cellwise enclosures of the terms `u i`, `U i j` by two real
  tables (the output of interval arithmetic over a cell); (iii) entrywise outward-rounded
  brackets of the Boltzmann factors (`QInterval.contains_boltzmann` in `Core/Rounding.lean`, and
  `volume_chartArc_toReal_bounds` below for the volume factors); (iv) two kernel computations
  `zverify … = some …`.  No statement about voxel integrals is assumed any more.
* `certified_torsion_partition_box` — the same with enclosures required only on the cells of the
  box (removed cells, e.g. sterically excluded ones, need none);
  `certified_torsion_partition_top` — additionally with the top-level kernel `zverifyTop`, so
  that no nonnegativity hypothesis is left to the caller.
* `certified_torsion_partition_full` — the full box: the integral over `∏ i, ⋃ a, s i a`.

## Chart arcs: rational bounds for the volume factors

With the rational atlas of the circle (`circParam`, `Core/Rounding.lean`) a cell with chart
endpoints `t₁ ≤ t₂` is the arc of angles `[2 arctan t₁, 2 arctan t₂)`.

* `two_arctan_sub_bounds_of_sq`, `two_arctan_sub_bounds` — rational enclosure of the angular
  measure `2 (arctan t₂ - arctan t₁)` (no transcendental function has to be evaluated);
* `volume_chartArc`, `volume_chartArc_toReal_bounds` — the Lebesgue volume of the arc and its
  rational bounds (the factors `vol i a` of the bridge);
* `chartArc_onebody_brackets` — computable rational brackets of `vol · exp(q)` for a chart arc
  (volume bounds times the `exp` enclosure of `Core/Rounding.lean`): the one-body hypotheses of
  the end-to-end theorem in executable form;
* `chartArc_onebody_brackets_of_sq`, `chartArc_onebody_brackets_pos`,
  `chartArc_onebody_brackets_neg` — the same with the upper volume bound `(t₂ - t₁)·2/(1 + m²)`,
  whose ratio to the lower bound tends to `1` when the arc is subdivided (the crude bound
  `2 (t₂ - t₁)` of `chartArc_onebody_brackets` does not improve under subdivision);
* `circParam_two_arctan`, `chartArc_param_mem` — the chart point `circParam t` sits at the angle
  `2 arctan t`, and every angle of the arc has its chart parameter in `[t₁, t₂)`.

## Non-vacuity

Three instances of `certified_torsion_partition_full` with kernel-checked certificates
(namespace `VoxelBridgeWitness`), so its hypotheses are jointly satisfiable:

* `exact_witness` — one coordinate, zero energy: the enclosure of `∫_{[0, 2)} 1 = 2` is `[2, 2]`;
* `pair_witness` — two coupled coordinates, non-degenerate table enclosures, outward-rounded
  factors, enumeration certificates: `937/1024 ≤ ∫ exp(-E) ≤ 6289/2025`;
* `chart_witness` — the torsion potential `cos θ` on two chart arcs with rational chart endpoints;
  all tables, volume bounds and Boltzmann brackets are computed by the interval layer.
-/

namespace MetricChain

open MeasureTheory Finset

/-! ### The abstract bridge -/

section Bridge

/-- **Integrability of the Boltzmann factor on a voxel.**  If the energy is measurable and bounded
below on a measurable voxel of finite volume, then `exp(-β E)` is integrable on the voxel for every
`β ≥ 0`.  This discharges the hypothesis `hint` of `voxel_boltzmann_bounds`. -/
theorem voxel_boltzmann_integrableOn {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) {V : Set Ω}
    (hV : MeasurableSet V) (hfin : μ V ≠ ⊤) {E : Ω → ℝ} (hE : Measurable E) {β Elo : ℝ}
    (hβ : 0 ≤ β) (hlo : ∀ ω ∈ V, Elo ≤ E ω) :
    IntegrableOn (fun ω => Real.exp (-β * E ω)) V μ := by
  refine Measure.integrableOn_of_bounded hfin ?_ (M := Real.exp (-β * Elo)) ?_
  · exact (Real.measurable_exp.comp (hE.const_mul (-β))).aestronglyMeasurable
  · refine ae_restrict_of_forall_mem hV fun ω hω => ?_
    rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
    apply Real.exp_le_exp.mpr
    have := mul_le_mul_of_nonneg_left (hlo ω hω) hβ
    linarith

/-- **Voxel bridge.**  Voxel-table enclosures of the energy (`Mlo.energy x ≤ E ≤ Mhi.energy x` on
the voxel `V x`), a factorised volume `vol(V x) = ∏ i, vol i (x i)` and outward-rounded rational
Boltzmann factors (`Ilo.w ≤ vol · exp(-β h_hi)`, `Ilo.W ≤ exp(-β J_hi)`,
`vol · exp(-β h_lo) ≤ Ihi.w`, `exp(-β J_lo) ≤ Ihi.W`) imply that the rational weights bracket the
Boltzmann integral of the voxel.  This is exactly the hypothesis `hb` of
`Z_encloses_voxel_integral` and `certified_voxel_partition`. -/
theorem pairwise_voxel_weight_bounds {Ω : Type*} [MeasurableSpace Ω] {n k : ℕ} (μ : Measure Ω)
    (V : Config n k → Set Ω) (vol : Fin n → Fin k → ℝ) (hvol0 : ∀ i a, 0 ≤ vol i a)
    (E : Ω → ℝ) {β : ℝ} (hβ : 0 ≤ β) (Mlo Mhi : PairModel ℝ (Fin n) (fun _ => Fin k))
    (Ilo Ihi : WInstance n k) (hlo : Ilo.Nonneg)
    (hwlo : ∀ i a, (Ilo.w i a : ℝ) ≤ vol i a * Real.exp (-β * Mhi.h i a))
    (hWlo : ∀ i j a b, (Ilo.W i j a b : ℝ) ≤ Real.exp (-β * Mhi.J i j a b))
    (hwhi : ∀ i a, vol i a * Real.exp (-β * Mlo.h i a) ≤ (Ihi.w i a : ℝ))
    (hWhi : ∀ i j a b, Real.exp (-β * Mlo.J i j a b) ≤ (Ihi.W i j a b : ℝ))
    (x : Config n k) (hmeas : MeasurableSet (V x)) (hfin : μ (V x) ≠ ⊤)
    (hvol : (μ (V x)).toReal = ∏ i, vol i (x i))
    (hint : IntegrableOn (fun ω => Real.exp (-β * E ω)) (V x) μ)
    (hElo : ∀ ω ∈ V x, Mlo.energy x ≤ E ω) (hEhi : ∀ ω ∈ V x, E ω ≤ Mhi.energy x) :
    ((Ilo.weight x : ℚ) : ℝ) ≤ ∫ ω in V x, Real.exp (-β * E ω) ∂μ ∧
      ∫ ω in V x, Real.exp (-β * E ω) ∂μ ≤ ((Ihi.weight x : ℚ) : ℝ) := by
  obtain ⟨h1, h2⟩ := voxel_boltzmann_bounds μ hmeas hfin E hβ hint hElo hEhi
  -- volume times Boltzmann factor of a table model, as a product over sites and ordered pairs
  have hfac : ∀ M : PairModel ℝ (Fin n) (fun _ => Fin k),
      (μ (V x)).toReal * Real.exp (-β * M.energy x) =
        (∏ i, vol i (x i) * Real.exp (-β * M.h i (x i))) *
          ∏ i, ∏ j ∈ univ.erase i, Real.exp (-β * M.J i j (x i) (x j)) := by
    intro M
    have hexp : Real.exp (-β * M.energy x) =
        (∏ i, Real.exp (-β * M.h i (x i))) *
          ∏ i, ∏ j ∈ univ.erase i, Real.exp (-β * M.J i j (x i) (x j)) := by
      unfold PairModel.energy
      rw [mul_add, Real.exp_add, Finset.mul_sum, Real.exp_sum, Finset.mul_sum, Real.exp_sum]
      congr 1
      apply Finset.prod_congr rfl
      intro i _
      rw [Finset.mul_sum, Real.exp_sum]
    rw [hvol, hexp, Finset.prod_mul_distrib, mul_assoc]
  rw [hfac Mhi] at h1
  rw [hfac Mlo] at h2
  unfold WInstance.weight
  push_cast
  constructor
  · refine le_trans ?_ h1
    apply mul_le_mul
    · exact Finset.prod_le_prod (fun i _ => by exact_mod_cast hlo.1 i (x i))
        fun i _ => hwlo i (x i)
    · apply Finset.prod_le_prod
      · intro i _
        exact Finset.prod_nonneg fun j _ => by exact_mod_cast hlo.2 i j (x i) (x j)
      · intro i _
        exact Finset.prod_le_prod (fun j _ => by exact_mod_cast hlo.2 i j (x i) (x j))
          fun j _ => hWlo i j (x i) (x j)
    · exact Finset.prod_nonneg fun i _ =>
        Finset.prod_nonneg fun j _ => by exact_mod_cast hlo.2 i j (x i) (x j)
    · exact Finset.prod_nonneg fun i _ => mul_nonneg (hvol0 i (x i)) (Real.exp_pos _).le
  · refine le_trans h2 ?_
    apply mul_le_mul
    · exact Finset.prod_le_prod
        (fun i _ => mul_nonneg (hvol0 i (x i)) (Real.exp_pos _).le) fun i _ => hwhi i (x i)
    · apply Finset.prod_le_prod
      · intro i _
        exact Finset.prod_nonneg fun j _ => (Real.exp_pos _).le
      · intro i _
        exact Finset.prod_le_prod (fun j _ => (Real.exp_pos _).le)
          fun j _ => hWhi i j (x i) (x j)
    · exact Finset.prod_nonneg fun i _ => Finset.prod_nonneg fun j _ => (Real.exp_pos _).le
    · exact Finset.prod_nonneg fun i _ =>
        le_trans (mul_nonneg (hvol0 i (x i)) (Real.exp_pos _).le) (hwhi i (x i))

end Bridge

/-! ### Product voxels in torsion coordinates -/

section ProductVoxels

variable {n k : ℕ}

/-- The product voxel of the configuration `x`: coordinate `i` ranges over the cell `s i (x i)`. -/
def prodVoxel (s : Fin n → Fin k → Set ℝ) (x : Config n k) : Set (Fin n → ℝ) :=
  Set.univ.pi fun i => s i (x i)

/-- Membership in a product voxel is coordinatewise membership in the cells. -/
theorem mem_prodVoxel {s : Fin n → Fin k → Set ℝ} {x : Config n k} {θ : Fin n → ℝ} :
    θ ∈ prodVoxel s x ↔ ∀ i, θ i ∈ s i (x i) := by
  simp [prodVoxel]

/-- A product voxel of measurable cells is measurable. -/
theorem measurableSet_prodVoxel {s : Fin n → Fin k → Set ℝ} (hs : ∀ i a, MeasurableSet (s i a))
    (x : Config n k) : MeasurableSet (prodVoxel s x) :=
  MeasurableSet.univ_pi fun i => hs i (x i)

/-- The volume of a product voxel is the product of the cell measures. -/
theorem measure_prodVoxel (ν : Fin n → Measure ℝ) [∀ i, SigmaFinite (ν i)]
    (s : Fin n → Fin k → Set ℝ) (x : Config n k) :
    Measure.pi ν (prodVoxel s x) = ∏ i, ν i (s i (x i)) :=
  Measure.pi_pi ν _

/-- A product voxel of cells of finite measure has finite volume. -/
theorem measure_prodVoxel_ne_top (ν : Fin n → Measure ℝ) [∀ i, SigmaFinite (ν i)]
    {s : Fin n → Fin k → Set ℝ} (hfin : ∀ i a, ν i (s i a) ≠ ⊤) (x : Config n k) :
    Measure.pi ν (prodVoxel s x) ≠ ⊤ := by
  rw [measure_prodVoxel]
  exact ENNReal.prod_ne_top fun i _ => hfin i (x i)

/-- Real-valued form of `measure_prodVoxel`: the volume factorises over the sites, as required by
the hypothesis `hvol` of `pairwise_voxel_weight_bounds`. -/
theorem toReal_measure_prodVoxel (ν : Fin n → Measure ℝ) [∀ i, SigmaFinite (ν i)]
    (s : Fin n → Fin k → Set ℝ) (x : Config n k) :
    (Measure.pi ν (prodVoxel s x)).toReal = ∏ i, (ν i (s i (x i))).toReal := by
  rw [measure_prodVoxel, ENNReal.toReal_prod]

/-- If the cells of every coordinate are pairwise disjoint, the product voxels of distinct
configurations are disjoint. -/
theorem prodVoxel_disjoint {s : Fin n → Fin k → Set ℝ}
    (hdisj : ∀ i a b, a ≠ b → Disjoint (s i a) (s i b)) {x y : Config n k} (hxy : x ≠ y) :
    Disjoint (prodVoxel s x) (prodVoxel s y) := by
  obtain ⟨i, hi⟩ := Function.ne_iff.mp hxy
  rw [Set.disjoint_left]
  intro θ hx hy
  exact Set.disjoint_left.mp (hdisj i _ _ hi) (mem_prodVoxel.mp hx i) (mem_prodVoxel.mp hy i)

/-- The voxels of a box tile the product of the unions of the surviving cells. -/
theorem iUnion_prodVoxel_boxFinset (s : Fin n → Fin k → Set ℝ) (D : Dom n k) :
    ⋃ x ∈ boxFinset D, prodVoxel s x = Set.univ.pi fun i => ⋃ a ∈ D i, s i a := by
  ext θ
  simp only [Set.mem_iUnion, mem_prodVoxel, Set.mem_univ_pi, mem_boxFinset, exists_prop]
  constructor
  · rintro ⟨x, hx, hθ⟩ i
    exact ⟨x i, hx i, hθ i⟩
  · intro h
    choose x hx using h
    exact ⟨x, fun i => (hx i).1, fun i => (hx i).2⟩

/-- The voxels of the full box tile the whole product domain `∏ i, ⋃ a, s i a`. -/
theorem iUnion_prodVoxel_fullDom (s : Fin n → Fin k → Set ℝ) :
    ⋃ x ∈ boxFinset (fullDom n k), prodVoxel s x = Set.univ.pi fun i => ⋃ a, s i a := by
  rw [iUnion_prodVoxel_boxFinset]
  congr 1
  funext i
  ext t
  simp [fullDom]

/-- Pairwise energy on the continuous configuration space `Fin n → ℝ` (torsion coordinates):
one-body terms `u i` and two-body terms `U i j` on ordered pairs `i ≠ j` (the diagonal `U i i` is
ignored), the same shape as `PairModel.energy`. -/
def torsionEnergy (u : Fin n → ℝ → ℝ) (U : Fin n → Fin n → ℝ → ℝ → ℝ) (θ : Fin n → ℝ) : ℝ :=
  ∑ i, u i (θ i) + ∑ i, ∑ j ∈ univ.erase i, U i j (θ i) (θ j)

/-- `torsionEnergy u U` is the energy of the pairwise model with continuous state spaces whose
tables are `u` and `U`. -/
theorem torsionEnergy_eq_energy (u : Fin n → ℝ → ℝ) (U : Fin n → Fin n → ℝ → ℝ → ℝ)
    (θ : Fin n → ℝ) :
    torsionEnergy u U θ = (⟨u, U⟩ : PairModel ℝ (Fin n) (fun _ => ℝ)).energy θ := rfl

/-- A pairwise energy with measurable one-body terms and (jointly) measurable two-body terms is
measurable. -/
theorem measurable_torsionEnergy {u : Fin n → ℝ → ℝ} {U : Fin n → Fin n → ℝ → ℝ → ℝ}
    (hu : ∀ i, Measurable (u i)) (hU : ∀ i j, j ≠ i → Measurable (Function.uncurry (U i j))) :
    Measurable (torsionEnergy u U) := by
  unfold torsionEnergy
  apply Measurable.add
  · exact Finset.measurable_sum _ fun i _ => (hu i).comp (measurable_pi_apply i)
  · refine Finset.measurable_sum _ fun i _ => Finset.measurable_sum _ fun j hj => ?_
    have hpair : Measurable fun θ : Fin n → ℝ => (θ i, θ j) :=
      (measurable_pi_apply i).prodMk (measurable_pi_apply j)
    exact (hU i j (Finset.ne_of_mem_erase hj)).comp hpair

/-- **Energy enclosure on a product voxel.**  If the tables of `Mlo` and `Mhi` enclose the
one-body terms on every cell and the two-body terms on every pair of cells (`j ≠ i`), then the
table energies of the configuration `x` enclose `torsionEnergy u U` on the whole voxel of `x`. -/
theorem torsionEnergy_voxel_bounds {s : Fin n → Fin k → Set ℝ} {u : Fin n → ℝ → ℝ}
    {U : Fin n → Fin n → ℝ → ℝ → ℝ} {Mlo Mhi : PairModel ℝ (Fin n) (fun _ => Fin k)}
    (hu : ∀ i a, ∀ t ∈ s i a, Mlo.h i a ≤ u i t ∧ u i t ≤ Mhi.h i a)
    (hU : ∀ i j, j ≠ i → ∀ a b, ∀ t ∈ s i a, ∀ t' ∈ s j b,
      Mlo.J i j a b ≤ U i j t t' ∧ U i j t t' ≤ Mhi.J i j a b)
    (x : Config n k) {θ : Fin n → ℝ} (hθ : θ ∈ prodVoxel s x) :
    Mlo.energy x ≤ torsionEnergy u U θ ∧ torsionEnergy u U θ ≤ Mhi.energy x := by
  have hθ' := mem_prodVoxel.mp hθ
  unfold PairModel.energy torsionEnergy
  constructor
  · apply add_le_add
    · exact Finset.sum_le_sum fun i _ => (hu i (x i) (θ i) (hθ' i)).1
    · exact Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j hj =>
        (hU i j (Finset.ne_of_mem_erase hj) (x i) (x j) (θ i) (hθ' i) (θ j) (hθ' j)).1
  · apply add_le_add
    · exact Finset.sum_le_sum fun i _ => (hu i (x i) (θ i) (hθ' i)).2
    · exact Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j hj =>
        (hU i j (Finset.ne_of_mem_erase hj) (x i) (x j) (θ i) (hθ' i) (θ j) (hθ' j)).2

/-- **Energy enclosure on a product voxel, per configuration.**  The sharper form of
`torsionEnergy_voxel_bounds`: only the table entries selected by the configuration `x` and only
the cells `s i (x i)` of its voxel are involved. -/
theorem torsionEnergy_config_bounds {s : Fin n → Fin k → Set ℝ} {u : Fin n → ℝ → ℝ}
    {U : Fin n → Fin n → ℝ → ℝ → ℝ} {Mlo Mhi : PairModel ℝ (Fin n) (fun _ => Fin k)}
    (x : Config n k)
    (hu : ∀ i, ∀ t ∈ s i (x i), Mlo.h i (x i) ≤ u i t ∧ u i t ≤ Mhi.h i (x i))
    (hU : ∀ i j, j ≠ i → ∀ t ∈ s i (x i), ∀ t' ∈ s j (x j),
      Mlo.J i j (x i) (x j) ≤ U i j t t' ∧ U i j t t' ≤ Mhi.J i j (x i) (x j))
    {θ : Fin n → ℝ} (hθ : θ ∈ prodVoxel s x) :
    Mlo.energy x ≤ torsionEnergy u U θ ∧ torsionEnergy u U θ ≤ Mhi.energy x := by
  have hθ' := mem_prodVoxel.mp hθ
  unfold PairModel.energy torsionEnergy
  constructor
  · apply add_le_add
    · exact Finset.sum_le_sum fun i _ => (hu i (θ i) (hθ' i)).1
    · exact Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j hj =>
        (hU i j (Finset.ne_of_mem_erase hj) (θ i) (hθ' i) (θ j) (hθ' j)).1
  · apply add_le_add
    · exact Finset.sum_le_sum fun i _ => (hu i (θ i) (hθ' i)).2
    · exact Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j hj =>
        (hU i j (Finset.ne_of_mem_erase hj) (θ i) (hθ' i) (θ j) (hθ' j)).2

/-- **Integrability on a product voxel.**  For a measurable energy that is bounded below on a
product voxel of measurable cells of finite measure, the Boltzmann factor is integrable on the
voxel (`β ≥ 0`).  For pairwise energies measurability follows from `measurable_torsionEnergy` and
the lower bound from `torsionEnergy_voxel_bounds`. -/
theorem integrableOn_prodVoxel_boltzmann (ν : Fin n → Measure ℝ) [∀ i, SigmaFinite (ν i)]
    {s : Fin n → Fin k → Set ℝ} (hs : ∀ i a, MeasurableSet (s i a))
    (hsfin : ∀ i a, ν i (s i a) ≠ ⊤) {E : (Fin n → ℝ) → ℝ} (hE : Measurable E) {β Elo : ℝ}
    (hβ : 0 ≤ β) (x : Config n k) (hlo : ∀ θ ∈ prodVoxel s x, Elo ≤ E θ) :
    IntegrableOn (fun θ => Real.exp (-β * E θ)) (prodVoxel s x) (Measure.pi ν) :=
  voxel_boltzmann_integrableOn _ (measurableSet_prodVoxel hs x)
    (measure_prodVoxel_ne_top ν hsfin x) hE hβ hlo

/-! ### End-to-end theorems -/

/-- **Certified partition function over product voxels (general energy).**  Let `E` be any
measurable energy on `Fin n → ℝ` which on every voxel of the box is enclosed by the table energies
of two real pairwise models `Mlo`, `Mhi`.  If the rational instances `Ilo`, `Ihi` are
outward-rounded brackets of the Boltzmann factors (cell measures absorbed in the one-body
factors), then two accepted certificates give a two-sided rational enclosure of the continuous
partition integral over the union of the voxels of the box.  `Ihi.Nonneg` is derived, not
assumed. -/
theorem certified_prodVoxel_partition (ν : Fin n → Measure ℝ) [∀ i, SigmaFinite (ν i)]
    (s : Fin n → Fin k → Set ℝ) (hs : ∀ i a, MeasurableSet (s i a))
    (hsfin : ∀ i a, ν i (s i a) ≠ ⊤) (hsdisj : ∀ i a b, a ≠ b → Disjoint (s i a) (s i b))
    (E : (Fin n → ℝ) → ℝ) (hE : Measurable E) {β : ℝ} (hβ : 0 ≤ β)
    (Mlo Mhi : PairModel ℝ (Fin n) (fun _ => Fin k)) (D : Dom n k)
    (hEb : ∀ x ∈ boxFinset D, ∀ θ ∈ prodVoxel s x, Mlo.energy x ≤ E θ ∧ E θ ≤ Mhi.energy x)
    (Ilo Ihi : WInstance n k) (hlo : Ilo.Nonneg)
    (hwlo : ∀ i a, (Ilo.w i a : ℝ) ≤ (ν i (s i a)).toReal * Real.exp (-β * Mhi.h i a))
    (hWlo : ∀ i j a b, (Ilo.W i j a b : ℝ) ≤ Real.exp (-β * Mhi.J i j a b))
    (hwhi : ∀ i a, (ν i (s i a)).toReal * Real.exp (-β * Mlo.h i a) ≤ (Ihi.w i a : ℝ))
    (hWhi : ∀ i j a b, Real.exp (-β * Mlo.J i j a b) ≤ (Ihi.W i j a b : ℝ))
    (clo chi : ZCert n k) (a b a' b' : ℚ) (hclo : zverify clo Ilo D = some (a, b))
    (hchi : zverify chi Ihi D = some (a', b')) :
    (a : ℝ) ≤ ∫ θ in ⋃ x ∈ boxFinset D, prodVoxel s x, Real.exp (-β * E θ) ∂(Measure.pi ν) ∧
      ∫ θ in ⋃ x ∈ boxFinset D, prodVoxel s x, Real.exp (-β * E θ) ∂(Measure.pi ν) ≤
        (b' : ℝ) := by
  have hhi : Ihi.Nonneg :=
    ⟨fun i a => by
        exact_mod_cast le_trans (mul_nonneg ENNReal.toReal_nonneg (Real.exp_pos _).le) (hwhi i a),
      fun i j a b => by exact_mod_cast le_trans (Real.exp_pos _).le (hWhi i j a b)⟩
  have hmeas : ∀ x ∈ boxFinset D, MeasurableSet (prodVoxel s x) := fun x _ =>
    measurableSet_prodVoxel hs x
  have hdisj : Set.Pairwise (↑(boxFinset D)) (Function.onFun Disjoint (prodVoxel s)) :=
    fun x _ y _ hxy => prodVoxel_disjoint hsdisj hxy
  have hint : ∀ x ∈ boxFinset D,
      IntegrableOn (fun θ => Real.exp (-β * E θ)) (prodVoxel s x) (Measure.pi ν) := fun x hx =>
    integrableOn_prodVoxel_boltzmann ν hs hsfin hE hβ x fun θ hθ => (hEb x hx θ hθ).1
  have hb : ∀ x ∈ boxFinset D,
      ((Ilo.weight x : ℚ) : ℝ) ≤ ∫ θ in prodVoxel s x, Real.exp (-β * E θ) ∂(Measure.pi ν) ∧
        ∫ θ in prodVoxel s x, Real.exp (-β * E θ) ∂(Measure.pi ν) ≤ ((Ihi.weight x : ℚ) : ℝ) :=
    fun x hx =>
      pairwise_voxel_weight_bounds (Measure.pi ν) (prodVoxel s) (fun i a => (ν i (s i a)).toReal)
        (fun _ _ => ENNReal.toReal_nonneg) E hβ Mlo Mhi Ilo Ihi hlo hwlo hWlo hwhi hWhi x
        (hmeas x hx) (measure_prodVoxel_ne_top ν hsfin x) (toReal_measure_prodVoxel ν s x)
        (hint x hx) (fun θ hθ => (hEb x hx θ hθ).1) fun θ hθ => (hEb x hx θ hθ).2
  exact certified_voxel_partition (Measure.pi ν) D (prodVoxel s) hmeas hdisj
    (fun θ => Real.exp (-β * E θ)) hint Ilo Ihi hlo hhi hb clo chi a b a' b' hclo hchi

/-- **Certified continuous partition function in torsion coordinates (end-to-end).**
Data: measurable, pairwise disjoint cells `s i a` of finite `ν i`-measure in every coordinate
(`ν i = volume` for Lebesgue measure in the angle, or any σ-finite chart measure); a pairwise
energy `torsionEnergy u U` with measurable terms; two real table models `Mlo`, `Mhi` enclosing the
one-body terms on every cell and the two-body terms on every pair of cells; rational instances
`Ilo`, `Ihi` whose factors are outward-rounded brackets of `ν i (s i a) · exp(-β h i a)` and
`exp(-β J i j a b)`; two accepted certificates.
Conclusion: `a ≤ ∫ exp(-β E) ≤ b'` over the union of the voxels of the box `D`.
No bracketing of voxel integrals is assumed: the hypothesis `hb` of `certified_voxel_partition`
is derived through `torsionEnergy_voxel_bounds` and `pairwise_voxel_weight_bounds`. -/
theorem certified_torsion_partition (ν : Fin n → Measure ℝ) [∀ i, SigmaFinite (ν i)]
    (s : Fin n → Fin k → Set ℝ) (hs : ∀ i a, MeasurableSet (s i a))
    (hsfin : ∀ i a, ν i (s i a) ≠ ⊤) (hsdisj : ∀ i a b, a ≠ b → Disjoint (s i a) (s i b))
    (u : Fin n → ℝ → ℝ) (U : Fin n → Fin n → ℝ → ℝ → ℝ) (hum : ∀ i, Measurable (u i))
    (hUm : ∀ i j, j ≠ i → Measurable (Function.uncurry (U i j))) {β : ℝ} (hβ : 0 ≤ β)
    (Mlo Mhi : PairModel ℝ (Fin n) (fun _ => Fin k))
    (hu : ∀ i a, ∀ t ∈ s i a, Mlo.h i a ≤ u i t ∧ u i t ≤ Mhi.h i a)
    (hU : ∀ i j, j ≠ i → ∀ a b, ∀ t ∈ s i a, ∀ t' ∈ s j b,
      Mlo.J i j a b ≤ U i j t t' ∧ U i j t t' ≤ Mhi.J i j a b)
    (Ilo Ihi : WInstance n k) (hlo : Ilo.Nonneg)
    (hwlo : ∀ i a, (Ilo.w i a : ℝ) ≤ (ν i (s i a)).toReal * Real.exp (-β * Mhi.h i a))
    (hWlo : ∀ i j a b, (Ilo.W i j a b : ℝ) ≤ Real.exp (-β * Mhi.J i j a b))
    (hwhi : ∀ i a, (ν i (s i a)).toReal * Real.exp (-β * Mlo.h i a) ≤ (Ihi.w i a : ℝ))
    (hWhi : ∀ i j a b, Real.exp (-β * Mlo.J i j a b) ≤ (Ihi.W i j a b : ℝ))
    (D : Dom n k) (clo chi : ZCert n k) (a b a' b' : ℚ)
    (hclo : zverify clo Ilo D = some (a, b)) (hchi : zverify chi Ihi D = some (a', b')) :
    (a : ℝ) ≤ ∫ θ in ⋃ x ∈ boxFinset D, prodVoxel s x,
        Real.exp (-β * torsionEnergy u U θ) ∂(Measure.pi ν) ∧
      ∫ θ in ⋃ x ∈ boxFinset D, prodVoxel s x,
        Real.exp (-β * torsionEnergy u U θ) ∂(Measure.pi ν) ≤ (b' : ℝ) :=
  certified_prodVoxel_partition ν s hs hsfin hsdisj (torsionEnergy u U)
    (measurable_torsionEnergy hum hUm) hβ Mlo Mhi D
    (fun x _ _ hθ => torsionEnergy_voxel_bounds hu hU x hθ) Ilo Ihi hlo hwlo hWlo hwhi hWhi
    clo chi a b a' b' hclo hchi

/-- **Box form of `certified_torsion_partition`.**  The table enclosures of the energy terms are
only required on the cells of the box `D`: cells that have been removed from the box (for
instance sterically excluded ones, on which the energy need not even be bounded) need no
enclosure.  The entrywise brackets are still required for all table entries (they make
`Ihi.Nonneg` derivable); for entries outside the box the tables are unconstrained. -/
theorem certified_torsion_partition_box (ν : Fin n → Measure ℝ) [∀ i, SigmaFinite (ν i)]
    (s : Fin n → Fin k → Set ℝ) (hs : ∀ i a, MeasurableSet (s i a))
    (hsfin : ∀ i a, ν i (s i a) ≠ ⊤) (hsdisj : ∀ i a b, a ≠ b → Disjoint (s i a) (s i b))
    (u : Fin n → ℝ → ℝ) (U : Fin n → Fin n → ℝ → ℝ → ℝ) (hum : ∀ i, Measurable (u i))
    (hUm : ∀ i j, j ≠ i → Measurable (Function.uncurry (U i j))) {β : ℝ} (hβ : 0 ≤ β)
    (Mlo Mhi : PairModel ℝ (Fin n) (fun _ => Fin k)) (D : Dom n k)
    (hu : ∀ i, ∀ a ∈ D i, ∀ t ∈ s i a, Mlo.h i a ≤ u i t ∧ u i t ≤ Mhi.h i a)
    (hU : ∀ i j, j ≠ i → ∀ a ∈ D i, ∀ b ∈ D j, ∀ t ∈ s i a, ∀ t' ∈ s j b,
      Mlo.J i j a b ≤ U i j t t' ∧ U i j t t' ≤ Mhi.J i j a b)
    (Ilo Ihi : WInstance n k) (hlo : Ilo.Nonneg)
    (hwlo : ∀ i a, (Ilo.w i a : ℝ) ≤ (ν i (s i a)).toReal * Real.exp (-β * Mhi.h i a))
    (hWlo : ∀ i j a b, (Ilo.W i j a b : ℝ) ≤ Real.exp (-β * Mhi.J i j a b))
    (hwhi : ∀ i a, (ν i (s i a)).toReal * Real.exp (-β * Mlo.h i a) ≤ (Ihi.w i a : ℝ))
    (hWhi : ∀ i j a b, Real.exp (-β * Mlo.J i j a b) ≤ (Ihi.W i j a b : ℝ))
    (clo chi : ZCert n k) (a b a' b' : ℚ)
    (hclo : zverify clo Ilo D = some (a, b)) (hchi : zverify chi Ihi D = some (a', b')) :
    (a : ℝ) ≤ ∫ θ in ⋃ x ∈ boxFinset D, prodVoxel s x,
        Real.exp (-β * torsionEnergy u U θ) ∂(Measure.pi ν) ∧
      ∫ θ in ⋃ x ∈ boxFinset D, prodVoxel s x,
        Real.exp (-β * torsionEnergy u U θ) ∂(Measure.pi ν) ≤ (b' : ℝ) :=
  certified_prodVoxel_partition ν s hs hsfin hsdisj (torsionEnergy u U)
    (measurable_torsionEnergy hum hUm) hβ Mlo Mhi D
    (fun x hx _ hθ =>
      have hxD := mem_boxFinset.mp hx
      torsionEnergy_config_bounds x (fun i => hu i (x i) (hxD i))
        (fun i j hji => hU i j hji (x i) (hxD i) (x j) (hxD j)) hθ)
    Ilo Ihi hlo hwlo hWlo hwhi hWhi clo chi a b a' b' hclo hchi

/-- **Top-level form.**  As `certified_torsion_partition_box`, but with the top-level kernel
`zverifyTop`, which checks nonnegativity of the factors itself: no nonnegativity hypothesis is
left to the caller, and energy enclosures are needed only on the cells of the box. -/
theorem certified_torsion_partition_top (ν : Fin n → Measure ℝ) [∀ i, SigmaFinite (ν i)]
    (s : Fin n → Fin k → Set ℝ) (hs : ∀ i a, MeasurableSet (s i a))
    (hsfin : ∀ i a, ν i (s i a) ≠ ⊤) (hsdisj : ∀ i a b, a ≠ b → Disjoint (s i a) (s i b))
    (u : Fin n → ℝ → ℝ) (U : Fin n → Fin n → ℝ → ℝ → ℝ) (hum : ∀ i, Measurable (u i))
    (hUm : ∀ i j, j ≠ i → Measurable (Function.uncurry (U i j))) {β : ℝ} (hβ : 0 ≤ β)
    (Mlo Mhi : PairModel ℝ (Fin n) (fun _ => Fin k)) (D : Dom n k)
    (hu : ∀ i, ∀ a ∈ D i, ∀ t ∈ s i a, Mlo.h i a ≤ u i t ∧ u i t ≤ Mhi.h i a)
    (hU : ∀ i j, j ≠ i → ∀ a ∈ D i, ∀ b ∈ D j, ∀ t ∈ s i a, ∀ t' ∈ s j b,
      Mlo.J i j a b ≤ U i j t t' ∧ U i j t t' ≤ Mhi.J i j a b)
    (Ilo Ihi : WInstance n k)
    (hwlo : ∀ i a, (Ilo.w i a : ℝ) ≤ (ν i (s i a)).toReal * Real.exp (-β * Mhi.h i a))
    (hWlo : ∀ i j a b, (Ilo.W i j a b : ℝ) ≤ Real.exp (-β * Mhi.J i j a b))
    (hwhi : ∀ i a, (ν i (s i a)).toReal * Real.exp (-β * Mlo.h i a) ≤ (Ihi.w i a : ℝ))
    (hWhi : ∀ i j a b, Real.exp (-β * Mlo.J i j a b) ≤ (Ihi.W i j a b : ℝ))
    (clo chi : ZCert n k) (a b a' b' : ℚ)
    (hclo : zverifyTop clo Ilo D = some (a, b)) (hchi : zverifyTop chi Ihi D = some (a', b')) :
    (a : ℝ) ≤ ∫ θ in ⋃ x ∈ boxFinset D, prodVoxel s x,
        Real.exp (-β * torsionEnergy u U θ) ∂(Measure.pi ν) ∧
      ∫ θ in ⋃ x ∈ boxFinset D, prodVoxel s x,
        Real.exp (-β * torsionEnergy u U θ) ∂(Measure.pi ν) ≤ (b' : ℝ) :=
  certified_torsion_partition_box ν s hs hsfin hsdisj u U hum hUm hβ Mlo Mhi D hu hU Ilo Ihi
    (zverifyTop_eq_some hclo).1 hwlo hWlo hwhi hWhi clo chi a b a' b'
    (zverifyTop_eq_some hclo).2 (zverifyTop_eq_some hchi).2

/-- **Full-box form of `certified_torsion_partition`.**  For `D = fullDom n k` the voxels tile the
product domain, so the certified quantity is the partition integral over `∏ i, ⋃ a, s i a`. -/
theorem certified_torsion_partition_full (ν : Fin n → Measure ℝ) [∀ i, SigmaFinite (ν i)]
    (s : Fin n → Fin k → Set ℝ) (hs : ∀ i a, MeasurableSet (s i a))
    (hsfin : ∀ i a, ν i (s i a) ≠ ⊤) (hsdisj : ∀ i a b, a ≠ b → Disjoint (s i a) (s i b))
    (u : Fin n → ℝ → ℝ) (U : Fin n → Fin n → ℝ → ℝ → ℝ) (hum : ∀ i, Measurable (u i))
    (hUm : ∀ i j, j ≠ i → Measurable (Function.uncurry (U i j))) {β : ℝ} (hβ : 0 ≤ β)
    (Mlo Mhi : PairModel ℝ (Fin n) (fun _ => Fin k))
    (hu : ∀ i a, ∀ t ∈ s i a, Mlo.h i a ≤ u i t ∧ u i t ≤ Mhi.h i a)
    (hU : ∀ i j, j ≠ i → ∀ a b, ∀ t ∈ s i a, ∀ t' ∈ s j b,
      Mlo.J i j a b ≤ U i j t t' ∧ U i j t t' ≤ Mhi.J i j a b)
    (Ilo Ihi : WInstance n k) (hlo : Ilo.Nonneg)
    (hwlo : ∀ i a, (Ilo.w i a : ℝ) ≤ (ν i (s i a)).toReal * Real.exp (-β * Mhi.h i a))
    (hWlo : ∀ i j a b, (Ilo.W i j a b : ℝ) ≤ Real.exp (-β * Mhi.J i j a b))
    (hwhi : ∀ i a, (ν i (s i a)).toReal * Real.exp (-β * Mlo.h i a) ≤ (Ihi.w i a : ℝ))
    (hWhi : ∀ i j a b, Real.exp (-β * Mlo.J i j a b) ≤ (Ihi.W i j a b : ℝ))
    (clo chi : ZCert n k) (a b a' b' : ℚ)
    (hclo : zverify clo Ilo (fullDom n k) = some (a, b))
    (hchi : zverify chi Ihi (fullDom n k) = some (a', b')) :
    (a : ℝ) ≤ ∫ θ in Set.univ.pi fun i => ⋃ a, s i a,
        Real.exp (-β * torsionEnergy u U θ) ∂(Measure.pi ν) ∧
      ∫ θ in Set.univ.pi fun i => ⋃ a, s i a,
        Real.exp (-β * torsionEnergy u U θ) ∂(Measure.pi ν) ≤ (b' : ℝ) := by
  have h := certified_torsion_partition ν s hs hsfin hsdisj u U hum hUm hβ Mlo Mhi hu hU Ilo Ihi
    hlo hwlo hWlo hwhi hWhi (fullDom n k) clo chi a b a' b' hclo hchi
  rwa [iUnion_prodVoxel_fullDom] at h

end ProductVoxels

/-! ### Chart arcs: rational bounds for the volume factors -/

section ChartArcs

/-- **Angular measure of a chart arc, general form.**  If `m² ≤ x² ≤ T²` for all chart parameters
`x` strictly between `t₁ ≤ t₂`, then the angle `2 (arctan t₂ - arctan t₁)` swept by the chart
`circParam` lies between `(t₂ - t₁) · 2 / (1 + T²)` and `(t₂ - t₁) · 2 / (1 + m²)`: this is the
mean value theorem for `2 arctan`, whose derivative is `2 / (1 + x²)`.  For rational
`t₁, t₂, m, T` both bounds are rational. -/
theorem two_arctan_sub_bounds_of_sq {t₁ t₂ m T : ℝ} (h : t₁ ≤ t₂)
    (hm : ∀ x ∈ Set.Ioo t₁ t₂, m ^ 2 ≤ x ^ 2) (hT : ∀ x ∈ Set.Ioo t₁ t₂, x ^ 2 ≤ T ^ 2) :
    (t₂ - t₁) * (2 / (1 + T ^ 2)) ≤ 2 * (Real.arctan t₂ - Real.arctan t₁) ∧
      2 * (Real.arctan t₂ - Real.arctan t₁) ≤ (t₂ - t₁) * (2 / (1 + m ^ 2)) := by
  have hD : Convex ℝ (Set.Icc t₁ t₂) := convex_Icc _ _
  have hcont : ContinuousOn Real.arctan (Set.Icc t₁ t₂) := Real.continuous_arctan.continuousOn
  have hdiff : DifferentiableOn ℝ Real.arctan (interior (Set.Icc t₁ t₂)) :=
    Real.differentiable_arctan.differentiableOn
  have hlo := hD.mul_sub_le_image_sub_of_le_deriv hcont hdiff (C := 1 / (1 + T ^ 2))
    (fun x hx => by
      rw [interior_Icc] at hx
      rw [Real.deriv_arctan]
      exact one_div_le_one_div_of_le (by positivity) (by linarith [hT x hx]))
    t₁ (Set.left_mem_Icc.mpr h) t₂ (Set.right_mem_Icc.mpr h) h
  have hhi := hD.image_sub_le_mul_sub_of_deriv_le hcont hdiff (C := 1 / (1 + m ^ 2))
    (fun x hx => by
      rw [interior_Icc] at hx
      rw [Real.deriv_arctan]
      exact one_div_le_one_div_of_le (by positivity) (by linarith [hm x hx]))
    t₁ (Set.left_mem_Icc.mpr h) t₂ (Set.right_mem_Icc.mpr h) h
  constructor
  · calc (t₂ - t₁) * (2 / (1 + T ^ 2)) = 2 * (1 / (1 + T ^ 2) * (t₂ - t₁)) := by ring
      _ ≤ 2 * (Real.arctan t₂ - Real.arctan t₁) := by linarith
  · calc 2 * (Real.arctan t₂ - Real.arctan t₁) ≤ 2 * (1 / (1 + m ^ 2) * (t₂ - t₁)) := by linarith
      _ = (t₂ - t₁) * (2 / (1 + m ^ 2)) := by ring

/-- **Rational enclosure of the angular measure of a chart arc.**  For chart endpoints
`t₁ ≤ t₂` in `[-T, T]` the angle swept by `circParam` satisfies
`(t₂ - t₁) · 2 / (1 + T²) ≤ 2 (arctan t₂ - arctan t₁) ≤ 2 (t₂ - t₁)`.  (For arcs that do not
contain `t = 0`, `two_arctan_sub_bounds_of_sq` with `m = min |t₁| |t₂|` gives the sharper upper
bound `(t₂ - t₁) · 2 / (1 + m²)`.) -/
theorem two_arctan_sub_bounds {t₁ t₂ T : ℝ} (h : t₁ ≤ t₂) (h₁ : |t₁| ≤ T) (h₂ : |t₂| ≤ T) :
    (t₂ - t₁) * (2 / (1 + T ^ 2)) ≤ 2 * (Real.arctan t₂ - Real.arctan t₁) ∧
      2 * (Real.arctan t₂ - Real.arctan t₁) ≤ 2 * (t₂ - t₁) := by
  have key := two_arctan_sub_bounds_of_sq (m := 0) (T := T) h
    (fun x _ => by nlinarith [sq_nonneg x])
    (fun x hx => by
      have hxT : |x| ≤ T :=
        abs_le.mpr ⟨by linarith [(abs_le.mp h₁).1, hx.1], by linarith [(abs_le.mp h₂).2, hx.2]⟩
      exact sq_le_sq' (by linarith [(abs_le.mp hxT).1]) (abs_le.mp hxT).2)
  refine ⟨key.1, le_trans key.2 (le_of_eq ?_)⟩
  ring

/-- Lebesgue volume of the cell of angles `[2 arctan t₁, 2 arctan t₂)` cut out by the chart
endpoints `t₁, t₂`. -/
theorem volume_chartArc (t₁ t₂ : ℝ) :
    volume (Set.Ico (2 * Real.arctan t₁) (2 * Real.arctan t₂)) =
      ENNReal.ofReal (2 * (Real.arctan t₂ - Real.arctan t₁)) := by
  rw [Real.volume_Ico, mul_sub]

/-- **Rational bounds for the volume factor of a chart arc.**  The real volume
`(volume cell).toReal` that enters the one-body brackets of `certified_torsion_partition` (with
Lebesgue measure in the angle coordinate) has the rational bounds of `two_arctan_sub_bounds`. -/
theorem volume_chartArc_toReal_bounds {t₁ t₂ T : ℝ} (h : t₁ ≤ t₂) (h₁ : |t₁| ≤ T)
    (h₂ : |t₂| ≤ T) :
    (t₂ - t₁) * (2 / (1 + T ^ 2)) ≤
        (volume (Set.Ico (2 * Real.arctan t₁) (2 * Real.arctan t₂))).toReal ∧
      (volume (Set.Ico (2 * Real.arctan t₁) (2 * Real.arctan t₂))).toReal ≤ 2 * (t₂ - t₁) := by
  have hmono : Real.arctan t₁ ≤ Real.arctan t₂ := Real.arctan_strictMono.monotone h
  rw [volume_chartArc, ENNReal.toReal_ofReal (by linarith)]
  exact two_arctan_sub_bounds h h₁ h₂

/-- **Computable one-body brackets on a chart arc.**  For rational chart endpoints `t₁ ≤ t₂` in
`[-T, T]` and rational exponents `q₁, q₂` (in the application `q₁ = -β h_hi`, `q₂ = -β h_lo`), the
rationals `(t₂ - t₁) · 2 / (1 + T²) · expLo m r q₁` and `2 (t₂ - t₁) · expHi m r q₂` bracket
`vol · exp q₁` from below and `vol · exp q₂` from above, where `vol` is the Lebesgue volume of the
arc.  These are the hypotheses `hwlo`, `hwhi` of `certified_torsion_partition` in executable form
(`m` Taylor terms and `r` argument halvings, see `exp_enclosure`); the two-body hypotheses
`hWlo`, `hWhi` are instances of `exp_enclosure` itself. -/
theorem chartArc_onebody_brackets {m r : ℕ} (hm : 0 < m) {t₁ t₂ T q₁ q₂ : ℚ} (h : t₁ ≤ t₂)
    (h₁ : |t₁| ≤ T) (h₂ : |t₂| ≤ T) (hq₁ : |q₁| ≤ 2 ^ r) (hq₂ : |q₂| ≤ 2 ^ r) :
    (((t₂ - t₁) * (2 / (1 + T ^ 2)) * expLo m r q₁ : ℚ) : ℝ) ≤
        (volume (Set.Ico (2 * Real.arctan (t₁ : ℝ)) (2 * Real.arctan (t₂ : ℝ)))).toReal *
          Real.exp (q₁ : ℝ) ∧
      (volume (Set.Ico (2 * Real.arctan (t₁ : ℝ)) (2 * Real.arctan (t₂ : ℝ)))).toReal *
          Real.exp (q₂ : ℝ) ≤ ((2 * (t₂ - t₁) * expHi m r q₂ : ℚ) : ℝ) := by
  have hle : (t₁ : ℝ) ≤ (t₂ : ℝ) := by exact_mod_cast h
  have hv := volume_chartArc_toReal_bounds (T := (T : ℝ)) hle (by exact_mod_cast h₁)
    (by exact_mod_cast h₂)
  have he₁ := (exp_enclosure m r hm q₁ hq₁).1
  have he₂ := (exp_enclosure m r hm q₂ hq₂).2
  have h0 : (0 : ℝ) ≤ ((expLo m r q₁ : ℚ) : ℝ) := by exact_mod_cast expLo_nonneg m r q₁
  push_cast
  exact ⟨mul_le_mul hv.1 he₁ h0 ENNReal.toReal_nonneg,
    mul_le_mul hv.2 he₂ (Real.exp_pos _).le (by linarith)⟩

/-- **Convergent rational bounds for the volume factor of a chart arc.**  With `m² ≤ t² ≤ T²` on
the arc, the volume lies between `(t₂ - t₁) · 2/(1 + T²)` and `(t₂ - t₁) · 2/(1 + m²)`; the ratio
of the two bounds tends to `1` when the arc is subdivided. -/
theorem volume_chartArc_toReal_bounds_of_sq {t₁ t₂ m T : ℝ} (h : t₁ ≤ t₂)
    (hm : ∀ x ∈ Set.Ioo t₁ t₂, m ^ 2 ≤ x ^ 2) (hT : ∀ x ∈ Set.Ioo t₁ t₂, x ^ 2 ≤ T ^ 2) :
    (t₂ - t₁) * (2 / (1 + T ^ 2)) ≤
        (volume (Set.Ico (2 * Real.arctan t₁) (2 * Real.arctan t₂))).toReal ∧
      (volume (Set.Ico (2 * Real.arctan t₁) (2 * Real.arctan t₂))).toReal ≤
        (t₂ - t₁) * (2 / (1 + m ^ 2)) := by
  have hmono : Real.arctan t₁ ≤ Real.arctan t₂ := Real.arctan_strictMono.monotone h
  rw [volume_chartArc, ENNReal.toReal_ofReal (by linarith)]
  exact two_arctan_sub_bounds_of_sq h hm hT

/-- **Computable one-body brackets on a chart arc, convergent form.**  As
`chartArc_onebody_brackets`, with the upper volume bound `(t₂ - t₁) · 2/(1 + m²)` for
`m² ≤ t²` on the arc, so that the enclosure tightens under subdivision of the arc. -/
theorem chartArc_onebody_brackets_of_sq {N r : ℕ} (hN : 0 < N) {t₁ t₂ m T q₁ q₂ : ℚ}
    (h : t₁ ≤ t₂) (hm : ∀ x ∈ Set.Ioo (t₁ : ℝ) (t₂ : ℝ), (m : ℝ) ^ 2 ≤ x ^ 2)
    (hT : ∀ x ∈ Set.Ioo (t₁ : ℝ) (t₂ : ℝ), x ^ 2 ≤ (T : ℝ) ^ 2)
    (hq₁ : |q₁| ≤ 2 ^ r) (hq₂ : |q₂| ≤ 2 ^ r) :
    (((t₂ - t₁) * (2 / (1 + T ^ 2)) * expLo N r q₁ : ℚ) : ℝ) ≤
        (volume (Set.Ico (2 * Real.arctan (t₁ : ℝ)) (2 * Real.arctan (t₂ : ℝ)))).toReal *
          Real.exp (q₁ : ℝ) ∧
      (volume (Set.Ico (2 * Real.arctan (t₁ : ℝ)) (2 * Real.arctan (t₂ : ℝ)))).toReal *
          Real.exp (q₂ : ℝ) ≤ (((t₂ - t₁) * (2 / (1 + m ^ 2)) * expHi N r q₂ : ℚ) : ℝ) := by
  have hle : (t₁ : ℝ) ≤ (t₂ : ℝ) := by exact_mod_cast h
  have hv := volume_chartArc_toReal_bounds_of_sq hle hm hT
  have he₁ := (exp_enclosure N r hN q₁ hq₁).1
  have he₂ := (exp_enclosure N r hN q₂ hq₂).2
  have h0 : (0 : ℝ) ≤ ((expLo N r q₁ : ℚ) : ℝ) := by exact_mod_cast expLo_nonneg N r q₁
  have hpos : (0 : ℝ) ≤ ((t₂ : ℝ) - t₁) * (2 / (1 + (m : ℝ) ^ 2)) := by
    have h1 : (0 : ℝ) ≤ (t₂ : ℝ) - t₁ := by linarith
    positivity
  push_cast
  exact ⟨mul_le_mul hv.1 he₁ h0 ENNReal.toReal_nonneg,
    mul_le_mul hv.2 he₂ (Real.exp_pos _).le hpos⟩

/-- **Arcs on the nonnegative side of a chart** (`0 ≤ t₁ ≤ t₂`): `m = t₁`, `T = t₂`.  The relative
width of the volume enclosure is `(1 + t₂²)/(1 + t₁²)`, which tends to `1` under subdivision. -/
theorem chartArc_onebody_brackets_pos {N r : ℕ} (hN : 0 < N) {t₁ t₂ q₁ q₂ : ℚ} (h0 : 0 ≤ t₁)
    (h : t₁ ≤ t₂) (hq₁ : |q₁| ≤ 2 ^ r) (hq₂ : |q₂| ≤ 2 ^ r) :
    (((t₂ - t₁) * (2 / (1 + t₂ ^ 2)) * expLo N r q₁ : ℚ) : ℝ) ≤
        (volume (Set.Ico (2 * Real.arctan (t₁ : ℝ)) (2 * Real.arctan (t₂ : ℝ)))).toReal *
          Real.exp (q₁ : ℝ) ∧
      (volume (Set.Ico (2 * Real.arctan (t₁ : ℝ)) (2 * Real.arctan (t₂ : ℝ)))).toReal *
          Real.exp (q₂ : ℝ) ≤ (((t₂ - t₁) * (2 / (1 + t₁ ^ 2)) * expHi N r q₂ : ℚ) : ℝ) := by
  have h0' : (0 : ℝ) ≤ (t₁ : ℝ) := by exact_mod_cast h0
  refine chartArc_onebody_brackets_of_sq hN h (fun x hx => ?_) (fun x hx => ?_) hq₁ hq₂
  · have hx1 := hx.1
    nlinarith
  · have hx1 := hx.1
    have hx2 := hx.2
    nlinarith

/-- **Arcs on the nonpositive side of a chart** (`t₁ ≤ t₂ ≤ 0`): `m = -t₂`, `T = -t₁`. -/
theorem chartArc_onebody_brackets_neg {N r : ℕ} (hN : 0 < N) {t₁ t₂ q₁ q₂ : ℚ} (h0 : t₂ ≤ 0)
    (h : t₁ ≤ t₂) (hq₁ : |q₁| ≤ 2 ^ r) (hq₂ : |q₂| ≤ 2 ^ r) :
    (((t₂ - t₁) * (2 / (1 + t₁ ^ 2)) * expLo N r q₁ : ℚ) : ℝ) ≤
        (volume (Set.Ico (2 * Real.arctan (t₁ : ℝ)) (2 * Real.arctan (t₂ : ℝ)))).toReal *
          Real.exp (q₁ : ℝ) ∧
      (volume (Set.Ico (2 * Real.arctan (t₁ : ℝ)) (2 * Real.arctan (t₂ : ℝ)))).toReal *
          Real.exp (q₂ : ℝ) ≤ (((t₂ - t₁) * (2 / (1 + t₂ ^ 2)) * expHi N r q₂ : ℚ) : ℝ) := by
  have h0' : (t₂ : ℝ) ≤ 0 := by exact_mod_cast h0
  refine chartArc_onebody_brackets_of_sq (m := t₂) (T := t₁) hN h (fun x hx => ?_)
    (fun x hx => ?_) hq₁ hq₂
  · have hx1 := hx.1
    have hx2 := hx.2
    nlinarith
  · have hx1 := hx.1
    have hx2 := hx.2
    nlinarith

/-- The chart point with parameter `t` sits at the angle `2 arctan t` (the converse reading of
`circParam_tan_half`). -/
theorem circParam_two_arctan (t : ℝ) :
    circParam t = (Real.cos (2 * Real.arctan t), Real.sin (2 * Real.arctan t)) := by
  have hhalf : 2 * Real.arctan t / 2 = Real.arctan t := by ring
  have h := circParam_tan_half (θ := 2 * Real.arctan t)
    (by rw [hhalf]; exact (Real.cos_arctan_pos t).ne')
  rwa [hhalf, Real.tan_arctan] at h

/-- Every angle `θ` of the arc `[2 arctan t₁, 2 arctan t₂)` has its chart parameter `tan (θ / 2)`
in `[t₁, t₂)`, and the chart reproduces the point `(cos θ, sin θ)`.  Hence an enclosure of an
energy term over the chart interval `[t₁, t₂]` (e.g. by `QInterval.contains_circParam`) is an
enclosure over the cell of angles, as required by the hypotheses `hu`, `hU` of
`certified_torsion_partition`. -/
theorem chartArc_param_mem {t₁ t₂ θ : ℝ}
    (hθ : θ ∈ Set.Ico (2 * Real.arctan t₁) (2 * Real.arctan t₂)) :
    Real.tan (θ / 2) ∈ Set.Ico t₁ t₂ ∧
      circParam (Real.tan (θ / 2)) = (Real.cos θ, Real.sin θ) := by
  have h1 : Real.arctan t₁ ≤ θ / 2 := by linarith [hθ.1]
  have h2 : θ / 2 < Real.arctan t₂ := by linarith [hθ.2]
  have hlo : -(Real.pi / 2) < θ / 2 := lt_of_lt_of_le (Real.neg_pi_div_two_lt_arctan t₁) h1
  have hhi : θ / 2 < Real.pi / 2 := lt_trans h2 (Real.arctan_lt_pi_div_two t₂)
  have harc : Real.arctan (Real.tan (θ / 2)) = θ / 2 := Real.arctan_tan hlo hhi
  refine ⟨⟨?_, ?_⟩, circParam_tan_half (Real.cos_pos_of_mem_Ioo ⟨hlo, hhi⟩).ne'⟩
  · exact Real.arctan_strictMono.le_iff_le.mp (by rw [harc]; exact h1)
  · exact Real.arctan_strictMono.lt_iff_lt.mp (by rw [harc]; exact h2)

end ChartArcs

end MetricChain

/-! ### Non-vacuity witnesses -/

namespace MetricChain.VoxelBridgeWitness

open MeasureTheory Finset

/-- Two unit cells `[0, 1)` and `[1, 2)` (the same in every coordinate). -/
def cells (a : Fin 2) : Set ℝ := Set.Ico (a : ℝ) ((a : ℝ) + 1)

/-- The cells are measurable. -/
theorem measurableSet_cells (a : Fin 2) : MeasurableSet (cells a) :=
  measurableSet_Ico

/-- Every cell has Lebesgue measure `1`. -/
theorem volume_cells (a : Fin 2) : volume (cells a) = 1 := by
  simp [cells]

/-- Distinct cells are disjoint. -/
theorem cells_disjoint (a b : Fin 2) (hab : a ≠ b) : Disjoint (cells a) (cells b) := by
  refine Set.disjoint_left.mpr fun t hta htb => hab ?_
  have h1 : ((a : ℕ) : ℝ) < (b : ℕ) + 1 := lt_of_le_of_lt hta.1 htb.2
  have h2 : ((b : ℕ) : ℝ) < (a : ℕ) + 1 := lt_of_le_of_lt htb.1 hta.2
  have h1' : (a : ℕ) < (b : ℕ) + 1 := by exact_mod_cast h1
  have h2' : (b : ℕ) < (a : ℕ) + 1 := by exact_mod_cast h2
  exact Fin.ext (by omega)

/-- The two cells tile `[0, 2)`. -/
theorem iUnion_cells : ⋃ a, cells a = Set.Ico (0 : ℝ) 2 := by
  ext t
  simp only [Set.mem_iUnion, Fin.exists_fin_two, cells, Set.mem_Ico, Fin.val_zero, Fin.val_one,
    Nat.cast_zero, Nat.cast_one, zero_add]
  constructor
  · rintro (⟨h1, h2⟩ | ⟨h1, h2⟩) <;> constructor <;> linarith
  · rintro ⟨h1, h2⟩
    rcases lt_or_ge t 1 with h | h
    · exact Or.inl ⟨h1, h⟩
    · exact Or.inr ⟨h, by linarith⟩

/-! #### Exact witness: one site, zero energy -/

/-- Unit weights on one site with two states. -/
def unitW : WInstance 1 2 where
  w := fun _ _ => 1
  W := fun _ _ _ _ => 1

/-- The zero table model. -/
def zeroModel : PairModel ℝ (Fin 1) (fun _ => Fin 2) where
  h := fun _ _ => 0
  J := fun _ _ _ _ => 0

/-- The kernel accepts the one-leaf certificate and returns the exact partition sum `2`. -/
theorem unitW_cert :
    zverify (.leaf (fun _ _ => 1) (fun _ _ => 1)) unitW (fullDom 1 2) = some (2, 2) := by
  decide +kernel

/-- **Exact witness.**  One coordinate, Lebesgue measure, cells `[0, 1)` and `[1, 2)`, zero
energy, `β = 1`, unit weights: all hypotheses of `certified_torsion_partition_full` hold and the
certified enclosure of `∫_{[0, 2)} exp(-0) = 2` is `[2, 2]`. -/
theorem exact_witness :
    (2 : ℝ) ≤ ∫ θ in Set.univ.pi fun _ : Fin 1 => Set.Ico (0 : ℝ) 2,
        Real.exp (-1 * torsionEnergy (fun _ _ => 0) (fun _ _ _ _ => 0) θ)
          ∂(Measure.pi fun _ : Fin 1 => (volume : Measure ℝ)) ∧
      ∫ θ in Set.univ.pi fun _ : Fin 1 => Set.Ico (0 : ℝ) 2,
        Real.exp (-1 * torsionEnergy (fun _ _ => 0) (fun _ _ _ _ => 0) θ)
          ∂(Measure.pi fun _ : Fin 1 => (volume : Measure ℝ)) ≤ 2 := by
  have hbr : ∀ (i : Fin 1) (a : Fin 2),
      (volume (cells a)).toReal * Real.exp (-1 * zeroModel.h i a) = 1 := by
    intro i a
    simp [volume_cells, zeroModel]
  have h := certified_torsion_partition_full (fun _ : Fin 1 => (volume : Measure ℝ))
    (fun _ => cells) (fun _ => measurableSet_cells)
    (fun _ a => by rw [volume_cells]; exact ENNReal.one_ne_top) (fun _ => cells_disjoint)
    (fun _ _ => 0) (fun _ _ _ _ => 0) (fun _ => measurable_const) (fun _ _ _ => measurable_const)
    (β := 1) zero_le_one zeroModel zeroModel
    (fun _ _ _ _ => ⟨le_rfl, le_rfl⟩) (fun _ _ _ _ _ _ _ _ _ => ⟨le_rfl, le_rfl⟩)
    unitW unitW ⟨fun _ _ => zero_le_one, fun _ _ _ _ => zero_le_one⟩
    (fun i a => by rw [hbr]; simp [unitW]) (fun i j a b => by simp [unitW, zeroModel])
    (fun i a => by rw [hbr]; simp [unitW]) (fun i j a b => by simp [unitW, zeroModel])
    _ _ 2 2 2 2 unitW_cert unitW_cert
  simp only [iUnion_cells] at h
  exact_mod_cast h

/-! #### Generic witness: two coupled sites, strict enclosures, outward-rounded factors -/

/-- First-order lower bound of a Boltzmann factor: `1 - β e ≤ exp(-β e)`. -/
theorem one_sub_le_boltzmann (β e : ℝ) : 1 - β * e ≤ Real.exp (-β * e) := by
  have := Real.add_one_le_exp (-β * e)
  linarith

/-- First-order upper bound of a Boltzmann factor: `exp(-β e) ≤ 1 / (1 + β e)` for `β e ≥ 0`. -/
theorem boltzmann_le_one_div {β e : ℝ} (h : 0 ≤ β * e) : Real.exp (-β * e) ≤ 1 / (1 + β * e) := by
  rw [neg_mul, Real.exp_neg, one_div]
  exact inv_anti₀ (by positivity) (by linarith [Real.add_one_le_exp (β * e)])

/-- Lower table model for `u i t = t / 4`, `U i j t t' = t t' / 8` on the unit cells. -/
noncomputable def loModel : PairModel ℝ (Fin 2) (fun _ => Fin 2) where
  h := fun _ a => (a : ℝ) / 4
  J := fun _ _ a b => (a : ℝ) * (b : ℝ) / 8

/-- Upper table model for `u i t = t / 4`, `U i j t t' = t t' / 8` on the unit cells. -/
noncomputable def hiModel : PairModel ℝ (Fin 2) (fun _ => Fin 2) where
  h := fun _ a => ((a : ℝ) + 1) / 4
  J := fun _ _ a b => ((a : ℝ) + 1) * ((b : ℝ) + 1) / 8

/-- Rational lower weights: `1 - e_hi ≤ exp(-e_hi)` entrywise (cell volumes are `1`). -/
def loW : WInstance 2 2 where
  w := fun _ a => 1 - ((a : ℚ) + 1) / 4
  W := fun _ _ a b => 1 - ((a : ℚ) + 1) * ((b : ℚ) + 1) / 8

/-- Rational upper weights: `exp(-e_lo) ≤ 1 / (1 + e_lo)` entrywise (cell volumes are `1`). -/
def hiW : WInstance 2 2 where
  w := fun _ a => 1 / (1 + (a : ℚ) / 4)
  W := fun _ _ a b => 1 / (1 + (a : ℚ) * (b : ℚ) / 8)

/-- Full enumeration certificate for two sites with two states. -/
def enumCert (I : WInstance 2 2) : ZCert 2 2 :=
  .branch 0 fun a => .branch 1 fun b =>
    .leaf (fun i j => I.W i j (![a, b] i) (![a, b] j)) (fun i j => I.W i j (![a, b] i) (![a, b] j))

/-- The kernel accepts the enumeration certificate of the lower instance: `Z⁻ = 937/1024`. -/
theorem loW_cert :
    zverify (enumCert loW) loW (fullDom 2 2) = some (937 / 1024, 937 / 1024) := by
  decide +kernel

/-- The kernel accepts the enumeration certificate of the upper instance: `Z⁺ = 6289/2025`. -/
theorem hiW_cert :
    zverify (enumCert hiW) hiW (fullDom 2 2) = some (6289 / 2025, 6289 / 2025) := by
  decide +kernel

/-- The lower weights are nonnegative (a finite rational check). -/
theorem loW_nonneg : loW.Nonneg := by
  unfold WInstance.Nonneg
  decide +kernel

/-- **Generic witness.**  Two coupled coordinates on `[0, 2)²` with Lebesgue measure, energy
`E θ = (θ₀ + θ₁) / 4 + θ₀ θ₁ / 4` (one-body terms `t / 4`, two-body terms `t t' / 8` on both
ordered pairs), `β = 1`, four voxels.  The table models are non-degenerate enclosures
(`Mlo ≠ Mhi`), the rational factors are genuine outward roundings
(`1 - e ≤ exp(-e) ≤ 1 / (1 + e)`), and the two enumeration certificates are checked by kernel
evaluation.  All hypotheses of `certified_torsion_partition_full` hold, and the certified
enclosure is `937/1024 ≤ ∫ exp(-E) ≤ 6289/2025` (numerical value of the integral: `2.046`). -/
theorem pair_witness :
    (937 / 1024 : ℝ) ≤ ∫ θ in Set.univ.pi fun _ : Fin 2 => Set.Ico (0 : ℝ) 2,
        Real.exp (-1 * torsionEnergy (fun _ t => t / 4) (fun _ _ t t' => t * t' / 8) θ)
          ∂(Measure.pi fun _ : Fin 2 => (volume : Measure ℝ)) ∧
      ∫ θ in Set.univ.pi fun _ : Fin 2 => Set.Ico (0 : ℝ) 2,
        Real.exp (-1 * torsionEnergy (fun _ t => t / 4) (fun _ _ t t' => t * t' / 8) θ)
          ∂(Measure.pi fun _ : Fin 2 => (volume : Measure ℝ)) ≤ 6289 / 2025 := by
  have hvol : ∀ a : Fin 2, (volume (cells a)).toReal = 1 := by
    intro a
    simp [volume_cells]
  have h := certified_torsion_partition_full (fun _ : Fin 2 => (volume : Measure ℝ))
    (fun _ => cells) (fun _ => measurableSet_cells)
    (fun _ a => by rw [volume_cells]; exact ENNReal.one_ne_top) (fun _ => cells_disjoint)
    (fun _ t => t / 4) (fun _ _ t t' => t * t' / 8)
    (fun _ => measurable_id.div_const 4)
    (fun _ _ _ => (measurable_fst.mul measurable_snd).div_const 8)
    (β := 1) zero_le_one loModel hiModel
    (fun i a t ht =>
      ⟨by show (a : ℝ) / 4 ≤ t / 4; linarith [ht.1],
        by show t / 4 ≤ ((a : ℝ) + 1) / 4; linarith [ht.2]⟩)
    (fun i j _ a b t ht t' ht' => by
      have ha0 : (0 : ℝ) ≤ (a : ℝ) := Nat.cast_nonneg _
      have hb0 : (0 : ℝ) ≤ (b : ℝ) := Nat.cast_nonneg _
      have h1 : (a : ℝ) * (b : ℝ) ≤ t * t' := mul_le_mul ht.1 ht'.1 hb0 (le_trans ha0 ht.1)
      have h2 : t * t' ≤ ((a : ℝ) + 1) * ((b : ℝ) + 1) :=
        mul_le_mul ht.2.le ht'.2.le (le_trans hb0 ht'.1) (by linarith)
      exact ⟨by show (a : ℝ) * (b : ℝ) / 8 ≤ t * t' / 8; linarith,
        by show t * t' / 8 ≤ ((a : ℝ) + 1) * ((b : ℝ) + 1) / 8; linarith⟩)
    loW hiW loW_nonneg
    (fun i a => by
      rw [hvol, one_mul]
      refine le_trans (le_of_eq ?_) (one_sub_le_boltzmann 1 (hiModel.h i a))
      simp [loW, hiModel])
    (fun i j a b => by
      refine le_trans (le_of_eq ?_) (one_sub_le_boltzmann 1 (hiModel.J i j a b))
      simp [loW, hiModel])
    (fun i a => by
      rw [hvol, one_mul]
      have h0 : (0 : ℝ) ≤ 1 * loModel.h i a := by
        simp only [loModel, one_mul]
        positivity
      refine le_trans (boltzmann_le_one_div h0) (le_of_eq ?_)
      simp [hiW, loModel])
    (fun i j a b => by
      have h0 : (0 : ℝ) ≤ 1 * loModel.J i j a b := by
        simp only [loModel, one_mul]
        positivity
      refine le_trans (boltzmann_le_one_div h0) (le_of_eq ?_)
      simp [hiW, loModel])
    _ _ _ _ _ _ loW_cert hiW_cert
  have e1 : ((937 / 1024 : ℚ) : ℝ) = 937 / 1024 := by norm_num
  have e2 : ((6289 / 2025 : ℚ) : ℝ) = 6289 / 2025 := by norm_num
  simp only [iUnion_cells] at h
  rw [e1, e2] at h
  exact h

/-! #### Chart witness: a torsion potential on two chart arcs, all rational data computed -/

/-- Chart-parameter intervals `[-1/3, 0]` and `[0, 1/2]` of the two cells (rational endpoints). -/
def chartIv (a : Fin 2) : QInterval := if a = 0 then ⟨-1 / 3, 0⟩ else ⟨0, 1 / 2⟩

/-- Rational enclosure of `cos θ` on the two cells, computed by the interval layer
(`QInterval.circParam`): `[4/5, 1]` and `[3/5, 1]`. -/
def cosIv (a : Fin 2) : QInterval := (chartIv a).circParam.1

/-- The cells: the arcs of angles `[2 arctan t₁, 2 arctan t₂)` of the two chart intervals. -/
noncomputable def arcs (a : Fin 2) : Set ℝ :=
  Set.Ico (2 * Real.arctan ((chartIv a).lo : ℝ)) (2 * Real.arctan ((chartIv a).hi : ℝ))

/-- Lower table model: the lower endpoints of the interval enclosures of `cos θ`. -/
noncomputable def cosLo : PairModel ℝ (Fin 1) (fun _ => Fin 2) where
  h := fun _ a => ((cosIv a).lo : ℝ)
  J := fun _ _ _ _ => 0

/-- Upper table model: the upper endpoints of the interval enclosures of `cos θ`. -/
noncomputable def cosHi : PairModel ℝ (Fin 1) (fun _ => Fin 2) where
  h := fun _ a => ((cosIv a).hi : ℝ)
  J := fun _ _ _ _ => 0

/-- Rational lower weights: lower volume bound (`T = 1/2`) times `expLo` at `-cos_hi`. -/
def arcLoW : WInstance 1 2 where
  w := fun _ a =>
    ((chartIv a).hi - (chartIv a).lo) * (2 / (1 + (1 / 2) ^ 2)) * expLo 6 0 (-(cosIv a).hi)
  W := fun _ _ _ _ => 1

/-- Rational upper weights: upper volume bound times `expHi` at `-cos_lo`. -/
def arcHiW : WInstance 1 2 where
  w := fun _ a => 2 * ((chartIv a).hi - (chartIv a).lo) * expHi 6 0 (-(cosIv a).lo)
  W := fun _ _ _ _ => 1

/-- The finite rational side conditions of `chartArc_onebody_brackets`, by kernel evaluation. -/
theorem chart_side : ∀ a : Fin 2, (chartIv a).lo ≤ (chartIv a).hi ∧ |(chartIv a).lo| ≤ 1 / 2 ∧
    |(chartIv a).hi| ≤ 1 / 2 ∧ |-(cosIv a).hi| ≤ 2 ^ 0 ∧ |-(cosIv a).lo| ≤ 2 ^ 0 := by
  decide +kernel

/-- The lower weights are nonnegative (a finite rational check). -/
theorem arcLoW_nonneg : arcLoW.Nonneg := by
  unfold WInstance.Nonneg
  decide +kernel

/-- The kernel accepts the one-leaf certificate of the lower instance: `Z⁻ = 1577/3240`. -/
theorem arcLoW_cert :
    zverify (.leaf (fun _ _ => 1) (fun _ _ => 1)) arcLoW (fullDom 1 2) =
      some (1577 / 3240, 1577 / 3240) := by
  decide +kernel

/-- The kernel accepts the one-leaf certificate of the upper instance:
`Z⁺ = 171810293/202500000`. -/
theorem arcHiW_cert :
    zverify (.leaf (fun _ _ => 1) (fun _ _ => 1)) arcHiW (fullDom 1 2) =
      some (171810293 / 202500000, 171810293 / 202500000) := by
  decide +kernel

/-- The arcs are measurable. -/
theorem measurableSet_arcs (a : Fin 2) : MeasurableSet (arcs a) :=
  measurableSet_Ico

/-- The arcs have finite length. -/
theorem volume_arcs_ne_top (a : Fin 2) : volume (arcs a) ≠ ⊤ := by
  unfold arcs
  rw [Real.volume_Ico]
  exact ENNReal.ofReal_ne_top

/-- The two arcs are disjoint: they share only the excluded endpoint `2 arctan 0`. -/
theorem arcs_disjoint (a b : Fin 2) (hab : a ≠ b) : Disjoint (arcs a) (arcs b) := by
  have key : Disjoint (arcs 0) (arcs 1) := by
    refine Set.disjoint_left.mpr fun θ h0 h1 => ?_
    have e : ((chartIv 1).lo : ℝ) = ((chartIv 0).hi : ℝ) := by simp [chartIv]
    have h0' : θ < 2 * Real.arctan ((chartIv 0).hi : ℝ) := h0.2
    have h1' : 2 * Real.arctan ((chartIv 1).lo : ℝ) ≤ θ := h1.1
    rw [e] at h1'
    exact absurd (lt_of_le_of_lt h1' h0') (lt_irrefl _)
  fin_cases a <;> fin_cases b
  · exact absurd rfl hab
  · exact key
  · exact key.symm
  · exact absurd rfl hab

/-- **Chart witness.**  One torsion angle with the potential `cos θ`, `β = 1`, Lebesgue measure,
and two cells with rational chart endpoints: the arcs of the chart-parameter intervals
`[-1/3, 0)` and `[0, 1/2)` (angles from about `-36.9°` to `53.1°`).  Every hypothesis of
`certified_torsion_partition_full` is discharged by the project's rational machinery: the energy
tables by `QInterval.contains_circParam` through `chartArc_param_mem`, the one-body brackets by
`chartArc_onebody_brackets` (volume bounds of `two_arctan_sub_bounds`, `exp` enclosure with six
Taylor terms), the finite side conditions and both certificates by kernel evaluation.  The
certified enclosure is `1577/3240 ≤ ∫ exp(-cos θ) dθ ≤ 171810293/202500000`, i.e. about
`[0.4867, 0.8485]` (numerical value of the integral: `0.648`). -/
theorem chart_witness :
    (1577 / 3240 : ℝ) ≤ ∫ θ in Set.univ.pi fun _ : Fin 1 => ⋃ a, arcs a,
        Real.exp (-1 * torsionEnergy (fun _ θ => Real.cos θ) (fun _ _ _ _ => 0) θ)
          ∂(Measure.pi fun _ : Fin 1 => (volume : Measure ℝ)) ∧
      ∫ θ in Set.univ.pi fun _ : Fin 1 => ⋃ a, arcs a,
        Real.exp (-1 * torsionEnergy (fun _ θ => Real.cos θ) (fun _ _ _ _ => 0) θ)
          ∂(Measure.pi fun _ : Fin 1 => (volume : Measure ℝ)) ≤ 171810293 / 202500000 := by
  have h := certified_torsion_partition_full (fun _ : Fin 1 => (volume : Measure ℝ))
    (fun _ => arcs) (fun _ => measurableSet_arcs) (fun _ => volume_arcs_ne_top)
    (fun _ => arcs_disjoint)
    (fun _ θ => Real.cos θ) (fun _ _ _ _ => 0) (fun _ => Real.measurable_cos)
    (fun _ _ _ => measurable_const) (β := 1) zero_le_one cosLo cosHi
    (fun i a θ hθ => by
      obtain ⟨ht, hc⟩ := chartArc_param_mem hθ
      have h := (QInterval.contains_circParam (I := chartIv a) ⟨ht.1, ht.2.le⟩).1
      rw [hc] at h
      exact h)
    (fun _ _ _ _ _ _ _ _ _ => ⟨le_rfl, le_rfl⟩)
    arcLoW arcHiW arcLoW_nonneg
    (fun i a => by
      obtain ⟨h01, hl, hh, hq₁, hq₂⟩ := chart_side a
      have key :=
        (chartArc_onebody_brackets (m := 6) (r := 0) (by norm_num) h01 hl hh hq₁ hq₂).1
      have hx : ((-(cosIv a).hi : ℚ) : ℝ) = -1 * cosHi.h i a := by simp [cosHi]
      rw [hx] at key
      exact key)
    (fun i j a b => by simp [arcLoW, cosHi])
    (fun i a => by
      obtain ⟨h01, hl, hh, hq₁, hq₂⟩ := chart_side a
      have key :=
        (chartArc_onebody_brackets (m := 6) (r := 0) (by norm_num) h01 hl hh hq₁ hq₂).2
      have hx : ((-(cosIv a).lo : ℚ) : ℝ) = -1 * cosLo.h i a := by simp [cosLo]
      rw [hx] at key
      exact key)
    (fun i j a b => by simp [arcHiW, cosLo])
    _ _ _ _ _ _ arcLoW_cert arcHiW_cert
  have e1 : ((1577 / 3240 : ℚ) : ℝ) = 1577 / 3240 := by norm_num
  have e2 : ((171810293 / 202500000 : ℚ) : ℝ) = 171810293 / 202500000 := by norm_num
  rw [e1, e2] at h
  exact h

end MetricChain.VoxelBridgeWitness
