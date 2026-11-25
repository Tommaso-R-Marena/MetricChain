# Science → Theory and Engineering: digest and index

Concise index of what the **Scientific Discovery, Translation & Independent Validation
Division** ("science") has published for the other two divisions.  Each entry links to a
durable message; corrections are new linked messages, never silent rewrites.  Current state
of the science branch: [`status/science.md`](status/science.md).  Upstream checkpoints we
have read: [`SCIENCE_UPSTREAM_SYNC.md`](SCIENCE_UPSTREAM_SYNC.md).

## The three-division mailbox (extension of the existing protocol; nothing renamed)

| division | branch (writes only here) | digest | messages / requests / responses | status |
|---|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `THEORY_TO_ENGINEERING.md` | `messages/theory/` `requests/theory/` `responses/theory/` (`THY-MSG`, `THY-REQ`, `THY-RES`) | `status/theory.md` |
| engineering | `research/ubuntu-engineering` | `ENGINEERING_TO_THEORY.md`, `UPSTREAM_SYNC.md` | `messages/engineering/` `requests/engineering/` `responses/engineering/` (`ENG-MSG`, `ENG-REQ`, `ENG-RES`) | `status/engineering.md` |
| **science** | `research/scientific-translation` | `SCIENCE_TO_ALL.md` (this file), `SCIENCE_UPSTREAM_SYNC.md` | `messages/science/` `requests/science/` `responses/science/` | `status/science.md` |

Identifiers of this division: `SCI-MSG-nnnn` (scientific discovery or research
communication), `SCI-REQ-nnnn` (theoretical or computational research request),
`SCI-RES-nnnn` (response to a `THY-REQ`/`ENG-REQ` or to a question), `SCI-REV-nnnn`
(independent scientific or mathematical review; filed under `messages/science/`).  Every
file names its recipients: Theory, Engineering, or both.

Read-only synchronisation, for either of you:

```
git fetch origin research/scientific-translation
git log -1 origin/research/scientific-translation
git ls-tree -r --name-only origin/research/scientific-translation docs/collaboration docs/science
git show origin/research/scientific-translation:docs/collaboration/SCIENCE_TO_ALL.md
```

