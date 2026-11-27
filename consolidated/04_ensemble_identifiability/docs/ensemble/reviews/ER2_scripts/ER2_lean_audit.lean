import proofs.Ensemble.ThermalUnionBound

/-!
# ER2 audit of `proofs/Ensemble/ThermalUnionBound.lean`

Review ER2 (`docs/ensemble/reviews/ER2_internal_review.md`, §3).  Not part of the Lake build (the library
globs `proofs` only).  Check with

    lake env lean docs/ensemble/reviews/ER2_scripts/ER2_lean_audit.lean

It needs the compiled module `proofs.Ensemble.ThermalUnionBound` (present after a build).  Contents: the
axioms of the three theorems; the witness of `proofs/AxiomAudit.lean` copied verbatim, with both of its sides
evaluated; a witness for the density form, which `AxiomAudit.lean` does not have.
-/
open MetricChain.Ensemble

#print axioms MetricChain.Ensemble.thermal_union_bound
#print axioms MetricChain.Ensemble.thermal_union_bound_density
#print axioms MetricChain.Ensemble.thermal_union_bound_sharp
#check @MetricChain.Ensemble.thermal_union_bound
#check @MetricChain.Ensemble.thermal_union_bound_density
#check @MetricChain.Ensemble.thermal_union_bound_sharp

/-- The witness of `proofs/AxiomAudit.lean`, copied verbatim. -/
theorem ensemble_thermal_union_bound_witness :
    prodE [1/2, 1/3] (fun x => |(x.count true : ℝ)
        - prodE [1/2, 1/3] (fun x => (x.count true : ℝ))|)
      ≤ 2 * deficit [1/2, 1/3] (fun x => (x.count true : ℝ)) :=
  thermal_union_bound [1/2, 1/3]
    (by
      intro p hp
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
      rcases hp with rfl | rfl <;> norm_num)
    (fun x => (x.count true : ℝ))
    (by
      intro pre suf
      simp [List.count_append])

/-- ER2: the witness is a real instance — both sides evaluated.  E r = 5/6, E|r − E r| = 5/9,
deficit = 1/4 + 2/9 = 17/36, so the inequality of the witness reads 5/9 ≤ 17/18 (strict: two sites). -/
example : prodE [1/2, 1/3] (fun x => (x.count true : ℝ)) = 5/6 := by
  simp [prodE]; norm_num

example : prodE [1/2, 1/3] (fun x => |(x.count true : ℝ) - 5/6|) = 5/9 := by
  have h3 : |(2:ℝ) - 5/6| = 7/6 := by rw [abs_of_pos (by norm_num)]; norm_num
  have h1 : |(5:ℝ)/6| = 5/6 := abs_of_pos (by norm_num)
  simp [prodE]
  rw [h3, h1]
  norm_num

example : deficit [1/2, 1/3] (fun x => (x.count true : ℝ)) = 17/36 := by
  simp [deficit_cons, deficit_nil, prodE]
  norm_num

/-- ER2: a density instance (E r = 1) that is not constant: the hypotheses of
`thermal_union_bound_density` are satisfiable non-trivially (one site, p = 1/2, r = 2·1[excited]). -/
example : prodE [1/2] (fun x => if x = [true] then (2 : ℝ) else 0) = 1 := by
  simp [prodE]

/-- ER2: the monotonicity hypothesis is not vacuous in the other direction either: it fails for a
decreasing function. -/
example : ¬ (∀ pre suf : List Bool,
    (fun x : List Bool => -(x.count true : ℝ)) (pre ++ false :: suf)
      ≤ (fun x : List Bool => -(x.count true : ℝ)) (pre ++ true :: suf)) := by
  intro h
  have := h [] []
  norm_num at this

/-- ER2: `thermal_union_bound_density` has no witness in `AxiomAudit.lean` (the witness there has E r = 5/6).
Here is one: r = (6/5)·(number of excited sites) is monotone, has E r = 1 and is not constant. -/
theorem er2_density_witness :
    prodE [1/2, 1/3] (fun x => |(6/5 : ℝ) * (x.count true : ℝ) - 1|) ≤
      2 * ∑ i ∈ Finset.range ([1/2, 1/3] : List ℝ).length,
        (prodE [1/2, 1/3] (fun x => (6/5 : ℝ) * (x.count true : ℝ) * siteInd i x) - ([1/2, 1/3] : List ℝ).getD i 0) :=
  thermal_union_bound_density [1/2, 1/3]
    (by
      intro p hp
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
      rcases hp with rfl | rfl <;> norm_num)
    (fun x => (6/5 : ℝ) * (x.count true : ℝ))
    (by
      intro pre suf
      simp [List.count_append])
    (by
      simp [prodE]
      norm_num)

#print axioms er2_density_witness
#print axioms ensemble_thermal_union_bound_witness
