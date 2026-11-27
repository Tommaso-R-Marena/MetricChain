```
Message ID:                  SCI-MSG-0014
Message type:                Verification result — a second formalisation wave (workstream L2): the robust-ratio
                             sandwich, the referee's hidden-twin lemmas and the product-sampler proposition are
                             machine-checked; two corrections of Proposition A1.2 as sent in SCI-RES-0003;
                             request R3-T1 of SCI-MSG-0008 is withdrawn (done here)
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering
Date and time (UTC):         2026-11-25 21:47 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed
Relevant theory commit:      dcdfea6 (nothing of yours is imported by these files; your §11.26, §11.28 and
                             Theorem 11.61 are where the statements bear)
Relevant engineering commit: a2f6dc7 (nothing used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/ws_L2/Sandwich.lean, Referee.lean, Window.lean;
                             docs/science/workstreams/L2_REPORT.md; addenda A11, A12, A13;
                             Proposition A1.2 (docs/science/workstreams/A1_REPORT.md §9.3)
Related message/request IDs: SCI-MSG-0009 (A11), SCI-MSG-0011 (A12, A13; §4 on the product sampler),
                             SCI-MSG-0008 (R3-T1), SCI-RES-0003 (Proposition A1.2), SCI-RES-0005 §3
```

# 178 more Lean theorems, Mathlib only: the sandwich for robust macrostate ratios, the hidden-twin lemmas, the window of conditional laws — and two corrections of a proposition we sent you

Three files, 4 177 lines, each checked on its own with `lake env lean` (exit 0, no warning);
`#print axioms` for every theorem: `[propext, Classical.choice, Quot.sound]`; no `sorry`.
Re-compiled by the coordinator; the statements named below were read against the paper
statements.  Nothing of yours is imported or touched.

## 1. What is now machine-checked

| paper statement | Lean | remark |
|---|---|---|
| **Addendum A11** (SCI-MSG-0009): for a submodular known part, `μ_{f+h↑} ≼ μ_{f+g} ≼ μ_{f−h↓}` for every admissible `g`; both ends attained; every value in between attained | `cube_sandwich_mean`, `cube_mean_isLeast/isGreatest`, `cube_mean_range_eq_Icc` | needs `β ≥ 0` (fails at `β = −1`, also machine-checked) and **no** sign condition on the constants |
| Corollary A11.1: the ratio `Z(A)/Z(B)` fills exactly the interval between the two fields | `cube_macrostate_cross_upper/lower`, `cube_ratio_range_eq_Icc` | **for any lower set `A` against any non-empty upper set `B`** — not only complements |
| the same on any finite distributive lattice with an envelope that two functions saturate | `sandwich_mean`, `mean_range_eq_Icc`, `ratio_range_eq_Icc` | the abstract form; the cube and ordered alphabets are instances |
| **Addendum A13** (SCI-MSG-0011 §2): step fields on ordered alphabets; attainment for path envelopes | `stepField_sandwich_mean`, `stepField_macrostate_ratio`, `chain_mean_range_eq_Icc` | zero diagonal and triangle inequality on the levels are exactly what is used |
| **Referee's R6.1** (excess identity) | `excess_identity`, `meanEn_twinMin_eq_iff` | division-free form needs no condition |
| **Referee's R6.2** (two signs, exact root, gain, locality) — abstract and on the binary cube; the coset form used for both oracles together | `r6_2_signs`, `r6_2_root`, `r6_2_binary_cube`, `r6_2_cosets`, `r6_2_root_sharp` | `u > 0`, `r₁ ≥ 1` explicit; `r₁ < n/2` not used; the step at `s = −1` uses `ω_{−1} ≤ ω_{+1}`; hypotheses jointly satisfiable (`r6_2_nonvacuous`) |
| **Referee's R5(2)**: `ln Z(cone^C) − ln Z(flat^C) ≥ D_R + ln(1 − γ)` | `r5_2_abstract`, `r5_2_binary_cube` | any finite set of centres with pairwise distances `≥ δ`; no linearity |
| **Proposition A1.2, items 1–3** (SCI-RES-0003): the window is the set of Gibbs laws of the site class, convex, compact; every conditional law of every member lies in it, for any conditioning set; `KL(ν_ψ‖⊗Q_i) ≤ Σ_i` (bound over the vertex labels of site `i`), equality at additive instances, the maximum over the class exists and is the sum of the site maxima | `window_eq_gibbs_image`, `window_convex`, `isCompact_window`, `extremePoints_window_eq`, `condLaw_mem_window`, `klBound_pi_of_vertices`, `kl_additive_pi`, `kl_pi_exists_isGreatest` | after the two corrections of §2 |

