import Mathlib
import proofs.Core.Basic
import proofs.Core.Rounding
import proofs.Frontiers.EnvelopeDuality
import proofs.Frontiers.Dominance
import proofs.Frontiers.HolderDecomposition
import proofs.Frontiers.FreeEnergySandwich
import proofs.Frontiers.EnsembleDivergence
import proofs.Frontiers.HoffmanWielandt
import proofs.Frontiers.Realizability
import proofs.Frontiers.Holonomy
import proofs.Frontiers.TorsionRMSD
import proofs.Frontiers.InvariantEnvelope
import proofs.Frontiers.PartitionCertificate
import proofs.Frontiers.IntervalInstance
import proofs.Frontiers.VoxelEnclosure
import proofs.Frontiers.VoxelBridge
import proofs.Frontiers.SeparableVoxel
import proofs.CertificateAlgebra
import proofs.Frontiers.ProofComplexity

/-!
# Axiom audit and non-vacuity witnesses

* `#audit_axioms` (invoked at the end of this file) walks **every** declaration in the
  `MetricChain` namespace and fails (throws) if any of them depends on an axiom other than
  `propext`, `Classical.choice`, `Quot.sound`.  In particular `sorryAx`, `Lean.ofReduceBool`
  (native evaluation) and user axioms are rejected.
* The explicit `#print axioms` lines below list the headline theorems for human inspection;
  `scripts/audit_all.sh` parses them as a second, independent check.
* The `example`s at the end are non-vacuity witnesses: concrete instantiations showing that the
  hypotheses of each headline theorem are jointly satisfiable on non-trivial instances.
-/

open Lean Elab Command in
/-- Audit every declaration below the given namespace: only the three standard axioms are allowed. -/
elab "#audit_axioms " ns:ident : command => do
  let env ← getEnv
  let pfx := ns.getId
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count : Nat := 0
  let mut bad : Array (Name × Array Name) := #[]
  for (name, _) in env.constants.toList do
    if pfx.isPrefixOf name then
      count := count + 1
      let axs ← Lean.collectAxioms name
      let extra := axs.filter fun a => !allowed.contains a
      unless extra.isEmpty do
        bad := bad.push (name, extra)
  if bad.isEmpty then
    logInfo m!"AXIOM AUDIT OK: {count} declarations under `{pfx}` use only propext / Classical.choice / Quot.sound"
  else
    throwError "AXIOM AUDIT FAILED: {bad}"

/-! ### Headline theorems -/

-- Core: outward rounding, rational intervals, certified exp, rational circle atlas
#print axioms MetricChain.roundUp_sub_roundDown_le
#print axioms MetricChain.QInterval.contains_mul
#print axioms MetricChain.exp_enclosure
#print axioms MetricChain.QInterval.contains_boltzmann
#print axioms MetricChain.circle_rational_atlas

-- Envelope duality (Direction A): exact characterisations under non-decomposable residuals
#print axioms MetricChain.robust_minimizer_iff
#print axioms MetricChain.robust_certified_iff
#print axioms MetricChain.robust_min_bracket
#print axioms MetricChain.robust_partition_bracket
#print axioms MetricChain.robust_min_interval_exact
#print axioms MetricChain.robust_partition_interval_exact
#print axioms MetricChain.robust_minimizer_with_anchors_iff
#print axioms MetricChain.anchor_card_lower_bound
#print axioms MetricChain.admissible_of_single_site
#print axioms MetricChain.differential_dee_sound
#print axioms MetricChain.energy_window_exact

-- Dominance calculus (Directions A + D)
#print axioms MetricChain.partition_transport
#print axioms MetricChain.partition_prune_bracket_fibers
#print axioms MetricChain.freeEnergy_prune_bracket
#print axioms MetricChain.thermal_dee
#print axioms MetricChain.boltzmannAvg_prune_error
#print axioms MetricChain.boltzmannAvg_dominance_error
#print axioms MetricChain.isLeast_sum_of_block_separable
#print axioms MetricChain.exact_margin_of_block_separable
#print axioms MetricChain.PairModel.goldstein_isLeast
#print axioms MetricChain.PairModel.goldstein_gauge_invariant
#print axioms MetricChain.PairModel.desmet_reparam_le
#print axioms MetricChain.PairModel.desmet_optimalGauge

