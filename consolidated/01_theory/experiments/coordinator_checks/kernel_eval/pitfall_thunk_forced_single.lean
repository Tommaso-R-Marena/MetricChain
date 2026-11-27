/-
Side experiment for README.md ("What failed, and what limits it"), not generated.

The largest theorem of pitfall_thunk_forced.lean alone.  Compare the peak memory of this file with
that of pitfall_thunk_forced.lean (three theorems of 50000, 100000 and 120000 steps): if the two
agree, the memory of a kernel evaluation is given back when the declaration is finished.
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

theorem t120k : g 120000 0 = true := by decide +kernel
