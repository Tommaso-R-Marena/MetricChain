import proofs.Frontiers.TwoRounds
/-!
R4 (SCI-REV-0003): what exactly do the machine-checked declarations of `TwoRounds.lean` say,
and on which axioms do they rest?  (Read-only use of the built project.)
-/
open MetricChain.TwoRounds

#check @TwoRound
#print TwoRound
#check @TwoRound.output_eq_of_virtual
#check @card_distinguished_le
#check @prob_output_ne_ge
#check @two_round_bound
#check @two_round_witness

#print axioms TwoRound.output_eq_of_virtual
#print axioms card_distinguished_le
#print axioms prob_output_ne_ge
#print axioms two_round_bound
#print axioms two_round_witness