-- Partition functions (Direction D)
#print axioms MetricChain.freeEnergy_holder
#print axioms MetricChain.gibbs_bogoliubov
#print axioms MetricChain.hoeffding_upper
#print axioms MetricChain.partition_ratio_sandwich
#print axioms MetricChain.bounded_differences_sandwich
#print axioms MetricChain.exists_two_level_worst_residual
#print axioms MetricChain.mcdiarmid_no_better_constant
#print axioms MetricChain.kl_reference_target_eq_gap
#print axioms MetricChain.kl_reference_target_le_bounded_differences
#print axioms MetricChain.bounded_differences_sandwich_any_reference
#print axioms MetricChain.kl_reference_target_le_any_reference
#print axioms MetricChain.correlated_reference_counterexample
#print axioms MetricChain.zverify_sound
#print axioms MetricChain.zverifyTop_sound
#print axioms MetricChain.negativeW_rejected
#print axioms MetricChain.Z_encloses_partitionFn
#print axioms MetricChain.certified_partition_of_intervals
#print axioms MetricChain.triangle_real_partition_enclosure
#print axioms MetricChain.voxel_boltzmann_bounds
#print axioms MetricChain.certified_voxel_partition
#print axioms MetricChain.pairwise_voxel_weight_bounds
#print axioms MetricChain.certified_torsion_partition
#print axioms MetricChain.certified_torsion_partition_full
#print axioms MetricChain.certified_torsion_partition_top
#print axioms MetricChain.two_arctan_sub_bounds
#print axioms MetricChain.chartArc_onebody_brackets
#print axioms MetricChain.VoxelBridgeWitness.chart_witness
#print axioms MetricChain.separable_voxel_bounds
#print axioms MetricChain.separable_voxel_ratio
#print axioms MetricChain.triangleZ_exact

-- Realizability and geometric stability (Direction C)
#print axioms MetricChain.hoffman_wielandt
#print axioms MetricChain.rank_psd_trace_obstruction
#print axioms MetricChain.K_identity
#print axioms MetricChain.sstress_lower_bound
#print axioms MetricChain.simplex_sstress_lower_bound
#print axioms MetricChain.simplex_not_realizable
#print axioms MetricChain.norm_holProd_le_sum
#print axioms MetricChain.norm_holTrans_le
#print axioms MetricChain.rigidWithin_chain
#print axioms MetricChain.exists_coaxial_angle
#print axioms MetricChain.IsTorsionMove.rigidWithin
#print axioms MetricChain.rigidWithin_torsion_chain
#print axioms MetricChain.residual_torsion_chain
#print axioms MetricChain.residual_torsion_chain_in
#print axioms MetricChain.residual_torsion_move_uniform
#print axioms MetricChain.residual_torsion_move_min_in
#print axioms MetricChain.residualLowerClass_of_rigidWithinIn
#print axioms MetricChain.residualLowerClass_of_invariant_lipschitz
#print axioms MetricChain.verifyR_sound_invariant

-- Certificate algebra (Direction E): Master Soundness Theorems and kernel-evaluated examples
#print axioms MetricChain.verify_sound
#print axioms MetricChain.verifyR_sound
#print axioms MetricChain.verifyR_sound_lower
#print axioms MetricChain.RProblem.consistent_iff_nonempty
#print axioms MetricChain.verifyRTop_sound
#print axioms MetricChain.verifyRLowerTop_sound
#print axioms MetricChain.negativeEnvelope_rejected
#print axioms MetricChain.certified_gap_interval
#print axioms MetricChain.inconsistentResidual_rejected
#print axioms MetricChain.certified_gap
#print axioms MetricChain.verify_sound_real
#print axioms MetricChain.verifyR_sound_real
#print axioms MetricChain.triangle_verified
#print axioms MetricChain.triangleResidual_gap
#print axioms MetricChain.leaf_two_config
#print axioms MetricChain.triangle_no_leaf_certificate
#print axioms MetricChain.sumFree_exponential
#print axioms MetricChain.sumFree_gap_exponential
#print axioms MetricChain.sumFree_complexity
#print axioms MetricChain.sumFree_tight
#print axioms MetricChain.sum_linear
#print axioms MetricChain.sum_rule_separation
#print axioms MetricChain.sum_rule_separation_size
#print axioms MetricChain.sum_rule_separation_dataSize

