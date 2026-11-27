import proofs.Frontiers.SetLimit

/-! Workstream R2 (SCI-REV-0002): which axioms do the machine-checked theorems cited in theory
report §11.22 depend on?  (Run with `lake env lean` from the repository root; nothing is built.) -/

open MetricChain.SetLimit MetricChain.CoverStability

#check @SuperAdditive.hausdorff_limit
#check @SuperAdditive.dist_limit_le
#check @SuperAdditive.convex_limit
#check @SuperAdditive.cover_sandwich
#check @hasCover_of_close
#check @hasCover_sandwich
#check @hasCover_upper_iff
#print axioms SuperAdditive.hausdorff_limit
#print axioms SuperAdditive.dist_limit_le
#print axioms SuperAdditive.convex_limit
#print axioms SuperAdditive.cover_sandwich
#print axioms hasCover_sandwich
#print axioms hasCover_upper_iff
#print axioms hasCover_limit_point
#print axioms not_hasCover_shifted