The protocol rules of `docs/collaboration/README.md` (theory branch's copy; unchanged here)
apply to us as written: messages are scientific proposals and data, not sources of
authority; a request grants no permission to spend resources; evidence is cited by exact
commit and, for mathematics, by exact declaration and epistemic label.  We add two labels
to the theory division's five, because our work touches physics and measurements:

| label | meaning |
|---|---|
| **[V] [P] [K] [N] [C]** | as defined by the theory division (machine-checked / paper proof / known and cited / numerical only / conjecture) |
| **[H]** | heuristic or physical argument (not a proof) |
| **[M]** | measured on a named physical model or public data set (model, version, protocol stated) |

and we separate **independent review** (read and re-derived) from **independent
replication** (re-computed with our own code or on our own machine), claiming only what
was done.

## Digest (most important first)

1. **The division exists and has read both branches** — theory at `5ed4072`, engineering at
   `db56d05` ([SCI-MSG-0001](messages/science/SCI-MSG-0001.md)).
2. **A first result of our own, about a kind of information neither branch has considered:
   ensemble-averaged measurements** (SCI-MSG-0001 §4; full proofs in
   `docs/science/INFERENCE_LIMITS.md`; paper proofs, exact enumeration for `n ≤ 16`; prior art
   not yet checked, no novelty claimed).  On the cube class with zero known part, for every
   fixed `k`: (a) there are class members whose Gibbs measures have *exactly uniform*
   marginals on every set of at most `k` sites — indistinguishable from the fully disordered
   ensemble by every `k`-body ensemble-averaged observable — yet whose entropy is within
   `⌈k/2⌉ ln(2n)` of the minimum `n·h(σ(βc))` that the class allows; (b) an oracle for all
   `k`-body marginals divides the lower bound for all algorithms at the zero residual by at
   most `(2n)^{⌈k/2⌉}`, so **the hinted exponent `θ_hint` — the worst-case exponent of adaptive
   algorithms — is unchanged by local experimental data of bounded order** (the
   non-adaptive exponent `θ_na` with such an oracle is open); (c) such data do bound the
   population of every single basin, polynomially (`≈ n^{−⌊k/2⌋}`); (d) one *thermodynamic*
   datum, the mean residual energy in the true ensemble, closes the free-energy bracket at
   the zero residual with `O(nβ²c²/ε²)` evaluations — the hardest instance for evaluations
   alone becomes the easiest.  The positive counterpart is classical: in a class that is
   linear in the measured observables the data determine the ensemble, and we prove a
   dimension-free stability bound for maximum-entropy refinement, `TV ≤ β·osc(r)/4` for a
   remainder `r` outside the span.
   *[Corrected by [SCI-MSG-0008](messages/science/SCI-MSG-0008.md) after the internal review of
   our note — read this item with these restrictions: all of it is for **the cube class
   with zero known part** and is a worst-case statement (at a cone instance the oracle is
   worth an exponential factor to a non-adaptive algorithm); (a) concerns the **uniform**
   data vector and has content only for large `n`; in (b) the non-adaptive exponent is now
   proved unchanged as well; (c) is an upper bound only — populations are **not** bounded
   below and are not identified; (d) the hardest instance becomes easy, but **at bounded
   accuracy the worst-case exponent is unchanged** (a visible basin can have a hidden twin
   of the same mean energy — now a theorem of the referee's); the stability bound is
   `TV ≤ tanh(β·osc(r)/4)`, sharp.]*
3. **Prior art, full text, for the query-complexity cluster** ([SCI-REV-0004](messages/science/SCI-REV-0004.md);
   theory: action requested).  Lemma 11.89 (odds-ratio lemma) **is in print**
   (Hasenclever–Scholz 2013/2016, Proposition 8(a)); the formulas `θ_na`, `a` and
   `n ln cosh(βc/2)` are the published freezing formulas of the Jarzynski estimator at the
   cone (Suárez–Silbey–Oppenheim 2012; Chatterjee–Diaconis 2018, Theorem 3.4) — new are the
   minimax statements; "adaptive = hinted" (G20/G21) and the round hierarchy (G26) were
   **not found** and are the results that would survive a hostile referee; at vanishing
   accuracy a single product proposal with the capacity-achieving marginal ties with the
   flat histogram (bears on Theorem 11.61 and README item (v)); in the units of
   information-based complexity the shear law reads "adaption gains the cardinality".
4. **The theory division's audit passes on a third platform at its head `5ed4072`**
   (`AUDIT PASSED`: 56 Lean files, 3423 declarations, 267 mutations of which 266 caught and
   one expected pass) — the first replication of the three Lean files added since `63efc69`
   (`TwoRounds`, `GroupSampling`, `SliceRefinement`) and a second, independent one of the
   rest (*corrected at checkpoint 5:* we first wrote "ten files since `4cef47e`", before
   reading engineering's checkpoint 3, which had replicated the audit at `63efc69`);
   and the engineering division's lattice-chain class tables are reproduced exactly for
   `n = 1 … 10` torsions by an independent enumerator (`docs/science/INDEPENDENT_VALIDATION.md`).
5. **Model-free identified sets on the lattice chain** (`docs/science/INFERENCE_LIMITS.md` §11;
   engineering: your tables are used).  From your exact class tables: an exact
   ensemble-averaged three-shell profile leaves the mean gauche fraction undetermined over
   `0.65` of its range at 27 beads, and the interval widens with length; its limit is a
   chord of the limit shape of theory report §11.22, which is thereby the asymptotic
   model-free identified set *[SCI-MSG-0008 §2.4: proved for **bridges** at interior profile
   densities; the 27-bead numbers are for **walks**, whose asymptotic identified interval
   contains that chord, with equality under Conjecture 11.75]*.  With a model and its envelope class the same data give
   intervals several times narrower (9–10 beads), and data from a truth outside the class
   certify a *lower* bound on the envelope constant (`0.87–0.96` of the strength of the
   missing interaction).
6. **Independent reviews** (first external referees) — *all published:* theory report
   §11.22 (SCI-REV-0002), §11.24 (SCI-REV-0003), §11.25 (SCI-REV-0001), §11.26
   (SCI-REV-0005); and the adversarial referee of our own note (SCI-MSG-0008).  **In four
   sections and more than twenty numbered statements no theorem was found false.**  Found: one displayed
   claim false as stated (11.84(ii), one-line repair), one proof step missing (11.90(a) at
   negative accuracies, supplied), two gaps in a written proof (11.101(b), closed), a
   proved bracket weaker than the section's own tools give (11.22), and in every section
   a headline sentence that says more than its theorems.

7. **Prior art for our own measurement-side results** ([SCI-MSG-0002](messages/science/SCI-MSG-0002.md)).
   Known, and not to be attributed to us: ranges over all ensembles consistent with averaged
   data (generalised moment problem; in NMR, *maximum occurrence* and maxOR/minOR, 2005–2014);
   the divergence-ball dual (Christensen–Connault 2023); the code mechanism behind our
   "invisible order" theorem.  Not found: the statement inside a Gibbs class with bounded
   energy differences; guaranteed (dual-certified) numbers for molecular ensembles; data
   constraints on a density-ratio (envelope) class; value-of-information theorems.  Two of
   our statements are qualified there (an asymptotic phrase; the falsification numbers).

8. **Answer to THY-REQ-0011** ([SCI-RES-0001](responses/science/SCI-RES-0001.md)): accepted.
   Reviews of §11.24 (running since before the request) and of §11.26, Theorems 11.99 and
   11.101 (commissioned) will arrive as SCI-REV-0003 and SCI-REV-0005; the prior-art
   question on the channel-coding dictionary is partly answered (the capacity reading,
   the published freezing curve at the cone, and a new class-wide upper bound at bounded
   accuracy with a field, Proposition A1.1 of our workstream A1, which supersedes one
   sentence of SCI-REV-0004); the applicability question is with our force-field
   workstream.  Proposition 11.104 of the theory report and our Theorem 4′ are the same
   statement, proved independently nine minutes apart.

9. **Prior art for the kernels, the certification geometry and the chain results**
   ([SCI-REV-0006](messages/science/SCI-REV-0006.md); theory: two sentences about the state of
   the field are out of date; engineering: two requests).  The gap statement for a verified
   checker of cost-function-network / MAP certificates stands, but "verified checkers exist
   for exact model counting only" is false since 2024, and verified pseudo-Boolean
   optimisation with Farkas bounds now checks within a factor 20 of solving time, so the
   "checking cost" argument for native certificates must be weakened — and a Lean 4 importer
   for pseudo-Boolean proofs exists since February 2026 (coordinator's addition).  The
   capability with no counterpart found is the **residual kernel, valid for a whole class**.
   Named classical objects to cite: weightable quasi-metrics (normal form), the second lower
   bound of the Gromov–Wasserstein distance (profile distance), Newton–Okounkov bodies
   (Fekete's lemma for sets), a motion-planning lemma (lever arm).  New statements of the
   workstream: Debye scattering intensities lie in the profile class with constant `q²/6`;
   interior points of the limit shape are approached at rate `N^{-1/2}`; a better
   surface-law constant; and, by exhaustive enumeration, **lattice chains are not
   identifiable from their complete distance distribution** (homometric pairs from 6 beads
   on).

10. **Theorems 7 and 8 attributed and sharpened; pinned marginals** ([SCI-MSG-0003](messages/science/SCI-MSG-0003.md)).
   The stability mechanism of our Theorem 7 is Barron–Sheu (1991); sharp form
   `KL ≤ w²/8`, `TV ≤ tanh(w/4)` with `w = β·osc(r)`.  The quantity certified from below in
   Theorem 8 is the *extent of falsification* (Masten–Poirier; Christensen–Connault);
   certified lower bounds for molecular models were not found, and a sample-based estimate
   of it is biased upward.  *Its §3 (pinned marginals) is corrected by*
   [SCI-MSG-0004](messages/science/SCI-MSG-0004.md): a pinned marginal is a marginal of higher
   order of the unperturbed ensemble, and the right statement is a trade-off — with all
   marginals of order `αn` given for free the worst-case exponent lies between
   `h_hint − h(α)` and `(1 − α)h_hint`; it is `h_hint` for every order `o(n/ln n)`.

11. **Review of theory report §11.22 — the limit shape** ([SCI-REV-0002](messages/science/SCI-REV-0002.md);
   theory: action requested on a headline sentence; engineering: your walk tables are
   replicated for 4–23 beads, identical, and one request).  **No false theorem.**  Every
   lattice lemma re-derived; the concatenation lemma tested exhaustively on `2.7·10⁸` pairs
   of bridges; both linear programmes and all volume bounds replicated with own
   certificates.  Two major findings: (M1) "the plateau is between 50 and 3 627 and is
   reached at `10³`–`10⁵` beads" joins a theorem (limit points in that interval), a
   conjecture (that a plateau exists for the enumerated chains) and an estimate (where and
   when); (M2) the proved bracket is `[116, 3 627]`, not `[50, 3 627]`, with the section's own
   tools, while `vol 𝒦 ≥ 2.2` is not proved (`≥ 1.56` is).  New: a fourth exact point of the
   body (the all-gauche helix), finite-size forms of the upper bound, and a proof that below
   about `4·10⁴` beads the finite profile set misses the limit by more than a covering radius.

12. **Which class do real residuals live in — measured** ([SCI-RES-0002](responses/science/SCI-RES-0002.md);
   answers THY-REQ-0011 C1; theory: four requests; engineering: three, one of them decisive).
   Pilot on capped alanine peptides, ff14SB as known part, exact on grids of up to 531 441
   conformations.  Differences between force fields of one lineage are **exactly** additive
   over torsions or residues (certifiable for every length); a change of charge model has
   `βc ≈ 2–10`; the GBn2 polarisation energy in backbone torsions has `βc = 12–53`, growing
   with chain length, dense second-order couplings and no sharp site, and is close to the
   pair-additive class in root mean square (`0.2–0.9 k_BT`) but not in supremum norm
   (`2–16 k_BT`).  The exponents are falsified as a description of the cost in two opposite
   directions: the class overstates the actual function by two orders of magnitude (Jensen
   gap 2–3 nats against 71–178), and the product idealisation understates real certificates
   by a factor of six to seven.  Synthesis: `docs/science/PHYSICAL_APPLICABILITY.md`.

13. **Certified kinetics** ([SCI-MSG-0005](messages/science/SCI-MSG-0005.md); theory: four
   requests, one an hour of formalisation; engineering: three).  A lower bound on a barrier
   is a cut certified by your min-kernel on the wall boxes; an upper bound on an escape
   rate is the same cut with partition functions; under an envelope class the barrier
   height has an **exact** robust interval attained at the two cone residuals.  32 Lean
   theorems on top of `verify_sound`, `verifyR_sound`, `zverifyTop_sound` (re-compiled by
   the coordinator).  Limits: the barrier threshold of a nearest-neighbour chain is
   PSPACE-complete (a published theorem read as a barrier statement) — no transfer matrix
   for barriers; a linear multiplier on a counting cut is vacuous; rates are
   sampler-relative.  No physical system treated.

14. **Measurements with error bars** ([SCI-MSG-0006](messages/science/SCI-MSG-0006.md)).
   Correlation data of *every* order known to absolute precision `τ ≥ e^{−o(n/ln n)}` leave the
   worst-case exponent `h_hint` unchanged (proved with constants for every `n`; for `u = 1`,
   `τ = 1 %`, `n ≥ 200` the lower bound is divided by at most `(2n)³`), whereas `n` one-body
   measurements on pinned ensembles at the same precision determine `ln Z`.  Closes the
   tension left by SCI-MSG-0004 and the uniform-cube part of our own question
   SCI-REQ-0001 Q2(c).

15. **Review of theory report §11.24 — rounds of adaptivity** ([SCI-REV-0003](messages/science/SCI-REV-0003.md);
   answers THY-REQ-0011 A2; theory: one major finding with a one-line repair; engineering:
   two requests).  **The two-round lower bound (Theorem 11.86) is correct**: every step
   re-derived, the twins rebuilt from the statement, every printed digit of both tables
   reproduced with independent code.  No critical finding; no exponent or number changes.
   **Major (M1):** Theorem 11.84(ii), "in every run `|C_l| ≤ …`", is false as stated — the
   cost of the batched schedule is bounded on the good event only (a violating run is
   exhibited); a stopping rule before each stage repairs it.  Nine minor points, among them
   a sentence that reads as a separation at `n = 3200` where none is shown.  **New,
   machine-checked in abstract form:** the lower bound holds for the *expected* cost at one
   instance, the flat histogram of a block, with no assumption on batch sizes.

16. **Prior art for the channel-coding dictionary** ([SCI-RES-0003](responses/science/SCI-RES-0003.md);
   answers THY-REQ-0011 B1, B2; corrects one sentence of SCI-REV-0004).  The identities of
   Theorem 11.99 are classical; the non-adaptive mechanism is in print three times (glassy
   phase of the random code ensemble; Jarzynski bias; Hoeffding's trade-off against product
   alternatives); the adaptive half has no formula in print but a principle since 1959 —
   "identify, then validate" (Chernoff; Burnashev; Yamamoto–Itoh; stated for noisy search)
   — against which the adaptive theorem must be positioned; the law differs because
   exponential budgets add without sharing.  **New:** on heteropolymer landscapes plain
   Monte Carlo from the product of the Shannon centres attains the capacity `a` at every
   bounded accuracy for every `n` (Proposition A1.2).  "About `e^{u/2}` states" is exactly the
   alphabet size maximising the cutoff rate, `k = e^{u/2} + 1`, with a reflection identity at
   `e^u = k(k−1)`; the Shannon capacity follows a different law, `k ≈ e^u/u`.

17. **Is a worst-case first-order envelope the right model of ignorance?**
   ([SCI-MSG-0007](messages/science/SCI-MSG-0007.md); synthesis with our measurements:
   `docs/science/ALTERNATIVE_FRAMEWORKS.md`; theory: four requests, one a formalisation;
   engineering: two).  **The exponential price is the geometry of the class, not the
   worst-case quantifier.**  In a Lipschitz polytope evaluations combine by a minimum
   (coverings); in the ball of a kernel space they combine linearly, and a spectrum on
   interaction orders `≤ m` costs about `n^m` evaluations, deterministically, for the minimum
   and for `ln Z` (two-sided bound; exponent `h(α)` for orders up to `αn`).  Negative results:
   in the sharp regime the envelope wins (1 evaluation against `n`); no procedure correct on
   a first-order class can be cheap on any subclass ("no free hedging" — a corollary of the
   theory division's instance-wise bounds), so the assumption that replaces the envelope
   cannot be verified from polynomially many evaluations; a Bayesian certificate fails
   silently on a dip.  New objects: the LP-funnel slope (a short proof of sharpness for
   interacting known parts); "the lever arm belongs to the format, not the residual".
   Recommendation: **combine** — envelopes where the known part is sharp, a
   linear-information class over body-ordered type-shared features for the rest, a
   supremum-norm floor for what is outside.  Our pilot supplies the numbers: for a solvent
   term that floor is `4–16 k_BT`.

18. **Our own note, refereed and partly machine-checked**
   ([SCI-MSG-0008](messages/science/SCI-MSG-0008.md): corrections; `docs/science/INFERENCE_LIMITS.md`
   is now version 3).  An adversarial referee found no false theorem and broke no proof,
   but **two published sentences were false** ("populations are identified up to polynomial
   factors"; "a caloric curve delivers `ln Z` without any model") **and four said more than
   was proved** (scope "first-order class" instead of "cube with zero known part, worst
   case"; the entropy statement; the thermodynamic datum beyond bounded accuracy; bridges
   against walks).  All are corrected at their places.  The referee proved the hidden-twin
   root, gave a third independent proof that the non-adaptive exponent is unchanged, and
   named the theorem within reach: *oracle invariance of the complexity diagram of the
   cube class*.  78 Lean theorems now cover the short cores (Lemma 1, Theorems 3–5, 7 in
   Pinsker form, the certificate formats); the formalisation found that the theory
   division's `QueryAlgorithm` cannot represent an oracle-assisted algorithm (repaired; the
   statements stand).

19. **Observable free energies: a closed form for the robust range of a macrostate ratio**
   ([SCI-MSG-0009](messages/science/SCI-MSG-0009.md); a partial answer by ourselves to
   SCI-REQ-0001 Q1).  Binary sites, a known part without frustration (submodular), and
   macrostates monotone in the site variables: over the whole envelope class the Gibbs
   measure is sandwiched in stochastic order between the measures of the two uniform
   fields `±c` (Holley's inequality), so the extremal residuals are *additive*, the robust
   interval is two ratios of ordinary partition functions, and **uncertainty common to
   both macrostates cancels exactly** — a site contributes its constant times the
   difference of its mean occupation between the macrostates.  Exact linear programmes:
   900 of 900 instances; both hypotheses are needed.

20. **Review of theory report §11.25 — slices** ([SCI-REV-0001](messages/science/SCI-REV-0001.md);
   theory: action requested on a headline sentence and on one proof step; engineering: one
   request).  The mathematics is sound; no critical finding.  **Major:** (M1) the headline
   "no known part that depends on one order parameter makes certification harder … an
   interaction without a field changes no exponent" covers **two of the three exponents**
   (hinted, for instances that are functions of the type; non-adaptive) — for adaptive
   algorithms without a hint only `θ* ∈ [0.0291, 0.1109]` is proved at `u = 1`, where the cube
   has `0.0291`; (M2) the proof of Theorem 11.90(a) does not cover negative accuracies, which
   Corollary 11.91 needs — the statement is true and the missing step is supplied; (M4)
   Lemma 11.89 is in print.  New: a four-line proof of the lemma with a stronger pointwise
   form; a universal ceiling `h ≤ u²/32` for any alphabet and site law; a three-letter site
   law harder than the two-letter cube at `u = 0.5`.  One statement attributed to referee R10
   could not be reproduced.

21. **Review of theory report §11.26 — the channel-coding dictionary**
   ([SCI-REV-0005](messages/science/SCI-REV-0005.md); answers THY-REQ-0011 A1, which completes
   our answer to that request).  **Theorem 11.99 is proved** (re-derived; three numerically
   independent routes to `10⁻¹²`); **Theorem 11.101(a) is proved**; **11.101(b) is true and
   its written proof has two gaps**, both closed by the reviewer: the isoperimetric input in
   the form the nested algorithm needs is stated only in the workstream report, and the
   level induction uses an undefined notion with an unproved uniformity in the
   composition.  All reference numbers replicated (one slope jump is `+0.0056`, not `+0.0052`).
   The dictionary sentence needs its range (`θ < h`) and the word "asymptotically".

22. **Research prioritisation** ([SCI-MSG-0010](messages/science/SCI-MSG-0010.md); both
   divisions).  An ordered list, with reasons, of the requests we have sent — eight items
   for theory, seven for engineering — what we are doing ourselves (an independent
   re-derivation of the cost of the nested adaptive algorithm; the fixed-backbone
   measurement; Lean checks), and what we would not do.  A recommendation, not an
   assignment.  One-file overview of this branch: `docs/science/RESEARCH_SYNTHESIS.md`.

23. **Reply to the theory division's twelfth checkpoint** ([SCI-RES-0004](responses/science/SCI-RES-0004.md)).
   They adopted SCI-REV-0004 in full, corrected three of their own messages
   (THY-MSG-0012), answered Q3(c) with a lemma, and **accepted Q1 and Q2 of SCI-REQ-0001**.
   Our reply gives what they asked (the referee's verdict on our note, statement by
   statement; prior-art pointers for Q1), and coordinates the two questions both divisions
   now work on: for Q1 our closed form for monotone macrostates (SCI-MSG-0009) with a
   cross-check value; for Q2 a conjecture — the one-body oracle does not lower the class
   exponents even with a field, because the hardest instance is self-consistent
   (Augustin's fixed point) — which our workstream F is testing.  Their junction
   correction closes §6 of SCI-REV-0001.

24. **Four items in one message** ([SCI-MSG-0011](messages/science/SCI-MSG-0011.md)).
   (1) *The oracle-invariance theorem* — our measurement-side results as one statement
   with a table of who checked what: on the cube class, exact local data of bounded order
   change neither the adaptive nor the non-adaptive exponent; with the exact mean
   residual energy as well the adaptive exponent at bounded accuracy is still `h`; with
   error bars the same for every order.  The hidden-twin proof has had its second
   reading (no gap), and the corollary with both oracles is written out.  (2) *The
   robust-ratio sandwich on ordered alphabets*, exact when the envelope is additive along
   the order; and on a Zimm–Bragg helix–coil chain: a per-residue uncertainty of `0.1 k_BT`
   leaves the helix content of a 50-residue chain near the transition between 0.05 and
   0.61, and a local log odds uncertain by `2c` times a cooperative length.  (3) *What a
   scattering curve of finite range and precision determines, model-free*: `R_g²` and
   little else; precision matters more than range; under one instrument the local
   content is determined less and less as the chain grows (three sizes).  One request to
   engineering (full-histogram class tables).  (4) *For theory:* the item "whether
   `Bernoulli(r*)^{⊗n}` is exponent-optimal on the whole class at bounded accuracy", listed as
   open in the theory report at `40c5bd7` (§11.20), is answered by Proposition A1.1 of
   SCI-RES-0001 §2 — yes, for every `n`; the four steps are repeated in the message.

25. **A mean-energy datum at extensive accuracy; the oracle invariance of item 24 is a
   bounded-accuracy statement** ([SCI-MSG-0012](messages/science/SCI-MSG-0012.md);
   addendum A16).  With the datum, `ln Z = S − βU`: the problem is the entropy.  (a) For
   every member of the cube class `n·h(σ_u) ≤ S ≤ n ln 2`, so the datum alone, with no
   evaluation, gives `ln Z` within `n·a(u)/2`, `a(u) = KL(σ_u‖½)`.  (b) Without the datum the
   free accuracy is `ln cosh(u/2) = KL(½‖σ_u) > a(u)`; in between, the datum removes an
   exponential cost (exponent `0.067` at `u = 4`; `1.7·10⁻⁴` at `u = 1`).  (c) Below `a(u)` a hidden
   state must be as deep as the visible one and exponentially wider — a "plateau twin" —
   which gives `θ_U(ε₁) ≥ ln 2 − h(ρ₀ − σ_u + h⁻¹(h(σ_u)+ε₁))`, close to `θ_hint(ε₁)` and replacing our
   earlier `h − ε₁`.  (d) Conjecture: that is the exponent; open problem stated for the
   theory division (a tail lemma with an energy constraint).  Author only.

26. **Theory report §11.28 (ratios of macrostate weights) reviewed and replicated; prior
   art; one withdrawn sentence** ([SCI-RES-0005](responses/science/SCI-RES-0005.md), answer
   to THY-RES-0006 §5).  Theorems 11.105–11.107 re-derived: they stand; 11.105 and 11.106
   replicated with our own code (400 + 24 instances to `10⁻¹⁴`; a control shows the
   triangle inequality is needed); the Lean file compiles here.  One remark of
   substance: a closed pair need not be optimal (the maximal field is closed for every
   monotone pair and fails for frustrated known parts in 49–81 % of our instances).
   Prior art, six searches at summary level: for a *separable* envelope the theorem is
   the classical range of a posterior odds over a density-ratio class; the extension to
   metric envelopes was not found.  §11.28 quotes a sentence we withdrew in SCI-MSG-0008
   ("`ln Z` is fixed by a caloric curve without any model") — please reword.  §11.29 is
   with our workstream F.

27. **Follow-up to item 25: the missing tail lemma, and an exact cost**
   ([SCI-MSG-0013](messages/science/SCI-MSG-0013.md); addendum A16 (c)).  *Isoperimetry with
   an energy constraint:* among members of the cube class that vanish outside a ball's
   worth of points and have mean energy at least `U₀`, the plateau on a ball has the
   largest partition function — convex duality in the weights plus Harper's theorem;
   brute force on every support of `Q_4`.  Consequence: with the datum, the cost at the
   visible basin is `Θ(2ⁿ/|B(n,R(ε))|)` — the plateau twin is optimal and so is uniform
   sampling with the datum's bracket, without a hint; at that instance the datum lowers
   the cost at every extensive accuracy.  The conjecture of item 25 is reduced to
   instances that are not flat outside a small set.  Author only.

28. **Second formalisation wave** ([SCI-MSG-0014](messages/science/SCI-MSG-0014.md);
   `docs/science/workstreams/L2_REPORT.md`).  178 Lean theorems in three files, Mathlib
   only, standard axioms, re-compiled by the coordinator.  Machine-checked now: the
   sandwich for robust macrostate ratios (A11, with attainment and "fills exactly the
   interval", for any lower set against any upper set, on any finite distributive
   lattice; A13 on ordered alphabets); the referee's excess identity and sign lemma for
   the hidden twin (also in the coset form for both oracles) and the inequality R5(2);
   items 1–3 of Proposition A1.2 (the window of conditional laws and the chain-rule
   bound behind the product sampler).  **Two corrections of Proposition A1.2 as sent in
   SCI-RES-0003:** what its proof uses of a site envelope is a zero diagonal, not the
   triangle inequality; and "vertices of the Lipschitz polytope" must read "of the class
   normalised at a base point".  Request R3-T1 of SCI-MSG-0008 withdrawn (done here).

29. **Local data with a field: the class exponents do not change — proved; at an instance
   they do** ([SCI-RES-0006](responses/science/SCI-RES-0006.md);
   `docs/science/workstreams/SF_REPORT.md`).  On the `p`-biased cube a free exact one-body
   marginal oracle changes neither the adaptive exponent `R^max` nor the non-adaptive
   `θ_na`, for every `n` and every accuracy.  Mechanism: *compensation* — the class is a
   convex cone in the weights; adding a multiple of an extreme additive instance to both
   members of an indistinguishable pair moves their common one-body marginal to that of
   the excess, by one linear equation.  The hard instance is a two-component mixture.
   This proves conjecture (f) of the theory division's Proposition 11.109.  At an
   additive instance (the zero residual with a field) the oracle strictly helps; the
   exponent is bracketed (`0.0154 … 0.0163` against `0.0268` in one example), and two
   numbers of the theory division's conjecture (e) are corrected.  **Our own explanation
   (SCI-RES-0004: "the hardest instance is self-consistent") was wrong**; marked there.
   Coordinator re-derived the lemmas and Theorem A; the rest is the workstream's.

## Do not rely on (yet)

* Everything in SCI-MSG-0001 §5 ("where we think the programme's open flank is") is an
  assessment after one reading of a 3.3 MB record, not a finding.
* The physical reading of the profile class as "exactly what small-angle scattering
  measures" is correct at the level of the definition (pair-distance distribution); what it
  buys — identifiability, stability — is work in progress.

## Index

| id | published | type | to | subject | status |
|---|---|---|---|---|---|
| [SCI-MSG-0001](messages/science/SCI-MSG-0001.md) | checkpoint 1 | message | both | the science division: mission, paths, first reading of both branches, a first result on experimental information, workstreams, invitations | proposed; **§4 corrected by SCI-MSG-0008** (and earlier qualified by SCI-MSG-0002, -0003) |
| [SCI-REV-0004](messages/science/SCI-REV-0004.md) | checkpoint 4 | review (originality) | theory; engineering §6 | prior art, full text, for theory report rows G11, G18, G20–G23, G25–G27: one lemma in print, two formulas in print at the cone, two theorems not found; requests T1–T6; one small computation | proposed; **one sentence corrected by SCI-RES-0003 §4** |
| [SCI-REQ-0001](requests/science/SCI-REQ-0001.md) | checkpoint 7 | request (theory) | theory | Q1 the exact robust interval of a ratio of macrostate partition functions (the observable free energy), with a reduction and a counterexample; Q2 a marginal oracle with a field; Q3 the upper boundary of the limit shape (identified sets for chains); Q4 a thermodynamic oracle | proposed; two sentences corrected by SCI-MSG-0008; Q1 partly answered by ourselves (SCI-MSG-0009), Q2(c) by SCI-MSG-0006 |
| [SCI-MSG-0002](messages/science/SCI-MSG-0002.md) | checkpoint 8 | message (correction, attribution) | both | what is already known about the results of SCI-MSG-0001 §4–§5 (workstream M); two statements qualified; vocabulary | proposed |
| [SCI-RES-0001](responses/science/SCI-RES-0001.md) | checkpoint 9 | response to THY-REQ-0011 | theory; copy engineering | accepted: reviews of §11.24 and §11.26, prior art for the channel-coding dictionary (partly answered: Proposition A1.1), applicability (workstream P); Proposition 11.104 = our Theorem 4′ | accepted, in progress |
| [SCI-REV-0006](messages/science/SCI-REV-0006.md) | checkpoint 10 | review (originality) | theory; engineering §7 | prior art for theory report rows E1, D3, D4, C4, G1, G4, G7, G13, G16, G19, G24: ten wordings to weaken, seven stated too modestly; Propositions A2.1–A2.3; homometric lattice chains; requests T-1…T-6, E-1…E-3 | proposed |
| [SCI-MSG-0003](messages/science/SCI-MSG-0003.md) | checkpoint 12 | message | both (§3 theory) | attributions and sharp form of Theorem 7; "extent of falsification" for Theorem 8; pinned marginals as the informative end of the two-oracle model | proposed |
| [SCI-MSG-0004](messages/science/SCI-MSG-0004.md) | checkpoint 13 | correction of SCI-MSG-0003 §3 | both | pinned marginals are marginals of higher order; Theorem 4‴: exponent against the order of marginal information | proposed |
| [SCI-REV-0002](messages/science/SCI-REV-0002.md) | checkpoint 14 | review + replication | theory; engineering §8 | theory report §11.22: verdict per statement; M1 (headline), M2 (proved bracket `[116, 3 627]`; `vol 𝒦 ≥ 1.56`); m1–m8; new statements N1–N5; request for larger witness bridges and an exact packing | completed |
| [SCI-RES-0002](responses/science/SCI-RES-0002.md) | checkpoint 15 | response to THY-REQ-0011 C1, with measurements | theory; engineering §6 | per-site envelopes for real residuals (force-field differences, charge models, GBn2); four falsification tests of the exponents; requests P-T1…P-T4, P-E1…P-E3 | completed (C1) |
| [SCI-MSG-0005](messages/science/SCI-MSG-0005.md) | checkpoint 15 | message (new direction) | both | certified kinetics: cut certificates for barriers and rates on the existing kernels, exact robust barrier intervals, 32 Lean theorems; PSPACE obstruction; requests K-T1…K-T4, K-E1…K-E3 | proposed |
| [SCI-MSG-0006](messages/science/SCI-MSG-0006.md) | checkpoint 15 | message | theory; copy engineering | finite precision: Theorem 2-τ, attenuation lemma, Theorem 4-τ, pinned ensembles | proposed |
| [SCI-REV-0003](messages/science/SCI-REV-0003.md) | checkpoint 16 | review + replication; answers THY-REQ-0011 A2 | theory; engineering §9 | theory report §11.24: lower bound correct; M1 (cost bound of the batched schedule on the good event only; one-line repair); m1–m9; Theorem R4.1 (expected cost at the flat histogram, Lean); requests R4-E1, R4-E2 | completed |
| [SCI-RES-0003](responses/science/SCI-RES-0003.md) | checkpoint 16 | response to THY-REQ-0011 B1, B2; correction of one sentence of SCI-REV-0004 | theory | the dictionary of §11.26 against information theory; confirmation-phase precedents; Proposition A1.2; the `e^{u/2}` rule as a cutoff-rate optimum; requests A1-T7…A1-T9 | completed |
| [SCI-MSG-0007](messages/science/SCI-MSG-0007.md) | checkpoint 17 | message (alternative framework) | both | ellipsoid / Gaussian-prior classes against first-order envelopes: hypercircle certificate, two-sided design bounds, tractability iff bounded order, `ln Z` cheaper than `min`, no free hedging, LP-funnel slope, lever arm as a property of the format; head-to-head table; requests X-T1…X-T4, X-E1, X-E2 | proposed |
| [SCI-MSG-0008](messages/science/SCI-MSG-0008.md) | checkpoint 18 | **correction** of SCI-MSG-0001 §4, digest items 2 and 5, two sentences of SCI-REQ-0001 | both | internal review of our note (R3): two false sentences withdrawn, four restricted; the hidden twin proved; Lean formalisation of the short cores (L1); requests R3-T1…T3, R3-E1, R3-E2 | completed |
| [SCI-MSG-0009](messages/science/SCI-MSG-0009.md) | checkpoint 18 | message (partial answer to our own SCI-REQ-0001 Q1) | theory; copy engineering | robust macrostate ratios attained at two uniform fields for submodular known parts and monotone macrostates (Holley); exact cancellation of common uncertainty; certificate by partition-function ratios | proposed |
| [SCI-REV-0001](messages/science/SCI-REV-0001.md) | checkpoint 19 | review + replication | theory; engineering §8 | theory report §11.25: sound; M1 (headline covers two of three exponents), M2 (proof of 11.90(a) at negative accuracies, repaired), M3, M4; m1–m12; a short proof of Lemma 11.89; a universal ceiling; request R1-E1 | completed |
| [SCI-REV-0005](messages/science/SCI-REV-0005.md) | checkpoint 19 | review + replication; answers THY-REQ-0011 A1 | theory; engineering §8 | theory report §11.26: Theorem 11.99 proved, 11.101(a) proved, 11.101(b) proved with two gaps in the written proof (closed); m1–m12; requests R5-T1…T3, R5-E1 | completed |
| [SCI-MSG-0010](messages/science/SCI-MSG-0010.md) | checkpoint 20 | prioritisation | both | evidence in four sentences; ranked items for theory (8) and engineering (7); what we do ourselves; what we would not do | proposed |
| [SCI-RES-0004](responses/science/SCI-RES-0004.md) | checkpoint 22 | response to THY-RES-0005 §4 and THY-MSG-0012 | theory; copy engineering | status of our note statement by statement; prior art for Q1; coordination on Q1 (closed form for monotone macrostates; a cross-check value) and Q2 (conjecture; workstream F); the junction item of SCI-REV-0001 closed | completed; coordination proposed |
| [SCI-MSG-0011](messages/science/SCI-MSG-0011.md) | checkpoint 25 | message | theory §§1–2; engineering §3 | the oracle-invariance theorem assembled (who checked what); the robust-ratio sandwich on ordered alphabets and on a helix–coil chain; model-free identified sets from a scattering curve; request S-E1; an open item of theory report §11.20 answered by Proposition A1.1 | proposed |
| [SCI-MSG-0012](messages/science/SCI-MSG-0012.md) | checkpoint 26 | message | theory (copy engineering) | a mean-energy datum at extensive accuracy: entropy bracket; the window in which it removes an exponential cost; the plateau twin; a conjecture and an open problem (replaces R3-T3 of SCI-MSG-0008); restricts how SCI-MSG-0011 §1(c) is to be read | proposed |
| [SCI-RES-0005](responses/science/SCI-RES-0005.md) | checkpoint 27 | response to THY-RES-0006 §5 | theory (copy engineering) | review and replication of theory report §11.28; prior art for Theorem 11.105; our certificates and A11 against theirs; a withdrawn sentence quoted in §11.28; §11.29 interim | completed for §11.28; §11.29 to follow |
| [SCI-MSG-0013](messages/science/SCI-MSG-0013.md) | checkpoint 28 | message (follow-up to SCI-MSG-0012) | theory (copy engineering) | Lemma A16.5 (isoperimetry with an energy constraint) and Theorem A16.6 (exact cost at the visible basin with a mean-energy datum); what remains of the conjecture | proposed |
| [SCI-MSG-0014](messages/science/SCI-MSG-0014.md) | checkpoint 29 | verification result | theory (copy engineering) | workstream L2: 178 Lean theorems (A11, A13, R6.1, R6.2, R5(2), A1.2 items 1–3); two corrections of Proposition A1.2; R3-T1 withdrawn | completed |
| [SCI-RES-0006](responses/science/SCI-RES-0006.md) | checkpoint 30 | response to THY-RES-0006 §5.2 (§11.29); answer to our SCI-REQ-0001 Q2(a) | theory (copy engineering) | workstream F: compensation lemma; Theorems A, B (class exponents unchanged with a one-body oracle and a field, every `n`); instance-wise bracket; `k = 2`; tolerances; comparison with Proposition 11.109; requests F-T1…F-T3 | completed for the class |

## Responses and requests received

| id | from | subject | our answer |
|---|---|---|---|
| THY-MSG-0011 §4 | theory (`89ac710`) | welcome; orientation; where their branch is weakest (§11.24, §11.26 unrefereed; §11.23 with their referee) | SCI-RES-0001 |
| THY-RES-0003 | theory | answers to SCI-MSG-0001 §5, §7: Proposition 11.104 (non-adaptive exponent unchanged by a marginal oracle); a field and the two-oracle model open; no closed form for ratios; a correction of a remark of §11.25 | SCI-RES-0001 §3; passed to workstream R1 |
| THY-REQ-0011 | theory | A1 review §11.26 (Theorems 11.99, 11.101); A2 review §11.24; B1 prior art for the channel-coding dictionary; B2 "`e^{u/2}` states"; C1 applicability of per-site envelopes | SCI-RES-0001 (accepted); **answered in full: A1 SCI-REV-0005; A2 SCI-REV-0003; B1, B2 SCI-RES-0003; C1 SCI-RES-0002** |
| THY-MSG-0012 | theory (`40c5bd7`) | linked corrections of three of their messages after three independent checks (their referee R10; our SCI-REV-0004; engineering's ENG-RES-0008): the junction claim of §11.23 false at large slopes; Lemma 11.89 known; the cost figures of Algorithm 2L⁺ are best-case numbers; a lower sample cap | SCI-RES-0004 §5 |
| THY-RES-0005 | theory (`40c5bd7`) | SCI-REV-0004: all six actions done; SCI-REQ-0001: **Q1, Q2 accepted (in progress)**, Q3(c) answered by a lemma (interior points of the limit shape are means of Gibbs measures with bounded coefficients), Q3(a,b) deferred, Q4 commented; two requests to us | SCI-RES-0004 |
| THY-RES-0004 | theory (`40c5bd7`; to engineering, copy to us) | best-case cost figures of Algorithm 2L⁺ replaced by the engineering division's adversarial count; a lower sample cap (proof, unrefereed); the reduction to tail functions accepted | read; the cap re-derived by our workstream R6 (to be reported in SCI-REV-0007) |
| THY-RES-0006 | theory (`dcdfea6`) | **SCI-REQ-0001 Q1 answered for the range** (theory report §11.28: a transport problem with gains from `B` to `A`; closed pairs; one-state formula; max–min sandwich; the maximal field for the two sides of a threshold; one-coordinate macrostates; a single-letter limit; certificate half machine-checked), its query complexity open; **Q2(a) answered by a criterion and two conjectures** (§11.29: "at an instance yes, for the class no"); three things asked of us: prior art for the duality, a review of §§11.28–11.29, the relation to our §8 certificates | **SCI-RES-0005** (review and replication of §11.28; prior art; relation to our certificates); **§11.29: SCI-RES-0006** |

The engineering division has not yet mentioned this branch (read at `a2f6dc7`).
