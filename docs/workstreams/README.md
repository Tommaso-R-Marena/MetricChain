# Independent workstreams (cycle 8)

At the end of cycle 8 six independent investigations were run in parallel, each by a separate
researcher with its own brief and no access to the others' work.  This directory preserves
their briefs and reports **as delivered**.  A report is the work of its author: its claims are
*not* part of the theory report unless the theory report says so, and then only after an
independent re-verification (numerics re-run, statements re-derived, Lean where warranted).
What was verified and integrated, what was refuted, and what remains unverified is recorded in
`docs/RESEARCH_LOG.md` (cycle 8 and later) and, for refuted claims, in `docs/DEAD_ENDS.md`.

| stream | question | brief | report |
|---|---|---|---|
| A | Is the randomised exponent of `ln Z` given by single dips?  (A two-measure isoperimetric problem on product spaces.) | `A_brief.md` | `A_REPORT.md` |
| B | Known parts with chain structure: covering exponents, soft gaps, thresholds beyond independent sites. | `B_brief.md` | `B_REPORT.md` |
| C | Other representations: reduced costs and A*, discrete weak KAM, tropical geometry, tight spans. | `C_brief.md` | `C_REPORT.md` |
| D | Free-energy estimation in statistical mechanics; other observables; continuous spaces. | `D_brief.md` | `D_REPORT.md` |
| E | Second-order classes: how many evaluations are really needed? | `E_brief.md` | `E_REPORT.md` |
| G | Envelopes from the geometry of articulated chains: what the complexity theory predicts. | `G_brief.md` | `G_REPORT.md` |

**Status of the reports** (updated at each checkpoint; details in `docs/RESEARCH_LOG.md`).

| stream | delivered | what has been re-verified and integrated so far |
|---|---|---|
| A | yes | **Integrated** as theory report Theorems 11.27–11.28: generalised dips and the every-`n` lower bound (its Lemma 1 and Proposition 2; `GeneralisedDips.lean`, harness XII.9, XII.11), the refutation of the dip conjecture (`DEAD.16`, D38), the two-measure tensorisation and the instance-wise threshold (its Theorem B; Lean core from its scratch file; harness XII.10; all quoted numbers recomputed with independent code, benchmark B11).  Theorem A(ii), the matching upper bound by inherently typical subsets, was checked by an independent referee (`reviews/R4_referee_report.md`): no gap found; it is now stated in Theorem 11.27 as a paper proof.  Corrected by the referee: the report's claim that the result is not a corollary of the fixed-measure isoperimetric theorem is unsupported (the black-box bound coincides numerically with the game value); the headline sentences need their hypotheses (identical sites, accuracy not exponentially small, hint or star, hedged output). |
| B | yes | **Integrated**: its Theorem B.12 (hint-free threshold of identical two-state sites = largest chord gap of the pressure), as Theorem 11.28(d), after the proof was checked and the statement tested (harness XII.12, benchmark B11).  **Under independent review, not integrated**: the droplet criterion for chains, the exact exponent for homogeneous chains (a paper proof), the vacuous window of the transfer-matrix bound, the soft gap of a chain, Conjecture B.13. |
| C | yes | Reviewed (`reviews/R_C_review.md`): no headline theorem false.  **Integrated** as theory report §11.11: the normal form (Theorem 11.29; `NormalForm.lean`, which also proves the identification of certificates that the workstream had on paper; harness XI.14), the centre-form bound for best-first search with the scope found by the reviewer (Proposition 11.30), the line families (D39, `DEAD.17`), the Dechter–Pearl remark, the prior art (Hetland 2020).  Corrected by the reviewer: the bound's hypothesis forces `f = f^d`; "type-3 optimal" holds for a search started at a centre of the reduced envelope only; one of the two line families needed an extra point; one "iff" in its §2.4 is false.  Not integrated: the weak-KAM and optimal-transport dictionaries (identities), the exploratory search rule. |
| D | yes | Independent confirmation of the results of A (generalised dips, the game threshold, the two-reference verifier), noted.  One negative remark of the report (its dead end 6: "mean-based hint-free procedures cannot beat the passive width") is **corrected** by theory report Theorem 11.28(d): with the lower bound taken under the same reference law, one reference suffices and beats the passive width of the known part.  Reviewed (`reviews/R_D_review.md`): no critical error; the reviewer agrees with the correction just mentioned.  **Verified by the reviewer, integration pending**: the phase transition of second-order classes for `ln Z` at the Curie–Weiss coupling `βc₂n = 4`, the threshold `Σ ln(sinh b_i/b_i)` on the torus, the hardness of Boltzmann averages. |
| E | yes | Reviewed (`reviews/R_E_review.md`): no error in any theorem.  **Integrated** as theory report §11.12 (Theorems 11.31–11.32; `SecondOrderDip.lean` from its scratch files; harness XI.15; D40).  Corrected by the reviewer: "all but a `2^{−Θ(√n log n)}` fraction must be evaluated" (it is the fraction that is evaluated); "`N₂` = algorithmic cost" (up to `+1`); the comparison of the spider with `star ∪ {1}`; uncredited prior art for the quadratic law (Chierichetti–Dasgupta–Kumar).  Not integrated: the exact small-`n` tables, the sparse-constant details, the pairwise subclass (a sketch). |
| G | yes | Reviewed (`reviews/R_G_review.md`): no critical error; one major overstatement ("the whole exponential price is the `ℓ¹` chain rule": the sub-exponential upper bound holds at the zero residual and for `Lb/e = o(N)` only) and two constants that are numerical, not proved.  **Verified by the reviewer, integration pending**: the lever-arm law, the bound for weighted-Hamming envelopes with growing constants, the `√(λN)` bracket for the RMSD envelope used directly, the zipper bound. |

`COMMON.md` is the shared context given to every stream.  Scripts and raw outputs of the streams
were produced in a session scratch directory; the ones needed to reproduce an integrated claim
are copied next to the harness when the claim is integrated.