/-! ### Non-vacuity witnesses -/

namespace MetricChain.NonVacuity

open Finset

/-- The discrete envelope on `Bool` with oscillation `1` is an envelope, and the zero residual is
admissible for it: the hypotheses of the envelope-duality theorems are satisfiable. -/
example : IsEnvelope (discreteEnvelope (X := Bool) 1) ∧ Admissible (discreteEnvelope (X := Bool) 1) fun _ => 0 :=
  ⟨discreteEnvelope_isEnvelope (by norm_num), fun x y => by unfold discreteEnvelope; split_ifs <;> norm_num⟩

/-- `robust_minimizer_iff` is not vacuous in either direction: with `f true = 0`, `f false = 2`
and oscillation `1`, `true` is robustly optimal-for-some-residual and `false` is not. -/
example :
    (∃ g, Admissible (discreteEnvelope (X := Bool) 1) g ∧
        ∀ y, (fun b : Bool => if b then (0 : ℝ) else 2) true + g true ≤
          (fun b : Bool => if b then (0 : ℝ) else 2) y + g y) ∧
      ¬ (∃ g, Admissible (discreteEnvelope (X := Bool) 1) g ∧
        ∀ y, (fun b : Bool => if b then (0 : ℝ) else 2) false + g false ≤
          (fun b : Bool => if b then (0 : ℝ) else 2) y + g y) := by
  constructor
  · exact (energy_window_exact (ω := 1) (by norm_num)
      (fun b : Bool => if b then (0 : ℝ) else 2) true).mpr (fun y => by cases y <;> norm_num)
  · intro h
    have := (energy_window_exact (ω := 1) (by norm_num)
      (fun b : Bool => if b then (0 : ℝ) else 2) false).mp h true
    norm_num at this

/-- `anchor_necessary` forces a non-trivial conclusion: on two states at envelope distance `1`
with zero white-box energy and zero residual (`κ = 0`), *every* exact certificate (`ε = 0`) must
evaluate both states. -/
example (A : Finset Bool) (hA : A.Nonempty)
    (hcert : ∀ y, A.inf' hA (fun _ => (0 : ℝ) + 0) - 0 ≤
      (0 : ℝ) + lowerEnv (discreteEnvelope (X := Bool) 1) A hA (fun _ => 0) y) :
    A = Finset.univ := by
  ext y
  simp only [Finset.mem_univ, iff_true]
  refine anchor_necessary (d := discreteEnvelope (X := Bool) 1) (fun _ => 0) (fun _ => 0)
    (κ := 0) (by norm_num) ?_ A hA (ε := 0) (Estar := 0) (σ := 1) ?_ hcert y ?_ ?_
  · intro x y
    unfold discreteEnvelope
    split_ifs <;> norm_num
  · intro a _
    norm_num
  · intro a _ hay
    unfold discreteEnvelope
    simp [hay]
  · norm_num

