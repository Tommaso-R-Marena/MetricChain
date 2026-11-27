import proofs.StructBio.FactorElimination
import proofs.AuditCommand

/-!
# Axiom audit of the Structural & Computational Biology division's Lean files

Self-contained: the theory division's `proofs/AxiomAudit.lean` is not modified by this division
(it belongs to the theory division's audited tree; whether it imports this directory is the
theory division's decision).  `lake build proofs.StructBio.AxiomAudit` prints the axioms of
every theorem named below and then walks **every** constant defined in a module `proofs.StructBio.*`
(private and auxiliary constants included), failing unless each depends on no axiom other than
`propext`, `Classical.choice`, `Quot.sound`.
-/

#print axioms MetricChain.sum_boxFinset_branch
#print axioms MetricChain.sum_boxFinset_repin
#print axioms MetricChain.sum_boxFinset_sumOut
#print axioms MetricChain.sum_boxFinset_elim
#print axioms MetricChain.sumOut_update_self
#print axioms MetricChain.sumOut_update_of_invariant
#print axioms MetricChain.sum_boxFinset_mono
#print axioms MetricChain.sum_boxFinset_prod_mono
#print axioms MetricChain.sum_boxFinset_prune
#print axioms MetricChain.sum_boxFinset_relax
#print axioms MetricChain.sum_boxFinset_relax_pair
#print axioms MetricChain.partitionFn_prune
#print axioms MetricChain.partitionFn_relax_pair
#print axioms MetricChain.iterate_sq_rounded_down
#print axioms MetricChain.iterate_sq_rounded_up
#print axioms MetricChain.expTaylor_add_expErr_pos
#print axioms MetricChain.iterate_sq_rounded_down_le_expLo
#print axioms MetricChain.expHi_le_iterate_sq_rounded_up
#print axioms MetricChain.exp_enclosure_rounded

#audit_axioms proofs.StructBio
