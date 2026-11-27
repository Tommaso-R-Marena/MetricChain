/-
  ER3 (internal review of Part VI of ENSEMBLE_REPORT.md): reviewer's Lean checks.
  Run from the repository root:   lake env lean docs/ensemble/reviews/ER3_scripts/er3_lean_checks.lean
  Nothing here is part of the division's proofs; it only (1) prints the axioms of the Part VI
  declarations, (2) instantiates them on instances that are not the division's witnesses, and
  (3) records two facts the report should state next to the machine-checked statements.
-/
import proofs.Ensemble.TwoStateCertificate
import proofs.Ensemble.PermanentCertificate

open MetricChain MetricChain.Ensemble Finset

#print axioms twoStateCert_eq_zero_iff
#print axioms twoStateCert_nonneg
#print axioms twoStateCert_unique_eq_zero
#print axioms twoStateCert_growth_three
#print axioms twoStateCert_growth_two
#print axioms permCert_nonneg
#print axioms permCert_eq_zero_iff
#print axioms permCert_eq_zero_iff_of_hall
#print axioms permCert_zero_set

/-! ### (A) The statements, restated verbatim: these `example`s only check that the declarations
have the types the report describes. -/

-- E20′ core: zero set of the two-state certificate.
example {ι : Type*} [Fintype ι] [DecidableEq ι] (a b : ι → ℝ) (ha : ∀ k, 0 ≤ a k)
    (hb : ∀ k, 0 ≤ b k) (hne : ∀ k, ¬ (a k = 0 ∧ b k = 0)) (htwo : ∀ k : ι, ∃ l, l ≠ k) :
    twoStateCert a b = 0 ↔ (∀ k, a k = 0) ∨ (∀ k, b k = 0) :=
  twoStateCert_eq_zero_iff a b ha hb hne htwo

-- E20″ core, three or more coordinates.
example {ι : Type*} [Fintype ι] [DecidableEq ι] (a b θ : ι → ℝ) (c : ℝ) (ha : ∀ k, 0 ≤ a k)
    (hb : ∀ k, 0 ≤ b k) (hor : ∀ k, θ k ≤ a k ∨ θ k ≤ b k) (hc0 : 0 ≤ c) (hcθ : ∀ k, c ≤ θ k)
    {i j m : ι} (hij : i ≠ j) (him : i ≠ m) (hjm : j ≠ m) :
    c * min (∑ k, a k) (∑ k, b k) ≤ twoStateCert a b :=
  twoStateCert_growth_three a b θ c ha hb hor hc0 hcθ hij him hjm

-- E21 (b), first sentence.
example {ι α β : Type*} [Fintype ι] [DecidableEq ι] [Fintype α] [DecidableEq α] [DecidableEq β]
    (s : ι → α → β) (x : α → β) (a : ι → α → ℝ)
    (ha : ∀ i k, 0 ≤ a i k) (hzero : ∀ i k, a i k = 0 ↔ x k = s i k)
    (hallS : ∀ I : Finset ι, 2 ≤ I.card →
      I.card ≤ (univ.filter (fun k => ∃ i ∈ I, ∃ j ∈ I, s i k ≠ s j k)).card) :
    permCert a = 0 ↔ ∃ i, x = s i :=
  permCert_zero_set s x a ha hzero hallS

/-! ### (B) Instances that are not the division's witnesses -/

/-- The quantitative two-coordinate statement on a *genuine* torus configuration (the division's
witness `a = (1,0)`, `b = (0,1)`, `θ = (1,1)` is an abstract instance: with `θ = β/4 = 1` the two
states are antipodal and then `a k + b k = 4`, which `(1,0),(0,1)` does not satisfy).
Antipodal states, configuration at `p` in coordinate 0 and at `q` in coordinate 1:
`a = (0, 4)`, `b = (4, 0)`, `θ = (1, 1)`, `c = 1/2`:  `1/2 * min 4 4 ≤ 0*0 + 4*4`. -/
example :
    (1 / 2 : ℝ) * min ((![0, 4] : Fin 2 → ℝ) 0 + (![0, 4] : Fin 2 → ℝ) 1)
        ((![4, 0] : Fin 2 → ℝ) 0 + (![4, 0] : Fin 2 → ℝ) 1)
      ≤ twoStateCert (ι := Fin 2) ![0, 4] ![4, 0] := by
  refine twoStateCert_growth_two ![0, 4] ![4, 0] ![1, 1] (1 / 2) ?_ ?_ ?_ ?_
    (by norm_num) (by norm_num)
  · intro k; fin_cases k <;> simp
  · intro k; fin_cases k <;> simp
  · intro k; fin_cases k <;> simp
  · intro k; fin_cases k <;> simp

