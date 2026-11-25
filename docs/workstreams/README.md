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
| B | yes | **Integrated**: its Theorem B.12 (hint-free threshold of identical two-state sites = largest chord gap of the pressure), as Theorem 11.28(d), after the proof was checked and the statement tested (harness XII.12, benchmark B11).  Reviewed (`reviews/R_B_review.md`): the theorems hold, including the exponent for chains (no gap found); **Conjecture B.13 is false** (explicit counterexamples by the reviewer, one recomputed here; D41), and the statement about the threshold of antiferromagnetic chains was wrong.  **Integrated** as theory report §11.15 (Theorems 11.39–11.40, Propositions 11.41–11.42).  Not integrated: the block brackets and tables, the three budgets for chains (two rows unproved). |
| C | yes | Reviewed (`reviews/R_C_review.md`): no headline theorem false.  **Integrated** as theory report §11.11: the normal form (Theorem 11.29; `NormalForm.lean`, which also proves the identification of certificates that the workstream had on paper; harness XI.14), the centre-form bound for best-first search with the scope found by the reviewer (Proposition 11.30), the line families (D39, `DEAD.17`), the Dechter–Pearl remark, the prior art (Hetland 2020).  Corrected by the reviewer: the bound's hypothesis forces `f = f^d`; "type-3 optimal" holds for a search started at a centre of the reduced envelope only; one of the two line families needed an extra point; one "iff" in its §2.4 is false.  Not integrated: the weak-KAM and optimal-transport dictionaries (identities), the exploratory search rule. |
| D | yes | Independent confirmation of the results of A (generalised dips, the game threshold, the two-reference verifier), noted.  One negative remark of the report (its dead end 6: "mean-based hint-free procedures cannot beat the passive width") is **corrected** by theory report Theorem 11.28(d): with the lower bound taken under the same reference law, one reference suffices and beats the passive width of the known part.  Reviewed (`reviews/R_D_review.md`): no critical error; the reviewer agrees with the correction just mentioned.  **Integrated** as theory report §11.13 (Theorems 11.33–11.35): the phase transition of second-order classes for `ln Z` at the Curie–Weiss coupling `βc₂n = 4`, the threshold `Σ ln(sinh b_i/b_i)` on the torus, the hardness of Boltzmann averages (harness XII.15 for the droplet, the Curie–Weiss sign and the circle).  Its three scratch Lean files restate lemmas that the repository already has in another parametrisation and were not added. |
| E | yes | Reviewed (`reviews/R_E_review.md`): no error in any theorem.  **Integrated** as theory report §11.12 (Theorems 11.31–11.32; `SecondOrderDip.lean` from its scratch files; harness XI.15; D40).  Corrected by the reviewer: "all but a `2^{−Θ(√n log n)}` fraction must be evaluated" (it is the fraction that is evaluated); "`N₂` = algorithmic cost" (up to `+1`); the comparison of the spider with `star ∪ {1}`; uncredited prior art for the quadratic law (Chierichetti–Dasgupta–Kumar).  Not integrated: the exact small-`n` tables, the sparse-constant details, the pairwise subclass (a sketch). |
| G | yes | Reviewed (`reviews/R_G_review.md`): no critical error; one major overstatement ("the whole exponential price is the `ℓ¹` chain rule": the sub-exponential upper bound holds at the zero residual and for `Lb/e = o(N)` only) and two constants that are numerical, not proved.  **Integrated** as theory report §11.14 (Theorems 11.36–11.38) with the reviewer's constants and scope, as D42, and as a warning in blueprint §7; its lemma on the residual-independence of the spot-check constant is now `SoftGapIndependence.lean` (harness XII.14). |

`COMMON.md` is the shared context given to every stream.  Scripts and raw outputs of the streams
were produced in a session scratch directory; the ones needed to reproduce an integrated claim
are copied next to the harness when the claim is integrated.  From workstream K on, a
workstream's own scripts and outputs are kept under `experiments/workstreams/<stream>/` (the
Computational Research Division pointed out that the earlier ones cannot be re-run; one of
their quantities, `m(δ)` of `P_REPORT.md` §3.2, turned out not to be reproducible as defined —
`DEAD_ENDS.md` D46).

## Cycle 10

Two further workstreams were started after checkpoint `59e6761`, each on a question that the
coordinator was working on at the same time, with the instruction to try to break the
coordinator's claims first.

| stream | question | brief | report |
|---|---|---|---|
| H | Algorithms without a hint on the cube: verify the Monte Carlo and non-adaptive results of theory report §11.16; is adaptivity enough to reach the hinted exponent? | `H_brief.md` | `H_REPORT.md` (delivered: the four statements of §11.16 confirmed; on radial instances adaptivity closes the whole gap; a two-level algorithm beats the non-adaptive exponent on the whole class; the coordinator's own multilevel accounting refuted.  Integrated as theory report §11.18, where its Theorems H1 and H2 are Theorems 11.51 and 11.52, its conjecture H4 is proved (Theorem 11.53) and one gap of its algorithm is repaired (`DEAD_ENDS.md` D45); the section was refereed in `reviews/R7_referee_report.md`) |
| P | Chains: envelopes from pair-distance profiles (theory report §11.17); verification on synthetic chains, lower bounds, prior art. | `P_brief.md` | `P_REPORT.md` (delivered; reviewed in `reviews/R_P_review.md`: no statement false, four numbers and several sentences of the summary corrected; its corrections to the coordinator's claims and the reviewer's corrections to its own are applied in theory report §11.17) |
| K | Adaptive algorithms without a hint at a **bounded** accuracy: is the exponent `h` (conjecture K), with a layer-cake sum for the lower end? | `K_brief.md` | `K_REPORT.md` (delivered: **the conjecture holds in its strong form** — exponent `h` at every fixed accuracy and down to `e^{-o(n)}`; a modified two-level algorithm 2L⁺ with explicit constants; the coordinator's sketch was wrong in its mechanism and in one reason, `DEAD_ENDS.md` D46.  Integrated as theory report §11.19 — its Lemma K.4, Theorem K1, Propositions K0/K2/K5 and Theorem K3 are Lemma 11.55, Theorem 11.56, Proposition 11.57 and Theorem 11.58 — **labelled unrefereed: referee R8 was reading it at the checkpoint of integration** (`reviews/R8_brief.md`).  Its four Lean files are merged into `proofs/Frontiers/BoundedAccuracy.lean`; its scripts and outputs are in `experiments/workstreams/K/`) |
| F | Algorithms without a hint with a **known part** (biased product reference measure; then `k`-state sites): non-adaptive exponent, tail lemma without Harper, does "adaptive = hinted" survive, instance-optimality in the field | `F_brief.md` | commissioned 2026-11-25; running at the time of writing |
| L | Lean: the exponent functions of the cube satisfy the abstract hypotheses (`HintPair`) of the convergence theorem, so that Theorem 11.53 is machine-checked for the cube and not only for an abstract pair | `L_brief.md` | `L_REPORT.md` (delivered: `proofs/Frontiers/CubeHintPair.lean`, 69 declarations, integrated after the coordinator's check; also both halves of the fixed-point statement on the cube) |
| S | A limit shape for profile sets and the thermodynamic limit of certificate sizes (the question the Computational Research Division put back to the theory in `ENG-REQ-0001`): reduction to site sets, concatenation and convexity for bridges, the buried-end obstruction for unrestricted walks, convergence of covering numbers, computable bounds for the plateau | `S_brief.md` | commissioned 2026-11-25; running at the time of writing |
