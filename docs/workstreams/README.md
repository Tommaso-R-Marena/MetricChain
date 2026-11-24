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
| A | yes | The refutation of the dip conjecture for sites with three or more states (flat four- and eight-state sites: re-derived by hand, exact binomial tails recomputed, harness `DEAD.16`, `DEAD_ENDS.md` D38).  The thresholds `ε₁^crit`, `ε₁^thr` of its three examples (recomputed by an independent linear program).  The proof of its Theorem B (two-measure tensorisation, bounded cost above the threshold): read and checked.  **Not yet integrated**: the scratch Lean file, the general lower bound as a theorem of the report, harness tests of the generalised dips.  **Not verified**: Theorem A(ii), the matching upper bound by inherently typical subsets — a paper proof that needs an independent referee. |
| C | yes | Nothing yet beyond the existence and abstract of the prior art it found (Hetland 2020, `prior_art/L7`).  Its normal form, its second best-first bound and its negative result on best-first search with a known part are to be verified in the next cycle. |
| B, D, E, G | not yet | — |

`COMMON.md` is the shared context given to every stream.  Scripts and raw outputs of the streams
were produced in a session scratch directory; the ones needed to reproduce an integrated claim
are copied next to the harness when the claim is integrated.
