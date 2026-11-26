/-
Side experiment for README.md ("What failed, and what limits it"), not generated.

The same loop as in pitfall_thunk_chain.lean, but the accumulator is the scrutinee of a `match` in
every step, so the kernel reduces it to a literal and the recursive call receives a term of
constant size (`Nat.add a 2` with a literal `a`).  Observed (logs/pitfall_thunk_forced.log): time
proportional to the number of steps, about 70 microseconds per step.
(A version of this file with a fourth theorem `g 200000 0 = true` ran through once and aborted once
with `std::bad_alloc` under the address-space limit; see README.md and
logs/pitfall_thunk_forced_4theorems_aborted.log.)
-/
def g : Nat → Nat → Bool
  | 0, _ => true
  | n+1, acc =>
      match acc with
      | 0 => g n 1
      | a+1 =>
          match Nat.ble a 1000000000 with
          | true => g n (Nat.add a 2)
          | false => false

theorem t050k : g 50000 0 = true := by decide +kernel
theorem t100k : g 100000 0 = true := by decide +kernel
theorem t120k : g 120000 0 = true := by decide +kernel
