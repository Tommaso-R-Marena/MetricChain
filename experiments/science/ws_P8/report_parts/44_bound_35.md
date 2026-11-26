### 3.5 The new constants at twelve residues [P for their validity as bounds of the remainder: Theorem AH; M for the numbers]

`p8_04_gamma12.py` and `p8_04b_gamma12_blocks.py` enumerate **all** subsets of order 4, 5, 6 (495,
792, 924) of the four twelve-residue peptides of the coordinator's reach table, with the same
anchor (P3's coordinate-descent anchor) and compute `ĉ_T` in P3's form and in the sharper forms
(0.05–0.15 s per subset after 15 s of set-up).  `Γ_m = Σ_T ĉ_T`, in `k_BT`:

<!--T:T6-->

*Checks at this size.*  (i) The sum over the enumerated subsets of my variant 'P3' equals P3's
closed-form `Γ_m` — the coordinator's numbers 689, 145, 23; 1 874, 568, 147; 5.4, 0.23, 0.0073;
316, 45, 5.0 — to at most `2·10⁻¹⁵` relative in all twelve cases, and the sum of 'AH' equals the
closed form with "X → A" likewise.  (ii) The chains `SAb ≤ SA ≤ S ≤ P3`, `SAb ≤ Sb ≤ S`, `SA ≤ AH ≤ P3`
hold for every subset.  (iii) On a random sample of subsets 'Sb' equals P3's own
`termwise.TermBound` in anchored mode (`p8_04c_termwise12.py`: Lys₁₂, order 4, eight subsets,
largest relative deviation `9.2·10⁻¹⁶`; Lys₁₂, order 5, four subsets, `3.9·10⁻¹⁶`; (LKSE)₃, order 4,
four subsets, `6.4·10⁻¹⁶`) — so the block-wise state-wise maximum at twelve residues is P3's own
code path, evaluated faster; only the step from 'Sb' to 'SAb' (Theorem AH) is mine.  (iv) The
exact anchored terms measured at twelve residues (§2.3) lie below the new constants subset by
subset.  Nothing at this size can be compared with exact all-context constants; the support is
§3.4.

*Reading.*  **Lys₁₂: 689, 145, 23.4 → 34.0, 2.40, 0.136 `k_BT`: factors 20, 60, 172.**  The new
constants fall 14- and 18-fold per order (P3's: 4.7- and 6.2-fold) — the slow fall the brief's
table showed was the merging step, which costs more the more sites of `T` are free.  (LKSE)₃:
1 874, 568, 147 → 296, 42.8, 4.87 (factors 6.3, 13, 30).  Ser₁₂: 5.44, 0.226, 0.0073 →
3.47, 0.138, 0.0042 (a factor 1.6–1.8: four moving atoms per side chain).  Leu₁₂: 316, 45.1, 5.01 →
286, 40.8, 4.53 (a factor 1.1: two rotamers per site, nothing to resolve; its slack is the
sign-blind one of P5).
"Anchored hosts" alone ('AH', the closed form) gains only 1.3–1.4: the terms with a host *in* `T`
dominate, and for those the anchor trick does nothing.

*For longer chains.*  The state-wise maximum has no closed form over `T`; at twenty residues and
order 5 there are 15 504 subsets (half an hour to an hour, extrapolating the speed above; not
run), at thirty residues and order 6 six hundred thousand.  A valid hybrid costs little: `Σ_T ĉ^{AH}_T` in closed form, minus
`Σ_{T near} (ĉ^{AH}_T − ĉ^{SAb}_T)` over the subsets inside a window, enumerated (every subset keeps a
valid constant).  Not run.
