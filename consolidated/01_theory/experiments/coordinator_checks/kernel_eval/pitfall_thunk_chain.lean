/-
Side experiment for README.md ("What failed, and what limits it"), not generated.

Pitfall: an accumulator that is passed along without ever being inspected by a `match`.
The kernel substitutes arguments unevaluated.  After i steps `acc` is therefore the nested term
`Nat.add (Nat.add (… (Nat.add 0 1) …) 1) 1` of depth i; its value is cached, but the term itself is
never replaced by the literal.  Observed (logs/pitfall_thunk_chain.log): the time per step is the
same for 50000 and 100000 steps and several times larger for 120000 steps.
-/
def f : Nat → Nat → Bool
  | 0, _ => true
  | n+1, acc =>
      match Nat.ble acc 1000000000 with
      | true => f n (Nat.add acc 1)
      | false => false

theorem t050k : f 50000 0 = true := by decide +kernel
theorem t100k : f 100000 0 = true := by decide +kernel
theorem t120k : f 120000 0 = true := by decide +kernel
