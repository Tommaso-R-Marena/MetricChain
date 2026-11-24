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
| A | yes | **Integrated** as theory report Theorems 11.27–11.28: generalised dips and the every-`n` lower bound (its Lemma 1 and Proposition 2; `GeneralisedDips.lean`, harness XII.9, XII.11), the refutation of the dip conjecture (`DEAD.16`, D38), the two-measure tensorisation and the instance-wise threshold (its Theorem B; Lean core from its scratch file; harness XII.10; all quoted numbers recomputed with independent code, benchmark B11).  **Not verified**: Theorem A(ii), the matching upper bound by inherently typical subsets — an independent referee is reading it; until then it is reported as a claim. |
| B | yes | **Integrated**: its Theorem B.12 (hint-free threshold of identical two-state sites = largest chord gap of the pressure), as Theorem 11.28(d), after the proof was checked and the statement tested (harness XII.12, benchmark B11).  **Under independent review, not integrated**: the droplet criterion for chains, the exact exponent for homogeneous chains (a paper proof), the vacuous window of the transfer-matrix bound, the soft gap of a chain, Conjecture B.13. |
| C | yes | Prior art it found is recorded (`prior_art/L7`: Hetland 2020).  **Under independent review, not integrated**: the normal form `(σ, 0, E^d)`, the second best-first bound, the Dechter–Pearl classification, the negative result on the line with a known part. |
| D | yes | Independent confirmation of the results of A (generalised dips, the game threshold, the two-reference verifier), noted.  One negative remark of the report (its dead end 6: "mean-based hint-free procedures cannot beat the passive width") is **corrected** by theory report Theorem 11.28(d): with the lower bound taken under the same reference law, one reference suffices and beats the passive width of the known part.  **Under independent review, not integrated**: the phase transition of second-order classes at the Curie–Weiss coupling, the threshold on the torus, the hardness of Boltzmann averages. |
| E | yes | **Under independent review, not integrated**: the second-order dip and "stars do not combine" (machine-checked in its scratch files), the sandwich for `N₂`, the mean-field transition, the spider. |
| G | yes | **Under independent review, not integrated**: the lever-arm law of the torsion-to-RMSD constants, the bounds for weighted-Hamming envelopes with growing constants, the `√(λN)` law for the RMSD envelope used directly, the zipper bound for contact residuals. |

`COMMON.md` is the shared context given to every stream.  Scripts and raw outputs of the streams
were produced in a session scratch directory; the ones needed to reproduce an integrated claim
are copied next to the harness when the claim is integrated.
