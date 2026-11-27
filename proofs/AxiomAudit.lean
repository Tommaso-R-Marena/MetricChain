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
import proofs.Frontiers.CertificationGeometry
import proofs.Frontiers.CertificateNotions
import proofs.Frontiers.ConditionalEnvelope
import proofs.Frontiers.CertificateComplexity
import proofs.Frontiers.ExponentialWeights
import proofs.Frontiers.ProductRates
import proofs.Frontiers.BestFirst
import proofs.Frontiers.ThermalRobustness
import proofs.Frontiers.SecondOrderEnvelope
import proofs.Frontiers.HigherOrderEnvelope
import proofs.Frontiers.SampledSandwich
import proofs.Frontiers.PartitionProduct
import proofs.Frontiers.RefereeLemmas
import proofs.Frontiers.QueryLowerBound
import proofs.Frontiers.SoftGapBounds
import proofs.Frontiers.QueryRefinements
import proofs.Frontiers.GeneralisedDips
import proofs.Frontiers.NormalForm
import proofs.Frontiers.SecondOrderDip
import proofs.Frontiers.SoftGapIndependence
import proofs.Frontiers.NonAdaptive
import proofs.Frontiers.LinearClass
import proofs.Frontiers.LinearKernel
import proofs.Frontiers.HintRecursion
import proofs.Frontiers.CubeHintPair
import proofs.Frontiers.BoundedAccuracy
import proofs.Frontiers.FieldShift
import proofs.Frontiers.GamePair
import proofs.Frontiers.CoverStability
import proofs.Frontiers.SetLimit
import proofs.Frontiers.TypeQuantiles
import proofs.Frontiers.SymmetricSampling
import proofs.Frontiers.TwoRounds
import proofs.Frontiers.TwoRoundsExpected
import proofs.Frontiers.GroupSampling
import proofs.Frontiers.SliceRefinement
import proofs.Frontiers.RenyiCentre
import proofs.Frontiers.MacroRatio
import proofs.Frontiers.Scattering
import proofs.Frontiers.BoxClass
import proofs.Frontiers.MonotoneSandwich
import proofs.Frontiers.ThirdOrderModel
import proofs.Frontiers.ShareCertificates
import proofs.Frontiers.HilbertBall
import proofs.Frontiers.BoxRatio
import proofs.Frontiers.AnchoredRemainder
import proofs.Frontiers.KineticsCertificates
import proofs.Frontiers.BarrierCertificate
import proofs.Frontiers.OracleCompensation
import proofs.Frontiers.OracleLowerBound
import proofs.Frontiers.ProductSamplerChainRule
import proofs.Frontiers.StateShares
import proofs.Frontiers.SoftMinLowerBound
import proofs.Frontiers.BennettTwoPoint
import proofs.Frontiers.BoxBennett
import proofs.Frontiers.ShareLevels
import proofs.Frontiers.DownClosedRemainder
import proofs.Frontiers.BoxAdditions
import proofs.Frontiers.AffineHalf
import proofs.Frontiers.BlockReductions
import proofs.Frontiers.RateFull
import proofs.Frontiers.SandwichCost
import proofs.Frontiers.SymmetricPairHypothesis
import proofs.Frontiers.SplitRule
import proofs.Frontiers.CoreGreedy
import proofs.Frontiers.TermOrders
import proofs.Frontiers.LineDynamics
import proofs.Frontiers.ResolvedPenalties
import proofs.Frontiers.GibbsRecovery
import proofs.Frontiers.Bonferroni
import proofs.Frontiers.FactorElimination
import proofs.AuditCommand

/-!
# Axiom audit and non-vacuity witnesses

* `#audit_axioms proofs` (defined in `AuditCommand.lean`, invoked as the last command of this
  file) walks **every** constant defined in a module of this project or in this file — whatever
  its namespace or visibility — and fails (throws) if any of them depends on an axiom other than
  `propext`, `Classical.choice`, `Quot.sound`.  In particular the placeholder axiom of incomplete
  proofs, the axiom of native evaluation and user axioms are rejected.
* The explicit `#print axioms` lines below list the headline theorems for human inspection;
  `scripts/audit_all.sh` parses them as a second, independent check.
* The theorems in the namespace `MetricChain.NonVacuity` are non-vacuity witnesses: concrete
  instantiations showing that the hypotheses of each headline theorem are jointly satisfiable on
  non-trivial instances.  They are *named* declarations (not anonymous examples) so that the
  automatic audit covers them too.
-/

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
#print axioms MetricChain.chartArc_onebody_brackets_pos
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
#print axioms MetricChain.rigidWithinIn_torsion_chain_min
#print axioms MetricChain.residual_torsion_chain
#print axioms MetricChain.residual_torsion_chain_in
#print axioms MetricChain.residual_torsion_move_uniform
#print axioms MetricChain.residual_torsion_move_min_in
#print axioms MetricChain.residualLowerClass_of_rigidWithinIn
#print axioms MetricChain.residualLowerClass_of_invariant_lipschitz
#print axioms MetricChain.verifyR_sound_invariant
#print axioms MetricChain.verifyITop_sound_invariant

-- Certificate algebra (Direction E): Master Soundness Theorems and kernel-evaluated examples
#print axioms MetricChain.verify_sound
#print axioms MetricChain.verifyR_sound
#print axioms MetricChain.verifyR_sound_lower
#print axioms MetricChain.RProblem.consistent_iff_nonempty
#print axioms MetricChain.verifyRTop_sound
#print axioms MetricChain.verifyRLowerTop_sound
#print axioms MetricChain.IProblem.consistent_iff_nonempty
#print axioms MetricChain.verifyITop_sound
#print axioms MetricChain.verifyITop_ofExact
#print axioms MetricChain.verifyITop_ofLower
#print axioms MetricChain.inconsistentInterval_rejected
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

-- Certification geometry (second phase): slack coverings and the three notions of certificate
#print axioms MetricChain.slack_isEnvelope
#print axioms MetricChain.certLB_eq
#print axioms MetricChain.isCertificate_iff_cover
#print axioms MetricChain.certificate_of_cover
#print axioms MetricChain.card_ge_of_weights
#print axioms MetricChain.card_ge_of_fooling
#print axioms MetricChain.card_ge_sum_inv
#print axioms MetricChain.partition_bound
#print axioms MetricChain.anchor_necessary'
#print axioms MetricChain.isConfigCertificate_iff
#print axioms MetricChain.cover_of_isValueCertificate
#print axioms MetricChain.isConfigCertificate_of_isCertificate
#print axioms MetricChain.isCertificate_insert_of_isConfigCertificate

-- Conditional envelope: evaluations as a tropical rank-one update
#print axioms MetricChain.condEnv_isEnvelope
#print axioms MetricChain.condEnv_isGreatest
#print axioms MetricChain.condEnv_tower
#print axioms MetricChain.robust_minimizer_with_anchors_iff'
#print axioms MetricChain.robust_certified_with_anchors_iff
#print axioms MetricChain.worst_case_regret_isGreatest

-- Certificate complexity: hardness, product landscapes, exponential-weights converses
#print axioms MetricChain.domCertificate_iff
#print axioms MetricChain.domCertificate_min_card
#print axioms MetricChain.product_single_certificate_iff
#print axioms MetricChain.partition_bound_hamming
#print axioms MetricChain.product_partition_bound
#print axioms MetricChain.homogeneous_certificate_dichotomy
#print axioms MetricChain.binary_certificate_exponential
#print axioms MetricChain.card_ge_exp_weights
#print axioms MetricChain.card_ge_entropy
#print axioms MetricChain.thermal_exp_weights
#print axioms MetricChain.product_exp_weights
#print axioms MetricChain.thermal_product_exp_weights
#print axioms MetricChain.thermal_binary_exponential

-- Best-first search with resource augmentation
#print axioms MetricChain.bestFirst_sep_a
#print axioms MetricChain.bestFirst_sep_b
#print axioms MetricChain.bestFirst_sep_c
#print axioms MetricChain.not_cocovered
#print axioms MetricChain.bestFirst_card_le
#print axioms MetricChain.bestFirst_certifies
#print axioms MetricChain.bestFirst_card_le_sharp

-- Finite temperature: thermal contact, free-energy certificates, transport-entropy
#print axioms MetricChain.gibbsProb_range_eq
#print axioms MetricChain.gibbsProb_range_with_anchors_eq
#print axioms MetricChain.admissible_iff_weights
#print axioms MetricChain.Zhi_eq
#print axioms MetricChain.mean_slack_le
#print axioms MetricChain.card_ge_laplace
#print axioms MetricChain.logMGF_le_transport_entropy
#print axioms MetricChain.gap_le_of_T1

-- Second-order envelopes: star sandwich, exact envelope, certified minimiser
#print axioms MetricChain.secondOrder_remainder
#print axioms MetricChain.pairwise_sandwich
#print axioms MetricChain.verify_sound_secondOrder
#print axioms MetricChain.secondOrder_envelope_exact
#print axioms MetricChain.secondOrder_robust_min_exact
#print axioms MetricChain.secondOrder_certified_minimizer_iff
#print axioms MetricChain.anchored_decomposition
#print axioms MetricChain.higherOrder_remainder
#print axioms MetricChain.higherOrder_remainder_sharp
#print axioms MetricChain.secondOrder_remainder_of_higherOrder
#print axioms MetricChain.higherOrder_witness

-- Probabilistic certificates: the sampled free-energy sandwich
#print axioms MetricChain.sample_mgf
#print axioms MetricChain.sample_mean_two_sided
#print axioms MetricChain.sampled_free_energy_sandwich
#print axioms MetricChain.sampled_free_energy_sandwich_good
#print axioms MetricChain.sampled_free_energy_sandwich_of_sample_size

-- Partition kernel with decomposition rules
#print axioms MetricChain.zverify2_sound
#print axioms MetricChain.zverify2Top_sound
#print axioms MetricChain.WInstance.Z_cut
#print axioms MetricChain.cut_rule_separation
#print axioms MetricChain.WInstance.Z_elim1
#print axioms MetricChain.WInstance.Z_elim2
#print axioms MetricChain.elimination_separation
#print axioms MetricChain.zverify2Top_chainCert
#print axioms MetricChain.chain_separation
#print axioms MetricChain.ferroChain_separation

-- Lemmas of the second referee: the certificate notions coincide; limitations
#print axioms MetricChain.config_exchange
#print axioms MetricChain.value_exchange
#print axioms MetricChain.exact_free_energy_certificate_eq_univ
#print axioms MetricChain.gauge_trivial_separation

-- Query complexity: every algorithm, deterministic or randomised
#print axioms MetricChain.exists_query_ne
#print axioms MetricChain.prob_query_ne_ge
#print axioms MetricChain.expected_queries_ge_packing
#print axioms MetricChain.queries_strict_cover
#print axioms MetricChain.queries_isValueCertificate
#print axioms MetricChain.certificateAlgorithm_correct
#print axioms MetricChain.instance_query_complexity
#print axioms MetricChain.expected_queries_ge
#print axioms MetricChain.expected_queries_ge_exp_weights_min
#print axioms MetricChain.binary_randomized_exponential
#print axioms MetricChain.log_sum_exp_dip_ge
#print axioms MetricChain.thermal_queries_strict_cover
#print axioms MetricChain.thermal_queries_bracket
#print axioms MetricChain.thermal_expected_queries_ge
#print axioms MetricChain.cube_thermal_randomized_exponential
#print axioms MetricChain.cube_thermal_randomized_bound
#print axioms MetricChain.spotCheck_correct
#print axioms MetricChain.min_spotCheck_correct

-- Soft-gap bounds: randomised upper bound, product form, deterministic against randomised
#print axioms MetricChain.softGap_le_add_slack
#print axioms MetricChain.detection_weight_ge
#print axioms MetricChain.thermal_spotCheck_correct
#print axioms MetricChain.exists_thermal_spotCheck_sample_size
#print axioms MetricChain.cube_deterministic_lower_bound
#print axioms MetricChain.cube_dipWeight_sum
#print axioms MetricChain.softGap_hamEnv_additive
#print axioms MetricChain.thermal_product_randomized

-- Refinements after the third referee report: pair detection, hedged spot-check, tiny accuracies
#print axioms MetricChain.exists_query_ne_pair
#print axioms MetricChain.prob_query_ne_pair
#print axioms MetricChain.hedgedSpotCheck_correct
#print axioms MetricChain.min_hedgedSpotCheck_correct
#print axioms MetricChain.cube_small_accuracy_randomized
#print axioms MetricChain.cube_exact_randomized
#print axioms MetricChain.thermal_exact_dip_randomized
#print axioms MetricChain.cube_exact_dip_randomized
#print axioms MetricChain.Referee3.pathoAlg_not_a_tree
#print axioms MetricChain.Referee3.packing_factor_attained

