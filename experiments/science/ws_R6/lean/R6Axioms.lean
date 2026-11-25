import proofs.Frontiers.BoundedAccuracy
import proofs.Frontiers.QueryRefinements

/-!
Workstream R6 (science division): read-only audit of the machine-checked inputs of theory report §§11.18–11.19.
Prints the statements and the axioms of the declarations on which the paper chain rests.
Run:  cd /home/user/MetricChain && lake env lean <absolute path of this file>
-/
open MetricChain MetricChain.BoundedAccuracy MetricChain.HintRecursion

#check @admissible
#print admissible
#print Rstep
#print exactRec
#check @exactRec_reaches_hint
#check @exactRec_ge_hint
#check @exactRec_tendsto_hint
#check @two_rung_bound
#check @certified_lower_sum_le_mean
#check @populated_part_le
#check @close_points_bound'
#check @width_le
#check @cube_exact_dip_randomized
#check @cubeNa_isLeast_allRadii
#check @cubeNa_add_cubeHint

#print axioms exactRec_reaches_hint
#print axioms exactRec_ge_hint
#print axioms exactRec_tendsto_hint
#print axioms two_rung_bound
#print axioms certified_lower_sum_le_mean
#print axioms populated_part_le
#print axioms close_points_bound'
#print axioms width_le
#print axioms cube_exact_dip_randomized
#print axioms cubeNa_isLeast_allRadii
