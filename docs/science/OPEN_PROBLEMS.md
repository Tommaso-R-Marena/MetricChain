# Open problems — science division

*Version 3 (2026-11-25; versions 1 and 2 at checkpoints 14 and 15).  Problems that this division has made precise, with what is known
and who is best placed to attack them.  Items already listed by the theory division
(theory report §12) are not repeated unless we add something.  "Sent" refers to a
published request.*

## A. Measurement as information (the two-oracle model)

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| A1 | **The exponent against the order of marginal information.**  Cube class, zero known part, all marginals of order `αn` free: the worst-case exponent `θ(α)` | `h_hint − h(α) ≤ θ(α) ≤ (1 − α)h_hint`; `θ = h_hint` for order `o(n/ln n)` (addenda A8) | — | theory |
| A2 | **A marginal oracle with a field** (no translation symmetry).  Is the exponent with a one-body marginal oracle the hinted exponent restricted to centres of the type forced by `τ(1−δ) + (1−τ)δ = p`, and is it strictly below `R^max`? | uniform cube: no exponent changes (Theorem 4; Theorem 4′ = theory's Proposition 11.104).  Theory's pointer: designs in the Johnson scheme inside one type class | SCI-REQ-0001 Q2 | theory |
| A3 | ~~**Finite precision, rigorously.**~~  **Settled for `τ ≥ e^{−o(n/ln n)}`** (addenda A10: attenuation lemma, Theorem 4-τ; SCI-MSG-0006).  What remains: tolerance `e^{−γn}` (then the relevant order is proportional to `n` and the question merges with A1); random instead of adversarial errors; **what a sampler is worth to the class** (the hard family of Theorem 4-τ is easy against samples) | additive form `|S_j/S_0 − tanh(u/2)^j| ≤ 2ξ/(1−ξ)`, `ξ` exponentially small | SCI-MSG-0006 | us; theory |
| A4 | **The hidden twin.**  ~~Existence of the root~~ — **proved by our referee** (R3 report, R6: excess identity, sign lemma, overlap bound; a second full reading and a machine check of three finite inequalities owed).  Open: the exponent with a mean-energy oracle at **extensive** accuracy (between `ln 2 − h(ρ₀) − ε₁` and `θ_hint(ε₁)`); the instance-wise cost | exact sums to `n = 5000`; proof for every `u > 0` and large `n` | SCI-REQ-0001 Q4; SCI-MSG-0008 R3-T1, R3-T3 | theory |
| A5 | **Exchange rate in mixed classes.**  `g = λ·Φ + r`, `r` first-order with constant `c`: how many evaluations does exact `Φ`-data save, as a function of `βc`? | ends: linear classes (rank-many of either kind); first-order classes (nothing) | SCI-MSG-0001 §7 | theory + us |
| A6 | **Perturbed ensembles.**  A model of measurements on pinned or biased ensembles with absolute precision: how many pinned sites are needed before the exponent drops? | `n` pinned one-body marginals give `ln Z` to `O(nτ)` (Proposition 4″-τ); nothing in between | — | us |

## B. Targets that can be measured

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| B1 | **The exact robust interval of a ratio of macrostate partition functions** over an envelope class.  **Solved for binary sites, submodular known parts and monotone macrostates** (addendum A11; SCI-MSG-0009): the extremal residuals are the two uniform fields, and common uncertainty cancels.  Open: frustrated known parts (the field fails in most random instances); non-monotone macrostates; unordered alphabets; the range given evaluations | reduction to a programme on one state (A3); three-point counterexample; the Holley sandwich (A11) | SCI-REQ-0001 Q1; SCI-MSG-0009 | theory; us |
| B2 | **Query complexity of certifying a ratio** with a hint — the counterpart of theory report Theorem 11.25 for an observable free energy | theory: "sum of the two thresholds (no cancellation)" for uncoupled macrostates | SCI-REQ-0001 Q1(c) | theory |
| B3 | **Flows with gains.**  Families of dual flows on product spaces for which the certificate inequality of `INFERENCE_LIMITS.md` §8 is checkable by a pairwise kernel | soundness proved; exact programmes to 10 beads; an outer bound through a divergence ball (addenda A4) | SCI-REQ-0001 (frontier map §4) | theory + engineering |

## C. Identified sets for chains

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| C1 | **The upper boundary `γ⁺` of the limit shape** and the chord at the athermal point: the asymptotic model-free identified interval of the gauche fraction given the mean profile | finite sizes: 0.14 → 0.65 between 7 and 27 beads, increasing; interior convergence at rate `N^{-1/2}` (A2.2) | SCI-REQ-0001 Q3 | theory |
| C2 | **Is the limit shape a Newton–Okounkov body?**  Can the concatenation error of the bridge lemma be made constant?  Then the number of attained profiles grows like `vol(𝒦)·N³` | prediction stated; plausibility check on the 27-bead count (A2 report §6) | SCI-REV-0006 T-4 | theory + engineering |
| C3 | **Identifiability of a chain from its distance distribution.**  (a) generic chains with fixed bond lengths: injective modulo isometries and reversal on a dense open set?  (b) does the homometric fraction on the cubic lattice have a positive limit?  (c) with a cutoff: the group of torsion re-orderings that preserve the contact framework | counterexamples from 6 beads on; 19 % of 9-bead site sets on the cubic lattice (A2.6); Boutin–Kemper does not apply to chains | SCI-REV-0006 E-2 | engineering (b); open (a), (c) |
| C4 | **Identified sets from a finite scattering curve.**  **First results (addendum A15):** exact model-free intervals as functions of the number of Shannon channels and of the tolerance, 11–15 beads — a curve fixes `R_g²` and little else; precision matters more than range; a compact-state population is bounded above only; under one instrument the unidentified part of a local observable (gauche fraction) grows with the chain at three sizes (0.47, 0.57, 0.62 with exact data).  Open: whether that fraction tends to one; larger chains (needs the engineering tables with full histograms, or a column-generation LP); a noise model instead of a hard tolerance band; form factors and contrast; the same with a model and its envelope class | full histogram and `R_g²` done to 15 beads; Debye intensities are in the profile class (A2.1); A15 | — | us; engineering for sizes |
| C5 | **Scaling of the combined interval** (model + envelope class + data) with chain length at fixed `b` | 8–10 beads: roughly constant for intensive targets (0.085, 0.094, 0.098 for the gauche fraction at `b = 1`) | — | us + engineering |

## D. The class question

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| D1 | **Which class does a real residual live in?**  **Pilot done** (SCI-RES-0002): same-lineage differences exactly additive / residue-local; charge models `βc ≈ 2–10`; GBn2 in backbone torsions `βc = 12–53`, near the pair-additive class in RMS only.  Open: (a) the same constants in **rotamer variables on a fixed backbone** — the setting in which the known part is pairwise; (b) asymptotics of the constants with chain length; (c) any certified *upper* bound for a many-body term; (d) relaxed geometry, side chains, Poisson–Boltzmann, quantum and learned residuals | exact on grids to 6 and 9 residues of alanine | SCI-RES-0002 P-E1 | engineering (a); us (b–d) |
| D2 | **A model of ignorance that is not worst-case**, with a tractability theorem for a physically plausible class | workstream X running | — | us |
| D3 | **Does a certified lower bound on model error stay informative for long chains?**  Is `b_min ≈ ε` a theorem for contact residuals? | `b_min/ε = 0.87, 0.96, 1.07` at 8, 9, 10 beads | — | us |
| D4 | **A class with known features and an analytic remainder.**  `g = θ⁰·F + ρ`, `F` and `θ⁰` known, `|ρ(x)| ≤ Σ_p K_p u_p(x)²` with known `u_p`: certificate cost; and the bound itself for the generalized-Born energy (second derivatives in the inverse Born radii, interval arithmetic over a cell) | structure found numerically in the pilot (`SP_REPORT.md` §3.4): first-order response in the Born radii leaves RMS 0.1–0.5 kcal/mol | SCI-RES-0002 P-T2 | theory (cost); us or engineering (the bound) |
| D5 | **A certified typical-norm remainder.**  For `ln Z`, `\|ln Z(f+g) − ln Z(f+ĝ)\| ≤ ln E_π e^{β\|g−ĝ\|}`: what must be certified, and can an exponential moment be bounded from samples with a guarantee? | sup/RMS is 4–8 for the measured residuals; Jensen gap 2–3 nats against a class bound of 71–178 | SCI-RES-0002 P-T3 | theory + us (workstream X) |

## E. Verification

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| E1 | **An independent line-by-line check of the cost of the nested adaptive algorithm** (theory report Theorems 11.52, 11.56) | two internal referees; engineering: no violation in `7·10⁶` mean runs | `PUBLICATION_OPPORTUNITIES.md` §1 | outside reader; or us in a later session |
| E2 | **Native certificates against pseudo-Boolean proofs** — size and checking time on the same runs | unmeasured | SCI-REV-0006 E-1 | engineering |
| E3 | **Is there a rigorous dual bracketing of generalised moment problems in robust Bayes** (Betrò; Betrò–Guglielmi) that would be a precedent for kernel-checkable identified sets? | texts not accessible to us | — | anyone with library access |
| E4 | **Machine-checking our own statements.**  Done for the short cores (workstream L1: Lemma 1, Theorem 3 in Markov form, Theorems 4, 4′, 5, 7 in Pinsker form, Propositions 6 and 9, the certificate formats, Pinsker's inequality).  Open: Theorem 2 (needs the entropy chain rule); the Krawtchouk form of Theorem 3; codes for `k ≥ 2`; the sharp Theorem 7; the referee's R5(2), R6.1, R6.2; **A11** (Mathlib has Holley's inequality as a consequence of the four-functions theorem — a short formalisation is plausible); Proposition A1.2 | 78 theorems | SCI-MSG-0008 R3-T1 | us; theory |

## F. Kinetics (workstream K; `workstreams/SK_REPORT.md` §5)

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| F1 | **Approximability of the barrier of a nearest-neighbour chain** (additive error `ε·max|J|`); hardness for binary chains or generic energies | exact threshold PSPACE-complete with barrier values in `{0,1}` (Wrochna's theorem) | — | theory; open |
| F2 | **Query-complexity exponent of barrier certification** on product spaces | certificates are coverings of a separator (lower) and of a path (upper); on the cube with a weight-dependent known part a lower certificate is a whole layer | SCI-MSG-0005 | theory |
| F3 | **Two-point robust quantities:** the exact robust range of the critical depth (spectral-gap exponent) | the upper end decouples; the lower end is a min–max over the polytope | SCI-MSG-0005 K-T4 | theory |
| F4 | **Effectiveness and size of tractable cuts for long chains** | 55–77 % of trap depths certified at 7–8 torsions; not monotone | SCI-MSG-0005 K-E1 | engineering |
| F5 | **A certified relaxed torsion scan on a real small molecule**, compared with a measured activation energy | format and soundness; the obstacle is that the energy is not pairwise in torsions | SCI-MSG-0005 K-E2 | engineering + us |

## G. Rounds of adaptivity and the coding dictionary (workstreams R4, A1)

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| G1 | **Is `τ^{(3)} = h`?**  The value of `τ^{(2)}` in `[0.359a, 0.624a]` at slope 1; strict monotonicity in the number of rounds | the lower end cannot be raised with the twins of Theorem 11.86 (the lemma is tight on them up to a polynomial factor) | SCI-REV-0003 §10 | theory |
| G2 | **The two-round exponent of the block-radial class on two known blocks** | conjectured `max{h, ϑ(φ₁), ϑ(φ₂)}`; lower half proved | SCI-REV-0003 | theory |
| G3 | **A two-round algorithm with a non-uniform first batch**: does hedging over block splits and shells lower `0.624a`? | the lower bound is driven by the dilution of a uniform blind batch | SCI-REV-0003 | theory |
| G4 | **Is `θ₂*` the right cost at the flat-histogram instance?** | lower bound for expected cost there (Corollary R4.2) | SCI-REV-0003 | theory |
| G5 | **A certified finite-`n` separation**: rows of the twins table in interval arithmetic | floating-point exact sums to `n = 6400` | SCI-REV-0003 R4-E1 | engineering |
| G6 | **Does a law of the form `E_sp(θ) − θ` for an adaptive scheme exist in active hypothesis testing, controlled sensing or group testing?** | not found in 41 searches; those three literatures were not searched | SCI-RES-0003 | anyone with library access |
| G7 | **Strictness: is a product sampler strictly worse than the stratified sample on a biased cube below capacity?** | never better at the level of type-counting formulas, equal as `θ ↑ a`; strictness is the failure of a saddle point, unproved | SCI-RES-0003 §2 | theory |

## H. Linear-information classes (workstream X; `workstreams/SX_REPORT.md` §5)

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| H1 | **A sharp–soft decomposition with a verified kernel**: `min(f+g) ≥ (kernel-certified bound of f + ĝ_A) − B_A·p̄` with a checkable certificate for `max P_A ≤ p̄` | hypercircle band; bridge to the pairwise kernel for order two | SCI-MSG-0007 X-T1 | theory |
| H2 | **The exact complexity of `ln Z` over an ellipsoid** (a design theorem); is the Curie–Weiss matrix extremal at every `n` and Frobenius norm? | interval formula; asymptotics below the transition | SCI-MSG-0007 X-T3 | theory |
| H3 | **Randomised algorithms for order-2 ellipsoids**: a polylogarithmic algorithm or a lower bound of order `M` | additive case: independent of `n` at extensive accuracy | — | theory + us |
| H4 | **Cover format against span format on real chain geometry**; the slack `κ` of certified envelopes | toy chains only | SCI-MSG-0007 X-E1, X-E2 | engineering |
| H5 | **Is expectation data more robust to out-of-class remainders than evaluation data?**  Evaluation designs lose a Lebesgue constant against a sup-norm remainder; maximum-entropy refinement against averaged data loses none (Theorem 7) — but the two bounds concern different objects | an observation (`ALTERNATIVE_FRAMEWORKS.md` §5) | — | us |
| H6 | **What are averaged data worth in an ellipsoid class of order `m` when `k < m`?**  The two-oracle question between the polytope (nothing) and `k ≥ m` (everything) | ends only | — | us |
| H7 | **Adversary or noise?**  Whether the remainder of a real many-body term outside a pair-additive class behaves like an adversary (amplified) or like noise (averaged) | pilot: sup/RMS 4–8 | SCI-RES-0002 P-T2, P-T3 | us + engineering |

## I. From the reviews of theory report §§11.25, 11.26 (workstreams R1, R5)

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| I1 | **The middle slice.**  Is the adaptive exponent without a hint on `T_{n/2}` equal to `R_unif`?  It decides whether "an interaction without a field changes no exponent" is a matter of wording or of substance | bounds `[R_unif, θ_na^cube]`, i.e. `[0.0291, 0.1109]` at `u = 1` | SCI-REV-0001 T7, R1-E1 | theory; engineering |
| I2 | **The extremal site law**: `sup_π F*_π(t)` for the Hamming envelope on `q` letters | ceiling `t(1−t)u²/8`; a three-letter law above the two-letter cube at `u = 0.5` (by 0.03 %) | SCI-REV-0001 T5 | theory |
| I3 | **Zero field maximises pairwise mutual information in ferromagnets** | proved for three spins; no violation in 3 000 random ferromagnets; false with mixed signs | SCI-REV-0001 §5 | theory; us |
| I4 | **Concavity of the two-letter site function** (= concavity in `ρ` of `max_p E_0(ρ, p)` for binary-input binary-output channels) | true on 500 + earlier random sites | SCI-REV-0005 R5-T3 | theory |
| I5 | **The error term of the isoperimetric input** of §11.26 (proof: `n^{−1/(2q_max+2)}`; evidence `ln n/n`) and a first simulation of the nested algorithm beyond two letters | nothing simulated | SCI-REV-0005 R5-E1 | engineering |
| I6 | **The junction of Proposition 11.81(b)**: does it come earlier than `βJ*` at large slopes, as attributed to referee R10? | not reproduced by our reviewer up to 97 % of `βJ*`, `u ≤ 6` | SCI-REV-0001 §6 | theory (publish R10's report) |