/-- … and such a certificate exists: with both states evaluated the certificate condition holds,
so the hypotheses of `anchor_necessary` / `anchor_card_lower_bound` are jointly satisfiable. -/
example : ∀ y, (Finset.univ : Finset Bool).inf' ⟨true, Finset.mem_univ _⟩ (fun _ => (0 : ℝ) + 0) - 0 ≤
    (0 : ℝ) + lowerEnv (discreteEnvelope (X := Bool) 1) Finset.univ ⟨true, Finset.mem_univ _⟩
      (fun _ => 0) y := by
  intro y
  have hne : (Finset.univ : Finset Bool).Nonempty := ⟨true, Finset.mem_univ _⟩
  have h1 : (0 : ℝ) - discreteEnvelope (X := Bool) 1 y y ≤
      lowerEnv (discreteEnvelope (X := Bool) 1) Finset.univ hne (fun _ => 0) y :=
    Finset.le_sup' (fun a => (0 : ℝ) - discreteEnvelope (X := Bool) 1 a y) (Finset.mem_univ y)
  have h2 : (Finset.univ : Finset Bool).inf' hne (fun _ => (0 : ℝ) + 0) ≤ (0 : ℝ) + 0 :=
    Finset.inf'_le (fun _ => (0 : ℝ) + 0) (Finset.mem_univ y)
  simp only [discreteEnvelope, if_true] at h1
  linarith

/-- The dominance transport lemma applies to a concrete two-state system: state `false`
(energy `3`) is dominated by `true` (energy `1`) with margin `2`. -/
example : partitionFn 1 (fun b : Bool => if b then (1 : ℝ) else 3) {false} ≤
    Real.exp (-1 * 2) * partitionFn 1 (fun b : Bool => if b then (1 : ℝ) else 3) {true} := by
  apply partition_transport (by norm_num) _ (fun _ => true)
  · intro x hx y hy _
    simp only [Finset.coe_singleton, Set.mem_singleton_iff] at hx hy
    rw [hx, hy]
  · intro x _
    simp
  · intro x hx
    simp only [Finset.mem_singleton] at hx
    subst hx
    norm_num

/-- The kernel's master theorem is exercised on a concrete instance with a tight bound. -/
example : (∀ x : Config 3 2, 1 ≤ triangle.energy x) ∧ triangle.energy ![0, 1, 0] = 1 :=
  ⟨triangle_lower_bound, triangle_optimum⟩

/-- `robust_minimizer_with_anchors_iff` discriminates: with one anchor (`true`, value `0`),
oscillation `1`, and white-box energies `f true = 0`, `f false = 3`, the state `false` cannot be
optimal for any admissible residual matching the anchor, whereas `true` can. -/
example :
    (∃ g, Admissible (discreteEnvelope (X := Bool) 1) g ∧ (∀ a ∈ ({true} : Finset Bool), g a = 0) ∧
        ∀ y, (fun b : Bool => if b then (0 : ℝ) else 3) true + g true ≤
          (fun b : Bool => if b then (0 : ℝ) else 3) y + g y) ∧
      ¬ (∃ g, Admissible (discreteEnvelope (X := Bool) 1) g ∧
        (∀ a ∈ ({true} : Finset Bool), g a = 0) ∧
        ∀ y, (fun b : Bool => if b then (0 : ℝ) else 3) false + g false ≤
          (fun b : Bool => if b then (0 : ℝ) else 3) y + g y) := by
  have hd := discreteEnvelope_isEnvelope (X := Bool) (ω := 1) (by norm_num)
  have hA : ({true} : Finset Bool).Nonempty := Finset.singleton_nonempty true
  have hv : ∀ a ∈ ({true} : Finset Bool), ∀ b ∈ ({true} : Finset Bool),
      (fun _ : Bool => (0 : ℝ)) a - (fun _ : Bool => (0 : ℝ)) b ≤
        discreteEnvelope (X := Bool) 1 a b := by
    intro a ha b hb
    rw [Finset.mem_singleton] at ha hb
    subst ha
    subst hb
    simp [discreteEnvelope]
  constructor
  · refine (robust_minimizer_with_anchors_iff hd {true} hA (fun _ => 0) hv
      (fun b : Bool => if b then (0 : ℝ) else 3) true).mpr ⟨fun y => ?_, fun y => ?_⟩
    · cases y
      · simp [discreteEnvelope]
        norm_num
      · simp [discreteEnvelope]
    · simp only [lowerEnv, upperEnv, Finset.sup'_singleton, Finset.inf'_singleton]
      cases y
      · simp [discreteEnvelope]
        norm_num
      · simp [discreteEnvelope]
  · intro h
    have h2 := ((robust_minimizer_with_anchors_iff hd {true} hA (fun _ => 0) hv
      (fun b : Bool => if b then (0 : ℝ) else 3) false).mp h).2 true
    simp [lowerEnv, upperEnv, Finset.sup'_singleton, Finset.inf'_singleton, discreteEnvelope] at h2