/-- A three-state instance of `permCert_zero_set` on three coordinates with values in `Fin 3`, in
which the states *share* coordinate values pairwise (so the easy sufficient condition "any two
states differ in at least K coordinates" fails) but the Hall condition holds:
`s⁰ = (0,0,0)`, `s¹ = (0,1,1)`, `s² = (1,0,2)`; configuration `x = (0,0,1)` (not a state).
Pairs differ in 2, 2, 3 coordinates; the triple does not coincide in 3 coordinates. -/
example :
    permCert (ι := Fin 3) (α := Fin 3)
      (fun i k => if (![0, 0, 1] : Fin 3 → Fin 3) k
          = (![![0, 0, 0], ![0, 1, 1], ![1, 0, 2]] : Fin 3 → Fin 3 → Fin 3) i k then (0 : ℝ) else 1)
      ≠ 0 := by
  intro h
  have key := (permCert_zero_set (ι := Fin 3) (α := Fin 3) (β := Fin 3)
    ![![0, 0, 0], ![0, 1, 1], ![1, 0, 2]] ![0, 0, 1]
    (fun i k => if (![0, 0, 1] : Fin 3 → Fin 3) k
          = (![![0, 0, 0], ![0, 1, 1], ![1, 0, 2]] : Fin 3 → Fin 3 → Fin 3) i k then (0 : ℝ) else 1)
    (by intro i k; split_ifs <;> norm_num)
    (by
      intro i k
      by_cases hx : (![0, 0, 1] : Fin 3 → Fin 3) k
          = (![![0, 0, 0], ![0, 1, 1], ![1, 0, 2]] : Fin 3 → Fin 3 → Fin 3) i k
      · rw [if_pos hx]; exact ⟨fun _ => hx, fun _ => rfl⟩
      · rw [if_neg hx]; exact ⟨fun h => absurd h one_ne_zero, fun h => absurd h hx⟩)
    (by decide)).mp h
  obtain ⟨i, hi⟩ := key
  fin_cases i
  · have := congrFun hi 2; revert this; decide
  · have := congrFun hi 1; revert this; decide
  · have := congrFun hi 0; revert this; decide

/-! ### (C) Two facts to state next to the machine-checked statements -/

/-- With more states than coordinates the permanent certificate is identically zero (there is no
injective assignment), whatever the entries: the Hall condition of `permCert_zero_set` then cannot
hold, and the certificate says nothing.  (Three states, two coordinates.) -/
example (a : Fin 3 → Fin 2 → ℝ) (ha : ∀ i k, 0 ≤ a i k) : permCert a = 0 := by
  rw [permCert_eq_zero_iff a ha]
  refine ⟨univ, ?_⟩
  calc ((univ : Finset (Fin 3)).biUnion (offSet a)).card
      ≤ (univ : Finset (Fin 2)).card := Finset.card_le_card (Finset.subset_univ _)
    _ < (univ : Finset (Fin 3)).card := by simp

/-- `twoStateCert_growth_three` needs no sign condition on `θ`, and `min (1, ·)` never matters in
the report's constant: the theorem is used with `c = min θ`, `θ k = β k / 4 ≤ 1`.  Nothing to
prove here; the example shows that the constant `c = min θ` is *not* sharp on the instance of the
division's own witness (`a = (1,0,0)`, `b = (0,1,1)`): the certificate is `2`, the bound `1`. -/
example : twoStateCert (ι := Fin 3) ![1, 0, 0] ![0, 1, 1] = 2 := by
  simp [twoStateCert, Fin.sum_univ_three, Finset.sum_filter]
  norm_num