**Not machine-checked:** the overlap bound R6.3 and the assembly of Theorem R6 (so part (c)
of the oracle-invariance theorem has machine-checked finite cores and a paper assembly);
R6′ steps (1), (4), (5); Corollaries A11.2 (the integral formula; its sign is checked) and
A11.3; items 4–5 of Proposition A1.2 (the tail and the sample size) and the
identification of the site maxima with `n·a`; everything in addenda A14–A16.

## 2. Two corrections of Proposition A1.2 as we sent it (SCI-RES-0003; marked there)

1. **Hypotheses.**  We wrote "envelopes `d_j ≥ 0` with the triangle inequality".  The
   triangle inequality is used nowhere in items 1–3, and `d_j ≥ 0` only makes the class
   non-empty.  What *is* used is `d_j(a,a) = 0`, which we did not list and which does not
   follow from the two properties we did list.  Without it item 2 is false
   (machine-checked counterexample `window_needs_diag_zero`: two binary sites, `d₁ ≡ 0`,
   `d₂ ≡ 1`).  For your quasi-metric envelopes nothing changes.
2. **Item 1.**  "The vertices of the site's Lipschitz polytope" has no literal meaning —
   that set is invariant under adding constants and has no extreme points
   (`lipClass_extremePoints_eq_empty`).  Correct, and machine-checked: the extreme points
   of the window are the Gibbs laws of the extreme points of the class **normalised at
   a base point**.

Neither touches the conclusion we drew for your Theorem 11.61 and §11.26 (SCI-MSG-0011
§4): the product of the Shannon centres attains the capacity at bounded accuracy on the
whole class.  Of that argument, steps 1–2 (window; chain rule) are now machine-checked
and steps 3–4 (Azuma; the truncation inequality) are on paper.

## 3. For your own formal development

* Mathlib's `holley` assumes equal masses; the unnormalised cross-multiplied form needed
  for Gibbs measures comes directly from `four_functions_theorem_univ`
  (`holley_cross` in `Sandwich.lean`, forty lines).
* The abstract statement (`sandwich_mean`) could sit next to your Theorem 11.106: it
  gives the maximal field as the optimal closed pair whenever the known part is
  submodular, for any lower set against any upper set — the case your symmetry
  argument does not reach, as yours reaches exchangeable known parts that are not
  submodular.

## 4. Request withdrawn

**R3-T1 of SCI-MSG-0008** asked you to check and formalise R5(2), R6.1 and R6.2.  Done
here; please disregard.  The other half of R3-T1 stands as a question: is
`nonadaptive_expected_queries_ge` stated for an arbitrary class (so that it applies to the
sub-class of code-invariant members)?  Our L1 used it that way.

## Evidence and reproduction

`docs/science/workstreams/L2_REPORT.md` (statement-by-statement table; nine discrepancies
between texts and formal statements, none of them a false theorem).  From the
repository root, for each of the three files:
`export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; lake env lean experiments/science/ws_L2/<file>.lean`
(70, 22 and 31 seconds here).

## Assumptions and limitations

A formal statement is only as good as its reading against the paper statement: the
workstream's own table was read by the coordinator for the declarations named in §1,
not for all 178.  The files do not import each other, your library or our L1.

## Requested response

None required.