/-- `verify_sound_real` applies to a real pairwise model whose tables are bounded below by the
rational triangle instance: its energy is at least `1` everywhere. -/
example (M : PairModel ℝ (Fin 3) (fun _ => Fin 2))
    (hh : ∀ i a, ((triangle.h i a : ℚ) : ℝ) ≤ M.h i a)
    (hJ : ∀ i j a b, ((triangle.J i j a b : ℚ) : ℝ) ≤ M.J i j a b) (x : Config 3 2) :
    ((1 : ℚ) : ℝ) ≤ M.energy x :=
  verify_sound_real triangleCert triangle (fullDom 3 2) 1 triangle_verified M hh hJ x
    (inBox_fullDom x)

/-- `boltzmannAvg_dominance_error` on a two-state system (margin `2`): discarding the dominated
state changes the average of any observable bounded by `1` by at most `2 e^{-2}`. -/
example (f : Bool → ℝ) (hf : ∀ b, |f b| ≤ 1) :
    |boltzmannAvg 1 (fun b : Bool => if b then (1 : ℝ) else 3) f ({false} ∪ {true}) -
        boltzmannAvg 1 (fun b : Bool => if b then (1 : ℝ) else 3) f {true}| ≤
      2 * 1 * Real.exp (-1 * 2) := by
  apply boltzmannAvg_dominance_error (by norm_num) _ f (fun _ => true)
  · intro x hx y hy _
    simp only [Finset.coe_singleton, Set.mem_singleton_iff] at hx hy
    rw [hx, hy]
  · intro x _
    simp
  · intro x hx
    simp only [Finset.mem_singleton] at hx
    subst hx
    norm_num
  · simp
  · exact Finset.singleton_nonempty true
  · intro x _
    exact hf x

/-- The relative-entropy identity is instantiated on the uniform two-state reference. -/
example (Δ : Bool → ℝ) (β : ℝ) :
    klFin (fun _ : Bool => (1 / 2 : ℝ)) (tilt (fun _ => 1 / 2) Δ β) =
      β * ∑ x : Bool, (1 / 2 : ℝ) * Δ x + Real.log (∑ x : Bool, (1 / 2 : ℝ) * Real.exp (-β * Δ x)) :=
  kl_reference_target_eq_gap (fun _ => 1 / 2) Δ (fun _ => by norm_num)
    (by rw [Fintype.sum_bool]; norm_num) β