-- Generalised dips and the two-measure sandwich (after workstream A)
#print axioms MetricChain.genDip_admissible
#print axioms MetricChain.log_sum_exp_genDip_ge
#print axioms MetricChain.genDip_expected_queries_ge
#print axioms MetricChain.genDip_expected_queries_ge_exp_weights
#print axioms MetricChain.genDip_recovers_dips
#print axioms MetricChain.twoMeasureBound_prod
#print axioms MetricChain.twoMeasureBound_pow
#print axioms MetricChain.mass_ge_of_twoMeasureBound
#print axioms MetricChain.product_mass_ge
#print axioms MetricChain.sumSig_lipschitz
#print axioms MetricChain.genDip_product_effect
#print axioms MetricChain.detect_weight_le
#print axioms MetricChain.twoMeasureLower_prod
#print axioms MetricChain.twoMeasureLower_pow
#print axioms MetricChain.product_sandwich

-- Normal form (after workstream C) and dense second-order classes (after workstream E)
#print axioms MetricChain.reduce_isEnvelope
#print axioms MetricChain.admissible_reduce_iff
#print axioms MetricChain.inf_add_phEnv_eq
#print axioms MetricChain.certLB_normalForm
#print axioms MetricChain.certUB_normalForm
#print axioms MetricChain.isValueCertificate_iff_normalForm
#print axioms MetricChain.isValueCertificate_normalForm_iff
#print axioms MetricChain.not_cocovered_centre
#print axioms MetricChain.SecondOrderDip.dip_mixedDiffBound
#print axioms MetricChain.SecondOrderDip.dip_witness
#print axioms MetricChain.SecondOrderDip.star_upper
#print axioms MetricChain.SecondOrderDip.stars_do_not_combine
#print axioms MetricChain.sum_gibbs_exp_softGap_indep
#print axioms MetricChain.sum_dipWeight_indep
#print axioms MetricChain.spotCheck_const_le_cover
#print axioms MetricChain.nonadaptive_expected_queries_ge
#print axioms MetricChain.cube_nonadaptive_bound
#print axioms MetricChain.sum_le_truncated_add_tail
#print axioms MetricChain.sum_truncated_ge
#print axioms MetricChain.linRes_sub_attained
#print axioms MetricChain.linRes_span_upper
#print axioms MetricChain.linRes_span_exact
#print axioms MetricChain.sumClass_span_upper
#print axioms MetricChain.sumClass_span_lower
#print axioms MetricChain.pairRes_span_upper_enclosure
#print axioms MetricChain.pairRes_sub_le
#print axioms MetricChain.pairRes_span_upper
#print axioms MetricChain.pairRes_sharp
#print axioms MetricChain.verifyL_sound
#print axioms MetricChain.verifyLTop_sound
#print axioms MetricChain.contactTriangle_verified
#print axioms MetricChain.contactTriangle_bound
#print axioms MetricChain.contactTriangle_class_nonempty
#print axioms MetricChain.HintRecursion.superSolution_le_hint
#print axioms MetricChain.HintRecursion.iterates_lt_hint_add
#print axioms MetricChain.HintRecursion.step_from_hint_le
#print axioms MetricChain.HintRecursion.klBin_shift
#print axioms MetricChain.HintRecursion.gaussPair
#print axioms MetricChain.HintRecursion.gauss_hint_superSolution
#print axioms MetricChain.LayerCake.level_mul_exceed_le_mean
#print axioms MetricChain.LayerCake.mean_le_layer_cake
#print axioms MetricChain.LayerCake.mean_le_upper
#print axioms MetricChain.LayerCake.upper_le_width
#print axioms MetricChain.LayerCake.fibre_sum_le
#print axioms MetricChain.LayerCake.close_points_bound
#print axioms MetricChain.LayerCake.negligibility_threshold_le
#print axioms MetricChain.HintRecursion.cubePair
#print axioms MetricChain.HintRecursion.cubeNa_isLeast_allRadii
#print axioms MetricChain.HintRecursion.cubeHint_lt_cubeNa
#print axioms MetricChain.HintRecursion.cube_superSolution_le_hint
#print axioms MetricChain.HintRecursion.cube_iterates_lt_hint_add
#print axioms MetricChain.HintRecursion.cube_step_from_hint_le
#print axioms MetricChain.HintRecursion.cube_hint_superSolution
#print axioms MetricChain.HintRecursion.cube_hintRecursion_witness

-- The exact level recursion and the passage to a bounded accuracy (theory report §11.19)
#print axioms MetricChain.BoundedAccuracy.stepLE_exact
#print axioms MetricChain.BoundedAccuracy.exactRec_props
#print axioms MetricChain.BoundedAccuracy.exactRec_reaches_hint
#print axioms MetricChain.BoundedAccuracy.exactRec_reaches_hint_of_pair
#print axioms MetricChain.BoundedAccuracy.exactRec_ge_hint
#print axioms MetricChain.BoundedAccuracy.exactRec_tendsto_hint
#print axioms MetricChain.BoundedAccuracy.bounded_iterates_lt
#print axioms MetricChain.BoundedAccuracy.two_rung_bound
#print axioms MetricChain.BoundedAccuracy.levels_reach_hint_at_zero
#print axioms MetricChain.BoundedAccuracy.cube_levels_reach_hint_at_zero
#print axioms MetricChain.BoundedAccuracy.cube_levels_reach_hint_at_zero_consistent
#print axioms MetricChain.BoundedAccuracy.certified_lower_sum_le_mean
#print axioms MetricChain.BoundedAccuracy.populated_part_le
#print axioms MetricChain.BoundedAccuracy.close_points_bound'
#print axioms MetricChain.BoundedAccuracy.width_le

-- The shift identity with a known field (theory report §11.20)
#print axioms MetricChain.FieldShift.klBin_tilt
#print axioms MetricChain.FieldShift.cone_rate_eq
#print axioms MetricChain.FieldShift.sphere_rate_eq
#print axioms MetricChain.FieldShift.shift_identity

-- Every game function yields a pair; the exact recursion converges (theory report §11.21)
#print axioms MetricChain.CoverStability.hasCover_of_close
#print axioms MetricChain.CoverStability.hasCover_sandwich
#print axioms MetricChain.CoverStability.hasCover_upper_iff
#print axioms MetricChain.CoverStability.hasCover_limit_point
#print axioms MetricChain.CoverStability.not_hasCover_shifted
#print axioms MetricChain.CoverStability.hasCover_shifted_of_close
#print axioms MetricChain.CoverStability.approx_multiple
#print axioms MetricChain.CoverStability.approx_nested
#print axioms MetricChain.CoverStability.approx_nested_example
#print axioms MetricChain.SetLimit.isClosed_lowerLimit
#print axioms MetricChain.SetLimit.mem_lowerLimit_of_tendsto
#print axioms MetricChain.SetLimit.hausdorff_limit
#print axioms MetricChain.SetLimit.SuperAdditive.approxNested
#print axioms MetricChain.SetLimit.SuperAdditive.combination
#print axioms MetricChain.SetLimit.SuperAdditive.hausdorff_limit
#print axioms MetricChain.SetLimit.SuperAdditive.dist_limit_le
#print axioms MetricChain.SetLimit.SuperAdditive.convex_limit
#print axioms MetricChain.SetLimit.SuperAdditive.cover_sandwich
#print axioms MetricChain.SetLimit.superAdditive_example
#print axioms MetricChain.SetLimit.one_mem_limit_example
#print axioms MetricChain.TypeQuantiles.upperDensity_succ_le
#print axioms MetricChain.TypeQuantiles.upperDensity_pred_le
#print axioms MetricChain.TypeQuantiles.admissible_succ
#print axioms MetricChain.TypeQuantiles.admissible_pred
#print axioms MetricChain.TypeQuantiles.truncate_lipschitz_insert
#print axioms MetricChain.TypeQuantiles.truncate_lipschitz_erase
#print axioms MetricChain.TypeQuantiles.truncate_ne_iff
#print axioms MetricChain.TypeQuantiles.witness_admissible
#print axioms MetricChain.SymmetricSampling.exists_perm_smul_eq
#print axioms MetricChain.SymmetricSampling.card_perm_smul_mem_mul
#print axioms MetricChain.SymmetricSampling.symmetric_nonadaptive_queries_ge
#print axioms MetricChain.SymmetricSampling.truncated_weight_queries_ge
#print axioms MetricChain.SymmetricSampling.symmetric_nonadaptive_witness
#print axioms MetricChain.SymmetricSampling.perm_fraction_le
#print axioms MetricChain.SymmetricSampling.symmetric_queries_ge
#print axioms MetricChain.SymmetricSampling.symmetric_queries_witness
#print axioms MetricChain.TwoRounds.TwoRound.output_eq_of_virtual
#print axioms MetricChain.TwoRounds.card_distinguished_le
#print axioms MetricChain.TwoRounds.prob_output_ne_ge
#print axioms MetricChain.TwoRounds.two_round_bound
#print axioms MetricChain.TwoRounds.two_round_witness
#print axioms MetricChain.GroupSampling.gdens_mono
#print axioms MetricChain.GroupSampling.gdens_smul
#print axioms MetricChain.GroupSampling.lowDens_shift
#print axioms MetricChain.GroupSampling.regLevel_admissible
#print axioms MetricChain.GroupSampling.regLevel_lowDens_le
#print axioms MetricChain.GroupSampling.regLevel_smul
#print axioms MetricChain.GroupSampling.truncate_admissible
#print axioms MetricChain.GroupSampling.truncate_gdens_le
#print axioms MetricChain.GroupSampling.group_nonadaptive_queries_ge
#print axioms MetricChain.GroupSampling.group_queries_ge
#print axioms MetricChain.GroupSampling.gdens_mul_card_orbit
#print axioms MetricChain.GroupSampling.group_witness
#print axioms MetricChain.SliceRefinement.sum_mem_bracket
#print axioms MetricChain.SliceRefinement.bracket_width
#print axioms MetricChain.SliceRefinement.argmax_deficit_le
#print axioms MetricChain.SliceRefinement.deficit_ge
#print axioms MetricChain.SliceRefinement.mean_le_of_biregular
#print axioms MetricChain.SliceRefinement.lower_end_any
#print axioms MetricChain.RenyiCentre.scale_le_inv_sum
#print axioms MetricChain.RenyiCentre.exists_ratio_le
#print axioms MetricChain.RenyiCentre.eq_of_forall_ratio_ge
#print axioms MetricChain.RenyiCentre.softmin_admissible
#print axioms MetricChain.MacroRatio.macro_le_of_plan
#print axioms MetricChain.MacroRatio.macro_single_le
#print axioms MetricChain.MacroRatio.macro_le_card_mul
#print axioms MetricChain.MacroRatio.cone_admissible
#print axioms MetricChain.MacroRatio.macro_cone_ge
#print axioms MetricChain.MacroRatio.closed_pair_within_A
#print axioms MetricChain.MacroRatio.closed_pair_within_B
#print axioms MetricChain.MacroRatio.closed_pair_cross
#print axioms MetricChain.MacroRatio.two_point_witness
#print axioms MetricChain.TwoRounds.R4.card_distinguished_le_sum
#print axioms MetricChain.TwoRounds.R4.two_round_expected_bound
#print axioms MetricChain.TwoRounds.R4.two_round_expected_cost
#print axioms MetricChain.TwoRounds.R4.two_round_bound_of_class
#print axioms MetricChain.Scattering.le_add_cube
#print axioms MetricChain.Scattering.sub_cube_le
#print axioms MetricChain.Scattering.abs_sinc_sub_le
#print axioms MetricChain.Scattering.sinc_sqrt_lipschitz
#print axioms MetricChain.Scattering.debye_sum_sub_le
#print axioms MetricChain.Scattering.debye_sub_le
#print axioms MetricChain.Scattering.debye_eq_of_matching
#print axioms MetricChain.Scattering.one_sub_sinc_le

-- Sup-norm (box) classes around a known function (theory report §11.30)
#print axioms MetricChain.BoxClass.Zw_sub_le_dip
#print axioms MetricChain.BoxClass.Zw_sub_le_bump
#print axioms MetricChain.BoxClass.detect_ge
#print axioms MetricChain.BoxClass.box_spotCheck_correct
#print axioms MetricChain.BoxClass.dipAlt_mem
#print axioms MetricChain.BoxClass.logZ_dipAlt_gt
#print axioms MetricChain.BoxClass.box_expected_queries_ge
#print axioms MetricChain.BoxClass.bumpAlt_mem
#print axioms MetricChain.BoxClass.logZ_bumpAlt_gt
#print axioms MetricChain.BoxClass.box_expected_queries_ge_mixed
#print axioms MetricChain.BoxClass.detect_ge_of_proportional
#print axioms MetricChain.BoxClass.box_spotCheck_correct_of_proportional
#print axioms MetricChain.BoxClass.jensen_bracket
#print axioms MetricChain.BoxClass.centre_weights

