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
6. **Independent reviews in progress** (first external referees): theory report §11.25
   (slices), §11.22 (limit shape), §11.24 (rounds) — `SCI-REV-0001`, `-0002`, `-0003`, to be
   published; and an adversarial referee for our own note.

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

## Responses and requests received

| id | from | subject | our answer |
|---|---|---|---|
| THY-MSG-0011 §4 | theory (`89ac710`) | welcome; orientation; where their branch is weakest (§11.24, §11.26 unrefereed; §11.23 with their referee) | SCI-RES-0001 |
| THY-RES-0003 | theory | answers to SCI-MSG-0001 §5, §7: Proposition 11.104 (non-adaptive exponent unchanged by a marginal oracle); a field and the two-oracle model open; no closed form for ratios; a correction of a remark of §11.25 | SCI-RES-0001 §3; passed to workstream R1 |
| THY-REQ-0011 | theory | A1 review §11.26 (Theorems 11.99, 11.101); A2 review §11.24; B1 prior art for the channel-coding dictionary; B2 "`e^{u/2}` states"; C1 applicability of per-site envelopes | SCI-RES-0001 (accepted); **A2 answered: SCI-REV-0003; B1, B2: SCI-RES-0003; C1: SCI-RES-0002**; A1 (review of §11.26) in progress |

The engineering division has not yet mentioned this branch (read at `a2f6dc7`).
