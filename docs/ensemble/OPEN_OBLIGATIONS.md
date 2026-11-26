# Unresolved proof obligations and open problems — Ensemble division

## Obligations (things our statements still owe)

| # | obligation | affects | priority |
|---|---|---|---|
| OB1 | ~~Internal adversarial review of every paper proof of version 1; apply its findings as linked corrections~~ **Done for Parts I–III** (`reviews/ER1_internal_review.md`; applied in report §7 item 6, ENSEMBLE-MSG-0003 §1a).  **Open:** the same for Parts IV and V, E2.2, E7′, E11(a) as rewritten, §4.4 (new in version 2; ER1 read E13(b), E17 once and made three remarks, which is not a review) | E13–E17, E7′ | high |
| OB2 | Read Odlyzko (1988) in the original: exact leading term `4C(p,3)(¾)ⁿ`, range `p ≤ n − 10n/ln n`, error term.  (ER1 confirmed the additive form through Irmatov's restatement; the original PDF was unreachable) | E10(c) | medium |
| OB3 | Read Deza–Laurent (book, the section on neighbourliness) or Ziegler's lectures: exact statement of 3-neighbourliness (ER1: confirmed in a search summary of Ziegler and by LP for `n ≤ 7`; the attribution to Deza–Laurent–Poljak 1992 is doubtful).  **No longer needed for E9(a)**, which now has its own proof (§4c.1 Remark 1); kept for the citation | citation only | low |
| OB4 | Read Garamvölgyi–Gortler–Jordán (2022) Sections 4–5 and check that nothing there contains E5(a)/E7; read Gortler–Healy–Thurston for the exact genericity statement used in E7 | E7 | high |
| OB5 | Read Vitushkin–Henkin (or Khavinson's book) for the exact hypotheses (domain, smoothness, weights) | E8.1 | medium |
| OB6 | Bai–Yin: exact hypotheses (i.i.d. entries with finite fourth moment; almost-sure convergence) | E11 | low |
| OB7 | Machine-check candidates: E1(a) "only if" (needs a theorem of the alternative), E2(a) weak duality in the dual form, the Littlewood–Offord lemma of E10, E12(a) | — | medium |
| OB8 | The sources marked "memory" in `PRIOR_ART.md` | novelty classes | medium |
| OB9 | Run the programme's full audit (`scripts/audit_all.sh`) on this branch | verified state | high |
| OB10 | Prior-art search for Parts IV and V and for E7′: first-order (density-ratio / Lipschitz-ratio) classes and identification by marginals; L¹ Poincaré inequalities for monotone functions (E15 is one line from them); body–bar frameworks and Stewart–Gough platforms with redundant legs; Donoho's modulus theory for moment problems | novelty classes of E13–E17, E7′ | high |
| OB11 | Read the Geometric Inference Division's `ENSEMBLE_RIGIDITY.md` in full (only its messages and theorem headings were read) and check our cross-references to its Theorems B, C, G and Proposition 3.1 | §§2.1, 4.2 of the report | medium |
| OB12 | Apply the science division's review SCI-REV-0020 (workstream R21) when it is published | E5, E7, E8, E1.3, §5 | high |
| OB13 | The translation from `thermal_union_bound` (monotone `r`, iterated product expectation) to Theorem E15(c) (total variation, one-body deficits, densities of class members) is on paper; a Lean statement about class members would close it | E15(c) | medium |
| OB14 | Store the threshold computations of §4.4 with their seeds in `experiments/ensemble/output_threshold.txt` (done at checkpoint 2 for the sizes quoted); larger sizes if the shared budget allows — a request to the engineering division would need the owner's authorisation for significant workloads | Conjecture C2 | low |
| OB15 | Baldi–Vershynin Theorem 4.2 is used as a black box: statement read verbatim, proof (their Sections 5–6) not read; journal reference not found.  Abbe–Shpilka–Wigderson Theorem 4.5 read only as quoted | E19 | medium |
| OB16 | Prior-art search for E20′ and the torus corollary of E20 (truncated trigonometric moment problems on tori; positive decompositions of tensors of format `2 × ⋯ × 2`); for E18′ (generic uniqueness of sparse non-negative representations); for C3 (ground-state capacity of higher-order interactions) | novelty classes of Part VI | medium |
| OB17 | Internal review of Part VI (written at the third checkpoint; read by nobody but its author) | E18–E20 | high |
| OB18 | The transfer of E20′ to chains rests on two statements of other divisions that we have not checked (competitors keep shared segments rigid; mean squared distances span the pairwise products of the differing torsions) | the remark after E20′ | medium |

## Open problems

Listed with their statements in `ENSEMBLE_REPORT.md` §9: O1 (capacity of pair data), O2
(`k`-body data; answered in part by E19), O3 (conformers with common rigid parts), O4
(quantitative ensemble rigidity), O5 (fewer moments), O6 (soft ensembles and adaptivity),
O7 (finite temperature), O8 (noise), O9 (a prior on the number of conformers, all
weights), O10 (the torus beyond sums of squares), and Conjectures C1 (the obstruction for
densities), C2 (a sharp threshold for pair data), C3 (the order of the capacity of
higher-order data).
