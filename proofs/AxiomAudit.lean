import Mathlib
import proofs.Core.Basic
import proofs.Core.Rounding
import proofs.Frontiers.EnvelopeDuality
import proofs.Frontiers.Dominance
import proofs.Frontiers.HolderDecomposition
import proofs.Frontiers.FreeEnergySandwich
import proofs.Frontiers.HoffmanWielandt
import proofs.Frontiers.Realizability
import proofs.Frontiers.Holonomy
import proofs.Frontiers.TorsionRMSD
import proofs.Frontiers.InvariantEnvelope
import proofs.Frontiers.PartitionCertificate
import proofs.Frontiers.VoxelEnclosure
import proofs.Frontiers.SeparableVoxel
import proofs.CertificateAlgebra
import proofs.Frontiers.ProofComplexity

/-!
# Axiom audit and non-vacuity witnesses

* `#audit_axioms` walks **every** declaration in the `MetricChain` namespace and fails (throws)
  if any of them depends on an axiom other than `propext`, `Classical.choice`, `Quot.sound`.
  In particular `sorryAx`, `Lean.ofReduceBool` (native evaluation) and user axioms are rejected.
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

#audit_axioms MetricChain

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
#print axioms MetricChain.robust_minimizer_with_anchors_iff
#print axioms MetricChain.anchor_card_lower_bound
#print axioms MetricChain.admissible_of_single_site
#print axioms MetricChain.differential_dee_sound
#print axioms MetricChain.energy_window_exact

-- Dominance calculus (Directions A + D)
#print axioms MetricChain.partition_transport
#print axioms MetricChain.freeEnergy_prune_bracket
#print axioms MetricChain.thermal_dee
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
#print axioms MetricChain.zverify_sound
#print axioms MetricChain.Z_encloses_partitionFn
#print axioms MetricChain.voxel_boltzmann_bounds
#print axioms MetricChain.certified_voxel_partition
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

-- Certificate algebra (Direction E): Master Soundness Theorems and kernel-evaluated examples
#print axioms MetricChain.verify_sound
#print axioms MetricChain.verifyR_sound
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

/-- `anchor_card_lower_bound` has satisfiable hypotheses and a non-trivial conclusion: on two
states at envelope distance `1` with zero white-box energy and zero residual (`κ = 0`), an exact
certificate (`ε = 0`) with both states as anchors exists, and the theorem forces `2 ≤ |A|`. -/
example :
    (Finset.univ.filter fun _ : Bool => (0 : ℝ) + 0 - 0 < (1 - 0) * 1 - 0).card ≤
      (Finset.univ : Finset Bool).card := by
  classical
  have hne : (Finset.univ : Finset Bool).Nonempty := ⟨true, Finset.mem_univ _⟩
  refine anchor_card_lower_bound (d := discreteEnvelope (X := Bool) 1) (fun _ => 0) (fun _ => 0)
    (κ := 0) (by norm_num) ?_ Finset.univ hne (ε := 0) (Estar := 0) (σ := 1) ?_ ?_ ?_
  · intro x y
    unfold discreteEnvelope
    split_ifs <;> norm_num
  · intro a _
    norm_num
  · intro y
    have h1 : (0 : ℝ) - discreteEnvelope (X := Bool) 1 y y ≤
        lowerEnv (discreteEnvelope (X := Bool) 1) Finset.univ hne (fun _ => 0) y :=
      Finset.le_sup' (fun a => (0 : ℝ) - discreteEnvelope (X := Bool) 1 a y) (Finset.mem_univ y)
    have h2 : (Finset.univ : Finset Bool).inf' hne (fun a => (0 : ℝ) + 0) ≤ (0 : ℝ) + 0 :=
      Finset.inf'_le (fun _ => (0 : ℝ) + 0) (Finset.mem_univ y)
    simp only [discreteEnvelope, if_true] at h1
    linarith
  · intro a y hay
    unfold discreteEnvelope
    simp [hay]

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

end MetricChain.NonVacuity
