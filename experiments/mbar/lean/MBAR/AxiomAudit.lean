import MBAR

/-!
Axiom audit of the headline declarations of Division 9.  Every line below must report only
`propext`, `Classical.choice`, `Quot.sound` (or no axioms).  Run by `audit.sh`; the output is
stored in `logs/axioms.log`.
-/

open MBAR MBAR.Model

-- Allocation (part A)
#print axioms MBAR.Model.weak_duality
#print axioms MBAR.Model.rstar_feasible
#print axioms MBAR.Model.pythagoras
#print axioms MBAR.Model.rstar_optimal
#print axioms MBAR.Model.strong_duality
#print axioms MBAR.Model.zfun_maximises
#print axioms MBAR.Model.J_rstar_formula
#print axioms MBAR.Model.V_eq_J_rstar
#print axioms MBAR.Model.V_eq_formula
#print axioms MBAR.Model.perspective_ineq
#print axioms MBAR.Model.J_convex
#print axioms MBAR.Model.V_convex
#print axioms MBAR.Model.V_convex_of_solutions
#print axioms MBAR.Model.cs_form
#print axioms MBAR.Model.precision_superadditive
#print axioms MBAR.Model.Q_le_budget
#print axioms MBAR.Model.efficiency_bound
#print axioms MBAR.Model.equivalence_sufficient
#print axioms MBAR.Model.rounding_bound
#print axioms MBAR.neyman_lower
#print axioms MBAR.neyman_attained
-- E-values (part B)
#print axioms MBAR.Model.expect_stat
#print axioms MBAR.Model.prod_pow_le_one
#print axioms MBAR.Model.stratified_evalue
#print axioms MBAR.Model.lr_family_evalue
#print axioms MBAR.Model.markov_finite
#print axioms MBAR.Model.lr_region_coverage
-- Lower bounds (part C)
#print axioms MBAR.weighted_ls_identity
#print axioms MBAR.edge_energy_identity
#print axioms MBAR.chisq_categorical
#print axioms MBAR.abs_exp_sub_one_le_mul_exp
#print axioms MBAR.kl_le_chisq
#print axioms MBAR.max_principle
#print axioms MBAR.harmonic_extremes
#print axioms MBAR.le_cam
#print axioms MBAR.Model.tilt_sum_one
#print axioms MBAR.Model.chisq_tilt
#print axioms MBAR.Model.chisq_budget
#print axioms MBAR.log_one_add_le
#print axioms MBAR.log_one_add_ge
-- Localisation and composition (handoff B1, C1, E3)
#print axioms MBAR.Softmax.hasDerivAt_m
#print axioms MBAR.Softmax.hasDerivAt_Vr
#print axioms MBAR.Softmax.kappa_ge
#print axioms MBAR.Softmax.Vr_ge
#print axioms MBAR.Softmax.curvature_integrated
#print axioms MBAR.curvature_sum
#print axioms MBAR.pairing_le
#print axioms MBAR.cut_localization
#print axioms MBAR.free_energy_envelope
#print axioms MBAR.contrast_composition