/-- `robust_min_interval_exact` on two states with one anchor (`true`, value `0`) and oscillation
`1`: the envelope optima are `-1` and `0`, and *every* value in between is the optimal value of
`f + g` for an admissible residual matching the anchor. -/
example (τ : ℝ) (h1 : -1 ≤ τ) (h0 : τ ≤ 0) :
    ∃ g : Bool → ℝ, Admissible (discreteEnvelope (X := Bool) 1) g ∧ g true = 0 ∧
      (Finset.univ : Finset Bool).inf' ⟨true, Finset.mem_univ _⟩ (fun y => (0 : ℝ) + g y) = τ := by
  have hd := discreteEnvelope_isEnvelope (X := Bool) (ω := 1) (by norm_num)
  have hA : ({true} : Finset Bool).Nonempty := Finset.singleton_nonempty true
  have hv : ∀ a ∈ ({true} : Finset Bool), ∀ b ∈ ({true} : Finset Bool),
      (fun _ : Bool => (0 : ℝ)) a - (fun _ : Bool => (0 : ℝ)) b ≤
        discreteEnvelope (X := Bool) 1 a b := by
    intro a ha b hb
    rw [Finset.mem_singleton] at ha hb
    subst ha
    subst hb
    simp [discreteEnvelope]
  obtain ⟨g, hg, hga, hmin⟩ := robust_min_interval_exact hd {true} hA (fun _ => 0) hv
    (fun _ => 0) Finset.univ ⟨true, Finset.mem_univ _⟩ τ (by
      constructor
      · apply (Finset.inf'_le _ (Finset.mem_univ false)).trans
        simp [lowerEnv, discreteEnvelope]
        linarith
      · apply Finset.le_inf'
        intro y _
        cases y <;> simp [upperEnv, discreteEnvelope] <;> linarith)
  exact ⟨g, hg, hga true (Finset.mem_singleton_self true), hmin⟩

/-- The top-level residual kernel is not vacuous: on the triangle problem the residual class is
non-empty and the certified bound holds for every residual in the (lower) class. -/
example : (∃ g : Config 3 2 → ℝ, ResidualClass triangleResidual g) ∧
    ∀ g : Config 3 2 → ℝ, ResidualLowerClass triangleResidual g →
      ∀ x : Config 3 2, ((1 / 8 : ℚ) : ℝ) ≤ (triangle.energy x : ℝ) + g x := by
  obtain ⟨h1, h2⟩ := verifyRTop_sound triangleResidualCert triangleResidual (fullDom 3 2) (1 / 8)
    triangleResidual_verifiedTop
  exact ⟨h1, fun g hg x => h2 g hg x (inBox_fullDom x)⟩

/-! #### A genuine instance of the invariant-residual pipeline

One torsion with two states (angles `0` and `π`), two atoms at unit distance from the axis (atom
`0` static, atom `1` rotating), residual `Δ X = dist (X 0) (X 1)` (invariant under all isometries,
`2`-Lipschitz).  The reduced inertia is `1/2` in every state, so the uniform constant is
`Λ · 2 √(2 · 1/2) = 4`. -/

/-- the reference point at unit distance from the axis -/
noncomputable def wP : AxisSpace := WithLp.toLp 2 ((1 : ℂ), (0 : ℝ))

/-- torsion angle of a state -/
noncomputable def wθ (s : Fin 2) : ℝ := if s = 0 then 0 else Real.pi

/-- embedding of the one-torsion state space -/
noncomputable def wEmb (x : Config 1 2) : Fin 2 → AxisSpace :=
  fun i => if i = 1 then axisRot (wθ (x 0)) wP else wP

/-- the residual: distance between the two atoms -/
noncomputable def wΔ (X : Fin 2 → AxisSpace) : ℝ := dist (X 0) (X 1)

theorem wΔ_invariant : RigidInvariantIn (⊤ : Submonoid (AxisSpace ≃ᵢ AxisSpace)) wΔ := by
  intro g _ y
  show dist (g (y 0)) (g (y 1)) = dist (y 0) (y 1)
  exact g.dist_eq _ _

theorem wΔ_lipschitz : ConfigLipschitz 2 wΔ := by
  intro x y
  have h1 : |dist (x 0) (x 1) - dist (y 0) (y 1)| ≤ dist (x 0) (y 0) + dist (x 1) (y 1) := by
    have := dist_dist_dist_le (x 0) (x 1) (y 0) (y 1)
    rwa [Real.dist_eq] at this
  have h2 : ∀ i : Fin 2, dist (x i) (y i) ≤ Real.sqrt (∑ j, dist (x j) (y j) ^ 2) := by
    intro i
    calc dist (x i) (y i) = Real.sqrt (dist (x i) (y i) ^ 2) := (Real.sqrt_sq dist_nonneg).symm
      _ ≤ Real.sqrt (∑ j, dist (x j) (y j) ^ 2) :=
        Real.sqrt_le_sqrt (Finset.single_le_sum (f := fun j => dist (x j) (y j) ^ 2)
          (fun j _ => sq_nonneg _) (Finset.mem_univ i))
  show |dist (x 0) (x 1) - dist (y 0) (y 1)| ≤ 2 * Real.sqrt (∑ j, dist (x j) (y j) ^ 2)
  linarith [h2 0, h2 1]

theorem wMove (x : Config 1 2) (i : Fin 1) (s : Fin 2) :
    ∃ (u : AxisSpace ≃ᵢ AxisSpace) (B : Finset (Fin 2)) (δ : ℝ),
      (∀ ψ : ℝ, u.trans ((axisRot ψ).trans u.symm) ∈ (⊤ : Submonoid (AxisSpace ≃ᵢ AxisSpace))) ∧
        IsTorsionMove u B δ (wEmb x) (wEmb (Function.update x i s)) ∧
          reducedInertia u B (wEmb x) ≤ 1 / 2 := by
  have hi : i = 0 := Subsingleton.elim i 0
  subst hi
  refine ⟨IsometryEquiv.refl AxisSpace, {1}, wθ s - wθ (x 0), fun ψ => Submonoid.mem_top _,
    ⟨fun j hj => ?_, fun j hj => ?_⟩, ?_⟩
  · have hj' : j ≠ 1 := by simpa using hj
    simp [wEmb, hj']
  · have hj' : j = 1 := by simpa using hj
    subst hj'
    show wEmb (Function.update x 0 s) 1 = axisRot (wθ s - wθ (x 0)) (wEmb x 1)
    simp only [wEmb, if_true, Function.update_self]
    rw [axisRot_axisRot, sub_add_cancel]
  · have hA : axialInertia (IsometryEquiv.refl AxisSpace) ({1} : Finset (Fin 2))ᶜ (wEmb x) = 1 := by
      have hc : ({1} : Finset (Fin 2))ᶜ = {0} := by decide
      rw [hc, axialInertia, sum_singleton]
      show ‖(wEmb x 0).fst‖ ^ 2 = 1
      simp [wEmb, wP]
    have hB : axialInertia (IsometryEquiv.refl AxisSpace) ({1} : Finset (Fin 2)) (wEmb x) = 1 := by
      rw [axialInertia, sum_singleton]
      show ‖(wEmb x 1).fst‖ ^ 2 = 1
      simp [wEmb, wP, axisRot_fst]
    rw [reducedInertia, hA, hB]
    norm_num

/-- the residual problem: no pairwise energy, envelope constant `4`, one anchor (state `0`,
published value `0 ≤ Δ`) -/
def wProblem : RProblem 1 2 where
  base := { h := fun _ _ => 0, J := fun _ _ _ _ => 0 }
  c := fun _ => 4
  anchors := [(![0], 0)]

/-- All hypotheses of `verifyR_sound_invariant` hold in this instance, and its conclusion is the
concrete certified bound `-4 ≤ E + Δ ∘ emb` on both states. -/
example (x : Config 1 2) : ((-4 : ℚ) : ℝ) ≤ (wProblem.base.energy x : ℝ) + wΔ (wEmb x) := by
  have hv : verifyR (.anchor 0 (.leaf (fun _ => -4) (fun _ _ => 0) (fun _ _ _ => 0))) wProblem
      (fullDom 1 2) (-4) = true := by decide +kernel
  refine verifyR_sound_invariant (Λ := 2) (by norm_num) wΔ_invariant wΔ_lipschitz wEmb
    (fun _ => 1 / 2) wMove wProblem ?_ ?_ _ (fullDom 1 2) (-4) hv x (inBox_fullDom x)
  · intro i
    have h : Real.sqrt (2 * (1 / 2)) = 1 := by norm_num
    rw [h]
    show (2 : ℝ) * (2 * 1) ≤ ((4 : ℚ) : ℝ)
    norm_num
  · intro p hp
    have hp' : p = (![0], 0) := by simpa [wProblem] using hp
    subst hp'
    show ((0 : ℚ) : ℝ) ≤ wΔ (wEmb ![0])
    rw [Rat.cast_zero]
    exact dist_nonneg

end MetricChain.NonVacuity

/-! ### Automatic audit of every declaration (run last, so that it also covers the definitions
used by the witnesses above) -/

#audit_axioms MetricChain