-- A ratio of two macrostate weights in a box class (theory report §11.30, Corollary 11.114)
#print axioms MetricChain.BoxClass.ratio_core
#print axioms MetricChain.BoxClass.ratio_detect_ge
#print axioms MetricChain.BoxClass.ratio_spotCheck_correct
#print axioms MetricChain.BoxClass.logRatio_dipAlt_gt
#print axioms MetricChain.BoxClass.logRatio_dipAlt_lt
#print axioms MetricChain.BoxClass.ratio_expected_queries_ge
#print axioms MetricChain.BoxClass.ratio_witness

-- The stochastic sandwich for monotone macrostates (theory report §11.28, Theorem 11.106a; the Scientific Discovery
-- Division's file, adopted)
#print axioms ScienceL2.holley_cross
#print axioms ScienceL2.sandwich_mean
#print axioms ScienceL2.macrostate_ratio
#print axioms ScienceL2.ratio_range_eq_Icc
#print axioms ScienceL2.cube_sandwich_mean
#print axioms ScienceL2.cube_macrostate_ratio_compl
#print axioms ScienceL2.cube_mean_isLeast
#print axioms ScienceL2.cube_mean_isGreatest
#print axioms ScienceL2.cube_ratio_range_eq_Icc
#print axioms ScienceL2.pairwise_submodular
#print axioms ScienceL2.stepField_sandwich_mean
#print axioms ScienceL2.cube_sandwich_strict_witness
#print axioms ScienceL2.cube_sandwich_fails_negative_beta

-- The compensation lemma and the lower bound for adaptive algorithms with an exact one-body oracle (theory report
-- §11.29, Theorem 11.109a (a)–(c); §11.20, Proposition 11.61a (i), (ii); the Scientific Discovery Division's files
-- of its message SCI-MSG-0019, adopted)
-- Theorem 11.109a (a), the compensation lemma; Proposition 11.109 (a), (b); Proposition 11.61a (i)
#print axioms ScienceL3.lemma3_i
#print axioms ScienceL3.lemma3_compensation
#print axioms ScienceL3.lemma3_compensation_bernoulli
#print axioms ScienceL3.oneW_compensated
#print axioms ScienceL3.lemma0_window_lipH
#print axioms ScienceL3.condMarg_mem_window_lipH
#print axioms ScienceL3.lemma0_additive_fill
#print axioms ScienceL3.lemma0_rigidity_lipH
-- Theorem 11.109a (b), the excess of a dip
#print axioms ScienceL3.lemma2_mass
#print axioms ScienceL3.lemma2_dens
#print axioms ScienceL3.densW_coneW
-- the packing bounds with an oracle; Theorem 11.109a (c)
#print axioms ScienceL3.lemma1a
#print axioms ScienceL3.lemma1b
#print axioms ScienceL3.theoremA_fin
#print axioms ScienceL3.theoremA_group
#print axioms ScienceL3.theoremA_group_sharp
#print axioms ScienceL3.theoremA_fin_chernoff
#print axioms ScienceL3.theoremA_fin_Cm
-- Proposition 11.61a (ii), the chain-rule bound
#print axioms ScienceL3.Chain.a1_item2_lip
#print axioms ScienceL3.Chain.a1_item2_isGreatest
-- non-vacuity of the correctness hypothesis; the two remarks on the ends of the window
#print axioms ScienceL3.exists_correct_oracle_algorithm
#print axioms ScienceL3.no_compensation_at_upper_end
#print axioms ScienceL3.window_of_equal_marginals

-- Third-order residual classes reduce to pairwise lower models (theory report Theorem 11.18a)
#print axioms MetricChain.anchoredInterp_three
#print axioms MetricChain.thirdOrderLowerModel_energy
#print axioms MetricChain.thirdOrder_pairwise_lower
#print axioms MetricChain.cover_of_site_shares
#print axioms MetricChain.thirdOrder_pairwise_lower_thirds
#print axioms MetricChain.cover_of_pair_thirds
#print axioms MetricChain.thirdOrder_pairwise_lower_pair_thirds
#print axioms MetricChain.verify_sound_thirdOrder
#print axioms MetricChain.thirdOrder_witness

-- Share certificates for the second-order sharp-minimum condition (theory report Proposition 11.18b)
#print axioms MetricChain.pairSum_le_of_shares
#print axioms MetricChain.secondOrder_certified_of_shares
#print axioms MetricChain.secondOrder_certified_of_rowSum
-- state-dependent shares for a pairwise known part (Proposition 11.18b (d), (e); proposed by the Scientific
-- Discovery Division, SCI-REV-0012)
#print axioms MetricChain.energy_sub_eq_excitations_add_secondDiff
#print axioms MetricChain.secondOrder_certified_of_state_shares
#print axioms MetricChain.secondOrder_certified_of_deficit_shares
#print axioms MetricChain.stateShare_witness

-- A lower bound for every algorithm from any law on labels, for any reference measure (theory report §11.32,
-- Theorem 11.116(c); workstream Y, Lemma A)
#print axioms MetricChain.softMinLabel_admissible
#print axioms MetricChain.exp_softMinLabel
#print axioms MetricChain.renyiG_eq
#print axioms MetricChain.softMin_expected_queries_ge
#print axioms MetricChain.renyiG_le_log_card

-- The two-point Bennett–Hoeffding bound and the floor-plus-variance bracket (theory report §11.30, Theorem
-- 11.110(f); the Scientific Discovery Division's file of its message SCI-MSG-0023, adopted), and the bracket in the
-- vocabulary of box classes
#print axioms ScienceL4.Bennett.key_exp_ineq
#print axioms ScienceL4.Bennett.exp_le_parabola
#print axioms ScienceL4.Bennett.parabola_le_exp
#print axioms ScienceL4.Bennett.mgf_le_one_add
#print axioms ScienceL4.Bennett.mgf_le_bennettB
#print axioms ScienceL4.Bennett.integral_exp_le_bennettB
#print axioms ScienceL4.Bennett.twoPoint_mean
#print axioms ScienceL4.Bennett.twoPoint_sq
#print axioms ScienceL4.Bennett.twoPoint_mgf
#print axioms ScienceL4.Bennett.bennettB_isGreatest
#print axioms ScienceL4.Bennett.bennettB_mono
#print axioms ScienceL4.Bennett.one_le_bennettB
#print axioms ScienceL4.Bennett.bennettB_le_one_add
#print axioms ScienceL4.Bennett.bennettB_le_exp_mul
#print axioms ScienceL4.Bennett.bennettW_nonneg
#print axioms ScienceL4.Bennett.bennettW_mono
#print axioms ScienceL4.Bennett.bennettW_le_log_one_add
#print axioms ScienceL4.Bennett.bennettW_le
#print axioms ScienceL4.Bennett.bennettW_sub_antitone
#print axioms ScienceL4.Bennett.remainder_bracket
#print axioms ScienceL4.Bennett.remainder_bracket_attained
#print axioms ScienceL4.Bennett.deterministic_bracket_of_lt
#print axioms ScienceL4.Bennett.log_mean_exp_neg_le
#print axioms ScienceL4.Bennett.bennettW_zero_left
#print axioms ScienceL4.Bennett.deterministic_bracket
#print axioms ScienceL4.Bennett.deterministic_bracket_sharp
#print axioms ScienceL4.Bennett.deterministic_bracket_sharp_le
#print axioms ScienceL4.Bennett.bracket_of_bounds
#print axioms ScienceL4.Bennett.bracket_of_pointwise_bounds
#print axioms ScienceL4.Bennett.bracket_of_midpoint
#print axioms ScienceL4.Bennett.ceiling_lower_bound
#print axioms ScienceL4.Bennett.bennett_bracket_weights
#print axioms ScienceL4.Bennett.chebyshev_sum
#print axioms ScienceL4.Bennett.certificate_of_mse
#print axioms ScienceL4.Bennett.iid_sample_mean_mse
#print axioms ScienceL4.Bennett.iid_certificate
#print axioms ScienceL4.Bennett.iid_certificate_delta
#print axioms MetricChain.BoxClass.bennett_bracket

-- Shares of the anchored constants at every level, windows, arbitrary allocations (theory report Theorem
-- 11.18d(c'); requested by the Scientific Discovery Division, SCI-MSG-0025, P6-T1)
#print axioms MetricChain.sum_levelShare_eq
#print axioms MetricChain.cover_of_level_shares
#print axioms MetricChain.choose_succ_mul_choose_le
#print axioms MetricChain.level_shares_antitone
#print axioms MetricChain.levelShare_one_eq_sitePenalty
#print axioms MetricChain.sum_levelShare_one
#print axioms MetricChain.levelShare_zero_empty
#print axioms MetricChain.levelShare_self
#print axioms MetricChain.sum_superset_levelShare_succ
#print axioms MetricChain.level_window_cover
#print axioms MetricChain.level_window_le
#print axioms MetricChain.cover_of_window_shares
#print axioms MetricChain.anchored_remainder_level_shares
#print axioms MetricChain.anchored_remainder_window_shares
#print axioms MetricChain.cover_of_subset_shares
#print axioms MetricChain.anchored_remainder_subset_shares
#print axioms MetricChain.level_shares_witness
#print axioms MetricChain.level_window_witness

-- The remainder identity for a down-closed family of evaluated subsets, and a mixed difference in an arbitrary
-- context (theory report Theorem 11.18d(a'), (b'); Propositions 10 and 11 of the Scientific Discovery Division's
-- workstream P5, SCI-MSG-0024, request P5-T2)
#print axioms MetricChain.downClosed_remainder_identity_mixConfig
#print axioms MetricChain.downClosed_remainder_identity
#print axioms MetricChain.downClosed_remainder_bound
#print axioms MetricChain.isThreshold_card_lt_iff
#print axioms MetricChain.downClosed_remainder_card_lt
#print axioms MetricChain.downClosed_remainder_witness
#print axioms MetricChain.downClosed_remainder_witness_family
#print axioms MetricChain.downClosed_remainder_witness_identity
#print axioms MetricChain.mixedDiff_context_identity
#print axioms MetricChain.mixedDiff_context_sub_bound
#print axioms MetricChain.mixedDiff_context_bound

-- Box classes: detection at the floor and the ceiling, the weighted sampler, bumps for ratios (the Scientific
-- Discovery Division's review SCI-REV-0013, adopted), and the lower bound for a ratio with dips and bumps (ours)
#print axioms MetricChain.BoxClass.detect_ge_at_floor
#print axioms MetricChain.BoxClass.detect_ge_at_ceiling
#print axioms MetricChain.BoxClass.detect_ge_weighted
#print axioms MetricChain.BoxClass.weighted_opt
#print axioms MetricChain.BoxClass.logRatio_bumpAlt_lt
#print axioms MetricChain.BoxClass.logRatio_bumpAlt_gt
#print axioms MetricChain.BoxClass.ratio_expected_queries_ge_mixed

-- An affine function on the cube is large on half of the points (the core of the Scientific Discovery Division's
-- counter-algorithm to the first version of Proposition 11.18e(b); SCI-REV-0013, adopted)
#print axioms ScienceR12.affine_half_large

-- Two blocks with a coupling: the reductions of Theorem 11.116(a), (b) in abstract form
#print axioms MetricChain.cut_coupling_admissible
#print axioms MetricChain.cut_coupling_partition
#print axioms MetricChain.cut_coupling_normalised
#print axioms MetricChain.gap_embedding_admissible
#print axioms MetricChain.gap_embedding_partition
#print axioms MetricChain.cut_coupling_witness

-- The rate of the level recursion (remark after Theorem 11.53), machine-checked by the Scientific Discovery Division
-- in its review SCI-REV-0014 on top of `StepLE.of_limit`, `StepLE.of_macro`, `StepLE.at_hint_fraction`; adopted
#print axioms ScienceR13.epoch_gain
#print axioms ScienceR13.closed_form
#print axioms ScienceR13.rate_of_epochs
#print axioms ScienceR13.lemma1
#print axioms ScienceR13.lemma2
#print axioms ScienceR13.epoch_of_stepLE
#print axioms ScienceR13.rate_top0
#print axioms ScienceR13.rate_all0
#print axioms ScienceR13.cube_exactRec_rate_top
#print axioms ScienceR13.cube_exactRec_rate_all
#print axioms ScienceR13.rate_zero

-- What a sandwich costs in terms of the true ensemble (the division's Lemma A17.16, SCI-MSG-0026; adopted; theory
-- report Proposition 11.113b(a))
#print axioms ScienceA17.floor_side
#print axioms ScienceA17.ceiling_side
#print axioms ScienceA17.Z_ratio
#print axioms ScienceA17.sandwich_cost

-- Kernel soundness for real models under the symmetrised pair hypothesis (an instance may store each pair table
-- once; requested by the Scientific Discovery Division, SCI-RES-0014, P7-T3, its Lemma P7.7)
#print axioms MetricChain.PairInstance.cast_energy_le_symm
#print axioms MetricChain.verify_sound_real_symm
#print axioms MetricChain.verify_sound_secondOrder_symm
#print axioms MetricChain.symm_of_termwise
#print axioms MetricChain.symm_hypothesis_witness

-- A domain-split rule as a layer over the kernel (one child for the states of a site in a list, one for the others;
-- requested by the Scientific Discovery Division, SCI-RES-0014, P7-T2), with a witness on which no single leaf
-- certifies and the split of two leaves does
#print axioms MetricChain.verifyS_sound
#print axioms MetricChain.verifyS_sound_real
#print axioms MetricChain.leafOK_mono
#print axioms MetricChain.split_leaves_imp_branch
#print axioms MetricChain.split_leaves_iff_branch
#print axioms MetricChain.splitTriangle_verified
#print axioms MetricChain.splitTriangle_lower_bound
#print axioms MetricChain.splitTriangle_optimum
#print axioms MetricChain.splitTriangle_no_leaf

-- Residuals in a Hilbert ball: the hypercircle band as a certificate (theory report Proposition 11.50a)
#print axioms MetricChain.Hypercircle.cauchy_schwarz
#print axioms MetricChain.Hypercircle.hypercircle_band
#print axioms MetricChain.Hypercircle.ball_certificate_sound
#print axioms MetricChain.Hypercircle.verify_sound_ball
#print axioms MetricChain.Hypercircle.isKernel_of_features
#print axioms MetricChain.Hypercircle.band_witness
#print axioms MetricChain.GamePair.exactRec_congr
#print axioms MetricChain.GamePair.HintShape.pair
#print axioms MetricChain.GamePair.HintShape.exists_pair
#print axioms MetricChain.GamePair.HintShape.exactRec_reaches
#print axioms MetricChain.GamePair.HintShape.superSolution
#print axioms MetricChain.GamePair.HintShape.Rstep_hint
#print axioms MetricChain.GamePair.HintShape.exactRec_tendsto
#print axioms MetricChain.GamePair.GameFunction.hintShape_critical
#print axioms MetricChain.GamePair.GameFunction.pair
#print axioms MetricChain.GamePair.GameFunction.exactRec_reaches
#print axioms MetricChain.GamePair.GameFunction.exactRec_tendsto
#print axioms MetricChain.GamePair.GameFunction.not_forall_shift_eq
#print axioms MetricChain.GamePair.GameFunction.critical_eq_neg_L
#print axioms MetricChain.GamePair.toyGame_gameFunction
#print axioms MetricChain.GamePair.hinted_toyGame
#print axioms MetricChain.GamePair.partner_toyGame
#print axioms MetricChain.GamePair.gauss_exactRec_tendsto
#print axioms MetricChain.product_rate_bound
#print axioms MetricChain.product_entropy_bound
#print axioms MetricChain.thermal_binary_sharp
#print axioms MetricChain.thermal_binary_single_tight

/-! ### Non-vacuity witnesses -/

namespace MetricChain.NonVacuity

open Finset

/-- The discrete envelope on `Bool` with oscillation `1` is an envelope, and the zero residual is
admissible for it: the hypotheses of the envelope-duality theorems are satisfiable. -/
theorem envelope_satisfiable : IsEnvelope (discreteEnvelope (X := Bool) 1) ∧ Admissible (discreteEnvelope (X := Bool) 1) fun _ => 0 :=
  ⟨discreteEnvelope_isEnvelope (by norm_num), fun x y => by unfold discreteEnvelope; split_ifs <;> norm_num⟩

/-- `robust_minimizer_iff` is not vacuous in either direction: with `f true = 0`, `f false = 2`
and oscillation `1`, `true` is robustly optimal-for-some-residual and `false` is not. -/
theorem robust_minimizer_discriminates :
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
theorem exact_certificate_contains_all (A : Finset Bool) (hA : A.Nonempty)
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
theorem exact_certificate_exists : ∀ y, (Finset.univ : Finset Bool).inf' ⟨true, Finset.mem_univ _⟩ (fun _ => (0 : ℝ) + 0) - 0 ≤
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
theorem transport_two_state : partitionFn 1 (fun b : Bool => if b then (1 : ℝ) else 3) {false} ≤
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
theorem triangle_tight : (∀ x : Config 3 2, 1 ≤ triangle.energy x) ∧ triangle.energy ![0, 1, 0] = 1 :=
  ⟨triangle_lower_bound, triangle_optimum⟩

/-- `robust_minimizer_with_anchors_iff` discriminates: with one anchor (`true`, value `0`),
oscillation `1`, and white-box energies `f true = 0`, `f false = 3`, the state `false` cannot be
optimal for any admissible residual matching the anchor, whereas `true` can. -/
theorem query_model_discriminates :
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
theorem real_model_bound (M : PairModel ℝ (Fin 3) (fun _ => Fin 2))
    (hh : ∀ i a, ((triangle.h i a : ℚ) : ℝ) ≤ M.h i a)
    (hJ : ∀ i j a b, ((triangle.J i j a b : ℚ) : ℝ) ≤ M.J i j a b) (x : Config 3 2) :
    ((1 : ℚ) : ℝ) ≤ M.energy x :=
  verify_sound_real triangleCert triangle (fullDom 3 2) 1 triangle_verified M hh hJ x
    (inBox_fullDom x)

/-- `boltzmannAvg_dominance_error` on a two-state system (margin `2`): discarding the dominated
state changes the average of any observable bounded by `1` by at most `2 e^{-2}`. -/
theorem observable_error_two_state (f : Bool → ℝ) (hf : ∀ b, |f b| ≤ 1) :
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
theorem kl_identity_two_state (Δ : Bool → ℝ) (β : ℝ) :
    klFin (fun _ : Bool => (1 / 2 : ℝ)) (tilt (fun _ => 1 / 2) Δ β) =
      β * ∑ x : Bool, (1 / 2 : ℝ) * Δ x + Real.log (∑ x : Bool, (1 / 2 : ℝ) * Real.exp (-β * Δ x)) :=
  kl_reference_target_eq_gap (fun _ => 1 / 2) Δ (fun _ => by norm_num)
    (by rw [Fintype.sum_bool]; norm_num) β

/-- `robust_min_interval_exact` on two states with one anchor (`true`, value `0`) and oscillation
`1`: the envelope optima are `-1` and `0`, and *every* value in between is the optimal value of
`f + g` for an admissible residual matching the anchor. -/
theorem robust_interval_exact_two_state (τ : ℝ) (h1 : -1 ≤ τ) (h0 : τ ≤ 0) :
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
theorem residual_top_nonvacuous : (∃ g : Config 3 2 → ℝ, ResidualClass triangleResidual g) ∧
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
theorem invariant_pipeline_instance (x : Config 1 2) : ((-4 : ℚ) : ℝ) ≤ (wProblem.base.energy x : ℝ) + wΔ (wEmb x) := by
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

/-- Interval version of the one-torsion instance: anchor state `0` with the interval evaluation
`[0, 0]`, envelope constant `4 = Λ · ρ` with `Λ = 2`, `ρ = 2`. -/
def wIProblem : IProblem 1 2 where
  base := { h := fun _ _ => 0, J := fun _ _ _ _ => 0 }
  c := fun _ => 4
  anchors := [⟨![0], 0, some 0⟩]

theorem wIProblem_verified :
    verifyITop (.anchor 0 (.leaf (fun _ => -4) (fun _ _ => 0) (fun _ _ _ => 0))) wIProblem
      (fullDom 1 2) (-4) = true := by decide +kernel

theorem wMoveIn (x : Config 1 2) (i : Fin 1) (s : Fin 2) :
    RigidWithinIn (⊤ : Submonoid (AxisSpace ≃ᵢ AxisSpace)) (wEmb x)
      (wEmb (Function.update x i s)) 2 := by
  obtain ⟨u, B, δ, hG, hmv, hI⟩ := wMove x i s
  refine (hmv.rigidWithinIn ⊤ hG).mono ?_
  have h1 : Real.sqrt (2 * reducedInertia u B (wEmb x)) ≤ 1 := by
    calc Real.sqrt (2 * reducedInertia u B (wEmb x)) ≤ Real.sqrt 1 :=
          Real.sqrt_le_sqrt (by linarith)
      _ = 1 := Real.sqrt_one
  have h2 : |Real.sin (δ / 2)| ≤ 1 := Real.abs_sin_le_one _
  have h3 := Real.sqrt_nonneg (2 * reducedInertia u B (wEmb x))
  have h4 := abs_nonneg (Real.sin (δ / 2))
  rw [abs_of_nonneg (by positivity), abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 2)]
  nlinarith

theorem wΔ_anchor : wΔ (wEmb ![0]) = 0 := by
  have h : wEmb ![0] 1 = wEmb ![0] 0 := by
    simp [wEmb, wθ, axisRot_apply]
    rfl
  unfold wΔ
  rw [h, dist_self]

/-- `verifyITop_sound_invariant` instantiated: all hypotheses are jointly satisfiable and both
conclusions (lower bound on the box, certified incumbent at the anchor) are obtained. -/
theorem interval_invariant_instance :
    (∀ x : Config 1 2, ((-4 : ℚ) : ℝ) ≤ (wIProblem.base.energy x : ℝ) + wΔ (wEmb x)) ∧
      (wIProblem.base.energy ![0] : ℝ) + wΔ (wEmb ![0]) ≤
        ((wIProblem.base.energy ![0] + 0 : ℚ) : ℝ) := by
  have key := verifyITop_sound_invariant (Λ := 2) (by norm_num) wΔ_invariant wΔ_lipschitz wEmb
    (fun _ => 2) (fun _ => by norm_num) wMoveIn wIProblem
    (fun i => by show (2 : ℝ) * 2 ≤ ((4 : ℚ) : ℝ); norm_num)
    (by
      intro p hp
      have hp' : p = ⟨![0], 0, some 0⟩ := by simpa [wIProblem] using hp
      subst hp'
      refine ⟨by simp [wΔ_anchor], fun h hh => ?_⟩
      have hh' : h = 0 := by simpa using hh.symm
      subst hh'
      simp [wΔ_anchor])
    (.anchor 0 (.leaf (fun _ => -4) (fun _ _ => 0) (fun _ _ _ => 0))) (fullDom 1 2) (-4)
    wIProblem_verified
  exact ⟨fun x => key.1 x (inBox_fullDom x),
    key.2 ⟨![0], 0, some 0⟩ (by simp [wIProblem]) 0 rfl⟩

/-! #### An invariance group smaller than the full isometry group

`Gz` is the group generated by the rotations about the torsion axis (proper motions), and
`Δz X = z(X 1) - z(X 0)` is the signed height difference along the axis: invariant under `Gz`,
`2`-Lipschitz, but *not* invariant under the mirror reflection `z ↦ -z`.  So the `G`-parametrised
torsion bound applies to an orientation-sensitive residual to which the `E(3)` statements
(`RigidInvariant`) do not apply. -/

/-- submonoid generated by the rotations about the `z`-axis -/
noncomputable def Gz : Submonoid (AxisSpace ≃ᵢ AxisSpace) :=
  Submonoid.closure (Set.range fun ψ : ℝ =>
    (IsometryEquiv.refl AxisSpace).trans ((axisRot ψ).trans (IsometryEquiv.refl AxisSpace).symm))

theorem Gz_axisRot_mem : ∀ ψ : ℝ,
    (IsometryEquiv.refl AxisSpace).trans ((axisRot ψ).trans (IsometryEquiv.refl AxisSpace).symm) ∈
      Gz :=
  fun ψ => Submonoid.subset_closure ⟨ψ, rfl⟩

/-- an orientation-sensitive residual: signed height difference along the axis -/
noncomputable def Δz (X : Fin 2 → AxisSpace) : ℝ := (X 1).snd - (X 0).snd

theorem Δz_invariantIn : RigidInvariantIn Gz Δz := by
  intro g hg
  induction hg using Submonoid.closure_induction with
  | mem g hg =>
    obtain ⟨ψ, rfl⟩ := hg
    intro y
    show ((axisRot ψ (y 1)).snd - (axisRot ψ (y 0)).snd) = (y 1).snd - (y 0).snd
    simp
  | one => intro y; rfl
  | mul g h _ _ ihg ihh =>
    intro y
    have := ihg (fun i => h (y i))
    rw [ihh y] at this
    exact this

/-- mirror reflection `(w, z) ↦ (w, -z)` -/
noncomputable def reflZ : AxisSpace ≃ᵢ AxisSpace where
  toFun p := WithLp.toLp 2 (p.fst, -p.snd)
  invFun p := WithLp.toLp 2 (p.fst, -p.snd)
  left_inv p := by
    show WithLp.toLp 2 (p.fst, - -p.snd) = p
    rw [neg_neg]; rfl
  right_inv p := by
    show WithLp.toLp 2 (p.fst, - -p.snd) = p
    rw [neg_neg]; rfl
  isometry_toFun := by
    refine Isometry.of_dist_eq fun p q => ?_
    rw [WithLp.prod_dist_eq_of_L2, WithLp.prod_dist_eq_of_L2]
    simp only [WithLp.toLp_fst, WithLp.toLp_snd]
    rw [dist_neg_neg]

/-- `Δz` is not invariant under all isometries: the `E(3)` theorems do not apply to it. -/
theorem Δz_not_rigidInvariant : ¬ RigidInvariant Δz := by
  intro h
  have h1 := h reflZ ![WithLp.toLp 2 ((0 : ℂ), (0 : ℝ)), WithLp.toLp 2 ((0 : ℂ), (1 : ℝ))]
  simp [Δz, reflZ] at h1
  norm_num at h1

theorem snd_sub_le_dist (p q : AxisSpace) : |p.snd - q.snd| ≤ dist p q := by
  rw [WithLp.prod_dist_eq_of_L2]
  have h : dist p.snd q.snd ^ 2 ≤ dist p.fst q.fst ^ 2 + dist p.snd q.snd ^ 2 := by
    nlinarith [sq_nonneg (dist p.fst q.fst)]
  calc |p.snd - q.snd| = dist p.snd q.snd := (Real.dist_eq _ _).symm
    _ = Real.sqrt (dist p.snd q.snd ^ 2) := (Real.sqrt_sq dist_nonneg).symm
    _ ≤ Real.sqrt (dist p.fst q.fst ^ 2 + dist p.snd q.snd ^ 2) := Real.sqrt_le_sqrt h

theorem Δz_lipschitz : ConfigLipschitz 2 Δz := by
  intro x y
  rw [Fin.sum_univ_two]
  have h0 := snd_sub_le_dist (x 0) (y 0)
  have h1 := snd_sub_le_dist (x 1) (y 1)
  have s0 : dist (x 0) (y 0) ≤ Real.sqrt (dist (x 0) (y 0) ^ 2 + dist (x 1) (y 1) ^ 2) :=
    Real.le_sqrt_of_sq_le (by nlinarith [sq_nonneg (dist (x 1) (y 1))])
  have s1 : dist (x 1) (y 1) ≤ Real.sqrt (dist (x 0) (y 0) ^ 2 + dist (x 1) (y 1) ^ 2) :=
    Real.le_sqrt_of_sq_le (by nlinarith [sq_nonneg (dist (x 0) (y 0))])
  have e : Δz x - Δz y = ((x 1).snd - (y 1).snd) - ((x 0).snd - (y 0).snd) := by
    unfold Δz; ring
  rw [e]
  have := abs_sub ((x 1).snd - (y 1).snd) ((x 0).snd - (y 0).snd)
  linarith

/-- The `G`-parametrised torsion bound instantiated at the proper subgroup `Gz ≠ ⊤` and a residual
that is not `E(3)`-invariant: the generalisation from all isometries to a group of motions
containing the axis rotations has content. -/
theorem signed_offset_residual_torsion_bound (p0 p1 : AxisSpace) (δ : ℝ) :
    |Δz ![p0, p1] - Δz ![p0, axisRot δ p1]| ≤
      2 * (2 * Real.sqrt (2 * reducedInertia (IsometryEquiv.refl AxisSpace)
        ({1} : Finset (Fin 2)) ![p0, p1]) * |Real.sin (δ / 2)|) := by
  refine residual_torsion_move_in (by norm_num) Δz_invariantIn Δz_lipschitz Gz_axisRot_mem ?_
  refine ⟨fun i hi => ?_, fun i hi => ?_⟩
  · have : i = 0 := by
      fin_cases i
      · rfl
      · exact absurd (Finset.mem_singleton.mpr rfl) hi
    subst this; rfl
  · have : i = 1 := Finset.mem_singleton.mp hi
    subst this; rfl

/-! #### Certification geometry (second phase) -/

/-- Slack partition sum of the two-point discrete envelope at `t = log 3`: `1 + 1/3`. -/
theorem bool_slack_sum (a : Bool) :
    ∑ y : Bool, Real.exp (-Real.log 3 * slack (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) a y)
      = 4 / 3 := by
  have h3 : Real.exp (-Real.log 3) = 1 / 3 := by
    rw [Real.exp_neg, Real.exp_log (by norm_num : (0 : ℝ) < 3)]
    norm_num
  rw [Fintype.sum_bool]
  cases a <;> simp [slack, discreteEnvelope, h3] <;> norm_num

/-- **Witness for `card_ge_exp_weights`.**  On two states with the discrete envelope of
oscillation `1` and `f = g = 0`, both states together are an exact certificate, and the
exponential-weights converse (uniform weights, `t = log 3`) shows that every exact certificate
evaluates both: the hypotheses of the theorem are satisfiable and its conclusion is sharp. -/
theorem exp_weights_two_state :
    IsCertificate (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) (fun _ => 0) univ
        univ_nonempty 0 ∧
      ∀ (A : Finset Bool) (hA : A.Nonempty),
        IsCertificate (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) (fun _ => 0) A hA 0 →
          2 ≤ A.card := by
  refine ⟨full_evaluation_certificate (fun x => by simp [discreteEnvelope]) _ _, ?_⟩
  intro A hA h
  have key := card_ge_exp_weights_certificate (t := Real.log 3) (Estar := 0) (B := 4 / 3)
    (Real.log_nonneg (by norm_num)) (fun _ : Bool => (1 : ℝ)) (fun _ => zero_le_one)
    (fun _ => by norm_num) h (by
      intro a _
      have := bool_slack_sum a
      simp only [one_mul, add_zero, sub_zero] at this ⊢
      exact this.le)
  simp only [mul_zero, Real.exp_zero, one_mul, Fintype.sum_bool] at key
  by_contra hlt
  have hc : A.card ≤ 1 := by omega
  have hc' : (A.card : ℝ) ≤ 1 := by exact_mod_cast hc
  nlinarith

/-- **Witness for `card_ge_entropy`.**  Two states, discrete envelope of oscillation `1`,
`f = g = 0`, `β = 1`: the full evaluated set reproduces the partition function exactly, and the
entropy bound at `t = log 3` shows that every evaluated set whose optimistic partition function
is exact contains both states (`log 2 ≤ log (|A| · 4/3)`). -/
theorem entropy_bound_two_state :
    (∑ y : Bool, Real.exp (-1 * ((0 : ℝ) + lowerEnv (discreteEnvelope 1) univ univ_nonempty
        (fun _ => 0) y)) ≤ Real.exp 0 * ∑ _y : Bool, Real.exp (-1 * ((0 : ℝ) + 0))) ∧
      ∀ (A : Finset Bool) (hA : A.Nonempty),
        (∑ y : Bool, Real.exp (-1 * ((0 : ℝ) + lowerEnv (discreteEnvelope 1) A hA
          (fun _ => 0) y)) ≤ Real.exp 0 * ∑ _y : Bool, Real.exp (-1 * ((0 : ℝ) + 0))) →
          2 ≤ A.card := by
  have hd : IsEnvelope (discreteEnvelope (X := Bool) 1) := discreteEnvelope_isEnvelope zero_le_one
  constructor
  · have hL : ∀ y : Bool, lowerEnv (discreteEnvelope 1) univ univ_nonempty
        (fun _ : Bool => (0 : ℝ)) y = 0 := fun y =>
      lowerEnv_eq_of_mem hd univ univ_nonempty _
        (fun a _ b _ => by
          simp only [sub_self]
          unfold discreteEnvelope
          split_ifs <;> norm_num)
        (mem_univ y)
    simp only [hL]
    rw [Real.exp_zero, one_mul]
  · intro A hA h
    have key := card_ge_entropy (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) (fun _ => 0) A hA
      (β := 1) (ε := 0) (t := Real.log 3) (B := 4 / 3) one_pos (Real.log_nonneg (by norm_num)) h
      (fun a _ => (bool_slack_sum a).le)
    have hπ : ∀ y : Bool, gibbsProb 1 (fun _ : Bool => (0 : ℝ)) y = 1 / 2 := by
      intro y
      simp [gibbsProb]
    simp only [add_zero, hπ, Fintype.sum_bool, mul_zero, zero_div] at key
    have hlog : Real.log 2 ≤ Real.log (A.card * (4 / 3)) := by
      have h2 : Real.log (1 / 2) = -Real.log 2 := by
        rw [one_div, Real.log_inv]
      rw [h2] at key
      linarith
    have hpos : (0 : ℝ) < A.card * (4 / 3) := by
      have : 0 < A.card := Finset.card_pos.mpr hA
      positivity
    have h2le : (2 : ℝ) ≤ A.card * (4 / 3) := by
      by_contra hlt
      have := Real.log_lt_log hpos (not_le.mp hlt)
      linarith
    by_contra hlt
    have hc : A.card ≤ 1 := by omega
    have hc' : (A.card : ℝ) ≤ 1 := by exact_mod_cast hc
    nlinarith

/-- **Witness for `CertificateNotions` (the referee's counterexample to the "any certificate"
gloss).**  Two states, discrete envelope of oscillation `1`, known part `0` at `true` and `5` at
`false`, zero residual.  The single evaluation at `false` certifies the configuration `true` as
an exact minimiser for every admissible residual consistent with it, although
(i) `{false}` is not a point certificate, and (ii) `true` is covered by no other point at the
level of the minimum, so every point certificate must evaluate it.  Evaluating the candidate
turns the configuration certificate into a point certificate. -/
theorem config_certificate_skips_forced_point :
    IsConfigCertificate (discreteEnvelope 1) (fun b : Bool => if b then (0 : ℝ) else 5)
        (fun _ => 0) {false} (singleton_nonempty false) true 0 ∧
      ¬ IsCertificate (discreteEnvelope 1) (fun b : Bool => if b then (0 : ℝ) else 5)
        (fun _ => 0) {false} (singleton_nonempty false) 0 ∧
      (∀ a : Bool, a ≠ true →
        ¬ Covers (discreteEnvelope 1) (fun b : Bool => if b then (0 : ℝ) else 5) (fun _ => 0)
          0 0 a true) ∧
      IsCertificate (discreteEnvelope 1) (fun b : Bool => if b then (0 : ℝ) else 5)
        (fun _ => 0) (insert true {false}) (insert_nonempty true {false}) 0 := by
  have hadm : Admissible (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) :=
    admissible_of_bounds (lo := 0) _ fun _ => by norm_num
  have hconf : IsConfigCertificate (discreteEnvelope 1) (fun b : Bool => if b then (0 : ℝ) else 5)
      (fun _ => 0) {false} (singleton_nonempty false) true 0 := by
    intro y
    have h := condEnv_le (discreteEnvelope 1) {false} (singleton_nonempty false)
      (fun _ : Bool => (0 : ℝ)) true y
    cases y <;> simp [discreteEnvelope] at h ⊢ <;> linarith
  refine ⟨hconf, ?_, ?_, isCertificate_insert_of_isConfigCertificate hadm _ hconf⟩
  · rw [single_evaluation_certificate_iff]
    intro h
    have := h true
    simp [discreteEnvelope] at this
    linarith
  · intro a ha
    cases a
    · simp [Covers, slack, discreteEnvelope]
    · exact absurd rfl ha

/-- **Witness for `exact_free_energy_certificate_eq_univ`.**  Two states, discrete envelope of
oscillation `1`, zero known part and zero residual, `β = 1`.  The slack is positive off the
diagonal and the full evaluation satisfies the hypothesis (both envelopes coincide with the
residual), so the hypotheses are jointly satisfiable; the theorem says that no smaller evaluated
set satisfies it. -/
theorem exact_free_energy_certificate_witness :
    (∀ a y : Bool, a ≠ y → 0 < slack (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) a y) ∧
      (∑ y : Bool, Real.exp (-1 * ((0 : ℝ) +
          lowerEnv (discreteEnvelope 1) univ univ_nonempty (fun _ => 0) y)) ≤
        ∑ y : Bool, Real.exp (-1 * ((0 : ℝ) +
          upperEnv (discreteEnvelope 1) univ univ_nonempty (fun _ => 0) y))) ∧
      ∀ (A : Finset Bool) (hA : A.Nonempty),
        (∑ y, Real.exp (-1 * ((0 : ℝ) + lowerEnv (discreteEnvelope 1) A hA (fun _ => 0) y)) ≤
          ∑ y, Real.exp (-1 * ((0 : ℝ) + upperEnv (discreteEnvelope 1) A hA (fun _ => 0) y))) →
        A = univ := by
  have hd : IsEnvelope (discreteEnvelope (X := Bool) 1) := discreteEnvelope_isEnvelope zero_le_one
  have hadm : Admissible (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) :=
    admissible_of_bounds (lo := 0) _ fun _ => by norm_num
  have hpos : ∀ a y : Bool, a ≠ y →
      0 < slack (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) a y := by
    intro a y hne
    simp [slack, discreteEnvelope, hne]
  refine ⟨hpos, ?_, fun A hA h => ?_⟩
  · refine Finset.sum_le_sum fun y _ => ?_
    rw [lowerEnv_eq_of_mem hd univ univ_nonempty _ (fun a _ b _ => hadm a b) (mem_univ y),
      upperEnv_eq_of_mem hd univ univ_nonempty _ (fun a _ b _ => hadm a b) (mem_univ y)]
  · exact exact_free_energy_certificate_eq_univ hadm (fun _ => 0) A hA one_pos hpos h

/-- **Witness for the deterministic query bounds (`queries_strict_cover`,
`instance_query_complexity`).**  Two states, discrete envelope of oscillation `1`, zero known
part.  (i) The algorithm that evaluates everything is exactly correct (`ε = 0`), so the
hypothesis is satisfiable.  (ii) Every exactly correct algorithm evaluates both states of the
zero residual: each state is within slack `1/2` of a queried point, and distinct states have
slack `1`. -/
theorem query_lower_bound_two_state :
    (∀ g : Bool → ℝ, Admissible (discreteEnvelope 1) g →
      |(fullQueryAlgorithm fun g : Bool → ℝ => univ.inf' univ_nonempty fun x => (0 : ℝ) + g x).output g -
        univ.inf' univ_nonempty fun x => (0 : ℝ) + g x| ≤ 0 / 2) ∧
      ∀ alg : QueryAlgorithm Bool,
        (∀ g : Bool → ℝ, Admissible (discreteEnvelope 1) g →
          |alg.output g - univ.inf' univ_nonempty fun x => (0 : ℝ) + g x| ≤ 0 / 2) →
        alg.queries (fun _ => 0) = univ := by
  have hd : IsEnvelope (discreteEnvelope (X := Bool) 1) := discreteEnvelope_isEnvelope zero_le_one
  have hadm : Admissible (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) :=
    admissible_of_bounds (lo := 0) _ fun _ => by norm_num
  refine ⟨fun g _ => by simp [fullQueryAlgorithm], fun alg hcorr => ?_⟩
  rw [Finset.eq_univ_iff_forall]
  intro y
  obtain ⟨a, ha, hlt⟩ := queries_strict_cover hd (fun _ : Bool => (0 : ℝ)) alg hcorr hadm
    (ε' := 1 / 2) (by norm_num) y
  have hinf : (univ.inf' univ_nonempty fun _ : Bool => (0 : ℝ) + 0) = 0 := by simp
  rw [hinf] at hlt
  by_cases hay : a = y
  · rw [← hay]
    exact ha
  · exfalso
    simp [slack, discreteEnvelope, hay] at hlt
    linarith

/-- **Witness for `binary_randomized_exponential`.**  For every `n` the hypotheses are
satisfiable with error probability `δ = 0` and accuracy `ε = 0`: the one-point probability space
carrying the algorithm that evaluates everything. -/
theorem binary_randomized_witness (n : ℕ) :
    ∀ g, Admissible (hamEnv fun _ : Fin n => (2 : ℝ)) g →
      1 - (0 : ℝ) ≤ ∑ _ω ∈ (univ : Finset Unit).filter (fun _ => |(fullQueryAlgorithm
          fun g : (Fin n → Bool) → ℝ =>
            univ.inf' univ_nonempty fun x => (∑ i, if x i then (1 : ℝ) else 0) + g x).output g -
        univ.inf' univ_nonempty fun x => (∑ i, if x i then (1 : ℝ) else 0) + g x| ≤ 0 / 2),
        (1 : ℝ) := by
  intro g _
  simp [fullQueryAlgorithm]

/-- **Witness for `cube_thermal_randomized_exponential`** at `m = 1`: the accuracy condition
holds for `ε = 0` (indeed `4 log (32/17) < log 16`), and the algorithm that evaluates everything
satisfies the correctness hypothesis with `δ = 0`. -/
theorem cube_thermal_randomized_witness :
    (0 : ℝ) + 4 * (1 : ℕ) * Real.log (32 / 17) < (1 : ℕ) * Real.log 16 ∧
      ∀ g, Admissible (hamEnv fun _ : Fin (4 * 1) => (1 : ℝ)) g →
        1 - (0 : ℝ) ≤ ∑ _ω ∈ (univ : Finset Unit).filter (fun _ => |(fullQueryAlgorithm
            fun g : (Fin (4 * 1) → Bool) → ℝ =>
              Real.log (∑ x, Real.exp (-Real.log 16 * ((0 : ℝ) + g x)))).output g -
          Real.log (∑ x, Real.exp (-Real.log 16 * ((0 : ℝ) + g x)))| ≤ 0 / 2), (1 : ℝ) := by
  constructor
  · have h : Real.log ((32 / 17 : ℝ) ^ 4) < Real.log 16 :=
      Real.log_lt_log (by positivity) (by norm_num)
    rw [Real.log_pow] at h
    push_cast at h ⊢
    linarith
  · intro g _
    simp [fullQueryAlgorithm]

/-- **Witness for `spotCheck_correct`.**  Two states, discrete envelope of oscillation `1`, the
minimum functional, hint `0`, the uniform sampling distribution, accuracy `ε / 2 = 1`.  Every
admissible residual whose minimum differs from `0` by more than `1` differs from the hint at
both states, so the hypotheses hold with `p = 1`, `N = 1`, `δ = 0`: one random evaluation
decides the minimum to within `1` with certainty. -/
theorem spotCheck_witness (g : Bool → ℝ) (hg : Admissible (discreteEnvelope 1) g) :
    1 - (0 : ℝ) ≤ ∑ _a ∈ univ.filter (fun a : Fin 1 → Bool =>
      |(spotCheck (fun g : Bool → ℝ => univ.inf' univ_nonempty fun x => g x) (fun _ => 0)
          a).output g - univ.inf' univ_nonempty fun x => g x| ≤ 2 / 2), ∏ _k : Fin 1, (1 / 2 : ℝ) := by
  refine spotCheck_correct (G := Admissible (discreteEnvelope 1))
    (Φ := fun g : Bool → ℝ => univ.inf' univ_nonempty fun x => g x) (fun _ => 0) 1
    (fun _ => 1 / 2) (fun _ => by norm_num) (by simp) (by norm_num) (le_refl 1)
    (fun g hg hfar => ?_) (by norm_num) g hg
  have hinf : (univ.inf' univ_nonempty fun _ : Bool => (0 : ℝ)) = 0 := by simp
  rw [hinf, sub_zero] at hfar
  obtain ⟨x₀, _, hx₀⟩ := Finset.exists_mem_eq_inf' univ_nonempty (fun x : Bool => g x)
  have hne : ∀ x : Bool, g x ≠ 0 := by
    intro x hx
    have hmx : (univ.inf' univ_nonempty fun x => g x) ≤ g x :=
      Finset.inf'_le (fun x => g x) (mem_univ x)
    have hd1 : discreteEnvelope (1 : ℝ) x x₀ ≤ 1 := by
      unfold discreteEnvelope
      split_ifs <;> norm_num
    have hadm := hg x x₀
    rcases lt_abs.mp hfar with hpos | hneg
    · linarith
    · linarith
  rw [Finset.filter_true_of_mem fun x _ => hne x]
  simp

/-- **Witness for `detection_weight_ge`.**  Two states, discrete envelope of oscillation `1`,
zero known part, `β = 1`, instance `g = 0` and alternative `g' = -1` (a constant shift, hence
admissible): `Z(g') = e · Z(g)`, so the hypothesis holds with `η = e - 1 > 0`. -/
theorem detection_weight_witness :
    Admissible (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) ∧
      Admissible (discreteEnvelope 1) (fun _ : Bool => (-1 : ℝ)) ∧ 0 ≤ Real.exp 1 - 1 ∧
      (1 + (Real.exp 1 - 1)) * ∑ _x : Bool, Real.exp (-1 * ((0 : ℝ) + 0)) ≤
        ∑ _x : Bool, Real.exp (-1 * ((0 : ℝ) + -1)) := by
  refine ⟨admissible_of_bounds (lo := 0) _ fun _ => by norm_num,
    admissible_of_bounds (lo := -1) _ fun _ => by norm_num, ?_, ?_⟩
  · have := Real.add_one_le_exp (1 : ℝ)
    linarith
  · simp
    linarith

/-- **Witness for `cube_deterministic_lower_bound`.**  For every `n`, `β` and `c` the algorithm
that evaluates everything is exactly correct (`ε = 0`), so the hypothesis is satisfiable. -/
theorem cube_deterministic_witness (n : ℕ) (β c : ℝ) :
    ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      |(fullQueryAlgorithm fun g : (Fin n → Bool) → ℝ =>
          Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ 0 / 2 := by
  intro g _
  simp [fullQueryAlgorithm]

/-- **Witness for `min_spotCheck_correct`.**  Two states, discrete envelope of oscillation `1`,
zero known part, hint `0`, exact accuracy (`ε = 0`), the uniform sampling distribution: every
closed slack ball and the set of minimisers have probability at least `1/2`, so the hypotheses
hold with `p = 1/2`, `N = 1`, `δ = 1/2` — one uniform sample returns the exact minimum of every
admissible residual with probability at least `1/2`. -/
theorem min_spotCheck_witness (g : Bool → ℝ) (hg : Admissible (discreteEnvelope 1) g) :
    1 - (1 / 2 : ℝ) ≤ ∑ _a ∈ univ.filter (fun a : Fin 1 → Bool =>
      |(spotCheck (fun g : Bool → ℝ => univ.inf' univ_nonempty fun x => (0 : ℝ) + g x)
          (fun _ => 0) a).output g - univ.inf' univ_nonempty fun x => (0 : ℝ) + g x| ≤ 0 / 2),
        ∏ _k : Fin 1, (1 / 2 : ℝ) := by
  have hinf : (univ.inf' univ_nonempty fun _ : Bool => (0 : ℝ) + 0) = 0 := by simp
  refine min_spotCheck_correct (d := discreteEnvelope 1) (ε := 0) (δ := 1 / 2) (p := 1 / 2)
    (fun _ : Bool => (0 : ℝ)) (fun _ => 0) 1
    (fun _ => 1 / 2) (fun _ => by norm_num) (by simp) (le_refl 0) (by norm_num)
    (fun y => ?_) ?_ (by norm_num) g hg
  · -- every closed ball contains its centre
    rw [hinf]
    have hmem : y ∈ univ.filter (fun a : Bool =>
        slack (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) a y ≤ 0 + 0 - 0 + 0 / 2) := by
      refine Finset.mem_filter.mpr ⟨mem_univ y, ?_⟩
      simp [slack, discreteEnvelope]
    calc (1 / 2 : ℝ) = ∑ a ∈ ({y} : Finset Bool), (1 / 2 : ℝ) := by simp
      _ ≤ _ := Finset.sum_le_sum_of_subset_of_nonneg (Finset.singleton_subset_iff.mpr hmem)
          fun _ _ _ => by norm_num
  · -- every state is a minimiser of the zero energy
    rw [hinf]
    simp
    norm_num

/-- **Witness for `min_hedgedSpotCheck_correct`.**  Two states, discrete envelope of oscillation
`1`, zero known part, hint `0`, accuracy `ε = 2` and hedge `η = 1` (so the accepted number is the
hint's minimum itself), the uniform sampling distribution: every closed slack ball of radius
`gap + ε - η` and the set of `η`-minimisers have probability at least `1/2`, so the hypotheses
hold with `p = 1/2`, `N = 1`, `δ = 1/2`. -/
theorem min_hedgedSpotCheck_witness (g : Bool → ℝ) (hg : Admissible (discreteEnvelope 1) g) :
    1 - (1 / 2 : ℝ) ≤ ∑ _a ∈ univ.filter (fun a : Fin 1 → Bool =>
      |(hedgedSpotCheck (fun g : Bool → ℝ => univ.inf' univ_nonempty fun x => (0 : ℝ) + g x)
          (fun _ => 0) ((univ.inf' univ_nonempty fun _ : Bool => (0 : ℝ) + 0) - 2 / 2 + 1)
          a).output g - univ.inf' univ_nonempty fun x => (0 : ℝ) + g x| ≤ 2 / 2),
        ∏ _k : Fin 1, (1 / 2 : ℝ) := by
  have hinf : (univ.inf' univ_nonempty fun _ : Bool => (0 : ℝ) + 0) = 0 := by simp
  refine min_hedgedSpotCheck_correct (d := discreteEnvelope 1) (ε := 2) (η := 1) (δ := 1 / 2)
    (p := 1 / 2) (fun _ : Bool => (0 : ℝ)) (fun _ => 0) 1
    (fun _ => 1 / 2) (fun _ => by norm_num) (by simp) (by norm_num) (by norm_num)
    (fun y => ?_) ?_ (by norm_num) g hg
  · -- every closed ball contains its centre
    rw [hinf]
    have hmem : y ∈ univ.filter (fun a : Bool =>
        slack (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) a y ≤ 0 + 0 - 0 + (2 - 1)) := by
      refine Finset.mem_filter.mpr ⟨mem_univ y, ?_⟩
      simp [slack, discreteEnvelope]
    calc (1 / 2 : ℝ) = ∑ a ∈ ({y} : Finset Bool), (1 / 2 : ℝ) := by simp
      _ ≤ _ := Finset.sum_le_sum_of_subset_of_nonneg (Finset.singleton_subset_iff.mpr hmem)
          fun _ _ _ => by norm_num
  · -- every state is a minimiser of the zero energy
    rw [hinf]
    simp
    norm_num

open Classical in
/-- **Witness for `cube_exact_dip_randomized` (and `thermal_exact_dip_randomized`).**  For every
`n`, `β > 0`, `c > 0` the hypotheses hold with radius `r = c`, ball size `B = 1` and accuracy
`ε = 0`: the dip of depth `c` at a point differs from the zero residual at that point only and
raises `log Z`.  Hence every randomised algorithm that returns `log Z` exactly with probability
`1 - δ` on the class makes at least `(1 - 2δ) 2^n` evaluations on the zero residual — the
statement `cube_exact_randomized`, obtained here from the general exact-dip bound. -/
theorem cube_exact_dip_witness (n : ℕ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {β c δ : ℝ} (hβ : 0 < β) (hc : 0 < c)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ (0 : ℝ) / 2), P ω) :
    (1 - 2 * δ) * 2 ^ n ≤ (∑ ω, P ω * ((alg ω).queries fun _ => 0).card) * 1 := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => c) :=
    hamEnv_isEnvelope fun _ => hc.le
  refine cube_exact_dip_randomized n alg P hP hP1 (r := c) hc.le (fun y => ?_) (fun a => ?_) hcorr
  · have hone : ∀ x : Fin n → Bool,
        (1 : ℝ) ≤ Real.exp (β * max 0 (c - hamEnv (fun _ : Fin n => c) x y)) := by
      intro x
      have h0 : (0 : ℝ) ≤ β * max 0 (c - hamEnv (fun _ : Fin n => c) x y) :=
        mul_nonneg hβ.le (le_max_left _ _)
      calc (1 : ℝ) = Real.exp 0 := Real.exp_zero.symm
        _ ≤ _ := Real.exp_le_exp.mpr h0
    have hy : (1 : ℝ) < Real.exp (β * max 0 (c - hamEnv (fun _ : Fin n => c) y y)) := by
      rw [hd.self y, sub_zero, max_eq_right hc.le]
      exact Real.one_lt_exp_iff.mpr (mul_pos hβ hc)
    have hlt : ∑ _x : Fin n → Bool, (1 : ℝ) <
        ∑ x : Fin n → Bool, Real.exp (β * max 0 (c - hamEnv (fun _ : Fin n => c) x y)) :=
      Finset.sum_lt_sum (fun x _ => hone x) ⟨y, mem_univ y, hy⟩
    have hcard : ∑ _x : Fin n → Bool, (1 : ℝ) = (2 : ℝ) ^ n := by simp
    rw [hcard] at hlt
    have hlog := Real.log_lt_log (by positivity) hlt
    linarith
  · have hsub : (univ.filter fun y : Fin n → Bool => hamEnv (fun _ : Fin n => c) a y < c) ⊆
        {a} := by
      intro y hy
      have hlt := (Finset.mem_filter.mp hy).2
      by_contra hne
      have hne' : a ≠ y := fun h => hne (by rw [Finset.mem_singleton]; exact h.symm)
      have := hamEnv_ge_of_ne hc.le hne'
      linarith
    have hcard := Finset.card_le_card hsub
    rw [Finset.card_singleton] at hcard
    exact_mod_cast hcard

/-- **Witness for `TwoMeasureBound`, `twoMeasureBound_pow` and `product_mass_ge`.**  One two-state
site with the uniform Gibbs law, the uniform reference, the discrete slack of oscillation `1`
and `β = 1` satisfies the two-measure bound with the (crude) constant `γ = 1`; hence `n` such
sites satisfy it with constant `n` (`twoMeasureBound_pow_witness`). -/
theorem twoMeasureBound_witness :
    TwoMeasureBound (fun _ : Bool => (1 / 2 : ℝ)) (fun _ => 1 / 2)
      (fun a b => if a = b then 0 else 1) 1 1 := by
  intro h hh
  have h01 := hh false true
  have h10 := hh true false
  simp only [Bool.false_eq_true, Bool.true_eq_false, if_false] at h01 h10
  rw [Fintype.sum_bool, Fintype.sum_bool]
  have e1 : Real.exp (1 * h true) ≤ Real.exp (1 * (1 / 2 * h true + 1 / 2 * h false) + 1) :=
    Real.exp_le_exp.mpr (by linarith)
  have e2 : Real.exp (1 * h false) ≤ Real.exp (1 * (1 / 2 * h true + 1 / 2 * h false) + 1) :=
    Real.exp_le_exp.mpr (by linarith)
  linarith

/-- The two-measure bound of `twoMeasureBound_witness` on `n` sites. -/
theorem twoMeasureBound_pow_witness (n : ℕ) :
    TwoMeasureBound (prodW (fun _ : Bool => (1 / 2 : ℝ)) n) (prodW (fun _ : Bool => (1 / 2 : ℝ)) n)
      (sumS (fun a b : Bool => if a = b then (0 : ℝ) else 1) n) 1 (n * 1) :=
  twoMeasureBound_pow _ _ _ 1 1 (fun _ => by norm_num) (fun _ => by norm_num) (by simp)
    (fun a => by simp) twoMeasureBound_witness n

/-- **Witness for `TwoMeasureLower` and `product_sandwich`.**  For the site of
`twoMeasureBound_witness` the reverse bound holds with constant `m = 0` (Jensen: the arithmetic
mean of two exponentials is at least the exponential of the mean), so `n` such sites satisfy the
two-sided sandwich `exp (E_{Qⁿ} h) ≤ ∑ πⁿ e^h ≤ exp (E_{Qⁿ} h + n)`. -/
theorem twoMeasureLower_witness :
    TwoMeasureLower (fun _ : Bool => (1 / 2 : ℝ)) (fun _ => 1 / 2)
      (fun a b => if a = b then 0 else 1) 1 0 := by
  intro h _
  rw [Fintype.sum_bool, Fintype.sum_bool]
  have key : Real.exp (1 * (1 / 2 * h true + 1 / 2 * h false) + 0) ≤
      1 / 2 * Real.exp (1 * h true) + 1 / 2 * Real.exp (1 * h false) := by
    have hx := Real.add_one_le_exp (1 * h true - (1 * (1 / 2 * h true + 1 / 2 * h false) + 0))
    have hy := Real.add_one_le_exp (1 * h false - (1 * (1 / 2 * h true + 1 / 2 * h false) + 0))
    have hpos := Real.exp_pos (1 * (1 / 2 * h true + 1 / 2 * h false) + 0)
    have e1 : Real.exp (1 * h true) = Real.exp (1 * (1 / 2 * h true + 1 / 2 * h false) + 0) *
        Real.exp (1 * h true - (1 * (1 / 2 * h true + 1 / 2 * h false) + 0)) := by
      rw [← Real.exp_add]
      congr 1
      ring
    have e2 : Real.exp (1 * h false) = Real.exp (1 * (1 / 2 * h true + 1 / 2 * h false) + 0) *
        Real.exp (1 * h false - (1 * (1 / 2 * h true + 1 / 2 * h false) + 0)) := by
      rw [← Real.exp_add]
      congr 1
      ring
    rw [e1, e2]
    nlinarith
  exact key

/-- The two-sided sandwich of `product_sandwich` on `n` copies of the witness site. -/
theorem product_sandwich_witness (n : ℕ) (h : Pw Bool n → ℝ)
    (hadm : ∀ a b, h b - h a ≤ sumS (fun a b : Bool => if a = b then (0 : ℝ) else 1) n a b) :
    Real.exp (1 * ∑ x, prodW (fun _ : Bool => (1 / 2 : ℝ)) n x * h x + n * 0) ≤
        ∑ x, prodW (fun _ : Bool => (1 / 2 : ℝ)) n x * Real.exp (1 * h x) ∧
      ∑ x, prodW (fun _ : Bool => (1 / 2 : ℝ)) n x * Real.exp (1 * h x) ≤
        Real.exp (1 * ∑ x, prodW (fun _ : Bool => (1 / 2 : ℝ)) n x * h x + n * 1) :=
  product_sandwich _ _ _ 1 0 1 (fun _ => by norm_num) (fun _ => by norm_num) (by simp)
    (fun a => by simp) twoMeasureLower_witness twoMeasureBound_witness n h hadm

/-- **Witness for `cube_nonadaptive_bound` (and `nonadaptive_expected_queries_ge`).**  For every
`n`, `β > 0`, `c > 0` the hypotheses hold with floor level `R = c`, ball size `B = 1` and accuracy
`ε = 0`: raising a cone to the level `c` changes it at its centre only and lowers `log Z`.
Hence every randomised non-adaptive algorithm that returns `log Z` exactly with probability
`1 - δ` on the class evaluates at least `(1 - 2δ) 2^n` points in expectation. -/
theorem cube_nonadaptive_witness (n : ℕ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {β c δ : ℝ} (hβ : 0 < β) (hc : 0 < c)
    (Q : Ω → Finset (Fin n → Bool)) (hna : ∀ ω g, (alg ω).queries g = Q ω)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ (0 : ℝ) / 2), P ω) :
    (1 - 2 * δ) * 2 ^ n ≤ (∑ ω, P ω * (Q ω).card) * 1 := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => c) :=
    hamEnv_isEnvelope fun _ => hc.le
  refine cube_nonadaptive_bound n alg P hP hP1 (R := c) hc.le Q hna (fun s => ?_) (fun a => ?_)
    hcorr
  · have hle : ∀ x : Fin n → Bool,
        Real.exp (-β * ((0 : ℝ) + max (hamEnv (fun _ : Fin n => c) x s) c)) ≤
          Real.exp (-β * ((0 : ℝ) + hamEnv (fun _ : Fin n => c) x s)) := by
      intro x
      refine Real.exp_le_exp.mpr ?_
      have := le_max_left (hamEnv (fun _ : Fin n => c) x s) c
      nlinarith
    have hs : Real.exp (-β * ((0 : ℝ) + max (hamEnv (fun _ : Fin n => c) s s) c)) <
        Real.exp (-β * ((0 : ℝ) + hamEnv (fun _ : Fin n => c) s s)) := by
      refine Real.exp_lt_exp.mpr ?_
      rw [hd.self s, max_eq_right hc.le]
      nlinarith
    have hlt : ∑ x : Fin n → Bool,
        Real.exp (-β * ((0 : ℝ) + max (hamEnv (fun _ : Fin n => c) x s) c)) <
        ∑ x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + hamEnv (fun _ : Fin n => c) x s)) :=
      Finset.sum_lt_sum (fun x _ => hle x) ⟨s, mem_univ s, hs⟩
    have hpos : 0 < ∑ x : Fin n → Bool,
        Real.exp (-β * ((0 : ℝ) + max (hamEnv (fun _ : Fin n => c) x s) c)) :=
      Finset.sum_pos (fun x _ => Real.exp_pos _) ⟨s, mem_univ s⟩
    have hlog := Real.log_lt_log hpos hlt
    linarith
  · have hsub : (univ.filter fun s : Fin n → Bool => hamEnv (fun _ : Fin n => c) a s < c) ⊆
        {a} := by
      intro s hs
      have hlt := (Finset.mem_filter.mp hs).2
      by_contra hne
      have hne' : a ≠ s := fun h => hne (by rw [Finset.mem_singleton]; exact h.symm)
      have := hamEnv_ge_of_ne hc.le hne'
      linarith
    have hcard := Finset.card_le_card hsub
    rw [Finset.card_singleton] at hcard
    exact_mod_cast hcard

/-- **Witness for `sum_le_truncated_add_tail`.**  Two states, discrete envelope of oscillation
`1`, the residual `(1, 0)`, `β = 1`, threshold `t = 1/2`: the state of weight `1` lies above the
threshold, the state of weight `e⁻¹` below it, and the lemma gives
`1 + e⁻¹ ≤ (1/2 + e⁻¹) + (1/2)(e - 1)`. -/
theorem tail_lemma_witness :
    (1 : ℝ) + Real.exp (-1) ≤ (1 / 2 + Real.exp (-1)) + 1 / 2 * (Real.exp 1 - 1) := by
  have he : (2 : ℝ) ≤ Real.exp 1 := by
    have := Real.add_one_le_exp (1 : ℝ)
    linarith
  have hinv : Real.exp (-1) ≤ 1 / 2 := by
    rw [Real.exp_neg]
    rw [inv_le_comm₀ (Real.exp_pos 1) (by norm_num)]
    simpa using he
  have hadm : Admissible (fun a b : Bool => if a = b then (0 : ℝ) else 1)
      (fun b : Bool => if b then (0 : ℝ) else 1) := by
    intro x y
    cases x <;> cases y <;> simp
  have key := sum_le_truncated_add_tail (X := Bool) hadm (β := 1) (t := 1 / 2) zero_le_one
    (fun _ => (1 : ℝ)) (fun x hx => by
      refine ⟨false, ?_, ?_⟩
      · simpa using hinv
      · cases x <;> simp)
  have hfilter : (univ.filter fun x : Bool =>
      (1 / 2 : ℝ) < Real.exp (-1 * (if x then (0 : ℝ) else 1))) = {true} := by
    ext x
    cases x
    · simp only [Finset.mem_filter, Finset.mem_univ, true_and, Bool.false_eq_true, if_false,
        Finset.mem_singleton, iff_false, not_lt]
      simpa using hinv
    · simp
      norm_num
  rw [hfilter] at key
  simp only [Fintype.sum_bool, if_true, Bool.false_eq_true, if_false, Finset.sum_singleton] at key
  have h1 : min (Real.exp (-1 * (0 : ℝ))) (1 / 2 : ℝ) = 1 / 2 := by
    rw [mul_zero, Real.exp_zero]
    exact min_eq_right (by norm_num)
  have h2 : min (Real.exp (-1 * (1 : ℝ))) (1 / 2 : ℝ) = Real.exp (-1) := by
    rw [mul_one]
    exact min_eq_left hinv
  rw [h1, h2] at key
  simp only [mul_zero, Real.exp_zero, mul_one] at key
  linarith

/-- **Witness for `linRes_span_exact` (and the span bracket).**  Three configurations with the
feature vectors `(1,0)`, `(0,1)`, `(1,1)`: the third is the sum of the first two, so two
evaluations determine the third value for every coefficient vector. -/
theorem linRes_span_witness (θ : Fin 2 → ℝ) :
    linRes (fun (x : Fin 3) (α : Fin 2) =>
        if x = 2 then (1 : ℝ) else if (x : ℕ) = (α : ℕ) then 1 else 0) θ 2 =
      ∑ k : Fin 2, (1 : ℝ) * linRes (fun (x : Fin 3) (α : Fin 2) =>
        if x = 2 then (1 : ℝ) else if (x : ℕ) = (α : ℕ) then 1 else 0) θ
          (if k = 0 then 0 else 1) := by
  refine linRes_span_exact _ θ (fun k : Fin 2 => if k = 0 then (0 : Fin 3) else 1)
    (fun _ => 1) 2 (fun α => ?_)
  fin_cases α <;> simp [Fin.sum_univ_two]

/-- **Witness for `pairRes_sub_le` (tightness of the profile envelope).**  Two configurations,
one grid cell: one has a pair inside the cutoff, the other has none, and the radial function
with increment `1` realises the full envelope distance `1`. -/
theorem pairRes_envelope_tight_witness :
    pairRes (fun k => if k = 0 then (1 : ℝ) else 0)
        (fun (x : Bool) (_ : ℕ) => if x then (1 : ℝ) else 0) 1 true -
      pairRes (fun k => if k = 0 then (1 : ℝ) else 0)
        (fun (x : Bool) (_ : ℕ) => if x then (1 : ℝ) else 0) 1 false =
      profEnv 1 (fun _ => 1) (fun (x : Bool) (_ : ℕ) => if x then (1 : ℝ) else 0) 1 true false ∧
    Admissible (profEnv 1 (fun _ => 1) (fun (x : Bool) (_ : ℕ) => if x then (1 : ℝ) else 0) 1)
      (pairRes (fun k => if k = 0 then (1 : ℝ) else 0)
        (fun (x : Bool) (_ : ℕ) => if x then (1 : ℝ) else 0) 1) := by
  refine ⟨?_, pairRes_admissible (by simp) (fun k hk => ?_) _⟩
  · simp [pairRes, profEnv, cumCount]
  · have hk0 : k = 0 := by omega
    subst hk0
    simp

/-- **Witness for `superSolution_le_hint` and `iterates_lt_hint_add` (the recursion of theory
report §11.18).**  In the small-slope limit the hinted exponent, continued by zero, is a
positive nonincreasing bounded function with `T ≤ R[T]` (`gauss_hint_superSolution`), so the
hypotheses of both theorems are satisfied by something other than zero, and the conclusion
`T ≤ θh` holds with equality: the bound is attained. -/
theorem hintRecursion_witness {g : ℝ} (hg : 0 < g) (hg1 : g < 1) :
    HintRecursion.gaussHintClip g ≤ HintRecursion.gaussHint g ∧
      HintRecursion.gaussHintClip g = HintRecursion.gaussHint g ∧
      0 < HintRecursion.gaussHintClip g ∧
      ∀ η : ℝ, 0 < η → ∃ k : ℕ, (fun (_ : ℕ) => HintRecursion.gaussHintClip) k g
        < HintRecursion.gaussHint g + η := by
  have hanti : ∀ x y : ℝ, 0 < x → x ≤ y →
      HintRecursion.gaussHintClip y ≤ HintRecursion.gaussHintClip x := by
    intro x y _ hxy
    unfold HintRecursion.gaussHintClip
    have h1 : min x 1 ≤ min y 1 := min_le_min hxy le_rfl
    have h2 : min y 1 ≤ 1 := min_le_right _ _
    nlinarith
  have hbdd : ∀ x : ℝ, 0 < x → HintRecursion.gaussHintClip x ≤ 1 := by
    intro x hx
    unfold HintRecursion.gaussHintClip
    have h1 : 0 ≤ min x 1 := le_min hx.le zero_le_one
    have h2 : min x 1 ≤ 1 := min_le_right _ _
    nlinarith
  have hnn : ∀ x : ℝ, 0 < x → 0 ≤ HintRecursion.gaussHintClip x := by
    intro x _
    unfold HintRecursion.gaussHintClip
    positivity
  refine ⟨HintRecursion.superSolution_le_hint HintRecursion.gaussPair
      HintRecursion.gauss_hint_superSolution hanti ⟨1, hbdd⟩ g hg hg1,
    HintRecursion.gaussHintClip_eq hg1.le, ?_, ?_⟩
  · unfold HintRecursion.gaussHintClip
    rw [min_eq_left hg1.le]
    have : 0 < 1 - g := by linarith
    positivity
  · intro η hη
    exact HintRecursion.iterates_lt_hint_add HintRecursion.gaussPair
      (fun _ => HintRecursion.gaussHintClip) (fun _ => HintRecursion.gauss_hint_superSolution)
      (fun _ _ _ => le_rfl) (fun _ => hanti) ⟨1, hbdd⟩ (fun _ => hnn) hg hg1 hη

end MetricChain.NonVacuity

-- The remainder of the anchored expansion as an identity; site penalties of every order (theory report Theorem 11.18d;
-- the statement is the Scientific Discovery Division's, SCI-MSG-0020)
#print axioms MetricChain.anchored_remainder_identity_mixConfig
#print axioms MetricChain.anchored_remainder_identity
#print axioms MetricChain.remainderBase_on
#print axioms MetricChain.anchored_remainder_bound
#print axioms MetricChain.cover_of_site_shares_order
#print axioms MetricChain.cover_of_equal_shares
#print axioms MetricChain.anchored_remainder_site_penalties
#print axioms MetricChain.anchored_remainder_witness

-- Barrier certificates: the Scientific Discovery Division's file (adopted) and the tree checker (theory report §11.31)
#print axioms MetricChain.Kinetics.cut_sound
#print axioms MetricChain.Kinetics.level_cut_sound
#print axioms MetricChain.Kinetics.robust_cut_sound
#print axioms MetricChain.Kinetics.robust_path_sound
#print axioms MetricChain.Kinetics.box_cut_barrier
#print axioms MetricChain.Kinetics.box_cut_barrier_residual
#print axioms MetricChain.Kinetics.certified_trap_height
#print axioms MetricChain.Kinetics.ferro_barrier
#print axioms MetricChain.Kinetics.ferroResidual_trap
#print axioms MetricChain.Kinetics.trap_survival
#print axioms MetricChain.Kinetics.trap_certificate
#print axioms MetricChain.Kinetics.trap_certificate_weighted
#print axioms MetricChain.Kinetics.box_trap_certificate
#print axioms MetricChain.Kinetics.ferroW_trap
#print axioms MetricChain.Dom.adjacent_iff
#print axioms MetricChain.CutTree.leaves_partition
#print axioms MetricChain.cutCheck_sound
#print axioms MetricChain.cutCheck_boxAdjacent_iff
#print axioms MetricChain.bcheck_sound
#print axioms MetricChain.bverify_sound
#print axioms MetricChain.bverify_sound_rev
#print axioms MetricChain.bverify_sound_real
#print axioms MetricChain.bverifyR_sound
#print axioms MetricChain.bverifyR_trap_height
#print axioms MetricChain.bverifyRTop_sound
#print axioms MetricChain.bverifyOn_sound
#print axioms MetricChain.ferro_barrier_exact
#print axioms MetricChain.maze_barrier_exact
#print axioms MetricChain.maze_boxCut_start_le
#print axioms MetricChain.maze_boxCut_target_le
#print axioms MetricChain.ferroWellR_trap
#print axioms MetricChain.scan_barrier_exact

#print axioms ScienceA17.sum_mul_eq_sum_increments
#print axioms ScienceA17.greedy_cost_le
#print axioms ScienceA17.marginal_tight
#print axioms ScienceA17.greedy_optimal
#print axioms MetricChain.remainderBase_host_anchor
#print axioms MetricChain.card_after_lt_of_hosts_last
#print axioms MetricChain.anchored_remainder_identity_orders
#print axioms MetricChain.anchored_remainder_bound_orders
#print axioms MetricChain.anchored_remainder_bound_hosts
#print axioms MetricChain.term_orders_sharp
#print axioms MetricChain.term_orders_sharp_host_moves
#print axioms MetricChain.anchoredSplit_sandwich_extrema
#print axioms MetricChain.anchoredSplit_exact_at_anchor

/-! ### The level recursion at the level of lines (theory report Theorem 11.53a; `LineDynamics.lean`) -/

#print axioms MetricChain.LineDynamics.line_le_Rstep
#print axioms MetricChain.LineDynamics.lines_le_exactRec
#print axioms MetricChain.LineDynamics.le_sSup_exactRec
#print axioms MetricChain.LineDynamics.gauss_slope_map
#print axioms MetricChain.LineDynamics.gauss_slope_map_least
#print axioms MetricChain.LineDynamics.gauss_lines_le_exactRec
#print axioms MetricChain.LineDynamics.gauss_level_two_ge
#print axioms MetricChain.LineDynamics.gauss_level_three_ge
#print axioms MetricChain.LineDynamics.StepLE.monotoneS_step
#print axioms MetricChain.LineDynamics.StepLE.line_step
#print axioms MetricChain.LineDynamics.StepLE.line_step_rate
#print axioms MetricChain.LineDynamics.gauss_level_two_majorant

/-! ### State-dependent penalties charged to sub-tuples, and the recovery of known slack
(requests P9-T1, P9-T3, A19-T1 of the Scientific Discovery Division, SCI-MSG-0028;
`ResolvedPenalties.lean`, `GibbsRecovery.lean`) -/

#print axioms MetricChain.ResolvedPenalties.resolved_allocation
#print axioms MetricChain.ResolvedPenalties.resolved_allocation_univ
#print axioms MetricChain.ResolvedPenalties.resolved_allocation_max
#print axioms MetricChain.ResolvedPenalties.reduction_step
#print axioms MetricChain.ResolvedPenalties.anchored_remainder_bound_orders_state
#print axioms MetricChain.ResolvedPenalties.anchored_remainder_bound_orders_off_anchor
#print axioms MetricChain.ResolvedPenalties.resolved_remainder_bound
#print axioms MetricChain.GibbsRecovery.lower_jensen
#print axioms MetricChain.GibbsRecovery.lower_product
#print axioms MetricChain.GibbsRecovery.upper_jensen
#print axioms MetricChain.GibbsRecovery.upper_product
#print axioms MetricChain.GibbsRecovery.log_Z_le_of_steps
#print axioms MetricChain.GibbsRecovery.log_Z_le_ueStep_iterate
#print axioms MetricChain.GibbsRecovery.log_Z_le_upStep_iterate

/-! ### The second Bonferroni inequality for a product of numbers in `[0, 1]` (inequality (c) of
Proposition A17.23 of the Scientific Discovery Division, SCI-RES-0035; `Bonferroni.lean`) -/

#print axioms MetricChain.Bonferroni.sum_sq_le_sq_sum
#print axioms MetricChain.Bonferroni.pairSum_nonneg
#print axioms MetricChain.Bonferroni.prod_one_sub_le
#print axioms MetricChain.Bonferroni.one_sub_sum_le_prod
#print axioms MetricChain.Bonferroni.prod_one_sub_mem
#print axioms MetricChain.Bonferroni.pairSum_eq_offDiag
#print axioms MetricChain.Bonferroni.prod_one_sub_le_witness

/-! ### Summing a site out of a box sum for arbitrary summands — the identity behind bucket
elimination, and the termwise relaxation of a factor (items R-1 and R-3 of STRUCTBIO-REQ-0003;
`FactorElimination.lean`) -/

#print axioms MetricChain.sum_boxFinset_branch
#print axioms MetricChain.sum_boxFinset_elim
#print axioms MetricChain.sum_boxFinset_sumOut
#print axioms MetricChain.sum_boxFinset_relax

/-! ### Automatic audit of every declaration (run last, so that it also covers the definitions
used by the witnesses above) -/

#audit_axioms proofs

